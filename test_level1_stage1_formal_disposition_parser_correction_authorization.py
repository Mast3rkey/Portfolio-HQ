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
import contextlib
import datetime
import hashlib
import inspect
import re
import subprocess
import sys
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

# -------------------------------------------------------------------------------------
# RE-ANCHORED by the XASSET-0058 Lifecycle B parser correction
# -------------------------------------------------------------------------------------
#: XASSET-0058 is design-only, so every claim below was measured against the LIVE merged bytes
#: -- which were the uncorrected ones at the time. The Lifecycle B implementation this decision
#: authorizes lawfully corrects them, so each such measurement is re-anchored to the IMMUTABLE
#: commit it was really about: this decision's own normal-merge commit, whose module blob is the
#: vulnerable identity. The reproduction therefore keeps proving exactly what it proved, over a
#: range that can never move, and the CLOSURE of the same cells is proved separately against the
#: real corrected parser by the Lifecycle B suite.
XASSET_0058_MERGE_SHA = "34c45900ce23742d04d80cf12471c34aabe9682d"




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


def _module_at(sha: str):
    """The production module exactly as it stood at ``sha``. Immutable, and never the live file.

    Compiled straight from the git blob in memory: this suite writes NOTHING to the filesystem,
    so loading the historical bytes may not either.
    """
    import importlib.util

    key = f"_authorization_module_at_{sha[:12]}"
    if key in sys.modules:
        return sys.modules[key]
    source = _content_at(sha, PRODUCTION_MODULE_RELPATH).decode("utf-8")
    spec = importlib.util.spec_from_loader(key, loader=None)
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(ROOT / PRODUCTION_MODULE_RELPATH)
    sys.modules[key] = module
    try:
        exec(compile(source, f"<{key}>", "exec"), module.__dict__)
    except BaseException:
        del sys.modules[key]
        raise
    return module


#: The UNCORRECTED parser -- the exact bytes XASSET-0058 measured. Every reproduction below runs
#: against this, never against the live file, so the defect it records stays reproducible for
#: ever rather than evaporating the moment the defect is fixed.
BASE_AUTH = _module_at(XASSET_0058_MERGE_SHA)


@contextlib.contextmanager
def _seams_at_base():
    """Drive the REAL seam runners against the BASE module's own real seams.

    The runners in the XASSET-0056 suite are written against its module-level ``A``. Rebinding
    that name is what makes the historical seam evidence reproducible: it is the same real
    runner code and the same real consumers, executed over the uncorrected bytes.
    """
    previous = _SEAMS_MODULE.A
    _SEAMS_MODULE.A = BASE_AUTH
    try:
        yield
    finally:
        _SEAMS_MODULE.A = previous
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

# -------------------------------------------------------------------------------------
# BLOCKING 1 (review `5034171910`) -- the EXHAUSTIVE printable-ASCII matrix
# -------------------------------------------------------------------------------------
#: The superseded matrix above substituted and inserted one handpicked character, ``"X"``. A
#: single representative cannot establish a claim about the ASCII families -- least of all when
#: the classifier's own delimiter, the COLON, is itself an ASCII character. ``MUTANTS`` is
#: RETAINED unchanged because it is the exact fixed-representative reproduction ``XASSET-0057``
#: SS-F.0.1 itself measured; the exhaustive matrix below is the evidence the families are decided on.
PRINTABLE_ASCII = tuple(chr(code) for code in range(0x20, 0x7F))

EXHAUSTIVE_FAMILIES = (
    "deletion",
    "ascii_substitution",
    "ascii_insertion",
    "transposition",
    "confusable_substitution",
)


def _exhaustive() -> list[tuple[str, int, str, str]]:
    """Every single-character mutation of the label over the WHOLE printable-ASCII alphabet.

    Returns ``(family, position, character, mutated_label)``. This is the SOLE source of every
    exhaustive count below -- no count is separately maintained.
    """
    out: list[tuple[str, int, str, str]] = []
    for i in NONSPACE_POSITIONS:
        out.append(("deletion", i, "", CANON_LABEL[:i] + CANON_LABEL[i + 1:]))
    for i in NONSPACE_POSITIONS:
        for character in PRINTABLE_ASCII:
            if character != CANON_LABEL[i]:
                out.append(
                    ("ascii_substitution", i, character,
                     CANON_LABEL[:i] + character + CANON_LABEL[i + 1:])
                )
    for i in NONSPACE_POSITIONS:
        for character in PRINTABLE_ASCII:
            out.append(
                ("ascii_insertion", i, character,
                 CANON_LABEL[:i] + character + CANON_LABEL[i:])
            )
    for i in ADJACENT_PAIRS:
        out.append(
            ("transposition", i, "",
             CANON_LABEL[:i] + CANON_LABEL[i + 1] + CANON_LABEL[i] + CANON_LABEL[i + 2:])
        )
    for i in NONSPACE_POSITIONS:
        out.append(
            ("confusable_substitution", i, CONFUSABLES[CANON_LABEL[i]],
             CANON_LABEL[:i] + CONFUSABLES[CANON_LABEL[i]] + CANON_LABEL[i + 1:])
        )
    return out


EXHAUSTIVE = _exhaustive()

#: Exactly the cells whose mutation character IS the classifier's own delimiter. These are the
#: cells the superseded first-colon rule left fail-open, and they are load-bearing on their own.
COLON_CELLS = [cell for cell in EXHAUSTIVE if cell[2] == ":"]

PLAIN, BOLD, INDENTED = "plain", "bold", "indented"


def _render(label: str, form: str) -> str:
    """The three GOVERNED presentations, and no fourth."""
    if form == PLAIN:
        return f"{label}: {ADVERSE_VERDICT}"
    if form == BOLD:
        return f"**{label}: {ADVERSE_VERDICT}**"
    if form == INDENTED:
        return f"   {label}: {ADVERSE_VERDICT}"
    raise AssertionError(form)


#: The three outcome classes, stated honestly. Only the third is unsafe.
SAFE_MALFORMED = "MALFORMED"        # recognized as a candidate, fails closed
SAFE_ADVERSE = "ADVERSE"            # still the canonical prefix; the adverse verdict wins
UNSAFE_BYPASS = "BYPASS"            # skipped, so the LATER APPROVAL wins


def _integrated_outcome(line: str, *, with_candidate_rule: bool) -> str:
    """The real parser's outcome, with the candidate hook integrated at its real branch."""
    body = f"{line}\n\n{PREFIX} {APPROVE}\n"
    if with_candidate_rule and hook_is_reachable(line) and is_candidate(line):
        return SAFE_MALFORMED
    # RE-ANCHORED: the substrate is the UNCORRECTED parser, so ``with_candidate_rule=False``
    # keeps reproducing the live-at-the-time defect and ``True`` keeps modelling the decided
    # boundary on top of it. The real corrected parser is proved to AGREE with the ``True``
    # column, cell for cell, by the Lifecycle B suite.
    result = BASE_AUTH.parse_formal_disposition(body)
    if result is BASE_AUTH.MALFORMED_FORMAL_DISPOSITION:
        return SAFE_MALFORMED
    if result is None:
        return "ABSENT"
    if result == APPROVE:
        return UNSAFE_BYPASS
    if result == ADVERSE_VERDICT:
        return SAFE_ADVERSE
    return "OTHER"



def _adverse_then_approval(label: str) -> str:
    """An adverse FIRST formal line, then a canonical approval. A skip lets the approval win."""
    return f"{label}: {ADVERSE_VERDICT}\n\n{PREFIX} {APPROVE}\n"


