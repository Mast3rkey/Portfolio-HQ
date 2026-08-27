"""Supporting artifact for ``XASSET-0059`` -- the Lifecycle B parser correction.

``XASSET-0058`` decided the formal-disposition recognition boundary and authorized **exactly
one** future implementation unit to build it. This module is that unit's proof.

It proves, mechanically rather than by assertion:

* the **whole** exhaustive printable-ASCII mutation matrix is closed by the REAL corrected
  ``parse_formal_disposition`` -- every family, every position, every character, in all three
  governed presentations, with the **colon cells** exercised independently and by name;
* **acceptance is unchanged** in every direction, and the open verdict vocabulary and
  whole-verdict exact equality survive untouched;
* **ordinary prose stays ABSENT**, and the ``§D.8`` terminating-colon residual is preserved
  exactly as the decision expressly reserved it;
* every real **historical lifecycle review body** retains its exact verdict;
* every resulting ``MALFORMED`` is refused at **all three real consumer seams**, in both native
  states, and a native ``APPROVED`` cannot rescue any of them;
* the candidate mechanism **cannot return or create a verdict** -- proved structurally, not hoped;
* and every guard here is **falsifiable**: the mutation harness at the end removes each one and
  requires the suite to notice, restoring every file byte-identically afterwards.

Counts are **derived from the iterated mappings**. No family total, seam total or control total
is a separately maintained literal, so a matrix that silently shrinks fails rather than passing
with a stale number.
"""

from __future__ import annotations

import ast
import hashlib
import inspect
import subprocess
import time
from pathlib import Path

import pytest

import level1_stage1_execution_authorization as AUTH

#: The three REAL consumer seams, reused from the suite that already drives them against the
#: live module rather than re-implemented as a second, divergent harness.
import test_level1_stage1_formal_disposition_parser_correction as _SEAMS_MODULE

#: The exhaustive matrix ``XASSET-0058`` decided the boundary on. Imported ONLY to cross-check
#: this module's own independently derived matrix against it; never used in place of it.
import test_level1_stage1_formal_disposition_parser_correction_authorization as _DECIDED


class _SEAMS:
    """Thin, explicit binding to the real seam runners. No behaviour of its own."""

    run_consumer_one = staticmethod(_SEAMS_MODULE._run_consumer_one)
    run_consumer_two = staticmethod(_SEAMS_MODULE._run_consumer_two)
    run_consumer_three = staticmethod(_SEAMS_MODULE._run_consumer_three)


ROOT = Path(__file__).resolve().parent
MODULE_RELPATH = "level1_stage1_execution_authorization.py"
DECISION_RELPATH = (
    "governance/decisions/XASSET-0059-endpoint-0001-formal-disposition-parser-correction.md"
)
CATALOG = ROOT / "governance" / "decisions.yaml"
WORKSTREAMS = ROOT / "operations" / "WORKSTREAMS.yaml"

# =====================================================================================
# Immutable identities
# =====================================================================================

#: This unit's base: the ``XASSET-0058`` authorization's own normal-merge commit. ``§G.2``
#: requires the implementation to base EXACTLY here.
AUTHORIZATION_MERGE_SHA = "34c45900ce23742d04d80cf12471c34aabe9682d"
AUTHORIZATION_MERGE_TREE = "76e1021499464f4c2152d9e55c0d03b5ea14708c"
AUTHORIZATION_ACCEPTED_HEAD = "e8d53c184a7612ab6e38ba8d7ae1e348f7046de2"
AUTHORIZATION_MERGE_PARENTS = (
    "556a43cf91679d3e8ca95703c8d49e672b662b73",
    "e8d53c184a7612ab6e38ba8d7ae1e348f7046de2",
)

#: ``XASSET-0057 §F.3`` **role 2** -- the vulnerable intermediate. A PERMANENT NEGATIVE PIN:
#: adverse history, never a bound end, never rebound or repaired by this unit (``§G.3``).
VULNERABLE_MODULE_SHA256 = (
    "12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5"
)

#: The paths ``XASSET-0058 §H`` forbids this unit to touch. The production module is DELIBERATELY
#: absent: it is the ONE surface ``§F.1`` authorizes, and pinning it here would forbid the
#: correction itself.
PROTECTED_RELPATHS = (
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_construction_universe_closure_validator.py",
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
    "allocate.py",
    "margin_state.py",
    "levels.py",
)

PREFIX = AUTH.FORMAL_DISPOSITION_PREFIX
APPROVE = AUTH.APPROVING_REVIEW_DISPOSITION
ADVERSE_VERDICT = "CHANGES REQUIRED"

#: DERIVED, never assumed: the swept region is the canonical prefix minus its terminating colon.
CANON_LABEL = PREFIX[:-1]

#: Every printable ASCII character. A single handpicked representative is NOT sufficient
#: evidence for an ASCII family -- independent review ``5034171910`` found exactly that defect,
#: and the classifier's own delimiter is itself one of these characters.
PRINTABLE_ASCII = tuple(chr(code) for code in range(0x20, 0x7F))

#: Confusables whose uppercase form stays NON-ASCII -- the documented mechanism by which the
#: printable-ASCII projection DELETES them. Asserted below, never assumed.
CONFUSABLES = {
    "F": "Ƒ", "O": "Ο", "R": "Ｒ", "M": "М", "A": "А",
    "L": "Ⅼ", "D": "Ⅾ", "I": "İ", "S": "Ѕ", "P": "Р",
    "T": "Т", "N": "Ν",
}

NONSPACE_POSITIONS = tuple(i for i, c in enumerate(CANON_LABEL) if c != " ")
ADJACENT_PAIRS = tuple(
    i for i in range(len(CANON_LABEL) - 1) if CANON_LABEL[i] != CANON_LABEL[i + 1]
)

FAMILIES = (
    "deletion",
    "ascii_substitution",
    "ascii_insertion",
    "transposition",
    "confusable_substitution",
)


def _exhaustive() -> list[tuple[str, int, str, str]]:
    """Every single-character mutation of the label over the WHOLE printable-ASCII alphabet.

    Returns ``(family, position, character, mutated_label)``. THE sole source of every count in
    this module -- nothing below maintains a total of its own.
    """
    out: list[tuple[str, int, str, str]] = []
    for i in NONSPACE_POSITIONS:
        out.append(("deletion", i, "", CANON_LABEL[:i] + CANON_LABEL[i + 1:]))
    for i in NONSPACE_POSITIONS:
        for character in PRINTABLE_ASCII:
            if character != CANON_LABEL[i]:
                out.append((
                    "ascii_substitution", i, character,
                    CANON_LABEL[:i] + character + CANON_LABEL[i + 1:],
                ))
    for i in NONSPACE_POSITIONS:
        for character in PRINTABLE_ASCII:
            out.append((
                "ascii_insertion", i, character,
                CANON_LABEL[:i] + character + CANON_LABEL[i:],
            ))
    for i in ADJACENT_PAIRS:
        out.append((
            "transposition", i, "",
            CANON_LABEL[:i] + CANON_LABEL[i + 1] + CANON_LABEL[i] + CANON_LABEL[i + 2:],
        ))
    for i in NONSPACE_POSITIONS:
        out.append((
            "confusable_substitution", i, CONFUSABLES[CANON_LABEL[i]],
            CANON_LABEL[:i] + CONFUSABLES[CANON_LABEL[i]] + CANON_LABEL[i + 1:],
        ))
    return out


EXHAUSTIVE = _exhaustive()

#: Exactly the cells whose mutation character IS the classifier's own delimiter. These are the
#: cells the SUPERSEDED first-colon rule left fail-open, so they are load-bearing on their own
#: and are never allowed to hide inside a family total.
COLON_CELLS = [cell for cell in EXHAUSTIVE if cell[2] == ":"]

PLAIN, BOLD, INDENTED = "plain", "bold", "indented"
PRESENTATIONS = (PLAIN, BOLD, INDENTED)


def _render(label: str, form: str) -> str:
    """The three GOVERNED presentations, and no fourth."""
    if form == PLAIN:
        return f"{label}: {ADVERSE_VERDICT}"
    if form == BOLD:
        return f"**{label}: {ADVERSE_VERDICT}**"
    if form == INDENTED:
        return f"   {label}: {ADVERSE_VERDICT}"
    raise AssertionError(form)


def _adverse_then_approval(line: str) -> str:
    """An adverse FIRST formal line, then a canonical approval. A skip lets the approval win."""
    return f"{line}\n\n{PREFIX} {APPROVE}\n"


#: The three outcome classes. Only the third is unsafe.
SAFE_MALFORMED = "MALFORMED"
SAFE_ADVERSE = "ADVERSE"
UNSAFE_BYPASS = "BYPASS"


def _classify(line: str) -> str:
    """The REAL corrected parser's outcome for an adverse first line + a later approval."""
    result = AUTH.parse_formal_disposition(_adverse_then_approval(line))
    if result is AUTH.MALFORMED_FORMAL_DISPOSITION:
        return SAFE_MALFORMED
    if result is None:
        return "ABSENT"
    if result == APPROVE:
        return UNSAFE_BYPASS
    if result == ADVERSE_VERDICT:
        return SAFE_ADVERSE
    return "OTHER"


def _ascii_fold(text: str) -> str:
    """The SAME ASCII-only case fold acceptance uses."""
    return "".join(c.upper() if "a" <= c <= "z" else c for c in text)


# =====================================================================================
# 1. The swept region and the matrix are DERIVED, and cross-checked against the decision
# =====================================================================================


