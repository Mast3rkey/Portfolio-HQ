"""Tests for currentness_report.py.

Three layers:

  1. focused unit tests over SYNTHETIC fixtures written to tmp_path;
  2. real-corpus reconciliation tests that DERIVE every expected number from
     the live repository rather than hardcoding an audit's observed value;
  3. adversarial/boundary cases that must fail closed.

No fixture in this file contains a real account balance, share count, margin
debt, buffer, or brokerage identifier. Synthetic values only.
"""

from __future__ import annotations

import ast
import hashlib
import json
import shutil
from datetime import date, datetime
from pathlib import Path

import pytest
import yaml

import currentness_report as cr

REPO_ROOT = Path(__file__).resolve().parent
AS_OF = date(2026, 9, 16)


# ── synthetic fixture builders ────────────────────────────────────────────

def _company(next_due="2026-12-01", last_reviewed="2026-09-01", catalysts=None,
             extra=None):
    doc = {
        "schema_version": 1,
        "company": {"ticker": "ZZFAKE", "name": "Synthetic Test Co"},
        "review": {"cadence_days": 90, "last_reviewed": last_reviewed,
                   "next_due": next_due, "log": []},
    }
    if catalysts is not None:
        doc["catalysts"] = catalysts
    if extra:
        doc.update(extra)
    return doc


def _write(path: Path, doc) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False))
    return path


def _registry(rows):
    return {"schema_version": 1, "tickers": rows}


def _registry_row(ticker="ZZFAKE", enabled=False):
    return {"ticker": ticker, "company_record_authority": "TEST-0001",
            "enrollment_authority": "TEST-0001", "enrolled_at": "2026-01-01",
            "template_version": "v1", "filing_trigger_profile": "domestic_issuer_v1",
            "refresh_policy": "path_a_fixed_scope_v1", "monitoring_enabled": enabled}


def _checkpoint_row(ticker="ZZFAKE", status="pending", channels=None):
    return {"ticker": ticker, "checkpoint_status": status,
            "channels": channels if channels is not None else {},
            "established_by": None}


# ── 1. closed vocabularies and module hygiene ─────────────────────────────

def test_status_vocabulary_is_closed_and_exact():
    assert set(cr.STATUSES) == {
        "OK", "APPROACHING", "AT_LIMIT", "OVER_LIMIT", "UNAVAILABLE",
        "STALE", "UNVERIFIED", "DISCREPANCY"}


def test_repository_state_vocabulary_is_closed_and_exact():
    assert set(cr.REPOSITORY_STATE_VERDICTS) == {
        "REPOSITORY_STATE_CURRENT", "REPOSITORY_STATE_STALE",
        "PRIVATE_CURRENT_EVIDENCE_REQUIRED"}


@pytest.mark.parametrize("forbidden", [
    "buy", "sell", "trim", "hold_recommendation", "trade", "order",
    "target_change", "new_target_pct", "recommended_target_pct", "score",
    "composite", "rank", "ranking", "conviction", "signal", "action",
])
def test_report_exposes_no_recommendation_field(forbidden):
    """No key anywhere in the emitted document may be a trade/target-change
    or scoring field. Walks the whole serialised tree, not just the top."""
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    seen: list[str] = []

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                seen.append(str(key))
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(report.as_dict())
    assert forbidden not in {k.lower() for k in seen}


def test_production_allocator_does_not_import_this_report():
    """One-way dependency. allocate.py must never import currentness_report."""
    tree = ast.parse((REPO_ROOT / "allocate.py").read_text())
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert "currentness_report" not in imported


def test_intelligence_report_and_allocate_remain_mutually_unaware():
    """This module importing both must not create an import relationship
    between them (PI-0011 boundary)."""
    for source, other in (("intelligence_report.py", "allocate"),
                          ("allocate.py", "intelligence_report")):
        tree = ast.parse((REPO_ROOT / source).read_text())
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module.split(".")[0])
        assert other not in names, f"{source} unexpectedly imports {other}"


def test_module_performs_no_write_capable_call():
    """Static AST proof: no write-mode open(), and no filesystem-mutating
    method call anywhere in this module. Substring matching would be fragile;
    this inspects the actual call nodes."""
    tree = ast.parse((REPO_ROOT / "currentness_report.py").read_text())
    mutating_methods = {"write_text", "write_bytes", "mkdir", "unlink", "rmdir",
                        "touch", "rename", "replace", "chmod", "symlink_to",
                        "hardlink_to", "writelines"}
    offenders: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id == "open":
            mode = None
            if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
                mode = node.args[1].value
            for kw in node.keywords:
                if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                    mode = kw.value.value
            if mode is not None and any(ch in str(mode) for ch in ("w", "a", "x", "+")):
                offenders.append(f"open(mode={mode!r}) at line {node.lineno}")
        if isinstance(func, ast.Attribute):
            # `str.replace` is not a filesystem call; only flag it on a Path-ish
            # receiver, which this module never builds for mutation anyway.
            if func.attr in mutating_methods and func.attr != "replace":
                offenders.append(f".{func.attr}() at line {node.lineno}")
    assert not offenders, f"write-capable calls present: {offenders}"


def test_module_declares_no_write_destination_constant():
    """intelligence_report.py owns the one approved write destination. This
    module must declare none of its own."""
    source = (REPO_ROOT / "currentness_report.py").read_text()
    assert "STALENESS_REPORT_RELATIVE_PATH" not in source


FORBIDDEN_PATHS = (
    "allocate.py", "levels.py", "margin_state.py", "alpaca_client.py",
    "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
    "intelligence_report.py", "freshness_validator.py", "freshness_state.py",
    "freshness_identity.py", "freshness_cadence.py",
    "portfolio_hq/owner/private_allocation.py",
    "portfolio_hq/owner/account_staging.py",
    "intelligence/reports/staleness_report.md",
    "intelligence/freshness_registry.yaml",
    "intelligence/freshness_checkpoints.yaml",
    "governance/decisions.yaml", "operations/WORKSTREAMS.yaml",
)


def _digests(paths):
    out = {}
    for rel in paths:
        p = REPO_ROOT / rel
        if p.exists():
            out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def test_building_the_report_mutates_no_forbidden_path():
    """Scope safety: importing and running this diagnostic leaves every
    forbidden production/config/governance path byte-identical."""
    before = _digests(FORBIDDEN_PATHS)
    assert before, "expected at least one forbidden path to exist"
    cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    cr.render(cr.build_report(root=REPO_ROOT, as_of=AS_OF))
    after = _digests(FORBIDDEN_PATHS)
    assert before == after


def test_intelligence_tree_is_not_mutated_by_a_report_run():
    """No Company/Theme/classification/valuation record may change."""
    tracked = sorted(
        str(p.relative_to(REPO_ROOT))
        for p in (REPO_ROOT / "intelligence").rglob("*.yaml"))
    before = _digests(tracked)
    cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    assert before == _digests(tracked)


def test_no_new_file_appears_under_intelligence_after_a_run():
    before = {p for p in (REPO_ROOT / "intelligence").rglob("*") if p.is_file()}
    cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    after = {p for p in (REPO_ROOT / "intelligence").rglob("*") if p.is_file()}
    assert before == after


# ── 2. strict numeric handling ────────────────────────────────────────────

@pytest.mark.parametrize("bad", [True, False])
def test_boolean_is_never_accepted_as_a_percentage(bad):
    value, reason = cr._checked_pct(bad, "synthetic")
    assert value is None and "boolean" in reason


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_percentage_rejected(bad):
    value, reason = cr._checked_pct(bad, "synthetic")
    assert value is None and "finite" in reason


@pytest.mark.parametrize("bad", ["3.0", None, [], {}])
def test_non_numeric_percentage_rejected(bad):
    value, reason = cr._checked_pct(bad, "synthetic")
    assert value is None and "real number" in reason


def test_negative_percentage_rejected_when_a_minimum_is_required():
    value, reason = cr._checked_pct(-0.01, "synthetic", minimum=0.0)
    assert value is None and ">= 0.0" in reason
    assert cr._checked_pct(-0.01, "synthetic") == (-0.01, None)


def test_real_numbers_accepted():
    assert cr._checked_pct(6, "x") == (6.0, None)
    assert cr._checked_pct(2.25, "x") == (2.25, None)


