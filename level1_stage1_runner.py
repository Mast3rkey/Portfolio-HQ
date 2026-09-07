"""Deterministic ENDPOINT-0001 Stage-1 runner and result writer.

Created under ``XASSET-0036`` SS-E.3, which authorizes exactly one ``XASSET-0030`` SS-G.B steps-2-7
implementation pass. This module is SS-G.B step 4's "deterministic Stage-1 runner, result
writer/serializer".

WHAT THIS MODULE IS
===================

``XASSET-0030`` SS-B.1 recorded the shape of the problem: everything downstream of the twelve gate
results is already a closed, order-independent composition, and nothing produced the gate results
themselves. This module supplies the deterministic machinery around that gap WITHOUT closing it by
invention.

Concretely, it does three things and refuses a fourth:

1. It traverses the frozen 680-construction universe through the production seam
   (``level1_construction_universe_closure_validator.generate_construction_universe``), in canonical
   order, consuming exactly the registered identities.
2. It supplies mechanically every value accepted authority DETERMINES -- the ``G2`` reading coupling
   from the canonical closed table, ``XASSET-0035`` SS-G's ``UNABLE_TO_DETERMINE`` posture for ``G3``
   and ``G5``, and ``XASSET-0035`` SS-F's pair-consumption classification -- and REFUSES any attempt
   by an executor to override a determined value.
3. It composes gate results into dispositions, cell outcomes, and roll-ups through the accepted
   derivation functions, never through arithmetic of its own.
4. **It invents no economic judgment.** The gate results accepted authority does not determine remain
   the executor's analytical act and must be supplied as inputs. There is no default, no fallback,
   and no "unknown means pass" anywhere in this module.

WHAT THIS MODULE DELIBERATELY DOES NOT ENCODE
=============================================

``XASSET-0030`` SS-E's six closable gates (``G1``, ``G2``, ``G4``, ``G6``, ``G7``, ``G11``) are a
``CURRENT_AUTHORITY_GATE_EVALUATION_SNAPSHOT``, expressly "not permanent gate closure", carrying
per-gate invalidation triggers in SS-E.1. Hard-coding those results here would let a future execution
silently carry a stale determination through the very amendment that changed its basis -- the exact
failure SS-E.1 exists to prevent. They are therefore NOT encoded, NOT defaulted, and NOT applied.
They are executor-supplied like any other undetermined gate.

FAIL-CLOSED AUTHORIZATION
=========================

:func:`run_stage1` and :func:`write_stage1_results` are the two outcome-producing entry points, and
each consults ``level1_stage1_execution_authorization.active_execution_is_authorized`` FIRST --
before any composition, any path resolution, any validation, and any file descriptor. That
predicate succeeds ONLY while the one authorized attempt is EXACTLY ``LANE_CLAIMED`` and its
attestation still authenticates against durable truth. ``READY`` is not enough (the claim has not
been taken) and ``COMPLETED`` is not enough either (the single attempt is spent; recovering a
crashed execution or a lost artifact is a governed act requiring new authority, never an ordinary
re-run). The deliberately broader ``claimed_execution_is_authorized``, true in ``CLAIMED`` or
``COMPLETED``, remains correct for authenticating an already-completed result and is NOT used here.

NEITHER production path has an injection seam. ``run_stage1`` takes only ``analytical_inputs`` and
``provenance``; ``write_stage1_results`` takes only ``document`` and writes only to the canonical
path. There is no authorizer, traversal, cell-universe, or destination parameter to substitute.

Synthetic composition is a separate PRIVATE seam, :func:`_compose_synthetic_stage1_document`, which
refuses a ``None`` traversal and refuses any record or analytical input naming a registered
construction, so it cannot reach a real disposition. :func:`_write_synthetic_results_artifact` is
its writing counterpart and is mechanically barred from the canonical results path. Neither seam
consults or confers authorization: they change no lane state, create no attestation, and claim no
attempt.

Structural, read-only traversal of the frozen universe is separately available through
:func:`verify_frozen_traversal` and :func:`pair_consumption_inventory`, which evaluate no gate,
derive no disposition, and write nothing. ``XASSET-0036`` SS-F.1(a) authorizes exactly that, and
SS-F.1(b) keeps every outcome-producing act prohibited until the lane is lawfully armed and claimed.
"""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import level1_construction_universe_closure_validator as CU
import level1_endpoint_evidence_preregistration_validator as PV

ROOT = Path(__file__).resolve().parent

SCHEMA_VERSION = 2
STUDY_ID = "ENDPOINT-0001"
STAGE_ID = "STAGE_1"
EXECUTION_ATTEMPT_ID = "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

#: Canonical results path, from ``result_schema.results_path``. This module never creates it as a
#: side effect of any other call; only :func:`write_stage1_results` writes, and only with O_EXCL.
RESULTS_RELPATH = "research/level1_endpoint_evidence/stage1_results.yaml"

