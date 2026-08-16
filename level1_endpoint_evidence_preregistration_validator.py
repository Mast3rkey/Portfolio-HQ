"""Structural validator for the ENDPOINT-0001 Level-1 endpoint-evidence pre-registration.

Authorized by governance/decisions/XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md

Read-only and mechanical. This module validates the closed structure, exact identities, derived
arithmetic, gate sequence, vocabularies, zero-parameter declaration, firewall completeness, and hash
conventions of the ENDPOINT-0001 pre-registration and protocol.

It cannot acquire data, execute the study, evaluate a cell, state an endpoint, or admit evidence.

Deliberate non-scope, recorded so the boundary is not blurred later: this module is NOT an
XASSET-0024 SS-J.1-J.12 endpoint-admission validator. No such production validator exists anywhere in
this repository, and building one is a separately authorized successor, not part of this filing.

Zero import coupling with allocate.py and margin_state.py in either direction.
"""

from __future__ import annotations

import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parent
PREREG_PATH = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"
PROTOCOL_PATH = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
DECISION_PATH = (
    ROOT
    / "governance/decisions"
    / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
)

STUDY_ID = "ENDPOINT-0001"
HASH_VERSION = "ENDPOINT-0001-PREREG-V1"

TOP_KEYS = (
    "schema_version",
    "study_id",
    "identifier_note",
    "authority",
    "research_question",
    "sleeves",
    "bounds",
    "driver_classes",
    "driver_class_scope",
    "stages",
    "cell_definition",
    "trial_inventory",
    "roll_up_units",
    "gate_sequence",
    "open_reading_handling",
    "result_vocabulary",
    "prohibited_inputs",
    "risk_lane_boundary",
    "representation",
    "consequential_parameter_registry",
    "data_and_sources",
    "provenance_manifest",
    "execution",
    "result_schema",
    "result_status_of_stage_1_output",
    "mandatory_abstention_conditions",
    "abstention_is_a_complete_outcome",
    "prohibited_scope",
    "protected_paths",
    "hash_version",
)

SLEEVES = ("equity", "fund_broad_market", "fund_gld_defensive", "crypto")
BOUNDS = ("LOWER", "UPPER")
DRIVER_CLASSES = (
    "portfolio_function",
    "valuation_opportunity_cost",
    "downside_path_risk",
    "recovery",
    "diversification_cobehavior",
    "sleeve_deployability",
)

GATE_IDS = (
    "G1_DRIVER_SUBJECT_MATTER",
    "G2_MAGNITUDE_INTRINSICALITY",
    "G3_NORMALIZATION",
    "G4_ORIGIN",
    "G5_CONSTRAINT_SHAPE",
    "G6_ROUTE_COMPLIANCE",
    "G7_DISCRETION_AND_PROVENANCE",
    "G8_UNIQUENESS",
    "G9_REPRESENTATION",
    "G10_PAIR_INDEPENDENCE",
    "G11_EXACTNESS_AND_DETERMINISM",
    "G12_RECONCILIATION_FEASIBILITY",
    "G13_SNAPSHOT_ADMISSIBILITY_PATH",
)
GATE_KEYS = (
    "gate_id",
    "gate_index",
    "question",
    "controlling_authority",
    "failure_disposition",
)
FAILURE_DISPOSITIONS = ("BLOCKED_CATEGORICALLY", "BLOCKED_PENDING_SEPARATE_PREREQUISITE")
PREREQUISITE_GATES = ("G9_REPRESENTATION", "G13_SNAPSHOT_ADMISSIBILITY_PATH")

CELL_OUTCOMES = (
    "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED",
    "BLOCKED_CATEGORICALLY",
    "BLOCKED_PENDING_SEPARATE_PREREQUISITE",
    "UNABLE_TO_DETERMINE",
)
ROLL_UP_OUTCOMES = (
    "CANDIDATE_CONSTRUCTION_IDENTIFIED",
    "PREREQUISITE_REQUIRED",
    "NO_CONSTRUCTIBLE_CANDIDATE",
    "UNABLE_TO_DETERMINE",
)
ROLL_UP_PRECEDENCE = (
    ("ANY_CELL_CONSTRUCTIBLE_CANDIDATE_IDENTIFIED", "CANDIDATE_CONSTRUCTION_IDENTIFIED"),
    ("ANY_CELL_BLOCKED_PENDING_SEPARATE_PREREQUISITE", "PREREQUISITE_REQUIRED"),
    ("ANY_CELL_UNABLE_TO_DETERMINE", "UNABLE_TO_DETERMINE"),
    ("ALL_CELLS_BLOCKED_CATEGORICALLY", "NO_CONSTRUCTIBLE_CANDIDATE"),
)

POINT_RANGE_VALUES = (
    "WOULD_SUPPORT_RANGE_ENDPOINT",
    "WOULD_SUPPORT_POINT_ENDPOINT",
    "WOULD_SUPPORT_NEITHER",
)

