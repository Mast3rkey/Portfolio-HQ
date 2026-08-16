"""Focused and adversarial tests for the ENDPOINT-0001 pre-registration validator.

Every mutation fixture is a deep copy of the real committed pre-registration, so a test that expects
rejection is proving the validator catches a change to the actual artifact rather than to a synthetic
stand-in.

Barred historical Level-1 values are never written as literals in this file. Where a scan must be
exercised, the sample is derived from the validator module's own pattern constants, so this test file
introduces no anchor of its own.
"""

from __future__ import annotations

import ast
import copy
import re
from pathlib import Path

import pytest
import yaml

import level1_endpoint_evidence_preregistration_validator as V

ROOT = Path(__file__).resolve().parent


@pytest.fixture(scope="module")
def raw_text() -> str:
    return V.PREREG_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def base_data(raw_text: str) -> dict:
    return yaml.safe_load(raw_text)


@pytest.fixture
def data(base_data: dict) -> dict:
    return copy.deepcopy(base_data)


def _errors(mutated: dict) -> tuple[str, ...]:
    return V.validate(mutated).errors


def _assert_rejected(mutated: dict, fragment: str) -> None:
    result = V.validate(mutated)
    assert not result.ok, f"expected rejection mentioning {fragment!r}, got a clean pass"
    assert any(fragment in e for e in result.errors), (
        f"expected an error mentioning {fragment!r}; got {result.errors}"
    )


# ---------------------------------------------------------------------------
# The committed artifacts
# ---------------------------------------------------------------------------


class TestCommittedArtifacts:
    def test_real_preregistration_validates_clean(self):
        result = V.validate_file()
        assert result.ok, f"committed artifacts must validate clean; got {result.errors}"

    def test_real_preregistration_structure_validates_clean(self, base_data: dict):
        assert V.validate(base_data).ok

    def test_canonical_files_exist(self):
        assert V.PREREG_PATH.exists()
        assert V.PROTOCOL_PATH.exists()
        assert V.DECISION_PATH.exists()

    def test_protocol_mirror_matches(self):
        text = V.PROTOCOL_PATH.read_text(encoding="utf-8")
        assert V.validate_protocol_mirror(text).ok

    def test_charter_hash_pins_match_committed_bytes(self):
        text = V.DECISION_PATH.read_text(encoding="utf-8")
        assert V.validate_charter_hash_pins(text).ok

    def test_hashes_are_reproducible(self):
        first = V.sha256_file(V.PREREG_PATH)
        second = V.sha256_file(V.PREREG_PATH)
        assert first == second and len(first) == 64


# ---------------------------------------------------------------------------
# Closed schema
# ---------------------------------------------------------------------------


class TestClosedSchema:
    def test_extra_top_level_key_rejected(self, data: dict):
        data["endpoint_value"] = "anything"
        _assert_rejected(data, "unexpected key")

    def test_missing_top_level_key_rejected(self, data: dict):
        del data["gate_sequence"]
        _assert_rejected(data, "missing key")

    def test_non_mapping_rejected(self):
        assert not V.validate({"schema_version": "1.0"}).ok

    @pytest.mark.parametrize("field", ["sleeves", "bounds", "driver_classes"])
    def test_population_change_rejected(self, data: dict, field: str):
        data[field] = list(data[field])[:-1]
        _assert_rejected(data, field)

    def test_added_sleeve_rejected(self, data: dict):
        data["sleeves"] = list(data["sleeves"]) + ["reserve"]
        _assert_rejected(data, "sleeves")

    def test_reordered_driver_classes_rejected(self, data: dict):
        data["driver_classes"] = list(reversed(data["driver_classes"]))
        _assert_rejected(data, "driver_classes")

    def test_study_id_change_rejected(self, data: dict):
        data["study_id"] = "RISK-0001"
        _assert_rejected(data, "study_id")


# ---------------------------------------------------------------------------
# Gate sequence
# ---------------------------------------------------------------------------


