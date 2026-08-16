"""Deterministic generator and structural validator for the ENDPOINT-0001 construction universe.

Authorized by governance/decisions/XASSET-0028-concrete-construction-universe-closure-determination.md

Read-only and mechanical. This module (a) generates the closed ENDPOINT-0001 Stage-1 construction
universe from already-accepted closed vocabularies, and (b) validates the XASSET-0028 determination
artifact at research/level1_construction_universe/CLOSURE_DETERMINATION_V1.yaml against it.

WHAT THE CLOSURE BASIS IS
-------------------------
XASSET-0027 SS-I.1 records that a provenance family is "a classification of provenance, not a
hypothesis", and names the dimensions that can inhabit one family: source identities, source
architectures, COMPARATOR ARCHITECTURES, evidence forms, external impositions, calibrations,
governance selections, provisional guardrails, and prescribed derivations. Of those, external
impositions / calibrations / governance selections / provisional guardrails / prescribed derivations
are exactly the five already-closed (route, NUM-0001 class) families; evidence form is representation,
preserved as a downstream gate rather than an identity dimension; and source identity is what Stage 1
searches for rather than something a registry can fix without enumerating every institution on earth.

That leaves comparator architecture as the one open identity dimension, and it is NOT open in accepted
authority -- XASSET-0020 SS-H already closes the direct-comparison contract:

  * exactly six unordered sleeve-sleeve pair records ("4 choose 2", binding); and
  * "Each of the four sleeves must also be compared directly with UNSIZED_UNASSIGNED_CAPITAL."

The accepted preregistration's own driver_class_scope block already partitions the six XASSET-0020
SS-E.1 DRIVER classes by evidence-item scope, and this module reproduces that partition rather than
inventing one:

  * ONE_SLEEVE                              -> portfolio_function, sleeve_deployability
  * ONE_UNORDERED_PAIR                       -> diversification_cobehavior
  * COMPARISON_SCOPED_COMPARATOR_NOT_FIXED   -> valuation_opportunity_cost, downside_path_risk,
                                                recovery

Crossing that partition with SS-H's closed comparison contract fixes each DRIVER class's comparator
architecture set exactly, without supplying any new comparator rule:

  * a ONE_SLEEVE class has no comparator                          -> 1 architecture  (SELF)
  * a ONE_UNORDERED_PAIR class ranges over SS-H's pair space, in
    which a given sleeve appears in exactly three pairs           -> 3 architectures (PAIR__*)
  * a COMPARISON_SCOPED class's "direct alternative" ranges over
    SS-H's mandated direct comparisons for that sleeve: the three
    other sleeves and UNSIZED_UNASSIGNED_CAPITAL                  -> 4 architectures (ALT__*)

UNSIZED_UNASSIGNED_CAPITAL is deliberately NOT a diversification_cobehavior comparator. SS-H's UAC
comparison is not a pair record and carries its own separate conclusion vocabulary, and the accepted
scope for that class is ONE_UNORDERED_PAIR. Registering a comparator the accepted contract does not
admit would be inventing a construction rather than enumerating one.

This closure basis is stated, non-outcome-aware (it is derived from evidence-item scope and the
comparison contract, never from which answer is wanted), non-economic (it enumerates SS-H's mandated
comparisons and selects, ranks, prefers, or excludes no sleeve or comparator), deterministic, and
byte-identically reproducible.

WHAT THIS MODULE CANNOT DO
--------------------------
It decides nothing. It cannot execute Stage 1, admit evidence, supply an endpoint, bound, point,
range, percentage, weight, target, or allocation, prefer a sleeve, resolve XASSET-0024 SS-K.1, decide
SS-J.12, supply a representation rule, or grant application authority.

Zero import coupling with allocate.py and margin_state.py in either direction. It imports the accepted
XASSET-0027 preregistration validator read-only so that the closed vocabularies and the contamination
firewall are the real accepted ones rather than literals repeated here.
"""

from __future__ import annotations

import hashlib
import json
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
PROTOCOL_PATH = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
PREREGISTRATION_PATH = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"

