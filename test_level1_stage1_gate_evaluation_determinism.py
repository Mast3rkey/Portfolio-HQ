"""Adversarial tests pinning the XASSET-0030 gate-evaluation determinism findings.

XASSET-0030 determined ``GATE_EVALUATION_METHOD_NOT_CLOSABLE``: six of the twelve Stage-1 gates are
deterministically closable against identified accepted feasibility authority, six are not, and the
canonical/enforcement contradiction is an implementation conformance defect rather than a governance
election.

These tests exist so that determination is **mechanically checkable rather than prose**. They pin only
determinations XASSET-0030 actually has authority to make: the precedence facts and the express
reservations are read from committed bytes, never asserted from this module's own opinion. A future,
separately authorized unit that corrects the validator or closes a reserved gate is EXPECTED to update
this module in the same PR — a failure here after such a unit is a signal to reconcile.

Nothing here arms, claims, completes, or executes Stage 1. Every candidate row is an isolated synthetic
fixture built in memory; no results document, lane directory, attestation, claim, completion, or ledger
entry is created or read for authorization purposes.
"""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import pytest
import yaml

import level1_construction_universe_closure_validator as CU
import level1_endpoint_evidence_preregistration_validator as P
import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
PREREG = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"
PROTOCOL = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
XASSET_0027 = (
    ROOT
    / "governance/decisions"
    / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
)
XASSET_0024 = (
    ROOT / "governance/decisions" / "XASSET-0024-level1-endpoint-basis-feasibility-determination.md"
)
DECISION = (
    ROOT
    / "governance/decisions"
    / "XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md"
)

# XASSET-0024 SS-D (operative subject-matter reading) and SS-K.1 (preserved contrary reading) together
# fix this pair for every registered construction. XASSET-0027 SS-M.1 routes the open reading through
# G2 and only G2.
SUBJECT_MATTER_READING = "PASSES"
PREFERENCE_ONLY_READING = "FAILS"

# XASSET-0030 SS-E, as corrected after review 4947074116.
CLOSABLE_GATES = {
    "G1_DRIVER_SUBJECT_MATTER",
    "G2_MAGNITUDE_INTRINSICALITY",
    "G4_ORIGIN",
    "G6_ROUTE_COMPLIANCE",
    "G7_DISCRETION_AND_PROVENANCE",
    "G11_EXACTNESS_AND_DETERMINISM",
}
UNCLOSABLE_GATES = {
    "G3_NORMALIZATION",
    "G5_CONSTRAINT_SHAPE",
    "G8_UNIQUENESS",
    "G9_REPRESENTATION",
    "G10_PAIR_INDEPENDENCE",
    "G12_SNAPSHOT_ADMISSIBILITY_PATH",
}


def _collapse(text: str) -> str:
    """Both canonical files and the decisions wrap prose; match on collapsed whitespace."""
    return " ".join(text.split())


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
    gates = {gate: "PASS" for gate in P.GATE_IDS}
    gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
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
            "prerequisite_failures": [],
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
    """Private structural seam only. Explicitly NOT an authorization path."""
    return P._validate_stage1_results_against_universe(
        {"candidate_results": [row], "cell_results": []},
        {construction_id: frozen},
    )


# --------------------------------------------------------------------------------------
# (1) Canonical categorical precedence vs the current validator prohibition
# --------------------------------------------------------------------------------------


