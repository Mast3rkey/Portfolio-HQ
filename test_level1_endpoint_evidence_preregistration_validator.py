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
import itertools
import random
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


def _assert_rejected(mutated: dict, fragment: str) -> None:
    result = V.validate(mutated)
    assert not result.ok, f"expected rejection mentioning {fragment!r}, got a clean pass"
    assert any(fragment in e for e in result.errors), (
        f"expected an error mentioning {fragment!r}; got {result.errors}"
    )


# ---------------------------------------------------------------------------
# Synthetic Stage-1 results helpers (no results document exists or is authorized)
# ---------------------------------------------------------------------------


def _passing_gates() -> dict[str, str]:
    return {gate: "PASS" for gate in V.GATE_IDS}


def _synthetic_universe(construction_ids=None) -> dict[str, dict]:
    """Build a SYNTHETIC closed construction universe for exercising the enforcement machinery.

    No closed construction universe exists in the repository (XASSET-0027 does not close one), so
    validate_stage1_results fails closed when called for real. These tests supply one explicitly to
    test the enforcement logic itself, which is a different claim from asserting a real one exists.
    """
    ids = tuple(construction_ids) if construction_ids is not None else V.generate_family_slot_grid()
    return {
        construction_id: {
            "cell_id": V.cell_id_of(construction_id),
            "source_architecture": "HYPOTHETICAL_SOURCE_ARCHITECTURE",
            "source_path": None,
            "source_sha256": None,
            "hypothetical_source_requirements": _FROZEN_REQUIREMENTS,
        }
        for construction_id in ids
    }


_FROZEN_REQUIREMENTS = "a source that would state the SS-C quantity intrinsically"


def _candidate_row(construction_id: str, gates: dict[str, str] | None = None, **overrides) -> dict:
    gates = gates if gates is not None else _passing_gates()
    sleeve, bound, driver_class, family_id = construction_id.split("::")
    family = {f[0]: f for f in V.CONSTRUCTION_FAMILIES}[family_id]
    row = {
        "construction_id": construction_id,
        "cell_id": V.cell_id_of(construction_id),
        "sleeve": sleeve,
        "bound": bound,
        "driver_class": driver_class,
        "family_id": family_id,
        "route": family[1],
        "num_0001_class": family[2],
        "source_architecture": "HYPOTHETICAL_SOURCE_ARCHITECTURE",
        "source_path": None,
        "source_sha256": None,
        "hypothetical_source_requirements": _FROZEN_REQUIREMENTS,
        "governing_authority_refs": ["XASSET-0024_SECTION_J"],
        "gate_results": gates,
        "categorical_failures": [g for g in V.CATEGORICAL_GATES if gates.get(g) == "FAIL"],
        "prerequisite_failures": [g for g in V.PREREQUISITE_GATES if gates.get(g) == "FAIL"],
        "disposition": V.derive_candidate_disposition(gates),
        "first_failing_gate_id": next((g for g in V.GATE_IDS if gates.get(g) == "FAIL"), None),
        "g2_outcome_under_subject_matter_reading": "PASSES",
        "g2_outcome_under_preference_only_reading": "PASSES",
        "g2_outcome_is_reading_dependent": False,
        "point_or_range_support": "WOULD_SUPPORT_RANGE_ENDPOINT",
        "representation_dependency": None,
        "uncertainty_statement": "recorded",
        # Added to the publishable schema by the XASSET-0036 SS-G.B package (MAJOR 2, review
        # 4953193650), so B1's preserved floor survives serialization instead of living only as
        # the runner's input-time refusal. A conforming row records it.
        "g12_basis": (
            "NO_LAWFUL_SUCCESSOR_IDENTIFIABLE_ON_INDEPENDENT_GROUNDS"
            if gates.get("G12_SNAPSHOT_ADMISSIBILITY_PATH") == "FAIL"
            else "LAWFUL_SUCCESSOR_IDENTIFIABLE"
        ),
    }
    row.update(overrides)
    return row


def _full_results(gates_for=None) -> dict:
    """A complete, conforming synthetic results document over the synthetic universe."""
    rows = []
    for construction_id in V.generate_family_slot_grid():
        gates = gates_for(construction_id) if gates_for else _passing_gates()
        rows.append(_candidate_row(construction_id, gates))
    by_cell: dict[str, list[str]] = {}
    for row in rows:
        by_cell.setdefault(row["cell_id"], []).append(row["disposition"])
    cells = [
        {"cell_id": cell, "outcome": V.derive_cell_outcome(dispositions)}
        for cell, dispositions in by_cell.items()
    ]
    return {"candidate_results": rows, "cell_results": cells, "disposition": "RECORDED"}


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
        assert V.validate_protocol_mirror(V.PROTOCOL_PATH.read_text(encoding="utf-8")).ok

    def test_charter_hash_pins_match_committed_bytes(self):
        assert V.validate_charter_hash_pins(V.DECISION_PATH.read_text(encoding="utf-8")).ok

    def test_hashes_are_reproducible(self):
        first = V.sha256_file(V.PREREG_PATH)
        assert first == V.sha256_file(V.PREREG_PATH) and len(first) == 64


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
        assert not V.validate({"schema_version": "2.0"}).ok

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
# MAJOR 1 — construction families and the closed candidate universe
# ---------------------------------------------------------------------------


class TestConstructionFamilies:
    def test_exactly_five_lawful_families(self, base_data: dict):
        assert len(base_data["construction_families"]["families"]) == 5

    def test_families_match_xasset_0023_route_class_coherence(self, base_data: dict):
        rows = base_data["construction_families"]["families"]
        assert [(r["route"], r["num_0001_class"]) for r in rows] == [
            ("R1", 1), ("R1", 3), ("R1", 4), ("R1", 5), ("R2", 2)
        ]

    def test_class_6_excluded(self, base_data: dict):
        assert base_data["construction_families"]["excluded_class"]["num_0001_class"] == 6

    def test_removing_a_family_rejected(self, data: dict):
        data["construction_families"]["families"].pop()
        _assert_rejected(data, "expected exactly 5 lawful")

    def test_adding_a_sixth_family_rejected(self, data: dict):
        extra = copy.deepcopy(data["construction_families"]["families"][0])
        extra["family_id"] = "R3_C7"
        data["construction_families"]["families"].append(extra)
        _assert_rejected(data, "expected exactly 5 lawful")

    def test_unlawful_route_class_pairing_rejected(self, data: dict):
        # R2 may only carry class 2 (XASSET-0023 SS-H.4 item 3).
        data["construction_families"]["families"][4]["num_0001_class"] = 4
        _assert_rejected(data, "num_0001_class")

    def test_family_that_only_clips_rejected(self, data: dict):
        data["construction_families"]["families"][0]["originates_or_clips"] = "CLIP"
        _assert_rejected(data, "originates_or_clips")

    def test_closure_basis_cites_accepted_authority(self, data: dict):
        data["construction_families"]["closure_basis"]["route_class_coherence_closed_by"] = "AUTHOR_JUDGMENT"
        _assert_rejected(data, "route_class_coherence_closed_by")

    def test_all_eight_non_routes_recorded(self, base_data: dict):
        assert len(base_data["construction_families"]["excluded_non_routes"]["non_routes"]) == 8


class TestFamilySlotGrid:
    def test_generator_produces_240_unique_slots(self):
        grid = V.generate_family_slot_grid()
        assert len(grid) == 240
        assert len(set(grid)) == 240

    def test_generator_is_byte_identically_reproducible(self):
        assert V.generate_family_slot_grid() == V.generate_family_slot_grid()

    def test_generator_covers_48_cells_with_five_slots_each(self):
        cells = V.generate_cell_universe()
        assert len(cells) == 48
        for cell in cells:
            members = [c for c in V.generate_family_slot_grid() if V.cell_id_of(c) == cell]
            assert len(members) == 5

    def test_every_sleeve_and_bound_covered(self):
        grid = V.generate_family_slot_grid()
        for sleeve in V.SLEEVES:
            for bound in V.BOUNDS:
                assert any(c.startswith(f"{sleeve}::{bound}::") for c in grid)

    def test_grid_is_the_product_of_the_closed_dimensions(self):
        expected = (
            len(V.SLEEVES) * len(V.BOUNDS) * len(V.DRIVER_CLASSES) * len(V.CONSTRUCTION_FAMILIES)
        )
        assert expected == len(V.generate_family_slot_grid()) == 240

    def test_slot_id_format_locked(self, data: dict):
        data["family_slot_grid"]["slot_id_format"] = "{sleeve}-{bound}"
        _assert_rejected(data, "slot_id_format")

    def test_slot_addition_must_stay_prohibited(self, data: dict):
        data["family_slot_grid"]["slot_addition_or_removal"] = "PERMITTED"
        _assert_rejected(data, "slot_addition_or_removal")

    def test_exhaustive_over_families_required(self, data: dict):
        data["family_slot_grid"]["exhaustive_over_families"] = False
        _assert_rejected(data, "family_slot_grid.exhaustive_over_families")

    def test_claiming_exhaustiveness_over_constructions_rejected(self, data: dict):
        # The load-bearing distinction: a family is a classification of provenance, not a hypothesis.
        data["family_slot_grid"]["exhaustive_over_constructions"] = True
        _assert_rejected(data, "family_slot_grid.exhaustive_over_constructions")

    def test_wrong_slot_count_rejected(self, data: dict):
        data["family_slot_grid"]["slot_count"] = 48
        _assert_rejected(data, "family_slot_grid.slot_count")


class TestConstructionUniverseIsClosed:
    """AMENDED BY XASSET-0028. The universe is CLOSED; the XASSET-0027 record is preserved."""

    def test_closure_status_is_closed_under_the_successor(self, base_data: dict):
        block = base_data["construction_universe_closure"]
        assert block["status"] == "CLOSED"
        assert block["amended_by"] == "XASSET-0028"
        assert block["predecessor_status"] == "NOT_CLOSED"
        # Structural closure is not operational authorization.
        assert block["stage_1_executable"] is False
        assert block["stage_1_structurally_closed"] is True
        assert block["stage_1_operationally_authorized"] is False

    def test_cardinality_and_hash_match_the_real_generator(self, base_data: dict):
        import level1_construction_universe_closure_validator as CU

        universe = CU.generate_construction_universe()
        block = base_data["construction_universe_closure"]
        assert block["registered_construction_count"] == len(universe)
        assert block["construction_universe_sha256"] == CU.universe_aggregate_sha256(universe)

    def test_reverting_to_not_closed_rejected(self, data: dict):
        data["construction_universe_closure"]["status"] = "NOT_CLOSED"
        _assert_rejected(data, "construction_universe_closure.status")

    def test_wrong_registered_count_rejected(self, data: dict):
        data["construction_universe_closure"]["registered_construction_count"] = 240
        _assert_rejected(data, "registered_construction_count")

    def test_wrong_universe_hash_rejected(self, data: dict):
        data["construction_universe_closure"]["construction_universe_sha256"] = "0" * 64
        _assert_rejected(data, "construction_universe_sha256")

    def test_claiming_operational_authorization_rejected(self, data: dict):
        data["construction_universe_closure"]["stage_1_operationally_authorized"] = True
        _assert_rejected(data, "stage_1_operationally_authorized")

    def test_permitting_executor_mutation_rejected(self, data: dict):
        data["construction_universe_closure"][
            "executor_may_add_omit_substitute_or_mutate_a_construction"
        ] = True
        _assert_rejected(data, "executor_may_add_omit_substitute_or_mutate_a_construction")

    def test_dropping_the_predecessor_record_rejected(self, data: dict):
        del data["construction_universe_closure"]["xasset_0027_predecessor_record"]
        _assert_rejected(data, "xasset_0027_predecessor_record")

    def test_rewriting_predecessor_status_rejected(self, data: dict):
        data["construction_universe_closure"]["xasset_0027_predecessor_record"]["status"] = "CLOSED"
        _assert_rejected(data, "xasset_0027_predecessor_record.status")

    def test_claiming_stage_1_is_executable_rejected(self, data: dict):
        data["construction_universe_closure"]["stage_1_executable"] = True
        _assert_rejected(data, "construction_universe_closure.stage_1_executable")

    def test_both_unavailable_routes_recorded_with_reasons(self, base_data: dict):
        unavailable = base_data["construction_universe_closure"]["xasset_0027_predecessor_record"][
            "routes_considered_and_unavailable_to_this_filing"
        ]
        assert [r["route"] for r in unavailable] == [
            "CONCRETE_FINITE_REGISTRY",
            "DETERMINISTIC_CONSTRUCTION_GRAMMAR",
        ]
        for row in unavailable:
            assert row["unavailable_to_this_filing_because"].strip()

    def test_dropping_an_unavailable_route_rejected(self, data: dict):
        data["construction_universe_closure"]["xasset_0027_predecessor_record"][
            "routes_considered_and_unavailable_to_this_filing"
        ].pop()
        _assert_rejected(data, "routes_considered_and_unavailable_to_this_filing")

    def test_empty_unavailability_reason_rejected(self, data: dict):
        data["construction_universe_closure"]["xasset_0027_predecessor_record"][
            "routes_considered_and_unavailable_to_this_filing"
        ][0]["unavailable_to_this_filing_because"] = "   "
        _assert_rejected(data, "unavailable_to_this_filing_because")

    def test_next_prerequisite_is_named(self, data: dict):
        data["construction_universe_closure"]["xasset_0027_predecessor_record"][
            "next_required_prerequisite"
        ] = "TBD"
        _assert_rejected(data, "next_required_prerequisite")

    def test_invented_completeness_must_stay_prohibited(self, data: dict):
        data["construction_universe_closure"]["invented_completeness"] = "PERMITTED"
        _assert_rejected(data, "invented_completeness")


