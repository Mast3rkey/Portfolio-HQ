"""Adversarial tests pinning the XASSET-0033 ``G12`` "could admit" tense determination.

``XASSET-0032`` §H left ``G12_SNAPSHOT_ADMISSIBILITY_PATH`` with exactly one blocker: the **tense of
"could admit"**. ``XASSET-0033`` takes that single question and returns a bounded negative —
``G12_COULD_ADMIT_TENSE_NOT_CLOSABLE`` — while closing one further sub-question and narrowing the
blocker.

These tests exist so the determination is **mechanically checkable rather than prose**. Every rule,
heading, qualifier, and section boundary below is read from committed bytes — the two canonical
artifacts and the accepted decisions — never asserted from this module's own opinion.

For each finding the suite pins two things: the **intended rule**, and its **nearest plausible
overreach** — the stronger claim a successor might be tempted to read out of the same text, which the
determination must refuse. Three overreaches matter most here and each has its own guard:

1. **Dissolution.** ``PROTOCOL_V1.md`` §6 and §6.1 both restate ``G12`` *without* the candidate-relative
   clause. A successor could "resolve" the tense question by dropping its subject. §C forecloses that,
   and ``TestClauseIsOperative`` pins both the temptation and the precedence rule that defeats it —
   while ``test_the_shorter_restatements_are_not_called_a_defect`` refuses the opposite overreach of
   manufacturing a governed-correction finding out of an abbreviation.
2. **Over-closure.** §E shows the two texts previously cited for the present-tense reading are
   *ordering* statements. The tempting next step is to call them a refutation.
   ``TestOrderingTextsAreNeutral`` pins that they are recorded as **neutral**, and that the inference
   available *from* the ordering to the present-tense reading is expressly preserved.
3. **Silent closure.** ``TestNoClosureIsClaimed`` and ``TestBothReadingsSurviveAdversarially`` fail if
   the decision ever asserts a ``G12`` result, drops either reading, or declares the competing reading
   unlawful.

They also pin the *negative space* that makes the determination honest: that the ``XASSET-0030`` 6/6
gate partition is unchanged, that ``G1``/``G2``/``G4``/``G6``/``G7``/``G11`` are not re-derived, that
``XASSET-0031``'s ``G3`` determination is neither reopened nor relied upon, that ``XASSET-0024`` §K.1 is
unresolved, that ``XASSET-0020`` §E.1 is unamended, that the ``XASSET-0032`` §H.1 "nonexistence is never
by itself FAIL" floor is not regressed, that ``G12``'s identifiability-only scope is not widened into
full §J.1 admission, and that no protected RISK result path is read or referenced.

Nothing here arms, claims, completes, or executes Stage 1. No gate is evaluated for any construction.
No results document, lane directory, attestation, claim, completion, or ledger entry is created or read
for authorization purposes.
"""

from __future__ import annotations

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
XASSET_0025 = GOV / "XASSET-0025-level1-endpoint-source-and-authority-identification.md"
XASSET_0026 = (
    GOV / "XASSET-0026-level1-endpoint-evidence-program-shape-and-sleeve-selection-basis.md"
)
XASSET_0027 = (
    GOV / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
)
XASSET_0030 = GOV / "XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md"
XASSET_0031 = (
    GOV / "XASSET-0031-endpoint-0001-stage-1-g3-share-of-the-whole-semantic-determination.md"
)
XASSET_0032 = (
    GOV / "XASSET-0032-endpoint-0001-stage-1-remaining-semantic-gate-determination.md"
)
DECISION = GOV / "XASSET-0033-endpoint-0001-stage-1-g12-could-admit-tense-determination.md"

#: The gates this unit must NOT re-derive — XASSET-0030's six closable gates.
CLOSABLE_SNAPSHOT_GATES = ("G1", "G2", "G4", "G6", "G7", "G11")

#: The gates XASSET-0032 determined and this unit must not reopen as premises.
XASSET_0032_GATES = ("G5", "G8", "G9", "G10")

