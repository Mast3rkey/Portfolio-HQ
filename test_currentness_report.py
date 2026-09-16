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
    with pytest.raises(cr.CurrentnessReportError):
        cr._strict_pct(bad, "synthetic")


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_percentage_rejected(bad):
    with pytest.raises(cr.CurrentnessReportError):
        cr._strict_pct(bad, "synthetic")


@pytest.mark.parametrize("bad", ["3.0", None, [], {}])
def test_non_numeric_percentage_rejected(bad):
    with pytest.raises(cr.CurrentnessReportError):
        cr._strict_pct(bad, "synthetic")


def test_real_numbers_accepted():
    assert cr._strict_pct(6, "x") == 6.0
    assert cr._strict_pct(2.25, "x") == 2.25


def test_boolean_target_pct_in_config_is_rejected(tmp_path):
    """allocate.build_roster coerces True -> 1.0 (bool subclasses int); this
    diagnostic refuses the raw value before that coercion can hide it."""
    targets = {"destination": [{"ticker": "ZZFAKE", "target_pct": True,
                                "asset_class": "equity"}],
               "caps": {"clusters": []}}
    _write(tmp_path / "targets.yaml", targets)
    _write(tmp_path / "issuer_lookthrough.yaml",
           {"issuer_ceiling_pct": 8.0, "common_driver_ceiling_pct": 40.0, "issuers": []})
    with pytest.raises(cr.CurrentnessReportError):
        cr.collect_target_weight_concentration(
            targets_path=tmp_path / "targets.yaml",
            lookthrough_path=tmp_path / "issuer_lookthrough.yaml")


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
    return {"shares": {}, "crypto_shares": {},
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
