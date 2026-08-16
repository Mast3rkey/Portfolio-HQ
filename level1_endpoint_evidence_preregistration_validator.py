"""Structural validator for the ENDPOINT-0001 Level-1 endpoint-evidence pre-registration.

Authorized by governance/decisions/XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md

Read-only and mechanical. This module validates the closed structure, exact identities, derived
arithmetic, construction-family closure, candidate-universe generation, gate sequence, disposition
rules, the XASSET-0024 SS-K.1 reading map, deferred-requirement handling, vocabularies, the
zero-parameter declaration, firewall completeness, and hash conventions of the ENDPOINT-0001
pre-registration and protocol.

It also supplies the pure, deterministic derivation functions the future Stage 1 execution must use
(candidate universe generation, G2 reading mapping, and candidate/cell/roll-up disposition), plus
validate_stage1_results(), which checks a Stage-1 results document against the frozen candidate
universe. Those functions make the determinism and exhaustiveness claims mechanically enforceable
rather than merely asserted.

It cannot acquire data, execute the study, decide a gate, state an endpoint, or admit evidence.
Deciding a gate outcome remains a human/analytical act performed under the charter; this module only
composes already-decided gate results into a disposition by a fixed rule.

Deliberate non-scope, recorded so the boundary is not blurred later: this module is NOT an
XASSET-0024 SS-J.1-J.12 endpoint-admission validator. No such production validator exists anywhere in
this repository, and building one is a separately authorized successor, not part of this filing. In
particular SS-J.12 is deferred and is not decided here.

Zero import coupling with allocate.py and margin_state.py in either direction.
"""

from __future__ import annotations

import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parent
PREREG_PATH = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"
PROTOCOL_PATH = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
DECISION_PATH = (
    ROOT
    / "governance/decisions"
    / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
)

SUCCESSOR_DECISION_PATH = (
    ROOT
    / "governance/decisions"
    / "XASSET-0028-concrete-construction-universe-closure-determination.md"
)

STUDY_ID = "ENDPOINT-0001"
HASH_VERSION = "ENDPOINT-0001-PREREG-V4"
PREDECESSOR_HASH_VERSION = "ENDPOINT-0001-PREREG-V3"

# XASSET-0028 closes the construction universe. Cardinality and integrity hash are recomputed
# from the real generator at validation time, never trusted as literals here.
REGISTERED_CONSTRUCTION_COUNT = 680

TOP_KEYS = (
    "schema_version",
    "study_id",
    "identifier_note",
    "authority",
    "lifecycle_effectivity",
    "stage_1_executability",
    "stages",
    "research_question",
    "sleeves",
    "bounds",
    "driver_classes",
    "driver_class_scope",
    "construction_families",
    "family_slot_grid",
    "construction_universe_closure",
    "completeness_rule",
    "trial_inventory",
    "roll_up_units",
    "gate_sequence",
    "categorical_definition",
    "prerequisite_definition",
    "disposition_rules",
    "open_reading_handling",
    "g2_reading_mapping",
    "stage_1_testable_subset",
    "deferred_admissibility_requirements",
    "result_vocabulary",
    "prohibited_inputs",
    "risk_lane_boundary",
    "representation",
    "consequential_parameter_registry",
    "data_and_sources",
    "source_architecture_vocabulary",
    "frozen_provenance_requirements",
    "provenance_manifest",
    "execution",
    "result_schema",
    "result_status_of_stage_1_output",
    "mandatory_abstention_conditions",
    "abstention_is_a_complete_outcome",
    "prohibited_scope",
    "protected_paths",
    "hash_version",
    "predecessor_hash_version",
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

# Closed by XASSET-0023 SS-H ("There is no third route") and SS-H.4 item 3 (R2 -> class 2;
# R1 -> classes 1, 3, 4, 5). Class 6 is disqualifying under SS-H.4 item 2. Derived, not invented.
CONSTRUCTION_FAMILIES = (
    ("R1_C1", "R1", 1, "EXTERNALLY_IMPOSED"),
    ("R1_C3", "R1", 3, "EMPIRICALLY_CALIBRATED"),
    ("R1_C4", "R1", 4, "EVIDENCE_BOUNDED_GOVERNANCE_SELECTION"),
    ("R1_C5", "R1", 5, "PROVISIONAL_GOVERNANCE_GUARDRAIL"),
    ("R2_C2", "R2", 2, "MATHEMATICALLY_DERIVED"),
)
FAMILY_KEYS = (
    "family_id",
    "route",
    "num_0001_class",
    "class_name",
    "originates_or_clips",
    "authority_ref",
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
    "G12_SNAPSHOT_ADMISSIBILITY_PATH",
)
GATE_KEYS = (
    "gate_id",
    "gate_index",
    "question",
    "controlling_authority",
    "failure_disposition",
)
FAILURE_DISPOSITIONS = ("BLOCKED_CATEGORICALLY", "BLOCKED_PENDING_SEPARATE_PREREQUISITE")
PREREQUISITE_GATES = ("G9_REPRESENTATION", "G12_SNAPSHOT_ADMISSIBILITY_PATH")
CATEGORICAL_GATES = tuple(g for g in GATE_IDS if g not in PREREQUISITE_GATES)

GATE_RESULT_VOCABULARY = ("PASS", "FAIL", "UNABLE_TO_DETERMINE", "NOT_APPLICABLE")

CANDIDATE_DISPOSITIONS = (
    "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED",
    "BLOCKED_CATEGORICALLY",
    "BLOCKED_PENDING_SEPARATE_PREREQUISITE",
    "UNABLE_TO_DETERMINE",
)
CELL_OUTCOMES = CANDIDATE_DISPOSITIONS
ROLL_UP_OUTCOMES = (
    "CANDIDATE_CONSTRUCTION_IDENTIFIED",
    "PREREQUISITE_REQUIRED",
    "NO_CONSTRUCTIBLE_CANDIDATE",
    "UNABLE_TO_DETERMINE",
)

# Candidate-level precedence. Categorical dominates, then uncertainty, then prerequisite.
# A prerequisite failure may not outrank UNABLE_TO_DETERMINE, because closing the named prerequisite
# cannot resolve the uncertainty; recording such a candidate as prerequisite-blocked would convert an
# open methodology question into a closeable to-do. Cell and roll-up precedence are unchanged.
CANDIDATE_PRECEDENCE = (
    ("ANY_CATEGORICAL_GATE_FAILURE", "BLOCKED_CATEGORICALLY"),
    ("ANY_GATE_UNABLE_TO_DETERMINE", "UNABLE_TO_DETERMINE"),
    ("ANY_PREREQUISITE_GATE_FAILURE", "BLOCKED_PENDING_SEPARATE_PREREQUISITE"),
    ("ALL_GATES_PASS", "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"),
)
CELL_PRECEDENCE = (
    ("ANY_CANDIDATE_CONSTRUCTIBLE_CANDIDATE_IDENTIFIED", "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"),
    ("ANY_CANDIDATE_BLOCKED_PENDING_SEPARATE_PREREQUISITE", "BLOCKED_PENDING_SEPARATE_PREREQUISITE"),
    ("ANY_CANDIDATE_UNABLE_TO_DETERMINE", "UNABLE_TO_DETERMINE"),
    ("ALL_CANDIDATES_BLOCKED_CATEGORICALLY", "BLOCKED_CATEGORICALLY"),
)
ROLL_UP_PRECEDENCE = (
    ("ANY_CELL_CONSTRUCTIBLE_CANDIDATE_IDENTIFIED", "CANDIDATE_CONSTRUCTION_IDENTIFIED"),
    ("ANY_CELL_BLOCKED_PENDING_SEPARATE_PREREQUISITE", "PREREQUISITE_REQUIRED"),
    ("ANY_CELL_UNABLE_TO_DETERMINE", "UNABLE_TO_DETERMINE"),
    ("ALL_CELLS_BLOCKED_CATEGORICALLY", "NO_CONSTRUCTIBLE_CANDIDATE"),
)

READING_VOCABULARY = ("PASSES", "FAILS", "UNABLE_TO_DETERMINE")
G2_MAPPING_KEYS = (
    "subject_matter_reading",
    "preference_only_reading",
    "g2_effective_outcome",
    "required_g2_gate_result",
    "reading_dependent",
)
G2_MAPPING_ROWS = (
    ("PASSES", "PASSES", "PASSES", "PASS", False),
    ("FAILS", "FAILS", "FAILS_CATEGORICALLY", "FAIL", False),
    ("PASSES", "FAILS", "UNABLE_TO_DETERMINE", "UNABLE_TO_DETERMINE", True),
    ("FAILS", "PASSES", "INCOHERENT_REJECTED", "RECORD_REJECTED", False),
    ("UNABLE_TO_DETERMINE", "ANY", "UNABLE_TO_DETERMINE", "UNABLE_TO_DETERMINE", False),
    ("ANY", "UNABLE_TO_DETERMINE", "UNABLE_TO_DETERMINE", "UNABLE_TO_DETERMINE", False),
)
# The effective-outcome value that means the two reading fields are mutually incoherent and the
# record is rejected outright rather than mapped to any gate result.
G2_RECORD_REJECTED = "RECORD_REJECTED"

POINT_RANGE_VALUES = (
    "WOULD_SUPPORT_RANGE_ENDPOINT",
    "WOULD_SUPPORT_POINT_ENDPOINT",
    "WOULD_SUPPORT_NEITHER",
)

SOURCE_ARCHITECTURES = ("EXISTING_SOURCE_ARCHITECTURE", "HYPOTHETICAL_SOURCE_ARCHITECTURE")

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
    "CONSTRUCTION_FAMILY_COUNT": 5,
    "CELL_COUNT": 48,
    "FAMILY_SLOT_COUNT": 240,
    "ROLL_UP_UNIT_COUNT": 8,
    "GATE_COUNT": 12,
}

LIFECYCLE_STEPS = (
    "ACCEPTED_INDEPENDENT_EXACT_HEAD_REVIEW",
    "PRINCIPAL_EXACT_HEAD_ACCEPTANCE",
    "MERGE",
    "IMMEDIATE_POST_MERGE_VERIFICATION",
    "SUCCESSFUL_MERGE_COMMIT_CI",
)