class TestCanonicalPrecedenceControls:
    """The precedence question is answered in committed text, not left to a governance election."""

    def test_preregistration_declares_itself_canonical_for_gates_and_vocabularies(self):
        text = _collapse(PREREG.read_text(encoding="utf-8"))
        assert (
            "This YAML is canonical for every closed identity, candidate, gate, ordering, "
            "vocabulary, and count." in text
        )

    def test_protocol_is_expressly_subordinate_and_prelabels_divergence_a_defect(self):
        text = _collapse(PROTOCOL.read_text(encoding="utf-8"))
        assert "It cannot enlarge or override the YAML." in text
        assert (
            "Where the two appear to differ, the YAML governs and the difference is a defect "
            "requiring a governed correction." in text
        )

    def test_validator_disclaims_gate_deciding_authority(self):
        text = _collapse(
            (ROOT / "level1_endpoint_evidence_preregistration_validator.py").read_text(
                encoding="utf-8"
            )
        )
        assert "Read-only and mechanical." in text
        assert "Deciding a gate outcome remains a human/analytical act" in text

    def test_xasset_0027_m1_permits_categorical_override_at_disposition_level(self):
        text = _collapse(XASSET_0027.read_text(encoding="utf-8"))
        assert (
            "necessarily disposes to `UNABLE_TO_DETERMINE`, unless a categorical gate "
            "independently fails" in text
        )

    def test_both_canonical_artifacts_carry_the_same_clause(self):
        clause = "unless some categorical gate independently fails"
        data = yaml.safe_load(PREREG.read_text(encoding="utf-8"))
        assert clause in _collapse(
            data["g2_reading_mapping"]["reading_dependent_end_to_end_note"]
        )
        assert clause in _collapse(PROTOCOL.read_text(encoding="utf-8"))

    @pytest.mark.parametrize(
        "gate", sorted(g for g in P.CATEGORICAL_GATES if g != "G2_MAGNITUDE_INTRINSICALITY")
    )
    def test_validator_currently_forbids_the_canonically_permitted_outcome(
        self, universe, sample_id, gate
    ):
        """The enforcement defect, reproduced across every other categorical gate."""
        gates = _reading_dependent_gates()
        gates[gate] = "FAIL"
        row = _candidate_row(universe[sample_id], sample_id, gates)
        assert row["disposition"] == "BLOCKED_CATEGORICALLY"

        result = _structural(row, universe[sample_id], sample_id)
        assert result.ok is False
        assert any(
            "may not be recorded as BLOCKED_CATEGORICALLY" in error for error in result.errors
        ), result.errors

    def test_categorical_branches_remain_defined_though_currently_unreachable(self):
        assert P.derive_cell_outcome(["BLOCKED_CATEGORICALLY"]) == "BLOCKED_CATEGORICALLY"


# --------------------------------------------------------------------------------------
# (2) G1 subject-matter vs G2 magnitude-reading boundary
# --------------------------------------------------------------------------------------


class TestG1IsNotG2:
    """SS-K.1's magnitude ambiguity is routed through G2 only; importing it into G1 is a new rule."""

    def test_k1_is_defined_as_a_magnitude_question_routed_through_g2(self):
        text = _collapse(XASSET_0027.read_text(encoding="utf-8"))
        assert "Whether §E.1's six classes house a magnitude statement remains open" in text
        assert "`G2` is therefore evaluated **under both readings**" in text

    def test_g1_has_independent_subject_matter_feasibility_authority(self):
        """XASSET-0024 SS-D, not the frozen specification, is what makes G1 closable."""
        text = _collapse(XASSET_0024.read_text(encoding="utf-8"))
        assert "Those six are *subject-matter* classes describing what evidence is about" in text
        assert (
            "A qualifying source must therefore be admissible as a DRIVER under at least one of "
            "the six **on its own subject matter**" in text
        )

    def test_only_g2_carries_per_reading_fields(self):
        """No G1 reading slot exists, and this decision invents none."""
        g2_fields = {
            "g2_outcome_under_subject_matter_reading",
            "g2_outcome_under_preference_only_reading",
            "g2_outcome_is_reading_dependent",
        }
        assert g2_fields <= set(P.REQUIRED_CANDIDATE_RESULT_KEYS)
        assert not any(
            key.startswith("g1_outcome_under") for key in P.REQUIRED_CANDIDATE_RESULT_KEYS
        )


# --------------------------------------------------------------------------------------
# (3) G12 identifiability vs existence
# --------------------------------------------------------------------------------------


class TestG12IdentifiabilityIsNotExistence:
    def test_canonical_mapping_scopes_g12_to_identifiability_only(self):
        data = yaml.safe_load(PREREG.read_text(encoding="utf-8"))
        items = {i["j_item"]: i["gate_or_basis"] for i in data["stage_1_testable_subset"]["items"]}
        assert items["J_2_SNAPSHOT_POSITION"] == "G12_IDENTIFIABILITY_ONLY_NO_SUCCESSOR_CREATED"

    def test_protocol_states_the_gate_records_identifiability(self):
        text = _collapse(PROTOCOL.read_text(encoding="utf-8"))
        assert "`G12` records whether a snapshot successor is *identifiable*" in text

    def test_a_successor_path_is_named_by_accepted_authority(self):
        """XASSET-0027 SS-P.2 names it, which is why nonexistence alone cannot settle the gate."""
        text = _collapse(XASSET_0027.read_text(encoding="utf-8"))
        assert "a **`XASSET-0021` snapshot successor**, which cannot admit evidence that does not yet exist" in text

    def test_no_governed_definition_of_identifiable_exists(self):
        """The blocker: neither canonical artifact defines the term or fixes 'could admit' tense."""
        for path in (PREREG, PROTOCOL):
            text = _collapse(path.read_text(encoding="utf-8"))
            assert "identifiable means" not in text.lower()
            assert "definition of identifiable" not in text.lower()


