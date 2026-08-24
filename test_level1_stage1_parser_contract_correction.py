"""Adversarial tests for the XASSET-0053-authorized formal-disposition parser correction.

XASSET-0054 IMPLEMENTS the single correction XASSET-0053 authorized, and nothing else.

WHAT WAS WRONG. ``parse_formal_disposition()`` returned ``str | None``, so ONE value carried
TWO different meanings:

  * **ABSENT**              -- the body carries no formal-looking disposition line at all; and
  * **MALFORMED/UNSUPPORTED** -- a formal-looking line WAS found and refused.

``_verify_selected_review_is_final()`` treats an unclassifiable verdict under a native
``APPROVED`` state as non-adverse, so an adverse line recorded in an unsupported shape
(``## FORMAL DISPOSITION: CHANGES REQUIRED``) was silently absorbed. A parser-only repair
cannot fix that -- the distinguishing value did not exist -- and, worse, the tempting
parser-only repair ACTIVELY REGRESSES safety by skipping the adverse line so a later approval
wins. Both were reproduced against the real module before anything was edited.

WHAT THIS SUITE DOES. It attacks the corrected paths through the REAL production functions,
not the parser alone: ``_derive_pr337_actor_ratification()``,
``verify_lifecycle_against_truth()`` and ``_verify_selected_review_is_final()`` are each driven
on their own authenticated seams, reusing the two established harnesses rather than inventing
a third, weaker stand-in.

NO STAGE-1 EXECUTION OCCURS IN THIS FILE. No attestation is created, no lane is written, no
``AUTHORIZATION_ROOT`` is touched, ``ATTEMPT_1`` is never claimed, no gate is evaluated, no
construction is dispositioned, no result is produced, no portfolio percentage is calculated and
no capital is allocated. Nothing here rebinds ``LOAD_BEARING_RELPATHS`` or re-pins any digest:
the drift this correction introduces is the designed fail-closed hand-off to the separately
authorized step-8-equivalent rebinding unit.
"""

from __future__ import annotations

import ast
import hashlib
import subprocess
from pathlib import Path

import pytest

import level1_stage1_execution_authorization as A
import test_level1_stage1_execution_authorization as H
import test_level1_stage1_pr337_lifecycle_actor_evidence_correction as R

ROOT = Path(__file__).resolve().parent
MODULE_RELPATH = "level1_stage1_execution_authorization.py"

DECISION_ID = "XASSET-0054"
AUTHORIZING_DECISION_ID = "XASSET-0053"

#: The exact `main` at which XASSET-0053 became effective, and this unit's base.
AUTHORIZING_MERGE_SHA = "683c324629544a84d2cf75ebca37325e3375c479"

BRANCH = "claude/xasset-0054-parser-contract-correction-h3nq7p"

#: Committed as a structurally impossible sentinel first, then replaced by the number GitHub
#: actually issued, in a fast-forward follow-up commit. NEVER predicted. Distinct from every
#: prior generation's sentinel, so a stale one can never masquerade as this unit's.
PR_SENTINEL = -54
PRIOR_SENTINELS = (-1, -2, -50, -51, -52, -53)

#: The number GitHub ISSUED for this unit, read back from the live API after the draft was
#: opened. Bound in the fast-forward follow-up commit; the sentinel above until then.
THIS_PULL_REQUEST = 355

APPROVE = A.APPROVING_REVIEW_DISPOSITION
ADVERSE = "CHANGES REQUIRED"
MALFORMED = A.MALFORMED_FORMAL_DISPOSITION

#: PR #349 review 5000581301's own formal line, byte-for-byte. Substantively approving,
#: mechanically unparseable before this correction.
HISTORICAL_LINE = (
    "**FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE "
    "— 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE**"
)

PLAIN_APPROVAL = f"FORMAL DISPOSITION: {APPROVE}"
BOLD_APPROVAL = f"**FORMAL DISPOSITION: {APPROVE}**"
PLAIN_ADVERSE = f"FORMAL DISPOSITION: {ADVERSE} — 1 MAJOR"
BOLD_ADVERSE = f"**FORMAL DISPOSITION: {ADVERSE} — 1 MAJOR**"
ADVERSE_HEADING = f"## FORMAL DISPOSITION: {ADVERSE}"

ABSENT_BODY = "Looks fine to me. No formal line at all."

#: Every unsupported shape §D.17 names. Each must fail closed, never be skipped.
UNSUPPORTED_SHAPES = {
    "heading": f"## FORMAL DISPOSITION: {ADVERSE}",
    "deep_heading": f"###### FORMAL DISPOSITION: {APPROVE}",
    "blockquote": f"> FORMAL DISPOSITION: {APPROVE}",
    "bullet_dash": f"- FORMAL DISPOSITION: {APPROVE}",
    "bullet_star": f"* FORMAL DISPOSITION: {APPROVE}",
    "numbered": f"1. FORMAL DISPOSITION: {APPROVE}",
    "backticked": f"`FORMAL DISPOSITION: {APPROVE}`",
    "code_fence_marker": f"```FORMAL DISPOSITION: {APPROVE}",
    "nested_emphasis": f"***FORMAL DISPOSITION: {APPROVE}***",
    "repeated_emphasis": f"****FORMAL DISPOSITION: {APPROVE}****",
    "partial_emphasis": f"**FORMAL DISPOSITION:** {APPROVE}",
    "inner_emphasis": f"**FORMAL DISPOSITION: *{APPROVE}***",
    "unbalanced_open": f"**FORMAL DISPOSITION: {APPROVE}",
    "unbalanced_close": f"FORMAL DISPOSITION: {APPROVE}**",
    "single_star_wrap": f"*FORMAL DISPOSITION: {APPROVE}*",
    "underscore_wrap": f"__FORMAL DISPOSITION: {APPROVE}__",
    "leading_prose": f"As noted, FORMAL DISPOSITION: {APPROVE}",
    "leading_bold_prose": f"**Note.** FORMAL DISPOSITION: {APPROVE}",
    "html_wrapped": f"<b>FORMAL DISPOSITION: {APPROVE}</b>",
    "table_cell": f"| FORMAL DISPOSITION: {APPROVE} |",
}


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def _module_source() -> str:
    return (ROOT / MODULE_RELPATH).read_text(encoding="utf-8")