# Lifecycle closure alone does NOT make Stage 1 executable. It makes this architecture effective.
# Stage 1 additionally requires a closed concrete construction universe, which XASSET-0027 neither
# creates nor authorizes anyone to create.
STAGE_1_EFFECTIVITY_GATES = (
    "INDEPENDENT_FULL_EXACT_HEAD_REVIEW",
    "PRINCIPAL_EXACT_HEAD_ACCEPTANCE",
    "MERGE",
    "POST_MERGE_VERIFICATION",
    "MERGE_COMMIT_CI_SUCCESS",
    "MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION",
)

STAGE_1_EXECUTION_PRECONDITION = (
    "XASSET_0028_LIFECYCLE_CLOSURE_ALL_SIX_GATES_THEN_MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION"
)

# XASSET-0027's precondition, retained as HISTORY only. Its lifecycle is complete, so an operative
# field still naming it would no longer block anything after structural closure.
PREDECESSOR_STAGE_1_EXECUTION_PRECONDITION = (
    "CONSTRUCTION_UNIVERSE_CLOSURE_THEN_XASSET_0027_LIFECYCLE_CLOSURE_AND_MERGED_HASH_VERIFICATION"
)

REQUIRED_ABSTENTION_CONDITIONS = (
    "REPRESENTATION_PATH_1_FAILS_AND_NO_ACCEPTED_RULE_EXISTS",
    "ANY_REQUIRED_INPUT_IS_BARRED_BY_ORIGIN",
    "ANY_STEP_COULD_HAVE_BEEN_CHOSEN_DIFFERENTLY",
    "A_SECOND_LAWFUL_VALUE_EXISTS_FOR_THE_SAME_QUANTITY",
    "AN_UNRESOLVED_PAIR_WOULD_BE_CONSUMED_AS_AN_INPUT",
    "THE_PREFERENCE_ONLY_READING_OF_SECTION_E_1_IS_ESTABLISHED",
    "A_CANDIDATE_WOULD_REQUIRE_INVENTING_A_LEVEL_1_AGGREGATION_OR_REPRESENTATION_RULE",
    "A_CANDIDATES_G2_OUTCOME_IS_READING_DEPENDENT_WHILE_SECTION_K_1_REMAINS_UNRESOLVED",
)

REQUIRED_PROHIBITED_SCOPE = (
    "ENDPOINT_CREATION",
    "LOWER_OR_UPPER_BOUND_VALUE",
    "SLEEVE_SELECTION_PREFERENCE_RANKING_OR_SEQUENCING",
    "PORTFOLIO_RECONCILIATION_OR_SUM_TARGETING",
    "CROSS_SLEEVE_OR_CROSS_BOUND_ARITHMETIC",
    "OPTIMIZER_WEIGHT_GRID_OR_SWEEP",
    "COMPOSITE_SCORE_OR_INDEX",
    "RESIDUAL_REDISTRIBUTION",
    "SNAPSHOT_EXTENSION_OR_REPLACEMENT",
    "EVIDENCE_ADMISSION",
    "APPLICATION_AUTHORITY_OR_REGISTRY_POPULATION",
    "REPRESENTATION_RULE_ADOPTION",
    "METHODOLOGY_AMENDMENT",
    "UNREGISTERED_CANDIDATES",
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
    "ANY_CLAIM_OF_FULL_J_1_THROUGH_J_12_COMPLIANCE",
)

OPEN_READING_FIELDS = (
    "g2_outcome_under_subject_matter_reading",
    "g2_outcome_under_preference_only_reading",
    "g2_outcome_is_reading_dependent",
)