# --------------------------------------------------------------------------------------
# (4) specification-requires-P vs accepted-authority-establishes-satisfiability
# --------------------------------------------------------------------------------------


class TestSatisfiabilityIsNotSpecification:
    def test_every_construction_is_hypothetical_so_requirement_text_alone_proves_nothing(
        self, universe
    ):
        assert {e["source_architecture"] for e in universe.values()} == {
            "HYPOTHETICAL_SOURCE_ARCHITECTURE"
        }

    def test_route_table_supplies_independent_feasibility_authority(self):
        """XASSET-0024 SS-D's 'Lawful in principle?' column is the basis for G4/G6/G11."""
        text = _collapse(XASSET_0024.read_text(encoding="utf-8"))
        assert "Lawful in principle?" in text
        assert text.count("**YES, conditionally**") >= 2
        assert "No route is invented here because the existing ones are difficult." in text

    def test_t5_is_closed_but_t1_t2_t3_t4_t6_t10_are_not(self):
        """XASSET-0027 SS-F is the feasibility authority for G6, and bounds what else it closes."""
        text = _collapse(XASSET_0027.read_text(encoding="utf-8"))
        assert "This closes the universal `T5` failure" in text
        assert (
            "It closes nothing else: `T1`, `T2`, `T3`, `T4`, and `T6` through `T10` are untouched"
            in text
        )

    def test_class_4_route_is_independently_determined_lawful(self):
        """XASSET-0024 SS-E.1 is the basis for G7."""
        text = _collapse(XASSET_0024.read_text(encoding="utf-8"))
        assert "It is a lawful route, and it is not a third route." in text

    def test_units_regime_is_the_basis_for_g11(self):
        text = _collapse(XASSET_0024.read_text(encoding="utf-8"))
        assert (
            "carried at exact source precision or as an exact rational derivation under "
            "XASSET-0021 §G" in text
        )


# --------------------------------------------------------------------------------------
# (5) / (6) the corrected closable / unclosable partition
# --------------------------------------------------------------------------------------


class TestCorrectedGatePartition:
    def test_partition_is_exhaustive_and_disjoint(self):
        assert CLOSABLE_GATES | UNCLOSABLE_GATES == set(P.GATE_IDS)
        assert not (CLOSABLE_GATES & UNCLOSABLE_GATES)
        assert len(CLOSABLE_GATES) == 6 and len(UNCLOSABLE_GATES) == 6

    def test_g3_is_expressly_reserved(self):
        text = _collapse(XASSET_0027.read_text(encoding="utf-8"))
        assert "Whether that suffices to carry a share-of-the-whole statement is what `G3` tests" in text
        assert "it does not determine that no bridge exists" in text

    def test_g5_is_expressly_reserved(self):
        """SS-M.4 reserves G5 the same way SS-M.3 reserves G3 — why G5 is not closable."""
        text = _collapse(XASSET_0027.read_text(encoding="utf-8"))
        assert (
            "is exactly what `G5` decides, per candidate, on the candidate's own terms. No "
            "prejudgment is recorded here." in text
        )

    def test_g9_mapping_is_unreconciled(self):
        data = yaml.safe_load(PREREG.read_text(encoding="utf-8"))
        assert "G9_REPRESENTATION" in P.PREREQUISITE_GATES
        conditions = {c["condition"] for c in data["mandatory_abstention_conditions"]}
        assert "REPRESENTATION_PATH_1_FAILS_AND_NO_ACCEPTED_RULE_EXISTS" in conditions

    def test_g8_uniqueness_is_scoped_to_an_admitted_set(self):
        data = yaml.safe_load(PREREG.read_text(encoding="utf-8"))
        gate = next(
            g for g in data["gate_sequence"]["gates"] if g["gate_id"] == "G8_UNIQUENESS"
        )
        assert "across the admitted set" in _collapse(gate["question"])

    def test_g10_depends_on_an_unresolved_pair_determination(self):
        data = yaml.safe_load(PREREG.read_text(encoding="utf-8"))
        gate = next(
            g for g in data["gate_sequence"]["gates"] if g["gate_id"] == "G10_PAIR_INDEPENDENCE"
        )
        assert "unresolved pair" in _collapse(gate["question"])

    @pytest.mark.parametrize("gate", sorted(CLOSABLE_GATES | UNCLOSABLE_GATES))
    def test_no_gate_outcome_is_preregistered_anywhere(self, universe, gate):
        """Whatever its disposition, no gate's RESULT is committed data.

        The preregistration names every gate; what it never carries is an outcome. Each gate entry
        holds exactly the declared record_keys, none of which is a result field.
        """
        assert gate not in repr(universe), f"{gate} leaked into the frozen universe"

        data = yaml.safe_load(PREREG.read_text(encoding="utf-8"))
        declared = set(data["gate_sequence"]["record_keys"])
        entry = next(g for g in data["gate_sequence"]["gates"] if g["gate_id"] == gate)
        assert set(entry) == declared
        assert not (set(entry) & {"result", "outcome", "gate_result", "disposition"})
        assert not set(entry.values()) & set(P.GATE_RESULT_VOCABULARY)

    def test_g2_is_the_one_gate_with_a_fixed_recorded_outcome(self, universe, sample_id):
        gates = _reading_dependent_gates()
        row = _candidate_row(universe[sample_id], sample_id, gates)
        assert (
            P.required_g2_gate_result(SUBJECT_MATTER_READING, PREFERENCE_ONLY_READING)
            == "UNABLE_TO_DETERMINE"
        )
        assert row["disposition"] == "UNABLE_TO_DETERMINE"
        assert _structural(row, universe[sample_id], sample_id).ok is True