class TestTheMatrixIsDerivedAndAgreesWithTheDecision:
    def test_the_region_is_the_prefix_without_its_colon(self):
        assert PREFIX.endswith(":")
        assert CANON_LABEL == "FORMAL DISPOSITION"
        assert len(CANON_LABEL) == 18
        assert len(NONSPACE_POSITIONS) == 17
        assert len([c for c in CANON_LABEL if c == " "]) == 1

    def test_the_alphabet_is_the_whole_printable_ascii_range(self):
        assert len(PRINTABLE_ASCII) == 95
        assert PRINTABLE_ASCII[0] == " " and PRINTABLE_ASCII[-1] == "~"
        assert ":" in PRINTABLE_ASCII  # the classifier's own delimiter is IN the alphabet

    def test_every_confusable_stays_non_ascii_when_uppercased(self):
        """The documented mechanism: the printable-ASCII projection DELETES them."""
        for ascii_char, glyph in CONFUSABLES.items():
            assert glyph != ascii_char
            assert not glyph.upper().isascii(), (ascii_char, glyph)

    def test_every_mutant_really_differs_from_the_canonical_label(self):
        for family, index, character, label in EXHAUSTIVE:
            assert label != CANON_LABEL, (family, index, character)

    def test_the_cell_count_is_derived_from_the_families(self):
        expected = (
            len(NONSPACE_POSITIONS)                                    # deletion
            + sum(1 for i in NONSPACE_POSITIONS
                  for c in PRINTABLE_ASCII if c != CANON_LABEL[i])     # substitution
            + len(NONSPACE_POSITIONS) * len(PRINTABLE_ASCII)           # insertion
            + len(ADJACENT_PAIRS)                                      # transposition
            + len(NONSPACE_POSITIONS)                                  # confusable
        )
        assert len(EXHAUSTIVE) == expected
        assert len({(f, i, c) for f, i, c, _ in EXHAUSTIVE}) == len(EXHAUSTIVE)

    def test_the_colon_cells_are_named_and_non_empty(self):
        assert len(COLON_CELLS) == 2 * len(NONSPACE_POSITIONS)
        assert all(character == ":" for _, _, character, _ in COLON_CELLS)
        assert {family for family, _, _, _ in COLON_CELLS} == {
            "ascii_substitution", "ascii_insertion",
        }

    def test_this_matrix_matches_the_one_the_boundary_was_DECIDED_on(self):
        """Independent derivation, then cross-checked. A silent divergence fails here."""
        assert set(EXHAUSTIVE) == set(_DECIDED.EXHAUSTIVE)
        assert len(COLON_CELLS) == len(_DECIDED.COLON_CELLS)


# =====================================================================================
# 2. THE claim: the whole matrix is closed, in every governed presentation
# =====================================================================================

#: Every cell's real outcome, once, in every presentation. Derived; the SOLE source of the
#: per-family and per-presentation totals asserted below.
OUTCOMES = {
    form: {(f, i, c): _classify(_render(label, form)) for f, i, c, label in EXHAUSTIVE}
    for form in PRESENTATIONS
}


class TestTheWholeMatrixIsClosedByTheRealParser:
    @pytest.mark.parametrize("form", PRESENTATIONS)
    def test_no_cell_lets_a_later_approval_win(self, form):
        """SS-D.3's operative property, stated as the property rather than as a count."""
        open_cells = [key for key, out in OUTCOMES[form].items() if out == UNSAFE_BYPASS]
        assert open_cells == [], open_cells[:5]

    @pytest.mark.parametrize("form", PRESENTATIONS)
    def test_every_cell_lands_in_one_of_the_two_SAFE_classes(self, form):
        classes = set(OUTCOMES[form].values())
        assert classes <= {SAFE_MALFORMED, SAFE_ADVERSE}, sorted(classes)

    @pytest.mark.parametrize("form", PRESENTATIONS)
    @pytest.mark.parametrize("family", FAMILIES)
    def test_every_family_is_closed_and_non_empty(self, form, family):
        cells = [k for k in OUTCOMES[form] if k[0] == family]
        assert cells, family  # a family that measured nothing would prove nothing
        assert all(OUTCOMES[form][k] != UNSAFE_BYPASS for k in cells)

    def test_the_derived_totals_are_consistent_across_presentations(self):
        for form in PRESENTATIONS:
            assert len(OUTCOMES[form]) == len(EXHAUSTIVE)
        total_cells = sum(len(OUTCOMES[f]) for f in PRESENTATIONS)
        assert total_cells == len(EXHAUSTIVE) * len(PRESENTATIONS)
        total_open = sum(
            1 for f in PRESENTATIONS for out in OUTCOMES[f].values() if out == UNSAFE_BYPASS
        )
        assert total_open == 0

    def test_every_ADVERSE_cell_kept_the_canonical_prefix_intact(self):
        """Not merely 'some cells are ADVERSE': each is ADVERSE for the RIGHT reason.

        A cell may only survive as ADVERSE when the canonical prefix is still intact at the
        start of its revealed line -- which is what SS-D.1's ASCII case compatibility requires,
        and what makes the adverse verdict legitimately win. The converse is deliberately NOT
        asserted: a line whose prefix survives can still fail closed for an unrelated reason
        (four-column indentation makes it an indented code block, for instance), and predicting
        which would mean re-implementing the production parser and comparing it with itself --
        exactly the vacuity SS-E prohibits. This is the safety-relevant direction: no cell whose
        prefix was BROKEN is ever allowed to pass as a genuine adverse record.
        """
        adverse_seen = 0
        for form in PRESENTATIONS:
            for (f, i, c), out in OUTCOMES[form].items():
                if out != SAFE_ADVERSE:
                    continue
                label = next(
                    lb for ff, ii, cc, lb in EXHAUSTIVE if (ff, ii, cc) == (f, i, c)
                )
                rendered = _ascii_fold(_render(label, form)).strip(" ")
                if rendered.startswith("**") and rendered.endswith("**"):
                    rendered = rendered[2:-2]
                assert rendered.startswith(PREFIX), (form, f, i, c)
                adverse_seen += 1
        assert adverse_seen > 0, "a matrix with no ADVERSE cell would prove nothing here"

    def test_no_cell_whose_prefix_was_broken_survives_as_ADVERSE(self):
        """The same boundary from the other side, stated as its own falsifiable claim."""
        for form in PRESENTATIONS:
            for (f, i, c), out in OUTCOMES[form].items():
                label = next(
                    lb for ff, ii, cc, lb in EXHAUSTIVE if (ff, ii, cc) == (f, i, c)
                )
                if PREFIX in _ascii_fold(_render(label, form)):
                    continue
                assert out == SAFE_MALFORMED, (form, f, i, c, out)

    def test_at_least_one_cell_of_each_SAFE_class_really_occurs(self):
        """Non-vacuity for the partition itself."""
        for form in PRESENTATIONS:
            values = set(OUTCOMES[form].values())
            assert SAFE_MALFORMED in values, form
            assert SAFE_ADVERSE in values, form


class TestTheColonCellsAreIndependentlyLoadBearing:
    """The 34 cells whose mutation character IS the delimiter -- and 33 of which the SUPERSEDED
    first-colon rule left fail-open. They are exercised by name, never absorbed into a total."""

    def test_the_colon_cells_are_non_empty_and_complete(self):
        assert len(COLON_CELLS) == 34
        by_family = {}
        for family, index, _c, _l in COLON_CELLS:
            by_family.setdefault(family, set()).add(index)
        assert set(by_family) == {"ascii_substitution", "ascii_insertion"}
        for family, indices in by_family.items():
            assert indices == set(NONSPACE_POSITIONS), family

    @pytest.mark.parametrize("form", PRESENTATIONS)
    def test_every_colon_cell_is_closed(self, form):
        open_cells = [
            (f, i) for f, i, c, _ in COLON_CELLS
            if OUTCOMES[form][(f, i, c)] == UNSAFE_BYPASS
        ]
        assert open_cells == [], open_cells

    @pytest.mark.parametrize("form", PRESENTATIONS)
    def test_every_colon_cell_is_MALFORMED_specifically(self, form):
        """Not merely 'not a bypass': an inserted or substituted colon BREAKS the canonical
        prefix, so every one of these must fail closed rather than survive as ADVERSE."""
        for family, index, character, _label in COLON_CELLS:
            assert OUTCOMES[form][(family, index, character)] == SAFE_MALFORMED, (
                form, family, index,
            )

    def test_the_real_terminating_colon_is_still_probed_behind_an_inserted_one(self):
        """The exact mechanism the correction repaired, stated as a mechanism."""
        for family, index, character, label in COLON_CELLS:
            folded = _ascii_fold(_render(label, PLAIN))
            assert AUTH._is_formal_disposition_candidate(folded), (family, index)


# =====================================================================================
# 3. The two attacks independent review `5034171910` named, pinned by name
# =====================================================================================

#: BLOCKING 1's own examples: an ASCII colon SUBSTITUTED into, and INSERTED into, the label.
#: Under the superseded first-colon rule each hid the real terminating colon behind itself.
NAMED_ATTACKS = (
    "FORM:L DISPOSITION",
    "FORM:AL DISPOSITION",
)


class TestTheNamedAttacksAreClosed:
    @pytest.mark.parametrize("label", NAMED_ATTACKS)
    def test_the_attack_is_MALFORMED_by_sentinel_identity(self, label):
        body = _adverse_then_approval(f"{label}: {ADVERSE_VERDICT}")
        assert AUTH.parse_formal_disposition(body) is AUTH.MALFORMED_FORMAL_DISPOSITION

    @pytest.mark.parametrize("label", NAMED_ATTACKS)
    def test_the_attack_carries_a_real_colon_at_an_admissible_index(self, label):
        """Non-vacuity for the mechanism: these are closed BECAUSE the real terminating colon
        is still probed, not because the line happened to fail some unrelated check."""
        line = f"{label}: {ADVERSE_VERDICT}"
        admissible = [
            k for k in AUTH._ADMISSIBLE_COLON_INDICES
            if k < len(line) and line[k] == ":"
        ]
        assert admissible, label
        assert AUTH._is_formal_disposition_candidate(_ascii_fold(line))

    @pytest.mark.parametrize("label", NAMED_ATTACKS)
    def test_the_attack_is_a_real_cell_of_the_exhaustive_matrix(self, label):
        assert any(lb == label for _f, _i, _c, lb in EXHAUSTIVE), label

    @pytest.mark.parametrize("label", NAMED_ATTACKS)
    @pytest.mark.parametrize("form", PRESENTATIONS)
    def test_the_attack_is_closed_in_every_presentation(self, label, form):
        assert _classify(_render(label, form)) == SAFE_MALFORMED


# =====================================================================================
# 4. ACCEPTANCE IS UNCHANGED -- exact positive controls for every accepted form
# =====================================================================================

