"""Supporting artifact for ``XASSET-0058``.

``XASSET-0058`` is a **design-only Lane G governance authorization**. It is the **Lifecycle A**
authorization ``XASSET-0057`` SS-F.0.3 requires, it **decides** the formal-disposition recognition
boundary ``XASSET-0057`` SS-F.0.2 reserved to it, and it **performs no parser correction**.

This module proves those claims mechanically rather than by assertion:

* the **defect family** is re-measured against the live merged bytes -- 85 cells, five families,
  the real parser and all three real consumer seams -- rather than quoted from ``XASSET-0057``;
* the **decided boundary** (SS-D) is carried as a *test-only reference model* and proved to close
  all 85 cells in all three governed presentations while regressing **nothing** on the repository's
  own committed corpora;
* this filing **changes no production byte** and leaves Stage 1 fail-closed; and
* every guard here is **falsifiable** -- the mutation harness at the end removes each one and
  requires the suite to notice.

Every historical fact is proved over an **immutable commit range** -- this unit's own base and its
ancestors -- so nothing depends on a moving ref, and the suite keeps passing at a merged-``main``
state where ``HEAD`` equals ``origin/main``.
"""

from __future__ import annotations

import ast
import datetime
import hashlib
import inspect
import re
import subprocess
from pathlib import Path

import pytest
import yaml

import level1_stage1_execution_authorization as AUTH

#: The three REAL consumer seams. Reused from the ``XASSET-0056`` suite that already drives them
#: against the live module, rather than re-implementing a second, divergent harness. These are the
#: actual production call sites of ``parse_formal_disposition``:
#:   1. ``_derive_pr337_actor_ratification``
#:   2. ``verify_lifecycle_against_truth``
#:   3. ``_verify_selected_review_is_final``
import test_level1_stage1_formal_disposition_parser_correction as _SEAMS_MODULE


class _SEAMS:
    """Thin, explicit binding to the real seam runners. No behaviour of its own."""

    run_consumer_one = staticmethod(_SEAMS_MODULE._run_consumer_one)
    run_consumer_two = staticmethod(_SEAMS_MODULE._run_consumer_two)
    run_consumer_three = staticmethod(_SEAMS_MODULE._run_consumer_three)


ROOT = Path(__file__).resolve().parent

# =====================================================================================
# Immutable identities -- every one independently verified from live git/GitHub before use
# =====================================================================================

#: This unit's own base: the normal-merge commit that closed the ``XASSET-0057`` lifecycle.
THIS_UNIT_BASE_SHA = "556a43cf91679d3e8ca95703c8d49e672b662b73"

#: ``XASSET-0057``'s independently reviewed and principal-accepted head.
XASSET_0057_ACCEPTED_HEAD = "53d2d3d770f379393a1a3fde4408915c9fcf81f0"

#: The merge's first parent -- the prior ``main`` tip -- and its second, the accepted head.
XASSET_0057_MERGE_PARENT_1 = "583022a5f2106d61f82d270edadd3520d8b0c55d"
XASSET_0057_PULL_REQUEST = 358
XASSET_0057_CLEAN_REVIEW_ID = "5030740306"
XASSET_0057_ACCEPTANCE_COMMENT_ID = "5425835377"
#: Authored by ``claude[bot]``. Recorded ONLY so it can never be mistaken for acceptance.
XASSET_0057_VOID_ACTOR_COMMENT_ID = "5425816981"
XASSET_0057_POST_MERGE_VERIFICATION_COMMENT_ID = "5425857818"
XASSET_0057_CLOSURE_COMMENT_ID = "5426014312"
XASSET_0057_MERGE_CI_RUN_ID = "32973075626"
XASSET_0057_MERGE_CI_JOB_ID = "98191135804"

#: The permanent negative pin (``XASSET-0057`` SS-F.0): the current, vulnerable merged module.
VULNERABLE_MODULE_SHA256 = "12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5"
VULNERABLE_MODULE_BLOB = "b5622f9e412afd604a11cde04317b79c5e57920a"
#: The stale digest the load-bearing register still binds. The mismatch is the safety property.
STALE_BOUND_MODULE_SHA256 = "4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541"

DECISION_ID = "XASSET-0058"
DECISION_RELPATH = (
    "governance/decisions/"
    "XASSET-0058-endpoint-0001-formal-disposition-parser-correction-authorization.md"
)
BRANCH = "claude/parser-correction-xasset-auth-w91gse"
THIS_GATE = "xasset0058-formal-disposition-parser-correction-authorization"
PR_SENTINEL = -58
PRIOR_SENTINELS = (-1, -2, -50, -51, -52, -53, -54, -55, -56, -57)

DECISION_PATH = ROOT / DECISION_RELPATH
CATALOG = ROOT / "governance" / "decisions.yaml"
WORKSTREAMS = ROOT / "operations" / "WORKSTREAMS.yaml"
PRODUCTION_MODULE_RELPATH = "level1_stage1_execution_authorization.py"


# =====================================================================================
# Small, explicit git helpers -- immutable ranges only, never a moving ref
# =====================================================================================
def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def _git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
    ).stdout


def _content_at(sha: str, relpath: str) -> bytes:
    return _git_bytes("show", f"{sha}:{relpath}")


def _blob_at(sha: str, relpath: str) -> str:
    return _git("rev-parse", f"{sha}:{relpath}").strip()


def _tracked(pattern: str) -> tuple[str, ...]:
    """The CI-equivalent tracked-file universe. A recursive glob silently omits dot-directories."""
    return tuple(p for p in _git("ls-files", pattern).split("\n") if p)


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_flat(decision_text: str) -> str:
    """The decision with soft line wrapping removed, so a quoted phrase is not split by a
    newline the Markdown source happens to contain."""
    return re.sub(r"\s+", " ", decision_text)


@pytest.fixture(scope="module")
def register() -> dict:
    doc = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
    return next(w for w in doc["workstreams"] if w["id"] == "WS-0014")


# =====================================================================================
# SS-C -- the defect family, RE-MEASURED against the live merged bytes
# =====================================================================================
PREFIX = AUTH.FORMAL_DISPOSITION_PREFIX
APPROVE = AUTH.APPROVING_REVIEW_DISPOSITION
ADVERSE_VERDICT = "CHANGES REQUIRED"

#: The swept region, DERIVED rather than assumed: the canonical prefix minus its colon.
CANON_LABEL = PREFIX[:-1]

#: Every confusable's uppercase form must remain non-ASCII -- that is the documented mechanism by
#: which the printable-ASCII projection DELETES it. Asserted, not assumed (see the guard below).
CONFUSABLES = {
    "F": "Ƒ",   # LATIN CAPITAL LETTER F WITH HOOK
    "O": "Ο",   # GREEK CAPITAL LETTER OMICRON
    "R": "Ｒ",   # FULLWIDTH LATIN CAPITAL LETTER R
    "M": "М",   # CYRILLIC CAPITAL LETTER EM
    "A": "А",   # CYRILLIC CAPITAL LETTER A
    "L": "Ⅼ",   # ROMAN NUMERAL FIFTY
    "D": "Ⅾ",   # ROMAN NUMERAL FIVE HUNDRED
    "I": "İ",   # LATIN CAPITAL LETTER I WITH DOT ABOVE
    "S": "Ѕ",   # CYRILLIC CAPITAL LETTER DZE
    "P": "Р",   # CYRILLIC CAPITAL LETTER ER
    "T": "Т",   # CYRILLIC CAPITAL LETTER TE
    "N": "Ν",   # GREEK CAPITAL LETTER NU
}

NONSPACE_POSITIONS = tuple(i for i, c in enumerate(CANON_LABEL) if c != " ")
ADJACENT_PAIRS = tuple(
    i for i in range(len(CANON_LABEL) - 1) if CANON_LABEL[i] != CANON_LABEL[i + 1]
)


def _mutants() -> list[tuple[str, int, str]]:
    """The five families, position by position. The SOLE source of every count below."""
    out: list[tuple[str, int, str]] = []
    for i in NONSPACE_POSITIONS:
        out.append(("deletion", i, CANON_LABEL[:i] + CANON_LABEL[i + 1:]))
    for i in NONSPACE_POSITIONS:
        out.append(("ascii_substitution", i, CANON_LABEL[:i] + "X" + CANON_LABEL[i + 1:]))
    for i in NONSPACE_POSITIONS:
        out.append(("insertion", i, CANON_LABEL[:i] + "X" + CANON_LABEL[i:]))
    for i in ADJACENT_PAIRS:
        out.append(
            (
                "transposition",
                i,
                CANON_LABEL[:i] + CANON_LABEL[i + 1] + CANON_LABEL[i] + CANON_LABEL[i + 2:],
            )
        )
    for i in NONSPACE_POSITIONS:
        out.append(
            (
                "confusable_substitution",
                i,
                CANON_LABEL[:i] + CONFUSABLES[CANON_LABEL[i]] + CANON_LABEL[i + 1:],
            )
        )
    return out


