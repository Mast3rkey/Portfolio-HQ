"""Tests for intelligence_report.py (PI-0011 bounded Intelligence Operations V1).

All synthetic fixtures use fictional placeholder tickers ("ZZZZ", "ZZZY",
"ZZYY", "ZYYY", ...) — no real portfolio ticker, real company thesis, or
real investment judgment appears in any fixture. Tests that intentionally
read the real repository (`intelligence/companies/`, `intelligence/themes/`,
`targets.yaml`, `holdings.yaml`) do so read-only, to prove non-mutation and
to derive expected counts dynamically from the filesystem — never to assert
a hard-coded roster size.
"""

from __future__ import annotations

import ast
import importlib
import re
import textwrap
from datetime import date, datetime
from pathlib import Path

import pytest
import yaml

import intelligence_report as ir
import intelligence_validator as iv


# ── fixtures / helpers ─────────────────────────────────────────────────────

def _valid_company(**overrides) -> dict:
    """A structurally complete, fully synthetic company record — same shape
    convention as test_intelligence_validator.py's own _valid_company()."""
    base = {
        "sector": "Fictional Sector",
        "industry": "Fictional Industry",
        "portfolio_role_ref": "T1",
        "review": {
            "cadence_days": 90,
            "last_reviewed": "2026-01-01",
            "next_due": "2026-04-01",
        },
    }
    base.update(overrides)
    return base


def _write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False))


def _valid_theme(**overrides) -> dict:
    base = {
        "theme_id": overrides.get("theme_id", "zzzz_theme"),
        "description": "Fictional theme for testing.",
        "lifecycle": "Established",
        "review": {
            "cadence_days": 90,
            "last_reviewed": "2026-01-01",
            "next_due": "2026-04-01",
        },
    }
    base.update(overrides)
    return base


def _targets_stub(tiers: dict, **extra) -> dict:
    """A minimal targets.yaml-shaped stub. `extra` lets tests prove
    non-tier config (crypto/caps/gates/margin) is ignored."""
    data = {"tiers": tiers}
    data.update(extra)
    return data


# ── staleness: date-boundary tests ─────────────────────────────────────────