PARAMETER_RECORD_KEYS = (
    "parameter_id",
    "value",
    "unit",
    "num_0001_class",
    "contextual_class",
    "selection_basis",
    "evidence_status",
    "supporting_evidence",
    "canonical_source",
    "duplicate_locations",
    "fallback_locations",
    "hardcoded_or_config_editable",
    "binding_status",
    "binding_scope",
    "valid_for_study_id",
    "lapse_condition",
    "reuse_rule",
    "calibrated",
    "evidence_bounded",
)

DERIVED_IDENTITIES = {
    "SLEEVE_COUNT": 4,
    "BOUND_COUNT": 2,
    "DRIVER_CLASS_COUNT": 6,
    "CELL_CEILING": 48,
    "ROLL_UP_UNIT_COUNT": 8,
    "GATE_COUNT": 13,
}

REQUIRED_ABSTENTION_CONDITIONS = (
    "REPRESENTATION_PATH_1_FAILS_AND_NO_ACCEPTED_RULE_EXISTS",
    "ANY_REQUIRED_INPUT_IS_BARRED_BY_ORIGIN",
    "ANY_STEP_COULD_HAVE_BEEN_CHOSEN_DIFFERENTLY",
    "A_SECOND_LAWFUL_VALUE_EXISTS_FOR_THE_SAME_QUANTITY",
    "AN_UNRESOLVED_PAIR_WOULD_BE_CONSUMED_AS_AN_INPUT",
    "THE_PREFERENCE_ONLY_READING_OF_SECTION_E_1_IS_ESTABLISHED",
    "A_CANDIDATE_WOULD_REQUIRE_INVENTING_A_LEVEL_1_AGGREGATION_OR_REPRESENTATION_RULE",
)

REQUIRED_PROHIBITED_SCOPE = (
    "ENDPOINT_CREATION",
    "LOWER_OR_UPPER_BOUND_VALUE",
    "SLEEVE_SELECTION_PREFERENCE_RANKING_OR_SEQUENCING",
    "PORTFOLIO_RECONCILIATION_OR_SUM_TARGETING",
    "OPTIMIZER_WEIGHT_GRID_OR_SWEEP",
    "COMPOSITE_SCORE_OR_INDEX",
    "RESIDUAL_REDISTRIBUTION",
    "SNAPSHOT_EXTENSION_OR_REPLACEMENT",
    "EVIDENCE_ADMISSION",
    "APPLICATION_AUTHORITY_OR_REGISTRY_POPULATION",
    "REPRESENTATION_RULE_ADOPTION",
    "METHODOLOGY_AMENDMENT",
    "RISK_PARAMETER_REUSE",
    "STAGE_2_EXECUTION",
)

REQUIRED_PROTECTED_PATHS = (
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
    "allocate.py",
    "margin_state.py",
    "levels.py",
    "/private/tmp/phq-risk0001-results",
)

REQUIRED_FORBIDDEN_RESULT_CONTENT = (
    "ANY_NUMERIC_SLEEVE_SHARE",
    "ANY_LOWER_OR_UPPER_BOUND_VALUE",
    "ANY_PERCENTAGE_OF_THE_NORMALIZED_UNIT",
    "ANY_TARGET_WEIGHT_OR_ALLOCATION",
    "ANY_COMPOSITE_SCORE_RANK_OR_INDEX",
    "ANY_SLEEVE_PREFERENCE_RANKING_OR_SEQUENCING",
    "ANY_PORTFOLIO_RECONCILIATION_OR_SUM_TO_WHOLE",
)

OPEN_READING_FIELDS = (
    "g2_outcome_under_subject_matter_reading",
    "g2_outcome_under_preference_only_reading",
    "g2_outcome_is_reading_dependent",
)

# Adversarial scan. Barred historical Level-1 values named by XASSET-0020 SS-M and XASSET-0025 SS-F.
# Written as digit-separated patterns so this module does not itself embed a usable anchor literal.
BARRED_NUMERAL_PATTERNS = (
    r"18\.67",
    r"14\.67",
    r"16\.67",
    r"33\.32",
    r"66\.68",
)

# An endpoint-shaped value is a bare percentage-like scalar presented as a share. Any such token in a
# preregistration that is required to contain no endpoint is a defect.
ENDPOINT_SHAPED_TOKEN = re.compile(
    r"(?<![\w.])(?:100(?:\.0+)?|\d{1,2}(?:\.\d+)?)\s*(?:%|percent\b|pct\b)", re.IGNORECASE
)

MIRROR_BLOCK_RE = re.compile(
    r"<!-- ENDPOINT-0001-PROTOCOL-MIRROR-V1\n(?P<body>.*?)\n-->", re.DOTALL
)
HASH_BLOCK_RE = re.compile(r"<!-- XASSET-0027-HASH-PINS-V1\n(?P<body>.*?)\n-->", re.DOTALL)


