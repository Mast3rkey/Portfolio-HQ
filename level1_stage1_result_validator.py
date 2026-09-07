"""Independent validator for an ENDPOINT-0001 Stage-1 results document.

Created under ``XASSET-0036`` SS-E.3, which authorizes exactly one ``XASSET-0030`` SS-G.B steps-2-7
implementation pass. This module is SS-G.B step 4's "dedicated result validator".

WHY THIS EXISTS SEPARATELY FROM THE RUNNER
==========================================

A results document is not trustworthy because the runner produced it. This module therefore assumes
nothing about how the document was built and **re-derives every composed value from the document's
own recorded gate results**, comparing the recomputation against what the document claims. A runner
that recorded a disposition its own gate results do not derive is rejected here even though the
runner emitted it happily.

Independence is drawn on the axis that matters. Composition is re-derived through the ACCEPTED
canonical functions in ``level1_endpoint_evidence_preregistration_validator`` -- ``XASSET-0027``
SS-M.1's precedence is the authority, and a second private reimplementation would risk diverging
from it rather than checking it. What this module never does is *trust the runner's own arithmetic*,
its traversal, its ordering, its inventory, or its structural claims: each of those is recomputed
here from the frozen universe directly.

It also enforces the boundaries a results document must not cross:

* exact ``680`` inventory, exact canonical order, no duplicate / missing / extra construction;
* immutable identity fields, checked against the frozen universe rather than against the document;
* the ``XASSET-0035`` SS-G reserved-gate posture for ``G3`` and ``G5``;
* the ``XASSET-0035`` SS-F pair-consumption classification, recomputed from frozen identities;
* the canonical ``G2`` reading coupling;
* ``result_schema.forbidden_result_content`` -- no numeric sleeve share, bound value, percentage,
  weight, score, rank, or sum-to-whole anywhere in the document.

This module is READ-ONLY. It writes nothing, creates no lane state, generates no attestation, claims
no attempt, and confers no authorization: calling it is not an authorization path, exactly as
``_validate_stage1_results_against_universe``'s own docstring records of itself.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import level1_construction_universe_closure_validator as CU
import level1_endpoint_evidence_preregistration_validator as PV
import level1_stage1_runner as RUNNER

ROOT = Path(__file__).resolve().parent

RESULT_TOP_LEVEL_KEYS = (
    "schema_version",
    "study_id",
    "stage_id",
    "provenance_manifest",
    "candidate_results",
    "cell_results",
    "roll_up_results",
    "deferred_requirements",
    "abstention_records",
    "limitations",
    "disposition",
)

CELL_RESULT_KEYS = (
    "cell_id",
    "sleeve",
    "bound",
    "driver_class",
    "outcome",
    "contributing_construction_ids",
)

ROLL_UP_RESULT_KEYS = ("sleeve", "bound", "outcome", "contributing_cell_ids")

PROVENANCE_REQUIRED_FIELDS = (
    "study_id",
    "stage_id",
    "execution_attempt_id",
    "authorizing_decision",
    "authorizing_decision_merge_sha",
    "protocol_path",
    "protocol_sha256_observed",
    "preregistration_path",
    "preregistration_sha256_observed",
    "hash_verification_result",
    "repository_head_sha",
    "execution_date",
    "candidates_evaluated",
    "candidates_expected",
    "cells_evaluated",
    "cells_expected",
    "validator_result",
)

#: ``result_schema.forbidden_result_content``. A Stage-1 document records dispositions, never
#: quantities: any bare numeric share, percentage, or weight is a category error rather than a
#: value out of range.
_FORBIDDEN_VALUE_KEY_PATTERNS = (
    re.compile(r"(?i)\b(share|percent|percentage|weight|allocation|target)\b"),
    re.compile(r"(?i)\b(score|rank|ranking|index|composite)\b"),
    re.compile(r"(?i)\b(lower_bound_value|upper_bound_value|bound_value)\b"),
)

#: Keys whose integer values are legitimate structural counts rather than quantities.
_PERMITTED_NUMERIC_KEYS = frozenset(
    {
        "schema_version",
        "num_0001_class",
        "candidates_evaluated",
        "candidates_expected",
        "cells_evaluated",
        "cells_expected",
        "ordinal",
    }
)


#: The closed ``g12_basis`` vocabulary, restated here rather than imported from the producing
#: runner so this validator can contradict a runner that drifts. ``XASSET-0035`` SS-E fixes ``G12``'s
#: modal register at lawful satisfiability of the frozen construction specification; SS-E.5 preserves
#: the floor that successor nonexistence is NEVER BY ITSELF a ground for concluding no successor
#: could admit the candidate. A lawful ``G12`` ``FAIL`` on independent grounds stays representable.
_G12_BASIS_VALUES = (
    "LAWFUL_SUCCESSOR_IDENTIFIABLE",
    "SUCCESSOR_NONEXISTENCE_ALONE",
    "NO_LAWFUL_SUCCESSOR_IDENTIFIABLE_ON_INDEPENDENT_GROUNDS",
    "UNDETERMINED",
)

#: The one basis that may never accompany a ``G12`` ``FAIL``.
_G12_BASIS_PROHIBITED_WITH_FAIL = "SUCCESSOR_NONEXISTENCE_ALONE"

#: The gate the basis is coupled to.
_G12_GATE_ID = "G12_SNAPSHOT_ADMISSIBILITY_PATH"


class ResultValidationError(ValueError):
    """Raised when a results document cannot even be parsed safely."""


def _reject_duplicate_keys(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    """A duplicate key silently discards the earlier value in ordinary ``json.loads``."""
    seen: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ResultValidationError(f"duplicate key {key!r} in the results document")
        seen[key] = value
    return seen


def load_results(payload: bytes | str) -> Mapping[str, Any]:
    """Parse a serialized results document, rejecting duplicate keys.

    ``json.loads`` silently keeps the LAST value for a duplicated key, so a document carrying two
    ``disposition`` entries would validate against whichever one happened to be written second.
    That is refused here rather than resolved.
    """
    text = payload.decode("utf-8") if isinstance(payload, bytes) else payload
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except ResultValidationError:
        raise
    except ValueError as exc:
        raise ResultValidationError(f"results document is not parseable: {exc}") from exc


#: Forbidden TOKENS, matched against a key name split on non-alphanumeric separators. A regex
#: word-boundary scan alone misses every compound form -- ``\btarget\b`` does not match
#: ``target_weight``, because ``_`` is a word character -- so a scan built only from phrase patterns
#: would pass exactly the key names most likely to smuggle a quantity in.
_FORBIDDEN_KEY_TOKENS = frozenset(
    {
        "share",
        "shares",
        "percent",
        "percentage",
        "pct",
        "weight",
        "weights",
        "allocation",
        "target",
        "targets",
        "score",
        "scores",
        "rank",
        "ranking",
        "index",
        "composite",
        "bound",
    }
)

#: Tokens that are legitimate structure rather than quantity, and would otherwise false-positive.
_PERMITTED_TOKEN_CONTEXTS = frozenset({"bound"})


def _tokenize_key(key: str) -> list[str]:
    return [token for token in re.split(r"[^0-9A-Za-z]+", key.lower()) if token]


def _forbidden_key_reason(key: str) -> str | None:
    """Return why a key name is forbidden, or ``None``."""
    tokens = _tokenize_key(key)
    for token in tokens:
        if token in _FORBIDDEN_KEY_TOKENS:
            # ``bound`` alone is the construction's own LOWER/UPPER identity dimension, which is
            # structural. It is forbidden only when it names a VALUE.
            if token in _PERMITTED_TOKEN_CONTEXTS and "value" not in tokens:
                continue
            return token
    for pattern in _FORBIDDEN_VALUE_KEY_PATTERNS:
        if pattern.search(key):
            return key
    return None


def _scan_forbidden_content(node: Any, path: str, errors: list[str]) -> None:
    """Reject forbidden quantitative content anywhere in the document tree."""
    if isinstance(node, Mapping):
        for key, value in node.items():
            key_text = str(key)
            reason = _forbidden_key_reason(key_text)
            if reason is not None:
                errors.append(
                    f"{path}.{key_text}: forbidden result content ({reason!r}) -- a Stage-1 "
                    "document records dispositions, never shares, weights, scores, ranks, or "
                    "bound values"
                )
            if (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and key_text not in _PERMITTED_NUMERIC_KEYS
            ):
                errors.append(
                    f"{path}.{key_text}: bare numeric value {value!r} is not a permitted structural "
                    "count; Stage 1 produces no quantity"
                )
            _scan_forbidden_content(value, f"{path}.{key_text}", errors)
    elif isinstance(node, (list, tuple)):
        for position, value in enumerate(node):
            _scan_forbidden_content(value, f"{path}[{position}]", errors)


def validate_stage1_result_document(
    document: Mapping[str, Any],
    *,
    traversal: Sequence[Mapping[str, Any]] | None = None,
    expected_cells: Sequence[str] | None = None,
    roll_up_unit_count: int | None = None,
) -> PV.ValidationResult:
    """Independently validate a Stage-1 results document. Fails closed.

    Confers no authorization. Every composed value is re-derived from the document's own recorded
    gate results and compared; every structural claim is recomputed from the frozen universe.

    ``traversal`` is injectable for the same reason
    ``_validate_stage1_results_against_universe`` takes an explicit universe: adversarial tests
    must be able to exercise frozen-identity enforcement over a small synthetic universe without
    any call form implying Stage-1 authorization, and without deriving a disposition for a real
    registered construction. Supplying one confers nothing.
    """
    errors: list[str] = []
    if not isinstance(document, Mapping):
        return PV.ValidationResult(False, ("stage1_results: expected a top-level mapping",))

    actual_keys = tuple(document)
    if actual_keys != RESULT_TOP_LEVEL_KEYS:
        missing = [key for key in RESULT_TOP_LEVEL_KEYS if key not in document]
        unexpected = [key for key in actual_keys if key not in RESULT_TOP_LEVEL_KEYS]
        if missing:
            errors.append(f"stage1_results: missing top-level key(s) {missing}")
        if unexpected:
            errors.append(f"stage1_results: unexpected top-level key(s) {unexpected}")
        if not missing and not unexpected:
            errors.append(
                f"stage1_results: top-level keys are out of canonical order: {list(actual_keys)}"
            )

    if document.get("study_id") != RUNNER.STUDY_ID:
        errors.append(f"stage1_results.study_id: expected {RUNNER.STUDY_ID!r}")
    if document.get("stage_id") != RUNNER.STAGE_ID:
        errors.append(f"stage1_results.stage_id: expected {RUNNER.STAGE_ID!r}")

    _scan_forbidden_content(document, "stage1_results", errors)

    records = tuple(
        CU.generate_construction_universe() if traversal is None else traversal
    )
    reference_by_id = {str(record["construction_id"]): record for record in records}
    frozen = (
        CU.frozen_construction_universe() if traversal is None else dict(reference_by_id)
    )
    expected_ids = tuple(str(record["construction_id"]) for record in records)
    cell_universe = (
        tuple(PV.generate_cell_universe())
        if expected_cells is None
        else tuple(expected_cells)
    )
    expected_roll_up_units = (
        PV.DERIVED_IDENTITIES["ROLL_UP_UNIT_COUNT"]
        if roll_up_unit_count is None
        else roll_up_unit_count
    )

    rows = document.get("candidate_results")
    if not isinstance(rows, list):
        return PV.ValidationResult(False, tuple(errors) + ("candidate_results: expected a list",))

    seen: list[str] = []
    by_id: dict[str, Mapping[str, Any]] = {}
    for position, row in enumerate(rows):
        where = f"candidate_results[{position}]"
        if not isinstance(row, Mapping):
            errors.append(f"{where}: expected a mapping")
            continue
        construction_id = str(row.get("construction_id"))
        if construction_id not in frozen:
            errors.append(f"{where}.construction_id: {construction_id!r} is not registered")
            continue
        if construction_id in by_id:
            errors.append(f"{where}.construction_id: {construction_id!r} is duplicated")
            continue
        seen.append(construction_id)
        by_id[construction_id] = row

        if tuple(row) != PV.REQUIRED_CANDIDATE_RESULT_KEYS:
            missing = [key for key in PV.REQUIRED_CANDIDATE_RESULT_KEYS if key not in row]
            extra = [key for key in row if key not in PV.REQUIRED_CANDIDATE_RESULT_KEYS]
            if missing:
                errors.append(f"{where}: missing key(s) {missing}")
            if extra:
                errors.append(f"{where}: unexpected key(s) {extra}")

        # Identity is checked against the FROZEN universe, never against the document's own
        # neighbouring fields, so a row cannot make itself internally consistent while lying.
        reference = reference_by_id.get(construction_id, {})
        for key in (
            "cell_id",
            "sleeve",
            "bound",
            "driver_class",
            "family_id",
            "route",
            "num_0001_class",
            "source_architecture",
            "hypothetical_source_requirements",
            "governing_authority_refs",
        ):
            if key in reference and not RUNNER._identity_equal(row.get(key), reference[key]):
                errors.append(
                    f"{where}.{key}: recorded {row.get(key)!r} but the frozen construction is "
                    f"{reference[key]!r}; identity fields are immutable"
                )

        gate_results = row.get("gate_results")
        if not isinstance(gate_results, Mapping):
            errors.append(f"{where}.gate_results: expected a mapping")
            continue
        unknown = set(gate_results) - set(PV.GATE_IDS)
        absent = set(PV.GATE_IDS) - set(gate_results)
        if unknown:
            errors.append(f"{where}.gate_results: unknown gate(s) {sorted(unknown)}")
        if absent:
            errors.append(
                f"{where}.gate_results: every applicable gate must be evaluated; missing "
                f"{sorted(absent)}"
            )
        bad = {
            gate: value
            for gate, value in gate_results.items()
            if value not in PV.GATE_RESULT_VOCABULARY
        }
        if bad:
            errors.append(f"{where}.gate_results: results must be in the closed vocabulary; {bad}")
        if unknown or absent or bad:
            continue

        # XASSET-0035 SS-G: the reserved-gate recording posture is mandatory, not advisory.
        for gate in RUNNER.RESERVED_POSTURE_GATES:
            if gate_results.get(gate) != "UNABLE_TO_DETERMINE":
                errors.append(
                    f"{where}.gate_results.{gate}: expected 'UNABLE_TO_DETERMINE' under the "
                    "XASSET-0035 SS-G reserved-gate posture, got "
                    f"{gate_results.get(gate)!r}"
                )

        # The canonical G2 coupling, re-derived rather than trusted.
        subject_matter = row.get("g2_outcome_under_subject_matter_reading")
        preference_only = row.get("g2_outcome_under_preference_only_reading")
        if (
            subject_matter in PV.READING_VOCABULARY
            and preference_only in PV.READING_VOCABULARY
        ):
            required = PV.required_g2_gate_result(str(subject_matter), str(preference_only))
            if required == PV.G2_RECORD_REJECTED:
                errors.append(f"{where}: the recorded G2 reading pair is an incoherent record")
            elif gate_results.get("G2_MAGNITUDE_INTRINSICALITY") != required:
                errors.append(
                    f"{where}.gate_results.G2_MAGNITUDE_INTRINSICALITY: recorded "
                    f"{gate_results.get('G2_MAGNITUDE_INTRINSICALITY')!r} but the two readings "
                    f"require {required!r}"
                )
            expected_dependence = PV.is_reading_dependent(str(subject_matter), str(preference_only))
            if row.get("g2_outcome_is_reading_dependent") is not expected_dependence:
                errors.append(
                    f"{where}.g2_outcome_is_reading_dependent: expected {expected_dependence}"
                )
        else:
            errors.append(f"{where}: both G2 reading outcomes must be in {PV.READING_VOCABULARY}")

        # XASSET-0035 SS-E.5's preserved floor, re-enforced against the PUBLISHED artifact. The
        # runner refuses this pairing at input time, but an input-time refusal is invisible to an
        # independent reader of the artifact, so the coupling is checked again here from the row's
        # own recorded basis and its own recorded G12 result.
        recorded_basis = row.get("g12_basis")
        if recorded_basis not in _G12_BASIS_VALUES:
            errors.append(
                f"{where}.g12_basis: recorded {recorded_basis!r} but must be one of "
                f"{list(_G12_BASIS_VALUES)}"
            )
        elif (
            gate_results.get(_G12_GATE_ID) == "FAIL"
            and recorded_basis == _G12_BASIS_PROHIBITED_WITH_FAIL
        ):
            errors.append(
                f"{where}: G12 may not FAIL on {_G12_BASIS_PROHIBITED_WITH_FAIL}; XASSET-0035 "
                "SS-E fixes the modal register at lawful satisfiability of the frozen "
                "specification, and successor nonexistence is never by itself a FAIL ground"
            )

        # Composition, re-derived from the row's OWN gate results.
        try:
            derived = PV.derive_candidate_disposition(dict(gate_results))
        except ValueError as exc:
            errors.append(f"{where}.gate_results: {exc}")
        else:
            if row.get("disposition") != derived:
                errors.append(
                    f"{where}.disposition: recorded {row.get('disposition')!r} but the recorded "
                    f"gate results derive {derived!r}"
                )

        expected_categorical = [
            gate for gate in PV.CATEGORICAL_GATES if gate_results.get(gate) == "FAIL"
        ]
        if list(row.get("categorical_failures") or []) != expected_categorical:
            errors.append(
                f"{where}.categorical_failures: recorded {row.get('categorical_failures')!r}, "
                f"gate results give {expected_categorical!r}"
            )
        expected_prerequisite = [
            gate for gate in PV.PREREQUISITE_GATES if gate_results.get(gate) == "FAIL"
        ]
        if list(row.get("prerequisite_failures") or []) != expected_prerequisite:
            errors.append(
                f"{where}.prerequisite_failures: recorded {row.get('prerequisite_failures')!r}, "
                f"gate results give {expected_prerequisite!r}"
            )

        if row.get("point_or_range_support") not in PV.POINT_RANGE_VALUES:
            errors.append(f"{where}.point_or_range_support: outside the closed vocabulary")
        statement = row.get("uncertainty_statement")
        if not isinstance(statement, str) or not statement.strip():
            errors.append(f"{where}.uncertainty_statement: must be recorded")
        # Canonical non_self_contained_handling: a determined G9 prerequisite failure names its
        # exact dependency, and only such a failure records one.
        if gate_results.get("G9_REPRESENTATION") == "FAIL":
            dependency = row.get("representation_dependency")
            if not isinstance(dependency, str) or not dependency.strip():
                errors.append(
                    f"{where}.representation_dependency: a G9 prerequisite failure must name its "
                    "exact dependency"
                )
        elif row.get("representation_dependency") is not None:
            errors.append(
                f"{where}.representation_dependency: recorded without a G9 prerequisite failure"
            )

    # Exact inventory and exact canonical order, recomputed from the frozen universe.
    missing_ids = [construction_id for construction_id in expected_ids if construction_id not in by_id]
    if missing_ids:
        errors.append(
            f"candidate_results: {len(missing_ids)} registered construction(s) are unevaluated; "
            f"partial publication is prohibited. First: {missing_ids[:5]}"
        )
    if tuple(seen) != expected_ids and not missing_ids:
        first = next(
            (
                position
                for position, (got, want) in enumerate(zip(tuple(seen), expected_ids))
                if got != want
            ),
            0,
        )
        errors.append(
            f"candidate_results: rows are not in canonical construction order; first divergence at "
            f"position {first}"
        )

    errors.extend(_validate_cells(document, by_id, cell_universe))
    errors.extend(_validate_roll_ups(document, expected_roll_up_units))
    errors.extend(_validate_abstentions(document, by_id))
    errors.extend(_validate_provenance(document, by_id, len(expected_ids), len(cell_universe)))
    return PV.ValidationResult(not errors, tuple(errors))


def _validate_cells(
    document: Mapping[str, Any],
    by_id: Mapping[str, Mapping[str, Any]],
    expected_cells: Sequence[str],
) -> list[str]:
    """Re-derive every cell outcome from its own contributing candidate dispositions."""
    errors: list[str] = []
    cells = document.get("cell_results")
    if not isinstance(cells, list):
        return ["cell_results: expected a list"]

    recorded = [str(cell.get("cell_id")) for cell in cells if isinstance(cell, Mapping)]
    if tuple(recorded) != tuple(expected_cells):
        errors.append(
            f"cell_results: expected the {len(expected_cells)} canonical cells in canonical order"
        )

    members: dict[str, list[str]] = {}
    for construction_id, row in by_id.items():
        members.setdefault(str(row.get("cell_id")), []).append(construction_id)

    for position, cell in enumerate(cells):
        where = f"cell_results[{position}]"
        if not isinstance(cell, Mapping):
            errors.append(f"{where}: expected a mapping")
            continue
        if tuple(cell) != CELL_RESULT_KEYS:
            errors.append(f"{where}: expected exactly {list(CELL_RESULT_KEYS)}")
            continue
        cell_id = str(cell.get("cell_id"))
        contributing = [str(value) for value in cell.get("contributing_construction_ids") or []]
        expected_members = members.get(cell_id, [])
        if contributing != expected_members:
            errors.append(
                f"{where}.contributing_construction_ids: does not match the candidate rows "
                f"carrying this cell_id"
            )
            continue
        dispositions = [by_id[construction_id]["disposition"] for construction_id in contributing]
        try:
            derived = PV.derive_cell_outcome(dispositions)
        except ValueError as exc:
            errors.append(f"{where}: {exc}")
            continue
        if cell.get("outcome") != derived:
            errors.append(
                f"{where}.outcome: recorded {cell.get('outcome')!r} but its candidates derive "
                f"{derived!r}"
            )
    return errors


def _validate_roll_ups(
    document: Mapping[str, Any], expected_roll_up_units: int
) -> list[str]:
    """Re-derive every roll-up from its own six cells, and only its own."""
    errors: list[str] = []
    roll_ups = document.get("roll_up_results")
    cells = document.get("cell_results")
    if not isinstance(roll_ups, list) or not isinstance(cells, list):
        return ["roll_up_results: expected a list"]

    outcome_by_cell = {
        str(cell.get("cell_id")): cell.get("outcome")
        for cell in cells
        if isinstance(cell, Mapping)
    }
    if len(roll_ups) != expected_roll_up_units:
        errors.append(
            f"roll_up_results: expected {expected_roll_up_units} units, got {len(roll_ups)}"
        )
    for position, unit in enumerate(roll_ups):
        where = f"roll_up_results[{position}]"
        if not isinstance(unit, Mapping):
            errors.append(f"{where}: expected a mapping")
            continue
        if tuple(unit) != ROLL_UP_RESULT_KEYS:
            errors.append(f"{where}: expected exactly {list(ROLL_UP_RESULT_KEYS)}")
            continue
        sleeve = str(unit.get("sleeve"))
        bound = str(unit.get("bound"))
        contributing = [str(value) for value in unit.get("contributing_cell_ids") or []]
        # canonical roll_up_units: computed_only_from_own_six_cells, with cross-bound and
        # cross-sleeve reference PROHIBITED.
        foreign = [
            cell_id
            for cell_id in contributing
            if not cell_id.startswith(f"{sleeve}::{bound}::")
        ]
        if foreign:
            errors.append(
                f"{where}.contributing_cell_ids: cross-sleeve or cross-bound reference is "
                f"prohibited; {foreign[:3]}"
            )
            continue
        try:
            derived = PV.derive_roll_up_outcome([outcome_by_cell[cell] for cell in contributing])
        except (ValueError, KeyError) as exc:
            errors.append(f"{where}: {exc}")
            continue
        if unit.get("outcome") != derived:
            errors.append(
                f"{where}.outcome: recorded {unit.get('outcome')!r} but its cells derive "
                f"{derived!r}"
            )
    return errors


def _validate_abstentions(
    document: Mapping[str, Any], by_id: Mapping[str, Mapping[str, Any]]
) -> list[str]:
    """Abstention records must exactly match the rows that abstained."""
    records = document.get("abstention_records")
    if not isinstance(records, list):
        return ["abstention_records: expected a list"]
    recorded = [str(entry.get("construction_id")) for entry in records if isinstance(entry, Mapping)]
    expected = [
        construction_id
        for construction_id, row in by_id.items()
        if row.get("disposition") == "UNABLE_TO_DETERMINE"
    ]
    if recorded != expected:
        return [
            "abstention_records: does not match the candidate rows disposing to "
            "UNABLE_TO_DETERMINE"
        ]
    return []


def _validate_provenance(
    document: Mapping[str, Any],
    by_id: Mapping[str, Mapping[str, Any]],
    expected_candidates: int,
    expected_cells: int,
) -> list[str]:
    """Every required provenance field must be present, and the counts must be truthful."""
    errors: list[str] = []
    manifest = document.get("provenance_manifest")
    if not isinstance(manifest, Mapping):
        return ["provenance_manifest: expected a mapping"]
    for field in PROVENANCE_REQUIRED_FIELDS:
        if field not in manifest:
            errors.append(f"provenance_manifest.{field}: required field is absent")
    if manifest.get("execution_attempt_id") not in (None, RUNNER.EXECUTION_ATTEMPT_ID):
        errors.append(
            f"provenance_manifest.execution_attempt_id: expected {RUNNER.EXECUTION_ATTEMPT_ID!r}"
        )
    if "candidates_expected" in manifest and manifest["candidates_expected"] != expected_candidates:
        errors.append(
            f"provenance_manifest.candidates_expected: expected {expected_candidates}, got "
            f"{manifest['candidates_expected']!r}"
        )
    if "cells_expected" in manifest and manifest["cells_expected"] != expected_cells:
        errors.append(
            f"provenance_manifest.cells_expected: expected {expected_cells}, got "
            f"{manifest['cells_expected']!r}"
        )
    if "candidates_evaluated" in manifest and manifest["candidates_evaluated"] != len(by_id):
        errors.append(
            f"provenance_manifest.candidates_evaluated: recorded "
            f"{manifest['candidates_evaluated']!r} but {len(by_id)} rows are present"
        )
    return errors


def validate_results_file(path: Path) -> PV.ValidationResult:
    """Load and validate a serialized results document. READ-ONLY."""
    if not path.exists():
        return PV.ValidationResult(False, (f"{path}: no Stage-1 results document exists",))
    try:
        document = load_results(path.read_bytes())
    except ResultValidationError as exc:
        return PV.ValidationResult(False, (str(exc),))
    return validate_stage1_result_document(document)


def main(argv: Sequence[str] | None = None) -> int:
    """Validate the canonical results artifact if one exists. Writes nothing."""
    path = ROOT / RUNNER.RESULTS_RELPATH
    if not path.exists():
        print(f"level1_stage1_result_validator: OK (no results artifact at {RUNNER.RESULTS_RELPATH})")
        return 0
    result = validate_results_file(path)
    if result.ok:
        print("level1_stage1_result_validator: OK")
        return 0
    for error in result.errors:
        print(f"  {error}")
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