REQUIRED_CANDIDATE_RESULT_KEYS = (
    "construction_id",
    "cell_id",
    "sleeve",
    "bound",
    "driver_class",
    "family_id",
    "route",
    "num_0001_class",
    "source_architecture",
    "source_path",
    "source_sha256",
    "hypothetical_source_requirements",
    "governing_authority_refs",
    "gate_results",
    "categorical_failures",
    "prerequisite_failures",
    "disposition",
    "first_failing_gate_id",
    "g2_outcome_under_subject_matter_reading",
    "g2_outcome_under_preference_only_reading",
    "g2_outcome_is_reading_dependent",
    "point_or_range_support",
    "representation_dependency",
    "uncertainty_statement",
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


# ======================================================================================
# Pure deterministic derivation — the determinism claims, made executable
# ======================================================================================


def generate_family_slot_grid() -> tuple[str, ...]:
    """Return the complete, ordered, deterministic family slot grid.

    A Cartesian product over four dimensions, each closed by accepted authority. Byte-identically
    reproducible; no executor input participates.

    This is EXHAUSTIVE OVER PROVENANCE FAMILIES and NOT EXHAUSTIVE OVER CONSTRUCTIONS. A slot names a
    lawful provenance shape for a sleeve and bound; it does not name a hypothesis. It is therefore a
    classification scaffold for a future construction universe and is expressly not a trial ceiling,
    not a candidate enumeration, and not a basis for claiming exhaustive non-constructibility.
    """
    out: list[str] = []
    for sleeve in SLEEVES:
        for bound in BOUNDS:
            for driver_class in DRIVER_CLASSES:
                for family_id, _route, _cls, _name in CONSTRUCTION_FAMILIES:
                    out.append(f"{sleeve}::{bound}::{driver_class}::{family_id}")
    return tuple(out)


def cell_id_of(slot_or_construction_id: str) -> str:
    """Return the owning cell id for a family slot id or a construction id."""
    return "::".join(slot_or_construction_id.split("::")[:3])


def generate_cell_universe() -> tuple[str, ...]:
    """Return the complete, ordered, deterministic cell universe."""
    seen: list[str] = []
    for slot_id in generate_family_slot_grid():
        cell = cell_id_of(slot_id)
        if cell not in seen:
            seen.append(cell)
    return tuple(seen)


def map_g2_reading(subject_matter: str, preference_only: str) -> str:
    """Map the two XASSET-0024 SS-K.1 readings to G2's effective outcome.

    An unresolved methodology reading is never a categorical impossibility: a candidate passing only
    under the subject-matter reading is governed as UNABLE_TO_DETERMINE while SS-K.1 stands.
    """
    if subject_matter not in READING_VOCABULARY or preference_only not in READING_VOCABULARY:
        raise ValueError(
            f"reading outcomes must be in {READING_VOCABULARY}; "
            f"got {subject_matter!r} / {preference_only!r}"
        )
    if subject_matter == "UNABLE_TO_DETERMINE" or preference_only == "UNABLE_TO_DETERMINE":
        return "UNABLE_TO_DETERMINE"
    if subject_matter == "PASSES" and preference_only == "PASSES":
        return "PASSES"
    if subject_matter == "FAILS" and preference_only == "FAILS":
        return "FAILS_CATEGORICALLY"
    if subject_matter == "PASSES" and preference_only == "FAILS":
        return "UNABLE_TO_DETERMINE"
    return "INCOHERENT_REJECTED"


def is_reading_dependent(subject_matter: str, preference_only: str) -> bool:
    """True only for the one genuinely reading-dependent combination."""
    return subject_matter == "PASSES" and preference_only == "FAILS"


def required_g2_gate_result(subject_matter: str, preference_only: str) -> str:
    """Return the G2 gate result the two SS-K.1 readings REQUIRE, or RECORD_REJECTED.

    This is the enforced identity that makes the reading map load-bearing rather than decorative.
    Without it a results record could carry the reading-dependent pair while recording G2 as PASS, and
    the candidate would derive to CONSTRUCTIBLE_CANDIDATE_IDENTIFIED -- the exact outcome the open
    SS-K.1 reading is supposed to make impossible.
    """
    effective = map_g2_reading(subject_matter, preference_only)
    if effective == "PASSES":
        return "PASS"
    if effective == "FAILS_CATEGORICALLY":
        return "FAIL"
    if effective == "UNABLE_TO_DETERMINE":
        return "UNABLE_TO_DETERMINE"
    return G2_RECORD_REJECTED


def derive_candidate_disposition(gate_results: Mapping[str, str]) -> str:
    """Compose already-decided gate results into a candidate disposition.

    Universal over gates. Categorical failures dominate everything; UNABLE_TO_DETERMINE then dominates
    a prerequisite failure. Implemented with membership tests over the gate mapping, so the result
    cannot depend on gate order.

    Uncertainty outranks a prerequisite failure because closing the named prerequisite cannot resolve
    the uncertainty. A candidate whose G2 is UNABLE_TO_DETERMINE because XASSET-0024 SS-K.1 is
    unresolved, and whose G9 representation also fails, is not merely waiting on a representation
    rule: supplying that rule would leave SS-K.1 exactly as unresolved. A categorical bar may dominate
    uncertainty because the candidate is barred whatever the uncertainty resolves to.

    This ordering is CANDIDATE-LEVEL ONLY. derive_cell_outcome and derive_roll_up_outcome keep their
    existing existential precedence, because a different candidate that is determinately
    prerequisite-blocked can legitimately keep a cell open while another candidate is uncertain.
    """
    unknown = set(gate_results) - set(GATE_IDS)
    if unknown:
        raise ValueError(f"unknown gate id(s): {sorted(unknown)}")
    missing = set(GATE_IDS) - set(gate_results)
    if missing:
        raise ValueError(f"every gate must be evaluated before classifying; missing {sorted(missing)}")
    bad = {g: v for g, v in gate_results.items() if v not in GATE_RESULT_VOCABULARY}
    if bad:
        raise ValueError(f"gate results must be in {GATE_RESULT_VOCABULARY}; got {bad}")

    if any(gate_results[g] == "FAIL" for g in CATEGORICAL_GATES):
        return "BLOCKED_CATEGORICALLY"
    if any(v == "UNABLE_TO_DETERMINE" for v in gate_results.values()):
        return "UNABLE_TO_DETERMINE"
    if any(gate_results[g] == "FAIL" for g in PREREQUISITE_GATES):
        return "BLOCKED_PENDING_SEPARATE_PREREQUISITE"
    return "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"


def derive_cell_outcome(candidate_dispositions: Iterable[str]) -> str:
    """Compose a cell's candidate dispositions into a cell outcome (existential over candidates)."""
    values = list(candidate_dispositions)
    bad = [v for v in values if v not in CANDIDATE_DISPOSITIONS]
    if bad:
        raise ValueError(f"candidate dispositions must be in {CANDIDATE_DISPOSITIONS}; got {bad}")
    if not values:
        raise ValueError("a cell outcome requires at least one candidate disposition")
    if "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED" in values:
        return "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"
    if "BLOCKED_PENDING_SEPARATE_PREREQUISITE" in values:
        return "BLOCKED_PENDING_SEPARATE_PREREQUISITE"
    if "UNABLE_TO_DETERMINE" in values:
        return "UNABLE_TO_DETERMINE"
    return "BLOCKED_CATEGORICALLY"


def derive_roll_up_outcome(cell_outcomes: Iterable[str]) -> str:
    """Compose a (sleeve, bound) unit's cell outcomes into a roll-up (existential over cells)."""
    values = list(cell_outcomes)
    bad = [v for v in values if v not in CELL_OUTCOMES]
    if bad:
        raise ValueError(f"cell outcomes must be in {CELL_OUTCOMES}; got {bad}")
    if not values:
        raise ValueError("a roll-up requires at least one cell outcome")
    if "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED" in values:
        return "CANDIDATE_CONSTRUCTION_IDENTIFIED"
    if "BLOCKED_PENDING_SEPARATE_PREREQUISITE" in values:
        return "PREREQUISITE_REQUIRED"
    if "UNABLE_TO_DETERMINE" in values:
        return "UNABLE_TO_DETERMINE"
    return "NO_CONSTRUCTIBLE_CANDIDATE"


# ======================================================================================
# Helpers
# ======================================================================================


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


def _precedence(
    actual: Any, expected: Sequence[tuple[str, str]], where: str, errors: list[str]
) -> None:
    if not isinstance(actual, list):
        errors.append(f"{where}: expected a list, got {type(actual).__name__}")
        return
    if len(actual) != len(expected):
        errors.append(f"{where}: expected {len(expected)} rules, got {len(actual)}")
        return
    for position, rule in enumerate(actual):
        loc = f"{where}[{position}]"
        if not isinstance(rule, Mapping):
            errors.append(f"{loc}: expected a mapping")
            continue
        _exact(rule.get("condition"), expected[position][0], f"{loc}.condition", errors)
        _exact(rule.get("outcome"), expected[position][1], f"{loc}.outcome", errors)


# ======================================================================================
# Section validators
# ======================================================================================


def _validate_identity(data: Mapping[str, Any], errors: list[str]) -> None:
    _exact(data.get("study_id"), STUDY_ID, "study_id", errors)
    _exact(data.get("hash_version"), HASH_VERSION, "hash_version", errors)
    _exact(list(data.get("sleeves") or []), list(SLEEVES), "sleeves", errors)
    _exact(list(data.get("bounds") or []), list(BOUNDS), "bounds", errors)
    _exact(list(data.get("driver_classes") or []), list(DRIVER_CLASSES), "driver_classes", errors)

    note = data.get("identifier_note")
    if isinstance(note, Mapping):
        if "not a governance decision prefix" not in str(note.get("statement", "")):
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
    _true(
        auth.get("authority_constituted_by_same_decision"),
        "authority.authority_constituted_by_same_decision",
        errors,
    )
    _false(
        auth.get("authority_exercised_by_this_program"),
        "authority.authority_exercised_by_this_program",
        errors,
    )


def _validate_lifecycle(data: Mapping[str, Any], errors: list[str]) -> None:
    life = data.get("lifecycle_effectivity")
    if not isinstance(life, Mapping):
        errors.append("lifecycle_effectivity: expected a mapping")
        return
    _exact(
        list(life.get("charter_effective_only_after_all_of") or []),
        list(LIFECYCLE_STEPS),
        "lifecycle_effectivity.charter_effective_only_after_all_of",
        errors,
    )
    _exact(
        life.get("stage_1_execution_may_begin_only_after"),
        STAGE_1_EXECUTION_PRECONDITION,
        "lifecycle_effectivity.stage_1_execution_may_begin_only_after",
        errors,
    )
    _false(life.get("merge_alone_is_sufficient"), "lifecycle_effectivity.merge_alone_is_sufficient", errors)


def _validate_stage_1_executability(data: Mapping[str, Any], errors: list[str]) -> None:
    """Stage 1 is not executable under this charter, and the YAML must say so unambiguously.

    Lifecycle closure makes the architecture effective. It does not close the concrete construction
    universe, which XASSET-0027 neither creates nor authorizes anyone to create.
    """
    block = data.get("stage_1_executability")
    if not isinstance(block, Mapping):
        errors.append("stage_1_executability: expected a mapping")
        return
    # Stage 1 is STRUCTURALLY unblocked by XASSET-0028's closed universe and remains OPERATIONALLY
    # unauthorized until that decision's own lifecycle closes. Both facts must be stated, and
    # `executable` must stay false so no runner can read structural closure as authorization.
    _false(block.get("executable"), "stage_1_executability.executable", errors)
    _exact(
        block.get("status"),
        "STRUCTURALLY_CLOSED_NOT_OPERATIONALLY_AUTHORIZED",
        "stage_1_executability.status",
        errors,
    )
    _exact(
        block.get("blocking_prerequisite"),
        "XASSET_0028_LIFECYCLE_CLOSURE",
        "stage_1_executability.blocking_prerequisite",
        errors,
    )
    _false(
        block.get("authorized_by_xasset_0027"),
        "stage_1_executability.authorized_by_xasset_0027",
        errors,
    )
    _false(
        block.get("authorized_by_xasset_0028"),
        "stage_1_executability.authorized_by_xasset_0028",
        errors,
    )
    _true(
        block.get("construction_universe_structurally_closed"),
        "stage_1_executability.construction_universe_structurally_closed",
        errors,
    )
    _true(
        block.get("no_merge_to_execution_gap"),
        "stage_1_executability.no_merge_to_execution_gap",
        errors,
    )
    required_gates = (
        "INDEPENDENT_FULL_EXACT_HEAD_REVIEW",
        "PRINCIPAL_EXACT_HEAD_ACCEPTANCE",
        "MERGE",
        "POST_MERGE_VERIFICATION",
        "MERGE_COMMIT_CI_SUCCESS",
        "MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION",
    )
    declared = block.get("operational_authorization_requires_all_of") or ()
    for gate in required_gates:
        if gate not in declared:
            errors.append(
                "stage_1_executability.operational_authorization_requires_all_of: must include "
                f"{gate!r}"
            )


def _validate_stages(data: Mapping[str, Any], errors: list[str]) -> None:
    stages = data.get("stages")
    if not isinstance(stages, Mapping):
        errors.append("stages: expected a mapping")
        return
    s1 = stages.get("stage_1")
    if isinstance(s1, Mapping):
        _false(s1.get("authorized_by_xasset_0027"), "stages.stage_1.authorized_by_xasset_0027", errors)
        _exact(
            s1.get("executable_only_after"),
            STAGE_1_EXECUTION_PRECONDITION,
            "stages.stage_1.executable_only_after",
            errors,
        )
        for flag in (
            "acquires_data",
            "fits_or_estimates_anything",
            "produces_endpoint",
            "produces_admissible_evidence",
        ):
            _false(s1.get(flag), f"stages.stage_1.{flag}", errors)
        _exact(s1.get("unit_of_work"), "ONE_CANDIDATE_EVALUATION", "stages.stage_1.unit_of_work", errors)
    else:
        errors.append("stages.stage_1: expected a mapping")
    s2 = stages.get("stage_2")
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


def _validate_construction_families(data: Mapping[str, Any], errors: list[str]) -> None:
    block = data.get("construction_families")
    if not isinstance(block, Mapping):
        errors.append("construction_families: expected a mapping")
        return

    closure = block.get("closure_basis")
    if isinstance(closure, Mapping):
        _exact(
            closure.get("route_set_closed_by"),
            "XASSET-0023_SECTION_H_THERE_IS_NO_THIRD_ROUTE",
            "construction_families.closure_basis.route_set_closed_by",
            errors,
        )
        _exact(
            closure.get("route_class_coherence_closed_by"),
            "XASSET-0023_SECTION_H_4_ITEM_3",
            "construction_families.closure_basis.route_class_coherence_closed_by",
            errors,
        )
    else:
        errors.append("construction_families.closure_basis: expected a mapping")

    _exact(
        list(block.get("record_keys") or []),
        list(FAMILY_KEYS),
        "construction_families.record_keys",
        errors,
    )

    families = block.get("families")
    if not isinstance(families, list):
        errors.append("construction_families.families: expected a list")
        return
    if len(families) != len(CONSTRUCTION_FAMILIES):
        errors.append(
            f"construction_families.families: expected exactly {len(CONSTRUCTION_FAMILIES)} lawful "
            f"(route, class) families closed by XASSET-0023 SS-H.4 item 3, got {len(families)}"
        )
        return
    for position, family in enumerate(families):
        where = f"construction_families.families[{position}]"
        if not _keys(family, FAMILY_KEYS, where, errors):
            continue
        family_id, route, num_class, class_name = CONSTRUCTION_FAMILIES[position]
        _exact(family.get("family_id"), family_id, f"{where}.family_id", errors)
        _exact(family.get("route"), route, f"{where}.route", errors)
        _exact(family.get("num_0001_class"), num_class, f"{where}.num_0001_class", errors)
        _exact(family.get("class_name"), class_name, f"{where}.class_name", errors)
        _exact(family.get("originates_or_clips"), "ORIGINATE", f"{where}.originates_or_clips", errors)

    excluded = block.get("excluded_class")
    if isinstance(excluded, Mapping):
        _exact(excluded.get("num_0001_class"), 6, "construction_families.excluded_class.num_0001_class", errors)
    else:
        errors.append("construction_families.excluded_class: expected a mapping")

    non_routes = block.get("excluded_non_routes")
    if isinstance(non_routes, Mapping):
        listed = non_routes.get("non_routes")
        if not isinstance(listed, list) or len(listed) != 8:
            errors.append(
                "construction_families.excluded_non_routes.non_routes: expected XASSET-0024 SS-D's "
                "eight non-routes N1 through N8"
            )
    else:
        errors.append("construction_families.excluded_non_routes: expected a mapping")


def _validate_family_slot_grid(data: Mapping[str, Any], errors: list[str]) -> None:
    """The grid is exhaustive over provenance families and NOT over constructions.

    Both facts must be stated affirmatively in the YAML. A grid that claimed exhaustiveness over
    constructions would license reporting a family-slot negative as exhaustive non-constructibility,
    which is precisely the overreach this validator exists to prevent.
    """
    grid = data.get("family_slot_grid")
    if not isinstance(grid, Mapping):
        errors.append("family_slot_grid: expected a mapping")
        return
    _exact(
        grid.get("generation_rule"),
        "CARTESIAN_PRODUCT_OF_SLEEVES_BOUNDS_DRIVER_CLASSES_AND_CONSTRUCTION_FAMILIES",
        "family_slot_grid.generation_rule",
        errors,
    )
    _exact(
        grid.get("slot_id_format"),
        "{sleeve}::{bound}::{driver_class}::{family_id}",
        "family_slot_grid.slot_id_format",
        errors,
    )
    _exact(grid.get("slot_count"), len(generate_family_slot_grid()), "family_slot_grid.slot_count", errors)
    _true(grid.get("exhaustive_over_families"), "family_slot_grid.exhaustive_over_families", errors)
    _false(
        grid.get("exhaustive_over_constructions"),
        "family_slot_grid.exhaustive_over_constructions",
        errors,
    )
    _true(grid.get("deterministic"), "family_slot_grid.deterministic", errors)
    _true(
        grid.get("byte_identically_reproducible"),
        "family_slot_grid.byte_identically_reproducible",
        errors,
    )
    _exact(
        grid.get("slot_addition_or_removal"),
        "PROHIBITED",
        "family_slot_grid.slot_addition_or_removal",
        errors,
    )


def _validate_construction_universe_closure(data: Mapping[str, Any], errors: list[str]) -> None:
    """The construction universe is CLOSED by XASSET-0028, and predecessor identity is preserved.

    Amended by XASSET-0028. Under XASSET-0027 this block recorded NOT_CLOSED and a named prerequisite.
    XASSET-0028 is the separately accepted amendment that pin rule requires; it closes the universe
    over a stated basis and supplies the count and integrity hash. The XASSET-0027 record is retained
    verbatim as historical predecessor identity and is checked here so it can never be quietly
    rewritten -- including its own discipline that neither route was permanently foreclosed.
    """
    block = data.get("construction_universe_closure")
    if not isinstance(block, Mapping):
        errors.append("construction_universe_closure: expected a mapping")
        return

    _exact(block.get("status"), "CLOSED", "construction_universe_closure.status", errors)
    _exact(block.get("amended_by"), "XASSET-0028",
           "construction_universe_closure.amended_by", errors)
    _exact(block.get("predecessor_authority"), "XASSET-0027",
           "construction_universe_closure.predecessor_authority", errors)
    _exact(block.get("successor_authority"), "XASSET-0028",
           "construction_universe_closure.successor_authority", errors)
    _exact(block.get("predecessor_status"), "NOT_CLOSED",
           "construction_universe_closure.predecessor_status", errors)

    # Structural closure is not operational authorization.
    _false(block.get("stage_1_executable"),
           "construction_universe_closure.stage_1_executable", errors)
    _true(block.get("stage_1_structurally_closed"),
          "construction_universe_closure.stage_1_structurally_closed", errors)
    _false(block.get("stage_1_operationally_authorized"),
           "construction_universe_closure.stage_1_operationally_authorized", errors)
    _false(block.get("executor_may_add_omit_substitute_or_mutate_a_construction"),
           "construction_universe_closure.executor_may_add_omit_substitute_or_mutate_a_construction",
           errors)
    _true(block.get("generator_is_canonical_source_of_construction_identity"),
          "construction_universe_closure.generator_is_canonical_source_of_construction_identity",
          errors)
    _exact(
        block.get("generator"),
        "level1_construction_universe_closure_validator.generate_construction_universe",
        "construction_universe_closure.generator",
        errors,
    )
    _exact(
        block.get("invented_completeness"),
        "PROHIBITED",
        "construction_universe_closure.invented_completeness",
        errors,
    )

    # Cardinality and integrity hash are recomputed from the real generator, never trusted as
    # written numbers.
    try:
        import level1_construction_universe_closure_validator as CU

        universe = CU.generate_construction_universe()
        if block.get("registered_construction_count") != len(universe):
            errors.append(
                "construction_universe_closure.registered_construction_count: must equal the "
                f"generated cardinality {len(universe)}"
            )
        if block.get("construction_universe_sha256") != CU.universe_aggregate_sha256(universe):
            errors.append(
                "construction_universe_closure.construction_universe_sha256: must equal the "
                "aggregate hash of the canonical serialization of the generated universe"
            )
    except ImportError as exc:  # pragma: no cover - defensive
        errors.append(f"construction_universe_closure: generator module unavailable: {exc}")

    props = block.get("closure_basis_properties")
    if not isinstance(props, Mapping):
        errors.append("construction_universe_closure.closure_basis_properties: expected a mapping")
    else:
        for flag in (
            "stated",
            "non_outcome_aware",
            "non_economic",
            "deterministic",
            "byte_identically_reproducible",
            "frozen_before_stage_1_outcomes",
            "contains_no_endpoint_value",
        ):
            _true(props.get(flag), f"construction_universe_closure.closure_basis_properties.{flag}",
                  errors)
        _false(
            props.get("selects_ranks_or_prefers_any_sleeve_or_comparator"),
            "construction_universe_closure.closure_basis_properties."
            "selects_ranks_or_prefers_any_sleeve_or_comparator",
            errors,
        )

    # ---- Historical predecessor identity, preserved verbatim ----
    pred = block.get("xasset_0027_predecessor_record")
    if not isinstance(pred, Mapping):
        errors.append(
            "construction_universe_closure.xasset_0027_predecessor_record: the XASSET-0027 record "
            "must be preserved as historical predecessor identity"
        )
        return
    _true(pred.get("preserved_verbatim"),
          "construction_universe_closure.xasset_0027_predecessor_record.preserved_verbatim", errors)
    _exact(pred.get("status"), "NOT_CLOSED",
           "construction_universe_closure.xasset_0027_predecessor_record.status", errors)
    _exact(
        pred.get("route_taken"),
        "HONEST_PREREQUISITE",
        "construction_universe_closure.xasset_0027_predecessor_record.route_taken",
        errors,
    )
    _exact(
        pred.get("next_required_prerequisite"),
        "CONCRETE_CONSTRUCTION_UNIVERSE_PREREGISTRATION",
        "construction_universe_closure.xasset_0027_predecessor_record.next_required_prerequisite",
        errors,
    )
    _true(
        pred.get("routes_are_unavailable_now_not_permanently_foreclosed"),
        "construction_universe_closure.xasset_0027_predecessor_record."
        "routes_are_unavailable_now_not_permanently_foreclosed",
        errors,
    )
    unavailable = pred.get("routes_considered_and_unavailable_to_this_filing")
    if not isinstance(unavailable, list) or len(unavailable) != 2:
        errors.append(
            "construction_universe_closure.xasset_0027_predecessor_record."
            "routes_considered_and_unavailable_to_this_filing: expected both routes "
            "(CONCRETE_FINITE_REGISTRY, DETERMINISTIC_CONSTRUCTION_GRAMMAR) with reasons"
        )
    else:
        _exact(
            [r.get("route") if isinstance(r, Mapping) else None for r in unavailable],
            ["CONCRETE_FINITE_REGISTRY", "DETERMINISTIC_CONSTRUCTION_GRAMMAR"],
            "construction_universe_closure.xasset_0027_predecessor_record."
            "routes_considered_and_unavailable_to_this_filing[].route",
            errors,
        )
        for position, row in enumerate(unavailable):
            where = (
                "construction_universe_closure.xasset_0027_predecessor_record."
                f"routes_considered_and_unavailable_to_this_filing[{position}]"
            )
            reason = row.get("unavailable_to_this_filing_because") if isinstance(row, Mapping) else None
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"{where}.unavailable_to_this_filing_because: expected a non-empty reason")
            elif isinstance(row, Mapping):
                # A route reason may not assert permanent impossibility. XASSET-0028 proves the
                # point: one of these very routes was in fact available to a later unit.
                for banned in (
                    "closeable only",
                    "can never",
                    "could never",
                    "is impossible",
                    "permanently foreclosed",
                    "no future",
                ):
                    if banned in reason.lower():
                        errors.append(
                            f"{where}.unavailable_to_this_filing_because: {banned!r} asserts a "
                            "permanent impossibility XASSET-0027 had no authority to determine; "
                            "record what it could not do from present authority instead"
                        )
            if isinstance(row, Mapping) and "rejected_because" in row:
                errors.append(
                    f"{where}.rejected_because: a route is recorded as unavailable to that filing, "
                    "not rejected; 'rejected' reads as permanently foreclosed"
                )

    completeness = data.get("completeness_rule")
    if isinstance(completeness, Mapping):
        _true(
            completeness.get("applies_only_after_construction_universe_closure"),
            "completeness_rule.applies_only_after_construction_universe_closure",
            errors,
        )
        _true(
            completeness.get("construction_universe_closure_now_exists"),
            "completeness_rule.construction_universe_closure_now_exists",
            errors,
        )
        _exact(
            completeness.get("closed_by"), "XASSET-0028", "completeness_rule.closed_by", errors
        )
        _true(
            completeness.get("cell_negative_requires_all_registered_constructions_evaluated"),
            "completeness_rule.cell_negative_requires_all_registered_constructions_evaluated",
            errors,
        )
        _true(
            completeness.get("family_slot_negative_does_not_establish_non_constructibility"),
            "completeness_rule.family_slot_negative_does_not_establish_non_constructibility",
            errors,
        )
        _false(
            completeness.get("unevaluated_construction_permitted"),
            "completeness_rule.unevaluated_construction_permitted",
            errors,
        )
        _false(
            completeness.get("partial_cell_outcome_permitted"),
            "completeness_rule.partial_cell_outcome_permitted",
            errors,
        )
    else:
        errors.append("completeness_rule: expected a mapping")


