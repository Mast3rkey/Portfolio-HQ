"""Adversarial tests pinning the ``XASSET-0034`` semantic-closure / execution-feasibility determination.

``XASSET-0030`` §G.B step 1 requires a successor to "resolve all **required** §G.A semantic/governance
prerequisites" before the single canonical / enforcement / outcome-producing-code / reauthorization
pass. ``XASSET-0032`` §N then records that all six "have been examined and none is closed", while its
Consequences state that two of them "cannot be closed by governance at all". ``XASSET-0034`` answers the
resulting sequencing question and returns **MIXED** — five items are execution-ready governed
source-/snapshot-dependent states, three residual **semantic** blockers stand, and §G.B is **not**
unlocked.

These tests exist so the determination is **mechanically checkable rather than prose**. Every rule,
heading, and qualifier below is read from committed bytes — the two canonical artifacts and the accepted
decisions — never asserted from this module's own opinion.

For each finding the suite pins two things: the **intended rule**, and its **nearest plausible
overreach** — the stronger claim a successor might read out of the same text, which the determination
must refuse. Four overreaches matter most here, and each has its own guard:

1. **Conflation.** The whole determination rests on separating *semantic rule closure* from *candidate
   satisfaction*. ``TestRuleVersusSatisfactionDistinction`` pins that both sides are stated and that the
   decision never treats a satisfaction residue as a closed gate.
2. **Acceleration.** The tempting move is to declare everything "runtime" and unlock §G.B.
   ``TestGBIsNotUnlocked`` and ``TestResidualBlockersSurviveAdversarially`` fail if the decision ever
   claims §G.B is enterable, drops a blocker, or downgrades one to a satisfaction question.
3. **Silent closure.** ``TestNoGateIsClosed`` fails if any of the six not-closable gates is recorded
   closable, or if any per-construction gate result is asserted anywhere.
4. **Invention.** ``TestNoCandidateFactIsInvented``, ``TestSourceDependentIsNotAutomaticPass`` and
   ``TestSourceDependentIsNotAutomaticFail`` pin that ``XASSET-0030`` §E Standards 1 and 2 are preserved
   in both directions — neither by-construction ``PASS`` nor nonexistence-``FAIL``.

They also pin the *negative space* that makes the determination honest: the ``XASSET-0030`` 6/6 partition
unchanged, ``XASSET-0024`` §K.1 unresolved, ``XASSET-0020`` §E.1 unamended, ``XASSET-0031``'s ``G3``
neither reopened nor used as a premise, the prerequisite class preserved, abstention still a complete
outcome, no canonical/validator/authorization/runner mutation, and no execution artifact.

Nothing here arms, claims, completes, or executes Stage 1. No gate is evaluated for any construction. No
results document, lane directory, attestation, claim, completion, or ledger entry is created or read for
authorization purposes.
"""

from __future__ import annotations

import ast
import hashlib
import re
from pathlib import Path

import pytest
import yaml

import level1_construction_universe_closure_validator as CU
import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
PREREG = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"
PROTOCOL = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
GOV = ROOT / "governance/decisions"

XASSET_0020 = GOV / "XASSET-0020-replacement-level1-economic-sizing-methodology.md"
XASSET_0024 = GOV / "XASSET-0024-level1-endpoint-basis-feasibility-determination.md"
XASSET_0026 = (
    GOV / "XASSET-0026-level1-endpoint-evidence-program-shape-and-sleeve-selection-basis.md"
)
XASSET_0027 = (
    GOV / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
)
XASSET_0028 = GOV / "XASSET-0028-concrete-construction-universe-closure-determination.md"
XASSET_0030 = GOV / "XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md"
XASSET_0031 = (
    GOV / "XASSET-0031-endpoint-0001-stage-1-g3-share-of-the-whole-semantic-determination.md"
)
XASSET_0032 = (
    GOV / "XASSET-0032-endpoint-0001-stage-1-remaining-semantic-gate-determination.md"
)
XASSET_0033 = GOV / "XASSET-0033-endpoint-0001-stage-1-g12-could-admit-tense-determination.md"
DECISION = (
    GOV
    / "XASSET-0034-endpoint-0001-stage-1-semantic-closure-and-execution-feasibility-determination.md"
)

#: XASSET-0030 §E's closable six — this unit must not re-derive or disturb them.
CLOSABLE_SNAPSHOT_GATES = ("G1", "G2", "G4", "G6", "G7", "G11")

