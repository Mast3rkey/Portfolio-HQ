"""Adversarial tests pinning the XASSET-0031 G3 share-of-the-whole determination.

XASSET-0031 determined ``SHARE_OF_THE_WHOLE_CONDITION_NOT_CLOSABLE``: the semantic condition a source
must satisfy to carry a Level-1 share of the whole **is** exactly statable from accepted authority, but
whether any construction satisfies it is expressly reserved by XASSET-0027 SS-J.3 and SS-M.3 and cannot
be closed by a governance unit.

These tests exist so that determination is **mechanically checkable rather than prose**. Every
reservation, criterion, and scope finding below is read from committed bytes; none is asserted from this
module's own opinion. The three positive sub-determinations are pinned the same way.

They also pin the *negative space* that makes the determination honest: that XASSET-0020 SS-E.1 is not
amended, that XASSET-0024 SS-K.1 is not resolved, that the XASSET-0030 6/6 gate partition is unchanged,
that G1 and G2 are not re-derived because no invalidation trigger fires, and that G5/G8/G9/G10/G12 are
untouched.

Nothing here arms, claims, completes, or executes Stage 1. Every candidate row is an isolated synthetic
fixture built in memory; no results document, lane directory, attestation, claim, completion, or ledger
entry is created or read for authorization purposes.
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
XASSET_0027 = (
    GOV / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
)
XASSET_0030 = GOV / "XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md"
DECISION = GOV / "XASSET-0031-endpoint-0001-stage-1-g3-share-of-the-whole-semantic-determination.md"


def _collapse(text: str) -> str:
    """Collapse Markdown hard-wrapping so a wrapped sentence matches as one string."""
    return re.sub(r"\s+", " ", text)


def _collapse_prose(text: str) -> str:
    """Like _collapse, but also strips Markdown blockquote markers.

    A wrapped `>` blockquote otherwise injects a stray `>` mid-sentence when collapsed, which would
    make a correct quotation fail to match for purely typographic reasons. Mirrors the helper in
    ``test_level1_stage1_gate_evaluation_determinism.py``.
    """
    stripped = "\n".join(line.lstrip().removeprefix(">").strip() for line in text.splitlines())
    return " ".join(stripped.split())


@pytest.fixture(scope="module")
def universe() -> dict:
    return CU.frozen_construction_universe()


@pytest.fixture(scope="module")
def decision_text() -> str:
    """Blockquote-safe, since several load-bearing statements are recorded as blockquotes."""
    return _collapse_prose(DECISION.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------------------
# The reproduction: what makes G3 ambiguous (XASSET-0031 SS-B)
# --------------------------------------------------------------------------------------


class TestG3AmbiguityReproduction:
    """SS-B. The exact ambiguity, reproduced from live frozen bytes rather than described."""

    R5_STIPULATION = "must be expressed against the normalized asset unit"

    def test_whole_denomination_is_stipulated_in_every_construction(self, universe):
        """SS-B.1. R5 is present in all 680 -- so any rule keyed on R5 is by-construction inference."""
        stipulating = [
            cid
            for cid, e in universe.items()
            if self.R5_STIPULATION in e["hypothetical_source_requirements"]
        ]
        assert len(stipulating) == len(universe) == 680

    def test_every_construction_is_hypothetical_so_no_denominator_can_be_inspected(self, universe):
        """SS-B.2. No source exists whose *declared* denominator could be read."""
        assert {e["source_architecture"] for e in universe.values()} == {
            "HYPOTHETICAL_SOURCE_ARCHITECTURE"
        }

    def test_each_driver_class_has_exactly_one_native_scope_and_none_is_the_whole(self, universe):
        """SS-B.3. SELF / PAIR / ALT -- no class carries a whole-portfolio scope."""
        scopes: dict[str, set[str]] = {}
        for cid, entry in universe.items():
            tag = cid.split("::")[-1].split("__")[0]
            scopes.setdefault(entry["driver_class"], set()).add(tag)

        assert scopes == {
            "portfolio_function": {"SELF"},
            "sleeve_deployability": {"SELF"},
            "diversification_cobehavior": {"PAIR"},
            "downside_path_risk": {"ALT"},
            "recovery": {"ALT"},
            "valuation_opportunity_cost": {"ALT"},
        }
        assert "WHOLE" not in {tag for tags in scopes.values() for tag in tags}

    def test_native_scope_counts_match_the_recorded_table(self, universe):
        counts = {"SELF": 0, "PAIR": 0, "ALT": 0}
        for cid in universe:
            counts[cid.split("::")[-1].split("__")[0]] += 1
        assert counts == {"SELF": 80, "PAIR": 120, "ALT": 480}

    def test_frozen_universe_carries_no_gate_outcome_for_g3_or_anything_else(self, universe):
        """SS-B.4. Ten identity fields; nothing that decides a gate."""
        observed: set[str] = set()
        for entry in universe.values():
            observed |= set(entry)
        assert observed == {
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
        assert not any("G3" in key for key in observed)

    def test_subject_matter_and_denominator_requirements_genuinely_coexist(self, universe):
        """SS-B.5. R3 (sleeve/pair/comparison scope) and R5 (whole denominator) in the same spec."""
        sample = universe["equity::LOWER::portfolio_function::R1_C1::SELF"]
        req = sample["hypothetical_source_requirements"]
        assert "R3. Its subject matter must be the equity sleeve's own portfolio_function evidence."in req
        assert self.R5_STIPULATION in req


# --------------------------------------------------------------------------------------
# The canonical G3 gate is a denominator-identity test (XASSET-0031 SS-C.1)
# --------------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def g3_gate() -> dict:
    """The canonical G3 gate record, located by id rather than by index."""
    data = yaml.safe_load(PREREG.read_text(encoding="utf-8"))

    def walk(node):
        if isinstance(node, dict):
            if node.get("gate_id") == "G3_NORMALIZATION":
                yield node
            for value in node.values():
                yield from walk(value)
        elif isinstance(node, list):
            for item in node:
                yield from walk(item)

    found = list(walk(data))
    assert len(found) == 1
    return found[0]


class TestG3IsADenominatorIdentityTest:
    def test_g3_asks_which_denominator_the_candidate_would_state(self, g3_gate):
        question = _collapse(g3_gate["question"])
        assert "share of one normalized unit of prospective unlevered asset-side capital" in question
        assert "rather than a quantity in the sleeve's own, within-instrument, market, per-share, or" in question

    def test_g3_controlling_authority_is_the_wrong_quantity_limb(self, g3_gate):
        """G3 maps to XASSET-0024 SS-F Limb 1 -- the wrong-quantity limb, i.e. T1."""
        assert g3_gate["controlling_authority"] == "XASSET-0024_SECTION_C_AND_SECTION_F_LIMB_1"
        assert g3_gate["failure_disposition"] == "BLOCKED_CATEGORICALLY"

    def test_protocol_enumerates_the_wrong_denominators(self):
        protocol = _collapse(PROTOCOL.read_text(encoding="utf-8"))
        assert (
            "A candidate that can only produce a sleeve-internal, within-fund, market-share, "
            "per-share, or leverage-bearing quantity fails there" in protocol
        )


# --------------------------------------------------------------------------------------
# The express reservations that make G3 not closable (XASSET-0031 SS-A)
# --------------------------------------------------------------------------------------


class TestG3IsExpresslyReserved:
    def test_j3_reserves_whether_portfolio_function_suffices(self):
        text = _collapse(XASSET_0027.read_text(encoding="utf-8"))
        assert "Whether that suffices to carry a share-of-the-whole statement is what `G3` tests." in text

    def test_m3_forbids_assuming_no_bridge_exists(self):
        text = _collapse(XASSET_0027.read_text(encoding="utf-8"))
        assert "it does not determine that no bridge exists" in text
        assert "the answer is a finding of the study rather than an assumption of the charter" in text

    def test_j1_states_the_scope_mismatch_and_bars_every_mapping(self):
        text = _collapse(XASSET_0027.read_text(encoding="utf-8"))
        assert (
            "Every one of `XASSET-0020` §E.1's six DRIVER classes is defined on a sleeve or on a "
            "comparison; the endpoint is a share **of the whole**." in text
        )
        assert "every mapping anyone would reach for is already barred by name" in text

    def test_decision_selects_the_negative_outcome(self, decision_text):
        assert "SHARE_OF_THE_WHOLE_CONDITION_NOT_CLOSABLE" in decision_text
        assert "The answer is NEGATIVE" in decision_text

    def test_decision_does_not_claim_g3_passes_or_fails_for_any_construction(self, decision_text):
        assert "evaluates `G3` or any other gate for no construction" in decision_text
        for forbidden in ("G3 → PASS", "G3 → FAIL", "`G3` → `PASS`", "`G3` → `FAIL`"):
            assert forbidden not in decision_text


# --------------------------------------------------------------------------------------
# The three positive sub-determinations (XASSET-0031 SS-C)
# --------------------------------------------------------------------------------------


class TestPositiveSubDeterminations:
    def test_c1_condition_requires_the_source_to_fix_the_denominator(self, decision_text):
        assert (
            "the `XASSET-0024` §C denominator — one normalized unit of prospective, unlevered, "
            "asset-side capital — is fixed by the source's own governed content" in decision_text
        )
        assert (
            "**supplied, chosen, composed, selected, or invented by a downstream reader** is not the "
            "§C denominator" in decision_text
        )

    def test_c1_admits_both_routes_via_t1s_own_disjunction(self, decision_text):
        """T1 reads 'states OR source-prescribes'; C.1 must not collapse that to R1 alone."""
        assert "either **stated** by the source itself" in decision_text
        assert "or produced by the source's **own complete prescribed derivation** (R2)" in decision_text
        assert "T1's own disjunction is load-bearing and is preserved here" in decision_text

    def test_c1_is_grounded_in_the_t1_criterion_text(self):
        """T1's disqualifier is the operative rule: any other quantity, however expressed."""
        text = _collapse(XASSET_0025.read_text(encoding="utf-8"))
        assert "**Right quantity** — states or source-prescribes a value for the §C quantity" in text
        assert "Any other quantity, however expressed as a percentage" in text

    def test_c1_is_grounded_in_the_risk_t1_failure_mode(self):
        """RISK magnitudes fail T1 because the denominator is unspecified BY THE SOURCE."""
        text = _collapse(XASSET_0025.read_text(encoding="utf-8"))
        assert "denominator is unspecified **by the source itself**" in text

    def test_c2_bars_downstream_authored_normalization(self, decision_text):
        assert (
            "No transformation of `portfolio_function`, `valuation_opportunity_cost`, "
            "`downside_path_risk`, `recovery`, `diversification_cobehavior`, or "
            "`sleeve_deployability` content into a portfolio percentage may be **composed, selected, "
            "invented, tuned, or completed** at application or Stage-1 time" in decision_text
        )

    def test_c2_states_the_boundary_is_authorship_not_execution_locus(self, decision_text):
        assert "The boundary is authorship, not execution locus." in decision_text
        assert (
            "Every one of those invalidators is an act of authorship or choice. None of them is the "
            "physical act of computing." in decision_text
        )

    def test_c2_preserves_no_third_route(self, decision_text):
        assert '"There is no third route"' in decision_text
        assert "Both are preserved exactly." in decision_text
        assert (
            "does not convert a lawful R2 into a third route" in decision_text
        )

    def test_c3_competent_authority_does_not_satisfy_g3(self, decision_text):
        assert (
            "Competent Level-1 endpoint authority therefore does not, and cannot, satisfy `G3`"
            in decision_text
        )

    def test_c3_is_grounded_in_the_committed_t1_versus_t5_distinction(self):
        text = _collapse(XASSET_0025.read_text(encoding="utf-8"))
        assert (
            "which are properties of what the evidence measures, not of who may certify it" in text
        )


