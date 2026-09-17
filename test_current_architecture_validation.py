"""Verification tests for the current-architecture target/concentration evidence matrix.

`research/current_architecture_validation/evidence_matrix.json` is a DATED
EVIDENCE SNAPSHOT, not policy and not authority. These tests exist so that none
of its load-bearing claims can be believed on the artifact's own say-so: every
number and every structural assertion below is RE-DERIVED here from live
repository state, retained evidence bytes, or the production exposure helper,
and then compared against what the artifact records.

If a test in the "current architecture" group fails, that is the intended
signal that configuration has changed since the artifact's `as_of_date`. The
artifact is then stale and must be re-dated or superseded by a new dated
artifact — per this repository's snapshot-preservation convention it must NOT
be silently rewritten to match new state while keeping its old date.

These tests read only. They change no target, cap, ceiling, cluster, gate,
margin parameter, holding, or allocator behaviour, execute no study, acquire no
data, and make no allocation recommendation.
"""

from __future__ import annotations

import ast
import itertools
import json
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
ARTIFACT_DIR = HERE / "research" / "current_architecture_validation"
MATRIX_PATH = ARTIFACT_DIR / "evidence_matrix.json"
REPORT_PATH = ARTIFACT_DIR / "EVIDENCE_MATRIX.md"

TARGETS = HERE / "targets.yaml"
LOOKTHROUGH = HERE / "issuer_lookthrough.yaml"
DUE_DILIGENCE = (
    HERE / "governance" / "evidence" / "PHQ-2026-01" / "final_due_diligence"
    / "Portfolio_HQ_Final_Due_Diligence_and_Approval_v1_32.json"
)
V2_DIR = HERE / "research" / "whole_portfolio_robustness_v2"
V1_DIR = HERE / "research" / "whole_portfolio_robustness"

TOL = 1e-9


# ── fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def matrix() -> dict:
    return json.loads(MATRIX_PATH.read_text())


@pytest.fixture(scope="module")
def targets() -> dict:
    return yaml.safe_load(TARGETS.read_text())


@pytest.fixture(scope="module")
def due_diligence() -> dict:
    return json.loads(DUE_DILIGENCE.read_text())


@pytest.fixture(scope="module")
def concentration():
    """Production-helper exposure at canonical target weights.

    Reuses `currentness_report.collect_target_weight_concentration`, which in
    turn delegates the look-through arithmetic to `allocate._issuer_exposure`.
    Deliberately NOT re-implemented here — a second implementation would prove
    only that two copies of the same mistake agree.
    """
    import currentness_report as cr

    result = cr.collect_target_weight_concentration()
    assert result.available, f"production exposure helper unavailable: {result.detail}"
    return result


def _param(matrix: dict, name_fragment: str) -> dict:
    hits = [p for p in matrix["parameters"] if name_fragment.lower() in p["parameter"].lower()]
    assert len(hits) == 1, f"expected exactly one parameter matching {name_fragment!r}, got {len(hits)}"
    return hits[0]


# ── artifact shape and scope safety ─────────────────────────────────────────

def test_artifact_files_exist():
    assert MATRIX_PATH.is_file()
    assert REPORT_PATH.is_file()


def test_artifact_claims_no_authority(matrix):
    assert matrix["status"] == "EVIDENCE_RECONCILIATION_ONLY"
    assert matrix["authority"].startswith("NONE")


def test_artifact_pins_its_own_basis(matrix):
    assert matrix["as_of_date"]
    assert len(matrix["base_commit"]) == 40


def test_every_parameter_carries_the_required_fields(matrix):
    required = {
        "parameter", "current_value", "current_scope", "canonical_source",
        "origin_source", "original_architecture", "current_architecture",
        "evidence_used", "current_architecture_tested", "alternatives_tested",
        "evidence_grade", "empirical_status", "known_limitations",
        "policy_status", "next_evidence_needed",
    }
    for p in matrix["parameters"]:
        assert required <= set(p), f"{p['parameter']}: missing {required - set(p)}"


def test_evidence_grades_come_from_the_closed_vocabulary(matrix):
    vocab = set(matrix["evidence_grade_vocabulary"])
    for p in matrix["parameters"]:
        assert p["evidence_grade"] in vocab, p["parameter"]


def test_no_parameter_claims_the_current_architecture_was_tested(matrix):
    """The artifact's central negative finding. If this ever legitimately
    changes, the finding itself has changed and the artifact must be revised."""
    for p in matrix["parameters"]:
        assert p["current_architecture_tested"] is False, p["parameter"]
        assert p["alternatives_tested"] is False, p["parameter"]