# ---------------------------------------------------------------------------
# The route unavailability is PRESENT-AUTHORITY, never a permanent foreclosure
# ---------------------------------------------------------------------------


class TestRouteUnavailabilityDoesNotForecloseTheFutureUnit:
    """XASSET-0027 records what IT cannot do; it determines nothing about the future SS-P.0 unit.

    A finite registry could in principle contain preregistered hypothetical source/construction
    architectures. This filing is not authorized to invent them, which is a statement about this
    filing's authority -- not a determination that no future authorized unit could ever close one.
    """

    def test_non_foreclosure_flag_is_recorded(self, base_data: dict):
        assert (
            base_data["construction_universe_closure"]["xasset_0027_predecessor_record"][
                "routes_are_unavailable_now_not_permanently_foreclosed"
            ]
            is True
        )

    def test_dropping_the_non_foreclosure_flag_rejected(self, data: dict):
        data["construction_universe_closure"]["xasset_0027_predecessor_record"][
            "routes_are_unavailable_now_not_permanently_foreclosed"
        ] = False
        _assert_rejected(data, "routes_are_unavailable_now_not_permanently_foreclosed")

    @pytest.mark.parametrize(
        "phrase",
        [
            "A concrete registry is closeable only for constructions built on sources that already exist.",
            "Such a registry can never be closed.",
            "A finite hypothetical registry is impossible.",
            "Route A is permanently foreclosed.",
            "No future unit may close it.",
        ],
    )
    def test_permanent_impossibility_claims_rejected(self, data: dict, phrase: str):
        data["construction_universe_closure"]["xasset_0027_predecessor_record"][
            "routes_considered_and_unavailable_to_this_filing"
        ][0]["unavailable_to_this_filing_because"] = phrase
        _assert_rejected(data, "permanent impossibility")

    def test_reverting_to_the_rejected_because_key_is_rejected(self, data: dict):
        row = data["construction_universe_closure"]["xasset_0027_predecessor_record"][
            "routes_considered_and_unavailable_to_this_filing"
        ][0]
        row["rejected_because"] = row["unavailable_to_this_filing_because"]
        _assert_rejected(data, "rejected_because")

    def test_prereg_does_not_claim_a_registry_requires_existing_sources(self, raw_text: str):
        lowered = raw_text.lower()
        assert "closeable only for constructions" not in lowered
        assert "closeable only over sources" not in lowered

    def test_prereg_states_the_present_authority_scope(self, base_data: dict):
        reason = base_data["construction_universe_closure"]["xasset_0027_predecessor_record"][
            "routes_considered_and_unavailable_to_this_filing"
        ][0]["unavailable_to_this_filing_because"]
        assert "cannot be closed by XASSET-0027 from the currently accepted corpus alone" in reason
        assert "does not determine whether that future unit" in reason

    def test_decision_does_not_claim_a_registry_requires_existing_sources(self):
        lowered = V.DECISION_PATH.read_text(encoding="utf-8").lower()
        assert "closeable only for constructions" not in lowered
        assert "closeable only over sources" not in lowered
        assert "is closeable only" not in lowered

    def test_protocol_does_not_claim_a_registry_requires_existing_sources(self):
        lowered = V.PROTOCOL_PATH.read_text(encoding="utf-8").lower()
        assert "closeable only for constructions" not in lowered
        assert "closeable only over sources" not in lowered

    def test_decision_states_it_does_not_prejudge_the_future_unit(self):
        text = V.DECISION_PATH.read_text(encoding="utf-8")
        assert "does not determine whether that future unit can" in text
        assert "finite hypothetical-architecture registry" in text

    def test_protocol_states_it_does_not_prejudge_the_future_unit(self):
        text = V.PROTOCOL_PATH.read_text(encoding="utf-8")
        assert "does not determine whether that unit can" in text
        assert "finite hypothetical-architecture registry" in text

    def test_p0_predecessor_note_preserved_verbatim(self, base_data: dict):
        pred = base_data["construction_universe_closure"]["xasset_0027_predecessor_record"]
        note = pred["next_required_prerequisite_note"]
        assert "does not pre-decide it" in note
        assert "does not choose among the possibilities that unit may consider" in note
        assert pred["authorized_by_xasset_0027"] is False
        assert pred["preserved_verbatim"] is True


class TestStage1IsNotExecutable:
    def test_stage_1_executability_block_says_not_executable(self, base_data: dict):
        block = base_data["stage_1_executability"]
        assert block["executable"] is False
        assert block["status"] == "STRUCTURALLY_CLOSED_NOT_OPERATIONALLY_AUTHORIZED"
        # AMENDED BY XASSET-0029: XASSET-0028's lifecycle has closed, so its blocker is spent and
        # is replaced by the strictly narrower external-attestation prerequisite.
        assert block["blocking_prerequisite"] == V.STAGE_1_BLOCKING_PREREQUISITE
        assert "XASSET_0037" in block["blocking_prerequisite"]
        assert "XASSET_0029" in block["predecessor_blocking_prerequisite_xasset_0029"]
        assert "EXTERNAL_ONE_SHOT_PREEXECUTION_ATTESTATION" in block["blocking_prerequisite"]
        assert block["authorized_by_xasset_0027"] is False
        assert block["authorized_by_xasset_0028"] is False
        assert block["authorized_by_xasset_0029"] is False
        # The committed boolean is permanently disqualified as an authorization source.
        assert block["executable_is_never_the_authorization_source"] is True
        assert block["construction_universe_structurally_closed"] is True
        assert block["no_merge_to_execution_gap"] is True

    def test_claiming_xasset_0028_authorizes_stage_1_rejected(self, data: dict):
        data["stage_1_executability"]["authorized_by_xasset_0028"] = True
        _assert_rejected(data, "stage_1_executability.authorized_by_xasset_0028")

    def test_dropping_an_operational_authorization_gate_rejected(self, data: dict):
        data["stage_1_executability"]["operational_authorization_requires_all_of"] = ["MERGE"]
        _assert_rejected(data, "operational_authorization_requires_all_of")

    def test_claiming_stage_1_executable_rejected(self, data: dict):
        data["stage_1_executability"]["executable"] = True
        _assert_rejected(data, "stage_1_executability.executable")

    def test_claiming_xasset_0027_authorizes_stage_1_rejected(self, data: dict):
        data["stage_1_executability"]["authorized_by_xasset_0027"] = True
        _assert_rejected(data, "stage_1_executability.authorized_by_xasset_0027")

    def test_stages_block_agrees_stage_1_is_unauthorized(self, base_data: dict):
        assert base_data["stages"]["stage_1"]["authorized_by_xasset_0027"] is False

    def test_stages_block_claiming_authorization_rejected(self, data: dict):
        data["stages"]["stage_1"]["authorized_by_xasset_0027"] = True
        _assert_rejected(data, "stages.stage_1.authorized_by_xasset_0027")

    def test_lifecycle_precondition_includes_construction_universe_closure(self, base_data: dict):
        # Lifecycle closure alone must not be stated as sufficient for Stage 1.
        assert (
            base_data["lifecycle_effectivity"]["stage_1_execution_may_begin_only_after"]
            == V.STAGE_1_EXECUTION_PRECONDITION
        )
        # AMENDED BY XASSET-0028. Construction-universe closure is no longer a *pending* condition:
        # XASSET-0028 supplies it, so the operative precondition is the six-gate successor lifecycle,
        # which is strictly stronger than the spent predecessor string it replaces.
        # FURTHER AMENDED BY XASSET-0029: the XASSET-0028 lifecycle is itself spent, so the
        # operative precondition is the XASSET-0029 lifecycle plus an external attestation.
        assert "XASSET_0037_LIFECYCLE_CLOSURE_ALL_SIX_GATES" in V.STAGE_1_EXECUTION_PRECONDITION
        assert (
            "XASSET_0029_LIFECYCLE_CLOSURE_ALL_SIX_GATES"
            in V.PREDECESSOR_STAGE_1_EXECUTION_PRECONDITION_XASSET_0029
        )
        assert (
            "EXTERNAL_ONE_SHOT_PREEXECUTION_ATTESTATION" in V.STAGE_1_EXECUTION_PRECONDITION
        )
        assert "CONSTRUCTION_UNIVERSE_CLOSURE" in V.PREDECESSOR_STAGE_1_EXECUTION_PRECONDITION
        assert (
            "XASSET_0028_LIFECYCLE_CLOSURE_ALL_SIX_GATES"
            in V.PREDECESSOR_STAGE_1_EXECUTION_PRECONDITION_XASSET_0028
        )

    def test_reverting_to_lifecycle_only_precondition_rejected(self, data: dict):
        data["lifecycle_effectivity"]["stage_1_execution_may_begin_only_after"] = (
            "XASSET_0027_LIFECYCLE_CLOSURE_AND_MERGED_HASH_VERIFICATION"
        )
        _assert_rejected(data, "stage_1_execution_may_begin_only_after")


class TestCompletenessRule:
    def test_completeness_rule_present(self, base_data: dict):
        rule = base_data["completeness_rule"]
        assert rule["applies_only_after_construction_universe_closure"] is True
        assert rule["cell_negative_requires_all_registered_constructions_evaluated"] is True
        assert rule["family_slot_negative_does_not_establish_non_constructibility"] is True
        assert rule["unevaluated_construction_permitted"] is False
        assert rule["partial_cell_outcome_permitted"] is False

    def test_permitting_unevaluated_constructions_rejected(self, data: dict):
        data["completeness_rule"]["unevaluated_construction_permitted"] = True
        _assert_rejected(data, "unevaluated_construction_permitted")

    def test_permitting_partial_cells_rejected(self, data: dict):
        data["completeness_rule"]["partial_cell_outcome_permitted"] = True
        _assert_rejected(data, "partial_cell_outcome_permitted")

    def test_dropping_the_negative_exhaustiveness_requirement_rejected(self, data: dict):
        data["completeness_rule"]["cell_negative_requires_all_registered_constructions_evaluated"] = False
        _assert_rejected(data, "cell_negative_requires_all_registered_constructions_evaluated")

    def test_claiming_a_family_slot_negative_is_exhaustive_rejected(self, data: dict):
        data["completeness_rule"]["family_slot_negative_does_not_establish_non_constructibility"] = False
        _assert_rejected(data, "family_slot_negative_does_not_establish_non_constructibility")