#: Protected RISK-0001 result identifiers, assembled from fragments so that asserting their absence
#: does not itself introduce the literal string into this file.
PROTECTED_RISK_NEEDLES = ("risk" + "_results", "RISK-0001" + " results")


def _collapse(text: str) -> str:
    """Collapse Markdown hard-wrapping so a wrapped sentence matches as one string.

    Blockquote markers are stripped first: a hard-wrapped ``>`` quote would otherwise leave a stray
    ``>`` mid-sentence and defeat an otherwise-correct match.
    """
    text = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    return re.sub(r"\s+", " ", text)


def _read(path: Path) -> str:
    return _collapse(path.read_text(encoding="utf-8"))


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


@pytest.fixture(scope="module")
def protocol_raw() -> str:
    return PROTOCOL.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def g12_gate(prereg: dict) -> dict:
    gates = prereg["gate_sequence"]["gates"]
    matches = [g for g in gates if g["gate_id"] == "G12_SNAPSHOT_ADMISSIBILITY_PATH"]
    assert len(matches) == 1, "G12 must appear exactly once in the canonical gate sequence"
    return matches[0]


# ======================================================================================
# The canonical gate itself — the object of the whole determination
# ======================================================================================


class TestCanonicalG12IsUnchanged:
    """The gate's own bytes must be exactly what the determination reasons about."""

    def test_g12_question_carries_the_candidate_relative_clause(self, g12_gate):
        q = _collapse(g12_gate["question"])
        assert "could admit the candidate" in q
        assert "identifiable" in q

    def test_g12_identity_fields_are_unchanged(self, g12_gate):
        assert g12_gate["gate_index"] == 12
        assert (
            g12_gate["controlling_authority"]
            == "XASSET-0024_J_1_AND_J_2_AND_XASSET_0026_G_2_CONSTRAINT_3"
        )
        assert g12_gate["failure_disposition"] == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"

    def test_this_filing_did_not_edit_the_gate_wording(self, g12_gate):
        """Nearest overreach: 'fixing' the tense by rewriting the gate."""
        assert g12_gate["question"].strip().startswith("Is a lawful XASSET-0021 snapshot successor")
        assert "noting that no snapshot successor is created, extended, or authorized" in _collapse(
            g12_gate["question"]
        )

    def test_prerequisite_definition_still_requires_a_named_dependency(self, prereg):
        pd = prereg["prerequisite_definition"]
        assert pd["term"] == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"
        assert pd["requires_named_dependency"] is True


# ======================================================================================
# §C — the clause is operative; the dissolution route is closed
# ======================================================================================


class TestClauseIsOperative:
    """§C. The tempting escape hatch, and the precedence rule that closes it."""

    def test_the_temptation_is_real_protocol_row_12_omits_the_clause(self, protocol_raw):
        """Pins the actual divergence the determination had to address."""
        row = [ln for ln in protocol_raw.splitlines() if ln.startswith("| 12 |")]
        assert len(row) == 1, "PROTOCOL §6 gate table row 12 moved"
        assert "could admit" not in row[0]
        assert "identifiable" in row[0]

    def test_the_temptation_is_real_protocol_6_1_omits_the_clause(self, protocol_raw):
        s61 = _section(protocol_raw, '### 6.1 What "categorical" means, precisely', "## 7.")
        assert "could admit" not in s61
        assert "identifiable" in s61

    def test_the_yaml_governs_gates_by_name(self, protocol_raw):
        head = _collapse(protocol_raw)
        assert (
            "canonical for every closed identity, candidate, gate, ordering, vocabulary, and count"
            in head
        )
        assert "It cannot enlarge or override the YAML" in head
        assert (
            "the YAML governs and the difference is a defect requiring a governed correction" in head
        )

    def test_decision_records_the_clause_as_operative(self, decision_text):
        assert '"that could admit the candidate" is operative gate text' in decision_text

    def test_decision_forecloses_evaluating_g12_with_the_conjunct_dropped(self, decision_text):
        assert (
            "may not be evaluated as bare successor-identifiability with the candidate-relative "
            "conjunct dropped" in decision_text.replace("**", "")
        )

    def test_the_shorter_restatements_are_not_called_a_defect(self, decision_text):
        """Nearest overreach in the opposite direction: manufacturing a defect finding.

        The precedence rule makes a *difference* a defect. An abbreviation in a summary table and an
        explanatory gloss is not a difference in what the gate requires, and the determination must
        say so rather than create correction work with no semantic content.
        """
        assert "This is **not** a defect finding against `PROTOCOL_V1.md`" in decision_text
        assert "No governed correction is triggered" in decision_text


