"""Adversarial tests for the XASSET-0036 SS-G.B steps-2-7 executable package.

Every test pins an authorized boundary AND its nearest plausible overreach, so a regression in
either direction fails rather than passing quietly.

EXECUTION BOUNDARY OBSERVED THROUGHOUT
======================================

``XASSET-0036`` SS-F.1 draws the line precisely: *accessing and traversing the frozen construction
identities is not execution; applying gate-evaluation semantics to those identities to derive
Stage-1 outcomes is execution.*

This module therefore:

* uses the REAL frozen 680 only for read-only structural traversal, ordering, inventory, identity,
  and pair-consumption checks -- SS-F.1(a);
* uses SYNTHETIC constructions and an injected authorizer for everything that composes a gate
  result, a disposition, a cell outcome, or a roll-up -- SS-F.1(b);
* never writes ``stage1_results.yaml``, never touches ``AUTHORIZATION_ROOT``, never creates an
  attestation, and never claims ``ATTEMPT_1``.

A dedicated test at the end asserts those last properties directly rather than by convention.
"""

from __future__ import annotations

import ast
import copy
import inspect
from pathlib import Path

import pytest

import level1_construction_universe_closure_validator as CU
import level1_endpoint_evidence_preregistration_validator as PV
import level1_stage1_execution_authorization as AUTH
import level1_stage1_result_validator as RV
import level1_stage1_runner as R

ROOT = Path(__file__).resolve().parent

XASSET_0029_DECISION_RELPATH = (
    "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md"
)

# A synthetic sleeve name that is NOT a member of the canonical four, so no synthetic construction
# id can collide with a real registered identity. An earlier draft of this module used "equity",
# which produced ids that ARE registered -- and every composition test would then have derived a
# disposition for a real construction, which XASSET-0036 SS-F.1(b) prohibits. The final test in this
# module asserts the absence of that collision directly rather than trusting the naming convention.
SYNTHETIC_SLEEVE = "zz_synthetic_sleeve"
SYNTHETIC_CELL = f"{SYNTHETIC_SLEEVE}::LOWER::portfolio_function"


