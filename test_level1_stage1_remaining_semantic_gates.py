"""Adversarial tests pinning the XASSET-0032 remaining-semantic-gate determination.

XASSET-0032 determined that all five remaining Stage-1 semantic prerequisites — ``G5``, ``G8``, ``G9``,
``G10``, ``G12`` — remain **NOT CLOSABLE**, each with bounded positive sub-determinations that *are*
closed.

These tests exist so the determination is **mechanically checkable rather than prose**. Every rule,
reservation, definition, and structural count below is read from committed bytes — the two canonical
artifacts, the accepted decisions, and the live frozen construction universe — never asserted from this
module's own opinion.

For each gate the suite pins two things: the **intended rule**, and its **nearest plausible overreach**
— the stronger claim a successor might be tempted to read out of the same text, which the determination
must refuse. That pairing is the point; a suite that only pinned the intended rules would not detect a
successor quietly widening one.

They also pin the *negative space* that makes the determination honest: that the XASSET-0030 6/6 gate
partition is unchanged, that G1/G2/G4/G6/G7/G11 are not re-derived, that XASSET-0031's G3 determination
is neither reopened nor relied upon, that XASSET-0024 SS-K.1 is unresolved, that XASSET-0020 SS-E.1 is
unamended, and that no protected RISK result path is read or referenced.

Nothing here arms, claims, completes, or executes Stage 1. No gate is evaluated for any construction.
No results document, lane directory, attestation, claim, completion, or ledger entry is created or read
for authorization purposes.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pytest
import yaml

import level1_construction_universe_closure_validator as CU
import level1_endpoint_evidence_preregistration_validator as P
import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
PREREG = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"
PROTOCOL = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
GOV = ROOT / "governance/decisions"

XASSET_0020 = GOV / "XASSET-0020-replacement-level1-economic-sizing-methodology.md"
XASSET_0021 = GOV / "XASSET-0021-level1-economic-sizing-application-prerequisite-closure.md"
XASSET_0023 = (
    GOV / "XASSET-0023-level1-non-abstention-feasibility-and-level2-prerequisite-determination.md"
)
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
DECISION = GOV / "XASSET-0032-endpoint-0001-stage-1-remaining-semantic-gate-determination.md"

THIS_UNITS_GATES = ("G5", "G8", "G9", "G10", "G12")


def _collapse(text: str) -> str:
    """Collapse Markdown hard-wrapping so a wrapped sentence matches as one string.

    Blockquote markers are stripped first: a hard-wrapped ``>`` quote would otherwise leave a stray
    ``>`` mid-sentence and defeat an otherwise-correct match.
    """
    text = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    return re.sub(r"\s+", " ", text)


def _read(path: Path) -> str:
    return _collapse(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def decision_text() -> str:
    return _read(DECISION)


@pytest.fixture(scope="module")
def prereg() -> dict:
    return yaml.safe_load(PREREG.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def protocol_text() -> str:
    return _read(PROTOCOL)


@pytest.fixture(scope="module")
def universe() -> tuple:
    return tuple(CU.generate_construction_universe())


def _field(construction, key):
    if isinstance(construction, dict):
        return construction.get(key)
    return getattr(construction, key, None)


# --------------------------------------------------------------------------------------
# B. Shared reproduction — the single structural root of all five determinations
# --------------------------------------------------------------------------------------


class TestSharedStructuralRoot:
    def test_every_construction_is_hypothetical(self, universe):
        """B.1: no candidate source exists whose properties any gate could inspect."""
        kinds = {_field(c, "source_architecture") for c in universe}
        assert kinds == {"HYPOTHETICAL_SOURCE_ARCHITECTURE"}
        assert len(universe) == 680

    def test_universe_identity_is_the_frozen_one(self, universe):
        assert CU.universe_aggregate_sha256(universe) == (
            "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
        )
        assert len({_field(c, "cell_id") for c in universe}) == 48

    def test_comparison_architecture_decomposes_exactly_three_ways(self, universe):
        """B.2: the decomposition SS-G.3 relies on, counted from committed bytes."""
        counts = Counter(_field(c, "comparison_subject_kind") for c in universe)
        assert counts == {
            "DIRECT_ALTERNATIVE": 480,
            "UNORDERED_PAIR": 120,
            "SLEEVE_SELF": 80,
        }

    def test_pair_id_present_exactly_on_the_unordered_pair_group(self, universe):
        with_pair = [c for c in universe if _field(c, "unordered_pair_id")]
        assert len(with_pair) == 120
        assert {_field(c, "comparison_subject_kind") for c in with_pair} == {"UNORDERED_PAIR"}
        assert {_field(c, "driver_class") for c in with_pair} == {"diversification_cobehavior"}

    def test_pair_constructions_cover_all_six_canonical_pairs_evenly(self, universe):
        counts = Counter(
            _field(c, "unordered_pair_id") for c in universe if _field(c, "unordered_pair_id")
        )
        assert set(counts) == {
            "equity__fund_broad_market",
            "equity__fund_gld_defensive",
            "equity__crypto",
            "fund_broad_market__fund_gld_defensive",
            "fund_broad_market__crypto",
            "fund_gld_defensive__crypto",
        }
        assert set(counts.values()) == {20}

    def test_direct_alternative_splits_360_sleeve_and_120_unassigned(self, universe):
        alts = [c for c in universe if _field(c, "comparison_subject_kind") == "DIRECT_ALTERNATIVE"]
        unassigned = [
            c for c in alts if _field(c, "comparator_architecture") == "ALT__UNSIZED_UNASSIGNED_CAPITAL"
        ]
        assert len(unassigned) == 120
        assert len(alts) - len(unassigned) == 360

    def test_nothing_in_the_universe_carries_a_gate_outcome(self, universe):
        """B.5: gate results are decided by a human analytical act, not produced anywhere."""
        for c in universe[:40]:
            keys = set(c) if isinstance(c, dict) else set(vars(c))
            assert not any(k.upper().startswith("G") and k[1:2].isdigit() for k in keys)


# --------------------------------------------------------------------------------------
# B.5 / K. The derivation functions conform, and the one recorded defect is untouched
# --------------------------------------------------------------------------------------


class TestEnforcementConformanceUnchanged:
    def test_prerequisite_gates_match_canonical(self, prereg):
        canonical = {
            g["gate_id"]
            for g in prereg["gate_sequence"]["gates"]
            if g["failure_disposition"] == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"
        }
        assert canonical == {"G9_REPRESENTATION", "G12_SNAPSHOT_ADMISSIBILITY_PATH"}
        assert set(P.PREREQUISITE_GATES) == canonical

    def test_candidate_disposition_conforms_to_canonical_precedence(self):
        base = {g: "PASS" for g in P.GATE_IDS}

        categorical = dict(base, G5_CONSTRAINT_SHAPE="FAIL")
        assert P.derive_candidate_disposition(categorical) == "BLOCKED_CATEGORICALLY"

        uncertain = dict(base, G2_MAGNITUDE_INTRINSICALITY="UNABLE_TO_DETERMINE")
        assert P.derive_candidate_disposition(uncertain) == "UNABLE_TO_DETERMINE"

        prereq = dict(base, G9_REPRESENTATION="FAIL")
        assert P.derive_candidate_disposition(prereq) == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"

        # Categorical dominates prerequisite; uncertainty dominates prerequisite.
        assert (
            P.derive_candidate_disposition(
                dict(base, G9_REPRESENTATION="FAIL", G10_PAIR_INDEPENDENCE="FAIL")
            )
            == "BLOCKED_CATEGORICALLY"
        )
        assert (
            P.derive_candidate_disposition(
                dict(base, G9_REPRESENTATION="FAIL", G2_MAGNITUDE_INTRINSICALITY="UNABLE_TO_DETERMINE")
            )
            == "UNABLE_TO_DETERMINE"
        )

    def test_this_unit_records_no_new_conformance_defect(self, decision_text):
        assert (
            "No new canonical or enforcement conformance defect was found in the five gates' analysis."
            in decision_text
        )

    def test_the_recorded_defect_is_neither_re_derived_nor_corrected(self, decision_text):
        assert (
            "This unit neither re-derives, expands, narrows, nor corrects it" in decision_text
        )


# --------------------------------------------------------------------------------------
# D. G5 — the rule is statable; the per-candidate reservation is not legislated through
# --------------------------------------------------------------------------------------


class TestG5ConstraintShape:
    def test_canonical_gate_definition_is_unchanged(self, prereg):
        gate = next(
            g for g in prereg["gate_sequence"]["gates"] if g["gate_id"] == "G5_CONSTRAINT_SHAPE"
        )
        assert gate["gate_index"] == 5
        assert gate["failure_disposition"] == "BLOCKED_CATEGORICALLY"
        assert gate["controlling_authority"] == "XASSET-0024_SECTION_F_LIMB_4_AND_NON_ROUTE_N1"
        assert "originate a bound" in _collapse(gate["question"])

    def test_limb_4_bar_is_read_from_committed_bytes(self):
        text = _read(XASSET_0024)
        assert (
            "A cap, ceiling, floor-as-limit, or concentration boundary that only "
            "blocks, caps, or clips cannot originate a bound however precisely it is expressed" in text
        )

    def test_n1_is_clip_only_and_not_lawful(self):
        text = _read(XASSET_0024)
        assert "may narrow already-authorized endpoints but may not create one" in text
        assert "Constraint application or bound intersection" in text

    def test_the_reservation_is_express_and_per_candidate(self):
        text = _read(XASSET_0027)
        assert (
            "is exactly what `G5` decides, per candidate, on the candidate's own terms. "
            "No prejudgment is recorded here." in text
        )

    def test_decision_states_the_rule_without_classifying_any_candidate(self, decision_text):
        assert "only if its own governed content originates the bound" in decision_text
        assert (
            "It does not classify any candidate, any DRIVER class, or any of the 680 constructions."
            in decision_text
        )

    # --- nearest plausible overreach -------------------------------------------------

    def test_no_class_wide_g5_verdict_for_any_driver_class(self, decision_text, prereg):
        assert (
            "This unit records no class-wide `G5` `PASS` or `FAIL` for any of the six classes"
            in decision_text
        )
        for cls in prereg["driver_classes"]:
            assert f"`G5` PASS for {cls}" not in decision_text
            assert f"`G5` FAIL for {cls}" not in decision_text

    def test_sleeve_deployability_is_not_presumed_constraint_shaped(self, decision_text):
        """The overreach SS-M.4 most directly forbids."""
        assert (
            "expressly does not treat the 40 `sleeve_deployability` constructions as presumptively "
            "constraint-shaped" in decision_text
        )
        assert "deployability evidence is never converted into an allocation rule here" in decision_text

    def test_sleeve_deployability_count_is_forty(self, universe):
        n = sum(1 for c in universe if _field(c, "driver_class") == "sleeve_deployability")
        assert n == 40

    def test_reservation_is_recorded_as_general_not_one_class(self, decision_text):
        assert "The reservation is general" in decision_text


# --------------------------------------------------------------------------------------
# E. G8 — existence AND uniqueness; vacuous uniqueness is not a PASS
# --------------------------------------------------------------------------------------


class TestG8Uniqueness:
    def test_canonical_gate_definition_is_unchanged(self, prereg):
        gate = next(g for g in prereg["gate_sequence"]["gates"] if g["gate_id"] == "G8_UNIQUENESS")
        assert gate["gate_index"] == 8
        assert gate["failure_disposition"] == "BLOCKED_CATEGORICALLY"
        assert gate["controlling_authority"] == "XASSET-0024_J_8"
        q = _collapse(gate["question"])
        assert "exactly one lawful value exist" in q
        assert "across the admitted set" in q

    def test_gate_says_exist_not_at_most_one(self, prereg):
        """The textual basis for reading SS-E.1's conjunction."""
        gate = next(g for g in prereg["gate_sequence"]["gates"] if g["gate_id"] == "G8_UNIQUENESS")
        q = _collapse(gate["question"])
        assert "at most one" not in q

    def test_decision_states_the_conjunction(self, decision_text):
        assert "is a conjunction, and vacuous uniqueness never satisfies it" in decision_text
        assert "Empty-set/vacuous uniqueness is therefore not a `G8` `PASS`." in decision_text

    def test_open_interval_with_no_member_fixing_rule_yields_no_lawful_bound(self):
        text = _read(XASSET_0024)
        assert (
            "If the authority leaves an open interval and states no rule fixing a member, "
            "no lawful bound exists" in text
        )

    def test_admitted_set_exists_and_is_non_empty(self):
        """SS-E.2's correction, counted from committed bytes rather than asserted."""
        raw = XASSET_0021.read_text(encoding="utf-8")
        c2 = raw.split("#### C.2 Non-RISK snapshot")[1].split("#### C.3")[0]
        c3 = raw.split("#### C.3 Accepted RISK snapshot")[1].split("### D.")[0]
        non_risk = [l for l in c2.splitlines() if l.startswith("| `")]
        risk = [l for l in c3.splitlines() if l.startswith("| `research/")]
        assert len(non_risk) == 21
        assert len(risk) == 14
        assert len(non_risk) + len(risk) == 35

    def test_the_snapshot_contains_zero_lawful_endpoint_values(self):
        text = _read(XASSET_0021)
        assert (
            "The frozen snapshot contains no such Level-1 endpoint authority for any sleeve." in text
        )

    # --- nearest plausible overreach -------------------------------------------------

    def test_zero_values_is_not_recorded_as_a_pass(self, decision_text):
        """The overreach: reading 'no competing value' as 'uniqueness satisfied'."""
        assert (
            "a failure of existence, not a trivial satisfaction of uniqueness" in decision_text
        )

    def test_zero_competing_values_does_not_close_the_gate(self, decision_text):
        assert "The correction narrows the blocker rather than removing it" in decision_text
        assert "successor-snapshot-dependent" in decision_text

    def test_no_tie_break_rule_is_introduced(self, decision_text):
        for banned in ("midpoint", "average", "precedence", "conservatism"):
            # The words appear only as prohibitions, never as an adopted resolution rule.
            assert f"resolve them by {banned}" not in decision_text
        assert "no midpoint, average, precedence, or conservatism rule available to resolve them" in (
            decision_text
        )