# ---------------------------------------------------------------------------------------------
# Predecessor (historical) and successor (effective) canonical identity.
#
# The XASSET-0027 pins are preserved verbatim as historical predecessor identity and are never
# rewritten. XASSET-0028 amends the canonical bytes under its own successor authority, so the
# effective pins are recomputed from observed bytes rather than pinned as literals here -- a literal
# would have to be edited in the same commit that changes the bytes it claims to verify, which is not
# a check. The determination artifact carries the effective digests, and this module verifies them
# against the real files.
# ---------------------------------------------------------------------------------------------
PREDECESSOR_PINS = {
    "research/level1_endpoint_evidence/PROTOCOL_V1.md": (
        "1a7b288718dfc688adb409ea9ecdf0fe5c858a32ee154f4f407c132895f41c8b"
    ),
    "research/level1_endpoint_evidence/pre_registration.yaml": (
        "bb25b1181c94d4dba2939a634b6fcb894f93597a664d5e91ffdcf021de3d385f"
    ),
}

REQUIRED_STATUS = "CLOSED"

# ---------------------------------------------------------------------------------------------
# Closed vocabularies. Every one is sourced from the accepted preregistration validator rather than
# restated, so a drift in accepted authority surfaces as an import-time mismatch instead of silently
# diverging.
# ---------------------------------------------------------------------------------------------
SLEEVES: tuple[str, ...] = tuple(PREREG.SLEEVES)
BOUNDS: tuple[str, ...] = tuple(PREREG.BOUNDS)
DRIVER_CLASSES: tuple[str, ...] = tuple(PREREG.DRIVER_CLASSES)
FAMILY_IDS: tuple[str, ...] = tuple(f[0] for f in PREREG.CONSTRUCTION_FAMILIES)
FAMILY_ROUTE: dict[str, str] = {f[0]: f[1] for f in PREREG.CONSTRUCTION_FAMILIES}
FAMILY_NUM_0001_CLASS: dict[str, int] = {f[0]: f[2] for f in PREREG.CONSTRUCTION_FAMILIES}

UNASSIGNED = "UNSIZED_UNASSIGNED_CAPITAL"

# XASSET-0020 SS-E.1 evidence-item scope, as already recorded in the accepted preregistration's
# driver_class_scope block. Reproduced here as the generator's switch, and cross-checked against the
# canonical file by check_scope_partition_matches_canonical().
SCOPE_ONE_SLEEVE = "ONE_SLEEVE"
SCOPE_ONE_UNORDERED_PAIR = "ONE_UNORDERED_PAIR"
SCOPE_COMPARISON = "COMPARISON_SCOPED_COMPARATOR_NOT_FIXED"

DRIVER_CLASS_SCOPE: dict[str, str] = {
    "portfolio_function": SCOPE_ONE_SLEEVE,
    "valuation_opportunity_cost": SCOPE_COMPARISON,
    "downside_path_risk": SCOPE_COMPARISON,
    "recovery": SCOPE_COMPARISON,
    "diversification_cobehavior": SCOPE_ONE_UNORDERED_PAIR,
    "sleeve_deployability": SCOPE_ONE_SLEEVE,
}

# Comparison-subject kinds. Closed.
SUBJECT_SLEEVE_SELF = "SLEEVE_SELF"
SUBJECT_UNORDERED_PAIR = "UNORDERED_PAIR"
SUBJECT_DIRECT_ALTERNATIVE = "DIRECT_ALTERNATIVE"

SUBJECT_KIND_BY_SCOPE = {
    SCOPE_ONE_SLEEVE: SUBJECT_SLEEVE_SELF,
    SCOPE_ONE_UNORDERED_PAIR: SUBJECT_UNORDERED_PAIR,
    SCOPE_COMPARISON: SUBJECT_DIRECT_ALTERNATIVE,
}