def _classify(body: str) -> str:
    """RE-ANCHORED: the UNCORRECTED parser this decision actually measured.

    XASSET-0058 is design-only, so ``AUTH`` was the uncorrected module when this suite was
    written. Pointing this at ``BASE_AUTH`` keeps every reproduction below measuring exactly the
    bytes it was written about, instead of silently re-measuring whatever the module later
    becomes -- which would make the recorded defect vanish rather than stay proved.
    """
    r = BASE_AUTH.parse_formal_disposition(body)
    if r is BASE_AUTH.MALFORMED_FORMAL_DISPOSITION:
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

    # ---------------------------------------------------------------------------------
    # BLOCKING 1: the alphabet itself is load-bearing evidence and must not silently
    # collapse back to a handpicked representative. Independent FULL review `5034171910`
    # found exactly that defect; a mutation probe then found that NOTHING here prevented
    # it recurring. These guards close that.
    # ---------------------------------------------------------------------------------
    def test_the_exhaustive_alphabet_is_the_WHOLE_printable_ascii_range(self):
        assert PRINTABLE_ASCII == tuple(chr(code) for code in range(0x20, 0x7F))
        assert len(PRINTABLE_ASCII) == 95
        assert PRINTABLE_ASCII[0] == " " and PRINTABLE_ASCII[-1] == "~"
        assert ":" in PRINTABLE_ASCII, "the classifier's own delimiter must be swept"
        assert all(c.isascii() and c.isprintable() for c in PRINTABLE_ASCII)
        # ...and it is genuinely an alphabet, not a single representative.
        assert len(set(PRINTABLE_ASCII)) == len(PRINTABLE_ASCII) > 1

    def test_the_exhaustive_matrix_size_FOLLOWS_from_the_alphabet_and_the_positions(self):
        """Every count is DERIVED. A shrunken alphabet cannot leave these consistent."""
        n_chars, n_pos, n_pairs = len(PRINTABLE_ASCII), len(NONSPACE_POSITIONS), len(ADJACENT_PAIRS)
        sizes = {family: 0 for family in EXHAUSTIVE_FAMILIES}
        for family, _, _, _ in EXHAUSTIVE:
            sizes[family] += 1
        assert sizes["deletion"] == n_pos
        assert sizes["transposition"] == n_pairs
        assert sizes["confusable_substitution"] == n_pos
        # substitution excludes the identity character at each position
        assert sizes["ascii_substitution"] == sum(
            sum(1 for c in PRINTABLE_ASCII if c != CANON_LABEL[i]) for i in NONSPACE_POSITIONS
        )
        assert sizes["ascii_insertion"] == n_pos * n_chars
        assert len(EXHAUSTIVE) == sum(sizes.values())
        # and the totals actually are what the decision states
        assert sizes["ascii_substitution"] == 1598
        assert sizes["ascii_insertion"] == 1615
        assert len(EXHAUSTIVE) == 3264

    def test_the_colon_cells_are_exactly_the_delimiter_mutations_and_are_not_empty(self):
        assert len(COLON_CELLS) > 0
        assert all(character == ":" for _, _, character, _ in COLON_CELLS)
        assert {family for family, _, _, _ in COLON_CELLS} == {
            "ascii_substitution", "ascii_insertion"
        }
        assert len(COLON_CELLS) == 2 * len(NONSPACE_POSITIONS) == 34


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
        assert (
            BASE_AUTH.parse_formal_disposition(body)
            is BASE_AUTH.MALFORMED_FORMAL_DISPOSITION
        )
        # ... and the corrected parser keeps it MALFORMED, by IDENTITY, not merely "not approving".
        assert AUTH.parse_formal_disposition(body) is AUTH.MALFORMED_FORMAL_DISPOSITION

    def test_position_zero_leaves_the_canonical_prefix_intact_as_a_substring(self):
        assert PREFIX in ("X" + CANON_LABEL + ":")

    def test_the_untampered_adverse_line_is_read_as_adverse(self):
        assert _classify(_adverse_then_approval(CANON_LABEL)) == "ADVERSE"

    def test_a_bypassing_body_really_yields_the_APPROVING_verdict(self):
        """Not merely 'not adverse': the later approval actually wins."""
        body = _adverse_then_approval("FORMAL DISPOSITON")  # one deletion
        assert BASE_AUTH.parse_formal_disposition(body) == APPROVE
        # RE-ANCHORED: and the corrected parser refuses that exact body, fail-closed.
        assert AUTH.parse_formal_disposition(body) is AUTH.MALFORMED_FORMAL_DISPOSITION


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
        with _seams_at_base():
            recorder = _SEAMS.run_consumer_one(_adverse_then_approval(label), monkeypatch)
        assert any(c.startswith("reviews:") for c in recorder.calls), (family, index)

    @pytest.mark.parametrize("family,index,label", _BYPASSING,
                             ids=[f"{f}-{i}" for f, i, _ in _BYPASSING])
    def test_seam_two_does_not_refuse(self, family, index, label):
        with _seams_at_base():
            errors = _SEAMS.run_consumer_two(_adverse_then_approval(label))
        assert not _seam_two_refused(errors)

    @pytest.mark.parametrize("family,index,label", _BYPASSING,
                             ids=[f"{f}-{i}" for f, i, _ in _BYPASSING])
    def test_seam_three_does_not_refuse(self, family, index, label):
        with _seams_at_base():
            errors = _SEAMS.run_consumer_three(_adverse_then_approval(label), "COMMENTED")
        assert not _seam_three_refused(errors)

    @pytest.mark.parametrize("family,index,label", _BYPASSING,
                             ids=[f"{f}-{i}" for f, i, _ in _BYPASSING])
    def test_seam_three_does_not_refuse_under_a_native_APPROVED_state(self, family, index, label):
        with _seams_at_base():
            errors = _SEAMS.run_consumer_three(_adverse_then_approval(label), "APPROVED")
        assert not _seam_three_refused(errors)

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
#: BLOCKING 1 (independent FULL review `5034171910`) -- CORRECTED, and the superseded rule is
#: recorded rather than deleted.
#:
#: The SUPERSEDED rule took the FIRST ASCII colon inside a closed window and rejected it when it
#: was not at an admissible index. An ASCII substitution or insertion of a COLON anywhere earlier
#: in the label therefore HID the real terminating colon behind itself, the length gate rejected
#: the impostor, and the adverse line was skipped so a later canonical approval won. That is the
#: very bypass this boundary exists to close, reachable with one printable-ASCII character --
#: reproduced at 31 of the exhaustive matrix's cells before this correction was written.
#:
#: The CORRECTED rule probes every ADMISSIBLE colon INDEX directly instead. A label within one
#: edit of the 18-character canonical label has length 17, 18 or 19, so its terminating colon can
#: only sit at index 17, 18 or 19. Those three indices are examined; an earlier colon can no
#: longer displace the real one, and the rule stays O(1) -- exactly three index probes per
#: projection, strictly fewer than a window scan.
ADMISSIBLE_COLON_INDICES = (
    len(CANON_LABEL) - MAX_EDITS,
    len(CANON_LABEL),
    len(CANON_LABEL) + MAX_EDITS,
)


def ascii_fold(text: str) -> str:
    """The SAME ASCII-only case fold acceptance already uses. A non-ASCII character never
    becomes an ASCII letter."""
    return "".join(c.upper() if "a" <= c <= "z" else c for c in text)


