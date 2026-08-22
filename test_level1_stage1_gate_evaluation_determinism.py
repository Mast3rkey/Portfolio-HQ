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


def _collapse_prose(text: str) -> str:
    """Like _collapse, but also strips Markdown blockquote markers.

    A wrapped `>` blockquote otherwise injects a stray `>` mid-sentence when collapsed, which would
    make a correct quotation fail to match for purely typographic reasons.
    """
    stripped = "\n".join(line.lstrip().removeprefix(">").strip() for line in text.splitlines())
    return " ".join(stripped.split())


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
            # Added to the publishable schema by the XASSET-0036 SS-G.B package (MAJOR 2, review
            # 4953193650). A conforming row records it; the coupling with a G12 FAIL is enforced.
            "g12_basis": (
                "NO_LAWFUL_SUCCESSOR_IDENTIFIABLE_ON_INDEPENDENT_GROUNDS"
                if gates.get("G12_SNAPSHOT_ADMISSIBILITY_PATH") == "FAIL"
                else "LAWFUL_SUCCESSOR_IDENTIFIABLE"
            ),
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
    def test_the_canonically_permitted_outcome_is_now_accepted(
        self, universe, sample_id, gate
    ):
        """AMENDED BY XASSET-0036 SS-E.2, which authorized SS-G.B step 3's correction.

        This test previously reproduced the XASSET-0030 SS-C enforcement DEFECT across every
        categorical gate: the validator rejected a lawfully-derived BLOCKED_CATEGORICALLY whenever
        G2 was reading-dependent, although XASSET-0027 SS-M.1 and both canonical artifacts permit it
        "unless a categorical gate independently fails". The defect has since been corrected, so the
        same fixture now pins the CORRECT behaviour across the same gates. The companion test below
        pins the other direction, so the overreach cannot return.
        """
        gates = _reading_dependent_gates()
        gates[gate] = "FAIL"
        row = _candidate_row(universe[sample_id], sample_id, gates)
        assert row["disposition"] == "BLOCKED_CATEGORICALLY"

        result = _structural(row, universe[sample_id], sample_id)
        assert result.ok is True, result.errors

    def test_reading_dependence_alone_still_may_not_be_recorded_as_categorical(
        self, universe, sample_id
    ):
        """The protection the defect branch was really guarding, preserved exactly."""
        gates = _reading_dependent_gates()
        row = _candidate_row(universe[sample_id], sample_id, gates)
        row["disposition"] = "BLOCKED_CATEGORICALLY"
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
        # Correction 3 renamed G.B to name the outcome-producing-code byte class explicitly.
        assert (
            "G.B — Final canonical / enforcement / **outcome-producing-code** / reauthorization "
            "reconciliation" in text
        )

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
        arm = section.index("attestation be produced and Stage 1 armed")
        assert rebind < arm, "arming must follow the rebinding lifecycle"

    def test_nothing_in_the_successor_model_is_authorized_here(self):
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert "This decision authorizes none of G.A or G.B" in text