@dataclass
class ValidationResult:
    """Outcome of a validation pass."""

    ok: bool
    errors: tuple[str, ...] = field(default_factory=tuple)

    def __bool__(self) -> bool:  # pragma: no cover - trivial
        return self.ok


def sha256_file(path: Path) -> str:
    """Return the SHA-256 of a file's raw bytes exactly as committed."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _keys(value: Any, expected: Sequence[str], where: str, errors: list[str]) -> bool:
    if not isinstance(value, Mapping):
        errors.append(f"{where}: expected a mapping, got {type(value).__name__}")
        return False
    actual = tuple(value)
    if actual != tuple(expected):
        missing = [k for k in expected if k not in actual]
        extra = [k for k in actual if k not in expected]
        if missing:
            errors.append(f"{where}: missing key(s) {missing}")
        if extra:
            errors.append(f"{where}: unexpected key(s) {extra}")
        if not missing and not extra:
            errors.append(f"{where}: key order differs from the closed schema")
        return False
    return True


def _exact(actual: Any, expected: Any, where: str, errors: list[str]) -> None:
    if actual != expected:
        errors.append(f"{where}: expected {expected!r}, got {actual!r}")


def _true(value: Any, where: str, errors: list[str]) -> None:
    if value is not True:
        errors.append(f"{where}: expected boolean True, got {value!r}")


def _false(value: Any, where: str, errors: list[str]) -> None:
    if value is not False:
        errors.append(f"{where}: expected boolean False, got {value!r}")


def _contains_all(actual: Any, required: Sequence[str], where: str, errors: list[str]) -> None:
    if not isinstance(actual, list):
        errors.append(f"{where}: expected a list, got {type(actual).__name__}")
        return
    for item in required:
        if item not in actual:
            errors.append(f"{where}: required entry {item!r} is absent")


def _validate_identity(data: Mapping[str, Any], errors: list[str]) -> None:
    _exact(data.get("study_id"), STUDY_ID, "study_id", errors)
    _exact(data.get("hash_version"), HASH_VERSION, "hash_version", errors)
    _exact(list(data.get("sleeves") or []), list(SLEEVES), "sleeves", errors)
    _exact(list(data.get("bounds") or []), list(BOUNDS), "bounds", errors)
    _exact(
        list(data.get("driver_classes") or []), list(DRIVER_CLASSES), "driver_classes", errors
    )

    note = data.get("identifier_note")
    if isinstance(note, Mapping):
        statement = str(note.get("statement", ""))
        if "not a governance decision prefix" not in statement:
            errors.append(
                "identifier_note.statement: must record that ENDPOINT-0001 is not a decision prefix"
            )
    else:
        errors.append("identifier_note: expected a mapping")


def _validate_authority(data: Mapping[str, Any], errors: list[str]) -> None:
    auth = data.get("authority")
    if not isinstance(auth, Mapping):
        errors.append("authority: expected a mapping")
        return
    _exact(auth.get("authorizing_decision"), "XASSET-0027", "authority.authorizing_decision", errors)
    _exact(auth.get("lane"), "OPS-0009_LANE_G", "authority.lane", errors)
    _exact(
        auth.get("program_shape"),
        "ALL_FOUR_SLEEVE_SELECTION_FREE_PROGRAM",
        "authority.program_shape",
        errors,
    )
    _true(auth.get("authority_constituted_by_same_decision"), "authority.authority_constituted_by_same_decision", errors)
    _false(auth.get("authority_exercised_by_this_program"), "authority.authority_exercised_by_this_program", errors)


def _validate_stages(data: Mapping[str, Any], errors: list[str]) -> None:
    stages = data.get("stages")
    if not isinstance(stages, Mapping):
        errors.append("stages: expected a mapping")
        return
    s1 = stages.get("stage_1")
    s2 = stages.get("stage_2")
    if isinstance(s1, Mapping):
        _true(s1.get("authorized_by_xasset_0027"), "stages.stage_1.authorized_by_xasset_0027", errors)
        _false(s1.get("acquires_data"), "stages.stage_1.acquires_data", errors)
        _false(s1.get("fits_or_estimates_anything"), "stages.stage_1.fits_or_estimates_anything", errors)
        _false(s1.get("produces_endpoint"), "stages.stage_1.produces_endpoint", errors)
        _false(s1.get("produces_admissible_evidence"), "stages.stage_1.produces_admissible_evidence", errors)
    else:
        errors.append("stages.stage_1: expected a mapping")
    if isinstance(s2, Mapping):
        _false(s2.get("authorized_by_xasset_0027"), "stages.stage_2.authorized_by_xasset_0027", errors)
        _exact(
            s2.get("authorization_requirement"),
            "SEPARATE_LATER_EXPLICITLY_ACCEPTED_GOVERNANCE_DECISION",
            "stages.stage_2.authorization_requirement",
            errors,
        )
    else:
        errors.append("stages.stage_2: expected a mapping")


def _validate_gates(data: Mapping[str, Any], errors: list[str]) -> None:
    seq = data.get("gate_sequence")
    if not isinstance(seq, Mapping):
        errors.append("gate_sequence: expected a mapping")
        return
    _true(
        seq.get("record_first_failing_gate_only"),
        "gate_sequence.record_first_failing_gate_only",
        errors,
    )
    _true(
        seq.get("gates_may_not_be_added_removed_reordered_or_reinterpreted_after_any_outcome_observed"),
        "gate_sequence.gates_may_not_be_added_removed_reordered_or_reinterpreted_after_any_outcome_observed",
        errors,
    )
    gates = seq.get("gates")
    if not isinstance(gates, list):
        errors.append("gate_sequence.gates: expected a list")
        return
    if len(gates) != len(GATE_IDS):
        errors.append(f"gate_sequence.gates: expected {len(GATE_IDS)} gates, got {len(gates)}")
        return
    for position, gate in enumerate(gates):
        where = f"gate_sequence.gates[{position}]"
        if not _keys(gate, GATE_KEYS, where, errors):
            continue
        _exact(gate.get("gate_id"), GATE_IDS[position], f"{where}.gate_id", errors)
        _exact(gate.get("gate_index"), position + 1, f"{where}.gate_index", errors)
        disposition = gate.get("failure_disposition")
        if disposition not in FAILURE_DISPOSITIONS:
            errors.append(f"{where}.failure_disposition: {disposition!r} is outside the closed set")
        expected = (
            "BLOCKED_PENDING_SEPARATE_PREREQUISITE"
            if gate.get("gate_id") in PREREQUISITE_GATES
            else "BLOCKED_CATEGORICALLY"
        )
        _exact(disposition, expected, f"{where}.failure_disposition", errors)
        if not str(gate.get("question", "")).strip():
            errors.append(f"{where}.question: must be non-empty")
        if not str(gate.get("controlling_authority", "")).strip():
            errors.append(f"{where}.controlling_authority: must be non-empty")


def _validate_counts(data: Mapping[str, Any], errors: list[str]) -> None:
    inventory = data.get("trial_inventory")
    if isinstance(inventory, Mapping):
        _exact(inventory.get("derived_ceiling_cells"), 48, "trial_inventory.derived_ceiling_cells", errors)
        _exact(inventory.get("reserve_cells"), 0, "trial_inventory.reserve_cells", errors)
        _exact(
            inventory.get("result_aware_cells"), "PROHIBITED", "trial_inventory.result_aware_cells", errors
        )
        _true(inventory.get("every_cell_must_be_recorded"), "trial_inventory.every_cell_must_be_recorded", errors)
        _true(
            inventory.get("cell_may_not_be_dropped_or_omitted"),
            "trial_inventory.cell_may_not_be_dropped_or_omitted",
            errors,
        )
    else:
        errors.append("trial_inventory: expected a mapping")

    roll_up = data.get("roll_up_units")
    if isinstance(roll_up, Mapping):
        _exact(roll_up.get("derived_count"), 8, "roll_up_units.derived_count", errors)
        _true(roll_up.get("computed_only_from_own_six_cells"), "roll_up_units.computed_only_from_own_six_cells", errors)
        _exact(roll_up.get("cross_bound_reference"), "PROHIBITED", "roll_up_units.cross_bound_reference", errors)
        _exact(roll_up.get("cross_sleeve_reference"), "PROHIBITED", "roll_up_units.cross_sleeve_reference", errors)
    else:
        errors.append("roll_up_units: expected a mapping")

    # The derived ceiling must equal the product of the closed populations, not merely assert a number.
    product = len(SLEEVES) * len(BOUNDS) * len(DRIVER_CLASSES)
    if product != 48:
        errors.append(f"derived arithmetic: closed populations imply {product} cells, not 48")


def _validate_registry(data: Mapping[str, Any], errors: list[str]) -> None:
    registry = data.get("consequential_parameter_registry")
    if not isinstance(registry, Mapping):
        errors.append("consequential_parameter_registry: expected a mapping")
        return
    _exact(
        list(registry.get("record_keys") or []),
        list(PARAMETER_RECORD_KEYS),
        "consequential_parameter_registry.record_keys",
        errors,
    )
    parameters = registry.get("parameters")
    if not isinstance(parameters, list):
        errors.append("consequential_parameter_registry.parameters: expected a list")
    elif parameters:
        errors.append(
            "consequential_parameter_registry.parameters: Stage 1 declares zero consequential "
            f"numeric parameters, but {len(parameters)} are registered; introducing one requires a "
            "separately accepted amendment with new hash pins"
        )

    declaration = registry.get("zero_parameter_declaration")
    if isinstance(declaration, Mapping):
        _true(
            declaration.get("stage_1_introduces_zero_consequential_numeric_parameters"),
            "consequential_parameter_registry.zero_parameter_declaration"
            ".stage_1_introduces_zero_consequential_numeric_parameters",
            errors,
        )
    else:
        errors.append("consequential_parameter_registry.zero_parameter_declaration: expected a mapping")

    identities = registry.get("derived_identities")
    if not isinstance(identities, Mapping):
        errors.append("consequential_parameter_registry.derived_identities: expected a mapping")
        return
    rows = identities.get("identities")
    if not isinstance(rows, list):
        errors.append("consequential_parameter_registry.derived_identities.identities: expected a list")
        return
    seen: dict[str, Any] = {}
    for row in rows:
        if not isinstance(row, Mapping):
            errors.append("derived_identities.identities[]: expected a mapping")
            continue
        seen[str(row.get("identity_id"))] = row.get("value")
        if row.get("contextual_class") != "CALCULATED_OUTPUT":
            errors.append(
                f"derived_identities[{row.get('identity_id')!r}].contextual_class: derived counts "
                "must be CALCULATED_OUTPUT, never a NUM-0001 parameter class"
            )
    for identity_id, expected in DERIVED_IDENTITIES.items():
        if identity_id not in seen:
            errors.append(f"derived_identities: {identity_id} is absent")
        else:
            _exact(seen[identity_id], expected, f"derived_identities[{identity_id}].value", errors)


def _validate_open_reading(data: Mapping[str, Any], errors: list[str]) -> None:
    handling = data.get("open_reading_handling")
    if not isinstance(handling, Mapping):
        errors.append("open_reading_handling: expected a mapping")
        return
    _false(handling.get("resolved_by_this_program"), "open_reading_handling.resolved_by_this_program", errors)
    _false(handling.get("relied_upon_by_this_program"), "open_reading_handling.relied_upon_by_this_program", errors)
    _exact(
        handling.get("handling"),
        "EVALUATE_G2_UNDER_BOTH_READINGS_AND_RECORD_BOTH",
        "open_reading_handling.handling",
        errors,
    )
    _exact(
        handling.get("consequence_if_preference_only_reading_later_established"),
        "ALL_CELLS_ABSTAIN",
        "open_reading_handling.consequence_if_preference_only_reading_later_established",
        errors,
    )
    _contains_all(
        handling.get("required_recorded_fields"),
        OPEN_READING_FIELDS,
        "open_reading_handling.required_recorded_fields",
        errors,
    )


def _validate_vocabulary(data: Mapping[str, Any], errors: list[str]) -> None:
    vocab = data.get("result_vocabulary")
    if not isinstance(vocab, Mapping):
        errors.append("result_vocabulary: expected a mapping")
        return
    _exact(list(vocab.get("cell_outcomes") or []), list(CELL_OUTCOMES), "result_vocabulary.cell_outcomes", errors)
    _exact(
        list(vocab.get("roll_up_outcomes") or []),
        list(ROLL_UP_OUTCOMES),
        "result_vocabulary.roll_up_outcomes",
        errors,
    )
    _true(vocab.get("roll_up_is_not_a_score"), "result_vocabulary.roll_up_is_not_a_score", errors)
    _exact(
        vocab.get("roll_up_mechanism"),
        "FIXED_PRECEDENCE_EXISTENCE_TEST",
        "result_vocabulary.roll_up_mechanism",
        errors,
    )

    precedence = vocab.get("roll_up_precedence")
    if not isinstance(precedence, list):
        errors.append("result_vocabulary.roll_up_precedence: expected a list")
    elif len(precedence) != len(ROLL_UP_PRECEDENCE):
        errors.append(
            f"result_vocabulary.roll_up_precedence: expected {len(ROLL_UP_PRECEDENCE)} rules, "
            f"got {len(precedence)}"
        )
    else:
        for position, rule in enumerate(precedence):
            where = f"result_vocabulary.roll_up_precedence[{position}]"
            if not isinstance(rule, Mapping):
                errors.append(f"{where}: expected a mapping")
                continue
            expected_condition, expected_outcome = ROLL_UP_PRECEDENCE[position]
            _exact(rule.get("condition"), expected_condition, f"{where}.condition", errors)
            _exact(rule.get("outcome"), expected_outcome, f"{where}.outcome", errors)

    support = vocab.get("point_or_range_support")
    if isinstance(support, Mapping):
        _exact(
            list(support.get("values") or []),
            list(POINT_RANGE_VALUES),
            "result_vocabulary.point_or_range_support.values",
            errors,
        )
        _exact(
            support.get("range_first_posture"),
            "CARRIED_FORWARD_UNCHANGED",
            "result_vocabulary.point_or_range_support.range_first_posture",
            errors,
        )
    else:
        errors.append("result_vocabulary.point_or_range_support: expected a mapping")


def _validate_firewall(data: Mapping[str, Any], errors: list[str]) -> None:
    firewall = data.get("prohibited_inputs")
    if not isinstance(firewall, Mapping):
        errors.append("prohibited_inputs: expected a mapping")
        return
    _true(
        firewall.get(
            "may_not_be_used_anchored_to_initialized_from_centered_on_sanity_checked_against_or_reverse_engineered_toward"
        ),
        "prohibited_inputs.may_not_be_used_anchored_to_...",
        errors,
    )
    _true(
        firewall.get("literal_scan_is_a_floor_not_the_boundary"),
        "prohibited_inputs.literal_scan_is_a_floor_not_the_boundary",
        errors,
    )
    _contains_all(
        firewall.get("barred_constructions"),
        ("EQUAL_DIVISION_INCLUDING_FRESHLY_COMPUTED", "RESIDUAL_OR_COMPLEMENT_PLUG", "MIDPOINT"),
        "prohibited_inputs.barred_constructions",
        errors,
    )
    _contains_all(
        firewall.get("barred_risk_reuse"),
        ("ALL_TWENTY_LAPSED_CONSEQUENTIAL_PARAMETERS", "GOLD_PARITY_ADMISSION_THRESHOLDS"),
        "prohibited_inputs.barred_risk_reuse",
        errors,
    )

    risk = data.get("risk_lane_boundary")
    if isinstance(risk, Mapping):
        _exact(risk.get("retry"), "PROHIBITED", "risk_lane_boundary.retry", errors)
        _exact(risk.get("attempt_3"), "DOES_NOT_EXIST", "risk_lane_boundary.attempt_3", errors)
        _exact(
            risk.get("protected_result_path"),
            "/private/tmp/phq-risk0001-results",
            "risk_lane_boundary.protected_result_path",
            errors,
        )
    else:
        errors.append("risk_lane_boundary: expected a mapping")


def _validate_representation(data: Mapping[str, Any], errors: list[str]) -> None:
    rep = data.get("representation")
    if not isinstance(rep, Mapping):
        errors.append("representation: expected a mapping")
        return
    _exact(
        rep.get("disposition"),
        "SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED",
        "representation.disposition",
        errors,
    )
    _true(rep.get("self_contained_path_preserved"), "representation.self_contained_path_preserved", errors)
    _false(rep.get("rule_created_by_this_program"), "representation.rule_created_by_this_program", errors)
    _false(
        rep.get("cm_14_through_cm_17_membership_designated"),
        "representation.cm_14_through_cm_17_membership_designated",
        errors,
    )


def _validate_execution(data: Mapping[str, Any], errors: list[str]) -> None:
    execution = data.get("execution")
    if not isinstance(execution, Mapping):
        errors.append("execution: expected a mapping")
        return

    stopping = execution.get("stopping_rules")
    if isinstance(stopping, Mapping):
        _exact(
            stopping.get("terminates_when"),
            "ALL_48_CELLS_CARRY_A_RECORDED_OUTCOME",
            "execution.stopping_rules.terminates_when",
            errors,
        )
        _exact(
            stopping.get("early_stop_on_positive_finding"),
            "PROHIBITED",
            "execution.stopping_rules.early_stop_on_positive_finding",
            errors,
        )
    else:
        errors.append("execution.stopping_rules: expected a mapping")

    rerun = execution.get("rerun_rule")
    if isinstance(rerun, Mapping):
        _exact(rerun.get("after_outcomes_observed"), "PROHIBITED", "execution.rerun_rule.after_outcomes_observed", errors)
        _exact(
            rerun.get("discovered_defect_automatic_rerun"),
            "PROHIBITED",
            "execution.rerun_rule.discovered_defect_automatic_rerun",
            errors,
        )
    else:
        errors.append("execution.rerun_rule: expected a mapping")

    mining = execution.get("history_mining_controls")
    if isinstance(mining, Mapping):
        for key in ("gates_frozen_before_evaluation", "cells_frozen_before_evaluation", "vocabulary_frozen_before_evaluation"):
            _true(mining.get(key), f"execution.history_mining_controls.{key}", errors)
        _exact(
            mining.get("outcome_aware_gate_change"),
            "PROHIBITED",
            "execution.history_mining_controls.outcome_aware_gate_change",
            errors,
        )
    else:
        errors.append("execution.history_mining_controls: expected a mapping")

    for key in ("out_of_sample_discipline", "neighboring_parameter_robustness"):
        block = execution.get(key)
        if isinstance(block, Mapping):
            _false(block.get("applicable_to_stage_1"), f"execution.{key}.applicable_to_stage_1", errors)
            if not str(block.get("reason", "")).strip():
                errors.append(f"execution.{key}.reason: a non-applicability claim must state its reason")
        else:
            errors.append(f"execution.{key}: expected a mapping")

    negative = execution.get("negative_result_preservation")
    if isinstance(negative, Mapping):
        _true(
            negative.get("all_cell_outcomes_recorded_regardless_of_direction"),
            "execution.negative_result_preservation.all_cell_outcomes_recorded_regardless_of_direction",
            errors,
        )
        _true(negative.get("null_is_a_complete_outcome"), "execution.negative_result_preservation.null_is_a_complete_outcome", errors)
    else:
        errors.append("execution.negative_result_preservation: expected a mapping")


def _validate_result_boundary(data: Mapping[str, Any], errors: list[str]) -> None:
    schema = data.get("result_schema")
    if isinstance(schema, Mapping):
        _false(schema.get("results_path_created_by_this_filing"), "result_schema.results_path_created_by_this_filing", errors)
        _contains_all(
            schema.get("forbidden_result_content"),
            REQUIRED_FORBIDDEN_RESULT_CONTENT,
            "result_schema.forbidden_result_content",
            errors,
        )
        _contains_all(
            schema.get("cell_result_keys"),
            OPEN_READING_FIELDS + ("cell_id", "outcome", "first_failing_gate_id"),
            "result_schema.cell_result_keys",
            errors,
        )
    else:
        errors.append("result_schema: expected a mapping")

    status = data.get("result_status_of_stage_1_output")
    if isinstance(status, Mapping):
        for key in (
            "is_a_driver_source",
            "is_admissible_endpoint_supporting_evidence",
            "may_be_cited_as_endpoint_supporting_evidence",
            "may_enter_a_snapshot_as_a_driver",
        ):
            _false(status.get(key), f"result_status_of_stage_1_output.{key}", errors)
    else:
        errors.append("result_status_of_stage_1_output: expected a mapping")


def _validate_abstention_and_scope(data: Mapping[str, Any], errors: list[str]) -> None:
    conditions = data.get("mandatory_abstention_conditions")
    if not isinstance(conditions, list):
        errors.append("mandatory_abstention_conditions: expected a list")
    else:
        present = {str(row.get("condition")) for row in conditions if isinstance(row, Mapping)}
        for required in REQUIRED_ABSTENTION_CONDITIONS:
            if required not in present:
                errors.append(f"mandatory_abstention_conditions: {required} is absent")
        for row in conditions:
            if isinstance(row, Mapping) and not str(row.get("authority", "")).strip():
                errors.append(
                    f"mandatory_abstention_conditions[{row.get('condition')!r}].authority: must be non-empty"
                )
    _true(data.get("abstention_is_a_complete_outcome"), "abstention_is_a_complete_outcome", errors)
    _contains_all(data.get("prohibited_scope"), REQUIRED_PROHIBITED_SCOPE, "prohibited_scope", errors)
    _contains_all(data.get("protected_paths"), REQUIRED_PROTECTED_PATHS, "protected_paths", errors)


def scan_for_barred_content(text: str, where: str) -> tuple[str, ...]:
    """Return adversarial-scan findings for barred numerals or endpoint-shaped tokens."""
    findings: list[str] = []
    for pattern in BARRED_NUMERAL_PATTERNS:
        if re.search(pattern, text):
            findings.append(
                f"{where}: a barred historical Level-1 value matching /{pattern}/ appears; "
                "barred values are referenced by name, never reproduced"
            )
    for match in ENDPOINT_SHAPED_TOKEN.finditer(text):
        findings.append(
            f"{where}: endpoint-shaped token {match.group(0)!r} appears; this document must contain "
            "no sleeve share, bound value, or percentage of the normalized unit"
        )
    return tuple(findings)


def validate(data: Mapping[str, Any]) -> ValidationResult:
    """Validate a parsed pre-registration mapping against the closed schema."""
    errors: list[str] = []
    if not _keys(data, TOP_KEYS, "pre_registration", errors):
        return ValidationResult(False, tuple(errors))
    _validate_identity(data, errors)
    _validate_authority(data, errors)
    _validate_stages(data, errors)
    _validate_gates(data, errors)
    _validate_counts(data, errors)
    _validate_registry(data, errors)
    _validate_open_reading(data, errors)
    _validate_vocabulary(data, errors)
    _validate_firewall(data, errors)
    _validate_representation(data, errors)
    _validate_execution(data, errors)
    _validate_result_boundary(data, errors)
    _validate_abstention_and_scope(data, errors)
    return ValidationResult(not errors, tuple(errors))


def protocol_mirror_expected() -> dict[str, str]:
    """Return the mirror values the protocol must reproduce."""
    return {
        "study_id": STUDY_ID,
        "sleeve_count": str(len(SLEEVES)),
        "bound_count": str(len(BOUNDS)),
        "driver_class_count": str(len(DRIVER_CLASSES)),
        "cell_ceiling": str(DERIVED_IDENTITIES["CELL_CEILING"]),
        "roll_up_unit_count": str(DERIVED_IDENTITIES["ROLL_UP_UNIT_COUNT"]),
        "gate_count": str(len(GATE_IDS)),
        "reserve_cells": "0",
        "consequential_parameter_count": "0",
        "stage_2_authorized": "false",
        "hash_version": HASH_VERSION,
    }


def extract_block(text: str, pattern: re.Pattern[str]) -> dict[str, str] | None:
    """Parse a key: value comment block, returning None when absent."""
    match = pattern.search(text)
    if match is None:
        return None
    body: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        body[key.strip()] = value.strip()
    return body


def validate_protocol_mirror(protocol_text: str) -> ValidationResult:
    """Validate the protocol's mirror block against the canonical identities."""
    errors: list[str] = []
    mirror = extract_block(protocol_text, MIRROR_BLOCK_RE)
    if mirror is None:
        return ValidationResult(False, ("PROTOCOL_V1.md: ENDPOINT-0001-PROTOCOL-MIRROR-V1 block absent",))
    expected = protocol_mirror_expected()
    for key, want in expected.items():
        got = mirror.get(key)
        if got is None:
            errors.append(f"protocol mirror: {key} is absent")
        elif got != want:
            errors.append(f"protocol mirror: {key} expected {want!r}, got {got!r}")
    for key in mirror:
        if key not in expected:
            errors.append(f"protocol mirror: unexpected key {key!r}")
    return ValidationResult(not errors, tuple(errors))