#: ``XASSET-0035`` SS-G.1: gates whose SATISFACTION is expressly reserved, recorded
#: ``UNABLE_TO_DETERMINE`` under a ``HYPOTHETICAL_SOURCE_ARCHITECTURE`` construction. The executor
#: does not choose this value and may not override it -- SS-G.2 eliminates every other value in the
#: closed four-value vocabulary.
RESERVED_POSTURE_GATES = ("G3_NORMALIZATION", "G5_CONSTRAINT_SHAPE")

#: ``G2`` is never supplied directly. It is derived from the two ``XASSET-0024`` SS-K.1 reading
#: outcomes through the canonical closed table, which ``g2_reading_mapping.coupled_to_g2_gate_result``
#: makes an enforced identity rather than an annotation.
DERIVED_FROM_READINGS_GATE = "G2_MAGNITUDE_INTRINSICALITY"

#: ``G9`` is supplied through its path-1 self-containment declaration rather than as a bare gate
#: result, so that ``XASSET-0035`` SS-G.3's determined/undetermined split cannot be collapsed.
REPRESENTATION_GATE = "G9_REPRESENTATION"

#: Everything the executor must supply directly, in canonical gate order.
EXECUTOR_SUPPLIED_GATES = tuple(
    gate
    for gate in PV.GATE_IDS
    if gate not in RESERVED_POSTURE_GATES
    and gate != DERIVED_FROM_READINGS_GATE
    and gate != REPRESENTATION_GATE
)

#: Closed vocabulary for the executor's ``G9`` path-1 declaration (``XASSET-0035`` SS-G.3).
G9_PATH_1_DECLARATIONS = (
    "SELF_CONTAINED",
    "DETERMINED_NOT_SELF_CONTAINED",
    "UNDETERMINED",
)

#: Closed vocabulary for the basis of a ``G12`` result. ``XASSET-0035`` SS-E.5 preserves the floor
#: that successor nonexistence is never BY ITSELF a ``FAIL`` ground, so that basis may accompany any
#: result except ``FAIL``.
G12_BASES = (
    "LAWFUL_SUCCESSOR_IDENTIFIABLE",
    "SUCCESSOR_NONEXISTENCE_ALONE",
    "NO_LAWFUL_SUCCESSOR_IDENTIFIABLE_ON_INDEPENDENT_GROUNDS",
    "UNDETERMINED",
)

#: Required keys on every executor analytical input.
ANALYTICAL_INPUT_KEYS = (
    "gate_results",
    "g2_outcome_under_subject_matter_reading",
    "g2_outcome_under_preference_only_reading",
    "g9_path_1_declaration",
    "g9_named_dependency",
    "g12_basis",
    "point_or_range_support",
    "uncertainty_statement",
)


class Stage1RunnerError(RuntimeError):
    """Raised when a Stage-1 run is refused. Every refusal is fail-closed."""


# ======================================================================================
# Read-only structural traversal -- XASSET-0036 SS-F.1(a)
#
# Nothing below evaluates a gate, derives a disposition, or writes anything.
# ======================================================================================


def frozen_traversal() -> tuple[Mapping[str, Any], ...]:
    """Return the frozen construction universe through the PRODUCTION seam, in canonical order.

    This is deliberately the same call the runner itself uses, so a structural check of this
    function is a check of the real traversal rather than of a synthetic lookalike.
    """
    return CU.generate_construction_universe()


def _identity_equal(observed: Any, expected: Any) -> bool:
    """Compare two frozen identity values, tolerating only list-vs-tuple container type.

    Order and elements are compared exactly. A reordered sequence, a changed element, an added or
    dropped element, or a different scalar all compare unequal. Strings are never treated as
    sequences here, so ``"AB"`` never equals ``["A", "B"]``.
    """
    observed_is_seq = isinstance(observed, (list, tuple))
    expected_is_seq = isinstance(expected, (list, tuple))
    if observed_is_seq != expected_is_seq:
        return False
    if observed_is_seq and expected_is_seq:
        if len(observed) != len(expected):
            return False
        return all(_identity_equal(a, b) for a, b in zip(observed, expected))
    return bool(observed == expected) and type(observed) is type(expected)


