"""Adversarial tests pinning the ``XASSET-0035`` residual-semantic-blocker determination.

``XASSET-0034`` returned ``SEMANTIC_CLOSURE_PARTIAL_THREE_RESIDUAL_BLOCKERS`` and left exactly three
semantic degrees of freedom standing between the program and ``XASSET-0030`` §G.B:

* **B1** — the tense of ``G12``'s "could admit";
* **B2** — ``XASSET-0024`` §H.4 consumption semantics for the 360 ``DIRECT_ALTERNATIVE`` constructions
  carrying a sleeve counterpart;
* **B3** — the shared *recording posture* for reserved-satisfiability gates evaluated against a frozen
  ``HYPOTHETICAL_SOURCE_ARCHITECTURE`` specification.

``XASSET-0035`` resolves all three. These tests exist so that resolution is **mechanically checkable
rather than prose**. Every rule below is read from committed bytes — the two canonical artifacts, the
frozen universe, and the accepted decisions — never asserted from this module's own opinion.

Two distinct routes are used by the determination and the suite pins the distinction, because conflating
them is how a governance unit legislates while appearing to read:

* **B2 and B3 are INTERPRETIVE** — accepted authority selects, and the competing reading is foreclosed by
  authority already in force. The suite pins the selecting texts and the foreclosure.
* **B1 is CONSTITUTIVE** — accepted authority does not select, and Lane-G governance states the rule
  prospectively. The suite pins that the decision *says so*, in its own headings, rather than presenting
  a governed choice as a discovered reading.

For each finding the suite pins the intended rule **and its nearest plausible overreach** — the stronger
claim a successor might read out of the same text, which the determination must refuse. The four
overreaches that matter most each have their own guard:

1. **B3 over-generalisation.** Stated broadly, B3 would swallow ``G10`` (nullifying B2's categorical
   consequence) and ``G12`` (nullifying B1). ``TestB3ScopeFence`` fails if B3 ever reaches ``G8``,
   ``G10``, ``G12``, or ``G2``'s reading map.
2. **Relabelling.** B2 must not convert a ``DIRECT_ALTERNATIVE`` construction into an ``UNORDERED_PAIR``
   one. ``TestB2DoesNotRelabelOrMutateIdentity`` pins the frozen universe, its cardinality, and its hash.
3. **Outcome assertion.** ``TestNoGateResultIsAsserted`` and ``TestSatisfactionResiduesPreserved`` fail if
   any per-construction gate result is recorded or any ``XASSET-0034`` §D residue is closed.
4. **Standards erosion.** ``TestStandardsPreservedBothDirections`` pins ``XASSET-0030`` §E Standards 1 and
   2 in both directions — neither by-construction ``PASS`` nor nonexistence-``FAIL``.

They also pin the negative space that makes the determination honest: the ``XASSET-0030`` 6/6 partition
unchanged with no §E.1 trigger fired, ``XASSET-0024`` §K.1 unresolved, ``XASSET-0020`` §E.1 unamended,
``XASSET-0031``'s ``G3`` neither reopened nor used as a premise, ``G9``'s determined path-1 failure still
prerequisite-blocked, abstention still a complete outcome, no canonical/validator/authorization/runner
mutation, and no execution artifact.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any construction**;
where a derivation function is exercised it is fed isolated synthetic gate-result dictionaries, the method
``XASSET-0030`` §B used. No results document, lane directory, attestation, claim, completion, or ledger
entry is created or read for authorization purposes. No ``risk_lane_boundary`` protected result path is
read, listed, opened, or referenced.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest
import yaml

import level1_construction_universe_closure_validator as CU
import level1_endpoint_evidence_preregistration_validator as V
import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
PREREG = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"
PROTOCOL = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
GOV = ROOT / "governance/decisions"

D0020 = GOV / "XASSET-0020-replacement-level1-economic-sizing-methodology.md"
D0024 = GOV / "XASSET-0024-level1-endpoint-basis-feasibility-determination.md"
D0027 = GOV / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
D0028 = GOV / "XASSET-0028-concrete-construction-universe-closure-determination.md"
D0030 = GOV / "XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md"
D0031 = GOV / "XASSET-0031-endpoint-0001-stage-1-g3-share-of-the-whole-semantic-determination.md"
D0032 = GOV / "XASSET-0032-endpoint-0001-stage-1-remaining-semantic-gate-determination.md"
D0033 = GOV / "XASSET-0033-endpoint-0001-stage-1-g12-could-admit-tense-determination.md"
D0034 = GOV / "XASSET-0034-endpoint-0001-stage-1-semantic-closure-and-execution-feasibility-determination.md"
D0035 = GOV / "XASSET-0035-endpoint-0001-stage-1-residual-semantic-blocker-determination.md"

FROZEN_UNIVERSE_SHA256 = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
PROTOCOL_SHA256 = "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
PREREG_SHA256 = "6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c"

# AMENDED BY XASSET-0036's SS-G.B steps-2-7 executable package. The two canonical digests below are
# XASSET-0029's, retained as HISTORICAL identity: XASSET-0036 SS-E.1 authorized reconciling the
# XASSET-0035 SS-E/SS-F/SS-G semantics into the canonical artifacts, and SS-E.7 authorized
# recomputing the pins afterwards. Rewriting these constants to the new values would erase what
# this filing actually accepted, so they stay exactly as accepted and the CURRENT-byte check now
# runs against the single effective source, level1_stage1_execution_authorization.CANONICAL_PINS.
XASSET_0029_PROTOCOL_SHA256 = PROTOCOL_SHA256
XASSET_0029_PREREG_SHA256 = PREREG_SHA256

#: The four sleeves. ``XASSET-0020`` §H's six unordered pairs are exactly ``C(4, 2)`` over this set.
SLEEVES = ("equity", "fund_broad_market", "fund_gld_defensive", "crypto")

#: ``XASSET-0020`` §H, in canonical order, as unordered ``frozenset`` objects.
CANONICAL_PAIRS = frozenset(
    {
        frozenset(("equity", "fund_broad_market")),
        frozenset(("equity", "fund_gld_defensive")),
        frozenset(("equity", "crypto")),
        frozenset(("fund_broad_market", "fund_gld_defensive")),
        frozenset(("fund_broad_market", "crypto")),
        frozenset(("fund_gld_defensive", "crypto")),
    }
)

ALL_GATE_IDS = (
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


# ======================================================================================
# Fixtures — committed bytes only
# ======================================================================================


@pytest.fixture(scope="module")
def prereg() -> dict:
    return yaml.safe_load(PREREG.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def protocol_text() -> str:
    return PROTOCOL.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision() -> str:
    return D0035.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def universe() -> dict:
    return CU.frozen_construction_universe()


def _norm(text: str) -> str:
    """Collapse whitespace so a phrase match is insensitive to where prose line-wraps.

    The decisions in this program are hard-wrapped at ~100 columns, so an exact phrase from a
    quoted rule is routinely split across a newline. Operative rules are additionally stated inside
    Markdown blockquotes, whose ``>`` continuation marker lands mid-phrase. Both are stripped so
    every assertion below is a genuine requirement that the phrase be *present*, without making it
    a hostage to the column at which the paragraph happened to break.
    """
    without_quote_markers = re.sub(r"^\s*>\s?", " ", text, flags=re.MULTILINE)
    return re.sub(r"\s+", " ", without_quote_markers)


def _section(text: str, letter: str) -> str:
    """Return one top-level ``### <letter>.`` section body.

    Anchored at line start with exactly three hashes, because a naive ``split("### E.")`` also
    matches inside the ``#### E.1`` sub-headings and would silently return a near-empty fragment
    that makes any ``in`` assertion over it vacuous.
    """
    match = re.search(
        rf"^### {re.escape(letter)}\..*?(?=^### [A-Z]\.|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match is not None, f"section {letter} not found"
    body = match.group(0)
    assert len(body) > 200, f"section {letter} extracted suspiciously short ({len(body)} chars)"
    return body


def _suffix(construction_id: str) -> str:
    return construction_id.split("::")[-1]


def _comparison_group(construction_id: str) -> str:
    """Classify a construction by its own frozen comparison-subject suffix.

    Read from the construction identity only. No driver class, family, route, bound, sleeve
    property, or economic attribute is consulted.
    """
    suffix = _suffix(construction_id)
    if suffix.startswith("PAIR__"):
        return "UNORDERED_PAIR"
    if suffix == "ALT__UNSIZED_UNASSIGNED_CAPITAL":
        return "DIRECT_ALTERNATIVE_UNASSIGNED"
    if suffix.startswith("ALT__"):
        return "DIRECT_ALTERNATIVE_SLEEVE"
    if suffix == "SELF":
        return "SLEEVE_SELF"
    raise AssertionError(f"unclassifiable comparison suffix: {suffix!r}")


def _counterpart(construction_id: str) -> str | None:
    suffix = _suffix(construction_id)
    for prefix in ("PAIR__", "ALT__"):
        if suffix.startswith(prefix):
            return suffix[len(prefix) :]
    return None


def _synthetic_gate_results(**overrides: str) -> dict[str, str]:
    """An isolated synthetic gate-result mapping.

    This is **not** any of the 680 constructions and carries no construction identity. It exists only to
    compose already-decided results through the real derivation function, the method ``XASSET-0030`` §B
    used.
    """
    results = {gate: "PASS" for gate in ALL_GATE_IDS}
    for gate, value in overrides.items():
        assert gate in results, f"unknown gate {gate!r}"
        results[gate] = value
    return results


# ======================================================================================
# Preflight — the frozen inputs this determination is anchored to
# ======================================================================================


class TestFrozenInputsUnchanged:
    def test_canonical_pins_match(self):
        """The current bytes match the current EFFECTIVE pins (XASSET-0036 SS-E.7)."""
        import hashlib

        assert (
            hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
            == A.CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH]
        )
        assert (
            hashlib.sha256(PREREG.read_bytes()).hexdigest()
            == A.CANONICAL_PINS[A.CANONICAL_PREREGISTRATION_RELPATH]
        )

    def test_this_filings_accepted_pins_are_retained_as_history(self):
        """Accepted history is never rewritten to match amended bytes."""
        assert A.XASSET_0029_CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH] == XASSET_0029_PROTOCOL_SHA256
        assert (
            A.XASSET_0029_CANONICAL_PINS[A.CANONICAL_PREREGISTRATION_RELPATH]
            == XASSET_0029_PREREG_SHA256
        )

    def test_universe_cardinality_and_hash(self, universe):
        assert len(universe) == 680
        assert CU.universe_aggregate_sha256() == FROZEN_UNIVERSE_SHA256

    def test_cell_count(self, universe):
        assert len({entry["cell_id"] for entry in universe.values()}) == 48

    def test_every_construction_is_hypothetical(self, universe):
        """B.8 — the shared root of B3."""
        assert {e["source_architecture"] for e in universe.values()} == {
            "HYPOTHETICAL_SOURCE_ARCHITECTURE"
        }

    def test_this_filing_added_no_load_bearing_path(self):
        """AMENDED BY XASSET-0036. This filing left the set at six; SS-G.B step 5 later extended it.

        What this test actually protects is that XASSET-0035 added nothing -- so it now asserts
        the six paths XASSET-0035 saw are all still present, and that any addition beyond them is
        exactly the outcome-producing set SS-G.B step 5 authorizes. It is not weakened into
        accepting an arbitrary set.
        """
        for relative in (
            "level1_stage1_execution_authorization.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "level1_construction_universe_closure_validator.py",
            A.CANONICAL_PROTOCOL_RELPATH,
            A.CANONICAL_PREREGISTRATION_RELPATH,
            "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
        ):
            assert relative in A.LOAD_BEARING_RELPATHS
        additions = set(A.LOAD_BEARING_RELPATHS) - {
            "level1_stage1_execution_authorization.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "level1_construction_universe_closure_validator.py",
            A.CANONICAL_PROTOCOL_RELPATH,
            A.CANONICAL_PREREGISTRATION_RELPATH,
            "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
        }
        assert additions == {
            "level1_stage1_runner.py",
            "level1_stage1_result_validator.py",
            "governance/decisions/XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
        }
        # No REAL results artifact is load-bearing, because none exists.
        assert "stage1_results" not in " ".join(A.LOAD_BEARING_RELPATHS).lower()


class TestStageOneRemainsUnarmed:
    def test_new_execution_is_not_authorized(self):
        authorized, _reason = A.new_execution_is_authorized()
        assert authorized is False

    def test_authorization_root_absent(self):
        assert not A.AUTHORIZATION_ROOT.exists()
        for path in (A.AUTHORIZATION_PATH, A.CLAIM_PATH, A.COMPLETION_PATH, A.LEDGER_PATH):
            assert not path.exists()

    def test_stage_1_executability_is_false(self, prereg):
        assert prereg["stage_1_executability"]["executable"] is False

    def test_no_execution_artifact_exists(self):
        assert not (ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()
        assert not list(ROOT.glob("**/stage1_results.yaml"))


# ======================================================================================
# Canonical facts the determination is built on (§B)
# ======================================================================================


class TestCanonicalFactsReproduce:
    def test_gate_result_vocabulary_is_closed_to_four(self, prereg):
        """B.1 — and therefore B3's elimination frame is finite."""
        assert prereg["result_vocabulary"]["gate_result_vocabulary"] == [
            "PASS",
            "FAIL",
            "UNABLE_TO_DETERMINE",
            "NOT_APPLICABLE",
        ]

    def test_no_reserved_or_deferred_gate_result_value_exists(self, prereg):
        vocab = set(prereg["result_vocabulary"]["gate_result_vocabulary"])
        for invented in ("SOURCE_DEPENDENT", "RESERVED", "DEFERRED", "NOT_YET_EVALUABLE"):
            assert invented not in vocab

    def test_prerequisite_set_is_exactly_g9_and_g12(self, prereg):
        """B.2 — the structural reason B3's prerequisite limb is unavailable to G3 and G5."""
        prerequisite = {
            g["gate_id"]
            for g in prereg["gate_sequence"]["gates"]
            if g["failure_disposition"] == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"
        }
        assert prerequisite == {"G9_REPRESENTATION", "G12_SNAPSHOT_ADMISSIBILITY_PATH"}
        assert set(V.PREREQUISITE_GATES) == prerequisite

    @pytest.mark.parametrize(
        "gate_id", ["G3_NORMALIZATION", "G5_CONSTRAINT_SHAPE", "G10_PAIR_INDEPENDENCE"]
    )
    def test_g3_g5_g10_are_categorical_class(self, prereg, gate_id):
        gate = next(g for g in prereg["gate_sequence"]["gates"] if g["gate_id"] == gate_id)
        assert gate["failure_disposition"] == "BLOCKED_CATEGORICALLY"

    def test_class_definitions_turn_on_closeability(self, prereg):
        """B.3 — the hinge for B3, and the reason a FAIL on G3 asserts non-closeability."""
        assert (
            prereg["categorical_definition"]["means"]
            == "NOT_CLOSEABLE_BY_A_NAMED_PREREQUISITE_UNDER_THE_CURRENTLY_ACCEPTED_METHODOLOGY"
        )
        assert (
            prereg["prerequisite_definition"]["means"]
            == "CLOSEABLE_BY_A_NAMED_SEPARATELY_AUTHORIZED_PREREQUISITE_WITHOUT_METHODOLOGY_AMENDMENT"
        )
        assert prereg["prerequisite_definition"]["requires_named_dependency"] is True

    def test_nine_of_twelve_gate_questions_are_counterfactual(self, prereg):
        """B.4 — §E.3's principal ground. The register is in the gate questions themselves."""
        would = [
            g["gate_id"]
            for g in prereg["gate_sequence"]["gates"]
            if g["question"].strip().startswith("Would")
        ]
        assert len(would) == 9
        assert set(would) == {
            "G2_MAGNITUDE_INTRINSICALITY",
            "G3_NORMALIZATION",
            "G5_CONSTRAINT_SHAPE",
            "G6_ROUTE_COMPLIANCE",
            "G7_DISCRETION_AND_PROVENANCE",
            "G8_UNIQUENESS",
            "G9_REPRESENTATION",
            "G10_PAIR_INDEPENDENCE",
            "G11_EXACTNESS_AND_DETERMINISM",
        }

    def test_g12_is_one_of_the_three_not_phrased_would(self, prereg):
        """The honest counterweight: G12's own surface grammar differs, which is why §E constitutes."""
        gate = next(
            g
            for g in prereg["gate_sequence"]["gates"]
            if g["gate_id"] == "G12_SNAPSHOT_ADMISSIBILITY_PATH"
        )
        assert not gate["question"].strip().startswith("Would")
        assert "could admit the candidate" in gate["question"]

    def test_gate_level_abstention_conditions_are_counterfactual(self, prereg):
        """B.5 — including §H.4's own condition, which B2 relies on."""
        names = {c["condition"] for c in prereg["mandatory_abstention_conditions"]}
        assert "AN_UNRESOLVED_PAIR_WOULD_BE_CONSUMED_AS_AN_INPUT" in names
        assert "A_CANDIDATE_WOULD_REQUIRE_INVENTING_A_LEVEL_1_AGGREGATION_OR_REPRESENTATION_RULE" in names
        assert "ANY_STEP_COULD_HAVE_BEEN_CHOSEN_DIFFERENTLY" in names
        authority = {
            c["condition"]: c["authority"] for c in prereg["mandatory_abstention_conditions"]
        }
        assert authority["AN_UNRESOLVED_PAIR_WOULD_BE_CONSUMED_AS_AN_INPUT"] == (
            "XASSET-0024_SECTION_H_4"
        )

    def test_every_applicable_gate_must_be_recorded(self, prereg):
        """B.9 — why disposition-inertness is never a licence to skip a gate result."""
        gs = prereg["gate_sequence"]
        assert gs["evaluation_requirement"] == "EVALUATE_EVERY_APPLICABLE_GATE_BEFORE_CLASSIFYING"
        assert gs["record_first_failing_gate_only"] is False

    def test_reinterpretation_is_barred_only_after_an_outcome_is_observed(self, prereg):
        """B.10 — affirmative authority that now is the lawful window for §E's constitutive act."""
        gs = prereg["gate_sequence"]
        assert (
            gs["gates_may_not_be_added_removed_reordered_or_reinterpreted_after_any_outcome_observed"]
            is True
        )
        assert prereg["execution"]["rerun_rule"]["after_outcomes_observed"] == "PROHIBITED"


