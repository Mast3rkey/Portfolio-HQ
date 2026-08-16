"""Adversarial tests pinning the XASSET-0030 gate-evaluation determinism findings.

XASSET-0030 determined ``GATE_EVALUATION_METHOD_NOT_CLOSABLE``: seven of the twelve Stage-1 gates
are deterministically closable from accepted authority, five are not, and one blocker is a
contradiction between the canonical files and the validator rather than a mere gap.

These tests exist so that determination is **mechanically checkable rather than prose**, and so the
findings cannot drift silently. They assert the repository's CURRENT structural state. A future,
separately authorized unit that lawfully closes the method (or resolves the contradiction) is
EXPECTED to update this module in the same PR that does so -- a failure here after such a unit is a
signal to reconcile, not a regression to suppress.

Nothing here arms, claims, completes, or executes Stage 1. Every candidate row is an isolated
synthetic fixture built in memory; no results document, lane directory, attestation, claim,
completion, or ledger entry is created or read for authorization purposes.
"""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import pytest

import level1_construction_universe_closure_validator as CU
import level1_endpoint_evidence_preregistration_validator as P
import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent

# The reading pair XASSET-0024 SS-D (operative subject-matter reading) and SS-K.1 (preserved contrary
# reading) together fix for every registered construction. XASSET-0030 SS-E records this as the one
# gate whose evaluation IS closable.
SUBJECT_MATTER_READING = "PASSES"
PREFERENCE_ONLY_READING = "FAILS"


# --------------------------------------------------------------------------------------
# Fixtures -- synthetic candidate rows only
# --------------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def universe() -> dict:
    return CU.frozen_construction_universe()


@pytest.fixture(scope="module")
def sample_id(universe: dict) -> str:
    return sorted(universe)[0]


def _reading_dependent_gates() -> dict[str, str]:
    """Every gate PASS except the two whose outcomes XASSET-0030 records as closable."""
    gates = {gate: "PASS" for gate in P.GATE_IDS}
    gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
    gates["G12_SNAPSHOT_ADMISSIBILITY_PATH"] = "FAIL"
    return gates


def _candidate_row(frozen: dict, construction_id: str, gates: dict[str, str]) -> dict:
    row = {key: frozen.get(key) for key in P.DUPLICATED_FROZEN_IDENTITY_FIELDS}
    row.update(
        {
            "construction_id": construction_id,
            "source_architecture": "HYPOTHETICAL_SOURCE_ARCHITECTURE",
            "source_path": None,
            "source_sha256": None,
            "hypothetical_source_requirements": frozen["hypothetical_source_requirements"],
            "gate_results": gates,
            "categorical_failures": [],
            "prerequisite_failures": ["G12_SNAPSHOT_ADMISSIBILITY_PATH"],
            "disposition": P.derive_candidate_disposition(gates),
            "first_failing_gate_id": None,
            "g2_outcome_under_subject_matter_reading": SUBJECT_MATTER_READING,
            "g2_outcome_under_preference_only_reading": PREFERENCE_ONLY_READING,
            "g2_outcome_is_reading_dependent": True,
            "point_or_range_support": "RANGE_FIRST",
            "representation_dependency": None,
            "uncertainty_statement": "XASSET-0024 SS-K.1 remains unresolved.",
        }
    )
    return row


def _structural(row: dict, frozen: dict, construction_id: str):
    """Private structural seam only. This is explicitly NOT an authorization path."""
    return P._validate_stage1_results_against_universe(
        {"candidate_results": [row], "cell_results": []},
        {construction_id: frozen},
    )


# --------------------------------------------------------------------------------------
# B.1 -- the SS-K.1 map consumes readings; nothing produces them
# --------------------------------------------------------------------------------------