#: SS-E.2's required control classes, one entry per class, each with the EXACT value it must
#: still return. A class that silently disappears fails the completeness guard below.
ACCEPTED_CONTROLS = {
    "plain canonical approval": (f"{PREFIX} {APPROVE}", APPROVE),
    "plain canonical adverse": (f"{PREFIX} {ADVERSE_VERDICT}", ADVERSE_VERDICT),
    "whole-line bold pair": (f"**{PREFIX} {APPROVE}**", APPROVE),
    "ascii lower case": (f"{PREFIX.lower()} {APPROVE}", APPROVE),
    "ascii mixed case": (f"FoRmAl DiSpOsItIoN: {APPROVE}", APPROVE),
    "validated finding-count suffix": (
        f"{PREFIX} {APPROVE} — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE", APPROVE,
    ),
    "three-space indent": (f"   {PREFIX} {APPROVE}", APPROVE),
    "lower-case verdict, returned verbatim": (
        f"{PREFIX} {APPROVE.lower()}", APPROVE.lower(),
    ),
    "open-vocabulary verdict": (
        f"{PREFIX} BOUNDED CORRECTION REQUIRED", "BOUNDED CORRECTION REQUIRED",
    ),
    "bold pair with a finding-count suffix": (
        f"**{PREFIX} {APPROVE} — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE**", APPROVE,
    ),
}

#: The classes SS-E.2 names explicitly. Kept separate from the mapping so that DELETING an
#: entry fails rather than silently shrinking the evidence.
REQUIRED_CONTROL_CLASSES = (
    "plain canonical approval",
    "plain canonical adverse",
    "whole-line bold pair",
    "ascii lower case",
    "ascii mixed case",
    "validated finding-count suffix",
)


class TestAcceptanceIsUnchanged:
    def test_every_required_control_class_is_present(self):
        missing = [c for c in REQUIRED_CONTROL_CLASSES if c not in ACCEPTED_CONTROLS]
        assert missing == [], missing
        assert len(ACCEPTED_CONTROLS) >= len(REQUIRED_CONTROL_CLASSES)

    @pytest.mark.parametrize("name", sorted(ACCEPTED_CONTROLS))
    def test_the_accepted_form_returns_exactly_what_it_returned_before(self, name):
        line, expected = ACCEPTED_CONTROLS[name]
        assert AUTH.parse_formal_disposition(line + "\n") == expected, name

    @pytest.mark.parametrize("name", sorted(ACCEPTED_CONTROLS))
    def test_the_accepted_form_never_reaches_the_candidate_rule_at_all(self, name):
        """STRUCTURAL: acceptance is untouched because the rule is UNREACHABLE from it.

        The candidate branch runs only when the canonical prefix is ABSENT from the ASCII-folded
        line. Every accepted form contains it, so no accepted line can reach the rule -- which is
        a stronger statement than 'the rule happens not to change the answer'.
        """
        line, _expected = ACCEPTED_CONTROLS[name]
        assert PREFIX in _ascii_fold(line), name

    @pytest.mark.parametrize("name", sorted(ACCEPTED_CONTROLS))
    def test_the_accepted_form_is_unchanged_when_a_later_line_follows(self, name):
        """First-formal-line governance is preserved: a later approval never overrides."""
        line, expected = ACCEPTED_CONTROLS[name]
        body = f"{line}\n\n{PREFIX} {APPROVE}\n"
        assert AUTH.parse_formal_disposition(body) == expected, name

    def test_the_verdict_is_never_normalized_truncated_or_case_folded(self):
        """XASSET-0055 SS-C: the ENTIRE post-prefix region is the verdict, verbatim."""
        for verdict in (
            "approved for principal exact-head acceptance",
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE",
            "SoMe UnUsUaL VeRdIcT",
            "CHANGES REQUIRED",
            "A",
        ):
            assert AUTH.parse_formal_disposition(f"{PREFIX} {verdict}\n") == verdict

    def test_whole_verdict_exact_equality_still_rejects_appended_text(self):
        """Appended text can never authenticate: a property of exact equality, not a heuristic."""
        assert AUTH.parse_formal_disposition(f"{PREFIX} {APPROVE} and more\n") != APPROVE

    def test_the_open_vocabulary_is_not_closed_by_this_correction(self):
        """A verdict never seen before still returns verbatim rather than being refused."""
        novel = "SOME ENTIRELY NEW DISPOSITION NOBODY HAS USED"
        assert AUTH.parse_formal_disposition(f"{PREFIX} {novel}\n") == novel


# =====================================================================================
# 5. Ordinary prose stays ABSENT, and the SS-D.8 residual is preserved EXACTLY
# =====================================================================================

#: SS-E.3's required shapes. Every one of these is ABSENT today and must stay ABSENT: turning
#: prose into a formal candidate is precisely the boundary collapse SS-F.0.2 item 4 forbids.
PROSE_ABSENT_CONTROLS = {
    "plain prose": "no disposition at all",
    "prose opening with the two words": (
        "formal disposition but is not in an accepted form, so its verdict is unknown"
    ),
    "heading": "# Heading mentioning formal disposition",
    "blockquote": "> quoted formal disposition text",
    "bullet": "- bullet mentioning formal disposition",
    "numbered bullet": "1. numbered item mentioning formal disposition",
    "malformed emphasis": "*formal disposition* in partial emphasis",
    "nested emphasis": "**formal disposition** inside a longer sentence",
    "inline code": "`formal disposition` referenced as code",
    "table row": "| formal disposition | some column |",
    "sentence use": "the formal disposition of the estate was settled",
    "unrelated prose": "this paragraph discusses dispositions generally",
}

#: SS-D.8's residual, decided as ABSENT and expressly RESERVED from this correction: mutation of
#: the TERMINATING COLON itself carries no colon at any admissible index, so it yields no
#: candidate. Closing it is outside this unit's grant and is proved NOT to have happened.
TERMINATING_COLON_RESIDUAL = {
    "colon deleted": f"{CANON_LABEL} {ADVERSE_VERDICT}",
    "colon -> semicolon": f"{CANON_LABEL}; {ADVERSE_VERDICT}",
    "colon -> full stop": f"{CANON_LABEL}. {ADVERSE_VERDICT}",
    "colon -> hyphen": f"{CANON_LABEL}- {ADVERSE_VERDICT}",
    "colon -> non-ASCII ratio colon": f"{CANON_LABEL}∶ {ADVERSE_VERDICT}",
    "colon -> fullwidth colon": f"{CANON_LABEL}： {ADVERSE_VERDICT}",
}


class TestOrdinaryProseStaysAbsent:
    def test_the_control_set_is_non_empty(self):
        assert len(PROSE_ABSENT_CONTROLS) >= 10

    @pytest.mark.parametrize("name", sorted(PROSE_ABSENT_CONTROLS))
    def test_the_prose_line_is_ABSENT_on_its_own(self, name):
        line = PROSE_ABSENT_CONTROLS[name]
        assert AUTH.parse_formal_disposition(line + "\n") is None, name

    @pytest.mark.parametrize("name", sorted(PROSE_ABSENT_CONTROLS))
    def test_the_prose_line_is_not_a_candidate(self, name):
        line = PROSE_ABSENT_CONTROLS[name]
        assert AUTH._is_formal_disposition_candidate(_ascii_fold(line)) is False, name

    @pytest.mark.parametrize("name", sorted(PROSE_ABSENT_CONTROLS))
    def test_the_prose_line_does_not_block_a_later_real_approval(self, name):
        """The boundary's other side: prose must not fail closed either."""
        body = _adverse_then_approval(PROSE_ABSENT_CONTROLS[name])
        assert AUTH.parse_formal_disposition(body) == APPROVE, name

    def test_a_code_fenced_approval_still_fails_closed(self):
        """Code samples can never authenticate (XASSET-0053 SS-D.8), and the candidate rule
        does not weaken that."""
        body = f"```\n{PREFIX} {APPROVE}\n```\n"
        assert AUTH.parse_formal_disposition(body) is AUTH.MALFORMED_FORMAL_DISPOSITION

    def test_a_fence_marker_line_carrying_the_prefix_still_fails_closed(self):
        body = f"``` {PREFIX} {APPROVE}\n"
        assert AUTH.parse_formal_disposition(body) is AUTH.MALFORMED_FORMAL_DISPOSITION

    def test_a_prefix_bearing_marker_line_is_never_silently_skipped(self):
        for marker in ("#", ">", "-", "    "):
            body = _adverse_then_approval(f"{marker}{PREFIX} {ADVERSE_VERDICT}")
            assert AUTH.parse_formal_disposition(body) is not None, marker


class TestTheTerminatingColonResidualIsPreservedExactly:
    """SS-D.8 -- decided as ABSENT, expressly reserved, and NOT closed here.

    This is a DIFFERENT case from the internal-colon one the correction closed, and the two must
    not be conflated. They are separated by which colon the line carries.
    """

    def test_the_residual_set_is_non_empty(self):
        assert len(TERMINATING_COLON_RESIDUAL) >= 3

    @pytest.mark.parametrize("name", sorted(TERMINATING_COLON_RESIDUAL))
    def test_the_residual_line_carries_no_colon_at_any_admissible_index(self, name):
        """The mechanism, not just the outcome: the rule still REQUIRES a colon."""
        line = TERMINATING_COLON_RESIDUAL[name]
        assert not any(
            k < len(line) and line[k] == ":" for k in AUTH._ADMISSIBLE_COLON_INDICES
        ), name

    @pytest.mark.parametrize("name", sorted(TERMINATING_COLON_RESIDUAL))
    def test_the_residual_line_is_not_a_candidate(self, name):
        line = TERMINATING_COLON_RESIDUAL[name]
        assert AUTH._is_formal_disposition_candidate(_ascii_fold(line)) is False, name

    @pytest.mark.parametrize("name", sorted(TERMINATING_COLON_RESIDUAL))
    def test_the_residual_line_is_still_ABSENT(self, name):
        line = TERMINATING_COLON_RESIDUAL[name]
        assert AUTH.parse_formal_disposition(line + "\n") is None, name

    @pytest.mark.parametrize("name", sorted(TERMINATING_COLON_RESIDUAL))
    def test_the_residual_is_UNCHANGED_behaviour_not_a_new_hole(self, name):
        """Disclosed honestly: these were ABSENT before the correction and remain ABSENT."""
        body = _adverse_then_approval(TERMINATING_COLON_RESIDUAL[name])
        assert AUTH.parse_formal_disposition(body) == APPROVE, name

    def test_the_two_cases_are_distinguished_by_the_colon_and_nothing_else(self):
        """The internal-colon case is CLOSED; the terminating-colon case remains ABSENT."""
        internal = f"FORM:L DISPOSITION: {ADVERSE_VERDICT}"
        terminating = f"{CANON_LABEL} {ADVERSE_VERDICT}"
        assert AUTH._is_formal_disposition_candidate(_ascii_fold(internal)) is True
        assert AUTH._is_formal_disposition_candidate(_ascii_fold(terminating)) is False
        assert any(
            k < len(internal) and internal[k] == ":"
            for k in AUTH._ADMISSIBLE_COLON_INDICES
        )
        assert not any(
            k < len(terminating) and terminating[k] == ":"
            for k in AUTH._ADMISSIBLE_COLON_INDICES
        )