# ======================================================================================
# Batchability (§C)
# ======================================================================================


class TestBatchabilityIsDetermined:
    def test_all_five_questions_are_answered(self, decision):
        section = decision.split("### C.")[1].split("### D.")[0]
        for marker in ("1. **", "2. **", "3. **", "4. **", "5. **"):
            assert marker in section

    def test_choice_is_recorded_explicitly(self, decision):
        assert "ALL-THREE COHERENT UNIT" in decision

    def test_cross_gate_policy_risk_is_disclosed_not_waved_through(self, decision):
        section = decision.split("### C.")[1].split("### D.")[0]
        assert "Only if B3 were stated broadly" in section
        assert "disjoint gate set" in section

    def test_blockers_address_disjoint_gate_sets(self, decision):
        section = decision.split("### C.")[1].split("### D.")[0]
        assert "`{G12}`" in section and "`{G10}`" in section and "`{G3, G5, G9}`" in section

    def test_no_determination_is_used_as_a_premise_for_another(self, decision):
        assert "no determination below is used as a premise for any other" in _norm(decision).lower()


class TestRouteLabellingIsExplicit:
    """The constitutive/interpretive distinction must be stated, not left to inference."""

    def test_both_routes_are_defined(self, decision):
        section = decision.split("### D.")[1].split("### E.")[0]
        assert "INTERPRETIVE closure" in section
        assert "CONSTITUTIVE closure" in section

    def test_b1_is_labelled_constitutive_in_the_determination_table(self, decision):
        table = decision.split("### A.")[1].split("### B.")[0]
        assert "**CONSTITUTIVE**" in table

    def test_b2_and_b3_are_labelled_interpretive(self, decision):
        table = decision.split("### A.")[1].split("### B.")[0]
        assert table.count("**INTERPRETIVE**") == 2

    def test_b1_section_restates_its_constitutive_character(self, decision):
        section = _norm(_section(decision, "E"))
        assert "constitutive governed statement, not a reading" in section

    def test_executor_may_apply_but_never_choose_the_rule(self, decision):
        assert "apply an already-fixed rule" in decision
        assert "never **choose what the rule is**" in decision