def _changed_paths() -> set[str]:
    """Every path this unit touches, tracked or not.

    ``git diff`` alone misses NEW files until they are staged, which would let a scope guard pass
    vacuously before the commit and only bite after it. Untracked paths are unioned in so the
    guards mean the same thing at every point in this unit's lifecycle.
    """
    tracked = set(_git("diff", "--name-only", AUTHORIZING_MERGE_SHA).split())
    untracked = set(_git("ls-files", "--others", "--exclude-standard").split())
    return tracked | untracked


# =====================================================================================
# 1-2-3. The three accepted shapes, at the parser and at the real consumers
# =====================================================================================


class TestTheAcceptedShapes:
    """Exactly two line shapes are accepted, and the verdict is never rewritten."""

    @pytest.mark.parametrize(
        "body",
        [
            PLAIN_APPROVAL,
            f"{PLAIN_APPROVAL} — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE",
            f"   {PLAIN_APPROVAL}   ",
            f"## Independent review\n\nprose\n\n{PLAIN_APPROVAL}\n\nmore prose\n",
        ],
    )
    def test_the_plain_canonical_line_is_still_accepted(self, body):
        assert A.parse_formal_disposition(body) == APPROVE

    @pytest.mark.parametrize(
        "body",
        [
            BOLD_APPROVAL,
            f"**FORMAL DISPOSITION: {APPROVE} — 0 BLOCKING**",
            f"   {BOLD_APPROVAL}   ",
            f"## Independent review\n\nprose\n\n{BOLD_APPROVAL}\n\nmore prose\n",
        ],
    )
    def test_the_precisely_balanced_whole_line_bold_form_is_accepted(self, body):
        assert A.parse_formal_disposition(body) == APPROVE

    def test_the_exact_historical_review_line_is_accepted(self):
        """PR #349 review 5000581301, byte-for-byte, in its real surrounding shape."""
        body = (
            "## Independent exact-head DELTA review — PR #349\n\n"
            "Scope, anchors and findings.\n\n"
            f"{HISTORICAL_LINE}\n\n"
            "Closing prose.\n"
        )
        assert A.parse_formal_disposition(body) == APPROVE

    def test_the_historical_line_really_is_the_balanced_whole_line_shape(self):
        """Non-vacuity: the shape claim is derived from the bytes, not assumed."""
        line = HISTORICAL_LINE.strip()
        assert line.startswith("**") and line.endswith("**")
        assert "*" not in line[2:-2]

    def test_only_the_wrapper_is_removed_and_the_verdict_is_never_rewritten(self):
        """No normalization, replacement, canonicalization, or fuzzy matching."""
        for verdict in ("APPROVED", "approved", "CHANGES REQUIRED", "Approved for something"):
            assert A.parse_formal_disposition(f"FORMAL DISPOSITION: {verdict}") == verdict
            assert A.parse_formal_disposition(f"**FORMAL DISPOSITION: {verdict}**") == verdict

    def test_a_near_miss_verdict_is_returned_verbatim_and_never_snapped_to_the_approval(self):
        near = APPROVE.replace("EXACT-HEAD", "EXACT HEAD")
        assert near != APPROVE
        assert A.parse_formal_disposition(f"**FORMAL DISPOSITION: {near}**") == near
        assert A.parse_formal_disposition(f"**FORMAL DISPOSITION: {near}**") != APPROVE

    def test_comparison_with_the_approving_constant_stays_exact(self):
        assert A.APPROVING_REVIEW_DISPOSITION == "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        assert A.FORMAL_DISPOSITION_PREFIX == "FORMAL DISPOSITION:"


# =====================================================================================
# 4-5. Adverse verdicts, plain and balanced-bold, stay adverse
# =====================================================================================


class TestAdverseVerdictsStayAdverse:
    @pytest.mark.parametrize("body", [PLAIN_ADVERSE, f"FORMAL DISPOSITION: {ADVERSE}"])
    def test_plain_adverse_parses_as_adverse(self, body):
        got = A.parse_formal_disposition(body)
        assert got == ADVERSE
        assert got != APPROVE

    @pytest.mark.parametrize("body", [BOLD_ADVERSE, f"**FORMAL DISPOSITION: {ADVERSE}**"])
    def test_balanced_bold_adverse_parses_as_adverse(self, body):
        got = A.parse_formal_disposition(body)
        assert got == ADVERSE
        assert got != APPROVE

    def test_an_adverse_line_quoting_the_approval_phrase_later_stays_adverse(self):
        """MAJOR 1 (review 4946464366) must not regress: prose never overrides the line."""
        body = (
            f"**FORMAL DISPOSITION: {ADVERSE} — 1 MAJOR**\n\n"
            f"This is NOT '{APPROVE}'.\n"
        )
        assert A.parse_formal_disposition(body) == ADVERSE

    @pytest.mark.parametrize(
        "body",
        [
            f"I would have written {APPROVE} but I cannot.",
            f"The phrase is '{APPROVE}'.\n\nNo formal line follows.",
            f"```\n{APPROVE}\n```",
            f"> {APPROVE}",
            f"## {APPROVE}",
        ],
    )
    def test_the_approval_phrase_alone_in_prose_never_yields_a_verdict(self, body):
        """§D.8: approval text as substring, quotation, heading, or code sample is not a verdict."""
        assert A.parse_formal_disposition(body) is None
        assert A.parse_formal_disposition(body) != APPROVE