#: XASSET-0030 §E's not-closable six — this unit must not close any of them.
NOT_CLOSABLE_GATES = ("G3", "G5", "G8", "G9", "G10", "G12")

#: The five §G.A items XASSET-0034 §D determines are NOT §G.B entry conditions.
EXECUTION_READY_ITEMS = ("G3", "G5", "G8", "G9", "G10")

#: Protected RISK-0001 result identifiers, assembled from fragments so that asserting their absence
#: does not itself introduce the literal string into this file.
PROTECTED_RISK_NEEDLES = ("risk" + "_results", "RISK-0001" + " results")

#: Paths this governance-only unit must leave byte-untouched.
PROTECTED_RELPATHS = (
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "level1_stage1_execution_authorization.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_construction_universe_closure_validator.py",
)

#: The two canonical pins, written as exact literals **here** rather than imported from the
#: authorization module. Importing them would make the comparison circular: mutating the module's own
#: declared pin would mutate the expectation with it and the test would still pass. That
#: non-circular design is preserved exactly; only the VALUES are advanced.
#:
#: AMENDED BY XASSET-0036 SS-E.1/SS-E.7. This filing changed no canonical byte, and that remains
#: true of it. The implementation XASSET-0036 later authorized reconciled the XASSET-0035
#: SS-E/SS-F/SS-G semantics into the canonical artifacts and recomputed the pins afterwards.
EXPECTED_CANONICAL_PINS = {
    "research/level1_endpoint_evidence/PROTOCOL_V1.md": (
        "86b2a5e8674247698ac592ce4734744f940b4a119ffda5fd702bc3cbf3e40c13"
    ),
    "research/level1_endpoint_evidence/pre_registration.yaml": (
        "e993df9f41d2f5352e51c9921dd006d50ab69518a730d37def106696b3f149d4"
    ),
}

#: XASSET-0029's pins, retained as HISTORICAL identity and asserted as such below. Accepted history
#: is never rewritten to match amended bytes.
XASSET_0029_CANONICAL_PINS = {
    "research/level1_endpoint_evidence/PROTOCOL_V1.md": (
        "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
    ),
    "research/level1_endpoint_evidence/pre_registration.yaml": (
        "6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c"
    ),
}

#: Artifacts whose existence would mean Stage 1 had been armed, claimed, or run.
EXECUTION_ARTIFACT_RELPATHS = (
    "research/level1_endpoint_evidence/stage1_results.yaml",
    "research/level1_endpoint_evidence/ATTEMPT_1",
    "research/level1_endpoint_evidence/attestation.yaml",
    "research/level1_endpoint_evidence/claim.yaml",
    "research/level1_endpoint_evidence/completion.yaml",
    "research/level1_endpoint_evidence/ledger.yaml",
)


def _collapse(text: str) -> str:
    """Collapse Markdown hard-wrapping so a wrapped sentence matches as one string.

    Blockquote markers are stripped first: a hard-wrapped ``>`` quote would otherwise leave a stray
    ``>`` mid-sentence and defeat an otherwise-correct match.
    """
    text = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    return re.sub(r"\s+", " ", text)


def _read(path: Path) -> str:
    return _collapse(path.read_text(encoding="utf-8"))


def _observed_canonical_digests() -> dict[str, str]:
    """SHA-256 over the canonical files' observed bytes, computed here.

    Deliberately independent of ``level1_stage1_execution_authorization`` so that a mutation of that
    module's own hashing path cannot make an unchanged-pins claim true by construction.
    """
    return {
        relpath: hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest()
        for relpath in EXPECTED_CANONICAL_PINS
    }


def _pin_mismatches(expected: dict[str, str]) -> list[str]:
    """Relpaths whose observed digest differs from ``expected``. Empty means every pin matches."""
    observed = _observed_canonical_digests()
    return sorted(rel for rel, digest in expected.items() if observed.get(rel) != digest)


def _section(text: str, start: str, end: str) -> str:
    """Slice a document between two literal markers, failing loudly if either moved."""
    assert start in text, f"section start moved: {start!r}"
    after = text.split(start, 1)[1]
    assert end in after, f"section end moved: {end!r}"
    return after.split(end, 1)[0]


@pytest.fixture(scope="module")
def decision_text() -> str:
    return _read(DECISION)