# ======================================================================================
# B1 — G12 modal register (§E)
# ======================================================================================


class TestB1ModalRegister:
    def test_the_statement_selects_lawful_satisfiability(self, decision):
        section = _norm(_section(decision, "E"))
        assert "lawful satisfiability of the frozen construction specification" in section
        assert "not against execution-time world state" in section

    def test_present_tense_world_state_reading_is_named_and_rejected(self, decision):
        """The rejected interpretation must be stated, not silently omitted."""
        assert "world-state" in decision
        assert "Adopt the present-tense / world-state register for `G12`.** Rejected" in decision

    def test_rejected_reading_becomes_unlawful_prospectively(self, decision):
        section = _norm(decision.split("#### E.4")[1].split("#### E.5")[0])
        assert "Before this statement, the world-state reading was lawful" in section
        assert "contradicts an accepted governed `G12`-scoped rule" in section

    def test_direction_is_not_justified_by_fewer_blocked_constructions(self, decision):
        section = decision.split("#### E.3")[1].split("#### E.4")[0]
        assert "not** because it blocks fewer" in section

    def test_authority_for_the_constitutive_act_is_cited(self, decision):
        section = _norm(decision.split("#### E.1")[1].split("#### E.2")[0])
        assert "§G.A" in section
        assert "a governed definition" in section
        assert "§I" in section

    def test_g12_remains_identifiability_only(self, decision, prereg):
        section = decision.split("#### E.5")[1].split("### F.")[0]
        assert "Identifiability only" in section
        assert "§J.1" in section
        items = {i["j_item"]: i["gate_or_basis"] for i in prereg["stage_1_testable_subset"]["items"]}
        assert items["J_2_SNAPSHOT_POSITION"] == "G12_IDENTIFIABILITY_ONLY_NO_SUCCESSOR_CREATED"

    def test_g12_clause_remains_operative_not_dissolved(self, decision):
        section = decision.split("#### E.5")[1].split("### F.")[0]
        assert "clause stays operative" in section

    def test_nonexistence_floor_is_preserved(self, decision):
        section = decision.split("#### E.5")[1].split("### F.")[0]
        assert "never by itself a `FAIL` ground" in section

    def test_scope_is_g12_only_not_program_wide(self, decision):
        section = decision.split("#### E.5")[1].split("### F.")[0]
        assert "**`G12` only.**" in section
        assert "not** a program-wide gate-modal register rule" in section

    def test_no_snapshot_successor_is_created(self, decision):
        assert "creates no snapshot successor" in _norm(decision).lower()

    def test_no_g12_gate_result_is_asserted(self, decision):
        section = _norm(decision.split("#### E.5")[1].split("### F.")[0])
        assert "No gate result is asserted" in section
        assert (
            "records no `PASS`, `FAIL`, or `UNABLE_TO_DETERMINE` for `G12` for any construction"
            in section
        )

    def test_g12_disposition_inertness_is_disclosed_not_relied_on(self, decision):
        section = decision.split("#### E.5")[1].split("### F.")[0]
        assert "Disposition-inert today, and that is not a licence" in section

    def test_both_g12_readings_are_disposition_inert_today(self):
        """Verified through the real derivation on synthetic inputs — not on any construction."""
        base = _synthetic_gate_results(G2_MAGNITUDE_INTRINSICALITY="UNABLE_TO_DETERMINE")
        as_pass = dict(base, G12_SNAPSHOT_ADMISSIBILITY_PATH="PASS")
        as_fail = dict(base, G12_SNAPSHOT_ADMISSIBILITY_PATH="FAIL")
        assert V.derive_candidate_disposition(as_pass) == "UNABLE_TO_DETERMINE"
        assert V.derive_candidate_disposition(as_fail) == "UNABLE_TO_DETERMINE"

    def test_interpretive_closure_of_b1_was_considered_and_refused(self, decision):
        """The suite must fail if the constitutive act is dressed up as a reading."""
        normalised = _norm(decision)
        assert "Close B1 interpretively on the strength of B.4" in normalised
        assert "Rejected, and this was the closest call" in normalised