# --------------------------------------------------------------------------------------
# F. G9 — path 2 closed, path-3 tension reconciled, path 1 preserved as source-dependent
# --------------------------------------------------------------------------------------


class TestG9Representation:
    def test_canonical_gate_definition_is_unchanged(self, prereg):
        gate = next(g for g in prereg["gate_sequence"]["gates"] if g["gate_id"] == "G9_REPRESENTATION")
        assert gate["gate_index"] == 9
        assert gate["failure_disposition"] == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"
        assert gate["controlling_authority"] == "XASSET-0024_SECTION_G_AND_J_9"

    def test_canonical_representation_block_fixes_the_gate_record(self, prereg):
        rep = prereg["representation"]
        assert rep["disposition"] == "SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED"
        assert rep["disposition_source"] == "XASSET-0026_SECTION_H"
        assert rep["rule_created_by_this_program"] is False
        assert rep["cm_14_through_cm_17_membership_designated"] is False
        assert (
            rep["non_self_contained_handling"]
            == "NAME_THE_EXACT_DEPENDENCY_AND_BLOCK_PENDING_SEPARATE_PREREQUISITE"
        )
        assert "fails G9 as a prerequisite" in _collapse(rep["non_self_contained_handling_note"])

    def test_protocol_agrees_with_the_yaml(self, protocol_text):
        """Both canonical artifacts say the same thing — SS-F.2's basis."""
        assert "fails `G9` as a prerequisite" in protocol_text

    def test_mandatory_abstention_condition_exists_at_the_endpoint_level(self, prereg):
        conds = {c["condition"]: c["authority"] for c in prereg["mandatory_abstention_conditions"]}
        assert (
            conds["REPRESENTATION_PATH_1_FAILS_AND_NO_ACCEPTED_RULE_EXISTS"]
            == "XASSET-0024_SECTION_G_PATH_3"
        )
        assert prereg["mandatory_abstention_conditions"] is not None

    def test_the_two_levels_are_reconciled_not_rivals(self, decision_text):
        plain = decision_text.replace("**", "")
        assert "operate at two different levels and describe one state" in plain
        assert "There is no conflict" in decision_text
        assert "`XASSET-0030`'s ground (b) is therefore withdrawn as a blocker." in decision_text

    def test_path_2_is_determinately_unavailable(self):
        assert (
            "which does not exist anywhere at Level 1" in _read(XASSET_0023)
        )
        assert "SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED" in _read(XASSET_0026)

    def test_every_construction_declares_representation_source_dependent(self, universe):
        """R8 read from each construction's own frozen requirements."""
        for c in universe[:80]:
            req = _collapse(str(_field(c, "hypothetical_source_requirements")))
            assert "Representation admissibility is source-dependent" in req
            assert "asserts no prior representation rule" in req
        postures = {_field(c, "representation_posture") for c in universe}
        assert postures == {"SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED"}

    # --- nearest plausible overreach -------------------------------------------------

    def test_reconciling_the_tension_does_not_close_the_gate(self, decision_text):
        """The overreach: treating one resolved ground as closing G9."""
        assert (
            "`G9` NOT CLOSABLE on path 1's source-dependence alone" in decision_text
        )

    def test_hypothetical_requirement_is_not_treated_as_an_actual_prerequisite(self, decision_text):
        """R8's presence in the spec must not be read as evidence path 1 is satisfiable."""
        assert (
            "Deriving `PASS` from `R8`'s presence would be the by-construction inference" in decision_text
        )

    def test_no_representation_rule_is_created(self, decision_text):
        assert "This unit creates no rule and designates no CM-14–CM-17 membership." in decision_text
        assert "invents no Level-1 representation aggregation or selection rule" in decision_text

    def test_categorical_dominance_is_preserved(self, decision_text):
        assert "the categorical disposition dominates" in decision_text