def _validate_counts(data: Mapping[str, Any], errors: list[str]) -> None:
    inventory = data.get("trial_inventory")
    if isinstance(inventory, Mapping):
        # A trial ceiling bounds hypotheses. AMENDED BY XASSET-0028: the construction universe IS
        # now closed, so the number of constructions is defined and an honest ceiling exists. It is
        # the registered construction count, recomputed from the real generator -- never the 240
        # family slots, which remain a classification grid and not a ceiling.
        _exact(inventory.get("status"), "DEFINED", "trial_inventory.status", errors)
        _exact(inventory.get("defined_by"), "XASSET-0028", "trial_inventory.defined_by", errors)
        _exact(
            inventory.get("predecessor_status_xasset_0027"),
            "NOT_YET_DEFINABLE",
            "trial_inventory.predecessor_status_xasset_0027",
            errors,
        )
        try:
            import level1_construction_universe_closure_validator as CU

            _exact(
                inventory.get("registered_constructions"),
                len(CU.generate_construction_universe()),
                "trial_inventory.registered_constructions",
                errors,
            )
        except ImportError as exc:  # pragma: no cover - defensive
            errors.append(f"trial_inventory: generator module unavailable: {exc}")
        _exact(
            inventory.get("unit_of_trial"),
            "ONE_CONSTRUCTION_EVALUATION",
            "trial_inventory.unit_of_trial",
            errors,
        )
        _exact(
            inventory.get("unit_of_trial_once_defined"),
            "ONE_CONSTRUCTION_EVALUATION",
            "trial_inventory.unit_of_trial_once_defined",
            errors,
        )
        _exact(inventory.get("derived_cells"), 48, "trial_inventory.derived_cells", errors)
        _exact(
            inventory.get("derived_family_slots"),
            240,
            "trial_inventory.derived_family_slots",
            errors,
        )
        _exact(inventory.get("family_slots_per_cell"), 5, "trial_inventory.family_slots_per_cell", errors)
        _exact(
            inventory.get("result_aware_constructions"),
            "PROHIBITED",
            "trial_inventory.result_aware_constructions",
            errors,
        )
        _true(
            inventory.get("every_registered_construction_must_be_recorded"),
            "trial_inventory.every_registered_construction_must_be_recorded",
            errors,
        )
        # The family-slot grid must not be smuggled back in as a candidate ceiling. `unit_of_trial`
        # is no longer banned -- XASSET-0028 closes the universe, so a lawful unit of trial exists --
        # but a ceiling derived from the 240 slots still is.
        for banned in ("derived_candidate_ceiling", "candidates_per_cell"):
            if banned in inventory:
                errors.append(
                    f"trial_inventory.{banned}: the 240 family slots are a classification grid and "
                    "may never be restated as a candidate ceiling"
                )
    else:
        errors.append("trial_inventory: expected a mapping")

    roll_up = data.get("roll_up_units")
    if isinstance(roll_up, Mapping):
        _exact(roll_up.get("derived_count"), 8, "roll_up_units.derived_count", errors)
        _true(
            roll_up.get("computed_only_from_own_six_cells"),
            "roll_up_units.computed_only_from_own_six_cells",
            errors,
        )
        _exact(roll_up.get("cross_bound_reference"), "PROHIBITED", "roll_up_units.cross_bound_reference", errors)
        _exact(roll_up.get("cross_sleeve_reference"), "PROHIBITED", "roll_up_units.cross_sleeve_reference", errors)
    else:
        errors.append("roll_up_units: expected a mapping")

    # Recompute the arithmetic from the closed populations rather than trusting the asserted numbers.
    cells = len(SLEEVES) * len(BOUNDS) * len(DRIVER_CLASSES)
    slots = cells * len(CONSTRUCTION_FAMILIES)
    if cells != 48 or slots != 240:
        errors.append(
            f"derived arithmetic: closed populations imply {cells} cells and {slots} family slots, "
            "not 48 and 240"
        )
    generated = generate_family_slot_grid()
    if len(generated) != 240:
        errors.append(f"generator produced {len(generated)} family slots, expected 240")
    if len(set(generated)) != len(generated):
        errors.append("generator produced duplicate family slot ids")
    if len(generate_cell_universe()) != 48:
        errors.append("generator produced an unexpected cell count")


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