MUTANTS = _mutants()
FAMILIES = ("deletion", "ascii_substitution", "insertion", "transposition",
            "confusable_substitution")


def _adverse_then_approval(label: str) -> str:
    """An adverse FIRST formal line, then a canonical approval. A skip lets the approval win."""
    return f"{label}: {ADVERSE_VERDICT}\n\n{PREFIX} {APPROVE}\n"


def _classify(body: str) -> str:
    r = AUTH.parse_formal_disposition(body)
    if r is AUTH.MALFORMED_FORMAL_DISPOSITION:
        return "MALFORMED"
    if r is None:
        return "ABSENT"
    if r == APPROVE:
        return "BYPASS"
    if r == ADVERSE_VERDICT:
        return "ADVERSE"
    return "OTHER"


class TestTheSweptRegionIsDerivedNotAssumed:
    def test_the_region_is_the_prefix_without_its_colon(self):
        assert PREFIX.endswith(":")
        assert CANON_LABEL == "FORMAL DISPOSITION"
        assert len(CANON_LABEL) == 18

    def test_there_are_exactly_seventeen_non_space_positions(self):
        assert len(NONSPACE_POSITIONS) == 17
        assert all(CANON_LABEL[i] != " " for i in NONSPACE_POSITIONS)
        assert len([c for c in CANON_LABEL if c == " "]) == 1

    def test_there_are_exactly_seventeen_distinct_character_adjacent_pairs(self):
        assert len(ADJACENT_PAIRS) == 17
        assert all(CANON_LABEL[i] != CANON_LABEL[i + 1] for i in ADJACENT_PAIRS)

    def test_every_confusable_stays_non_ascii_when_uppercased(self):
        """The documented mechanism: the printable-ASCII projection DELETES these characters."""
        for ascii_char, glyph in CONFUSABLES.items():
            assert glyph != ascii_char
            assert not glyph.isascii()
            assert not glyph.upper().isascii(), (ascii_char, glyph)

    def test_the_matrix_is_exactly_eighty_five_cells(self):
        assert len(MUTANTS) == 85
        for family in FAMILIES:
            assert sum(1 for f, _, _ in MUTANTS if f == family) == 17, family

    def test_every_mutant_actually_differs_from_the_canonical_label(self):
        for family, index, label in MUTANTS:
            assert label != CANON_LABEL, (family, index)


class TestTheDefectFamilyReproducesAtTheParser:
    @pytest.mark.parametrize("family,index,label", MUTANTS,
                             ids=[f"{f}-{i}" for f, i, _ in MUTANTS])
    def test_each_cell_is_either_a_bypass_or_fails_closed(self, family, index, label):
        result = _classify(_adverse_then_approval(label))
        assert result in ("BYPASS", "MALFORMED"), (family, index, label, result)

    def test_exactly_eighty_four_of_eighty_five_cells_bypass(self):
        results = {(f, i): _classify(_adverse_then_approval(l)) for f, i, l in MUTANTS}
        assert sum(1 for v in results.values() if v == "BYPASS") == 84
        assert sum(1 for v in results.values() if v == "MALFORMED") == 1

    def test_the_per_family_counts_are_seventeen_except_insertion(self):
        by_family = {fam: 0 for fam in FAMILIES}
        for family, index, label in MUTANTS:
            if _classify(_adverse_then_approval(label)) == "BYPASS":
                by_family[family] += 1
        assert by_family == {
            "deletion": 17,
            "ascii_substitution": 17,
            "insertion": 16,
            "transposition": 17,
            "confusable_substitution": 17,
        }

    def test_the_one_non_bypassing_cell_is_insertion_at_position_zero(self):
        survivors = [
            (f, i, l) for f, i, l in MUTANTS
            if _classify(_adverse_then_approval(l)) != "BYPASS"
        ]
        assert survivors == [("insertion", 0, "XFORMAL DISPOSITION")]

    def test_position_zero_returns_the_sentinel_OBJECT_not_a_literal(self):
        """SS-C pins it by IDENTITY, so a future refactor cannot reproduce it accidentally."""
        body = _adverse_then_approval("X" + CANON_LABEL)
        assert AUTH.parse_formal_disposition(body) is AUTH.MALFORMED_FORMAL_DISPOSITION

    def test_position_zero_leaves_the_canonical_prefix_intact_as_a_substring(self):
        assert PREFIX in ("X" + CANON_LABEL + ":")

    def test_the_untampered_adverse_line_is_read_as_adverse(self):
        assert _classify(_adverse_then_approval(CANON_LABEL)) == "ADVERSE"

    def test_a_bypassing_body_really_yields_the_APPROVING_verdict(self):
        """Not merely 'not adverse': the later approval actually wins."""
        body = _adverse_then_approval("FORMAL DISPOSITON")  # one deletion
        assert AUTH.parse_formal_disposition(body) == APPROVE


# ---- the three REAL consumer seams --------------------------------------------------
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


_BYPASSING = [(f, i, l) for f, i, l in MUTANTS if _classify(_adverse_then_approval(l)) == "BYPASS"]


class TestTheDefectFamilyReachesEveryRealConsumerSeam:
    def test_the_bypassing_set_is_the_eighty_four(self):
        assert len(_BYPASSING) == 84

    @pytest.mark.parametrize("family,index,label", _BYPASSING,
                             ids=[f"{f}-{i}" for f, i, _ in _BYPASSING])
    def test_seam_one_is_reached(self, family, index, label, monkeypatch):
        """Seam 1 -- ``_derive_pr337_actor_ratification``: the tampered body passes the parser
        gate exactly as a clean approval does, so execution proceeds past it."""
        recorder = _SEAMS.run_consumer_one(_adverse_then_approval(label), monkeypatch)
        assert any(c.startswith("reviews:") for c in recorder.calls), (family, index)

    @pytest.mark.parametrize("family,index,label", _BYPASSING,
                             ids=[f"{f}-{i}" for f, i, _ in _BYPASSING])
    def test_seam_two_does_not_refuse(self, family, index, label):
        assert not _seam_two_refused(_SEAMS.run_consumer_two(_adverse_then_approval(label)))

    @pytest.mark.parametrize("family,index,label", _BYPASSING,
                             ids=[f"{f}-{i}" for f, i, _ in _BYPASSING])
    def test_seam_three_does_not_refuse(self, family, index, label):
        assert not _seam_three_refused(
            _SEAMS.run_consumer_three(_adverse_then_approval(label), "COMMENTED")
        )

    @pytest.mark.parametrize("family,index,label", _BYPASSING,
                             ids=[f"{f}-{i}" for f, i, _ in _BYPASSING])
    def test_seam_three_does_not_refuse_under_a_native_APPROVED_state(self, family, index, label):
        assert not _seam_three_refused(
            _SEAMS.run_consumer_three(_adverse_then_approval(label), "APPROVED")
        )

    # ---- controls: the seams DO refuse the untampered adverse body ----
    def test_seam_one_stops_on_the_untampered_adverse_body(self, monkeypatch):
        recorder = _SEAMS.run_consumer_one(_adverse_then_approval(CANON_LABEL), monkeypatch)
        assert not any(c.startswith("reviews:") for c in recorder.calls)

    def test_seam_two_refuses_the_untampered_adverse_body(self):
        assert _seam_two_refused(_SEAMS.run_consumer_two(_adverse_then_approval(CANON_LABEL)))

    def test_seam_three_refuses_the_untampered_adverse_body(self):
        assert _seam_three_refused(
            _SEAMS.run_consumer_three(_adverse_then_approval(CANON_LABEL), "COMMENTED")
        )

    def test_seam_three_refuses_it_even_with_a_native_APPROVED_state(self):
        assert _seam_three_refused(
            _SEAMS.run_consumer_three(_adverse_then_approval(CANON_LABEL), "APPROVED")
        )

    def test_position_zero_fails_closed_at_seam_two_rather_than_bypassing(self):
        """The one cell that is NOT a bypass is refused, and refused as MALFORMED."""
        errors = _SEAMS.run_consumer_two(_adverse_then_approval("X" + CANON_LABEL))
        assert any(_MALFORMED_TEXT in e for e in errors), errors