# Source-architecture posture. Every construction SPANS both accepted source architectures rather
# than fixing one, so this is deliberately NOT an identity dimension. Making it one would either
# double the universe with a hypothetical twin of every construction whose existing-source answer
# XASSET-0025 Outcome C already settled, or force enumeration of arbitrary institution names -- the
# unbounded qualitative search this unit exists to remove. A construction fixes the question, the
# sleeve, the bound, the DRIVER class, the provenance family, and the comparator architecture;
# whether a qualifying source already exists or comes to exist later is exactly what Stage 1
# evaluates, and it is what the categorical/prerequisite distinction of XASSET-0027 SS-I.3 separates.
SOURCE_ARCHITECTURE_SCOPE = "SPANS_" + "_AND_".join(PREREG.SOURCE_ARCHITECTURES)

# Representation is preserved as a downstream dependency and gate (G9), never an identity dimension,
# per XASSET-0026 SS-I item 8 and XASSET-0027's conformance table.
REPRESENTATION_POSTURE = "SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED"

# R2 is the source-prescribed-derivation route. XASSET-0023 SS-H.3 item 3 bars an APPLICATION from
# composing a derivation the sources do not prescribe ("composing one is authorship, not derivation").
# It does not bar preregistering the hypothesis that a qualifying source must itself prescribe one.
# Every R2 construction therefore carries this source requirement and composes nothing.
R2_FAMILY_ID = "R2_C2"
R2_SOURCE_REQUIREMENT = (
    "The qualifying source must itself prescribe exactly one lawful XASSET-0023 SS-H.3 derivation, "
    "using admitted DRIVER inputs and closed arithmetic only. This construction states a requirement "
    "on the source and composes, selects among, or invents no derivation."
)
R1_SOURCE_REQUIREMENT = (
    "The qualifying source must itself uniquely state the bound under XASSET-0023 SS-H.2, carrying "
    "this family's NUM-0001 class from competent stating authority. This construction states a "
    "requirement on the source and originates no value."
)

ID_SEPARATOR = "::"

# Reused from XASSET-0027's own correction after independent review: phrasing that asserts permanent
# impossibility rather than a bound on present authority.
BANNED_PERMANENCE_PHRASES = (
    "closeable only",
    "can never",
    "could never",
    "is impossible",
    "permanently foreclosed",
    "no future",
)

# Phrasing a Stage-1 runner could act on as though operational authorization already existed.
BANNED_EXECUTION_CLAIMS = (
    "stage 1 is authorized",
    "stage 1 is now authorized",
    "stage 1 may begin",
    "stage 1 may now begin",
    "execution is authorized",
    "begin stage 1",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# =============================================================================================
# Contamination firewall -- reused, never re-implemented
# =============================================================================================
def scan_for_barred_content(text: str, where: str) -> tuple[str, ...]:
    """Delegate to the accepted XASSET-0027 firewall.

    MINOR 2 of review 4945473310 found a locally re-declared barred-numeral tuple that omitted one of
    the accepted validator's five historical values, and a percentage regex narrower than the accepted
    endpoint-shaped scan. Rather than resynchronise two copies, this module calls the accepted
    firewall directly, so it can never again be weaker than its predecessor.
    """
    return PREREG.scan_for_barred_content(text, where)


def _walk_strings(node: Any, path: str = "$"):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, Mapping):
        for key, value in node.items():
            yield from _walk_strings(value, f"{path}.{key}")
    elif isinstance(node, Sequence) and not isinstance(node, (str, bytes)):
        for index, value in enumerate(node):
            yield from _walk_strings(value, f"{path}[{index}]")