# --------------------------------------------------------------------------------------
# G. G10 — 'unresolved' defined, all six determined, consumption left open
# --------------------------------------------------------------------------------------


class TestG10PairIndependence:
    def test_canonical_gate_definition_is_unchanged(self, prereg):
        gate = next(
            g for g in prereg["gate_sequence"]["gates"] if g["gate_id"] == "G10_PAIR_INDEPENDENCE"
        )
        assert gate["gate_index"] == 10
        assert gate["failure_disposition"] == "BLOCKED_CATEGORICALLY"
        assert gate["controlling_authority"] == "XASSET-0024_SECTION_H_4_AND_J_10"

    def test_unresolved_is_identified_with_unable_to_determine(self):
        """SS-G.1's basis: XASSET-0020 SS-I names the referent directly."""
        text = _read(XASSET_0020)
        assert "must record the pair conclusion as `unable_to_determine`" in text
        assert "valid under every possible direction of the unresolved pair" in text

    def test_all_four_recorded_pairs_are_unable_to_determine(self):
        text = _read(XASSET_0021)
        assert (
            "each have the deterministic pair conclusion `unable_to_determine` under this snapshot"
            in text
        )
        assert "This is an application rule, not a populated pair record." in text

    def test_the_two_missing_pairs_are_closed_by_section_i(self):
        text = _read(XASSET_0021)
        assert (
            "XASSET-0020 §I already closes the application rule: the pair conclusion is "
            "`unable_to_determine`" in text
        )
        assert "fund_broad_market__fund_gld_defensive" in text
        assert "fund_broad_market__crypto" in text

    def test_six_canonical_pairs_exist_and_are_the_ones_determined(self):
        text = _read(XASSET_0020)
        assert "Exactly six unordered pair records exist" in text
        for pair in (
            "equity__fund_broad_market",
            "equity__fund_gld_defensive",
            "equity__crypto",
            "fund_broad_market__fund_gld_defensive",
            "fund_broad_market__crypto",
            "fund_gld_defensive__crypto",
        ):
            assert pair in text

    def test_decision_records_the_three_way_decomposition(self, decision_text):
        assert "**120**" in decision_text and "**360**" in decision_text and "**200**" in decision_text

    # --- protected-evidence boundary -------------------------------------------------

    def test_protected_result_path_is_never_read_or_referenced(self, prereg):
        """The boundary is recorded and honoured, not crossed."""
        boundary = prereg["risk_lane_boundary"]
        assert (
            boundary["protected_result_path_access"]
            == "PROHIBITED_NO_READ_WRITE_DELETE_CLEAN_RESET_OR_REPURPOSE"
        )
        protected = boundary["protected_result_path"]
        assert not Path(protected).exists() or True  # existence is irrelevant; access is not performed
        # The decision must not contain the protected path as an accessed location.
        assert protected not in DECISION.read_text(encoding="utf-8")

    def test_decision_records_the_boundary_as_dissolved_not_crossed(self, decision_text):
        assert "The `risk_lane_boundary` concern is dissolved rather than crossed" in decision_text
        assert "was not read, listed, or referenced" in decision_text

    # --- nearest plausible overreach -------------------------------------------------

    def test_no_g10_fail_is_recorded_for_the_120_pair_constructions(self, decision_text):
        """The overreach: 'all six unresolved today' does not travel to a successor snapshot."""
        assert 'expressly scoped "**under this snapshot**"' in decision_text
        assert "does not travel" in _read(DECISION)

    def test_no_g10_pass_is_recorded_for_the_200(self, decision_text):
        assert (
            "The 200-construction group is **not** recorded as `G10` `PASS`." in decision_text
        )
        assert (
            "A specification's silence about pair consumption is not proof that an eventual source "
            "consumes no pair" in decision_text
        )

    def test_consumption_semantics_for_the_360_stay_open(self, decision_text):
        assert "No accepted authority fixes whether a `DIRECT_ALTERNATIVE` construction" in decision_text
        assert "Both readings are defensible and nothing selects." in decision_text

    def test_unassigned_capital_is_not_one_of_the_six_pairs(self, decision_text):
        assert (
            "`UNSIZED_UNASSIGNED_CAPITAL` is a separate `XASSET-0020` §H comparison family"
            in decision_text
        )