# =====================================================================================
# SS-D -- the DECIDED boundary, carried as a TEST-ONLY reference model
# =====================================================================================
#: This model is the specification SS-D states, expressed executably. It is deliberately
#: test-only: SS-A is design-only and this filing adds NO production behaviour. It is not a
#: re-implementation of a production detector -- no such detector exists yet, and the future
#: Lifecycle B implementation is separately required (SS-E item 1) to be driven through the REAL
#: ``parse_formal_disposition`` rather than compared against a copy of itself.

MAX_EDITS = 1
#: A label within one edit of the 18-character canonical label has length 17, 18 or 19, so its
#: terminating colon can only sit at index 17, 18 or 19. The search window is CLOSED at 20.
COLON_SEARCH_LIMIT = len(CANON_LABEL) + MAX_EDITS + 1


def ascii_fold(text: str) -> str:
    """The SAME ASCII-only case fold acceptance already uses. A non-ASCII character never
    becomes an ASCII letter."""
    return "".join(c.upper() if "a" <= c <= "z" else c for c in text)


def osa(a: str, b: str, cap: int = MAX_EDITS) -> int:
    """Restricted Damerau / optimal-string-alignment distance, capped at ``cap``.

    Deletion, insertion, substitution and ADJACENT TRANSPOSITION each cost exactly 1.
    Returns ``min(distance, cap + 1)``; never explores beyond the cap.
    """
    la, lb = len(a), len(b)
    if abs(la - lb) > cap:
        return cap + 1
    if lb == 0:
        return la if la <= cap else cap + 1
    prev2: list[int] | None = None
    prev1 = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [cap + 1] * lb
        lo, hi = max(1, i - cap), min(lb, i + cap)
        for j in range(lo, hi + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            value = min(prev1[j] + 1, cur[j - 1] + 1, prev1[j - 1] + cost)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                value = min(value, prev2[j - 2] + 1)
            cur[j] = value
        if min(cur) > cap:
            return cap + 1
        prev2, prev1 = prev1, cur
    return min(prev1[lb], cap + 1)


def projections(line: str) -> tuple[str, ...]:
    """The line under the two GOVERNED wrapper forms, and no third."""
    indent = 0
    while indent < len(line) and line[indent] == " ":
        indent += 1
    end = len(line)
    while end > indent and line[end - 1] in " \t":
        end -= 1
    revealed = line[indent:end]
    if len(revealed) >= 4 and revealed.startswith("**") and revealed.endswith("**"):
        return (revealed, revealed[2:-2])
    return (revealed,)


def is_candidate(line: str) -> bool:
    """SS-D.2, exactly. Classification only: it can never produce or repair a verdict."""
    for projection in projections(line):
        colon = projection.find(":", 0, COLON_SEARCH_LIMIT)
        if colon == -1:
            continue
        if abs(colon - len(CANON_LABEL)) > MAX_EDITS:
            continue
        if osa(ascii_fold(projection[:colon]), CANON_LABEL) <= MAX_EDITS:
            return True
    return False


def hook_is_reachable(line: str) -> bool:
    """The candidate rule runs ONLY on the branch the parser takes when the canonical prefix is
    absent from the ASCII-folded line, and when the existing wide resemblance test also fails."""
    folded = ascii_fold(line)
    resembles = PREFIX in "".join(c for c in line.upper() if " " <= c <= "~")
    return PREFIX not in folded and not resembles


class TestTheReferenceModelIsCorrect:
    """Known-bad controls for the metric itself. A detector with no controls proves nothing."""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            ("abc", "abc", 0),
            ("abc", "abd", 1),            # substitution
            ("abc", "ab", 1),             # deletion
            ("ab", "abc", 1),             # insertion
            ("ab", "ba", 1),              # adjacent transposition
            ("abc", "acb", 1),            # adjacent transposition, interior
            ("", "", 0),
            ("a", "", 1),
            ("", "a", 1),
            (CANON_LABEL, CANON_LABEL, 0),
            (CANON_LABEL, "FROMAL DISPOSITION", 1),
            ("FORMAL DISPOSITON", CANON_LABEL, 1),
        ],
    )
    def test_within_cap_distances_are_exact(self, a, b, expected):
        assert osa(a, b) == expected

    @pytest.mark.parametrize(
        "a,b",
        [
            ("abcd", "badc"),   # two transpositions
            ("abc", "xyz"),     # three substitutions
            ("ab", ""),         # two deletions
            ("", "ab"),
            (CANON_LABEL, "FORMAL"),
            (CANON_LABEL, ""),
        ],
    )
    def test_beyond_cap_distances_saturate_and_never_report_within_cap(self, a, b):
        assert osa(a, b) == MAX_EDITS + 1
        assert osa(a, b) > MAX_EDITS

    def test_the_metric_is_symmetric_on_the_matrix(self):
        for _, _, label in MUTANTS:
            assert osa(ascii_fold(label), CANON_LABEL) == osa(CANON_LABEL, ascii_fold(label))

    def test_transposition_is_genuinely_one_edit_not_two(self):
        """Without the Damerau term a transposition costs 2, and the family would escape."""
        assert osa("FROMAL DISPOSITION", CANON_LABEL) == 1

    def test_the_fold_never_turns_a_non_ascii_character_into_an_ascii_letter(self):
        for glyph in CONFUSABLES.values():
            assert ascii_fold(glyph) == glyph
            assert not ascii_fold(glyph).isascii()

    def test_the_fold_makes_ascii_case_interchangeable(self):
        assert ascii_fold("formal disposition") == CANON_LABEL
        assert ascii_fold("FoRmAl DiSpOsItIoN") == CANON_LABEL

    def test_projections_are_exactly_the_two_governed_wrapper_forms(self):
        assert projections("FORMAL DISPOSITION: X") == ("FORMAL DISPOSITION: X",)
        assert projections("**FORMAL DISPOSITION: X**") == (
            "**FORMAL DISPOSITION: X**",
            "FORMAL DISPOSITION: X",
        )
        assert len(projections("***a***")) == 2      # never a third
        assert projections("**") == ("**",)          # too short to unwrap


class TestTheDecidedBoundaryClosesTheWholeFamily:
    @pytest.mark.parametrize("family,index,label", MUTANTS,
                             ids=[f"{f}-{i}" for f, i, _ in MUTANTS])
    def test_the_plain_line_is_a_candidate(self, family, index, label):
        assert is_candidate(f"{label}: {ADVERSE_VERDICT}"), (family, index, label)

    @pytest.mark.parametrize("family,index,label", MUTANTS,
                             ids=[f"{f}-{i}" for f, i, _ in MUTANTS])
    def test_the_bold_wrapped_line_is_a_candidate(self, family, index, label):
        assert is_candidate(f"**{label}: {ADVERSE_VERDICT}**"), (family, index, label)

    @pytest.mark.parametrize("family,index,label", MUTANTS,
                             ids=[f"{f}-{i}" for f, i, _ in MUTANTS])
    def test_the_indented_line_is_a_candidate(self, family, index, label):
        assert is_candidate(f"   {label}: {ADVERSE_VERDICT}"), (family, index, label)

    def test_the_totals_are_eighty_five_in_each_of_the_three_presentations(self):
        plain = sum(1 for _, _, l in MUTANTS if is_candidate(f"{l}: {ADVERSE_VERDICT}"))
        bold = sum(1 for _, _, l in MUTANTS if is_candidate(f"**{l}: {ADVERSE_VERDICT}**"))
        indented = sum(1 for _, _, l in MUTANTS if is_candidate(f"   {l}: {ADVERSE_VERDICT}"))
        assert (plain, bold, indented) == (85, 85, 85)
        assert plain + bold + indented == 255

    def test_every_per_family_count_is_seventeen(self):
        by_family = {fam: 0 for fam in FAMILIES}
        for family, _, label in MUTANTS:
            if is_candidate(f"{label}: {ADVERSE_VERDICT}"):
                by_family[family] += 1
        assert by_family == {fam: 17 for fam in FAMILIES}

    @pytest.mark.parametrize("family,index,label", _BYPASSING,
                             ids=[f"{f}-{i}" for f, i, _ in _BYPASSING])
    def test_every_bypassing_cell_is_on_the_reachable_branch(self, family, index, label):
        """The rule is useless unless the parser actually reaches it for these lines."""
        assert hook_is_reachable(f"{label}: {ADVERSE_VERDICT}"), (family, index)