# =====================================================================================
# 6. Every REAL historical lifecycle review body retains its verdict
# =====================================================================================

#: REAL first-formal lines from REAL merged lifecycle reviews in this repository, verbatim, each
#: recorded with the pull request and review id it was actually posted on. Committed rather than
#: fetched, so this stays offline, deterministic and CI-equivalent.
HISTORICAL_REVIEW_LINES = (
    (359, 5034171910,
     "FORMAL DISPOSITION: CHANGES REQUIRED — 2 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE",
     "CHANGES REQUIRED"),
    (359, 5035960873,
     "FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
     " — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE",
     APPROVE),
    (358, 5026362328, "FORMAL DISPOSITION: BOUNDED CORRECTION REQUIRED",
     "BOUNDED CORRECTION REQUIRED"),
    (358, 5026856868, "FORMAL DISPOSITION: BOUNDED CORRECTION REQUIRED",
     "BOUNDED CORRECTION REQUIRED"),
    (358, 5027180757, "FORMAL DISPOSITION: BOUNDED CORRECTION REQUIRED",
     "BOUNDED CORRECTION REQUIRED"),
    (358, 5027496489, "FORMAL DISPOSITION: BOUNDED CORRECTION REQUIRED",
     "BOUNDED CORRECTION REQUIRED"),
    (358, 5030740306, "FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE",
     APPROVE),
    (357, 5015482594,
     "FORMAL DISPOSITION: BOUNDED CORRECTION REQUIRED"
     " — 1 BLOCKING / 0 MAJOR / 2 MINOR / 0 NOTE",
     "BOUNDED CORRECTION REQUIRED"),
    (357, 5019911766,
     "FORMAL DISPOSITION: BOUNDED CORRECTION REQUIRED"
     " — 1 BLOCKING / 0 MAJOR / 2 MINOR / 0 NOTE",
     "BOUNDED CORRECTION REQUIRED"),
    (357, 5020912146,
     "FORMAL DISPOSITION: BOUNDED CORRECTION REQUIRED"
     " — 1 BLOCKING / 0 MAJOR / 1 MINOR / 0 NOTE",
     "BOUNDED CORRECTION REQUIRED"),
    (357, 5022602312,
     "FORMAL DISPOSITION: BOUNDED CORRECTION REQUIRED"
     " — 1 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE",
     "BOUNDED CORRECTION REQUIRED"),
    (357, 5024576065,
     "FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
     " — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE",
     APPROVE),
)

#: A REAL bot review body carrying NO formal line at all. It was ABSENT and must stay ABSENT --
#: the ABSENT side of the boundary matters as much as the MALFORMED side.
HISTORICAL_ABSENT_BODY = (
    "\n### 💡 Codex Review\n\n"
    "**Reject homoglyph substitutions in the prefix**\n\n"
    "When a formal-looking adverse line replaces a prefix letter with a Unicode homoglyph ...\n"
)


class TestRealHistoricalReviewBodiesRetainTheirVerdicts:
    def test_the_corpus_is_substantial_and_exercises_several_verdicts(self):
        assert len(HISTORICAL_REVIEW_LINES) >= 12
        verdicts = {v for _pr, _rid, _line, v in HISTORICAL_REVIEW_LINES}
        assert len(verdicts) >= 3, verdicts
        assert APPROVE in verdicts  # an authenticating body
        assert any(v != APPROVE for v in verdicts)  # and adverse ones

    @pytest.mark.parametrize(
        "pr,review_id,line,verdict", HISTORICAL_REVIEW_LINES,
        ids=[f"pr{p}-{r}" for p, r, _l, _v in HISTORICAL_REVIEW_LINES],
    )
    def test_the_real_review_line_still_yields_its_exact_verdict(self, pr, review_id, line, verdict):
        assert AUTH.parse_formal_disposition(line + "\n") == verdict, (pr, review_id)

    @pytest.mark.parametrize(
        "pr,review_id,line,verdict", HISTORICAL_REVIEW_LINES,
        ids=[f"pr{p}-{r}" for p, r, _l, _v in HISTORICAL_REVIEW_LINES],
    )
    def test_the_real_review_line_is_never_reclassified_as_MALFORMED(self, pr, review_id, line, verdict):
        result = AUTH.parse_formal_disposition(line + "\n")
        assert result is not AUTH.MALFORMED_FORMAL_DISPOSITION, (pr, review_id)
        assert result is not None, (pr, review_id)

    def test_the_committed_bold_wrapped_review_fixture_is_unaffected(self):
        """PR #349 review 5000581301's line, byte-for-byte, from this repository's own fixtures."""
        line = _SEAMS_MODULE.REVIEW_5000581301_LINE
        assert AUTH.parse_formal_disposition(line + "\n") == APPROVE

    def test_the_real_body_with_no_formal_line_stays_ABSENT(self):
        assert AUTH.parse_formal_disposition(HISTORICAL_ABSENT_BODY) is None

    def test_every_authenticating_line_still_authenticates_end_to_end(self):
        authenticating = [
            line for _p, _r, line, v in HISTORICAL_REVIEW_LINES if v == APPROVE
        ]
        assert authenticating  # non-vacuity
        for line in authenticating:
            assert AUTH.parse_formal_disposition(line + "\n") == APPROVE


# =====================================================================================
# 7. ALL THREE real consumer seams refuse every attack
# =====================================================================================

_MALFORMED_TEXT = "not in an accepted form"
_ABSENT_TEXT = "carries no parseable"


def _seam_two_refused(errors) -> bool:
    joined = " ".join(errors)
    return (_MALFORMED_TEXT in joined) or (_ABSENT_TEXT in joined) or (ADVERSE_VERDICT in joined)


def _seam_three_refused(errors) -> bool:
    joined = " ".join(errors)
    return (
        (_MALFORMED_TEXT in joined)
        or (ADVERSE_VERDICT in joined)
        or ("cannot be proven non-adverse" in joined)
    )


def _seam_one_reached_finality(recorder) -> bool:
    return any(call.startswith("reviews:") for call in recorder.calls)


def _seam_subset() -> list[tuple[str, int, str, str]]:
    """The DECLARED, DERIVED safety-critical subset for seams 1 and 2.

    Seam 2's real implementation invokes many ``git`` subprocesses per call -- measured at
    ~100 ms -- so driving the whole 3 264-cell matrix through it is not feasible. SS-E.5 therefore
    requires a declared subset that includes EVERY colon cell and EVERY family-by-position
    representative, with the subset's composition ASSERTED rather than assumed. It is derived
    here, once, and the assertions below check it against the matrix rather than against a
    remembered number.
    """
    chosen: dict[tuple[str, int, str], tuple[str, int, str, str]] = {}
    for cell in COLON_CELLS:                       # every colon cell, in full
        chosen[(cell[0], cell[1], cell[2])] = cell
    seen_pairs = {(c[0], c[1]) for c in COLON_CELLS}
    for cell in EXHAUSTIVE:                        # then one representative per family/position
        pair = (cell[0], cell[1])
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            chosen[(cell[0], cell[1], cell[2])] = cell
    return sorted(chosen.values(), key=lambda c: (c[0], c[1], c[2]))


SEAM_SUBSET = _seam_subset()


class TestTheSeamSubsetCompositionIsAsserted:
    def test_the_subset_contains_every_colon_cell(self):
        assert all(cell in SEAM_SUBSET for cell in COLON_CELLS)
        assert len([c for c in SEAM_SUBSET if c[2] == ":"]) == len(COLON_CELLS)

    def test_the_subset_covers_every_family_by_position_pair(self):
        covered = {(f, i) for f, i, _c, _l in SEAM_SUBSET}
        expected = {(f, i) for f, i, _c, _l in EXHAUSTIVE}
        assert covered == expected, sorted(expected - covered)[:5]

    def test_the_subset_covers_every_family(self):
        assert {f for f, _i, _c, _l in SEAM_SUBSET} == set(FAMILIES)

    def test_the_subset_is_non_empty_and_smaller_than_the_matrix(self):
        assert len(SEAM_SUBSET) >= len(COLON_CELLS)
        assert 0 < len(SEAM_SUBSET) < len(EXHAUSTIVE)

    def test_every_subset_member_is_a_real_matrix_cell(self):
        assert all(cell in EXHAUSTIVE for cell in SEAM_SUBSET)


class TestEveryCellIsRefusedAtSeamThree:
    """Seam 3 -- ``_verify_selected_review_is_final`` -- over the WHOLE matrix, BOTH states."""

    @pytest.mark.parametrize("form", PRESENTATIONS)
    @pytest.mark.parametrize("state", ["COMMENTED", "APPROVED"])
    def test_every_cell_in_the_whole_matrix_is_refused(self, form, state):
        checked = 0
        unrefused = []
        for _f, _i, _c, label in EXHAUSTIVE:
            body = _adverse_then_approval(_render(label, form))
            if not _seam_three_refused(_SEAMS.run_consumer_three(body, state)):
                unrefused.append(label)
            checked += 1
        assert checked == len(EXHAUSTIVE)          # non-vacuity: the loop really ran
        assert unrefused == [], unrefused[:5]

    def test_a_native_APPROVED_state_rescues_nothing(self):
        """SS-E.6: the rescue path is exercised explicitly, not merely parametrized past."""
        rescued = []
        for _f, _i, _c, label in COLON_CELLS:
            body = _adverse_then_approval(_render(label, PLAIN))
            if not _seam_three_refused(_SEAMS.run_consumer_three(body, "APPROVED")):
                rescued.append(label)
        assert COLON_CELLS  # non-vacuity
        assert rescued == [], rescued

    def test_the_genuinely_ABSENT_policy_is_preserved_exactly(self):
        """XASSET-0053 SS-D.20.1: a genuinely ABSENT body keeps its EXISTING seam-3 treatment.

        This is the property the correction must NOT disturb: it adds refusals for tampered
        records, and changes nothing for bodies that carry no formal record at all.
        """
        for name, line in PROSE_ABSENT_CONTROLS.items():
            body = _adverse_then_approval(line)
            commented = _SEAMS.run_consumer_three(body, "COMMENTED")
            approved = _SEAMS.run_consumer_three(body, "APPROVED")
            assert not _seam_three_refused(commented), name
            assert not _seam_three_refused(approved), name

    def test_the_untampered_adverse_body_is_still_refused(self):
        """Known-good control for the refusal detector itself."""
        body = _adverse_then_approval(f"{CANON_LABEL}: {ADVERSE_VERDICT}")
        assert _seam_three_refused(_SEAMS.run_consumer_three(body, "COMMENTED"))
        assert _seam_three_refused(_SEAMS.run_consumer_three(body, "APPROVED"))

    def test_a_clean_approval_is_NOT_refused(self):
        """The other half of the control: a detector that refused everything would prove nothing."""
        body = f"{PREFIX} {APPROVE}\n"
        assert not _seam_three_refused(_SEAMS.run_consumer_three(body, "COMMENTED"))