class TestTrialInventoryIsDefined:
    def test_trial_inventory_status_is_defined(self, base_data: dict):
        inventory = base_data["trial_inventory"]
        assert inventory["status"] == "DEFINED"
        assert inventory["unit_of_trial_once_defined"] == "ONE_CONSTRUCTION_EVALUATION"
        assert inventory["unit_of_trial"] == "ONE_CONSTRUCTION_EVALUATION"
        assert inventory["defined_by"] == "XASSET-0028"
        assert inventory["predecessor_status_xasset_0027"] == "NOT_YET_DEFINABLE"

    def test_registered_constructions_match_the_generator(self, base_data: dict):
        import level1_construction_universe_closure_validator as CU

        assert base_data["trial_inventory"]["registered_constructions"] == len(
            CU.generate_construction_universe()
        )

    def test_wrong_registered_construction_count_rejected(self, data: dict):
        data["trial_inventory"]["registered_constructions"] = 240
        _assert_rejected(data, "trial_inventory.registered_constructions")

    def test_family_slot_arithmetic_still_recorded(self, base_data: dict):
        assert base_data["trial_inventory"]["derived_family_slots"] == 240
        assert base_data["trial_inventory"]["family_slots_per_cell"] == 5

    def test_reverting_to_not_yet_definable_rejected(self, data: dict):
        data["trial_inventory"]["status"] = "NOT_YET_DEFINABLE"
        _assert_rejected(data, "trial_inventory.status")

    @pytest.mark.parametrize(
        "banned_key",
        ("derived_candidate_ceiling", "candidates_per_cell"),
    )
    def test_smuggling_back_an_old_ceiling_key_rejected(self, data: dict, banned_key: str):
        data["trial_inventory"][banned_key] = 240
        _assert_rejected(data, f"trial_inventory.{banned_key}")

    def test_wrong_family_slot_count_rejected(self, data: dict):
        data["trial_inventory"]["derived_family_slots"] = 48
        _assert_rejected(data, "derived_family_slots")

    def test_derived_identity_mismatch_rejected(self, data: dict):
        for row in data["consequential_parameter_registry"]["derived_identities"]["identities"]:
            if row["identity_id"] == "FAMILY_SLOT_COUNT":
                row["value"] = 480
        _assert_rejected(data, "FAMILY_SLOT_COUNT")

    def test_derived_identity_may_not_be_a_num_0001_class(self, data: dict):
        rows = data["consequential_parameter_registry"]["derived_identities"]["identities"]
        rows[0]["contextual_class"] = "EMPIRICALLY_CALIBRATED"
        _assert_rejected(data, "CALCULATED_OUTPUT")

    def test_missing_derived_identity_rejected(self, data: dict):
        rows = data["consequential_parameter_registry"]["derived_identities"]["identities"]
        data["consequential_parameter_registry"]["derived_identities"]["identities"] = [
            r for r in rows if r["identity_id"] != "CONSTRUCTION_FAMILY_COUNT"
        ]
        _assert_rejected(data, "CONSTRUCTION_FAMILY_COUNT")


# ---------------------------------------------------------------------------
# Stage-1 results enforcement — fails closed, and enforces a closed universe
# ---------------------------------------------------------------------------


def _validate(results, universe=None):
    """Validate a synthetic results document against a SYNTHETIC construction universe.

    Uses the PRIVATE structural seam. The public validate_stage1_results() takes no universe
    argument and always enforces operational authorization; see TestStage1ResultsFailsClosed.
    """
    return V._validate_stage1_results_against_universe(results, universe or _synthetic_universe())


class TestStage1ResultsFailsClosed:
    def test_the_real_closed_construction_universe_is_now_the_frozen_680(self):
        """AMENDED BY XASSET-0028. Emptiness is no longer what fails closed; lifecycle is."""
        universe = V.closed_construction_universe()
        assert len(universe) == 680
        for record in universe.values():
            assert record["source_architecture"] == "HYPOTHETICAL_SOURCE_ARCHITECTURE"
            assert record["hypothetical_source_requirements"].strip()

    def test_a_real_call_is_rejected_because_stage_1_is_not_authorized(self):
        r = V.validate_stage1_results(_full_results())
        assert not r.ok
        assert any("not operationally authorized" in e for e in r.errors)

    def test_structural_closure_alone_does_not_authorize_execution(self):
        authorized, reason = V.stage_1_operational_authorization_is_effective()
        assert authorized is False
        # AMENDED BY XASSET-0029: the current authority is named, and the reason must state that
        # an external attestation -- not merely a closed lifecycle -- is still required.
        assert "XASSET-0029" in reason
        assert "attestation" in reason
        assert "no merge-to-execution gap" in reason
        for gate in V.STAGE_1_EFFECTIVITY_GATES:
            assert gate in reason

    def test_an_explicitly_empty_universe_is_rejected(self):
        r = V._validate_stage1_results_against_universe(_full_results(), {})
        assert not r.ok
        assert any("no closed construction universe exists" in e for e in r.errors)

    def test_the_family_slot_grid_is_not_itself_a_construction_universe(self):
        """The public path refuses; only the private structural seam takes a supplied universe."""
        assert V.validate_stage1_results(_full_results()).ok is False
        assert _validate(_full_results()).ok is True


class TestStage1ResultsEnforcement:
    def test_complete_conforming_results_accepted(self):
        assert _validate(_full_results()).ok

    def test_unregistered_construction_rejected(self):
        results = _full_results()
        results["candidate_results"].append(
            _candidate_row("equity::LOWER::portfolio_function::R1_C1")
            | {"construction_id": "equity::LOWER::portfolio_function::R9_C9"}
        )
        r = _validate(results)
        assert not r.ok and any("not in the frozen construction universe" in e for e in r.errors)

    def test_missing_registered_construction_rejected(self):
        results = _full_results()
        results["candidate_results"].pop()
        r = _validate(results)
        assert not r.ok and any("no recorded disposition" in e for e in r.errors)

    def test_duplicate_construction_rejected(self):
        results = _full_results()
        results["candidate_results"].append(copy.deepcopy(results["candidate_results"][0]))
        r = _validate(results)
        assert not r.ok and any("duplicated" in e for e in r.errors)

    def test_non_exhaustive_negative_cell_rejected(self):
        """A cell may not be recorded negative when its registered set is incomplete."""
        results = _full_results()
        target = results["cell_results"][0]["cell_id"]
        results["candidate_results"] = [
            r for r in results["candidate_results"] if r["cell_id"] != target
        ] + [r for r in results["candidate_results"] if r["cell_id"] == target][:2]
        results["cell_results"][0]["outcome"] = "BLOCKED_CATEGORICALLY"
        r = _validate(results)
        assert not r.ok
        assert any("no recorded disposition" in e or "registered dispositions" in e for e in r.errors)

    def test_outcome_aware_candidate_removal_rejected(self):
        """Dropping the one candidate that survived, to make a cell look negative, is caught."""
        def gates_for(cid):
            g = _passing_gates()
            if not cid.endswith("R1_C4"):
                g["G4_ORIGIN"] = "FAIL"
            return g

        results = _full_results(gates_for)
        survivor = next(
            r for r in results["candidate_results"]
            if r["disposition"] == "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"
        )
        results["candidate_results"] = [
            r for r in results["candidate_results"] if r["construction_id"] != survivor["construction_id"]
        ]
        for cell in results["cell_results"]:
            if cell["cell_id"] == survivor["cell_id"]:
                cell["outcome"] = "BLOCKED_CATEGORICALLY"
        r = _validate(results)
        assert not r.ok

    def test_cell_outcome_must_equal_the_deterministic_derivation(self):
        results = _full_results()
        results["cell_results"][0]["outcome"] = "BLOCKED_CATEGORICALLY"
        r = _validate(results)
        assert not r.ok and any("deterministically derive" in e for e in r.errors)

    def test_disposition_must_equal_the_derivation_from_its_own_gates(self):
        results = _full_results()
        results["candidate_results"][0]["disposition"] = "BLOCKED_CATEGORICALLY"
        r = _validate(results)
        assert not r.ok and any("deterministically derive" in e for e in r.errors)

    def test_missing_governing_authority_refs_rejected(self):
        results = _full_results()
        results["candidate_results"][0]["governing_authority_refs"] = []
        r = _validate(results)
        assert not r.ok and any("governing_authority_refs" in e for e in r.errors)

    def test_missing_required_candidate_key_rejected(self):
        results = _full_results()
        del results["candidate_results"][0]["point_or_range_support"]
        r = _validate(results)
        assert not r.ok and any("point_or_range_support" in e for e in r.errors)

    def test_candidate_order_cannot_affect_the_result(self):
        results = _full_results()
        shuffled = copy.deepcopy(results)
        random.Random(20260816).shuffle(shuffled["candidate_results"])
        random.Random(99).shuffle(shuffled["cell_results"])
        assert _validate(results).ok
        assert _validate(shuffled).ok

    def test_full_j_compliance_claim_rejected(self):
        results = _full_results()
        results["disposition"] = "J_1_THROUGH_J_12_SATISFIED"
        r = _validate(results)
        assert not r.ok and any("may not be claimed" in e for e in r.errors)

    def test_exhaustive_non_constructibility_claim_rejected(self):
        results = _full_results()
        results["disposition"] = "EXHAUSTIVE_NON_CONSTRUCTIBILITY"
        r = _validate(results)
        assert not r.ok and any("may not be claimed" in e for e in r.errors)

    def test_incomplete_gate_coverage_rejected(self):
        results = _full_results()
        gates = dict(_passing_gates())
        del gates["G7_DISCRETION_AND_PROVENANCE"]
        results["candidate_results"][0]["gate_results"] = gates
        r = _validate(results)
        assert not r.ok and any("every gate must be evaluated" in e for e in r.errors)

    def test_non_mapping_results_rejected(self):
        assert not V._validate_stage1_results_against_universe([], _synthetic_universe()).ok


# ---------------------------------------------------------------------------
# Frozen provenance — exact source identity, verified against observed bytes
# ---------------------------------------------------------------------------

# A real, stable, committed file this PR does not touch. Its digest is computed at test time from
# the file's own bytes, so this test file hardcodes no digest and cannot drift.
_REAL_SOURCE_PATH = "governance/decisions/README.md"


def _existing_source_universe():
    """A synthetic universe whose first construction has a FROZEN existing-source identity."""
    universe = dict(_synthetic_universe())
    first = V.generate_family_slot_grid()[0]
    universe[first] = {
        "cell_id": V.cell_id_of(first),
        "source_architecture": "EXISTING_SOURCE_ARCHITECTURE",
        "source_path": _REAL_SOURCE_PATH,
        "source_sha256": V.sha256_file(ROOT / _REAL_SOURCE_PATH),
        "hypothetical_source_requirements": None,
    }
    return universe