def candidate(line: str) -> bool:
    """Call the candidate rule the way ``parse_formal_disposition`` calls it.

    MAJOR 1 of review ``5037196415``: the rule takes SS-D.1's line bounds from its caller and
    derives none for itself, so every caller supplies them. Deriving them here mirrors the parser.
    """
    folded = ascii_fold(line)
    start = 0
    while start < len(folded) and folded[start] == " ":
        start += 1
    end = len(folded)
    while end > start and folded[end - 1] in " \t":
        end -= 1
    return AUTH._is_formal_disposition_candidate(folded, start, end)


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
    """SS-D.2, exactly. Classification only: it can never produce or repair a verdict.

    Every admissible colon index is probed, so an internal colon cannot hide the real
    terminating one. The explicit length gate the superseded rule needed is subsumed: an
    admissible index IS the label length, by construction.
    """
    for projection in projections(line):
        for index in ADMISSIBLE_COLON_INDICES:
            if index < len(projection) and projection[index] == ":":
                if osa(ascii_fold(projection[:index]), CANON_LABEL) <= MAX_EDITS:
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
    """The EXHAUSTIVE printable-ASCII matrix. Every count is derived from ``EXHAUSTIVE``."""

    def test_the_matrix_is_genuinely_exhaustive_over_printable_ascii(self):
        assert len(PRINTABLE_ASCII) == 95
        assert PRINTABLE_ASCII[0] == " " and PRINTABLE_ASCII[-1] == "~"
        assert ":" in PRINTABLE_ASCII, "the classifier's own delimiter must be in the alphabet"
        subs = [c for f, _, c, _ in EXHAUSTIVE if f == "ascii_substitution"]
        ins = [c for f, _, c, _ in EXHAUSTIVE if f == "ascii_insertion"]
        assert set(ins) == set(PRINTABLE_ASCII)
        assert set(subs) <= set(PRINTABLE_ASCII) and len(set(subs)) == 95
        assert len({f for f, _, _, _ in EXHAUSTIVE}) == len(EXHAUSTIVE_FAMILIES)

    def test_the_matrix_is_not_the_superseded_fixed_representative(self):
        """A single handpicked character cannot establish an ASCII-family claim."""
        assert len(EXHAUSTIVE) > len(MUTANTS) * 30
        assert len({c for _, _, c, _ in EXHAUSTIVE if c}) > 1

    @pytest.mark.parametrize("form", [PLAIN, BOLD, INDENTED])
    def test_no_cell_lets_a_later_approval_win(self, form):
        """THE safety property, stated as what it actually is: not 'everything is MALFORMED',
        but 'no mutation lets the adverse line be skipped so the later approval wins'."""
        bypasses = [
            (f, i, c, l) for f, i, c, l in EXHAUSTIVE
            if _integrated_outcome(_render(l, form), with_candidate_rule=True) == UNSAFE_BYPASS
        ]
        assert bypasses == [], bypasses[:8]

    @pytest.mark.parametrize("form", [PLAIN, BOLD, INDENTED])
    def test_every_cell_lands_in_a_named_safe_class(self, form):
        allowed = {SAFE_MALFORMED, SAFE_ADVERSE}
        seen = {
            _integrated_outcome(_render(l, form), with_candidate_rule=True)
            for _, _, _, l in EXHAUSTIVE
        }
        assert seen <= allowed, seen - allowed

    def test_the_adverse_class_is_genuinely_safe_and_small(self):
        """The cells that stay ADVERSE do so because the parser still reads the CANONICAL
        prefix -- ASCII case, and CommonMark-insignificant leading space. The adverse verdict
        wins, so no approval can. They are enumerated, not waved through."""
        adverse = [
            (f, i, c, l) for f, i, c, l in EXHAUSTIVE
            if _integrated_outcome(_render(l, PLAIN), with_candidate_rule=True) == SAFE_ADVERSE
        ]
        assert adverse, "an empty class here would mean the classification collapsed"
        for f, i, c, l in adverse:
            assert not hook_is_reachable(f"{l}: {ADVERSE_VERDICT}"), (f, i, c)
            body = f"{l}: {ADVERSE_VERDICT}\n\n{PREFIX} {APPROVE}\n"
            assert AUTH.parse_formal_disposition(body) == ADVERSE_VERDICT, (f, i, c)
        # every one is an ASCII lower-case fold or the single leading-space insertion
        for f, i, c, l in adverse:
            assert (c.islower() and c.isascii()) or c == " ", (f, i, c)

    def test_the_superseded_first_colon_rule_really_was_fail_open(self):
        """Non-vacuity: the correction must be shown to have fixed something real."""
        def superseded(line):
            for projection in projections(line):
                colon = projection.find(":", 0, len(CANON_LABEL) + MAX_EDITS + 1)
                if colon == -1 or abs(colon - len(CANON_LABEL)) > MAX_EDITS:
                    continue
                if osa(ascii_fold(projection[:colon]), CANON_LABEL) <= MAX_EDITS:
                    return True
            return False

        open_cells = []
        for f, i, c, l in EXHAUSTIVE:
            line = _render(l, PLAIN)
            if hook_is_reachable(line) and not superseded(line):
                body = f"{line}\n\n{PREFIX} {APPROVE}\n"
                if BASE_AUTH.parse_formal_disposition(body) == APPROVE:
                    open_cells.append((f, i, c))
        assert open_cells, "if nothing was fail-open the correction would be pointless"
        # every one of them was a COLON mutation, and every one is closed now
        assert {c for _, _, c in open_cells} == {":"}
        for f, i, c in open_cells:
            label = next(l for ff, ii, cc, l in EXHAUSTIVE if (ff, ii, cc) == (f, i, c))
            assert is_candidate(_render(label, PLAIN)), (f, i, c)

    @pytest.mark.parametrize("family", EXHAUSTIVE_FAMILIES)
    def test_each_family_has_zero_bypasses(self, family):
        cells = [(f, i, c, l) for f, i, c, l in EXHAUSTIVE if f == family]
        assert cells, family
        bypasses = [
            t for t in cells
            if _integrated_outcome(_render(t[3], PLAIN), with_candidate_rule=True) == UNSAFE_BYPASS
        ]
        assert bypasses == [], (family, bypasses[:5])

    @pytest.mark.parametrize("family,index,character,label", COLON_CELLS,
                             ids=[f"{f}-{i}" for f, i, _, _ in COLON_CELLS])
    def test_every_colon_cell_is_a_candidate_in_every_presentation(
        self, family, index, character, label
    ):
        """The colon is INDEPENDENTLY load-bearing: it is the classifier's own delimiter."""
        assert character == ":"
        for form in (PLAIN, BOLD, INDENTED):
            line = _render(label, form)
            outcome = _integrated_outcome(line, with_candidate_rule=True)
            assert outcome != UNSAFE_BYPASS, (family, index, form, outcome)

    def test_the_two_attacks_the_review_named_are_pinned_by_name(self):
        """`FORM:L DISPOSITION:` and `FORM:AL DISPOSITION:` -- BLOCKING 1's own examples."""
        for label in ("FORM:L DISPOSITION", "FORM:AL DISPOSITION"):
            line = f"{label}: {ADVERSE_VERDICT}"
            assert hook_is_reachable(line), label
            assert is_candidate(line), label
            assert _integrated_outcome(line, with_candidate_rule=True) == SAFE_MALFORMED, label
            body = f"{line}\n\n{PREFIX} {APPROVE}\n"
            assert BASE_AUTH.parse_formal_disposition(body) == APPROVE, (
                "the BASE parser must still show the bypass this correction closes"
            )
            # RE-ANCHORED: and the corrected parser now refuses that exact body, fail-closed.
            assert (
                AUTH.parse_formal_disposition(body) is AUTH.MALFORMED_FORMAL_DISPOSITION
            ), label

    def test_the_retained_fixed_representative_still_holds(self):
        """`MUTANTS` is SS-F.0.1's own measurement and is not discarded by the expansion."""
        assert len(MUTANTS) == 85
        for _, _, label in MUTANTS:
            assert _integrated_outcome(f"{label}: {ADVERSE_VERDICT}",
                                       with_candidate_rule=True) != UNSAFE_BYPASS


#: Seam 2 costs ~129 ms per call, and PROFILING SHOWS WHY: `_verify_successor_rebinding_identity`
#: issues ~48 git subprocesses per invocation, work that is entirely UNRELATED to the parser
#: branch under test. Driving all 3 264 cells through it would spend ~7 minutes of every future
#: suite run on git plumbing that cannot vary with the parse result. Seam 3 costs ~0.03 ms, so it
#: is driven EXHAUSTIVELY in both native states. Seams 1 and 2 are driven over the
#: safety-critical subset, chosen deterministically and stated exactly: every colon cell, every
#: cell the superseded rule left fail-open, and one representative per (family, position).
def _seam_subset() -> list[tuple[str, int, str, str]]:
    chosen: dict[tuple[str, int, str], tuple[str, int, str, str]] = {}
    for cell in COLON_CELLS:
        chosen[(cell[0], cell[1], cell[2])] = cell
    seen_positions: set[tuple[str, int]] = set()
    for cell in EXHAUSTIVE:
        key = (cell[0], cell[1])
        if key not in seen_positions:
            seen_positions.add(key)
            chosen.setdefault((cell[0], cell[1], cell[2]), cell)
    return sorted(chosen.values(), key=lambda c: (c[0], c[1], c[2]))


