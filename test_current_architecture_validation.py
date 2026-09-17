"""Verification tests for the current-architecture target/concentration evidence matrix.

`research/current_architecture_validation/evidence_matrix.json` is a DATED
EVIDENCE SNAPSHOT, not policy and not authority. These tests exist so that none
of its load-bearing claims can be believed on the artifact's own say-so.

Reconciliation basis
--------------------
Every substantive claim is re-derived against the artifact's OWN PINNED BASE
COMMIT (`base_commit` in the matrix), read read-only out of git — never against
the live working tree. That is deliberate and is the whole point:

    CURRENT-ARCH-VALIDATION-0001 is a historical record of what was true at its
    stated basis. A later, legitimate change to live repository inputs — a
    refreshed `issuer_lookthrough.yaml`, a defined common-driver inclusion rule,
    an executed successor robustness study, an authorized target or cap change —
    does not make that historical record false, and must NOT by itself turn
    repository CI red.

Verifying against the pinned basis keeps the check permanently strong (it still
proves the artifact was internally coherent and matched its basis when created)
while decoupling a historical research record from future live policy. The
artifact is never rewritten to current values.

The artifact files themselves are read from the working tree, because they are
this pull request's own content and do not exist at the base commit.

If the base commit object is unavailable (a shallow clone that does not reach
it), the basis-dependent tests skip with an explicit reason rather than failing
— that is an environment limitation, not evidence of a defect. Full-history CI
still exercises the stronger check.

These tests read only. They change no target, cap, ceiling, cluster, gate,
margin parameter, holding, or allocator behaviour, execute no study, acquire no
data, and make no allocation recommendation.
"""

from __future__ import annotations

import ast
import itertools
import json
import subprocess
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
ARTIFACT_DIR = HERE / "research" / "current_architecture_validation"
MATRIX_PATH = ARTIFACT_DIR / "evidence_matrix.json"
REPORT_PATH = ARTIFACT_DIR / "EVIDENCE_MATRIX.md"

DUE_DILIGENCE_PATH = (
    "governance/evidence/PHQ-2026-01/final_due_diligence/"
    "Portfolio_HQ_Final_Due_Diligence_and_Approval_v1_32.json"
)
V2_PREFIX = "research/whole_portfolio_robustness_v2"
V1_PREFIX = "research/whole_portfolio_robustness"

TOL = 1e-9

#: Live paths whose content the snapshot's substantive claims were derived from.
#: Used only to REPORT whether live state still matches the basis. Drift here is
#: expected over time and is never a test failure.
SNAPSHOT_SOURCE_PATHS = (
    "targets.yaml",
    "issuer_lookthrough.yaml",
    DUE_DILIGENCE_PATH,
    f"{V1_PREFIX}/evidence_disposition.json",
    f"{V2_PREFIX}/validation/input_admission.json",
    f"{V2_PREFIX}/inputs/input_freeze.json",
    f"{V2_PREFIX}/pre_registration.yaml",
    "docs/NUMERIC_PARAMETER_PROVENANCE_AUDIT.md",
    "docs/PORTFOLIO_POLICY_MANUAL.md",
    "reports/t1t2_trim_backtest.md",
)

_MATRIX = json.loads(MATRIX_PATH.read_text())
SNAPSHOT_BASE_COMMIT = _MATRIX["base_commit"]


def _snapshot_text(path: str) -> str | None:
    """Read `path` as of the artifact's pinned base commit, or None."""
    try:
        proc = subprocess.run(
            ["git", "show", f"{SNAPSHOT_BASE_COMMIT}:{path}"],
            cwd=HERE, capture_output=True, text=True, check=False,
        )
    except OSError:  # pragma: no cover - git binary absent
        return None
    return proc.stdout if proc.returncode == 0 else None


def _base_commit_available() -> bool:
    try:
        proc = subprocess.run(
            ["git", "cat-file", "-e", f"{SNAPSHOT_BASE_COMMIT}^{{commit}}"],
            cwd=HERE, capture_output=True, text=True, check=False,
        )
    except OSError:  # pragma: no cover - git binary absent
        return False
    return proc.returncode == 0


