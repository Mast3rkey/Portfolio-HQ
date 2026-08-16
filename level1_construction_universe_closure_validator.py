"""Structural validator for the ENDPOINT-0001 construction-universe closure determination.

Authorized by governance/decisions/XASSET-0028-concrete-construction-universe-closure-determination.md

Read-only and mechanical. This module validates the XASSET-0028 determination artifact at
research/level1_construction_universe/CLOSURE_DETERMINATION_V1.yaml, which answers XASSET-0027
SS-P.0 in the negative: a concrete construction universe for ENDPOINT-0001 Stage 1 cannot be closed
under XASSET-0028's authority, and two independent prerequisites are named.

Because the determination is negative, this module's job is the mirror image of a closure validator's.
It does not check that a frozen universe is complete; it mechanically preserves the fact that none
exists. Specifically it enforces that:

  * the determination records NOT_CLOSED_PREREQUISITE_REQUIRED and Stage 1 as not executable;
  * no construction is registered and no universe is frozen anywhere in the artifact;
  * both canonical ENDPOINT-0001 files remain byte-identical to their XASSET-0027 hash pins, digests
    recomputed from observed bytes rather than trusted from the document;
  * nothing in the artifact claims the family-slot grid IS the construction universe, that the
    construction universe is closed, or that the qualitative search surface is closed -- the last of
    which also blocks a downstream reader from acting on the stale sentence disclosed as FINDING_1;
  * the negative is not overstated as permanent impossibility, reusing XASSET-0027's own banned-phrase
    discipline adopted after its independent review found exactly that overclaim;
  * both prerequisites are present with their independence recorded, so a successor cannot satisfy the
    narrower one and report the universe as closeable;
  * the PREREQ-1 slot arithmetic is verified against the accepted family-slot generator rather than
    trusted as a written number;
  * no comparator rule is supplied, no endpoint-shaped value appears, and the preserved postures
    (SS-K.1 unresolved, SS-J.12 deferred, representation, Stage 2, application authority) are intact.

It decides nothing. It cannot close a construction universe, register a construction, supply a
comparator rule, execute Stage 1, or admit evidence.

Zero import coupling with allocate.py and margin_state.py in either direction. It imports exactly one
read-only generator from the accepted XASSET-0027 preregistration validator, so that the slot
arithmetic is checked against the real generator instead of a literal repeated here.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

import level1_endpoint_evidence_preregistration_validator as PREREG

ROOT = Path(__file__).resolve().parent
DETERMINATION_PATH = ROOT / "research/level1_construction_universe/CLOSURE_DETERMINATION_V1.yaml"
DECISION_PATH = (
    ROOT
    / "governance/decisions"
    / "XASSET-0028-concrete-construction-universe-closure-determination.md"
)

CANONICAL_PINS = {
    "research/level1_endpoint_evidence/PROTOCOL_V1.md": (
        "1a7b288718dfc688adb409ea9ecdf0fe5c858a32ee154f4f407c132895f41c8b"
    ),
    "research/level1_endpoint_evidence/pre_registration.yaml": (
        "bb25b1181c94d4dba2939a634b6fcb894f93597a664d5e91ffdcf021de3d385f"
    ),
}

REQUIRED_STATUS = "NOT_CLOSED_PREREQUISITE_REQUIRED"

REQUIRED_PREREQUISITE_IDS = (
    "PREREQ_1_COMPARATOR_ADMISSIBILITY_RULE",
    "PREREQ_2_HYPOTHETICAL_SOURCE_ARCHITECTURE_ENUMERATION_PRINCIPLE",
)

REQUIRED_CLOSURE_CRITERIA = (
    "C1_FINITE",
    "C2_FROZEN_BEFORE_OUTCOME",
    "C3_EXHAUSTIVE_OVER_CONSTRUCTIONS",
    "C4_NO_EXECUTOR_DISCRETION",
    "C5_REPRODUCIBLE_IDENTITY",
)

REQUIRED_ROUTES = (
    "CONCRETE_FINITE_REGISTRY",
    "DETERMINISTIC_CONSTRUCTION_GRAMMAR",
    "DOMINANCE_OVER_A_MAXIMALLY_PERMISSIVE_CONSTRUCTION",
    "FINITE_QUOTIENT_OVER_GATE_OUTCOME_VECTORS",
    "HONEST_NEGATIVE_WITH_NAMED_PREREQUISITES",
)

# The three XASSET-0020 SS-E.1 DRIVER classes XASSET-0026 SS-D records as comparison-scoped with no
# comparator fixed. diversification_cobehavior is deliberately absent: its comparator space is closed
# by XASSET-0020 at exactly six unordered pairs.
COMPARISON_SCOPED_DRIVER_CLASSES = (
    "valuation_opportunity_cost",
    "downside_path_risk",
    "recovery",
)

# Reused from XASSET-0027's own correction: phrasing that asserts permanent impossibility rather than
# a bound on present authority.
BANNED_PERMANENCE_PHRASES = (
    "closeable only",
    "can never",
    "could never",
    "is impossible",
    "permanently foreclosed",
    "no future",
)

# Phrasing that would let a downstream runner treat the scaffold as the universe, or act on the stale
# sentence disclosed as FINDING_1.
BANNED_CLOSURE_CLAIMS = (
    "search surface is closed",
    "search surface is now closed",
    "universe is closed",
    "universe is now closed",
    "grid is the construction universe",
    "slots are the construction universe",
)

# XASSET-0020 SS-M contamination list -- barred historical outputs, never reproduced.
BARRED_HISTORICAL_NUMERALS = ("18.67", "14.67", "16.67", "33.32")

PERCENT_SHAPED = re.compile(r"\d\s*%|\d+\.\d+\s*percent", re.IGNORECASE)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _walk_strings(value: Any, where: str = "") -> list[tuple[str, str]]:
    """Yield every (location, string) pair in the document tree."""
    found: list[tuple[str, str]] = []
    if isinstance(value, str):
        found.append((where or "<root>", value))
    elif isinstance(value, Mapping):
        for key, item in value.items():
            found.append((f"{where}.{key}" if where else str(key), str(key)))
            found.extend(_walk_strings(item, f"{where}.{key}" if where else str(key)))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for index, item in enumerate(value):
            found.extend(_walk_strings(item, f"{where}[{index}]"))
    return found


def _exact(actual: Any, expected: Any, where: str, errors: list[str]) -> None:
    if actual != expected:
        errors.append(f"{where}: expected {expected!r}, found {actual!r}")


def _true(value: Any, where: str, errors: list[str]) -> None:
    if value is not True:
        errors.append(f"{where}: must be exactly true, found {value!r}")


def _false(value: Any, where: str, errors: list[str]) -> None:
    if value is not False:
        errors.append(f"{where}: must be exactly false, found {value!r}")


def _nonempty_str(value: Any, where: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{where}: must be a non-empty string, found {value!r}")


def comparison_scoped_slot_count() -> int:
    """Count comparison-scoped family slots from the accepted generator, not from a literal.

    This is the mechanical check behind PREREQ-1's stated blast radius. It filters the real
    XASSET-0027 family-slot grid rather than trusting a number written in the determination.
    """
    slots = PREREG.generate_family_slot_grid()
    return sum(
        1
        for slot in slots
        if slot.split("::")[2] in COMPARISON_SCOPED_DRIVER_CLASSES
    )


def total_slot_count() -> int:
    return len(PREREG.generate_family_slot_grid())


def _validate_identity(data: Mapping[str, Any], errors: list[str]) -> None:
    _exact(data.get("determination_id"), "ENDPOINT-0001-CONSTRUCTION-UNIVERSE-CLOSURE-V1",
           "determination_id", errors)
    _exact(data.get("study_id"), "ENDPOINT-0001", "study_id", errors)
    _exact(data.get("governing_decision"), "XASSET-0028", "governing_decision", errors)
    _exact(data.get("answers"), "XASSET_0027_SECTION_P_0", "answers", errors)
    _nonempty_str(data.get("question_verbatim"), "question_verbatim", errors)


def _validate_determination(data: Mapping[str, Any], errors: list[str]) -> None:
    block = data.get("determination")
    if not isinstance(block, Mapping):
        errors.append("determination: missing or not a mapping")
        return
    _exact(block.get("status"), REQUIRED_STATUS, "determination.status", errors)
    _false(block.get("stage_1_executable"), "determination.stage_1_executable", errors)
    _false(block.get("a_concrete_construction_universe_was_frozen"),
           "determination.a_concrete_construction_universe_was_frozen", errors)
    _exact(block.get("outcome_class"), "NEGATIVE_PREREQUISITE_REQUIRED",
           "determination.outcome_class", errors)
    _true(block.get("determination_is_present_authority_bounded"),
          "determination.determination_is_present_authority_bounded", errors)
    _true(block.get("determination_is_not_permanent_impossibility"),
          "determination.determination_is_not_permanent_impossibility", errors)
    _nonempty_str(block.get("statement"), "determination.statement", errors)


def _validate_canonical_files(data: Mapping[str, Any], errors: list[str]) -> None:
    block = data.get("canonical_files_verified")
    if not isinstance(block, Mapping):
        errors.append("canonical_files_verified: missing or not a mapping")
        return
    _false(block.get("modified_by_this_determination"),
           "canonical_files_verified.modified_by_this_determination", errors)
    files = block.get("files")
    if not isinstance(files, Sequence) or isinstance(files, (str, bytes)):
        errors.append("canonical_files_verified.files: must be a list")
        return
    recorded = {}
    for index, entry in enumerate(files):
        if not isinstance(entry, Mapping):
            errors.append(f"canonical_files_verified.files[{index}]: not a mapping")
            continue
        recorded[entry.get("path")] = entry.get("sha256")
    for path, pin in CANONICAL_PINS.items():
        if path not in recorded:
            errors.append(f"canonical_files_verified.files: missing entry for {path}")
            continue
        if recorded[path] != pin:
            errors.append(
                f"canonical_files_verified.files[{path}].sha256: recorded {recorded[path]!r} "
                f"does not match the XASSET-0027 pin {pin!r}"
            )
            continue
        target = ROOT / path
        if not target.exists():
            errors.append(f"{path}: canonical file is missing")
            continue
        observed = sha256_file(target)
        if observed != pin:
            errors.append(
                f"{path}: observed digest {observed!r} does not match the XASSET-0027 pin {pin!r}; "
                "the canonical file has changed and this determination's basis is void"
            )


def _validate_closure_test(data: Mapping[str, Any], errors: list[str]) -> None:
    block = data.get("closure_test")
    if not isinstance(block, Mapping):
        errors.append("closure_test: missing or not a mapping")
        return
    criteria = block.get("criteria")
    if not isinstance(criteria, Sequence) or isinstance(criteria, (str, bytes)):
        errors.append("closure_test.criteria: must be a list")
        return
    seen = {}
    for index, entry in enumerate(criteria):
        if not isinstance(entry, Mapping):
            errors.append(f"closure_test.criteria[{index}]: not a mapping")
            continue
        seen[entry.get("id")] = entry
    for required in REQUIRED_CLOSURE_CRITERIA:
        if required not in seen:
            errors.append(f"closure_test.criteria: missing {required}")
    c3 = seen.get("C3_EXHAUSTIVE_OVER_CONSTRUCTIONS")
    if isinstance(c3, Mapping):
        _false(c3.get("satisfiable_under_this_authority"),
               "closure_test.criteria[C3].satisfiable_under_this_authority", errors)
        _true(c3.get("decisive"), "closure_test.criteria[C3].decisive", errors)


def _validate_routes(data: Mapping[str, Any], errors: list[str]) -> None:
    routes = data.get("routes_examined")
    if not isinstance(routes, Sequence) or isinstance(routes, (str, bytes)):
        errors.append("routes_examined: must be a list")
        return
    seen = {}
    for index, entry in enumerate(routes):
        if not isinstance(entry, Mapping):
            errors.append(f"routes_examined[{index}]: not a mapping")
            continue
        seen[entry.get("route")] = entry
    for required in REQUIRED_ROUTES:
        if required not in seen:
            errors.append(f"routes_examined: missing {required}")
    taken = [name for name, entry in seen.items() if entry.get("taken") is True]
    if taken != ["HONEST_NEGATIVE_WITH_NAMED_PREREQUISITES"]:
        errors.append(
            "routes_examined: exactly HONEST_NEGATIVE_WITH_NAMED_PREREQUISITES must be marked "
            f"taken, found {taken!r}"
        )
    for name in REQUIRED_ROUTES:
        entry = seen.get(name)
        if not isinstance(entry, Mapping):
            continue
        expected = name == "HONEST_NEGATIVE_WITH_NAMED_PREREQUISITES"
        if entry.get("available_under_this_authority") is not expected:
            errors.append(
                f"routes_examined[{name}].available_under_this_authority: expected {expected!r}"
            )


def _validate_prerequisites(data: Mapping[str, Any], errors: list[str]) -> None:
    block = data.get("blocking_prerequisites")
    if not isinstance(block, Mapping):
        errors.append("blocking_prerequisites: missing or not a mapping")
        return
    _nonempty_str(block.get("independence_note"),
                  "blocking_prerequisites.independence_note", errors)
    prereqs = block.get("prerequisites")
    if not isinstance(prereqs, Sequence) or isinstance(prereqs, (str, bytes)):
        errors.append("blocking_prerequisites.prerequisites: must be a list")
        return
    seen = {}
    for index, entry in enumerate(prereqs):
        if not isinstance(entry, Mapping):
            errors.append(f"blocking_prerequisites.prerequisites[{index}]: not a mapping")
            continue
        seen[entry.get("id")] = entry
    for required in REQUIRED_PREREQUISITE_IDS:
        if required not in seen:
            errors.append(f"blocking_prerequisites.prerequisites: missing {required}")
            continue
        entry = seen[required]
        _nonempty_str(entry.get("what_is_missing"),
                      f"{required}.what_is_missing", errors)
        _nonempty_str(entry.get("why_this_unit_cannot_supply_it"),
                      f"{required}.why_this_unit_cannot_supply_it", errors)

    total = total_slot_count()
    comparison = comparison_scoped_slot_count()

    p1 = seen.get("PREREQ_1_COMPARATOR_ADMISSIBILITY_RULE")
    if isinstance(p1, Mapping):
        _exact(p1.get("blocks_slots"), comparison,
               "PREREQ_1.blocks_slots (verified against the accepted family-slot generator)", errors)
        _exact(p1.get("blocks_slots_of"), total, "PREREQ_1.blocks_slots_of", errors)
        affected = list(p1.get("affected_driver_classes") or [])
        if sorted(affected) != sorted(COMPARISON_SCOPED_DRIVER_CLASSES):
            errors.append(
                "PREREQ_1.affected_driver_classes: must be exactly the three comparison-scoped "
                f"classes XASSET-0026 SS-D names, found {affected!r}"
            )
        unaffected = list(p1.get("unaffected_driver_classes") or [])
        if "diversification_cobehavior" not in unaffected:
            errors.append(
                "PREREQ_1.unaffected_driver_classes: diversification_cobehavior must be recorded as "
                "unaffected; XASSET-0020 closes its comparator space at exactly six unordered pairs"
            )

    p2 = seen.get("PREREQ_2_HYPOTHETICAL_SOURCE_ARCHITECTURE_ENUMERATION_PRINCIPLE")
    if isinstance(p2, Mapping):
        _exact(p2.get("blocks_slots"), total, "PREREQ_2.blocks_slots", errors)
        _exact(p2.get("blocks_slots_of"), total, "PREREQ_2.blocks_slots_of", errors)


def _validate_preserved(data: Mapping[str, Any], errors: list[str]) -> None:
    block = data.get("preserved")
    if not isinstance(block, Mapping):
        errors.append("preserved: missing or not a mapping")
        return
    _exact(block.get("xasset_0024_section_k_1_reading"),
           "UNRESOLVED_NEITHER_RESOLVED_NOR_RELIED_UPON",
           "preserved.xasset_0024_section_k_1_reading", errors)
    _exact(block.get("xasset_0024_section_j_12"), "NOT_YET_DETERMINABLE_DEFERRED",
           "preserved.xasset_0024_section_j_12", errors)
    _exact(block.get("representation_posture"), "SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED",
           "preserved.representation_posture", errors)
    _exact(block.get("family_slot_grid_status"),
           "CLASSIFICATION_SCAFFOLD_NOT_A_CONSTRUCTION_UNIVERSE",
           "preserved.family_slot_grid_status", errors)
    _exact(block.get("application_authority"), "WITHHELD",
           "preserved.application_authority", errors)
    for key in (
        "representation_rule_created",
        "cm_14_through_cm_17_designated",
        "family_slot_grid_is_a_trial_ceiling",
        "stage_2_authorized",
        "level1_endpoint_authority_exercised",
        "risk_0001_artifacts_accessed",
        "risk_reuse_authorized",
    ):
        _false(block.get(key), f"preserved.{key}", errors)


def _validate_zero_parameters(data: Mapping[str, Any], errors: list[str]) -> None:
    block = data.get("consequential_parameter_registry")
    if not isinstance(block, Mapping):
        errors.append("consequential_parameter_registry: missing or not a mapping")
        return
    if block.get("parameters") != []:
        errors.append(
            "consequential_parameter_registry.parameters: must be empty; introducing a parameter "
            "requires a separately accepted governance amendment"
        )
    declaration = block.get("zero_parameter_declaration")
    if not isinstance(declaration, Mapping):
        errors.append("consequential_parameter_registry.zero_parameter_declaration: missing")
        return
    _true(declaration.get("introduces_zero_consequential_numeric_parameters"),
          "zero_parameter_declaration.introduces_zero_consequential_numeric_parameters", errors)


def _validate_non_authorization(data: Mapping[str, Any], errors: list[str]) -> None:
    block = data.get("non_authorization")
    if not isinstance(block, Mapping):
        errors.append("non_authorization: missing or not a mapping")
        return
    if not block:
        errors.append("non_authorization: must not be empty")
    for key, value in block.items():
        if value is not False:
            errors.append(f"non_authorization.{key}: must be exactly false, found {value!r}")


def _is_disclosed_quotation(where: str) -> bool:
    """True only for the verbatim-quotation field of a disclosed finding.

    Disclosing defective text requires reproducing it, so exactly one field path is exempt from the
    closure-claim scan: `disclosed_findings[N].observed_text`. The exemption is deliberately narrow.
    It does NOT extend to any other field, to any other block, or to the permanence, percentage, or
    barred-numeral scans, all of which continue to apply to quoted text as well.
    """
    return bool(re.fullmatch(r"disclosed_findings\[\d+\]\.observed_text", where))


def _validate_language_firewall(data: Mapping[str, Any], errors: list[str]) -> None:
    """Reject overclaimed permanence, closure claims, endpoint-shaped values, and barred numerals."""
    for where, text in _walk_strings(data):
        lowered = text.lower()

        for banned in BANNED_PERMANENCE_PHRASES:
            if banned in lowered:
                errors.append(
                    f"{where}: {banned!r} asserts a permanent impossibility this determination has "
                    "no authority to establish; record what cannot be done under present authority "
                    "instead"
                )

        if not _is_disclosed_quotation(where):
            for banned in BANNED_CLOSURE_CLAIMS:
                if banned in lowered:
                    errors.append(
                        f"{where}: {banned!r} would let a reader treat the construction universe or "
                        "the qualitative search surface as closed; neither is closed"
                    )

        if PERCENT_SHAPED.search(text):
            errors.append(
                f"{where}: an endpoint-shaped percentage may not appear in this determination"
            )

        for numeral in BARRED_HISTORICAL_NUMERALS:
            if numeral in text:
                errors.append(
                    f"{where}: {numeral!r} is a barred historical output under XASSET-0020 SS-M and "
                    "may never be reproduced"
                )


def _validate_findings(data: Mapping[str, Any], errors: list[str]) -> None:
    findings = data.get("disclosed_findings")
    if not isinstance(findings, Sequence) or isinstance(findings, (str, bytes)):
        errors.append("disclosed_findings: must be a list")
        return
    ids = {entry.get("id") for entry in findings if isinstance(entry, Mapping)}
    if "FINDING_1_STALE_SEARCH_SURFACE_SENTENCE_IN_CANONICAL_PREREGISTRATION" not in ids:
        errors.append(
            "disclosed_findings: the stale canonical-preregistration sentence must remain disclosed"
        )
    for index, entry in enumerate(findings):
        if not isinstance(entry, Mapping):
            errors.append(f"disclosed_findings[{index}]: not a mapping")
            continue
        _nonempty_str(entry.get("not_corrected_because"),
                      f"disclosed_findings[{index}].not_corrected_because", errors)


def validate_determination_data(data: Any) -> list[str]:
    """Validate an already-loaded determination document. Returns a list of errors."""
    errors: list[str] = []
    if not isinstance(data, Mapping):
        return ["determination document: top level must be a mapping"]
    _validate_identity(data, errors)
    _validate_determination(data, errors)
    _validate_canonical_files(data, errors)
    _validate_closure_test(data, errors)
    _validate_routes(data, errors)
    _validate_prerequisites(data, errors)
    _validate_preserved(data, errors)
    _validate_zero_parameters(data, errors)
    _validate_non_authorization(data, errors)
    _validate_findings(data, errors)
    _validate_language_firewall(data, errors)
    return errors


def validate_determination_file(path: Path = DETERMINATION_PATH) -> list[str]:
    if not path.exists():
        return [f"{path}: determination artifact is missing"]
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # pragma: no cover - exercised by a dedicated test
        return [f"{path}: could not be parsed as YAML: {exc}"]
    except OSError as exc:  # pragma: no cover - exercised by a dedicated test
        return [f"{path}: could not be read: {exc}"]
    return validate_determination_data(data)


def main() -> int:
    errors = validate_determination_file()
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print(
        "OK (construction universe NOT CLOSED; prerequisite required; Stage 1 NOT EXECUTABLE; "
        f"{total_slot_count()} family slots remain a classification scaffold, "
        f"{comparison_scoped_slot_count()} of them additionally blocked by the missing comparator "
        "rule)"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