SEAM_SUBSET = _seam_subset()


#: The cells the LIVE parser ALREADY returns the MALFORMED sentinel for. These are REAL cells of
#: the exhaustive matrix -- not synthetic stand-ins -- and they are the only cells whose
#: MALFORMED-to-seam behaviour can be driven through UNCORRECTED production code today, because
#: this filing is DESIGN ONLY and changes no production byte.
LIVE_MALFORMED_CELLS = [
    cell for cell in EXHAUSTIVE
    if _integrated_outcome(_render(cell[3], PLAIN), with_candidate_rule=False) == SAFE_MALFORMED
]

#: The cells the LIVE parser lets BYPASS. After the correction each becomes MALFORMED at the
#: parser; the seam behaviour that then applies is the one proven on LIVE_MALFORMED_CELLS.
LIVE_BYPASS_CELLS = [
    cell for cell in EXHAUSTIVE
    if _integrated_outcome(_render(cell[3], PLAIN), with_candidate_rule=False) == UNSAFE_BYPASS
]


class TestEveryCellIsRefusedAtEveryRealConsumerSeam:
    """The seam claim, proved as a COMPOSITION of two independently measured halves.

    This filing changes no production byte, so the corrected parser does not exist yet and a
    corrected cell's MALFORMED result cannot be pushed through the real seams directly. Skipping
    the seam whenever the corrected outcome is MALFORMED would make these tests assert NOTHING --
    after the correction that is 3 246 of 3 264 cells and 34 of 34 colon cells. The claim is
    therefore proved in two REAL halves, each with its own non-emptiness guard:

      PART A -- with the candidate rule, EVERY cell's parser outcome is MALFORMED, never BYPASS.
      PART B -- a MALFORMED body is REFUSED at every real seam, in both native states, driven
                through the REAL seams over REAL matrix cells the LIVE parser already returns
                MALFORMED for.

    A and B compose to the claim. Neither half is allowed to be empty.
    """

    def test_the_seam_subset_is_declared_and_covers_what_it_claims(self):
        assert len(SEAM_SUBSET) >= len(COLON_CELLS)
        assert all(cell in SEAM_SUBSET for cell in COLON_CELLS)
        covered = {(f, i) for f, i, _, _ in SEAM_SUBSET}
        expected = {(f, i) for f, i, _, _ in EXHAUSTIVE}
        assert covered == expected, "every (family, position) must appear at least once"

    def test_both_halves_of_the_composition_are_non_empty(self):
        """A composition of two vacuous halves would prove nothing. Neither half may be empty."""
        assert len(LIVE_MALFORMED_CELLS) > 0, "PART B would have nothing real to drive"
        assert len(LIVE_BYPASS_CELLS) > 0, "PART A would have nothing real to close"
        assert len(LIVE_MALFORMED_CELLS) + len(LIVE_BYPASS_CELLS) + 18 == len(EXHAUSTIVE)

    # ------------------------------------------------------------------ PART A
    def test_partA_every_cell_becomes_MALFORMED_at_the_parser_never_BYPASS(self):
        """Exhaustive, all three presentations, driven through the REAL parser."""
        for form in (PLAIN, BOLD, INDENTED):
            outcomes = {
                _integrated_outcome(_render(label, form), with_candidate_rule=True)
                for _, _, _, label in EXHAUSTIVE
            }
            assert UNSAFE_BYPASS not in outcomes, form
            assert outcomes <= {SAFE_MALFORMED, SAFE_ADVERSE}, (form, sorted(outcomes))

    # ------------------------------------------------------------------ PART B
    def test_partB_seam_three_refuses_every_live_malformed_cell(self):
        """Every real cell the live parser already calls MALFORMED, through the REAL seam."""
        survivors = [
            (f, i, c) for f, i, c, l in LIVE_MALFORMED_CELLS
            if not _seam_three_refused(
                _SEAMS.run_consumer_three(f"{_render(l, PLAIN)}\n\n{PREFIX} {APPROVE}\n",
                                          "COMMENTED")
            )
        ]
        assert survivors == [], survivors[:8]

    def test_partB_seam_three_refuses_every_live_malformed_cell_under_native_APPROVED(self):
        """Native-`APPROVED` rescue must fail. Exhaustive over the same real cells."""
        survivors = [
            (f, i, c) for f, i, c, l in LIVE_MALFORMED_CELLS
            if not _seam_three_refused(
                _SEAMS.run_consumer_three(f"{_render(l, PLAIN)}\n\n{PREFIX} {APPROVE}\n",
                                          "APPROVED")
            )
        ]
        assert survivors == [], survivors[:8]

    @pytest.mark.parametrize(
        "family,index,character,label",
        LIVE_MALFORMED_CELLS[::8],
        ids=[f"{f}-{i}-{ord(c) if c else 0}" for f, i, c, _ in LIVE_MALFORMED_CELLS[::8]],
    )
    def test_partB_seam_two_refuses_live_malformed_cells(self, family, index, character, label):
        body = f"{_render(label, PLAIN)}\n\n{PREFIX} {APPROVE}\n"
        assert _seam_two_refused(_SEAMS.run_consumer_two(body)), (family, index, character)

    @pytest.mark.parametrize(
        "family,index,character,label",
        LIVE_MALFORMED_CELLS[::8],
        ids=[f"{f}-{i}-{ord(c) if c else 0}" for f, i, c, _ in LIVE_MALFORMED_CELLS[::8]],
    )
    def test_partB_seam_one_refuses_live_malformed_cells(
        self, family, index, character, label, monkeypatch
    ):
        body = f"{_render(label, PLAIN)}\n\n{PREFIX} {APPROVE}\n"
        recorder = _SEAMS.run_consumer_one(body, monkeypatch)
        assert not any(c.startswith("reviews:") for c in recorder.calls), (family, index)

    def test_the_parametrized_partB_seam_samples_are_not_empty(self):
        """The `[::8]` stride must actually select cells, and must include every family present."""
        sample = LIVE_MALFORMED_CELLS[::8]
        assert len(sample) >= 8, len(sample)
        assert {f for f, _, _, _ in sample} == {f for f, _, _, _ in LIVE_MALFORMED_CELLS}

    # ------------------------------------------------------- the composition itself
    def test_the_composition_closes_every_cell_including_every_colon_cell(self):
        """A and B together: no cell survives at any seam, and the colon cells are named.

        Stated as the composition rather than asserted as if the seam had been driven on an
        uncorrected parser -- which it cannot be, and which this filing does not pretend.
        """
        by_parser = {
            (f, i, c): _integrated_outcome(_render(l, PLAIN), with_candidate_rule=True)
            for f, i, c, l in EXHAUSTIVE
        }
        assert UNSAFE_BYPASS not in by_parser.values()
        for f, i, c, _ in COLON_CELLS:
            assert by_parser[(f, i, c)] == SAFE_MALFORMED, (f, i, c)
        # ...and MALFORMED is exactly the state PART B drove through all three real seams.
        assert len(LIVE_MALFORMED_CELLS) > 0

    def test_the_live_parser_still_shows_the_defect_at_these_seams(self):
        """Control: without the candidate rule the colon cells DO reach the seams and pass.

        RE-ANCHORED to the BASE seams. A control that silently re-measured the CORRECTED parser
        would report ``reached == 0`` and turn this guard into a tautology instead of the
        live-defect detector it is. The corrected refusal is proved separately, below.
        """
        reached = 0
        corrected_refused = 0
        for f, i, c, l in COLON_CELLS:
            body = f"{_render(l, PLAIN)}\n\n{PREFIX} {APPROVE}\n"
            with _seams_at_base():
                errors = _SEAMS.run_consumer_three(body, "COMMENTED")
            if not _seam_three_refused(errors):
                reached += 1
            if _seam_three_refused(_SEAMS.run_consumer_three(body, "COMMENTED")):
                corrected_refused += 1
        assert reached >= 30, reached
        # RE-ANCHORED: every one of those same cells is refused at the REAL corrected seam.
        assert corrected_refused == len(COLON_CELLS), (corrected_refused, len(COLON_CELLS))