def _existing_source_results(**overrides):
    results = _full_results()
    first = V.generate_family_slot_grid()[0]
    row = next(r for r in results["candidate_results"] if r["construction_id"] == first)
    row.update(
        {
            "source_architecture": "EXISTING_SOURCE_ARCHITECTURE",
            "source_path": _REAL_SOURCE_PATH,
            "source_sha256": V.sha256_file(ROOT / _REAL_SOURCE_PATH),
            "hypothetical_source_requirements": None,
        }
    )
    row.update(overrides)
    return results


class TestFrozenProvenance:
    def test_existing_source_matching_the_frozen_identity_and_bytes_accepted(self):
        r = V._validate_stage1_results_against_universe(_existing_source_results(), _existing_source_universe())
        assert r.ok, r.errors

    def test_existing_source_requires_exact_path_and_hash(self):
        results = _existing_source_results(source_path=None, source_sha256=None)
        r = V._validate_stage1_results_against_universe(results, _existing_source_universe())
        assert not r.ok and any("source_path" in e for e in r.errors)
        assert any("source_sha256" in e for e in r.errors)

    def test_existing_source_rejects_a_malformed_digest(self):
        results = _existing_source_results(source_sha256="not-a-digest")
        r = V._validate_stage1_results_against_universe(results, _existing_source_universe())
        assert not r.ok and any("source_sha256" in e for e in r.errors)

    def test_syntactically_valid_but_arbitrary_digest_rejected(self):
        """Shape validation is not identity validation: a well-formed digest must still match."""
        results = _existing_source_results(source_sha256="a" * 64)
        r = V._validate_stage1_results_against_universe(results, _existing_source_universe())
        assert not r.ok
        assert any("does not match the frozen construction identity" in e for e in r.errors)

    def test_a_path_the_result_author_chose_is_rejected(self):
        """The path must be the FROZEN one, not one selected at results time."""
        results = _existing_source_results(source_path="constitution/INVESTMENT_CONSTITUTION.md")
        r = V._validate_stage1_results_against_universe(results, _existing_source_universe())
        assert not r.ok
        assert any("the frozen construction identity names" in e for e in r.errors)

    def test_digest_that_does_not_match_the_observed_bytes_rejected(self):
        """Both the frozen record and the result agree, but neither matches the file on disk."""
        universe = _existing_source_universe()
        first = V.generate_family_slot_grid()[0]
        wrong = "b" * 64
        universe[first] = dict(universe[first]) | {"source_sha256": wrong}
        results = _existing_source_results(source_sha256=wrong)
        r = V._validate_stage1_results_against_universe(results, universe)
        assert not r.ok
        assert any("does not match the observed bytes" in e for e in r.errors)

    def test_nonexistent_frozen_source_rejected(self):
        universe = _existing_source_universe()
        first = V.generate_family_slot_grid()[0]
        universe[first] = dict(universe[first]) | {"source_path": "governance/does_not_exist.md"}
        results = _existing_source_results(source_path="governance/does_not_exist.md")
        r = V._validate_stage1_results_against_universe(results, universe)
        assert not r.ok and any("does not exist" in e for e in r.errors)

    def test_path_escaping_the_repository_rejected(self):
        universe = _existing_source_universe()
        first = V.generate_family_slot_grid()[0]
        escape = "../outside.md"
        universe[first] = dict(universe[first]) | {"source_path": escape}
        results = _existing_source_results(source_path=escape)
        r = V._validate_stage1_results_against_universe(results, universe)
        assert not r.ok and any("outside the repository" in e for e in r.errors)

    def test_architecture_may_not_depart_from_the_frozen_identity(self):
        results = _full_results()
        results["candidate_results"][0]["source_architecture"] = "EXISTING_SOURCE_ARCHITECTURE"
        r = _validate(results)
        assert not r.ok
        assert any("may not alter a frozen architecture" in e for e in r.errors)

    def test_hypothetical_source_must_not_carry_a_path_or_hash(self):
        results = _full_results()
        results["candidate_results"][0]["source_path"] = _REAL_SOURCE_PATH
        r = _validate(results)
        assert not r.ok and any("must carry no source_path" in e for e in r.errors)

    def test_hypothetical_source_requires_a_requirements_statement(self):
        results = _full_results()
        results["candidate_results"][0]["hypothetical_source_requirements"] = "  "
        r = _validate(results)
        assert not r.ok and any("hypothetical_source_requirements" in e for e in r.errors)

    def test_results_time_authored_requirements_rejected(self):
        """A non-empty string authored in the results document is not a preregistration."""
        results = _full_results()
        results["candidate_results"][0]["hypothetical_source_requirements"] = (
            "something the result author made up at write time"
        )
        r = _validate(results)
        assert not r.ok
        assert any("does not match the frozen construction identity" in e for e in r.errors)

    def test_preregistration_records_the_frozen_provenance_requirements(self, base_data: dict):
        frozen = base_data["frozen_provenance_requirements"]
        assert frozen["binding_on_any_future_stage_1"] is True
        assert frozen["existing_source_architecture"]["observed_bytes_must_be_verified_against_the_frozen_hash"] is True
        assert frozen["existing_source_architecture"]["syntactic_validation_is_insufficient"] is True
        assert (
            frozen["hypothetical_source_architecture"]["executor_authored_free_text_at_results_time"]
            == "PROHIBITED"
        )
        assert frozen["result_author_may_alter_a_frozen_architecture"] is False
        assert frozen["structurally_satisfied"] is True
        assert frozen["operationally_usable"] is False

    def test_claiming_frozen_provenance_is_operationally_usable_rejected(self, data: dict):
        data["frozen_provenance_requirements"]["operationally_usable"] = True
        _assert_rejected(data, "frozen_provenance_requirements.operationally_usable")

    def test_permitting_results_time_free_text_rejected(self, data: dict):
        data["frozen_provenance_requirements"]["hypothetical_source_architecture"][
            "executor_authored_free_text_at_results_time"
        ] = "PERMITTED"
        _assert_rejected(data, "executor_authored_free_text_at_results_time")

    def test_dropping_observed_bytes_verification_rejected(self, data: dict):
        data["frozen_provenance_requirements"]["existing_source_architecture"][
            "observed_bytes_must_be_verified_against_the_frozen_hash"
        ] = False
        _assert_rejected(data, "observed_bytes_must_be_verified_against_the_frozen_hash")


# ---------------------------------------------------------------------------
# MAJOR 2 — gates, compound failures, order independence
# ---------------------------------------------------------------------------


class TestGateSequence:
    def test_twelve_gates(self, base_data: dict):
        assert len(base_data["gate_sequence"]["gates"]) == 12

    def test_reconciliation_gate_removed(self, base_data: dict):
        ids = [g["gate_id"] for g in base_data["gate_sequence"]["gates"]]
        assert "G12_RECONCILIATION_FEASIBILITY" not in ids
        assert "G12_SNAPSHOT_ADMISSIBILITY_PATH" in ids

    def test_reintroducing_the_reconciliation_gate_rejected(self, data: dict):
        data["gate_sequence"]["gates"][11]["gate_id"] = "G12_RECONCILIATION_FEASIBILITY"
        _assert_rejected(data, "must not appear")

    def test_first_failure_wins_must_be_disabled(self, base_data: dict):
        assert base_data["gate_sequence"]["record_first_failing_gate_only"] is False
        assert base_data["gate_sequence"]["first_failing_gate_is_diagnostic_only"] is True

    def test_reenabling_first_failure_wins_rejected(self, data: dict):
        data["gate_sequence"]["record_first_failing_gate_only"] = True
        _assert_rejected(data, "record_first_failing_gate_only")

    def test_evaluate_all_gates_requirement_locked(self, data: dict):
        data["gate_sequence"]["evaluation_requirement"] = "STOP_AT_FIRST_FAILURE"
        _assert_rejected(data, "evaluation_requirement")

    def test_gate_removed_rejected(self, data: dict):
        data["gate_sequence"]["gates"].pop()
        _assert_rejected(data, "expected 12 gates")

    def test_gate_reorder_rejected(self, data: dict):
        gates = data["gate_sequence"]["gates"]
        gates[0], gates[1] = gates[1], gates[0]
        _assert_rejected(data, "gate_id")

    def test_gate_index_gap_rejected(self, data: dict):
        data["gate_sequence"]["gates"][4]["gate_index"] = 99
        _assert_rejected(data, "gate_index")

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


class TestCompoundFailureClassification:
    """The review's core MAJOR 2 scenario: a prerequisite gate must never mask a categorical one."""

    def test_g9_plus_g10_is_categorical(self):
        gates = _passing_gates()
        gates["G9_REPRESENTATION"] = "FAIL"
        gates["G10_PAIR_INDEPENDENCE"] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "BLOCKED_CATEGORICALLY"

    def test_g9_plus_g11_is_categorical(self):
        gates = _passing_gates()
        gates["G9_REPRESENTATION"] = "FAIL"
        gates["G11_EXACTNESS_AND_DETERMINISM"] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "BLOCKED_CATEGORICALLY"

    @pytest.mark.parametrize("categorical_gate", V.CATEGORICAL_GATES)
    def test_g9_plus_any_categorical_is_categorical(self, categorical_gate: str):
        gates = _passing_gates()
        gates["G9_REPRESENTATION"] = "FAIL"
        gates[categorical_gate] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "BLOCKED_CATEGORICALLY"

    @pytest.mark.parametrize("prerequisite_gate", V.PREREQUISITE_GATES)
    def test_prerequisite_only_failure_is_prerequisite(self, prerequisite_gate: str):
        gates = _passing_gates()
        gates[prerequisite_gate] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"

    def test_both_prerequisite_gates_only_is_still_prerequisite(self):
        gates = _passing_gates()
        for gate in V.PREREQUISITE_GATES:
            gates[gate] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"

    @pytest.mark.parametrize("categorical_gate", V.CATEGORICAL_GATES)
    def test_categorical_only_failure_is_categorical(self, categorical_gate: str):
        gates = _passing_gates()
        gates[categorical_gate] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "BLOCKED_CATEGORICALLY"

    def test_all_pass_is_constructible(self):
        assert V.derive_candidate_disposition(_passing_gates()) == "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"

    def test_unable_to_determine_without_failures(self):
        gates = _passing_gates()
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
        assert V.derive_candidate_disposition(gates) == "UNABLE_TO_DETERMINE"

    def test_categorical_failure_dominates_unable_to_determine(self):
        gates = _passing_gates()
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
        gates["G4_ORIGIN"] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "BLOCKED_CATEGORICALLY"

    def test_gate_order_cannot_alter_the_disposition(self):
        """Permuting the gate mapping's insertion order must not change the outcome."""
        gates = _passing_gates()
        gates["G9_REPRESENTATION"] = "FAIL"
        gates["G10_PAIR_INDEPENDENCE"] = "FAIL"
        baseline = V.derive_candidate_disposition(gates)
        rng = random.Random(4945187522)
        for _ in range(25):
            items = list(gates.items())
            rng.shuffle(items)
            assert V.derive_candidate_disposition(dict(items)) == baseline

    def test_unknown_gate_rejected(self):
        gates = _passing_gates()
        gates["G99_INVENTED"] = "PASS"
        with pytest.raises(ValueError, match="unknown gate"):
            V.derive_candidate_disposition(gates)

    def test_invalid_gate_result_rejected(self):
        gates = _passing_gates()
        gates["G1_DRIVER_SUBJECT_MATTER"] = "MOSTLY_FINE"
        with pytest.raises(ValueError, match="gate results must be in"):
            V.derive_candidate_disposition(gates)