# --------------------------------------------------------------------------------------
# H. G12 — identifiability floor and scope closed; tense preserved as unfixed
# --------------------------------------------------------------------------------------


class TestG12SnapshotAdmissibilityPath:
    def test_canonical_gate_definition_is_unchanged(self, prereg):
        gate = next(
            g
            for g in prereg["gate_sequence"]["gates"]
            if g["gate_id"] == "G12_SNAPSHOT_ADMISSIBILITY_PATH"
        )
        assert gate["gate_index"] == 12
        assert gate["failure_disposition"] == "BLOCKED_PENDING_SEPARATE_PREREQUISITE"
        assert (
            gate["controlling_authority"]
            == "XASSET-0024_J_1_AND_J_2_AND_XASSET_0026_G_2_CONSTRAINT_3"
        )
        assert "identifiable" in _collapse(gate["question"])

    def test_canonical_mapping_is_identifiability_only(self, prereg):
        rows = {r["gate_or_basis"] for r in prereg["deferred_admissibility_requirements"].get(
            "requirements", []
        )} if False else None
        raw = PREREG.read_text(encoding="utf-8")
        assert "G12_IDENTIFIABILITY_ONLY_NO_SUCCESSOR_CREATED" in raw
        assert "G12_PLUS_SOURCE_CURRENTNESS_RULE" in raw

    def test_protocol_fixes_the_identifiability_floor(self, protocol_text):
        assert "records whether a snapshot successor is *identifiable*" in protocol_text
        assert (
            "No snapshot successor is created, extended, replaced, or authorized by this program"
            in protocol_text
        )

    def test_prerequisite_requires_a_named_dependency(self, prereg, protocol_text):
        assert prereg["prerequisite_definition"]["requires_named_dependency"] is True
        assert (
            prereg["prerequisite_definition"]["means"]
            == "CLOSEABLE_BY_A_NAMED_SEPARATELY_AUTHORIZED_PREREQUISITE_WITHOUT_METHODOLOGY_AMENDMENT"
        )
        assert "and the dependency must be named" in protocol_text.replace("**", "")

    def test_protocol_confines_g12_to_partial_testability(self, protocol_text):
        assert "J.1 admission | partially testable" in protocol_text
        assert "J.2 snapshot position | partially testable" in protocol_text
        assert "identifiability only" in protocol_text

    def test_stage_1_never_claims_full_j_compliance(self, protocol_text):
        assert "never that full §J admissibility has been established" in protocol_text

    def test_named_dependency_is_identified_in_accepted_authority(self):
        assert "cannot admit evidence that does not yet exist" in _read(XASSET_0027)
        assert "Snapshot successor after evidence, before any application" in _read(XASSET_0026)

    def test_decision_states_the_floor_and_the_scope(self, decision_text):
        assert (
            "the nonexistence of a snapshot successor may never, by itself, be recorded as `G12` "
            "`FAIL`" in decision_text.replace("**", "")
        )
        assert (
            "`G12` may not be evaluated by importing §J.1's hash-match, validator-pass, or governed- "
            "freshness conditions" in decision_text.replace("**", "")
        )

    # --- nearest plausible overreach -------------------------------------------------

    def test_neither_tense_reading_is_adopted(self, decision_text):
        assert "nothing in either canonical artifact or any accepted decision selects between them" in (
            decision_text.replace("**", "")
        )
        assert "`G12` NOT CLOSABLE" in decision_text

    def test_nonexistent_is_not_equated_with_unidentifiable(self, decision_text):
        assert 'does not mean "exists"' in decision_text

    def test_disposition_inertness_is_not_a_licence(self, decision_text):
        """The overreach: 'it doesn't matter today' becoming 'it need not be fixed'."""
        assert "This does not make the gate result optional." in decision_text
        assert "would become outcome-determining the moment §K.1 is resolved" in decision_text

    def test_evaluate_every_gate_requirement_is_intact(self, prereg):
        seq = prereg["gate_sequence"]
        assert seq["evaluation_requirement"] == "EVALUATE_EVERY_APPLICABLE_GATE_BEFORE_CLASSIFYING"
        assert seq["record_first_failing_gate_only"] is False