def verify_frozen_traversal(
    traversal: Sequence[Mapping[str, Any]] | None = None,
) -> tuple[bool, tuple[str, ...]]:
    """Structurally verify the production traversal against the frozen universe. READ-ONLY.

    Proves exact coverage, exact canonical ordering, absence of duplicate/missing/extra
    constructions, immutability of the identity fields the traversal shares with the frozen
    universe mapping, and the ``680 / 48 / aggregate-hash`` verification.

    Evaluates no gate, derives no disposition, and writes nothing. Returns ``(ok, errors)`` rather
    than raising, so a caller cannot mistake a structural check for an authorization.
    """
    errors: list[str] = []
    records = tuple(frozen_traversal() if traversal is None else traversal)
    frozen = CU.frozen_construction_universe()

    expected_ids = tuple(frozen)
    actual_ids = tuple(str(record.get("construction_id")) for record in records)

    if len(records) != PV.REGISTERED_CONSTRUCTION_COUNT:
        errors.append(
            f"traversal length {len(records)} != registered construction count "
            f"{PV.REGISTERED_CONSTRUCTION_COUNT}"
        )

    seen: set[str] = set()
    duplicates = []
    for construction_id in actual_ids:
        if construction_id in seen:
            duplicates.append(construction_id)
        seen.add(construction_id)
    if duplicates:
        errors.append(f"duplicate construction ids in traversal: {sorted(set(duplicates))[:5]}")

    missing = [construction_id for construction_id in expected_ids if construction_id not in seen]
    if missing:
        errors.append(f"constructions missing from traversal: {missing[:5]}")
    extra = [construction_id for construction_id in actual_ids if construction_id not in frozen]
    if extra:
        errors.append(f"unregistered constructions in traversal: {sorted(set(extra))[:5]}")

    # Exact canonical ORDER, not merely the same set. A reordered traversal would still produce a
    # valid-looking document while silently changing which construction a positional reader sees.
    if actual_ids != expected_ids:
        first = next(
            (
                position
                for position, (got, want) in enumerate(zip(actual_ids, expected_ids))
                if got != want
            ),
            min(len(actual_ids), len(expected_ids)),
        )
        errors.append(
            f"traversal order diverges from the frozen universe at position {first}: "
            f"{actual_ids[first:first + 1]} != {expected_ids[first:first + 1]}"
        )

    # Identity immutability / no relabelling: every field the traversal shares with the frozen
    # mapping must be byte-equal to it.
    for record in records:
        construction_id = str(record.get("construction_id"))
        reference = frozen.get(construction_id)
        if not isinstance(reference, Mapping):
            continue
        for key, expected in reference.items():
            if key not in record:
                errors.append(f"{construction_id}: traversal omits frozen identity field {key!r}")
                continue
            # list/tuple is a container-type artifact of the two accessors, not an identity
            # difference. Order and elements are still compared exactly -- a reordered or altered
            # sequence still fails.
            if not _identity_equal(record[key], expected):
                errors.append(
                    f"{construction_id}.{key}: traversal has {record[key]!r} but the frozen "
                    f"universe has {expected!r}; identity fields are immutable"
                )

    if len(set(str(record.get("cell_id")) for record in records)) != PV.DERIVED_IDENTITIES["CELL_COUNT"]:
        errors.append(
            f"traversal spans {len(set(str(r.get('cell_id')) for r in records))} cells, "
            f'expected {PV.DERIVED_IDENTITIES["CELL_COUNT"]}'
        )

    observed_hash = CU.universe_aggregate_sha256()
    import level1_stage1_execution_authorization as authorization

    if observed_hash != authorization.CONSTRUCTION_UNIVERSE_SHA256:
        errors.append(
            f"construction universe aggregate hash {observed_hash} != pinned "
            f"{authorization.CONSTRUCTION_UNIVERSE_SHA256}"
        )
    return (not errors), tuple(errors)


def pair_consumption_of(record: Mapping[str, Any]) -> tuple[str, str] | None:
    """Return the canonical ``XASSET-0020`` SS-H unordered pair a construction consumes, or ``None``.

    ``XASSET-0035`` SS-F.1: a construction consumes a pair **iff both of its own two frozen named
    comparison endpoints are sleeves**. The pair is the single unordered pair those endpoints form,
    returned in canonical sorted order.

    SS-F.6's abuses are barred structurally rather than by comment. Consumption is read only from
    ``sleeve`` and ``counterpart``: ``unordered_pair_id`` is never consulted, so an absent label
    cannot imply non-consumption; only the construction's OWN two endpoints are considered, so no
    pair is reachable transitively; and nothing here mutates ``comparison_subject_kind`` or
    ``unordered_pair_id``, so no construction is relabelled.
    """
    sleeves = set(PV.SLEEVES)
    own = record.get("sleeve")
    counterpart = record.get("counterpart")
    if own in sleeves and counterpart in sleeves and own != counterpart:
        return tuple(sorted((str(own), str(counterpart))))  # type: ignore[return-value]
    return None