def test_boolean_target_pct_in_config_is_unavailable_not_a_crash(tmp_path):
    """allocate.build_roster coerces True -> 1.0 (bool subclasses int); this
    diagnostic refuses the raw value before that coercion can hide it, and does
    so as controlled UNAVAILABLE so one bad row cannot abort the whole report."""
    targets = {"destination": [{"ticker": "ZZFAKE", "target_pct": True,
                                "asset_class": "equity"}],
               "caps": {"clusters": []}}
    _write(tmp_path / "targets.yaml", targets)
    _write(tmp_path / "issuer_lookthrough.yaml",
           {"issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0, "issuers": []})
    result = cr.collect_target_weight_concentration(
        targets_path=tmp_path / "targets.yaml",
        lookthrough_path=tmp_path / "issuer_lookthrough.yaml")
    assert result.available is False
    assert result.status == cr.UNAVAILABLE
    assert "boolean" in result.detail
    assert result.clusters == () and result.issuers == () and result.common_driver is None


# ── 3. overdue boundary and catalyst semantics ────────────────────────────

def test_next_due_equal_to_as_of_is_not_overdue(tmp_path):
    """The existing strict rule is `next_due < as_of`. Equality is NOT overdue."""
    d = tmp_path / "companies"
    _write(d / "ZZFAKE.yaml", _company(next_due="2026-09-16"))
    result = cr.collect_company_currentness(companies_dir=d, as_of_date=AS_OF)
    assert result.overdue_count == 0
    assert result.records[0].overdue is False


def test_next_due_one_day_before_as_of_is_overdue(tmp_path):
    d = tmp_path / "companies"
    _write(d / "ZZFAKE.yaml", _company(next_due="2026-09-15"))
    result = cr.collect_company_currentness(companies_dir=d, as_of_date=AS_OF)
    assert result.overdue_count == 1
    assert result.records[0].days_overdue == 1
    assert result.records[0].status == cr.STALE


def test_future_next_due_is_not_overdue(tmp_path):
    d = tmp_path / "companies"
    _write(d / "ZZFAKE.yaml", _company(next_due="2027-01-01"))
    result = cr.collect_company_currentness(companies_dir=d, as_of_date=AS_OF)
    assert result.overdue_count == 0


def test_future_last_reviewed_is_flagged_as_an_anomaly(tmp_path):
    d = tmp_path / "companies"
    _write(d / "ZZFAKE.yaml", _company(last_reviewed="2027-05-05", next_due="2027-08-05"))
    result = cr.collect_company_currentness(companies_dir=d, as_of_date=AS_OF)
    row = result.records[0]
    assert any("future" in a for a in row.anomalies)
    assert row.status == cr.UNVERIFIED


def test_next_due_before_last_reviewed_is_flagged(tmp_path):
    d = tmp_path / "companies"
    _write(d / "ZZFAKE.yaml", _company(last_reviewed="2026-09-01", next_due="2026-08-01"))
    result = cr.collect_company_currentness(companies_dir=d, as_of_date=AS_OF)
    assert any("precedes" in a for a in result.records[0].anomalies)


def test_lapsed_pending_catalyst_detected(tmp_path):
    d = tmp_path / "companies"
    _write(d / "ZZFAKE.yaml", _company(catalysts=[
        {"catalyst": "synthetic quarterly result", "expected": "2026-08-01",
         "status": "pending"}]))
    result = cr.collect_company_currentness(companies_dir=d, as_of_date=AS_OF)
    assert result.total_lapsed_catalysts == 1
    assert result.records_with_lapsed_catalysts == 1
    assert result.lapsed_catalysts[0].days_overdue == 46
    assert result.records[0].status == cr.UNVERIFIED


def test_non_pending_lapsed_catalyst_is_not_counted(tmp_path):
    d = tmp_path / "companies"
    _write(d / "ZZFAKE.yaml", _company(catalysts=[
        {"catalyst": "synthetic", "expected": "2026-08-01", "status": "resolved"}]))
    result = cr.collect_company_currentness(companies_dir=d, as_of_date=AS_OF)
    assert result.total_lapsed_catalysts == 0


def test_future_pending_catalyst_is_not_lapsed(tmp_path):
    d = tmp_path / "companies"
    _write(d / "ZZFAKE.yaml", _company(catalysts=[
        {"catalyst": "synthetic", "expected": "2027-01-01", "status": "pending"}]))
    result = cr.collect_company_currentness(companies_dir=d, as_of_date=AS_OF)
    assert result.total_lapsed_catalysts == 0


def test_record_without_catalysts_is_reported_not_treated_as_clean(tmp_path):
    d = tmp_path / "companies"
    _write(d / "ZZFAKE.yaml", _company())
    result = cr.collect_company_currentness(companies_dir=d, as_of_date=AS_OF)
    assert result.records_without_catalysts == 1
    assert result.records[0].catalysts_present is False
    assert result.records[0].status == cr.UNVERIFIED


def test_malformed_catalyst_date_is_unevaluable_not_silently_clean(tmp_path):
    d = tmp_path / "companies"
    _write(d / "ZZFAKE.yaml", _company(catalysts=[
        {"catalyst": "synthetic", "expected": "not-a-date", "status": "pending"}]))
    result = cr.collect_company_currentness(companies_dir=d, as_of_date=AS_OF)
    assert result.total_lapsed_catalysts == 0
    assert result.records[0].unevaluable_field_count >= 1
    assert result.records[0].status == cr.UNVERIFIED


def test_empty_companies_directory_is_zero_coverage_not_an_error(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    result = cr.collect_company_currentness(companies_dir=d, as_of_date=AS_OF)
    assert result.record_count == 0
    assert result.status == cr.OK


def test_canonical_coverage_gap_is_reported(tmp_path):
    d = tmp_path / "companies"
    _write(d / "ZZFAKE.yaml", _company())
    result = cr.collect_company_currentness(
        companies_dir=d, canonical_equities=("ZZFAKE", "ZZMISSING"), as_of_date=AS_OF)
    assert result.canonical_covered == ("ZZFAKE",)
    assert result.canonical_uncovered == ("ZZMISSING",)
    assert result.status == cr.UNVERIFIED


def test_not_overdue_is_explicitly_not_declared_current(tmp_path):
    d = tmp_path / "companies"
    _write(d / "ZZFAKE.yaml", _company(next_due="2027-01-01", catalysts=[
        {"catalyst": "synthetic", "expected": "2027-01-01", "status": "pending"}]))
    result = cr.collect_company_currentness(companies_dir=d, as_of_date=AS_OF)
    assert result.overdue_count == 0
    assert any("not thereby current" in n.lower() for n in result.notes)


# ── 4. freshness monitor status ───────────────────────────────────────────

def test_disabled_monitoring_and_pending_checkpoint_report_unverified(tmp_path):
    reg = _write(tmp_path / "registry.yaml", _registry([_registry_row(enabled=False)]))
    chk = _write(tmp_path / "checkpoints.yaml", _registry([_checkpoint_row(status="pending")]))
    result = cr.collect_freshness_monitor_status(registry_path=reg, checkpoints_path=chk)
    assert result.enrolled_count == 1
    assert result.monitoring_enabled_count == 0
    assert result.verified_checkpoint_count == 0
    assert result.pending_or_unverified_count == 1
    assert result.rows[0].derived_state == "unverified"
    assert result.rows[0].status == cr.UNVERIFIED
    assert result.operational_event_monitoring_exists is False
    assert result.cadence_mechanism_exists is True
    assert result.status == cr.UNVERIFIED


def test_enabled_and_verified_row_is_still_unverified_without_a_monitor_record(tmp_path):
    """Existing spec-§9 precedence: `monitor_record_exists is False` forces
    `unverified` regardless of enrollment or checkpoint state. This repository
    has no monitor-run record surface at all, so `current` is UNREACHABLE by
    construction — the report must not paper over that."""
    reg = _write(tmp_path / "registry.yaml", _registry([_registry_row(enabled=True)]))
    chk = _write(tmp_path / "checkpoints.yaml",
                 _registry([_checkpoint_row(status="verified")]))
    result = cr.collect_freshness_monitor_status(registry_path=reg, checkpoints_path=chk)
    assert result.rows[0].monitoring_enabled is True
    assert result.rows[0].checkpoint_status == "verified"
    assert result.rows[0].derived_state == "unverified"
    assert result.rows[0].status == cr.UNVERIFIED
    assert result.operational_event_monitoring_exists is False


def test_current_state_is_unreachable_from_repository_evidence(tmp_path):
    """No repository path can produce `operational_event_monitoring_exists`."""
    reg = _write(tmp_path / "registry.yaml", _registry([
        _registry_row("ZZA", enabled=True), _registry_row("ZZB", enabled=False)]))
    chk = _write(tmp_path / "checkpoints.yaml", _registry([
        _checkpoint_row("ZZA", status="verified"),
        _checkpoint_row("ZZB", status="pending")]))
    result = cr.collect_freshness_monitor_status(registry_path=reg, checkpoints_path=chk)
    assert all(r.derived_state != "current" for r in result.rows)
    assert result.operational_event_monitoring_exists is False
    assert "unreachable" in result.notes[0]


def test_missing_checkpoint_row_is_unavailable_not_current(tmp_path):
    reg = _write(tmp_path / "registry.yaml", _registry([_registry_row(enabled=True)]))
    chk = _write(tmp_path / "checkpoints.yaml", _registry([]))
    result = cr.collect_freshness_monitor_status(registry_path=reg, checkpoints_path=chk)
    assert result.rows[0].checkpoint_present is False
    assert result.rows[0].derived_state is None
    assert result.rows[0].status == cr.UNAVAILABLE
    assert result.operational_event_monitoring_exists is False


def test_malformed_monitoring_flag_is_unavailable(tmp_path):
    row = _registry_row()
    row["monitoring_enabled"] = "yes"
    reg = _write(tmp_path / "registry.yaml", _registry([row]))
    chk = _write(tmp_path / "checkpoints.yaml", _registry([_checkpoint_row()]))
    result = cr.collect_freshness_monitor_status(registry_path=reg, checkpoints_path=chk)
    assert result.rows[0].monitoring_enabled is None
    assert result.rows[0].status == cr.UNAVAILABLE
    assert "boolean" in result.rows[0].detail


def test_duplicate_registry_ticker_identity_is_reported(tmp_path):
    reg = _write(tmp_path / "registry.yaml",
                 _registry([_registry_row("ZZFAKE"), _registry_row("ZZFAKE")]))
    chk = _write(tmp_path / "checkpoints.yaml", _registry([_checkpoint_row("ZZFAKE")]))
    result = cr.collect_freshness_monitor_status(registry_path=reg, checkpoints_path=chk)
    assert result.duplicate_tickers == ("ZZFAKE",)
    assert result.status == cr.UNVERIFIED


def test_unreadable_freshness_files_fail_closed(tmp_path):
    result = cr.collect_freshness_monitor_status(
        registry_path=tmp_path / "absent.yaml",
        checkpoints_path=tmp_path / "also-absent.yaml")
    assert result.enrolled_count == 0
    assert result.schema_valid is False
    assert result.operational_event_monitoring_exists is False
    assert result.status == cr.UNVERIFIED


# ── 5. committed staleness-report health ──────────────────────────────────

def test_committed_report_stale_by_date_and_scope(tmp_path):
    p = tmp_path / "staleness_report.md"
    p.write_text("# Intelligence Staleness Report\n_As of: 2026-07-20._\n\n"
                 "## Coverage note\n7 companies scanned: A, B.\n")
    result = cr.inspect_committed_staleness_report(
        report_path=p, current_company_count=53, as_of_date=AS_OF)
    assert result.as_of_date == "2026-07-20"
    assert result.companies_scanned_claim == 7
    assert result.status == cr.STALE
    assert "58d" in result.detail
    assert "53 records exist now" in result.detail


def test_committed_report_agreeing_is_ok(tmp_path):
    p = tmp_path / "staleness_report.md"
    p.write_text("_As of: 2026-09-16._\n\n4 companies scanned: A.\n")
    result = cr.inspect_committed_staleness_report(
        report_path=p, current_company_count=4, as_of_date=AS_OF)
    assert result.status == cr.OK


def test_missing_committed_report_is_unavailable(tmp_path):
    result = cr.inspect_committed_staleness_report(
        report_path=tmp_path / "nope.md", current_company_count=3, as_of_date=AS_OF)
    assert result.present is False
    assert result.status == cr.UNAVAILABLE


def test_committed_report_is_never_rewritten(tmp_path):
    p = tmp_path / "staleness_report.md"
    original = "_As of: 2026-07-20._\n\n7 companies scanned: A.\n"
    p.write_text(original)
    cr.inspect_committed_staleness_report(
        report_path=p, current_company_count=53, as_of_date=AS_OF)
    assert p.read_text() == original


# ── 6. target-weight concentration ────────────────────────────────────────

def _synthetic_policy(tmp_path, *, clusters=None, issuers=None, retained=None,
                      destination=None):
    targets = {
        "destination": destination if destination is not None else [
            {"ticker": "ZZA", "target_pct": 10.0, "asset_class": "equity"},
            {"ticker": "ZZB", "target_pct": 5.0, "asset_class": "equity"},
            {"ticker": "ZZFUND", "target_pct": 20.0, "asset_class": "fund"},
        ],
        "caps": {"clusters": clusters if clusters is not None else []},
    }
    lookthrough = {"issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
                   "issuers": issuers if issuers is not None else []}
    if retained is not None:
        lookthrough["retained_common_driver_measurement"] = retained
    t = _write(tmp_path / "targets.yaml", targets)
    l = _write(tmp_path / "issuer_lookthrough.yaml", lookthrough)
    return t, l


def test_cluster_utilisation_and_headroom(tmp_path):
    t, l = _synthetic_policy(tmp_path, clusters=[
        {"name": "zzcluster", "pct": 25.0, "tickers": ["ZZA", "ZZB"]}])
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    c = result.clusters[0]
    assert c.target_exposure_pct == pytest.approx(15.0)
    assert c.utilisation_pct == pytest.approx(60.0)
    assert c.headroom_pct == pytest.approx(10.0)
    assert c.status == cr.OK


def test_empty_cluster_is_unavailable_not_ok(tmp_path):
    t, l = _synthetic_policy(tmp_path, clusters=[
        {"name": "zzdead", "pct": 20.0, "tickers": []}])
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    c = result.clusters[0]
    assert c.status == cr.UNAVAILABLE
    assert "dead configuration" in c.detail
    assert c.status != cr.OK


def test_cluster_over_limit(tmp_path):
    t, l = _synthetic_policy(tmp_path, clusters=[
        {"name": "zztight", "pct": 10.0, "tickers": ["ZZA", "ZZB"]}])
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    assert result.clusters[0].status == cr.OVER_LIMIT
    assert result.status == cr.OVER_LIMIT


def test_cluster_exactly_at_limit(tmp_path):
    t, l = _synthetic_policy(tmp_path, clusters=[
        {"name": "zzexact", "pct": 15.0, "tickers": ["ZZA", "ZZB"]}])
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    assert result.clusters[0].status == cr.AT_LIMIT


def test_cluster_approaching_limit(tmp_path):
    t, l = _synthetic_policy(tmp_path, clusters=[
        {"name": "zznear", "pct": 16.0, "tickers": ["ZZA", "ZZB"]}])
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    assert result.clusters[0].status == cr.APPROACHING


def test_cluster_member_absent_from_roster_is_disclosed(tmp_path):
    t, l = _synthetic_policy(tmp_path, clusters=[
        {"name": "zzpartial", "pct": 25.0, "tickers": ["ZZA", "ZZGHOST"]}])
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    assert "ZZGHOST" in result.clusters[0].detail


def test_issuer_exposure_uses_the_production_helper(tmp_path):
    """Direct + embedded must equal what allocate._issuer_exposure produces for
    the same target-weight basis — proving reuse rather than reimplementation."""
    import allocate
    issuers = [{"ticker": "ZZA", "funds": [{"fund": "ZZFUND", "fund_holding_weight": 0.10}]}]
    t, l = _synthetic_policy(tmp_path, issuers=issuers)
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    lookthrough = yaml.safe_load(Path(l).read_text())
    expected = allocate._issuer_exposure({"ZZA": 10.0, "ZZB": 5.0, "ZZFUND": 20.0},
                                         100.0, lookthrough)
    row = result.issuers[0]
    assert row.direct_pct == pytest.approx(expected["issuers"]["ZZA"]["direct_pct"])
    assert row.embedded_pct == pytest.approx(expected["issuers"]["ZZA"]["embedded_pct"])
    assert row.effective_pct == pytest.approx(expected["issuers"]["ZZA"]["effective_pct"])
    assert result.common_driver.recomputed_pct == pytest.approx(
        expected["common_driver_current_pct"])


def test_issuer_with_no_fund_mapping_has_zero_embedded(tmp_path):
    t, l = _synthetic_policy(tmp_path, issuers=[{"ticker": "ZZA", "funds": []}])
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    row = result.issuers[0]
    assert row.embedded_pct == pytest.approx(0.0)
    assert row.effective_pct == pytest.approx(10.0)


def test_issuer_over_ceiling_flagged(tmp_path):
    t, l = _synthetic_policy(tmp_path, issuers=[
        {"ticker": "ZZA", "funds": [{"fund": "ZZFUND", "fund_holding_weight": 0.50}]}])
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    assert result.issuers[0].status == cr.OVER_LIMIT
    assert result.max_issuer.ticker == "ZZA"


def test_retained_measurement_reconciling_is_not_a_discrepancy(tmp_path):
    issuers = [{"ticker": "ZZA", "funds": []}]
    t, l = _synthetic_policy(tmp_path, issuers=issuers,
                             retained={"value_pct": 10.0, "measured_at": "2026-01-01"})
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    d = result.common_driver
    assert d.recomputed_pct == pytest.approx(10.0)
    assert d.reconciles is True
    assert d.discrepancy_flag is None
    assert d.status != cr.DISCREPANCY


def test_falsified_retained_measurement_raises_discrepancy(tmp_path):
    """Adversarial: a retained value that does not match recomputation must be
    surfaced with BOTH values, and must not overwrite the retained figure."""
    issuers = [{"ticker": "ZZA", "funds": []}]
    t, l = _synthetic_policy(tmp_path, issuers=issuers,
                             retained={"value_pct": 3.0, "measured_at": "2026-01-01"})
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    d = result.common_driver
    assert d.discrepancy_flag == cr.RETAINED_MEASUREMENT_DISCREPANCY
    assert d.status == cr.DISCREPANCY
    assert d.retained_value_pct == pytest.approx(3.0)
    assert d.recomputed_pct == pytest.approx(10.0)
    assert d.retained_delta_pct == pytest.approx(7.0)
    # the retained figure on disk is untouched
    assert yaml.safe_load(Path(l).read_text())[
        "retained_common_driver_measurement"]["value_pct"] == 3.0


def test_discrepancy_does_not_hide_the_ceiling_verdict(tmp_path):
    """status may be DISCREPANCY while the ceiling itself is breached; the
    ceiling verdict must remain independently machine-readable."""
    issuers = [{"ticker": "ZZA", "funds": [{"fund": "ZZFUND", "fund_holding_weight": 2.0}]}]
    t, l = _synthetic_policy(tmp_path, issuers=issuers,
                             retained={"value_pct": 1.0, "measured_at": "2026-01-01"})
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    d = result.common_driver
    assert d.status == cr.DISCREPANCY
    assert d.limit_status == cr.OVER_LIMIT
    assert result.status == cr.OVER_LIMIT


def test_boolean_retained_measurement_is_not_parsed_as_a_number(tmp_path):
    t, l = _synthetic_policy(tmp_path, issuers=[{"ticker": "ZZA", "funds": []}],
                             retained={"value_pct": True, "measured_at": "2026-01-01"})
    result = cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)
    assert result.common_driver.retained_value_pct is None
    assert result.common_driver.reconciles is None


def test_unreadable_policy_is_unavailable_not_zero(tmp_path):
    result = cr.collect_target_weight_concentration(
        targets_path=tmp_path / "absent.yaml",
        lookthrough_path=tmp_path / "absent2.yaml")
    assert result.available is False
    assert result.status == cr.UNAVAILABLE
    assert result.clusters == ()
    assert result.common_driver is None


# ── 7. repository account state and the private-evidence boundary ─────────

def _holdings(cash_date="2026-09-16", margin_date="2026-09-16", debt=0.0):
    # All THREE position tracks are declared explicitly. An omitted track is
    # an undeclared track, not an empty one, and would now (correctly) block on
    # the declaration gate — which would silently turn every fixture built on
    # this helper into a vacuous pass for whatever it was actually written to
    # test. See test_a_missing_position_track_is_not_an_empty_one.
    return {"shares": {}, "crypto_shares": {}, "holdings": {},
            "cash": {"balance": 1000.0, "synced_at": cash_date},
            "margin": {"debt": debt, "buffer_pct": 100.0, "synced_at": margin_date}}


def test_stale_repository_state_is_never_labeled_current(tmp_path):
    p = _write(tmp_path / "holdings.yaml",
               _holdings(cash_date="2026-08-01", margin_date="2026-07-31"))
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.verdict == cr.REPOSITORY_STATE_STALE
    assert state.verdict != cr.REPOSITORY_STATE_CURRENT
    assert state.dollars_from_repository_state is False
    assert state.blocked_by


def test_fresh_repository_state_is_current(tmp_path):
    p = _write(tmp_path / "holdings.yaml", _holdings())
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.verdict == cr.REPOSITORY_STATE_CURRENT
    assert state.dollars_from_repository_state is True


def test_historical_zero_debt_is_never_reported_as_current_margin_usage(tmp_path):
    """Adversarial: stale margin observation carrying debt 0.0 must NOT be
    reported as 'the account currently has no margin'."""
    p = _write(tmp_path / "holdings.yaml",
               _holdings(cash_date="2026-08-01", margin_date="2026-07-31", debt=0.0))
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.margin_usage_statement == cr.MARGIN_USAGE_UNAVAILABLE
    assert "unavailable from repository-only evidence" in state.margin_usage_statement
    blob = json.dumps(state.as_dict()).lower()
    for claim in ("zero margin", "no margin is", "currently carries no margin,",
                  "margin usage: 0", "margin_usage_pct"):
        assert claim not in blob


def test_even_fresh_repository_state_does_not_assert_current_margin_usage(tmp_path):
    p = _write(tmp_path / "holdings.yaml", _holdings(debt=0.0))
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.verdict == cr.REPOSITORY_STATE_CURRENT
    assert state.margin_usage_statement == cr.MARGIN_USAGE_UNAVAILABLE


def test_unreadable_holdings_fails_closed(tmp_path):
    state = cr.collect_repository_account_state(holdings_path=tmp_path / "absent.yaml")
    assert state.verdict == cr.PRIVATE_CURRENT_EVIDENCE_REQUIRED
    assert state.dollars_from_repository_state is False
    assert state.margin_usage_statement == cr.MARGIN_USAGE_UNAVAILABLE


def test_private_evidence_capability_reported_without_reading_private_evidence():
    cap = cr.detect_private_evidence_capability()
    assert cap.available is True
    assert cap.module == "portfolio_hq.owner.private_allocation"
    assert cap.entrypoint == "run"
    assert isinstance(cap.schema_version, int)
    # Capability only. The payload carries no account VALUE: every field is a
    # fixed descriptor, and the sole number present is the adapter's declared
    # schema version. Checked structurally, not by word-matching prose.
    payload = cap.as_dict()
    assert set(payload) == {"available", "module", "entrypoint",
                            "schema_version", "detail"}
    numbers = [v for v in payload.values()
               if isinstance(v, (int, float)) and not isinstance(v, bool)]
    assert numbers == [cap.schema_version]
    assert payload["detail"] == cap.detail and isinstance(payload["detail"], str)


def test_capability_detection_never_invokes_the_adapter_or_reads_evidence():
    """Structural proof over CODE, not prose: this module never imports the
    account-staging surface, never calls the adapter's run(), and names no
    runtime-evidence identifier outside a comment or docstring."""
    tree = ast.parse((REPO_ROOT / "currentness_report.py").read_text())

    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    assert not any("account_staging" in name for name in imported)

    # No attribute call of the form <anything>.run(...) on the adapter, and no
    # evidence-bearing identifier used as a real name anywhere.
    forbidden_names = {"runtime_root", "supplement_bytes", "receipt_sha256",
                       "submission_id", "account_staging"}
    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            used.add(node.attr)
        elif isinstance(node, ast.arg):
            used.add(node.arg)
    assert not (used & forbidden_names), f"evidence surface used: {used & forbidden_names}"

    # And no string literal in this module is a var/ runtime path.
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            assert not node.value.startswith("var/"), node.value


def test_stale_repository_state_still_reports_the_private_path_as_available(tmp_path):
    p = _write(tmp_path / "holdings.yaml",
               _holdings(cash_date="2026-08-01", margin_date="2026-07-31"))
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.verdict == cr.REPOSITORY_STATE_STALE
    assert state.private_evidence.available is True
    assert any("NOT blocked by this verdict" in n for n in state.notes)


# ── 8. current-holdings exposure seam ─────────────────────────────────────

def test_current_holdings_exposure_unavailable_when_repository_stale(tmp_path):
    p = _write(tmp_path / "holdings.yaml",
               _holdings(cash_date="2026-08-01", margin_date="2026-07-31"))
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    result = cr.collect_current_holdings_exposure(state)
    assert result.result == cr.CURRENT_HOLDINGS_UNAVAILABLE
    assert result.status == cr.UNAVAILABLE
    assert result.clusters == ()
    assert result.issuers == ()
    assert result.common_driver is None


def test_current_holdings_exposure_unavailable_even_when_repository_current(tmp_path):
    p = _write(tmp_path / "holdings.yaml", _holdings())
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    result = cr.collect_current_holdings_exposure(state)
    assert result.available is False
    assert result.result == cr.CURRENT_HOLDINGS_UNAVAILABLE


def test_supplied_exposure_seam_passes_through_without_recomputation(tmp_path):
    p = _write(tmp_path / "holdings.yaml", _holdings())
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    supplied = {"clusters": [cr.ClusterConstraint(
        name="zz", cap_pct=25.0, members=("ZZA",), target_exposure_pct=30.0,
        utilisation_pct=120.0, headroom_pct=-5.0, status=cr.OVER_LIMIT)]}
    result = cr.collect_current_holdings_exposure(state, supplied_exposure=supplied)
    assert result.available is True
    assert result.result == "SUPPLIED_BY_CALLER"
    assert result.status == cr.OVER_LIMIT
    assert result.clusters[0].target_exposure_pct == 30.0


def test_supplied_exposure_rejects_untyped_payload(tmp_path):
    p = _write(tmp_path / "holdings.yaml", _holdings())
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    with pytest.raises(cr.CurrentnessReportError):
        cr.collect_current_holdings_exposure(state, supplied_exposure=[1, 2, 3])
    with pytest.raises(cr.CurrentnessReportError):
        cr.collect_current_holdings_exposure(
            state, supplied_exposure={"clusters": [{"name": "zz"}]})


# ── 9. report assembly, rendering, CLI ────────────────────────────────────

def test_report_is_json_serialisable_and_carries_the_disclaimer():
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    blob = json.dumps(report.as_dict(), default=str)
    assert "does not create policy" in blob
    assert "authorizes no transaction" in blob
    assert report.overall_status in cr.STATUSES


def test_render_is_text_and_mentions_every_section():
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    text = cr.render(report)
    for heading in ("1. REPOSITORY ACCOUNT-STATE STATUS",
                    "2. COMPANY-INTELLIGENCE CURRENTNESS",
                    "3. FRESHNESS MONITOR STATUS",
                    "4. COMMITTED STALENESS-REPORT HEALTH",
                    "5. TARGET-WEIGHT CONCENTRATION PREFLIGHT",
                    "6. CURRENT-HOLDINGS CONCENTRATION STATUS",
                    "7. BINDING-CONSTRAINT SUMMARY",
                    "8. CURRENTNESS VS INVESTMENT AUTHORITY"):
        assert heading in text


def test_cli_json_mode_runs_clean(capsys):
    assert cr.main(["--json", "--root", str(REPO_ROOT), "--as-of", "2026-09-16"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["overall_status"] in cr.STATUSES


def test_cli_rejects_a_malformed_as_of(capsys):
    assert cr.main(["--as-of", "not-a-date"]) == 2
    assert "ISO calendar date" in capsys.readouterr().err


def test_report_is_deterministic_for_a_fixed_as_of():
    a = cr.build_report(root=REPO_ROOT, as_of=AS_OF).as_dict()
    b = cr.build_report(root=REPO_ROOT, as_of=AS_OF).as_dict()
    assert json.dumps(a, sort_keys=True, default=str) == \
           json.dumps(b, sort_keys=True, default=str)


# ── 10. real-corpus reconciliation (derived, never hardcoded) ─────────────

def test_real_corpus_company_counts_match_an_independent_derivation():
    """Every expected number is derived here from the live corpus, so this
    fails if the implementation drifts — it encodes no audit constant."""
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    c = report.company_intelligence

    companies_dir = REPO_ROOT / "intelligence" / "companies"
    files = sorted(companies_dir.glob("*.yaml"))
    assert c.record_count == len(files)

    expected_no_catalysts = 0
    expected_lapsed = 0
    for path in files:
        doc = yaml.safe_load(path.read_text()) or {}
        catalysts = doc.get("catalysts")
        if not (isinstance(catalysts, list) and catalysts):
            expected_no_catalysts += 1
            continue
        for entry in catalysts:
            if not isinstance(entry, dict):
                continue
            if entry.get("status") != "pending":
                continue
            expected = entry.get("expected")
            parsed = expected if isinstance(expected, date) and not isinstance(
                expected, datetime) else None
            if parsed is None and isinstance(expected, str):
                try:
                    parsed = date.fromisoformat(expected.strip())
                except ValueError:
                    parsed = None
            if parsed is not None and parsed < AS_OF:
                expected_lapsed += 1

    assert c.records_without_catalysts == expected_no_catalysts
    assert c.total_lapsed_catalysts == expected_lapsed
    assert len(c.lapsed_catalysts) == expected_lapsed


def test_real_corpus_lapsed_catalysts_are_actually_lapsed():
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    for row in report.company_intelligence.lapsed_catalysts:
        assert date.fromisoformat(row.expected) < AS_OF
        assert row.days_overdue == (AS_OF - date.fromisoformat(row.expected)).days


def test_real_corpus_canonical_equity_coverage_is_derived_from_targets():
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    targets = yaml.safe_load((REPO_ROOT / "targets.yaml").read_text())
    expected = {str(r["ticker"]).upper() for r in targets["destination"]
                if r.get("asset_class") == "equity"}
    covered = set(report.company_intelligence.canonical_covered)
    uncovered = set(report.company_intelligence.canonical_uncovered)
    assert covered | uncovered == expected
    assert not (covered & uncovered)


def test_real_corpus_freshness_counts_match_the_files():
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    m = report.freshness_monitor
    reg = yaml.safe_load((REPO_ROOT / "intelligence" / "freshness_registry.yaml").read_text())
    chk = yaml.safe_load((REPO_ROOT / "intelligence" / "freshness_checkpoints.yaml").read_text())
    rows = [r for r in reg["tickers"] if isinstance(r, dict)]
    assert m.enrolled_count == len(rows)
    assert m.monitoring_enabled_count == sum(
        1 for r in rows if r.get("monitoring_enabled") is True)
    assert m.verified_checkpoint_count == sum(
        1 for r in chk["tickers"]
        if isinstance(r, dict) and r.get("checkpoint_status") == "verified")
    # every row not derivably 'current' counts as pending/unverified
    assert m.pending_or_unverified_count == sum(
        1 for r in m.rows if r.status != cr.OK)


def test_real_corpus_common_driver_matches_the_production_helper():
    """Independently confirm the recomputed figure straight from
    allocate._issuer_exposure — no golden constant is written here."""
    import allocate
    targets = yaml.safe_load((REPO_ROOT / "targets.yaml").read_text())
    lookthrough = yaml.safe_load((REPO_ROOT / "issuer_lookthrough.yaml").read_text())
    values = {str(r["ticker"]).upper(): float(r["target_pct"])
              for r in targets["destination"]}
    expected = allocate._issuer_exposure(values, 100.0, lookthrough)

    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    driver = report.target_weight_concentration.common_driver
    assert driver.recomputed_pct == pytest.approx(
        expected["common_driver_current_pct"])
    retained = lookthrough["retained_common_driver_measurement"]["value_pct"]
    assert driver.retained_value_pct == pytest.approx(float(retained))
    # Whether they reconcile is DERIVED, not asserted as a constant.
    reconciles = abs(driver.recomputed_pct - float(retained)) <= \
        cr.RETAINED_MEASUREMENT_TOLERANCE_PCT
    assert driver.reconciles is reconciles
    assert (driver.discrepancy_flag is None) is reconciles


def test_real_corpus_cluster_exposures_match_target_sums():
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    targets = yaml.safe_load((REPO_ROOT / "targets.yaml").read_text())
    values = {str(r["ticker"]).upper(): float(r["target_pct"])
              for r in targets["destination"]}
    configured = {c["name"]: c for c in targets["caps"]["clusters"]}
    assert {c.name for c in report.target_weight_concentration.clusters} == set(configured)
    for row in report.target_weight_concentration.clusters:
        members = [str(t).upper() for t in configured[row.name]["tickers"]]
        assert row.target_exposure_pct == pytest.approx(
            sum(values.get(t, 0.0) for t in members))
        if not members:
            assert row.status == cr.UNAVAILABLE


def test_real_corpus_committed_staleness_report_scope_is_compared_to_now():
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    s = report.committed_staleness_report
    assert s.current_company_count == report.company_intelligence.record_count
    if s.companies_scanned_claim is not None and \
            s.companies_scanned_claim != s.current_company_count:
        assert s.status == cr.STALE


def test_real_corpus_current_holdings_exposure_is_never_computed_from_repo_state():
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    h = report.current_holdings_exposure
    assert h.available is False
    assert h.result == cr.CURRENT_HOLDINGS_UNAVAILABLE
    assert h.clusters == () and h.issuers == () and h.common_driver is None


def test_real_corpus_report_always_states_margin_usage_is_unavailable():
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    assert report.repository_account_state.margin_usage_statement == \
        cr.MARGIN_USAGE_UNAVAILABLE
    assert any(a.area == "current margin usage" and a.status == cr.UNAVAILABLE
               for a in report.attention)


# ── 11. MAJOR 1 regressions — a quantity is never a resolved valuation ────
#
# Pre-fix defect: collect_repository_account_state() passed holdings.yaml's raw
# `shares`/`crypto_shares` quantities to allocate.valuation_completeness(),
# whose first argument is by production contract RESOLVED CURRENT DOLLAR
# VALUES. A finite nonzero quantity (4.05 shares) therefore satisfied the
# completeness check as though it were a resolved $4.05 holding, so fresh
# cash + fresh margin + an entirely unvalued book reported
# REPOSITORY_STATE_CURRENT with dollars available. Fail-open; forbidden.

def _fresh_dates():
    return {"cash": {"balance": 1000.0, "synced_at": "2026-09-16"},
            "margin": {"debt": 0.0, "buffer_pct": 100.0, "synced_at": "2026-09-16"}}


def test_fresh_dates_plus_unvalued_equity_share_is_not_repository_current(tmp_path):
    """THE MAJOR 1 REGRESSION. Everything dated fresh, one nonzero tracked
    share, no resolved dollar value anywhere."""
    doc = {"shares": {"ZZFAKE": 4.05}, "crypto_shares": {}, "holdings": {},
           **_fresh_dates()}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))

    assert state.cash_state == "current"
    assert state.margin_state == "current"
    assert state.valuation_complete is False
    assert state.dollars_from_repository_state is False
    assert state.verdict != cr.REPOSITORY_STATE_CURRENT
    assert any("VALUATION" in reason for reason in state.blocked_by)
    assert any("ZZFAKE" in reason for reason in state.blocked_by)


def test_fresh_dates_plus_unvalued_crypto_quantity_is_not_repository_current(tmp_path):
    """The equivalent crypto case — crypto_shares is the same trap."""
    doc = {"shares": {}, "crypto_shares": {"ZZCOIN": 0.5}, "holdings": {},
           **_fresh_dates()}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))

    assert state.cash_state == "current" and state.margin_state == "current"
    assert state.valuation_complete is False
    assert state.dollars_from_repository_state is False
    assert state.verdict != cr.REPOSITORY_STATE_CURRENT
    assert any("ZZCOIN" in reason for reason in state.blocked_by)