class TestGateSequence:
    def test_thirteen_gates(self, base_data: dict):
        assert len(base_data["gate_sequence"]["gates"]) == 13

    def test_gate_removed_rejected(self, data: dict):
        data["gate_sequence"]["gates"].pop()
        _assert_rejected(data, "expected 13 gates")

    def test_gate_added_rejected(self, data: dict):
        extra = copy.deepcopy(data["gate_sequence"]["gates"][0])
        extra["gate_id"] = "G14_EXTRA"
        data["gate_sequence"]["gates"].append(extra)
        _assert_rejected(data, "expected 13 gates")

    def test_gate_reorder_rejected(self, data: dict):
        gates = data["gate_sequence"]["gates"]
        gates[0], gates[1] = gates[1], gates[0]
        _assert_rejected(data, "gate_id")

    def test_gate_index_gap_rejected(self, data: dict):
        data["gate_sequence"]["gates"][4]["gate_index"] = 99
        _assert_rejected(data, "gate_index")

    def test_normalization_gate_present(self, base_data: dict):
        ids = [g["gate_id"] for g in base_data["gate_sequence"]["gates"]]
        assert "G3_NORMALIZATION" in ids
        assert "G2_MAGNITUDE_INTRINSICALITY" in ids

    @pytest.mark.parametrize("gate_id", V.PREREQUISITE_GATES)
    def test_prerequisite_gates_keep_prerequisite_disposition(self, data: dict, gate_id: str):
        for gate in data["gate_sequence"]["gates"]:
            if gate["gate_id"] == gate_id:
                gate["failure_disposition"] = "BLOCKED_CATEGORICALLY"
        _assert_rejected(data, "failure_disposition")

    def test_categorical_gate_may_not_become_prerequisite(self, data: dict):
        for gate in data["gate_sequence"]["gates"]:
            if gate["gate_id"] == "G4_ORIGIN":
                gate["failure_disposition"] = "BLOCKED_PENDING_SEPARATE_PREREQUISITE"
        _assert_rejected(data, "failure_disposition")

    def test_disposition_outside_closed_set_rejected(self, data: dict):
        data["gate_sequence"]["gates"][0]["failure_disposition"] = "PASSED_WITH_JUDGMENT"
        _assert_rejected(data, "outside the closed set")

    def test_empty_controlling_authority_rejected(self, data: dict):
        data["gate_sequence"]["gates"][0]["controlling_authority"] = "  "
        _assert_rejected(data, "controlling_authority")

    def test_gate_freeze_flag_required(self, data: dict):
        key = "gates_may_not_be_added_removed_reordered_or_reinterpreted_after_any_outcome_observed"
        data["gate_sequence"][key] = False
        _assert_rejected(data, key)


# ---------------------------------------------------------------------------
# Derived arithmetic
# ---------------------------------------------------------------------------


class TestDerivedArithmetic:
    def test_cell_ceiling_is_the_product_of_the_populations(self, base_data: dict):
        product = (
            len(base_data["sleeves"])
            * len(base_data["bounds"])
            * len(base_data["driver_classes"])
        )
        assert product == base_data["trial_inventory"]["derived_ceiling_cells"] == 48

    def test_roll_up_count_is_sleeves_times_bounds(self, base_data: dict):
        assert len(base_data["sleeves"]) * len(base_data["bounds"]) == 8
        assert base_data["roll_up_units"]["derived_count"] == 8

    def test_wrong_ceiling_rejected(self, data: dict):
        data["trial_inventory"]["derived_ceiling_cells"] = 47
        _assert_rejected(data, "derived_ceiling_cells")

    def test_nonzero_reserve_rejected(self, data: dict):
        data["trial_inventory"]["reserve_cells"] = 2
        _assert_rejected(data, "reserve_cells")

    def test_derived_identity_value_mismatch_rejected(self, data: dict):
        for row in data["consequential_parameter_registry"]["derived_identities"]["identities"]:
            if row["identity_id"] == "CELL_CEILING":
                row["value"] = 96
        _assert_rejected(data, "CELL_CEILING")

    def test_derived_identity_may_not_be_a_num_0001_class(self, data: dict):
        rows = data["consequential_parameter_registry"]["derived_identities"]["identities"]
        rows[0]["contextual_class"] = "EMPIRICALLY_CALIBRATED"
        _assert_rejected(data, "CALCULATED_OUTPUT")

    def test_missing_derived_identity_rejected(self, data: dict):
        rows = data["consequential_parameter_registry"]["derived_identities"]["identities"]
        data["consequential_parameter_registry"]["derived_identities"]["identities"] = [
            r for r in rows if r["identity_id"] != "GATE_COUNT"
        ]
        _assert_rejected(data, "GATE_COUNT")