@pytest.mark.parametrize("forbidden", [
    "buy", "sell", "trim_recommendation", "order", "trade", "shares",
    "recommended_target_pct", "new_target_pct", "score", "rank", "ranking",
])
def test_artifact_contains_no_recommendation_or_order_key(matrix, forbidden):
    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                assert k != forbidden, f"forbidden key {forbidden!r} present"
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(matrix)


def test_artifact_states_margin_is_out_of_scope(matrix):
    joined = " ".join(matrix["boundaries"]).lower()
    assert "out of scope" in joined and "margin" in joined
    assert "stage 1 remains unarmed" in joined


def test_this_module_never_writes(tmp_path):
    """AST proof that the test module opens nothing for writing."""
    tree = ast.parse(Path(__file__).read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            name = getattr(fn, "attr", None) or getattr(fn, "id", None)
            assert name not in {"write_text", "write_bytes", "mkdir", "unlink", "rmtree"}, \
                f"write-capable call {name!r} present"


# ── current architecture: re-derived from live config ───────────────────────

def test_targets_yaml_has_no_tiers_key(targets):
    """The structural fact that orphans every tier-era backtest."""
    assert "tiers" not in targets


def test_tier_era_backtests_still_depend_on_the_absent_tiers_key(matrix):
    affected = matrix["study_reconciliation"]["tier_dependency_finding"]["affected_scripts"]
    assert set(affected) == {
        "backtest_weights.py", "backtest_t1t2_trim.py", "backtest_trend.py",
        "backtest_regime.py", "backtest_rungs.py", "backtest_trims.py",
    }
    direct = {"backtest_regime.py", "backtest_rungs.py", "backtest_trims.py"}
    for script in affected:
        text = (HERE / script).read_text()
        if script in direct:
            assert '["tiers"]' in text, f"{script} no longer reads targets.yaml['tiers']"
        else:
            assert "from backtest_regime import" in text or "from backtest_trims import" in text, \
                f"{script} no longer inherits its roster from a tier-reading module"


def test_destination_rows_and_total_match_the_artifact(matrix, targets):
    rows = targets["destination"]
    total = sum(float(r["target_pct"]) for r in rows)
    derived = matrix["derived_measurements"]
    assert len(rows) == derived["destination_rows"]
    assert abs(total - derived["destination_total_pct"]) < TOL
    assert derived["targets_yaml_has_tiers_key"] is False
    assert "99.25" in _param(matrix, "canonical destination")["current_value"]


def test_current_weights_are_byte_identical_to_the_retained_source(targets, due_diligence):
    """Provenance check for all 36 weights: verbatim transcription, SPCX removed,
    nothing renormalized."""
    current = {r["ticker"].upper(): float(r["target_pct"]) for r in targets["destination"]}
    retained = {
        r["ticker"].strip().upper(): float(r["target_weight_percent"])
        for r in due_diligence["architecture_rows"]
    }
    assert set(retained) - set(current) == {"SPCX"}
    assert set(current) - set(retained) == set()
    mismatched = [t for t in set(current) & set(retained) if abs(current[t] - retained[t]) > TOL]
    assert mismatched == [], f"weights drifted from retained source: {mismatched}"
    assert abs(sum(retained.values()) - 100.0) < TOL
    assert abs(sum(current.values()) - 99.25) < TOL


def test_cluster_membership_and_utilisation_match_the_artifact(matrix, concentration):
    recorded = {c["name"]: c for c in matrix["derived_measurements"]["clusters"]}
    assert set(recorded) == {c.name for c in concentration.clusters}
    for cl in concentration.clusters:
        rec = recorded[cl.name]
        assert list(cl.members) == rec["members"], cl.name
        assert abs(cl.cap_pct - rec["cap_pct"]) < TOL, cl.name
        assert abs(cl.target_exposure_pct - rec["target_exposure_pct"]) < TOL, cl.name
        assert abs(cl.utilisation_pct - rec["utilisation_pct"]) < TOL, cl.name
        assert cl.status == rec["status"], cl.name


def test_oil_cluster_is_dead_configuration_not_a_satisfied_limit(concentration):
    oil = next(c for c in concentration.clusters if c.name == "oil")
    assert oil.members == ()
    assert oil.status == "UNAVAILABLE", "a zero-member cap must never report OK"


def test_semis_and_power_infra_are_non_binding_at_target_weights(concentration):
    util = {c.name: c.utilisation_pct for c in concentration.clusters}
    assert util["semis"] < 100.0
    assert util["power_infra"] < 100.0


def test_max_issuer_matches_the_artifact(matrix, concentration):
    rec = matrix["derived_measurements"]["max_issuer"]
    live = concentration.max_issuer
    assert live.ticker == rec["ticker"]
    for field in ("direct_pct", "embedded_pct", "effective_pct", "ceiling_pct", "headroom_pct"):
        assert abs(getattr(live, field) - rec[field]) < TOL, field


def test_common_driver_recomputation_matches_the_artifact(matrix, concentration):
    rec = matrix["derived_measurements"]["common_driver"]
    live = concentration.common_driver
    assert abs(live.recomputed_pct - rec["recomputed_pct"]) < 1e-6
    assert abs(live.ceiling_pct - rec["ceiling_pct"]) < TOL
    assert abs(live.retained_value_pct - rec["retained_value_pct"]) < TOL
    assert live.reconciles is False
    assert live.limit_status == "OVER_LIMIT"


# ── the retained-evidence reconciliation (facts about frozen bytes) ──────────

def test_retained_lookthrough_line_items_equal_the_current_recomputation(
    due_diligence, concentration
):
    """The core reconciliation: the discrepancy is NOT configuration drift."""
    line_item_sum = sum(r["effective_weight"] for r in due_diligence["lookthrough_exposure"]) * 100.0
    assert abs(line_item_sum - concentration.common_driver.recomputed_pct) < 1e-6, (
        "retained line items no longer equal the current recomputation — the "
        "artifact's central reconciliation claim would need revisiting"
    )


def test_retained_headline_is_inconsistent_with_its_own_line_items(due_diligence):
    rows = due_diligence["lookthrough_exposure"]
    headline = due_diligence["lookthrough_summary"]["effective_ai_platform_common_driver_estimate"]
    total = sum(r["effective_weight"] for r in rows)
    assert abs(total - headline) > 1e-6
    assert abs((total - headline) * 100.0 - 1.6170) < 1e-6


def test_unique_embedded_exclusion_reproduces_the_retained_headline(matrix, due_diligence):
    """Exhaustive search over all 2,047 non-empty subsets; exactly one matches."""
    rows = due_diligence["lookthrough_exposure"]
    names = [r["issuer"] for r in rows]
    embedded = [r["embedded_weight"] for r in rows]
    gap = sum(r["effective_weight"] for r in rows) - \
        due_diligence["lookthrough_summary"]["effective_ai_platform_common_driver_estimate"]

    hits = []
    for k in range(1, len(rows) + 1):
        for combo in itertools.combinations(range(len(rows)), k):
            if abs(sum(embedded[i] for i in combo) - gap) < TOL:
                hits.append(sorted(names[i] for i in combo))

    assert len(hits) == 1, f"reconciliation is no longer unique: {hits}"
    assert hits[0] == ["AAPL", "LLY", "TSLA"]
    assert matrix["derived_measurements"]["unique_embedded_exclusion_sets_reproducing_headline"] == hits


def test_retained_mega6_is_reproducible_from_the_same_line_items(due_diligence):
    """Corroborates that the line items — not the headline — are the reliable part."""
    rows = {r["issuer"]: r["effective_weight"] for r in due_diligence["lookthrough_exposure"]}
    mega6 = ["NVDA", "MSFT", "AMZN", "Alphabet (GOOGL+GOOG)", "AVGO", "META"]
    assert abs(sum(rows[n] for n in mega6)
               - due_diligence["lookthrough_summary"]["effective_mega6_weight"]) < TOL


def test_retained_nvda_effective_weight_reproduces_exactly(due_diligence, concentration):
    retained_nvda = next(
        r for r in due_diligence["lookthrough_exposure"] if r["issuer"] == "NVDA"
    )["effective_weight"]
    assert abs(retained_nvda * 100.0 - concentration.max_issuer.effective_pct) < 1e-9


# ── study status: re-derived from retained research artifacts ───────────────

def test_v1_study_is_classified_not_decision_grade(matrix):
    disposition = json.loads((V1_DIR / "evidence_disposition.json").read_text())
    assert disposition["current_evidence_status"] == "EVIDENCE_LIMITED_NOT_DECISION_GRADE"
    assert "THE_STUDY_VALIDATED_OR_CONFIRMED_THE_ACCEPTED_BASELINE" in disposition["barred_claims"]
    assert matrix["study_reconciliation"]["risk_0005_invalidation"]["status"] == \
        disposition["current_evidence_status"]


def test_v2_has_no_execution_results(matrix):
    contents = matrix["study_reconciliation"]["whole_portfolio_robustness_v2_contents"]
    assert not (V2_DIR / "execution").exists()
    assert contents["execution_directory"] is False
    assert contents["results"] is False
    assert contents["retained_decision_grade_results"] is False
    assert (V2_DIR / "PROTOCOL.md").is_file()
    assert (V2_DIR / "pre_registration.yaml").is_file()


def test_v2_input_admission_failed(matrix):
    admission = json.loads((V2_DIR / "validation" / "input_admission.json").read_text())
    assert admission["admitted"] is False
    assert admission["disposition"] == "INPUT_ADMISSION_FAILED"
    assert admission["historical_results_executed"] is False
    assert sorted(admission["errors"]) == sorted(
        matrix["study_reconciliation"]["whole_portfolio_robustness_v2_contents"]["blocking_errors"]
    )


def test_v2_frozen_inputs_are_unresolved(matrix):
    freeze = json.loads((V2_DIR / "inputs" / "input_freeze.json").read_text())
    assert freeze["dff_availability"]["status"] == "UNRESOLVED"
    assert freeze["dff_availability"]["substitution"] == "PROHIBITED"
    sol = next(c for c in freeze["crypto"] if c["symbol"] == "SOL")
    assert sol["provider"] == "UNRESOLVED_SINGLE_USD_SPOT_SOURCE"
    assert freeze["result_free"] is True


def test_v2_preregistration_requires_a_crypto_disposition_before_execution():
    prereg = yaml.safe_load((V2_DIR / "pre_registration.yaml").read_text())
    assert prereg["status"] == "PREREGISTERED_NOT_EXECUTED"
    assert prereg["frozen_inputs"]["crypto"] == "NEW_SUCCESSOR_DISPOSITION_REQUIRED_BEFORE_EXECUTION"


def test_determination_is_case_3_and_nothing_was_executed(matrix):
    det = matrix["determination"]
    assert det["phase_c_case"] == "CASE_3_NO_EXISTING_AUTHORITY_OR_STUDY_CAN_ANSWER"
    assert det["no_new_study_executed"] is True


def test_cluster_shaped_backtest_arm_never_ran(matrix):
    report = (HERE / "reports" / "t1t2_trim_backtest.md").read_text()
    assert "Arm D did not run" in report
    assert matrix["study_reconciliation"]["backtest_t1t2_trim_py"]["arm_d_cluster_ran"] is False


def test_no_study_calibrated_any_cap_or_ceiling(matrix):
    calib = matrix["study_reconciliation"]["cap_calibration"]
    assert set(calib.values()) == {False}


# ── protected paths must be untouched by this unit ──────────────────────────

@pytest.mark.parametrize("protected", [
    "targets.yaml", "issuer_lookthrough.yaml", "gates.yaml", "holdings.yaml",
    "allocate.py", "levels.py", "margin_state.py",
])
def test_protected_path_is_not_written_by_this_unit(protected):
    """This unit adds evidence only. These files must exist and are never
    modified by anything in research/current_architecture_validation/."""
    assert (HERE / protected).is_file()
    for artifact in ARTIFACT_DIR.rglob("*"):
        if artifact.is_file():
            assert artifact.suffix in {".md", ".json"}, \
                f"only documentation artifacts belong here, found {artifact.name}"


def test_provenance_audit_predates_and_omits_the_lookthrough_controls(matrix):
    """The repository's own numeric-parameter provenance audit never covered the
    8% issuer or 40% common-driver ceilings, because it predates the file that
    introduced them."""
    rec = matrix["derived_measurements"]["provenance_audit_coverage"]
    text = (HERE / "docs" / "NUMERIC_PARAMETER_PROVENANCE_AUDIT.md").read_text().lower()
    assert text.count("issuer") == rec["occurrences_of_issuer"] == 0
    assert text.count("common-driver") == rec["occurrences_of_common_driver"] == 0
    assert "look-through" not in text and "lookthrough" not in text
    assert rec["audit_date"] in (HERE / "docs" / "NUMERIC_PARAMETER_PROVENANCE_AUDIT.md").read_text()
    assert rec["audit_predates_current_architecture"] is True


def test_policy_manual_also_predates_the_current_architecture():
    """docs/PORTFOLIO_POLICY_MANUAL.md still documents the retired tier era."""
    text = (HERE / "docs" / "PORTFOLIO_POLICY_MANUAL.md").read_text()
    assert "**As of:** 2026-07-18" in text
    assert "T1/T2 concentration ceiling" in text, \
        "manual no longer describes the retired T1/T2 ceiling — staleness finding needs revisiting"