# ======================================================================================
# B2 — G10 §H.4 consumption semantics (§F)
# ======================================================================================


class TestB2ConsumptionRule:
    def test_rule_is_stated_on_frozen_comparison_identity(self, decision):
        section = _norm(decision.split("#### F.1")[1].split("#### F.2")[0])
        assert (
            "if and only if both of its own two frozen named comparison endpoints are members of "
            "the four-sleeve set" in section
        )
        assert "never by the presence or absence of the `unordered_pair_id` label" in section

    def test_all_four_terms_are_given_accepted_meanings(self, decision):
        section = decision.split("#### F.2")[1].split("#### F.3")[0]
        for term in ("**Pair.**", "**`UNORDERED_PAIR`.**", "**`DIRECT_ALTERNATIVE`.**"):
            assert term in section
        assert "Consumption / use / reference" in section
        assert "Unresolved-pair protection" in section

    def test_no_seventh_record_authority_is_cited(self, decision):
        """The selector XASSET-0032 §G.4 did not have."""
        assert "does not create a seventh record" in decision

    def test_h4_counterfactual_test_is_quoted(self, decision):
        section = _norm(decision.split("#### F.2")[1].split("#### F.3")[0])
        assert "is not an input to it at all" in section
        assert "would move under some direction of that pair" in section
        assert "Direction-invariance by independence is the test" in section

    def test_section_i_independence_clause_is_cited(self, decision):
        normalised = _norm(decision)
        assert "independently and directly governed" in normalised
        assert "not a derived relationship" in normalised


class TestB2AuthorityReproducesFromCommittedBytes:
    def test_xasset_0020_h_contains_the_no_seventh_record_rule(self):
        text = _norm(D0020.read_text(encoding="utf-8"))
        assert "it does not create a seventh record" in text

    def test_xasset_0020_h_requires_direction_per_applicable_driver(self):
        text = _norm(D0020.read_text(encoding="utf-8"))
        assert "all six driver categories considered" in text
        assert "direction per applicable driver" in text

    def test_xasset_0020_h_declares_exactly_six_pairs(self):
        text = _norm(D0020.read_text(encoding="utf-8"))
        assert "Exactly six unordered pair records exist" in text

    def test_xasset_0020_i_bars_transitivity(self):
        text = _norm(D0020.read_text(encoding="utf-8"))
        assert "may not be filled by transitivity through equity or another sleeve" in text

    def test_xasset_0024_h4_is_substance_based(self):
        text = _norm(D0024.read_text(encoding="utf-8")).lower()
        assert "is not an input to it at all" in text
        assert "direction-robustness by inspection is not" in text

    def test_unsized_unassigned_capital_is_a_separate_comparison_family(self):
        text = _norm(D0020.read_text(encoding="utf-8"))
        assert "UNSIZED_UNASSIGNED_CAPITAL" in text
        assert "sleeve_preferred" in text and "unassigned_preserved" in text


class TestB2MechanicalEffect:
    """The 360-construction inventory, proved from construction identity alone."""

    def test_comparison_group_decomposition(self, universe):
        counts: dict[str, int] = {}
        for construction_id in universe:
            group = _comparison_group(construction_id)
            counts[group] = counts.get(group, 0) + 1
        assert counts == {
            "UNORDERED_PAIR": 120,
            "DIRECT_ALTERNATIVE_SLEEVE": 360,
            "DIRECT_ALTERNATIVE_UNASSIGNED": 120,
            "SLEEVE_SELF": 80,
        }
        assert sum(counts.values()) == 680

    def test_every_direct_alternative_sleeve_maps_to_a_canonical_pair(self, universe):
        mapped = 0
        for construction_id, entry in universe.items():
            if _comparison_group(construction_id) != "DIRECT_ALTERNATIVE_SLEEVE":
                continue
            counterpart = _counterpart(construction_id)
            assert counterpart in SLEEVES
            assert entry["sleeve"] in SLEEVES
            assert frozenset((entry["sleeve"], counterpart)) in CANONICAL_PAIRS
            mapped += 1
        assert mapped == 360

    def test_no_degenerate_self_equals_counterpart_construction(self, universe):
        for construction_id, entry in universe.items():
            counterpart = _counterpart(construction_id)
            if counterpart in SLEEVES:
                assert entry["sleeve"] != counterpart

    def test_distribution_is_exactly_sixty_per_canonical_pair(self, universe):
        per_pair: dict[frozenset, int] = {}
        for construction_id, entry in universe.items():
            if _comparison_group(construction_id) != "DIRECT_ALTERNATIVE_SLEEVE":
                continue
            key = frozenset((entry["sleeve"], _counterpart(construction_id)))
            per_pair[key] = per_pair.get(key, 0) + 1
        assert set(per_pair) == CANONICAL_PAIRS
        assert set(per_pair.values()) == {60}

    def test_unordered_pair_group_is_twenty_per_canonical_pair(self, universe):
        per_pair: dict[frozenset, int] = {}
        for construction_id, entry in universe.items():
            if _comparison_group(construction_id) != "UNORDERED_PAIR":
                continue
            key = frozenset((entry["sleeve"], _counterpart(construction_id)))
            per_pair[key] = per_pair.get(key, 0) + 1
        assert set(per_pair) == CANONICAL_PAIRS
        assert set(per_pair.values()) == {20}

    def test_consuming_population_is_480_and_non_consuming_is_200(self, universe):
        consuming = sum(
            1
            for cid in universe
            if _comparison_group(cid) in {"UNORDERED_PAIR", "DIRECT_ALTERNATIVE_SLEEVE"}
        )
        non_consuming = sum(
            1
            for cid in universe
            if _comparison_group(cid) in {"DIRECT_ALTERNATIVE_UNASSIGNED", "SLEEVE_SELF"}
        )
        assert consuming == 480
        assert non_consuming == 200
        assert consuming + non_consuming == 680

    def test_unassigned_counterpart_is_not_a_sleeve(self, universe):
        for construction_id in universe:
            if _comparison_group(construction_id) != "DIRECT_ALTERNATIVE_UNASSIGNED":
                continue
            assert _counterpart(construction_id) == "UNSIZED_UNASSIGNED_CAPITAL"
            assert _counterpart(construction_id) not in SLEEVES

    def test_sleeve_self_has_no_comparison_counterpart(self, universe):
        for construction_id in universe:
            if _comparison_group(construction_id) != "SLEEVE_SELF":
                continue
            assert _counterpart(construction_id) is None

    def test_the_360_carry_three_of_the_six_driver_classes(self, universe):
        drivers = {
            entry["driver_class"]
            for cid, entry in universe.items()
            if _comparison_group(cid) == "DIRECT_ALTERNATIVE_SLEEVE"
        }
        assert drivers == {"valuation_opportunity_cost", "downside_path_risk", "recovery"}

    def test_no_economic_property_is_consulted_by_the_rule(self, universe):
        """Consumption is a function of identity fields only, never of any economic attribute."""
        sample = next(iter(universe))
        entry = universe[sample]
        for forbidden in ("value", "weight", "target", "percentage", "endpoint", "bound_value"):
            assert forbidden not in entry


class TestB2ForeclosesTheLabelReading:
    def test_specification_silence_reasoning_is_cited(self, decision):
        section = decision.split("#### F.4")[1].split("#### F.5")[0]
        assert "silence" in section.lower()
        assert "Standard 1" in section

    def test_xasset_0032_g5_reasoning_reproduces_from_committed_bytes(self):
        text = _norm(D0032.read_text(encoding="utf-8"))
        assert (
            "A specification's silence about pair consumption is not proof that an eventual "
            "source consumes no pair" in text
        )

    def test_the_asymmetry_argument_is_stated(self, decision):
        section = decision.split("#### F.4")[1].split("#### F.5")[0]
        assert "cannot bar that inference for 200 constructions and permit it for 360" in section


