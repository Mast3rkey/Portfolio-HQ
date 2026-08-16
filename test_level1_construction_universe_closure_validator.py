"""Focused and adversarial tests for the XASSET-0028 construction-universe closure.

Covers the deterministic generator, the closed identity schema, the canonical serialization and
aggregate hash, the determination artifact's structural validation, the predecessor/successor pin
lineage, the preserved postures, and the contamination firewall.

Every mutation test asserts that a *corrupted* universe or determination is REJECTED, not merely that
the clean one passes.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path

import pytest
import yaml

import level1_construction_universe_closure_validator as V
import level1_endpoint_evidence_preregistration_validator as PREREG

REPO_ROOT = Path(__file__).resolve().parent
DETERMINATION = REPO_ROOT / "research/level1_construction_universe/CLOSURE_DETERMINATION_V1.yaml"


@pytest.fixture(scope="module")
def universe():
    return V.generate_construction_universe()


@pytest.fixture
def determination():
    return yaml.safe_load(DETERMINATION.read_text(encoding="utf-8"))


# =============================================================================================
# 1-7  Cardinality, determinism, identity, ordering, coverage
# =============================================================================================
class TestUniverseShape:
    def test_1_cardinality_is_independently_derived_not_a_literal(self, universe):
        """Recompute the cardinality from the closed dimensions without reading any literal."""
        expected = 0
        for sleeve in V.SLEEVES:
            for _bound in V.BOUNDS:
                for driver_class in V.DRIVER_CLASSES:
                    for _family in V.FAMILY_IDS:
                        expected += len(V.comparator_architectures(sleeve, driver_class))
        assert len(universe) == expected
        assert V.derived_cardinality() == expected
        assert expected == 680

    def test_1b_formula_matches_accepted_closed_dimensions(self):
        per = sum(len(V.comparator_architectures(V.SLEEVES[0], d)) for d in V.DRIVER_CLASSES)
        assert per == 17
        assert len(V.SLEEVES) * len(V.BOUNDS) * len(V.FAMILY_IDS) * per == 680

    def test_2_repeated_generation_is_byte_identical(self):
        a = V.canonical_universe_json(V.generate_construction_universe())
        b = V.canonical_universe_json(V.generate_construction_universe())
        assert a == b

    def test_3_aggregate_hash_is_stable_across_calls(self):
        assert V.universe_aggregate_sha256() == V.universe_aggregate_sha256()

    def test_3b_aggregate_hash_independently_recomputed(self, universe):
        blob = json.dumps(universe, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        assert hashlib.sha256(blob.encode("utf-8")).hexdigest() == V.universe_aggregate_sha256(
            universe
        )

    def test_4_construction_ids_are_unique(self, universe):
        ids = [r["construction_id"] for r in universe]
        assert len(set(ids)) == len(ids)

    def test_5_ordering_is_deterministic_and_ordinals_are_dense(self, universe):
        assert [r["ordinal"] for r in universe] == list(range(1, len(universe) + 1))
        again = V.generate_construction_universe()
        assert [r["construction_id"] for r in again] == [r["construction_id"] for r in universe]

    def test_5b_ordering_follows_the_declared_key_order(self, universe):
        seen = [
            (
                V.SLEEVES.index(r["sleeve"]),
                V.BOUNDS.index(r["bound"]),
                V.DRIVER_CLASSES.index(r["driver_class"]),
                V.FAMILY_IDS.index(r["family_id"]),
            )
            for r in universe
        ]
        assert seen == sorted(seen)

    def test_6_exactly_48_cells_all_covered(self, universe):
        cells = {r["cell_id"] for r in universe}
        assert len(cells) == 48
        expected = {
            V.cell_id(s, b, d) for s in V.SLEEVES for b in V.BOUNDS for d in V.DRIVER_CLASSES
        }
        assert cells == expected

    def test_7_per_driver_and_per_cell_cardinalities_exact(self, universe):
        per_driver: dict[str, int] = {}
        for r in universe:
            per_driver[r["driver_class"]] = per_driver.get(r["driver_class"], 0) + 1
        assert per_driver == {
            "portfolio_function": 40,
            "valuation_opportunity_cost": 160,
            "downside_path_risk": 160,
            "recovery": 160,
            "diversification_cobehavior": 120,
            "sleeve_deployability": 40,
        }
        assert sum(per_driver.values()) == 680
        assert set(V.per_cell_cardinality().values()) == {5, 15, 20}

    def test_7b_every_construction_belongs_to_a_valid_cell_and_family(self, universe):
        for r in universe:
            assert r["sleeve"] in V.SLEEVES
            assert r["bound"] in V.BOUNDS
            assert r["driver_class"] in V.DRIVER_CLASSES
            assert r["family_id"] in V.FAMILY_IDS
            assert r["cell_id"] == V.cell_id(r["sleeve"], r["bound"], r["driver_class"])
            assert r["construction_id"].startswith(r["cell_id"] + V.ID_SEPARATOR)


# =============================================================================================
# 8-19  Mutation rejection
# =============================================================================================
def _identity_hash(universe) -> str:
    return V.universe_aggregate_sha256(universe)


class TestMutationRejected:
    def test_8_duplicate_construction_changes_identity(self, universe):
        mutated = list(universe) + [copy.deepcopy(universe[0])]
        assert _identity_hash(mutated) != _identity_hash(universe)
        ids = [r["construction_id"] for r in mutated]
        assert len(set(ids)) != len(ids)

    def test_9_missing_construction_changes_identity(self, universe):
        mutated = list(universe)[1:]
        assert len(mutated) == len(universe) - 1
        assert _identity_hash(mutated) != _identity_hash(universe)

    def test_10_extra_unregistered_construction_changes_identity(self, universe):
        extra = copy.deepcopy(universe[0])
        extra["construction_id"] = "equity::LOWER::portfolio_function::R1_C1::INVENTED"
        assert _identity_hash(list(universe) + [extra]) != _identity_hash(universe)

    def test_11_reordering_changes_identity_because_order_is_binding(self, universe):
        mutated = list(universe)
        mutated[0], mutated[1] = mutated[1], mutated[0]
        assert _identity_hash(mutated) != _identity_hash(universe)

    def test_12_id_collision_detectable(self, universe):
        mutated = copy.deepcopy(list(universe))
        mutated[1]["construction_id"] = mutated[0]["construction_id"]
        ids = [r["construction_id"] for r in mutated]
        assert len(set(ids)) < len(ids)

    @pytest.mark.parametrize(
        "field,value",
        [
            ("sleeve", "crypto"),
            ("bound", "UPPER"),
            ("driver_class", "recovery"),
            ("family_id", "R2_C2"),
            ("counterpart", "crypto"),
            ("comparator_architecture", "ALT__crypto"),
            ("source_architecture", "EXISTING_SOURCE_ARCHITECTURE"),
            ("hypothetical_source_requirements", "any source at all will do"),
            ("evidence_proposition", "a different hypothesis entirely"),
            ("representation_posture", "A_PRIOR_RULE"),
        ],
    )
    def test_13_to_19_any_hypothesis_defining_mutation_changes_identity(
        self, universe, field, value
    ):
        mutated = copy.deepcopy(list(universe))
        mutated[0][field] = value
        assert _identity_hash(mutated) != _identity_hash(universe)

    def test_17b_route_and_class_always_match_the_family(self, universe):
        for r in universe:
            assert r["route"] == V.FAMILY_ROUTE[r["family_id"]]
            assert r["num_0001_class"] == V.FAMILY_NUM_0001_CLASS[r["family_id"]]


# =============================================================================================
# 20-23  Comparator grammar
# =============================================================================================
class TestComparatorGrammar:
    def test_20_uac_is_never_a_diversification_cobehavior_comparator(self, universe):
        for r in universe:
            if r["driver_class"] == "diversification_cobehavior":
                assert r["counterpart"] != V.UNASSIGNED
                assert V.UNASSIGNED not in r["comparator_architecture"]

    def test_20b_uac_is_present_for_every_comparison_scoped_class(self, universe):
        for driver_class in ("valuation_opportunity_cost", "downside_path_risk", "recovery"):
            for sleeve in V.SLEEVES:
                arch = V.comparator_architectures(sleeve, driver_class)
                assert (f"ALT__{V.UNASSIGNED}", V.UNASSIGNED) in arch
                assert len(arch) == 4

    @pytest.mark.parametrize("driver_class", ["portfolio_function", "sleeve_deployability"])
    def test_21_22_self_only_for_one_sleeve_scoped_classes(self, universe, driver_class):
        arch = V.comparator_architectures(V.SLEEVES[0], driver_class)
        assert arch == (("SELF", None),)
        for r in universe:
            if r["driver_class"] == driver_class:
                assert r["counterpart"] is None
                assert r["comparator_architecture"] == "SELF"
                assert r["comparison_subject_kind"] == V.SUBJECT_SLEEVE_SELF

    def test_23_pair_identity_is_canonical_and_unordered(self, universe):
        pairs = set()
        for r in universe:
            if r["driver_class"] == "diversification_cobehavior":
                pid = r["unordered_pair_id"]
                assert pid is not None
                pairs.add(pid)
                # canonical: reversing the arguments yields the same id
                assert V.unordered_pair_id(r["sleeve"], r["counterpart"]) == pid
                assert V.unordered_pair_id(r["counterpart"], r["sleeve"]) == pid
        assert len(pairs) == 6  # 4 choose 2, XASSET-0020 SS-H

    def test_23b_never_self_paired(self, universe):
        for r in universe:
            if r["counterpart"] is not None and r["counterpart"] != V.UNASSIGNED:
                assert r["counterpart"] != r["sleeve"]

    def test_23c_scope_partition_matches_canonical_bytes(self):
        assert V.check_scope_partition_matches_canonical() == ()

    def test_23d_unknown_sleeve_or_driver_rejected(self):
        with pytest.raises(ValueError):
            V.comparator_architectures("not_a_sleeve", "recovery")
        with pytest.raises(ValueError):
            V.comparator_architectures("equity", "not_a_driver")


# =============================================================================================
# 24-27  R2, source architecture, free text, representation
# =============================================================================================
class TestHypothesisIntegrity:
    def test_24_r2_requires_a_source_prescribed_derivation_and_composes_nothing(self, universe):
        r2 = [r for r in universe if r["family_id"] == V.R2_FAMILY_ID]
        assert len(r2) == 136  # 680 / 5 families
        for r in r2:
            req = r["hypothetical_source_requirements"]
            assert "must itself prescribe exactly one XASSET-0023 SS-H.3 derivation" in req
            assert "may compose, select among, or invent that derivation" in req
        # No arithmetic operator is ever emitted into a hypothesis field.
        for r in universe:
            assert not re.search(r"[=+*/]|\bsum\b|\bmean\b", r["hypothetical_source_requirements"])

    def test_24b_r1_requires_a_source_stated_bound(self, universe):
        for r in universe:
            if r["family_id"] != V.R2_FAMILY_ID:
                assert "uniquely state the bound under XASSET-0023 SS-H.2" in (
                    r["hypothetical_source_requirements"]
                )

    def test_25_source_architecture_is_frozen_hypothetical_on_every_record(self, universe):
        assert {r["source_architecture"] for r in universe} == {
            V.FROZEN_SOURCE_ARCHITECTURE
        }
        assert V.FROZEN_SOURCE_ARCHITECTURE in PREREG.SOURCE_ARCHITECTURES
        # hypothetical_forbids: no path or hash may appear in a frozen identity.
        for r in universe:
            assert "source_path" not in r
            assert "source_sha256" not in r

    def test_26_no_result_author_free_text_field_exists(self, universe):
        """Descriptive fields must be regenerable from closed identity alone."""
        for r in universe[:40] + universe[-40:]:
            regenerated = V._evidence_proposition(
                r["sleeve"], r["bound"], r["driver_class"], r["family_id"], r["counterpart"]
            )
            assert regenerated == r["evidence_proposition"]
            regen_req = V._hypothetical_source_requirements(
                r["sleeve"], r["bound"], r["driver_class"], r["family_id"], r["counterpart"]
            )
            assert regen_req == r["hypothetical_source_requirements"]

    def test_26b_evidence_proposition_is_unique_per_construction(self, universe):
        props = [r["evidence_proposition"] for r in universe]
        assert len(set(props)) == len(props)

    def test_27_representation_is_a_posture_not_a_solved_rule(self, universe):
        for r in universe:
            assert r["representation_posture"] == "SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED"
        blob = V.canonical_universe_json(universe)
        for banned in ("CM-14", "CM-15", "CM-16", "CM-17", "representation_rule"):
            assert banned not in blob


# =============================================================================================
# 28-31  Preserved postures
# =============================================================================================
class TestPreservedPostures:
    def test_28_k1_remains_unresolved(self, determination):
        assert (
            determination["preserved_postures"]["xasset_0024_section_k1"]
            == "UNRESOLVED_BOTH_READINGS_PRESERVED"
        )

    def test_28b_no_construction_assumes_a_k1_reading(self, universe):
        blob = V.canonical_universe_json(universe)
        for banned in ("subject_matter_reading", "preference_only_reading", "k1_resolved"):
            assert banned not in blob

    def test_29_j12_remains_deferred(self, determination):
        assert determination["preserved_postures"]["section_j12"] == "DEFERRED"

    def test_29b_no_whole_candidate_reconciliation_in_identity(self, universe):
        blob = V.canonical_universe_json(universe)
        for banned in ("reconciliation", "whole_candidate"):
            assert banned not in blob

    def test_30_stage_2_unauthorized(self, determination):
        assert determination["preserved_postures"]["stage_2"] == "NOT_AUTHORIZED"
        assert "STAGE_2_AUTHORIZATION" in determination["prohibited_scope"]

    def test_31_application_authority_withheld(self, determination):
        assert determination["preserved_postures"]["application_authority"] == "WITHHELD"
        assert "APPLICATION_AUTHORITY" in determination["prohibited_scope"]


# =============================================================================================
# 32-37  Firewalls
# =============================================================================================
class TestFirewalls:
    def test_32_no_endpoint_shaped_value_in_universe_or_determination(self, universe):
        blob = V.canonical_universe_json(universe)
        assert PREREG.ENDPOINT_SHAPED_TOKEN.search(blob) is None
        text = DETERMINATION.read_text(encoding="utf-8")
        assert PREREG.ENDPOINT_SHAPED_TOKEN.search(text) is None

    def test_33_contamination_firewall_is_the_full_predecessor_one(self):
        """MINOR 2: the successor must never protect fewer values than its predecessor."""
        assert len(PREREG.BARRED_NUMERAL_PATTERNS) == 5
        for pattern in PREREG.BARRED_NUMERAL_PATTERNS:
            probe = pattern.replace("\\", "")
            findings = V.scan_for_barred_content(f"value {probe} here", "probe")
            assert findings, f"barred numeral {probe} was not caught"

    def test_33b_scan_delegates_rather_than_duplicating(self):
        assert V.scan_for_barred_content.__doc__
        assert V.scan_for_barred_content("clean text", "w") == PREREG.scan_for_barred_content(
            "clean text", "w"
        )
        assert not hasattr(V, "BARRED_HISTORICAL_NUMERALS")

    def test_33c_universe_and_determination_are_contamination_free(self, universe):
        assert V.scan_for_barred_content(V.canonical_universe_json(universe), "universe") == ()
        assert (
            V.scan_for_barred_content(DETERMINATION.read_text(encoding="utf-8"), "determination")
            == ()
        )

    def test_34_no_equal_split_midpoint_or_residual_leakage(self, universe):
        blob = V.canonical_universe_json(universe).lower()
        for banned in ("equal split", "midpoint", "residual", "pro-rata", "pro rata", "optimizer"):
            assert banned not in blob

    def test_35_zero_consequential_numeric_free_parameters(self, universe):
        """Every number in a construction is an index or a derived class label, never a parameter."""
        for r in universe:
            for key, value in r.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    assert key in ("ordinal", "num_0001_class")

    def test_36_universe_is_not_outcome_aware(self, universe):
        blob = V.canonical_universe_json(universe).lower()
        for banned in ("blocked_categorically", "disposition", "pass", "fail", "outcome"):
            assert banned not in blob

    def test_37_no_reserve_or_unregistered_construction_path(self, universe):
        blob = V.canonical_universe_json(universe).lower()
        for banned in ("reserve_construction", "unregistered", "ad_hoc", "discretionary"):
            assert banned not in blob


# =============================================================================================
# 38-42  Canonical lineage, Stage-1 gating, artifacts
# =============================================================================================
class TestCanonicalLineageAndStage1:
    def test_38_predecessor_hashes_preserved_as_history(self, determination):
        pred = determination["canonical_amendment"]["predecessor_pins"]
        assert (
            pred["research/level1_endpoint_evidence/PROTOCOL_V1.md"]
            == "1a7b288718dfc688adb409ea9ecdf0fe5c858a32ee154f4f407c132895f41c8b"
        )
        assert (
            pred["research/level1_endpoint_evidence/pre_registration.yaml"]
            == "bb25b1181c94d4dba2939a634b6fcb894f93597a664d5e91ffdcf021de3d385f"
        )
        assert determination["canonical_amendment"]["rewrites_accepted_history"] is False

    def test_38b_xasset_0027_record_preserved_inside_the_canonical_file(self):
        data = yaml.safe_load(
            (REPO_ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )
        pred = data["construction_universe_closure"]["xasset_0027_predecessor_record"]
        assert pred["status"] == "NOT_CLOSED"
        assert pred["preserved_verbatim"] is True
        assert len(pred["routes_considered_and_unavailable_to_this_filing"]) == 2

    def test_39_successor_pins_verify_observed_final_bytes(self, determination):
        for rel, digest in determination["canonical_amendment"]["successor_pins"].items():
            assert V.sha256_file(REPO_ROOT / rel) == digest

    def test_39b_successor_pins_differ_from_predecessor(self, determination):
        amendment = determination["canonical_amendment"]
        for rel, digest in amendment["successor_pins"].items():
            assert digest != amendment["predecessor_pins"][rel]

    def test_40_stale_contradictory_sentence_is_superseded(self):
        data = yaml.safe_load(
            (REPO_ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )
        decl = data["consequential_parameter_registry"]["zero_parameter_declaration"]
        assert "candidate universe now closed" not in decl["design_consequence"]
        assert "XASSET-0028" in decl["design_consequence"]
        assert "design_consequence_amendment_note" in decl
        # And no operative field simultaneously says NOT_CLOSED.
        assert data["construction_universe_closure"]["status"] == "CLOSED"

    def test_40b_protocol_mirror_agrees_with_preregistration(self):
        protocol = (REPO_ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md").read_text(
            encoding="utf-8"
        )
        assert PREREG.validate_protocol_mirror(protocol).ok

    def test_41_pre_lifecycle_execution_remains_blocked(self, determination):
        stage_1 = determination["stage_1"]
        assert stage_1["construction_universe_structurally_closed"] is True
        assert stage_1["operationally_authorized"] is False
        assert stage_1["executed_by_this_unit"] is False
        assert stage_1["no_merge_to_execution_gap"] is True
        data = yaml.safe_load(
            (REPO_ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )
        assert data["stage_1_executability"]["executable"] is False
        assert data["stage_1_executability"]["authorized_by_xasset_0028"] is False

    def test_42_no_stage1_result_or_application_artifact_exists(self):
        assert not (REPO_ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()
        assert not (REPO_ROOT / "intelligence/level1_application").exists()
        assert list(REPO_ROOT.glob("**/stage1_results.yaml")) == []

    def test_42b_risk_results_path_never_referenced_as_an_input(self):
        text = Path(V.__file__).read_text(encoding="utf-8")
        assert "/private/tmp/phq-risk0001-results" not in text


# =============================================================================================
# Determination-artifact structural validation
# =============================================================================================
class TestDeterminationValidation:
    def test_clean_artifact_validates(self):
        assert V.validate_file().ok

    def test_status_must_be_closed(self, determination):
        determination["status"] = "NOT_CLOSED"
        assert not V.validate(determination).ok

    def test_wrong_cardinality_rejected(self, determination):
        determination["universe_identity"]["registered_construction_count"] = 679
        result = V.validate(determination)
        assert not result.ok
        assert any("registered_construction_count" in e for e in result.errors)

    def test_wrong_aggregate_hash_rejected(self, determination):
        determination["universe_identity"]["aggregate_sha256"] = "0" * 64
        result = V.validate(determination)
        assert any("aggregate_sha256" in e for e in result.errors)

    def test_wrong_per_cell_rejected(self, determination):
        key = next(iter(determination["per_cell_cardinality"]))
        determination["per_cell_cardinality"][key] = 99
        assert not V.validate(determination).ok

    def test_claiming_uac_as_pair_comparator_rejected(self, determination):
        determination["comparator_contract"][
            "unassigned_capital_is_a_diversification_cobehavior_comparator"
        ] = True
        assert not V.validate(determination).ok

    def test_claiming_a_new_comparator_rule_rejected(self, determination):
        determination["comparator_contract"]["supplies_a_new_comparator_rule"] = True
        assert not V.validate(determination).ok

    def test_mutated_scope_partition_rejected(self, determination):
        determination["comparator_contract"]["driver_class_scope"][
            "diversification_cobehavior"
        ] = "COMPARISON_SCOPED_COMPARATOR_NOT_FIXED"
        assert not V.validate(determination).ok

    def test_operational_authorization_claim_rejected(self, determination):
        determination["stage_1"]["operationally_authorized"] = True
        assert not V.validate(determination).ok

    def test_missing_effectivity_gate_rejected(self, determination):
        determination["stage_1"]["effectivity_gates"] = ["MERGE"]
        assert not V.validate(determination).ok

    def test_unknown_top_level_key_rejected(self, determination):
        determination["smuggled"] = "value"
        assert not V.validate(determination).ok

    def test_missing_top_level_key_rejected(self, determination):
        del determination["universe_identity"]
        assert not V.validate(determination).ok

    def test_successor_pin_equal_to_predecessor_rejected(self, determination):
        amendment = determination["canonical_amendment"]
        rel = "research/level1_endpoint_evidence/PROTOCOL_V1.md"
        amendment["successor_pins"][rel] = amendment["predecessor_pins"][rel]
        result = V.validate(determination)
        assert any("unchanged from the predecessor pin" in e for e in result.errors)

    def test_rewritten_predecessor_pin_rejected(self, determination):
        determination["canonical_amendment"]["predecessor_pins"][
            "research/level1_endpoint_evidence/PROTOCOL_V1.md"
        ] = "0" * 64
        result = V.validate(determination)
        assert any("predecessor_pins" in e for e in result.errors)

    @pytest.mark.parametrize("phrase", list(V.BANNED_PERMANENCE_PHRASES))
    def test_permanence_overclaim_rejected(self, determination, phrase):
        determination["closure_basis"] = f"this route {phrase} be revisited"
        result = V.validate(determination)
        assert any(phrase in e for e in result.errors)

    @pytest.mark.parametrize("phrase", list(V.BANNED_EXECUTION_CLAIMS))
    def test_execution_authorization_claim_rejected(self, determination, phrase):
        determination["closure_basis"] = f"note: {phrase} now"
        result = V.validate(determination)
        assert any(phrase in e for e in result.errors)

    def test_endpoint_shaped_token_in_artifact_rejected(self, determination):
        determination["closure_basis"] = "the sleeve receives 12.5% of the unit"
        assert not V.validate(determination).ok

    def test_barred_historical_numeral_in_artifact_rejected(self, determination):
        determination["closure_basis"] = "prior output was 66.68 here"
        result = V.validate(determination)
        assert any("barred historical" in e for e in result.errors)

    def test_missing_prohibited_scope_entry_rejected(self, determination):
        determination["prohibited_scope"] = ["STAGE_1_EXECUTION"]
        assert not V.validate(determination).ok

    def test_non_mapping_rejected(self):
        assert not V.validate([]).ok

    def test_unparseable_file_rejected(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text("::: not yaml :::", encoding="utf-8")
        assert not V.validate_file(bad).ok

    def test_missing_file_rejected(self, tmp_path):
        assert not V.validate_file(tmp_path / "absent.yaml").ok


# =============================================================================================
# Coupling and isolation
# =============================================================================================
class TestCoupling:
    def test_zero_allocator_and_margin_import_coupling(self):
        text = Path(V.__file__).read_text(encoding="utf-8")
        for banned in ("import allocate", "import margin_state", "from allocate", "from margin_state"):
            assert banned not in text
        for other in ("allocate.py", "margin_state.py", "levels.py"):
            src = (REPO_ROOT / other).read_text(encoding="utf-8")
            assert "level1_construction_universe_closure_validator" not in src

    def test_generator_is_pure_no_clock_or_randomness(self):
        text = Path(V.__file__).read_text(encoding="utf-8")
        for banned in ("random.", "datetime.now", "time.time", "os.environ", "date.today"):
            assert banned not in text

    def test_prereg_validator_still_passes_with_amended_canonical_bytes(self):
        assert PREREG.validate_file().ok


# =============================================================================================
# Review 4946087943 — BLOCKING 1: frozen source-architecture / provenance model
# =============================================================================================
class TestFrozenSourceProvenanceModel:
    def test_1_generator_identity_satisfies_canonical_frozen_provenance(self, universe):
        """Every record carries exactly what frozen_provenance_requirements demands."""
        for r in universe:
            assert r["source_architecture"] == "HYPOTHETICAL_SOURCE_ARCHITECTURE"
            assert r["hypothetical_source_requirements"].strip()
            assert "source_path" not in r and "source_sha256" not in r

    def test_1b_canonical_contract_still_binds_this_unit(self):
        data = yaml.safe_load(
            (REPO_ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )
        frozen = data["frozen_provenance_requirements"]
        assert frozen["applies_to"] == "THE_FUTURE_CONSTRUCTION_UNIVERSE_CLOSURE_UNIT"
        assert frozen["binding_on_any_future_stage_1"] is True
        assert frozen["result_author_may_alter_a_frozen_architecture"] is False

    def test_2_source_architecture_cannot_be_selected_at_result_time(self, determination):
        assert determination["source_architecture_contract"][
            "source_architecture_selectable_at_result_time"
        ] is False
        determination["source_architecture_contract"][
            "source_architecture_selectable_at_result_time"
        ] = True
        assert not V.validate(determination).ok

    def test_3_existing_source_identity_cannot_be_substituted(self, universe):
        """A frozen HYPOTHETICAL record may not be silently converted to an EXISTING one."""
        frozen = V.frozen_construction_universe()
        cid = universe[0]["construction_id"]
        row = _result_row(cid, universe[0])
        row["source_architecture"] = "EXISTING_SOURCE_ARCHITECTURE"
        row["source_path"] = "research/level1_endpoint_evidence/PROTOCOL_V1.md"
        row["source_sha256"] = "0" * 64
        errs = _run_stage1(row, frozen)
        assert any("may not alter a frozen architecture" in e for e in errs)

    @pytest.mark.parametrize(
        "mutation,needle",
        [
            ({"hypothetical_source_requirements": "anything I like"},
             "does not match the frozen construction"),
            ({"hypothetical_source_requirements": ""},
             "required for HYPOTHETICAL_SOURCE_ARCHITECTURE"),
            ({"source_path": "research/level1_endpoint_evidence/PROTOCOL_V1.md"},
             "must carry no source_path or source_sha256"),
            ({"source_sha256": "a" * 64}, "must carry no source_path or source_sha256"),
        ],
    )
    def test_4_to_9_frozen_requirements_cannot_be_mutated(self, universe, mutation, needle):
        frozen = V.frozen_construction_universe()
        row = _result_row(universe[0]["construction_id"], universe[0])
        row.update(mutation)
        errs = _run_stage1(row, frozen)
        assert any(needle in e for e in errs), errs

    def test_10_generated_construction_is_structurally_consumable(self, universe):
        """The frozen adapter emits exactly the shape validate_stage1_results() expects."""
        frozen = V.frozen_construction_universe()
        assert len(frozen) == len(universe)
        for cid, rec in frozen.items():
            assert set(rec) == set(V.FROZEN_RESULT_IDENTITY_FIELDS)
        row = _result_row(universe[0]["construction_id"], universe[0])
        errs = _run_stage1(row, frozen)
        # No provenance-identity error survives for a faithful row.
        assert not [
            e
            for e in errs
            if "source_architecture" in e
            or "hypothetical_source_requirements" in e
            or "source_path" in e
            or "source_sha256" in e
        ], errs

    def test_11_two_evaluations_share_one_frozen_hypothesis_identity(self):
        a = V.frozen_construction_universe()
        b = V.frozen_construction_universe()
        assert a == b
        assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)

    def test_12_negative_does_not_depend_on_an_unbounded_source_search(self, universe):
        """No institution, vendor, jurisdiction, or document is named anywhere."""
        blob = V.canonical_universe_json(universe).lower()
        for banned in ("inc.", "llc", "gmbh", "bloomberg", "msci", "s&p", "morningstar",
                       "vendor", "institution name", "provider name"):
            assert banned not in blob

    def test_12b_requirements_are_identity_determined_and_distinct(self, universe):
        reqs = [r["hypothetical_source_requirements"] for r in universe]
        assert len(set(reqs)) == len(reqs)

    def test_existing_source_half_is_disposed_not_omitted(self, determination):
        contract = determination["source_architecture_contract"]
        assert contract["existing_source_architecture_disposition"] == (
            "RESOLVED_BY_XASSET_0025_OUTCOME_C_OVER_THE_XASSET_0021_FROZEN_SNAPSHOT"
        )
        determination["source_architecture_contract"][
            "existing_source_architecture_disposition"
        ] = "OMITTED"
        assert not V.validate(determination).ok


# =============================================================================================
# Review 4946087943 — MAJOR 1: one unified six-gate Stage-1 lifecycle
# =============================================================================================
class TestUnifiedStage1Lifecycle:
    def test_13_operative_preconditions_name_the_successor_lifecycle(self):
        data = yaml.safe_load(
            (REPO_ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )
        expected = PREREG.STAGE_1_EXECUTION_PRECONDITION
        assert "XASSET_0028" in expected
        assert data["lifecycle_effectivity"]["stage_1_execution_may_begin_only_after"] == expected
        assert data["stages"]["stage_1"]["executable_only_after"] == expected
        # The spent XASSET-0027 condition survives only as explicit history.
        assert data["lifecycle_effectivity"][
            "predecessor_stage_1_execution_may_begin_only_after_xasset_0027"
        ] == PREREG.PREDECESSOR_STAGE_1_EXECUTION_PRECONDITION
        assert "XASSET_0027" in PREREG.PREDECESSOR_STAGE_1_EXECUTION_PRECONDITION

    def test_14_all_six_gates_required_everywhere(self, determination):
        assert len(V.STAGE_1_EFFECTIVITY_GATES) == 6
        assert set(determination["stage_1"]["effectivity_gates"]) == set(
            V.STAGE_1_EFFECTIVITY_GATES
        )
        assert set(PREREG.STAGE_1_EFFECTIVITY_GATES) == set(V.STAGE_1_EFFECTIVITY_GATES)
        data = yaml.safe_load(
            (REPO_ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )
        assert set(
            data["stage_1_executability"]["operational_authorization_requires_all_of"]
        ) == set(V.STAGE_1_EFFECTIVITY_GATES)

    @pytest.mark.parametrize("gate", list(V.STAGE_1_EFFECTIVITY_GATES))
    def test_15_removing_any_gate_fails_validation(self, determination, gate):
        determination["stage_1"]["effectivity_gates"] = [
            g for g in V.STAGE_1_EFFECTIVITY_GATES if g != gate
        ]
        result = V.validate(determination)
        assert not result.ok
        assert any(gate in e for e in result.errors)

    def test_15b_unknown_gate_rejected(self, determination):
        determination["stage_1"]["effectivity_gates"] = list(
            V.STAGE_1_EFFECTIVITY_GATES
        ) + ["SOMETHING_ELSE"]
        assert not V.validate(determination).ok

    def test_16_merge_alone_is_insufficient(self, determination):
        determination["stage_1"]["effectivity_gates"] = ["MERGE"]
        assert not V.validate(determination).ok

    def test_17_structural_closure_alone_is_insufficient(self):
        """The universe is readable, and Stage 1 still fails closed."""
        assert len(PREREG.closed_construction_universe()) == 680
        authorized, reason = PREREG.stage_1_operational_authorization_is_effective()
        assert authorized is False
        assert "not true" in reason
        result = PREREG.validate_stage1_results({"candidate_results": []})
        assert not result.ok
        assert any("not operationally authorized" in e for e in result.errors)

    def test_17b_fail_closed_reads_canonical_bytes_not_a_constant(self, tmp_path):
        """A results author cannot flip authorization; it is read from the canonical file."""
        fake = tmp_path / "prereg.yaml"
        fake.write_text("stage_1_executability:\n  executable: true\n", encoding="utf-8")
        assert PREREG.stage_1_operational_authorization_is_effective(fake)[0] is True
        fake.write_text("stage_1_executability:\n  executable: false\n", encoding="utf-8")
        assert PREREG.stage_1_operational_authorization_is_effective(fake)[0] is False


# =============================================================================================
# Review 4946087943 — MINOR 1: unambiguous no-preference boolean
# =============================================================================================
class TestNoPreferenceBoolean:
    def test_18_predicate_and_value_agree_and_are_enforced(self):
        data = yaml.safe_load(
            (REPO_ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )
        props = data["construction_universe_closure"]["closure_basis_properties"]
        assert props["selects_ranks_or_prefers_any_sleeve_or_comparator"] is False
        assert "selects_ranks_or_prefers_no_sleeve_or_comparator" not in props

    def test_18b_flipping_the_flag_is_rejected(self):
        data = yaml.safe_load(
            (REPO_ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )
        data["construction_universe_closure"]["closure_basis_properties"][
            "selects_ranks_or_prefers_any_sleeve_or_comparator"
        ] = True
        result = PREREG.validate(data)
        assert not result.ok
        assert any("selects_ranks_or_prefers_any_sleeve_or_comparator" in e for e in result.errors)


def _result_row(construction_id: str, record) -> dict:
    """Build a faithful Stage-1 candidate row from a frozen construction."""
    row = {key: None for key in PREREG.REQUIRED_CANDIDATE_RESULT_KEYS}
    row.update(
        {
            "construction_id": construction_id,
            "cell_id": record["cell_id"],
            "sleeve": record["sleeve"],
            "bound": record["bound"],
            "driver_class": record["driver_class"],
            "family_id": record["family_id"],
            "route": record["route"],
            "num_0001_class": record["num_0001_class"],
            "source_architecture": record["source_architecture"],
            "hypothetical_source_requirements": record["hypothetical_source_requirements"],
            "governing_authority_refs": list(record["governing_authority_refs"]),
        }
    )
    # REQUIRED_CANDIDATE_RESULT_KEYS requires source_path/source_sha256 to be PRESENT, while
    # source_architecture_vocabulary.hypothetical_forbids requires them to carry no value. Both are
    # satisfied by present-and-None, which is exactly what a frozen HYPOTHETICAL row looks like.
    row["source_path"] = None
    row["source_sha256"] = None
    return row


def _run_stage1(row: dict, frozen) -> tuple[str, ...]:
    """Exercise the PRIVATE structural validator, which is explicitly not an authorization path."""
    # PRIVATE structural seam. It confers no authorization and is not the public boundary.
    return PREREG._validate_stage1_results_against_universe(
        {"candidate_results": [row]}, frozen
    ).errors


# =============================================================================================
# Review 4946154405 — BLOCKING 1: the public authorization boundary is unconditional
# =============================================================================================
class TestPublicAuthorizationBoundary:
    def test_1_public_validator_fails_before_lifecycle_closure(self):
        result = PREREG.validate_stage1_results({"candidate_results": []})
        assert not result.ok
        assert any("not operationally authorized" in e for e in result.errors)

    def test_2_public_api_exposes_no_universe_parameter(self):
        """The bypass was a public parameter; it is removed, not merely discouraged."""
        import inspect

        params = inspect.signature(PREREG.validate_stage1_results).parameters
        assert list(params) == ["results"]
        assert "construction_universe" not in params

    def test_2b_supplying_a_universe_to_the_public_api_is_impossible(self):
        with pytest.raises(TypeError):
            PREREG.validate_stage1_results(  # type: ignore[call-arg]
                {"candidate_results": []},
                construction_universe=V.frozen_construction_universe(),
            )

    def test_2c_an_alternate_universe_cannot_reach_the_public_path(self):
        """Even a hand-built universe cannot be routed through the public boundary."""
        with pytest.raises(TypeError):
            PREREG.validate_stage1_results({"candidate_results": []}, {})  # type: ignore[call-arg]

    def test_3_private_helper_confers_no_authorization(self):
        """The structural seam validates shape; it never reports Stage 1 authorized."""
        frozen = V.frozen_construction_universe()
        result = PREREG._validate_stage1_results_against_universe(
            {"candidate_results": []}, frozen
        )
        # It runs structural checks rather than short-circuiting on authorization...
        assert not any("not operationally authorized" in e for e in result.errors)
        # ...and the real authorization state is unchanged by having called it.
        assert PREREG.stage_1_operational_authorization_is_effective()[0] is False
        assert not PREREG.validate_stage1_results({"candidate_results": []}).ok

    def test_4_results_document_cannot_self_authorize(self):
        forged = {
            "candidate_results": [],
            "stage_1_executability": {"executable": True},
            "operationally_authorized": True,
            "authorization": "GRANTED",
        }
        result = PREREG.validate_stage1_results(forged)
        assert not result.ok
        assert any("not operationally authorized" in e for e in result.errors)

    def test_5_merge_alone_is_insufficient(self):
        """Authorization is read from canonical bytes, which no merge event flips."""
        data = yaml.safe_load(
            (REPO_ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )
        assert data["stage_1_executability"]["executable"] is False
        assert "MERGE" in data["stage_1_executability"][
            "operational_authorization_requires_all_of"
        ]
        assert len(data["stage_1_executability"]["operational_authorization_requires_all_of"]) == 6

    def test_6_all_six_gates_still_required(self):
        assert len(PREREG.STAGE_1_EFFECTIVITY_GATES) == 6
        _, reason = PREREG.stage_1_operational_authorization_is_effective()
        for gate in PREREG.STAGE_1_EFFECTIVITY_GATES:
            assert gate in reason


# =============================================================================================
# Review 4946154405 — MAJOR 1: singular successor current state
# =============================================================================================
class TestSingularSuccessorState:
    @pytest.fixture
    def prereg(self):
        return yaml.safe_load(
            (REPO_ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )

    def test_7_frozen_provenance_is_structurally_satisfied(self, prereg):
        frozen = prereg["frozen_provenance_requirements"]
        assert frozen["structurally_satisfied"] is True

    def test_8_frozen_provenance_is_not_operationally_usable(self, prereg):
        assert prereg["frozen_provenance_requirements"]["operationally_usable"] is False

    def test_8b_ambiguous_single_flag_cannot_return(self, prereg):
        assert "currently_satisfiable" not in prereg["frozen_provenance_requirements"]
        prereg["frozen_provenance_requirements"]["currently_satisfiable"] = False
        result = PREREG.validate(prereg)
        assert not result.ok
        assert any("currently_satisfiable" in e for e in result.errors)

    def test_8c_claiming_operational_usability_rejected(self, prereg):
        prereg["frozen_provenance_requirements"]["operationally_usable"] = True
        assert not PREREG.validate(prereg).ok

    def test_9_no_current_state_claims_no_universe_exists(self, prereg):
        """The predecessor claim survives only under an explicitly historical key."""
        frozen = prereg["frozen_provenance_requirements"]
        historical = frozen["predecessor_currently_satisfiable_note_xasset_0027"]
        assert "no construction universe existed" in historical.lower()
        assert "HISTORICAL ONLY" in historical
        # No operative field repeats it.
        for key, value in frozen.items():
            if key.startswith("predecessor_"):
                continue
            if isinstance(value, str):
                assert "no construction universe exists" not in value.lower()

    def test_9b_lifecycle_note_no_longer_requires_a_future_closure_unit(self, prereg):
        note = prereg["lifecycle_effectivity"]["note"]
        assert "closed by its own future, separately" not in note
        assert "XASSET-0028" in note
        assert prereg["construction_universe_closure"]["status"] == "CLOSED"

    def test_10_protocol_predecessor_prose_is_labelled_historical(self):
        text = (REPO_ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md").read_text(
            encoding="utf-8"
        )
        assert "### 5.3 `XASSET-0027` PREDECESSOR STATE" in text
        assert "### 5.5 `XASSET-0027` PREDECESSOR STATE" in text
        assert "AMENDED BY `XASSET-0028`" in text
        # The old current-state heading is gone.
        assert "## 5. Population, provenance families, and why the construction universe is not closed" not in text


# =============================================================================================
# Review 4946154405 — MAJOR 2: full frozen result-identity binding
# =============================================================================================
class TestFrozenResultIdentityBinding:
    def test_adapter_exposes_every_duplicated_identity_field(self, universe):
        frozen = V.frozen_construction_universe()
        for field in (
            "cell_id",
            "sleeve",
            "bound",
            "driver_class",
            "family_id",
            "route",
            "num_0001_class",
            "governing_authority_refs",
            "source_architecture",
            "hypothetical_source_requirements",
        ):
            assert field in frozen[universe[0]["construction_id"]]

    @pytest.mark.parametrize(
        "field,bad",
        [
            ("cell_id", "crypto::UPPER::recovery"),
            ("sleeve", "crypto"),
            ("bound", "UPPER"),
            ("driver_class", "recovery"),
            ("family_id", "R2_C2"),
            ("route", "R2"),
            ("num_0001_class", 2),
            ("governing_authority_refs", ["INVENTED-0001"]),
        ],
    )
    def test_11_to_18_mutating_any_duplicated_identity_field_is_rejected(
        self, universe, field, bad
    ):
        """A valid construction_id must not license a relabelled row."""
        frozen = V.frozen_construction_universe()
        row = _result_row(universe[0]["construction_id"], universe[0])
        row[field] = bad
        errs = _run_stage1(row, frozen)
        assert any(field in e and "frozen construction identity" in e for e in errs), errs

    def test_19_source_architecture_mutation_rejected(self, universe):
        frozen = V.frozen_construction_universe()
        row = _result_row(universe[0]["construction_id"], universe[0])
        row["source_architecture"] = "EXISTING_SOURCE_ARCHITECTURE"
        assert any("frozen" in e for e in _run_stage1(row, frozen))

    def test_20_hypothetical_requirement_mutation_rejected(self, universe):
        frozen = V.frozen_construction_universe()
        row = _result_row(universe[0]["construction_id"], universe[0])
        row["hypothetical_source_requirements"] = "whatever the executor prefers"
        assert any(
            "hypothetical_source_requirements" in e for e in _run_stage1(row, frozen)
        )

    def test_21_cell_rollup_cannot_be_altered_by_row_mislabelling(self, universe):
        """A row may not relabel its cell, so roll-up ranges over the registered cell."""
        frozen = V.frozen_construction_universe()
        row = _result_row(universe[0]["construction_id"], universe[0])
        registered_cell = frozen[universe[0]["construction_id"]]["cell_id"]
        row["cell_id"] = "crypto::UPPER::recovery"
        errs = _run_stage1(row, frozen)
        assert any("cell_id" in e for e in errs)
        assert registered_cell != "crypto::UPPER::recovery"

    def test_faithful_row_passes_identity_binding(self, universe):
        frozen = V.frozen_construction_universe()
        row = _result_row(universe[0]["construction_id"], universe[0])
        errs = _run_stage1(row, frozen)
        assert not [e for e in errs if "frozen construction identity" in e], errs