# ---------------------------------------------------------------------------
# Zero-parameter declaration — the anti-tuning guarantee
# ---------------------------------------------------------------------------


class TestZeroParameterDeclaration:
    def test_registry_is_empty_in_the_committed_artifact(self, base_data: dict):
        assert base_data["consequential_parameter_registry"]["parameters"] == []

    def test_smuggled_parameter_rejected(self, data: dict):
        data["consequential_parameter_registry"]["parameters"] = [
            {"parameter_id": "MATERIALITY_TOLERANCE", "value": "0.05"}
        ]
        _assert_rejected(data, "zero consequential")

    def test_declaration_flag_must_be_true(self, data: dict):
        block = data["consequential_parameter_registry"]["zero_parameter_declaration"]
        block["stage_1_introduces_zero_consequential_numeric_parameters"] = False
        _assert_rejected(data, "stage_1_introduces_zero_consequential_numeric_parameters")

    def test_record_keys_locked(self, data: dict):
        registry = data["consequential_parameter_registry"]
        registry["record_keys"] = list(registry["record_keys"])[:5]
        _assert_rejected(data, "record_keys")

    def test_registry_schema_matches_established_repository_shape(self, base_data: dict):
        assert (
            tuple(base_data["consequential_parameter_registry"]["record_keys"])
            == V.PARAMETER_RECORD_KEYS
        )


# ---------------------------------------------------------------------------
# Roll-up is an existence test, never a score
# ---------------------------------------------------------------------------


class TestRollUpIsNotAScore:
    def test_precedence_has_exactly_four_rules_in_order(self, base_data: dict):
        rules = base_data["result_vocabulary"]["roll_up_precedence"]
        assert len(rules) == 4
        assert [r["condition"] for r in rules] == [c for c, _ in V.ROLL_UP_PRECEDENCE]
        assert [r["outcome"] for r in rules] == [o for _, o in V.ROLL_UP_PRECEDENCE]

    def test_reordered_precedence_rejected(self, data: dict):
        rules = data["result_vocabulary"]["roll_up_precedence"]
        rules[0], rules[1] = rules[1], rules[0]
        _assert_rejected(data, "roll_up_precedence")

    def test_dropped_precedence_rule_rejected(self, data: dict):
        data["result_vocabulary"]["roll_up_precedence"].pop()
        _assert_rejected(data, "roll_up_precedence")

    def test_scoring_mechanism_rejected(self, data: dict):
        data["result_vocabulary"]["roll_up_mechanism"] = "WEIGHTED_MAJORITY_VOTE"
        _assert_rejected(data, "roll_up_mechanism")

    def test_not_a_score_flag_required(self, data: dict):
        data["result_vocabulary"]["roll_up_is_not_a_score"] = False
        _assert_rejected(data, "roll_up_is_not_a_score")

    def test_cell_outcome_vocabulary_locked(self, data: dict):
        data["result_vocabulary"]["cell_outcomes"] = list(
            data["result_vocabulary"]["cell_outcomes"]
        ) + ["PARTIALLY_SUPPORTED"]
        _assert_rejected(data, "cell_outcomes")

    def test_cross_bound_and_cross_sleeve_reference_prohibited(self, base_data: dict):
        roll_up = base_data["roll_up_units"]
        assert roll_up["cross_bound_reference"] == "PROHIBITED"
        assert roll_up["cross_sleeve_reference"] == "PROHIBITED"

    def test_cross_sleeve_inference_permitted_is_rejected(self, data: dict):
        data["roll_up_units"]["cross_sleeve_reference"] = "PERMITTED"
        _assert_rejected(data, "cross_sleeve_reference")