# ======================================================================================
# §D/§G — both readings must survive, adversarially
# ======================================================================================


class TestBothReadingsSurviveAdversarially:
    """A determination that quietly dropped or adopted a reading would fail here."""

    def test_present_tense_reading_is_stated_with_its_ground(self, decision_text):
        assert "Present-tense / current-candidate-capability" in decision_text
        assert "must be able to admit the candidate as it stands at evaluation time" in decision_text
        assert "HYPOTHETICAL_SOURCE_ARCHITECTURE" in decision_text

    def test_forward_looking_reading_is_stated_with_its_ground(self, decision_text):
        assert "Forward-looking / ordered-successor-capability" in decision_text
        assert "Existence now is not required" in decision_text

    def test_the_two_readings_are_recorded_as_producing_opposite_results(self, decision_text):
        assert "Yields `FAIL` for all 680" in decision_text
        assert "Yields `PASS` on the identifiability conjunct" in decision_text

    def test_the_competing_reading_is_expressly_not_declared_unlawful(self, decision_text):
        assert "It survives as *lawful*, not as *correct*" in decision_text
        assert "Removing the *supports* for a reading does not make the reading unlawful" in (
            decision_text
        )

    def test_executor_divergence_table_names_both_grounds(self, decision_text):
        assert "may therefore still lawfully diverge" in decision_text
        assert "Executor A's ground is narrower than it was before this filing" in decision_text


# ======================================================================================
# §E — the core finding: the cited texts are ordering statements, and are NEUTRAL
# ======================================================================================


class TestOrderingTextsAreNeutral:
    """§E. Read in their own sections, both cited texts fix position, not capability."""

    def test_xasset_0026_g2_heading_declares_ordering_constraints(self):
        assert "Four ordering constraints that do bind, on every packaging" in _read(XASSET_0026)

    def test_constraint_3_title_is_itself_an_ordering_statement(self):
        assert "Snapshot successor after evidence, before any application" in _read(XASSET_0026)

    def test_constraint_3_operative_sentence_is_paired_and_brackets_position(self):
        text = _read(XASSET_0026)
        assert (
            "A snapshot successor cannot admit evidence that does not yet exist, and no application "
            "may read the evidence before it does" in text
        )

    def test_xasset_0026_states_the_third_constraints_position_is_fixed(self):
        assert "the third's position in the sequence *is* fixed" in _read(XASSET_0026)

    def test_xasset_0027_p2_is_a_list_of_required_future_successors(self):
        assert "Separately required successors, none authorized here" in _read(XASSET_0027)

    @pytest.mark.parametrize(
        "qualifier",
        (
            "if and when a candidate source exists to test",
            "at the first later stage where actual candidate endpoint values or sets coexist",
            "only if and when a candidate source is not self-contained",
        ),
    )
    def test_p2_siblings_carry_overt_timing_qualifiers(self, qualifier):
        """The G12 clause sits in the same grammatical slot as three explicit timing notes."""
        assert qualifier in _read(XASSET_0027)

    def test_the_g12_clause_occupies_that_same_slot(self):
        assert "cannot admit evidence that does not yet exist" in _read(XASSET_0027)

    def test_decision_records_them_as_neutral_not_as_refutation(self, decision_text):
        """The nearest overreach: treating an ordering frame as defeating present-tense."""
        assert "Both are ordering statements, and an ordering statement is consistent with either "
        assert "Neither is a capability verdict" in decision_text

    def test_decision_expressly_preserves_the_inference_from_ordering(self, decision_text):
        """§E.3 must keep the present-tense proponent's route open, not quietly close it."""
        assert "That inference is available" in decision_text
        assert "Why this is a narrowing and not a closure" in decision_text

    def test_decision_states_exactly_what_it_removes(self, decision_text):
        assert (
            "is **not** available is citing §G.2 constraint 3 or §P.2 as *independent affirmative "
            "support* for the present-tense reading" in decision_text
        )