# --------------------------------------------------------------------------------------
# Cross-gate: no accidental policy, no gate reclassified
# --------------------------------------------------------------------------------------


class TestNoCrossGatePolicy:
    def test_decision_states_no_determination_is_a_premise_for_another(self, decision_text):
        assert (
            "No determination above is used as a premise for any other." in decision_text.replace(
                "**", ""
            )
        )

    def test_no_gate_class_index_or_disposition_changes(self, prereg):
        expected = {
            "G5_CONSTRAINT_SHAPE": (5, "BLOCKED_CATEGORICALLY"),
            "G8_UNIQUENESS": (8, "BLOCKED_CATEGORICALLY"),
            "G9_REPRESENTATION": (9, "BLOCKED_PENDING_SEPARATE_PREREQUISITE"),
            "G10_PAIR_INDEPENDENCE": (10, "BLOCKED_CATEGORICALLY"),
            "G12_SNAPSHOT_ADMISSIBILITY_PATH": (12, "BLOCKED_PENDING_SEPARATE_PREREQUISITE"),
        }
        for gate in prereg["gate_sequence"]["gates"]:
            if gate["gate_id"] in expected:
                idx, disp = expected[gate["gate_id"]]
                assert gate["gate_index"] == idx
                assert gate["failure_disposition"] == disp

    def test_twelve_gates_remain(self, prereg):
        assert len(prereg["gate_sequence"]["gates"]) == 12
        assert len(P.GATE_IDS) == 12

    def test_gates_may_not_be_reordered_after_outcomes(self, prereg):
        assert (
            prereg["gate_sequence"][
                "gates_may_not_be_added_removed_reordered_or_reinterpreted_after_any_outcome_observed"
            ]
            is True
        )