# --------------------------------------------------------------------------------------
# R2 authorship vs execution (XASSET-0031 SS-C.2 limbs A/B, SS-E) -- review 4947565573 MAJOR 1
# --------------------------------------------------------------------------------------


class TestR2AuthorshipVersusExecution:
    """The six cases the corrected SS-C.2 must distinguish.

    Cases 1, 2 and 4 must be rejected as authorship or free choice; cases 3 and 5 must not be
    barred *merely* because the executor runs the arithmetic; case 6 must confirm no third route
    was created. None of these establishes that any R2 construction clears G3.
    """

    def test_case1_application_invented_formula_is_barred(self, decision_text):
        """An application-authored normalization formula is limb A."""
        limb_a = decision_text.split("**A — BARRED:")[1].split("**B —")[0]
        assert "**composed, selected, invented, tuned, or completed**" in limb_a
        assert "the application itself supplies" in limb_a
        assert "a new portfolio model" in limb_a

    def test_case2_application_selecting_among_formulas_is_barred(self):
        """XASSET-0024 SS-D bars a SELECTED derivation, not only an invented one."""
        text = _collapse(XASSET_0024.read_text(encoding="utf-8"))
        assert "Any composed, selected, or invented derivation (that is authorship" in text

    def test_case3_source_prescribed_derivation_is_not_barred_by_execution_locus(
        self, decision_text
    ):
        """The corrected limb B: prescription upstream, arithmetic may run downstream."""
        limb_b = decision_text.split("**B — NOT CATEGORICALLY BARRED:")[1].split(
            "**The operative test"
        )[0]
        assert "the application may **execute** that derivation" in limb_b
        assert "Execution is not authorship." in limb_b
        assert "That the arithmetic physically runs downstream does not convert a lawful R2" in limb_b

    def test_case3_requires_the_prescription_to_be_complete_and_choice_free(self, decision_text):
        limb_b = decision_text.split("**B — NOT CATEGORICALLY BARRED:")[1].split(
            "**The operative test"
        )[0]
        assert "prescribes the **complete** derivation" in limb_b
        assert "its inputs, its operations, its ordering, and the §C quantity and denominator" in limb_b
        assert "**zero free choice**" in limb_b

    def test_case4_tunable_coefficient_or_free_choice_is_rejected(self, decision_text):
        """SS-H.3 item 7 is named as the operative control, and quoted."""
        assert (
            "if any step could have been chosen differently without violating the source's own "
            "prescription, it is a model parameter and the derivation fails" in decision_text
        )
        assert "a derivation that does not is authorship no matter where it runs" in decision_text

    def test_case4_control_is_grounded_in_committed_authority(self):
        text = _collapse(XASSET_0024.read_text(encoding="utf-8"))
        assert "any tunable coefficient, ordering, tolerance, cutoff, or selection" in text
        assert "§H.3 item 7's test is the control" in text

    def test_case5_mechanical_execution_is_consistent_with_r2_in_the_route_table(
        self, decision_text
    ):
        """The SS-E table must state where the arithmetic may run, per route."""
        assert "| Route | Who fixes the §C denominator | Where the arithmetic may run |" in decision_text
        table = decision_text.split("| Route | Who fixes the §C denominator |")[1].split(
            "**Neither route is a"
        )[0]
        r2_row = [r for r in table.split("|\n") if "**R2** — uniquely derived" in r]
        assert r2_row
        assert "**Downstream execution is permitted**" in r2_row[0]
        assert "it executes, never composes, selects, tunes, or completes" in r2_row[0]

    def test_case5_r1_row_still_has_no_arithmetic(self, decision_text):
        table = decision_text.split("| Route | Who fixes the §C denominator |")[1].split(
            "**Neither route is a"
        )[0]
        r1_row = [r for r in table.split("|\n") if "**R1** — uniquely stated" in r]
        assert r1_row
        assert "there is no arithmetic to run" in r1_row[0]

    def test_case6_no_third_route_is_created(self, decision_text):
        assert "does not convert a lawful R2 into a third route" in decision_text
        assert "Nothing about R2 requires the arithmetic itself to have been performed upstream" in decision_text

    def test_j1_barred_list_is_not_evidence_against_limb_b(self, decision_text):
        """SS-J.1's mappings are barred because the APPLICATION would choose them."""
        assert (
            "Each is barred because the application would be choosing it" in decision_text
            and "so §J.1's list is not evidence against limb B" in decision_text
        )

    def test_correction_grants_nothing_about_g3(self, decision_text):
        """The widened R2 reading must not become a G3 finding."""
        assert (
            "This does not establish that any R2 construction actually satisfies `G3`."
            in decision_text
        )
        assert (
            "no finding here is that any of the 136 registered `R2_C2` constructions clears `G3`"
            in decision_text
        )

    def test_r2_c2_family_count_is_real(self, universe):
        """The 136 figure cited in SS-E is read from the frozen universe, not asserted."""
        assert sum(1 for e in universe.values() if e["family_id"] == "R2_C2") == 136