class TestDispositionRulesDeclared:
    def test_order_independence_declared(self, base_data: dict):
        assert base_data["disposition_rules"]["order_independent"] is True

    def test_categorical_dominance_declared(self, base_data: dict):
        assert (
            base_data["disposition_rules"]["candidate_disposition"]["categorical_dominates_prerequisite"]
            is True
        )

    def test_removing_categorical_dominance_rejected(self, data: dict):
        data["disposition_rules"]["candidate_disposition"]["categorical_dominates_prerequisite"] = False
        _assert_rejected(data, "categorical_dominates_prerequisite")

    def test_candidate_precedence_order_locked(self, data: dict):
        rules = data["disposition_rules"]["candidate_disposition"]["precedence"]
        rules[0], rules[1] = rules[1], rules[0]
        _assert_rejected(data, "candidate_disposition.precedence")

    def test_cell_precedence_order_locked(self, data: dict):
        rules = data["disposition_rules"]["cell_outcome"]["precedence"]
        rules[0], rules[1] = rules[1], rules[0]
        _assert_rejected(data, "cell_outcome.precedence")

    def test_roll_up_precedence_order_locked(self, data: dict):
        rules = data["disposition_rules"]["roll_up_outcome"]["precedence"]
        rules[0], rules[1] = rules[1], rules[0]
        _assert_rejected(data, "roll_up_outcome.precedence")

    def test_declared_precedence_matches_the_executable_functions(self, base_data: dict):
        assert [r["outcome"] for r in base_data["disposition_rules"]["candidate_disposition"]["precedence"]] == [
            o for _c, o in V.CANDIDATE_PRECEDENCE
        ]
        assert [r["outcome"] for r in base_data["disposition_rules"]["cell_outcome"]["precedence"]] == [
            o for _c, o in V.CELL_PRECEDENCE
        ]
        assert [r["outcome"] for r in base_data["disposition_rules"]["roll_up_outcome"]["precedence"]] == [
            o for _c, o in V.ROLL_UP_PRECEDENCE
        ]


class TestCellAndRollUpDerivation:
    def test_cell_is_existential_over_candidates(self):
        assert V.derive_cell_outcome(
            ["BLOCKED_CATEGORICALLY"] * 4 + ["CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"]
        ) == "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"

    def test_cell_negative_requires_all_categorical(self):
        assert V.derive_cell_outcome(["BLOCKED_CATEGORICALLY"] * 5) == "BLOCKED_CATEGORICALLY"

    def test_cell_prerequisite_beats_categorical(self):
        assert V.derive_cell_outcome(
            ["BLOCKED_CATEGORICALLY"] * 4 + ["BLOCKED_PENDING_SEPARATE_PREREQUISITE"]
        ) == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"

    def test_cell_order_independent(self):
        values = [
            "BLOCKED_CATEGORICALLY",
            "UNABLE_TO_DETERMINE",
            "BLOCKED_PENDING_SEPARATE_PREREQUISITE",
            "BLOCKED_CATEGORICALLY",
            "BLOCKED_CATEGORICALLY",
        ]
        outcomes = {V.derive_cell_outcome(list(p)) for p in itertools.permutations(values)}
        assert outcomes == {"BLOCKED_PENDING_SEPARATE_PREREQUISITE"}

    def test_roll_up_order_independent(self):
        values = ["BLOCKED_CATEGORICALLY", "UNABLE_TO_DETERMINE", "BLOCKED_CATEGORICALLY"]
        outcomes = {V.derive_roll_up_outcome(list(p)) for p in itertools.permutations(values)}
        assert outcomes == {"UNABLE_TO_DETERMINE"}

    def test_roll_up_negative_requires_all_categorical(self):
        assert V.derive_roll_up_outcome(["BLOCKED_CATEGORICALLY"] * 6) == "NO_CONSTRUCTIBLE_CANDIDATE"

    def test_roll_up_positive(self):
        assert V.derive_roll_up_outcome(
            ["BLOCKED_CATEGORICALLY"] * 5 + ["CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"]
        ) == "CANDIDATE_CONSTRUCTION_IDENTIFIED"

    def test_empty_inputs_rejected(self):
        with pytest.raises(ValueError):
            V.derive_cell_outcome([])
        with pytest.raises(ValueError):
            V.derive_roll_up_outcome([])

    def test_invalid_values_rejected(self):
        with pytest.raises(ValueError):
            V.derive_cell_outcome(["MOSTLY_OK"])
        with pytest.raises(ValueError):
            V.derive_roll_up_outcome(["MOSTLY_OK"])


# ---------------------------------------------------------------------------
# MAJOR 2 — the XASSET-0024 SS-K.1 reading map
# ---------------------------------------------------------------------------


class TestOpenReadingMapping:
    def test_open_reading_is_not_resolved(self, base_data: dict):
        handling = base_data["open_reading_handling"]
        assert handling["resolved_by_this_program"] is False
        assert handling["relied_upon_by_this_program"] is False

    def test_resolving_the_reading_rejected(self, data: dict):
        data["open_reading_handling"]["resolved_by_this_program"] = True
        _assert_rejected(data, "resolved_by_this_program")

    def test_single_reading_evaluation_rejected(self, data: dict):
        data["open_reading_handling"]["handling"] = "ASSUME_SUBJECT_MATTER_READING"
        _assert_rejected(data, "handling")

    def test_per_reading_vocabulary_closed(self, base_data: dict):
        assert base_data["open_reading_handling"]["per_reading_vocabulary"] == list(V.READING_VOCABULARY)

    def test_reading_vocabulary_change_rejected(self, data: dict):
        data["open_reading_handling"]["per_reading_vocabulary"] = ["YES", "NO"]
        _assert_rejected(data, "per_reading_vocabulary")

    def test_reading_dependent_maps_to_unable_to_determine(self):
        assert V.map_g2_reading("PASSES", "FAILS") == "UNABLE_TO_DETERMINE"
        assert V.is_reading_dependent("PASSES", "FAILS") is True

    def test_reading_dependent_is_not_categorical(self):
        """The load-bearing correction: an unresolved reading is not a categorical impossibility."""
        assert V.map_g2_reading("PASSES", "FAILS") != "FAILS_CATEGORICALLY"

    def test_both_readings_fail_is_categorical(self):
        assert V.map_g2_reading("FAILS", "FAILS") == "FAILS_CATEGORICALLY"
        assert V.is_reading_dependent("FAILS", "FAILS") is False

    def test_both_readings_pass(self):
        assert V.map_g2_reading("PASSES", "PASSES") == "PASSES"

    def test_incoherent_combination_rejected(self):
        assert V.map_g2_reading("FAILS", "PASSES") == "INCOHERENT_REJECTED"

    @pytest.mark.parametrize(
        "sm,po",
        [("UNABLE_TO_DETERMINE", "PASSES"), ("PASSES", "UNABLE_TO_DETERMINE"),
         ("UNABLE_TO_DETERMINE", "UNABLE_TO_DETERMINE"), ("UNABLE_TO_DETERMINE", "FAILS")],
    )
    def test_uncertain_reading_maps_to_unable_to_determine(self, sm: str, po: str):
        assert V.map_g2_reading(sm, po) == "UNABLE_TO_DETERMINE"

    def test_invalid_reading_value_rejected(self):
        with pytest.raises(ValueError):
            V.map_g2_reading("MAYBE", "PASSES")

    def test_declared_table_locked(self, data: dict):
        data["g2_reading_mapping"]["rows"][2]["g2_effective_outcome"] = "FAILS_CATEGORICALLY"
        _assert_rejected(data, "g2_effective_outcome")

    def test_reading_dependent_target_outcome_locked(self, data: dict):
        data["g2_reading_mapping"]["reading_dependent_maps_to_candidate_outcome"] = "BLOCKED_CATEGORICALLY"
        _assert_rejected(data, "reading_dependent_maps_to_candidate_outcome")

    # CORRECTED UNDER XASSET-0036 SS-E.2. This test previously asserted that ANY
    # BLOCKED_CATEGORICALLY disposition was rejected while G2 was reading-dependent -- including
    # this case, where G4_ORIGIN independently FAILS. That pinned the XASSET-0030 SS-C
    # enforcement-conformance defect: XASSET-0027 SS-M.1 and both canonical artifacts admit exactly
    # that disposition "unless a categorical gate independently fails". The corrected pair below
    # pins BOTH directions, so neither the overreach nor its opposite can return silently.
    def test_results_accept_categorical_when_another_gate_independently_fails(self):
        """An independent categorical failure lawfully derives BLOCKED_CATEGORICALLY."""
        results = _full_results()
        row = results["candidate_results"][0]
        gates = _passing_gates()
        gates["G4_ORIGIN"] = "FAIL"
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
        row.update(
            {
                "gate_results": gates,
                "categorical_failures": ["G4_ORIGIN"],
                "disposition": "BLOCKED_CATEGORICALLY",
                "first_failing_gate_id": "G4_ORIGIN",
                "g2_outcome_under_subject_matter_reading": "PASSES",
                "g2_outcome_under_preference_only_reading": "FAILS",
                "g2_outcome_is_reading_dependent": True,
            }
        )
        # The cell this row belongs to must reflect its own candidates' dispositions.
        for cell in results["cell_results"]:
            if cell["cell_id"] == row["cell_id"]:
                cell["outcome"] = V.derive_cell_outcome(
                    [
                        candidate["disposition"]
                        for candidate in results["candidate_results"]
                        if candidate["cell_id"] == cell["cell_id"]
                    ]
                )
        r = _validate(results)
        assert r.ok, r.errors

    def test_results_reject_categorical_from_reading_dependence_alone(self):
        """Reading dependence alone is uncertainty, never a categorical bar."""
        results = _full_results()
        row = results["candidate_results"][0]
        gates = _passing_gates()
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
        row.update(
            {
                "gate_results": gates,
                "disposition": "BLOCKED_CATEGORICALLY",
                "g2_outcome_under_subject_matter_reading": "PASSES",
                "g2_outcome_under_preference_only_reading": "FAILS",
                "g2_outcome_is_reading_dependent": True,
            }
        )
        r = _validate(results)
        assert not r.ok
        assert any("reading-dependent" in e for e in r.errors)

    def test_results_reject_inconsistent_dependence_flag(self):
        results = _full_results()
        results["candidate_results"][0]["g2_outcome_is_reading_dependent"] = True
        r = _validate(results)
        assert not r.ok and any("g2_outcome_is_reading_dependent" in e for e in r.errors)

    def test_results_reject_incoherent_reading_pair(self):
        results = _full_results()
        results["candidate_results"][0].update(
            {
                "g2_outcome_under_subject_matter_reading": "FAILS",
                "g2_outcome_under_preference_only_reading": "PASSES",
            }
        )
        r = _validate(results)
        assert not r.ok and any("incoherent" in e for e in r.errors)


# ---------------------------------------------------------------------------
# The reading map GOVERNS the recorded G2 gate result rather than annotating it
# ---------------------------------------------------------------------------


def _reading_dependent_row(**gate_overrides):
    """A results document whose first candidate carries the reading-dependent SS-K.1 pair."""
    results = _full_results()
    row = results["candidate_results"][0]
    gates = _passing_gates()
    gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
    gates.update(gate_overrides)
    row.update(
        {
            "gate_results": gates,
            "disposition": V.derive_candidate_disposition(gates),
            "categorical_failures": [g for g in V.CATEGORICAL_GATES if gates.get(g) == "FAIL"],
            "prerequisite_failures": [g for g in V.PREREQUISITE_GATES if gates.get(g) == "FAIL"],
            "g2_outcome_under_subject_matter_reading": "PASSES",
            "g2_outcome_under_preference_only_reading": "FAILS",
            "g2_outcome_is_reading_dependent": True,
        }
    )
    # Recompute the owning cell so the document stays internally consistent.
    by_cell: dict[str, list[str]] = {}
    for r in results["candidate_results"]:
        by_cell.setdefault(r["cell_id"], []).append(r["disposition"])
    results["cell_results"] = [
        {"cell_id": cell, "outcome": V.derive_cell_outcome(d)} for cell, d in by_cell.items()
    ]
    return results