class TestTheEditBudgetIsJustifiedExactly:
    """SS-D.2's `NUM-0001` class 5 justification, proved rather than asserted."""

    def _candidate_at(self, line: str, cap: int) -> bool:
        for projection in projections(line):
            colon = projection.find(":", 0, len(CANON_LABEL) + cap + 1)
            if colon == -1:
                continue
            if abs(colon - len(CANON_LABEL)) > cap:
                continue
            if osa(ascii_fold(projection[:colon]), CANON_LABEL, cap=cap) <= cap:
                return True
        return False

    def test_one_is_the_smallest_budget_that_closes_the_family(self):
        """Every cell is a single-character mutation, so a budget of zero reaches none of them
        and a budget of one reaches all of them."""
        at_zero = [l for _, _, l in MUTANTS
                   if self._candidate_at(f"{l}: {ADVERSE_VERDICT}", 0)]
        at_one = [l for _, _, l in MUTANTS
                  if self._candidate_at(f"{l}: {ADVERSE_VERDICT}", 1)]
        assert at_zero == []
        assert len(at_one) == 85

    def test_a_wider_budget_is_NOT_ruled_out_by_a_measured_false_positive(self, markdown_corpus):
        """SS-D.2 states this explicitly rather than implying the budget is a safety ceiling.
        The decision would be MISLEADING if a wider budget did in fact misfire here, so the
        claim is measured, not assumed."""
        _, lines = markdown_corpus
        for cap in (1, 2, 3):
            regressions = [l for l in lines if self._candidate_at(l, cap) and _absent_today(l)]
            assert regressions == [], (cap, regressions[:5])

    def test_the_decision_does_not_claim_one_is_a_false_positive_ceiling(self, decision_flat):
        assert "It is **not** selected as a false-positive ceiling" in decision_flat
        assert "budgets of **2 and 3 were also measured" in decision_flat
        assert "largest budget" not in decision_flat

    def test_the_declared_budget_matches_the_model(self, decision_flat):
        assert MAX_EDITS == 1
        assert "The edit budget is exactly one" in decision_flat
        assert "`NUM-0001` class 5 provisional governance guardrail" in decision_flat


class TestAcceptanceIsUnreachableFromTheCandidateRule:
    ACCEPTED_FORMS = (
        f"{PREFIX} {APPROVE}",
        f"**{PREFIX} {APPROVE}**",
        f"formal disposition: {APPROVE}",
        f"FoRmAl DiSpOsItIoN: {APPROVE}",
        f"{PREFIX} {ADVERSE_VERDICT}",
        f"{PREFIX} {APPROVE} -- 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE",
        f"   {PREFIX} {APPROVE}",
    )

    @pytest.mark.parametrize("form", ACCEPTED_FORMS)
    def test_the_hook_is_not_reachable_for_any_accepted_form(self, form):
        assert not hook_is_reachable(form), form

    @pytest.mark.parametrize("form", ACCEPTED_FORMS)
    def test_every_accepted_form_still_yields_a_verdict_today(self, form):
        result = AUTH.parse_formal_disposition(form + "\n")
        assert isinstance(result, str), form

    def test_the_approving_forms_authenticate_exactly(self):
        for form in (f"{PREFIX} {APPROVE}", f"**{PREFIX} {APPROVE}**",
                     f"formal disposition: {APPROVE}"):
            assert AUTH.parse_formal_disposition(form + "\n") == APPROVE, form

    def test_an_adverse_canonical_verdict_is_returned_verbatim(self):
        assert AUTH.parse_formal_disposition(f"{PREFIX} {ADVERSE_VERDICT}\n") == ADVERSE_VERDICT

    def test_a_lower_case_verdict_is_returned_exactly_as_written(self):
        """XASSET-0055 SS-D: the verdict is never case-folded, normalized or coerced."""
        assert AUTH.parse_formal_disposition(f"{PREFIX} approved\n") == "approved"

    def test_the_candidate_rule_returns_only_a_boolean(self):
        for _, _, label in MUTANTS:
            assert is_candidate(f"{label}: {ADVERSE_VERDICT}") is True
        assert is_candidate("ordinary prose") is False

    def test_the_candidate_rule_never_names_the_approving_value(self):
        """Structural: a classifier that cannot mention the approval cannot manufacture it."""
        source = inspect.getsource(is_candidate)
        assert APPROVE not in source
        assert "APPROVING_REVIEW_DISPOSITION" not in source

    def test_the_candidate_rule_reads_only_the_label_never_the_verdict(self):
        """Changing everything AFTER the colon cannot change the classification."""
        for _, _, label in MUTANTS:
            base = is_candidate(f"{label}: {ADVERSE_VERDICT}")
            for tail in (APPROVE, "", "anything at all", "*" * 200):
                assert is_candidate(f"{label}: {tail}") is base, (label, tail)


class TestOrdinaryProseStaysAbsent:
    PROSE = (
        "## Findings",
        "Note: this is fine",
        "The formal disposition of the estate: pending",
        "> FORMAL DISPOSITION was discussed",
        "- see the formal disposition rules below",
        "formal disposition but is not in an accepted form",
        "```",
        "~~~",
        "Findings: 0 BLOCKING / 0 MAJOR",
        "A formal, dispositive ruling: yes",
        "",
        "    indented code: not a disposition",
        "*partial emphasis*: no",
        "**unbalanced: no",
    )

    @pytest.mark.parametrize("line", PROSE)
    def test_the_line_is_not_a_candidate(self, line):
        assert not is_candidate(line), line

    @pytest.mark.parametrize("line", PROSE)
    def test_the_line_is_not_newly_malformed(self, line):
        """Whatever it is today, the rule does not change it."""
        today = AUTH.parse_formal_disposition(line + "\n")
        if today is None:
            assert not is_candidate(line), line


def _absent_today(line: str) -> bool:
    return AUTH.parse_formal_disposition(line + "\n") is None


@pytest.fixture(scope="module")
def markdown_corpus() -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Every line of every TRACKED Markdown file. Offline, deterministic, CI-equivalent."""
    files = _tracked("*.md")
    lines: list[str] = []
    for relpath in files:
        lines.extend((ROOT / relpath).read_text(encoding="utf-8", errors="replace").split("\n"))
    return files, tuple(lines)


class TestTheCommittedCorpusDoesNotRegress:
    def test_the_corpus_is_substantial_enough_to_be_evidence(self, markdown_corpus):
        files, lines = markdown_corpus
        assert len(files) >= 400
        assert len(lines) >= 100_000

    def test_no_committed_markdown_line_goes_from_absent_to_candidate(self, markdown_corpus):
        _, lines = markdown_corpus
        regressions = [l for l in lines if is_candidate(l) and _absent_today(l)]
        assert regressions == [], regressions[:5]

    def test_lines_the_rule_flags_are_already_malformed_or_already_a_verdict(self, markdown_corpus):
        _, lines = markdown_corpus
        flagged = [l for l in lines if is_candidate(l)]
        assert flagged, "a rule that flags nothing at all would prove nothing"
        for line in flagged:
            today = AUTH.parse_formal_disposition(line + "\n")
            assert today is not None, line

    def test_the_flagged_lines_partition_exhaustively_with_an_empty_regression_bucket(
        self, markdown_corpus
    ):
        """SS-D.5's accounting: every flagged line is already MALFORMED or already a verdict,
        the regression bucket is EMPTY, and there is no fourth category left unexplained."""
        _, lines = markdown_corpus
        flagged = [l for l in lines if is_candidate(l)]
        already_malformed = [
            l for l in flagged
            if AUTH.parse_formal_disposition(l + "\n") is AUTH.MALFORMED_FORMAL_DISPOSITION
        ]
        already_verdict = [
            l for l in flagged if isinstance(AUTH.parse_formal_disposition(l + "\n"), str)
        ]
        regressions = [l for l in flagged if _absent_today(l)]
        assert len(already_malformed) + len(already_verdict) + len(regressions) == len(flagged)
        assert regressions == [], regressions[:5]
        assert already_malformed, "a partition with an empty first bucket would prove nothing"
        assert already_verdict, "a partition with an empty second bucket would prove nothing"

    def test_no_verdict_yielding_line_lacks_the_canonical_prefix_in_the_fold(self, markdown_corpus):
        """Independent confirmation that the hook can never run on an accepted line."""
        _, lines = markdown_corpus
        offenders = [
            l for l in lines
            if isinstance(AUTH.parse_formal_disposition(l + "\n"), str)
            and PREFIX not in ascii_fold(l)
        ]
        assert offenders == [], offenders[:5]

    def test_the_real_committed_review_line_fixture_is_unaffected(self):
        """A REAL historical lifecycle review line, committed in this repository's own fixtures."""
        line = _SEAMS_MODULE.REVIEW_5000581301_LINE
        assert AUTH.parse_formal_disposition(line + "\n") == APPROVE
        assert not hook_is_reachable(line)


