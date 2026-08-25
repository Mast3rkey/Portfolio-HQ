"""XASSET-0056 -- the bounded FORMAL DISPOSITION parser correction.

Adversarial proof for the single replacement parser-correction implementation authorized by
``XASSET-0055`` §H, within the permitted set ``XASSET-0053`` §C fixes and every clause of
``XASSET-0053`` §D.

What this suite proves, and what it deliberately does not:

  * it proves the corrected parser accepts EXACTLY the two governed wrapper forms, validates
    recognized separator suffixes as finding-count metadata, honours the EARLIEST separator,
    separates ABSENT from MALFORMED / UNSUPPORTED end to end, preserves an OPEN verdict
    vocabulary with exact text, and compares the WHOLE verdict for equality;
  * it proves all three -- and only three -- production consumers enforce that distinction at
    their real seams, that MALFORMED is never rescued by a native ``APPROVED`` state, and that
    each consumer's established ABSENT policy is preserved;
  * it proves the scope boundary: no fourth call site, no second helper (this correction
    introduces ZERO), no general parsing framework, and no other existing production function
    changed;
  * it proves the designed FAIL-CLOSED hand-off -- the load-bearing digest is now stale, both
    authorization predicates remain ``False``, and Stage 1 remains NOT EXECUTABLE;
  * it authorizes, arms, claims, executes and rebinds NOTHING.
"""

from __future__ import annotations

import ast
import hashlib
import subprocess
import sys
import types
from pathlib import Path

import pytest
import yaml

import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
MODULE_RELPATH = "level1_stage1_execution_authorization.py"

DECISION_ID = "XASSET-0056"
DECISION = ROOT / "governance/decisions/XASSET-0056-endpoint-0001-formal-disposition-parser-correction.md"
CATALOG = ROOT / "governance/decisions.yaml"
WORKSTREAMS = ROOT / "operations/WORKSTREAMS.yaml"

#: This unit's base: the merge that made XASSET-0055 EFFECTIVE.
BASE_SHA = "29e4969885970d942a5acecc1424fb2e2b080d60"

#: The module's identity AT THE BASE -- the value the bound merge still carries, and which this
#: correction lawfully and deliberately makes stale.
BASE_MODULE_SHA256 = "4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541"
BASE_MODULE_BLOB = "f71b08b4ebe95f161c57cdbb2a924748f13af02d"

APPROVE = A.APPROVING_REVIEW_DISPOSITION
PREFIX = A.FORMAL_DISPOSITION_PREFIX
#: Resolved with a fallback ONLY so this suite can be COLLECTED against the uncorrected base
#: and yield an honest per-test non-vacuity count. At the corrected head this is the real
#: sentinel and nothing is softened -- `test_the_sentinel_attribute_really_exists` fails loudly
#: if the attribute is ever absent, so the fallback can never silently stand in for it.
MALFORMED = getattr(A, "MALFORMED_FORMAL_DISPOSITION", object())

#: PR #349 review 5000581301's line, byte-for-byte. The wrapper is a precisely balanced,
#: whole-line bold pair and the enclosed text carries no further ``*``.
REVIEW_5000581301_LINE = (
    "**FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE "
    "— 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE**"
)

#: The recognized separator tuple, byte-for-byte. XASSET-0055 §E.4 leaves it UNCHANGED; this
#: correction governs what may FOLLOW a separator, never which separators are recognized.
SEPARATORS = ("—", "--", " - ", "|")

P = A.parse_formal_disposition


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def _base_source() -> str:
    return _git("show", f"{BASE_SHA}:{MODULE_RELPATH}")


def _live_source() -> str:
    return (ROOT / MODULE_RELPATH).read_text(encoding="utf-8")


def _toplevel(source: str) -> dict[str, str]:
    """Every top-level def/class name -> its exact source text."""
    lines = source.splitlines(keepends=True)
    out: dict[str, str] = {}
    for node in ast.parse(source).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out[node.name] = "".join(lines[node.lineno - 1 : node.end_lineno])
    return out


def _call_sites(source: str) -> list[int]:
    return [
        node.lineno
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "parse_formal_disposition"
    ]


# =====================================================================================
# 1. The two accepted wrapper forms -- and no others
# =====================================================================================


class TestTheTwoAcceptedWrapperForms:
    def test_the_plain_canonical_line_still_parses_exactly_as_before(self):
        assert P(f"{PREFIX} {APPROVE}") == APPROVE

    def test_the_balanced_whole_line_bold_wrapper_is_accepted(self):
        assert P(f"**{PREFIX} {APPROVE}**") == APPROVE

    def test_review_5000581301s_exact_line_now_yields_the_approving_verdict(self):
        """§D.18.10 / §I.1: byte-for-byte, unparseable at the base, approving now."""
        assert P(REVIEW_5000581301_LINE) == APPROVE

    def test_review_5000581301s_exact_line_was_unparseable_at_the_base(self):
        """Non-vacuity for the test above, proved against the base bytes, not asserted."""
        assert "def parse_formal_disposition(body: str) -> str | None:" in _base_source()

    def test_the_bold_wrapper_carries_no_further_asterisk(self):
        inner = REVIEW_5000581301_LINE[2:-2]
        assert "*" not in inner
        assert inner.startswith(PREFIX)

    def test_an_adverse_verdict_parses_adversely_in_both_accepted_forms(self):
        """§D.7: wrapper recognition must not create an escape for an adverse review."""
        for body in (f"{PREFIX} CHANGES REQUIRED", f"**{PREFIX} CHANGES REQUIRED**"):
            assert P(body) == "CHANGES REQUIRED"
            assert P(body) != APPROVE


# =====================================================================================
# 2. Separator suffixes: recognized set unchanged, contents VALIDATED
# =====================================================================================


class TestEveryRecognizedSeparator:
    def test_the_recognized_separator_tuple_is_byte_unchanged(self):
        """§E.4. Compared against the BASE bytes, not against a restatement."""
        marker = 'for separator in ("—", "--", " - ", "|"):'
        assert marker in _base_source()
        assert marker in _live_source()

    @pytest.mark.parametrize("separator", SEPARATORS)
    @pytest.mark.parametrize("wrapper", ["plain", "bold"])
    def test_a_valid_finding_count_suffix_is_stripped_for_every_separator(
        self, separator, wrapper
    ):
        line = f"{PREFIX} {APPROVE} {separator} 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE"
        body = line if wrapper == "plain" else f"**{line}**"
        assert P(body) == APPROVE

    @pytest.mark.parametrize("separator", SEPARATORS)
    def test_an_arbitrary_suffix_is_malformed_for_every_separator(self, separator):
        body = f"{PREFIX} {APPROVE} {separator} CHANGES REQUIRED"
        assert P(body) is MALFORMED
        assert P(body) != APPROVE