def test_a_quantity_is_never_promoted_to_a_dollar_valuation(tmp_path):
    """A quantity that would look like a perfectly plausible dollar value must
    still count as unresolved — the two are different kinds of number."""
    doc = {"shares": {"ZZFAKE": 1234.56}, "crypto_shares": {}, "holdings": {},
           **_fresh_dates()}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.valuation_complete is False
    assert state.verdict != cr.REPOSITORY_STATE_CURRENT


def test_many_unvalued_positions_are_all_reported_not_just_the_first(tmp_path):
    doc = {"shares": {"ZZA": 1.0, "ZZB": 2.0}, "crypto_shares": {"ZZC": 3.0},
           "holdings": {}, **_fresh_dates()}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    blocked = " ".join(state.blocked_by)
    for ticker in ("ZZA", "ZZB", "ZZC"):
        assert ticker in blocked
    assert any("3 nonzero tracked position(s)" in n
               for n in state.holdings_observation_notes)


def test_zero_quantity_positions_do_not_require_a_valuation(tmp_path):
    """A zero quantity is not a tracked position — existing production
    semantics, preserved."""
    doc = {"shares": {"ZZFAKE": 0.0}, "crypto_shares": {"ZZCOIN": 0},
           "holdings": {}, **_fresh_dates()}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.valuation_complete is True
    assert state.verdict == cr.REPOSITORY_STATE_CURRENT