# --------------------------------------------------------------------------------------
# Per-class capability, and the refusal to flatten it (XASSET-0031 SS-D)
# --------------------------------------------------------------------------------------


class TestPerClassCapability:
    SIX_CLASSES = (
        "portfolio_function",
        "valuation_opportunity_cost",
        "downside_path_risk",
        "recovery",
        "diversification_cobehavior",
        "sleeve_deployability",
    )

    def test_all_six_classes_are_analyzed_separately(self, decision_text):
        for cls in self.SIX_CLASSES:
            assert f"`{cls}`" in decision_text

    def test_universe_carries_exactly_these_six_classes(self, universe):
        assert {e["driver_class"] for e in universe.values()} == set(self.SIX_CLASSES)

    def test_e1_is_an_admission_rule_not_a_realization_finding(self):
        """SS-E.1 says the classes MAY SUPPORT preference -- eligibility, not a determination."""
        text = _collapse(XASSET_0020.read_text(encoding="utf-8"))
        assert (
            "Only these closed driver classes may support positive or negative economic allocation "
            "preference" in text
        )
        # The word that carries the whole distinction.
        assert "may support" in text

    def test_direction_is_recorded_permitted_not_class_wide_realized(self, decision_text):
        assert "Level 2 (direction) is class-wide PERMITTED — not class-wide realized." in decision_text
        assert "It does not determine that every class, every source, or every admitted item" in decision_text
        assert "a result, not a class attribute" in decision_text

    def test_capability_table_says_permitted_source_result_dependent_for_every_class(
        self, decision_text
    ):
        table = decision_text.split("| # | DRIVER class |")[1].split("**Level 1 (subject matter)")[0]
        assert table.count("**PERMITTED** (source/result-dependent)") == 6
        # The overclaimed bare-YES direction cell must be gone from the direction column.
        for cls in self.SIX_CLASSES:
            row = [r for r in table.split("|\n") if f"`{cls}`" in r]
            assert row, cls
            assert "**PERMITTED** (source/result-dependent)" in row[0]

    @pytest.mark.parametrize(
        "value,is_direction",
        [
            ("self_preferred", True),
            ("counterpart_preferred", True),
            ("indistinguishable", False),
            ("unable_to_determine", False),
        ],
    )
    def test_only_two_of_the_four_pair_values_are_directions(
        self, decision_text, value, is_direction
    ):
        """The semantic distinction, not mere vocabulary presence."""
        per_value = decision_text.split("| §H value | What it is |")[1].split(
            "**Two of the four are therefore non-directional"
        )[0]
        row = [r for r in per_value.split("|\n") if f"`{value}`" in r]
        assert row, value
        if is_direction:
            assert "a **direction**" in row[0]
        else:
            assert "**not a direction**" in row[0]

    def test_the_two_non_directional_outcomes_are_preserved_by_name(self, decision_text):
        assert "Two of the four are therefore non-directional outcomes" in decision_text
        assert "a determinate **tie**" in decision_text
        assert "preserved **uncertainty**" in decision_text

    def test_the_surviving_claim_is_magnitude_freedom_not_universal_direction(self, decision_text):
        assert (
            "none of the four carries a magnitude" in decision_text
            and "every value is qualitative" in decision_text
        )

    def test_sect_h_condition_table_grounds_the_non_directional_readings(self):
        """indistinguishable = determinate tie; unable_to_determine = unclosed state."""
        text = _collapse(XASSET_0020.read_text(encoding="utf-8"))
        assert (
            "At least one driver is applicable; every applicable driver is `indistinguishable`" in text
        )
        assert (
            "Any contrary directions, required missingness, staleness, conflict, failed "
            "representation gate, or other unclosed state | `unable_to_determine` |" in text
        )

    def test_portfolio_function_is_the_only_portfolio_framed_class(self):
        """The SS-E.1 scope language, read from committed bytes rather than asserted."""
        text = _collapse(XASSET_0020.read_text(encoding="utf-8"))
        assert (
            "`portfolio_function` — the sleeve's directly evidenced job in the prospective portfolio"
            in text
        )
        for other in ("valuation_opportunity_cost", "downside_path_risk", "recovery"):
            marker = f"`{other}` — "
            assert marker in text

    def test_portfolio_function_observation_is_carried_forward_not_converted(self, decision_text):
        """SS-J.3's observation must stay an observation -- never a class-wide G3 disposition."""
        assert "as a fact and not as a prediction" in decision_text
        assert "RESERVED — §J.3 names this class specifically" in decision_text

    def test_capability_is_recorded_source_dependent_not_class_wide(self, decision_text):
        assert "Why the reserved answer is source-dependent and not class-wide" in decision_text
        assert (
            "Recording a class-wide `G3` disposition would therefore assert something about sources "
            "that the class does not determine" in decision_text
        )

    def test_no_class_is_recorded_as_clearing_g3(self, decision_text):
        """Every level-4 cell is RESERVED; none is YES."""
        table = decision_text.split("Level 1 (subject matter) is class-wide YES")[0]
        row_region = table.split("| # | DRIVER class |")[1]
        assert row_region.count("RESERVED") >= 6

    def test_sleeve_deployability_g5_overlap_is_named_but_not_entered(self, decision_text):
        assert "additionally contested at `G5`" in decision_text
        assert "This filing takes no position on `G5` for that class or any other" in decision_text