# --------------------------------------------------------------------------------------
# Frozen universe integrity
# --------------------------------------------------------------------------------------


class TestSnapshotIsCurrentAuthorityNotPermanentClosure:
    """The 6/6 table is a CURRENT_AUTHORITY snapshot with per-gate invalidation triggers.

    These tests pin the *durability contract*, not the gate names: a closable result may be reused
    only while its controlling authority is unchanged, and each such gate must name what invalidates
    it. They are deliberately written so that adding or removing a closable gate does not silently
    weaken them -- every closable gate must carry a trigger row.
    """

    def test_table_is_labelled_a_current_authority_snapshot(self):
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert "CURRENT_AUTHORITY_GATE_EVALUATION_SNAPSHOT" in text
        assert "not permanent gate closure" in text

    def test_reuse_is_conditioned_on_unchanged_controlling_authority(self):
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert "only while every controlling authority and premise" in text

    def test_no_permanent_closure_language_survives(self):
        """The exact phrases review 4947130884 MAJOR 1 flagged must not reappear."""
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        for banned in (
            "need not re-derive them",
            "need no further work",
            "Ordered by dependency",
        ):
            assert banned not in text, banned

    def test_replacement_wording_is_present(self):
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert (
            "need no separate work while their controlling authority remains unchanged" in text
        )

    @pytest.mark.parametrize("gate", sorted(CLOSABLE_GATES))
    def test_every_closable_gate_has_an_invalidation_row(self, gate):
        """No gate may be marked closable without naming what re-derivation it depends on."""
        text = DECISION.read_text(encoding="utf-8")
        section = text.split("#### E.1")[1].split("### F.")[0]
        short = gate.split("_")[0]  # G1, G2, G4, ...
        row = next(
            (line for line in section.splitlines() if line.strip().startswith(f"| `{short}` |")),
            None,
        )
        assert row is not None, f"{short} has no E.1 invalidation row"
        assert row.count("|") >= 4, row
        trigger = row.split("|")[3].strip()
        assert trigger, f"{short} has an empty re-derivation trigger"

    def test_g1_and_g2_name_their_upstream_dependencies(self):
        """MAJOR 1's two named cases: G1 on SS-E.1/SS-D, G2 on SS-K.1's present state."""
        section = DECISION.read_text(encoding="utf-8").split("#### E.1")[1].split("### F.")[0]
        g1 = next(line for line in section.splitlines() if line.strip().startswith("| `G1` |"))
        g2 = next(line for line in section.splitlines() if line.strip().startswith("| `G2` |"))
        assert "§E.1" in g1 and "§D" in g1
        assert "§K.1" in g2 and "§M.1" in g2
        assert "amended" in g1
        assert "resolved or amended" in g2

    def test_snapshot_is_tied_to_xasset_0027_reopen_triggers(self):
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert "§Q" in text
        section = DECISION.read_text(encoding="utf-8").split("#### E.1")[1].split("### F.")[0]
        assert section.count("**§Q**") >= 6, "each closable gate should carry a §Q linkage"

    def test_the_e1_clarification_coupling_is_stated_explicitly(self):
        """The G3 corrective is G1/G2's own invalidation trigger; the decision must say so."""
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert "must re-derive `G1` and `G2`" in text

    def test_xasset_0027_q_actually_contains_the_cited_triggers(self):
        """Reproduced from controlling text, not asserted from the decision alone."""
        text = _collapse(XASSET_0027.read_text(encoding="utf-8"))
        assert "`XASSET-0020` §E.1's driver classes or §L's endpoint row is amended" in text
        assert "a reviewer establishes `XASSET-0024` §K.1's contrary reading of §E.1" in text
        assert "`NUM-0001`'s classes, §6, §7, or §8 change" in text
        assert "either pinned canonical hash changes" in text