# =====================================================================================
# 11. The FIRST formal-disposition line governs
# =====================================================================================


class TestFirstFormalLineGoverns:
    def test_a_later_adverse_line_cannot_override_an_earlier_approval(self):
        body = f"{PLAIN_APPROVAL}\n\n{PLAIN_ADVERSE}\n"
        assert A.parse_formal_disposition(body) == APPROVE

    def test_a_later_approval_cannot_override_an_earlier_adverse_line(self):
        body = f"{PLAIN_ADVERSE}\n\n{PLAIN_APPROVAL}\n"
        assert A.parse_formal_disposition(body) == ADVERSE

    def test_the_first_line_governs_across_the_two_accepted_shapes(self):
        assert A.parse_formal_disposition(f"{BOLD_ADVERSE}\n{PLAIN_APPROVAL}") == ADVERSE
        assert A.parse_formal_disposition(f"{PLAIN_ADVERSE}\n{BOLD_APPROVAL}") == ADVERSE


# =====================================================================================
# 9-10. An unsupported formal-looking line STOPS classification -- never skipped
# =====================================================================================


class TestUnsupportedShapesFailClosed:
    @pytest.mark.parametrize("name,line", sorted(UNSUPPORTED_SHAPES.items()))
    def test_every_unsupported_shape_is_malformed_not_absent(self, name, line):
        assert A.parse_formal_disposition(line) is MALFORMED, name

    @pytest.mark.parametrize("name,line", sorted(UNSUPPORTED_SHAPES.items()))
    def test_no_unsupported_shape_is_ever_read_as_the_approval(self, name, line):
        assert A.parse_formal_disposition(line) != APPROVE, name

    @pytest.mark.parametrize("name,line", sorted(UNSUPPORTED_SHAPES.items()))
    def test_an_unsupported_line_is_never_skipped_for_a_later_valid_approval(self, name, line):
        """THE hazard §D.17 forbids: the naive parser-only repair returns the approval here."""
        body = f"{line}\n\n… later …\n\n{HISTORICAL_LINE}\n"
        assert A.parse_formal_disposition(body) is MALFORMED, name

    def test_the_worked_adverse_heading_case_stops_classification(self):
        body = f"{ADVERSE_HEADING}\n… later …\n{HISTORICAL_LINE}\n"
        assert A.parse_formal_disposition(body) is MALFORMED

    def test_a_naive_skip_semantics_repair_really_would_have_flipped_this_verdict(self):
        """Non-vacuity for the test above, executed in memory only."""

        def naive(text: str) -> str | None:
            for raw in text.splitlines():
                stripped = raw.strip()
                if stripped.startswith("**") and stripped.endswith("**"):
                    stripped = stripped[2:-2].strip()
                if not stripped.upper().startswith(A.FORMAL_DISPOSITION_PREFIX):
                    continue  # <-- the skip
                verdict = stripped[len(A.FORMAL_DISPOSITION_PREFIX):].strip()
                for sep in ("—", "--", " - ", "|"):
                    if sep in verdict:
                        verdict = verdict.split(sep, 1)[0].strip()
                return verdict
            return None

        body = f"{ADVERSE_HEADING}\n… later …\n{HISTORICAL_LINE}\n"
        assert naive(body) == APPROVE          # the regression the correction had to avoid
        assert A.parse_formal_disposition(body) is MALFORMED

    def test_an_unsupported_line_before_a_plain_approval_also_stops_classification(self):
        assert A.parse_formal_disposition(f"{ADVERSE_HEADING}\n{PLAIN_APPROVAL}") is MALFORMED


# =====================================================================================
# 7. ABSENT keeps its own, separate meaning
# =====================================================================================


class TestAbsentIsDistinctFromMalformed:
    @pytest.mark.parametrize(
        "body",
        [
            ABSENT_BODY,
            "",
            "\n\n\n",
            "## A heading\n\nSome prose about the disposition of the matter.\n",
            "The reviewer had no formal opinion.",
        ],
    )
    def test_genuinely_absent_bodies_return_none(self, body):
        assert A.parse_formal_disposition(body) is None

    @pytest.mark.parametrize("body", [None, 17, [], {}, object()])
    def test_a_non_string_body_is_absent_not_malformed(self, body):
        assert A.parse_formal_disposition(body) is None

    def test_absent_and_malformed_are_no_longer_the_same_value(self):
        """The exact conflation XASSET-0053 §C item 2 exists to end."""
        absent = A.parse_formal_disposition(ABSENT_BODY)
        malformed = A.parse_formal_disposition(ADVERSE_HEADING)
        assert absent is None
        assert malformed is MALFORMED
        assert absent is not malformed
        assert malformed is not None

    def test_the_sentinel_is_a_singleton_and_not_a_string(self):
        assert A.parse_formal_disposition(ADVERSE_HEADING) is A.MALFORMED_FORMAL_DISPOSITION
        assert not isinstance(MALFORMED, str)
        assert MALFORMED != APPROVE
        assert MALFORMED != ADVERSE
        assert bool(MALFORMED) is False
        assert repr(MALFORMED) == "MALFORMED_FORMAL_DISPOSITION"