# --------------------------------------------------------------------------------------
# Native scope does not decide G3 (XASSET-0031 SS-D) -- DELTA review 4947665744 MAJOR 1
# --------------------------------------------------------------------------------------


class TestNativeScopeDoesNotDecideG3:
    """The stale mirror this correction removed, pinned so it cannot return.

    The prior head said of the five non-portfolio-framed classes that "reaching the whole from any of
    them would require precisely the mapping SS-C.2 bars" -- a class-wide negative that contradicted
    the corrected SS-C.2 limb B and the SS-E R2 row. Native scope is an observation about subject
    matter; it decides nothing about G3 either way.
    """

    NON_PORTFOLIO_FRAMED = (
        "valuation_opportunity_cost",
        "downside_path_risk",
        "recovery",
        "diversification_cobehavior",
        "sleeve_deployability",
    )

    def _five_class_bullet(self, decision_text: str) -> str:
        return decision_text.split("**The other five carry no portfolio-framed scope language at all.**")[
            1
        ].split("**Why the reserved answer is source-dependent")[0]

    def test1_native_scope_does_not_itself_imply_g3_impossible(self, decision_text):
        bullet = self._five_class_bullet(decision_text)
        assert (
            "That observation is about native scope only, and does not by itself decide `G3` for any "
            "of them." in bullet
        )
        assert "Neither satisfaction nor impossibility is determined here for any class." in bullet

    STALE = "Reaching the whole from any of them would require precisely the mapping"

    def test1_the_removed_class_wide_negative_survives_only_as_history(self, decision_text):
        """The stale formulation must appear exactly once, inside the correction record.

        Stricter than a bare absence check: the phrase is legitimately quoted where correction 2
        documents what it removed, so this pins BOTH that it is quoted there AND that it is nowhere
        else -- in particular, nowhere in SS-D's live body.
        """
        assert decision_text.count(self.STALE) == 1
        i = decision_text.find(self.STALE)
        context = decision_text[max(0, i - 400) : i]
        assert "**Correction 2**" in context or "**MAJOR 1** — §D's five-class bullet" in context

    def test1_the_stale_claim_is_absent_from_the_live_five_class_bullet(self, decision_text):
        bullet = self._five_class_bullet(decision_text)
        assert self.STALE not in bullet
        assert "§C.2 bars" not in bullet

    def test2_five_class_source_may_reach_the_quantity_via_r1_or_prescribed_r2(self, decision_text):
        bullet = self._five_class_bullet(decision_text)
        assert "reaches the §C quantity only by satisfying §C.1 on its own terms" in bullet
        assert "R1's direct statement" in bullet
        assert "complete, zero-free-choice, source-prescribed R2 derivation that yields it" in bullet

    def test3_application_authored_conversion_remains_barred(self, decision_text):
        bullet = self._five_class_bullet(decision_text)
        assert (
            "any conversion the application would compose, select, invent, or tune remains barred by "
            "§C.2 limb A" in bullet
        )

    def test4_source_prescribed_r2_execution_remains_permitted_in_principle(self, decision_text):
        """The SS-C.2/SS-E permission must still stand after this correction."""
        assert "**B — NOT CATEGORICALLY BARRED:" in decision_text
        assert "**Downstream execution is permitted**" in decision_text

    def test5_no_class_wide_g3_pass_or_fail_is_introduced(self, decision_text):
        """Every level-4 cell stays RESERVED; no class is recorded as clearing or failing G3."""
        table = decision_text.split("| # | DRIVER class |")[1].split("**Level 1 (subject matter)")[0]
        assert table.count("RESERVED") >= 6
        for verdict in ("**PASS**", "**FAIL**", "G3 PASS", "G3 FAIL"):
            assert verdict not in table

    def test5_no_class_is_declared_incapable(self, decision_text):
        for phrase in ("can never reach", "cannot reach the whole", "never reach the whole"):
            assert phrase not in decision_text

    def test6_portfolio_function_remains_separately_reserved_under_j3(self, decision_text):
        assert "RESERVED — §J.3 names this class specifically" in decision_text
        assert "Whether that suffices to carry a share-of-the-whole statement is what `G3` tests." in decision_text

    @pytest.mark.parametrize("cls", NON_PORTFOLIO_FRAMED)
    def test7_all_five_remain_source_dependent_at_g3(self, decision_text, cls):
        table = decision_text.split("| # | DRIVER class |")[1].split("**Level 1 (subject matter)")[0]
        row = [r for r in table.split("|\n") if f"`{cls}`" in r]
        assert row, cls
        assert "RESERVED" in row[0]
        assert "source-dependent" in row[0]

    def test7_capability_is_still_recorded_source_dependent_not_class_wide(self, decision_text):
        assert "Why the reserved answer is source-dependent and not class-wide" in decision_text

    def test8_gate_map_unchanged_by_this_correction(self, decision_text):
        assert (
            "The `CURRENT_AUTHORITY_GATE_EVALUATION_SNAPSHOT` stands exactly as `XASSET-0030` §E left it"
            in decision_text
        )
        assert "`G3` remains not closable" in decision_text
        assert "SHARE_OF_THE_WHOLE_CONDITION_NOT_CLOSABLE" in decision_text

    def test_native_scope_facts_themselves_are_preserved(self, decision_text, universe):
        """The valid observation survives: SELF/PAIR/ALT, no class whole-scoped."""
        bullet = self._five_class_bullet(decision_text)
        assert "Their native subject matter is `SELF`, `PAIR`, or `ALT`" in bullet
        assert "not the whole" in bullet
        # And it is still true of the frozen universe.
        tags = {cid.split("::")[-1].split("__")[0] for cid in universe}
        assert tags == {"SELF", "PAIR", "ALT"}