# ======================================================================================
# §F — the forward-looking supports are recorded as inference, not as authority
# ======================================================================================


class TestForwardLookingSupportIsNotOverstated:
    def test_the_canonical_register_statements_exist_verbatim(self, prereg):
        desc = _collapse(prereg["stages"]["stage_1"]["description"])
        assert "Stage 1 evaluates constructibility" in desc
        assert "is identifiable for that candidate" in desc
        assert prereg["stages"]["stage_1"]["acquires_data"] is False
        assert prereg["stages"]["stage_1"]["produces_admissible_evidence"] is False

    def test_the_satisfiability_register_is_in_the_gate_canonical_yaml(self):
        raw = _collapse(PREREG.read_text(encoding="utf-8"))
        assert (
            "Stage 1 evaluates whether the frozen specification is lawfully satisfiable under the "
            "twelve gates" in raw
        )
        assert "the registered specification was evaluated and blocked" in raw

    def test_decision_labels_the_bridge_as_inference_not_authority(self, decision_text):
        assert (
            "therefore every gate question's modal is read counterfactually" in decision_text
        )
        assert "records it as such rather than as authority" in decision_text

    def test_decision_refuses_the_universal_negative_objection(self, decision_text):
        """XASSET-0025 §D forecloses 'a gate cannot fail every candidate'."""
        assert "A universal structural negative is not itself disqualifying" in decision_text
        assert "is a coherent, honest Stage-1 outcome, not an absurdity" in decision_text

    def test_xasset_0025_section_d_actually_says_that(self):
        assert (
            "This is not a finding about any particular source; it is the shape of the current "
            "authority" in _read(XASSET_0025)
        )


# ======================================================================================
# §A/§G — no closure is claimed, and no gate result is produced
# ======================================================================================


class TestNoClosureIsClaimed:
    def test_the_verdict_is_the_bounded_negative(self, decision_text):
        assert "G12_COULD_ADMIT_TENSE_NOT_CLOSABLE" in decision_text
        assert "`G12` remains **NOT CLOSABLE**" in decision_text

    def test_the_surviving_degree_of_freedom_is_stated_exactly(self, decision_text):
        assert (
            "No accepted text defines the modal \"could\", states a gate-level tense or modal rule, "
            "or ranks the canonical Stage-1 register statements" in decision_text
        )

    def test_no_g12_result_is_asserted_for_any_construction(self, decision_text):
        assert "No gate is evaluated for any construction" in decision_text
        assert "No candidate disposition, cell outcome, or roll-up is produced" in decision_text

    def test_the_negative_is_recorded_as_reached_on_authority_not_convenience(self, decision_text):
        assert (
            "This is a negative determination reached on the authority, not a deferral for "
            "convenience" in decision_text.replace("**", "")
        )

    def test_the_smallest_future_authority_is_named_and_not_authorized(self, decision_text):
        assert "Smallest sufficient corrective — a `G12`-scoped modal statement" in decision_text
        assert "It requires **no new evidence**" in decision_text
        assert "Neither is authorized, drafted, scoped, or begun by this filing" in decision_text

    def test_the_broader_corrective_is_disclosed_with_its_blast_radius(self, decision_text):
        """A successor must not take the wider rule as free — it reaches every gate."""
        assert "would therefore be an invalidation trigger for that partition" in decision_text
        assert "as a **caution**, not a recommendation" in decision_text