# ---------------------------------------------------------------------------
# XASSET-0024 SS-K.1 open reading
# ---------------------------------------------------------------------------


class TestOpenReadingPreserved:
    def test_open_reading_is_not_resolved(self, base_data: dict):
        handling = base_data["open_reading_handling"]
        assert handling["resolved_by_this_program"] is False
        assert handling["relied_upon_by_this_program"] is False

    def test_resolving_the_reading_rejected(self, data: dict):
        data["open_reading_handling"]["resolved_by_this_program"] = True
        _assert_rejected(data, "resolved_by_this_program")

    def test_relying_on_the_reading_rejected(self, data: dict):
        data["open_reading_handling"]["relied_upon_by_this_program"] = True
        _assert_rejected(data, "relied_upon_by_this_program")

    def test_single_reading_evaluation_rejected(self, data: dict):
        data["open_reading_handling"]["handling"] = "ASSUME_SUBJECT_MATTER_READING"
        _assert_rejected(data, "handling")

    def test_both_reading_fields_required(self, data: dict):
        fields = data["open_reading_handling"]["required_recorded_fields"]
        data["open_reading_handling"]["required_recorded_fields"] = [
            f for f in fields if f != "g2_outcome_under_preference_only_reading"
        ]
        _assert_rejected(data, "g2_outcome_under_preference_only_reading")

    def test_preference_only_consequence_is_universal_abstention(self, base_data: dict):
        assert (
            base_data["open_reading_handling"][
                "consequence_if_preference_only_reading_later_established"
            ]
            == "ALL_CELLS_ABSTAIN"
        )


# ---------------------------------------------------------------------------
# Stage boundary
# ---------------------------------------------------------------------------


class TestStageBoundary:
    def test_stage_2_is_not_authorized(self, base_data: dict):
        assert base_data["stages"]["stage_2"]["authorized_by_xasset_0027"] is False

    def test_authorizing_stage_2_rejected(self, data: dict):
        data["stages"]["stage_2"]["authorized_by_xasset_0027"] = True
        _assert_rejected(data, "stages.stage_2.authorized_by_xasset_0027")

    @pytest.mark.parametrize(
        "flag",
        [
            "acquires_data",
            "fits_or_estimates_anything",
            "produces_endpoint",
            "produces_admissible_evidence",
        ],
    )
    def test_stage_1_boundary_flags_must_stay_false(self, data: dict, flag: str):
        data["stages"]["stage_1"][flag] = True
        _assert_rejected(data, flag)

    def test_stage_2_requires_separate_authorization(self, base_data: dict):
        assert (
            base_data["stages"]["stage_2"]["authorization_requirement"]
            == "SEPARATE_LATER_EXPLICITLY_ACCEPTED_GOVERNANCE_DECISION"
        )

    def test_authority_not_exercised_by_the_program(self, base_data: dict):
        assert base_data["authority"]["authority_exercised_by_this_program"] is False

    def test_exercising_authority_rejected(self, data: dict):
        data["authority"]["authority_exercised_by_this_program"] = True
        _assert_rejected(data, "authority_exercised_by_this_program")


# ---------------------------------------------------------------------------
# Execution discipline
# ---------------------------------------------------------------------------