# =============================================================================================
# The generator
# =============================================================================================
def comparator_architectures(sleeve: str, driver_class: str) -> tuple[tuple[str, str | None], ...]:
    """Return the closed (architecture_id, counterpart) list for one sleeve and DRIVER class.

    Pure. Ordering is canonical sleeve order for sleeve counterparts, with UNSIZED_UNASSIGNED_CAPITAL
    last, so the enumeration is deterministic and no ordering can imply preference.
    """
    if sleeve not in SLEEVES:
        raise ValueError(f"unknown sleeve {sleeve!r}")
    if driver_class not in DRIVER_CLASS_SCOPE:
        raise ValueError(f"unknown driver class {driver_class!r}")

    scope = DRIVER_CLASS_SCOPE[driver_class]
    others = tuple(s for s in SLEEVES if s != sleeve)

    if scope == SCOPE_ONE_SLEEVE:
        return (("SELF", None),)
    if scope == SCOPE_ONE_UNORDERED_PAIR:
        # XASSET-0020 SS-H closes this space at the six unordered pairs; a given sleeve appears in
        # exactly three of them. UNSIZED_UNASSIGNED_CAPITAL is absent by construction: the SS-H UAC
        # comparison is not a pair record and this class's accepted scope is ONE_UNORDERED_PAIR.
        return tuple((f"PAIR__{other}", other) for other in others)
    if scope == SCOPE_COMPARISON:
        # SS-E.1's "the direct alternative", ranging over exactly the direct comparisons SS-H mandates
        # for this sleeve: the three other sleeves, and UNSIZED_UNASSIGNED_CAPITAL.
        return tuple((f"ALT__{other}", other) for other in others) + (
            (f"ALT__{UNASSIGNED}", UNASSIGNED),
        )
    raise ValueError(f"unhandled scope {scope!r}")


def unordered_pair_id(a: str, b: str) -> str:
    """Return XASSET-0020 SS-H's canonical unordered pair id for two sleeves."""
    first, second = sorted((a, b), key=SLEEVES.index)
    return f"{first}__{second}"


def _evidence_proposition(
    sleeve: str, bound: str, driver_class: str, family_id: str, counterpart: str | None
) -> str:
    """Deterministically generate the construction's exact evidence question.

    Generated from closed identity only. No free text is authored at results time, so two executors
    handed the same construction id necessarily test the same hypothesis.
    """
    route_clause = (
        "prescribes exactly one derivation of"
        if family_id == R2_FAMILY_ID
        else "uniquely states"
    )
    if counterpart is None:
        subject = f"the {sleeve} sleeve's own {driver_class} evidence"
    elif counterpart == UNASSIGNED:
        subject = (
            f"{driver_class} evidence directly comparing the {sleeve} sleeve with "
            f"{UNASSIGNED}"
        )
    elif DRIVER_CLASS_SCOPE[driver_class] == SCOPE_ONE_UNORDERED_PAIR:
        subject = (
            f"direct {driver_class} pair evidence for the unordered pair "
            f"{unordered_pair_id(sleeve, counterpart)}"
        )
    else:
        subject = (
            f"{driver_class} evidence directly comparing the {sleeve} sleeve with the "
            f"{counterpart} sleeve as the direct alternative"
        )
    return (
        f"Does there exist a source, admissible under the ENDPOINT-0001 evidence-admission contract, "
        f"which {route_clause} a {bound} bound on the {sleeve} sleeve's share of the normalized asset "
        f"unit, on the basis of {subject}, with provenance family {family_id}?"
    )


def construction_id(
    sleeve: str, bound: str, driver_class: str, family_id: str, architecture_id: str
) -> str:
    return ID_SEPARATOR.join((sleeve, bound, driver_class, family_id, architecture_id))


def cell_id(sleeve: str, bound: str, driver_class: str) -> str:
    return ID_SEPARATOR.join((sleeve, bound, driver_class))