def validate_charter_hash_pins(
    decision_text: str, prereg_path: Path = PREREG_PATH, protocol_path: Path = PROTOCOL_PATH
) -> ValidationResult:
    """Validate that the charter's pinned hashes match the canonical files as committed."""
    errors: list[str] = []
    pins = extract_block(decision_text, HASH_BLOCK_RE)
    if pins is None:
        return ValidationResult(False, ("XASSET-0027: XASSET-0027-HASH-PINS-V1 block absent",))
    expected_paths = {
        "protocol_path": "research/level1_endpoint_evidence/PROTOCOL_V1.md",
        "preregistration_path": "research/level1_endpoint_evidence/pre_registration.yaml",
    }
    for key, want in expected_paths.items():
        if pins.get(key) != want:
            errors.append(f"hash pins: {key} expected {want!r}, got {pins.get(key)!r}")
    for key, path in (("protocol_sha256", protocol_path), ("preregistration_sha256", prereg_path)):
        pinned = pins.get(key)
        if not pinned:
            errors.append(f"hash pins: {key} is absent")
            continue
        actual = sha256_file(path)
        if pinned != actual:
            errors.append(
                f"hash pins: {key} mismatch — charter pins {pinned}, file is {actual}; "
                "a mismatch voids execution authority"
            )
    return ValidationResult(not errors, tuple(errors))