class TestReadingMapCouplesToTheRecordedGateResult:
    @pytest.mark.parametrize(
        "sm,po,expected",
        [
            ("PASSES", "PASSES", "PASS"),
            ("FAILS", "FAILS", "FAIL"),
            ("PASSES", "FAILS", "UNABLE_TO_DETERMINE"),
            ("FAILS", "PASSES", V.G2_RECORD_REJECTED),
            ("UNABLE_TO_DETERMINE", "PASSES", "UNABLE_TO_DETERMINE"),
            ("PASSES", "UNABLE_TO_DETERMINE", "UNABLE_TO_DETERMINE"),
        ],
    )
    def test_required_gate_result_for_every_pair(self, sm: str, po: str, expected: str):
        assert V.required_g2_gate_result(sm, po) == expected

    def test_reading_dependent_pair_recorded_as_pass_is_rejected(self):
        """DELTA MAJOR 2A: the exact defect — reading-dependent readings, G2 recorded PASS."""
        results = _reading_dependent_row()
        row = results["candidate_results"][0]
        gates = dict(row["gate_results"])
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "PASS"
        row["gate_results"] = gates
        row["disposition"] = V.derive_candidate_disposition(gates)
        r = _validate(results)
        assert not r.ok
        assert any("the reading map governs" in e for e in r.errors)

    def test_reading_dependent_pair_recorded_as_pass_cannot_yield_a_constructible_candidate(self):
        results = _reading_dependent_row()
        row = results["candidate_results"][0]
        gates = dict(row["gate_results"])
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "PASS"
        row["gate_results"] = gates
        row["disposition"] = "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"
        r = _validate(results)
        assert not r.ok

    def test_reading_dependent_pair_recorded_as_fail_is_rejected(self):
        results = _reading_dependent_row()
        row = results["candidate_results"][0]
        gates = dict(row["gate_results"])
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "FAIL"
        row["gate_results"] = gates
        row["disposition"] = V.derive_candidate_disposition(gates)
        r = _validate(results)
        assert not r.ok
        assert any("G2_MAGNITUDE_INTRINSICALITY" in e for e in r.errors)

    def test_both_readings_pass_but_g2_recorded_unable_is_rejected(self):
        results = _full_results()
        row = results["candidate_results"][0]
        gates = _passing_gates()
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
        row["gate_results"] = gates
        row["disposition"] = V.derive_candidate_disposition(gates)
        r = _validate(results)
        assert not r.ok
        assert any("the reading map governs" in e for e in r.errors)

    def test_correctly_coupled_reading_dependent_candidate_is_accepted(self):
        results = _reading_dependent_row()
        assert results["candidate_results"][0]["disposition"] == "UNABLE_TO_DETERMINE"
        assert _validate(results).ok


# ---------------------------------------------------------------------------
# DELTA MAJOR 2B — uncertainty outranks a prerequisite failure, at candidate level only
# ---------------------------------------------------------------------------


class TestUncertaintyOutranksPrerequisite:
    def test_uncertain_g2_with_failing_prerequisite_is_unable_to_determine(self):
        """The exact defect: closing G9 cannot resolve SS-K.1, so this is not a to-do."""
        gates = _passing_gates()
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
        gates["G9_REPRESENTATION"] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "UNABLE_TO_DETERMINE"

    def test_uncertainty_also_outranks_the_snapshot_prerequisite(self):
        gates = _passing_gates()
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
        gates["G12_SNAPSHOT_ADMISSIBILITY_PATH"] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "UNABLE_TO_DETERMINE"

    def test_categorical_still_dominates_uncertainty(self):
        gates = _passing_gates()
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
        gates["G4_ORIGIN"] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "BLOCKED_CATEGORICALLY"

    def test_categorical_dominates_uncertainty_and_prerequisite_together(self):
        gates = _passing_gates()
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
        gates["G9_REPRESENTATION"] = "FAIL"
        gates["G4_ORIGIN"] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "BLOCKED_CATEGORICALLY"

    def test_prerequisite_alone_is_still_prerequisite_blocked(self):
        gates = _passing_gates()
        gates["G9_REPRESENTATION"] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"

    def test_results_reject_reading_dependent_recorded_as_prerequisite_blocked(self):
        results = _reading_dependent_row(G9_REPRESENTATION="FAIL")
        row = results["candidate_results"][0]
        row["disposition"] = "BLOCKED_PENDING_SEPARATE_PREREQUISITE"
        r = _validate(results)
        assert not r.ok
        assert any("BLOCKED_PENDING_SEPARATE_PREREQUISITE" in e for e in r.errors)

    def test_cell_precedence_is_unchanged(self):
        """A determinately prerequisite-blocked sibling may still keep a cell open."""
        assert [o for _c, o in V.CELL_PRECEDENCE] == [
            "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED",
            "BLOCKED_PENDING_SEPARATE_PREREQUISITE",
            "UNABLE_TO_DETERMINE",
            "BLOCKED_CATEGORICALLY",
        ]
        assert V.derive_cell_outcome(
            ["UNABLE_TO_DETERMINE", "BLOCKED_PENDING_SEPARATE_PREREQUISITE"]
        ) == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"

    def test_roll_up_precedence_is_unchanged(self):
        assert [o for _c, o in V.ROLL_UP_PRECEDENCE] == [
            "CANDIDATE_CONSTRUCTION_IDENTIFIED",
            "PREREQUISITE_REQUIRED",
            "UNABLE_TO_DETERMINE",
            "NO_CONSTRUCTIBLE_CANDIDATE",
        ]
        assert V.derive_roll_up_outcome(
            ["UNABLE_TO_DETERMINE", "BLOCKED_PENDING_SEPARATE_PREREQUISITE"]
        ) == "PREREQUISITE_REQUIRED"

    def test_candidate_precedence_declared_order_matches(self, base_data: dict):
        conditions = [
            r["condition"] for r in base_data["disposition_rules"]["candidate_disposition"]["precedence"]
        ]
        assert conditions == [
            "ANY_CATEGORICAL_GATE_FAILURE",
            "ANY_GATE_UNABLE_TO_DETERMINE",
            "ANY_PREREQUISITE_GATE_FAILURE",
            "ALL_GATES_PASS",
        ]

    def test_uncertainty_dominance_declared(self, base_data: dict):
        cand = base_data["disposition_rules"]["candidate_disposition"]
        assert cand["uncertainty_dominates_prerequisite"] is True
        assert cand["applies_at"] == "CANDIDATE_LEVEL_ONLY"

    def test_removing_uncertainty_dominance_rejected(self, data: dict):
        data["disposition_rules"]["candidate_disposition"]["uncertainty_dominates_prerequisite"] = False
        _assert_rejected(data, "uncertainty_dominates_prerequisite")

    def test_widening_the_scope_beyond_candidate_level_rejected(self, data: dict):
        data["disposition_rules"]["candidate_disposition"]["applies_at"] = "ALL_LEVELS"
        _assert_rejected(data, "applies_at")

    def test_g2_coupling_flag_required(self, data: dict):
        data["g2_reading_mapping"]["coupled_to_g2_gate_result"] = False
        _assert_rejected(data, "coupled_to_g2_gate_result")

    def test_required_gate_result_column_locked(self, data: dict):
        data["g2_reading_mapping"]["rows"][2]["required_g2_gate_result"] = "PASS"
        _assert_rejected(data, "required_g2_gate_result")


class TestCategoricalDefinitionNarrowed:
    def test_categorical_is_methodology_scoped(self, base_data: dict):
        block = base_data["categorical_definition"]
        assert block["means"] == "NOT_CLOSEABLE_BY_A_NAMED_PREREQUISITE_UNDER_THE_CURRENTLY_ACCEPTED_METHODOLOGY"
        assert block["does_not_mean"] == "PERMANENTLY_IMPOSSIBLE_UNDER_ALL_FUTURE_GOVERNANCE"

    def test_permanent_impossibility_claim_rejected(self, data: dict):
        data["categorical_definition"]["means"] = "NO_FUTURE_AUTHORIZATION_CAN_LIFT_THE_BAR"
        _assert_rejected(data, "categorical_definition.means")

    def test_prerequisite_requires_a_named_dependency(self, data: dict):
        data["prerequisite_definition"]["requires_named_dependency"] = False
        _assert_rejected(data, "requires_named_dependency")

    def test_protocol_does_not_claim_permanent_impossibility(self):
        text = V.PROTOCOL_PATH.read_text(encoding="utf-8")
        assert "no future authorization can lift" not in text.lower()


# ---------------------------------------------------------------------------
# MAJOR 3 — J.12 deferral
# ---------------------------------------------------------------------------


class TestJ12Deferred:
    def test_j12_recorded_as_deferred(self, base_data: dict):
        items = base_data["stage_1_testable_subset"]["items"]
        j12 = next(i for i in items if i["j_item"].startswith("J_12"))
        assert j12["stage_1_status"] == "NOT_YET_DETERMINABLE_DEFERRED"

    def test_all_twelve_j_items_mapped(self, base_data: dict):
        assert len(base_data["stage_1_testable_subset"]["items"]) == 12

    def test_claiming_j12_testable_rejected(self, data: dict):
        for item in data["stage_1_testable_subset"]["items"]:
            if item["j_item"].startswith("J_12"):
                item["stage_1_status"] = "TESTABLE"
        _assert_rejected(data, "J_12.stage_1_status")

    def test_deferred_requirement_present(self, base_data: dict):
        reqs = base_data["deferred_admissibility_requirements"]["requirements"]
        assert any(r["requirement_id"] == "J_12_EXACT_SET_VALUED_RECONCILIATION" for r in reqs)

    def test_removing_the_deferred_requirement_rejected(self, data: dict):
        data["deferred_admissibility_requirements"]["requirements"] = []
        _assert_rejected(data, "requirements: expected a non-empty list")

    def test_stage_1_may_not_claim_deferred_compliance(self, data: dict):
        data["deferred_admissibility_requirements"]["requirements"][0]["stage_1_may_claim_compliance"] = True
        _assert_rejected(data, "stage_1_may_claim_compliance")

    def test_deferral_must_state_its_reason(self, data: dict):
        data["deferred_admissibility_requirements"]["requirements"][0]["why_not_determinable_in_stage_1"] = " "
        _assert_rejected(data, "why_not_determinable_in_stage_1")

    def test_cross_sleeve_arithmetic_prohibited(self, data: dict):
        data["deferred_admissibility_requirements"][
            "cross_sleeve_arithmetic_to_satisfy_a_deferred_requirement"
        ] = "PERMITTED"
        _assert_rejected(data, "cross_sleeve_arithmetic_to_satisfy_a_deferred_requirement")

    def test_full_j_compliance_claim_is_forbidden_result_content(self, base_data: dict):
        assert (
            "ANY_CLAIM_OF_FULL_J_1_THROUGH_J_12_COMPLIANCE"
            in base_data["result_schema"]["forbidden_result_content"]
        )

    def test_stage_1_output_may_not_claim_full_j_compliance(self, data: dict):
        data["result_status_of_stage_1_output"]["may_claim_full_j_1_through_j_12_compliance"] = True
        _assert_rejected(data, "may_claim_full_j_1_through_j_12_compliance")

    def test_no_gate_decides_reconciliation(self, base_data: dict):
        for gate in base_data["gate_sequence"]["gates"]:
            assert "RECONCILIATION" not in gate["gate_id"]

    def test_cross_sleeve_arithmetic_in_prohibited_scope(self, base_data: dict):
        assert "CROSS_SLEEVE_OR_CROSS_BOUND_ARITHMETIC" in base_data["prohibited_scope"]