# --------------------------------------------------------------------------------------
# SS-K.1 preserved, and shown non-dispositive (XASSET-0031 SS-F)
# --------------------------------------------------------------------------------------


class TestKOneTreatment:
    def test_k1_is_neither_resolved_nor_relied_upon(self, decision_text):
        assert "This filing adopts neither §K.1 reading" in decision_text
        assert "resolves `XASSET-0024` §K.1 neither way" in decision_text

    def test_both_readings_are_stated_with_their_effect_on_g3(self, decision_text):
        assert "**Subject-matter** (operative for `XASSET-0024` Outcome A)" in decision_text
        assert "**Preference-only** (contrary, preserved)" in decision_text
        assert "**`G3` remains open.**" in decision_text
        assert "**`G3` is never reached as an independent question.**" in decision_text

    def test_k1_is_recorded_as_not_dispositive_of_g3(self, decision_text):
        assert "§K.1 is not dispositive of `G3` in either direction" in decision_text

    def test_t1_and_t2_are_separate_criteria_in_committed_authority(self):
        """The basis for SS-F's reconciliation: T1 != T2 in XASSET-0025 SS-D."""
        text = _collapse(XASSET_0025.read_text(encoding="utf-8"))
        assert "| T1 | **Right quantity**" in text
        assert "| T2 | **Admitted subject matter**" in text

    def test_reconciliation_with_xasset_0030_does_not_contradict_it(self, decision_text):
        assert "Nothing in `XASSET-0030` is contradicted" in decision_text
        assert "its §G.A named a shape, not a sufficient text" in decision_text


# --------------------------------------------------------------------------------------
# SS-E.1 not amended, and the G1/G2 triggers verifiably do not fire (XASSET-0031 SS-G, SS-H)
# --------------------------------------------------------------------------------------