def _validate_gates(data: Mapping[str, Any], errors: list[str]) -> None:
    seq = data.get("gate_sequence")
    if not isinstance(seq, Mapping):
        errors.append("gate_sequence: expected a mapping")
        return
    _exact(
        seq.get("evaluation_requirement"),
        "EVALUATE_EVERY_APPLICABLE_GATE_BEFORE_CLASSIFYING",
        "gate_sequence.evaluation_requirement",
        errors,
    )
    _false(seq.get("record_first_failing_gate_only"), "gate_sequence.record_first_failing_gate_only", errors)
    _true(
        seq.get("first_failing_gate_is_diagnostic_only"),
        "gate_sequence.first_failing_gate_is_diagnostic_only",
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

    gate_ids = [g.get("gate_id") for g in gates if isinstance(g, Mapping)]
    for removed in ("G12_RECONCILIATION_FEASIBILITY", "G13_SNAPSHOT_ADMISSIBILITY_PATH"):
        if removed in gate_ids:
            errors.append(
                f"gate_sequence.gates: {removed} must not appear; XASSET-0024 SS-J.12 is deferred as a "
                "whole-candidate prerequisite and the snapshot gate is G12"
            )


def _validate_definitions(data: Mapping[str, Any], errors: list[str]) -> None:
    cat = data.get("categorical_definition")
    if isinstance(cat, Mapping):
        _exact(cat.get("term"), "BLOCKED_CATEGORICALLY", "categorical_definition.term", errors)
        _exact(
            cat.get("means"),
            "NOT_CLOSEABLE_BY_A_NAMED_PREREQUISITE_UNDER_THE_CURRENTLY_ACCEPTED_METHODOLOGY",
            "categorical_definition.means",
            errors,
        )
        _exact(
            cat.get("does_not_mean"),
            "PERMANENTLY_IMPOSSIBLE_UNDER_ALL_FUTURE_GOVERNANCE",
            "categorical_definition.does_not_mean",
            errors,
        )
    else:
        errors.append("categorical_definition: expected a mapping")

    pre = data.get("prerequisite_definition")
    if isinstance(pre, Mapping):
        _true(pre.get("requires_named_dependency"), "prerequisite_definition.requires_named_dependency", errors)
    else:
        errors.append("prerequisite_definition: expected a mapping")


def _validate_disposition_rules(data: Mapping[str, Any], errors: list[str]) -> None:
    rules = data.get("disposition_rules")
    if not isinstance(rules, Mapping):
        errors.append("disposition_rules: expected a mapping")
        return
    _true(rules.get("order_independent"), "disposition_rules.order_independent", errors)

    cand = rules.get("candidate_disposition")
    if isinstance(cand, Mapping):
        _exact(
            cand.get("quantifier"),
            "UNIVERSAL_OVER_ITS_OWN_GATE_RESULTS",
            "disposition_rules.candidate_disposition.quantifier",
            errors,
        )
        _true(
            cand.get("categorical_dominates_prerequisite"),
            "disposition_rules.candidate_disposition.categorical_dominates_prerequisite",
            errors,
        )
        _true(
            cand.get("uncertainty_dominates_prerequisite"),
            "disposition_rules.candidate_disposition.uncertainty_dominates_prerequisite",
            errors,
        )
        _exact(
            cand.get("applies_at"),
            "CANDIDATE_LEVEL_ONLY",
            "disposition_rules.candidate_disposition.applies_at",
            errors,
        )
        _precedence(
            cand.get("precedence"),
            CANDIDATE_PRECEDENCE,
            "disposition_rules.candidate_disposition.precedence",
            errors,
        )
    else:
        errors.append("disposition_rules.candidate_disposition: expected a mapping")

    cell = rules.get("cell_outcome")
    if isinstance(cell, Mapping):
        _exact(
            cell.get("quantifier"),
            "EXISTENTIAL_OVER_ITS_OWN_FIVE_CANDIDATE_DISPOSITIONS",
            "disposition_rules.cell_outcome.quantifier",
            errors,
        )
        _precedence(cell.get("precedence"), CELL_PRECEDENCE, "disposition_rules.cell_outcome.precedence", errors)
    else:
        errors.append("disposition_rules.cell_outcome: expected a mapping")

    roll = rules.get("roll_up_outcome")
    if isinstance(roll, Mapping):
        _precedence(
            roll.get("precedence"), ROLL_UP_PRECEDENCE, "disposition_rules.roll_up_outcome.precedence", errors
        )
    else:
        errors.append("disposition_rules.roll_up_outcome: expected a mapping")


def _validate_open_reading(data: Mapping[str, Any], errors: list[str]) -> None:
    handling = data.get("open_reading_handling")
    if not isinstance(handling, Mapping):
        errors.append("open_reading_handling: expected a mapping")
        return
    _false(handling.get("resolved_by_this_program"), "open_reading_handling.resolved_by_this_program", errors)
    _false(handling.get("relied_upon_by_this_program"), "open_reading_handling.relied_upon_by_this_program", errors)
    _exact(
        handling.get("handling"),
        "EVALUATE_G2_UNDER_BOTH_READINGS_AND_MAP_DETERMINISTICALLY",
        "open_reading_handling.handling",
        errors,
    )
    _exact(
        list(handling.get("per_reading_vocabulary") or []),
        list(READING_VOCABULARY),
        "open_reading_handling.per_reading_vocabulary",
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

    mapping = data.get("g2_reading_mapping")
    if not isinstance(mapping, Mapping):
        errors.append("g2_reading_mapping: expected a mapping")
        return
    _true(mapping.get("closed_table"), "g2_reading_mapping.closed_table", errors)
    # Without this the table is decorative: a record could carry the reading-dependent pair while
    # recording G2 as PASS, and derive a constructible candidate.
    _true(mapping.get("coupled_to_g2_gate_result"), "g2_reading_mapping.coupled_to_g2_gate_result", errors)
    _exact(
        mapping.get("reading_dependent_maps_to_candidate_outcome"),
        "UNABLE_TO_DETERMINE",
        "g2_reading_mapping.reading_dependent_maps_to_candidate_outcome",
        errors,
    )
    _exact(
        list(mapping.get("record_keys") or []),
        list(G2_MAPPING_KEYS),
        "g2_reading_mapping.record_keys",
        errors,
    )
    rows = mapping.get("rows")
    if not isinstance(rows, list) or len(rows) != len(G2_MAPPING_ROWS):
        errors.append(f"g2_reading_mapping.rows: expected {len(G2_MAPPING_ROWS)} closed rows")
        return
    for position, row in enumerate(rows):
        where = f"g2_reading_mapping.rows[{position}]"
        if not _keys(row, G2_MAPPING_KEYS, where, errors):
            continue
        sm, po, out, gate, dep = G2_MAPPING_ROWS[position]
        _exact(row.get("subject_matter_reading"), sm, f"{where}.subject_matter_reading", errors)
        _exact(row.get("preference_only_reading"), po, f"{where}.preference_only_reading", errors)
        _exact(row.get("g2_effective_outcome"), out, f"{where}.g2_effective_outcome", errors)
        _exact(row.get("required_g2_gate_result"), gate, f"{where}.required_g2_gate_result", errors)
        _exact(row.get("reading_dependent"), dep, f"{where}.reading_dependent", errors)

    # The declared table and both executable mapping functions must agree on every concrete pair.
    for sm in READING_VOCABULARY:
        for po in READING_VOCABULARY:
            declared = None
            declared_gate = None
            for r_sm, r_po, r_out, r_gate, _dep in G2_MAPPING_ROWS:
                if (r_sm in (sm, "ANY")) and (r_po in (po, "ANY")):
                    declared = r_out
                    declared_gate = r_gate
                    break
            computed = map_g2_reading(sm, po)
            if declared is not None and declared != computed:
                errors.append(
                    f"g2_reading_mapping: declared table gives {declared!r} for ({sm}, {po}) but "
                    f"map_g2_reading() gives {computed!r}"
                )
            computed_gate = required_g2_gate_result(sm, po)
            if declared_gate is not None and declared_gate != computed_gate:
                errors.append(
                    f"g2_reading_mapping: declared table requires G2 {declared_gate!r} for ({sm}, {po}) "
                    f"but required_g2_gate_result() gives {computed_gate!r}"
                )


def _validate_deferred(data: Mapping[str, Any], errors: list[str]) -> None:
    subset = data.get("stage_1_testable_subset")
    if isinstance(subset, Mapping):
        items = subset.get("items")
        if not isinstance(items, list) or len(items) != 12:
            errors.append("stage_1_testable_subset.items: expected all twelve XASSET-0024 SS-J items")
        else:
            j12 = [i for i in items if isinstance(i, Mapping) and i.get("j_item", "").startswith("J_12")]
            if not j12:
                errors.append("stage_1_testable_subset.items: J_12 is absent")
            else:
                _exact(
                    j12[0].get("stage_1_status"),
                    "NOT_YET_DETERMINABLE_DEFERRED",
                    "stage_1_testable_subset J_12.stage_1_status",
                    errors,
                )
    else:
        errors.append("stage_1_testable_subset: expected a mapping")

    deferred = data.get("deferred_admissibility_requirements")
    if not isinstance(deferred, Mapping):
        errors.append("deferred_admissibility_requirements: expected a mapping")
        return
    _exact(
        deferred.get("cross_sleeve_arithmetic_to_satisfy_a_deferred_requirement"),
        "PROHIBITED",
        "deferred_admissibility_requirements.cross_sleeve_arithmetic_to_satisfy_a_deferred_requirement",
        errors,
    )
    reqs = deferred.get("requirements")
    if not isinstance(reqs, list) or not reqs:
        errors.append("deferred_admissibility_requirements.requirements: expected a non-empty list")
        return
    ids = {str(r.get("requirement_id")) for r in reqs if isinstance(r, Mapping)}
    if "J_12_EXACT_SET_VALUED_RECONCILIATION" not in ids:
        errors.append(
            "deferred_admissibility_requirements: J_12_EXACT_SET_VALUED_RECONCILIATION must be recorded "
            "as deferred; XASSET-0020 SS-K defines reconciliation jointly over the whole candidate"
        )
    for req in reqs:
        if not isinstance(req, Mapping):
            continue
        _false(
            req.get("stage_1_may_claim_compliance"),
            f"deferred_admissibility_requirements[{req.get('requirement_id')!r}].stage_1_may_claim_compliance",
            errors,
        )
        if not str(req.get("why_not_determinable_in_stage_1", "")).strip():
            errors.append(
                f"deferred_admissibility_requirements[{req.get('requirement_id')!r}]"
                ".why_not_determinable_in_stage_1: must be non-empty"
            )


def _validate_vocabulary(data: Mapping[str, Any], errors: list[str]) -> None:
    vocab = data.get("result_vocabulary")
    if not isinstance(vocab, Mapping):
        errors.append("result_vocabulary: expected a mapping")
        return
    _exact(
        list(vocab.get("candidate_dispositions") or []),
        list(CANDIDATE_DISPOSITIONS),
        "result_vocabulary.candidate_dispositions",
        errors,
    )
    _exact(list(vocab.get("cell_outcomes") or []), list(CELL_OUTCOMES), "result_vocabulary.cell_outcomes", errors)
    _exact(
        list(vocab.get("roll_up_outcomes") or []),
        list(ROLL_UP_OUTCOMES),
        "result_vocabulary.roll_up_outcomes",
        errors,
    )
    _exact(
        list(vocab.get("gate_result_vocabulary") or []),
        list(GATE_RESULT_VOCABULARY),
        "result_vocabulary.gate_result_vocabulary",
        errors,
    )
    _true(vocab.get("no_outcome_is_a_score"), "result_vocabulary.no_outcome_is_a_score", errors)
    _exact(
        vocab.get("mechanism"),
        "FIXED_PRECEDENCE_QUANTIFIER_TESTS",
        "result_vocabulary.mechanism",
        errors,
    )

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
        # The registered set is supplied by the future construction universe closure unit, not by the
        # 240 family slots. Pinning the stopping rule to 240 would reintroduce the family-slot ceiling
        # as though it were a candidate enumeration.
        _exact(
            stopping.get("terminates_when"),
            "EVERY_REGISTERED_CONSTRUCTION_IN_THE_CLOSED_CONSTRUCTION_UNIVERSE_CARRIES_A_RECORDED_DISPOSITION",
            "execution.stopping_rules.terminates_when",
            errors,
        )
        # AMENDED BY XASSET-0028: the rule now ranges over the closed registered set.
        _false(
            stopping.get("stopping_rule_currently_has_no_registered_set"),
            "execution.stopping_rules.stopping_rule_currently_has_no_registered_set",
            errors,
        )
        _exact(
            stopping.get("stopping_rule_amended_by"),
            "XASSET-0028",
            "execution.stopping_rules.stopping_rule_amended_by",
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
        for key in (
            "gates_frozen_before_evaluation",
            "candidates_frozen_before_evaluation",
            "vocabulary_frozen_before_evaluation",
        ):
            _true(mining.get(key), f"execution.history_mining_controls.{key}", errors)
        _exact(
            mining.get("outcome_aware_gate_change"),
            "PROHIBITED",
            "execution.history_mining_controls.outcome_aware_gate_change",
            errors,
        )
        _exact(
            mining.get("outcome_aware_candidate_addition_or_removal"),
            "PROHIBITED",
            "execution.history_mining_controls.outcome_aware_candidate_addition_or_removal",
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
            negative.get("all_candidate_dispositions_recorded_regardless_of_direction"),
            "execution.negative_result_preservation.all_candidate_dispositions_recorded_regardless_of_direction",
            errors,
        )
        _true(
            negative.get("null_is_a_complete_outcome"),
            "execution.negative_result_preservation.null_is_a_complete_outcome",
            errors,
        )
    else:
        errors.append("execution.negative_result_preservation: expected a mapping")


def _validate_result_boundary(data: Mapping[str, Any], errors: list[str]) -> None:
    arch = data.get("source_architecture_vocabulary")
    if isinstance(arch, Mapping):
        _exact(
            list(arch.get("values") or []),
            list(SOURCE_ARCHITECTURES),
            "source_architecture_vocabulary.values",
            errors,
        )
        _contains_all(
            arch.get("existing_requires"),
            ("source_path", "source_sha256"),
            "source_architecture_vocabulary.existing_requires",
            errors,
        )
        _contains_all(
            arch.get("hypothetical_forbids"),
            ("source_path", "source_sha256"),
            "source_architecture_vocabulary.hypothetical_forbids",
            errors,
        )
    else:
        errors.append("source_architecture_vocabulary: expected a mapping")

    frozen = data.get("frozen_provenance_requirements")
    if isinstance(frozen, Mapping):
        _true(
            frozen.get("binding_on_any_future_stage_1"),
            "frozen_provenance_requirements.binding_on_any_future_stage_1",
            errors,
        )
        existing = frozen.get("existing_source_architecture")
        if isinstance(existing, Mapping):
            for key in (
                "identity_must_be_frozen_before_execution",
                "path_and_hash_must_be_bound_to_a_preregistered_construction_identity",
                "observed_bytes_must_be_verified_against_the_frozen_hash",
                "syntactic_validation_is_insufficient",
            ):
                _true(existing.get(key), f"frozen_provenance_requirements.existing_source_architecture.{key}", errors)
        else:
            errors.append("frozen_provenance_requirements.existing_source_architecture: expected a mapping")
        hypothetical = frozen.get("hypothetical_source_architecture")
        if isinstance(hypothetical, Mapping):
            _true(
                hypothetical.get("requirements_must_be_frozen_before_execution"),
                "frozen_provenance_requirements.hypothetical_source_architecture."
                "requirements_must_be_frozen_before_execution",
                errors,
            )
            _exact(
                hypothetical.get("executor_authored_free_text_at_results_time"),
                "PROHIBITED",
                "frozen_provenance_requirements.hypothetical_source_architecture."
                "executor_authored_free_text_at_results_time",
                errors,
            )
        else:
            errors.append("frozen_provenance_requirements.hypothetical_source_architecture: expected a mapping")
        _false(
            frozen.get("result_author_may_alter_a_frozen_architecture"),
            "frozen_provenance_requirements.result_author_may_alter_a_frozen_architecture",
            errors,
        )
        # No construction universe exists, so no architecture is frozen. This is the direct mechanical
        # reason no results document can satisfy these requirements today.
        _false(
            frozen.get("currently_satisfiable"),
            "frozen_provenance_requirements.currently_satisfiable",
            errors,
        )
    else:
        errors.append("frozen_provenance_requirements: expected a mapping")

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
            schema.get("candidate_result_keys"),
            REQUIRED_CANDIDATE_RESULT_KEYS,
            "result_schema.candidate_result_keys",
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
            "may_claim_full_j_1_through_j_12_compliance",
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
    _validate_lifecycle(data, errors)
    _validate_stage_1_executability(data, errors)
    _validate_stages(data, errors)
    _validate_construction_families(data, errors)
    _validate_family_slot_grid(data, errors)
    _validate_construction_universe_closure(data, errors)
    _validate_counts(data, errors)
    _validate_registry(data, errors)
    _validate_gates(data, errors)
    _validate_definitions(data, errors)
    _validate_disposition_rules(data, errors)
    _validate_open_reading(data, errors)
    _validate_deferred(data, errors)
    _validate_vocabulary(data, errors)
    _validate_firewall(data, errors)
    _validate_representation(data, errors)
    _validate_execution(data, errors)
    _validate_result_boundary(data, errors)
    _validate_abstention_and_scope(data, errors)
    return ValidationResult(not errors, tuple(errors))


# ======================================================================================
# Stage-1 results validation — enforces the frozen universe on a future results document
# ======================================================================================


def closed_construction_universe() -> Mapping[str, Mapping[str, Any]]:
    """Return the closed construction universe.

    AMENDED BY XASSET-0028. Under XASSET-0027 this was deliberately empty because no concrete
    universe existed. XASSET-0028 closes one, so this now returns the real frozen universe: each
    construction_id mapped to its frozen cell_id, source_architecture, and (since every registered
    construction is HYPOTHETICAL_SOURCE_ARCHITECTURE) its frozen hypothetical_source_requirements.

    Returning a non-empty universe makes the enforcement machinery real and testable. It does NOT
    authorize execution: stage_1_operational_authorization_is_effective() is an independent gate that
    validate_stage1_results() consults first and that no results author can satisfy from a results
    document.
    """
    try:
        import level1_construction_universe_closure_validator as CU
    except ImportError:  # pragma: no cover - defensive
        return {}
    return CU.frozen_construction_universe()


def stage_1_operational_authorization_is_effective(
    prereg_path: Path = PREREG_PATH,
) -> tuple[bool, str]:
    """Report whether Stage-1 OPERATIONAL authorization is effective, and why not when it is not.

    Structural closure of the construction universe is not authorization. The canonical
    stage_1_executability block carries `executable`, which stays false until the full XASSET-0028
    six-gate lifecycle has closed and a later, separately governed amendment flips it. Reading the
    canonical file rather than a module constant means a results author cannot bypass this by
    constructing a document, and a merge alone cannot flip it either.
    """
    try:
        data = yaml.safe_load(prereg_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:  # pragma: no cover - defensive
        return False, f"canonical preregistration unreadable: {exc}"
    block = (data or {}).get("stage_1_executability")
    if not isinstance(block, Mapping):
        return False, "canonical stage_1_executability block absent"
    if block.get("executable") is not True:
        return False, (
            "stage_1_executability.executable is not true; the construction universe is "
            "structurally closed but Stage-1 operational authorization requires the full "
            f"XASSET-0028 lifecycle ({', '.join(STAGE_1_EFFECTIVITY_GATES)}). Structural closure is "
            "not authorization, and there is no merge-to-execution gap."
        )
    return True, ""


def validate_stage1_results(
    results: Mapping[str, Any],
    construction_universe: Mapping[str, Mapping[str, Any]] | None = None,
) -> ValidationResult:
    """Validate a Stage-1 results document against a CLOSED construction universe.

    ``construction_universe`` maps each frozen ``construction_id`` to its frozen provenance:
    ``cell_id``, ``source_architecture``, and either ``source_path``/``source_sha256`` (existing) or
    ``hypothetical_source_requirements`` (hypothetical). It defaults to
    :func:`closed_construction_universe`, which is EMPTY, so a real call fails closed: no results
    document may be produced while the construction universe is not closed.

    Supplying a universe explicitly does not authorize execution; it exercises the enforcement
    machinery a future, separately authorized closure unit and Stage-1 implementation must pass.
    """
    errors: list[str] = []
    if not isinstance(results, Mapping):
        return ValidationResult(False, ("stage1_results: expected a top-level mapping",))

    # Lifecycle gate on the REAL path. XASSET-0028 closes the universe structurally, so
    # closed_construction_universe() is no longer empty and can no longer fail closed by emptiness
    # alone. An actual Stage-1 run passes no universe and is refused here until the six-gate
    # XASSET-0028 lifecycle is complete.
    #
    # An explicitly supplied universe still exercises the enforcement machinery without authorizing
    # anything -- the same distinction this function's own accepted docstring already drew.
    if construction_universe is None:
        authorized, reason = stage_1_operational_authorization_is_effective()
        if not authorized:
            return ValidationResult(
                False,
                (f"stage1_results: Stage-1 execution is not operationally authorized — {reason}",),
            )
        construction_universe = closed_construction_universe()
    if not construction_universe:
        return ValidationResult(
            False,
            (
                "stage1_results: no closed construction universe exists, so no Stage-1 results "
                "document may be produced or validated. The 240 family slots classify provenance and "
                "do not enumerate constructions. Closing a concrete construction universe requires "
                "its own separately authorized unit (CONCRETE_CONSTRUCTION_UNIVERSE_PREREGISTRATION).",
            ),
        )

    expected_universe = tuple(construction_universe)
    candidates = results.get("candidate_results")
    if not isinstance(candidates, list):
        return ValidationResult(False, ("stage1_results.candidate_results: expected a list",))

    seen: dict[str, Mapping[str, Any]] = {}
    for position, row in enumerate(candidates):
        where = f"candidate_results[{position}]"
        if not isinstance(row, Mapping):
            errors.append(f"{where}: expected a mapping")
            continue
        construction_id = row.get("construction_id")
        if construction_id not in construction_universe:
            errors.append(
                f"{where}.construction_id: {construction_id!r} is not in the frozen construction "
                "universe; unregistered constructions are prohibited"
            )
            continue
        if construction_id in seen:
            errors.append(f"{where}.construction_id: {construction_id!r} is duplicated")
            continue
        seen[str(construction_id)] = row
        frozen = construction_universe[str(construction_id)]

        for key in REQUIRED_CANDIDATE_RESULT_KEYS:
            if key not in row:
                errors.append(f"{where}: required key {key!r} is absent")

        # Provenance must be the FROZEN identity, verified against observed bytes. Accepting a
        # syntactically valid path plus an arbitrary 64-hex string validates shape, not identity.
        architecture = row.get("source_architecture")
        frozen_architecture = frozen.get("source_architecture") if isinstance(frozen, Mapping) else None
        if architecture not in SOURCE_ARCHITECTURES:
            errors.append(f"{where}.source_architecture: {architecture!r} is outside the closed set")
        elif architecture != frozen_architecture:
            errors.append(
                f"{where}.source_architecture: recorded {architecture!r} but the frozen construction "
                f"identity is {frozen_architecture!r}; a result author may not alter a frozen architecture"
            )
        elif architecture == "EXISTING_SOURCE_ARCHITECTURE":
            recorded_path = str(row.get("source_path") or "").strip()
            recorded_sha = str(row.get("source_sha256") or "")
            frozen_path = str(frozen.get("source_path") or "").strip()
            frozen_sha = str(frozen.get("source_sha256") or "")
            if not recorded_path:
                errors.append(f"{where}.source_path: required for EXISTING_SOURCE_ARCHITECTURE")
            elif recorded_path != frozen_path:
                errors.append(
                    f"{where}.source_path: recorded {recorded_path!r} but the frozen construction "
                    f"identity names {frozen_path!r}"
                )
            if not re.fullmatch(r"[0-9a-f]{64}", recorded_sha):
                errors.append(f"{where}.source_sha256: required 64-hex digest for EXISTING_SOURCE_ARCHITECTURE")
            elif recorded_sha != frozen_sha:
                errors.append(
                    f"{where}.source_sha256: recorded digest does not match the frozen construction "
                    "identity's digest"
                )
            elif recorded_path == frozen_path and recorded_path:
                # Verify the digest against the file's observed bytes, not merely its syntax.
                resolved = (ROOT / recorded_path).resolve()
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    errors.append(f"{where}.source_path: {recorded_path!r} resolves outside the repository")
                else:
                    if not resolved.is_file():
                        errors.append(
                            f"{where}.source_path: {recorded_path!r} does not exist; a frozen source "
                            "identity must name an actual file whose bytes can be verified"
                        )
                    else:
                        observed = sha256_file(resolved)
                        if observed != recorded_sha:
                            errors.append(
                                f"{where}.source_sha256: recorded digest does not match the observed "
                                f"bytes of {recorded_path!r}"
                            )
        else:
            if row.get("source_path") is not None or row.get("source_sha256") is not None:
                errors.append(
                    f"{where}: HYPOTHETICAL_SOURCE_ARCHITECTURE must carry no source_path or source_sha256"
                )
            recorded_requirements = str(row.get("hypothetical_source_requirements") or "").strip()
            frozen_requirements = str(frozen.get("hypothetical_source_requirements") or "").strip()
            if not recorded_requirements:
                errors.append(
                    f"{where}.hypothetical_source_requirements: required for HYPOTHETICAL_SOURCE_ARCHITECTURE"
                )
            elif recorded_requirements != frozen_requirements:
                errors.append(
                    f"{where}.hypothetical_source_requirements: does not match the frozen construction "
                    "identity; a non-empty string authored at results time is not a preregistration"
                )

        if not row.get("governing_authority_refs"):
            errors.append(f"{where}.governing_authority_refs: must be non-empty")

        # The reading map must be applied exactly, and it must GOVERN the recorded G2 gate result.
        sm = row.get("g2_outcome_under_subject_matter_reading")
        po = row.get("g2_outcome_under_preference_only_reading")
        gate_results = row.get("gate_results")
        if sm in READING_VOCABULARY and po in READING_VOCABULARY:
            required_gate = required_g2_gate_result(str(sm), str(po))
            if required_gate == G2_RECORD_REJECTED:
                errors.append(
                    f"{where}: subject-matter FAILS with preference-only PASSES is incoherent; the "
                    "preference-only reading is strictly narrower"
                )
            elif isinstance(gate_results, Mapping):
                recorded_gate = gate_results.get("G2_MAGNITUDE_INTRINSICALITY")
                if recorded_gate != required_gate:
                    errors.append(
                        f"{where}.gate_results.G2_MAGNITUDE_INTRINSICALITY: recorded {recorded_gate!r} "
                        f"but the two SS-K.1 readings require {required_gate!r}; the reading map governs "
                        "the recorded gate result and is not an annotation beside it"
                    )
            expected_dep = is_reading_dependent(str(sm), str(po))
            if row.get("g2_outcome_is_reading_dependent") is not expected_dep:
                errors.append(
                    f"{where}.g2_outcome_is_reading_dependent: expected {expected_dep}, got "
                    f"{row.get('g2_outcome_is_reading_dependent')!r}"
                )
            if expected_dep and row.get("disposition") == "BLOCKED_CATEGORICALLY":
                errors.append(
                    f"{where}: a reading-dependent G2 outcome may not be recorded as "
                    "BLOCKED_CATEGORICALLY while XASSET-0024 SS-K.1 remains unresolved"
                )
            if expected_dep and row.get("disposition") == "BLOCKED_PENDING_SEPARATE_PREREQUISITE":
                errors.append(
                    f"{where}: a reading-dependent G2 outcome may not be recorded as "
                    "BLOCKED_PENDING_SEPARATE_PREREQUISITE; closing a named prerequisite cannot "
                    "resolve XASSET-0024 SS-K.1"
                )
        else:
            errors.append(f"{where}: both G2 reading outcomes must be in {READING_VOCABULARY}")

        # Disposition must equal the deterministic derivation from the recorded gate results.
        if isinstance(gate_results, Mapping):
            try:
                derived = derive_candidate_disposition(gate_results)
            except ValueError as exc:
                errors.append(f"{where}.gate_results: {exc}")
            else:
                if row.get("disposition") != derived:
                    errors.append(
                        f"{where}.disposition: recorded {row.get('disposition')!r} but the gate results "
                        f"deterministically derive {derived!r}"
                    )
        else:
            errors.append(f"{where}.gate_results: expected a mapping of every gate id to a result")

    missing = [c for c in expected_universe if c not in seen]
    if missing:
        errors.append(
            f"candidate_results: {len(missing)} registered construction(s) have no recorded "
            f"disposition, e.g. {missing[:3]}; a cell outcome requires its complete registered set"
        )

    # Cell outcomes must be the deterministic composition of their own registered constructions.
    cell_rows = results.get("cell_results")
    if isinstance(cell_rows, list):
        for position, row in enumerate(cell_rows):
            where = f"cell_results[{position}]"
            if not isinstance(row, Mapping):
                errors.append(f"{where}: expected a mapping")
                continue
            cell_id = str(row.get("cell_id"))
            members = [c for c in expected_universe if cell_id_of(c) == cell_id]
            if not members:
                errors.append(f"{where}.cell_id: {cell_id!r} is not a registered cell")
                continue
            dispositions = [seen[m].get("disposition") for m in members if m in seen]
            if len(dispositions) != len(members):
                errors.append(
                    f"{where}: cell {cell_id!r} has {len(dispositions)} of {len(members)} registered "
                    "dispositions; a negative cell outcome requires every registered construction to "
                    "be evaluated"
                )
                continue
            try:
                derived = derive_cell_outcome([str(d) for d in dispositions])
            except ValueError as exc:
                errors.append(f"{where}: {exc}")
                continue
            if row.get("outcome") != derived:
                errors.append(
                    f"{where}.outcome: recorded {row.get('outcome')!r} but its registered constructions "
                    f"deterministically derive {derived!r}"
                )

    for banned in ("J_1_THROUGH_J_12_SATISFIED", "FULL_J_COMPLIANCE"):
        if banned in str(results.get("disposition", "")):
            errors.append(
                f"stage1_results.disposition: {banned!r} may not be claimed; XASSET-0024 SS-J.12 is "
                "deferred and Stage 1 tests only the Stage-1-testable subset"
            )
    for banned in ("EXHAUSTIVE_NON_CONSTRUCTIBILITY", "NO_CONSTRUCTION_IS_POSSIBLE"):
        if banned in str(results.get("disposition", "")):
            errors.append(
                f"stage1_results.disposition: {banned!r} may not be claimed; a family-slot negative "
                "means only that no construction the executor considered within that provenance "
                "family qualified"
            )

    return ValidationResult(not errors, tuple(errors))


# ======================================================================================
# Companion-document validation
# ======================================================================================


def protocol_mirror_expected() -> dict[str, str]:
    """Return the mirror values the protocol must reproduce."""
    return {
        "study_id": STUDY_ID,
        "sleeve_count": str(len(SLEEVES)),
        "bound_count": str(len(BOUNDS)),
        "driver_class_count": str(len(DRIVER_CLASSES)),
        "construction_family_count": str(len(CONSTRUCTION_FAMILIES)),
        "cell_count": str(DERIVED_IDENTITIES["CELL_COUNT"]),
        "family_slot_count": str(DERIVED_IDENTITIES["FAMILY_SLOT_COUNT"]),
        "roll_up_unit_count": str(DERIVED_IDENTITIES["ROLL_UP_UNIT_COUNT"]),
        "gate_count": str(len(GATE_IDS)),
        "consequential_parameter_count": "0",
        "stage_1_executable": "false",
        "construction_universe_closed": "true",
        "registered_construction_count": str(REGISTERED_CONSTRUCTION_COUNT),
        "construction_universe_sha256": _universe_sha256(),
        "stage_1_structurally_closed": "true",
        "stage_1_operationally_authorized": "false",
        "stage_2_authorized": "false",
        "j12_deferred": "true",
        "hash_version": HASH_VERSION,
        "predecessor_hash_version": PREDECESSOR_HASH_VERSION,
    }


def _universe_sha256() -> str:
    """Aggregate identity hash of the XASSET-0028 construction universe, recomputed live.

    Imported lazily so this accepted validator keeps zero import-time dependency on the XASSET-0028
    module, and so a missing successor module surfaces as an explicit error rather than an import
    crash.
    """
    import level1_construction_universe_closure_validator as CU

    return CU.universe_aggregate_sha256()


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


# XASSET-0027's accepted pins, retained as HISTORICAL predecessor identity. XASSET-0028 amends the
# canonical bytes under successor authority, so these no longer describe the current files -- and must
# not be rewritten to pretend otherwise. They are asserted verbatim so accepted history stays auditable.
PREDECESSOR_PINS = {
    "protocol_sha256": "1a7b288718dfc688adb409ea9ecdf0fe5c858a32ee154f4f407c132895f41c8b",
    "preregistration_sha256": "bb25b1181c94d4dba2939a634b6fcb894f93597a664d5e91ffdcf021de3d385f",
}

SUCCESSOR_HASH_BLOCK_RE = re.compile(
    r"<!-- XASSET-0028-HASH-PINS-V1\n(?P<body>.*?)\n-->", re.DOTALL
)


def validate_successor_hash_pins(
    decision_text: str, prereg_path: Path = PREREG_PATH, protocol_path: Path = PROTOCOL_PATH
) -> ValidationResult:
    """Validate XASSET-0028's successor pins against the canonical files as committed.

    The successor pins are the EFFECTIVE ones once XASSET-0028's lifecycle closes. They are verified
    against observed bytes, and they must differ from the predecessor pins -- an amendment that left
    the bytes unchanged would not be an amendment.
    """
    errors: list[str] = []
    pins = extract_block(decision_text, SUCCESSOR_HASH_BLOCK_RE)
    if pins is None:
        return ValidationResult(False, ("XASSET-0028: XASSET-0028-HASH-PINS-V1 block absent",))
    expected_paths = {
        "protocol_path": "research/level1_endpoint_evidence/PROTOCOL_V1.md",
        "preregistration_path": "research/level1_endpoint_evidence/pre_registration.yaml",
    }
    for key, want in expected_paths.items():
        if pins.get(key) != want:
            errors.append(f"successor pins: {key} expected {want!r}, got {pins.get(key)!r}")
    for key, path in (("protocol_sha256", protocol_path), ("preregistration_sha256", prereg_path)):
        pinned = pins.get(key)
        if not pinned:
            errors.append(f"successor pins: {key} is absent")
            continue
        actual = sha256_file(path)
        if pinned != actual:
            errors.append(
                f"successor pins: {key} mismatch -- XASSET-0028 pins {pinned}, file is {actual}"
            )
        if pinned == PREDECESSOR_PINS[key]:
            errors.append(
                f"successor pins: {key} equals the predecessor pin; the amendment must change the "
                "canonical bytes it re-pins"
            )
    for key, want in PREDECESSOR_PINS.items():
        got = pins.get(f"predecessor_{key}")
        if got != want:
            errors.append(
                f"successor pins: predecessor_{key} must retain the XASSET-0027 value {want!r}, "
                f"got {got!r}"
            )
    return ValidationResult(not errors, tuple(errors))


def validate_charter_hash_pins(
    decision_text: str, prereg_path: Path = PREREG_PATH, protocol_path: Path = PROTOCOL_PATH
) -> ValidationResult:
    """Validate that the XASSET-0027 charter retains its historical pins verbatim.

    AMENDED BY XASSET-0028. This previously asserted that the pinned digests still matched the live
    canonical files. XASSET-0028 amends those files under successor authority, so that assertion
    would now force either a false failure or a rewrite of accepted history. It instead asserts the
    charter still records exactly the digests it accepted -- history preserved, not restated as
    current fact. Current-byte verification moved to validate_successor_hash_pins().
    """
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
    for key, want in PREDECESSOR_PINS.items():
        pinned = pins.get(key)
        if not pinned:
            errors.append(f"hash pins: {key} is absent")
        elif pinned != want:
            errors.append(
                f"hash pins: {key} is {pinned}, but XASSET-0027's accepted historical pin is {want}; "
                "accepted history may not be rewritten"
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
        errors.extend(validate_charter_hash_pins(DECISION_PATH.read_text(encoding="utf-8")).errors)
    else:
        errors.append(f"{DECISION_PATH}: file not found")

    # XASSET-0028 successor pins are the EFFECTIVE ones for the amended canonical bytes.
    if SUCCESSOR_DECISION_PATH.exists():
        errors.extend(
            validate_successor_hash_pins(
                SUCCESSOR_DECISION_PATH.read_text(encoding="utf-8")
            ).errors
        )
    else:
        errors.append(f"{SUCCESSOR_DECISION_PATH}: file not found")

    return ValidationResult(not errors, tuple(errors))


def main() -> int:  # pragma: no cover - CLI
    result = validate_file()
    if result.ok:
        print(
            f"level1_endpoint_evidence_preregistration_validator: OK ({STUDY_ID}; "
            f"{len(generate_family_slot_grid())} family slots over {len(generate_cell_universe())} "
            f"cells; construction universe CLOSED at {REGISTERED_CONSTRUCTION_COUNT} registered "
            "constructions; Stage 1 NOT EXECUTABLE)"
        )
        return 0
    print(f"level1_endpoint_evidence_preregistration_validator: {len(result.errors)} error(s)")
    for error in result.errors:
        print(f"  - {error}")
    return 1


if __name__ == "__main__":  # pragma: no cover - CLI
    sys.exit(main())