def test_positive_control_no_tracked_positions_can_prove_completeness(tmp_path):
    """Positive control A: nothing tracked, so nothing is unresolved.

    SUPERSEDED FIXTURE. This control previously omitted `holdings:` entirely
    and still expected REPOSITORY_STATE_CURRENT — which is precisely the
    fail-open the declaration gate now closes, so as written it was asserting
    the defect rather than the property. A legitimate empty book DECLARES all
    three tracks as explicit empty mappings; that is what is controlled here.
    """
    doc = {"shares": {}, "crypto_shares": {}, "holdings": {}, **_fresh_dates()}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.valuation_complete is True
    assert state.dollars_from_repository_state is True
    assert state.verdict == cr.REPOSITORY_STATE_CURRENT


def test_manual_dollar_snapshot_is_structurally_complete_but_not_current(tmp_path):
    """SUPERSEDES the former positive control B.

    The manual `holdings:` snapshot IS a resolved dollar value, so
    allocate.valuation_completeness() still reports structural completeness —
    every tracked position carries some value. But it is UNDATED, so it cannot
    show that value is CURRENT. Those are two different claims and only the
    first is provable from repository state; current-dollar availability must
    therefore stay false."""
    doc = {"shares": {"ZZFAKE": 4.05}, "crypto_shares": {},
           "holdings": {"ZZFAKE": 1234.56}, **_fresh_dates()}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))

    assert state.valuation_complete is True          # structurally complete
    assert state.valuation_evidence_dated is False   # but not shown to be current
    assert state.dollars_from_repository_state is False
    assert state.verdict != cr.REPOSITORY_STATE_CURRENT
    assert any("VALUATION CURRENCY" in reason for reason in state.blocked_by)


def test_partial_manual_coverage_still_fails_closed(tmp_path):
    """One valued, one not — completeness is all-or-nothing."""
    doc = {"shares": {"ZZA": 1.0, "ZZB": 2.0}, "crypto_shares": {},
           "holdings": {"ZZA": 500.0}, **_fresh_dates()}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.valuation_complete is False
    assert state.valuation_evidence_dated is False
    assert state.verdict != cr.REPOSITORY_STATE_CURRENT
    assert any("ZZB" in r for r in state.blocked_by)


def test_module_never_calls_a_price_fetching_surface():
    """Structural AST proof: this module fetches no prices, so it must make no
    call to any price-producing helper. Checked over real call/name nodes —
    a prose mention of `resolve_holdings()` in a comment is documentation, not
    a call, and substring matching would wrongly flag it."""
    tree = ast.parse((REPO_ROOT / "currentness_report.py").read_text())
    banned = {"get_bars", "get_crypto_latest", "resolve_holdings", "fetch_market",
              "fetch_crypto", "AlpacaPaperClient", "compute_all", "days_until_earnings"}
    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                used.add(func.id)
            elif isinstance(func, ast.Attribute):
                used.add(func.attr)
        elif isinstance(node, ast.Import):
            used.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                used.add(node.module.split(".")[0])
            used.update(a.name for a in node.names)
    offenders = used & banned
    assert not offenders, f"price-fetching surface called/imported: {offenders}"