class TestExecutionDiscipline:
    def test_early_stop_prohibited(self, base_data: dict):
        assert (
            base_data["execution"]["stopping_rules"]["early_stop_on_positive_finding"]
            == "PROHIBITED"
        )

    def test_permitting_early_stop_rejected(self, data: dict):
        data["execution"]["stopping_rules"]["early_stop_on_positive_finding"] = "PERMITTED"
        _assert_rejected(data, "early_stop_on_positive_finding")

    def test_rerun_after_outcomes_prohibited(self, data: dict):
        data["execution"]["rerun_rule"]["after_outcomes_observed"] = "PERMITTED"
        _assert_rejected(data, "after_outcomes_observed")

    def test_automatic_defect_rerun_prohibited(self, data: dict):
        data["execution"]["rerun_rule"]["discovered_defect_automatic_rerun"] = "PERMITTED"
        _assert_rejected(data, "discovered_defect_automatic_rerun")

    def test_history_mining_controls_required(self, data: dict):
        data["execution"]["history_mining_controls"]["gates_frozen_before_evaluation"] = False
        _assert_rejected(data, "gates_frozen_before_evaluation")

    def test_outcome_aware_gate_change_prohibited(self, data: dict):
        data["execution"]["history_mining_controls"]["outcome_aware_gate_change"] = "PERMITTED"
        _assert_rejected(data, "outcome_aware_gate_change")

    @pytest.mark.parametrize(
        "block", ["out_of_sample_discipline", "neighboring_parameter_robustness"]
    )
    def test_non_applicability_must_state_a_reason(self, data: dict, block: str):
        data["execution"][block]["reason"] = "   "
        _assert_rejected(data, f"execution.{block}.reason")

    @pytest.mark.parametrize(
        "block", ["out_of_sample_discipline", "neighboring_parameter_robustness"]
    )
    def test_non_applicability_is_recorded_honestly_not_claimed_performed(
        self, base_data: dict, block: str
    ):
        entry = base_data["execution"][block]
        assert entry["applicable_to_stage_1"] is False
        assert entry["reason"].strip()

    def test_stage_2_must_still_carry_out_of_sample_discipline(self, base_data: dict):
        assert (
            base_data["execution"]["out_of_sample_discipline"]["required_of_any_future_stage_2"]
            is True
        )

    def test_negative_results_preserved(self, data: dict):
        block = data["execution"]["negative_result_preservation"]
        block["all_cell_outcomes_recorded_regardless_of_direction"] = False
        _assert_rejected(data, "all_cell_outcomes_recorded_regardless_of_direction")


# ---------------------------------------------------------------------------
# Firewall, RISK boundary, representation
# ---------------------------------------------------------------------------


class TestFirewall:
    def test_literal_scan_is_a_floor(self, base_data: dict):
        assert base_data["prohibited_inputs"]["literal_scan_is_a_floor_not_the_boundary"] is True

    def test_downgrading_the_literal_scan_claim_rejected(self, data: dict):
        data["prohibited_inputs"]["literal_scan_is_a_floor_not_the_boundary"] = False
        _assert_rejected(data, "literal_scan_is_a_floor_not_the_boundary")

    def test_equal_division_barred_by_construction(self, base_data: dict):
        barred = base_data["prohibited_inputs"]["barred_constructions"]
        assert "EQUAL_DIVISION_INCLUDING_FRESHLY_COMPUTED" in barred
        assert "RESIDUAL_OR_COMPLEMENT_PLUG" in barred

    def test_removing_equal_division_bar_rejected(self, data: dict):
        data["prohibited_inputs"]["barred_constructions"] = [
            c
            for c in data["prohibited_inputs"]["barred_constructions"]
            if c != "EQUAL_DIVISION_INCLUDING_FRESHLY_COMPUTED"
        ]
        _assert_rejected(data, "EQUAL_DIVISION_INCLUDING_FRESHLY_COMPUTED")

    def test_risk_reuse_barred(self, data: dict):
        data["prohibited_inputs"]["barred_risk_reuse"] = []
        _assert_rejected(data, "ALL_TWENTY_LAPSED_CONSEQUENTIAL_PARAMETERS")

    def test_risk_lane_boundary_intact(self, base_data: dict):
        risk = base_data["risk_lane_boundary"]
        assert risk["retry"] == "PROHIBITED"
        assert risk["attempt_3"] == "DOES_NOT_EXIST"
        assert risk["protected_result_path"] == "/private/tmp/phq-risk0001-results"

    def test_permitting_risk_retry_rejected(self, data: dict):
        data["risk_lane_boundary"]["retry"] = "PERMITTED"
        _assert_rejected(data, "risk_lane_boundary.retry")