def generate_construction_universe() -> tuple[dict[str, Any], ...]:
    """Generate the complete, closed ENDPOINT-0001 Stage-1 construction universe.

    Pure and deterministic: no clock, no randomness, no filesystem read, no environment. Repeated
    calls return byte-identical content in identical order.
    """
    universe: list[dict[str, Any]] = []
    ordinal = 0
    for sleeve in SLEEVES:
        for bound in BOUNDS:
            for driver_class in DRIVER_CLASSES:
                scope = DRIVER_CLASS_SCOPE[driver_class]
                for family_id in FAMILY_IDS:
                    for architecture_id, counterpart in comparator_architectures(
                        sleeve, driver_class
                    ):
                        ordinal += 1
                        record: dict[str, Any] = {
                            "ordinal": ordinal,
                            "construction_id": construction_id(
                                sleeve, bound, driver_class, family_id, architecture_id
                            ),
                            "cell_id": cell_id(sleeve, bound, driver_class),
                            "sleeve": sleeve,
                            "bound": bound,
                            "driver_class": driver_class,
                            "driver_class_scope": scope,
                            "family_id": family_id,
                            "route": FAMILY_ROUTE[family_id],
                            "num_0001_class": FAMILY_NUM_0001_CLASS[family_id],
                            "comparison_subject_kind": SUBJECT_KIND_BY_SCOPE[scope],
                            "comparator_architecture": architecture_id,
                            "counterpart": counterpart,
                            "unordered_pair_id": (
                                unordered_pair_id(sleeve, counterpart)
                                if scope == SCOPE_ONE_UNORDERED_PAIR
                                else None
                            ),
                            "source_architecture_scope": SOURCE_ARCHITECTURE_SCOPE,
                            "evidence_proposition": _evidence_proposition(
                                sleeve, bound, driver_class, family_id, counterpart
                            ),
                            "source_requirement": (
                                R2_SOURCE_REQUIREMENT
                                if family_id == R2_FAMILY_ID
                                else R1_SOURCE_REQUIREMENT
                            ),
                            "representation_posture": REPRESENTATION_POSTURE,
                            "governing_authority_refs": (
                                "XASSET-0020_SECTION_E1",
                                "XASSET-0020_SECTION_H",
                                "XASSET-0023_SECTION_H",
                                "XASSET-0024_SECTION_C",
                                "XASSET-0027_SECTION_I",
                                "XASSET-0028",
                            ),
                        }
                        universe.append(record)
    return tuple(universe)