def test_real_corpus_repository_valuation_is_incomplete_and_says_why():
    """On the live corpus every tracked position is share/coin-tracked with no
    manual dollar snapshot, so repository-only valuation is genuinely
    incomplete — derived, not asserted as a constant."""
    doc = yaml.safe_load((REPO_ROOT / "holdings.yaml").read_text())
    expected = sum(1 for q in (doc.get("shares") or {}).values() if float(q) != 0)
    expected += sum(1 for q in (doc.get("crypto_shares") or {}).values() if float(q) != 0)
    manual = doc.get("holdings") or {}

    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    state = report.repository_account_state
    if expected > 0 and not manual:
        assert state.valuation_complete is False
        assert state.dollars_from_repository_state is False
        assert state.verdict != cr.REPOSITORY_STATE_CURRENT


# ── 12. MAJOR 2 regressions — no silent ceiling fallback, strict rows ─────
#
# Pre-fix defect: lookthrough.get("issuer_ceiling_pct", 8.0) and
# lookthrough.get("common_driver_ceiling_pct", 40.0) meant a missing
# safety-sensitive key still produced a plausible OK/OVER_LIMIT verdict against
# a historical literal, and allocate._issuer_exposure's float() coercion turned
# a Boolean fund_holding_weight into a 100% constituent.

def _policy_with(tmp_path, lookthrough):
    targets = {"destination": [
        {"ticker": "ZZA", "target_pct": 10.0, "asset_class": "equity"},
        {"ticker": "ZZFUND", "target_pct": 20.0, "asset_class": "fund"}],
        "caps": {"clusters": []}}
    t = _write(tmp_path / "targets.yaml", targets)
    l = _write(tmp_path / "issuer_lookthrough.yaml", lookthrough)
    return cr.collect_target_weight_concentration(targets_path=t, lookthrough_path=l)


_VALID_ISSUERS = [{"ticker": "ZZA",
                   "funds": [{"fund": "ZZFUND", "fund_holding_weight": 0.10}]}]


def _assert_controlled_unavailable(result, fragment):
    assert result.available is False
    assert result.status == cr.UNAVAILABLE
    assert fragment in result.detail
    # nothing plausible is published alongside the refusal
    assert result.clusters == ()
    assert result.issuers == ()
    assert result.max_issuer is None
    assert result.common_driver is None
    assert result.destination_total_pct is None


def test_missing_issuer_ceiling_does_not_fall_back_to_the_historical_literal(tmp_path):
    """THE MAJOR 2 REGRESSION (issuer half)."""
    result = _policy_with(tmp_path, {"common_driver_ceiling_pct": 40.0,
                                     "issuers": _VALID_ISSUERS})
    _assert_controlled_unavailable(result, "missing required 'issuer_ceiling_pct'")
    assert "8" not in result.detail.split("issuer_ceiling_pct")[0]


def test_missing_common_driver_ceiling_does_not_fall_back(tmp_path):
    """THE MAJOR 2 REGRESSION (common-driver half)."""
    result = _policy_with(tmp_path, {"issuer_ceiling_pct": 8.0,
                                     "issuers": _VALID_ISSUERS})
    _assert_controlled_unavailable(
        result, "missing required 'common_driver_ceiling_pct'")


def test_both_ceilings_missing_is_unavailable(tmp_path):
    result = _policy_with(tmp_path, {"issuers": _VALID_ISSUERS})
    _assert_controlled_unavailable(result, "missing required")


@pytest.mark.parametrize("bad", [True, False])
def test_boolean_ceiling_is_rejected(tmp_path, bad):
    result = _policy_with(tmp_path, {"issuer_ceiling_pct": bad,
                                     "common_driver_ceiling_pct": 40.0,
                                     "issuers": _VALID_ISSUERS})
    _assert_controlled_unavailable(result, "must not be a boolean")


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_ceiling_is_rejected(tmp_path, bad):
    result = _policy_with(tmp_path, {"issuer_ceiling_pct": 8.0,
                                     "common_driver_ceiling_pct": bad,
                                     "issuers": _VALID_ISSUERS})
    _assert_controlled_unavailable(result, "must be finite")


def test_negative_ceiling_is_rejected(tmp_path):
    result = _policy_with(tmp_path, {"issuer_ceiling_pct": -1.0,
                                     "common_driver_ceiling_pct": 40.0,
                                     "issuers": _VALID_ISSUERS})
    _assert_controlled_unavailable(result, ">= 0.0")


@pytest.mark.parametrize("bad", ["8", None, [], {}])
def test_non_numeric_ceiling_is_rejected(tmp_path, bad):
    result = _policy_with(tmp_path, {"issuer_ceiling_pct": bad,
                                     "common_driver_ceiling_pct": 40.0,
                                     "issuers": _VALID_ISSUERS})
    _assert_controlled_unavailable(result, "must be a real number")


@pytest.mark.parametrize("bad", [True, False])
def test_boolean_fund_holding_weight_never_reaches_the_production_helper(tmp_path, bad):
    """float(True) is 1.0 — a Boolean weight would have become a 100% fund
    constituent inside allocate._issuer_exposure. Refused at this boundary;
    the production helper is not modified."""
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA",
                     "funds": [{"fund": "ZZFUND", "fund_holding_weight": bad}]}]})
    _assert_controlled_unavailable(result, "must not be a boolean")


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_fund_holding_weight_is_rejected(tmp_path, bad):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA",
                     "funds": [{"fund": "ZZFUND", "fund_holding_weight": bad}]}]})
    _assert_controlled_unavailable(result, "must be finite")


def test_negative_fund_holding_weight_is_rejected(tmp_path):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA",
                     "funds": [{"fund": "ZZFUND", "fund_holding_weight": -0.1}]}]})
    _assert_controlled_unavailable(result, ">= 0.0")


def test_missing_fund_holding_weight_is_rejected(tmp_path):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA", "funds": [{"fund": "ZZFUND"}]}]})
    _assert_controlled_unavailable(result, "missing 'fund_holding_weight'")


@pytest.mark.parametrize("bad", ["not-a-mapping", 3, None, []])
def test_malformed_fund_row_is_rejected(tmp_path, bad):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA", "funds": [bad]}]})
    _assert_controlled_unavailable(result, "is not a mapping")


@pytest.mark.parametrize("bad", ["", "   ", None, 3, []])
def test_malformed_fund_identity_is_rejected(tmp_path, bad):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA",
                     "funds": [{"fund": bad, "fund_holding_weight": 0.1}]}]})
    _assert_controlled_unavailable(result, "must be a non-empty string")


def test_duplicate_issuer_identity_is_rejected_not_silently_collapsed(tmp_path):
    """_issuer_exposure keys its result by ticker, so a duplicate would be
    silently collapsed and one row's weights lost."""
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA", "funds": []},
                    {"ticker": "zza", "funds": []}]})
    _assert_controlled_unavailable(result, "duplicate issuer identity")


def test_duplicate_fund_identity_within_one_issuer_is_rejected(tmp_path):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA", "funds": [
            {"fund": "ZZFUND", "fund_holding_weight": 0.1},
            {"fund": "ZZFUND", "fund_holding_weight": 0.2}]}]})
    _assert_controlled_unavailable(result, "duplicate fund identity")


@pytest.mark.parametrize("bad", ["", "   ", None, 3, []])
def test_malformed_issuer_ticker_is_rejected(tmp_path, bad):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": bad, "funds": []}]})
    _assert_controlled_unavailable(result, "must be a non-empty string")


@pytest.mark.parametrize("bad", ["nope", 3, {}])
def test_malformed_issuers_container_is_rejected(tmp_path, bad):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": bad})
    _assert_controlled_unavailable(result, "issuers must be a list")


@pytest.mark.parametrize("bad", ["nope", 3, {}])
def test_malformed_funds_container_is_rejected(tmp_path, bad):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA", "funds": bad}]})
    _assert_controlled_unavailable(result, "funds must be a list")


def test_malformed_issuer_row_is_rejected(tmp_path):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": ["not-a-mapping"]})
    _assert_controlled_unavailable(result, "is not a mapping")


def test_positive_control_valid_lookthrough_still_computes(tmp_path):
    """The refusals above must not have broken the working path."""
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": _VALID_ISSUERS})
    assert result.available is True
    assert result.issuers[0].ticker == "ZZA"
    assert result.issuers[0].embedded_pct == pytest.approx(2.0)
    assert result.common_driver.ceiling_pct == pytest.approx(40.0)
    assert result.issuers[0].ceiling_pct == pytest.approx(8.0)


def test_explicitly_empty_issuers_list_is_valid_zero_coverage(tmp_path):
    """A DECLARED empty membership is a legitimate state. An absent key is not
    — see test_absent_issuers_key_is_unavailable below."""
    result = _policy_with(tmp_path, {"issuer_ceiling_pct": 8.0,
                                     "common_driver_ceiling_pct": 40.0,
                                     "issuers": []})
    assert result.available is True
    assert result.issuers == ()
    assert result.common_driver.recomputed_pct == pytest.approx(0.0)


def test_explicitly_empty_funds_list_is_valid(tmp_path):
    """Likewise a declared empty fund list: real direct exposure, no embedded."""
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA", "funds": []}]})
    assert result.available is True
    assert result.issuers[0].direct_pct == pytest.approx(10.0)
    assert result.issuers[0].embedded_pct == pytest.approx(0.0)


def test_validate_lookthrough_rejects_a_non_mapping_document(tmp_path):
    validated, reason = cr.validate_lookthrough(["not", "a", "mapping"])
    assert validated is None and "not a mapping" in reason


def test_real_corpus_lookthrough_passes_strict_validation():
    """The committed configuration must satisfy the strict validator — if it
    ever stops doing so, that is a real finding, not a test to relax."""
    lookthrough = yaml.safe_load((REPO_ROOT / "issuer_lookthrough.yaml").read_text())
    validated, reason = cr.validate_lookthrough(lookthrough)
    assert reason is None, reason
    assert validated["issuer_ceiling_pct"] == pytest.approx(
        float(lookthrough["issuer_ceiling_pct"]))
    assert validated["common_driver_ceiling_pct"] == pytest.approx(
        float(lookthrough["common_driver_ceiling_pct"]))
    assert len(validated["issuers"]) == len(lookthrough["issuers"])


def test_real_corpus_ceilings_are_read_from_config_not_defaulted():
    """The published ceilings must equal the committed values, and the module
    must contain no ceiling fallback literal."""
    lookthrough = yaml.safe_load((REPO_ROOT / "issuer_lookthrough.yaml").read_text())
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    t = report.target_weight_concentration
    assert t.available is True
    assert t.common_driver.ceiling_pct == pytest.approx(
        float(lookthrough["common_driver_ceiling_pct"]))
    for row in t.issuers:
        assert row.ceiling_pct == pytest.approx(float(lookthrough["issuer_ceiling_pct"]))

    source = (REPO_ROOT / "currentness_report.py").read_text()
    for fallback in ('"issuer_ceiling_pct", 8.0', '"common_driver_ceiling_pct", 40.0',
                     "get(\"issuer_ceiling_pct\", ", "get(\"common_driver_ceiling_pct\", "):
        assert fallback not in source, f"ceiling fallback still present: {fallback}"


# ── 13. DELTA MAJOR 1 — undated valuation never proves currency ───────────
#
# Pre-fix defect: the manual `holdings:` dollar snapshot satisfied
# allocate.valuation_completeness(), so fresh cash + fresh margin + an UNDATED
# manual value produced REPOSITORY_STATE_CURRENT / dollars available. A manual
# value is real but undated; structural completeness is not currency.
#
# holdings.yaml dates exactly two blocks (cash.synced_at, margin.synced_at) —
# see allocate.write_state(), its only writer. There is no per-position
# valuation timestamp, so any nonzero position fails closed.