class TestReadingMapConsumesRatherThanProduces:
    def test_map_is_deterministic_once_both_readings_are_supplied(self):
        assert (
            P.required_g2_gate_result(SUBJECT_MATTER_READING, PREFERENCE_ONLY_READING)
            == "UNABLE_TO_DETERMINE"
        )
        assert P.is_reading_dependent(SUBJECT_MATTER_READING, PREFERENCE_ONLY_READING) is True

    def test_no_module_function_derives_the_readings_from_a_construction(self, universe, sample_id):
        """The gap: no callable maps a frozen construction to its two SS-K.1 reading outcomes."""
        frozen = universe[sample_id]
        assert "g2_outcome_under_subject_matter_reading" not in frozen
        assert "g2_outcome_under_preference_only_reading" not in frozen

        # Only three reading-related CALLABLES exist, and all three consume the two readings as
        # arguments rather than deriving them. (OPEN_READING_FIELDS is a constant naming the three
        # fields a results row must record; it produces nothing.)
        allowed = {"required_g2_gate_result", "is_reading_dependent", "map_g2_reading"}
        for module in (P, CU, A):
            for name in dir(module):
                if name.startswith("_") or "reading" not in name.lower():
                    continue
                if not callable(getattr(module, name)):
                    continue
                assert name in allowed, (
                    f"unexpected reading-related callable {module.__name__}.{name}"
                )


# --------------------------------------------------------------------------------------
# B.2 -- the frozen universe carries identity only, never outcomes
# --------------------------------------------------------------------------------------


class TestFrozenUniverseCarriesNoGateOutcomes:
    EXPECTED_KEYS = {
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
    }

    def test_universe_entries_carry_exactly_the_identity_fields(self, universe):
        observed = set()
        for entry in universe.values():
            observed |= set(entry)
        assert observed == self.EXPECTED_KEYS

    def test_no_gate_id_appears_anywhere_in_the_universe(self, universe):
        blob = repr(universe)
        for gate in P.GATE_IDS:
            assert gate not in blob, f"{gate} leaked into the frozen universe"

    def test_universe_identity_is_unchanged(self, universe):
        assert len(universe) == A.CONSTRUCTION_COUNT == 680
        assert len({e["cell_id"] for e in universe.values()}) == A.CONSTRUCTION_CELL_COUNT == 48
        assert (
            A.CONSTRUCTION_UNIVERSE_SHA256
            == "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
        )

    def test_every_construction_is_hypothetical_source_architecture(self, universe):
        assert {e["source_architecture"] for e in universe.values()} == {
            "HYPOTHETICAL_SOURCE_ARCHITECTURE"
        }


# --------------------------------------------------------------------------------------
# B.3 / Finding 2 -- G3 remains undetermined, and its PASS/UTD branch is disposition-neutral
# --------------------------------------------------------------------------------------


class TestG3RemainsUndetermined:
    @pytest.mark.parametrize("g3", ["PASS", "UNABLE_TO_DETERMINE"])
    def test_pass_and_unable_to_determine_are_disposition_neutral(self, universe, sample_id, g3):
        """Narrowing recorded by XASSET-0030 SS-B.4: two of G3's three answers agree."""
        gates = _reading_dependent_gates()
        gates["G3_NORMALIZATION"] = g3
        row = _candidate_row(universe[sample_id], sample_id, gates)
        assert row["disposition"] == "UNABLE_TO_DETERMINE"
        assert _structural(row, universe[sample_id], sample_id).ok is True

    def test_fail_derives_a_materially_different_disposition(self, universe, sample_id):
        """The ambiguity is real: the third answer changes the outcome."""
        gates = _reading_dependent_gates()
        gates["G3_NORMALIZATION"] = "FAIL"
        assert P.derive_candidate_disposition(gates) == "BLOCKED_CATEGORICALLY"


# --------------------------------------------------------------------------------------
# Finding 1 -- canonical text and validator contradict each other
# --------------------------------------------------------------------------------------