BASE_AVAILABLE = _base_commit_available()

requires_snapshot_basis = pytest.mark.skipif(
    not BASE_AVAILABLE,
    reason=(
        f"snapshot base commit {SNAPSHOT_BASE_COMMIT[:12]} is not reachable in this "
        "clone (shallow checkout); historical-basis reconciliation is skipped here "
        "and is exercised by full-history CI"
    ),
)


def snapshot_text(path: str) -> str:
    """Basis content for `path`, skipping the test if it cannot be read."""
    text = _snapshot_text(path)
    if text is None:
        pytest.skip(f"{path} not readable at snapshot base commit {SNAPSHOT_BASE_COMMIT[:12]}")
    return text


def live_basis_drift() -> tuple[str, tuple[str, ...]]:
    """Classify live state against the snapshot basis. Informational only."""
    if not BASE_AVAILABLE:
        return "BASE_UNAVAILABLE", ()
    drifted = []
    for path in SNAPSHOT_SOURCE_PATHS:
        basis = _snapshot_text(path)
        live_path = HERE / path
        live = live_path.read_text() if live_path.is_file() else None
        if basis != live:
            drifted.append(path)
    return ("MATCHES_BASIS" if not drifted else "DRIFTED_FROM_BASIS"), tuple(drifted)


# ── fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def matrix() -> dict:
    return json.loads(MATRIX_PATH.read_text())


@pytest.fixture(scope="module")
def targets() -> dict:
    return yaml.safe_load(snapshot_text("targets.yaml"))


@pytest.fixture(scope="module")
def due_diligence() -> dict:
    return json.loads(snapshot_text(DUE_DILIGENCE_PATH))


@pytest.fixture(scope="module")
def concentration(tmp_path_factory):
    """Production-helper exposure at the snapshot basis' canonical target weights.

    Reuses `currentness_report.collect_target_weight_concentration`, which in
    turn delegates the look-through arithmetic to `allocate._issuer_exposure`.
    Deliberately NOT re-implemented here — a second implementation would prove
    only that two copies of the same mistake agree.

    The two config inputs are materialised read-only from the pinned base
    commit into a temporary directory, so this reconciliation is unaffected by
    any later legitimate change to the live files.
    """
    import currentness_report as cr

    basis_dir = tmp_path_factory.mktemp("snapshot_basis")
    targets_path = basis_dir / "targets.yaml"
    lookthrough_path = basis_dir / "issuer_lookthrough.yaml"
    targets_path.write_text(snapshot_text("targets.yaml"))
    lookthrough_path.write_text(snapshot_text("issuer_lookthrough.yaml"))

    result = cr.collect_target_weight_concentration(
        targets_path=targets_path, lookthrough_path=lookthrough_path,
    )
    assert result.available, f"production exposure helper unavailable: {result.detail}"
    return result


def _param(matrix: dict, name_fragment: str) -> dict:
    hits = [p for p in matrix["parameters"] if name_fragment.lower() in p["parameter"].lower()]
    assert len(hits) == 1, f"expected exactly one parameter matching {name_fragment!r}, got {len(hits)}"
    return hits[0]


# ── artifact shape and scope safety (always run) ────────────────────────────

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
    """The artifact's central negative finding, as of its stated basis."""
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


def test_this_module_never_writes_outside_pytest_scratch_space():
    """AST proof that this module performs no destructive filesystem call, and
    that every write it does make is confined to pytest-managed scratch space.

    The `concentration` fixture materialises the base-commit config files, and
    one adversarial test writes a mutated fixture; both must live under
    `tmp_path` / `tmp_path_factory`, never a repository path.
    """
    tree = ast.parse(Path(__file__).read_text())

    destructive = [
        name for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        for name in [getattr(node.func, "attr", None) or getattr(node.func, "id", None)]
        if name in {"unlink", "rmtree", "rmdir", "remove", "chmod"}
    ]
    assert destructive == [], f"destructive call(s) present: {destructive}"

    writes = {"write_text", "write_bytes", "open", "mkdir"}
    scratch = {"tmp_path", "tmp_path_factory"}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        used = {
            name for sub in ast.walk(node)
            if isinstance(sub, ast.Call)
            for name in [getattr(sub.func, "attr", None) or getattr(sub.func, "id", None)]
            if name in writes
        }
        if not used:
            continue
        params = {a.arg for a in node.args.args}
        assert params & scratch, (
            f"{node.name} calls {sorted(used)} without a pytest scratch fixture "
            "in scope — a write could land on a repository path"
        )