class TestSectionE1IsNotAmended:
    def test_decision_states_no_amendment(self, decision_text):
        assert (
            "This filing amends, clarifies, narrows, widens, or supersedes nothing in "
            "`XASSET-0020` §E.1." in decision_text
        )

    def test_xasset_0020_is_byte_unchanged_in_this_working_tree(self):
        import subprocess

        out = subprocess.run(
            ["git", "diff", "--name-only", "HEAD", "--", str(XASSET_0020.relative_to(ROOT))],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        assert out.stdout.strip() == ""

    def test_upstream_authorities_relied_on_are_byte_unchanged(self):
        import subprocess

        paths = [
            str(p.relative_to(ROOT))
            for p in (XASSET_0024, XASSET_0025, XASSET_0027, XASSET_0030, PREREG, PROTOCOL)
        ]
        out = subprocess.run(
            ["git", "diff", "--name-only", "HEAD", "--", *paths],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        assert out.stdout.strip() == ""

    def test_a_future_clarification_must_carry_two_properties_not_one(self, decision_text):
        assert "Magnitude housing (T2 / `G2`, §K.1's question)" in decision_text
        assert "Denominator scope (T1 / `G3`, this unit's question)" in decision_text
        assert "closing only the first leaves `G3` exactly where it is" in decision_text


class TestG1AndG2AreNotReDerived:
    """SS-H. Every XASSET-0030 SS-E.1 trigger is checked, and none fires."""

    def test_decision_checks_each_trigger_explicitly(self, decision_text):
        for trigger in (
            "§E.1's classes or scope amended",
            "§D's subject-matter determination amended or superseded",
            "§M.1's routing changed / reading slot added to `G1`",
            "§K.1 resolved or amended",
            "§E.1 clarified so as to settle magnitude capability",
            "Reading map or `required_g2_gate_result` coupling changed",
            "Either pinned canonical hash changed",
        ):
            assert trigger in decision_text

    def test_no_trigger_fires(self, decision_text):
        assert "**No trigger fires, so `G1` and `G2` are not re-derived" in decision_text

    def test_magnitude_capability_is_left_open_for_all_six_classes(self, decision_text):
        assert "Level 3 recorded **OPEN** for all six classes" in decision_text

    def test_canonical_hashes_match_the_effective_pins(self):
        """AMENDED BY XASSET-0036 SS-E.1/SS-E.7.

        This filing changed no canonical byte and neither re-derived G1 nor G2. The implementation
        XASSET-0036 later authorized amended the canonical artifacts and recomputed the pins, so
        the literals asserted here are XASSET-0029's and are now checked as history.
        """
        import hashlib

        assert (
            A.XASSET_0029_CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH]
            == "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
        )
        assert (
            A.XASSET_0029_CANONICAL_PINS[A.CANONICAL_PREREGISTRATION_RELPATH]
            == "6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c"
        )
        assert (
            hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
            == A.CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH]
        )
        assert (
            hashlib.sha256(PREREG.read_bytes()).hexdigest()
            == A.CANONICAL_PINS[A.CANONICAL_PREREGISTRATION_RELPATH]
        )


# --------------------------------------------------------------------------------------
# The gate map is unchanged, and the other five reserved gates are untouched
# --------------------------------------------------------------------------------------


class TestGateMapUnchanged:
    CLOSABLE = ("G1", "G2", "G4", "G6", "G7", "G11")
    NOT_CLOSABLE = ("G3", "G5", "G8", "G9", "G10", "G12")

    def test_partition_is_restated_unchanged(self, decision_text):
        assert "The `CURRENT_AUTHORITY_GATE_EVALUATION_SNAPSHOT` stands exactly as `XASSET-0030` §E left it" in decision_text
        assert len(self.CLOSABLE) == len(self.NOT_CLOSABLE) == 6

    def test_g3_remains_not_closable_and_independently_sufficient(self, decision_text):
        assert "`G3` remains not closable" in decision_text
        assert "remains independently sufficient" in decision_text

    def test_other_reserved_gates_are_explicitly_untouched(self, decision_text):
        assert (
            "`G5`, `G8`, `G9`, `G10`, and `G12` are **untouched** — this unit examined none of them "
            "and determines nothing about any of them." in decision_text
        )

    def test_decision_determines_nothing_about_the_other_five(self, decision_text):
        assert "determines nothing about `G5`, `G8`, `G9`, `G10`, or `G12`" in decision_text


# --------------------------------------------------------------------------------------
# Adversarial cases: the rule must fail closed on outcome-determining discretion
# --------------------------------------------------------------------------------------