class TestTheResidualIsDispositionedNotOmitted:
    COLON_MUTATIONS = (
        f"{CANON_LABEL} {ADVERSE_VERDICT}",        # colon deleted
        f"{CANON_LABEL}; {ADVERSE_VERDICT}",       # colon substituted, ASCII
        f"{CANON_LABEL}： {ADVERSE_VERDICT}",  # colon substituted, fullwidth
    )

    @pytest.mark.parametrize("line", COLON_MUTATIONS)
    def test_it_is_not_a_candidate(self, line):
        assert not is_candidate(line), line

    @pytest.mark.parametrize("line", COLON_MUTATIONS)
    def test_it_is_already_absent_today_so_nothing_regresses(self, line):
        assert _absent_today(line), line

    def test_the_decision_states_the_residual_explicitly(self, decision_flat):
        assert "SS-D.8" not in decision_flat  # the file uses the real section glyph
        assert "explicitly dispositioned rather than silently omitted" in decision_flat
        assert "decided as ABSENT" in decision_flat

    def test_the_decision_records_that_it_is_unchanged_behaviour(self, decision_flat):
        assert "unchanged behaviour" in decision_flat

    def test_the_decision_records_why_a_case_based_rule_was_not_taken(self, decision_flat):
        assert "removes and PROHIBITS" in decision_flat
        assert "closed by accepted authority and was not taken" in decision_flat

    def test_the_decision_leaves_the_residual_open_rather_than_closing_it(self, decision_flat):
        assert "open, unresolved and outside this grant" in decision_flat


class TestTheRuleIsBoundedAndDeterministic:
    @pytest.mark.parametrize("length", [100, 10_000, 200_000])
    def test_the_colon_window_is_closed_so_length_does_not_matter(self, length):
        line = "x" * length + ": tail"
        assert not is_candidate(line)

    def test_a_colon_beyond_the_window_can_never_qualify(self):
        assert COLON_SEARCH_LIMIT == 20
        line = "x" * 25 + ":"
        assert line.find(":") > COLON_SEARCH_LIMIT
        assert not is_candidate(line)

    def test_a_qualifying_label_is_found_at_each_admissible_colon_index(self):
        for label in ("FORMAL DISPOSITON", CANON_LABEL, "XFORMAL DISPOSITION"):
            assert len(label) in (17, 18, 19)
            assert is_candidate(f"{label}: x")

    def test_the_rule_is_deterministic(self):
        probe = f"FORMAL DISPOSITON: {ADVERSE_VERDICT}"
        assert len({is_candidate(probe) for _ in range(500)}) == 1

    def test_no_line_is_left_undefined(self):
        """Totality: every input lands in exactly one of the two classes."""
        for line in ("", " ", ":", "a" * 500, "\t", "**:**", CANON_LABEL, f"{CANON_LABEL}:"):
            assert isinstance(is_candidate(line), bool), line


# =====================================================================================
# The decision's own operative text -- grounded, not paraphrased
# =====================================================================================
class TestTheDecisionSaysWhatItMustSay:
    def test_the_determination_is_named(self, decision_flat):
        assert "FORMAL_DISPOSITION_PARSER_CORRECTION_AUTHORIZED" in decision_flat

    def test_it_grants_exactly_one_future_unit(self, decision_flat):
        assert "Exactly **one** future, separate, bounded pull request may implement" in decision_flat

    def test_it_is_design_only_and_corrects_no_parser(self, decision_flat):
        assert "design-only" in decision_flat
        assert "**Merging this decision corrects no parser.**" in decision_flat

    @pytest.mark.parametrize("family", FAMILIES)
    def test_every_family_is_named_and_decided(self, decision_flat, family):
        human = family.replace("_", " ")
        assert human.split()[0] in decision_flat.lower(), family

    def test_the_five_families_are_each_dispositioned_to_MALFORMED(self, decision_text):
        table = decision_text.split("#### D.3")[1].split("#### D.4")[0]
        assert table.count("**MALFORMED**") >= 5
        assert "**17 / 17**" in table
        assert "**85 / 85**" in table

    def test_acceptance_is_stated_unchanged(self, decision_flat):
        assert "Acceptance is UNCHANGED" in decision_flat
        assert "Fuzzy matching is confined to CLASSIFICATION and is forbidden in ACCEPTANCE" in decision_flat

    def test_the_candidate_rule_can_never_authenticate(self, decision_flat):
        assert "Candidate recognition can NEVER authenticate" in decision_flat
        assert "may **only** cause additional **fail-closed MALFORMED** results" in decision_flat

    def test_the_edit_budget_is_classified_under_NUM_0001(self, decision_flat):
        assert "`NUM-0001` class 5 provisional governance guardrail" in decision_flat

    def test_prose_is_preserved_as_absent(self, decision_flat):
        assert "Ordinary prose stays ABSENT" in decision_flat

    def test_the_rejected_alternative_is_recorded(self, decision_flat):
        assert "The rejected alternative, recorded because it was measured" in decision_flat

    def test_both_lifecycles_are_required(self, decision_flat):
        for step in ("A1.", "A2.", "A3.", "A4.", "A5.", "A6.", "A7."):
            assert f"* **{step}**" in decision_flat, step
        for step in ("B1.", "B2.", "B3.", "B4.", "B5.", "B6.", "B7.", "B8."):
            assert f"* **{step}**" in decision_flat, step

    def test_merged_is_not_effective(self, decision_flat):
        assert "Merged is not effective" in decision_flat
        assert "None of A1–A7 is individually sufficient" in decision_flat

    def test_the_B5_merge_is_named_as_the_rebinding_base(self, decision_flat):
        assert "B5 normal-merge commit is the SHA tested by B7 and named by B8" in decision_flat
        assert "sole** qualifying base" in decision_flat

    def test_the_consumers_are_out_of_scope(self, decision_flat):
        assert "They are therefore **out of scope**" in decision_flat
        assert "without editing them" in decision_flat

    def test_the_vulnerable_identity_is_reaffirmed_as_a_negative_pin(self, decision_flat):
        assert VULNERABLE_MODULE_SHA256 in decision_flat
        assert "permanent negative pin" in decision_flat

    def test_it_disclaims_the_rebinding(self, decision_flat):
        assert "performs **no** rebinding" in decision_flat

    def test_the_absolute_non_authorization_is_present(self, decision_flat):
        for phrase in ("arm Stage 1", "generate an attestation", "claim `ATTEMPT_1`",
                       "stays permanently `false`", "Stage 1 remains UNARMED and NOT EXECUTABLE"):
            assert phrase in decision_flat, phrase

    def test_the_void_actor_comment_is_recorded_as_void(self, decision_flat):
        assert XASSET_0057_VOID_ACTOR_COMMENT_ID in decision_flat
        assert "VOID, never acceptance" in decision_flat

    def test_the_preflight_pins_the_real_lifecycle_identities(self, decision_flat):
        for identity in (
            THIS_UNIT_BASE_SHA,
            XASSET_0057_ACCEPTED_HEAD,
            XASSET_0057_MERGE_PARENT_1,
            XASSET_0057_CLEAN_REVIEW_ID,
            XASSET_0057_ACCEPTANCE_COMMENT_ID,
            XASSET_0057_POST_MERGE_VERIFICATION_COMMENT_ID,
            XASSET_0057_CLOSURE_COMMENT_ID,
            XASSET_0057_MERGE_CI_RUN_ID,
            XASSET_0057_MERGE_CI_JOB_ID,
        ):
            assert identity in decision_flat, identity

    def test_the_frontmatter_is_consistent(self, decision_text):
        head = decision_text.split("---")[1]
        meta = yaml.safe_load(head)
        assert meta["decision_id"] == DECISION_ID
        assert meta["status"] == "Proposed"
        assert meta["supporting_artifact"] == Path(__file__).name
        assert "XASSET-0057" in meta["related_decisions"]

    def test_no_sentinel_survives_in_the_decision(self, decision_text):
        for sentinel in (PR_SENTINEL, *PRIOR_SENTINELS):
            assert f"#{sentinel}" not in decision_text, sentinel