def validate_file(path: Path = PREREG_PATH) -> ValidationResult:
    """Validate the pre-registration file, its adversarial scans, and its companion documents."""
    if not path.exists():
        return ValidationResult(False, (f"{path}: file not found",))
    raw = path.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:  # pragma: no cover - defensive
        return ValidationResult(False, (f"{path}: YAML parse failure: {exc}",))
    if not isinstance(data, dict):
        return ValidationResult(False, (f"{path}: expected a top-level mapping",))

    result = validate(data)
    errors = list(result.errors)
    errors.extend(scan_for_barred_content(raw, str(path.name)))

    if PROTOCOL_PATH.exists():
        protocol_text = PROTOCOL_PATH.read_text(encoding="utf-8")
        errors.extend(validate_protocol_mirror(protocol_text).errors)
        errors.extend(scan_for_barred_content(protocol_text, PROTOCOL_PATH.name))
    else:
        errors.append(f"{PROTOCOL_PATH}: file not found")

    if DECISION_PATH.exists():
        errors.extend(
            validate_charter_hash_pins(DECISION_PATH.read_text(encoding="utf-8")).errors
        )
    else:
        errors.append(f"{DECISION_PATH}: file not found")

    return ValidationResult(not errors, tuple(errors))


def main() -> int:  # pragma: no cover - CLI
    result = validate_file()
    if result.ok:
        print(f"level1_endpoint_evidence_preregistration_validator: OK ({STUDY_ID})")
        return 0
    print(f"level1_endpoint_evidence_preregistration_validator: {len(result.errors)} error(s)")
    for error in result.errors:
        print(f"  - {error}")
    return 1


if __name__ == "__main__":  # pragma: no cover - CLI
    sys.exit(main())