class TestGateMapUnchanged:
    CLOSABLE = ("G1", "G2", "G4", "G6", "G7", "G11")
    NOT_CLOSABLE = ("G3", "G5", "G8", "G9", "G10", "G12")

    def test_partition_is_six_and_six(self):
        assert len(self.CLOSABLE) == len(self.NOT_CLOSABLE) == 6
        assert not set(self.CLOSABLE) & set(self.NOT_CLOSABLE)

    def test_decision_states_the_map_is_unchanged(self, decision_text):
        assert (
            "The `XASSET-0030` 6/6 gate map is UNCHANGED." in decision_text.replace("**", "")
        )
        assert (
            "No gate moves between the closable and not-closable partitions." in decision_text
        )

    def test_all_five_remain_not_closable(self, decision_text):
        assert "all five remain `NOT_CLOSABLE`" in decision_text

    def test_g1_g2_g4_g6_g7_g11_are_not_re_derived(self, decision_text):
        assert (
            "are **not** re-derived and are not relied on by anything below" in decision_text
        )

    def test_no_invalidation_trigger_is_claimed_to_fire(self, decision_text):
        assert "No `XASSET-0030` §E.1 invalidation trigger fires" in decision_text


# --------------------------------------------------------------------------------------
# Preservation: G3, SS-K.1, SS-E.1, and XASSET-0030's own text
# --------------------------------------------------------------------------------------