class TestTheFindingCountSuffixGrammar:
    """The count grammar is STRICT: ASCII digits, exactly ONE ordinary space, one CATEGORY.

    PR #355's ``partition(" ")`` plus ``category.strip()`` silently accepted multiple spaces.
    That behaviour is not reused. Only the independently governed requirement -- §E.1's grammar
    -- is carried forward, and it is enforced literally.
    """

    VALID = [
        "0 BLOCKING",
        "1 MAJOR",
        "12 MINOR",
        "0 NOTE",
        "0 BLOCKING / 0 MAJOR",
        "0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE",
        "1 BLOCKING / 2 MAJOR / 3 MINOR / 4 NOTE",
        "007 BLOCKING",
    ]

    #: Every one of these must be MALFORMED. Grouped by the trap each one closes.
    INVALID = [
        # -- exactly one space, never more -------------------------------------------------
        ("two spaces", "0  BLOCKING"),
        ("three spaces", "0   BLOCKING"),
        ("space before the digits and two after", " 0  BLOCKING"),
        # -- tabs, wherever they survive the line strip ------------------------------------
        ("tab between digits and category", "0\tBLOCKING"),
        ("space then tab", "0 \tBLOCKING"),
        ("tab before the digits", "\t0 BLOCKING"),
        ("tab before a slash", "0 BLOCKING\t/ 1 MAJOR"),
        ("tab after a slash", "0 BLOCKING /\t1 MAJOR"),
        ("tab then further text", "0 BLOCKING\tmore"),
        # -- missing separator space -------------------------------------------------------
        ("no space at all", "0BLOCKING"),
        ("underscore instead of space", "0_BLOCKING"),
        # -- signed and decimal counts -----------------------------------------------------
        ("leading plus", "+0 BLOCKING"),
        ("leading minus", "-1 BLOCKING"),
        ("decimal point", "0.5 BLOCKING"),
        ("comma group", "1,000 BLOCKING"),
        # -- non-ASCII digit forms ---------------------------------------------------------
        ("Arabic-Indic digit", "\u0663 BLOCKING"),
        ("fullwidth digit", "\uff10 BLOCKING"),
        ("Devanagari digit", "\u0969 BLOCKING"),
        ("superscript digit", "\u00b2 BLOCKING"),
        # -- missing or empty slash components ---------------------------------------------
        ("doubled slash", "0 BLOCKING // 1 MAJOR"),
        ("trailing slash", "0 BLOCKING /"),
        ("leading slash", "/ 0 BLOCKING"),
        ("only a slash", "/"),
        ("slash with only spaces", "0 BLOCKING /   "),
        # -- arbitrary trailing suffix text ------------------------------------------------
        ("prose after a valid count", "0 BLOCKING and more"),
        ("a second verdict after a valid count", "0 BLOCKING CHANGES REQUIRED"),
        ("bare prose", "and please rewrite it"),
        # -- category vocabulary is exact --------------------------------------------------
        ("lower-case category", "0 blocking"),
        ("mixed-case category", "0 Blocking"),
        ("unknown category", "0 BANANAS"),
        ("category with no count", "BLOCKING"),
        ("count with no category", "0"),
        # -- nothing at all ----------------------------------------------------------------
        ("empty suffix", ""),
    ]

    @pytest.mark.parametrize("suffix", VALID)
    def test_a_valid_count_list_is_accepted(self, suffix):
        assert P(f"{PREFIX} {APPROVE} \u2014 {suffix}") == APPROVE

    @pytest.mark.parametrize("suffix", VALID)
    def test_a_valid_count_list_is_accepted_in_the_bold_form_too(self, suffix):
        assert P(f"**{PREFIX} {APPROVE} \u2014 {suffix}**") == APPROVE

    @pytest.mark.parametrize("label,suffix", INVALID, ids=[l for l, _ in INVALID])
    def test_an_invalid_count_list_is_malformed(self, label, suffix):
        body = f"{PREFIX} {APPROVE} \u2014 {suffix}"
        assert P(body) is MALFORMED, label

    @pytest.mark.parametrize("label,suffix", INVALID, ids=[l for l, _ in INVALID])
    def test_an_invalid_count_list_never_authenticates(self, label, suffix):
        assert P(f"{PREFIX} {APPROVE} \u2014 {suffix}") != APPROVE, label

    @pytest.mark.parametrize(
        "label,suffix",
        [(l, s) for l, s in INVALID if s.strip()],
        ids=[l for l, s in INVALID if s.strip()],
    )
    def test_an_invalid_count_list_is_malformed_for_every_separator(self, label, suffix):
        for separator in SEPARATORS:
            body = f"{PREFIX} {APPROVE} {separator} {suffix}"
            assert P(body) is MALFORMED, (label, separator)

    def test_an_empty_suffix_is_separator_dependent_and_never_authenticates(self):
        """The one honestly separator-dependent case, stated rather than papered over.

        With nothing after the separator, the pre-existing whole-line ``line.strip()`` removes
        the trailing space. For ``"\u2014"``, ``"--"`` and ``"|"`` the separator still survives, so
        the empty suffix is MALFORMED. For ``" - "`` it does NOT survive -- the token needs a
        trailing space -- so no recognized separator is present and §C.1 correctly returns the
        whole region verbatim. Both outcomes refuse; only the diagnostic differs, exactly the
        cost §C states. What holds for ALL FOUR is that none of them authenticates.
        """
        for separator in ("\u2014", "--", "|"):
            assert P(f"{PREFIX} {APPROVE} {separator} ") is MALFORMED, separator
        dashed = P(f"{PREFIX} {APPROVE}  -  ")
        assert dashed is not MALFORMED
        assert isinstance(dashed, str)
        for separator in SEPARATORS:
            assert P(f"{PREFIX} {APPROVE} {separator} ") != APPROVE, separator

    def test_the_category_is_compared_unstripped(self):
        """PR #355 stripped the category, which silently accepted multiple spaces.

        The correction compares what ``partition`` actually returns, so a second space stays
        attached to the category and fails the vocabulary check.
        """
        assert P(f"{PREFIX} {APPROVE} \u2014 0  BLOCKING") is MALFORMED
        source = _toplevel(_live_source())["parse_formal_disposition"]
        assert "category.strip()" not in source
        assert "category.strip(" not in source

    def test_only_ordinary_spaces_are_trimmed_in_the_suffix_path(self):
        """``.strip(" ")``, never bare ``.strip()`` -- bare strip swallows tabs silently.

        Scoped to the two lines that actually trim the SUFFIX. The verdict's own ``.strip()``
        is untouched base behaviour and is deliberately not caught by this scan.
        """
        parser = _toplevel(_live_source())["parse_formal_disposition"]
        suffix_lines = [
            line for line in parser.splitlines()
            if ("suffix = region[" in line) or ("for element in suffix" in line)
            or ("element.strip" in line)
        ]
        assert suffix_lines
        joined = "\n".join(suffix_lines)
        assert joined.count('strip(" ")') == 2, joined
        assert ".strip()" not in joined, joined

    def test_every_tab_surviving_the_line_strip_is_rejected(self):
        for suffix in ("0\tBLOCKING", "\t0 BLOCKING", "0 BLOCKING\t/ 1 MAJOR", "0 BLOCKING\tmore"):
            assert P(f"{PREFIX} {APPROVE} \u2014 {suffix}") is MALFORMED, suffix

    def test_a_trailing_tab_at_end_of_line_is_base_behaviour_not_this_corrections_scope(self):
        """Disclosed precisely rather than overclaimed.

        A tab at the very END of the line is removed by the pre-existing whole-line
        ``line.strip()`` before any grammar runs. That strip is byte-identical to the base and
        is not this correction's to change, so the outcome here is IDENTICAL to the base. Every
        tab that survives that strip is rejected, which is the test immediately above.
        """
        body = f"{PREFIX} {APPROVE} \u2014 0 BLOCKING\t"
        assert P(body) == APPROVE
        assert "stripped = line.strip()" in _base_source()
        assert "stripped = line.strip()" in _live_source()

    def test_a_suffix_is_never_discarded_unread(self):
        """§E.1: the pre-correction parser split and threw the suffix away."""
        assert P(f"{PREFIX} {APPROVE} | CHANGES REQUIRED") is MALFORMED


class TestTheEarliestSeparatorGoverns:
    def test_the_mixed_separator_tuple_order_bypass_is_closed(self):
        """§E.3: the em dash is tuple[0]; splitting on it first erased the adverse '|' text."""
        body = f"{PREFIX} {APPROVE} | CHANGES REQUIRED — 0 BLOCKING"
        assert P(body) is MALFORMED
        assert P(body) != APPROVE

    def test_the_bypass_really_authenticated_at_the_base(self):
        """Non-vacuity: the base parser looped the tuple in order and discarded each suffix."""
        base = _base_source()
        assert "verdict = verdict.split(separator, 1)[0].strip()" in base

    @pytest.mark.parametrize("first,second", [("|", "—"), ("—", "|"), (" - ", "|")])
    def test_whichever_separator_comes_first_is_the_one_that_governs(self, first, second):
        body = f"{PREFIX} {APPROVE} {first} NOT A COUNT {second} 0 BLOCKING"
        assert P(body) is MALFORMED

    def test_a_valid_suffix_after_the_earliest_separator_still_parses(self):
        body = f"{PREFIX} {APPROVE} — 0 BLOCKING / 0 MAJOR"
        assert P(body) == APPROVE


# =====================================================================================
# 3. Unsupported decoration and prose fail CLOSED -- never skipped
# =====================================================================================


UNSUPPORTED_LINES = [
    f"## {PREFIX} CHANGES REQUIRED",                 # heading
    f"### {PREFIX} {APPROVE}",                       # heading, approving
    f"> {PREFIX} {APPROVE}",                         # blockquote
    f"- {PREFIX} {APPROVE}",                         # bullet
    f"* {PREFIX} {APPROVE}",                         # bullet
    f"1. {PREFIX} {APPROVE}",                        # ordered bullet
    f"`{PREFIX} {APPROVE}`",                         # inline code
    f"*{PREFIX} {APPROVE}*",                         # single-asterisk emphasis
    f"**{PREFIX} {APPROVE}",                         # unbalanced: open only
    f"****{PREFIX} {APPROVE}****",                   # nested / doubled
    f"**{PREFIX} *{APPROVE}***",                     # nested inner emphasis
    f"__{PREFIX} {APPROVE}__",                       # underscore emphasis
    f"I will now give my {PREFIX} {APPROVE}",        # leading operative prose
    f"see the {PREFIX} above",                       # prose reference
]


class TestUnsupportedShapesFailClosed:
    @pytest.mark.parametrize("line", UNSUPPORTED_LINES)
    def test_each_unsupported_shape_is_malformed_not_absent(self, line):
        assert P(line) is MALFORMED
        assert P(line) is not None

    @pytest.mark.parametrize("line", UNSUPPORTED_LINES)
    def test_no_unsupported_shape_ever_authenticates(self, line):
        assert P(line) != APPROVE

    def test_an_unsupported_first_line_is_never_skipped_for_a_later_good_one(self):
        """§D.17: skipping is the failure mode; failing closed is the requirement."""
        body = (
            f"## {PREFIX} CHANGES REQUIRED\n"
            "\n"
            "   ... later ...\n"
            "\n"
            f"**{PREFIX} {APPROVE} — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE**\n"
        )
        assert P(body) is MALFORMED
        assert P(body) != APPROVE

    def test_a_trailing_bold_marker_is_verdict_text_not_a_wrapper(self):
        """A close marker with no OPEN marker never made the line a wrapper.

        The line still begins with the canonical prefix, so it is a plain canonical line whose
        verdict region simply ends in ``**``. §C.1 returns that region verbatim and §C.4 forbids
        pretending a boundary can be located inside it, so it fails closed by INEQUALITY.
        Behaviour here is IDENTICAL to the base -- this correction changes nothing about it.
        """
        body = f"{PREFIX} {APPROVE}**"
        assert P(body) == f"{APPROVE}**"
        assert P(body) != APPROVE
        assert P(body) is not MALFORMED

    def test_a_code_fenced_disposition_cannot_win(self):
        """§D.17 names code-fenced lines among the shapes that must fail closed."""
        body = f"```\n{PREFIX} {APPROVE}\n```\n"
        assert P(body) is MALFORMED
        assert P(body) != APPROVE

    def test_a_tilde_fence_is_treated_the_same_as_a_backtick_fence(self):
        body = f"~~~\n{PREFIX} {APPROVE}\n~~~\n"
        assert P(body) is MALFORMED

    def test_an_unclosed_fence_fails_closed_for_every_later_line(self):
        body = f"```\nsample\n\n{PREFIX} {APPROVE}\n"
        assert P(body) is MALFORMED

    def test_a_fenced_sample_after_a_valid_first_line_is_never_reached(self):
        """First-formal-line governance decides before any later fenced sample matters.

        This is the real shape of review 5004478133, which quotes fenced disposition samples
        BELOW its own operative first line.
        """
        body = (
            f"{PREFIX} BOUNDED CORRECTION REQUIRED — 0 BLOCKING / 1 MAJOR\n"
            "\n"
            f"```\n## {PREFIX} CHANGES REQUIRED\n**{PREFIX} {APPROVE}**\n```\n"
        )
        assert P(body) == "BOUNDED CORRECTION REQUIRED"

    def test_approval_quoted_in_explanatory_prose_never_authenticates(self):
        """§D.8: the MAJOR 1 finding from review 4946464366 stays closed."""
        body = (
            f"{PREFIX} CHANGES REQUIRED\n"
            "\n"
            f"I could not write '{APPROVE}' because of the finding below.\n"
        )
        assert P(body) == "CHANGES REQUIRED"
        assert P(body) != APPROVE