# =====================================================================================
# 6-8-12. The REAL consumers: _verify_selected_review_is_final()
# =====================================================================================


def _finality(entries, *, selected_at="2026-08-16T10:00:00Z", merged_at="2026-08-16T12:00:00Z"):
    """Drive the REAL finality function on the real authenticated seam."""
    gov = H.FakeGovernance()
    gov.review_records = {
        H.REVIEW_ID: dict(gov.review_records[H.REVIEW_ID], submitted_at=selected_at),
    }
    for i, (state, body, submitted) in enumerate(entries):
        rid = f"49000010{i:02d}"
        gov.review_records[rid] = {
            "id": rid,
            "commit_id": H.HEAD,
            "body": body,
            "user": {"login": H.REVIEWER_LOGIN},
            "state": state,
            "submitted_at": submitted,
            "html_url": f"{H.PR_URL}#pullrequestreview-{rid}",
        }
    pull = dict(gov.pulls[A.AUTHORIZING_PULL_REQUEST], merged_at=merged_at)
    return A._verify_selected_review_is_final(
        H.sources(governance=gov),
        A.AUTHORIZING_PULL_REQUEST,
        H.HEAD,
        H.REVIEW_ID,
        selected_at,
        pull,
    )


LATER = "2026-08-16T11:00:00Z"


class TestFinalityConsumerEnforcesTheDistinction:
    """``_verify_selected_review_is_final()`` -- the defect site itself."""

    def test_a_later_native_approved_review_with_no_formal_line_is_still_non_adverse(self):
        """ABSENT policy PRESERVED, exactly as it was: this is the one rescue that survives."""
        assert _finality([("APPROVED", ABSENT_BODY, LATER)]) == []

    def test_a_later_native_approved_review_with_an_unsupported_adverse_heading_now_fails(self):
        """THE correction: native APPROVED may no longer rescue MALFORMED/UNSUPPORTED."""
        errors = _finality([("APPROVED", ADVERSE_HEADING, LATER)])
        assert len(errors) == 1
        assert "unsupported shape" in errors[0]
        assert "fails closed" in errors[0]

    @pytest.mark.parametrize("name,line", sorted(UNSUPPORTED_SHAPES.items()))
    def test_every_unsupported_shape_fails_finality_under_native_approved(self, name, line):
        assert len(_finality([("APPROVED", line, LATER)])) == 1, name

    def test_an_unsupported_line_followed_by_a_valid_approval_cannot_be_skipped(self):
        """A later, better-formed approval in the SAME body never rescues the first line."""
        body = f"{ADVERSE_HEADING}\n\n… later …\n\n{HISTORICAL_LINE}\n"
        errors = _finality([("APPROVED", body, LATER)])
        assert len(errors) == 1
        assert "unsupported shape" in errors[0]

    def test_a_later_native_changes_requested_review_is_rejected_independently(self):
        """MAJOR 2 preserved: the NATIVE state is adverse whatever the body says."""
        errors = _finality([("CHANGES_REQUESTED", PLAIN_APPROVAL, LATER)])
        assert len(errors) == 1
        assert "CHANGES_REQUESTED" in errors[0]

    def test_a_native_changes_requested_review_carrying_the_bold_approval_is_still_rejected(self):
        errors = _finality([("CHANGES_REQUESTED", HISTORICAL_LINE, LATER)])
        assert len(errors) == 1
        assert "CHANGES_REQUESTED" in errors[0]

    def test_a_later_approving_pass_in_either_accepted_shape_is_not_adverse(self):
        assert _finality([("COMMENTED", PLAIN_APPROVAL, LATER)]) == []
        assert _finality([("COMMENTED", BOLD_APPROVAL, LATER)]) == []
        assert _finality([("COMMENTED", HISTORICAL_LINE, LATER)]) == []

    def test_a_later_adverse_verdict_in_either_accepted_shape_is_adverse(self):
        for body in (PLAIN_ADVERSE, BOLD_ADVERSE):
            errors = _finality([("COMMENTED", body, LATER)])
            assert len(errors) == 1
            assert "adverse formal disposition" in errors[0]

    def test_an_unclassifiable_review_with_no_native_state_still_fails_closed(self):
        errors = _finality([("", ABSENT_BODY, LATER)])
        assert len(errors) == 1
        assert "fails closed" in errors[0]

    def test_the_malformed_branch_is_checked_before_the_approving_branch(self):
        """Structural, not incidental: the guard cannot be reordered into a rescue."""
        src = _module_source()
        body = src[src.index("def _verify_selected_review_is_final("):]
        body = body[: body.index("\n    return errors")]
        i_native = body.index("if state in NATIVE_ADVERSE_REVIEW_STATES:")
        i_malformed = body.index("if verdict is MALFORMED_FORMAL_DISPOSITION:")
        i_approve = body.index("if verdict == APPROVING_REVIEW_DISPOSITION:")
        i_absent = body.index("if verdict is None:")
        assert i_native < i_malformed < i_approve < i_absent

    def test_the_native_approved_rescue_still_exists_but_only_under_the_absent_branch(self):
        src = _module_source()
        body = src[src.index("def _verify_selected_review_is_final("):]
        body = body[: body.index("\n    return errors")]
        absent_branch = body[body.index("if verdict is None:"):]
        assert "if state in NATIVE_NON_ADVERSE_REVIEW_STATES:" in absent_branch
        malformed_branch = body[
            body.index("if verdict is MALFORMED_FORMAL_DISPOSITION:")
            : body.index("if verdict == APPROVING_REVIEW_DISPOSITION:")
        ]
        assert "NATIVE_NON_ADVERSE_REVIEW_STATES" not in malformed_branch