def pair_consumption_inventory(
    traversal: Sequence[Mapping[str, Any]] | None = None,
) -> Mapping[str, Any]:
    """Recompute ``XASSET-0035`` SS-F.5's structural inventory from frozen identities. READ-ONLY.

    Evaluates no gate and records no ``G10`` result: SS-F.7 is explicit that consumption is not
    ``G10``'s outcome.
    """
    records = tuple(frozen_traversal() if traversal is None else traversal)
    per_pair: dict[tuple[str, str], int] = {}
    consuming = 0
    for record in records:
        pair = pair_consumption_of(record)
        if pair is None:
            continue
        consuming += 1
        per_pair[pair] = per_pair.get(pair, 0) + 1
    return {
        "total": len(records),
        "consuming": consuming,
        "non_consuming": len(records) - consuming,
        "distinct_pairs": len(per_pair),
        "per_pair": {"::".join(pair): count for pair, count in sorted(per_pair.items())},
    }


# ======================================================================================
# Determined values -- supplied mechanically, never by the executor
# ======================================================================================


def determined_gate_results(analytical_input: Mapping[str, Any]) -> dict[str, str]:
    """Return the gate results accepted authority DETERMINES for a construction.

    ``G3`` and ``G5`` take ``XASSET-0035`` SS-G's reserved-gate posture unconditionally. ``G2`` is
    derived from the two SS-K.1 readings through the canonical closed table. ``G9`` follows SS-G.3's
    determined/undetermined split.
    """
    determined: dict[str, str] = {gate: "UNABLE_TO_DETERMINE" for gate in RESERVED_POSTURE_GATES}

    subject_matter = str(analytical_input.get("g2_outcome_under_subject_matter_reading"))
    preference_only = str(analytical_input.get("g2_outcome_under_preference_only_reading"))
    required = PV.required_g2_gate_result(subject_matter, preference_only)
    if required == PV.G2_RECORD_REJECTED:
        raise Stage1RunnerError(
            "G2 readings are incoherent: the preference-only reading is strictly narrower, so "
            "FAILS/PASSES is a recording defect and is rejected rather than mapped to an outcome"
        )
    determined[DERIVED_FROM_READINGS_GATE] = required

    declaration = str(analytical_input.get("g9_path_1_declaration"))
    if declaration == "UNDETERMINED":
        # XASSET-0035 SS-G.2: FAIL would name a dependency and thereby assert a DETERMINED path-1
        # failure, which is precisely what is undetermined.
        determined[REPRESENTATION_GATE] = "UNABLE_TO_DETERMINE"
    elif declaration == "DETERMINED_NOT_SELF_CONTAINED":
        # SS-G.3: the determined case stays prerequisite-blocked under canonical
        # non_self_contained_handling. B3 does not convert it.
        determined[REPRESENTATION_GATE] = "FAIL"
    elif declaration == "SELF_CONTAINED":
        determined[REPRESENTATION_GATE] = "PASS"
    else:
        raise Stage1RunnerError(
            f"g9_path_1_declaration must be one of {G9_PATH_1_DECLARATIONS}; got {declaration!r}"
        )
    return determined