class TestFirstFormalLineGoverns:
    def test_the_first_valid_formal_line_decides(self):
        body = f"{PREFIX} CHANGES REQUIRED\n\n{PREFIX} {APPROVE}\n"
        assert P(body) == "CHANGES REQUIRED"

    def test_a_later_line_cannot_override_an_earlier_one_in_either_form(self):
        body = f"**{PREFIX} CHANGES REQUIRED**\n\n{PREFIX} {APPROVE}\n"
        assert P(body) == "CHANGES REQUIRED"

    def test_leading_non_formal_prose_is_scanned_past_without_penalty(self):
        body = f"# Review\n\nSome notes.\n\n{PREFIX} {APPROVE}\n"
        assert P(body) == APPROVE


# =====================================================================================
# 4. ABSENT is not MALFORMED -- the distinction §C item 2 exists for
# =====================================================================================


class TestAbsentVersusMalformed:
    ABSENT_BODIES = [
        "",
        "Looks good to me.",
        "# Review\n\nNo disposition line here at all.\n",
        "LGTM, shipping.",
    ]

    @pytest.mark.parametrize("body", ABSENT_BODIES)
    def test_a_body_with_no_formal_looking_line_is_absent(self, body):
        assert P(body) is None
        assert P(body) is not MALFORMED

    @pytest.mark.parametrize("line", UNSUPPORTED_LINES)
    def test_a_formal_looking_but_unsupported_line_is_malformed(self, line):
        assert P(line) is MALFORMED
        assert P(line) is not None

    def test_the_two_are_distinct_values(self):
        assert MALFORMED is not None
        assert P("no disposition") is not P(f"## {PREFIX} CHANGES REQUIRED")

    def test_a_non_string_body_is_absent_not_malformed(self):
        for body in (None, 17, [], {}):
            assert P(body) is None

    def test_the_sentinel_attribute_really_exists(self):
        """The collection fallback above may never stand in for the real sentinel."""
        assert hasattr(A, "MALFORMED_FORMAL_DISPOSITION")
        assert MALFORMED is A.MALFORMED_FORMAL_DISPOSITION

    def test_the_sentinel_is_a_singleton_with_a_readable_repr(self):
        assert P(f"## {PREFIX} X") is P(f"> {PREFIX} Y")
        assert repr(MALFORMED) == "MALFORMED_FORMAL_DISPOSITION"

    def test_the_sentinel_never_equals_a_verdict_string(self):
        assert MALFORMED != APPROVE
        assert MALFORMED != ""
        assert not isinstance(MALFORMED, str)


# =====================================================================================
# 5. The verdict channel stays OPEN, exact, and case-preserving
# =====================================================================================