@pytest.fixture(scope="module")
def base_prereg() -> dict:
    """The committed canonical pre-registration, parsed. Never mutated."""
    import yaml

    return yaml.safe_load(PV.PREREG_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def prereg(base_prereg: dict) -> dict:
    """A deep copy, safe to mutate adversarially."""
    return copy.deepcopy(base_prereg)


def _synthetic_record(family_id: str, counterpart: str | None = None) -> dict:
    """A synthetic construction. Deliberately NOT a registered identity's outcome surface."""
    suffix = "SELF" if counterpart is None else f"ALT__{counterpart}"
    return {
        "construction_id": f"{SYNTHETIC_CELL}::{family_id}::{suffix}",
        "cell_id": SYNTHETIC_CELL,
        "sleeve": SYNTHETIC_SLEEVE,
        "bound": "LOWER",
        "driver_class": "portfolio_function",
        "family_id": family_id,
        "route": "R1",
        "num_0001_class": 1,
        "comparison_subject_kind": "SLEEVE_SELF" if counterpart is None else "DIRECT_ALTERNATIVE",
        "counterpart": counterpart,
        "unordered_pair_id": None,
        "source_architecture": "HYPOTHETICAL_SOURCE_ARCHITECTURE",
        "hypothetical_source_requirements": "synthetic requirement",
        "governing_authority_refs": ["XASSET-0024_SECTION_J"],
    }


SYNTHETIC_TRAVERSAL = [_synthetic_record("R1_C1"), _synthetic_record("R1_C3", "crypto")]


def _input(**overrides) -> dict:
    base = {
        "gate_results": {gate: "PASS" for gate in R.EXECUTOR_SUPPLIED_GATES},
        "g2_outcome_under_subject_matter_reading": "PASSES",
        "g2_outcome_under_preference_only_reading": "FAILS",
        "g9_path_1_declaration": "UNDETERMINED",
        "g9_named_dependency": None,
        "g12_basis": "LAWFUL_SUCCESSOR_IDENTIFIABLE",
        "point_or_range_support": "WOULD_SUPPORT_RANGE_ENDPOINT",
        "uncertainty_statement": "synthetic",
    }
    base.update(overrides)
    return base


def _provenance() -> dict:
    manifest = {field: "recorded" for field in RV.PROVENANCE_REQUIRED_FIELDS}
    manifest.update(
        {
            "execution_attempt_id": R.EXECUTION_ATTEMPT_ID,
            "candidates_expected": len(SYNTHETIC_TRAVERSAL),
            "candidates_evaluated": len(SYNTHETIC_TRAVERSAL),
            "cells_expected": 1,
            "cells_evaluated": 1,
        }
    )
    return manifest


def _run(inputs=None, traversal=None):
    traversal = SYNTHETIC_TRAVERSAL if traversal is None else traversal
    inputs = (
        {record["construction_id"]: _input() for record in traversal}
        if inputs is None
        else inputs
    )
    return R._compose_synthetic_stage1_document(
        inputs,
        provenance=_provenance(),
        traversal=traversal,
        cell_universe=[SYNTHETIC_CELL],
    )


def _validate(document, traversal=None):
    return RV.validate_stage1_result_document(
        document,
        traversal=SYNTHETIC_TRAVERSAL if traversal is None else traversal,
        expected_cells=[SYNTHETIC_CELL],
        roll_up_unit_count=1,
    )


# ======================================================================================
# Canonical reconciliation -- XASSET-0035 SS-E/SS-F/SS-G transcribed (SS-G.B step 2)
# ======================================================================================


class TestCanonicalReconciliation:
    def test_the_committed_canonical_artifacts_validate_clean(self):
        assert PV.validate_file().ok, PV.validate_file().errors

    def test_all_three_semantic_blocks_are_present(self, base_prereg):
        assert "g12_modal_register" in base_prereg
        assert "pair_consumption_rule" in base_prereg
        assert "reserved_gate_recording_posture" in base_prereg

    # ---- B1 ----------------------------------------------------------------------------
    def test_b1_register_is_lawful_satisfiability(self, base_prereg):
        register = base_prereg["g12_modal_register"]
        assert register["register"] == "LAWFUL_SATISFIABILITY_OF_THE_FROZEN_CONSTRUCTION_SPECIFICATION"
        assert register["rejected_register"] == "EXECUTION_TIME_WORLD_STATE"

    def test_b1_alternate_tense_reintroduced_is_rejected(self, prereg):
        """The competing world-state reading may not return through the canonical file."""
        prereg["g12_modal_register"]["register"] = "EXECUTION_TIME_WORLD_STATE"
        assert not PV.validate(prereg).ok

    def test_b1_is_g12_scoped_and_a_program_wide_rule_is_rejected(self, prereg):
        assert prereg["g12_modal_register"]["scope"] == "G12_ONLY"
        prereg["g12_modal_register"]["is_program_wide_gate_modal_rule"] = True
        assert not PV.validate(prereg).ok

    def test_b1_nonexistence_floor_may_not_be_dropped(self, prereg):
        prereg["g12_modal_register"]["successor_nonexistence_alone_is_never_a_fail_ground"] = False
        assert not PV.validate(prereg).ok

    def test_b1_identifiability_only_may_not_be_dropped(self, prereg):
        prereg["g12_modal_register"]["identifiability_only"] = False
        assert not PV.validate(prereg).ok

    def test_b1_could_admit_clause_may_not_be_dissolved(self, prereg):
        prereg["g12_modal_register"]["could_admit_clause_remains_operative"] = False
        assert not PV.validate(prereg).ok

    # ---- B2 ----------------------------------------------------------------------------
    def test_b2_is_determined_by_frozen_identity_not_the_label(self, base_prereg):
        rule = base_prereg["pair_consumption_rule"]
        assert rule["determined_by"] == "FROZEN_COMPARISON_IDENTITY"
        assert rule["never_determined_by"] == "UNORDERED_PAIR_ID_LABEL"

    def test_b2_label_based_consumption_is_rejected(self, prereg):
        prereg["pair_consumption_rule"]["determined_by"] = "UNORDERED_PAIR_ID_LABEL"
        assert not PV.validate(prereg).ok

    def test_b2_permitting_transitive_consumption_is_rejected(self, prereg):
        prereg["pair_consumption_rule"]["transitive_consumption_permitted"] = True
        assert not PV.validate(prereg).ok

    def test_b2_permitting_relabelling_is_rejected(self, prereg):
        prereg["pair_consumption_rule"]["relabelling_permitted"] = True
        assert not PV.validate(prereg).ok

    def test_b2_label_absence_inference_may_not_be_permitted(self, prereg):
        prereg["pair_consumption_rule"]["label_absence_is_not_evidence_of_non_consumption"] = False
        assert not PV.validate(prereg).ok

    def test_b2_inventory_totals_are_pinned(self, base_prereg):
        inventory = base_prereg["pair_consumption_rule"]["structural_inventory"]
        assert inventory["consuming_total"] == 480
        assert inventory["non_consuming_total"] == 200
        assert inventory["universe_total"] == 680

    @pytest.mark.parametrize("field,value", [("consuming_total", 481), ("non_consuming_total", 199)])
    def test_b2_drifted_totals_are_rejected(self, prereg, field, value):
        prereg["pair_consumption_rule"]["structural_inventory"][field] = value
        assert not PV.validate(prereg).ok

    def test_b2_rows_must_sum_to_their_declared_totals(self, prereg):
        """A row and a total may not drift apart while each looks individually plausible."""
        rows = prereg["pair_consumption_rule"]["structural_inventory"]["rows"]
        rows[0]["count"] = rows[0]["count"] + 1
        assert not PV.validate(prereg).ok

    def test_b2_claiming_a_non_consuming_group_consumes_is_rejected(self, prereg):
        rows = prereg["pair_consumption_rule"]["structural_inventory"]["rows"]
        for row in rows:
            if row["group"] == "SELF":
                row["consumes_canonical_pair"] = True
        assert not PV.validate(prereg).ok

    def test_b2_does_not_determine_g10_result(self, prereg):
        assert prereg["pair_consumption_rule"]["determines_g10_result"] is False
        prereg["pair_consumption_rule"]["determines_g10_result"] = True
        assert not PV.validate(prereg).ok

    # ---- B3 ----------------------------------------------------------------------------
    def test_b3_records_unable_to_determine(self, base_prereg):
        assert base_prereg["reserved_gate_recording_posture"]["recorded_value"] == "UNABLE_TO_DETERMINE"

    @pytest.mark.parametrize("value", ["PASS", "FAIL", "NOT_APPLICABLE"])
    def test_b3_any_other_recorded_value_is_rejected(self, prereg, value):
        prereg["reserved_gate_recording_posture"]["recorded_value"] = value
        assert not PV.validate(prereg).ok

    def test_b3_reaches_exactly_three_items(self, base_prereg):
        posture = base_prereg["reserved_gate_recording_posture"]
        assert [row["gate"] for row in posture["applies_to"]] == [
            "G3_NORMALIZATION",
            "G5_CONSTRAINT_SHAPE",
            "G9_REPRESENTATION",
        ]

    @pytest.mark.parametrize(
        "gate", ["G8_UNIQUENESS", "G10_PAIR_INDEPENDENCE", "G12_SNAPSHOT_ADMISSIBILITY_PATH"]
    )
    def test_b3_may_not_be_widened_to_the_excluded_gates(self, prereg, gate):
        """A broader B3 would silently decide B1 and B2 -- XASSET-0035 SS-G.4."""
        prereg["reserved_gate_recording_posture"]["applies_to"].append(
            {"gate": gate, "gate_class": "categorical", "reservation_authority": "X", "condition": "Y"}
        )
        assert not PV.validate(prereg).ok

    def test_b3_dropping_an_excluded_gate_from_the_scope_limit_is_rejected(self, prereg):
        prereg["reserved_gate_recording_posture"]["does_not_apply_to"] = ["G8_UNIQUENESS"]
        assert not PV.validate(prereg).ok

    def test_b3_g9_condition_is_the_undetermined_case_only(self, base_prereg):
        rows = base_prereg["reserved_gate_recording_posture"]["applies_to"]
        g9 = next(row for row in rows if row["gate"] == "G9_REPRESENTATION")
        assert g9["condition"] == "PATH_1_SELF_CONTAINMENT_UNDETERMINED"

    def test_b3_widening_g9_beyond_the_undetermined_case_is_rejected(self, prereg):
        rows = prereg["reserved_gate_recording_posture"]["applies_to"]
        for row in rows:
            if row["gate"] == "G9_REPRESENTATION":
                row["condition"] = "ALWAYS"
        assert not PV.validate(prereg).ok

    def test_b3_may_not_convert_a_determined_g9_failure(self, prereg):
        prereg["reserved_gate_recording_posture"][
            "determined_g9_path_1_failure_remains_prerequisite_blocked"
        ] = False
        assert not PV.validate(prereg).ok

    def test_b3_may_not_generalize_the_g2_reading_mapping(self, prereg):
        prereg["reserved_gate_recording_posture"]["generalizes_g2_reading_mapping"] = True
        assert not PV.validate(prereg).ok

    def test_b3_may_not_change_a_gate_class(self, prereg):
        prereg["reserved_gate_recording_posture"]["changes_any_gate_class"] = True
        assert not PV.validate(prereg).ok


# ======================================================================================
# The XASSET-0030 SS-C enforcement correction (SS-G.B step 3)
# ======================================================================================


class TestEnforcementCorrection:
    """Both directions. Neither the defect nor an over-permissive fix may return."""

    def _row(self, gates, disposition):
        universe_id = PV.generate_family_slot_grid()[0]
        sleeve, bound, driver_class, family_id = universe_id.split("::")
        family = {f[0]: f for f in PV.CONSTRUCTION_FAMILIES}[family_id]
        requirements = "a synthetic requirement"
        universe = {
            universe_id: {
                "cell_id": PV.cell_id_of(universe_id),
                "source_architecture": "HYPOTHETICAL_SOURCE_ARCHITECTURE",
                "source_path": None,
                "source_sha256": None,
                "hypothetical_source_requirements": requirements,
            }
        }
        row = {
            "construction_id": universe_id,
            "cell_id": PV.cell_id_of(universe_id),
            "sleeve": sleeve,
            "bound": bound,
            "driver_class": driver_class,
            "family_id": family_id,
            "route": family[1],
            "num_0001_class": family[2],
            "source_architecture": "HYPOTHETICAL_SOURCE_ARCHITECTURE",
            "source_path": None,
            "source_sha256": None,
            "hypothetical_source_requirements": requirements,
            "governing_authority_refs": ["XASSET-0024_SECTION_J"],
            "gate_results": gates,
            "categorical_failures": [g for g in PV.CATEGORICAL_GATES if gates.get(g) == "FAIL"],
            "prerequisite_failures": [g for g in PV.PREREQUISITE_GATES if gates.get(g) == "FAIL"],
            "disposition": disposition,
            "first_failing_gate_id": next(
                (g for g in PV.GATE_IDS if gates.get(g) == "FAIL"), None
            ),
            "g2_outcome_under_subject_matter_reading": "PASSES",
            "g2_outcome_under_preference_only_reading": "FAILS",
            "g2_outcome_is_reading_dependent": True,
            "point_or_range_support": "WOULD_SUPPORT_RANGE_ENDPOINT",
            "representation_dependency": None,
            "uncertainty_statement": "recorded",
            "g12_basis": (
                "NO_LAWFUL_SUCCESSOR_IDENTIFIABLE_ON_INDEPENDENT_GROUNDS"
                if gates.get("G12_SNAPSHOT_ADMISSIBILITY_PATH") == "FAIL"
                else "LAWFUL_SUCCESSOR_IDENTIFIABLE"
            ),
        }
        results = {
            "candidate_results": [row],
            "cell_results": [
                {
                    "cell_id": PV.cell_id_of(universe_id),
                    "outcome": PV.derive_cell_outcome([disposition]),
                }
            ],
            "disposition": "RECORDED",
        }
        return PV._validate_stage1_results_against_universe(results, universe)

    def _reading_dependent_gates(self):
        gates = {gate: "PASS" for gate in PV.GATE_IDS}
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
        return gates

    @pytest.mark.parametrize(
        "gate",
        [g for g in PV.CATEGORICAL_GATES if g != "G2_MAGNITUDE_INTRINSICALITY"],
    )
    def test_any_independent_categorical_failure_lawfully_derives_categorical(self, gate):
        """XASSET-0027 SS-M.1: '...unless a categorical gate independently fails'."""
        gates = self._reading_dependent_gates()
        gates[gate] = "FAIL"
        assert PV.derive_candidate_disposition(gates) == "BLOCKED_CATEGORICALLY"
        assert self._row(gates, "BLOCKED_CATEGORICALLY").ok

    def test_reading_dependence_alone_may_not_produce_a_categorical_disposition(self):
        result = self._row(self._reading_dependent_gates(), "BLOCKED_CATEGORICALLY")
        assert not result.ok
        assert any("reading-dependent" in error for error in result.errors)

    def test_reading_dependence_alone_still_derives_uncertainty(self):
        gates = self._reading_dependent_gates()
        assert PV.derive_candidate_disposition(gates) == "UNABLE_TO_DETERMINE"
        assert self._row(gates, "UNABLE_TO_DETERMINE").ok

    def test_a_prerequisite_failure_does_not_become_categorical(self):
        """Uncertainty still outranks a prerequisite failure -- precedence is unchanged."""
        gates = self._reading_dependent_gates()
        gates["G9_REPRESENTATION"] = "FAIL"
        assert PV.derive_candidate_disposition(gates) == "UNABLE_TO_DETERMINE"

    def test_gate_order_cannot_change_the_disposition(self):
        gates = self._reading_dependent_gates()
        gates["G10_PAIR_INDEPENDENCE"] = "FAIL"
        forward = PV.derive_candidate_disposition(dict(gates))
        reversed_order = PV.derive_candidate_disposition(dict(reversed(list(gates.items()))))
        assert forward == reversed_order == "BLOCKED_CATEGORICALLY"


# ======================================================================================
# Read-only structural traversal of the REAL frozen 680 -- XASSET-0036 SS-F.1(a)
# ======================================================================================


class TestRealFrozenTraversalStructural:
    def test_the_production_traversal_verifies_clean(self):
        ok, errors = R.verify_frozen_traversal()
        assert ok, errors

    def test_the_traversal_consumes_exactly_680(self):
        assert len(R.frozen_traversal()) == PV.REGISTERED_CONSTRUCTION_COUNT == 680

    def test_the_traversal_is_wired_to_the_frozen_universe_not_a_hand_built_copy(self):
        assert R.frozen_traversal() == CU.generate_construction_universe()

    def test_the_traversal_is_in_exact_canonical_order(self):
        assert tuple(
            str(record["construction_id"]) for record in R.frozen_traversal()
        ) == tuple(CU.frozen_construction_universe())

    def test_no_duplicate_construction(self):
        ids = [str(record["construction_id"]) for record in R.frozen_traversal()]
        assert len(set(ids)) == len(ids)

    def test_a_reordered_traversal_is_rejected(self):
        records = list(R.frozen_traversal())
        records[0], records[1] = records[1], records[0]
        ok, errors = R.verify_frozen_traversal(records)
        assert not ok and any("order" in error for error in errors)

    def test_a_duplicated_construction_is_rejected(self):
        records = list(R.frozen_traversal())
        records[1] = records[0]
        ok, errors = R.verify_frozen_traversal(records)
        assert not ok and any("duplicate" in error for error in errors)

    def test_a_missing_construction_is_rejected(self):
        ok, errors = R.verify_frozen_traversal(list(R.frozen_traversal())[:-1])
        assert not ok and any("missing" in error or "length" in error for error in errors)

    def test_an_extra_unregistered_construction_is_rejected(self):
        records = list(R.frozen_traversal()) + [_synthetic_record("R1_C1", "crypto")]
        ok, errors = R.verify_frozen_traversal(records)
        assert not ok and any("unregistered" in error or "length" in error for error in errors)

    def test_a_relabelled_identity_field_is_rejected(self):
        records = [dict(record) for record in R.frozen_traversal()]
        records[0]["family_id"] = "R2_C2"
        ok, errors = R.verify_frozen_traversal(records)
        assert not ok and any("immutable" in error for error in errors)

    def test_the_universe_hash_is_verified(self):
        assert CU.universe_aggregate_sha256() == AUTH.CONSTRUCTION_UNIVERSE_SHA256

    def test_identity_comparison_is_strict(self):
        assert R._identity_equal(["a", "b"], ("a", "b")) is True
        assert R._identity_equal(["a", "b"], ["b", "a"]) is False
        assert R._identity_equal("ab", ["a", "b"]) is False
        assert R._identity_equal(1, True) is False


class TestRealPairConsumptionInventory:
    """B2 recomputed from frozen identities. No gate is evaluated and no G10 result recorded."""

    def test_inventory_matches_the_accepted_480_200_split(self):
        inventory = R.pair_consumption_inventory()
        assert inventory["total"] == 680
        assert inventory["consuming"] == 480
        assert inventory["non_consuming"] == 200

    def test_all_six_canonical_pairs_carry_eighty_each(self):
        inventory = R.pair_consumption_inventory()
        assert inventory["distinct_pairs"] == 6
        assert set(inventory["per_pair"].values()) == {80}

    def test_consumption_is_never_read_from_the_label(self):
        """All 360 consuming DIRECT_ALTERNATIVE records carry NO unordered_pair_id."""
        consuming_alternatives = [
            record
            for record in R.frozen_traversal()
            if record["comparison_subject_kind"] == "DIRECT_ALTERNATIVE"
            and R.pair_consumption_of(record) is not None
        ]
        assert len(consuming_alternatives) == 360
        assert all(record["unordered_pair_id"] is None for record in consuming_alternatives)

    def test_a_label_only_record_does_not_consume(self):
        """Adding a label to a non-sleeve comparison may not create consumption."""
        probe = {"sleeve": "equity", "counterpart": None, "unordered_pair_id": "equity::crypto"}
        assert R.pair_consumption_of(probe) is None

    def test_consumption_is_not_transitive(self):
        """Only the construction's OWN two endpoints, never a pair reachable through a chain."""
        probe = {"sleeve": "equity", "counterpart": "crypto", "unordered_pair_id": None}
        assert R.pair_consumption_of(probe) == ("crypto", "equity")

    def test_a_non_sleeve_counterpart_does_not_consume(self):
        probe = {"sleeve": "equity", "counterpart": "UNSIZED_UNASSIGNED_CAPITAL"}
        assert R.pair_consumption_of(probe) is None

    def test_a_degenerate_self_pair_does_not_consume(self):
        probe = {"sleeve": "equity", "counterpart": "equity"}
        assert R.pair_consumption_of(probe) is None

    def test_no_construction_is_relabelled_by_computing_consumption(self):
        before = copy.deepcopy(list(R.frozen_traversal()))
        R.pair_consumption_inventory()
        after = list(R.frozen_traversal())
        assert [dict(record) for record in after] == [dict(record) for record in before]


# ======================================================================================
# The runner -- synthetic constructions only (SS-F.1(b) observed)
# ======================================================================================


class TestRunnerFailsClosed:
    def test_the_production_path_refuses_while_stage_1_is_unclaimed(self):
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            R.run_stage1({})
        assert "lawfully claimed execution" in str(excinfo.value)

    def test_the_real_new_execution_gate_is_false(self):
        authorized, _ = AUTH.new_execution_is_authorized()
        assert authorized is False

    def test_the_real_claimed_execution_gate_is_false(self):
        authorized, _ = AUTH.claimed_execution_is_authorized()
        assert authorized is False

    def test_partial_publication_is_refused(self):
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            R._compose_synthetic_stage1_document(
                {}, provenance=_provenance(), traversal=SYNTHETIC_TRAVERSAL,
                cell_universe=[SYNTHETIC_CELL],
            )
        assert "partial publication is prohibited" in str(excinfo.value)

    def test_an_unregistered_construction_is_refused(self):
        inputs = {record["construction_id"]: _input() for record in SYNTHETIC_TRAVERSAL}
        inputs["not::a::registered::construction::SELF"] = _input()
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            R._compose_synthetic_stage1_document(
                inputs, provenance=_provenance(), traversal=SYNTHETIC_TRAVERSAL,
                cell_universe=[SYNTHETIC_CELL],
            )
        assert "unregistered" in str(excinfo.value)


class TestProductionCompositionRequiresAClaim:
    """BLOCKING 1 (review 4953193650). The production path asks the CLAIMED question and has no
    injection seam; the synthetic seam cannot reach a registered construction."""

    def test_run_stage1_asks_the_claimed_question_not_the_ready_question(self):
        """Checked against the parsed CODE, so a docstring mentioning the other question by name
        cannot make this pass or fail."""
        tree = ast.parse(inspect.getsource(R.run_stage1).lstrip())
        called = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        assert "claimed_execution_is_authorized" in called
        assert "new_execution_is_authorized" not in called

    def test_run_stage1_accepts_no_authorizer_traversal_or_cell_universe_parameter(self):
        parameters = set(inspect.signature(R.run_stage1).parameters)
        assert parameters == {"analytical_inputs", "provenance"}

    def test_run_stage1_refuses_before_composing_any_row(self, monkeypatch):
        calls = []
        monkeypatch.setattr(
            R, "build_candidate_row", lambda *a, **k: calls.append(1) or {}
        )
        with pytest.raises(R.Stage1RunnerError):
            R.run_stage1({})
        assert calls == []

    def test_a_ready_but_unclaimed_lane_does_not_authorize_composition(self, monkeypatch):
        monkeypatch.setattr(AUTH, "new_execution_is_authorized", lambda *a, **k: (True, ""))
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            R.run_stage1({})
        assert "lawfully claimed execution" in str(excinfo.value)

    def test_the_synthetic_seam_refuses_a_none_traversal(self):
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            R._compose_synthetic_stage1_document(
                {}, traversal=None, cell_universe=[SYNTHETIC_CELL]
            )
        assert "explicit traversal" in str(excinfo.value)

    def test_the_synthetic_seam_refuses_a_registered_record(self):
        registered = sorted(R._registered_construction_ids())[0]
        record = dict(SYNTHETIC_TRAVERSAL[0])
        record["construction_id"] = registered
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            R._compose_synthetic_stage1_document(
                {registered: _input()},
                traversal=[record],
                cell_universe=[SYNTHETIC_CELL],
            )
        assert "may not name registered construction" in str(excinfo.value)

    def test_the_synthetic_seam_refuses_a_registered_analytical_input(self):
        registered = sorted(R._registered_construction_ids())[0]
        inputs = {record["construction_id"]: _input() for record in SYNTHETIC_TRAVERSAL}
        inputs[registered] = _input()
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            R._compose_synthetic_stage1_document(
                inputs, traversal=SYNTHETIC_TRAVERSAL, cell_universe=[SYNTHETIC_CELL]
            )
        assert "may not name registered construction" in str(excinfo.value)

    def test_the_synthetic_seam_is_private_and_the_public_one_is_not_reachable_around(self):
        public = {name for name in dir(R) if not name.startswith("_")}
        assert "_compose_synthetic_stage1_document".lstrip("_") not in public
        assert not any("authoriz" in name and "readiness" not in name for name in public)


class TestRunnerDeterminedValues:
    @pytest.mark.parametrize("gate", R.RESERVED_POSTURE_GATES)
    def test_b3_gates_are_forced_to_unable_to_determine(self, gate):
        document = _run()
        assert all(
            row["gate_results"][gate] == "UNABLE_TO_DETERMINE"
            for row in document["candidate_results"]
        )

    @pytest.mark.parametrize("gate", R.RESERVED_POSTURE_GATES)
    @pytest.mark.parametrize("value", ["PASS", "FAIL", "NOT_APPLICABLE"])
    def test_b3_gates_may_not_be_supplied_by_the_executor(self, gate, value):
        """Refused even when the supplied value agrees, so the rule cannot become advisory."""
        gates = {g: "PASS" for g in R.EXECUTOR_SUPPLIED_GATES}
        gates[gate] = value
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            _run({record["construction_id"]: _input(gate_results=gates) for record in SYNTHETIC_TRAVERSAL})
        assert "determined by accepted authority" in str(excinfo.value)

    def test_b3_gates_may_not_be_supplied_even_with_the_determined_value(self):
        gates = {g: "PASS" for g in R.EXECUTOR_SUPPLIED_GATES}
        gates["G3_NORMALIZATION"] = "UNABLE_TO_DETERMINE"
        with pytest.raises(R.Stage1RunnerError):
            _run({record["construction_id"]: _input(gate_results=gates) for record in SYNTHETIC_TRAVERSAL})

    def test_g2_may_not_be_supplied_directly(self):
        gates = {g: "PASS" for g in R.EXECUTOR_SUPPLIED_GATES}
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "PASS"
        with pytest.raises(R.Stage1RunnerError):
            _run({record["construction_id"]: _input(gate_results=gates) for record in SYNTHETIC_TRAVERSAL})

    def test_g2_is_derived_from_the_canonical_reading_table(self):
        document = _run()
        for row in document["candidate_results"]:
            assert row["gate_results"]["G2_MAGNITUDE_INTRINSICALITY"] == "UNABLE_TO_DETERMINE"
            assert row["g2_outcome_is_reading_dependent"] is True

    def test_an_incoherent_reading_pair_is_refused(self):
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            _run(
                {
                    record["construction_id"]: _input(
                        g2_outcome_under_subject_matter_reading="FAILS",
                        g2_outcome_under_preference_only_reading="PASSES",
                    )
                    for record in SYNTHETIC_TRAVERSAL
                }
            )
        assert "incoherent" in str(excinfo.value)

    def test_g9_undetermined_records_unable_to_determine(self):
        document = _run()
        assert all(
            row["gate_results"]["G9_REPRESENTATION"] == "UNABLE_TO_DETERMINE"
            for row in document["candidate_results"]
        )

    def test_g9_determined_failure_stays_prerequisite_blocked_not_utd(self):
        """XASSET-0035 SS-G.3: B3 applies only to the undetermined case."""
        document = _run(
            {
                record["construction_id"]: _input(
                    g9_path_1_declaration="DETERMINED_NOT_SELF_CONTAINED",
                    g9_named_dependency="a named Level-1 representation rule",
                )
                for record in SYNTHETIC_TRAVERSAL
            }
        )
        for row in document["candidate_results"]:
            assert row["gate_results"]["G9_REPRESENTATION"] == "FAIL"
            assert row["prerequisite_failures"] == ["G9_REPRESENTATION"]

    def test_a_determined_g9_failure_must_name_its_dependency(self):
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            _run(
                {
                    record["construction_id"]: _input(
                        g9_path_1_declaration="DETERMINED_NOT_SELF_CONTAINED"
                    )
                    for record in SYNTHETIC_TRAVERSAL
                }
            )
        assert "name its exact dependency" in str(excinfo.value)

    def test_g9_self_contained_records_pass(self):
        document = _run(
            {
                record["construction_id"]: _input(g9_path_1_declaration="SELF_CONTAINED")
                for record in SYNTHETIC_TRAVERSAL
            }
        )
        assert all(
            row["gate_results"]["G9_REPRESENTATION"] == "PASS"
            for row in document["candidate_results"]
        )

    def test_b1_floor_g12_may_not_fail_on_nonexistence_alone(self):
        gates = {g: "PASS" for g in R.EXECUTOR_SUPPLIED_GATES}
        gates["G12_SNAPSHOT_ADMISSIBILITY_PATH"] = "FAIL"
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            _run(
                {
                    record["construction_id"]: _input(
                        gate_results=gates, g12_basis="SUCCESSOR_NONEXISTENCE_ALONE"
                    )
                    for record in SYNTHETIC_TRAVERSAL
                }
            )
        assert "successor nonexistence alone" in str(excinfo.value)

    def test_b1_permits_g12_failure_on_independent_grounds(self):
        gates = {g: "PASS" for g in R.EXECUTOR_SUPPLIED_GATES}
        gates["G12_SNAPSHOT_ADMISSIBILITY_PATH"] = "FAIL"
        document = _run(
            {
                record["construction_id"]: _input(
                    gate_results=gates,
                    g12_basis="NO_LAWFUL_SUCCESSOR_IDENTIFIABLE_ON_INDEPENDENT_GROUNDS",
                )
                for record in SYNTHETIC_TRAVERSAL
            }
        )
        assert all(
            row["gate_results"]["G12_SNAPSHOT_ADMISSIBILITY_PATH"] == "FAIL"
            for row in document["candidate_results"]
        )

    def test_the_xasset_0030_snapshot_is_not_encoded_as_a_default(self):
        """SS-E.1 invalidation triggers make a hard-coded snapshot unsafe. No gate defaults."""
        for gate in ("G1_DRIVER_SUBJECT_MATTER", "G4_ORIGIN", "G6_ROUTE_COMPLIANCE",
                     "G7_DISCRETION_AND_PROVENANCE", "G11_EXACTNESS_AND_DETERMINISM"):
            assert gate in R.EXECUTOR_SUPPLIED_GATES
        gates = {g: "PASS" for g in R.EXECUTOR_SUPPLIED_GATES}
        del gates["G1_DRIVER_SUBJECT_MATTER"]
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            _run({record["construction_id"]: _input(gate_results=gates) for record in SYNTHETIC_TRAVERSAL})
        assert "were not evaluated" in str(excinfo.value)


class TestRunnerCompositionIsOrderIndependent:
    def test_candidate_order_does_not_change_any_outcome(self):
        forward = _run()
        reverse_traversal = list(reversed(SYNTHETIC_TRAVERSAL))
        reverse = R._compose_synthetic_stage1_document(
            {record["construction_id"]: _input() for record in reverse_traversal},
            provenance=_provenance(),
            traversal=reverse_traversal,
            cell_universe=[SYNTHETIC_CELL],
        )
        assert [row["disposition"] for row in forward["candidate_results"]] == list(
            reversed([row["disposition"] for row in reverse["candidate_results"]])
        )
        assert forward["cell_results"][0]["outcome"] == reverse["cell_results"][0]["outcome"]
        assert forward["roll_up_results"][0]["outcome"] == reverse["roll_up_results"][0]["outcome"]

    def test_input_mapping_order_does_not_change_the_document(self):
        inputs = {record["construction_id"]: _input() for record in SYNTHETIC_TRAVERSAL}
        shuffled = dict(reversed(list(inputs.items())))
        assert _run(inputs) == _run(shuffled)


class TestSerializer:
    def test_serialization_is_byte_reproducible(self):
        document = _run()
        assert R.serialize_stage1_results(document) == R.serialize_stage1_results(document)

    def test_artifact_hash_is_stable(self):
        document = _run()
        assert R.stage1_result_artifact_sha256(document) == R.stage1_result_artifact_sha256(document)

    def test_a_content_change_changes_the_artifact_hash(self):
        document = _run()
        tampered = copy.deepcopy(document)
        tampered["candidate_results"][0]["uncertainty_statement"] = "changed"
        assert R.stage1_result_artifact_sha256(document) != R.stage1_result_artifact_sha256(
            tampered
        )

    def test_row_key_order_is_the_canonical_result_schema_order(self):
        document = _run()
        for row in document["candidate_results"]:
            assert tuple(row) == PV.REQUIRED_CANDIDATE_RESULT_KEYS

    def test_serializer_does_not_sort_keys_away(self):
        """Sorting would silently destroy the canonical ordering the schema fixes."""
        document = _run()
        text = R.serialize_stage1_results(document).decode("utf-8")
        assert text.index('"schema_version"') < text.index('"study_id"')
        assert text.index('"candidate_results"') < text.index('"cell_results"')

    def test_synthetic_write_seam_refuses_to_overwrite(self, tmp_path):
        document = _run()
        target = tmp_path / "results.yaml"
        R._write_synthetic_results_artifact(document, target)
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            R._write_synthetic_results_artifact(document, target)
        assert "written once" in str(excinfo.value)


class TestPublicationBoundary:
    """BLOCKING 2 (review 4953193650). Publication requires a lawful claim, the canonical path,
    and full independent validation -- all BEFORE any file is opened."""

    def test_writer_accepts_no_path_parameter(self):
        assert set(inspect.signature(R.write_stage1_results).parameters) == {"document"}

    def test_writer_refuses_while_stage_1_is_unclaimed(self):
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            R.write_stage1_results(_run())
        assert "lawfully claimed execution" in str(excinfo.value)

    def test_writer_opens_no_file_when_unclaimed(self, monkeypatch):
        opened = []
        monkeypatch.setattr(R.os, "open", lambda *a, **k: opened.append(a) or 1)
        with pytest.raises(R.Stage1RunnerError):
            R.write_stage1_results(_run())
        assert opened == []

    def test_writer_refuses_an_invalid_document_even_when_claimed(self, monkeypatch):
        monkeypatch.setattr(AUTH, "claimed_execution_is_authorized", lambda *a, **k: (True, ""))
        opened = []
        monkeypatch.setattr(R.os, "open", lambda *a, **k: opened.append(a) or 1)
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            R.write_stage1_results({"not": "a results document"})
        assert "failed independent validation" in str(excinfo.value)
        assert opened == []

    def test_writer_validation_precedes_any_open(self, monkeypatch):
        """A synthetic document is well-formed only against a synthetic universe, so validating
        it against the REAL frozen universe must fail -- and must fail before any open."""
        monkeypatch.setattr(AUTH, "claimed_execution_is_authorized", lambda *a, **k: (True, ""))
        opened = []
        monkeypatch.setattr(R.os, "open", lambda *a, **k: opened.append(a) or 1)
        with pytest.raises(R.Stage1RunnerError):
            R.write_stage1_results(_run())
        assert opened == []

    def test_the_canonical_results_path_does_not_exist(self):
        assert not R.canonical_results_path().exists()

    def test_the_canonical_path_is_the_declared_relpath(self):
        assert R.canonical_results_path() == R.ROOT / R.RESULTS_RELPATH

    def test_the_synthetic_write_seam_may_not_target_the_canonical_path(self):
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            R._write_synthetic_results_artifact(_run(), R.canonical_results_path())
        assert "may never target the canonical results path" in str(excinfo.value)

    def test_the_writer_names_all_three_gates(self):
        source = inspect.getsource(R.write_stage1_results)
        assert "claimed_execution_is_authorized" in source
        assert "validate_stage1_result_document" in source
        assert "canonical_results_path" in source
        # The claim gate is asked before validation, and validation before any open.
        assert source.index("claimed_execution_is_authorized") < source.index(
            "validate_stage1_result_document"
        )
        assert source.index("validate_stage1_result_document") < source.index("_open_exclusive")


class TestResultIdentityIsSingular:
    """MAJOR 1 (review 4953193650). The writer returns the SEMANTIC identity the completion path
    binds, never the artifact byte checksum."""

    def test_writer_returns_the_semantic_identity(self, monkeypatch, tmp_path):
        document = _run()
        monkeypatch.setattr(AUTH, "claimed_execution_is_authorized", lambda *a, **k: (True, ""))
        monkeypatch.setattr(
            R, "canonical_results_path", lambda: tmp_path / "published.yaml"
        )
        monkeypatch.setattr(
            RV, "validate_stage1_result_document", lambda *a, **k: PV.ValidationResult(True, ())
        )
        returned = R.write_stage1_results(document)
        assert returned == AUTH.stage1_result_identity(document)
        assert returned != R.stage1_result_artifact_sha256(document)

    def test_the_two_hashes_are_different_functions(self):
        document = _run()
        assert AUTH.stage1_result_identity(document) != R.stage1_result_artifact_sha256(document)

    def test_key_reordering_changes_the_artifact_hash_but_not_the_identity(self):
        document = _run()
        reordered = dict(reversed(list(document.items())))
        assert AUTH.stage1_result_identity(document) == AUTH.stage1_result_identity(reordered)
        assert R.stage1_result_artifact_sha256(document) != R.stage1_result_artifact_sha256(
            reordered
        )

    def test_the_completion_path_binds_the_semantic_identity(self):
        for function in (AUTH.complete_execution, AUTH.completed_result_is_authorized):
            assert "stage1_result_identity" in inspect.getsource(function)

    def test_no_authorization_function_consumes_the_artifact_checksum(self):
        assert "stage1_result_artifact_sha256" not in Path(
            "level1_stage1_execution_authorization.py"
        ).read_text(encoding="utf-8")


# ======================================================================================
# The independent result validator
# ======================================================================================


class TestG12BasisIsPersistedAndIndependentlyEnforced:
    """MAJOR 2 (review 4953193650). B1's preserved floor survives serialization: the basis the
    runner validated is recorded in the publishable artifact, and the independent validator
    re-enforces the coupling rather than trusting the producer."""

    def test_the_schema_declares_the_basis_key(self):
        assert "g12_basis" in PV.REQUIRED_CANDIDATE_RESULT_KEYS

    def test_every_row_records_the_basis_the_runner_validated(self):
        document = _run()
        for row in document["candidate_results"]:
            assert row["g12_basis"] == "LAWFUL_SUCCESSOR_IDENTIFIABLE"

    def test_the_runner_and_the_validator_agree_on_the_closed_vocabulary(self):
        assert set(R.G12_BASES) == set(RV._G12_BASIS_VALUES) == set(PV.G12_BASIS_VALUES)

    def test_the_validator_defines_its_vocabulary_independently_of_the_runner(self):
        source = inspect.getsource(RV)
        marker = source.index("_G12_BASIS_VALUES = (")
        assert "RUNNER.G12_BASES" not in source
        assert "LAWFUL_SUCCESSOR_IDENTIFIABLE" in source[marker : marker + 400]

    @pytest.mark.parametrize("basis", ["", None, "SOMETHING_ELSE", "lawful_successor_identifiable"])
    def test_an_unknown_or_missing_basis_is_rejected(self, basis):
        document = _run()
        document["candidate_results"][0]["g12_basis"] = basis
        result = _validate(document)
        assert not result.ok and any("g12_basis" in error for error in result.errors)

    def test_a_g12_fail_on_successor_nonexistence_alone_is_rejected(self):
        document = _run()
        row = document["candidate_results"][0]
        row["gate_results"]["G12_SNAPSHOT_ADMISSIBILITY_PATH"] = "FAIL"
        row["g12_basis"] = "SUCCESSOR_NONEXISTENCE_ALONE"
        result = _validate(document)
        assert not result.ok
        assert any("SUCCESSOR_NONEXISTENCE_ALONE" in error for error in result.errors)

    def test_a_g12_fail_on_independent_grounds_remains_representable(self):
        inputs = {
            record["construction_id"]: _input(
                gate_results={
                    **{gate: "PASS" for gate in R.EXECUTOR_SUPPLIED_GATES},
                    "G12_SNAPSHOT_ADMISSIBILITY_PATH": "FAIL",
                },
                g12_basis="NO_LAWFUL_SUCCESSOR_IDENTIFIABLE_ON_INDEPENDENT_GROUNDS",
            )
            for record in SYNTHETIC_TRAVERSAL
        }
        document = _run(inputs)
        assert _validate(document).ok, _validate(document).errors

    def test_successor_nonexistence_alone_is_lawful_when_g12_does_not_fail(self):
        inputs = {
            record["construction_id"]: _input(g12_basis="SUCCESSOR_NONEXISTENCE_ALONE")
            for record in SYNTHETIC_TRAVERSAL
        }
        document = _run(inputs)
        assert _validate(document).ok, _validate(document).errors

    def test_the_runner_still_refuses_the_pairing_at_input_time(self):
        inputs = {
            record["construction_id"]: _input(
                gate_results={
                    **{gate: "PASS" for gate in R.EXECUTOR_SUPPLIED_GATES},
                    "G12_SNAPSHOT_ADMISSIBILITY_PATH": "FAIL",
                },
                g12_basis="SUCCESSOR_NONEXISTENCE_ALONE",
            )
            for record in SYNTHETIC_TRAVERSAL
        }
        with pytest.raises(R.Stage1RunnerError) as excinfo:
            _run(inputs)
        assert "successor nonexistence alone" in str(excinfo.value)

    def test_the_basis_survives_a_serialize_parse_round_trip(self):
        document = _run()
        parsed = RV.load_results(R.serialize_stage1_results(document))
        assert [row["g12_basis"] for row in parsed["candidate_results"]] == [
            row["g12_basis"] for row in document["candidate_results"]
        ]

    def test_tampering_with_the_basis_after_serialization_is_caught(self):
        inputs = {
            record["construction_id"]: _input(
                gate_results={
                    **{gate: "PASS" for gate in R.EXECUTOR_SUPPLIED_GATES},
                    "G12_SNAPSHOT_ADMISSIBILITY_PATH": "FAIL",
                },
                g12_basis="NO_LAWFUL_SUCCESSOR_IDENTIFIABLE_ON_INDEPENDENT_GROUNDS",
            )
            for record in SYNTHETIC_TRAVERSAL
        }
        document = _run(inputs)
        assert _validate(document).ok
        parsed = RV.load_results(R.serialize_stage1_results(document))
        parsed["candidate_results"][0]["g12_basis"] = "SUCCESSOR_NONEXISTENCE_ALONE"
        assert not _validate(parsed).ok

    def test_the_canonical_artifact_declares_the_coupling(self, prereg):
        block = prereg["result_schema"]["g12_basis_vocabulary"]
        assert block["prohibited_with_g12_fail"] == "SUCCESSOR_NONEXISTENCE_ALONE"
        assert block["coupling_is_enforced"] is True
        assert set(block["values"]) == set(PV.G12_BASIS_VALUES)


class TestResultValidator:
    def test_a_clean_document_validates(self):
        assert _validate(_run()).ok, _validate(_run()).errors

    def test_a_substituted_disposition_is_rejected(self):
        document = _run()
        document["candidate_results"][0]["disposition"] = "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"
        result = _validate(document)
        assert not result.ok
        assert any("deriv" in error for error in result.errors)

    def test_a_substituted_cell_outcome_is_rejected(self):
        document = _run()
        document["cell_results"][0]["outcome"] = "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"
        assert not _validate(document).ok

    def test_a_substituted_roll_up_outcome_is_rejected(self):
        document = _run()
        document["roll_up_results"][0]["outcome"] = "CANDIDATE_CONSTRUCTION_IDENTIFIED"
        assert not _validate(document).ok

    def test_a_relabelled_identity_field_is_rejected(self):
        document = _run()
        document["candidate_results"][0]["family_id"] = "R2_C2"
        result = _validate(document)
        assert not result.ok and any("immutable" in error for error in result.errors)

    def test_reordered_rows_are_rejected(self):
        document = _run()
        document["candidate_results"] = list(reversed(document["candidate_results"]))
        result = _validate(document)
        assert not result.ok and any("canonical construction order" in e for e in result.errors)

    def test_a_duplicated_row_is_rejected(self):
        document = _run()
        document["candidate_results"].append(copy.deepcopy(document["candidate_results"][0]))
        result = _validate(document)
        assert not result.ok and any("duplicated" in error for error in result.errors)

    def test_a_partial_inventory_is_rejected(self):
        document = _run()
        document["candidate_results"] = document["candidate_results"][:1]
        result = _validate(document)
        assert not result.ok and any("unevaluated" in error for error in result.errors)

    def test_the_b3_posture_is_enforced_at_validation_time(self):
        document = _run()
        document["candidate_results"][0]["gate_results"]["G3_NORMALIZATION"] = "PASS"
        result = _validate(document)
        assert not result.ok and any("reserved-gate posture" in e for e in result.errors)

    def test_a_broken_g2_coupling_is_rejected(self):
        document = _run()
        document["candidate_results"][0]["gate_results"]["G2_MAGNITUDE_INTRINSICALITY"] = "PASS"
        assert not _validate(document).ok

    def test_forbidden_numeric_content_is_rejected(self):
        document = _run()
        document["candidate_results"][0]["sleeve_share"] = 0.25
        result = _validate(document)
        assert not result.ok
        assert any("forbidden result content" in e or "numeric" in e for e in result.errors)

    @pytest.mark.parametrize(
        "key", ["target_weight", "composite_score", "rank", "allocation", "lower_bound_value"]
    )
    def test_forbidden_quantitative_keys_are_rejected(self, key):
        document = _run()
        document["provenance_manifest"][key] = "anything"
        result = _validate(document)
        assert not result.ok and any("forbidden result content" in e for e in result.errors)

    def test_a_missing_provenance_field_is_rejected(self):
        document = _run()
        del document["provenance_manifest"]["repository_head_sha"]
        assert not _validate(document).ok

    def test_an_untruthful_candidate_count_is_rejected(self):
        document = _run()
        document["provenance_manifest"]["candidates_evaluated"] = 999
        assert not _validate(document).ok

    def test_a_wrong_execution_attempt_id_is_rejected(self):
        document = _run()
        document["provenance_manifest"]["execution_attempt_id"] = "ENDPOINT-0001::STAGE_1::ATTEMPT_2"
        assert not _validate(document).ok

    def test_a_cross_bound_roll_up_reference_is_rejected(self):
        document = _run()
        document["roll_up_results"][0]["contributing_cell_ids"] = [
            f"{SYNTHETIC_SLEEVE}::UPPER::portfolio_function"
        ]
        result = _validate(document)
        assert not result.ok and any("prohibited" in error for error in result.errors)

    def test_mismatched_abstention_records_are_rejected(self):
        document = _run()
        document["abstention_records"] = []
        assert not _validate(document).ok

    def test_an_unexpected_top_level_key_is_rejected(self):
        document = _run()
        document["extra"] = True
        assert not _validate(document).ok

    def test_duplicate_keys_are_rejected_at_load(self):
        document = _run()
        text = R.serialize_stage1_results(document).decode("utf-8")
        tampered = text.replace(
            '"disposition": "RECORDED"', '"disposition": "RECORDED",\n  "disposition": "X"', 1
        )
        with pytest.raises(RV.ResultValidationError) as excinfo:
            RV.load_results(tampered)
        assert "duplicate key" in str(excinfo.value)

    def test_malformed_serialization_is_rejected(self):
        with pytest.raises(RV.ResultValidationError):
            RV.load_results("{not json")

    def test_a_missing_results_file_fails_closed(self, tmp_path):
        assert not RV.validate_results_file(tmp_path / "absent.yaml").ok

    def test_the_validator_does_not_trust_the_runner(self, tmp_path):
        """A round trip through disk still re-derives everything."""
        document = _run()
        target = tmp_path / "results.yaml"
        R._write_synthetic_results_artifact(document, target)
        loaded = RV.load_results(target.read_bytes())
        assert _validate(loaded).ok

    def test_an_empty_document_against_the_real_universe_reports_all_680(self):
        """Structural only: a set difference over identifiers evaluates no gate."""
        document = _run()
        document.update(
            {
                "candidate_results": [],
                "cell_results": [],
                "roll_up_results": [],
                "abstention_records": [],
            }
        )
        result = RV.validate_stage1_result_document(document)
        assert not result.ok
        assert any("680 registered construction" in error for error in result.errors)


# ======================================================================================
# Trust boundary and pins (SS-G.B steps 5-6)
# ======================================================================================


class TestTrustBoundary:
    def test_the_runner_is_load_bearing(self):
        assert "level1_stage1_runner.py" in AUTH.LOAD_BEARING_RELPATHS

    def test_the_result_validator_is_load_bearing(self):
        assert "level1_stage1_result_validator.py" in AUTH.LOAD_BEARING_RELPATHS

    def test_the_authorizing_decision_is_load_bearing(self):
        assert any(
            "XASSET-0036" in relative for relative in AUTH.LOAD_BEARING_RELPATHS
        )

    def test_every_prior_load_bearing_path_is_retained(self):
        for relative in (
            "level1_stage1_execution_authorization.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "level1_construction_universe_closure_validator.py",
            AUTH.CANONICAL_PROTOCOL_RELPATH,
            AUTH.CANONICAL_PREREGISTRATION_RELPATH,
            "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
        ):
            assert relative in AUTH.LOAD_BEARING_RELPATHS

    def test_every_load_bearing_path_exists(self):
        for relative in AUTH.LOAD_BEARING_RELPATHS:
            assert (ROOT / relative).exists(), relative

    def test_no_outcome_producing_module_is_left_outside_the_boundary(self):
        """The governing SS-G.B invariant, asserted rather than assumed."""
        outcome_producing = {
            "level1_stage1_runner.py",
            "level1_stage1_result_validator.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "level1_construction_universe_closure_validator.py",
        }
        assert outcome_producing <= set(AUTH.LOAD_BEARING_RELPATHS)

    def test_the_existing_exact_byte_mechanism_is_reused(self):
        """Expected identity is derived from the merged tree, never a constant here."""
        source = (ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        assert "enforcement drift" in source
        assert "live_load_bearing_hashes" in source


class TestCanonicalPins:
    def test_the_effective_pins_match_the_committed_canonical_bytes(self):
        result = PV.validate_current_canonical_pins()
        assert result.ok, result.errors

    def test_pins_are_not_placeholders(self):
        assert AUTH.pins_are_placeholders() is False

    def test_a_wrong_canonical_pin_is_detected(self, tmp_path):
        wrong = tmp_path / "PROTOCOL_V1.md"
        wrong.write_text("not the canonical protocol", encoding="utf-8")
        result = PV.validate_current_canonical_pins(protocol_path=wrong)
        assert not result.ok

    def test_the_predecessor_pins_are_retained_verbatim(self):
        assert (
            PV.XASSET_0029_PINS["protocol_sha256"]
            == "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
        )
        assert (
            PV.XASSET_0029_PINS["preregistration_sha256"]
            == "6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c"
        )

    def test_accepted_history_is_not_rewritten(self):
        """XASSET-0029's own decision file still records the digests it accepted."""
        text = (ROOT / XASSET_0029_DECISION_RELPATH).read_text(encoding="utf-8")
        assert PV.validate_xasset_0029_successor_hash_pins(text).ok

    def test_the_effective_pins_differ_from_the_predecessor(self):
        """An amendment that left the bytes unchanged would not be an amendment."""
        assert (
            AUTH.CANONICAL_PINS[AUTH.CANONICAL_PROTOCOL_RELPATH]
            != AUTH.XASSET_0029_CANONICAL_PINS[AUTH.CANONICAL_PROTOCOL_RELPATH]
        )
        assert (
            AUTH.CANONICAL_PINS[AUTH.CANONICAL_PREREGISTRATION_RELPATH]
            != AUTH.XASSET_0029_CANONICAL_PINS[AUTH.CANONICAL_PREREGISTRATION_RELPATH]
        )

    def test_the_universe_hash_pin_is_unchanged(self):
        assert (
            AUTH.CONSTRUCTION_UNIVERSE_SHA256
            == "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
        )
        assert AUTH.CONSTRUCTION_COUNT == 680
        assert AUTH.CONSTRUCTION_CELL_COUNT == 48


# ======================================================================================
# No execution, no unauthorized reach -- asserted directly
# ======================================================================================


class TestNoExecutionOccurred:
    def test_no_results_artifact_exists_in_the_repository(self):
        assert not (ROOT / R.RESULTS_RELPATH).exists()

    def test_the_authorization_root_is_absent(self):
        paths = AUTH.LanePaths()
        assert not paths.authorization.exists()
        assert not paths.claim.exists()
        assert not paths.completion.exists()
        assert not paths.ledger.exists()

    def test_stage_1_is_not_executable(self):
        authorized, _ = AUTH.new_execution_is_authorized()
        assert authorized is False

    def test_the_lane_is_absent_and_attempt_1_is_unclaimed(self):
        state, _ = AUTH.lane_state_at(AUTH.LanePaths())
        assert state == AUTH.LANE_ABSENT

    @pytest.mark.parametrize("module", ["level1_stage1_runner.py", "level1_stage1_result_validator.py"])
    def test_no_network_or_subprocess_reach(self, module):
        """Neither new module may import a network, subprocess, or brokerage surface."""
        tree = ast.parse((ROOT / module).read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        forbidden = {
            "socket",
            "http",
            "urllib",
            "urllib3",
            "requests",
            "subprocess",
            "yfinance",
            "alpaca_client",
            "curl_cffi",
        }
        assert not (imported & forbidden), sorted(imported & forbidden)

    @pytest.mark.parametrize("module", ["level1_stage1_runner.py", "level1_stage1_result_validator.py"])
    def test_no_protected_risk_reach(self, module):
        """XASSET-0036 SS-F: no protected RISK result path is read or referenced.

        The forbidden tokens are ASSEMBLED rather than written as literals, so this suite itself
        carries no reference to the protected path -- the same discipline the XASSET-0036
        authorization suite applied to its own AST guard.
        """
        source = (ROOT / module).read_text(encoding="utf-8")
        forbidden = (
            "risk" + "_lane_boundary",
            "phq-" + "risk0001-results",
            "risk" + "_level1",
        )
        for token in forbidden:
            assert token not in source, token

    def test_the_only_write_surface_is_the_explicit_writer(self):
        """No module-level or incidental filesystem write exists in either new module."""
        for module in ("level1_stage1_runner.py", "level1_stage1_result_validator.py"):
            tree = ast.parse((ROOT / module).read_text(encoding="utf-8"))
            writers = {
                node.func.attr
                for node in ast.walk(tree)
                if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in {"write_text", "write_bytes", "mkdir", "touch", "unlink"}
            }
            assert not writers, (module, writers)

    def test_the_result_validator_writes_nothing_at_all(self):
        tree = ast.parse((ROOT / "level1_stage1_result_validator.py").read_text(encoding="utf-8"))
        opens = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open"
        }
        assert not opens

    def test_running_the_structural_checks_creates_no_lane_state(self):
        R.verify_frozen_traversal()
        R.pair_consumption_inventory()
        paths = AUTH.LanePaths()
        assert not paths.authorization.exists()
        assert not paths.claim.exists()

    def test_using_the_synthetic_seam_confers_nothing(self):
        _run()
        assert AUTH.new_execution_is_authorized()[0] is False
        assert AUTH.claimed_execution_is_authorized()[0] is False
        assert not AUTH.LanePaths().authorization.exists()

    def test_no_real_registered_construction_carries_a_disposition_in_this_suite(self):
        """Every composed row in this module names a SYNTHETIC construction."""
        registered = set(CU.frozen_construction_universe())
        document = _run()
        for row in document["candidate_results"]:
            assert row["construction_id"] not in registered