# ======================================================================================
# Regression guards — the floors XASSET-0032 already closed must not slip
# ======================================================================================


class TestNoNonexistenceEqualsFailRegression:
    """XASSET-0032 §H.1's floor is the single most regressible rule in this area."""

    def test_the_floor_is_restated_in_this_decision(self, decision_text):
        assert "nonexistence of a successor is never by itself `FAIL`" in decision_text

    def test_executor_a_ground_is_distinguished_from_successor_nonexistence(self, decision_text):
        assert (
            "its ground is *candidate* nonexistence, not *successor* nonexistence" in decision_text
        )

    def test_the_decision_never_asserts_a_successor_exists(self, decision_text):
        assert (
            "**No snapshot successor** is created, extended, replaced, identified as existing, or "
            "authorized" in decision_text
        )

    def test_no_snapshot_successor_appears_anywhere_in_the_repository_as_a_record(self):
        """A successor is a governance artifact, not a claim in prose."""
        assert not (ROOT / "intelligence/level1_application").exists()


class TestScopeIsNotWidenedIntoFullJ1Admission:
    """XASSET-0032 §H.2 — G12 is identifiability only."""

    def test_the_scope_limit_is_restated(self, decision_text):
        assert "identifiability only, never full §J.1 admission" in decision_text

    def test_the_testability_table_still_says_identifiability_only(self, protocol_raw):
        s81 = _section(protocol_raw, "### 8.1 The Stage-1-testable subset", "### 8.2")
        assert "`G12`, identifiability only" in _collapse(s81)

    @pytest.mark.parametrize(
        "j1_condition",
        ("hash-match", "validator-pass", "governed freshness", "own validator passes"),
    )
    def test_no_j1_admission_condition_is_imported_as_a_g12_criterion(
        self, decision_text, j1_condition
    ):
        """The overreach: silently converting a partial gate into a full admission test.

        The determination may *name* §J.1's conditions when restating the scope limit, but must never
        state that G12 tests them.
        """
        assert f"`G12` tests {j1_condition}" not in decision_text
        assert f"G12 tests {j1_condition}" not in decision_text


# ======================================================================================
# §H — citation corrections, classification unchanged
# ======================================================================================


class TestCitationCorrections:
    def test_the_dependency_chain_is_in_protocol_section_17_not_12(self, protocol_raw):
        chain = (
            "new evidence → **lawful snapshot successor** → endpoint-capable downstream consumption "
            "→ application."
        )
        s12 = _section(protocol_raw, "## 12. Parameters", "## 13.")
        s17 = _section(protocol_raw, "## 17. Lifecycle and downstream boundary", "## Amendment")
        assert chain not in s12
        assert chain in s17

    def test_the_prior_citation_slip_is_real(self):
        """Reproduces XASSET-0032 §H.3's actual wording, so the correction is not invented."""
        assert "`PROTOCOL_V1.md` §12 records the dependency order" in _read(XASSET_0032)

    def test_the_correction_is_recorded_as_section_number_only(self, decision_text):
        assert "The **quotation is accurate**; only the section number is wrong" in decision_text

    def test_both_corrections_leave_the_classification_unchanged(self, decision_text):
        corrections = _section(
            decision_text, "### H. Corrections to prior basis statements", "### I."
        )
        assert corrections.count("NOT CLOSABLE** — unchanged") == 2

    def test_no_prior_decision_text_is_edited(self, decision_text):
        assert "**no prior decision's text is edited**" in decision_text


# ======================================================================================
# Preservation — the negative space that keeps the determination honest
# ======================================================================================