class TestRepresentation:
    def test_no_rule_created(self, base_data: dict):
        rep = base_data["representation"]
        assert rep["rule_created_by_this_program"] is False
        assert rep["cm_14_through_cm_17_membership_designated"] is False
        assert rep["disposition"] == "SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED"

    def test_creating_a_rule_rejected(self, data: dict):
        data["representation"]["rule_created_by_this_program"] = True
        _assert_rejected(data, "rule_created_by_this_program")

    def test_designating_cm_membership_rejected(self, data: dict):
        data["representation"]["cm_14_through_cm_17_membership_designated"] = True
        _assert_rejected(data, "cm_14_through_cm_17_membership_designated")

    def test_self_contained_path_preserved(self, data: dict):
        data["representation"]["self_contained_path_preserved"] = False
        _assert_rejected(data, "self_contained_path_preserved")


# ---------------------------------------------------------------------------
# Result boundary — the backdoor-endpoint control
# ---------------------------------------------------------------------------


class TestResultBoundary:
    @pytest.mark.parametrize(
        "flag",
        [
            "is_a_driver_source",
            "is_admissible_endpoint_supporting_evidence",
            "may_be_cited_as_endpoint_supporting_evidence",
            "may_enter_a_snapshot_as_a_driver",
        ],
    )
    def test_stage_1_output_is_never_evidence(self, base_data: dict, flag: str):
        assert base_data["result_status_of_stage_1_output"][flag] is False

    @pytest.mark.parametrize(
        "flag",
        [
            "is_a_driver_source",
            "is_admissible_endpoint_supporting_evidence",
            "may_be_cited_as_endpoint_supporting_evidence",
            "may_enter_a_snapshot_as_a_driver",
        ],
    )
    def test_promoting_stage_1_output_to_evidence_rejected(self, data: dict, flag: str):
        data["result_status_of_stage_1_output"][flag] = True
        _assert_rejected(data, flag)

    @pytest.mark.parametrize("entry", V.REQUIRED_FORBIDDEN_RESULT_CONTENT)
    def test_forbidden_result_content_complete(self, base_data: dict, entry: str):
        assert entry in base_data["result_schema"]["forbidden_result_content"]

    def test_removing_forbidden_result_content_rejected(self, data: dict):
        data["result_schema"]["forbidden_result_content"] = [
            e
            for e in data["result_schema"]["forbidden_result_content"]
            if e != "ANY_NUMERIC_SLEEVE_SHARE"
        ]
        _assert_rejected(data, "ANY_NUMERIC_SLEEVE_SHARE")

    def test_results_file_not_created_by_this_filing(self, base_data: dict):
        assert base_data["result_schema"]["results_path_created_by_this_filing"] is False
        assert not (ROOT / base_data["result_schema"]["results_path"]).exists()

    def test_cell_result_keys_carry_both_readings(self, base_data: dict):
        keys = base_data["result_schema"]["cell_result_keys"]
        for field in V.OPEN_READING_FIELDS:
            assert field in keys


# ---------------------------------------------------------------------------
# Abstention and prohibited scope
# ---------------------------------------------------------------------------


class TestAbstentionAndScope:
    @pytest.mark.parametrize("condition", V.REQUIRED_ABSTENTION_CONDITIONS)
    def test_abstention_condition_present(self, base_data: dict, condition: str):
        present = {row["condition"] for row in base_data["mandatory_abstention_conditions"]}
        assert condition in present

    def test_removed_abstention_condition_rejected(self, data: dict):
        data["mandatory_abstention_conditions"] = [
            r
            for r in data["mandatory_abstention_conditions"]
            if r["condition"] != "ANY_STEP_COULD_HAVE_BEEN_CHOSEN_DIFFERENTLY"
        ]
        _assert_rejected(data, "ANY_STEP_COULD_HAVE_BEEN_CHOSEN_DIFFERENTLY")

    def test_abstention_condition_requires_an_authority(self, data: dict):
        data["mandatory_abstention_conditions"][0]["authority"] = ""
        _assert_rejected(data, "authority")

    def test_abstention_is_a_complete_outcome(self, data: dict):
        data["abstention_is_a_complete_outcome"] = False
        _assert_rejected(data, "abstention_is_a_complete_outcome")

    @pytest.mark.parametrize("entry", V.REQUIRED_PROHIBITED_SCOPE)
    def test_prohibited_scope_entry_present(self, base_data: dict, entry: str):
        assert entry in base_data["prohibited_scope"]

    @pytest.mark.parametrize("entry", V.REQUIRED_PROTECTED_PATHS)
    def test_protected_path_present(self, base_data: dict, entry: str):
        assert entry in base_data["protected_paths"]

    def test_removing_a_prohibited_scope_entry_rejected(self, data: dict):
        data["prohibited_scope"] = [e for e in data["prohibited_scope"] if e != "ENDPOINT_CREATION"]
        _assert_rejected(data, "ENDPOINT_CREATION")

    def test_removing_the_risk_protected_path_rejected(self, data: dict):
        data["protected_paths"] = [
            p for p in data["protected_paths"] if p != "/private/tmp/phq-risk0001-results"
        ]
        _assert_rejected(data, "phq-risk0001-results")