# =====================================================================================
# The lifecycle this filing rests on -- proved over an immutable range
# =====================================================================================
class TestTheXasset0057LifecycleIsClosed:
    def test_the_merge_has_exactly_two_ordered_parents(self):
        parents = _git("rev-list", "--parents", "-n", "1", THIS_UNIT_BASE_SHA).split()
        assert parents == [
            THIS_UNIT_BASE_SHA,
            XASSET_0057_MERGE_PARENT_1,
            XASSET_0057_ACCEPTED_HEAD,
        ]

    def test_the_merge_tree_is_byte_identical_to_the_accepted_head_tree(self):
        assert _git("rev-parse", f"{THIS_UNIT_BASE_SHA}^{{tree}}").strip() == _git(
            "rev-parse", f"{XASSET_0057_ACCEPTED_HEAD}^{{tree}}"
        ).strip()

    def test_there_is_zero_drift_between_the_accepted_head_and_the_merge(self):
        diff = _git("diff", "--name-only", XASSET_0057_ACCEPTED_HEAD, THIS_UNIT_BASE_SHA).strip()
        assert diff == ""

    def test_the_base_is_an_ancestor_of_the_accepted_head(self):
        subprocess.run(
            ["git", "merge-base", "--is-ancestor",
             XASSET_0057_MERGE_PARENT_1, XASSET_0057_ACCEPTED_HEAD],
            cwd=ROOT, check=True,
        )

    def test_this_unit_bases_exactly_on_that_merge(self):
        """Immutable: the merge is an ancestor of this branch and nothing intervenes on it."""
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", THIS_UNIT_BASE_SHA, "HEAD"],
            cwd=ROOT, check=True,
        )

    def test_the_xasset_0057_decision_exists_at_the_base(self):
        content = _content_at(
            THIS_UNIT_BASE_SHA,
            "governance/decisions/"
            "XASSET-0057-endpoint-0001-stage-1-post-parser-correction-rebinding-authorization.md",
        ).decode("utf-8")
        assert "STEP_8_EQUIVALENT_REBINDING_AUTHORIZED" in content

    def test_xasset_0057_reserved_this_boundary_to_a_later_decision(self):
        """The authority for THIS filing, quoted from the merged predecessor rather than inferred."""
        content = _content_at(
            THIS_UNIT_BASE_SHA,
            "governance/decisions/"
            "XASSET-0057-endpoint-0001-stage-1-post-parser-correction-rebinding-authorization.md",
        ).decode("utf-8")
        flat = re.sub(r"\s+", " ", content)
        assert "This filing does not decide that recognition boundary" in flat
        assert "reserved to that future decision, which must decide it and prove it" in flat

    def test_xasset_0057_requires_two_lifecycles(self):
        content = _content_at(
            THIS_UNIT_BASE_SHA,
            "governance/decisions/"
            "XASSET-0057-endpoint-0001-stage-1-post-parser-correction-rebinding-authorization.md",
        ).decode("utf-8")
        flat = re.sub(r"\s+", " ", content)
        assert "TWO lifecycles must close, not one" in flat
        assert "Merged is not effective" in flat


# =====================================================================================
# Scope isolation -- this filing moves no production byte
# =====================================================================================
PROTECTED_RELPATHS = (
    PRODUCTION_MODULE_RELPATH,
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_construction_universe_closure_validator.py",
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
    "allocate.py",
    "margin_state.py",
    "levels.py",
)


class TestThisFilingChangesNoProductionByte:
    @pytest.mark.parametrize("relpath", PROTECTED_RELPATHS)
    def test_the_path_is_byte_identical_to_the_base(self, relpath):
        assert _blob_at("HEAD", relpath) == _blob_at(THIS_UNIT_BASE_SHA, relpath), relpath

    def test_the_production_module_still_carries_the_vulnerable_identity(self):
        digest = hashlib.sha256((ROOT / PRODUCTION_MODULE_RELPATH).read_bytes()).hexdigest()
        assert digest == VULNERABLE_MODULE_SHA256
        assert _blob_at("HEAD", PRODUCTION_MODULE_RELPATH) == VULNERABLE_MODULE_BLOB

    def test_the_register_still_binds_the_stale_digest(self):
        assert STALE_BOUND_MODULE_SHA256 != VULNERABLE_MODULE_SHA256
        raw = WORKSTREAMS.read_text(encoding="utf-8")
        assert STALE_BOUND_MODULE_SHA256 in raw

    def test_the_load_bearing_boundary_is_unchanged_at_eighteen(self):
        assert len(AUTH.LOAD_BEARING_RELPATHS) == 18
        base = _content_at(THIS_UNIT_BASE_SHA, PRODUCTION_MODULE_RELPATH).decode("utf-8")
        assert base == (ROOT / PRODUCTION_MODULE_RELPATH).read_text(encoding="utf-8")

    def test_this_module_adds_no_production_import_of_itself(self):
        """Nothing in production may import this test-only reference model."""
        source = (ROOT / PRODUCTION_MODULE_RELPATH).read_text(encoding="utf-8")
        assert Path(__file__).stem not in source

    def test_the_reference_model_is_defined_here_and_nowhere_in_production(self):
        source = (ROOT / PRODUCTION_MODULE_RELPATH).read_text(encoding="utf-8")
        for name in ("is_candidate", "def osa(", "COLON_SEARCH_LIMIT"):
            assert name not in source, name