class TestAdversarialCases:
    """Each case is the inference the SS-C.1/SS-C.2 rule must refuse."""

    @pytest.mark.parametrize(
        "wrong_denominator",
        [
            "sleeve-internal",
            "within-fund",
            "market-share",
            "per-share",
            "leverage-bearing",
        ],
    )
    def test_named_wrong_denominators_are_barred_by_the_protocol(self, wrong_denominator):
        """Cases 1-2: strong evidence in the wrong denominator never becomes a share."""
        protocol = _collapse(PROTOCOL.read_text(encoding="utf-8"))
        assert wrong_denominator in protocol

    def test_a_share_figure_alone_does_not_confer_driver_status(self):
        """Case 3: a source with a number but no subject-matter claim fails SS-E.1."""
        text = _collapse(XASSET_0024.read_text(encoding="utf-8"))
        assert (
            "A source whose only claim to DRIVER status is that it contains a share figure does not "
            "satisfy §E.1." in text
        )

    def test_competent_authority_alone_does_not_close_g3(self, decision_text):
        """Case 4 inverted: the most plausible false close is named and refused."""
        assert (
            "A future filing that attempted to close `G3` by constituting an authority competent for "
            "Level-1 shares would be answering T5 and leaving T1 exactly where it is." in decision_text
        )

    def test_unregistered_coefficient_fails_the_free_choice_test(self, decision_text):
        """Case 5: any tunable step is a model parameter."""
        assert "free-choice test" in decision_text
        assert "Any such step is a new portfolio model" in decision_text

    @pytest.mark.parametrize(
        "barred",
        [
            "midpoint",
            "symmetry or equal-division convention",
            "composite score",
            "residual plug",
            "default range width",
            "optimizer or grid search",
        ],
    )
    def test_midpoint_equal_weight_and_residual_derivations_are_barred_by_name(self, barred):
        """Case 6: every convenience derivation is already barred in committed authority."""
        text = _collapse(XASSET_0027.read_text(encoding="utf-8"))
        assert barred in text

    def test_endpoints_must_be_independently_governed_not_derived_from_each_other(self):
        """Cases 7-8: a lawful range needs two independent endpoints, never a justified midpoint."""
        text = _collapse(XASSET_0024.read_text(encoding="utf-8"))
        assert "independence is affirmatively required" in text
        assert "What is **not** permitted is deriving one bound from the other" in text

    def test_pair_evidence_cannot_become_an_absolute_portfolio_weight(self, decision_text):
        """Case 9: PAIR-scoped content is comparison-scoped; downstream-AUTHORED conversion is barred.

        Updated for the corrected SS-C.2 limb A wording (review 4947565573 MAJOR 1). The bar is on
        the application composing/selecting/inventing the conversion, not on execution locus.
        """
        assert "`PAIR` — \"direct … pair evidence for the unordered pair …\"" in decision_text
        assert (
            "content into a portfolio percentage may be **composed, selected, invented, tuned, or "
            "completed** at application or Stage-1 time" in decision_text
        )

    def test_representations_may_not_be_averaged(self):
        """Case 10: no majority, average, weighting, or representative selection."""
        text = _collapse(XASSET_0024.read_text(encoding="utf-8"))
        assert (
            "No majority, average, weighting, representative selection, or \"most conservative\" "
            "selection is permitted" in text
        )

    def test_deployability_constraint_shape_is_reserved_to_g5_not_answered_here(self, decision_text):
        """Case 11: deployability as a constraint is G5's question, and is not entered."""
        assert "`XASSET-0027` §M.4 reserves constraint-shape per candidate" in decision_text
        assert "§M.4 is untouched" in decision_text

    def test_both_k1_readings_are_given_an_explicit_g3_outcome(self, decision_text):
        """Case 12: the unresolved reading must not produce a silently different result."""
        assert "| §K.1 reading | Effect on `G2` | Effect on `G3` |" in decision_text

    def test_an_e1_amendment_would_have_fired_g1_and_g2_triggers(self, decision_text):
        """Case 13: the coupling is acknowledged, and avoided rather than ignored."""
        assert (
            "A filing that had reached the same substantive conclusions by editing §E.1 would have "
            "cost two re-derivations for no additional finding." in decision_text
        )

    @pytest.mark.parametrize("barred_value", ["18.67", "14.67", "16.67", "33.32"])
    def test_barred_historical_values_are_not_reintroduced_as_anchors(self, barred_value):
        """Case 14: no barred value appears anywhere in this unit's own text."""
        assert barred_value not in DECISION.read_text(encoding="utf-8")

    def test_source_dependent_capability_is_not_replaced_by_a_class_wide_answer(self, decision_text):
        """Case 15: the honest answer is recorded instead of an invented class-wide one."""
        assert "where it is source-dependent rather than class-wide that is recorded" in decision_text


# --------------------------------------------------------------------------------------
# By-construction inference remains rejected
# --------------------------------------------------------------------------------------


class TestByConstructionInferenceStillRejected:
    def test_standard_1_is_quoted_from_xasset_0030(self):
        text = _collapse(XASSET_0030.read_text(encoding="utf-8"))
        assert (
            "**(a) a specification requiring property P** is never by itself **(b) proof that P is "
            "lawfully satisfiable.**" in text
        )

    def test_decision_applies_standard_1_to_r5(self, decision_text):
        assert (
            "Deriving `PASS` from R5's own presence is by-construction inference" in decision_text
        )

    def test_decision_rejects_both_available_closures(self, decision_text):
        assert "Both available closures were tested and both fail." in decision_text


# --------------------------------------------------------------------------------------
# Nothing here authorizes, arms, or executes
# --------------------------------------------------------------------------------------