class TestB2DoesNotRelabelOrMutateIdentity:
    def test_the_four_abuse_guards_are_all_stated(self, decision):
        section = decision.split("#### F.6")[1].split("#### F.7")[0]
        assert "No hidden pair inference" in section
        assert "No transitive consumption" in section
        assert "No relabelling" in section
        assert "No ignoring genuine consumption" in section

    def test_consumption_is_expressly_not_identity(self, decision):
        assert "Consumption is not identity" in _norm(decision)

    def test_the_360_remain_direct_alternative_with_no_pair_id(self, universe):
        for construction_id in universe:
            if _comparison_group(construction_id) != "DIRECT_ALTERNATIVE_SLEEVE":
                continue
            assert not _suffix(construction_id).startswith("PAIR__")

    def test_universe_identity_is_untouched_by_this_filing(self, universe):
        assert len(universe) == 680
        assert CU.universe_aggregate_sha256() == FROZEN_UNIVERSE_SHA256

    def test_no_seventh_pair_is_created(self, universe):
        observed: set[frozenset] = set()
        for construction_id, entry in universe.items():
            counterpart = _counterpart(construction_id)
            if counterpart in SLEEVES:
                observed.add(frozenset((entry["sleeve"], counterpart)))
        assert observed == CANONICAL_PAIRS
        assert len(observed) == 6


class TestB2DoesNotDetermineTheGateResult:
    def test_evaluation_time_pair_status_is_expressly_left_open(self, decision):
        section = _norm(decision.split("#### F.7")[1].split("#### F.8")[0])
        assert "does not determine `G10`'s result" in section
        assert "unresolved at evaluation time" in section
        assert "under this snapshot" in section

    def test_the_200_are_not_recorded_pass(self, decision):
        section = decision.split("#### F.7")[1].split("#### F.8")[0]
        assert "not** recorded `G10` `PASS`" in section

    def test_categorical_consequence_is_conditional_and_verified(self, decision):
        section = decision.split("#### F.8")[1].split("### G.")[0]
        assert "if the consumed pair is unresolved at evaluation time" in section

    def test_categorical_domination_reproduces_on_synthetic_inputs(self):
        results = _synthetic_gate_results(
            G2_MAGNITUDE_INTRINSICALITY="UNABLE_TO_DETERMINE",
            G10_PAIR_INDEPENDENCE="FAIL",
        )
        assert V.derive_candidate_disposition(results) == "BLOCKED_CATEGORICALLY"

    def test_enforcement_defect_is_recorded_not_corrected(self, decision):
        section = decision.split("#### F.8")[1].split("### G.")[0]
        assert "does not correct it" in section
        assert "neither re-derived, expanded, narrowed, nor corrected" in section

    def test_the_enforcement_defect_was_not_fixed_by_this_filing(self):
        """AMENDED BY XASSET-0036 SS-E.2, which authorized SS-G.B step 3's correction.

        XASSET-0035 SS-F.8 raised the stakes on the XASSET-0030 SS-C defect and expressly did NOT
        correct it, recording that the correction "belongs to SS-G.B step 3". That correction has
        since landed. What this test protects is the SUBSTANCE the defect branch guarded -- that
        reading dependence alone never yields a categorical disposition -- which is preserved
        exactly, alongside the canonically permitted outcome the defect wrongly blocked.
        """
        source = (ROOT / "level1_endpoint_evidence_preregistration_validator.py").read_text(
            encoding="utf-8"
        )
        assert "a reading-dependent G2 outcome may not be recorded as " in source
        assert "independently fails" in source

        gates = {gate: "PASS" for gate in V.GATE_IDS}
        gates["G2_MAGNITUDE_INTRINSICALITY"] = "UNABLE_TO_DETERMINE"
        # Reading dependence alone is still uncertainty, never a categorical bar.
        assert V.derive_candidate_disposition(dict(gates)) == "UNABLE_TO_DETERMINE"
        # An independent categorical failure now lawfully derives BLOCKED_CATEGORICALLY, which is
        # exactly what XASSET-0027 SS-M.1 and both canonical artifacts always permitted.
        gates["G10_PAIR_INDEPENDENCE"] = "FAIL"
        assert V.derive_candidate_disposition(gates) == "BLOCKED_CATEGORICALLY"


# ======================================================================================
# B3 — reserved-gate recording posture (§G)
# ======================================================================================


class TestB3RecordingPosture:
    def test_rule_selects_unable_to_determine(self, decision):
        section = decision.split("#### G.1")[1].split("#### G.2")[0]
        assert "records `UNABLE_TO_DETERMINE`" in section

    def test_rule_is_scoped_to_exactly_three_items(self, decision):
        section = decision.split("#### G.1")[1].split("#### G.2")[0]
        assert "`G3`" in section and "`G5`" in section and "`G9` path 1" in section
        assert "applies to no other gate" in section

    def test_per_gate_routes_are_stated_separately(self, decision):
        section = decision.split("#### G.2")[1].split("#### G.3")[0]
        assert "**`G3` (categorical class).**" in section
        assert "**`G5` (categorical class).**" in section
        assert "**`G9` path 1, undetermined (prerequisite class).**" in section

    def test_shared_outcome_but_per_gate_route_is_disclosed(self, decision):
        section = decision.split("#### G.1")[1].split("#### G.2")[0]
        assert "route** differs per gate" in section


class TestStandardsPreservedBothDirections:
    def test_standard_1_bars_by_construction_pass(self, decision):
        assert "Standard 1" in decision
        section = decision.split("#### G.2")[1].split("#### G.3")[0]
        assert "never by itself proof that P is lawfully satisfiable" in section

    def test_standard_2_bars_nonexistence_fail(self, decision):
        section = decision.split("#### G.2")[1].split("#### G.3")[0]
        assert "inferred from nonexistence alone" in section

    def test_neither_standard_is_weakened(self, decision):
        section = decision.split("#### G.3")[1].split("#### G.4")[0]
        assert "Neither Standard is weakened" in section

    def test_standards_reproduce_from_xasset_0030(self):
        text = D0030.read_text(encoding="utf-8")
        assert "is never by itself" in text
        assert "never inferred from nonexistence alone" in text

    def test_standards_bind_executors_per_xasset_0034(self):
        text = D0034.read_text(encoding="utf-8")
        assert "bind any executor" in text


class TestB3DoesNotProduceAPassOrANegativeJudgment:
    def test_hypothetical_absence_does_not_pass(self, decision):
        section = decision.split("#### G.3")[1].split("#### G.4")[0]
        assert "Not a pass by specification-satisfaction" in section

    def test_hypothetical_absence_does_not_categorical_fail(self, decision):
        section = decision.split("#### G.3")[1].split("#### G.4")[0]
        assert "Not a negative portfolio judgment" in section
        assert "neither `FAIL` nor" in section

    def test_unable_to_determine_is_not_a_negative_disposition(self):
        results = _synthetic_gate_results(
            G3_NORMALIZATION="UNABLE_TO_DETERMINE",
            G5_CONSTRAINT_SHAPE="UNABLE_TO_DETERMINE",
            G9_REPRESENTATION="UNABLE_TO_DETERMINE",
        )
        assert V.derive_candidate_disposition(results) == "UNABLE_TO_DETERMINE"

    def test_a_fail_on_g3_would_have_been_categorical(self):
        """The value B3 refuses, shown to be materially different from the one it selects."""
        results = _synthetic_gate_results(G3_NORMALIZATION="FAIL")
        assert V.derive_candidate_disposition(results) == "BLOCKED_CATEGORICALLY"

    def test_b3_posture_is_disposition_inert_today(self):
        with_g2_only = _synthetic_gate_results(G2_MAGNITUDE_INTRINSICALITY="UNABLE_TO_DETERMINE")
        with_b3 = _synthetic_gate_results(
            G2_MAGNITUDE_INTRINSICALITY="UNABLE_TO_DETERMINE",
            G3_NORMALIZATION="UNABLE_TO_DETERMINE",
            G5_CONSTRAINT_SHAPE="UNABLE_TO_DETERMINE",
            G9_REPRESENTATION="UNABLE_TO_DETERMINE",
        )
        assert V.derive_candidate_disposition(with_g2_only) == V.derive_candidate_disposition(with_b3)

    def test_disposition_inertness_is_not_treated_as_a_licence(self, decision):
        section = decision.split("#### G.5")[1].split("### H.")[0]
        assert "not a licence" in section
        assert "§H.5" in section