def canonical_universe_json(universe: Sequence[Mapping[str, Any]]) -> str:
    """Canonical JSON serialization used for the aggregate identity hash."""
    return json.dumps(universe, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def universe_aggregate_sha256(universe: Sequence[Mapping[str, Any]] | None = None) -> str:
    """SHA-256 over the canonical serialization of the complete generated universe."""
    if universe is None:
        universe = generate_construction_universe()
    return hashlib.sha256(canonical_universe_json(universe).encode("utf-8")).hexdigest()


def derived_cardinality() -> int:
    """Cardinality derived from the closed dimensions, never a written literal."""
    per_sleeve_bound_family = sum(
        len(comparator_architectures(SLEEVES[0], driver_class))
        for driver_class in DRIVER_CLASSES
    )
    return len(SLEEVES) * len(BOUNDS) * len(FAMILY_IDS) * per_sleeve_bound_family


def per_cell_cardinality() -> dict[str, int]:
    """Registered construction count for each of the 48 cells."""
    counts: dict[str, int] = {}
    for record in generate_construction_universe():
        counts[record["cell_id"]] = counts.get(record["cell_id"], 0) + 1
    return counts


def check_scope_partition_matches_canonical(path: Path | None = None) -> tuple[str, ...]:
    """Cross-check the generator's scope switch against the canonical preregistration bytes.

    The partition is the generator's single most load-bearing input. Reading it back from the
    canonical file makes a silent divergence impossible.
    """
    path = path or PREREGISTRATION_PATH
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return (f"driver_class_scope: canonical preregistration unreadable: {exc}",)
    classes = (data or {}).get("driver_class_scope", {}).get("classes")
    if not isinstance(classes, Mapping):
        return ("driver_class_scope: canonical block missing or malformed",)
    for driver_class, expected in sorted(DRIVER_CLASS_SCOPE.items()):
        entry = classes.get(driver_class)
        if not isinstance(entry, Mapping):
            errors.append(f"driver_class_scope: canonical entry for {driver_class!r} missing")
            continue
        observed = entry.get("minimum_evidence_item_scope")
        if observed != expected:
            errors.append(
                f"driver_class_scope: {driver_class!r} canonical scope is {observed!r} but the "
                f"generator assumes {expected!r}"
            )
    for driver_class in classes:
        if driver_class not in DRIVER_CLASS_SCOPE:
            errors.append(
                f"driver_class_scope: canonical file declares unknown DRIVER class {driver_class!r}"
            )
    return tuple(errors)


# =============================================================================================
# Determination-artifact validation
# =============================================================================================
class ValidationResult:
    def __init__(self, ok: bool, errors: tuple[str, ...]):
        self.ok = ok
        self.errors = errors

    def __bool__(self) -> bool:  # pragma: no cover - trivial
        return self.ok


def _nonempty_str(value: Any, where: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{where}: must be a non-empty string")


def _true(value: Any, where: str, errors: list[str]) -> None:
    if value is not True:
        errors.append(f"{where}: must be true")


def _false(value: Any, where: str, errors: list[str]) -> None:
    if value is not False:
        errors.append(f"{where}: must be false")


TOP_KEYS = (
    "determination_id",
    "authorizing_decision",
    "status",
    "closure_basis",
    "closed_dimensions",
    "comparator_contract",
    "universe_identity",
    "per_cell_cardinality",
    "canonical_amendment",
    "stage_1",
    "preserved_postures",
    "prohibited_scope",
)


def validate(data: Mapping[str, Any]) -> ValidationResult:
    """Validate the parsed determination artifact against the closed schema and the generator."""
    errors: list[str] = []
    if not isinstance(data, Mapping):
        return ValidationResult(False, ("determination: top level must be a mapping",))

    missing = [key for key in TOP_KEYS if key not in data]
    extra = [key for key in data if key not in TOP_KEYS]
    for key in missing:
        errors.append(f"determination: required key {key!r} missing")
    for key in extra:
        errors.append(f"determination: unknown key {key!r}")
    if missing:
        return ValidationResult(False, tuple(errors))

    _nonempty_str(data.get("determination_id"), "determination_id", errors)
    if data.get("authorizing_decision") != "XASSET-0028":
        errors.append("authorizing_decision: must be 'XASSET-0028'")
    if data.get("status") != REQUIRED_STATUS:
        errors.append(f"status: must be {REQUIRED_STATUS!r}")

    _validate_closed_dimensions(data.get("closed_dimensions"), errors)
    _validate_comparator_contract(data.get("comparator_contract"), errors)
    _validate_universe_identity(data.get("universe_identity"), errors)
    _validate_per_cell(data.get("per_cell_cardinality"), errors)
    _validate_stage_1(data.get("stage_1"), errors)
    _validate_preserved_postures(data.get("preserved_postures"), errors)
    _validate_canonical_amendment(data.get("canonical_amendment"), errors)
    _scan_text(data, errors)

    return ValidationResult(not errors, tuple(errors))


def _validate_closed_dimensions(block: Any, errors: list[str]) -> None:
    if not isinstance(block, Mapping):
        errors.append("closed_dimensions: must be a mapping")
        return
    expected = {
        "sleeves": list(SLEEVES),
        "bounds": list(BOUNDS),
        "driver_classes": list(DRIVER_CLASSES),
        "provenance_families": list(FAMILY_IDS),
    }
    for key, want in expected.items():
        got = block.get(key)
        if list(got or []) != want:
            errors.append(f"closed_dimensions.{key}: must equal the accepted closed vocabulary")


def _validate_comparator_contract(block: Any, errors: list[str]) -> None:
    if not isinstance(block, Mapping):
        errors.append("comparator_contract: must be a mapping")
        return
    _true(block.get("enumerates_xasset_0020_section_h_only"),
          "comparator_contract.enumerates_xasset_0020_section_h_only", errors)
    _false(block.get("supplies_a_new_comparator_rule"),
           "comparator_contract.supplies_a_new_comparator_rule", errors)
    _false(block.get("unassigned_capital_is_a_diversification_cobehavior_comparator"),
           "comparator_contract.unassigned_capital_is_a_diversification_cobehavior_comparator",
           errors)
    scope = block.get("driver_class_scope")
    if not isinstance(scope, Mapping) or dict(scope) != DRIVER_CLASS_SCOPE:
        errors.append(
            "comparator_contract.driver_class_scope: must reproduce the canonical scope partition"
        )
    counts = block.get("architectures_per_driver_class")
    want_counts = {
        driver_class: len(comparator_architectures(SLEEVES[0], driver_class))
        for driver_class in DRIVER_CLASSES
    }
    if not isinstance(counts, Mapping) or dict(counts) != want_counts:
        errors.append(
            "comparator_contract.architectures_per_driver_class: must equal the generated counts"
        )


def _validate_universe_identity(block: Any, errors: list[str]) -> None:
    if not isinstance(block, Mapping):
        errors.append("universe_identity: must be a mapping")
        return
    universe = generate_construction_universe()
    if block.get("registered_construction_count") != len(universe):
        errors.append(
            "universe_identity.registered_construction_count: must equal the generated cardinality"
        )
    if block.get("derived_cardinality") != derived_cardinality():
        errors.append("universe_identity.derived_cardinality: must equal the derived cardinality")
    if block.get("aggregate_sha256") != universe_aggregate_sha256(universe):
        errors.append(
            "universe_identity.aggregate_sha256: must equal the SHA-256 of the canonical "
            "serialization of the generated universe"
        )
    _true(block.get("deterministic"), "universe_identity.deterministic", errors)
    _true(block.get("byte_identically_reproducible"),
          "universe_identity.byte_identically_reproducible", errors)
    _true(block.get("frozen_before_stage_1_outcomes"),
          "universe_identity.frozen_before_stage_1_outcomes", errors)
    _false(block.get("executor_may_add_or_omit_a_construction"),
           "universe_identity.executor_may_add_or_omit_a_construction", errors)
    if block.get("generator") != "level1_construction_universe_closure_validator."\
                                 "generate_construction_universe":
        errors.append("universe_identity.generator: must name the generator function")


def _validate_per_cell(block: Any, errors: list[str]) -> None:
    if not isinstance(block, Mapping):
        errors.append("per_cell_cardinality: must be a mapping")
        return
    want = per_cell_cardinality()
    if dict(block) != want:
        errors.append(
            "per_cell_cardinality: must equal the generated per-cell counts for all "
            f"{len(want)} cells"
        )


def _validate_stage_1(block: Any, errors: list[str]) -> None:
    if not isinstance(block, Mapping):
        errors.append("stage_1: must be a mapping")
        return
    _true(block.get("construction_universe_structurally_closed"),
          "stage_1.construction_universe_structurally_closed", errors)
    _false(block.get("operationally_authorized"), "stage_1.operationally_authorized", errors)
    _false(block.get("executed_by_this_unit"), "stage_1.executed_by_this_unit", errors)
    required = (
        "INDEPENDENT_FULL_EXACT_HEAD_REVIEW",
        "PRINCIPAL_EXACT_HEAD_ACCEPTANCE",
        "MERGE",
        "POST_MERGE_VERIFICATION",
        "MERGE_COMMIT_CI_SUCCESS",
    )
    gates = block.get("effectivity_gates")
    for gate in required:
        if gate not in (gates or ()):
            errors.append(f"stage_1.effectivity_gates: must include {gate!r}")


def _validate_preserved_postures(block: Any, errors: list[str]) -> None:
    if not isinstance(block, Mapping):
        errors.append("preserved_postures: must be a mapping")
        return
    if block.get("xasset_0024_section_k1") != "UNRESOLVED_BOTH_READINGS_PRESERVED":
        errors.append("preserved_postures.xasset_0024_section_k1: SS-K.1 must remain unresolved")
    if block.get("section_j12") != "DEFERRED":
        errors.append("preserved_postures.section_j12: SS-J.12 must remain deferred")
    if block.get("representation") != REPRESENTATION_POSTURE:
        errors.append(f"preserved_postures.representation: must be {REPRESENTATION_POSTURE!r}")
    if block.get("stage_2") != "NOT_AUTHORIZED":
        errors.append("preserved_postures.stage_2: must be NOT_AUTHORIZED")
    if block.get("application_authority") != "WITHHELD":
        errors.append("preserved_postures.application_authority: must be WITHHELD")
    if block.get("risk_0001_reuse") != "PROHIBITED_NOT_ACCESSED":
        errors.append("preserved_postures.risk_0001_reuse: must be PROHIBITED_NOT_ACCESSED")


def _validate_canonical_amendment(block: Any, errors: list[str]) -> None:
    if not isinstance(block, Mapping):
        errors.append("canonical_amendment: must be a mapping")
        return
    predecessor = block.get("predecessor_pins")
    if not isinstance(predecessor, Mapping) or dict(predecessor) != PREDECESSOR_PINS:
        errors.append(
            "canonical_amendment.predecessor_pins: must preserve the XASSET-0027 pins verbatim"
        )
    successor = block.get("successor_pins")
    if not isinstance(successor, Mapping):
        errors.append("canonical_amendment.successor_pins: must be a mapping")
        return
    for rel, digest in sorted(successor.items()):
        path = ROOT / rel
        if not path.exists():
            errors.append(f"canonical_amendment.successor_pins: {rel} does not exist")
            continue
        observed = sha256_file(path)
        if observed != digest:
            errors.append(
                f"canonical_amendment.successor_pins: {rel} observed digest {observed} does not "
                f"match the recorded successor pin {digest}"
            )
    for rel in PREDECESSOR_PINS:
        if rel not in successor:
            errors.append(f"canonical_amendment.successor_pins: {rel} missing")
        elif successor.get(rel) == PREDECESSOR_PINS[rel]:
            errors.append(
                f"canonical_amendment.successor_pins: {rel} is unchanged from the predecessor pin, "
                "but this amendment must change the canonical bytes"
            )
    if block.get("predecessor_authority") != "XASSET-0027":
        errors.append("canonical_amendment.predecessor_authority: must be 'XASSET-0027'")
    if block.get("successor_authority") != "XASSET-0028":
        errors.append("canonical_amendment.successor_authority: must be 'XASSET-0028'")
    _true(block.get("historical_predecessor_identity_preserved"),
          "canonical_amendment.historical_predecessor_identity_preserved", errors)
    _false(block.get("rewrites_accepted_history"),
           "canonical_amendment.rewrites_accepted_history", errors)


def _validate_prohibited_scope(data: Mapping[str, Any], errors: list[str]) -> None:
    required = (
        "STAGE_1_EXECUTION",
        "STAGE_2_AUTHORIZATION",
        "ENDPOINT_VALUE_OF_ANY_KIND",
        "SLEEVE_PREFERENCE_OR_RANKING",
        "APPLICATION_AUTHORITY",
        "RISK_0001_REUSE",
    )
    scope = data.get("prohibited_scope") or ()
    for item in required:
        if item not in scope:
            errors.append(f"prohibited_scope: must include {item!r}")


def _scan_text(data: Mapping[str, Any], errors: list[str]) -> None:
    _validate_prohibited_scope(data, errors)
    for where, text in _walk_strings(data):
        errors.extend(scan_for_barred_content(text, where))
        lowered = text.lower()
        for phrase in BANNED_PERMANENCE_PHRASES:
            if phrase in lowered:
                errors.append(
                    f"{where}: {phrase!r} asserts permanent impossibility rather than a bound on "
                    "present authority"
                )
        for phrase in BANNED_EXECUTION_CLAIMS:
            if phrase in lowered:
                errors.append(
                    f"{where}: {phrase!r} would let a reader treat Stage 1 as operationally "
                    "authorized; structural closure is not authorization"
                )


def validate_file(path: Path | None = None) -> ValidationResult:
    path = path or DETERMINATION_PATH
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return ValidationResult(False, (f"determination: unreadable: {exc}",))
    except yaml.YAMLError as exc:
        return ValidationResult(False, (f"determination: not parseable as YAML: {exc}",))
    result = validate(data if isinstance(data, Mapping) else {})
    scope_errors = check_scope_partition_matches_canonical()
    if scope_errors:
        return ValidationResult(False, result.errors + scope_errors)
    return result


def main(argv: Sequence[str] | None = None) -> int:  # pragma: no cover - CLI
    result = validate_file()
    if result.ok:
        universe = generate_construction_universe()
        print(
            f"OK ({len(universe)} registered constructions across "
            f"{len(per_cell_cardinality())} cells)"
        )
        return 0
    for error in result.errors:
        print(f"ERROR {error}")
    return 1


if __name__ == "__main__":  # pragma: no cover - CLI
    sys.exit(main(sys.argv[1:]))