@pytest.fixture(scope="module")
def decision_raw() -> str:
    return DECISION.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def prereg() -> dict:
    return yaml.safe_load(PREREG.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. Semantic-rule closure is not conflated with candidate satisfaction
# ---------------------------------------------------------------------------


class TestRuleVersusSatisfactionDistinction:
    """The determination's load-bearing distinction must be stated, not implied."""

    def test_both_sides_of_the_distinction_are_stated(self, decision_text: str) -> None:
        assert "Semantic rule closure" in decision_text
        assert "Satisfaction" in decision_text
        assert "This is governance work" in decision_text
        assert "This is the study's work" in decision_text

    def test_the_required_versus_not_required_rule_is_explicit(self, decision_text: str) -> None:
        assert (
            "a §G.A prerequisite is **required** for §G.B entry if and only if it is a *semantic "
            "rule* question" in decision_text
        )
        assert (
            "A prerequisite whose only residue is *satisfaction* is **not** required" in decision_text
        )

    def test_the_distinction_is_grounded_in_prior_accepted_text_not_invented(self) -> None:
        """XASSET-0031 §A and XASSET-0032 §C.1 must actually contain the cited language."""
        assert (
            "What cannot be closed is whether any construction satisfies it" in _read(XASSET_0031)
        )
        assert (
            "separate the semantic rule accepted authority *does* fix from the satisfaction question"
            in _read(XASSET_0032)
        )

    def test_overreach_the_decision_never_calls_a_satisfaction_residue_a_closed_gate(
        self, decision_text: str
    ) -> None:
        for gate in NOT_CLOSABLE_GATES:
            for verb in ("is now closed", "is hereby closed", "becomes closable"):
                assert f"{gate} {verb}" not in decision_text

    def test_overreach_satisfaction_is_not_licence_to_decide_semantics_at_run_time(
        self, decision_text: str
    ) -> None:
        assert "Satisfaction is not a licence to decide semantics at run time" in decision_text
        assert "not choosing what the rule is" in decision_text

    def test_the_run_time_rejection_it_preserves_is_real(self) -> None:
        assert (
            "File nothing and let a Stage-1 executor decide at run time.** Rejected outright"
            in _read(XASSET_0032)
        )


# ---------------------------------------------------------------------------
# 2. An absent candidate fact is never invented
# ---------------------------------------------------------------------------


class TestNoCandidateFactIsInvented:
    def test_no_gate_result_is_asserted_for_any_construction(self, decision_text: str) -> None:
        assert (
            "evaluates no gate for any construction and\nasserts no per-construction outcome"
            in DECISION.read_text(encoding="utf-8")
            or "evaluates no gate for any construction" in decision_text
        )

    def test_no_construction_id_appears_anywhere(self, decision_raw: str) -> None:
        """A construction id would mean a per-construction judgment had been recorded."""
        assert not re.search(r"\bC\d{3,4}__", decision_raw)

    @pytest.mark.parametrize("phrase", ["all 680 pass", "all 680 fail", "every construction passes"])
    def test_overreach_no_blanket_class_wide_result_is_asserted(
        self, decision_text: str, phrase: str
    ) -> None:
        assert phrase.lower() not in decision_text.lower()

    def test_universe_is_untouched_and_still_hypothetical(self) -> None:
        universe = CU.frozen_construction_universe()
        assert len(universe) == 680
        assert {c["source_architecture"] for c in universe.values()} == {
            "HYPOTHETICAL_SOURCE_ARCHITECTURE"
        }
        assert CU.universe_aggregate_sha256() == (
            "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
        )

    def test_the_decision_records_the_hypothetical_fact_rather_than_working_around_it(
        self, decision_text: str
    ) -> None:
        assert "HYPOTHETICAL_SOURCE_ARCHITECTURE" in decision_text


# ---------------------------------------------------------------------------
# 3. Prerequisite-blocked states remain prerequisite-blocked
# ---------------------------------------------------------------------------


class TestPrerequisiteClassPreserved:
    def test_prerequisite_definition_still_requires_a_named_dependency(self, prereg: dict) -> None:
        assert prereg["prerequisite_definition"]["requires_named_dependency"] is True

    def test_prerequisite_gates_are_still_exactly_g9_and_g12(self, prereg: dict) -> None:
        prerequisite = {
            g["gate_id"]
            for g in prereg["gate_sequence"]["gates"]
            if g["failure_disposition"] == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"
        }
        assert prerequisite == {"G9_REPRESENTATION", "G12_SNAPSHOT_ADMISSIBILITY_PATH"}

    def test_the_decision_does_not_reclassify_any_gate(self, decision_text: str) -> None:
        assert (
            "changes\nno gate's class, index, question, controlling authority, or failure disposition"
            in DECISION.read_text(encoding="utf-8")
            or "changes no gate's class" in decision_text
        )

    def test_g9_path3_reconciliation_is_carried_not_reopened(self, decision_text: str) -> None:
        assert "reconciled by both canonical artifacts" in decision_text.lower()

    def test_overreach_prerequisite_is_not_converted_into_uncertainty_for_convenience(
        self, decision_text: str
    ) -> None:
        assert "prerequisite limb is structurally unavailable" in decision_text
        for bad in (
            "prerequisite failures may be recorded as UNABLE_TO_DETERMINE",
            "record prerequisite gates as uncertainty",
        ):
            assert bad.lower() not in decision_text.lower()


# ---------------------------------------------------------------------------
# 4. Abstention remains a complete lawful outcome where accepted
# ---------------------------------------------------------------------------


class TestAbstentionRemainsComplete:
    def test_canonical_abstention_flag_is_untouched(self, prereg: dict) -> None:
        assert prereg["abstention_is_a_complete_outcome"] is True

    def test_the_eight_mandatory_abstention_conditions_are_intact(self, prereg: dict) -> None:
        assert len(prereg["mandatory_abstention_conditions"]) == 8

    def test_the_decision_records_abstention_as_a_representable_state(
        self, decision_text: str
    ) -> None:
        assert "abstention_is_a_complete_outcome" in decision_text

    def test_overreach_abstention_is_not_offered_as_a_substitute_for_a_missing_rule(
        self, decision_text: str
    ) -> None:
        """B3 must not be dissolved by declaring abstention the default."""
        assert (
            "Recording `UNABLE_TO_DETERMINE` instead would itself be a third,\n  unauthorized choice"
            in DECISION.read_text(encoding="utf-8")
            or "would itself be a third," in decision_text
        )


# ---------------------------------------------------------------------------
# 5 & 6. Source-dependent status becomes neither an automatic PASS nor an automatic FAIL
# ---------------------------------------------------------------------------


class TestSourceDependentIsNotAutomaticPass:
    def test_standard_1_is_preserved_verbatim_in_the_source(self) -> None:
        assert (
            "a specification requiring property P** is never by itself **(b) proof that P is "
            "lawfully satisfiable" in _read(XASSET_0030)
        )

    def test_the_decision_carries_standard_1_forward(self, decision_text: str) -> None:
        assert "Standard 1" in decision_text
        assert "never by itself (b) proof that P is lawfully satisfiable" in decision_text

    def test_overreach_no_pass_is_derived_from_a_frozen_requirement(
        self, decision_text: str
    ) -> None:
        assert "bars `PASS` inferred from the specification's own\n  requirement" in DECISION.read_text(
            encoding="utf-8"
        ) or "bars `PASS` inferred from the specification" in decision_text
        for bad in ("R5 therefore satisfies G3", "R8 therefore satisfies G9"):
            assert bad.lower() not in decision_text.lower()


class TestSourceDependentIsNotAutomaticFail:
    def test_standard_2_is_preserved_verbatim_in_the_source(self) -> None:
        assert "never inferred from nonexistence alone" in _read(XASSET_0030)

    def test_the_decision_carries_standard_2_forward(self, decision_text: str) -> None:
        assert "Standard 2" in decision_text
        assert "never inferred from nonexistence alone" in decision_text

    def test_the_g12_nonexistence_floor_is_not_regressed(self) -> None:
        assert (
            "the nonexistence of a snapshot successor may never, by itself, be recorded as `G12` "
            "`FAIL`" in _read(XASSET_0032)
        )

    def test_overreach_no_fail_is_derived_from_absence(self, decision_text: str) -> None:
        for bad in (
            "no source exists therefore fail",
            "nonexistence therefore fail",
            "all 680 fail because no source exists",
        ):
            assert bad.lower() not in decision_text.lower()


# ---------------------------------------------------------------------------
# 7. A real unresolved semantic choice still blocks §G.B
# ---------------------------------------------------------------------------


class TestGBIsNotUnlocked:
    def test_the_determination_is_mixed_not_a_green_light(self, decision_text: str) -> None:
        assert "SEMANTIC_CLOSURE_PARTIAL_THREE_RESIDUAL_BLOCKERS" in decision_text
        assert "§G.B is NOT yet unlocked" in decision_text

    def test_option_a_and_option_b_are_both_expressly_rejected(self, decision_text: str) -> None:
        assert "Neither option A nor option B is supportable" in decision_text

    def test_gb_may_not_begin(self, decision_text: str) -> None:
        assert "The step is therefore **not** met, and §G.B may not begin." in decision_text

    def test_the_structural_reason_is_stated_not_merely_asserted(self, decision_text: str) -> None:
        assert "Reconciliation is a transcription act" in decision_text
        assert "presupposes accepted semantics to transcribe" in decision_text

    def test_the_gb_invariant_is_restated_unweakened(self, decision_text: str) -> None:
        assert (
            "no outcome-producing executable code may be created,\nchanged, or left outside the "
            "bound execution identity after the final rebinding and before `ATTEMPT_1`"
            in DECISION.read_text(encoding="utf-8")
            or "no outcome-producing executable code may be created" in decision_text
        )

    def test_overreach_no_part_of_gb_is_entered(self, decision_text: str) -> None:
        assert "enters no part\nof §G.B" in DECISION.read_text(
            encoding="utf-8"
        ) or "enters no part of §G.B" in decision_text


class TestResidualBlockersSurviveAdversarially:
    @pytest.mark.parametrize("blocker", ["B1", "B2", "B3"])
    def test_each_blocker_is_named(self, decision_text: str, blocker: str) -> None:
        assert blocker in decision_text

    def test_all_three_blockers_carry_their_four_required_elements(
        self, decision_text: str
    ) -> None:
        section = _section(decision_text, "### E. Residual blockers", "### F. Effect on")
        assert section.count("**Authority.**") == 3
        assert section.count("**Degree of freedom.**") == 3
        assert section.count("**Consequence.**") == 3
        assert section.count("**Why the vocabulary cannot save it.**") == 3

    def test_each_blocker_is_shown_to_be_semantics_not_satisfaction(
        self, decision_text: str
    ) -> None:
        section = _section(decision_text, "### E. Residual blockers", "### F. Effect on")
        assert section.count("This is not satisfaction.") == 3
        assert "The question is not what any source exhibits" in section

    def test_b1_rests_on_xasset_0033_not_on_a_fresh_reading(self) -> None:
        assert "G12_COULD_ADMIT_TENSE_NOT_CLOSABLE" in _read(XASSET_0033)

    def test_b2_rests_on_xasset_0032_g4_verbatim(self) -> None:
        assert "Both readings are defensible and nothing selects" in _read(XASSET_0032)

    def test_b3_is_genuinely_unaddressed_in_the_canonical_artifacts(self) -> None:
        """The B3 gap must be real: the *only* gate-result mapping in canon is ``G2``-scoped.

        The value is word-bounded so that ``recorded as failing`` — prose inside the ``G2``
        ``incoherence_note`` about a *recording defect* — is not mistaken for a mapping rule.
        """
        raw = PREREG.read_text(encoding="utf-8")
        needle = re.compile(
            r"(?:records?|must be recorded as|recorded as)\s+`?"
            r"(PASS|FAIL|UNABLE_TO_DETERMINE)\b`?",
            re.IGNORECASE,
        )
        g2_block = _section(raw, "g2_reading_mapping:", "\nstage_1_testable_subset:")
        outside = [
            m.group(0)
            for m in needle.finditer(raw)
            if m.group(0) not in g2_block
        ]
        assert outside == [], f"a non-G2 mapping rule appeared in canon: {outside}"

    def test_b3_the_only_precedent_is_the_g2_table_and_it_is_not_generalizable(self) -> None:
        """``XASSET-0032`` must actually have refused to extend the ``G2`` mechanism."""
        assert "Adding reading slots would be a new rule" in _read(XASSET_0032)

    def test_overreach_no_blocker_is_downgraded_to_a_satisfaction_question(
        self, decision_text: str
    ) -> None:
        for bad in (
            "B1 is a satisfaction question",
            "B2 is a satisfaction question",
            "B3 is a satisfaction question",
        ):
            assert bad.lower() not in decision_text.lower()

    def test_overreach_the_disposition_inert_defence_is_expressly_foreclosed(
        self, decision_text: str
    ) -> None:
        assert "disposition-inert **today** only" in decision_text


# ---------------------------------------------------------------------------
# 8. No gate is "closed" merely for convenience
# ---------------------------------------------------------------------------


class TestNoGateIsClosed:
    def test_the_six_six_partition_is_declared_unchanged(self, decision_text: str) -> None:
        assert "`XASSET-0030`'s 6/6 gate map is UNCHANGED" in decision_text

    @pytest.mark.parametrize("gate", NOT_CLOSABLE_GATES)
    def test_every_not_closable_gate_stays_not_closable(
        self, decision_text: str, gate: str
    ) -> None:
        assert f"{gate} is now closable" not in decision_text
        assert f"{gate} → `PASS`" not in decision_text
        assert f"{gate} → `FAIL`" not in decision_text

    def test_execution_ready_is_explicitly_not_gate_closure(self, decision_text: str) -> None:
        section = _section(decision_text, "**D.6 — What D.1–D.5 do not do.**", "### E. Residual")
        assert "they close no gate" in section
        assert "remains **NOT CLOSABLE**" in section

    def test_the_five_execution_ready_items_are_all_named(self, decision_text: str) -> None:
        section = _section(decision_text, "### D. Execution-ready", "### E. Residual blockers")
        for item in EXECUTION_READY_ITEMS:
            assert f"`{item}`" in section

    def test_work_eliminated_is_justified_per_item_not_waved_through(
        self, decision_text: str
    ) -> None:
        section = _section(
            decision_text, "#### E.4 — Deliberately **not** created as blockers", "### F. Effect on"
        )
        for item in ("`G3`", "`G5`", "`G9`", "`G8`", "`G10`"):
            assert item in section

    def test_overreach_no_reservation_is_lifted(self, decision_text: str) -> None:
        assert "they lift no reservation" in decision_text
        for bad in ("§M.3 is lifted", "§M.4 is lifted", "the reservation no longer applies"):
            assert bad.lower() not in decision_text.lower()


# ---------------------------------------------------------------------------
# 9. No G3 / §K.1 / §E.1 silent resolution
# ---------------------------------------------------------------------------


class TestNoSilentResolution:
    def test_k1_remains_unresolved(self, decision_text: str) -> None:
        assert "§K.1 remains\nunresolved" in DECISION.read_text(
            encoding="utf-8"
        ) or "§K.1 remains unresolved" in decision_text
        assert "resolves `XASSET-0024` §K.1 neither\nway" in DECISION.read_text(
            encoding="utf-8"
        ) or "resolves `XASSET-0024` §K.1 neither way" in decision_text

    def test_e1_remains_unamended(self, decision_text: str) -> None:
        assert "§E.1 unamended" in decision_text

    def test_g3_is_neither_reopened_nor_used_as_a_premise(self, decision_text: str) -> None:
        assert "neither\nreopened, narrowed, extended, nor used as a premise" in DECISION.read_text(
            encoding="utf-8"
        ) or "nor used as a premise" in decision_text

    def test_canonical_open_reading_is_still_unresolved_by_this_program(self, prereg: dict) -> None:
        assert prereg["open_reading_handling"]["resolved_by_this_program"] is False
        assert prereg["open_reading_handling"]["relied_upon_by_this_program"] is False

    def test_the_closable_six_are_not_re_derived(self, decision_text: str) -> None:
        assert "No gate moves partition" in decision_text

    def test_overreach_no_g2_reading_map_extension(self, decision_text: str) -> None:
        section = _section(
            decision_text, "#### E.4 — Deliberately **not** created as blockers", "### F. Effect on"
        )
        assert "Extend `g2_reading_mapping` to other gates" in section


# ---------------------------------------------------------------------------
# 10. No canonical / enforcement / runner mutation
# ---------------------------------------------------------------------------


class TestCanonicalPinsStillMatch:
    """Strict digest verification of both frozen canonical pins.

    Corrected after FULL review ``4950747345`` MINOR 1. The prior form was
    ``assert A.canonical_protocol_sha256() if hasattr(A, "canonical_protocol_sha256") else True``,
    which verified nothing: the helper does not exist, so the ternary was unconditionally ``True``;
    had it existed, any non-empty return would have passed even when wrong; and the preregistration
    pin was never checked at all.
    """

    @pytest.mark.parametrize("relpath", sorted(EXPECTED_CANONICAL_PINS))
    def test_observed_digest_equals_the_exact_expected_pin(self, relpath: str) -> None:
        observed = _observed_canonical_digests()[relpath]
        assert observed == EXPECTED_CANONICAL_PINS[relpath]

    def test_no_pin_mismatches_at_all(self) -> None:
        assert _pin_mismatches(EXPECTED_CANONICAL_PINS) == []

    def test_the_authorization_module_declares_the_same_exact_pins(self) -> None:
        """Catches a module-side pin edit that the file-digest check alone would not see."""
        assert dict(A.CANONICAL_PINS) == EXPECTED_CANONICAL_PINS

    def test_the_modules_own_strict_verifier_agrees(self) -> None:
        """Option B cross-check: the module's own observed-hash helper reaches the same values."""
        assert dict(A.live_canonical_hashes()) == EXPECTED_CANONICAL_PINS
        assert A.pins_are_placeholders() is False

    @pytest.mark.parametrize("relpath", sorted(EXPECTED_CANONICAL_PINS))
    def test_adversarial_a_mutated_expected_digest_is_detected(self, relpath: str) -> None:
        """Proof the comparison discriminates — no canonical file is touched.

        One hex character of the *expectation* is flipped; the mismatch must surface for exactly
        that relpath and for no other.
        """
        digest = EXPECTED_CANONICAL_PINS[relpath]
        flipped = ("f" if digest[0] != "f" else "0") + digest[1:]
        assert flipped != digest

        mutated = dict(EXPECTED_CANONICAL_PINS)
        mutated[relpath] = flipped
        assert _pin_mismatches(mutated) == [relpath]

    def test_adversarial_both_pins_mutated_are_both_detected(self) -> None:
        mutated = {rel: "0" * 64 for rel in EXPECTED_CANONICAL_PINS}
        assert _pin_mismatches(mutated) == sorted(EXPECTED_CANONICAL_PINS)

    def test_the_predecessor_pins_are_retained_as_history(self) -> None:
        """The literals XASSET-0029 accepted, asserted against the module's historical constant."""
        assert dict(A.XASSET_0029_CANONICAL_PINS) == XASSET_0029_CANONICAL_PINS
        assert dict(A.CANONICAL_PINS) != XASSET_0029_CANONICAL_PINS

    def test_adversarial_a_truthiness_check_would_not_have_caught_either(self) -> None:
        """Pins the reviewer's diagnosis: truthiness is satisfied by a wrong digest."""
        wrong = "0" * 64
        assert bool(wrong) is True
        assert wrong != EXPECTED_CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH]
        assert wrong != EXPECTED_CANONICAL_PINS[A.CANONICAL_PREREGISTRATION_RELPATH]
        assert wrong != XASSET_0029_CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH]