class TestB3PreservesClassesAndAbstention:
    def test_g9_determined_path_1_failure_stays_prerequisite(self, decision):
        section = decision.split("#### G.3")[1].split("#### G.4")[0]
        assert "remains prerequisite-blocked" in section
        assert "applies only to the undetermined case" in section

    def test_canonical_non_self_contained_handling_is_unchanged(self, prereg):
        rep = prereg["representation"]
        assert (
            rep["non_self_contained_handling"]
            == "NAME_THE_EXACT_DEPENDENCY_AND_BLOCK_PENDING_SEPARATE_PREREQUISITE"
        )
        assert rep["rule_created_by_this_program"] is False
        assert rep["cm_14_through_cm_17_membership_designated"] is False

    def test_no_categorical_gate_becomes_a_prerequisite_gate(self, decision):
        section = decision.split("#### G.3")[1].split("#### G.4")[0]
        assert "No gate changes class" in section

    def test_gate_classes_are_byte_identical_to_canonical(self, prereg):
        observed = {
            g["gate_id"]: g["failure_disposition"] for g in prereg["gate_sequence"]["gates"]
        }
        assert observed["G3_NORMALIZATION"] == "BLOCKED_CATEGORICALLY"
        assert observed["G5_CONSTRAINT_SHAPE"] == "BLOCKED_CATEGORICALLY"
        assert observed["G9_REPRESENTATION"] == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"
        assert observed["G12_SNAPSHOT_ADMISSIBILITY_PATH"] == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"

    def test_abstention_remains_a_complete_outcome(self, prereg, decision):
        assert prereg["abstention_is_a_complete_outcome"] is True
        assert len(prereg["mandatory_abstention_conditions"]) == 8
        section = decision.split("#### G.3")[1].split("#### G.4")[0]
        assert "Abstention remains a complete outcome" in section

    def test_reservations_are_cited_not_lifted(self, decision):
        section = _norm(decision.split("#### G.2")[1].split("#### G.3")[0])
        assert "§M.3" in section and "§M.4" in section
        assert "it does not determine that no bridge exists" in section
        assert "No prejudgment is recorded here" in section

    def test_reservations_reproduce_from_xasset_0027(self):
        text = D0027.read_text(encoding="utf-8")
        assert "it does not determine that no bridge exists" in text
        assert "No prejudgment is recorded here" in text


class TestB3ScopeFence:
    """The single largest batching risk in this filing, pinned."""

    def test_scope_limit_section_exists(self, decision):
        assert "#### G.4 — Scope limit" in decision

    @pytest.mark.parametrize("gate", ["`G8`", "`G10`", "`G12`"])
    def test_each_excluded_gate_is_named_as_not_reached(self, decision, gate):
        section = _norm(decision.split("#### G.4")[1].split("#### G.5")[0])
        assert gate in section
        assert "Not reached" in section

    def test_b3_does_not_soften_the_g10_categorical_consequence(self, decision):
        section = decision.split("#### G.4")[1].split("#### G.5")[0]
        assert "does not give `G10` an `UNABLE_TO_DETERMINE` posture" in section

    def test_g2_reading_map_is_not_generalized(self, decision):
        section = decision.split("#### G.4")[1].split("#### G.5")[0]
        assert "`G2` is untouched" in section
        assert "not** generalized" in section

    def test_open_reading_handling_stays_unrelied_on(self, prereg):
        orh = prereg["open_reading_handling"]
        assert orh["resolved_by_this_program"] is False
        assert orh["relied_upon_by_this_program"] is False

    def test_g2_reading_map_still_yields_unable_to_determine(self):
        assert V.required_g2_gate_result("PASSES", "FAILS") == "UNABLE_TO_DETERMINE"
        assert V.is_reading_dependent("PASSES", "FAILS") is True


# ======================================================================================
# Preservation and non-authorization (§H, §K)
# ======================================================================================


class TestSixSixPartitionPreserved:
    def test_no_e1_invalidation_trigger_fires(self, decision):
        section = _norm(decision.split("#### H.1")[1].split("#### H.2")[0])
        assert "6/6 map is unchanged" in section
        assert section.count("**No**") >= 3

    def test_each_closable_gate_is_checked_by_name(self, decision):
        section = decision.split("#### H.1")[1].split("#### H.2")[0]
        for gate in ("`G1`", "`G2`", "`G4`", "`G6`", "`G7`", "`G11`"):
            assert gate in section

    def test_canonical_j2_mapping_untouched(self, prereg):
        items = {i["j_item"]: i["gate_or_basis"] for i in prereg["stage_1_testable_subset"]["items"]}
        assert items["J_1_ADMISSION"] == "G12_PLUS_SOURCE_CURRENTNESS_RULE"
        assert items["J_2_SNAPSHOT_POSITION"] == "G12_IDENTIFIABILITY_ONLY_NO_SUCCESSOR_CREATED"


class TestSatisfactionResiduesPreserved:
    def test_all_five_residues_are_recorded_as_unclosed(self, decision):
        section = decision.split("#### H.2")[1].split("#### H.3")[0]
        assert "None is closed, narrowed, or converted" in section
        for token in ("`G3`", "`G5`", "`G9` path 1", "`G8`", "`G10` blocker 1"):
            assert token in section

    def test_recording_posture_is_distinguished_from_satisfaction(self, decision):
        section = decision.split("#### H.2")[1].split("#### H.3")[0]
        assert "does not answer what any source exhibits" in section
        assert "does not answer whether any pair is unresolved at evaluation time" in section

    def test_g3_satisfaction_is_not_closed(self, decision):
        assert "closes no gate on satisfaction" in _norm(decision).lower()

    def test_xasset_0031_g3_is_not_used_as_a_premise(self, decision):
        normalised = _norm(decision)
        assert "neither reopened nor used as a premise" in normalised
        assert "unused as a premise" in normalised


class TestOpenQuestionsStayOpen:
    def test_k1_remains_unresolved(self, decision, prereg):
        assert "§K.1 stays unresolved" in _norm(decision)
        assert prereg["open_reading_handling"]["resolved_by_this_program"] is False

    def test_e1_remains_unamended(self, decision):
        assert "`XASSET-0020` §E.1 stays unamended" in _norm(decision)

    def test_xasset_0020_e1_scope_is_not_amended(self, decision):
        assert "leaves `XASSET-0020` §E.1 unamended" in decision


class TestCorrectionsRecordedForwardOnly:
    def test_three_corrections_are_tabulated(self, decision):
        section = decision.split("#### H.3")[1].split("#### H.4")[0]
        for marker in ("H.3.1", "H.3.2", "H.3.3"):
            assert marker in section

    def test_no_prior_decision_text_is_edited(self, decision):
        section = decision.split("#### H.3")[1].split("#### H.4")[0]
        assert "No prior decision's text is edited" in section

    def test_xasset_0033_verdict_is_not_recorded_as_wrong(self, decision):
        section = decision.split("#### H.3")[1].split("#### H.4")[0]
        assert "stands as correct on `XASSET-0033`'s own bar" in section

    def test_prior_decisions_are_unmodified_on_disk(self):
        """The three corrected filings must remain byte-identical to their accepted state."""
        for path in (D0032, D0033, D0034):
            text = path.read_text(encoding="utf-8")
            assert "XASSET-0035" not in text