class TestPreservation:
    def test_the_xasset_0030_partition_is_declared_unchanged(self, decision_text):
        assert "The `XASSET-0030` **6/6 gate partition is unchanged**" in decision_text

    @pytest.mark.parametrize("gate", CLOSABLE_SNAPSHOT_GATES)
    def test_no_closable_gate_is_re_derived(self, decision_text, gate):
        """Naming a gate in the preservation list is fine; re-determining one is not."""
        for verdict in ("CLOSABLE", "NOT CLOSABLE", "PASS", "FAIL"):
            assert f"`{gate}` {verdict}" not in decision_text
            assert f"{gate} is {verdict}" not in decision_text

    @pytest.mark.parametrize("gate", XASSET_0032_GATES)
    def test_no_xasset_0032_gate_is_reopened_or_used_as_a_premise(self, decision_text, gate):
        for verdict in ("CLOSABLE", "NOT CLOSABLE", "PASS", "FAIL"):
            assert f"`{gate}` {verdict}" not in decision_text

    def test_g3_is_neither_reopened_nor_used_as_a_premise(self, decision_text):
        assert (
            "`XASSET-0031`'s `G3` determination is **neither reopened nor used as a premise**"
            in decision_text
        )

    def test_k1_remains_unresolved(self, decision_text):
        assert "`XASSET-0024` §K.1 is **not resolved**" in decision_text

    def test_e1_remains_unamended(self, decision_text):
        assert "`XASSET-0020` §E.1 is **not amended**" in decision_text

    def test_xasset_0024_k1_is_still_open_in_the_canonical_yaml(self, prereg):
        gate2 = [
            g for g in prereg["gate_sequence"]["gates"] if g["gate_id"] == "G2_MAGNITUDE_INTRINSICALITY"
        ][0]
        assert "two open readings" in _collapse(gate2["question"])

    def test_the_disposition_inertness_observation_is_not_converted_into_a_licence(
        self, decision_text
    ):
        assert "still is not a licence" in decision_text
        assert "every applicable gate must still be evaluated and recorded" in decision_text


class TestStage1RemainsUnarmedAndNotExecutable:
    def test_no_execution_is_authorized(self):
        authorized, reason = A.new_execution_is_authorized()
        assert authorized is False
        assert "no attestation present" in reason

    def test_attempt_1_identity_is_untouched(self):
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

    def test_canonical_pins_are_unchanged(self):
        assert (
            A.sha256_file(ROOT / A.CANONICAL_PROTOCOL_RELPATH)
            == "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
        )
        assert (
            A.sha256_file(ROOT / A.CANONICAL_PREREGISTRATION_RELPATH)
            == "6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c"
        )

    def test_load_bearing_paths_are_unchanged_and_carry_no_runner(self):
        assert len(A.LOAD_BEARING_RELPATHS) == 6
        assert not any(
            "runner" in p or "stage1_results" in p for p in A.LOAD_BEARING_RELPATHS
        ), A.LOAD_BEARING_RELPATHS

    def test_no_results_document_exists(self):
        assert not (ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()

    def test_the_universe_is_unchanged(self):
        universe = CU.generate_construction_universe()
        assert len(universe) == 680

    def test_the_decision_states_stage_1_remains_unarmed(self, decision_text):
        assert "Stage 1 remains NOT EXECUTABLE and UNARMED" in decision_text
        assert "`ATTEMPT_1` is intact and unconsumed" in decision_text


class TestNoPortfolioEffectAndNoProtectedEvidence:
    def test_decision_disclaims_every_portfolio_effect(self, decision_text):
        assert "**No portfolio effect of any kind**" in decision_text

    def test_no_endpoint_or_share_value_appears(self, decision_raw):
        """No §C quantity value may appear anywhere in this filing."""
        for contaminated in ("18.67", "14.67", "16.67", "33.32", "63.25"):
            assert contaminated not in decision_raw

    def test_no_protected_risk_result_path_is_referenced(self, decision_raw):
        for needle in PROTECTED_RISK_NEEDLES:
            assert needle not in decision_raw

    def test_this_module_reads_no_protected_risk_path(self):
        """Self-check: this suite must not itself name a protected results path.

        The needles are assembled from fragments so that asserting their absence does not put the
        literal string into this file and make the check vacuously self-defeating.
        """
        source = Path(__file__).read_text(encoding="utf-8")
        for needle in PROTECTED_RISK_NEEDLES:
            assert source.count(needle) == 0