class TestNothingHereAuthorizesOrExecutes:
    def test_execution_remains_unauthorized(self):
        authorized, reason = A.new_execution_is_authorized()
        assert authorized is False
        assert "no attestation present" in reason

    def test_universe_identity_is_unchanged(self, universe):
        assert len(universe) == A.CONSTRUCTION_COUNT == 680
        assert len({e["cell_id"] for e in universe.values()}) == A.CONSTRUCTION_CELL_COUNT == 48
        assert (
            A.CONSTRUCTION_UNIVERSE_SHA256
            == "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
        )

    def test_no_stage1_results_document_exists(self):
        assert not (ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()
        assert not list((ROOT / "research/level1_endpoint_evidence").glob("**/stage1_results.yaml"))

    def test_this_decision_is_not_load_bearing_and_the_six_are_retained(self):
        """AMENDED BY XASSET-0036 SS-E.6.

        The property this filing was protecting -- that IT added nothing to the trust boundary --
        is preserved: its own decision file is still not load-bearing. SS-G.B step 5 later added
        exactly the outcome-producing paths, and the six this filing saw are all still present.
        """
        assert Path(DECISION).name not in A.LOAD_BEARING_RELPATHS
        for relative in (
            "level1_stage1_execution_authorization.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "level1_construction_universe_closure_validator.py",
            A.CANONICAL_PROTOCOL_RELPATH,
            A.CANONICAL_PREREGISTRATION_RELPATH,
            "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
        ):
            assert relative in A.LOAD_BEARING_RELPATHS

    def test_load_bearing_paths_are_byte_identical_to_head(self):
        """No load-bearing path may differ from ``HEAD`` in this working tree.

        RESTORED BY XASSET-0042 after review 4975556072 MINOR 1. An interim revision removed
        ``level1_stage1_execution_authorization.py`` from this comparison, on the reasoning
        that an authorized correction lawfully changes it. That was wrong in scope: the
        exemption was permanent and unconditional, so every future UNCOMMITTED, unauthorized
        edit to the most sensitive load-bearing path would have been invisible here --
        reproduced by appending a line to the module and watching this guard pass.

        The authorized correction is a COMMITTED change. At any committed head the working
        tree matches ``HEAD``, so all ten paths compare clean and no exemption is needed. The
        PR's own base->head delta is covered separately, by
        ``test_pr_delta_touches_only_the_one_authorized_load_bearing_path``, which is a
        different question and must not be answered by weakening this one.
        """
        import subprocess

        # EXTENDED BY XASSET-0044, 10 -> 14, by direct membership; nothing removed.
        # EXTENDED AGAIN BY XASSET-0047, 14 -> 16, likewise by direct membership and likewise
        # removing nothing. The byte-identity comparison below is the load-bearing check and is
        # unchanged in kind -- it still covers EVERY path in the live tuple, so it grows with it.
        # This count is bound at BOTH ends so neither a silent shrink back nor an unexplained
        # further growth passes.
        # EXTENDED AGAIN BY XASSET-0049, 16 -> 18, likewise by direct membership and likewise
        # removing nothing. Bound at BOTH ends for the third time, so neither a silent shrink
        # back to any earlier size nor an unexplained further growth passes.
        # RE-ANCHORED BY XASSET-0060, and STRENGTHENED rather than relaxed. XASSET-0057 §F.7
        # authorized ONE additive extension, 18 -> 25, adding the six decisions that authorized and
        # defined the formal-disposition parser plus the rebinding's own decision. The bare count
        # this line carried could not tell an authorized addition from a wholesale replacement of
        # equal length, so both ends are now bound: the eighteen this unit saw must still ALL be
        # present (nothing removed, swapped or traded away), and the live count is pinned EXACTLY
        # at 25 so a further silent addition still fails here.
        assert len(A.LOAD_BEARING_RELPATHS) == 25
        assert len(set(A.LOAD_BEARING_RELPATHS)) == 25
        assert len(A.LOAD_BEARING_RELPATHS) != 18
        assert len(A.LOAD_BEARING_RELPATHS) != 16
        assert len(A.LOAD_BEARING_RELPATHS) != 14
        out = subprocess.run(
            ["git", "diff", "--name-only", "HEAD", "--", *A.LOAD_BEARING_RELPATHS],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        assert out.stdout.strip() == ""

    def test_pr_delta_touches_only_the_one_authorized_load_bearing_path(self):
        """The committed base->head delta may change exactly ONE load-bearing path.

        Added alongside the restoration above, never in place of it. This asks about the
        PR's committed content; the guard above asks about the working tree. Both must hold.
        """
        import subprocess

        #: The only load-bearing path a merged, effective decision (XASSET-0041) authorizes
        #: this pull request to change.
        AUTHORIZED_CORRECTION_PATH = "level1_stage1_execution_authorization.py"
        assert AUTHORIZED_CORRECTION_PATH in A.LOAD_BEARING_RELPATHS

        # RE-ANCHORED BY XASSET-0044. This asks what XASSET-0042's OWN pull request changed, and
        # that pull request is merged and closed, so its delta is a CLOSED range: PR #342's base
        # through PR #342's merge. Computing `merge-base origin/main HEAD` instead re-scoped the
        # question to whatever branch happens to be checked out -- so any later, separately
        # authorized unit lawfully changing a load-bearing path would fail here, reporting a defect
        # in XASSET-0042 that XASSET-0042 did not commit. Immutable, and evaluated over the ten
        # paths XASSET-0042 itself bound rather than a set a later generation grew.
        CORRECTION_BASE = "9c8647f9dddacdf63825f569097214ba65299fe8"
        CORRECTION_MERGE = "5fbfc94d7333e552bd2654261e0c57134a172e31"
        for commit in (CORRECTION_BASE, CORRECTION_MERGE):
            probe = subprocess.run(
                ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
                cwd=ROOT, capture_output=True,
            )
            if probe.returncode != 0:
                pytest.skip(f"{commit} is unavailable in this checkout")
        # The boundary AS XASSET-0042 BOUND IT -- ten paths, read from the module at that merge.
        # Using the LIVE set would be wrong in kind, not just in size: XASSET-0044 later made
        # XASSET-0042's OWN decision file load-bearing, so the live set retroactively re-scopes a
        # question about what XASSET-0042 was allowed to touch.
        import ast as _ast

        module_source = subprocess.run(
            ["git", "show", f"{CORRECTION_MERGE}:level1_stage1_execution_authorization.py"],
            cwd=ROOT, capture_output=True, check=False,
        )
        if module_source.returncode != 0:
            pytest.skip("the correction merge's module is unavailable in this checkout")
        tree = _ast.parse(module_source.stdout.decode("utf-8"))
        literals: dict[str, str] = {}
        bound_paths: list[str] | None = None
        for node in tree.body:
            if not isinstance(node, _ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, _ast.Name):
                continue
            if isinstance(node.value, _ast.Constant) and isinstance(node.value.value, str):
                literals[target.id] = node.value.value
            elif target.id == "LOAD_BEARING_RELPATHS" and isinstance(node.value, _ast.Tuple):
                bound_paths = [
                    element.value if isinstance(element, _ast.Constant)
                    else literals[element.id]
                    for element in node.value.elts
                ]
        assert bound_paths is not None and len(bound_paths) == 10
        assert AUTHORIZED_CORRECTION_PATH in bound_paths

        out = subprocess.run(
            ["git", "diff", "--name-only", CORRECTION_BASE, CORRECTION_MERGE,
             "--", *bound_paths],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        changed = [line for line in out.stdout.split("\n") if line.strip()]
        assert changed in ([], [AUTHORIZED_CORRECTION_PATH]), (
            f"the delta changes load-bearing paths beyond the one authorized: {changed}"
        )

    def test_decision_carries_the_absolute_non_authorization(self, decision_text):
        for clause in (
            "generates no `XASSET-0029` attestation",
            "consumes nothing of `ATTEMPT_1`",
            "creates no Stage-1 runner and no `stage1_results.yaml`",
            "introduces no consequential numeric parameter",
            "accesses no protected RISK results path",
        ):
            assert clause in decision_text

    def test_this_module_creates_no_lane_or_results_artifact(self):
        assert not (ROOT / "research/level1_endpoint_evidence/attempts").exists()