class TestGBUnlockIsTiedToLifecycleClosure:
    """Correction 1 / FULL review `4951655331` MINOR 1.

    The operative unlock rule must enumerate **complete** lifecycle closure, including successful
    merge-commit CI bound to the exact merge SHA. Every test below is written so that deleting or
    weakening the merge-commit-CI condition fails the suite.
    """

    def test_unlock_is_not_claimed_on_merge(self, decision):
        section = _norm(_section(decision, "I"))
        assert "not unlocked by this PR being opened, nor by any single lifecycle step in isolation" in section

    def test_all_seven_conditions_are_enumerated(self, decision):
        section = _norm(_section(decision, "I"))
        for step in (
            "Independent exact-head review",
            "any required bounded correction and exact-head re-review",
            "explicit principal exact-head acceptance",
            "normal merge",
            "immediate post-merge verification",
            "successful merge-commit CI whose `head_sha` is the exact merge SHA",
            "final post-CI verification and lifecycle closure",
        ):
            assert step in section, f"missing lifecycle condition: {step!r}"

    def test_conditions_are_numbered_one_through_seven(self, decision):
        section = _section(decision, "I")
        for n in range(1, 8):
            assert re.search(rf"^{n}\. \*\*", section, flags=re.MULTILINE), f"missing numbered item {n}"

    # ---- the four "alone is not enough" properties, each pinned separately ----

    def test_exact_head_review_alone_does_not_unlock(self, decision):
        section = _norm(_section(decision, "I"))
        assert "None of these is individually sufficient" in section
        assert "Independent exact-head review" in section

    def test_principal_acceptance_alone_does_not_unlock(self, decision):
        section = _norm(_section(decision, "I"))
        assert "principal acceptance does not" in section

    def test_merge_alone_does_not_unlock(self, decision):
        section = _norm(_section(decision, "I"))
        assert "merge does not" in section

    def test_post_merge_verification_without_merge_commit_ci_does_not_unlock(self, decision):
        section = _norm(_section(decision, "I"))
        assert (
            "post-merge verification without a successful exact merge-commit CI run does not" in section
        )

    def test_pr_head_ci_is_not_a_substitute_for_merge_commit_ci(self, decision):
        section = _norm(_section(decision, "I"))
        assert "not the PR head's own CI run" in section
        assert "a green PR-head CI run" in section

    def test_merge_commit_ci_must_bind_the_exact_merge_sha(self, decision):
        section = _norm(_section(decision, "I"))
        assert "`head_sha` is the exact merge SHA" in section
        assert "not a run against any other commit" in section

    def test_final_lifecycle_closure_is_required(self, decision):
        section = _norm(_section(decision, "I"))
        assert "final post-CI verification and lifecycle closure" in section
        assert "merged-successor identity verification" in section

    def test_only_complete_closure_unlocks(self, decision):
        section = _norm(_section(decision, "I"))
        assert "Only complete closure of all seven does" in section

    # ---- grounded in the repository's own definition, which must stay unmodified ----

    def test_rule_is_grounded_in_required_lifecycle_gates(self, decision):
        section = _norm(_section(decision, "I"))
        assert "REQUIRED_LIFECYCLE_GATES" in section
        assert "not a new requirement invented here" in section

    def test_canonical_required_lifecycle_gates_include_merge_commit_ci(self):
        """The authority the corrected rule cites — read from the live load-bearing module."""
        assert "MERGE_COMMIT_CI_SUCCESS" in A.REQUIRED_LIFECYCLE_GATES
        assert "MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION" in A.REQUIRED_LIFECYCLE_GATES
        assert len(A.REQUIRED_LIFECYCLE_GATES) == 6

    def test_canonical_stage_1_names_all_six_gates(self, prereg):
        assert (
            prereg["stages"]["stage_1"]["executable_only_after"]
            == "XASSET_0029_LIFECYCLE_CLOSURE_ALL_SIX_GATES_THEN_EXTERNAL_ONE_SHOT_PREEXECUTION_ATTESTATION"
        )

    def test_authorization_module_is_cited_not_modified(self, decision):
        section = _norm(_section(decision, "I"))
        assert "neither reads nor modifies that module's bytes" in section

    # ---- every mirror carries the corrected condition ----

    def test_section_a_summary_carries_merge_commit_ci(self, decision):
        section = _norm(_section(decision, "A"))
        assert "merge-commit CI whose `head_sha` is the exact merge SHA" in section
        assert "All seven conditions at §I are required" in section

    def test_consequences_mirror_carries_complete_closure(self, decision):
        tail = _norm(decision.split("## Consequences")[1])
        assert "in full" in tail
        assert "merge-commit CI on the exact merge SHA" in tail

    def test_alternatives_mirror_rejects_merge_alone(self, decision):
        tail = _norm(decision.split("## Alternatives Considered")[1])
        assert "all seven conditions, including successful merge-commit CI on the exact merge SHA" in tail

    def test_workstreams_mirror_carries_merge_commit_ci(self):
        text = _norm((ROOT / "operations/WORKSTREAMS.yaml").read_text(encoding="utf-8"))
        assert "SUCCESSFUL MERGE-COMMIT CI WHOSE head_sha IS THE EXACT MERGE SHA" in text
        assert "post-merge verification without exact merge-commit CI does not" in text

    def test_claude_md_pointer_carries_merge_commit_ci(self):
        text = _norm((ROOT / "CLAUDE.md").read_text(encoding="utf-8"))
        assert "successful merge-commit CI whose `head_sha` is the exact merge SHA" in text
        assert "a green PR-head run is not a substitute" in text

    def test_correction_history_records_the_finding(self, decision):
        normalised = _norm(decision)
        assert "Correction 1" in normalised
        assert "4951655331" in normalised
        assert "omits successful merge-commit CI on the exact merge SHA" in normalised

    def test_correction_is_lifecycle_wording_only(self, decision):
        normalised = _norm(decision)
        assert "Lifecycle-effectivity wording only" in normalised

    def test_gb_invariant_is_restated_unchanged(self, decision):
        section = _norm(decision.split("### I.")[1].split("### J.")[0])
        assert (
            "no outcome-producing executable code may be created, changed, or left outside the "
            "bound execution identity after the final rebinding and before" in section
        )

    def test_no_part_of_gb_is_performed(self, decision):
        section = _norm(decision.split("### I.")[1].split("### J.")[0])
        assert "authorizes none of §G.B and performs no part of it" in section


class TestNoGateResultIsAsserted:
    def test_decision_asserts_no_per_construction_outcome(self, decision):
        assert (
            "evaluates no gate for any construction and asserts no per-construction outcome"
            in _norm(decision)
        )

    def test_no_construction_id_appears_with_a_gate_result(self, decision):
        """A crude but effective guard: no construction identifier is quoted at all."""
        assert "::LOWER::" not in decision
        assert "::UPPER::" not in decision

    def test_universe_carries_no_gate_outcome(self, universe):
        for entry in universe.values():
            for gate in ALL_GATE_IDS:
                assert gate not in entry


class TestWorkNotCreated:
    def test_eliminated_work_is_tabulated(self, decision):
        section = decision.split("### J.")[1].split("### K.")[0]
        assert "Why not created" in section

    def test_no_program_wide_modal_rule_is_created(self, decision):
        section = decision.split("### J.")[1].split("### K.")[0]
        assert "program-wide gate-modal register rule" in section

    def test_g2_reading_map_extension_is_refused(self, decision):
        section = decision.split("### J.")[1].split("### K.")[0]
        assert "g2_reading_mapping" in section

    def test_enforcement_defect_correction_is_deferred_to_gb(self, decision):
        section = decision.split("### J.")[1].split("### K.")[0]
        assert "§G.B step 3" in section

    def test_relabelling_is_refused(self, decision):
        section = decision.split("### J.")[1].split("### K.")[0]
        assert "Relabel the 360" in section