# ---------------------------------------------------------------------------
# MINOR 1 — lifecycle effectivity
# ---------------------------------------------------------------------------


class TestLifecycleEffectivity:
    def test_all_five_lifecycle_steps_required(self, base_data: dict):
        assert base_data["lifecycle_effectivity"]["charter_effective_only_after_all_of"] == list(
            V.LIFECYCLE_STEPS
        )

    def test_merge_alone_is_not_sufficient(self, base_data: dict):
        assert base_data["lifecycle_effectivity"]["merge_alone_is_sufficient"] is False

    def test_claiming_merge_alone_suffices_rejected(self, data: dict):
        data["lifecycle_effectivity"]["merge_alone_is_sufficient"] = True
        _assert_rejected(data, "merge_alone_is_sufficient")

    def test_dropping_post_merge_verification_rejected(self, data: dict):
        data["lifecycle_effectivity"]["charter_effective_only_after_all_of"] = [
            s for s in V.LIFECYCLE_STEPS if s != "IMMEDIATE_POST_MERGE_VERIFICATION"
        ]
        _assert_rejected(data, "charter_effective_only_after_all_of")

    def test_dropping_merge_commit_ci_rejected(self, data: dict):
        data["lifecycle_effectivity"]["charter_effective_only_after_all_of"] = [
            s for s in V.LIFECYCLE_STEPS if s != "SUCCESSFUL_MERGE_COMMIT_CI"
        ]
        _assert_rejected(data, "charter_effective_only_after_all_of")

    def test_stage_1_gated_on_construction_universe_closure_and_lifecycle_closure(
        self, base_data: dict
    ):
        precondition = base_data["lifecycle_effectivity"]["stage_1_execution_may_begin_only_after"]
        assert precondition == V.STAGE_1_EXECUTION_PRECONDITION
        # AMENDED BY XASSET-0028: the operative precondition is the six-gate successor lifecycle.
        assert precondition.startswith("XASSET_0037_LIFECYCLE_CLOSURE_ALL_SIX_GATES_THEN_")
        assert V.PREDECESSOR_STAGE_1_EXECUTION_PRECONDITION.startswith(
            "CONSTRUCTION_UNIVERSE_CLOSURE_THEN_"
        )
        assert (
            "XASSET_0027_LIFECYCLE_CLOSURE_AND_MERGED_HASH_VERIFICATION"
            in V.PREDECESSOR_STAGE_1_EXECUTION_PRECONDITION
        )
        # The spent predecessor condition must no longer be the operative one.
        assert precondition != V.PREDECESSOR_STAGE_1_EXECUTION_PRECONDITION

    def test_gating_stage_1_on_merge_alone_rejected(self, data: dict):
        data["lifecycle_effectivity"]["stage_1_execution_may_begin_only_after"] = "MERGE"
        _assert_rejected(data, "stage_1_execution_may_begin_only_after")

    def test_decision_binds_effectivity_to_the_full_lifecycle(self):
        text = V.DECISION_PATH.read_text(encoding="utf-8")
        assert "Merge alone is not sufficient" in text
        assert "immediate post-merge verification" in text
        assert "merge-commit CI" in text


# ---------------------------------------------------------------------------
# Zero-parameter declaration
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
# Vocabulary
# ---------------------------------------------------------------------------


class TestVocabulary:
    def test_candidate_and_cell_vocabularies_locked(self, base_data: dict):
        vocab = base_data["result_vocabulary"]
        assert vocab["candidate_dispositions"] == list(V.CANDIDATE_DISPOSITIONS)
        assert vocab["cell_outcomes"] == list(V.CELL_OUTCOMES)
        assert vocab["roll_up_outcomes"] == list(V.ROLL_UP_OUTCOMES)
        assert vocab["gate_result_vocabulary"] == list(V.GATE_RESULT_VOCABULARY)

    def test_added_vocabulary_value_rejected(self, data: dict):
        data["result_vocabulary"]["cell_outcomes"] = list(data["result_vocabulary"]["cell_outcomes"]) + [
            "PARTIALLY_SUPPORTED"
        ]
        _assert_rejected(data, "cell_outcomes")

    def test_scoring_mechanism_rejected(self, data: dict):
        data["result_vocabulary"]["mechanism"] = "WEIGHTED_MAJORITY_VOTE"
        _assert_rejected(data, "mechanism")

    def test_not_a_score_flag_required(self, data: dict):
        data["result_vocabulary"]["no_outcome_is_a_score"] = False
        _assert_rejected(data, "no_outcome_is_a_score")

    def test_cross_bound_and_cross_sleeve_reference_prohibited(self, base_data: dict):
        roll_up = base_data["roll_up_units"]
        assert roll_up["cross_bound_reference"] == "PROHIBITED"
        assert roll_up["cross_sleeve_reference"] == "PROHIBITED"

    def test_cross_sleeve_inference_permitted_is_rejected(self, data: dict):
        data["roll_up_units"]["cross_sleeve_reference"] = "PERMITTED"
        _assert_rejected(data, "cross_sleeve_reference")

    def test_point_or_range_values_locked(self, data: dict):
        data["result_vocabulary"]["point_or_range_support"]["values"] = ["ALWAYS"]
        _assert_rejected(data, "point_or_range_support.values")


# ---------------------------------------------------------------------------
# Stage boundary
# ---------------------------------------------------------------------------


class TestStageBoundary:
    def test_stage_2_is_not_authorized(self, base_data: dict):
        assert base_data["stages"]["stage_2"]["authorized_by_xasset_0027"] is False

    def test_authorizing_stage_2_rejected(self, data: dict):
        data["stages"]["stage_2"]["authorized_by_xasset_0027"] = True
        _assert_rejected(data, "stages.stage_2.authorized_by_xasset_0027")

    def test_stage_2_requires_separate_authorization(self, base_data: dict):
        assert (
            base_data["stages"]["stage_2"]["authorization_requirement"]
            == "SEPARATE_LATER_EXPLICITLY_ACCEPTED_GOVERNANCE_DECISION"
        )

    def test_weakening_stage_2_authorization_requirement_rejected(self, data: dict):
        data["stages"]["stage_2"]["authorization_requirement"] = "AUTOMATIC_ON_POSITIVE_FINDING"
        _assert_rejected(data, "stages.stage_2.authorization_requirement")

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

    def test_stage_1_executability_gated_on_both_preconditions(self, base_data: dict):
        assert (
            base_data["stages"]["stage_1"]["executable_only_after"]
            == V.STAGE_1_EXECUTION_PRECONDITION
        )

    def test_gating_stage_1_on_merge_alone_rejected_in_stages_block(self, data: dict):
        data["stages"]["stage_1"]["executable_only_after"] = "MERGE"
        _assert_rejected(data, "stages.stage_1.executable_only_after")

    def test_stage_1_unit_of_work_is_a_candidate(self, base_data: dict):
        assert base_data["stages"]["stage_1"]["unit_of_work"] == "ONE_CANDIDATE_EVALUATION"

    def test_execution_stopping_rule_ranges_over_registered_constructions(self, base_data: dict):
        stopping = base_data["execution"]["stopping_rules"]
        assert stopping["terminates_when"] == (
            "EVERY_REGISTERED_CONSTRUCTION_IN_THE_CLOSED_CONSTRUCTION_UNIVERSE_"
            "CARRIES_A_RECORDED_DISPOSITION"
        )
        # AMENDED BY XASSET-0028: the rule now ranges over the closed registered set.
        assert stopping["stopping_rule_currently_has_no_registered_set"] is False
        assert stopping["stopping_rule_amended_by"] == "XASSET-0028"

    def test_pinning_the_stopping_rule_to_the_family_slot_count_rejected(self, data: dict):
        data["execution"]["stopping_rules"]["terminates_when"] = (
            "ALL_240_REGISTERED_CANDIDATES_CARRY_A_RECORDED_DISPOSITION"
        )
        _assert_rejected(data, "terminates_when")

    def test_cell_only_stopping_rule_rejected(self, data: dict):
        data["execution"]["stopping_rules"]["terminates_when"] = "ALL_48_CELLS_CARRY_A_RECORDED_OUTCOME"
        _assert_rejected(data, "terminates_when")

    def test_authority_not_exercised_by_the_program(self, base_data: dict):
        assert base_data["authority"]["authority_exercised_by_this_program"] is False

    def test_exercising_authority_rejected(self, data: dict):
        data["authority"]["authority_exercised_by_this_program"] = True
        _assert_rejected(data, "authority_exercised_by_this_program")

    def test_stage_2_prohibited_in_scope(self, base_data: dict):
        assert "STAGE_2_EXECUTION" in base_data["prohibited_scope"]


# ---------------------------------------------------------------------------
# Execution discipline
# ---------------------------------------------------------------------------