# =====================================================================================
# 12. The REAL consumer: verify_lifecycle_against_truth()
# =====================================================================================


def _selected_review_errors(body: str) -> list[str]:
    """Drive the REAL lifecycle verifier with one altered selected-review body."""
    gov = H.FakeGovernance()
    gov.review_records[H.REVIEW_ID] = dict(gov.review_records[H.REVIEW_ID], body=body)
    doc = A.build_authorization_payload(
        authorization_head=H.HEAD,
        lifecycle_evidence=H.lifecycle(),
        author_identity=H.AUTHOR_LOGIN,
        generated_at_utc="2026-08-16T00:00:00Z",
        merge_sha=H.MERGE,
    )
    doc["load_bearing_identity"] = {
        rel: A.sha256_file(ROOT / rel) for rel in sorted(A.LOAD_BEARING_RELPATHS)
    }
    return [e for e in A.verify_lifecycle_against_truth(doc, H.sources(governance=gov))
            if "review" in e and str(H.REVIEW_ID) in e]


class TestLifecycleVerifierEnforcesTheDistinction:
    def test_a_genuinely_absent_disposition_keeps_its_own_message(self):
        """ABSENT policy PRESERVED: fail-closed, with the message it always had."""
        errors = _selected_review_errors(ABSENT_BODY)
        assert any("carries no parseable" in e for e in errors)
        assert not any("unsupported shape" in e for e in errors)

    def test_a_malformed_disposition_fails_closed_with_its_own_message(self):
        errors = _selected_review_errors(ADVERSE_HEADING)
        assert any("unsupported shape" in e for e in errors)
        assert not any("carries no parseable" in e for e in errors)

    @pytest.mark.parametrize("name,line", sorted(UNSUPPORTED_SHAPES.items()))
    def test_every_unsupported_shape_fails_the_selected_review_gate(self, name, line):
        assert any("unsupported shape" in e for e in _selected_review_errors(line)), name

    def test_an_adverse_verdict_still_fails_with_the_adverse_message(self):
        errors = _selected_review_errors(PLAIN_ADVERSE)
        assert any("formal disposition is" in e for e in errors)

    def test_the_plain_approving_body_passes_the_disposition_gate(self):
        assert _selected_review_errors(PLAIN_APPROVAL) == []

    def test_the_balanced_bold_approving_body_now_passes_the_disposition_gate(self):
        """The substantive fix, at the real seam: review 5000581301's shape authenticates."""
        assert _selected_review_errors(HISTORICAL_LINE) == []
        assert _selected_review_errors(BOLD_APPROVAL) == []

    def test_the_three_outcomes_produce_three_distinguishable_results(self):
        absent = _selected_review_errors(ABSENT_BODY)
        malformed = _selected_review_errors(ADVERSE_HEADING)
        approved = _selected_review_errors(HISTORICAL_LINE)
        assert absent and malformed and approved == []
        assert absent != malformed


# =====================================================================================
# 12. The REAL consumer: _derive_pr337_actor_ratification()
# =====================================================================================


def _ratification(body: str, *, repin: bool):
    """Drive the REAL PR #337 ratification derivation with one altered review body.

    ``repin=True`` recomputes the review fingerprint from the mutated fixture, which removes
    the SEPARATE fingerprint gate from the picture so the disposition gate proves its own
    mechanism. ``repin=False`` leaves the fixture pins in place.
    """
    gov = R.Governance()
    key = (R.P341, R.P341_REVIEW)
    gov.review_records[key] = dict(gov.review_records[key], body=body)
    pins = dict(R.FIXTURE_FINGERPRINTS)
    if repin:
        pins["RATIFICATION_REVIEW_FINGERPRINT"] = A._review_record_fingerprint(
            gov.review_records[key]
        )
    originals = {name: getattr(A, name) for name in pins}
    try:
        for name, digest in pins.items():
            setattr(A, name, digest)
        return A._derive_pr337_actor_ratification(
            R.document(), R.sources(governance=gov), gov.pull_request(R.P337)
        )
    finally:
        for name, value in originals.items():
            setattr(A, name, value)