class TestNoProtectedMutation:
    @pytest.mark.parametrize("relpath", PROTECTED_RELPATHS)
    def test_protected_path_still_exists_and_is_load_bearing_or_canonical(
        self, relpath: str
    ) -> None:
        assert (ROOT / relpath).is_file()

    # AMENDED BY XASSET-0036 SS-E.3/SS-E.6. This filing created no runner and extended nothing,
    # and both remain true of it. SS-G.B steps 4-5 later created the outcome-producing modules and
    # bound them, which is the outcome this filing's own successor model called for.
    def test_the_six_paths_this_filing_saw_are_all_retained(self) -> None:
        assert {
            "level1_stage1_execution_authorization.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "level1_construction_universe_closure_validator.py",
            "research/level1_endpoint_evidence/PROTOCOL_V1.md",
            "research/level1_endpoint_evidence/pre_registration.yaml",
            "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
        } <= set(A.LOAD_BEARING_RELPATHS)

    def test_the_outcome_producing_modules_are_bound_not_loose(self) -> None:
        """The governing SS-G.B invariant: no outcome-producing code outside the boundary."""
        for relative in ("level1_stage1_runner.py", "level1_stage1_result_validator.py"):
            assert (ROOT / relative).exists()
            assert relative in A.LOAD_BEARING_RELPATHS
        assert not (ROOT / "level1_stage1_result_writer.py").exists()

    def test_the_decision_disclaims_every_protected_mutation(self, decision_text: str) -> None:
        for phrase in (
            "corrects no validator",
            "extends no `LOAD_BEARING_RELPATHS`",
            "amends no\ncanonical file",
            "creates no Stage-1 runner",
        ):
            raw = DECISION.read_text(encoding="utf-8")
            assert phrase in raw or phrase.replace("\n", " ") in decision_text

    def test_overreach_no_rebinding_is_performed_or_claimed(self, decision_text: str) -> None:
        assert "performs no load-bearing reauthorization or rebinding" in decision_text