class TestTheSafetyCriticalSubsetIsRefusedAtSeamsOneAndTwo:
    @pytest.mark.parametrize(
        "family,index,character,label", SEAM_SUBSET,
        ids=[f"{f}-{i}-{ord(c) if c else 0}" for f, i, c, _l in SEAM_SUBSET],
    )
    def test_seam_one_stops_at_the_parser_gate(self, family, index, character, label, monkeypatch):
        """Seam 1 -- ``_derive_pr337_actor_ratification``: execution must NOT proceed past it."""
        body = _adverse_then_approval(_render(label, PLAIN))
        recorder = _SEAMS.run_consumer_one(body, monkeypatch)
        assert not _seam_one_reached_finality(recorder), (family, index, character)

    @pytest.mark.parametrize(
        "family,index,character,label", SEAM_SUBSET,
        ids=[f"{f}-{i}-{ord(c) if c else 0}" for f, i, c, _l in SEAM_SUBSET],
    )
    def test_seam_one_is_not_rescued_by_a_native_APPROVED_state(
        self, family, index, character, label, monkeypatch
    ):
        body = _adverse_then_approval(_render(label, PLAIN))
        recorder = _SEAMS.run_consumer_one(body, monkeypatch, state="APPROVED")
        assert not _seam_one_reached_finality(recorder), (family, index, character)

    @pytest.mark.parametrize(
        "family,index,character,label", SEAM_SUBSET,
        ids=[f"{f}-{i}-{ord(c) if c else 0}" for f, i, c, _l in SEAM_SUBSET],
    )
    def test_seam_two_refuses(self, family, index, character, label):
        """Seam 2 -- ``verify_lifecycle_against_truth``."""
        body = _adverse_then_approval(_render(label, PLAIN))
        assert _seam_two_refused(_SEAMS.run_consumer_two(body)), (family, index, character)

    def test_seam_one_reaches_finality_for_a_clean_approval(self, monkeypatch):
        """Known-good control: a broken 'did it stop' detector cannot make the above look green."""
        recorder = _SEAMS.run_consumer_one(f"{PREFIX} {APPROVE}", monkeypatch)
        assert _seam_one_reached_finality(recorder), recorder.calls

    def test_seam_two_does_not_refuse_a_clean_approval(self):
        assert not _seam_two_refused(_SEAMS.run_consumer_two(f"{PREFIX} {APPROVE}"))

    def test_seam_one_and_two_both_refuse_the_untampered_adverse_body(self, monkeypatch):
        body = _adverse_then_approval(f"{CANON_LABEL}: {ADVERSE_VERDICT}")
        recorder = _SEAMS.run_consumer_one(body, monkeypatch)
        assert not _seam_one_reached_finality(recorder)
        assert _seam_two_refused(_SEAMS.run_consumer_two(body))


# =====================================================================================
# 8. STRUCTURAL: the candidate mechanism cannot return or create a verdict
# =====================================================================================


def _live_source() -> str:
    return (ROOT / MODULE_RELPATH).read_text(encoding="utf-8")


def _toplevel(source: str) -> dict[str, ast.AST]:
    return {
        node.name: node
        for node in ast.parse(source).body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }


def _call_sites(source: str, name: str) -> list[int]:
    return [
        node.lineno
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == name
    ]


HELPER_NAME = "_is_formal_disposition_candidate"


class TestTheCandidateMechanismCannotCreateAVerdict:
    def test_it_returns_only_boolean_literals(self):
        """STRUCTURAL, by AST: every ``return`` in the helper is ``True`` or ``False``.

        A verdict is a ``str``; a helper that can only return a bool literal can never produce,
        repair, complete or coerce one. This is proved from the syntax tree, not by sampling.
        """
        node = _toplevel(_live_source())[HELPER_NAME]
        returns = [n for n in ast.walk(node) if isinstance(n, ast.Return)]
        assert returns, "a helper with no return statement would prove nothing"
        for ret in returns:
            assert isinstance(ret.value, ast.Constant), ast.dump(ret)
            assert isinstance(ret.value.value, bool), ast.dump(ret)

    def test_its_declared_return_type_is_bool(self):
        node = _toplevel(_live_source())[HELPER_NAME]
        assert isinstance(node.returns, ast.Name) and node.returns.id == "bool"

    def test_it_really_returns_a_bool_for_every_matrix_cell(self):
        """Execution, alongside the structural proof rather than instead of it."""
        for _f, _i, _c, label in EXHAUSTIVE:
            for form in PRESENTATIONS:
                value = AUTH._is_formal_disposition_candidate(_ascii_fold(_render(label, form)))
                assert value is True or value is False, (label, form)

    def test_it_never_names_the_approving_verdict_or_the_sentinel(self):
        source = ast.get_source_segment(_live_source(), _toplevel(_live_source())[HELPER_NAME])
        for banned in (
            "APPROVING_REVIEW_DISPOSITION",
            "MALFORMED_FORMAL_DISPOSITION",
            "APPROVED FOR PRINCIPAL",
        ):
            assert banned not in source, banned

    def test_it_reads_only_the_label_region_never_the_verdict_region(self):
        """The verdict text can be anything at all without changing the classification."""
        for label in ("FORM:L DISPOSITION", "FORMAL DISPOSITON", CANON_LABEL):
            outcomes = {
                AUTH._is_formal_disposition_candidate(_ascii_fold(f"{label}: {verdict}"))
                for verdict in (
                    APPROVE, ADVERSE_VERDICT, "", "ANYTHING AT ALL", "x" * 500,
                )
            }
            assert len(outcomes) == 1, label

    def test_the_rule_only_ever_ADDS_refusals(self):
        """SS-D.6: its sole effect is additional fail-closed MALFORMED results.

        Proved over the whole matrix and every accepted and prose control: wherever the helper
        fires, the parser's answer is MALFORMED -- never a verdict, and never ABSENT.
        """
        fired = 0
        for _f, _i, _c, label in EXHAUSTIVE:
            for form in PRESENTATIONS:
                line = _render(label, form)
                if not AUTH._is_formal_disposition_candidate(_ascii_fold(line)):
                    continue
                if PREFIX in _ascii_fold(line):
                    continue  # accepted-form territory; the rule is unreachable there
                fired += 1
                assert _classify(line) == SAFE_MALFORMED, line
        assert fired > 0, "a rule that never fires would prove nothing"