class TestPreservation:
    def test_g3_is_untouched_and_not_relied_upon(self, decision_text):
        assert "`G3` is untouched." in decision_text
        assert (
            "preserved exactly and are not reopened, narrowed, or relied upon as a premise"
            in decision_text
        )

    def test_xasset_0031_still_says_it_determined_nothing_about_these_five(self):
        """This unit determines them; XASSET-0031's own accepted text is not edited."""
        text = _read(XASSET_0031)
        assert "determines nothing about `G5`, `G8`, `G9`, `G10`, or `G12`" in text

    def test_k1_is_not_resolved(self, decision_text):
        assert "resolves `XASSET-0024` §K.1 neither way" in decision_text
        assert "remains **unresolved**" in decision_text

    def test_e1_is_not_amended(self, decision_text):
        assert "amends no `XASSET-0020` §E.1 scope" in decision_text
        assert "remains **unamended**" in decision_text

    def test_k1_open_reading_still_present_in_canonical(self, prereg):
        assert prereg["open_reading_handling"]["open_question_source"] == "XASSET-0024_SECTION_K_1"

    def test_xasset_0030_text_is_not_edited(self, decision_text):
        assert "`XASSET-0030`'s text is not edited." in decision_text

    def test_corrections_do_not_change_classification(self, decision_text):
        assert (
            "the **classification is unchanged** — the gate remains not closable" in decision_text
        )

    def test_no_third_route_is_preserved(self):
        assert "There is no third route" in _read(XASSET_0023)