class TestSuccessorSequencing:
    """Semantic prerequisites first; one canonical/enforcement/reauthorization pass after."""

    def test_two_distinct_classes_exist(self):
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert "G.A — Semantic / governance prerequisites" in text
        assert "G.B — Final canonical / enforcement / reauthorization reconciliation" in text

    def test_no_early_validator_only_reauthorization_prerequisite(self):
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert "No early validator-only reauthorization prerequisite exists" in text

    def test_efficiency_reason_is_stated(self):
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert (
            "Do not spend one reauthorization lifecycle on an intermediate enforcement state" in text
        )

    def test_semantic_set_covers_every_unclosable_gate(self):
        """G.A must name each open semantic question, so none is silently dropped."""
        section = DECISION.read_text(encoding="utf-8").split("#### G.A")[1].split("#### G.B")[0]
        for gate in sorted(UNCLOSABLE_GATES):
            short = gate.split("_")[0]
            assert f"`{short}`" in section, f"{short} missing from the semantic prerequisite set"

    def test_semantic_set_does_not_mandate_a_single_filing(self):
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert "These need not be one filing." in text

    def test_arming_is_last_and_follows_the_single_rebinding_lifecycle(self):
        section = DECISION.read_text(encoding="utf-8").split("#### G.B")[1].split("### H.")[0]
        rebind = section.index("rebinding lifecycle")
        arm = section.index("may Stage 1 be armed")
        assert rebind < arm, "arming must follow the rebinding lifecycle"

    def test_nothing_in_the_successor_model_is_authorized_here(self):
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert "This decision authorizes none of G.A or G.B" in text


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
        observed: set[str] = set()
        for entry in universe.values():
            observed |= set(entry)
        assert observed == self.EXPECTED_KEYS

    def test_universe_identity_is_unchanged(self, universe):
        assert len(universe) == A.CONSTRUCTION_COUNT == 680
        assert len({e["cell_id"] for e in universe.values()}) == A.CONSTRUCTION_CELL_COUNT == 48
        assert (
            A.CONSTRUCTION_UNIVERSE_SHA256
            == "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
        )


# --------------------------------------------------------------------------------------
# Load-bearing reauthorization dependency (XASSET-0030 SS-D)
# --------------------------------------------------------------------------------------


class TestLoadBearingReauthorizationDependency:
    def test_both_validators_are_load_bearing_authorization_paths(self):
        assert "level1_endpoint_evidence_preregistration_validator.py" in A.LOAD_BEARING_RELPATHS
        assert "level1_construction_universe_closure_validator.py" in A.LOAD_BEARING_RELPATHS

    def test_working_tree_bytes_are_bound_and_drift_is_an_error(self):
        source = _collapse(
            (ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        )
        assert "enforcement drift" in source
        # The message is assembled across adjacent f-string literals; collapse before matching.
        assert 'load-bearing code has changed " "since the authorized merge' in source

    def test_this_unit_left_every_load_bearing_path_untouched(self):
        """Governance-only: correcting the Finding 1 defect is deliberately out of scope."""
        import subprocess

        changed = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        ).stdout.split()
        assert not (set(changed) & set(A.LOAD_BEARING_RELPATHS)), changed


# --------------------------------------------------------------------------------------
# (7) Non-authorization guards
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
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        forbidden = {"write_authorization", "claim_execution", "complete_execution"}
        called = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        assert not (called & forbidden)

    def test_no_fixture_names_a_real_source_or_acquires_data(self):
        """Every fixture is a frozen hypothetical; none carries a source path or hash."""
        source = Path(__file__).read_text(encoding="utf-8")
        assert '"source_path": None' in source
        assert '"source_sha256": None' in source
        # Tokens are assembled at runtime so this guard cannot match its own literal.
        banned = ["req" + "uests", "url" + "lib", "yfin" + "ance", "alp" + "aca",
                  "phq-risk" + "0001-results"]
        imported = {
            node.module.split(".")[0]
            for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.ImportFrom) and node.module
        } | {
            alias.name.split(".")[0]
            for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        assert not (imported & set(banned)), imported
        for token in banned:
            assert source.count(token) <= 1, token