# ---------------------------------------------------------------------------
# 11. No execution artifact
# ---------------------------------------------------------------------------


class TestNoExecutionArtifact:
    @pytest.mark.parametrize("relpath", EXECUTION_ARTIFACT_RELPATHS)
    def test_execution_artifact_is_absent(self, relpath: str) -> None:
        assert not (ROOT / relpath).exists()

    def test_stage_1_is_not_authorized(self) -> None:
        authorized, _reason = A.new_execution_is_authorized()
        assert authorized is False

    def test_results_path_was_not_created_by_any_filing(self, prereg: dict) -> None:
        assert prereg["result_schema"]["results_path_created_by_this_filing"] is False

    def test_the_decision_states_stage_1_remains_unarmed(self, decision_text: str) -> None:
        assert "Stage 1 is UNARMED and NOT EXECUTABLE" in decision_text
        assert "`ATTEMPT_1` is intact, unclaimed, unconsumed" in decision_text

    def test_no_protected_risk_result_path_is_referenced(self, decision_raw: str) -> None:
        for needle in PROTECTED_RISK_NEEDLES:
            assert needle not in decision_raw


# ---------------------------------------------------------------------------
# Cross-cutting integrity
# ---------------------------------------------------------------------------


class TestFilingIntegrity:
    def test_frontmatter_declares_the_expected_identity(self, decision_raw: str) -> None:
        assert "decision_id: XASSET-0034" in decision_raw
        assert "status: Proposed" in decision_raw
        assert "supporting_artifact: test_level1_stage1_semantic_closure_feasibility.py" in (
            decision_raw
        )

    def test_the_decision_cites_the_evaluation_posture_it_relies_on(self) -> None:
        """XASSET-0028 §F must actually say what §B.5 attributes to it."""
        assert (
            "Stage 1 evaluates whether a **frozen specification** is lawfully satisfiable"
            in _read(XASSET_0028)
        )

    def test_the_circularity_it_resolves_is_real_in_the_source(self) -> None:
        assert "cannot be closed by governance at all" in _read(XASSET_0032)
        assert "Resolve all required §G.A semantic/governance prerequisites" in _read(XASSET_0030)

    def test_this_module_contains_no_vacuous_assertions(self) -> None:
        """No assertion may be satisfiable without exercising the property it claims to pin.

        Widened after FULL review ``4950747345`` MINOR 1. The prior form checked only bare truthy
        literals, which is why it did not catch
        ``assert A.canonical_protocol_sha256() if hasattr(...) else True`` — a *ternary* whose
        fallback branch was an unconditional ``True``. Three shapes are now rejected:

        1. ``assert <truthy literal>``;
        2. ``assert X if cond else <truthy literal>`` — an unconditional-pass fallback;
        3. ``assert X or <truthy literal>`` — short-circuits to true regardless of ``X``.
        """
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))

        def _is_truthy_const(node: ast.expr) -> bool:
            return isinstance(node, ast.Constant) and bool(node.value)

        vacuous: list[tuple[int, str]] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assert):
                continue
            test = node.test
            if _is_truthy_const(test):
                vacuous.append((node.lineno, "bare truthy literal"))
            elif isinstance(test, ast.IfExp) and (
                _is_truthy_const(test.body) or _is_truthy_const(test.orelse)
            ):
                vacuous.append((node.lineno, "ternary with unconditional-pass branch"))
            elif isinstance(test, ast.BoolOp) and isinstance(test.op, ast.Or) and any(
                _is_truthy_const(value) for value in test.values
            ):
                vacuous.append((node.lineno, "or-ed truthy literal"))

        assert vacuous == [], f"vacuous assertions: {vacuous}"

    def test_the_vacuous_assertion_guard_catches_the_shape_that_slipped_through(self) -> None:
        """Direct regression proof against the exact defect FULL review 4950747345 found."""

        def _vacuous_shapes(src: str) -> list[str]:
            tree = ast.parse(src)

            def _is_truthy_const(node: ast.expr) -> bool:
                return isinstance(node, ast.Constant) and bool(node.value)

            found: list[str] = []
            for node in ast.walk(tree):
                if not isinstance(node, ast.Assert):
                    continue
                test = node.test
                if _is_truthy_const(test):
                    found.append("bare")
                elif isinstance(test, ast.IfExp) and (
                    _is_truthy_const(test.body) or _is_truthy_const(test.orelse)
                ):
                    found.append("ternary")
                elif isinstance(test, ast.BoolOp) and isinstance(test.op, ast.Or) and any(
                    _is_truthy_const(value) for value in test.values
                ):
                    found.append("or")
            return found

        original_defect = (
            'assert A.canonical_protocol_sha256() '
            'if hasattr(A, "canonical_protocol_sha256") else True'
        )
        assert _vacuous_shapes(original_defect) == ["ternary"]
        assert _vacuous_shapes("assert True") == ["bare"]
        assert _vacuous_shapes("assert x == 1 or True") == ["or"]
        # A genuine assertion of each shape's non-vacuous form must NOT be flagged.
        assert _vacuous_shapes("assert a if cond else b") == []
        assert _vacuous_shapes("assert observed == expected") == []