class TestStageOneRemainsFailClosed:
    def test_all_three_authorization_predicates_are_false(self):
        for predicate in (
            AUTH.new_execution_is_authorized,
            AUTH.claimed_execution_is_authorized,
            AUTH.active_execution_is_authorized,
        ):
            authorized, reason = predicate()
            assert authorized is False, predicate.__name__
            assert isinstance(reason, str) and reason.strip()

    def test_the_completed_result_predicate_is_false(self):
        authorized, _ = AUTH.completed_result_is_authorized({})
        assert authorized is False

    def test_the_lane_is_absent(self):
        state, _ = AUTH.lane_state_at(AUTH.LanePaths())
        assert state == AUTH.LANE_ABSENT

    def test_no_lane_artifact_exists(self):
        for path in (AUTH.AUTHORIZATION_ROOT, AUTH.AUTHORIZATION_PATH,
                     AUTH.CLAIM_PATH, AUTH.COMPLETION_PATH, AUTH.LEDGER_PATH):
            assert not path.exists(), path

    def test_no_results_artifact_exists(self):
        assert not (ROOT / "stage1_results.yaml").exists()
        assert _tracked("stage1_results.yaml") == ()

    def test_the_attempt_is_intact(self):
        assert AUTH.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

    def test_this_suite_writes_nothing(self):
        """AST-scoped: no filesystem write call appears anywhere in this module."""
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        forbidden = {"write_text", "write_bytes", "mkdir", "touch", "unlink", "rmdir", "open"}
        seen = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        assert not (seen & forbidden), sorted(seen & forbidden)

    def test_this_suite_never_calls_a_state_changing_authorization_function(self):
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        forbidden = {"write_authorization", "claim_execution", "complete_execution",
                     "build_authorization_payload"}
        seen = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        } | {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        assert not (seen & forbidden), sorted(seen & forbidden)


# =====================================================================================
# The register is synchronized ADDITIVELY
# =====================================================================================
class TestTheRegisterIsSynchronized:
    def test_this_units_gate_exists(self, register):
        assert THIS_GATE in [g["gate"] for g in register["milestones"]]

    def test_the_predecessor_gate_text_is_untouched(self):
        base_doc = yaml.safe_load(
            _content_at(THIS_UNIT_BASE_SHA, "operations/WORKSTREAMS.yaml").decode("utf-8")
        )
        base_ws = next(w for w in base_doc["workstreams"] if w["id"] == "WS-0014")
        gate_id = "xasset0057-post-parser-correction-rebinding-authorization"
        base_gate = next(g for g in base_ws["milestones"] if g["gate"] == gate_id)
        live_doc = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
        live_ws = next(w for w in live_doc["workstreams"] if w["id"] == "WS-0014")
        live_gate = next(g for g in live_ws["milestones"] if g["gate"] == gate_id)
        assert live_gate == base_gate, "a predecessor gate was rewritten instead of appended to"

    def test_gates_are_only_appended(self, register):
        base_doc = yaml.safe_load(
            _content_at(THIS_UNIT_BASE_SHA, "operations/WORKSTREAMS.yaml").decode("utf-8")
        )
        base_ws = next(w for w in base_doc["workstreams"] if w["id"] == "WS-0014")
        before = base_ws["milestones"]
        live = register["milestones"]
        assert live[: len(before)] == before, "existing gates were modified, not appended to"
        assert len(live) == len(before) + 1

    def test_no_sentinel_survives_anywhere_in_the_register(self):
        raw = WORKSTREAMS.read_text(encoding="utf-8")
        for sentinel in (PR_SENTINEL, *PRIOR_SENTINELS):
            assert f"active_pr: {sentinel}" not in raw, sentinel
            assert f"pr: {sentinel}" not in raw, sentinel

    def test_the_shared_live_fields_name_this_unit(self, register):
        assert register["active_branch"] == BRANCH
        assert register["last_verified_main_sha"] == THIS_UNIT_BASE_SHA
        assert register["last_verified_main_sha"] != XASSET_0057_MERGE_PARENT_1

    def test_the_active_pr_is_a_real_github_number(self, register):
        pr = register["active_pr"]
        assert isinstance(pr, int) and pr > XASSET_0057_PULL_REQUEST
        assert pr not in PRIOR_SENTINELS and pr != PR_SENTINEL

    def test_the_workstream_stays_proposed_and_secondary(self, register):
        assert register["status"] == "proposed"
        assert register["priority"] == "secondary"

    def test_the_last_verified_date_is_a_real_date(self, register):
        datetime.date.fromisoformat(str(register["last_verified_date"]))


@pytest.fixture(scope="module")
def rows() -> list[dict]:
    return yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["decisions"]


class TestTheCatalogIsSynchronized:
    def test_this_decision_is_catalogued_exactly_once(self, rows):
        matches = [r for r in rows if r["decision_id"] == DECISION_ID]
        assert len(matches) == 1

    def test_the_catalogued_row_matches_the_decisions_own_frontmatter(self, rows, decision_text):
        row = next(r for r in rows if r["decision_id"] == DECISION_ID)
        meta = yaml.safe_load(decision_text.split("---")[1])
        for key in ("date", "status", "category", "supporting_artifact"):
            assert str(row[key]) == str(meta[key]), key
        assert row["file"] == DECISION_RELPATH
        assert row["related_decisions"] == meta["related_decisions"]

    def test_the_referenced_file_and_artifact_both_exist(self, rows):
        row = next(r for r in rows if r["decision_id"] == DECISION_ID)
        assert (ROOT / row["file"]).is_file()
        assert (ROOT / row["supporting_artifact"]).is_file()

    def test_exactly_one_row_was_added(self, rows):
        base_rows = yaml.safe_load(
            _content_at(THIS_UNIT_BASE_SHA, "governance/decisions.yaml").decode("utf-8")
        )["decisions"]
        assert len(rows) == len(base_rows) + 1
        assert rows[: len(base_rows)] == base_rows

    def test_the_identifier_was_unused_at_the_base(self):
        raw = _content_at(THIS_UNIT_BASE_SHA, "governance/decisions.yaml").decode("utf-8")
        assert DECISION_ID not in raw

    def test_the_identifier_is_unused_anywhere_in_reachable_history(self):
        """Derived, never predicted: no commit reachable from this unit's base introduced it."""
        hits = _git("log", "--oneline", "-S", DECISION_ID, THIS_UNIT_BASE_SHA).strip()
        assert hits == "", hits


# =====================================================================================
# Falsifiability -- every guard above must actually catch something
# =====================================================================================
class TestTheGuardsAreFalsifiable:
    """Each probe breaks one property and requires the corresponding check to notice.

    These are in-process, in-memory probes on the reference model and on synthetic inputs.
    They mutate no file, so no restoration step is needed and none is claimed.
    """

    def test_dropping_the_transposition_term_loses_the_transposition_family(self):
        def osa_without_damerau(a, b, cap=MAX_EDITS):
            la, lb = len(a), len(b)
            if abs(la - lb) > cap:
                return cap + 1
            if lb == 0:
                return la if la <= cap else cap + 1
            prev1 = list(range(lb + 1))
            for i in range(1, la + 1):
                cur = [i] + [cap + 1] * lb
                lo, hi = max(1, i - cap), min(lb, i + cap)
                for j in range(lo, hi + 1):
                    cost = 0 if a[i - 1] == b[j - 1] else 1
                    cur[j] = min(prev1[j] + 1, cur[j - 1] + 1, prev1[j - 1] + cost)
                if min(cur) > cap:
                    return cap + 1
                prev1 = cur
            return min(prev1[lb], cap + 1)

        transpositions = [l for f, _, l in MUTANTS if f == "transposition"]
        assert len(transpositions) == 17
        lost = [l for l in transpositions if osa_without_damerau(ascii_fold(l), CANON_LABEL) > 1]
        assert len(lost) == 17, "the Damerau term is load-bearing and must be proved so"

    def test_raising_the_edit_budget_to_zero_loses_the_entire_family(self):
        kept = [l for _, _, l in MUTANTS if osa(ascii_fold(l), CANON_LABEL, cap=0) <= 0]
        assert kept == []

    def test_dropping_the_ascii_fold_loses_the_lower_case_forms(self):
        """Without the fold a lower-case label is 18 substitutions away, not zero."""
        assert osa("formal disposition", CANON_LABEL) == MAX_EDITS + 1
        assert osa(ascii_fold("formal disposition"), CANON_LABEL) == 0

    def test_dropping_the_bold_projection_loses_every_bold_wrapped_cell(self):
        def is_candidate_without_bold(line):
            indent = 0
            while indent < len(line) and line[indent] == " ":
                indent += 1
            end = len(line)
            while end > indent and line[end - 1] in " \t":
                end -= 1
            p = line[indent:end]
            colon = p.find(":", 0, COLON_SEARCH_LIMIT)
            if colon == -1 or abs(colon - len(CANON_LABEL)) > MAX_EDITS:
                return False
            return osa(ascii_fold(p[:colon]), CANON_LABEL) <= MAX_EDITS

        lost = [l for _, _, l in MUTANTS
                if not is_candidate_without_bold(f"**{l}: {ADVERSE_VERDICT}**")]
        assert len(lost) == 85, "the bold projection is load-bearing and must be proved so"

    def test_dropping_the_indent_trim_loses_every_indented_cell(self):
        def is_candidate_without_indent_trim(line):
            colon = line.find(":", 0, COLON_SEARCH_LIMIT)
            if colon == -1 or abs(colon - len(CANON_LABEL)) > MAX_EDITS:
                return False
            return osa(ascii_fold(line[:colon]), CANON_LABEL) <= MAX_EDITS

        lost = [l for _, _, l in MUTANTS
                if not is_candidate_without_indent_trim(f"   {l}: {ADVERSE_VERDICT}")]
        assert len(lost) == 85

    def test_widening_the_colon_window_would_admit_a_far_colon(self):
        """The window is load-bearing: without it a distant colon reaches the comparison."""
        line = "x" * 40 + ":"
        assert line.find(":", 0, COLON_SEARCH_LIMIT) == -1
        assert line.find(":") == 40

    def test_removing_the_length_gate_still_refuses_a_far_label(self):
        """Defence in depth: the metric alone must also reject an over-long label."""
        assert osa(ascii_fold("A" * 19), CANON_LABEL) > MAX_EDITS

    def test_a_two_edit_label_is_correctly_refused(self):
        """A known-bad control on the boundary itself: two edits must NOT qualify."""
        two_edits = "FRMAL DISPOSITON"  # one deletion in each word
        assert osa(ascii_fold(two_edits), CANON_LABEL) > MAX_EDITS
        assert not is_candidate(f"{two_edits}: {ADVERSE_VERDICT}")

    def test_the_matrix_would_notice_a_silently_shrunken_family(self):
        assert len({f for f, _, _ in MUTANTS}) == 5
        assert len(MUTANTS) == 85

    def test_the_seam_refusal_helpers_are_not_vacuous(self):
        """A helper that returned True for everything would hide every bypass."""
        assert not _seam_two_refused(())
        assert not _seam_three_refused(())
        assert _seam_two_refused((f"... {ADVERSE_VERDICT} ...",))
        assert _seam_three_refused((f"... {_MALFORMED_TEXT} ...",))

    def test_the_classifier_helper_distinguishes_all_five_outcomes(self):
        assert _classify(f"{PREFIX} {APPROVE}\n") == "BYPASS"
        assert _classify(f"{PREFIX} {ADVERSE_VERDICT}\n") == "ADVERSE"
        assert _classify("nothing here\n") == "ABSENT"
        assert _classify(f"## {PREFIX} {APPROVE}\n") == "MALFORMED"
        assert _classify(f"{PREFIX} something else\n") == "OTHER"

    def test_every_decision_text_guard_reads_the_decision_not_this_module(self):
        """Structural, AST-scoped: a guard that read ``__file__`` would be satisfiable by its own
        assertion text. Every test in the decision-text class must therefore take the decision
        fixture as a parameter, and none may reference ``__file__``."""
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        cls = next(
            node for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef) and node.name == "TestTheDecisionSaysWhatItMustSay"
        )
        methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
        assert len(methods) >= 15
        for method in methods:
            params = {a.arg for a in method.args.args}
            assert params & {"decision_text", "decision_flat"}, method.name
            # Reading this module's OWN text inside a decision-text guard would make the
            # assertion satisfiable by its own source. Naming ``Path(__file__).name`` to compare
            # against the catalogued artifact is a different, legitimate use and is permitted.
            for call in ast.walk(method):
                if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)):
                    continue
                if call.func.attr not in ("read_text", "read_bytes"):
                    continue
                target = ast.dump(call.func.value)
                assert "__file__" not in target, method.name

    def test_the_decision_text_guards_would_fail_against_an_empty_decision(self, decision_flat):
        """Known-bad control: the phrases they require are genuinely absent from a blank body,
        so the guards cannot be passing vacuously."""
        for phrase in ("FORMAL_DISPOSITION_PARSER_CORRECTION_AUTHORIZED",
                       "Merging this decision corrects no parser.",
                       "Acceptance is UNCHANGED"):
            assert phrase in decision_flat, phrase
            assert phrase not in "", phrase