def _check_analytical_input(construction_id: str, analytical_input: Mapping[str, Any]) -> None:
    """Fail closed on any malformed, incomplete, or overreaching executor input."""
    if not isinstance(analytical_input, Mapping):
        raise Stage1RunnerError(f"{construction_id}: analytical input must be a mapping")

    missing = [key for key in ANALYTICAL_INPUT_KEYS if key not in analytical_input]
    if missing:
        raise Stage1RunnerError(f"{construction_id}: analytical input is missing {missing}")
    unexpected = [key for key in analytical_input if key not in ANALYTICAL_INPUT_KEYS]
    if unexpected:
        raise Stage1RunnerError(f"{construction_id}: analytical input has unexpected keys {unexpected}")

    supplied = analytical_input.get("gate_results")
    if not isinstance(supplied, Mapping):
        raise Stage1RunnerError(f"{construction_id}: gate_results must be a mapping")

    # The executor may supply ONLY the undetermined gates. Attempting to supply a determined value
    # is refused even when the value happens to agree -- otherwise a later divergence would be
    # silently accepted, and the determination would become advisory.
    overreach = [gate for gate in supplied if gate not in EXECUTOR_SUPPLIED_GATES]
    if overreach:
        raise Stage1RunnerError(
            f"{construction_id}: gate(s) {sorted(overreach)} are determined by accepted authority "
            "and may not be supplied by an executor"
        )
    absent = [gate for gate in EXECUTOR_SUPPLIED_GATES if gate not in supplied]
    if absent:
        raise Stage1RunnerError(f"{construction_id}: gate(s) {absent} were not evaluated")

    bad = {
        gate: value for gate, value in supplied.items() if value not in PV.GATE_RESULT_VOCABULARY
    }
    if bad:
        raise Stage1RunnerError(
            f"{construction_id}: gate results must be in {PV.GATE_RESULT_VOCABULARY}; got {bad}"
        )

    for key in ("g2_outcome_under_subject_matter_reading", "g2_outcome_under_preference_only_reading"):
        if analytical_input.get(key) not in PV.READING_VOCABULARY:
            raise Stage1RunnerError(
                f"{construction_id}.{key}: must be in {PV.READING_VOCABULARY}, got "
                f"{analytical_input.get(key)!r}"
            )

    declaration = analytical_input.get("g9_path_1_declaration")
    if declaration not in G9_PATH_1_DECLARATIONS:
        raise Stage1RunnerError(
            f"{construction_id}.g9_path_1_declaration: must be in {G9_PATH_1_DECLARATIONS}, got "
            f"{declaration!r}"
        )
    named_dependency = analytical_input.get("g9_named_dependency")
    if declaration == "DETERMINED_NOT_SELF_CONTAINED":
        # Canonical non_self_contained_handling is NAME_THE_EXACT_DEPENDENCY_AND_BLOCK_PENDING_...,
        # so a determined failure without a named dependency is not a lawful record.
        if not isinstance(named_dependency, str) or not named_dependency.strip():
            raise Stage1RunnerError(
                f"{construction_id}: a determined G9 path-1 failure must name its exact dependency"
            )
    elif named_dependency is not None:
        raise Stage1RunnerError(
            f"{construction_id}: g9_named_dependency is recorded only for a determined path-1 failure"
        )

    basis = analytical_input.get("g12_basis")
    if basis not in G12_BASES:
        raise Stage1RunnerError(
            f"{construction_id}.g12_basis: must be in {G12_BASES}, got {basis!r}"
        )
    # XASSET-0035 SS-E.5's preserved floor, enforced rather than documented: successor nonexistence
    # is never BY ITSELF a ground for concluding no successor could admit the candidate.
    if supplied.get("G12_SNAPSHOT_ADMISSIBILITY_PATH") == "FAIL" and basis == "SUCCESSOR_NONEXISTENCE_ALONE":
        raise Stage1RunnerError(
            f"{construction_id}: G12 may not FAIL on successor nonexistence alone; XASSET-0035 "
            "SS-E fixes the modal register at lawful satisfiability of the frozen specification, "
            "not execution-time world state"
        )

    if analytical_input.get("point_or_range_support") not in PV.POINT_RANGE_VALUES:
        raise Stage1RunnerError(
            f"{construction_id}.point_or_range_support: must be in {PV.POINT_RANGE_VALUES}"
        )
    statement = analytical_input.get("uncertainty_statement")
    if not isinstance(statement, str) or not statement.strip():
        raise Stage1RunnerError(f"{construction_id}: uncertainty_statement must be recorded")


# ======================================================================================
# Composition
# ======================================================================================


def build_candidate_row(
    record: Mapping[str, Any], analytical_input: Mapping[str, Any]
) -> dict[str, Any]:
    """Compose one candidate result row deterministically. Order-independent by construction."""
    construction_id = str(record["construction_id"])
    _check_analytical_input(construction_id, analytical_input)

    gate_results = dict(analytical_input["gate_results"])
    gate_results.update(determined_gate_results(analytical_input))

    disposition = PV.derive_candidate_disposition(gate_results)
    subject_matter = str(analytical_input["g2_outcome_under_subject_matter_reading"])
    preference_only = str(analytical_input["g2_outcome_under_preference_only_reading"])

    return {
        "construction_id": construction_id,
        "cell_id": record["cell_id"],
        "sleeve": record["sleeve"],
        "bound": record["bound"],
        "driver_class": record["driver_class"],
        "family_id": record["family_id"],
        "route": record["route"],
        "num_0001_class": record["num_0001_class"],
        "source_architecture": record["source_architecture"],
        "source_path": None,
        "source_sha256": None,
        "hypothetical_source_requirements": record["hypothetical_source_requirements"],
        "governing_authority_refs": list(record["governing_authority_refs"]),
        "gate_results": {gate: gate_results[gate] for gate in PV.GATE_IDS},
        "categorical_failures": [
            gate for gate in PV.CATEGORICAL_GATES if gate_results.get(gate) == "FAIL"
        ],
        "prerequisite_failures": [
            gate for gate in PV.PREREQUISITE_GATES if gate_results.get(gate) == "FAIL"
        ],
        "disposition": disposition,
        # Diagnostic only -- canonical first_failing_gate_is_diagnostic_only is true, and every
        # applicable gate is evaluated regardless.
        "first_failing_gate_id": next(
            (gate for gate in PV.GATE_IDS if gate_results.get(gate) == "FAIL"), None
        ),
        "g2_outcome_under_subject_matter_reading": subject_matter,
        "g2_outcome_under_preference_only_reading": preference_only,
        "g2_outcome_is_reading_dependent": PV.is_reading_dependent(subject_matter, preference_only),
        "point_or_range_support": analytical_input["point_or_range_support"],
        "representation_dependency": analytical_input["g9_named_dependency"],
        "uncertainty_statement": analytical_input["uncertainty_statement"],
        # XASSET-0035 SS-E.5's preserved floor, carried into the publishable artifact rather than
        # left as an input-time refusal an independent reader cannot see. The runner emits exactly
        # the basis it validated above; the independent result validator re-enforces the coupling.
        "g12_basis": str(analytical_input["g12_basis"]),
    }