def test_matrix_documents_its_own_verification_semantics(matrix):
    """The artifact must state that it is reconciled against its pinned basis
    and is not a gate on future live state."""
    semantics = matrix["verification_semantics"]
    assert semantics["reconciliation_basis"] == "PINNED_BASE_COMMIT"
    assert semantics["future_live_drift_fails_ci"] is False
    assert semantics["historical_values_rewritten_to_current"] is False


# ── snapshot-basis reconciliation (skips only if the basis is unreachable) ──

@requires_snapshot_basis
def test_targets_yaml_had_no_tiers_key_at_the_snapshot_basis(targets):
    """The structural fact that orphaned every tier-era backtest."""
    assert "tiers" not in targets


@requires_snapshot_basis
def test_tier_era_backtests_depended_on_the_absent_tiers_key(matrix):
    affected = matrix["study_reconciliation"]["tier_dependency_finding"]["affected_scripts"]
    assert set(affected) == {
        "backtest_weights.py", "backtest_t1t2_trim.py", "backtest_trend.py",
        "backtest_regime.py", "backtest_rungs.py", "backtest_trims.py",
    }
    direct = {"backtest_regime.py", "backtest_rungs.py", "backtest_trims.py"}
    for script in affected:
        text = snapshot_text(script)
        if script in direct:
            assert '["tiers"]' in text, f"{script} did not read targets.yaml['tiers'] at basis"
        else:
            assert "from backtest_regime import" in text or "from backtest_trims import" in text, \
                f"{script} did not inherit its roster from a tier-reading module at basis"


@requires_snapshot_basis
def test_destination_rows_and_total_match_the_artifact(matrix, targets):
    rows = targets["destination"]
    total = sum(float(r["target_pct"]) for r in rows)
    derived = matrix["derived_measurements"]
    assert len(rows) == derived["destination_rows"]
    assert abs(total - derived["destination_total_pct"]) < TOL
    assert derived["targets_yaml_has_tiers_key"] is False
    assert "99.25" in _param(matrix, "canonical destination")["current_value"]


@requires_snapshot_basis
def test_current_weights_are_numerically_identical_to_the_retained_source(targets, due_diligence):
    """Provenance check for all 36 weights.

    This proves NUMERIC / ECONOMIC identity after parsing, not byte identity:
    both sides are compared as floats, and the retained JSON carries
    representations such as 3.5000000000000004 that are economically equal to
    the YAML's 3.50 without being byte-identical.
    """
    current = {r["ticker"].upper(): float(r["target_pct"]) for r in targets["destination"]}
    retained = {
        r["ticker"].strip().upper(): float(r["target_weight_percent"])
        for r in due_diligence["architecture_rows"]
    }
    assert set(retained) - set(current) == {"SPCX"}
    assert set(current) - set(retained) == set()
    mismatched = [t for t in set(current) & set(retained) if abs(current[t] - retained[t]) > TOL]
    assert mismatched == [], f"weights differ from retained source: {mismatched}"
    assert abs(sum(retained.values()) - 100.0) < TOL
    assert abs(sum(current.values()) - 99.25) < TOL