def test_holdings_schema_still_dates_only_cash_and_margin():
    """PINS THE SCHEMA FACT the currency rule rests on.

    allocate.write_state() is the only writer of holdings.yaml. It emits
    `synced_at` for the cash and margin blocks only; holdings/shares/
    crypto_shares are written as bare mappings. If a dated valuation form is
    ever added, this test fails and forces a deliberate decision rather than
    letting the fail-closed rule silently persist — or silently lapse."""
    source = (REPO_ROOT / "allocate.py").read_text()
    body = source[source.index("def write_state("):source.index("def update_cash(")]
    emitted = body.count('f"  synced_at: ')
    assert emitted == 2, (
        f"write_state() emits {emitted} synced_at fields, not 2 — re-derive which "
        "blocks are dated before trusting the valuation-currency rule")
    for dated_block in ('f"  synced_at: {cash.get(', 'f"  synced_at: {margin.get('):
        assert dated_block in body
    # the three value/quantity tracks are still written undated
    for track in ('f.write("holdings:\\n")', 'f.write("shares:\\n")',
                  'f.write("crypto_shares:\\n")'):
        assert track in body

    doc = yaml.safe_load((REPO_ROOT / "holdings.yaml").read_text())
    assert "synced_at" in (doc.get("cash") or {})
    assert "synced_at" in (doc.get("margin") or {})
    for track in cr.VALUATION_EVIDENCE_TRACKS:
        block = doc.get(track) or {}
        assert "synced_at" not in block
        for value in block.values():
            assert not isinstance(value, dict), (
                f"{track} entries are no longer bare scalars — a per-position "
                "structure may now carry a date; re-derive the currency rule")


def test_undated_manual_valuation_does_not_prove_current_dollars(tmp_path):
    """THE DELTA MAJOR 1 REGRESSION. Fresh cash + fresh margin + nonzero
    tracked position + manual dollar fallback + no admissible valuation
    timestamp => must NOT be current/available."""
    doc = {"shares": {"ZZFAKE": 4.05}, "crypto_shares": {},
           "holdings": {"ZZFAKE": 1234.56}, **_fresh_dates()}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))

    assert state.cash_state == "current" and state.margin_state == "current"
    assert state.valuation_evidence_dated is False
    # ZZFAKE is share-tracked AND manually valued: one position, not two.
    assert state.positions_requiring_valuation == 1
    assert state.dollars_from_repository_state is False
    assert state.verdict != cr.REPOSITORY_STATE_CURRENT
    assert any("no dated current valuation" in r for r in state.blocked_by)


def test_manual_only_position_is_counted_even_though_untracked(tmp_path):
    """A manual-only entry is never `expected` by valuation_completeness (it is
    in no shares/crypto_shares block), so before this gate it received zero
    scrutiny and passed as complete. It is a position and it counts."""
    doc = {"shares": {}, "crypto_shares": {}, "holdings": {"ZZONLY": 500.0},
           **_fresh_dates()}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))

    assert state.valuation_complete is True       # structurally, nothing is missing
    assert state.valuation_evidence_dated is False
    assert state.positions_requiring_valuation == 1
    assert state.verdict != cr.REPOSITORY_STATE_CURRENT


@pytest.mark.parametrize("doc,expected", [
    ({"shares": {"ZZA": 1.0}, "crypto_shares": {}, "holdings": {}}, 1),
    ({"shares": {}, "crypto_shares": {"ZZC": 0.5}, "holdings": {}}, 1),
    ({"shares": {}, "crypto_shares": {}, "holdings": {"ZZM": 10.0}}, 1),
    ({"shares": {"ZZA": 1.0}, "crypto_shares": {"ZZC": 2.0},
      "holdings": {"ZZM": 3.0}}, 3),
])
def test_every_track_counts_toward_positions_requiring_valuation(doc, expected):
    evidence = cr.dated_valuation_evidence(doc)
    assert evidence["position_count"] == expected
    assert evidence["dated"] is False
    assert evidence["reason"] is not None


def test_one_ticker_in_two_tracks_is_one_position(tmp_path):
    """A share-tracked name that also carries a manual dollar fallback is the
    documented production pattern — it is a single position to value."""
    evidence = cr.dated_valuation_evidence(
        {"shares": {"ZZA": 1.0}, "crypto_shares": {}, "holdings": {"ZZA": 500.0}})
    assert evidence["position_count"] == 1
    mixed = cr.dated_valuation_evidence(
        {"shares": {"ZZA": 1.0}, "crypto_shares": {}, "holdings": {"zza": 500.0}})
    assert mixed["position_count"] == 1, "ticker identity must be case-insensitive"


def test_a_malformed_position_entry_counts_rather_than_being_dismissed():
    """A malformed value is not provably empty, so it must not be treated as
    an absent position and quietly skipped."""
    for bad in (True, float("nan"), "not-a-number", None, [], {}):
        evidence = cr.dated_valuation_evidence(
            {"shares": {"ZZBAD": bad}, "crypto_shares": {}, "holdings": {}})
        assert evidence["position_count"] == 1, bad
        assert evidence["dated"] is False


def test_positive_control_empty_book_proves_valuation_completeness(tmp_path):
    """THE PRESERVED POSITIVE CONTROL. Nothing to value, so the currency
    question does not arise — fresh cash and margin alone are sufficient."""
    doc = {"shares": {}, "crypto_shares": {}, "holdings": {}, **_fresh_dates()}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))

    assert state.valuation_complete is True
    assert state.valuation_evidence_dated is True
    assert state.positions_requiring_valuation == 0
    assert state.dollars_from_repository_state is True
    assert state.verdict == cr.REPOSITORY_STATE_CURRENT
    assert state.blocked_by == ()


def test_positive_control_all_zero_positions_is_an_empty_book(tmp_path):
    doc = {"shares": {"ZZA": 0.0}, "crypto_shares": {"ZZC": 0},
           "holdings": {"ZZM": 0.0}, **_fresh_dates()}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.positions_requiring_valuation == 0
    assert state.verdict == cr.REPOSITORY_STATE_CURRENT


def test_currency_gate_only_restricts_never_loosens(tmp_path):
    """Stale cash plus an empty book: the gate says 'dated', but the production
    availability fact still blocks. The gate must never upgrade that."""
    doc = {"shares": {}, "crypto_shares": {}, "holdings": {},
           "cash": {"balance": 1000.0, "synced_at": "2026-08-01"},
           "margin": {"debt": 0.0, "buffer_pct": 100.0, "synced_at": "2026-08-01"}}
    p = _write(tmp_path / "holdings.yaml", doc)
    state = cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.valuation_evidence_dated is True
    assert state.dollars_from_repository_state is False
    assert state.verdict == cr.REPOSITORY_STATE_STALE


def test_module_names_no_hypothetical_valuation_timestamp_field():
    """The fix must not invent a new valuation authority by naming a field a
    future schema 'should' carry."""
    source = (REPO_ROOT / "currentness_report.py").read_text()
    for invented in ("holdings_synced_at", "valued_at", "valuation_synced_at",
                     "priced_at", "positions_synced_at"):
        assert invented not in source, f"invented valuation authority: {invented}"


def test_real_corpus_positions_force_undated_verdict():
    """Derived from the live file, not asserted as a constant."""
    doc = yaml.safe_load((REPO_ROOT / "holdings.yaml").read_text())
    expected = cr.dated_valuation_evidence(doc)["position_count"]
    report = cr.build_report(root=REPO_ROOT, as_of=AS_OF)
    state = report.repository_account_state
    assert state.positions_requiring_valuation == expected
    if expected > 0:
        assert state.valuation_evidence_dated is False
        assert state.dollars_from_repository_state is False
        assert state.verdict != cr.REPOSITORY_STATE_CURRENT


# ── 14. DELTA MAJOR 2 — a missing membership key is not an empty set ──────

def test_absent_issuers_key_is_unavailable(tmp_path):
    """THE DELTA MAJOR 2 REGRESSION (top level). Pre-fix this published a
    plausible 0.0000% common-driver exposure with status OK."""
    result = _policy_with(tmp_path, {"issuer_ceiling_pct": 8.0,
                                     "common_driver_ceiling_pct": 40.0})
    _assert_controlled_unavailable(result, "missing required 'issuers'")
    assert "not an empty membership" in result.detail


def test_absent_funds_key_on_an_issuer_row_is_unavailable(tmp_path):
    """THE DELTA MAJOR 2 REGRESSION (per issuer). Pre-fix this published
    ZZA at 10.0000% direct with zero embedded — understating the controls."""
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA"}]})
    _assert_controlled_unavailable(result, "missing required 'funds'")
    assert "not an empty membership" in result.detail


def test_absent_funds_on_a_later_issuer_row_is_still_caught(tmp_path):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA", "funds": []}, {"ticker": "ZZB"}]})
    _assert_controlled_unavailable(result, "missing required 'funds'")
    assert "issuers[1]" in result.detail


def test_explicit_null_issuers_is_rejected_as_a_type_error(tmp_path):
    """`issuers: null` is present-but-wrong-typed, distinct from absent."""
    result = _policy_with(tmp_path, {"issuer_ceiling_pct": 8.0,
                                     "common_driver_ceiling_pct": 40.0,
                                     "issuers": None})
    _assert_controlled_unavailable(result, "issuers must be a list")


def test_explicit_null_funds_is_rejected_as_a_type_error(tmp_path):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA", "funds": None}]})
    _assert_controlled_unavailable(result, "funds must be a list")


def test_real_corpus_declares_issuers_and_every_funds_key():
    """The committed configuration must declare membership explicitly — if it
    ever stops, that is a real finding, not a test to relax."""
    lookthrough = yaml.safe_load((REPO_ROOT / "issuer_lookthrough.yaml").read_text())
    assert "issuers" in lookthrough
    for row in lookthrough["issuers"]:
        assert "funds" in row, f"{row.get('ticker')} does not declare funds"
    validated, reason = cr.validate_lookthrough(lookthrough)
    assert reason is None, reason


# ── 13. an undeclared position track is not an empty one ──────────────────────
#
# THE THIRD-ROUND MAJOR 1 REGRESSIONS. `dated_valuation_evidence` previously
# read each track as `holdings_doc.get(track) or {}` and skipped non-mappings,
# so a MISSING, NULL or NON-MAPPING track produced the same answer as a
# genuinely declared empty one: zero positions, nothing to value, and a fresh
# REPOSITORY_STATE_CURRENT verdict for a file whose position record had not
# been read at all. Two of those shapes did not even reach a verdict — they
# raised out of production helpers.

_UNDECLARED_FRAGMENT = "POSITION TRACK DECLARATION"


def _state_for(tmp_path, doc, name="holdings.yaml"):
    p = _write(tmp_path / name, doc)
    return cr.collect_repository_account_state(
        holdings_path=p, as_of=datetime(2026, 9, 16, 12, 0, 0))


def _assert_declaration_blocked(state, track):
    """An undeclared track fails CLOSED: never CURRENT, never dollar-usable,
    the track named, and no fabricated position count standing in for the
    count nobody could take."""
    assert state.verdict != cr.REPOSITORY_STATE_CURRENT
    assert state.dollars_from_repository_state is False
    assert state.positions_requiring_valuation is None, (
        "0 would claim a count was taken; it was not")
    assert state.valuation_complete is None, (
        "completeness was never evaluated and must not be reported as a bool")
    blocked = " ".join(state.blocked_by)
    assert _UNDECLARED_FRAGMENT in blocked
    assert track in blocked
    # the separate accepted path is never closed off by this refusal
    assert state.private_evidence.available is True
    assert any("private-evidence adapter" in n for n in state.notes)


@pytest.mark.parametrize("track", ["shares", "crypto_shares", "holdings"])
def test_a_missing_position_track_is_not_an_empty_one(tmp_path, track):
    """Each of the three tracks, omitted one at a time."""
    doc = {"shares": {}, "crypto_shares": {}, "holdings": {}, **_fresh_dates()}
    doc.pop(track)
    _assert_declaration_blocked(_state_for(tmp_path, doc), track)


def test_all_three_tracks_missing_is_not_an_empty_book(tmp_path):
    """The worst case: no position record of any kind, previously reported as
    a current, fully valued, zero-position book."""
    _assert_declaration_blocked(_state_for(tmp_path, dict(_fresh_dates())), "shares")


@pytest.mark.parametrize("track", ["shares", "crypto_shares", "holdings"])
def test_an_explicit_null_track_is_not_an_empty_one(tmp_path, track):
    """`shares:` with nothing after it parses to None, which `or {}` silently
    converted into a declared empty mapping."""
    doc = {"shares": {}, "crypto_shares": {}, "holdings": {}, **_fresh_dates()}
    doc[track] = None
    _assert_declaration_blocked(_state_for(tmp_path, doc), track)