def _registered_construction_ids() -> frozenset[str]:
    """The real frozen registered identities. Read-only; evaluates nothing."""
    return frozenset(str(record["construction_id"]) for record in frozen_traversal())


def new_execution_readiness() -> tuple[bool, str]:
    """Report the READY question for the read-only self-check. Authorizes nothing."""
    import level1_stage1_execution_authorization as authorization

    return authorization.new_execution_is_authorized()


def run_stage1(
    analytical_inputs: Mapping[str, Mapping[str, Any]],
    *,
    provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Compose the real Stage-1 results document. PRODUCTION path. FAILS CLOSED.

    BLOCKING 1 (review 4953193650): this previously asked only ``new_execution_is_authorized`` --
    "may a NEW execution start" -- and accepted an injected authorizer on the real path, so a
    caller could compose real outcomes over the real frozen 680 without any claim ever existing.
    Reproduced before correcting.

    Composing a disposition for a registered construction IS the real work, so the question that
    must be answered here is ``active_execution_is_authorized`` -- "is the one lawful attempt
    CURRENTLY IN PROGRESS", i.e. exactly ``LANE_CLAIMED`` and still authenticated. There is NO
    injection seam on this path: the only authorizer is the real one, the only traversal is the
    real frozen universe, and the only cell ordering is the canonical one.

    BLOCKING 1 (review 4953558775): this asked ``claimed_execution_is_authorized`` instead, which
    answers a deliberately broader question and is true in ``COMPLETED`` as well, because the
    completed-result authentication path needs that provenance. A terminal lane therefore did not
    terminate composition. Reproduced before correcting, on isolated temporary lane paths.

    Synthetic composition lives in :func:`_compose_synthetic_stage1_document`, which is
    mechanically barred from every registered identity.
    """
    import level1_stage1_execution_authorization as authorization

    authorized, reason = authorization.active_execution_is_authorized()
    if not authorized:
        raise Stage1RunnerError(
            "Stage-1 outcomes may only be composed by a lawfully claimed execution that is "
            "currently in progress -- " + reason
        )

    records = tuple(frozen_traversal())
    ok, errors = verify_frozen_traversal(records)
    if not ok:
        raise Stage1RunnerError(f"frozen traversal failed structural verification: {errors}")
    return _compose_stage1_document(
        analytical_inputs,
        provenance=provenance,
        records=records,
        ordered_cells=tuple(PV.generate_cell_universe()),
    )


def _compose_synthetic_stage1_document(
    analytical_inputs: Mapping[str, Mapping[str, Any]],
    *,
    provenance: Mapping[str, Any] | None = None,
    traversal: Sequence[Mapping[str, Any]],
    cell_universe: Sequence[str],
) -> dict[str, Any]:
    """Compose over a SYNTHETIC universe. Private seam; authorizes and publishes nothing.

    Two mechanical restrictions make this seam incapable of standing in for the production path:
    a traversal must be supplied explicitly (``None`` is refused rather than silently defaulting
    to the real 680), and no supplied record or analytical input may name a registered
    construction. A caller therefore cannot reach a real disposition through this door.
    """
    if traversal is None:
        raise Stage1RunnerError(
            "the synthetic composition seam requires an explicit traversal; it may never fall "
            "back to the real frozen universe"
        )
    records = tuple(traversal)
    registered = _registered_construction_ids()
    offending = sorted(
        {str(record["construction_id"]) for record in records}.union(map(str, analytical_inputs))
        & registered
    )
    if offending:
        raise Stage1RunnerError(
            "the synthetic composition seam may not name registered construction(s) "
            f"{offending[:5]}; real dispositions are composed only by run_stage1 under a lawful "
            "claim"
        )
    return _compose_stage1_document(
        analytical_inputs,
        provenance=provenance,
        records=records,
        ordered_cells=tuple(cell_universe),
    )


def _compose_stage1_document(
    analytical_inputs: Mapping[str, Mapping[str, Any]],
    *,
    provenance: Mapping[str, Any] | None,
    records: Sequence[Mapping[str, Any]],
    ordered_cells: Sequence[str],
) -> dict[str, Any]:
    """Pure, deterministic composition. Selects no traversal and consults no authorization."""
    expected_ids = [str(record["construction_id"]) for record in records]
    unregistered = [key for key in analytical_inputs if key not in set(expected_ids)]
    if unregistered:
        raise Stage1RunnerError(
            f"analytical inputs name unregistered constructions: {sorted(unregistered)[:5]}"
        )
    # canonical execution.stopping_rules: partial publication is PROHIBITED and the run terminates
    # only when EVERY registered construction carries a recorded disposition.
    unevaluated = [key for key in expected_ids if key not in analytical_inputs]
    if unevaluated:
        raise Stage1RunnerError(
            f"{len(unevaluated)} registered construction(s) carry no analytical input; partial "
            f"publication is prohibited. First: {unevaluated[:5]}"
        )

    rows = [build_candidate_row(record, analytical_inputs[str(record["construction_id"])]) for record in records]

    by_cell: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_cell.setdefault(str(row["cell_id"]), []).append(row)
    # Cells are emitted in the supplied cell-universe order, not in dict-insertion or sorted
    # order, so the document's ordering is a canonical fact rather than an artifact of traversal.
    # The production caller always supplies the canonical order.
    ordered_cells = tuple(ordered_cells)
    # A cell present in the traversal but absent from the ordering would be silently dropped,
    # which would publish a partial document while every other check passed.
    orphan_cells = [cell_id for cell_id in by_cell if cell_id not in set(ordered_cells)]
    if orphan_cells:
        raise Stage1RunnerError(
            f"{len(orphan_cells)} cell(s) in the traversal are absent from the cell universe and "
            f"would be dropped: {sorted(orphan_cells)[:5]}"
        )
    cell_results = []
    for cell_id in ordered_cells:
        members = by_cell.get(cell_id)
        if members is None:
            continue
        sleeve, bound, driver_class = cell_id.split("::")
        cell_results.append(
            {
                "cell_id": cell_id,
                "sleeve": sleeve,
                "bound": bound,
                "driver_class": driver_class,
                "outcome": PV.derive_cell_outcome([row["disposition"] for row in members]),
                "contributing_construction_ids": [str(row["construction_id"]) for row in members],
            }
        )

    by_unit: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for cell in cell_results:
        by_unit.setdefault((str(cell["sleeve"]), str(cell["bound"])), []).append(cell)
    roll_up_results = [
        {
            "sleeve": sleeve,
            "bound": bound,
            "outcome": PV.derive_roll_up_outcome([cell["outcome"] for cell in cells]),
            "contributing_cell_ids": [str(cell["cell_id"]) for cell in cells],
        }
        for (sleeve, bound), cells in sorted(by_unit.items())
    ]

    abstention_records = [
        {
            "construction_id": str(row["construction_id"]),
            "disposition": row["disposition"],
            "uncertainty_statement": row["uncertainty_statement"],
        }
        for row in rows
        if row["disposition"] == "UNABLE_TO_DETERMINE"
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "study_id": STUDY_ID,
        "stage_id": STAGE_ID,
        "provenance_manifest": dict(provenance or {}),
        "candidate_results": rows,
        "cell_results": cell_results,
        "roll_up_results": roll_up_results,
        "deferred_requirements": ["J_12"],
        "abstention_records": abstention_records,
        "limitations": [
            "Stage 1 tests only the Stage-1-testable subset of XASSET-0024 SS-J.1 through SS-J.12.",
            "No endpoint, bound, percentage, weight, rank, target, or allocation is produced.",
            "XASSET-0024 SS-K.1 remains unresolved; every G2 result carries both reading outcomes.",
        ],
        "disposition": "RECORDED",
    }


# ======================================================================================
# Result writer / serializer
# ======================================================================================


def serialize_stage1_results(document: Mapping[str, Any]) -> bytes:
    """Serialize a results document to deterministic, byte-reproducible UTF-8 bytes.

    JSON with a fixed separator set and NO key sorting: the document's own insertion order is the
    canonical order (candidate rows in frozen traversal order, row keys in ``result_schema``
    order), and sorting would silently destroy it. Serializing the same document twice yields
    byte-identical output.
    """
    return (
        json.dumps(document, ensure_ascii=False, indent=2, separators=(",", ": "), sort_keys=False)
        + "\n"
    ).encode("utf-8")


def stage1_result_artifact_sha256(document: Mapping[str, Any]) -> str:
    """SHA-256 of the SERIALIZED BYTES. Diagnostic only -- this is NOT the result identity.

    MAJOR 1 (review 4953193650): the writer previously returned this value while the whole
    authorization chain -- ``complete_execution`` and ``completed_result_is_authorized`` -- binds
    ``level1_stage1_execution_authorization.stage1_result_identity``, the SHA-256 of the CANONICAL
    SORTED JSON. The two are different functions of the same document and diverge whenever key
    order changes, so returning this one invited a caller to bind an identity the completion path
    would then reject. Reproduced before correcting.

    This value therefore authorizes nothing and is never accepted anywhere an identity is
    required. It exists only to express byte-level artifact reproducibility. Use
    :func:`level1_stage1_execution_authorization.stage1_result_identity` for identity.
    """
    return hashlib.sha256(serialize_stage1_results(document)).hexdigest()


def _open_exclusive(path: Path) -> int:
    """``O_EXCL`` open, so an artifact can never be silently regenerated or replayed."""
    try:
        return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError as exc:
        raise Stage1RunnerError(
            f"{path} already exists; a Stage-1 results artifact is written once and never replaced"
        ) from exc


def canonical_results_path() -> Path:
    """The one path a real Stage-1 results artifact may ever occupy."""
    return ROOT / RESULTS_RELPATH


def write_stage1_results(document: Mapping[str, Any]) -> str:
    """Publish the real Stage-1 results artifact. PRODUCTION path. FAILS CLOSED.

    Returns the SEMANTIC RESULT IDENTITY -- ``stage1_result_identity`` -- the single value the
    completion and publication path already binds.

    BLOCKING 2 (review 4953193650): this previously accepted an arbitrary path, consulted no
    authorization, and validated nothing, so any caller could write any bytes anywhere and call
    the output a Stage-1 results artifact. Reproduced before correcting by writing a garbage
    document the independent validator rejects.

    Three gates now precede any file being opened, in this order, and every one fails closed:

    1. the one lawful attempt must be CURRENTLY IN PROGRESS -- exactly ``LANE_CLAIMED``, still
       authenticated;
    2. the destination is the canonical path and nothing else -- there is no path parameter;
    3. the document must pass the INDEPENDENT result validator, in memory, in full.

    Only after all three pass is the file opened, and then with ``O_EXCL``.

    BLOCKING 1 (review 4953558775): gate 1 asked ``claimed_execution_is_authorized``, which is
    also true in ``COMPLETED``. A canonical artifact lost or removed after completion could
    therefore be recreated here -- ``O_EXCL`` protects nothing once the path is gone -- turning
    the ordinary writer into an ungoverned recovery bypass. It now asks
    ``active_execution_is_authorized`` and refuses in ``COMPLETED`` exactly as in ``READY``:
    recovering a lost artifact is a governed act requiring new authority, never a re-publish.
    """
    import level1_stage1_execution_authorization as authorization
    import level1_stage1_result_validator as result_validator

    authorized, reason = authorization.active_execution_is_authorized()
    if not authorized:
        raise Stage1RunnerError(
            "a Stage-1 results artifact may only be published by a lawfully claimed execution "
            "that is currently in progress -- " + reason
        )

    outcome = result_validator.validate_stage1_result_document(document)
    if not outcome.ok:
        raise Stage1RunnerError(
            "the results document failed independent validation and will not be published; "
            f"first errors: {list(outcome.errors)[:5]}"
        )

    path = canonical_results_path()
    payload = serialize_stage1_results(document)
    handle = _open_exclusive(path)
    with os.fdopen(handle, "wb") as stream:
        stream.write(payload)
    return authorization.stage1_result_identity(document)


def _write_synthetic_results_artifact(document: Mapping[str, Any], path: Path) -> str:
    """Serialize a SYNTHETIC document to a caller-chosen path. Private seam; publishes nothing.

    Mechanically barred from the canonical results path, so it can never stand in for
    :func:`write_stage1_results`. Returns the artifact byte checksum, which authorizes nothing.
    """
    destination = Path(path)
    if destination.resolve() == canonical_results_path().resolve():
        raise Stage1RunnerError(
            "the synthetic write seam may never target the canonical results path; a real "
            "artifact is published only by write_stage1_results under a lawful claim"
        )
    payload = serialize_stage1_results(document)
    handle = _open_exclusive(destination)
    with os.fdopen(handle, "wb") as stream:
        stream.write(payload)
    return hashlib.sha256(payload).hexdigest()


def main(argv: Sequence[str] | None = None) -> int:
    """Read-only structural self-check. Executes no Stage 1 and writes nothing."""
    ok, errors = verify_frozen_traversal()
    inventory = pair_consumption_inventory()
    authorized, reason = new_execution_readiness()
    print(f"frozen traversal structurally verified: {ok}")
    for error in errors:
        print(f"  {error}")
    print(
        f"pair consumption: {inventory['consuming']} consuming / "
        f"{inventory['non_consuming']} non-consuming over {inventory['total']} "
        f"({inventory['distinct_pairs']} distinct canonical pairs)"
    )
    print(f"Stage 1 operationally authorized: {authorized} -- {reason}")
    return 0 if ok else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