def test_overdue_review_strict_boundary(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    _write_yaml(d / "ZZZZ.yaml", _valid_company(review={
        "cadence_days": 90, "last_reviewed": "2026-01-01", "next_due": "2026-07-01",
    }))
    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert [o.ticker for o in findings.overdue_reviews] == ["ZZZZ"]
    assert findings.overdue_reviews[0].days_overdue == 18


def test_review_due_today_is_not_overdue(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    _write_yaml(d / "ZZZZ.yaml", _valid_company(review={
        "cadence_days": 90, "last_reviewed": "2026-01-01", "next_due": "2026-07-19",
    }))
    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert findings.overdue_reviews == ()


def test_review_in_future_is_not_overdue(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    _write_yaml(d / "ZZZZ.yaml", _valid_company(review={
        "cadence_days": 90, "last_reviewed": "2026-01-01", "next_due": "2026-08-01",
    }))
    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert findings.overdue_reviews == ()


# ── staleness: catalyst semantics ──────────────────────────────────────────

def test_catalyst_pending_and_lapsed_is_flagged(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    _write_yaml(d / "ZZZZ.yaml", _valid_company(catalysts=[
        {"catalyst": "made-up catalyst", "expected": "2026-06-01", "status": "pending"},
    ]))
    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert [c.ticker for c in findings.lapsed_catalysts] == ["ZZZZ"]
    assert findings.lapsed_catalysts[0].status == "pending"


def test_catalyst_non_pending_status_is_not_flagged_lapsed(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    _write_yaml(d / "ZZZZ.yaml", _valid_company(catalysts=[
        {"catalyst": "made-up catalyst", "expected": "2026-06-01", "status": "resolved"},
    ]))
    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert findings.lapsed_catalysts == ()
    assert findings.unable_to_evaluate == ()


def test_catalyst_in_future_is_not_flagged(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    _write_yaml(d / "ZZZZ.yaml", _valid_company(catalysts=[
        {"catalyst": "made-up catalyst", "expected": "2026-12-31", "status": "pending"},
    ]))
    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert findings.lapsed_catalysts == ()


# ── staleness: invalid vs. unable-to-evaluate ──────────────────────────────

def test_schema_invalid_file_goes_to_schema_invalid_only(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    # review missing required keys (cadence_days/last_reviewed) -> schema-invalid,
    # even though next_due alone would otherwise look overdue.
    _write_yaml(d / "ZZZZ.yaml", {"review": {"next_due": "2020-01-01"}})
    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert [i.ticker for i in findings.schema_invalid] == ["ZZZZ"]
    assert findings.overdue_reviews == ()
    assert findings.lapsed_catalysts == ()
    assert findings.unable_to_evaluate == ()


def test_schema_valid_but_unparseable_next_due(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    _write_yaml(d / "ZZZZ.yaml", _valid_company(review={
        "cadence_days": 90, "last_reviewed": "2026-01-01", "next_due": "not-a-date",
    }))
    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert findings.overdue_reviews == ()
    assert findings.schema_invalid == ()
    assert len(findings.unable_to_evaluate) == 1
    u = findings.unable_to_evaluate[0]
    assert u.ticker == "ZZZZ"
    assert u.field_name == "review.next_due"
    assert u.raw_value == "not-a-date"


def test_schema_valid_but_non_string_catalyst_status(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    _write_yaml(d / "ZZZZ.yaml", _valid_company(catalysts=[
        {"catalyst": "made-up catalyst", "expected": "2026-06-01", "status": 123},
    ]))
    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert findings.lapsed_catalysts == ()
    assert findings.schema_invalid == ()
    assert len(findings.unable_to_evaluate) == 1
    u = findings.unable_to_evaluate[0]
    assert u.ticker == "ZZZZ"
    assert "status" in u.field_name
    assert u.raw_value == 123


# ── staleness: missing review date is surfaced, never silently skipped ────

def test_no_review_key_at_all_is_unable_to_evaluate(tmp_path):
    """A validator-accepted company record with no `review:` key at all
    (review is optional per spec §9) must never be silently skipped —
    PI-0011 correction 2 requires an explicit Unable-to-evaluate finding,
    and it must never be classified as overdue."""
    d = tmp_path / "companies"
    d.mkdir()
    company = _valid_company()
    del company["review"]
    _write_yaml(d / "ZZZZ.yaml", company)

    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))

    assert findings.schema_invalid == ()  # still schema-valid: review is optional
    assert findings.overdue_reviews == ()  # never classified as overdue
    assert len(findings.unable_to_evaluate) == 1
    u = findings.unable_to_evaluate[0]
    assert u.ticker == "ZZZZ"
    assert u.field_name == "review.next_due"
    assert u.raw_value is None
    assert "missing" in u.reason.lower()


def test_review_explicit_null_is_unable_to_evaluate(tmp_path):
    """`review: null` is schema-valid (same as an absent key) but must be
    surfaced the same way — never silently skipped, never overdue."""
    d = tmp_path / "companies"
    d.mkdir()
    company = _valid_company()
    company["review"] = None
    _write_yaml(d / "ZZZZ.yaml", company)

    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))

    assert findings.schema_invalid == ()
    assert findings.overdue_reviews == ()
    assert len(findings.unable_to_evaluate) == 1
    u = findings.unable_to_evaluate[0]
    assert u.ticker == "ZZZZ"
    assert u.field_name == "review.next_due"
    assert u.raw_value is None


def test_review_missing_required_keys_stays_schema_invalid_not_unable_to_evaluate(tmp_path):
    """A `review:` mapping present but missing required keys
    (cadence_days/last_reviewed/next_due) is ALREADY schema-invalid under
    the existing, unmodified intelligence_validator.py — that verdict must
    be preserved exactly. It goes only to Schema-invalid, never to Unable
    to evaluate (no double-reporting of the same underlying problem)."""
    d = tmp_path / "companies"
    d.mkdir()
    _write_yaml(d / "ZZZZ.yaml", {"review": {"next_due": "2020-01-01"}})

    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))

    assert [i.ticker for i in findings.schema_invalid] == ["ZZZZ"]
    assert findings.unable_to_evaluate == ()
    assert findings.overdue_reviews == ()


# ── staleness: PyYAML-decoded date objects are accepted directly ──────────

def test_review_next_due_as_yaml_date_object_is_evaluated_normally(tmp_path):
    """PyYAML decodes an unquoted `next_due: 2026-07-01` into an actual
    datetime.date object, not a string. A valid date object must be
    evaluated normally (PI-0011 correction 3), not routed to
    Unable-to-evaluate."""
    d = tmp_path / "companies"
    d.mkdir()
    p = d / "ZZZZ.yaml"
    company = _valid_company(review={
        "cadence_days": 90, "last_reviewed": "2026-01-01", "next_due": date(2026, 7, 1),
    })
    p.write_text(yaml.safe_dump(company, sort_keys=False))

    # sanity: confirm the actual round trip through YAML really does
    # produce a date object, not a string, before evaluating the claim
    reloaded = yaml.safe_load(p.read_text())
    assert isinstance(reloaded["review"]["next_due"], date)
    assert not isinstance(reloaded["review"]["next_due"], str)

    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert findings.unable_to_evaluate == ()
    assert findings.schema_invalid == ()
    assert [o.ticker for o in findings.overdue_reviews] == ["ZZZZ"]
    assert findings.overdue_reviews[0].next_due == "2026-07-01"  # canonical ISO text, per correction 3


def test_catalyst_expected_as_yaml_date_object_is_evaluated_normally(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    p = d / "ZZZZ.yaml"
    company = _valid_company(catalysts=[
        {"catalyst": "made-up catalyst", "expected": date(2026, 6, 1), "status": "pending"},
    ])
    p.write_text(yaml.safe_dump(company, sort_keys=False))

    reloaded = yaml.safe_load(p.read_text())
    assert isinstance(reloaded["catalysts"][0]["expected"], date)

    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert findings.unable_to_evaluate == ()
    assert [c.ticker for c in findings.lapsed_catalysts] == ["ZZZZ"]
    assert findings.lapsed_catalysts[0].expected == "2026-06-01"


def test_review_next_due_as_full_datetime_is_unable_to_evaluate_not_truncated(tmp_path):
    """A full datetime.datetime timestamp (decoded from a YAML value that
    also carries a time component) must NOT be silently truncated to its
    calendar date — that would substitute an untested schema meaning.
    Narrowest implementation: treated as unable-to-evaluate instead."""
    d = tmp_path / "companies"
    d.mkdir()
    p = d / "ZZZZ.yaml"
    company = _valid_company(review={
        "cadence_days": 90, "last_reviewed": "2026-01-01",
        "next_due": datetime(2026, 7, 1, 10, 30),
    })
    p.write_text(yaml.safe_dump(company, sort_keys=False))

    reloaded = yaml.safe_load(p.read_text())
    assert isinstance(reloaded["review"]["next_due"], datetime)

    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert findings.overdue_reviews == ()
    assert len(findings.unable_to_evaluate) == 1
    assert findings.unable_to_evaluate[0].field_name == "review.next_due"


# ── staleness: deterministic ordering ──────────────────────────────────────

def test_staleness_deterministic_alphabetical_ordering(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    for ticker in ("ZZYY", "ZZZZ", "ZYYY"):
        _write_yaml(d / f"{ticker}.yaml", _valid_company(review={
            "cadence_days": 90, "last_reviewed": "2026-01-01", "next_due": "2020-01-01",
        }))
    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert [o.ticker for o in findings.overdue_reviews] == ["ZYYY", "ZZYY", "ZZZZ"]
    assert findings.companies_scanned == ("ZYYY", "ZZYY", "ZZZZ")


# ── staleness: empty states ─────────────────────────────────────────────────

def test_missing_companies_directory_is_valid_zero_state(tmp_path):
    findings = ir.collect_staleness_findings(tmp_path / "does_not_exist", as_of_date=date(2026, 7, 19))
    assert findings.companies_scanned == ()
    assert findings.overdue_reviews == ()
    text = ir.render_staleness_report(findings)
    assert "0 companies scanned" in text
    assert "No companies have an overdue review as of 2026-07-19." in text
    assert "No lapsed catalysts as of 2026-07-19." in text
    assert "Nothing flagged as unable to evaluate as of 2026-07-19." in text
    assert "No schema-invalid company records as of 2026-07-19." in text


def test_empty_companies_directory_is_valid_zero_state(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    assert findings.companies_scanned == ()
    text = ir.render_staleness_report(findings)
    assert "0 companies scanned" in text


def test_render_populated_report_contains_all_section_headers(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    _write_yaml(d / "ZZZZ.yaml", _valid_company())
    findings = ir.collect_staleness_findings(d, as_of_date=date(2026, 7, 19))
    text = ir.render_staleness_report(findings)
    for header in (
        "# Intelligence Staleness Report",
        "## Overdue company reviews",
        "## Lapsed pending catalysts",
        "## Unable to evaluate",
        "## Schema-invalid company records",
        "## Coverage note",
    ):
        assert header in text
    assert "_As of: 2026-07-19." in text
    assert "ZZZZ" in text  # coverage note lists the scanned ticker


# ── render: Markdown table-cell escaping (pipe / CR / newline) ────────────

def test_render_escapes_pipe_and_newlines_in_catalyst_label():
    """A human-authored catalyst label containing a pipe and embedded
    CRLF/LF must not break the Markdown table into extra columns or rows
    (PI-0011 correction 4) — output formatting only, no source-record
    change."""
    poison = "weird|pipe\r\nand\nnewlines"
    findings = ir.StalenessFindings(
        as_of_date=date(2026, 7, 19),
        companies_scanned=("ZZZZ",),
        lapsed_catalysts=(ir.LapsedCatalyst(
            ticker="ZZZZ", catalyst=poison, expected="2026-06-01",
            status="pending", days_overdue=5,
        ),),
    )
    text = ir.render_staleness_report(findings)

    assert "\r" not in text  # carriage returns never survive into the report
    matching_lines = [ln for ln in text.splitlines() if "weird" in ln]
    assert len(matching_lines) == 1  # the embedded newlines did not fragment this into extra lines
    row = matching_lines[0]
    assert row.startswith("|") and row.endswith("|")
    assert "\\|" in row  # the embedded pipe was escaped, not left as a raw column delimiter
    # exactly 5 columns -> 6 true delimiters; the escaped embedded pipe must
    # not be counted as a 7th delimiter
    unescaped_pipes = re.findall(r"(?<!\\)\|", row)
    assert len(unescaped_pipes) == 6


def test_render_escapes_pipe_and_newlines_in_validator_error_text():
    """A validator error message containing a pipe and embedded newline
    must not break the Schema-invalid table."""
    poison = "bad value|contains a pipe\r\nand a newline\nand another"
    findings = ir.StalenessFindings(
        as_of_date=date(2026, 7, 19),
        companies_scanned=("ZZZZ",),
        schema_invalid=(ir.SchemaInvalidRecord(ticker="ZZZZ", errors=(poison,)),),
    )
    text = ir.render_staleness_report(findings)

    assert "\r" not in text
    matching_lines = [ln for ln in text.splitlines() if "bad value" in ln]
    assert len(matching_lines) == 1
    row = matching_lines[0]
    assert row.startswith("|") and row.endswith("|")
    assert "\\|" in row
    # 2 columns -> 3 true delimiters
    unescaped_pipes = re.findall(r"(?<!\\)\|", row)
    assert len(unescaped_pipes) == 3


def test_render_escapes_pipe_in_unable_to_evaluate_reason_and_raw_value():
    findings = ir.StalenessFindings(
        as_of_date=date(2026, 7, 19),
        companies_scanned=("ZZZZ",),
        unable_to_evaluate=(ir.UnableToEvaluate(
            ticker="ZZZZ",
            field_name="review.next_due",
            raw_value="bad|value\nwith a break",
            reason="unparseable|reason\nwith a break",
        ),),
    )
    text = ir.render_staleness_report(findings)

    assert "\r" not in text
    matching_lines = [ln for ln in text.splitlines() if "unparseable" in ln]
    assert len(matching_lines) == 1
    row = matching_lines[0]
    assert row.startswith("|") and row.endswith("|")
    # 4 columns -> 5 true delimiters
    unescaped_pipes = re.findall(r"(?<!\\)\|", row)
    assert len(unescaped_pipes) == 5


# ── role-drift ──────────────────────────────────────────────────────────────

def test_role_drift_match(tmp_path):
    companies = tmp_path / "companies"
    companies.mkdir()
    _write_yaml(companies / "ZZZZ.yaml", _valid_company(portfolio_role_ref="T1"))
    targets = tmp_path / "targets.yaml"
    _write_yaml(targets, _targets_stub({"T1": {"weight_pct": 3.35, "tickers": ["ZZZZ"]}}))

    report = ir.check_portfolio_role_drift(companies, targets)
    assert report.checked == 1
    assert report.matched == 1
    assert report.mismatched == 0
    assert report.findings == ()


def test_role_drift_mismatch(tmp_path):
    companies = tmp_path / "companies"
    companies.mkdir()
    _write_yaml(companies / "ZZZZ.yaml", _valid_company(portfolio_role_ref="T2"))
    targets = tmp_path / "targets.yaml"
    _write_yaml(targets, _targets_stub({"T1": {"tickers": ["ZZZZ"]}}))

    report = ir.check_portfolio_role_drift(companies, targets)
    assert report.mismatched == 1
    assert report.findings[0].status == ir.ROLE_MISMATCH
    assert report.findings[0].portfolio_role_ref == "T2"
    assert report.findings[0].target_tiers == ("T1",)


def test_role_drift_not_in_targets(tmp_path):
    companies = tmp_path / "companies"
    companies.mkdir()
    _write_yaml(companies / "ZZZZ.yaml", _valid_company(portfolio_role_ref="band"))
    targets = tmp_path / "targets.yaml"
    _write_yaml(targets, _targets_stub({"T1": {"tickers": ["SOMETHINGELSE"]}}))

    report = ir.check_portfolio_role_drift(companies, targets)
    assert report.not_in_targets == 1
    assert report.findings[0].status == ir.ROLE_NOT_IN_TARGETS
    assert report.findings[0].target_tiers == ()


def test_role_drift_ambiguous_multiple_tier_membership(tmp_path):
    companies = tmp_path / "companies"
    companies.mkdir()
    _write_yaml(companies / "ZZZZ.yaml", _valid_company(portfolio_role_ref="T1"))
    targets = tmp_path / "targets.yaml"
    _write_yaml(targets, _targets_stub({
        "T1": {"tickers": ["ZZZZ"]},
        "T2": {"tickers": ["ZZZZ"]},
    }))

    report = ir.check_portfolio_role_drift(companies, targets)
    assert report.ambiguous == 1
    assert report.findings[0].status == ir.ROLE_AMBIGUOUS
    assert set(report.findings[0].target_tiers) == {"T1", "T2"}


def test_role_drift_ignores_non_tier_config(tmp_path):
    """crypto/caps/gates/margin blocks must never be treated as tier
    membership (PI-0011 scope: tiers.*.tickers only)."""
    companies = tmp_path / "companies"
    companies.mkdir()
    _write_yaml(companies / "ZZZZ.yaml", _valid_company(portfolio_role_ref="T1"))
    targets = tmp_path / "targets.yaml"
    _write_yaml(targets, _targets_stub(
        {"T1": {"tickers": ["SOMETHINGELSE"]}},
        crypto={"coins": ["ZZZZ"]},
        caps={"clusters": [{"name": "fake", "tickers": ["ZZZZ"]}]},
    ))

    report = ir.check_portfolio_role_drift(companies, targets)
    assert report.not_in_targets == 1  # crypto/caps membership must not count as a tier match


def test_role_drift_never_rewrites_either_source(tmp_path):
    companies = tmp_path / "companies"
    companies.mkdir()
    company_path = companies / "ZZZZ.yaml"
    _write_yaml(company_path, _valid_company(portfolio_role_ref="T2"))
    targets = tmp_path / "targets.yaml"
    _write_yaml(targets, _targets_stub({"T1": {"tickers": ["ZZZZ"]}}))

    before_company = company_path.read_bytes()
    before_targets = targets.read_bytes()

    report = ir.check_portfolio_role_drift(companies, targets)
    assert report.mismatched == 1  # sanity: the check actually ran and found the mismatch

    assert company_path.read_bytes() == before_company
    assert targets.read_bytes() == before_targets


def test_role_drift_missing_companies_directory_is_valid_zero_state(tmp_path):
    targets = tmp_path / "targets.yaml"
    _write_yaml(targets, _targets_stub({"T1": {"tickers": []}}))
    report = ir.check_portfolio_role_drift(tmp_path / "does_not_exist", targets)
    assert report.checked == 0
    assert report.findings == ()


# ── theme-reference results surfaced via public validator API only ────────

def test_broken_theme_reference_surfaced_via_public_validate_company_file(tmp_path):
    companies = tmp_path / "companies"
    companies.mkdir()
    themes = tmp_path / "themes"
    themes.mkdir()
    _write_yaml(companies / "ZZZZ.yaml", _valid_company(themes=["nonexistent_theme"]))

    rollup = ir.build_coverage_rollup(companies, themes)
    assert len(rollup.company_validation_errors) == 1
    ticker, errors = rollup.company_validation_errors[0]
    assert ticker == "ZZZZ"
    assert any("nonexistent_theme" in e for e in errors)
    # sanity: intelligence_validator's own function actually produced this,
    # not a reimplementation in intelligence_report.py.
    direct = iv.validate_company_file(companies / "ZZZZ.yaml")
    assert direct.errors == list(errors)


def test_theme_reverse_membership_rejected_via_public_validate_themes_directory(tmp_path):
    themes = tmp_path / "themes"
    themes.mkdir()
    _write_yaml(themes / "zzzz_theme.yaml", _valid_theme(companies=["ZZZZ"]))
    companies = tmp_path / "companies"
    companies.mkdir()

    rollup = ir.build_coverage_rollup(companies, themes)
    assert len(rollup.theme_validation_errors) == 1
    theme_id, errors = rollup.theme_validation_errors[0]
    assert theme_id == "zzzz_theme"
    assert any("companies" in e for e in errors)


# ── no private intelligence_validator symbol is imported or called ────────

_PUBLIC_VALIDATOR_API = {
    "validate_company_data",
    "validate_company_file",
    "validate_directory",
    "validate_theme_data",
    "validate_theme_file",
    "validate_themes_directory",
    "ValidationResult",
    "DirectoryValidationResult",
}


def test_no_private_intelligence_validator_symbol_used():
    with open(ir.__file__) as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "intelligence_validator":
            for alias in node.names:
                assert not alias.name.startswith("_"), (
                    f"private symbol imported from intelligence_validator: {alias.name}"
                )
        if isinstance(node, ast.Attribute):
            value = node.value
            if isinstance(value, ast.Name) and value.id == "_validator":
                assert not node.attr.startswith("_"), (
                    f"private intelligence_validator attribute accessed: _validator.{node.attr}"
                )
                assert node.attr in _PUBLIC_VALIDATOR_API, (
                    f"intelligence_validator attribute not in known public API: {node.attr}"
                )


# ── coverage: filesystem-derived, no hard-coding, no index/cache ──────────

def test_coverage_counts_are_derived_from_filesystem_not_hardcoded(tmp_path):
    companies = tmp_path / "companies"
    companies.mkdir()
    themes = tmp_path / "themes"
    themes.mkdir()
    for ticker in ("ZZZZ", "ZZZY", "ZZYY"):
        _write_yaml(companies / f"{ticker}.yaml", _valid_company())
        (companies / f"{ticker}.md").write_text("# fictional thesis\n")
    _write_yaml(themes / "zzzz_theme.yaml", _valid_theme())
    (themes / "zzzz_theme.md").write_text("# fictional theme narrative\n")

    rollup = ir.build_coverage_rollup(companies, themes)
    assert rollup.company_yaml_count == 3
    assert rollup.company_markdown_count == 3
    assert rollup.theme_yaml_count == 1
    assert rollup.theme_markdown_count == 1


def test_coverage_reports_company_theme_references(tmp_path):
    companies = tmp_path / "companies"
    companies.mkdir()
    themes = tmp_path / "themes"
    themes.mkdir()
    _write_yaml(themes / "zzzz_theme.yaml", _valid_theme())
    _write_yaml(companies / "ZZZZ.yaml", _valid_company(themes=["zzzz_theme"]))

    rollup = ir.build_coverage_rollup(companies, themes)
    assert rollup.company_theme_refs == (("ZZZZ", "zzzz_theme"),)


def test_coverage_creates_no_index_cache_or_new_file(tmp_path):
    companies = tmp_path / "companies"
    companies.mkdir()
    themes = tmp_path / "themes"
    themes.mkdir()
    _write_yaml(companies / "ZZZZ.yaml", _valid_company())

    before = set(tmp_path.rglob("*"))
    ir.build_coverage_rollup(companies, themes)
    after = set(tmp_path.rglob("*"))
    assert before == after


# ── renderer performs no filesystem I/O ────────────────────────────────────

def test_renderer_performs_no_filesystem_io(monkeypatch):
    def fail_write_text(self, *a, **k):
        pytest.fail("render_staleness_report must not write any file")

    def fail_open(*a, **k):
        pytest.fail("render_staleness_report must not open any file")

    monkeypatch.setattr(Path, "write_text", fail_write_text)
    monkeypatch.setattr("builtins.open", fail_open)

    findings = ir.StalenessFindings(as_of_date=date(2026, 7, 19), companies_scanned=("ZZZZ",))
    text = ir.render_staleness_report(findings)
    assert isinstance(text, str)
    assert "ZZZZ" in text


# ── writer: single fixed path, fails clearly, never auto-creates dirs ──────

def test_writer_writes_to_exact_approved_relative_path(tmp_path):
    (tmp_path / "intelligence" / "reports").mkdir(parents=True)
    output_path = ir.write_staleness_report("hello", tmp_path)
    assert output_path == tmp_path / "intelligence" / "reports" / "staleness_report.md"
    assert output_path.read_text() == "hello"


def test_writer_fails_clearly_when_report_directory_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        ir.write_staleness_report("hello", tmp_path)
    # nothing should have been created anywhere under tmp_path
    assert list(tmp_path.rglob("*")) == []


def test_only_write_staleness_report_writes_to_disk():
    """Static guarantee: no function other than write_staleness_report
    contains a write-mode open()/Path.write_text() call."""
    with open(ir.__file__) as f:
        source = f.read()
    tree = ast.parse(source)
    write_modes = {"w", "a", "x", "w+", "a+", "r+", "wb", "ab", "xb"}
    offending: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for inner in ast.walk(node):
                if isinstance(inner, ast.Call):
                    func = inner.func
                    name = getattr(func, "attr", None) or getattr(func, "id", None)
                    if name == "write_text":
                        offending.add(node.name)
                    if name == "open":
                        for arg in list(inner.args)[1:2] + inner.keywords:
                            value = arg.value if isinstance(arg, ast.keyword) else arg
                            if isinstance(value, ast.Constant) and value.value in write_modes:
                                offending.add(node.name)
    assert offending == {"write_staleness_report"}


def test_module_never_creates_directories():
    with open(ir.__file__) as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
            assert name not in ("mkdir", "makedirs"), f"unexpected directory-creation call: {ast.dump(node)}"


# ── import side effects ─────────────────────────────────────────────────────

def test_module_top_level_has_no_side_effecting_statements():
    """Importing intelligence_report.py must not generate or rewrite a
    report. Static proof: every top-level statement is an import, an
    assignment, a class/function definition, the module docstring, or the
    `if __name__ == "__main__":` guard — nothing else executes on import."""
    with open(ir.__file__) as f:
        source = f.read()
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.If):
            test = node.test
            is_main_guard = (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
            )
            assert is_main_guard, f"unexpected top-level if-statement: {ast.dump(node)}"
            continue
        if isinstance(node, ast.Expr):
            assert isinstance(node.value, ast.Constant), (
                f"unexpected top-level expression statement: {ast.dump(node)}"
            )
            continue
        assert isinstance(
            node, (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign, ast.FunctionDef, ast.ClassDef)
        ), f"unexpected top-level statement: {ast.dump(node)}"


def test_reimporting_module_does_not_touch_real_report_file():
    report_path = Path("intelligence/reports/staleness_report.md")
    before = report_path.read_bytes() if report_path.exists() else None
    importlib.reload(ir)
    after = report_path.read_bytes() if report_path.exists() else None
    assert before == after


# ── real-repository: derived counts, non-mutation, isolation ──────────────

def test_real_repository_coverage_matches_filesystem_glob():
    """Never hard-codes a roster size — derives expected counts from the
    filesystem at test time, so adding a properly governed company/theme
    record later does not break this test."""
    companies_dir = Path("intelligence/companies")
    themes_dir = Path("intelligence/themes")
    expected_company_yaml = len(list(companies_dir.glob("*.yaml")))
    expected_company_md = len(list(companies_dir.glob("*.md")))
    expected_theme_yaml = len(list(themes_dir.glob("*.yaml")))
    expected_theme_md = len(list(themes_dir.glob("*.md")))

    rollup = ir.build_coverage_rollup(companies_dir, themes_dir)

    assert rollup.company_yaml_count == expected_company_yaml
    assert rollup.company_markdown_count == expected_company_md
    assert rollup.theme_yaml_count == expected_theme_yaml
    assert rollup.theme_markdown_count == expected_theme_md
    assert rollup.company_validation_errors == ()
    assert rollup.theme_validation_errors == ()


def test_real_repository_role_drift_is_a_non_gating_smoke_test():
    """Role-drift findings (MISMATCH / NOT_IN_TARGETS /
    AMBIGUOUS_TARGET_MEMBERSHIP) are advisory human-review output, not a
    code invariant — PI-0011 requires this test to NEVER fail merely
    because the real portfolio currently has one (a role-drift finding is
    an expected, legitimate, time-varying state, not a bug). This test
    only asserts the scan's own internal consistency and non-mutation
    guarantees; it makes no assertion about *how many* (or whether zero)
    advisory findings currently exist."""
    companies_dir = Path("intelligence/companies")
    targets_path = Path("targets.yaml")
    before_targets = targets_path.read_bytes()
    before_companies = {p: p.read_bytes() for p in companies_dir.glob("*.yaml")}

    report = ir.check_portfolio_role_drift(companies_dir, targets_path)

    # the scan completed and its own internal counts are self-consistent
    assert report.checked == report.matched + report.mismatched + report.not_in_targets + report.ambiguous

    # every individually-listed finding is a real advisory state, never MATCH
    assert all(f.status != ir.ROLE_MATCH for f in report.findings)
    assert all(
        f.status in (ir.ROLE_MISMATCH, ir.ROLE_NOT_IN_TARGETS, ir.ROLE_AMBIGUOUS)
        for f in report.findings
    )

    # deterministic ordering
    tickers = [f.ticker for f in report.findings]
    assert tickers == sorted(tickers)

    # neither source was touched by running the check
    assert targets_path.read_bytes() == before_targets
    assert {p: p.read_bytes() for p in companies_dir.glob("*.yaml")} == before_companies


def test_real_repository_source_files_remain_byte_identical(tmp_path):
    protected = (
        list(Path("intelligence/companies").glob("*"))
        + list(Path("intelligence/themes").glob("*"))
        + [Path("targets.yaml"), Path("holdings.yaml")]
    )
    before = {p: p.read_bytes() for p in protected}

    ir.collect_staleness_findings(Path("intelligence/companies"), as_of_date=date(2026, 7, 19))
    ir.check_portfolio_role_drift(Path("intelligence/companies"), Path("targets.yaml"))
    ir.build_coverage_rollup(Path("intelligence/companies"), Path("intelligence/themes"))

    after = {p: p.read_bytes() for p in protected}
    assert before == after


# ── static import isolation, both directions ───────────────────────────────

def _imported_module_names(path: str) -> set[str]:
    with open(path) as f:
        tree = ast.parse(f.read())
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_intelligence_report_does_not_import_allocate_or_margin_state():
    names = _imported_module_names(ir.__file__)
    assert "allocate" not in names
    assert "margin_state" not in names


def test_allocate_does_not_import_intelligence_report():
    assert "intelligence_report" not in _imported_module_names("allocate.py")


def test_margin_state_does_not_import_intelligence_report():
    assert "intelligence_report" not in _imported_module_names("margin_state.py")


def test_run_portfolio_check_never_invokes_intelligence_report():
    with open("run_portfolio_check.sh") as f:
        source = f.read()
    assert "intelligence_report" not in source


# ── CLI: action group, --as-of combinations, exit codes ────────────────────

def test_cli_no_arguments_exits_2():
    with pytest.raises(SystemExit) as exc_info:
        ir.main([])
    assert exc_info.value.code == 2


def test_cli_mutually_exclusive_flags_rejected():
    with pytest.raises(SystemExit) as exc_info:
        ir.main(["--staleness", "--coverage"])
    assert exc_info.value.code == 2


def test_cli_as_of_invalid_with_role_drift_alone():
    with pytest.raises(SystemExit) as exc_info:
        ir.main(["--role-drift", "--as-of", "2026-07-19"])
    assert exc_info.value.code == 2


def test_cli_as_of_invalid_with_coverage_alone():
    with pytest.raises(SystemExit) as exc_info:
        ir.main(["--coverage", "--as-of", "2026-07-19"])
    assert exc_info.value.code == 2


def test_cli_as_of_bad_date_format_exits_2():
    with pytest.raises(SystemExit) as exc_info:
        ir.main(["--staleness", "--as-of", "not-a-date"])
    assert exc_info.value.code == 2


def test_cli_staleness_as_of_passed_through_and_writes_once(monkeypatch):
    captured = {}

    def fake_collect(companies_dir, as_of_date):
        captured["as_of_date"] = as_of_date
        return ir.StalenessFindings(as_of_date=as_of_date, companies_scanned=())

    def fake_write(text, root):
        captured["wrote"] = True
        return Path(root) / ir.STALENESS_REPORT_RELATIVE_PATH

    monkeypatch.setattr(ir, "collect_staleness_findings", fake_collect)
    monkeypatch.setattr(ir, "write_staleness_report", fake_write)

    rc = ir.main(["--staleness", "--as-of", "2026-08-01"])
    assert rc == 0
    assert captured["as_of_date"] == date(2026, 8, 1)
    assert captured["wrote"] is True


def test_cli_staleness_exit_1_on_genuine_write_failure(monkeypatch):
    monkeypatch.setattr(
        ir, "collect_staleness_findings",
        lambda d, a: ir.StalenessFindings(as_of_date=a, companies_scanned=()),
    )

    def raiser(text, root):
        raise FileNotFoundError("simulated approved-directory-missing failure")

    monkeypatch.setattr(ir, "write_staleness_report", raiser)
    rc = ir.main(["--staleness", "--as-of", "2026-07-19"])
    assert rc == 1


def test_cli_role_drift_alone_never_writes(monkeypatch):
    def fail_write(*a, **k):
        pytest.fail("write_staleness_report must not be called for --role-drift")

    monkeypatch.setattr(ir, "write_staleness_report", fail_write)
    monkeypatch.setattr(
        ir, "check_portfolio_role_drift",
        lambda c, t: ir.RoleDriftReport(0, 0, 0, 0, 0, ()),
    )
    rc = ir.main(["--role-drift"])
    assert rc == 0


def test_cli_coverage_alone_never_writes(monkeypatch):
    def fail_write(*a, **k):
        pytest.fail("write_staleness_report must not be called for --coverage")

    monkeypatch.setattr(ir, "write_staleness_report", fail_write)
    monkeypatch.setattr(
        ir, "build_coverage_rollup",
        lambda c, t: ir.CoverageRollup(0, 0, 0, 0, (), (), ()),
    )
    rc = ir.main(["--coverage"])
    assert rc == 0


def test_cli_all_runs_all_three_and_writes_exactly_once(monkeypatch):
    calls = {"staleness": 0, "role": 0, "coverage": 0, "write": 0}

    def fake_collect(d, a):
        calls["staleness"] += 1
        return ir.StalenessFindings(as_of_date=a, companies_scanned=())

    def fake_write(text, root):
        calls["write"] += 1
        return Path(root) / ir.STALENESS_REPORT_RELATIVE_PATH

    def fake_role(c, t):
        calls["role"] += 1
        return ir.RoleDriftReport(0, 0, 0, 0, 0, ())

    def fake_cov(c, t):
        calls["coverage"] += 1
        return ir.CoverageRollup(0, 0, 0, 0, (), (), ())

    monkeypatch.setattr(ir, "collect_staleness_findings", fake_collect)
    monkeypatch.setattr(ir, "write_staleness_report", fake_write)
    monkeypatch.setattr(ir, "check_portfolio_role_drift", fake_role)
    monkeypatch.setattr(ir, "build_coverage_rollup", fake_cov)

    rc = ir.main(["--all", "--as-of", "2026-07-19"])
    assert rc == 0
    assert calls == {"staleness": 1, "role": 1, "coverage": 1, "write": 1}