@requires_snapshot_basis
def test_retained_source_is_not_byte_identical_only_numerically_identical(due_diligence):
    """Pins the precision of the claim above: at least one retained value is
    numerically equal to its YAML counterpart without sharing its text form."""
    retained_raw = {
        r["ticker"].strip().upper(): r["target_weight_percent"]
        for r in due_diligence["architecture_rows"]
    }
    yaml_rows = yaml.safe_load(snapshot_text("targets.yaml"))["destination"]
    yaml_raw = {r["ticker"].upper(): r["target_pct"] for r in yaml_rows}
    differing_text = [
        t for t in set(retained_raw) & set(yaml_raw)
        if repr(retained_raw[t]) != repr(yaml_raw[t])
        and abs(float(retained_raw[t]) - float(yaml_raw[t])) < TOL
    ]
    assert differing_text, (
        "expected at least one numerically-equal / textually-different value; "
        "if none remains, the 'numeric not byte identity' wording can be revisited"
    )


@requires_snapshot_basis
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


@requires_snapshot_basis
def test_oil_cluster_is_dead_configuration_not_a_satisfied_limit(concentration):
    oil = next(c for c in concentration.clusters if c.name == "oil")
    assert oil.members == ()
    assert oil.status == "UNAVAILABLE", "a zero-member cap must never report OK"


@requires_snapshot_basis
def test_semis_and_power_infra_are_non_binding_at_target_weights(concentration):
    util = {c.name: c.utilisation_pct for c in concentration.clusters}
    assert util["semis"] < 100.0
    assert util["power_infra"] < 100.0


@requires_snapshot_basis
def test_max_issuer_matches_the_artifact(matrix, concentration):
    rec = matrix["derived_measurements"]["max_issuer"]
    live = concentration.max_issuer
    assert live.ticker == rec["ticker"]
    for field in ("direct_pct", "embedded_pct", "effective_pct", "ceiling_pct", "headroom_pct"):
        assert abs(getattr(live, field) - rec[field]) < TOL, field


@requires_snapshot_basis
def test_common_driver_recomputation_matches_the_artifact(matrix, concentration):
    rec = matrix["derived_measurements"]["common_driver"]
    live = concentration.common_driver
    assert abs(live.recomputed_pct - rec["recomputed_pct"]) < 1e-6
    assert abs(live.ceiling_pct - rec["ceiling_pct"]) < TOL
    assert abs(live.retained_value_pct - rec["retained_value_pct"]) < TOL
    assert live.reconciles is False
    assert live.limit_status == "OVER_LIMIT"


# ── the retained-evidence reconciliation ────────────────────────────────────

@requires_snapshot_basis
def test_retained_lookthrough_line_items_equal_the_recomputation_at_basis(
    due_diligence, concentration
):
    """The core reconciliation: the discrepancy is NOT configuration drift."""
    line_item_sum = sum(r["effective_weight"] for r in due_diligence["lookthrough_exposure"]) * 100.0
    assert abs(line_item_sum - concentration.common_driver.recomputed_pct) < 1e-6


@requires_snapshot_basis
def test_retained_headline_is_inconsistent_with_its_own_line_items(due_diligence):
    rows = due_diligence["lookthrough_exposure"]
    headline = due_diligence["lookthrough_summary"]["effective_ai_platform_common_driver_estimate"]
    total = sum(r["effective_weight"] for r in rows)
    assert abs(total - headline) > 1e-6
    assert abs((total - headline) * 100.0 - 1.6170) < 1e-6


@requires_snapshot_basis
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


@requires_snapshot_basis
def test_retained_mega6_is_reproducible_from_the_same_line_items(due_diligence):
    """Corroborates that the line items — not the headline — are the reliable part."""
    rows = {r["issuer"]: r["effective_weight"] for r in due_diligence["lookthrough_exposure"]}
    mega6 = ["NVDA", "MSFT", "AMZN", "Alphabet (GOOGL+GOOG)", "AVGO", "META"]
    assert abs(sum(rows[n] for n in mega6)
               - due_diligence["lookthrough_summary"]["effective_mega6_weight"]) < TOL


@requires_snapshot_basis
def test_retained_nvda_effective_weight_reproduces_exactly(due_diligence, concentration):
    retained_nvda = next(
        r for r in due_diligence["lookthrough_exposure"] if r["issuer"] == "NVDA"
    )["effective_weight"]
    assert abs(retained_nvda * 100.0 - concentration.max_issuer.effective_pct) < 1e-9


# ── study status at the snapshot basis ──────────────────────────────────────