# ---------------------------------------------------------------------------
# Adversarial content scans
# ---------------------------------------------------------------------------


class TestAdversarialScans:
    @pytest.mark.parametrize("pattern", V.BARRED_NUMERAL_PATTERNS)
    def test_barred_numeral_is_detected(self, pattern: str):
        # Derive a matching sample from the module's own pattern so this file embeds no anchor.
        sample = pattern.replace("\\", "")
        findings = V.scan_for_barred_content(f"value: {sample}", "fixture")
        assert findings, f"scanner missed a value matching /{pattern}/"

    def test_committed_artifacts_carry_no_barred_numeral(self):
        for path in (V.PREREG_PATH, V.PROTOCOL_PATH):
            text = path.read_text(encoding="utf-8")
            for pattern in V.BARRED_NUMERAL_PATTERNS:
                assert not re.search(pattern, text), f"{path.name} reproduces a barred value"

    @pytest.mark.parametrize("token", ["12%", "7.5 percent", "40 pct", "100%"])
    def test_endpoint_shaped_token_is_detected(self, token: str):
        findings = V.scan_for_barred_content(f"the sleeve share is {token}", "fixture")
        assert findings, f"scanner missed endpoint-shaped token {token!r}"

    def test_committed_artifacts_carry_no_endpoint_shaped_token(self):
        for path in (V.PREREG_PATH, V.PROTOCOL_PATH):
            findings = V.scan_for_barred_content(path.read_text(encoding="utf-8"), path.name)
            assert not findings, f"{path.name}: {findings}"

    def test_ordinary_prose_is_not_a_false_positive(self):
        clean = "The share of one normalized unit attributable to one named sleeve, at exact precision."
        assert V.scan_for_barred_content(clean, "fixture") == ()

    def test_derived_counts_are_not_false_positives(self):
        assert V.scan_for_barred_content("4 sleeves x 2 bounds x 6 classes = 48 cells", "f") == ()

    def test_decision_states_no_endpoint_value(self):
        text = V.DECISION_PATH.read_text(encoding="utf-8")
        for pattern in V.BARRED_NUMERAL_PATTERNS:
            assert not re.search(pattern, text), "the decision reproduces a barred value"


# ---------------------------------------------------------------------------
# Mirror and hash pins
# ---------------------------------------------------------------------------