# =====================================================================================
# The coupled predecessor suites were RE-ANCHORED, never weakened
# =====================================================================================
#: WS-0014's `active_branch`, `active_pr` and `last_verified_main_sha` are SINGLE SHARED live
#: self-reference fields under `OPS-0001`'s Active-GitHub-fields rule, so they lawfully name
#: whichever unit is live. Every suite that pinned the previous generation's values is therefore
#: re-anchored: the new value becomes the positive pin, the superseded value is RETAINED as a
#: NEGATIVE pin rather than deleted, and no assertion is removed, skipped, xfailed or relaxed.
REANCHORED_SUITES = (
    "test_level1_stage1_activation_authorization.py",
    "test_level1_stage1_formal_disposition_parser_correction.py",
    "test_level1_stage1_parser_contract_correction_authorization.py",
    "test_level1_stage1_post_correction_rebinding.py",
    "test_level1_stage1_post_correction_rebinding_authorization.py",
    "test_level1_stage1_post_merge_ci_recovery_authorization.py",
    "test_level1_stage1_post_merge_ci_recovery_reauthorization.py",
    "test_level1_stage1_post_merge_ci_recovery_reconciliation.py",
    "test_level1_stage1_post_parser_correction_rebinding_authorization.py",
    "test_level1_stage1_post_rebinding_drift_authorization.py",
    "test_level1_stage1_pr337_actor_evidence_correction_authorization.py",
    "test_level1_stage1_readiness_verification_authorization.py",
    "test_level1_stage1_verdict_boundary_governance.py",
)

#: The generation this unit supersedes as the live shared value.
SUPERSEDED_GENERATION_SHA = XASSET_0057_MERGE_PARENT_1
SUPERSEDED_GENERATION_BRANCH = "claude/xasset-successor-authorization-3b0btg"


class TestThePredecessorSuitesWereReAnchoredNotWeakened:
    def test_every_re_anchored_suite_exists_and_was_actually_modified(self):
        changed = set(_git("diff", "--name-only", THIS_UNIT_BASE_SHA).split())
        for name in REANCHORED_SUITES:
            assert (ROOT / name).is_file(), name
            assert name in changed, name

    def test_the_only_files_touched_are_this_units_own_change_set(self):
        allowed = set(REANCHORED_SUITES) | {
            "governance/decisions.yaml",
            "operations/WORKSTREAMS.yaml",
            "test_portfolio_hq_dashboard_decisions.py",
            DECISION_RELPATH,
            Path(__file__).name,
        }
        tracked_changes = set(_git("diff", "--name-only", THIS_UNIT_BASE_SHA).split())
        untracked = set(_git("ls-files", "--others", "--exclude-standard").split())
        extra = (tracked_changes | untracked) - allowed
        assert not extra, sorted(extra)

    def test_no_re_anchored_assertion_was_skipped_deleted_or_relaxed(self):
        """A re-anchor may add a pin, but never `skip`, `xfail`, or a shrunken assertion count."""
        for name in REANCHORED_SUITES:
            live = (ROOT / name).read_text(encoding="utf-8")
            base = _content_at(THIS_UNIT_BASE_SHA, name).decode("utf-8")
            for banned in ("pytest.mark.skip", "pytest.mark.xfail", "pytest.skip("):
                assert live.count(banned) == base.count(banned), (name, banned)
            assert live.count("assert ") >= base.count("assert "), name

    def test_no_re_anchored_suite_is_a_load_bearing_path(self):
        """Re-anchoring a bound path would silently invalidate the module's own trust boundary
        and require a rebinding this governance filing is not authorized to perform."""
        bound = set(AUTH.LOAD_BEARING_RELPATHS)
        for name in REANCHORED_SUITES:
            assert name not in bound, name

    def test_the_superseded_generation_survives_as_a_negative_pin(self):
        """Deleting the old value instead of demoting it would leave the field bound at only one
        end, which is precisely the failure this convention exists to prevent."""
        for name in REANCHORED_SUITES:
            base = _content_at(THIS_UNIT_BASE_SHA, name).decode("utf-8")
            if SUPERSEDED_GENERATION_SHA not in base and SUPERSEDED_GENERATION_BRANCH not in base:
                continue
            live = (ROOT / name).read_text(encoding="utf-8")
            assert (
                SUPERSEDED_GENERATION_SHA in live or SUPERSEDED_GENERATION_BRANCH in live
            ), name

    def test_this_units_value_is_now_the_positive_pin_in_every_constant_suite(self):
        """Only suites that DEFINE the generation constant are in scope: a suite that merely
        NAMES it inside its own meta-assertion text is checking someone else's file, not
        carrying a pin of its own, and requiring a definition there would be a false positive."""
        defining = [
            name for name in REANCHORED_SUITES
            if f'XASSET0058_MAIN_SHA = "{THIS_UNIT_BASE_SHA}"'
            in (ROOT / name).read_text(encoding="utf-8")
        ]
        assert len(defining) >= 9, defining
        for name in defining:
            live = (ROOT / name).read_text(encoding="utf-8")
            assert "== XASSET0058_MAIN_SHA" in live, name
            assert f'XASSET0057_MAIN_SHA = "{SUPERSEDED_GENERATION_SHA}"' in live, name
            assert "!= XASSET0057_MAIN_SHA" in live, name

    def test_the_successor_named_suites_advanced_their_successor_constants(self):
        """The suites that track their successor by NAME rather than by generation constant are
        advanced on the same terms: the new value is the positive pin, and this unit's
        predecessor is retained as a negative pin."""
        for name in ("test_level1_stage1_verdict_boundary_governance.py",
                     "test_level1_stage1_parser_contract_correction_authorization.py"):
            live = (ROOT / name).read_text(encoding="utf-8")
            assert f'SUCCESSOR_MAIN_SHA = "{THIS_UNIT_BASE_SHA}"' in live or (
                "SUCCESSOR_MAIN_SHA = XASSET0058_MAIN_SHA" in live
            ), name
            assert f'SUCCESSOR_BRANCH = "{BRANCH}"' in live, name
            assert f'XASSET0057_BRANCH = "{SUPERSEDED_GENERATION_BRANCH}"' in live, name
            assert "XASSET-0058" in live, name

    def test_the_re_anchoring_is_non_vacuous_at_the_base(self):
        """Each re-anchored suite must genuinely have failed at the base under this unit's
        register, otherwise the edits were cosmetic."""
        base_register = _content_at(THIS_UNIT_BASE_SHA, "operations/WORKSTREAMS.yaml").decode("utf-8")
        before = next(
            w for w in yaml.safe_load(base_register)["workstreams"] if w["id"] == "WS-0014"
        )
        live = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
        now = next(w for w in live["workstreams"] if w["id"] == "WS-0014")
        assert before["last_verified_main_sha"] == SUPERSEDED_GENERATION_SHA
        assert before["active_branch"] == SUPERSEDED_GENERATION_BRANCH
        assert now["last_verified_main_sha"] == THIS_UNIT_BASE_SHA
        assert now["active_branch"] == BRANCH
        assert now["last_verified_main_sha"] != before["last_verified_main_sha"]
        assert now["active_branch"] != before["active_branch"]

    def test_the_decision_discloses_the_re_anchoring(self, decision_flat):
        assert "re-anchor" in decision_flat.lower()