@pytest.mark.parametrize("track,value", [
    ("shares", ["ZZA", "ZZB"]),
    ("crypto_shares", "ZZCOIN 0.5"),
    ("holdings", 7),
    ("shares", True),
])
def test_a_non_mapping_track_is_refused_not_skipped(tmp_path, track, value):
    """A non-mapping track was skipped entirely. Two of these shapes also
    raised out of production helpers rather than producing a diagnostic:
    a non-mapping `shares`/`crypto_shares` raises AttributeError inside
    allocate.valuation_completeness, and a non-mapping `holdings` raises
    ValueError while building the resolved-value map. allocate.py is NOT
    changed; the declaration gate runs first so neither is ever reached."""
    doc = {"shares": {}, "crypto_shares": {}, "holdings": {}, **_fresh_dates()}
    doc[track] = value
    _assert_declaration_blocked(_state_for(tmp_path, doc), track)


def test_a_non_mapping_track_produces_a_diagnostic_not_an_exception(tmp_path):
    """Explicitly: the two crash shapes are controlled UNAVAILABLE now."""
    for track, value in (("shares", "ZZA 1"), ("crypto_shares", 7),
                         ("holdings", ["ZZA"])):
        doc = {"shares": {}, "crypto_shares": {}, "holdings": {},
               **_fresh_dates()}
        doc[track] = value
        state = _state_for(tmp_path, doc, name=f"h-{track}.yaml")  # no raise
        assert state.verdict == cr.PRIVATE_CURRENT_EVIDENCE_REQUIRED


def test_undeclared_track_reason_is_stated_once_not_duplicated(tmp_path):
    """The declaration failure travels through the production availability
    helper as the valuation blocker; it must not ALSO be appended as a
    currency blocker."""
    doc = {"shares": {}, "crypto_shares": {}, **_fresh_dates()}
    state = _state_for(tmp_path, doc)
    occurrences = sum(r.count(_UNDECLARED_FRAGMENT) for r in state.blocked_by)
    assert occurrences == 1, state.blocked_by


def test_undeclared_track_notes_never_publish_a_position_count(tmp_path):
    """`len()` of a str or list would publish a number describing the wrong
    thing: len("ZZA 1") is 5, not five positions."""
    doc = {"shares": "ZZA 1", "crypto_shares": {}, "holdings": {},
           **_fresh_dates()}
    state = _state_for(tmp_path, doc)
    notes = " ".join(state.holdings_observation_notes)
    assert "NOT DECLARED" in notes
    assert "positions: 5" not in notes
    assert any("valuation completeness was NOT evaluated" in n for n in state.notes)


def test_an_undeclared_track_still_reports_stale_cash_as_stale(tmp_path):
    """The declaration gate RESTRICTS; it never relabels an independently
    knowable fact. Stale dates stay the stale verdict."""
    doc = {"shares": {}, "crypto_shares": {},
           "cash": {"balance": 1000.0, "synced_at": "2026-08-01"},
           "margin": {"debt": 0.0, "buffer_pct": 100.0, "synced_at": "2026-07-31"}}
    state = _state_for(tmp_path, doc)
    assert state.verdict == cr.REPOSITORY_STATE_STALE
    assert state.cash_state == "stale"
    assert state.dollars_from_repository_state is False
    assert any(_UNDECLARED_FRAGMENT in r for r in state.blocked_by)


def test_an_undeclared_track_never_suppresses_the_margin_usage_statement(tmp_path):
    doc = {"shares": {}, "crypto_shares": {}, **_fresh_dates()}
    state = _state_for(tmp_path, doc)
    assert state.margin_usage_statement == cr.MARGIN_USAGE_UNAVAILABLE


@pytest.mark.parametrize("doc,declared", [
    ({"shares": {}, "crypto_shares": {}, "holdings": {}}, True),
    ({"shares": {"ZZA": 0.0}, "crypto_shares": {}, "holdings": {}}, True),
    ({"shares": {}, "crypto_shares": {}}, False),
    ({"shares": None, "crypto_shares": {}, "holdings": {}}, False),
    ({"shares": [], "crypto_shares": {}, "holdings": {}}, False),
])
def test_dated_valuation_evidence_reports_declaration_directly(doc, declared):
    evidence = cr.dated_valuation_evidence(doc)
    assert evidence["tracks_declared"] is declared
    if declared:
        assert evidence["declaration_reason"] is None
        assert isinstance(evidence["position_count"], int)
    else:
        assert _UNDECLARED_FRAGMENT in evidence["declaration_reason"]
        assert evidence["position_count"] is None
        assert evidence["dated"] is False
        assert evidence["reason"] is None


def test_positive_control_explicitly_declared_empty_book_is_still_current(tmp_path):
    """THE PRESERVED POSITIVE CONTROL for this gate. All three tracks present
    and explicitly empty is a real declaration of an empty book, and it must
    remain CURRENT — the gate refuses silence, not emptiness."""
    doc = {"shares": {}, "crypto_shares": {}, "holdings": {}, **_fresh_dates()}
    state = _state_for(tmp_path, doc)
    assert state.verdict == cr.REPOSITORY_STATE_CURRENT
    assert state.dollars_from_repository_state is True
    assert state.valuation_complete is True
    assert state.positions_requiring_valuation == 0


def test_positive_control_declared_all_zero_book_is_still_current(tmp_path):
    """Explicit zero quantities are a declaration too, and production already
    treats a zero quantity as no position. Unchanged."""
    doc = {"shares": {"ZZA": 0.0}, "crypto_shares": {"ZZC": 0},
           "holdings": {"ZZM": 0.0}, **_fresh_dates()}
    state = _state_for(tmp_path, doc)
    assert state.verdict == cr.REPOSITORY_STATE_CURRENT
    assert state.positions_requiring_valuation == 0


def test_real_corpus_declares_all_three_position_tracks():
    """The committed baseline declares all three as mappings, so this gate
    changes nothing about the real corpus's verdict — if that ever stops being
    true it is a genuine finding about holdings.yaml, not a test to relax."""
    doc = yaml.safe_load((REPO_ROOT / "holdings.yaml").read_text())
    for track in cr.VALUATION_EVIDENCE_TRACKS:
        assert track in doc, track
        assert isinstance(doc[track], dict), track
    assert cr.dated_valuation_evidence(doc)["tracks_declared"] is True


# ── 14. a whitespace-padded look-through identity is refused, not trimmed ─────
#
# THE THIRD-ROUND MAJOR 2 REGRESSIONS. validate_lookthrough normalised
# identities for its duplicate check (`.strip().upper()`) but reconstructed the
# validated structure from the RAW strings, while the production helper
# allocate._issuer_exposure resolves with `.upper()` and NO `.strip()`. A padded
# identity therefore passed validation and then matched no canonical holdings
# key, contributing 0.0% direct and 0.0% embedded exposure and understating the
# 8% issuer and 40% common-driver controls while still reporting OK.

_PADDED_FRAGMENT = "whitespace-padded"


@pytest.mark.parametrize("ticker", [" ZZA", "ZZA ", " ZZA ", "\tZZA", "ZZA\n"])
def test_a_padded_issuer_ticker_is_refused(tmp_path, ticker):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": ticker,
                     "funds": [{"fund": "ZZFUND", "fund_holding_weight": 0.10}]}]})
    _assert_controlled_unavailable(result, _PADDED_FRAGMENT)


@pytest.mark.parametrize("fund", [" ZZFUND", "ZZFUND ", " ZZFUND "])
def test_a_padded_fund_identity_is_refused(tmp_path, fund):
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA",
                     "funds": [{"fund": fund, "fund_holding_weight": 0.10}]}]})
    _assert_controlled_unavailable(result, _PADDED_FRAGMENT)


def test_the_padded_identity_refusal_names_the_production_mismatch(tmp_path):
    """The reason must explain WHY, so a reader can act on it rather than
    guessing that padding is merely untidy."""
    _, reason = cr.validate_lookthrough({
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": " ZZA ", "funds": []}]})
    assert ".strip()" in reason and ".upper()" in reason
    assert "8%" in reason and "40%" in reason


def test_padded_identity_would_have_zeroed_real_exposure(tmp_path):
    """THE DEFECT ITSELF, demonstrated against the unmodified production
    helper: identical economics, one padded identity, exposure silently gone.
    allocate._issuer_exposure is called here, never modified."""
    import allocate
    holdings = {"ZZA": 10.0, "ZZFUND": 100.0}
    clean = {"ticker": "ZZA",
             "funds": [{"fund": "ZZFUND", "fund_holding_weight": 0.5}]}
    padded = {"ticker": " ZZA ",
              "funds": [{"fund": " ZZFUND ", "fund_holding_weight": 0.5}]}

    honest = allocate._issuer_exposure(holdings, 110.0, {"issuers": [clean]})
    silent = allocate._issuer_exposure(holdings, 110.0, {"issuers": [padded]})
    assert honest["common_driver_current_pct"] > 50.0
    assert silent["common_driver_current_pct"] == 0.0
    # and validate_lookthrough now refuses to hand the padded form onward
    assert cr.validate_lookthrough({
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [padded]})[0] is None


def test_lowercase_identities_are_accepted_because_production_uppercases(tmp_path):
    """Case is NOT the divergence — `_issuer_exposure` applies `.upper()` to
    both identities, so a lowercase row resolves identically there and here.
    Refusing it would be a rule this defect does not justify."""
    validated, reason = cr.validate_lookthrough({
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "zza",
                     "funds": [{"fund": "zzfund", "fund_holding_weight": 0.10}]}]})
    assert reason is None
    assert validated["issuers"][0]["ticker"] == "zza"


def test_duplicate_detection_stays_canonical_across_case(tmp_path):
    """Unchanged: duplicates are still detected on the canonical identity, so
    ZZA and zza remain one issuer."""
    result = _policy_with(tmp_path, {
        "issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
        "issuers": [{"ticker": "ZZA", "funds": []},
                    {"ticker": "zza", "funds": []}]})
    _assert_controlled_unavailable(result, "duplicate issuer identity")


def test_validated_identities_are_passed_through_unmodified(tmp_path):
    """Approach A, stated structurally: the validator REFUSES padding, it does
    not canonicalise. Every accepted identity reaches the production helper
    exactly as the file wrote it, so this report can never publish an exposure
    the allocator would not compute from the same configuration."""
    lookthrough = {"issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0,
                   "issuers": [{"ticker": "zzA",
                                "funds": [{"fund": "zzFund",
                                           "fund_holding_weight": 0.10}]}]}
    validated, reason = cr.validate_lookthrough(lookthrough)
    assert reason is None
    assert validated["issuers"][0]["ticker"] == "zzA"
    assert validated["issuers"][0]["funds"][0]["fund"] == "zzFund"


def test_real_corpus_carries_no_padded_identity():
    """The committed configuration is canonical today, so this refusal changes
    nothing economically about the real report — verified, not assumed."""
    lookthrough = yaml.safe_load((REPO_ROOT / "issuer_lookthrough.yaml").read_text())
    for row in lookthrough["issuers"]:
        assert row["ticker"] == row["ticker"].strip(), row["ticker"]
        for fund in row.get("funds") or []:
            assert fund["fund"] == fund["fund"].strip(), fund["fund"]
    assert cr.validate_lookthrough(lookthrough)[1] is None


def test_render_never_prints_a_bare_none_for_unevaluated_completeness(tmp_path):
    """`None` must not read as a falsy completeness result in the rendered
    report — it means the question was never asked."""
    root = tmp_path / "root"
    root.mkdir()
    for name in ("targets.yaml", "gates.yaml", "issuer_lookthrough.yaml"):
        shutil.copy(REPO_ROOT / name, root / name)
    _write(root / "holdings.yaml",
           {"shares": None, "crypto_shares": {}, "holdings": {},
            **_fresh_dates()})
    (root / "intelligence").mkdir()
    out = cr.render(cr.build_report(root=root, as_of=AS_OF))
    line = next(l for l in out.splitlines() if "valuation complete" in l)
    assert "NOT EVALUATED" in line
    assert line.strip().rstrip().endswith(")")
    assert "valuation complete          None" not in out


@pytest.mark.parametrize("bad", [None, 7, "holdings", [], True, 1.5])
def test_dated_valuation_evidence_fails_closed_on_a_non_mapping_document(bad):
    """A non-mapping document declares no track at all. The in-module caller
    already coerces one to {} before reaching here, but this is public and must
    refuse rather than raise."""
    evidence = cr.dated_valuation_evidence(bad)
    assert evidence["tracks_declared"] is False
    assert evidence["position_count"] is None
    assert evidence["dated"] is False
    assert _UNDECLARED_FRAGMENT in evidence["declaration_reason"]