class TestMirrorAndPins:
    def test_missing_mirror_block_rejected(self):
        result = V.validate_protocol_mirror("# protocol with no mirror block\n")
        assert not result.ok
        assert any("MIRROR" in e for e in result.errors)

    def test_mirror_value_mismatch_rejected(self):
        text = V.PROTOCOL_PATH.read_text(encoding="utf-8").replace(
            "cell_ceiling: 48", "cell_ceiling: 96"
        )
        result = V.validate_protocol_mirror(text)
        assert not result.ok
        assert any("cell_ceiling" in e for e in result.errors)

    def test_mirror_extra_key_rejected(self):
        text = V.PROTOCOL_PATH.read_text(encoding="utf-8").replace(
            "hash_version: ENDPOINT-0001-PREREG-V1",
            "hash_version: ENDPOINT-0001-PREREG-V1\nsmuggled_key: yes",
        )
        result = V.validate_protocol_mirror(text)
        assert not result.ok
        assert any("smuggled_key" in e for e in result.errors)

    def test_mirror_reports_stage_2_unauthorized(self):
        mirror = V.extract_block(
            V.PROTOCOL_PATH.read_text(encoding="utf-8"), V.MIRROR_BLOCK_RE
        )
        assert mirror is not None
        assert mirror["stage_2_authorized"] == "false"
        assert mirror["consequential_parameter_count"] == "0"

    def test_missing_hash_block_rejected(self):
        result = V.validate_charter_hash_pins("## decision with no pins\n")
        assert not result.ok
        assert any("HASH-PINS" in e for e in result.errors)

    def test_hash_mismatch_voids_execution_authority(self):
        text = V.DECISION_PATH.read_text(encoding="utf-8")
        actual = V.sha256_file(V.PREREG_PATH)
        tampered = text.replace(actual, "0" * 64)
        result = V.validate_charter_hash_pins(tampered)
        assert not result.ok
        assert any("voids execution authority" in e for e in result.errors)

    def test_wrong_pinned_path_rejected(self):
        text = V.DECISION_PATH.read_text(encoding="utf-8").replace(
            "protocol_path: research/level1_endpoint_evidence/PROTOCOL_V1.md",
            "protocol_path: research/level1_sleeve_robustness/PROTOCOL_V1.md",
        )
        result = V.validate_charter_hash_pins(text)
        assert not result.ok
        assert any("protocol_path" in e for e in result.errors)


# ---------------------------------------------------------------------------
# Module boundaries and repository invariants
# ---------------------------------------------------------------------------


class TestModuleBoundaries:
    def test_zero_import_coupling_with_allocator_and_margin(self):
        tree = ast.parse(Path(V.__file__).read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        assert "allocate" not in imported
        assert "margin_state" not in imported
        assert "levels" not in imported

    def test_validator_performs_no_writes(self):
        source = Path(V.__file__).read_text(encoding="utf-8")
        for forbidden in ("write_text(", "write_bytes(", "open(", "os.remove", "shutil."):
            assert forbidden not in source, f"validator must be read-only; found {forbidden!r}"

    def test_risk_result_path_is_named_as_protected_never_opened(self):
        # The module names the RISK results path twice, both as inert string constants: once in
        # REQUIRED_PROTECTED_PATHS and once in the firewall equality check. Neither is a filesystem
        # access. The property that matters is that every path this module actually touches is one
        # of its three declared canonical targets, none of which is under the RISK lane.
        assert "/private/tmp/phq-risk0001-results" in V.REQUIRED_PROTECTED_PATHS
        touched = (V.PREREG_PATH, V.PROTOCOL_PATH, V.DECISION_PATH)
        for path in touched:
            resolved = str(path.resolve())
            assert "phq-risk0001-results" not in resolved
            assert "level1_sleeve_robustness" not in resolved
        source = Path(V.__file__).read_text(encoding="utf-8")
        assert "Path(" not in source.replace("Path(__file__)", ""), (
            "the module must construct no filesystem path beyond its three declared constants"
        )

    def test_validator_is_not_an_endpoint_admission_validator(self):
        # The J.1-J.12 admission validator is a separately authorized successor, not this module.
        assert V.__doc__ is not None
        collapsed = " ".join(V.__doc__.split())
        assert "is NOT an XASSET-0024" in collapsed
        assert "endpoint-admission validator" in collapsed
        assert "separately authorized successor" in collapsed


class TestRepositoryInvariants:
    def test_application_directory_absent(self):
        assert not (ROOT / "intelligence/level1_application").exists()

    def test_results_directory_contains_no_execution_artifact(self):
        research_dir = ROOT / "research/level1_endpoint_evidence"
        names = sorted(p.name for p in research_dir.iterdir())
        assert names == ["PROTOCOL_V1.md", "pre_registration.yaml"]

    def test_risk_lane_artifacts_untouched_by_this_module(self):
        assert (ROOT / "research/level1_sleeve_robustness/pre_registration.yaml").exists()

    def test_decision_file_declares_lane_g_and_proposed_status(self):
        text = V.DECISION_PATH.read_text(encoding="utf-8")
        assert "status: Proposed" in text
        assert "decision_id: XASSET-0027" in text