class TestRunnerTrustBoundarySequencing:
    """§G.B must bind outcome-producing code BEFORE the final rebinding, not merely before arming.

    These pin the *governance contract* in XASSET-0030. They deliberately do not reference any runner
    file: none exists, and building one is prohibited here. Nothing in this class writes, arms, claims,
    or executes anything.
    """

    @staticmethod
    def _gb() -> str:
        return DECISION.read_text(encoding="utf-8").split("#### G.B")[1].split("### H.")[0]

    def _step_index(self, needle: str) -> int:
        gb = self._gb()
        assert needle in gb, f"missing from G.B: {needle!r}"
        return gb.index(needle)

    def test_the_invariant_is_stated_plainly(self):
        text = _collapse_prose(DECISION.read_text(encoding="utf-8"))
        assert (
            "No outcome-producing executable code may be created, changed, or left outside the "
            "bound execution identity after the final rebinding and before `ATTEMPT_1`." in text
        )

    def test_outcome_producing_code_is_defined(self):
        gb = _collapse(self._gb())
        for capability in ("deciding", "ordering", "serializing", "writing", "materially altering"):
            assert capability in gb, capability

    def test_runner_implementation_precedes_the_binding_extension(self):
        impl = self._step_index("Implement and fully validate")
        bind = self._step_index("Extend the successor operational-authorization trust boundary")
        assert impl < bind

    def test_binding_extension_precedes_the_rebinding_lifecycle(self):
        bind = self._step_index("Extend the successor operational-authorization trust boundary")
        rebind = self._step_index("rebinding lifecycle against those")
        assert bind < rebind

    def test_rebinding_covers_canonical_enforcement_and_outcome_producing_bytes(self):
        gb = _collapse(self._gb())
        assert (
            "canonical **and** enforcement **and** outcome-producing executable" in gb
        ), "the rebinding scope must name all three byte classes"

    def test_pins_are_computed_only_after_all_three_byte_classes_stabilize(self):
        gb = _collapse(self._gb())
        assert (
            "only after all** canonical **and** validator/enforcement **and** "
            "runner/result-production bytes have stabilized" in gb
        )

    def test_runner_readiness_is_read_only_and_follows_rebinding(self):
        rebind = self._step_index("rebinding lifecycle against those")
        readiness = self._step_index("read-only verification of already-bound bytes")
        assert rebind < readiness
        gb = _collapse(self._gb())
        assert (
            "It is **not** a phase in which outcome-producing executable code may still be created "
            "or changed." in gb
        )

    def test_post_rebinding_drift_fails_closed_before_ready_or_claim(self):
        gb = _collapse(self._gb())
        assert (
            "Any post-rebinding drift in runner / result-production bytes must fail closed before "
            "`READY` or claim" in gb
        )

    def test_arming_is_last(self):
        gb = self._gb()
        arm = gb.index("attestation be produced and Stage 1 armed")
        for earlier in (
            "Implement and fully validate",
            "Extend the successor operational-authorization trust boundary",
            "rebinding lifecycle against those",
            "read-only verification of already-bound bytes",
            "must fail closed before",
        ):
            assert gb.index(earlier) < arm, earlier

    def test_the_gap_is_justified_and_has_since_been_closed(self):
        """AMENDED BY XASSET-0036 SS-E.6, which authorized SS-G.B step 5's extension.

        XASSET-0030 SS-D recorded the gap -- no runner was in the six-path set, because none
        existed -- and SS-G.B step 5 exists to close it. The decision text stating the gap is
        unchanged and still asserted here; the gap itself is now closed, which is the outcome that
        text called for rather than a contradiction of it.
        """
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert "No Stage-1 runner is in that set" in text
        assert "level1_stage1_runner.py" in A.LOAD_BEARING_RELPATHS
        assert "level1_stage1_result_validator.py" in A.LOAD_BEARING_RELPATHS
        # No REAL results artifact is load-bearing, because none exists.
        assert not any("stage1_results" in path for path in A.LOAD_BEARING_RELPATHS)

    def test_this_pr_builds_no_runner_and_changes_no_load_bearing_set(self):
        text = _collapse(DECISION.read_text(encoding="utf-8"))
        assert (
            "This decision builds no runner, changes no `LOAD_BEARING_RELPATHS`, and amends no "
            "`XASSET-0029`." in text
        )
        assert not (ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()

    def test_load_bearing_set_enumerated_by_this_decision_is_still_present(self):
        """AMENDED BY XASSET-0036 SS-E.6.

        XASSET-0030 SS-D enumerated the six paths that existed when it was accepted. Those six are
        still asserted present here, and the decision's own "exactly six" wording is unchanged and
        still checked -- it accurately describes SS-D's own moment. The three paths SS-G.B step 5
        later added are verified separately, in this suite's own trust-boundary test above and in
        the XASSET-0036 package suite.
        """
        section = DECISION.read_text(encoding="utf-8").split("### D.")[1].split("### E.")[0]
        enumerated = [
            "level1_stage1_execution_authorization.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "level1_construction_universe_closure_validator.py",
            A.CANONICAL_PROTOCOL_RELPATH,
            A.CANONICAL_PREREGISTRATION_RELPATH,
            "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
        ]
        for path in enumerated:
            assert path in section, f"{path} missing from the SS-D enumeration"
            assert path in A.LOAD_BEARING_RELPATHS, f"{path} dropped from the live set"
        assert "exactly **six** paths" in _collapse(section)


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

    def test_the_recorded_dependency_was_discharged_exactly_as_authorized(self):
        """AMENDED BY XASSET-0036 SS-E.5/SS-E.6, which authorized SS-G.B steps 3 and 5.

        This test previously asserted that ``origin/main...HEAD`` touched no load-bearing path.
        That was the right check for XASSET-0030's own governance-only unit, but the expression
        captures WHATEVER BRANCH IS CHECKED OUT rather than that unit specifically -- so on the
        authorized implementation branch it necessarily fails, since SS-G.B steps 3 and 5 exist
        precisely to change those paths. (It also passes vacuously whenever HEAD equals
        ``origin/main``, which is why it is not a durable guard.)

        SS-D recorded the dependency: correcting the Finding 1 defect deliberately creates
        enforcement drift, and the trust boundary must then be extended to cover the
        outcome-producing code. What is durably checkable, and what this test now asserts, is that
        the dependency was discharged EXACTLY as authorized -- the six paths SS-D enumerated are
        all retained, the additions are exactly the authorized outcome-producing set, and no real
        results artifact is load-bearing because none exists.
        """
        enumerated = {
            "level1_stage1_execution_authorization.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "level1_construction_universe_closure_validator.py",
            A.CANONICAL_PROTOCOL_RELPATH,
            A.CANONICAL_PREREGISTRATION_RELPATH,
            "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
        }
        assert enumerated <= set(A.LOAD_BEARING_RELPATHS)
        assert set(A.LOAD_BEARING_RELPATHS) - enumerated == {
            "level1_stage1_runner.py",
            "level1_stage1_result_validator.py",
            "governance/decisions/XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
            # AMENDED BY XASSET-0037 / SS-G.B step 8's successor rebinding. SS-D's six enumerated
            # paths are still all retained above, and the additions remain EXACTLY the authorized
            # set -- outcome-producing code plus each authorizing decision.
            "governance/decisions/XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md",
            # FURTHER AMENDED BY XASSET-0044's post-correction operational rebinding, filed under
            # SS-D's reconciliation clause (SS-G.B step 8 is NOT re-consumed). The invariant this
            # test exists to hold is unchanged and is still exact: SS-D's six enumerated paths are
            # all retained above, and every addition is still EXACTLY outcome-producing code plus
            # each authorizing decision -- here, the correction's own authorization, the corrected
            # module's decision, the rebinding's authorization, and the rebinding itself. Each is
            # bound by DIRECT MEMBERSHIP; a citation or prose restatement is not a byte binding.
            "governance/decisions/XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md",
            "governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md",
            "governance/decisions/XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md",
            "governance/decisions/XASSET-0044-endpoint-0001-stage-1-post-correction-operational-rebinding.md",
            # FURTHER AMENDED BY XASSET-0047's post-merge-CI recovery, filed under XASSET-0046
            # SS-G.6 after XASSET-0044's own merge-commit CI failed permanently at the exact merge
            # SHA its effectivity condition names. The invariant is unchanged and still exact:
            # SS-D's six enumerated paths are all retained above, and every addition remains
            # EXACTLY outcome-producing code plus each authorizing decision -- here, the recovery's
            # own authorization and the recovery itself. Each is bound by DIRECT MEMBERSHIP.
            "governance/decisions/XASSET-0046-endpoint-0001-stage-1-post-merge-ci-recovery-reauthorization.md",
            "governance/decisions/XASSET-0047-endpoint-0001-stage-1-post-merge-ci-recovery-reconciliation.md",
            # FURTHER AMENDED BY XASSET-0049's step-8-EQUIVALENT successor operational rebinding,
            # authorized by XASSET-0048 SS-E (SS-G.B step 8's OWN budget stays spent on
            # XASSET-0037 and is not re-consumed). The invariant is unchanged and still EXACT:
            # SS-D's six enumerated paths are all retained above, and every addition remains
            # EXACTLY outcome-producing code plus each authorizing decision -- here, this
            # rebinding's own authorization and the rebinding itself. Each is bound by DIRECT
            # MEMBERSHIP; a citation or prose restatement is not a byte binding.
            "governance/decisions/XASSET-0048-endpoint-0001-stage-1-step-8-equivalent-rebinding-authorization.md",
            "governance/decisions/XASSET-0049-endpoint-0001-stage-1-step-8-equivalent-successor-operational-rebinding.md",
        }
        # Every addition beyond SS-D's six is either outcome-producing code or a governance
        # decision file. Nothing else may enter the trust boundary by this route.
        for path in set(A.LOAD_BEARING_RELPATHS) - enumerated:
            assert path.startswith("governance/decisions/") or path.endswith(".py"), path
        assert not any("stage1_results" in path for path in A.LOAD_BEARING_RELPATHS)


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

    def test_canonical_pins_match_the_effective_pins(self):
        """AMENDED BY XASSET-0036 SS-E.1/SS-E.7.

        This unit changed no canonical byte, and that remains true of it. The literals it asserted
        are XASSET-0029's, retained below as history; XASSET-0036's authorized reconciliation
        amended the bytes and recomputed the pins, so the live check now runs against the single
        effective source rather than a superseded literal.
        """
        xasset_0029_pins = {
            "research/level1_endpoint_evidence/PROTOCOL_V1.md": (
                "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
            ),
            "research/level1_endpoint_evidence/pre_registration.yaml": (
                "6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c"
            ),
        }
        assert A.XASSET_0029_CANONICAL_PINS == xasset_0029_pins
        for relpath, digest in A.CANONICAL_PINS.items():
            observed = hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest()
            assert observed == digest, f"{relpath} does not match its effective pin"

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