class TestPr337RatificationEnforcesTheDistinction:
    def test_the_baseline_fixture_really_does_ratify(self):
        """Non-vacuity: without it, every negative below would be trivially true."""
        got = _ratification(R.APPROVING, repin=True)
        assert got.acceptance is True
        assert got.post_merge_verification is True

    def test_a_genuinely_absent_disposition_does_not_ratify(self):
        """ABSENT policy PRESERVED: fail-closed, exactly as before."""
        got = _ratification(ABSENT_BODY, repin=True)
        assert got.acceptance is False
        assert got.post_merge_verification is False

    @pytest.mark.parametrize("name,line", sorted(UNSUPPORTED_SHAPES.items()))
    def test_no_unsupported_shape_ratifies(self, name, line):
        got = _ratification(line, repin=True)
        assert got.acceptance is False, name
        assert got.post_merge_verification is False, name

    def test_an_adverse_disposition_does_not_ratify(self):
        got = _ratification(PLAIN_ADVERSE, repin=True)
        assert got.acceptance is False

    def test_the_balanced_bold_approving_shape_ratifies(self):
        """The substantive fix, at the third real seam."""
        got = _ratification(f"**FORMAL DISPOSITION: {APPROVE} — 0 BLOCKING**", repin=True)
        assert got.acceptance is True
        assert got.post_merge_verification is True

    def test_the_separate_fingerprint_gate_is_untouched_by_the_correction(self):
        """A body change that now PARSES still relocks on the byte-exact fingerprint."""
        got = _ratification(f"**FORMAL DISPOSITION: {APPROVE} — 0 BLOCKING**", repin=False)
        assert got.acceptance is False
        assert got.post_merge_verification is False

    def test_the_consumer_still_reads_the_disposition_through_an_inequality(self):
        """No new branch was needed here; both new outcomes fail closed on `!=`."""
        src = _module_source()
        body = src[src.index("def _derive_pr337_actor_ratification("):]
        body = body[: body.index("\ndef ", 1)]
        assert 'parse_formal_disposition(rat_review.get("body") or "") != ' \
               "APPROVING_REVIEW_DISPOSITION" in body.replace("\n", " ").replace("  ", " ")


# =====================================================================================
# 13. Durable historical records and fingerprints are unchanged
# =====================================================================================


class TestDurableRecordsAreUnchanged:
    FINGERPRINT_CONSTANTS = (
        "RATIFICATION_REVIEW_FINGERPRINT",
        "RATIFICATION_COMMENT_FINGERPRINT",
        "RATIFICATION_VERIFICATION_FINGERPRINT",
        "RATIFICATION_CLOSURE_FINGERPRINT",
    )

    @pytest.mark.parametrize("name", FINGERPRINT_CONSTANTS)
    def test_every_fingerprint_pin_is_byte_identical_to_the_base(self, name):
        base = _git("show", f"{AUTHORIZING_MERGE_SHA}:{MODULE_RELPATH}")
        tree = ast.parse(base)
        wanted = {
            n.targets[0].id: ast.literal_eval(n.value)
            for n in tree.body
            if isinstance(n, ast.Assign)
            and isinstance(n.targets[0], ast.Name)
            and n.targets[0].id == name
        }
        assert wanted[name] == getattr(A, name)

    def test_no_review_comment_or_ci_identity_constant_moved(self):
        base = _git("show", f"{AUTHORIZING_MERGE_SHA}:{MODULE_RELPATH}")
        tree = ast.parse(base)
        moved = []
        for node in tree.body:
            if not (isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)):
                continue
            name = node.targets[0].id
            if not (name.isupper() and any(
                k in name for k in ("REVIEW", "COMMENT", "MERGE", "HEAD", "CI_", "PULL",
                                    "FINGERPRINT", "DECISION", "SHA", "ACTOR", "GATES")
            )):
                continue
            try:
                expected = ast.literal_eval(node.value)
            except (ValueError, SyntaxError):
                continue
            if hasattr(A, name) and getattr(A, name) != expected:
                moved.append(name)
        assert not moved, moved

    def test_the_lifecycle_gate_tuple_is_unchanged(self):
        base = _git("show", f"{AUTHORIZING_MERGE_SHA}:{MODULE_RELPATH}")
        assert 'REQUIRED_LIFECYCLE_GATES' in base
        assert len(A.REQUIRED_LIFECYCLE_GATES) == 6

    def test_the_load_bearing_path_set_is_unchanged(self):
        """Compared as SOURCE TEXT: the tuple names two module constants, so it is not a literal."""
        base_src = _git("show", f"{AUTHORIZING_MERGE_SHA}:{MODULE_RELPATH}")
        live_src = _module_source()

        def segment(src):
            for node in ast.parse(src).body:
                if isinstance(node, ast.Assign) and \
                        getattr(node.targets[0], "id", "") == "LOAD_BEARING_RELPATHS":
                    return ast.get_source_segment(src, node)
            pytest.fail("LOAD_BEARING_RELPATHS not found")

        assert segment(base_src) == segment(live_src)
        assert len(A.LOAD_BEARING_RELPATHS) == 18
        assert A.LOAD_BEARING_RELPATHS[0] == MODULE_RELPATH


# =====================================================================================
# 14. Scope: no fourth call site, no framework, nothing else touched
# =====================================================================================