class TestExecutionDiscipline:
    def test_early_stop_prohibited(self, base_data: dict):
        assert (
            base_data["execution"]["stopping_rules"]["early_stop_on_positive_finding"] == "PROHIBITED"
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

    def test_candidates_frozen_before_evaluation(self, data: dict):
        data["execution"]["history_mining_controls"]["candidates_frozen_before_evaluation"] = False
        _assert_rejected(data, "candidates_frozen_before_evaluation")

    def test_outcome_aware_candidate_change_prohibited(self, data: dict):
        data["execution"]["history_mining_controls"][
            "outcome_aware_candidate_addition_or_removal"
        ] = "PERMITTED"
        _assert_rejected(data, "outcome_aware_candidate_addition_or_removal")

    def test_outcome_aware_gate_change_prohibited(self, data: dict):
        data["execution"]["history_mining_controls"]["outcome_aware_gate_change"] = "PERMITTED"
        _assert_rejected(data, "outcome_aware_gate_change")

    @pytest.mark.parametrize("block", ["out_of_sample_discipline", "neighboring_parameter_robustness"])
    def test_non_applicability_must_state_a_reason(self, data: dict, block: str):
        data["execution"][block]["reason"] = "   "
        _assert_rejected(data, f"execution.{block}.reason")

    @pytest.mark.parametrize("block", ["out_of_sample_discipline", "neighboring_parameter_robustness"])
    def test_non_applicability_recorded_honestly(self, base_data: dict, block: str):
        entry = base_data["execution"][block]
        assert entry["applicable_to_stage_1"] is False
        assert entry["reason"].strip()

    def test_stage_2_must_still_carry_out_of_sample_discipline(self, base_data: dict):
        assert (
            base_data["execution"]["out_of_sample_discipline"]["required_of_any_future_stage_2"] is True
        )

    def test_negative_results_preserved(self, data: dict):
        block = data["execution"]["negative_result_preservation"]
        block["all_candidate_dispositions_recorded_regardless_of_direction"] = False
        _assert_rejected(data, "all_candidate_dispositions_recorded_regardless_of_direction")


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
            c for c in data["prohibited_inputs"]["barred_constructions"]
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
# Result boundary
# ---------------------------------------------------------------------------


class TestResultBoundary:
    @pytest.mark.parametrize(
        "flag",
        [
            "is_a_driver_source",
            "is_admissible_endpoint_supporting_evidence",
            "may_be_cited_as_endpoint_supporting_evidence",
            "may_enter_a_snapshot_as_a_driver",
            "may_claim_full_j_1_through_j_12_compliance",
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
            "may_claim_full_j_1_through_j_12_compliance",
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
            e for e in data["result_schema"]["forbidden_result_content"]
            if e != "ANY_NUMERIC_SLEEVE_SHARE"
        ]
        _assert_rejected(data, "ANY_NUMERIC_SLEEVE_SHARE")

    def test_results_file_not_created_by_this_filing(self, base_data: dict):
        assert base_data["result_schema"]["results_path_created_by_this_filing"] is False
        assert not (ROOT / base_data["result_schema"]["results_path"]).exists()

    @pytest.mark.parametrize("key", V.REQUIRED_CANDIDATE_RESULT_KEYS)
    def test_candidate_result_provenance_keys_present(self, base_data: dict, key: str):
        assert key in base_data["result_schema"]["candidate_result_keys"]

    def test_removing_a_provenance_key_rejected(self, data: dict):
        data["result_schema"]["candidate_result_keys"] = [
            k for k in data["result_schema"]["candidate_result_keys"] if k != "source_sha256"
        ]
        _assert_rejected(data, "source_sha256")

    def test_source_architecture_vocabulary_closed(self, base_data: dict):
        assert base_data["source_architecture_vocabulary"]["values"] == list(V.SOURCE_ARCHITECTURES)

    def test_hypothetical_must_forbid_path_and_hash(self, data: dict):
        data["source_architecture_vocabulary"]["hypothetical_forbids"] = []
        _assert_rejected(data, "hypothetical_forbids")


# ---------------------------------------------------------------------------
# Abstention and prohibited scope
# ---------------------------------------------------------------------------


class TestAbstentionAndScope:
    @pytest.mark.parametrize("condition", V.REQUIRED_ABSTENTION_CONDITIONS)
    def test_abstention_condition_present(self, base_data: dict, condition: str):
        present = {row["condition"] for row in base_data["mandatory_abstention_conditions"]}
        assert condition in present

    def test_reading_dependent_abstention_condition_present(self, base_data: dict):
        present = {row["condition"] for row in base_data["mandatory_abstention_conditions"]}
        assert "A_CANDIDATES_G2_OUTCOME_IS_READING_DEPENDENT_WHILE_SECTION_K_1_REMAINS_UNRESOLVED" in present

    def test_removed_abstention_condition_rejected(self, data: dict):
        data["mandatory_abstention_conditions"] = [
            r for r in data["mandatory_abstention_conditions"]
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
        assert V.scan_for_barred_content(f"value: {sample}", "fixture")

    def test_committed_artifacts_carry_no_barred_numeral(self):
        for path in (V.PREREG_PATH, V.PROTOCOL_PATH):
            text = path.read_text(encoding="utf-8")
            for pattern in V.BARRED_NUMERAL_PATTERNS:
                assert not re.search(pattern, text), f"{path.name} reproduces a barred value"

    @pytest.mark.parametrize("token", ["12%", "7.5 percent", "40 pct", "100%"])
    def test_endpoint_shaped_token_is_detected(self, token: str):
        assert V.scan_for_barred_content(f"the sleeve share is {token}", "fixture")

    def test_committed_artifacts_carry_no_endpoint_shaped_token(self):
        for path in (V.PREREG_PATH, V.PROTOCOL_PATH):
            findings = V.scan_for_barred_content(path.read_text(encoding="utf-8"), path.name)
            assert not findings, f"{path.name}: {findings}"

    def test_ordinary_prose_is_not_a_false_positive(self):
        clean = "The share of one normalized unit attributable to one named sleeve, at exact precision."
        assert V.scan_for_barred_content(clean, "fixture") == ()

    def test_derived_counts_are_not_false_positives(self):
        assert V.scan_for_barred_content("4 x 2 x 6 x 5 = 240 candidates over 48 cells", "f") == ()

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
        assert not result.ok and any("MIRROR" in e for e in result.errors)

    def test_mirror_value_mismatch_rejected(self):
        text = V.PROTOCOL_PATH.read_text(encoding="utf-8").replace(
            "family_slot_count: 240", "family_slot_count: 480"
        )
        result = V.validate_protocol_mirror(text)
        assert not result.ok and any("family_slot_count" in e for e in result.errors)

    def test_mirror_extra_key_rejected(self):
        text = V.PROTOCOL_PATH.read_text(encoding="utf-8").replace(
            f"hash_version: {V.HASH_VERSION}",
            f"hash_version: {V.HASH_VERSION}\nsmuggled_key: yes",
        )
        result = V.validate_protocol_mirror(text)
        assert not result.ok and any("smuggled_key" in e for e in result.errors)

    def test_mirror_reports_the_corrected_design(self):
        mirror = V.extract_block(V.PROTOCOL_PATH.read_text(encoding="utf-8"), V.MIRROR_BLOCK_RE)
        assert mirror is not None
        assert mirror["stage_2_authorized"] == "false"
        assert mirror["consequential_parameter_count"] == "0"
        assert mirror["construction_family_count"] == "5"
        assert mirror["family_slot_count"] == "240"
        assert mirror["gate_count"] == "12"
        assert mirror["j12_deferred"] == "true"

    def test_mirror_reports_stage_1_not_executable(self):
        mirror = V.extract_block(V.PROTOCOL_PATH.read_text(encoding="utf-8"), V.MIRROR_BLOCK_RE)
        assert mirror is not None
        # Structurally closed, operationally unauthorized -- both stated, neither conflated.
        assert mirror["stage_1_executable"] == "false"
        assert mirror["construction_universe_closed"] == "true"
        assert mirror["stage_1_structurally_closed"] == "true"
        assert mirror["stage_1_operationally_authorized"] == "false"
        assert mirror["registered_construction_count"] == "680"
        assert mirror["predecessor_hash_version"] == V.PREDECESSOR_HASH_VERSION

    def test_mirror_claiming_stage_1_executable_rejected(self):
        text = V.PROTOCOL_PATH.read_text(encoding="utf-8").replace(
            "stage_1_executable: false", "stage_1_executable: true"
        )
        result = V.validate_protocol_mirror(text)
        assert not result.ok and any("stage_1_executable" in e for e in result.errors)

    def test_mirror_reverting_to_an_unclosed_universe_rejected(self):
        text = V.PROTOCOL_PATH.read_text(encoding="utf-8").replace(
            "construction_universe_closed: true", "construction_universe_closed: false"
        )
        result = V.validate_protocol_mirror(text)
        assert not result.ok and any("construction_universe_closed" in e for e in result.errors)

    def test_mirror_claiming_operational_authorization_rejected(self):
        text = V.PROTOCOL_PATH.read_text(encoding="utf-8").replace(
            "stage_1_operationally_authorized: false", "stage_1_operationally_authorized: true"
        )
        result = V.validate_protocol_mirror(text)
        assert not result.ok and any(
            "stage_1_operationally_authorized" in e for e in result.errors
        )

    def test_mirror_wrong_universe_hash_rejected(self):
        import level1_construction_universe_closure_validator as CU

        text = V.PROTOCOL_PATH.read_text(encoding="utf-8").replace(
            CU.universe_aggregate_sha256(), "0" * 64
        )
        result = V.validate_protocol_mirror(text)
        assert not result.ok and any("construction_universe_sha256" in e for e in result.errors)

    def test_missing_hash_block_rejected(self):
        result = V.validate_charter_hash_pins("## decision with no pins\n")
        assert not result.ok and any("HASH-PINS" in e for e in result.errors)

    def test_rewriting_the_historical_predecessor_pin_rejected(self):
        """XASSET-0027's accepted pins are HISTORY and may never be restated."""
        text = V.DECISION_PATH.read_text(encoding="utf-8")
        tampered = text.replace(V.PREDECESSOR_PINS["preregistration_sha256"], "0" * 64)
        result = V.validate_charter_hash_pins(tampered)
        assert not result.ok
        assert any("accepted historical pin" in e for e in result.errors)

    def test_successor_pins_verify_the_live_canonical_bytes(self):
        text = V.SUCCESSOR_DECISION_PATH.read_text(encoding="utf-8")
        assert V.validate_successor_hash_pins(text).ok

    def test_successor_pin_mismatch_rejected(self):
        # AMENDED BY XASSET-0029: XASSET-0028's pins are historical, so a mismatch now means the
        # decision no longer records the digests it actually accepted -- history being rewritten.
        text = V.SUCCESSOR_DECISION_PATH.read_text(encoding="utf-8").replace(
            V.XASSET_0028_PINS["preregistration_sha256"], "0" * 64
        )
        result = V.validate_successor_hash_pins(text)
        assert not result.ok
        assert any("accepted historical pin" in e for e in result.errors)

    def test_successor_pin_equal_to_predecessor_rejected(self):
        text = V.SUCCESSOR_DECISION_PATH.read_text(encoding="utf-8").replace(
            f"protocol_sha256: {V.XASSET_0028_PINS['protocol_sha256']}",
            f"protocol_sha256: {V.PREDECESSOR_PINS['protocol_sha256']}",
        )
        result = V.validate_successor_hash_pins(text)
        assert not result.ok
        assert any("equals the predecessor pin" in e for e in result.errors)

    def test_missing_successor_block_rejected(self):
        result = V.validate_successor_hash_pins("## no pins here\n")
        assert not result.ok and any("XASSET-0028-HASH-PINS-V1" in e for e in result.errors)

    def test_successor_must_retain_predecessor_lineage(self):
        text = V.SUCCESSOR_DECISION_PATH.read_text(encoding="utf-8").replace(
            f"predecessor_protocol_sha256: {V.PREDECESSOR_PINS['protocol_sha256']}",
            "predecessor_protocol_sha256: " + "0" * 64,
        )
        result = V.validate_successor_hash_pins(text)
        assert not result.ok
        assert any("must retain the XASSET-0027 value" in e for e in result.errors)

    def test_wrong_pinned_path_rejected(self):
        text = V.DECISION_PATH.read_text(encoding="utf-8").replace(
            "protocol_path: research/level1_endpoint_evidence/PROTOCOL_V1.md",
            "protocol_path: research/level1_sleeve_robustness/PROTOCOL_V1.md",
        )
        result = V.validate_charter_hash_pins(text)
        assert not result.ok and any("protocol_path" in e for e in result.errors)


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
        assert "/private/tmp/phq-risk0001-results" in V.REQUIRED_PROTECTED_PATHS
        for path in (V.PREREG_PATH, V.PROTOCOL_PATH, V.DECISION_PATH):
            resolved = str(path.resolve())
            assert "phq-risk0001-results" not in resolved
            assert "level1_sleeve_robustness" not in resolved
        source = Path(V.__file__).read_text(encoding="utf-8")
        assert "Path(" not in source.replace("Path(__file__)", "")

    def test_validator_is_not_an_endpoint_admission_validator(self):
        assert V.__doc__ is not None
        collapsed = " ".join(V.__doc__.split())
        assert "is NOT an XASSET-0024" in collapsed
        assert "endpoint-admission validator" in collapsed
        assert "separately authorized successor" in collapsed
        assert "SS-J.12 is deferred" in collapsed

    def test_validator_does_not_decide_gates(self):
        """The module composes already-decided gate results; it never decides one."""
        collapsed = " ".join(V.__doc__.split())
        assert "cannot acquire data, execute the study, decide a gate" in collapsed


class TestRepositoryInvariants:
    def test_application_directory_absent(self):
        assert not (ROOT / "intelligence/level1_application").exists()

    def test_research_directory_contains_no_execution_artifact(self):
        research_dir = ROOT / "research/level1_endpoint_evidence"
        assert sorted(p.name for p in research_dir.iterdir()) == [
            "PROTOCOL_V1.md",
            "pre_registration.yaml",
        ]

    def test_risk_lane_artifacts_untouched_by_this_module(self):
        assert (ROOT / "research/level1_sleeve_robustness/pre_registration.yaml").exists()

    def test_decision_file_declares_lane_g_and_proposed_status(self):
        text = V.DECISION_PATH.read_text(encoding="utf-8")
        assert "status: Proposed" in text
        assert "decision_id: XASSET-0027" in text