def _superseded_first_colon_is_candidate(line: str) -> bool:
    """The SUPERSEDED rule, reconstructed EXACTLY as review `5034171910` described it.

    Retained as a NEGATIVE reference model so the finding stays reproducible: it must keep
    failing on the colon cells, and the corrected rule must keep closing them. A regression in
    either direction fails.
    """
    for projection in projections(line):
        index = projection.find(":", 0, len(CANON_LABEL) + MAX_EDITS + 1)
        if index < 0:
            continue
        if abs(index - len(CANON_LABEL)) > MAX_EDITS:
            continue
        if osa(ascii_fold(projection[:index]), CANON_LABEL) <= MAX_EDITS:
            return True
    return False


class TestTheReviewFindingStaysReproducible:
    """`5034171910` BLOCKING 1, pinned by measurement rather than by narrative."""

    @pytest.mark.parametrize(
        "line",
        [
            "FORM:L DISPOSITION: CHANGES REQUIRED",   # substitution, the review's own example
            "FORM:AL DISPOSITION: CHANGES REQUIRED",  # insertion, the review's own example
        ],
    )
    def test_the_two_named_bodies_were_fail_open_and_are_now_closed(self, line):
        body = f"{line}\n\n{PREFIX} {APPROVE}\n"
        # the superseded rule did not even see them...
        assert _superseded_first_colon_is_candidate(line) is False
        # ...so the BASE parser returned the LATER APPROVAL, which is the whole defect.
        assert BASE_AUTH.parse_formal_disposition(body) == APPROVE
        # RE-ANCHORED: the REAL corrected parser refuses it, by sentinel IDENTITY.
        assert AUTH.parse_formal_disposition(body) is AUTH.MALFORMED_FORMAL_DISPOSITION
        # the corrected rule sees them, and the outcome becomes fail-closed MALFORMED.
        assert is_candidate(line) is True
        assert _integrated_outcome(line, with_candidate_rule=True) == SAFE_MALFORMED

    @pytest.mark.parametrize("family", ["ascii_substitution", "ascii_insertion"])
    def test_the_reviewers_sixteen_of_seventeen_figure_reproduces_exactly(self, family):
        cells = [c for c in COLON_CELLS if c[0] == family]
        assert len(cells) == 17, family
        rejected = [
            index for _, index, _, label in cells
            if not _superseded_first_colon_is_candidate(_render(label, PLAIN))
        ]
        assert len(rejected) == 16, (family, rejected)
        # ...and the corrected rule closes ALL seventeen.
        closed = [
            index for _, index, _, label in cells
            if is_candidate(_render(label, PLAIN))
        ]
        assert len(closed) == 17, (family, closed)

    def test_the_two_models_genuinely_differ_on_the_colon_cells(self):
        """Guards against the negative model accidentally becoming the corrected one."""
        differing = [
            (f, i) for f, i, _, label in COLON_CELLS
            if _superseded_first_colon_is_candidate(_render(label, PLAIN))
            != is_candidate(_render(label, PLAIN))
        ]
        assert len(differing) == 32, len(differing)

    def test_the_two_models_AGREE_on_ordinary_prose(self):
        """The correction must not have widened the rule on anything but the colon boundary."""
        import subprocess
        files = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "*.md"],
            capture_output=True, text=True, check=True,
        ).stdout.split()
        disagreements = []
        for relpath in files:
            for line in (ROOT / relpath).read_text(encoding="utf-8",
                                                   errors="replace").splitlines():
                if _superseded_first_colon_is_candidate(line) != is_candidate(line):
                    disagreements.append((relpath, line[:60]))
        assert disagreements == [], disagreements[:5]


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
    def test_indexed_probing_makes_length_irrelevant(self, length):
        line = "x" * length + ": tail"
        assert not is_candidate(line)

    def test_exactly_three_indices_are_probed_and_no_others(self):
        assert ADMISSIBLE_COLON_INDICES == (17, 18, 19)
        assert len(ADMISSIBLE_COLON_INDICES) == 3
        # a colon anywhere else can never qualify, however close
        for bad in (0, 1, 4, 16, 20, 21, 40):
            assert bad not in ADMISSIBLE_COLON_INDICES
            line = "x" * bad + ":" + "y" * 40
            assert not is_candidate(line), bad

    def test_an_internal_colon_no_longer_hides_the_real_one(self):
        """The exact regression BLOCKING 1 reported, pinned as its own assertion."""
        assert is_candidate("FORM:L DISPOSITION: CHANGES REQUIRED")
        assert is_candidate("FORM:AL DISPOSITION: CHANGES REQUIRED")
        # and the superseded first-colon reading would have refused both
        for line in ("FORM:L DISPOSITION: CHANGES REQUIRED",
                     "FORM:AL DISPOSITION: CHANGES REQUIRED"):
            first = line.find(":", 0, 20)
            assert first not in ADMISSIBLE_COLON_INDICES, line

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

    def test_the_D3_table_states_zero_corrected_bypass_for_every_family(self, decision_text):
        """The D.3 table is PARSED, and each family's numbers are checked against the LIVE matrix.

        A count of bolded literals would pass on a table that said anything at all. This parses
        the real rows and cross-checks four independently derived quantities per family -- cell
        count, live BYPASS, corrected BYPASS and corrected MALFORMED -- against the exhaustive
        matrix recomputed here. It fails if the decision's own table drifts from the evidence.
        """
        table = decision_text.split("#### D.3")[1].split("#### D.4")[0]
        rows = {}
        for raw in table.splitlines():
            if not raw.strip().startswith("|"):
                continue
            cells = [c.strip() for c in raw.strip().strip("|").split("|")]
            if len(cells) != 6:
                continue
            numbers = []
            for cell in cells[1:]:
                digits = cell.replace("*", "").replace("\u202f", "").replace(" ", "")
                if not digits.isdigit():
                    numbers = None
                    break
                numbers.append(int(digits))
            if numbers is None:
                continue
            rows[cells[0].replace("*", "").strip()] = numbers

        assert len(rows) >= 6, sorted(rows)

        expected = {}
        for family, position, character, label in EXHAUSTIVE:
            bucket = expected.setdefault(family, {"n": 0, "live": 0, "bypass": 0, "malformed": 0})
            line = _render(label, PLAIN)
            bucket["n"] += 1
            if _integrated_outcome(line, with_candidate_rule=False) == UNSAFE_BYPASS:
                bucket["live"] += 1
            corrected = _integrated_outcome(line, with_candidate_rule=True)
            if corrected == UNSAFE_BYPASS:
                bucket["bypass"] += 1
            elif corrected == SAFE_MALFORMED:
                bucket["malformed"] += 1

        label_for = {
            "deletion": "Single-character deletion",
            "ascii_substitution": "ASCII substitution (all 95)",
            "ascii_insertion": "ASCII insertion (all 95)",
            "transposition": "Adjacent transposition",
            "confusable_substitution": "Unicode / confusable substitution",
        }
        for family, numbers in expected.items():
            row = rows[label_for[family]]
            assert row[0] == numbers["n"], (family, row, numbers)
            assert row[1] == numbers["live"], (family, row, numbers)
            assert row[2] == numbers["bypass"] == 0, (family, row, numbers)
            assert row[3] == numbers["malformed"], (family, row, numbers)

        total = rows["TOTAL"]
        assert total[0] == sum(v["n"] for v in expected.values()) == len(EXHAUSTIVE)
        assert total[1] == sum(v["live"] for v in expected.values())
        assert total[2] == 0
        assert total[3] == sum(v["malformed"] for v in expected.values())

    def test_the_superseded_claims_are_recorded_and_NOT_preserved_as_family_claims(
        self, decision_flat
    ):
        """The first draft's 17/17 and 85/85 must survive only as a DISCLAIMED supersession."""
        assert "17 / 17" in decision_flat and "85 / 85" in decision_flat
        assert "are **not** preserved as a claim about the" in decision_flat
        # ...and they must NOT reappear as a live family disposition.
        d3 = decision_flat.split("#### D.3")[1].split("#### D.4")[0]
        assert "**17 / 17**" not in d3
        assert "**85 / 85**" not in d3

    def test_the_decision_states_the_safety_property_not_only_counts(self, decision_flat):
        """A count can drift; the PROPERTY is what the boundary actually guarantees.

        Scoped to SS-D.3 itself, not to the document as a whole: the same sentence also appears
        in the bounded-correction record, and a guard satisfied by that copy alone would not
        actually require SS-D.3 -- the operative disposition section -- to state it.
        """
        property_text = (
            "no cell of the exhaustive matrix, in any governed presentation, "
            "lets a later approval win"
        )
        d3 = decision_flat.split("#### D.3")[1].split("#### D.4")[0]
        assert property_text in d3.lower()
        assert property_text in decision_flat.lower()

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
    """RE-ANCHORED to THIS FILING's own immutable range.

    ``XASSET-0058`` changed no production byte -- a fact about **its own** range,
    ``THIS_UNIT_BASE_SHA .. XASSET_0058_MERGE_SHA``. Written against ``HEAD`` it silently became
    a claim that no LATER unit may change one either, which would forbid the very implementation
    this decision exists to authorize. Every claim is now proved over that immutable range, and
    the lawful Lifecycle B delta is pinned separately and exactly.
    """

    @pytest.mark.parametrize("relpath", PROTECTED_RELPATHS)
    def test_the_path_is_byte_identical_to_the_base(self, relpath):
        assert _blob_at(XASSET_0058_MERGE_SHA, relpath) == _blob_at(
            THIS_UNIT_BASE_SHA, relpath
        ), relpath

    @pytest.mark.parametrize(
        "relpath", [r for r in PROTECTED_RELPATHS if r != PRODUCTION_MODULE_RELPATH]
    )
    def test_every_other_protected_path_is_untouched_across_this_units_own_range(self, relpath):
        """XASSET-0058 §F/§H authorize ONE production surface and no other.

        RE-ANCHORED to a CLOSED IMMUTABLE RANGE. This previously compared the live
        ``HEAD`` against this unit's base, which asserted that no LATER, separately
        authorized unit may ever touch a protected path -- authority this filing does
        not have and never claimed. XASSET-0058 can only speak for its own delta, so
        that is what is measured: base -> this unit's own merge, both immutable, so the
        claim is exact and permanent instead of decaying with every later merge.
        """
        assert _blob_at(XASSET_0058_MERGE_SHA, relpath) == _blob_at(
            THIS_UNIT_BASE_SHA, relpath
        ), relpath
        # NEGATIVE PIN: the range is genuinely non-empty, so the check is not vacuous.
        assert _git("diff", "--name-only", THIS_UNIT_BASE_SHA, XASSET_0058_MERGE_SHA).strip()

    def test_the_production_module_still_carries_the_vulnerable_identity(self):
        """The vulnerable identity is preserved as ADVERSE HISTORY at this filing's own merge.

        RE-ANCHORED: XASSET-0057 §F.3 makes ``12eab05e…`` **role 2** -- a permanent negative pin,
        "never a bound end under any reading" -- and XASSET-0058 §G.3 forbids the Lifecycle B
        implementation from rebinding, re-pinning or repairing it. So it is asserted where it is
        genuinely immutable, and the live module is required to have MOVED OFF it, which is what
        proves the authorized correction actually landed.
        """
        base = _content_at(XASSET_0058_MERGE_SHA, PRODUCTION_MODULE_RELPATH)
        assert hashlib.sha256(base).hexdigest() == VULNERABLE_MODULE_SHA256
        assert _blob_at(XASSET_0058_MERGE_SHA, PRODUCTION_MODULE_RELPATH) == (
            VULNERABLE_MODULE_BLOB
        )
        live = hashlib.sha256((ROOT / PRODUCTION_MODULE_RELPATH).read_bytes()).hexdigest()
        assert live != VULNERABLE_MODULE_SHA256
        # XASSET-0057 §F.3 role 3 / XASSET-0058 §G.4: DERIVED at merge, never predicted here.
        assert live not in (ROOT / DECISION_RELPATH).read_text(encoding="utf-8")
        assert live not in WORKSTREAMS.read_text(encoding="utf-8")
        assert live not in CATALOG.read_text(encoding="utf-8")

    def test_the_register_still_binds_the_stale_digest(self):
        assert STALE_BOUND_MODULE_SHA256 != VULNERABLE_MODULE_SHA256
        raw = WORKSTREAMS.read_text(encoding="utf-8")
        assert STALE_BOUND_MODULE_SHA256 in raw

    def test_the_load_bearing_boundary_is_unchanged_at_eighteen(self):
        """The BOUNDARY is unchanged; only the parser's own bytes lawfully moved.

        RE-ANCHORED: XASSET-0058 §H forbids re-pinning or extending ``LOAD_BEARING_RELPATHS``,
        so the count and the exact membership are still asserted -- at HEAD, where it matters --
        while the byte-identity claim moves to the immutable range it was really about.
        """
        # RE-ANCHORED BY XASSET-0060, the ONE rebinding XASSET-0057 §E authorizes. THIS filing
        # left the boundary at eighteen -- immutable, and asserted over its own range below.
        # XASSET-0057 §F.7 then REQUIRED the successor to extend it, so pinning the live count at
        # eighteen asserted the opposite of the authority this suite exists to protect. Both ends
        # are bound: the eighteen this unit saw are still an ORDERED PREFIX -- nothing removed,
        # reordered or traded away -- and the live count is pinned EXACTLY at twenty-five.
        base_boundary = tuple(BASE_AUTH.LOAD_BEARING_RELPATHS)
        assert len(base_boundary) == 18
        assert tuple(AUTH.LOAD_BEARING_RELPATHS)[:18] == base_boundary
        assert len(AUTH.LOAD_BEARING_RELPATHS) == 25
        assert len(set(AUTH.LOAD_BEARING_RELPATHS)) == 25
        base = _content_at(THIS_UNIT_BASE_SHA, PRODUCTION_MODULE_RELPATH)
        assert base == _content_at(XASSET_0058_MERGE_SHA, PRODUCTION_MODULE_RELPATH)

    def test_this_module_adds_no_production_import_of_itself(self):
        """Nothing in production may import this test-only reference model."""
        source = (ROOT / PRODUCTION_MODULE_RELPATH).read_text(encoding="utf-8")
        assert Path(__file__).stem not in source

    def test_the_reference_model_is_defined_here_and_nowhere_in_production(self):
        """RE-ANCHORED, and INVERTED into the stronger claim.

        While XASSET-0058 was design-only the model existed nowhere in production, and that is
        asserted at this filing's own merge. Its Lifecycle B implementation then IMPLEMENTS the
        decided boundary, so the interesting property is no longer absence -- it is AGREEMENT.
        The real production parser is required to match this reference model on every cell of the
        exhaustive matrix, in every governed presentation, which the absence check never proved.
        """
        base = _content_at(XASSET_0058_MERGE_SHA, PRODUCTION_MODULE_RELPATH).decode("utf-8")
        for name in ("is_candidate", "def osa(", "ADMISSIBLE_COLON_INDICES"):
            assert name not in base, name
        # The model is still TEST-ONLY: production imports nothing from this module.
        live = (ROOT / PRODUCTION_MODULE_RELPATH).read_text(encoding="utf-8")
        assert Path(__file__).stem not in live
        # ...and production now AGREES with it, cell for cell.
        checked = 0
        for _f, _i, _c, label in EXHAUSTIVE:
            for form in (PLAIN, BOLD, INDENTED):
                line = _render(label, form)
                if not hook_is_reachable(line):
                    continue
                assert candidate(line) is is_candidate(line), (line, form)
                checked += 1
        assert checked >= len(EXHAUSTIVE), checked


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
        # RE-ANCHORED BY XASSET-0059: "this filing appended exactly one gate" is a claim about
        # THIS filing's own immutable range. Measured against the live register it would forbid
        # every later unit from appending one of its own, which is exactly what the convention
        # requires them to do. The APPEND-ONLY property is still asserted at HEAD -- and that is
        # the part that actually protects the record.
        merged = yaml.safe_load(
            _content_at(XASSET_0058_MERGE_SHA, "operations/WORKSTREAMS.yaml").decode("utf-8")
        )
        merged_ws = next(w for w in merged["workstreams"] if w["id"] == "WS-0014")
        assert merged_ws["milestones"][: len(before)] == before
        assert len(merged_ws["milestones"]) == len(before) + 1
        live = register["milestones"]
        assert live[: len(before)] == before, "existing gates were modified, not appended to"
        assert len(live) >= len(before) + 1

    def test_no_sentinel_survives_anywhere_in_the_register(self):
        raw = WORKSTREAMS.read_text(encoding="utf-8")
        for sentinel in (PR_SENTINEL, *PRIOR_SENTINELS):
            assert f"active_pr: {sentinel}" not in raw, sentinel
            assert f"pr: {sentinel}" not in raw, sentinel

    #: RE-ANCHORED BY XASSET-0059. WS-0014's live fields are SHARED (OPS-0001), so once this
    #: filing merged they lawfully moved onto the Lifecycle B unit SS-F authorizes. This filing's
    #: own durable record is its GATE, which does not move; the superseded values are retained
    #: below as NEGATIVE pins, so the fields stay bound at BOTH ends.
    # ADVANCED BY XASSET-0060; XASSET-0059's values are retained below as NEGATIVE pins.
    XASSET0060_BRANCH = "claude/xasset-0057-rebinding-gqtg9o"
    #: ADVANCED BY XASSET-0061; the predecessor is retained above as a negative pin.
    SUCCESSOR_BRANCH = "claude/xasset-0061-authorization-jux8p9"
    XASSET0060_MAIN_SHA_PIN = "301e79334876a4bda6e7b89a6156b34e8d38a605"
    #: ADVANCED BY XASSET-0061; the predecessor is retained above as a NEGATIVE pin.
    SUCCESSOR_MAIN_SHA = "413e033ac33741829168762ab24d73327c047d4b"
    XASSET0059_BRANCH = "claude/xasset-0058-parser-correction-a2kteq"
    XASSET0059_MAIN_SHA = "34c45900ce23742d04d80cf12471c34aabe9682d"

    def test_the_shared_live_fields_have_advanced_beyond_this_unit(self, register):
        assert register["active_branch"] != "claude/xasset-0061-authorization-jux8p9"
        assert register["last_verified_main_sha"] != "413e033ac33741829168762ab24d73327c047d4b"
        assert register["last_verified_main_sha"] != self.XASSET0060_MAIN_SHA_PIN
        assert register["active_branch"] != self.XASSET0059_BRANCH
        assert register["last_verified_main_sha"] != self.XASSET0059_MAIN_SHA
        assert register["active_branch"] != BRANCH
        assert register["last_verified_main_sha"] != THIS_UNIT_BASE_SHA
        assert register["last_verified_main_sha"] != XASSET_0057_MERGE_PARENT_1

    def test_the_active_pr_is_a_real_github_number(self, register):
        """RE-ANCHORED BY XASSET-0059 onto this filing's OWN durable record.

        ``active_pr`` is SHARED, so it now carries the successor unit's number -- and while
        that successor is still unmerged it lawfully carries an IMPOSSIBLE SENTINEL, exactly as
        this filing's own gate description records doing. Asserting a real number on the shared
        field would therefore forbid the very convention this repository uses. THIS filing's
        number is pinned where it cannot move: on its own gate.
        """
        gate = next(
            g for g in register["milestones"]
            if g["gate"] == "xasset0058-formal-disposition-parser-correction-authorization"
        )
        pr = gate["pr"]
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
        # RE-ANCHORED BY XASSET-0059, for the same reason: exactly-one-row is a claim about
        # THIS filing's own range. Append-only is still asserted at HEAD.
        merged_rows = yaml.safe_load(
            _content_at(XASSET_0058_MERGE_SHA, "governance/decisions.yaml").decode("utf-8")
        )["decisions"]
        assert len(merged_rows) == len(base_rows) + 1
        assert merged_rows[: len(base_rows)] == base_rows
        assert rows[: len(base_rows)] == base_rows
        assert len(rows) >= len(base_rows) + 1

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
            for index in ADMISSIBLE_COLON_INDICES:
                if index < len(p) and p[index] == ":" \
                        and osa(ascii_fold(p[:index]), CANON_LABEL) <= MAX_EDITS:
                    return True
            return False

        lost = [l for _, _, l in MUTANTS
                if not is_candidate_without_bold(f"**{l}: {ADVERSE_VERDICT}**")]
        assert len(lost) == 85, "the bold projection is load-bearing and must be proved so"

    def test_dropping_the_indent_trim_loses_every_indented_cell(self):
        def is_candidate_without_indent_trim(line):
            for index in ADMISSIBLE_COLON_INDICES:
                if index < len(line) and line[index] == ":" \
                        and osa(ascii_fold(line[:index]), CANON_LABEL) <= MAX_EDITS:
                    return True
            return False

        lost = [l for _, _, l in MUTANTS
                if not is_candidate_without_indent_trim(f"   {l}: {ADVERSE_VERDICT}")]
        assert len(lost) == 85

    # ---- BLOCKING 1: the colon protection is INDEPENDENTLY load-bearing ----
    def test_reverting_to_the_superseded_first_colon_rule_reopens_the_bypass(self):
        """The isolating probe. It must fail for the INTENDED reason -- an internal colon
        displacing the real terminating one -- not for any incidental difference."""
        def superseded(line):
            for projection in projections(line):
                colon = projection.find(":", 0, len(CANON_LABEL) + MAX_EDITS + 1)
                if colon == -1 or abs(colon - len(CANON_LABEL)) > MAX_EDITS:
                    continue
                if osa(ascii_fold(projection[:colon]), CANON_LABEL) <= MAX_EDITS:
                    return True
            return False

        reopened = [
            (f, i) for f, i, c, l in COLON_CELLS
            if is_candidate(_render(l, PLAIN)) and not superseded(_render(l, PLAIN))
        ]
        assert len(reopened) >= 30, reopened
        # and the reason is exactly the displacement, proved per cell
        for f, i in reopened:
            label = next(l for ff, ii, _, l in COLON_CELLS if (ff, ii) == (f, i))
            line = _render(label, PLAIN)
            assert line.find(":", 0, 20) not in ADMISSIBLE_COLON_INDICES, (f, i)
            assert any(
                k < len(line) and line[k] == ":" for k in ADMISSIBLE_COLON_INDICES
            ), (f, i)

    def test_probing_only_one_admissible_index_loses_colon_cells(self):
        """Each of the three indices carries real weight; none is decorative."""
        for only in ADMISSIBLE_COLON_INDICES:
            def narrowed(line, _only=only):
                for projection in projections(line):
                    if _only < len(projection) and projection[_only] == ":" \
                            and osa(ascii_fold(projection[:_only]), CANON_LABEL) <= MAX_EDITS:
                        return True
                return False

            lost = [(f, i) for f, i, c, l in EXHAUSTIVE
                    if is_candidate(_render(l, PLAIN)) and not narrowed(_render(l, PLAIN))]
            assert lost, f"index {only} would be decorative if narrowing to it lost nothing"

    def test_dropping_the_colon_requirement_entirely_would_break_the_prose_boundary(self):
        """Known-bad control in the OTHER direction: the colon is what keeps prose ABSENT."""
        def colonless(line):
            for projection in projections(line):
                for k in ADMISSIBLE_COLON_INDICES:
                    if osa(ascii_fold(projection[:k]), CANON_LABEL) <= MAX_EDITS:
                        return True
            return False

        prose = "formal disposition but is not in an accepted form, and stays ABSENT"
        assert not is_candidate(prose)
        assert colonless(prose), "without the colon requirement this prose would be flagged"

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