class TestAbsoluteNonAuthorization:
    @pytest.mark.parametrize(
        "phrase",
        [
            "generates no `XASSET-0029` attestation",
            "arms and executes no Stage 1",
            "creates no Stage-1 runner",
            "consumes nothing of `ATTEMPT_1`",
            "corrects no validator",
            "extends no `LOAD_BEARING_RELPATHS`",
            "amends no canonical file",
            "enters no part of\n§G.B",
            "creates no snapshot successor",
            "weakens no validator or test",
            "rewrites no accepted history",
        ],
    )
    def test_non_authorization_clause_present(self, decision, phrase):
        assert _norm(phrase) in _norm(decision)

    def test_protected_risk_path_is_not_referenced(self, decision):
        assert "protected result path** and reuses no `RISK`" in _norm(decision)

    def test_module_does_not_read_the_protected_path(self):
        """This suite must not reach the protected RISK results location either.

        Checked at AST level over *executable* string constants rather than over raw source text,
        so the guard cannot be satisfied — or defeated — by the wording of this module's own prose.
        The two key names are assembled from fragments for the same reason: a literal here would
        make the test match itself.
        """
        protected_key = "risk_lane" + "_boundary"
        protected_field = "protected_result" + "_path"
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        # Exact equality, not substring containment: a *read* of the canonical block looks like the
        # bare key name used as a subscript or attribute, never like prose that mentions it.
        constants = {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        assert protected_key not in constants
        assert protected_field not in constants
        # And no attribute access of either name anywhere in the module.
        attributes = {
            node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
        }
        assert protected_key not in attributes
        assert protected_field not in attributes

    def test_no_portfolio_state_is_changed(self, decision):
        for token in ("`targets.yaml`", "`holdings.yaml`", "`gates.yaml`", "`issuer_lookthrough.yaml`"):
            assert token in decision


class TestNoMutationOfLoadBearingOrCanonicalPaths:
    def test_supporting_artifact_is_this_module(self, decision):
        head = decision.split("---")[1]
        meta = yaml.safe_load(head)
        assert meta["supporting_artifact"] == Path(__file__).name

    def test_decision_id_and_status(self, decision):
        head = decision.split("---")[1]
        meta = yaml.safe_load(head)
        assert meta["decision_id"] == "XASSET-0035"
        assert meta["status"] == "Proposed"

    def test_related_decisions_include_the_four_predecessors(self, decision):
        head = decision.split("---")[1]
        meta = yaml.safe_load(head)
        for predecessor in ("XASSET-0031", "XASSET-0032", "XASSET-0033", "XASSET-0034"):
            assert predecessor in meta["related_decisions"]

    def test_this_module_performs_no_filesystem_write(self):
        """AST-level guard: no mutating filesystem call is made anywhere in this module.

        Checked over call *targets* rather than raw source text, so the guard is precise and cannot
        match its own assertion strings.
        """
        mutating = {
            "write_text",
            "write_bytes",
            "mkdir",
            "touch",
            "unlink",
            "rmdir",
            "rename",
            "replace",
            "chmod",
            "symlink_to",
        }
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        called = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        # ``str.replace`` is not a filesystem call; exclude it by requiring a Path-shaped receiver.
        offenders = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in mutating
            and node.func.attr != "replace"
        }
        assert offenders == set(), f"mutating filesystem calls present: {sorted(offenders)}"
        assert "write_text" not in called and "mkdir" not in called


# ======================================================================================
# Determinism — the bar this whole series is measured against
# ======================================================================================


class TestTwoConformingExecutorsCannotDiverge:
    def test_b1_register_is_single_valued(self, decision):
        """Exactly one of the two registers is selected, and the other is named as rejected."""
        section = decision.split("#### E.2")[1].split("#### E.3")[0]
        assert "lawful satisfiability" in section
        assert "not against execution-time world state" in section

    def test_b2_rule_is_a_total_function_of_frozen_identity(self, universe):
        """Applied twice to the same frozen inputs it must return the same partition."""
        first = {cid: _comparison_group(cid) for cid in universe}
        second = {cid: _comparison_group(cid) for cid in universe}
        assert first == second
        assert len(set(first.values())) == 4

    def test_b2_rule_is_decidable_for_every_construction(self, universe):
        for cid, entry in universe.items():
            group = _comparison_group(cid)
            counterpart = _counterpart(cid)
            consumes = group in {"UNORDERED_PAIR", "DIRECT_ALTERNATIVE_SLEEVE"}
            if consumes:
                assert frozenset((entry["sleeve"], counterpart)) in CANONICAL_PAIRS
            else:
                assert counterpart in (None, "UNSIZED_UNASSIGNED_CAPITAL")

    def test_b3_rule_selects_one_value_from_a_closed_four_value_vocabulary(self, prereg):
        vocab = prereg["result_vocabulary"]["gate_result_vocabulary"]
        assert "UNABLE_TO_DETERMINE" in vocab
        assert len(vocab) == 4

    def test_determination_names_all_three_as_resolved(self, decision):
        assert "ALL_THREE_RESIDUAL_SEMANTIC_BLOCKERS_RESOLVED" in decision
        table = decision.split("### A.")[1].split("### B.")[0]
        assert "**B1**" in table and "**B2**" in table and "**B3**" in table


class TestCorrection1ChangedOnlyLifecycleWording:
    """Correction 1 must not have moved any B1/B2/B3 semantic, nor unarmed Stage 1's state."""

    def test_b1_rule_text_unchanged(self, decision):
        section = _norm(_section(decision, "E"))
        assert "lawful satisfiability of the frozen construction specification" in section
        assert "not against execution-time world state" in section
        assert "constitutive governed statement, not a reading" in section

    def test_b2_rule_and_inventory_unchanged(self, decision, universe):
        section = _norm(_section(decision, "F"))
        assert (
            "if and only if both of its own two frozen named comparison endpoints are members of "
            "the four-sleeve set" in section
        )
        assert "never by the presence or absence of the `unordered_pair_id` label" in section
        # 480 / 200 inventory recomputed live, not read from prose.
        consuming = sum(
            1
            for cid in universe
            if _comparison_group(cid) in {"UNORDERED_PAIR", "DIRECT_ALTERNATIVE_SLEEVE"}
        )
        assert consuming == 480
        assert len(universe) - consuming == 200

    def test_b3_rule_and_fence_unchanged(self, decision):
        section = _norm(_section(decision, "G"))
        assert "records `UNABLE_TO_DETERMINE`" in section
        assert "applies to no other gate" in section
        assert "does not give `G10` an `UNABLE_TO_DETERMINE` posture" in section
        assert "remains prerequisite-blocked" in section

    def test_determination_verdict_unchanged(self, decision):
        assert "ALL_THREE_RESIDUAL_SEMANTIC_BLOCKERS_RESOLVED" in decision

    def test_six_six_map_and_open_questions_unchanged(self, decision, prereg):
        normalised = _norm(decision)
        assert "6/6 map is unchanged" in normalised
        assert "§K.1 stays unresolved" in normalised
        assert "`XASSET-0020` §E.1 stays unamended" in normalised
        assert prereg["open_reading_handling"]["resolved_by_this_program"] is False

    def test_enforcement_defect_disclosure_preserved_per_note_1(self, decision):
        """FULL review NOTE 1: this disclosure is successor scope and must survive the correction."""
        section = _norm(decision.split("#### F.8")[1].split("### G.")[0])
        assert "480" in section
        assert "does not correct it" in section
        assert "neither re-derived, expanded, narrowed, nor corrected" in section

    def test_stage_1_still_unarmed_after_correction(self):
        authorized, _reason = A.new_execution_is_authorized()
        assert authorized is False
        assert not A.AUTHORIZATION_ROOT.exists()

    def test_frozen_inputs_still_exact_after_correction(self):
        """AMENDED BY XASSET-0036 SS-E.1/SS-E.7, as in ``test_canonical_pins_match`` above.

        The canonical digests now track the current EFFECTIVE pins. The FROZEN UNIVERSE hash is
        deliberately still asserted against its literal accepted value: XASSET-0036 SS-F forbids
        changing the construction identities, universe, cardinality, or universe hash, so that one
        must NOT have moved.
        """
        import hashlib

        assert (
            hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
            == A.CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH]
        )
        assert (
            hashlib.sha256(PREREG.read_bytes()).hexdigest()
            == A.CANONICAL_PINS[A.CANONICAL_PREREGISTRATION_RELPATH]
        )
        assert CU.universe_aggregate_sha256() == FROZEN_UNIVERSE_SHA256


class TestSuiteHasNoVacuousAssertions:
    """An AST guard: every test function must contain at least one real assertion."""

    def test_every_test_function_asserts(self):
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        offenders: list[str] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef) or not node.name.startswith("test"):
                continue
            has_assert = any(
                isinstance(inner, (ast.Assert, ast.Raise)) for inner in ast.walk(node)
            )
            has_pytest_raises = any(
                isinstance(inner, ast.withitem) for inner in ast.walk(node)
            )
            if not (has_assert or has_pytest_raises):
                offenders.append(node.name)
        assert offenders == [], f"vacuous test functions: {offenders}"

    def test_suite_covers_all_three_blockers(self):
        source = Path(__file__).read_text(encoding="utf-8")
        assert "class TestB1ModalRegister" in source
        assert "class TestB2ConsumptionRule" in source
        assert "class TestB3RecordingPosture" in source
        assert "class TestB3ScopeFence" in source