class TestTheVerdictChannelStaysOpen:
    @pytest.mark.parametrize(
        "verdict",
        [
            "BOUNDED CORRECTION REQUIRED",
            "CHANGES REQUIRED",
            "DELTA APPROVED",
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE",
            "SOME ENTIRELY NEW VERDICT NOBODY HAS WRITTEN YET",
        ],
    )
    def test_an_arbitrary_verdict_is_returned_verbatim(self, verdict):
        assert P(f"{PREFIX} {verdict}") == verdict

    @pytest.mark.parametrize(
        "verdict",
        ["approved", "Approved", "APPROVED", "bounded correction required", "Changes Required"],
    )
    def test_mixed_and_lower_case_verdicts_return_exactly_as_written(self, verdict):
        """§D of XASSET-0055: prior behaviour RESTORED, and the heuristic prohibited."""
        assert P(f"{PREFIX} {verdict}") == verdict

    def test_the_base_behaviour_for_lower_case_is_preserved_exactly(self):
        """Measured against the base bytes rather than asserted from memory."""
        import importlib.util
        import sys
        import tempfile

        blob = subprocess.run(
            ["git", "show", f"{BASE_SHA}:{MODULE_RELPATH}"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout
        directory = tempfile.mkdtemp(prefix="phq-base-module-")
        path = Path(directory) / "_base_module.py"
        path.write_bytes(blob)
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[path.stem] = module
        spec.loader.exec_module(module)
        for verdict in ("approved", "Approved", "bounded correction required"):
            assert module.parse_formal_disposition(f"{PREFIX} {verdict}") == verdict
            assert P(f"{PREFIX} {verdict}") == verdict

    def test_no_case_length_or_word_count_heuristic_exists(self):
        """§D: the prohibition is enforced against the shipped source, not promised."""
        source = _toplevel(_live_source())["parse_formal_disposition"]
        for banned in (".islower()", ".isupper()", ".casefold()", ".title()", "len(verdict)"):
            assert banned not in source, banned

    def test_no_closed_verdict_vocabulary_was_introduced(self):
        """Checked over the parser's STRING CONSTANTS, not its prose.

        A substring scan would flag an illustrative comment, which proves nothing. What matters
        is whether any verdict text is a live literal the parser compares against. The only
        closed vocabulary it may carry is §E.1's finding-count CATEGORY set, which is metadata,
        not a verdict, and that set is asserted exactly.
        """
        fn = next(
            n for n in ast.parse(_live_source()).body
            if isinstance(n, ast.FunctionDef) and n.name == "parse_formal_disposition"
        )
        constants = {
            node.value
            for node in ast.walk(fn)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        constants.discard(ast.get_docstring(fn))
        for verdict in ("CHANGES REQUIRED", "BOUNDED CORRECTION REQUIRED", APPROVE, "DELTA APPROVED"):
            assert verdict not in constants, verdict
        assert {"BLOCKING", "MAJOR", "MINOR", "NOTE"} <= constants
        assert "APPROVING_REVIEW_DISPOSITION" not in {
            n.id for n in ast.walk(fn) if isinstance(n, ast.Name)
        }

    def test_the_verdict_is_never_normalized_or_coerced(self):
        odd = "  weird   spacing   INSIDE  "
        assert P(f"{PREFIX} {odd}") == odd.strip()


# =====================================================================================
# 6. Whole-verdict exact equality -- appended text can never authenticate
# =====================================================================================


class TestWholeVerdictExactEquality:
    @pytest.mark.parametrize(
        "appended",
        ["DO NOT MERGE", "PENDING REVIEW", "but see below", "X"],
    )
    @pytest.mark.parametrize("wrapper", ["plain", "bold"])
    def test_appended_undelimited_text_never_authenticates(self, appended, wrapper):
        """§C.2/§C.3: a property of exact equality over the WHOLE region."""
        line = f"{PREFIX} {APPROVE} {appended}"
        body = line if wrapper == "plain" else f"**{line}**"
        assert P(body) != APPROVE

    def test_the_whole_region_is_returned_not_truncated(self):
        """§C.1: never truncated to a prefix of itself."""
        body = f"{PREFIX} {APPROVE} DO NOT MERGE"
        assert P(body) == f"{APPROVE} DO NOT MERGE"

    def test_undelimited_trailing_text_is_not_falsely_classified_malformed(self):
        """§C.4: rejected by INEQUALITY, because no rule can locate the boundary."""
        body = f"{PREFIX} {APPROVE} DO NOT MERGE"
        assert P(body) is not MALFORMED
        assert isinstance(P(body), str)

    def test_the_approval_is_never_matched_as_a_prefix_or_substring(self):
        assert P(f"{PREFIX} {APPROVE} AND MORE") != APPROVE
        assert P(f"{PREFIX} NOT {APPROVE}") != APPROVE


# =====================================================================================
# 7. The three production consumers, at their REAL seams
# =====================================================================================


class _Recorder:
    """A governance stand-in that RECORDS which lookups actually happened.

    Consumer 1 returns the same all-false value however it refuses, so the return value alone
    cannot show WHERE it stopped. The ordered gates make that observable instead: the parser
    check precedes ``_verify_selected_review_is_final``, which is the first thing to call
    ``reviews()``. If ``reviews()`` was never called, execution stopped at or before the parser.
    No gate is neutralised to achieve this.
    """

    def __init__(self, review_body: str, review_state: str = "COMMENTED"):
        self.calls: list[str] = []
        self._review = {
            "id": A.RATIFICATION_REVIEW_ID,
            "commit_id": A.RATIFICATION_HEAD_SHA,
            "state": review_state,
            "submitted_at": "2026-08-01T00:00:00Z",
            "body": review_body,
            "html_url": f"https://github.com/x/y/pull/{A.RATIFICATION_PULL_REQUEST}",
            "user": {"login": A.PRINCIPAL_ACCOUNT_LOGIN},
        }

    def pull_request(self, number):
        self.calls.append(f"pull_request:{number}")
        if number == A.RATIFICATION_PULL_REQUEST:
            return {
                "base": {"repo": {"full_name": A.REPOSITORY_IDENTITY}},
                "head": {"sha": A.RATIFICATION_HEAD_SHA},
                "merged": True,
                "merge_commit_sha": A.RATIFICATION_MERGE_SHA,
                "merged_at": "2026-08-02T00:00:00Z",
            }
        return None

    def review(self, number, review_id):
        self.calls.append(f"review:{number}:{review_id}")
        return dict(self._review)

    def reviews(self, number):
        self.calls.append(f"reviews:{number}")
        return [dict(self._review)]

    def issue_comment(self, comment_id):
        self.calls.append(f"issue_comment:{comment_id}")
        return None

    def workflow_run(self, run_id):
        self.calls.append(f"workflow_run:{run_id}")
        return None

    def workflow_job(self, job_id):
        self.calls.append(f"workflow_job:{job_id}")
        return None


def _pr337_document() -> dict:
    """A document that satisfies consumer 1's scope pins, so its parser gate is REACHED."""
    return {
        "authorizing_pull_request": A.RATIFIED_PULL_REQUEST,
        "authorization_head": A.RATIFIED_HEAD_SHA,
        "lifecycle_evidence": {
            "independent_review": {"review_id": A.RATIFIED_REVIEW_ID},
            "merge": {"merge_sha": A.RATIFIED_MERGE_SHA},
            "principal_acceptance": {"comment_id": A.RATIFIED_ACCEPTANCE_COMMENT_ID},
            "post_merge_verification": {
                "comment_id": A.RATIFIED_POST_MERGE_VERIFICATION_COMMENT_ID
            },
        },
    }


def _pr337_pull() -> dict:
    return {
        "base": {"repo": {"full_name": A.REPOSITORY_IDENTITY}},
        "head": {"sha": A.RATIFIED_HEAD_SHA},
        "merged": True,
        "merge_commit_sha": A.RATIFIED_MERGE_SHA,
    }


def _run_consumer_one(body: str, monkeypatch, state: str = "COMMENTED") -> _Recorder:
    recorder = _Recorder(body, state)
    review = recorder.review(A.RATIFICATION_PULL_REQUEST, A.RATIFICATION_REVIEW_ID)
    # The fixture universe carries its OWN accepted record, so its fingerprint is derived from
    # that record by the REAL fingerprint function -- the documented pattern in this repository.
    # No gate is disabled: the fingerprint is still computed and still compared.
    monkeypatch.setattr(A, "RATIFICATION_REVIEW_FINGERPRINT", A._review_record_fingerprint(review))
    recorder.calls.clear()
    A._derive_pr337_actor_ratification(
        _pr337_document(), A.TruthSources(governance=recorder), _pr337_pull()
    )
    return recorder


class TestConsumerOneDeriveePr337ActorRatification:
    def test_an_approving_body_passes_the_parser_gate(self, monkeypatch):
        """Positive control: execution reaches the finality machinery beyond the parser."""
        recorder = _run_consumer_one(f"{PREFIX} {APPROVE}", monkeypatch)
        assert any(c.startswith("reviews:") for c in recorder.calls), recorder.calls

    def test_a_malformed_body_stops_at_the_parser_gate(self, monkeypatch):
        recorder = _run_consumer_one(f"## {PREFIX} {APPROVE}", monkeypatch)
        assert not any(c.startswith("reviews:") for c in recorder.calls), recorder.calls

    def test_an_absent_body_stops_at_the_parser_gate(self, monkeypatch):
        recorder = _run_consumer_one("no disposition at all", monkeypatch)
        assert not any(c.startswith("reviews:") for c in recorder.calls), recorder.calls

    def test_the_bold_wrapper_now_passes_where_it_previously_could_not(self, monkeypatch):
        recorder = _run_consumer_one(REVIEW_5000581301_LINE, monkeypatch)
        assert any(c.startswith("reviews:") for c in recorder.calls), recorder.calls

    def test_a_malformed_body_is_refused_even_with_a_native_approved_state(self, monkeypatch):
        recorder = _run_consumer_one(f"## {PREFIX} {APPROVE}", monkeypatch, state="APPROVED")
        assert not any(c.startswith("reviews:") for c in recorder.calls), recorder.calls

    def test_native_changes_requested_is_adverse_independently_of_the_body(self, monkeypatch):
        recorder = _run_consumer_one(f"{PREFIX} {APPROVE}", monkeypatch, state="CHANGES_REQUESTED")
        assert not any(c.startswith("reviews:") for c in recorder.calls), recorder.calls

    def test_the_ratification_is_all_false_for_every_refused_body(self, monkeypatch):
        for body in ("no disposition", f"## {PREFIX} {APPROVE}", f"{PREFIX} CHANGES REQUIRED"):
            recorder = _Recorder(body)
            result = A._derive_pr337_actor_ratification(
                _pr337_document(), A.TruthSources(governance=recorder), _pr337_pull()
            )
            assert result.acceptance is False
            assert result.post_merge_verification is False

    def test_the_consumer_enforces_the_distinction_explicitly(self):
        source = _toplevel(_live_source())["_derive_pr337_actor_ratification"]
        assert "MALFORMED_FORMAL_DISPOSITION" in source


def _run_consumer_two(body: str, state: str = "COMMENTED") -> tuple[str, ...]:
    class Gov:
        def pull_request(self, number):
            return {
                "base": {"repo": {"full_name": A.REPOSITORY_IDENTITY}},
                "head": {"sha": "0" * 40},
                "merged": True,
                "merge_commit_sha": "1" * 40,
                "merged_at": "2026-08-02T00:00:00Z",
            }

        def review(self, number, review_id):
            return {
                "id": review_id,
                "commit_id": "0" * 40,
                "state": state,
                "submitted_at": "2026-08-01T00:00:00Z",
                "body": body,
                "user": {"login": A.PRINCIPAL_ACCOUNT_LOGIN},
            }

        def reviews(self, number):
            return []

        def issue_comment(self, comment_id):
            return None

        def workflow_run(self, run_id):
            return None

        def workflow_job(self, job_id):
            return None

    document = {
        "authorizing_pull_request": 999,
        "authorization_head": "0" * 40,
        "lifecycle_evidence": {"independent_review": {"review_id": "12345"}},
    }
    return A.verify_lifecycle_against_truth(document, A.TruthSources(governance=Gov()))


class TestConsumerTwoVerifyLifecycleAgainstTruth:
    def test_an_absent_disposition_keeps_its_existing_error_verbatim(self):
        """§D.19: the ABSENT policy is PRESERVED, not silently repurposed."""
        errors = _run_consumer_two("no disposition at all")
        assert any("carries no parseable" in e for e in errors), errors

    def test_a_malformed_disposition_gets_its_own_distinct_error(self):
        errors = _run_consumer_two(f"## {PREFIX} CHANGES REQUIRED")
        assert any("is not in an accepted form" in e for e in errors), errors
        assert not any("carries no parseable" in e for e in errors), errors

    def test_the_two_errors_are_never_the_same_string(self):
        absent = [e for e in _run_consumer_two("nothing") if "parseable" in e or "accepted form" in e]
        malformed = [
            e for e in _run_consumer_two(f"> {PREFIX} {APPROVE}")
            if "parseable" in e or "accepted form" in e
        ]
        assert absent and malformed
        assert set(absent) != set(malformed)

    def test_an_adverse_verdict_keeps_its_own_error(self):
        errors = _run_consumer_two(f"{PREFIX} CHANGES REQUIRED")
        assert any("formal disposition is" in e for e in errors), errors

    def test_the_bold_approval_no_longer_produces_the_unparseable_error(self):
        errors = _run_consumer_two(REVIEW_5000581301_LINE)
        assert not any("carries no parseable" in e for e in errors), errors
        assert not any("is not in an accepted form" in e for e in errors), errors

    def test_a_malformed_line_fails_closed_even_with_a_native_approved_state(self):
        errors = _run_consumer_two(f"## {PREFIX} {APPROVE}", state="APPROVED")
        assert any("is not in an accepted form" in e for e in errors), errors

    def test_the_consumer_enforces_the_distinction_explicitly(self):
        source = _toplevel(_live_source())["verify_lifecycle_against_truth"]
        assert "MALFORMED_FORMAL_DISPOSITION" in source


def _run_consumer_three(later_body: str, later_state: str) -> list[str]:
    head = "b2059e80101fc6457f4004939d7d12886e6feedf"

    class Gov:
        def pull_request(self, number):
            return {}

        def review(self, number, review_id):
            return None

        def reviews(self, number):
            return [
                {
                    "id": "1",
                    "commit_id": head,
                    "state": "COMMENTED",
                    "submitted_at": "2026-01-01T00:00:00Z",
                    "body": f"{PREFIX} {APPROVE}",
                },
                {
                    "id": "999",
                    "commit_id": head,
                    "state": later_state,
                    "submitted_at": "2026-06-01T00:00:00Z",
                    "body": later_body,
                },
            ]

        def issue_comment(self, comment_id):
            return None

        def workflow_run(self, run_id):
            return None

        def workflow_job(self, job_id):
            return None

    return A._verify_selected_review_is_final(
        A.TruthSources(governance=Gov()),
        349,
        head,
        "1",
        "2026-01-01T00:00:00Z",
        {"merged_at": "2026-12-01T00:00:00Z"},
    )


class TestConsumerThreeVerifySelectedReviewIsFinal:
    def test_a_genuinely_absent_disposition_with_native_approved_stays_non_adverse(self):
        """§D.20.1: the existing ABSENT policy is INTENTIONALLY PRESERVED."""
        assert _run_consumer_three("Looks fine, shipping it.", "APPROVED") == []

    def test_a_malformed_disposition_with_native_approved_now_fails_finality(self):
        """§D.20.2: this is the load-bearing correction -- native state never rescues."""
        errors = _run_consumer_three(f"## {PREFIX} CHANGES REQUIRED", "APPROVED")
        assert errors
        assert any("not in an accepted form" in e for e in errors), errors

    def test_the_rescue_really_existed_at_the_base(self):
        """Non-vacuity: at the base BOTH returned None and both were rescued."""
        base = _base_source()
        assert "if verdict is None:" in base
        assert "if state in NATIVE_NON_ADVERSE_REVIEW_STATES:" in base

    def test_an_absent_disposition_without_a_recognised_state_still_fails_closed(self):
        errors = _run_consumer_three("no disposition", "COMMENTED")
        assert errors

    def test_a_later_adverse_verdict_is_still_adverse(self):
        errors = _run_consumer_three(f"{PREFIX} CHANGES REQUIRED", "COMMENTED")
        assert any("later adverse formal disposition" in e for e in errors), errors

    def test_a_later_native_changes_requested_is_independently_adverse(self):
        errors = _run_consumer_three(f"{PREFIX} {APPROVE}", "CHANGES_REQUESTED")
        assert errors

    def test_a_later_approving_review_is_not_adverse_in_either_form(self):
        assert _run_consumer_three(f"{PREFIX} {APPROVE}", "COMMENTED") == []
        assert _run_consumer_three(REVIEW_5000581301_LINE, "COMMENTED") == []

    def test_a_malformed_line_is_refused_before_any_native_state_branch(self):
        source = _toplevel(_live_source())["_verify_selected_review_is_final"]
        malformed_at = source.index("MALFORMED_FORMAL_DISPOSITION")
        native_at = source.index("NATIVE_NON_ADVERSE_REVIEW_STATES")
        assert malformed_at < native_at

    def test_the_consumer_enforces_the_distinction_explicitly(self):
        source = _toplevel(_live_source())["_verify_selected_review_is_final"]
        assert "MALFORMED_FORMAL_DISPOSITION" in source


# =====================================================================================
# 7-bis. Every REAL review body, base versus corrected -- exactly one changes
# =====================================================================================


def _base_module():
    """The authorization module EXACTLY as it existed at this unit's base."""
    import importlib.util
    import sys
    import tempfile

    blob = subprocess.run(
        ["git", "show", f"{BASE_SHA}:{MODULE_RELPATH}"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    directory = tempfile.mkdtemp(prefix="phq-base-parity-")
    path = Path(directory) / "_base_parity.py"
    path.write_bytes(blob)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module


#: The real lifecycle reviews this repository actually depends on, reproduced with their true
#: operative first lines and the structures that could plausibly interact with this correction
#: -- later bold text, later headings, and (for 5004478133) a genuine fenced block quoting
#: disposition samples BELOW the operative line.
REAL_REVIEW_BODIES = {
    "4974291044": (
        f"{PREFIX} {APPROVE} — 0 BLOCKING / 0 MAJOR / 0 MINOR / 1 NOTE\n\n"
        "Independent **FULL exact-head review** of PR #341.\n\n## Conclusion\n\nSound.\n"
    ),
    "5004478133": (
        f"{PREFIX} BOUNDED CORRECTION REQUIRED — 0 BLOCKING / 1 MAJOR / 2 MINOR / 0 NOTE\n\n"
        "MAJOR 1 — text.\n\n"
        f"```\n## {PREFIX} CHANGES REQUIRED\n**{PREFIX} {APPROVE}**\n```\n\nmore text\n"
    ),
    "5004859164": (
        f"{PREFIX} BOUNDED CORRECTION REQUIRED — 0 BLOCKING / 0 MAJOR / 1 MINOR / 0 NOTE\n\nbody\n"
    ),
    "5005144938": (
        f"{PREFIX} {APPROVE} — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE\n\nbody\n"
    ),
    "5011963664": (
        f"{PREFIX} {APPROVE} — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE\n\n"
        "Independent FULL exact-head review — PR #356 / XASSET-0055\n\n- Base: `683c324`\n"
    ),
}

#: The ONE review whose parse this correction exists to change.
DEFECTIVE_REVIEW_BODY = (
    f"## Independent review\n\n{REVIEW_5000581301_LINE}\n\ntext\n"
)


class TestEveryRealReviewParsesIdenticallyExceptTheDefectiveOne:
    """The blast-radius proof: this correction moves exactly one real review, and no other."""

    @pytest.mark.parametrize("review_id", sorted(REAL_REVIEW_BODIES))
    def test_each_real_review_parses_exactly_as_it_did_at_the_base(self, review_id):
        body = REAL_REVIEW_BODIES[review_id]
        assert _base_module().parse_formal_disposition(body) == P(body)

    @pytest.mark.parametrize("review_id", sorted(REAL_REVIEW_BODIES))
    def test_each_real_review_still_yields_its_own_true_verdict(self, review_id):
        body = REAL_REVIEW_BODIES[review_id]
        expected = APPROVE if review_id in {"4974291044", "5005144938", "5011963664"} \
            else "BOUNDED CORRECTION REQUIRED"
        assert P(body) == expected

    def test_the_defective_review_is_the_only_one_that_changes(self):
        base = _base_module()
        moved = [
            rid for rid, body in REAL_REVIEW_BODIES.items()
            if base.parse_formal_disposition(body) != P(body)
        ]
        assert moved == [], moved
        assert base.parse_formal_disposition(DEFECTIVE_REVIEW_BODY) is None
        assert P(DEFECTIVE_REVIEW_BODY) == APPROVE

    def test_a_fenced_sample_below_an_operative_line_never_changes_the_outcome(self):
        """5004478133 is the real case: it quotes fenced disposition samples in its body."""
        body = REAL_REVIEW_BODIES["5004478133"]
        assert "```" in body
        assert P(body) == "BOUNDED CORRECTION REQUIRED"
        assert _base_module().parse_formal_disposition(body) == P(body)


# =====================================================================================
# 7-ter. BLOCKING 1 (review 5015482594) -- a fence must be a REAL fence
# =====================================================================================

#: The reviewed head that review 5015482594 was anchored to. Every attack below AUTHENTICATED
#: there; each non-vacuity test proves that against the real historical module, by EXECUTING it,
#: never by matching its text.
REVIEWED_HEAD_SHA = "e5732620606628051c93c5fbccdbc74037405c2e"

BT = "`" * 3
BT4 = "`" * 4
TL = "~" * 3

#: Every shape that Markdown still renders INSIDE the opening fence, but which the reviewed
#: head's single shared boolean toggled its way out of. Keyed by the review's own description.
FENCE_ESCAPE_ATTACKS: dict[str, str] = {
    "mismatched tilde marker inside a backtick fence": f"{BT}\n{TL}\n{PREFIX} {APPROVE}\n{BT}\n",
    "info-string marker inside a backtick fence": f"{BT}\n{BT}python\n{PREFIX} {APPROVE}\n{BT}\n",
    "shorter same-character marker cannot close": f"{BT4}\n{BT}\n{PREFIX} {APPROVE}\n{BT4}\n",
    "mismatched backtick marker inside a tilde fence": f"{TL}\n{BT}\n{PREFIX} {APPROVE}\n{TL}\n",
    "a closer carrying an info string is not a closer": f"{BT}\n{BT}tail\n{PREFIX} {APPROVE}\n{BT}\n",
    "an over-indented marker cannot close": f"{BT}\n    {BT}\n{PREFIX} {APPROVE}\n{BT}\n",
    "a tab-indented marker cannot close": f"{BT}\n\t{BT}\n{PREFIX} {APPROVE}\n{BT}\n",
    "a nested opener does not close the active fence": f"{BT}\n{BT}\n{BT}\n{PREFIX} {APPROVE}\n",
}

#: A fence-marker line whose own text carries the formal prefix. It must NEVER be skipped, so a
#: later, better-formed approval can never win past it.
MARKER_LINES_CARRYING_THE_PREFIX: dict[str, str] = {
    "an OPENING marker's info string carries an adverse verdict":
        f"{BT} {PREFIX} CHANGES REQUIRED\ncode\n{BT}\n{PREFIX} {APPROVE}\n",
    "a CLOSING-shaped marker line carries an adverse verdict":
        f"{BT}\ncode\n{BT} {PREFIX} CHANGES REQUIRED\n{PREFIX} {APPROVE}\n",
    "a nested marker line carries an adverse verdict":
        f"{BT}\n{TL} {PREFIX} CHANGES REQUIRED\n{BT}\n{PREFIX} {APPROVE}\n",
    "a tilde marker's info string carries an adverse verdict":
        f"{TL} {PREFIX} CHANGES REQUIRED\n{TL}\n{PREFIX} {APPROVE}\n",
}

ALL_BLOCKING_ONE_ATTACKS: dict[str, str] = {
    **FENCE_ESCAPE_ATTACKS,
    **MARKER_LINES_CARRYING_THE_PREFIX,
}

#: Two of the twelve shapes happened to fail closed at the reviewed head as well -- not because
#: that parser understood fences, but because their marker lines toggled the shared boolean an
#: EVEN number of times. That is an accident of parity, not a property: adding or removing one
#: marker line flips it. They are kept as hardening guards and are named here so the non-vacuity
#: measurement below states the truth rather than over-claiming twelve reproductions.
PARITY_ACCIDENT_GUARDS: frozenset[str] = frozenset(
    {
        "a nested opener does not close the active fence",
        "a nested marker line carries an adverse verdict",
    }
)

#: Measured, not assumed: the shapes that really did authenticate at the reviewed head.
BLOCKING_ONE_REPRODUCTIONS: tuple[str, ...] = tuple(
    sorted(set(ALL_BLOCKING_ONE_ATTACKS) - PARITY_ACCIDENT_GUARDS)
)


_REVIEWED_HEAD_MODULE: "types.ModuleType | None" = None


def _reviewed_head_module() -> "types.ModuleType":
    """Import the module EXACTLY as review 5015482594 saw it, once.

    A real module object is registered in ``sys.modules`` before execution because the module
    defines ``@dataclass`` types, which resolve their own module during class creation.
    """
    global _REVIEWED_HEAD_MODULE
    if _REVIEWED_HEAD_MODULE is None:
        name = "_reviewed_head_" + REVIEWED_HEAD_SHA[:12]
        module = types.ModuleType(name)
        module.__file__ = str(ROOT / MODULE_RELPATH)
        sys.modules[name] = module
        source = _git("show", f"{REVIEWED_HEAD_SHA}:{MODULE_RELPATH}")
        exec(compile(source, module.__file__, "exec"), module.__dict__)
        _REVIEWED_HEAD_MODULE = module
    return _REVIEWED_HEAD_MODULE


def _reviewed_head_parse(body: str):
    """Parse ``body`` with the reviewed head's own parser.

    Executes the historical module rather than matching its text, so non-vacuity here is a
    behavioural fact about the reviewed head and not a claim about its source.
    """
    return _reviewed_head_module().parse_formal_disposition(body)


class TestBlockingOneFenceEscapes:
    """The parser seam. Every attack must fail CLOSED, and must have authenticated before."""

    @pytest.mark.parametrize("name", sorted(ALL_BLOCKING_ONE_ATTACKS))
    def test_the_attack_now_fails_closed(self, name):
        assert P(ALL_BLOCKING_ONE_ATTACKS[name]) is MALFORMED

    @pytest.mark.parametrize("name", sorted(ALL_BLOCKING_ONE_ATTACKS))
    def test_the_attack_never_yields_the_approval(self, name):
        assert P(ALL_BLOCKING_ONE_ATTACKS[name]) != APPROVE

    @pytest.mark.parametrize("name", BLOCKING_ONE_REPRODUCTIONS)
    def test_the_attack_really_authenticated_at_the_reviewed_head(self, name):
        """Non-vacuity: BLOCKING 1 was real, measured by EXECUTING the reviewed head."""
        assert _reviewed_head_parse(ALL_BLOCKING_ONE_ATTACKS[name]) == APPROVE

    @pytest.mark.parametrize("name", sorted(PARITY_ACCIDENT_GUARDS))
    def test_the_parity_guards_are_honestly_labelled(self, name):
        """These two failed closed at the reviewed head only by EVEN marker parity."""
        reviewed = _reviewed_head_module()
        assert (
            _reviewed_head_parse(ALL_BLOCKING_ONE_ATTACKS[name])
            is reviewed.MALFORMED_FORMAL_DISPOSITION
        )

    def test_the_reproduction_count_is_measured_not_asserted(self):
        """Ten of twelve shapes authenticated at the reviewed head; two did not."""
        reviewed = _reviewed_head_module()
        authenticated = {
            name
            for name, body in ALL_BLOCKING_ONE_ATTACKS.items()
            if reviewed.parse_formal_disposition(body) == APPROVE
        }
        assert authenticated == set(BLOCKING_ONE_REPRODUCTIONS)
        assert len(authenticated) == 10
        assert len(PARITY_ACCIDENT_GUARDS) == 2
        assert len(ALL_BLOCKING_ONE_ATTACKS) == 12

    def test_a_single_extra_marker_line_flips_a_parity_guard_open(self):
        """Why parity is an accident, not a property.

        Three backtick markers then a tilde marker. Markdown pairs the first two, re-opens on
        the third, and treats the tilde line as CONTENT of that still-open fence -- so the
        approval below it is fenced. The reviewed head simply counted four toggles, landed on
        ``False``, and authenticated it.
        """
        flipped = f"{BT}\n{BT}\n{BT}\n{TL}\n{PREFIX} {APPROVE}\n"
        assert _reviewed_head_parse(flipped) == APPROVE
        assert P(flipped) is MALFORMED

    @pytest.mark.parametrize("name", sorted(ALL_BLOCKING_ONE_ATTACKS))
    def test_the_attack_is_malformed_not_absent(self, name):
        """§D.19: an unsupported shape is never allowed to masquerade as ABSENT."""
        assert P(ALL_BLOCKING_ONE_ATTACKS[name]) is not None


class TestBlockingOneValidClosersStillClose:
    """The correction may only TIGHTEN. A syntactically valid closer must still close."""

    def test_an_exactly_matching_closer_closes_the_fence(self):
        body = f"{BT}\ncode\n{BT}\n{PREFIX} {APPROVE}\n"
        assert P(body) == APPROVE

    def test_a_longer_closer_closes_the_fence(self):
        """CommonMark: a closer needs AT LEAST the opening length, not exactly it."""
        body = f"{BT}\ncode\n{BT4}\n{PREFIX} {APPROVE}\n"
        assert P(body) == APPROVE

    def test_a_tilde_fence_closes_on_its_own_marker(self):
        body = f"{TL}\ncode\n{TL}\n{PREFIX} {APPROVE}\n"
        assert P(body) == APPROVE

    @pytest.mark.parametrize("indent", ["", " ", "  ", "   "])
    def test_a_closer_indented_up_to_three_columns_closes(self, indent):
        body = f"{BT}\ncode\n{indent}{BT}\n{PREFIX} {APPROVE}\n"
        assert P(body) == APPROVE

    def test_a_closer_with_trailing_spaces_closes(self):
        body = f"{BT}\ncode\n{BT}   \n{PREFIX} {APPROVE}\n"
        assert P(body) == APPROVE

    def test_a_two_character_run_is_not_a_fence_marker_at_all(self):
        assert P(f"``\n{PREFIX} {APPROVE}\n") == APPROVE

    def test_a_reopened_fence_after_a_valid_close_still_fences(self):
        body = f"{BT}\na\n{BT}\n{BT}\n{PREFIX} {APPROVE}\n{BT}\n"
        assert P(body) is MALFORMED


class TestBlockingOnePreservedInvariants:
    """Everything BLOCKING 1's repair was forbidden to disturb."""

    def test_first_formal_line_governance_is_preserved(self):
        """The real shape of review 5004478133: a fenced sample BELOW an operative line."""
        body = (
            f"{PREFIX} BOUNDED CORRECTION REQUIRED — 1 BLOCKING / 0 MAJOR\n"
            f"\n{BT}\n{TL}\n{PREFIX} {APPROVE}\n{BT}\n"
        )
        assert P(body) == "BOUNDED CORRECTION REQUIRED"

    def test_absent_is_still_absent_when_a_fence_never_opens(self):
        assert P("no disposition here at all\n") is None

    def test_a_body_of_only_fences_is_absent_not_malformed(self):
        assert P(f"{BT}\ncode\n{BT}\n") is None

    def test_the_open_verdict_vocabulary_survives(self):
        body = f"{BT}\ncode\n{BT}\n{PREFIX} SOME ENTIRELY NEW VERDICT\n"
        assert P(body) == "SOME ENTIRELY NEW VERDICT"

    def test_the_separator_grammar_still_applies_after_a_closed_fence(self):
        good = f"{BT}\ncode\n{BT}\n{PREFIX} {APPROVE} — 0 BLOCKING / 1 MINOR\n"
        bad = f"{BT}\ncode\n{BT}\n{PREFIX} {APPROVE} — anything at all\n"
        assert P(good) == APPROVE
        assert P(bad) is MALFORMED

    def test_the_bold_wrapper_still_works_after_a_closed_fence(self):
        body = f"{BT}\ncode\n{BT}\n**{PREFIX} {APPROVE}**\n"
        assert P(body) == APPROVE

    def test_every_real_review_body_is_unchanged_by_this_correction(self):
        """Blast radius of the BLOCKING 1 repair, measured: ZERO real reviews change."""
        for body in list(REAL_REVIEW_BODIES.values()) + [REVIEW_5000581301_LINE]:
            before, after = _reviewed_head_parse(body), P(body)
            reviewed_malformed = _reviewed_head_module().MALFORMED_FORMAL_DISPOSITION
            classify = lambda v, mal: (  # noqa: E731
                "MALFORMED" if v is mal else "ABSENT" if v is None else v
            )
            assert classify(before, reviewed_malformed) == classify(after, MALFORMED)

    def test_this_reviews_own_adverse_body_parses_to_its_true_verdict(self):
        """Review 5015482594's own first line, with its validated finding-count suffix."""
        body = (
            f"{PREFIX} BOUNDED CORRECTION REQUIRED — 1 BLOCKING / 0 MAJOR / 2 MINOR / 0 NOTE\n"
            f"\nIndependent FULL exact-head review of `{BASE_SHA}..{REVIEWED_HEAD_SHA}`.\n"
        )
        assert P(body) == "BOUNDED CORRECTION REQUIRED"


class TestBlockingOneAtTheThreeConsumerSeams:
    """The same attacks, driven through every real production consumer."""

    @pytest.mark.parametrize("name", sorted(ALL_BLOCKING_ONE_ATTACKS))
    def test_consumer_one_stops_at_the_parser_gate(self, name, monkeypatch):
        recorder = _run_consumer_one(ALL_BLOCKING_ONE_ATTACKS[name], monkeypatch)
        assert not any(c.startswith("reviews:") for c in recorder.calls), recorder.calls

    @pytest.mark.parametrize("name", sorted(ALL_BLOCKING_ONE_ATTACKS))
    def test_consumer_one_refuses_even_with_a_native_approved_state(self, name, monkeypatch):
        recorder = _run_consumer_one(
            ALL_BLOCKING_ONE_ATTACKS[name], monkeypatch, state="APPROVED"
        )
        assert not any(c.startswith("reviews:") for c in recorder.calls), recorder.calls

    @pytest.mark.parametrize("name", sorted(ALL_BLOCKING_ONE_ATTACKS))
    def test_consumer_two_reports_the_malformed_error(self, name):
        errors = _run_consumer_two(ALL_BLOCKING_ONE_ATTACKS[name])
        assert any("is not in an accepted form" in e for e in errors), errors
        assert not any("carries no parseable" in e for e in errors), errors

    @pytest.mark.parametrize("name", sorted(ALL_BLOCKING_ONE_ATTACKS))
    def test_consumer_two_refuses_even_with_a_native_approved_state(self, name):
        errors = _run_consumer_two(ALL_BLOCKING_ONE_ATTACKS[name], state="APPROVED")
        assert any("is not in an accepted form" in e for e in errors), errors

    @pytest.mark.parametrize("name", sorted(ALL_BLOCKING_ONE_ATTACKS))
    def test_consumer_three_fails_finality_despite_a_native_approved_state(self, name):
        """§D.20.2 -- the load-bearing seam: a native APPROVED never rescues MALFORMED."""
        errors = _run_consumer_three(ALL_BLOCKING_ONE_ATTACKS[name], "APPROVED")
        assert errors
        assert any("not in an accepted form" in e for e in errors), errors

    @pytest.mark.parametrize("name", BLOCKING_ONE_REPRODUCTIONS)
    def test_consumer_three_was_silent_at_the_reviewed_head(self, name):
        """Non-vacuity at the consumer seam, established from the reviewed head's own verdict.

        Consumer 3 treats an approving verdict as "a later approving pass is not adverse" and
        moves on, so a verdict of APPROVE at the reviewed head is exactly finality falling
        silent over a review Markdown still renders as fenced.
        """
        assert _reviewed_head_parse(ALL_BLOCKING_ONE_ATTACKS[name]) == APPROVE

    def test_consumer_three_still_preserves_the_genuinely_absent_policy(self):
        """§D.20.1 -- ABSENT + native APPROVED stays non-adverse. Untouched by this repair."""
        assert _run_consumer_three("Looks fine, shipping it.", "APPROVED") == []


class TestBlockingOneCorrectionShape:
    """The repair is confined to the parser and introduces no new surface."""

    def test_the_repair_lives_only_inside_the_parser(self):
        live = _toplevel(_live_source())
        assert "fence_char" in live["parse_formal_disposition"]
        for name, source in live.items():
            if name != "parse_formal_disposition":
                assert "fence_char" not in source, name

    def test_the_single_shared_boolean_is_gone(self):
        live = _live_source()
        assert "inside_code_fence" not in live
        assert "inside_code_fence" in _git("show", f"{REVIEWED_HEAD_SHA}:{MODULE_RELPATH}")

    def test_the_repair_added_no_module_level_name(self):
        reviewed = _git("show", f"{REVIEWED_HEAD_SHA}:{MODULE_RELPATH}")

        def names(source: str) -> set[str]:
            found = set()
            for node in ast.parse(source).body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    found.add(node.name)
                elif isinstance(node, ast.Assign):
                    found.update(t.id for t in node.targets if isinstance(t, ast.Name))
                elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                    found.add(node.target.id)
            return found

        assert names(_live_source()) == names(reviewed)

    def test_the_repair_added_no_call_site(self):
        assert len(_call_sites(_live_source())) == 3
        assert len(_call_sites(_git("show", f"{REVIEWED_HEAD_SHA}:{MODULE_RELPATH}"))) == 3

    def test_only_the_parser_changed_since_the_reviewed_head(self):
        reviewed = _toplevel(_git("show", f"{REVIEWED_HEAD_SHA}:{MODULE_RELPATH}"))
        live = _toplevel(_live_source())
        changed = {n for n in live if reviewed.get(n) != live[n]}
        assert changed == {"parse_formal_disposition"}, sorted(changed)

    def test_the_closer_rule_names_all_three_conditions(self):
        parser = _toplevel(_live_source())["parse_formal_disposition"]
        assert "marker == fence_char" in parser  # same character
        assert "run >= fence_len" in parser  # at least the opening length
        assert "stripped[run:].strip()" in parser  # marker and spaces only


# =====================================================================================
# 8. The scope boundary -- exhaustively, against the base
# =====================================================================================


class TestTheScopeBoundaryHolds:
    PERMITTED = {
        "parse_formal_disposition",
        "_derive_pr337_actor_ratification",
        "verify_lifecycle_against_truth",
        "_verify_selected_review_is_final",
    }

    def test_only_the_four_permitted_production_functions_changed(self):
        base, live = _toplevel(_base_source()), _toplevel(_live_source())
        changed = {n for n in set(base) & set(live) if base[n] != live[n]}
        assert changed == self.PERMITTED, sorted(changed ^ self.PERMITTED)

    def test_nothing_was_removed_from_the_module(self):
        base, live = _toplevel(_base_source()), _toplevel(_live_source())
        assert not (set(base) - set(live)), sorted(set(base) - set(live))

    def test_the_only_addition_is_the_single_sentinel_type(self):
        base, live = _toplevel(_base_source()), _toplevel(_live_source())
        assert sorted(set(live) - set(base)) == ["_MalformedFormalDisposition"]

    @staticmethod
    def _module_level_assignments(source: str) -> set[str]:
        names = set()
        for node in ast.parse(source).body:
            if isinstance(node, ast.Assign):
                names.update(t.id for t in node.targets if isinstance(t, ast.Name))
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                names.add(node.target.id)
        return names

    def test_no_standalone_production_constant_was_introduced(self):
        """§C's permitted set is EXHAUSTIVE -- a module-level constant would be a FIFTH surface.

        ``_toplevel`` above only sees defs and classes, so a smuggled ``_SEPARATORS = (...)``
        would slip past it entirely. Module-level ASSIGNMENTS are therefore compared directly.
        The separator tuple and the category vocabulary both live INLINE inside the parser,
        which is an already-permitted surface.
        """
        new = self._module_level_assignments(_live_source()) - self._module_level_assignments(
            _base_source()
        )
        assert new == {"MALFORMED_FORMAL_DISPOSITION"}, sorted(new)

    @pytest.mark.parametrize(
        "banned",
        [
            "_FORMAL_DISPOSITION_SEPARATORS",
            "_FINDING_COUNT_CATEGORIES",
            "_SEPARATORS",
            "_CATEGORIES",
            "_FINDING_COUNT_RE",
            "_COUNT_PATTERN",
        ],
    )
    def test_no_named_extraction_of_the_grammar_exists(self, banned):
        assert banned not in self._module_level_assignments(_live_source())
        assert banned not in _live_source()

    def test_the_grammar_literals_live_inside_the_parser(self):
        parser = _toplevel(_live_source())["parse_formal_disposition"]
        assert '"BLOCKING", "MAJOR", "MINOR", "NOTE"' in parser
        assert 'for separator in ("\u2014", "--", " - ", "|"):' in parser

    def test_call_sites_are_counted_by_ast_not_by_substring(self):
        """The audit's point, proved rather than asserted.

        The module names ``parse_formal_disposition`` in its own ``def`` line and in comments,
        so a substring count over-reports. Only an AST walk counts actual CALLS, and the two
        genuinely disagree -- which is why every call-site assertion here uses the AST.
        """
        live = _live_source()
        substring = live.count("parse_formal_disposition")
        ast_calls = len(_call_sites(live))
        assert ast_calls == 3
        assert substring > ast_calls, (substring, ast_calls)

    def test_there_are_exactly_three_call_sites_and_no_fourth(self):
        assert len(_call_sites(_base_source())) == 3
        assert len(_call_sites(_live_source())) == 3

    def test_the_three_call_sites_are_the_three_named_consumers(self):
        tree = ast.parse(_live_source())
        holders = set()
        for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            for node in ast.walk(fn):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id == "parse_formal_disposition"
                ):
                    holders.add(fn.name)
        assert holders == self.PERMITTED - {"parse_formal_disposition"}

    def test_no_new_helper_function_was_introduced_at_all(self):
        """The ceiling is ONE; this correction introduces ZERO, which is strictly smaller."""
        def funcs(src):
            return {
                n.name for n in ast.walk(ast.parse(src))
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
        new = funcs(_live_source()) - funcs(_base_source())
        assert {n for n in new if not n.startswith("__")} == set(), sorted(new)

    def test_no_general_purpose_parsing_framework_was_created(self):
        live = _live_source()
        for banned in ("class Parser", "class Grammar", "class Tokenizer", "class Lexer", "re.compile"):
            assert banned not in _toplevel(live)["parse_formal_disposition"], banned

    def test_the_result_representation_is_exactly_one_sentinel(self):
        assert isinstance(MALFORMED, A._MalformedFormalDisposition)
        assert A._MalformedFormalDisposition.__slots__ == ()

    @pytest.mark.parametrize(
        "constant",
        [
            "NATIVE_ADVERSE_REVIEW_STATES",
            "NATIVE_NON_ADVERSE_REVIEW_STATES",
            "APPROVING_REVIEW_DISPOSITION",
            "FORMAL_DISPOSITION_PREFIX",
            "LOAD_BEARING_RELPATHS",
            "AUTHORIZING_DECISION",
            "AUTHORIZING_PULL_REQUEST",
            "REVIEWED_BASE_SHA",
        ],
    )
    def test_untouched_constants_are_byte_identical_to_the_base(self, constant):
        base = [l for l in _base_source().splitlines() if l.startswith(f"{constant} =")]
        live = [l for l in _live_source().splitlines() if l.startswith(f"{constant} =")]
        assert base == live and base

    def test_no_other_repository_file_carries_a_production_change(self):
        changed = set(_git("diff", "--name-only", BASE_SHA).split())
        production = {p for p in changed if p.endswith(".py") and not p.startswith("test_")}
        assert production == {MODULE_RELPATH}, sorted(production)

    def test_no_protected_or_canonical_path_was_touched(self):
        changed = set(_git("diff", "--name-only", BASE_SHA).split())
        forbidden = set(A.CANONICAL_PINS) | {
            p for p in A.LOAD_BEARING_RELPATHS if p != MODULE_RELPATH
        }
        assert not (changed & forbidden), sorted(changed & forbidden)

    def test_no_risk_lane_boundary_artifact_is_referenced(self):
        assert "risk_lane_boundary" not in _toplevel(_live_source())["parse_formal_disposition"]


# =====================================================================================
# 9. The designed FAIL-CLOSED hand-off -- the stale digest, unrepaired
# =====================================================================================


class TestTheStaleLoadBearingDigestFailsClosed:
    def test_the_module_is_load_bearing_index_zero(self):
        assert A.LOAD_BEARING_RELPATHS[0] == MODULE_RELPATH

    def test_the_module_digest_is_now_stale_by_design(self):
        live = hashlib.sha256((ROOT / MODULE_RELPATH).read_bytes()).hexdigest()
        assert live != BASE_MODULE_SHA256
        assert _git("hash-object", MODULE_RELPATH).strip() != BASE_MODULE_BLOB

    def test_no_rebinding_or_re_pinning_was_performed(self):
        """§J: the drift is the hand-off to a LATER, separately authorized unit."""
        assert A.AUTHORIZING_DECISION == "XASSET-0049"
        assert A.AUTHORIZING_PULL_REQUEST == 349
        assert A.REVIEWED_BASE_SHA == "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"

    def test_the_bound_merge_constants_are_untouched(self):
        base = _base_source()
        live = _live_source()
        for marker in ("AUTHORIZING_DECISION =", "AUTHORIZING_PULL_REQUEST =", "REVIEWED_BASE_SHA ="):
            assert [l for l in base.splitlines() if l.startswith(marker)] == \
                   [l for l in live.splitlines() if l.startswith(marker)]

    def test_both_authorization_predicates_remain_false(self):
        allowed, reason = A.new_execution_is_authorized()
        assert allowed is False and reason
        allowed, reason = A.active_execution_is_authorized()
        assert allowed is False and reason

    def test_stage_1_remains_unarmed_and_not_executable(self):
        assert not A.AUTHORIZATION_ROOT.exists()
        assert not A.AUTHORIZATION_PATH.exists()
        assert not A.CLAIM_PATH.exists()
        assert not A.COMPLETION_PATH.exists()
        assert not A.LEDGER_PATH.exists()

    def test_attempt_one_is_intact_unclaimed_and_unconsumed(self):
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"
        assert not A.CLAIM_PATH.exists()
        assert not A.COMPLETION_PATH.exists()

    def test_no_results_artifact_exists_anywhere_in_the_repository(self):
        assert not list(ROOT.rglob("stage1_results.yaml"))

    def test_the_enforcement_drift_check_is_still_present_and_unweakened(self):
        assert "enforcement drift:" in _live_source()
        assert _toplevel(_base_source())["_verify_git_anchored_identity"] == \
            _toplevel(_live_source())["_verify_git_anchored_identity"]


# =====================================================================================
# 10. The mandatory zero-write end-to-end rehearsal
# =====================================================================================


class TestTheZeroWriteRehearsal:
    def test_the_corrected_parser_is_exercised_through_all_three_real_consumer_paths(self):
        """One rehearsal, all three seams, writing nothing."""
        seen = []

        # consumer 3 -- real path
        seen.append(_run_consumer_three(REVIEW_5000581301_LINE, "COMMENTED") == [])
        # consumer 2 -- real path
        errs = _run_consumer_two(REVIEW_5000581301_LINE)
        seen.append(not any("carries no parseable" in e for e in errs))
        # consumer 1 -- real path
        recorder = _Recorder(REVIEW_5000581301_LINE)
        A._derive_pr337_actor_ratification(
            _pr337_document(), A.TruthSources(governance=recorder), _pr337_pull()
        )
        seen.append(any(c.startswith("review:") for c in recorder.calls))
        assert all(seen), seen

    def test_the_rehearsal_wrote_no_authorization_state(self):
        assert not A.AUTHORIZATION_ROOT.exists()
        assert not A.AUTHORIZATION_PATH.exists()
        assert not A.CLAIM_PATH.exists()
        assert not A.COMPLETION_PATH.exists()
        assert not A.LEDGER_PATH.exists()
        assert not list(ROOT.rglob("stage1_results.yaml"))

    def test_both_predicates_are_still_false_after_the_rehearsal(self):
        assert A.new_execution_is_authorized()[0] is False
        assert A.active_execution_is_authorized()[0] is False

    def test_the_rehearsal_calls_no_lane_mutating_function(self):
        """Checked structurally over the rehearsal's OWN call graph, not by substring.

        The names are assembled from fragments so this assertion cannot match itself.
        """
        banned = {"write_" + "authorization", "build_" + "authorization_payload"}
        cls = next(
            n for n in ast.parse(Path(__file__).read_text(encoding="utf-8")).body
            if isinstance(n, ast.ClassDef) and n.name == "TestTheZeroWriteRehearsal"
        )
        called = {
            node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
            for node in ast.walk(cls)
            if isinstance(node, ast.Call)
        }
        assert not (called & banned), sorted(called & banned)


# =====================================================================================
# 11. This unit's own governance record
# =====================================================================================


class TestTheGovernanceRecord:
    def test_the_decision_file_exists(self):
        assert DECISION.exists()

    @staticmethod
    def _catalog_ids() -> list[str]:
        data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
        return [e["decision_id"] for e in data["decisions"]]

    def test_the_decision_is_catalogued_last(self):
        ids = self._catalog_ids()
        assert ids[-1] == DECISION_ID
        assert ids.count(DECISION_ID) == 1

    def test_the_catalogued_file_path_resolves(self):
        data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
        entry = data["decisions"][-1]
        assert entry["decision_id"] == DECISION_ID
        assert (ROOT / entry["file"]).exists()
        assert entry["supporting_artifact"] == Path(__file__).name

    def test_the_consumed_identifier_is_not_reused(self):
        """XASSET-0054 belongs to closed-unmerged PR #355 and never entered the catalog."""
        assert "XASSET-0054" not in self._catalog_ids()

    def test_the_decision_records_its_own_bounded_scope(self):
        text = DECISION.read_text(encoding="utf-8")
        for token in ("XASSET-0055", "XASSET-0053", "parse_formal_disposition"):
            assert token in text, token

    def test_the_decision_does_not_claim_its_own_completion(self):
        text = DECISION.read_text(encoding="utf-8").lower()
        assert "not merged" in text or "draft" in text

    def test_the_register_records_this_unit(self):
        data = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        assert DECISION_ID in yaml.safe_dump(ws)

    def test_the_register_carries_the_new_module_identity(self):
        live = hashlib.sha256((ROOT / MODULE_RELPATH).read_bytes()).hexdigest()
        flat = WORKSTREAMS.read_text(encoding="utf-8").replace("\n", "").replace(" ", "")
        assert live in flat

    def test_the_superseded_module_identity_is_retained_as_a_negative_pin(self):
        flat = WORKSTREAMS.read_text(encoding="utf-8").replace("\n", "").replace(" ", "")
        assert BASE_MODULE_SHA256 in flat

    def test_the_reviewed_head_module_identity_is_also_retained(self):
        """BLOCKING 1's correction supersedes a value the register already recorded.

        Both superseded identities stay as negative pins, so a silent revert to EITHER of them
        fails rather than quietly reinstating a reviewed-and-rejected parser.
        """
        reviewed = hashlib.sha256(
            _git("show", f"{REVIEWED_HEAD_SHA}:{MODULE_RELPATH}").encode("utf-8")
        ).hexdigest()
        flat = WORKSTREAMS.read_text(encoding="utf-8").replace("\n", "").replace(" ", "")
        assert reviewed in flat
        assert reviewed != hashlib.sha256((ROOT / MODULE_RELPATH).read_bytes()).hexdigest()

    def test_the_register_no_longer_claims_the_pull_request_number_is_unbound(self):
        """MINOR 2 of review 5015482594: structured pr and prose must agree."""
        text = WORKSTREAMS.read_text(encoding="utf-8")
        gate = text.split("gate: xasset0056-formal-disposition-parser-correction", 1)[1]
        gate = gate.split("      - gate:", 1)[0]
        assert "in_progress with pr null" not in gate
        assert "pr: 357" in gate
        assert "status: in_progress" in gate
        assert "BOUND pull request #357" in gate

    def test_the_register_states_one_measured_test_change_account(self):
        """MINOR 3 of review 5015482594: one measurement, categories named precisely."""
        text = WORKSTREAMS.read_text(encoding="utf-8")
        gate = text.split("gate: xasset0056-formal-disposition-parser-correction", 1)[1]
        gate = gate.split("      - gate:", 1)[0]
        flat = " ".join(gate.split())
        assert "17 test files changed in total" in flat
        assert "16 are PRE-EXISTING suites" in flat
        assert "assertion LINES re-anchored" in flat
        assert "seventeen assertions across three suites" not in flat