@requires_snapshot_basis
def test_v1_study_is_classified_not_decision_grade(matrix):
    disposition = json.loads(snapshot_text(f"{V1_PREFIX}/evidence_disposition.json"))
    assert disposition["current_evidence_status"] == "EVIDENCE_LIMITED_NOT_DECISION_GRADE"
    assert "THE_STUDY_VALIDATED_OR_CONFIRMED_THE_ACCEPTED_BASELINE" in disposition["barred_claims"]
    assert matrix["study_reconciliation"]["risk_0005_invalidation"]["status"] == \
        disposition["current_evidence_status"]


@requires_snapshot_basis
def test_v2_had_no_execution_results_at_basis(matrix):
    contents = matrix["study_reconciliation"]["whole_portfolio_robustness_v2_contents"]
    listing = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", SNAPSHOT_BASE_COMMIT, f"{V2_PREFIX}/"],
        cwd=HERE, capture_output=True, text=True, check=False,
    )
    assert listing.returncode == 0
    paths = listing.stdout.split()
    assert not any(p.startswith(f"{V2_PREFIX}/execution/") for p in paths)
    assert contents["execution_directory"] is False
    assert contents["results"] is False
    assert contents["retained_decision_grade_results"] is False
    assert f"{V2_PREFIX}/PROTOCOL.md" in paths
    assert f"{V2_PREFIX}/pre_registration.yaml" in paths


@requires_snapshot_basis
def test_v2_input_admission_failed(matrix):
    admission = json.loads(snapshot_text(f"{V2_PREFIX}/validation/input_admission.json"))
    assert admission["admitted"] is False
    assert admission["disposition"] == "INPUT_ADMISSION_FAILED"
    assert admission["historical_results_executed"] is False
    assert sorted(admission["errors"]) == sorted(
        matrix["study_reconciliation"]["whole_portfolio_robustness_v2_contents"]["blocking_errors"]
    )


@requires_snapshot_basis
def test_v2_frozen_inputs_are_unresolved():
    freeze = json.loads(snapshot_text(f"{V2_PREFIX}/inputs/input_freeze.json"))
    assert freeze["dff_availability"]["status"] == "UNRESOLVED"
    assert freeze["dff_availability"]["substitution"] == "PROHIBITED"
    sol = next(c for c in freeze["crypto"] if c["symbol"] == "SOL")
    assert sol["provider"] == "UNRESOLVED_SINGLE_USD_SPOT_SOURCE"
    assert freeze["result_free"] is True


@requires_snapshot_basis
def test_v2_preregistration_requires_a_crypto_disposition_before_execution():
    prereg = yaml.safe_load(snapshot_text(f"{V2_PREFIX}/pre_registration.yaml"))
    assert prereg["status"] == "PREREGISTERED_NOT_EXECUTED"
    assert prereg["frozen_inputs"]["crypto"] == "NEW_SUCCESSOR_DISPOSITION_REQUIRED_BEFORE_EXECUTION"


def test_determination_is_case_3_and_nothing_was_executed(matrix):
    det = matrix["determination"]
    assert det["phase_c_case"] == "CASE_3_NO_EXISTING_AUTHORITY_OR_STUDY_CAN_ANSWER"
    assert det["no_new_study_executed"] is True


@requires_snapshot_basis
def test_cluster_shaped_backtest_arm_never_ran(matrix):
    report = snapshot_text("reports/t1t2_trim_backtest.md")
    assert "Arm D did not run" in report
    assert matrix["study_reconciliation"]["backtest_t1t2_trim_py"]["arm_d_cluster_ran"] is False


def test_no_study_calibrated_any_cap_or_ceiling(matrix):
    calib = matrix["study_reconciliation"]["cap_calibration"]
    assert set(calib.values()) == {False}