# ── 15. a malformed position entry must not escape as an exception ────────────
#
# THE FOURTH-ROUND MAJOR REGRESSIONS. The declaration gate proved the three
# tracks EXIST and are mappings. It did not prove their CONTENTS are readable,
# and once the mappings exist collect_repository_account_state() still handed
# them to the unmodified production helper, which does a bare `float(qty)` over
# every shares/crypto_shares quantity and later joins the collected symbols
# into text. Reproduced at the parent commit, end to end, with all three tracks
# explicitly declared and fresh cash/margin dates:
#
#   shares:        {ZZBAD: "not-a-number"}  -> ValueError  (allocate.py:319)
#   shares:        {ZZBAD: []}              -> TypeError   (allocate.py:319)
#   shares:        {ZZBAD: {}}              -> TypeError   (allocate.py:319)
#   shares:        {ZZBAD: None}            -> TypeError   (allocate.py:319)
#   crypto_shares: {ZZBAD: "not-a-number"}  -> ValueError  (allocate.py:322)
#   crypto_shares: {ZZBAD: []}              -> TypeError   (allocate.py:322)
#   crypto_shares: {ZZBAD: {}}              -> TypeError   (allocate.py:322)
#   any track with a non-string ticker key  -> TypeError at ", ".join(...)
#
# The pre-existing malformed-entry test exercises dated_valuation_evidence()
# directly, so it never reached the crash site. These go end to end.

_MALFORMED_FRAGMENT = "MALFORMED POSITION INPUT"


def _declared(**tracks):
    """All three tracks explicitly declared, fresh dates, one track overridden."""
    doc = {"shares": {}, "crypto_shares": {}, "holdings": {}, **_fresh_dates()}
    doc.update(tracks)
    return doc


def _assert_malformed_blocked(state, *fragments):
    """A malformed entry fails CLOSED, names itself, and invents nothing."""
    assert state.verdict != cr.REPOSITORY_STATE_CURRENT
    assert state.dollars_from_repository_state is False
    # completeness was never evaluated -- it must not read as either True or a
    # production-derived False, because the helper was never asked
    assert state.valuation_complete is not True
    assert state.valuation_complete is None
    blocked = " ".join(state.blocked_by)
    assert _MALFORMED_FRAGMENT in blocked
    for fragment in fragments:
        assert fragment in blocked, f"{fragment!r} not named in: {blocked}"
    # the malformed line is still a POSITION -- never silently zeroed or dropped
    assert state.positions_requiring_valuation is not None
    assert state.positions_requiring_valuation >= 1
    # the separate accepted route is untouched by this refusal
    assert state.private_evidence.available is True
    assert any("private-evidence adapter" in n for n in state.notes)
    assert any("NOT evaluated" in n for n in state.notes)


@pytest.mark.parametrize("bad", ["not-a-number", [], {}, None, float("nan"),
                                 float("inf"), True, "", "1,234"])
def test_malformed_share_quantity_is_a_diagnostic_not_an_exception(tmp_path, bad):
    """Every shape `float(qty)` cannot take, plus the shapes it takes but must
    not: bool (float(True) is 1.0) and non-finite."""
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml",
                             _declared(shares={"ZZBAD": bad})),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    _assert_malformed_blocked(state, "shares.ZZBAD")


@pytest.mark.parametrize("bad", ["not-a-number", [], {}, None, float("nan"), True])
def test_malformed_crypto_quantity_is_a_diagnostic_not_an_exception(tmp_path, bad):
    """crypto_shares is coerced by the same bare float() one loop later."""
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml",
                             _declared(crypto_shares={"ZZBAD": bad})),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    _assert_malformed_blocked(state, "crypto_shares.ZZBAD")


@pytest.mark.parametrize("track", ["shares", "crypto_shares", "holdings"])
@pytest.mark.parametrize("key", [7, 3.5, None, True, "", "   "])
def test_malformed_ticker_identity_is_a_diagnostic_not_an_exception(tmp_path, track, key):
    """A non-string ticker key crashes at a DIFFERENT site from the quantity
    coercion -- `", ".join(unresolved)` and `", ".join(invalid)` inside
    valuation_completeness -- and reaches all three tracks, including the
    manual holdings snapshot whose VALUES production validates for itself."""
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml",
                             _declared(**{track: {key: 1.0}})),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    _assert_malformed_blocked(state, track, "ticker identity")


def test_every_reproduced_crash_shape_now_returns_a_state(tmp_path):
    """The eight shapes reproduced as uncaught exceptions at the parent commit,
    asserted as a set: each returns a state object rather than raising."""
    shapes = [
        ("shares", {"ZZBAD": "not-a-number"}), ("shares", {"ZZBAD": []}),
        ("shares", {"ZZBAD": {}}), ("shares", {"ZZBAD": None}),
        ("crypto_shares", {"ZZBAD": "not-a-number"}), ("crypto_shares", {"ZZBAD": []}),
        ("crypto_shares", {"ZZBAD": {}}), ("shares", {7: 1.0}),
    ]
    for i, (track, block) in enumerate(shapes):
        state = cr.collect_repository_account_state(   # must not raise
            holdings_path=_write(tmp_path / f"h{i}.yaml", _declared(**{track: block})),
            as_of=datetime(2026, 9, 16, 12, 0, 0))
        assert state.verdict == cr.PRIVATE_CURRENT_EVIDENCE_REQUIRED
        assert state.valuation_complete is None


def test_malformed_entry_names_every_offender_not_just_the_first(tmp_path):
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml",
                             _declared(shares={"ZZA": "x", "ZZB": []},
                                       crypto_shares={"ZZC": {}})),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    blocked = " ".join(state.blocked_by)
    for name in ("shares.ZZA", "shares.ZZB", "crypto_shares.ZZC"):
        assert name in blocked
    assert "3 tracked entr" in blocked


def test_malformed_entry_reason_is_stated_once_not_duplicated(tmp_path):
    """It travels through the single production availability rule as the
    valuation blocker; it must not also be appended as a currency blocker."""
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml",
                             _declared(shares={"ZZBAD": "x"})),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert sum(r.count(_MALFORMED_FRAGMENT) for r in state.blocked_by) == 1


def test_a_malformed_entry_still_reports_stale_cash_as_stale(tmp_path):
    """This gate RESTRICTS; it never relabels an independently knowable fact."""
    doc = _declared(shares={"ZZBAD": "x"})
    doc["cash"]["synced_at"] = "2026-08-01"
    doc["margin"]["synced_at"] = "2026-07-31"
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml", doc),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.verdict == cr.REPOSITORY_STATE_STALE
    assert state.cash_state == "stale"
    assert state.dollars_from_repository_state is False
    assert any(_MALFORMED_FRAGMENT in r for r in state.blocked_by)


def test_a_malformed_entry_never_suppresses_the_margin_usage_statement(tmp_path):
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml",
                             _declared(shares={"ZZBAD": "x"})),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.margin_usage_statement == cr.MARGIN_USAGE_UNAVAILABLE


def test_the_declaration_gate_outranks_the_malformed_gate(tmp_path):
    """Both can fail at once. The more fundamental failure is the one reported,
    and the malformed check is not even reached -- there is nothing to read."""
    doc = _declared(shares={"ZZBAD": "x"})
    doc.pop("crypto_shares")
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml", doc),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    blocked = " ".join(state.blocked_by)
    assert _UNDECLARED_FRAGMENT in blocked
    assert _MALFORMED_FRAGMENT not in blocked
    evidence = cr.dated_valuation_evidence(doc)
    assert evidence["tracks_declared"] is False
    assert evidence["entries_wellformed"] is None


@pytest.mark.parametrize("doc,wellformed", [
    ({"shares": {}, "crypto_shares": {}, "holdings": {}}, True),
    ({"shares": {"ZZA": 0.0}, "crypto_shares": {}, "holdings": {}}, True),
    ({"shares": {"ZZA": 1.0}, "crypto_shares": {}, "holdings": {"ZZA": 500.0}}, True),
    ({"shares": {"ZZA": "x"}, "crypto_shares": {}, "holdings": {}}, False),
    ({"shares": {}, "crypto_shares": {"ZZC": []}, "holdings": {}}, False),
    ({"shares": {}, "crypto_shares": {}, "holdings": {4: 1.0}}, False),
])
def test_dated_valuation_evidence_reports_wellformedness_directly(doc, wellformed):
    evidence = cr.dated_valuation_evidence(doc)
    assert evidence["entries_wellformed"] is wellformed
    if wellformed:
        assert evidence["malformed_reason"] is None
    else:
        assert _MALFORMED_FRAGMENT in evidence["malformed_reason"]
        assert evidence["reason"] is None          # the currency gate is not reached
        assert evidence["position_count"] >= 1     # never zeroed


def test_a_malformed_entry_is_never_counted_as_zero_or_absent(tmp_path):
    """The principle the pre-existing direct test established, now proven end
    to end: a malformed line is a position of unknown size, not an empty slot."""
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml",
                             _declared(shares={"ZZBAD": "not-a-number"})),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.positions_requiring_valuation == 1
    assert state.valuation_complete is not True
    assert "0 tracked" not in " ".join(state.blocked_by)


def test_no_price_is_fetched_and_no_value_invented_for_a_malformed_entry(tmp_path):
    """Nothing numeric is published for the malformed line."""
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml",
                             _declared(shares={"ZZBAD": "not-a-number"})),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    blob = json.dumps(state.as_dict())
    assert "$" not in blob
    assert "ZZBAD" in blob          # named, not hidden
    assert state.valuation_complete is None


# ── positive controls this gate must NOT disturb ──────────────────────────────

def test_positive_control_malformed_gate_leaves_an_empty_book_current(tmp_path):
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml", _declared()),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.verdict == cr.REPOSITORY_STATE_CURRENT
    assert state.valuation_complete is True


def test_positive_control_malformed_gate_leaves_an_all_zero_book_current(tmp_path):
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml",
                             _declared(shares={"ZZA": 0.0},
                                       crypto_shares={"ZZC": 0},
                                       holdings={"ZZM": 0.0})),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.verdict == cr.REPOSITORY_STATE_CURRENT
    assert state.valuation_complete is True


def test_positive_control_a_valid_nonzero_position_still_blocks_on_currency(tmp_path):
    """Well-formed and still not current -- the undated-valuation rule from the
    previous round is untouched, and it is a DIFFERENT reason."""
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml",
                             _declared(shares={"ZZA": 4.05})),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.verdict != cr.REPOSITORY_STATE_CURRENT
    blocked = " ".join(state.blocked_by)
    assert "VALUATION CURRENCY" in blocked
    assert _MALFORMED_FRAGMENT not in blocked
    assert state.valuation_complete is False       # production evaluated it


def test_positive_control_a_malformed_holdings_VALUE_stays_productions_call(tmp_path):
    """SCOPE BOUNDARY. The manual `holdings:` track's VALUES are validated
    inside production by _finite_scalar, which returns a flag rather than
    raising and correctly reports complete=False. That judgement is production's
    and this gate must not take it over -- only the identity check reaches
    `holdings`, because only the join does."""
    state = cr.collect_repository_account_state(
        holdings_path=_write(tmp_path / "holdings.yaml",
                             _declared(shares={"ZZA": 1.0},
                                       holdings={"ZZA": "not-a-number"})),
        as_of=datetime(2026, 9, 16, 12, 0, 0))
    assert state.verdict != cr.REPOSITORY_STATE_CURRENT
    assert state.valuation_complete is False       # production's answer, not None
    blocked = " ".join(state.blocked_by)
    assert _MALFORMED_FRAGMENT not in blocked
    assert "ZZA" in blocked


def test_real_corpus_position_entries_are_all_wellformed():
    """The committed baseline is readable, so this gate changes nothing about
    the real corpus -- if that ever stops being true it is a genuine finding."""
    doc = yaml.safe_load((REPO_ROOT / "holdings.yaml").read_text())
    evidence = cr.dated_valuation_evidence(doc)
    assert evidence["tracks_declared"] is True
    assert evidence["entries_wellformed"] is True
    assert evidence["malformed_reason"] is None