class TestTheProductionShapeIsExactlyAuthorized:
    def test_there_is_no_fourth_call_site_of_the_parser(self):
        sites = _call_sites(_live_source(), "parse_formal_disposition")
        assert len(sites) == 3, sites

    def test_the_helper_has_exactly_one_call_site(self):
        sites = _call_sites(_live_source(), HELPER_NAME)
        assert len(sites) == 1, sites

    def test_the_helper_is_called_only_from_the_parser(self):
        parser = _toplevel(_live_source())["parse_formal_disposition"]
        inner = [
            n for n in ast.walk(parser)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id == HELPER_NAME
        ]
        assert len(inner) == 1

    def test_exactly_one_helper_was_added_and_no_second(self):
        """SS-F.2's ceiling is ONE, and it is now exactly spent."""
        base = subprocess.run(
            ["git", "show", f"{AUTHORIZATION_MERGE_SHA}:{MODULE_RELPATH}"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout

        def funcs(src):
            return {
                n.name for n in ast.walk(ast.parse(src))
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                and not n.name.startswith("__")
            }

        added = funcs(_live_source()) - funcs(base)
        assert added == {HELPER_NAME}, sorted(added)

    def test_no_general_parsing_framework_was_created(self):
        source = _live_source()
        helper = ast.get_source_segment(source, _toplevel(source)[HELPER_NAME])
        parser = ast.get_source_segment(source, _toplevel(source)["parse_formal_disposition"])
        for banned in (
            "class Parser", "class Grammar", "class Tokenizer", "class Lexer",
            "re.compile", "unicodedata", "import ", "NORMALIZ",
        ):
            assert banned not in helper, banned
            assert banned not in parser, banned

    def test_no_confusable_map_or_normalization_table_was_added(self):
        source = _live_source()
        helper = ast.get_source_segment(source, _toplevel(source)[HELPER_NAME])
        assert "CONFUSABLE" not in helper.upper()
        assert helper.count("{") == helper.count("}")  # no dict literal table smuggled in

    def test_the_admissible_indices_are_DERIVED_not_written_as_literals(self):
        source = _live_source()
        marker = "_ADMISSIBLE_COLON_INDICES = tuple("
        assert source.count(marker) == 1
        block = source[source.index(marker):]
        block = block[: block.index("\n)\n") + 3]
        for literal in ("17", "18", "19"):
            assert literal not in block, literal
        assert "len(" in block
        assert AUTH._ADMISSIBLE_COLON_INDICES == (17, 18, 19)

    def test_the_edit_budget_and_label_are_derived_from_the_prefix(self):
        assert AUTH._FORMAL_DISPOSITION_LABEL == PREFIX[:-1]
        assert AUTH._FORMAL_DISPOSITION_EDIT_BUDGET == 1
        assert AUTH._ADMISSIBLE_COLON_INDICES == tuple(
            len(AUTH._FORMAL_DISPOSITION_LABEL) + d
            for d in range(
                -AUTH._FORMAL_DISPOSITION_EDIT_BUDGET,
                AUTH._FORMAL_DISPOSITION_EDIT_BUDGET + 1,
            )
        )

    def test_only_the_parser_and_the_new_helper_changed_in_production(self):
        base = subprocess.run(
            ["git", "show", f"{AUTHORIZATION_MERGE_SHA}:{MODULE_RELPATH}"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout

        def defs(src):
            lines = src.splitlines(keepends=True)
            return {
                n.name: "".join(lines[n.lineno - 1: n.end_lineno])
                for n in ast.parse(src).body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            }

        old, new = defs(base), defs(_live_source())
        changed = {n for n in new if old.get(n) != new[n]}
        assert changed == {"parse_formal_disposition", HELPER_NAME}, sorted(changed)
        assert not (set(old) - set(new)), sorted(set(old) - set(new))


# =====================================================================================
# 9. The distance metric is CORRECT -- differential against a general implementation
# =====================================================================================


def _reference_osa(a: str, b: str) -> int:
    """A general, unrestricted OSA distance. Independent of the production implementation.

    The production rule needs only "is the distance within the budget", so it uses a closed-form
    first-divergence test rather than a matrix. That is only sound if it AGREES with a real
    distance function, so a genuine one is computed here and the two are compared directly. This
    is a DIFFERENT mechanism, not the same code twice.
    """
    la, lb = len(a), len(b)
    d = [[0] * (lb + 1) for _ in range(la + 1)]
    for i in range(la + 1):
        d[i][0] = i
    for j in range(lb + 1):
        d[0][j] = j
    for i in range(1, la + 1):
        for j in range(1, lb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d[la][lb]


def _production_within_budget(label: str) -> bool:
    """The production rule's own verdict for ``label``, isolated from colon handling.

    The label is presented at an admissible index with a real terminating colon, so the ONLY
    thing that can decide the outcome is the distance test itself.
    """
    return AUTH._is_formal_disposition_candidate(_ascii_fold(label + ":"))


class TestTheDistanceMetricIsCorrect:
    @pytest.mark.parametrize(
        "a,b,expected",
        [
            ("abc", "abc", 0),
            ("abc", "abd", 1),
            ("abc", "ab", 1),
            ("ab", "abc", 1),
            ("ab", "ba", 1),
            ("abc", "acb", 1),
            ("", "", 0),
            ("a", "", 1),
            ("abc", "cba", 2),
            (CANON_LABEL, CANON_LABEL, 0),
            (CANON_LABEL, "FROMAL DISPOSITION", 1),
            ("FORMAL DISPOSITON", CANON_LABEL, 1),
            ("FORMAL", CANON_LABEL, 12),
        ],
    )
    def test_the_reference_metric_itself_is_right(self, a, b, expected):
        """Known-bad controls for the CONTROL. A detector with no controls proves nothing."""
        assert _reference_osa(a, b) == expected

    def test_the_reference_metric_is_symmetric(self):
        for a, b in (("abc", "abd"), ("ab", "abc"), (CANON_LABEL, "FROMAL DISPOSITION")):
            assert _reference_osa(a, b) == _reference_osa(b, a)

    def test_production_agrees_with_the_reference_over_the_whole_matrix(self):
        """Every mutated label, both directions, against a real distance function."""
        checked = 0
        for _f, _i, _c, label in EXHAUSTIVE:
            folded = _ascii_fold(label)
            expected = _reference_osa(folded, CANON_LABEL) <= 1
            assert _production_within_budget(label) is expected, (label, folded)
            checked += 1
        assert checked == len(EXHAUSTIVE)

    def test_production_agrees_with_the_reference_on_MULTI_edit_labels(self):
        """The interesting side: labels the rule must REJECT. Non-vacuity is asserted."""
        multi = []
        for i in NONSPACE_POSITIONS:
            for j in NONSPACE_POSITIONS:
                if i >= j:
                    continue
                broken = list(CANON_LABEL)
                broken[i] = "X"
                broken[j] = "Y"
                multi.append("".join(broken))
        assert multi  # non-vacuity
        rejected = 0
        for label in multi:
            expected = _reference_osa(_ascii_fold(label), CANON_LABEL) <= 1
            assert _production_within_budget(label) is expected, label
            if not expected:
                rejected += 1
        assert rejected == len(multi), (rejected, len(multi))

    def test_production_rejects_labels_whose_length_is_far_from_canonical(self):
        for label in ("", "F", "FORMAL", CANON_LABEL + "XX", "X" * 40):
            assert _reference_osa(_ascii_fold(label), CANON_LABEL) > 1, label
            assert _production_within_budget(label) is False, label

    def test_the_budget_is_exactly_one_and_two_edits_are_refused(self):
        two_edits = "FROMAL DISPOSITON"          # one transposition AND one deletion
        assert _reference_osa(two_edits, CANON_LABEL) == 2
        assert _production_within_budget(two_edits) is False

    def test_ascii_case_folding_makes_case_irrelevant_to_classification(self):
        for label in ("form:l disposition", "FORM:L DISPOSITION", "FoRm:L dIsPoSiTiOn"):
            line = f"{label}: {ADVERSE_VERDICT}"
            assert AUTH._is_formal_disposition_candidate(_ascii_fold(line)) is True, label

    def test_a_non_ascii_character_never_folds_into_an_ascii_label_letter(self):
        """SS-D.1: ASCII-only folding. ``ſ`` uppercases to ``S`` under Unicode, and must not here."""
        assert _ascii_fold("ſ") == "ſ"
        assert _ascii_fold("ı") == "ı"
        line = f"FORMAL DISPOſITION: {APPROVE}"
        assert AUTH.parse_formal_disposition(line + "\n") != APPROVE


class TestTheRuleIsBounded:
    def test_it_is_flat_in_the_line_length(self):
        """O(1): three index probes and three capped comparisons, whatever the line's length."""
        short = f"FORM:L DISPOSITION: {ADVERSE_VERDICT}"
        long = f"FORM:L DISPOSITION: {'x' * 2_000_000}"

        def timed(line: str) -> float:
            folded = _ascii_fold(line)
            best = None
            for _ in range(5):
                start = time.perf_counter()
                for _ in range(200):
                    AUTH._is_formal_disposition_candidate(folded)
                elapsed = time.perf_counter() - start
                best = elapsed if best is None else min(best, elapsed)
            return best

        # Folding is linear, so it is done ONCE, outside the measurement, on both sides.
        assert timed(long) < timed(short) * 20

    def test_it_probes_at_most_three_indices_per_projection(self):
        assert len(AUTH._ADMISSIBLE_COLON_INDICES) == 3
        assert len(set(AUTH._ADMISSIBLE_COLON_INDICES)) == 3

    def test_it_recognizes_exactly_the_two_governed_wrapper_forms(self):
        """No third projection exists, so no new wrapper is recognized."""
        line = f"FORM:L DISPOSITION: {ADVERSE_VERDICT}"
        assert AUTH._is_formal_disposition_candidate(_ascii_fold(line)) is True
        assert AUTH._is_formal_disposition_candidate(_ascii_fold(f"**{line}**")) is True
        # A THIRD wrapper is not recognized: single asterisks are not a governed form.
        assert AUTH._is_formal_disposition_candidate(_ascii_fold(f"*{line}*")) is False
        assert AUTH._is_formal_disposition_candidate(_ascii_fold(f"_{line}_")) is False


# =====================================================================================
# 10. Stage 1 remains fail-closed, and this unit's scope is exactly what was authorized
# =====================================================================================


def _blob_at(commit: str, relpath: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"{commit}:{relpath}"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()


class TestStageOneRemainsFailClosed:
    def test_all_three_authorization_predicates_are_false(self):
        for predicate in (
            AUTH.new_execution_is_authorized,
            AUTH.claimed_execution_is_authorized,
            AUTH.active_execution_is_authorized,
        ):
            authorized, _reason = predicate()
            assert authorized is False, predicate.__name__

    def test_the_lane_is_absent_and_attempt_one_is_unconsumed(self):
        state, _reason = AUTH.lane_state_at(AUTH.LanePaths())
        assert state == AUTH.LANE_ABSENT
        assert not AUTH.AUTHORIZATION_ROOT.exists()
        assert not AUTH.AUTHORIZATION_PATH.exists()
        assert not AUTH.CLAIM_PATH.exists()
        assert AUTH.EXECUTION_ATTEMPT_ID.endswith("ATTEMPT_1")

    def test_no_results_artifact_exists(self):
        assert not (ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()

    def test_the_load_bearing_boundary_is_unchanged_at_eighteen(self):
        assert len(AUTH.LOAD_BEARING_RELPATHS) == 18
        base = subprocess.run(
            ["git", "show", f"{AUTHORIZATION_MERGE_SHA}:{MODULE_RELPATH}"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
        assert base.count("LOAD_BEARING_RELPATHS = (") == 1
        # The MEMBERSHIP is unchanged too, not merely the count.
        before = base[base.index("LOAD_BEARING_RELPATHS = ("):]
        before = before[: before.index("\n)\n")]
        after = _live_source()[_live_source().index("LOAD_BEARING_RELPATHS = ("):]
        after = after[: after.index("\n)\n")]
        assert before == after

    def test_this_suite_writes_nothing_during_collection_or_any_test(self):
        """Every filesystem write lives INSIDE the mutation harness, which pytest never calls.

        The harness must write -- that is what a mutation probe is -- so the honest property is
        containment, not absence: no write may appear anywhere a collected test can reach it.
        """
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        harness = {"_run_mutation_proof"}
        offenders = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in harness:
                continue
            for inner in ast.walk(node):
                if not isinstance(inner, ast.Call):
                    continue
                attr = getattr(inner.func, "attr", None)
                if attr in ("write_text", "write_bytes", "unlink", "mkdir", "rmtree"):
                    offenders.append((getattr(node, "name", "<module>"), attr))
        assert offenders == [], offenders


class TestThisUnitsScopeIsExactlyWhatWasAuthorized:
    def test_the_base_is_the_authorization_merge(self):
        """SS-G.2: the implementation must base EXACTLY on the authorization's own merge."""
        merge_base = subprocess.run(
            ["git", "merge-base", "HEAD", AUTHORIZATION_MERGE_SHA],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        assert merge_base == AUTHORIZATION_MERGE_SHA

    def test_the_authorization_merge_shape_is_what_it_claims(self):
        parents = subprocess.run(
            ["git", "log", "-1", "--pretty=%P", AUTHORIZATION_MERGE_SHA],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
        assert tuple(parents) == AUTHORIZATION_MERGE_PARENTS
        tree = subprocess.run(
            ["git", "rev-parse", f"{AUTHORIZATION_MERGE_SHA}^{{tree}}"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        assert tree == AUTHORIZATION_MERGE_TREE
        accepted_tree = subprocess.run(
            ["git", "rev-parse", f"{AUTHORIZATION_ACCEPTED_HEAD}^{{tree}}"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        assert accepted_tree == AUTHORIZATION_MERGE_TREE  # zero drift at merge

    @pytest.mark.parametrize("relpath", PROTECTED_RELPATHS)
    def test_the_protected_path_is_byte_identical_to_the_base(self, relpath):
        assert _blob_at("HEAD", relpath) == _blob_at(AUTHORIZATION_MERGE_SHA, relpath), relpath

    def test_the_production_module_is_the_ONLY_protected_path_this_unit_changes(self):
        changed = subprocess.run(
            ["git", "diff", "--name-only", AUTHORIZATION_MERGE_SHA, "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
        bound = set(AUTH.LOAD_BEARING_RELPATHS)
        touched_bound = sorted(set(changed) & bound)
        assert touched_bound == [MODULE_RELPATH], touched_bound

    def test_the_vulnerable_identity_survives_as_a_permanent_negative_pin(self):
        """SS-G.3: role 2 is adverse history. It is never rebound, re-pinned or repaired."""
        base = subprocess.run(
            ["git", "show", f"{AUTHORIZATION_MERGE_SHA}:{MODULE_RELPATH}"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
        assert hashlib.sha256(base.encode("utf-8")).hexdigest() == VULNERABLE_MODULE_SHA256
        flat = WORKSTREAMS.read_text(encoding="utf-8").replace("\n", "").replace(" ", "")
        assert VULNERABLE_MODULE_SHA256 in flat

    def test_the_corrected_identity_is_NEVER_PREDICTED_anywhere(self):
        """SS-G.4 / XASSET-0057 SS-F.3 role 3: derived at merge, stated nowhere in advance.

        This is the operative constraint on THIS unit, so it is enforced mechanically rather
        than promised: the live digest must appear in no governed record at all.
        """
        live = hashlib.sha256((ROOT / MODULE_RELPATH).read_bytes()).hexdigest()
        assert live != VULNERABLE_MODULE_SHA256
        for path in (WORKSTREAMS, CATALOG, ROOT / DECISION_RELPATH, Path(__file__)):
            assert live not in path.read_text(encoding="utf-8"), str(path)

    def test_the_decision_exists_and_records_its_own_incompleteness(self):
        text = (ROOT / DECISION_RELPATH).read_text(encoding="utf-8")
        for token in ("XASSET-0058", "parse_formal_disposition", "Lifecycle B"):
            assert token in text, token
        lowered = text.lower()
        assert "not merged" in lowered or "draft" in lowered

    def test_no_test_was_skipped_xfailed_or_deleted_anywhere_in_this_unit(self):
        changed = subprocess.run(
            ["git", "diff", "--name-only", AUTHORIZATION_MERGE_SHA, "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
        suites = [n for n in changed if n.startswith("test_") and n.endswith(".py")]
        assert suites  # non-vacuity
        for name in suites:
            live = (ROOT / name).read_text(encoding="utf-8")
            base = subprocess.run(
                ["git", "show", f"{AUTHORIZATION_MERGE_SHA}:{name}"],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            if base.returncode != 0:
                continue  # a file this unit ADDS has no base to compare against
            for banned in ("pytest.mark.skip", "pytest.mark.xfail", "pytest.skip("):
                assert live.count(banned) == base.stdout.count(banned), (name, banned)
            assert live.count("assert ") >= base.stdout.count("assert "), name


# =====================================================================================
# 11. MUTATION PROOF -- every guard above is falsifiable, and fails for its INTENDED reason
# =====================================================================================

def _anchor(*parts: str) -> str:
    """Join an anchor from fragments.

    A probe that targets THIS module cannot store its anchor as one literal: the literal would
    then appear twice -- at the real definition, and in the table -- and the "exactly once"
    guard would abort every self-targeting probe. Assembling it at runtime keeps that guard
    meaningful rather than relaxing it.
    """
    return "".join(parts)


#: Each probe: ``(id, relpath, anchor, replacement, why, expected_failure_marker)``.
#:
#: ``anchor`` must occur EXACTLY ONCE in the file -- zero occurrences means the guard moved and
#: the probe is stale, more than one means the probe is ambiguous. Either is ABORTED, never
#: silently reported as "caught". ``replacement`` must differ from ``anchor``, or the probe is a
#: no-op that would trivially "pass" while proving nothing.
#:
#: ``expected_failure_marker`` names a test whose failure is the INTENDED reason. A probe that
#: only breaks something unrelated is reported as MISSED-INTENT rather than counted as caught.
MUTATIONS: tuple[tuple[str, str, str, str, str, str], ...] = (
    # ---- isolating probes: one per STRUCTURAL ELEMENT of the classifier -----------------
    (
        "P01-first-colon-search-reintroduced",
        MODULE_RELPATH,
        "            if index >= len(projection) or projection[index] != \":\":\n"
        "                continue",
        "            index = projection.find(\":\")\n"
        "            if index == -1 or index not in _ADMISSIBLE_COLON_INDICES:\n"
        "                continue",
        "reverting to the SUPERSEDED first-colon search must reopen the colon cells",
        "TestTheColonCellsAreIndependentlyLoadBearing",
    ),
    (
        "P02-admissible-indices-reduced",
        MODULE_RELPATH,
        "    for offset in range(-_FORMAL_DISPOSITION_EDIT_BUDGET, "
        "_FORMAL_DISPOSITION_EDIT_BUDGET + 1)",
        "    for offset in (0,)",
        "probing fewer than all three admissible indices must reopen cells",
        "TestTheWholeMatrixIsClosedByTheRealParser",
    ),
    (
        "P03-colon-requirement-dropped",
        MODULE_RELPATH,
        "            if index >= len(projection) or projection[index] != \":\":",
        "            if index >= len(projection):",
        "dropping the colon requirement must violate the preserved SS-D.8 residual",
        "TestTheTerminatingColonResidualIsPreservedExactly",
    ),
    (
        "P04-edit-budget-widened",
        MODULE_RELPATH,
        "_FORMAL_DISPOSITION_EDIT_BUDGET = 1",
        "_FORMAL_DISPOSITION_EDIT_BUDGET = 2",
        "widening the budget must disagree with the reference distance metric",
        "TestTheDistanceMetricIsCorrect",
    ),
    (
        "P05-bold-projection-removed",
        MODULE_RELPATH,
        "        projections.append(revealed[2:-2])",
        "        pass",
        "dropping the bold projection must reopen the bold presentation",
        "TestTheWholeMatrixIsClosedByTheRealParser",
    ),
    (
        "P06-transposition-arm-removed",
        MODULE_RELPATH,
        "                    or (  # one ADJACENT transposition\n"
        "                        label[head:head + 2] == canonical[head:head + 2][::-1]\n"
        "                        and label[head + 2:] == canonical[head + 2:]\n"
        "                    )",
        "                    or False",
        "the transposition family must stop being closed",
        "TestTheWholeMatrixIsClosedByTheRealParser",
    ),
    (
        "P07-deletion-arm-removed",
        MODULE_RELPATH,
        "                if label[head:] == canonical[head + 1:]:  # one character deleted",
        "                if False:  # one character deleted",
        "the deletion family must stop being closed",
        "TestTheWholeMatrixIsClosedByTheRealParser",
    ),
    (
        "P08-insertion-arm-removed",
        MODULE_RELPATH,
        "            elif label[head + 1:] == canonical[head:]:  # one character inserted",
        "            elif False:  # one character inserted",
        "the insertion family must stop being closed",
        "TestTheWholeMatrixIsClosedByTheRealParser",
    ),
    (
        "P09-substitution-arm-removed",
        MODULE_RELPATH,
        "                    or label[head + 1:] == canonical[head + 1:]  # one substitution",
        "                    or False  # one substitution",
        "the substitution and confusable families must stop being closed",
        "TestTheWholeMatrixIsClosedByTheRealParser",
    ),
    (
        "P10-hook-unreachable",
        MODULE_RELPATH,
        "            if _is_formal_disposition_candidate(ascii_upper):",
        "            if False and _is_formal_disposition_candidate(ascii_upper):",
        "disconnecting the hook must reopen the entire matrix",
        "TestTheWholeMatrixIsClosedByTheRealParser",
    ),
    (
        "P11-helper-returns-a-verdict",
        MODULE_RELPATH,
        "    return False\n\n\ndef parse_formal_disposition",
        "    return bool(canonical)\n\n\ndef parse_formal_disposition",
        "a non-literal return must fail the structural no-verdict proof",
        "TestTheCandidateMechanismCannotCreateAVerdict",
    ),
    (
        "P12-acceptance-widened",
        MODULE_RELPATH,
        "        if FORMAL_DISPOSITION_PREFIX not in ascii_upper:",
        "        if FORMAL_DISPOSITION_PREFIX not in ascii_upper.replace(\"0\", \"O\"):",
        "touching acceptance must break the accepted-form controls",
        "TestAcceptanceIsUnchanged",
    ),
    # ---- probes against THIS SUITE's own evidence ---------------------------------------
    (
        "P13-alphabet-collapsed-to-one-character",
        Path(__file__).name,
        _anchor("PRINTABLE_ASCII = tuple(chr(code)", " for code in range(0x20, 0x7F))"),
        _anchor("PRINTABLE_ASCII", " = (\"X\",)"),
        "collapsing the exhaustive alphabet back to one handpicked character must fail",
        "TestTheMatrixIsDerivedAndAgreesWithTheDecision",
    ),
    (
        "P14-colon-removed-from-the-alphabet",
        Path(__file__).name,
        _anchor("PRINTABLE_ASCII = tuple(chr(code)", " for code in range(0x20, 0x7F))"),
        _anchor("PRINTABLE_ASCII = tuple(c for c in map(chr,",
                " range(0x20, 0x7F)) if c != \":\")"),
        "removing the delimiter from the alphabet must fail the colon-cell guards",
        "TestTheColonCellsAreIndependentlyLoadBearing",
    ),
    (
        "P15-families-truncated",
        Path(__file__).name,
        _anchor("    for i in ADJACENT_PAIRS:\n",
                "        out.append((\n",
                "            \"transposition\", i, \"\","),
        _anchor("    for i in ADJACENT_PAIRS[:0]:\n",
                "        out.append((\n",
                "            \"transposition\", i, \"\","),
        "silently dropping a family must fail the derived-count and cross-check guards",
        "TestTheMatrixIsDerivedAndAgreesWithTheDecision",
    ),
    (
        "P16-seam-subset-loses-the-colon-cells",
        Path(__file__).name,
        _anchor("    for cell in COLON_CELLS:                       ",
                "# every colon cell, in full\n",
                "        chosen[(cell[0], cell[1], cell[2])] = cell"),
        _anchor("    for cell in COLON_CELLS[:0]:                   ",
                "# every colon cell, in full\n",
                "        chosen[(cell[0], cell[1], cell[2])] = cell"),
        "a subset that drops the colon cells must fail its own composition assertion",
        "TestTheSeamSubsetCompositionIsAsserted",
    ),
    (
        "P17-seam-refusal-detector-broken",
        Path(__file__).name,
        _anchor("def _seam_three_refused(errors) -> bool:\n",
                "    joined = \" \".join(errors)"),
        _anchor("def _seam_three_refused(errors) -> bool:\n",
                "    return True\n",
                "    joined = \" \".join(errors)"),
        "a refusal detector that always says 'refused' must fail its known-good control",
        "TestEveryCellIsRefusedAtSeamThree",
    ),
    (
        "P18-seam-one-detector-broken",
        Path(__file__).name,
        _anchor("def _seam_one_reached_finality(recorder) -> bool:\n",
                "    return any(call.startswith(\"reviews:\")",
                " for call in recorder.calls)"),
        _anchor("def _seam_one_reached_finality(recorder) -> bool:\n",
                "    return False"),
        "a seam-1 detector that never reports finality must fail its known-good control",
        "TestTheSafetyCriticalSubsetIsRefusedAtSeamsOneAndTwo",
    ),
    (
        "P19-non-emptiness-guard-removed",
        Path(__file__).name,
        _anchor("        assert checked == len(EXHAUSTIVE)          ",
                "# non-vacuity: the loop really ran"),
        _anchor("        assert True          ",
                "# non-vacuity: the loop really ran"),
        "removing a non-emptiness guard must be caught by the harness's own vacuity scan",
        "TestTheMutationHarnessIsSound",
    ),
    (
        "P20-residual-control-emptied",
        Path(__file__).name,
        _anchor("    \"colon deleted\": ", "f\"{CANON_LABEL} {ADVERSE_VERDICT}\","),
        _anchor("    \"colon deleted -- REMOVED\": ", "\"unrelated prose\","),
        "weakening the preserved-residual controls must fail",
        "TestTheTerminatingColonResidualIsPreservedExactly",
    ),
    (
        "P21-accepted-control-class-deleted",
        Path(__file__).name,
        _anchor("    \"whole-line bold pair\": ", "(f\"**{PREFIX} {APPROVE}**\", APPROVE),"),
        _anchor("    \"whole-line bold pair -- REMOVED\": ",
                "(f\"{PREFIX} {APPROVE}\", APPROVE),"),
        "deleting a required acceptance-control class must fail the completeness guard",
        "TestAcceptanceIsUnchanged",
    ),
    (
        "P22-historical-corpus-emptied",
        Path(__file__).name,
        _anchor("HISTORICAL_REVIEW_LINES = (\n", "    (359, 5034171910,"),
        _anchor("HISTORICAL_REVIEW_LINES = (\n", "    (359, 5034171910,\n)\n",
                "UNUSED = (\n    (359, 5034171910,"),
        "emptying the historical corpus must fail its substantiality guard",
        "TestRealHistoricalReviewBodiesRetainTheirVerdicts",
    ),
    (
        "P23-reference-metric-made-trivial",
        Path(__file__).name,
        _anchor("def _reference_osa(a: str,", " b: str) -> int:"),
        _anchor("def _reference_osa(a: str,", " b: str) -> int:\n    return 0"),
        "a trivial reference metric must fail its OWN known-bad controls",
        "TestTheDistanceMetricIsCorrect",
    ),
    (
        "P24-prose-controls-emptied",
        Path(__file__).name,
        _anchor("    \"plain prose\": ", "\"no disposition at all\","),
        _anchor("    \"plain prose -- REMOVED\": ", "\"formal disposition: SOMETHING\","),
        "weakening the prose ABSENT controls must fail",
        "TestOrdinaryProseStaysAbsent",
    ),
)


def _assert_no_vacuous_assertions(source: str) -> list[str]:
    """SS-E's 'vacuity is prohibited', enforced on THIS module's own text."""
    offenders = []
    for lineno, line in enumerate(source.split("\n"), 1):
        stripped = line.strip()
        if not stripped.startswith("assert "):
            continue
        body = stripped[len("assert "):]
        if body.startswith("True") or body.startswith("not False"):
            offenders.append(f"{lineno}: {stripped}")
        if " or True" in body or body.endswith("or True"):
            offenders.append(f"{lineno}: {stripped}")
    return offenders


class TestTheMutationHarnessIsSound:
    def test_every_anchor_occurs_exactly_once(self):
        for probe_id, relpath, anchor, _replacement, _why, _marker in MUTATIONS:
            text = (ROOT / relpath).read_text(encoding="utf-8")
            assert text.count(anchor) == 1, (probe_id, relpath, text.count(anchor))

    def test_no_probe_is_a_no_op(self):
        for probe_id, _relpath, anchor, replacement, _why, _marker in MUTATIONS:
            assert anchor != replacement, probe_id

    def test_every_probe_names_a_distinct_id(self):
        ids = [p[0] for p in MUTATIONS]
        assert len(set(ids)) == len(ids)

    def test_the_probe_set_covers_every_required_category(self):
        ids = " ".join(p[0] for p in MUTATIONS)
        for required in (
            "first-colon", "admissible-indices", "colon-requirement", "alphabet-collapsed",
            "seam-refusal", "non-emptiness", "residual", "accepted-control",
        ):
            assert required in ids, required

    def test_there_is_at_least_one_probe_per_mutation_family(self):
        ids = " ".join(p[0] for p in MUTATIONS)
        for family_marker in ("transposition", "deletion", "insertion", "substitution"):
            assert family_marker in ids, family_marker

    def test_every_probe_targets_a_real_file(self):
        for probe_id, relpath, *_rest in MUTATIONS:
            assert (ROOT / relpath).exists(), (probe_id, relpath)

    def test_this_module_contains_no_vacuous_assertion(self):
        offenders = _assert_no_vacuous_assertions(Path(__file__).read_text(encoding="utf-8"))
        assert offenders == [], offenders

    def test_the_harness_has_an_explicit_main_guard(self):
        source = Path(__file__).read_text(encoding="utf-8")
        assert 'if __name__ == "__main__":' in source

    def test_the_probe_count_is_substantial(self):
        assert len(MUTATIONS) >= 20


def _run_mutation_proof() -> int:
    """Apply each probe, require the suite to NOTICE, and restore every file byte-identically.

    Safety properties, all of them load-bearing:

    * pre-run hashes and original bytes are captured INDEPENDENTLY, before any mutation, and
      restoration always compares against that pre-run snapshot -- never against one taken while
      a mutation is active;
    * a missing, duplicated or no-op anchor is ABORTED, never counted as caught;
    * the complete worktree is inspected for residue at the end, not just the mutated files.
    """
    import os
    import sys

    targets = sorted({relpath for _id, relpath, *_rest in MUTATIONS})
    # --- pre-run snapshot, captured ONCE, before anything is touched --------------------
    original: dict[str, bytes] = {}
    pre_hash: dict[str, str] = {}
    for relpath in targets:
        data = (ROOT / relpath).read_bytes()
        original[relpath] = data
        pre_hash[relpath] = hashlib.sha256(data).hexdigest()

    pre_status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout

    caught, missed, aborted = [], [], []
    for probe_id, relpath, anchor, replacement, why, marker in MUTATIONS:
        text = original[relpath].decode("utf-8")
        occurrences = text.count(anchor)
        if occurrences != 1:
            aborted.append(f"{probe_id}: anchor occurs {occurrences}x in {relpath}")
            continue
        if anchor == replacement:
            aborted.append(f"{probe_id}: no-op probe")
            continue
        mutated = text.replace(anchor, replacement, 1)
        if mutated == text:
            aborted.append(f"{probe_id}: mutation changed nothing")
            continue
        (ROOT / relpath).write_text(mutated, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-x", "-q", "--no-header",
                 "-p", "no:cacheprovider", Path(__file__).name],
                cwd=ROOT, capture_output=True, text=True,
            )
            noticed = result.returncode != 0
            intended = marker in (result.stdout + result.stderr)
            if noticed and intended:
                caught.append(probe_id)
            elif noticed:
                missed.append(f"{probe_id}: FAILED, but not via {marker} (wrong reason)")
            else:
                missed.append(f"{probe_id}: NOT CAUGHT -- {why}")
        finally:
            # ALWAYS restore from the PRE-RUN bytes, never from a mid-mutation snapshot.
            (ROOT / relpath).write_bytes(original[relpath])

    # --- restoration proof, against the INDEPENDENTLY captured pre-run hashes -----------
    for relpath in targets:
        now = hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest()
        if now != pre_hash[relpath]:
            aborted.append(f"RESTORATION FAILED: {relpath}")

    post_status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    residue = "" if post_status == pre_status else post_status

    print(f"caught  : {len(caught)}")
    print(f"missed  : {len(missed)}")
    for line in missed:
        print(f"   MISSED  {line}")
    print(f"aborted : {len(aborted)}")
    for line in aborted:
        print(f"   ABORT   {line}")
    print(f"restored: {len(targets)} file(s) byte-identical to their pre-run hashes")
    print(f"residue : {'NONE' if not residue else residue}")
    ok = not missed and not aborted and not residue
    print("RESULT  :", "ALL PROBES CAUGHT, WORKTREE CLEAN" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_run_mutation_proof())