@requires_snapshot_basis
def test_provenance_audit_predates_and_omits_the_lookthrough_controls(matrix):
    """The repository's own numeric-parameter provenance audit never covered the
    8% issuer or 40% common-driver ceilings, because it predates the file that
    introduced them."""
    rec = matrix["derived_measurements"]["provenance_audit_coverage"]
    raw = snapshot_text("docs/NUMERIC_PARAMETER_PROVENANCE_AUDIT.md")
    text = raw.lower()
    assert text.count("issuer") == rec["occurrences_of_issuer"] == 0
    assert text.count("common-driver") == rec["occurrences_of_common_driver"] == 0
    assert "look-through" not in text and "lookthrough" not in text
    assert rec["audit_date"] in raw
    assert rec["audit_predates_current_architecture"] is True


@requires_snapshot_basis
def test_policy_manual_also_predates_the_current_architecture():
    """docs/PORTFOLIO_POLICY_MANUAL.md documented the retired tier era at basis."""
    text = snapshot_text("docs/PORTFOLIO_POLICY_MANUAL.md")
    assert "**As of:** 2026-07-18" in text
    assert "T1/T2 concentration ceiling" in text


# ── the snapshot must not become a live-policy gate ─────────────────────────

def test_artifact_dir_holds_documentation_only():
    for artifact in ARTIFACT_DIR.rglob("*"):
        if artifact.is_file():
            assert artifact.suffix in {".md", ".json"}, \
                f"only documentation artifacts belong here, found {artifact.name}"


@requires_snapshot_basis
@pytest.mark.parametrize("protected", [
    "targets.yaml", "issuer_lookthrough.yaml", "gates.yaml", "holdings.yaml",
    "allocate.py", "levels.py", "margin_state.py",
])
def test_protected_path_existed_at_basis_and_is_not_written_by_this_unit(protected):
    """This unit adds evidence only. Existence is asserted at the snapshot basis
    so that a later authorized rename or removal is not converted into a CI
    failure owned by a historical research record."""
    assert _snapshot_text(protected) is not None


def test_live_basis_drift_is_reported_but_never_fatal():
    """A legitimate future change to live inputs must not fail this suite.

    This test records the live-versus-basis classification and asserts only that
    it is one of the known values. It passes whether live state still matches the
    snapshot basis or has since drifted — that is precisely the decoupling.
    """
    status, drifted = live_basis_drift()
    assert status in {"MATCHES_BASIS", "DRIFTED_FROM_BASIS", "BASE_UNAVAILABLE"}
    assert isinstance(drifted, tuple)
    if status == "DRIFTED_FROM_BASIS":
        assert drifted, "DRIFTED_FROM_BASIS must name the drifted paths"


@requires_snapshot_basis
def test_snapshot_reconciliation_ignores_live_working_tree_content(tmp_path):
    """Adversarial proof of the decoupling mechanism.

    Writing a mutated copy of a snapshot source into a scratch directory must not
    change what `snapshot_text` returns, because it reads from the pinned base
    commit rather than from any working-tree file.
    """
    basis = snapshot_text("issuer_lookthrough.yaml")
    mutated = basis.replace("fund_holding_weight: 0.0190", "fund_holding_weight: 0.0205")
    assert mutated != basis, "fixture no longer representative of a PD-2 style refresh"
    (tmp_path / "issuer_lookthrough.yaml").write_text(mutated)

    assert snapshot_text("issuer_lookthrough.yaml") == basis
    assert "fund_holding_weight: 0.0190" in snapshot_text("issuer_lookthrough.yaml")


def test_matrix_records_that_drift_does_not_invalidate_the_snapshot(matrix):
    semantics = matrix["verification_semantics"]
    assert semantics["live_drift_disposition"] == "HISTORICAL_RECORD_REMAINS_TRUE"

    # The correction must not smuggle in a lifecycle framework. The artifact
    # declares this explicitly, and nothing in the repository implements one.
    declared = [item.lower() for item in semantics["not_introduced"]]
    for absent in ("lifecycle", "supersession", "governance decision", "latest-artifact"):
        assert any(absent in item for item in declared), \
            f"artifact does not disclaim introducing a {absent} mechanism"
    assert all(item.startswith("no ") for item in declared)
    assert not (ARTIFACT_DIR / "registry.yaml").exists()
    assert not (ARTIFACT_DIR / "lifecycle.yaml").exists()