#: The generation that succeeded THIS filing: the Lifecycle B parser correction its own
#: SS-F authorizes. WS-0014's live fields are SHARED, so they lawfully moved onto it.
# ADVANCED BY XASSET-0060, on exactly the terms this file's own meta-assertions already state:
# XASSET-0059's constant becomes a NEGATIVE pin -- retained with its exact value, never deleted --
# and the newly live unit is the positive pin.
#: ADVANCED BY XASSET-0061. WS-0014's single shared live field lawfully moved onto
#: the successor. XASSET-0060's own value is RETAINED as a NEGATIVE pin, so the chain
#: stays bound at BOTH ends rather than only the newest.
XASSET0060_MAIN_SHA = "301e79334876a4bda6e7b89a6156b34e8d38a605"
XASSET0061_MAIN_SHA = "413e033ac33741829168762ab24d73327c047d4b"
SUCCESSOR_MAIN_SHA = XASSET0061_MAIN_SHA
#: ADVANCED BY XASSET-0061. XASSET-0060's branch is retained as a NEGATIVE pin.
XASSET0060_BRANCH = "claude/xasset-0057-rebinding-gqtg9o"
XASSET0061_BRANCH = "claude/xasset-0061-authorization-jux8p9"
SUCCESSOR_BRANCH_NAME = XASSET0061_BRANCH
XASSET0059_MAIN_SHA_VALUE = "34c45900ce23742d04d80cf12471c34aabe9682d"
XASSET0059_BRANCH_NAME = "claude/xasset-0058-parser-correction-a2kteq"


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
        # RE-ANCHORED: this filing's own change set is its own IMMUTABLE range. Measured at
        # HEAD it would forbid every later unit from touching any file this one touched.
        allowed |= {PRODUCTION_MODULE_RELPATH}
        tracked_changes = set(
            _git("diff", "--name-only", THIS_UNIT_BASE_SHA, XASSET_0058_MERGE_SHA).split()
        )
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
        # RE-ANCHORED BY XASSET-0059: this filing's own constant is now itself a NEGATIVE
        # pin -- retained with its exact value, never deleted -- and the successor generation
        # is the positive pin. The chain stays bound at EVERY end, not just the two newest.
        # RE-ANCHORED BY XASSET-0059: "defines the generation constant" means defines it at
        # MODULE level, which is what this scan was always about. A CLASS-scoped
        # ``SUCCESSOR_*``/``XASSET00NN_*`` attribute is the OTHER convention, and it is covered
        # by ``test_the_successor_named_suites_advanced_their_successor_constants`` -- requiring
        # both shapes of the same file would demand a pin that suite does not use. Anchoring on
        # the line start makes the filter EXACT rather than merely narrower.
        defining = [
            name for name in REANCHORED_SUITES
            if f'\nXASSET0058_MAIN_SHA = "{THIS_UNIT_BASE_SHA}"'
            in (ROOT / name).read_text(encoding="utf-8")
        ]
        assert len(defining) >= 9, defining
        for name in defining:
            live = (ROOT / name).read_text(encoding="utf-8")
            assert "!= XASSET0058_MAIN_SHA" in live, name
            # ADVANCED BY XASSET-0060: XASSET-0059's constant is retained with its exact value
            # as a NEGATIVE pin, and the newly live unit's constant is the positive one.
            assert f'XASSET0059_MAIN_SHA = "{XASSET0059_MAIN_SHA_VALUE}"' in live, name
            assert "!= XASSET0059_MAIN_SHA" in live, name
            # ADVANCED BY XASSET-0061: XASSET-0060's constant becomes a NEGATIVE pin,
            # retained with its exact value, and XASSET-0061 is the positive pin.
            assert f'XASSET0060_MAIN_SHA = "{XASSET0060_MAIN_SHA}"' in live, name
            assert "!= XASSET0060_MAIN_SHA" in live, name
            assert f'XASSET0061_MAIN_SHA = "{SUCCESSOR_MAIN_SHA}"' in live, name
            # XASSET-0061 is historical and must remain an exact negative pin.
            assert '!= "413e033ac33741829168762ab24d73327c047d4b"' in live, name
            assert f'XASSET0057_MAIN_SHA = "{SUPERSEDED_GENERATION_SHA}"' in live, name
            assert "!= XASSET0057_MAIN_SHA" in live, name

    def test_the_successor_named_suites_advanced_their_successor_constants(self):
        """The suites that track their successor by NAME rather than by generation constant are
        advanced on the same terms: the new value is the positive pin, and this unit's
        predecessor is retained as a negative pin."""
        for name in ("test_level1_stage1_verdict_boundary_governance.py",
                     "test_level1_stage1_parser_contract_correction_authorization.py"):
            live = (ROOT / name).read_text(encoding="utf-8")
            # RE-ANCHORED BY XASSET-0059: the SUCCESSOR constants name the newly live unit,
            # and this filing's own generation is retained beside them as a NEGATIVE pin.
            assert f'SUCCESSOR_MAIN_SHA = XASSET0061_MAIN_SHA' in live or (
                f'SUCCESSOR_MAIN_SHA = "{SUCCESSOR_MAIN_SHA}"' in live) or (
                "SUCCESSOR_MAIN_SHA = XASSET0060_MAIN_SHA" in live
            ), name
            assert f'SUCCESSOR_BRANCH = "{SUCCESSOR_BRANCH_NAME}"' in live, name
            assert '!= "413e033ac33741829168762ab24d73327c047d4b"' in live, name
            assert f'XASSET0059_BRANCH = "{XASSET0059_BRANCH_NAME}"' in live, name
            assert f'XASSET0058_BRANCH = "{BRANCH}"' in live, name
            assert f'XASSET0057_BRANCH = "{SUPERSEDED_GENERATION_BRANCH}"' in live, name
            assert "XASSET-0058" in live, name
            assert "XASSET-0059" in live, name
            assert "XASSET-0060" in live, name

    def test_the_re_anchoring_is_non_vacuous_at_the_base(self):
        """Each re-anchored suite must genuinely have failed at the base under this unit's
        register, otherwise the edits were cosmetic."""
        base_register = _content_at(THIS_UNIT_BASE_SHA, "operations/WORKSTREAMS.yaml").decode("utf-8")
        before = next(
            w for w in yaml.safe_load(base_register)["workstreams"] if w["id"] == "WS-0014"
        )
        live = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
        now = next(w for w in live["workstreams"] if w["id"] == "WS-0014")
        # RE-ANCHORED BY XASSET-0059. "This filing moved the shared fields onto itself" is a
        # fact about THIS filing's own range, so it is proved at THIS filing's own merge. The
        # shared fields have since lawfully moved again, onto the Lifecycle B unit -- which is
        # the convention working, not a regression -- and that is asserted separately below.
        merged = yaml.safe_load(
            _content_at(XASSET_0058_MERGE_SHA, "operations/WORKSTREAMS.yaml").decode("utf-8")
        )
        at_merge = next(w for w in merged["workstreams"] if w["id"] == "WS-0014")
        assert before["last_verified_main_sha"] == SUPERSEDED_GENERATION_SHA
        assert before["active_branch"] == SUPERSEDED_GENERATION_BRANCH
        assert at_merge["last_verified_main_sha"] == THIS_UNIT_BASE_SHA
        assert at_merge["active_branch"] == BRANCH
        assert at_merge["last_verified_main_sha"] != before["last_verified_main_sha"]
        assert at_merge["active_branch"] != before["active_branch"]
        # ...and the SHARED fields now name the successor, bound at BOTH ends.
        assert now["last_verified_main_sha"] != THIS_UNIT_BASE_SHA
        assert now["active_branch"] != BRANCH
        assert now["last_verified_main_sha"] != before["last_verified_main_sha"]

    def test_the_decision_discloses_the_re_anchoring(self, decision_flat):
        assert "re-anchor" in decision_flat.lower()
