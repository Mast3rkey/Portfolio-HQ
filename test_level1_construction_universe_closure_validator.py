"""Focused and adversarial tests for the ENDPOINT-0001 construction-universe closure determination.

Authorized by governance/decisions/XASSET-0028-concrete-construction-universe-closure-determination.md

The determination is negative, so these tests are the mirror image of a closure test suite. They
prove that the artifact cannot be mutated into a closure claim, that the family-slot grid cannot be
promoted into the construction universe, that the negative is not overstated as permanent
impossibility, and that both prerequisites survive intact -- plus the twenty-two adversarial failure
classes the authorizing unit was required to test against.
"""

from __future__ import annotations

import ast
import copy
from pathlib import Path

import pytest
import yaml

import level1_construction_universe_closure_validator as V

ROOT = Path(__file__).resolve().parent


@pytest.fixture(scope="module")
def real() -> dict:
    return yaml.safe_load(V.DETERMINATION_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def doc(real: dict) -> dict:
    return copy.deepcopy(real)


def find(errors: list[str], needle: str) -> bool:
    return any(needle in error for error in errors)


# ==================================================================================================
# Baseline
# ==================================================================================================


class TestBaseline:
    def test_real_determination_validates_clean(self):
        assert V.validate_determination_file() == []

    def test_real_determination_records_the_negative(self, real):
        assert real["determination"]["status"] == "NOT_CLOSED_PREREQUISITE_REQUIRED"
        assert real["determination"]["stage_1_executable"] is False
        assert real["determination"]["a_concrete_construction_universe_was_frozen"] is False

    def test_real_determination_answers_p_0(self, real):
        assert real["answers"] == "XASSET_0027_SECTION_P_0"
        assert real["governing_decision"] == "XASSET-0028"

    def test_main_returns_zero(self, capsys):
        assert V.main() == 0
        out = capsys.readouterr().out
        assert "NOT CLOSED" in out
        assert "NOT EXECUTABLE" in out


# ==================================================================================================
# 1-6, 15  Universe integrity: no construction may be registered, invented, or promoted
# ==================================================================================================


class TestUniverseIntegrity:
    def test_status_cannot_be_upgraded_to_closed(self, doc):
        doc["determination"]["status"] = "CLOSED"
        assert find(V.validate_determination_data(doc), "determination.status")

    def test_stage_1_cannot_be_marked_executable(self, doc):
        doc["determination"]["stage_1_executable"] = True
        assert find(V.validate_determination_data(doc), "determination.stage_1_executable")

    def test_universe_cannot_be_marked_frozen(self, doc):
        doc["determination"]["a_concrete_construction_universe_was_frozen"] = True
        assert find(
            V.validate_determination_data(doc),
            "a_concrete_construction_universe_was_frozen",
        )

    def test_outcome_class_cannot_be_flipped_positive(self, doc):
        doc["determination"]["outcome_class"] = "POSITIVE_UNIVERSE_CLOSED"
        assert find(V.validate_determination_data(doc), "determination.outcome_class")

    def test_no_construction_registry_exists_in_the_artifact(self, real):
        """The artifact registers no construction -- there is nothing an executor could run.

        Checked against parsed keys rather than raw substrings, so that ordinary prose using the
        word "constructions" cannot mask, or be mistaken for, an actual registry key.
        """
        forbidden = {
            "construction_id",
            "constructions",
            "registered_constructions",
            "construction_registry",
            "closed_construction_universe",
        }

        def keys_of(node):
            found = set()
            if isinstance(node, dict):
                for key, value in node.items():
                    found.add(str(key))
                    found |= keys_of(value)
            elif isinstance(node, list):
                for item in node:
                    found |= keys_of(item)
            return found

        assert keys_of(real) & forbidden == set()

    def test_family_slot_grid_status_cannot_be_promoted_to_the_universe(self, doc):
        doc["preserved"]["family_slot_grid_status"] = "THE_CONSTRUCTION_UNIVERSE"
        assert find(V.validate_determination_data(doc), "preserved.family_slot_grid_status")

    def test_family_slot_grid_cannot_become_a_trial_ceiling(self, doc):
        doc["preserved"]["family_slot_grid_is_a_trial_ceiling"] = True
        assert find(
            V.validate_determination_data(doc), "preserved.family_slot_grid_is_a_trial_ceiling"
        )

    @pytest.mark.parametrize("claim", list(V.BANNED_CLOSURE_CLAIMS))
    def test_every_closure_claim_is_rejected(self, doc, claim):
        doc["determination"]["statement"] = f"The {claim} and Stage 1 may proceed."
        assert find(V.validate_determination_data(doc), "would let a reader treat")


# ==================================================================================================
# 7-8  Frozen provenance: canonical identity cannot be substituted or faked
# ==================================================================================================


class TestCanonicalProvenance:
    def test_recorded_hash_must_match_the_accepted_pin(self, doc):
        doc["canonical_files_verified"]["files"][0]["sha256"] = "0" * 64
        assert find(V.validate_determination_data(doc), "does not match the XASSET-0027 pin")

    def test_substituted_source_path_is_rejected(self, doc):
        doc["canonical_files_verified"]["files"][0]["path"] = "research/elsewhere/PROTOCOL_V1.md"
        assert find(V.validate_determination_data(doc), "missing entry for")

    def test_correct_looking_but_wrong_hash_is_rejected(self, doc):
        """A plausible 64-hex string that is not the pinned digest must still fail."""
        doc["canonical_files_verified"]["files"][1]["sha256"] = "a1b2c3d4" * 8
        assert find(V.validate_determination_data(doc), "does not match the XASSET-0027 pin")

    def test_claiming_canonical_files_were_modified_is_rejected(self, doc):
        doc["canonical_files_verified"]["modified_by_this_determination"] = True
        assert find(V.validate_determination_data(doc), "modified_by_this_determination")

    def test_observed_bytes_are_recomputed_not_trusted(self):
        """The pins are verified against the files on disk, not merely against the document."""
        for path, pin in V.CANONICAL_PINS.items():
            assert V.sha256_file(ROOT / path) == pin

    def test_canonical_files_are_byte_unchanged_by_this_unit(self):
        assert V.validate_determination_file() == []
        for path, pin in V.CANONICAL_PINS.items():
            assert V.sha256_file(ROOT / path) == pin


# ==================================================================================================
# 9-11, 16  Prerequisite integrity and the slot arithmetic
# ==================================================================================================


class TestPrerequisites:
    @pytest.mark.parametrize("prereq_id", list(V.REQUIRED_PREREQUISITE_IDS))
    def test_neither_prerequisite_may_be_dropped(self, doc, prereq_id):
        doc["blocking_prerequisites"]["prerequisites"] = [
            p for p in doc["blocking_prerequisites"]["prerequisites"] if p["id"] != prereq_id
        ]
        assert find(V.validate_determination_data(doc), f"missing {prereq_id}")

    def test_independence_note_is_required(self, doc):
        doc["blocking_prerequisites"]["independence_note"] = ""
        assert find(V.validate_determination_data(doc), "independence_note")

    def test_prereq_1_slot_count_is_verified_against_the_real_generator(self, doc):
        p1 = doc["blocking_prerequisites"]["prerequisites"][0]
        p1["blocks_slots"] = 999
        assert find(V.validate_determination_data(doc), "verified against the accepted family-slot")

    def test_generator_derived_counts_are_what_the_artifact_claims(self, real):
        p1 = real["blocking_prerequisites"]["prerequisites"][0]
        assert p1["blocks_slots"] == V.comparison_scoped_slot_count()
        assert p1["blocks_slots_of"] == V.total_slot_count()

    def test_comparison_scoped_count_is_one_half_of_the_grid(self):
        """Three of six DRIVER classes are comparison-scoped, so exactly half the slots."""
        assert V.comparison_scoped_slot_count() * 2 == V.total_slot_count()

    def test_prereq_1_affected_classes_must_be_exactly_the_three_comparison_scoped(self, doc):
        p1 = doc["blocking_prerequisites"]["prerequisites"][0]
        p1["affected_driver_classes"] = ["valuation_opportunity_cost"]
        assert find(V.validate_determination_data(doc), "affected_driver_classes")

    def test_diversification_cobehavior_must_stay_unaffected(self, doc):
        """XASSET-0020 closes its comparator space at six unordered pairs; it is not blocked."""
        p1 = doc["blocking_prerequisites"]["prerequisites"][0]
        p1["unaffected_driver_classes"] = ["portfolio_function"]
        assert find(V.validate_determination_data(doc), "diversification_cobehavior")

    def test_prereq_2_must_block_every_slot(self, doc):
        p2 = doc["blocking_prerequisites"]["prerequisites"][1]
        p2["blocks_slots"] = 120
        assert find(V.validate_determination_data(doc), "PREREQ_2.blocks_slots")

    def test_prerequisites_state_why_this_unit_cannot_supply_them(self, real):
        for entry in real["blocking_prerequisites"]["prerequisites"]:
            assert entry["why_this_unit_cannot_supply_it"].strip()

    def test_no_comparator_rule_is_supplied(self, real):
        assert real["non_authorization"]["supplies_a_comparator_rule"] is False


# ==================================================================================================
# 12-14  Contamination: representation, anchors, equal-split and residual leakage
# ==================================================================================================


class TestContamination:
    def test_representation_dependency_cannot_be_silently_solved(self, doc):
        doc["preserved"]["representation_posture"] = "AGGREGATION_RULE_SUPPLIED"
        assert find(V.validate_determination_data(doc), "preserved.representation_posture")

    def test_no_representation_rule_is_created(self, doc):
        doc["preserved"]["representation_rule_created"] = True
        assert find(V.validate_determination_data(doc), "representation_rule_created")

    def test_cm_membership_is_not_designated(self, doc):
        doc["preserved"]["cm_14_through_cm_17_designated"] = True
        assert find(V.validate_determination_data(doc), "cm_14_through_cm_17_designated")

    @pytest.mark.parametrize("numeral", list(V.BARRED_HISTORICAL_NUMERALS))
    def test_barred_historical_anchors_are_rejected(self, doc, numeral):
        doc["determination"]["statement"] = f"A prior output of {numeral} is noted."
        assert find(V.validate_determination_data(doc), "barred historical output")

    @pytest.mark.parametrize("value", ["25%", "12.5 %", "3.75 percent"])
    def test_endpoint_shaped_percentages_are_rejected(self, doc, value):
        doc["determination"]["statement"] = f"The endpoint would be {value}."
        assert find(V.validate_determination_data(doc), "endpoint-shaped percentage")

    def test_real_artifact_contains_no_percentage_or_barred_anchor(self, real):
        assert not find(V.validate_determination_data(real), "endpoint-shaped percentage")
        assert not find(V.validate_determination_data(real), "barred historical output")


# ==================================================================================================
# 18-19  Neither overstated closure nor overstated impossibility
# ==================================================================================================


class TestNoOverclaim:
    @pytest.mark.parametrize("phrase", list(V.BANNED_PERMANENCE_PHRASES))
    def test_permanent_impossibility_phrasing_is_rejected(self, doc, phrase):
        doc["determination"]["statement"] = f"Closure {phrase} be achieved."
        assert find(V.validate_determination_data(doc), "asserts a permanent impossibility")

    def test_present_authority_bound_cannot_be_dropped(self, doc):
        doc["determination"]["determination_is_present_authority_bounded"] = False
        assert find(V.validate_determination_data(doc), "present_authority_bounded")

    def test_non_permanence_flag_cannot_be_dropped(self, doc):
        doc["determination"]["determination_is_not_permanent_impossibility"] = False
        assert find(V.validate_determination_data(doc), "not_permanent_impossibility")

    def test_negative_does_not_rest_on_lack_of_imagination(self, real):
        """The artifact must state why more imagination would not produce exhaustiveness."""
        reason = real["specification_analysis"]["why_this_is_not_a_failure_of_imagination"]
        assert "closure principle" in reason
        assert "exhaustiveness" in reason

    def test_dissolution_path_keeps_the_blocker_non_permanent(self, real):
        assert real["non_governance_dissolution_path"]["exists"] is True

    def test_partial_closure_is_recorded_as_achievable_but_not_shipped(self, real):
        assert real["partial_closure"]["achievable"] is True
        assert real["partial_closure"]["shipped"] is False


# ==================================================================================================
# The disclosed-quotation exemption is narrow
# ==================================================================================================


class TestQuotationExemptionIsNarrow:
    def test_exemption_matches_only_the_observed_text_field(self):
        assert V._is_disclosed_quotation("disclosed_findings[0].observed_text")
        assert V._is_disclosed_quotation("disclosed_findings[7].observed_text")

    @pytest.mark.parametrize(
        "where",
        [
            "disclosed_findings[0].why_it_is_a_finding",
            "disclosed_findings[0].enforcement_response",
            "disclosed_findings[0].observed_text.nested",
            "determination.statement",
            "observed_text",
            "routes_examined[0].observed_text",
        ],
    )
    def test_exemption_does_not_extend_anywhere_else(self, where):
        assert not V._is_disclosed_quotation(where)

    def test_same_phrase_outside_the_quotation_field_is_still_rejected(self, doc):
        doc["disclosed_findings"][0]["why_it_is_a_finding"] = "the search surface is closed"
        assert find(V.validate_determination_data(doc), "would let a reader treat")

    def test_permanence_scan_still_applies_inside_the_quotation_field(self, doc):
        """The exemption covers closure claims only, never permanence overclaim."""
        doc["disclosed_findings"][0]["observed_text"] = "closure can never be achieved"
        assert find(V.validate_determination_data(doc), "asserts a permanent impossibility")

    def test_percentage_scan_still_applies_inside_the_quotation_field(self, doc):
        doc["disclosed_findings"][0]["observed_text"] = "the endpoint is 25%"
        assert find(V.validate_determination_data(doc), "endpoint-shaped percentage")


# ==================================================================================================
# 17  A construction family is not a concrete construction
# ==================================================================================================


class TestFamilyIsNotAConstruction:
    def test_grid_remains_a_classification_scaffold(self, real):
        assert (
            real["preserved"]["family_slot_grid_status"]
            == "CLASSIFICATION_SCAFFOLD_NOT_A_CONSTRUCTION_UNIVERSE"
        )

    def test_grammar_route_records_the_relabelling_trap(self, real):
        grammar = next(
            r for r in real["routes_examined"] if r["route"] == "DETERMINISTIC_CONSTRUCTION_GRAMMAR"
        )
        assert "relabel the five provenance families" in grammar["unavailable_because"]

    def test_accepted_grid_is_not_exhaustive_over_constructions(self):
        """Cross-check against the accepted preregistration rather than restating it."""
        prereg = yaml.safe_load(V.PREREG.PREREG_PATH.read_text(encoding="utf-8"))
        assert prereg["family_slot_grid"]["exhaustive_over_constructions"] is False
        assert prereg["construction_universe_closure"]["status"] == "NOT_CLOSED"


# ==================================================================================================
# 20-22  K.1, J.12, and RISK boundaries
# ==================================================================================================


class TestPreservedOpenQuestions:
    def test_k_1_cannot_be_implicitly_resolved(self, doc):
        doc["preserved"]["xasset_0024_section_k_1_reading"] = "RESOLVED_SUBJECT_MATTER_READING"
        assert find(V.validate_determination_data(doc), "section_k_1_reading")

    def test_j_12_cannot_be_prematurely_reconciled(self, doc):
        doc["preserved"]["xasset_0024_section_j_12"] = "RECONCILED"
        assert find(V.validate_determination_data(doc), "section_j_12")

    def test_risk_artifacts_recorded_as_not_accessed(self, doc):
        doc["preserved"]["risk_0001_artifacts_accessed"] = True
        assert find(V.validate_determination_data(doc), "risk_0001_artifacts_accessed")

    def test_risk_reuse_cannot_be_authorized(self, doc):
        doc["preserved"]["risk_reuse_authorized"] = True
        assert find(V.validate_determination_data(doc), "risk_reuse_authorized")

    def test_no_risk_result_path_is_referenced_anywhere(self):
        for path in (V.DETERMINATION_PATH, ROOT / V.__name__.replace(".", "/")):
            pass
        text = V.DETERMINATION_PATH.read_text(encoding="utf-8")
        assert "phq-risk0001-results" not in text
        module = Path(V.__file__).read_text(encoding="utf-8")
        assert "phq-risk0001-results" not in module

    def test_stage_2_cannot_be_authorized(self, doc):
        doc["preserved"]["stage_2_authorized"] = True
        assert find(V.validate_determination_data(doc), "stage_2_authorized")

    def test_endpoint_authority_remains_unexercised(self, doc):
        doc["preserved"]["level1_endpoint_authority_exercised"] = True
        assert find(V.validate_determination_data(doc), "level1_endpoint_authority_exercised")

    def test_application_authority_remains_withheld(self, doc):
        doc["preserved"]["application_authority"] = "GRANTED"
        assert find(V.validate_determination_data(doc), "application_authority")


# ==================================================================================================
# Closure test and route completeness
# ==================================================================================================


class TestClosureTestAndRoutes:
    @pytest.mark.parametrize("criterion", list(V.REQUIRED_CLOSURE_CRITERIA))
    def test_no_closure_criterion_may_be_dropped(self, doc, criterion):
        doc["closure_test"]["criteria"] = [
            c for c in doc["closure_test"]["criteria"] if c["id"] != criterion
        ]
        assert find(V.validate_determination_data(doc), f"missing {criterion}")

    def test_c3_cannot_be_marked_satisfiable(self, doc):
        for entry in doc["closure_test"]["criteria"]:
            if entry["id"] == "C3_EXHAUSTIVE_OVER_CONSTRUCTIONS":
                entry["satisfiable_under_this_authority"] = True
        assert find(V.validate_determination_data(doc), "C3].satisfiable_under_this_authority")

    def test_c3_must_remain_decisive(self, doc):
        for entry in doc["closure_test"]["criteria"]:
            if entry["id"] == "C3_EXHAUSTIVE_OVER_CONSTRUCTIONS":
                entry["decisive"] = False
        assert find(V.validate_determination_data(doc), "C3].decisive")

    @pytest.mark.parametrize("route", list(V.REQUIRED_ROUTES))
    def test_no_route_may_be_dropped(self, doc, route):
        doc["routes_examined"] = [r for r in doc["routes_examined"] if r["route"] != route]
        assert find(V.validate_determination_data(doc), f"missing {route}")

    def test_a_rejected_route_cannot_be_marked_taken(self, doc):
        doc["routes_examined"][0]["taken"] = True
        assert find(V.validate_determination_data(doc), "must be marked")

    def test_registry_route_cannot_be_marked_available(self, doc):
        doc["routes_examined"][0]["available_under_this_authority"] = True
        assert find(V.validate_determination_data(doc), "available_under_this_authority")

    def test_both_dominance_and_quotient_routes_were_examined(self, real):
        names = {r["route"] for r in real["routes_examined"]}
        assert "DOMINANCE_OVER_A_MAXIMALLY_PERMISSIVE_CONSTRUCTION" in names
        assert "FINITE_QUOTIENT_OVER_GATE_OUTCOME_VECTORS" in names


# ==================================================================================================
# Parameters, non-authorization, findings, and malformed input
# ==================================================================================================


class TestParametersAndNonAuthorization:
    def test_a_consequential_parameter_cannot_be_introduced(self, doc):
        doc["consequential_parameter_registry"]["parameters"] = [{"parameter_id": "X"}]
        assert find(V.validate_determination_data(doc), "must be empty")

    def test_zero_parameter_declaration_cannot_be_dropped(self, doc):
        doc["consequential_parameter_registry"]["zero_parameter_declaration"][
            "introduces_zero_consequential_numeric_parameters"
        ] = False
        assert find(V.validate_determination_data(doc), "introduces_zero_consequential")

    @pytest.mark.parametrize(
        "key",
        [
            "closes_a_construction_universe",
            "makes_stage_1_executable",
            "authorizes_stage_2",
            "supplies_a_comparator_rule",
            "resolves_xasset_0024_section_k_1",
            "amends_any_canonical_hash_pinned_file",
            "authorizes_chart_ladder_optimizer_deployment_trade_or_order",
        ],
    )
    def test_no_non_authorization_may_be_flipped_true(self, doc, key):
        doc["non_authorization"][key] = True
        assert find(V.validate_determination_data(doc), f"non_authorization.{key}")

    def test_non_authorization_cannot_be_emptied(self, doc):
        doc["non_authorization"] = {}
        assert find(V.validate_determination_data(doc), "must not be empty")


class TestFindings:
    def test_stale_sentence_finding_must_remain_disclosed(self, doc):
        doc["disclosed_findings"] = []
        assert find(V.validate_determination_data(doc), "must remain disclosed")

    def test_a_finding_must_say_why_it_was_not_corrected(self, doc):
        doc["disclosed_findings"][0]["not_corrected_because"] = ""
        assert find(V.validate_determination_data(doc), "not_corrected_because")

    def test_finding_1_points_at_the_real_stale_text(self, real):
        """The disclosure must be verifiable against the canonical file it names."""
        finding = real["disclosed_findings"][0]
        assert "pre_registration.yaml" in finding["location"]
        prereg_text = V.PREREG.PREREG_PATH.read_text(encoding="utf-8")
        assert "the qualitative" in prereg_text and "search surface is closed" in prereg_text

    def test_finding_1_is_not_claimed_to_be_an_enforcement_gap(self, real):
        assert real["disclosed_findings"][0]["is_an_enforcement_gap"] is False


class TestMalformedInput:
    def test_non_mapping_top_level_is_rejected(self):
        assert V.validate_determination_data(["not", "a", "mapping"]) != []

    def test_missing_file_is_reported(self, tmp_path):
        errors = V.validate_determination_file(tmp_path / "absent.yaml")
        assert find(errors, "missing")

    def test_malformed_yaml_is_reported(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text("determination: [unclosed\n", encoding="utf-8")
        assert find(V.validate_determination_file(bad), "could not be parsed")

    def test_empty_document_is_rejected(self, tmp_path):
        empty = tmp_path / "empty.yaml"
        empty.write_text("", encoding="utf-8")
        assert V.validate_determination_file(empty) != []


# ==================================================================================================
# Repository invariants and isolation
# ==================================================================================================


class TestRepositoryInvariants:
    def test_no_stage_1_results_artifact_exists(self):
        assert not (ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()

    def test_no_application_directory_exists(self):
        assert not (ROOT / "intelligence/level1_application").exists()

    def test_endpoint_evidence_directory_still_holds_exactly_its_two_canonical_files(self):
        """This unit sited its artifact elsewhere precisely so this invariant stays untouched."""
        research_dir = ROOT / "research/level1_endpoint_evidence"
        assert sorted(p.name for p in research_dir.iterdir()) == [
            "PROTOCOL_V1.md",
            "pre_registration.yaml",
        ]

    def test_determination_directory_holds_only_the_determination(self):
        directory = ROOT / "research/level1_construction_universe"
        assert sorted(p.name for p in directory.iterdir()) == ["CLOSURE_DETERMINATION_V1.yaml"]

    def test_zero_import_coupling_with_allocator_and_margin(self):
        tree = ast.parse(Path(V.__file__).read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        assert "allocate" not in imported
        assert "margin_state" not in imported
        assert "levels" not in imported

    def test_only_read_only_generator_is_borrowed_from_the_charter_validator(self):
        """The single cross-module dependency exists so slot counts are derived, not asserted."""
        assert V.PREREG.generate_family_slot_grid() == V.PREREG.generate_family_slot_grid()
        assert len(V.PREREG.generate_family_slot_grid()) == V.total_slot_count()

    def test_decision_file_exists_and_is_lane_g_proposed(self):
        text = V.DECISION_PATH.read_text(encoding="utf-8")
        assert "decision_id: XASSET-0028" in text
        assert "status: Proposed" in text