class TestScopeIsExactlyWhatWasAuthorized:
    def test_there_are_exactly_three_parser_call_sites(self):
        tree = ast.parse(_module_source())
        calls = [
            n for n in ast.walk(tree)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Name)
            and n.func.id == "parse_formal_disposition"
        ]
        assert len(calls) == 3

    def test_the_three_call_sites_are_the_three_named_consumers(self):
        src = _module_source()
        tree = ast.parse(src)
        owners = []
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for n in ast.walk(fn):
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                        and n.func.id == "parse_formal_disposition":
                    owners.append(fn.name)
        assert sorted(owners) == sorted([
            "_derive_pr337_actor_ratification",
            "verify_lifecycle_against_truth",
            "_verify_selected_review_is_final",
        ])

    def test_exactly_one_new_helper_was_introduced(self):
        base = ast.parse(_git("show", f"{AUTHORIZING_MERGE_SHA}:{MODULE_RELPATH}"))
        live = ast.parse(_module_source())

        def names(tree):
            return {n.name for n in tree.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}

        added = names(live) - names(base)
        removed = names(base) - names(live)
        assert removed == set()
        assert added == {"_formal_disposition_line_verdict", "_MalformedFormalDisposition"}

    def test_the_helper_is_not_a_general_parsing_framework(self):
        """One question, one line, no state, no configuration, no second parser."""
        tree = ast.parse(_module_source())
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == "_formal_disposition_line_verdict")
        args = fn.args
        assert [a.arg for a in args.args] == ["stripped"]
        assert args.vararg is None and args.kwarg is None
        assert args.kwonlyargs == [] and args.defaults == []
        # It classifies ONE line: no splitlines, no iteration over a body, no regex engine,
        # no I/O, no global state.
        forbidden = {"splitlines", "compile", "match", "search", "findall", "sub", "open",
                     "read_text", "loads", "safe_load"}
        used = {n.attr for n in ast.walk(fn) if isinstance(n, ast.Attribute)}
        assert not (used & forbidden), sorted(used & forbidden)
        assert not [n for n in ast.walk(fn) if isinstance(n, (ast.Global, ast.Nonlocal))]

    def test_the_sentinel_class_carries_no_behaviour_beyond_identity(self):
        tree = ast.parse(_module_source())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef)
                   and n.name == "_MalformedFormalDisposition")
        methods = {n.name for n in cls.body if isinstance(n, ast.FunctionDef)}
        assert methods <= {"__repr__", "__bool__"}
        assert any(isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "__slots__"
                   for n in cls.body)

    def test_no_other_production_function_changed(self):
        """Every other top-level definition is byte-identical to the base commit."""
        base_src = _git("show", f"{AUTHORIZING_MERGE_SHA}:{MODULE_RELPATH}")
        live_src = _module_source()
        base = {n.name: ast.get_source_segment(base_src, n)
                for n in ast.parse(base_src).body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
        live = {n.name: ast.get_source_segment(live_src, n)
                for n in ast.parse(live_src).body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
        permitted = {
            "parse_formal_disposition",
            "_formal_disposition_line_verdict",
            "_MalformedFormalDisposition",
            "_derive_pr337_actor_ratification",
            "verify_lifecycle_against_truth",
            "_verify_selected_review_is_final",
        }
        changed = {name for name, body in base.items() if live.get(name) != body}
        assert changed <= permitted, sorted(changed - permitted)

    def test_the_three_consumers_changed_by_the_minimum(self):
        """Each consumer's change is confined to the disposition branch, and is small."""
        base_src = _git("show", f"{AUTHORIZING_MERGE_SHA}:{MODULE_RELPATH}")
        live_src = _module_source()
        import difflib
        for name, budget in (
            ("_derive_pr337_actor_ratification", 4),
            ("verify_lifecycle_against_truth", 12),
            ("_verify_selected_review_is_final", 16),
        ):
            def seg(src):
                return next(
                    ast.get_source_segment(src, n) for n in ast.parse(src).body
                    if isinstance(n, ast.FunctionDef) and n.name == name
                ).splitlines()
            diff = [
                ln for ln in difflib.unified_diff(seg(base_src), seg(live_src), n=0)
                if ln.startswith(("+", "-")) and not ln.startswith(("+++", "---"))
            ]
            assert len(diff) <= budget, (name, len(diff), diff)

    def test_the_only_load_bearing_path_touched_is_the_one_authorized(self):
        changed = _changed_paths()
        touched = changed & set(A.LOAD_BEARING_RELPATHS)
        assert touched == {MODULE_RELPATH}

    def test_no_historical_governance_record_is_edited(self):
        """§D.13: the durable record is evidence, never a repair surface."""
        changed = sorted(c for c in _changed_paths() if c.startswith("governance/decisions/"))
        assert changed == [
            "governance/decisions/"
            "XASSET-0054-endpoint-0001-formal-disposition-parser-contract-correction.md"
        ], changed

    def test_no_prior_decision_file_or_audit_artifact_is_touched(self):
        changed = _changed_paths()
        assert not [c for c in changed if c.startswith("governance/audits/")]
        assert not [c for c in changed if c.startswith("governance/evidence/")]

    def test_no_protected_portfolio_or_canonical_path_is_touched(self):
        changed = _changed_paths()
        forbidden = {
            "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
            "allocate.py", "margin_state.py", "levels.py",
            "research/level1_endpoint_evidence/PROTOCOL_V1.md",
            "research/level1_endpoint_evidence/pre_registration.yaml",
        }
        assert not (changed & forbidden), sorted(changed & forbidden)


# =====================================================================================
# The critical consequence: NO operational authority is restored
# =====================================================================================


class TestRegisterSynchronisation:
    """The register's own bookkeeping for this unit, including the sentinel-then-bind step."""

    @staticmethod
    def _ws0014() -> dict:
        import yaml

        data = yaml.safe_load((ROOT / "operations/WORKSTREAMS.yaml").read_text(encoding="utf-8"))
        return next(w for w in data["workstreams"] if w["id"] == "WS-0014")

    def test_the_workstream_is_untouched_in_status_and_priority(self):
        ws = self._ws0014()
        assert ws["status"] == "proposed"
        assert ws["priority"] == "secondary"

    def test_exactly_zero_primary_workstreams(self):
        import yaml

        data = yaml.safe_load((ROOT / "operations/WORKSTREAMS.yaml").read_text(encoding="utf-8"))
        assert sum(1 for w in data["workstreams"] if w.get("priority") == "primary") == 0

    def test_the_shared_live_fields_name_this_unit_and_are_bound_at_both_ends(self):
        ws = self._ws0014()
        assert ws["active_branch"] == BRANCH
        assert ws["last_verified_main_sha"] == AUTHORIZING_MERGE_SHA
        # Every finished generation's value is a negative pin, so a silent revert still fails.
        for finished in (
            "cc1d1b62b8b48c7123b73e05e7ea04af89c89cd6",
            "8def8bd096b4edecbf10fc20870a6d03b6cb56fe",
            "a941455491cc5e4d3d868775fb6b4b88f0fe2ce3",
            "f052efad38e3d57e3e5615799ac3bcbebe83ff5f",
        ):
            assert ws["last_verified_main_sha"] != finished, finished
        assert ws["active_branch"] != "claude/xasset-0053-parser-contract-auth-k7m2qx"

    def test_this_units_gate_exists_and_is_not_marked_complete_by_its_own_filing(self):
        gate = next(
            g for g in self._ws0014()["milestones"]
            if g["gate"] == "xasset0054-parser-contract-correction-implementation"
        )
        assert gate["status"] == "in_progress"
        assert gate["status"] != "complete"

    def test_the_prior_units_gate_is_not_rewritten(self):
        gate = next(
            g for g in self._ws0014()["milestones"]
            if g["gate"] == "xasset0053-parser-contract-correction-authorization"
        )
        assert gate["pr"] == 354

    def test_the_gate_records_the_corrected_module_identity_for_the_rebinding_unit(self):
        gate = next(
            g for g in self._ws0014()["milestones"]
            if g["gate"] == "xasset0054-parser-contract-correction-implementation"
        )
        flat = " ".join(gate["description"].split())
        assert hashlib.sha256((ROOT / MODULE_RELPATH).read_bytes()).hexdigest() in flat
        assert "NOT re-pinned" in flat or "NOT RE-PINNED" in flat.upper()

    def test_the_active_pr_is_the_real_github_number_not_the_sentinel(self):
        active = self._ws0014()["active_pr"]
        assert active == THIS_PULL_REQUEST
        assert active != PR_SENTINEL, "the sentinel was never replaced"
        assert active not in PRIOR_SENTINELS
        assert active > 354

    def test_this_units_gate_carries_the_real_pull_request_number(self):
        gate = next(
            g for g in self._ws0014()["milestones"]
            if g["gate"] == "xasset0054-parser-contract-correction-implementation"
        )
        assert gate["pr"] == THIS_PULL_REQUEST
        assert gate["pr"] != PR_SENTINEL, "the sentinel was never replaced"

    def test_no_sentinel_survives_anywhere_in_the_register(self):
        raw = (ROOT / "operations/WORKSTREAMS.yaml").read_text(encoding="utf-8")
        for sentinel in (PR_SENTINEL, *PRIOR_SENTINELS):
            assert f"active_pr: {sentinel}" not in raw, sentinel
            assert f"pr: {sentinel}" not in raw, sentinel


class TestNoOperationalAuthorityIsRestored:
    """The correction repairs an authentication CONTRACT. It arms nothing."""

    def test_new_execution_is_not_authorized(self):
        authorized, reason = A.new_execution_is_authorized()
        assert authorized is False
        assert reason

    def test_active_execution_is_not_authorized(self):
        authorized, _ = A.active_execution_is_authorized()
        assert authorized is False

    def test_claimed_and_completed_execution_are_not_authorized_either(self):
        assert A.claimed_execution_is_authorized()[0] is False

    def test_the_public_executability_flag_is_still_false(self):
        import yaml

        prereg = yaml.safe_load(
            (ROOT / "research/level1_endpoint_evidence/pre_registration.yaml")
            .read_text(encoding="utf-8")
        )
        assert prereg["stage_1_executability"]["executable"] is False

    def test_the_authorization_root_does_not_exist(self):
        assert not Path(A.AUTHORIZATION_ROOT).exists()

    def test_the_lane_is_absent_and_attempt_1_is_unclaimed(self):
        state, _ = A.lane_state_at(A.LanePaths())
        assert state == A.LANE_ABSENT
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

    def test_no_results_document_exists(self):
        assert not (ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()

    def test_this_unit_creates_no_attestation_and_no_lane(self):
        """Structural: nothing in this suite or this diff writes to the lane location."""
        changed = _changed_paths()
        assert not [c for c in changed if "stage1_results" in c or "attestation" in c.lower()]

    def test_the_bound_authorizing_identity_did_not_move(self):
        assert A.AUTHORIZING_DECISION == "XASSET-0049"
        assert A.AUTHORIZING_PULL_REQUEST == 349
        assert A.REVIEWED_BASE_SHA == "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"

    def test_no_rebinding_or_re_pinning_occurred(self):
        """The module's bound digest is deliberately left STALE for the rebinding unit."""
        bound = _git("show", f"{AUTHORIZING_MERGE_SHA}:{MODULE_RELPATH}")
        live = _module_source()
        assert bound != live, "non-vacuity: the module really did change"
        digest_now = hashlib.sha256(live.encode()).hexdigest()
        register = (ROOT / "operations/WORKSTREAMS.yaml").read_text(encoding="utf-8")
        flat = register.replace("\n", "").replace(" ", "")
        assert digest_now in flat, (
            "the register must hand the separately authorized rebinding unit the corrected "
            "byte identity"
        )

    def test_the_correction_cites_its_authority(self):
        assert AUTHORIZING_DECISION_ID in _module_source()