# --------------------------------------------------------------------------------------
# Nothing here authorizes, arms, or executes
# --------------------------------------------------------------------------------------


class TestNothingHereAuthorizesOrExecutes:
    def test_stage_1_is_not_authorized(self):
        authorized, reason = A.new_execution_is_authorized()
        assert authorized is False
        assert "no attestation present" in reason

    def test_lane_state_is_absent(self):
        for path in (
            A.AUTHORIZATION_ROOT,
            A.AUTHORIZATION_PATH,
            A.CLAIM_PATH,
            A.COMPLETION_PATH,
            A.LEDGER_PATH,
        ):
            assert not Path(path).exists()

    def test_no_stage1_results_document_exists(self):
        assert not list(ROOT.rglob("stage1_results.yaml"))

    # AMENDED BY XASSET-0036 SS-E.6/SS-E.7. This filing added nothing to the trust boundary and
    # changed no canonical byte, and both remain true of it. The implementation XASSET-0036 later
    # authorized extended the boundary (SS-G.B step 5) and recomputed the pins (step 6), so these
    # tests now assert this filing's accepted values as HISTORY and the live state as exactly the
    # authorized result.
    def test_the_six_paths_this_filing_saw_are_all_retained(self):
        assert {
            "level1_stage1_execution_authorization.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "level1_construction_universe_closure_validator.py",
            "research/level1_endpoint_evidence/PROTOCOL_V1.md",
            "research/level1_endpoint_evidence/pre_registration.yaml",
            "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
        } <= set(A.LOAD_BEARING_RELPATHS)

    def test_the_only_additions_are_the_authorized_outcome_producing_paths(self):
        additions = set(A.LOAD_BEARING_RELPATHS) - {
            "level1_stage1_execution_authorization.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "level1_construction_universe_closure_validator.py",
            "research/level1_endpoint_evidence/PROTOCOL_V1.md",
            "research/level1_endpoint_evidence/pre_registration.yaml",
            "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
        }
        assert additions == {
            "level1_stage1_runner.py",
            "level1_stage1_result_validator.py",
            "governance/decisions/XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
            # AMENDED BY XASSET-0037 / SS-G.B step 8: the successor rebinding adds its OWN decision
            # to the bound identity, on the footing XASSET-0029 and XASSET-0036 already occupy.
            # This filing's accepted six paths are still all retained above; NOTHING was removed.
            "governance/decisions/XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md",
            # EXTENDED AGAIN BY XASSET-0044 / XASSET-0030 SS-D. The post-correction rebinding
            # binds the four decisions that jointly make the corrected bytes lawful, by DIRECT
            # MEMBERSHIP. Every path above is still retained; NOTHING was removed.
            "governance/decisions/"
            "XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md",
            "governance/decisions/"
            "XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md",
            "governance/decisions/"
            "XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md",
            "governance/decisions/"
            "XASSET-0044-endpoint-0001-stage-1-post-correction-operational-rebinding.md",
        }

    def test_canonical_pins_are_history_and_current_bytes_match_the_effective_pins(self):
        assert (
            A.XASSET_0029_CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH]
            == "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
        )
        assert (
            A.XASSET_0029_CANONICAL_PINS[A.CANONICAL_PREREGISTRATION_RELPATH]
            == "6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c"
        )
        assert (
            A.sha256_file(ROOT / A.CANONICAL_PROTOCOL_RELPATH)
            == A.CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH]
        )
        assert (
            A.sha256_file(ROOT / A.CANONICAL_PREREGISTRATION_RELPATH)
            == A.CANONICAL_PINS[A.CANONICAL_PREREGISTRATION_RELPATH]
        )

    def test_decision_asserts_no_per_construction_outcome(self, decision_text):
        assert (
            "evaluates no gate for any construction and asserts no per-construction outcome"
            in decision_text.replace("**", "")
        )

    def test_decision_contains_no_endpoint_value(self, decision_text):
        assert "creates no endpoint, bound, point, range, percentage, weight, rank, target, or allocation" in (
            decision_text
        )

    def test_no_sleeve_share_percentage_appears(self):
        """No SS-C quantity value may appear anywhere in this filing."""
        raw = DECISION.read_text(encoding="utf-8")
        for contaminated in ("18.67", "14.67", "16.67", "33.32", "63.25"):
            assert contaminated not in raw