class TestReadingDependentCategoricalContradiction:
    CANONICAL_CLAUSE = "unless some categorical gate independently fails"

    @staticmethod
    def _collapse(text: str) -> str:
        """Both canonical files wrap prose, so match on whitespace-collapsed text."""
        return " ".join(text.split())

    def test_preregistration_says_categorical_failure_is_expected(self):
        import yaml

        data = yaml.safe_load(
            (ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )
        note = data["g2_reading_mapping"]["reading_dependent_end_to_end_note"]
        assert self.CANONICAL_CLAUSE in self._collapse(note)

    def test_protocol_says_the_same(self):
        text = (ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md").read_text(
            encoding="utf-8"
        )
        assert self.CANONICAL_CLAUSE in self._collapse(text)

    @pytest.mark.parametrize(
        "gate",
        [g for g in P.CATEGORICAL_GATES if g != "G2_MAGNITUDE_INTRINSICALITY"],
    )
    def test_validator_forbids_what_the_canonical_files_expect(self, universe, sample_id, gate):
        """Every categorical gate is unrepresentable while G2 is reading-dependent."""
        gates = _reading_dependent_gates()
        gates[gate] = "FAIL"
        row = _candidate_row(universe[sample_id], sample_id, gates)
        assert row["disposition"] == "BLOCKED_CATEGORICALLY"

        result = _structural(row, universe[sample_id], sample_id)
        assert result.ok is False
        assert any(
            "may not be recorded as BLOCKED_CATEGORICALLY" in error for error in result.errors
        ), result.errors

    def test_the_categorical_branch_of_the_cell_rule_is_therefore_unreachable(self):
        """derive_cell_outcome still HAS the branch; no lawful candidate can reach it today."""
        assert P.derive_cell_outcome(["BLOCKED_CATEGORICALLY"]) == "BLOCKED_CATEGORICALLY"


# --------------------------------------------------------------------------------------
# Closable gates -- recorded so a successor need not re-derive them
# --------------------------------------------------------------------------------------


class TestClosableGateDeterminations:
    def test_g12_is_a_prerequisite_failure_not_a_categorical_one(self):
        assert "G12_SNAPSHOT_ADMISSIBILITY_PATH" in P.PREREQUISITE_GATES
        assert "G12_SNAPSHOT_ADMISSIBILITY_PATH" not in P.CATEGORICAL_GATES

    def test_g9_is_a_prerequisite_gate_while_section_g_path_3_says_abstention(self):
        """The unreconciled mapping XASSET-0030 SS-E records for G9."""
        assert "G9_REPRESENTATION" in P.PREREQUISITE_GATES
        import yaml

        data = yaml.safe_load(
            (ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )
        conditions = {c["condition"] for c in data["mandatory_abstention_conditions"]}
        assert "REPRESENTATION_PATH_1_FAILS_AND_NO_ACCEPTED_RULE_EXISTS" in conditions

    def test_prerequisite_failure_alone_still_yields_unable_to_determine(
        self, universe, sample_id
    ):
        """G2 UTD dominates the G12 prerequisite failure, so G9's mapping cannot flip a disposition."""
        gates = _reading_dependent_gates()
        gates["G9_REPRESENTATION"] = "FAIL"
        row = _candidate_row(universe[sample_id], sample_id, gates)
        assert row["disposition"] == "UNABLE_TO_DETERMINE"
        assert _structural(row, universe[sample_id], sample_id).ok is True


# --------------------------------------------------------------------------------------
# Non-authorization guards
# --------------------------------------------------------------------------------------


class TestNothingHereAuthorizesOrExecutes:
    def test_stage_1_remains_unarmed(self):
        authorized, reason = A.new_execution_is_authorized()
        assert authorized is False
        assert "attestation" in reason.lower()

    def test_lane_artifacts_do_not_exist(self):
        assert not A.AUTHORIZATION_ROOT.exists()
        assert not A.AUTHORIZATION_PATH.exists()
        assert not A.CLAIM_PATH.exists()
        assert not A.COMPLETION_PATH.exists()
        assert not A.LEDGER_PATH.exists()

    def test_no_stage1_results_document_exists(self):
        assert not (ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()

    def test_canonical_pins_are_unchanged_by_this_unit(self):
        expected = {
            "research/level1_endpoint_evidence/PROTOCOL_V1.md": (
                "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
            ),
            "research/level1_endpoint_evidence/pre_registration.yaml": (
                "6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c"
            ),
        }
        for relpath, digest in expected.items():
            observed = hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest()
            assert observed == digest, f"{relpath} canonical bytes changed"

    def test_this_module_never_writes_to_the_authorization_lane(self):
        """Static guard: no write/claim/complete call appears anywhere in this file."""
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        forbidden = {"write_authorization", "claim_execution", "complete_execution"}
        called = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        assert not (called & forbidden)
