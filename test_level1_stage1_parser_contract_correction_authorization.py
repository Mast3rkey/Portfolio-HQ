"""Adversarial tests pinning the ``XASSET-0053`` formal-disposition parser-contract authorization.

``XASSET-0052``'s single authorized link-5 unit ran and reached a terminal
``STOPPED_BEFORE_ATTESTATION``. It stopped on **one** condition: PR #349's exact-head review
``5000581301`` carries its formal disposition on a **markdown-bolded** line, and
``parse_formal_disposition()`` requires the stripped line to *start with* ``FORMAL DISPOSITION:``,
so the leading ``**`` defeats ``str.startswith`` and the verdict cannot be authenticated.

``XASSET-0052`` §H forbade that unit from repairing what it found, and §J said the consequence in
terms: remediation "requires **separately authorized things**", and "**Finding the work is not
authority to do the work.**" ``XASSET-0053`` supplies exactly the first of those — the parser
correction — and nothing else.

The whole risk of an authorization filing is that it grants more than it says, or that a future
session reads more out of it than it contains. The whole risk of *this particular* authorization is
sharper still: it authorizes an edit to a **disposition parser**, and every relaxation of a
disposition parser is a candidate re-opening of the ``MAJOR 1`` hole review ``4946464366`` closed,
where ``APPROVING_REVIEW_DISPOSITION in body`` let an adverse review pass because later explanatory
text quoted the approval phrase.

Every test below therefore pins **an authorized boundary and its nearest plausible overreach**.
The overreaches that matter most each have a dedicated guard:

1. **The correction performed here.** ``TestTheCorrectionIsNotPerformedHere`` fails if the
   authorization module moves by a single byte, or if any load-bearing or protected path drifts.
2. **The authority/performance distinction collapsed.**
   ``TestTheAuthorityPerformanceDistinction`` fails if the parser correction is placed inside a
   "not authorized" list, or if §A.1's canonical sentence is absent or weakened.
3. **More than one unit granted.** ``TestExactlyOneFutureUnit``.
4. **The safety boundary softened.** ``TestTheSafetyBoundaryIsConjunctiveAndComplete`` binds all
   fourteen §D clauses as whole lines, so prefixing a permissive qualifier fails rather than
   survives.
5. **The parser relaxation broadened past the demonstrated shape.**
   ``TestTheRelaxationIsBoundedToTheDemonstratedShape`` fails if arbitrary emphasis, substring
   matching, or verdict rewriting is admitted.
6. **The correction read as restoring operational authority.**
   ``TestTheCorrectionCannotRestoreOperationalAuthority`` fails if §E or §H.2 is weakened.
7. **The downstream chain shortened.** ``TestDownstreamConsequences`` binds all six §H items,
   including the never-predict-a-merge-SHA rule.
8. **The historical record treated as a repair surface.** ``TestTheHistoricalRecordIsNotEditable``.
9. **``XASSET-0052`` revived.** ``TestXasset0052GrantIsSpentButTheDecisionStandsAsHistory``.
10. **A stale or absent reproduction.** ``TestTheDefectIsReproducedFromLiveArtifacts`` re-derives
    the parser contract from the module itself rather than trusting the filing's prose.

They also pin the negative space that makes the filing honest: this authorization PR changes no
canonical file, no validator, no authorization module, no runner, no result validator, and no
load-bearing byte; all eighteen load-bearing paths, both canonical pins, the frozen universe, and
the outcome-capable module identities are untouched; ``REQUIRED_LIFECYCLE_GATES`` is still the
six-element tuple; and Stage 1 is still ``UNARMED`` with lane state ``ABSENT`` and ``ATTEMPT_1``
unclaimed.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No results document, lane directory, attestation, claim, completion, or ledger
entry is created or read for authorization purposes. No ``risk_lane_boundary`` protected result
path is read, listed, opened, or referenced. **No network call is made by this suite** — every
live fact it needs was re-derived in preflight and is pinned here as a constant, so the suite is
deterministic in CI.
"""

from __future__ import annotations

import ast
import hashlib
import re
import subprocess
from pathlib import Path

import pytest
import yaml

import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
GOV = ROOT / "governance/decisions"
WORKSTREAMS = ROOT / "operations/WORKSTREAMS.yaml"
CATALOG = ROOT / "governance/decisions.yaml"

DECISION_ID = "XASSET-0053"
DECISION = (
    GOV
    / "XASSET-0053-endpoint-0001-formal-disposition-parser-contract-correction-authorization.md"
)

D0040 = (
    GOV / "XASSET-0040-endpoint-0001-stage-1-step-11-activation-and-execution-authorization.md"
)
D0048 = GOV / "XASSET-0048-endpoint-0001-stage-1-step-8-equivalent-rebinding-authorization.md"
D0049 = (
    GOV
    / "XASSET-0049-endpoint-0001-stage-1-step-8-equivalent-successor-operational-rebinding.md"
)
D0052 = (
    GOV
    / "XASSET-0052-endpoint-0001-stage-1-renewed-step-11-activation-and-execution-authorization.md"
)

# ---------------------------------------------------------------------------------------------
# The base this filing is anchored to: XASSET-0052's own lifecycle-closing merge, which is the
# exact `main` at which the link-5 unit acted and stopped.
# ---------------------------------------------------------------------------------------------

BASE_SHA = "cc1d1b62b8b48c7123b73e05e7ea04af89c89cd6"

#: The XASSET-0049 bound merge. Every load-bearing and protected identity is compared to THIS.
BOUND_MERGE_SHA = "a941455491cc5e4d3d868775fb6b4b88f0fe2ce3"
BOUND_MERGE_PARENT_1 = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"
BOUND_MERGE_PARENT_2 = "b2059e80101fc6457f4004939d7d12886e6feedf"
BOUND_MERGE_TREE = "b7015b271362ae0c2fe663e8bfda9c6d10de5e7e"

# ---------------------------------------------------------------------------------------------
# The defect, pinned from the live artifacts re-derived in preflight.
# ---------------------------------------------------------------------------------------------

#: PR #349's exact-head review -- substantively APPROVING, mechanically unparseable.
DEFECTIVE_REVIEW_ID = "5000581301"
DEFECTIVE_REVIEW_PR = 349
DEFECTIVE_REVIEW_HEAD = "b2059e80101fc6457f4004939d7d12886e6feedf"
DEFECTIVE_REVIEW_BODY_SHA256 = (
    "6a221d8a36ae8c00e057c763c175879556133569b645b5302ca142fa1001177a"
)

#: The exact line, read directly from GitHub in preflight. The wrapper is a precisely balanced,
#: whole-line bold pair and the enclosed text carries no further `*`.
DEFECTIVE_FORMAL_LINE = (
    "**FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE "
    "— 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE**"
)

#: The only other review on PR #349 -- wrong head AND adverse. Pinned so it can never be promoted
#: into an admissible alternative.
ADVERSE_REVIEW_ID = "5000502119"
ADVERSE_REVIEW_HEAD = "8ab773866c5959cd61a73dd48af197339c48754a"
ADVERSE_DISPOSITION = "CHANGES REQUIRED"

#: The single validation error the public path returns today.
VALIDATION_ERROR_FRAGMENT = (
    "carries no parseable 'FORMAL DISPOSITION:' line, so its verdict cannot be authenticated"
)

# ---------------------------------------------------------------------------------------------
# The spent link-5 grant. NEGATIVE pins: a silent revival must FAIL, not pass unnoticed.
# ---------------------------------------------------------------------------------------------

LINK5_STOP_COMMENT = "5389820540"
LINK5_STOP_DETERMINATION = "STOPPED_BEFORE_ATTESTATION"
LINK5_STOP_BODY_SHA256 = (
    "4ee46f3f23e6ab25c45e395b4193e886b5e1ffc176b296aabf0d19f6691702f2"
)
XASSET0052_CLOSURE_COMMENT = "5389700733"
XASSET0052_ACCEPTED_HEAD = "8f1cc608e1219b2cb9fcbf8f8f42a24fbd0f131c"
XASSET0052_BASE = "8def8bd096b4edecbf10fc20870a6d03b6cb56fe"
XASSET0052_MERGE_CI_RUN = "32679424717"
XASSET0052_MERGE_CI_JOB = "97293351500"

#: XASSET-0040's own spent grant, one generation earlier. Still a negative pin.
SPENT_STEP11_EVIDENCE_COMMENT = "5343692162"

# ---------------------------------------------------------------------------------------------
# The pins the withheld clauses bind.
# ---------------------------------------------------------------------------------------------

EXPECTED_LOAD_BEARING_COUNT = 18

#: The authorization module blob at the stop, and therefore at this filing. If the correction is
#: performed here rather than merely authorized, THIS is what changes.
AUTHORIZATION_MODULE_RELPATH = "level1_stage1_execution_authorization.py"
AUTHORIZATION_MODULE_BLOB = "f71b08b4ebe95f161c57cdbb2a924748f13af02d"
AUTHORIZATION_MODULE_SHA256 = (
    "4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541"
)

OUTCOME_CAPABLE_MODULE_WITNESS = {
    "level1_stage1_runner.py":
        "4a88cf6d0271da0dc3a6ca175fadb0223bf7ff8843479733cbcf0effd47ba5d9",
    "level1_stage1_result_validator.py":
        "b4773eb767158434136b72316e9802308b9e6fb47b6e45f8f10445c02cee3b7a",
    "level1_endpoint_evidence_preregistration_validator.py":
        "b3a87e4f8b828d420795348642c977a9f0585eafa9262a4be48df406f770233d",
    "level1_construction_universe_closure_validator.py":
        "1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5",
    AUTHORIZATION_MODULE_RELPATH: AUTHORIZATION_MODULE_SHA256,
}

CANONICAL_PINS = {
    "research/level1_endpoint_evidence/PROTOCOL_V1.md":
        "1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84",
    "research/level1_endpoint_evidence/pre_registration.yaml":
        "898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f",
}

CONSTRUCTION_COUNT = 680
CELL_COUNT = 48
UNIVERSE_SHA = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"

BOUND_AUTHORIZING_DECISION = "XASSET-0049"
BOUND_AUTHORIZING_PULL_REQUEST = 349
BOUND_REVIEWED_BASE_SHA = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"

EXPECTED_LIFECYCLE_GATES = (
    "INDEPENDENT_FULL_EXACT_HEAD_REVIEW",
    "PRINCIPAL_EXACT_HEAD_ACCEPTANCE",
    "MERGE",
    "POST_MERGE_VERIFICATION",
    "MERGE_COMMIT_CI_SUCCESS",
    "MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION",
)

ATTEMPT_ID = "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

PORTFOLIO_RELPATHS = (
    "allocate.py",
    "margin_state.py",
    "levels.py",
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
)

#: An impossible sentinel, distinct from every sentinel used before (-1, -2, -50, -51, -52).
#: Committed first, then replaced by the number GitHub actually issued in a fast-forward follow-up
#: commit. RETAINED as a negative pin so a revert to the unbound state still fails.
PR_SENTINEL = -53
PRIOR_SENTINELS = (-1, -2, -50, -51, -52)

#: The number GitHub ISSUED for this unit, read back from the live API after the draft was opened.
#: Never predicted, never guessed. Committed as the sentinel first; bound in a fast-forward
#: follow-up commit once GitHub has actually issued the number.
THIS_PULL_REQUEST = 354

THIS_GATE = "xasset0053-parser-contract-correction-authorization"
PRIOR_UNIT_GATE = "xasset0052-renewed-step11-activation-authorization"
PRIOR_CLOSURE_GATE = "xasset0052-post-merge-verification-and-link5-stop"

BRANCH = "claude/xasset-0053-parser-contract-auth-k7m2qx"


# =============================================================================================
# helpers
# =============================================================================================


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _flat_quote(text: str) -> str:
    """Flatten, dropping Markdown blockquote continuation markers.

    The canonical sentence is a blockquote, so a naive flatten interleaves "> " between its
    wrapped lines. Stripping the marker is a formatting normalisation only -- no word changes.
    """
    stripped = "\n".join(
        line.lstrip()[2:] if line.lstrip().startswith("> ") else line
        for line in text.splitlines()
    )
    return _flat(stripped)


def _sha256_at(commit: str, relpath: str) -> str:
    raw = subprocess.run(
        ["git", "show", f"{commit}:{relpath}"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    return hashlib.sha256(raw).hexdigest()


def _blob_at(commit: str, relpath: str) -> str:
    return _git("rev-parse", f"{commit}:{relpath}").strip()


def _section(text: str, heading: str) -> str:
    """The body of one '### X' section, up to the next same-level heading."""
    start = text.index(heading)
    rest = text[start + len(heading):]
    nxt = rest.find("\n### ")
    return rest if nxt < 0 else rest[:nxt]


def _bullets_under(text: str, clause: str) -> list[str]:
    """Whole bullet lines governed by a 'must not:' style clause.

    Binding whole lines is deliberate: a substring assertion survives a permissive qualifier being
    prefixed to the bullet, which is exactly the mutation this class must catch.
    """
    body = text[text.index(clause) + len(clause):]
    stop = body.find("\n### ")
    if stop >= 0:
        body = body[:stop]
    out: list[str] = []
    for raw in body.splitlines():
        s = raw.strip()
        if s.startswith("- "):
            out.append(s)
        elif not s:
            continue
        elif s.startswith(("**", "#")):
            break
        elif out:
            # a wrapped continuation of the bullet above; join so whole-line binding sees it all
            out[-1] = out[-1] + " " + s
    return [_flat(b) for b in out]


@pytest.fixture(scope="module")
def decision() -> str:
    return DECISION.read_text()


@pytest.fixture(scope="module")
def flat(decision: str) -> str:
    return _flat(decision)


@pytest.fixture(scope="module")
def catalog() -> list[dict]:
    return yaml.safe_load(CATALOG.read_text())["decisions"]


@pytest.fixture(scope="module")
def bullets() -> list[str]:
    return _bullets_under(
        DECISION.read_text(), "The parser-correction unit, and this filing, **must not**:"
    )


@pytest.fixture(scope="module")
def ws0014() -> dict:
    data = yaml.safe_load(WORKSTREAMS.read_text())
    return next(w for w in data["workstreams"] if w["id"] == "WS-0014")


# =============================================================================================
# The filing itself
# =============================================================================================


class TestTheFilingExistsAndIsWellFormed:
    def test_the_decision_file_exists(self):
        assert DECISION.exists()

    def test_the_frontmatter_is_complete_and_proposed(self, decision):
        assert decision.startswith("---\n")
        front = yaml.safe_load(decision.split("---", 2)[1])
        assert front["decision_id"] == DECISION_ID
        assert front["status"] == "Proposed"
        assert front["supporting_artifact"] == Path(__file__).name
        assert str(front["date"]) == "2026-08-24"

    def test_the_frontmatter_relates_to_the_whole_chain(self, decision):
        front = yaml.safe_load(decision.split("---", 2)[1])
        related = set(front["related_decisions"])
        for required in ("XASSET-0040", "XASSET-0048", "XASSET-0049", "XASSET-0052"):
            assert required in related, required

    def test_every_required_section_is_present(self, decision):
        for heading in (
            "### A. Determination",
            "#### A.1",
            "### B. The defect, reproduced independently",
            "### C. Authority granted",
            "### D. The required safety boundary",
            "### E. This filing does not restore operational authority",
            "### F. Authority withheld",
            "### G. Fail-closed",
            "### H. Downstream consequences",
            "### I. Packaging and evidence",
            "### J. Effectivity",
            "### K. Absolute non-performance",
            "### L. Mandatory downstream prevention",
            "### M. Review-format convention",
            "## Rationale",
            "## Alternatives Considered",
            "## Consequences",
        ):
            assert heading in decision, heading


class TestTheAuthorityPerformanceDistinction:
    """MAJOR 2's lesson from PR #353, applied one decision later.

    A filing that both grants and denies the same act is unsafe acceptance evidence, because a
    reader cannot tell which half governs.
    """

    def test_the_canonical_sentence_is_present_verbatim(self, decision):
        quoted = _flat_quote(decision)
        assert (
            "`XASSET-0053` **authorizes** exactly one future, separate **parser-contract "
            "correction unit**, but **this filing performs none of that work**"
        ) in quoted

    def test_the_canonical_sentence_carries_the_exercisability_clause(self, decision):
        quoted = _flat_quote(decision)
        assert "not exercisable unless and until §J's seven conditions close" in quoted

    def test_the_three_prohibited_claims_are_named(self, flat):
        assert "Three claims are therefore prohibited" in flat
        assert "not authorized by this filing itself" in flat
        assert "zero correction authority" in flat

    def test_the_banned_formulations_never_appear_operatively(self, decision):
        """ADDED after mutation probes P02 and P03, which this suite MISSED on its first pass.

        Naming the prohibited claims is not enough. Nothing stopped the decision from ALSO
        asserting one of them operatively somewhere else, so the probes that moved the denial out
        of the prohibition list and into live text went uncaught -- the exact defect class review
        5003284327 MAJOR 2 identified one filing earlier, and which PR #353's own register probe
        M2-g then found a second instance of. It is bound here directly: each banned formulation
        may appear ONLY inside §A.1's own explicit list of prohibited claims, never as operative
        text anywhere in the document.
        """
        marker = "Three claims are therefore prohibited"
        assert marker in decision, "the prohibition list is missing"
        before, after = decision.split(marker, 1)
        # the list ends where §A.1 ends and §B begins
        prohibited, rest = after.split("### B.", 1)
        operative = _flat(before + rest)
        for banned in (
            "not authorized by this filing itself",
            "zero correction authority",
            "adds zero correction authority",
        ):
            assert banned not in operative, banned
        # non-vacuity: the prohibition list must actually quote what it forbids
        flat_prohibited = _flat(prohibited)
        assert "not authorized by this filing itself" in flat_prohibited
        assert "zero correction authority" in flat_prohibited

    def test_no_performance_claim_is_made_anywhere(self, flat):
        """The third prohibited claim, bound as its own guard (probe P03's class)."""
        for banned in (
            "This filing is design-only and adds zero correction authority",
            "this filing corrected the parser",
            "this filing performed the correction",
        ):
            assert banned not in flat, banned
        assert "**This filing is design-only. It performs none of that work.**" in flat

    def test_the_withheld_section_disclaims_denying_the_grant(self, decision):
        section = _section(decision, "### K. Absolute non-performance")
        assert "never a denial of the one thing §A authorizes" in _flat(section)

    @pytest.mark.parametrize(
        "phrase",
        [
            "parser correction",
            "parse_formal_disposition",
            "correct the parser",
        ],
    )
    def test_no_withheld_bullet_places_the_correction_on_the_denied_side(self, decision, phrase):
        """The grant must never appear inside §F's own 'must not' enumeration."""
        bullets = _bullets_under(decision, "The parser-correction unit, and this filing, **must not**:")
        assert bullets, "the withheld clause parsed to nothing"
        for bullet in bullets:
            lowered = bullet.lower()
            if phrase.lower() in lowered:
                # permitted only where it names the unit's OWN scope boundary, never the grant
                assert "any other parser" in lowered or "no other" in lowered, bullet


class TestExactlyOneFutureUnit:
    def test_the_determination_names_exactly_one_unit(self, flat):
        assert (
            "**Exactly one** future, separate, bounded **parser-contract correction unit** is "
            "authorized" in flat
        )

    def test_the_consequences_repeat_exactly_one(self, flat):
        assert "**exactly one** future,\nseparate, bounded parser-contract correction unit" in _flat(
            DECISION.read_text()
        ) or "**exactly one** future, separate, bounded parser-contract correction unit" in flat

    def test_no_successor_unit_is_authorized(self, decision):
        bullets = _bullets_under(decision, "The parser-correction unit, and this filing, **must not**:")
        assert any("authorize any successor unit of any kind" in b for b in bullets)


class TestTheDefectIsReproducedFromLiveArtifacts:
    """The filing's claim about the parser is re-derived from the module, not trusted as prose."""

    def test_the_parser_contract_is_exactly_what_the_filing_describes(self):
        src = inspect_source = _git("show", f"{BASE_SHA}:{AUTHORIZATION_MODULE_RELPATH}")
        tree = ast.parse(src)
        fn = next(
            n for n in tree.body
            if isinstance(n, ast.FunctionDef) and n.name == "parse_formal_disposition"
        )
        body = ast.get_source_segment(src, fn)
        assert "stripped.upper().startswith(FORMAL_DISPOSITION_PREFIX)" in body
        assert inspect_source  # the module was genuinely read from the tree

    def test_the_prefix_and_approving_disposition_are_unchanged(self):
        assert A.FORMAL_DISPOSITION_PREFIX == "FORMAL DISPOSITION:"
        assert A.APPROVING_REVIEW_DISPOSITION == "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"

    def test_the_defective_line_is_not_parseable_today(self):
        """The live defect, exercised directly against the shipped parser."""
        body = f"## header\n\n{DEFECTIVE_FORMAL_LINE}\n\nexplanatory text\n"
        assert A.parse_formal_disposition(body) is None

    def test_the_wrapper_is_precisely_balanced_and_whole_line(self):
        line = DEFECTIVE_FORMAL_LINE.strip()
        assert line.startswith("**") and line.endswith("**")
        assert "*" not in line[2:-2], "the enclosed text must carry no further emphasis marker"

    def test_removing_exactly_the_balanced_wrapper_yields_the_approving_verdict(self):
        """§B.3, exercised. Nothing on GitHub or on disk is altered by this."""
        line = DEFECTIVE_FORMAL_LINE.strip()
        unwrapped = line[2:-2].strip()
        got = A.parse_formal_disposition(f"## header\n\n{unwrapped}\n")
        assert got == A.APPROVING_REVIEW_DISPOSITION

    def test_the_adverse_review_still_parses_as_adverse_today(self):
        got = A.parse_formal_disposition(
            f"FORMAL DISPOSITION: {ADVERSE_DISPOSITION} — 0 BLOCKING / 3 MAJOR\n"
        )
        assert got == ADVERSE_DISPOSITION
        assert got != A.APPROVING_REVIEW_DISPOSITION

    def test_the_filing_records_the_exact_defective_line(self, decision):
        assert DEFECTIVE_FORMAL_LINE in decision

    def test_the_filing_records_the_exact_validation_error(self, flat):
        assert _flat(VALIDATION_ERROR_FRAGMENT) in flat

    def test_the_filing_records_the_review_and_head_identities(self, flat):
        assert DEFECTIVE_REVIEW_ID in flat
        assert DEFECTIVE_REVIEW_HEAD in flat
        assert DEFECTIVE_REVIEW_BODY_SHA256 in flat

    def test_the_filing_forecloses_the_only_alternative_review(self, flat):
        assert ADVERSE_REVIEW_ID in flat
        assert "No admissible alternative" in flat

    def test_the_filing_classifies_the_defect_honestly(self, flat):
        assert "formatting/parser-contract mismatch" in flat
        assert "**not** an adverse review" in flat
        assert "**not** drift" in flat


class TestTheSafetyBoundaryIsConjunctiveAndComplete:
    """All eighteen §D clauses, bound as whole lines."""

    REQUIRED = {
        "D.1": "Continue accepting the existing unformatted canonical line",
        "D.2": "Accept only a precisely balanced, whole-line Markdown-bold wrapper",
        "D.3": "Normalize formatting before extracting the verdict; never normalize or replace the",
        "D.4": 'Preserve "first formal disposition line governs."',
        "D.5": "Preserve exact comparison with `APPROVING_REVIEW_DISPOSITION`",
        "D.6": "Preserve independent rejection of native `CHANGES_REQUESTED`",
        "D.7": "Reject wrapped or unwrapped `CHANGES REQUIRED`",
        "D.8": "Reject approval text appearing only as a substring, quotation, explanation,",
        "D.9": "Reject leading or trailing operative prose around the formal line",
        "D.10": "Reject unbalanced, nested, partial, repeated, or ambiguous emphasis markers",
        "D.11": "Preserve every surrounding protection unchanged",
        "D.12": "Add behavioral and mutation tests",
        "D.13": "Do not edit review `5000581301`, any historical review, comment, acceptance",
        "D.14": "Do not repair any other parser, and do not broaden the accepted review grammar",
        "D.15": "Exercise all three production consumers",
        "D.16": "The accepted grammar is exactly the two demonstrated forms, and no more",
        "D.17": "An unsupported formal-looking line FAILS CLOSED; it is never skipped",
        "D.18": "Required behavioral coverage",
    }

    @pytest.mark.parametrize("clause,text", sorted(REQUIRED.items()))
    def test_each_clause_is_present(self, decision, clause, text):
        assert f"**{clause} — {text}" in decision, clause

    def test_the_boundary_is_declared_conjunctive(self, flat):
        assert "must** satisfy **all** of the following" in flat
        assert "Failure on any one is a defect in the correction, not a permitted trade-off" in flat

    def test_no_clause_was_dropped(self, decision):
        section = _section(decision, "### D. The required safety boundary")
        found = set(re.findall(r"\*\*(D\.\d+)", section))
        assert found == set(self.REQUIRED), sorted(set(self.REQUIRED) ^ found)


class TestTheRelaxationIsBoundedToTheDemonstratedShape:
    def test_verdict_rewriting_is_prohibited(self, flat):
        assert "never normalize or replace the verdict itself" in flat
        assert "may **not** rewrite, substitute, canonicalize, fuzzy-match, or coerce" in flat

    def test_mapping_a_non_approving_verdict_to_approving_is_prohibited(self, flat):
        assert "may **not** map a\nnon-approving verdict onto an approving one" in _flat(
            DECISION.read_text()
        ) or "may **not** map a non-approving verdict onto an approving one" in flat

    def test_substring_comparison_is_prohibited(self, flat):
        assert "Substring, prefix, case-insensitive, or\nsimilarity comparison is prohibited" in \
            _flat(DECISION.read_text()) or \
            "Substring, prefix, case-insensitive, or similarity comparison is prohibited" in flat

    def test_the_major1_regression_is_named_by_its_review_id(self, flat):
        assert "4946464366" in flat

    def test_broadening_beyond_the_demonstrated_shape_is_refused(self, flat):
        assert "No other formatting is admitted by this authorization" in flat
        assert "no other emphasis style" in flat

    def test_arbitrary_emphasis_is_rejected_in_alternatives(self, decision):
        section = _section(decision, "## Alternatives Considered") if \
            "### " not in _section(decision, "## Alternatives Considered") else decision
        assert "Accept arbitrary Markdown emphasis" in decision
        assert "invents grammar" in decision


class TestTheHistoricalRecordIsNotEditable:
    def test_editing_the_review_is_prohibited_in_the_boundary(self, flat):
        assert "Do not edit review `5000581301`, any historical review, comment, acceptance" in flat

    def test_the_reason_is_stated_not_merely_asserted(self, flat):
        assert "The durable record is evidence, not a repair surface" in flat

    def test_editing_records_is_also_a_withheld_bullet(self, decision):
        bullets = _bullets_under(decision, "The parser-correction unit, and this filing, **must not**:")
        assert any("edit any historical review, comment, acceptance record, or closure record" in b
                   for b in bullets)

    def test_the_alternative_was_considered_and_rejected(self, decision):
        assert "Edit review `5000581301` to unbolded text" in decision


class TestTheLiveFormatScanIsRecordedAndGrounded:
    """§B.7 -- the scan is stated with its counts, and with the two records that make it bite."""

    def test_the_scan_is_declared_independently_re_run(self, flat):
        assert "B.7 — The live review-format scan, independently re-run." in flat
        assert "enumerated directly from the GitHub review API in this session" in flat
        assert "the counts were re-derived rather than accepted" in flat

    @pytest.mark.parametrize(
        "fragment",
        (
            "**34** such lines exist",
            "**20** plain canonical",
            "**8** precisely balanced whole-line bold",
            "**6** Markdown-heading",
        ),
    )
    def test_each_count_is_stated(self, flat, fragment):
        assert fragment in flat, fragment

    def test_the_scan_covers_the_whole_lifecycle_range(self, flat):
        assert "across PRs #337–#353" in flat

    def test_a_real_bolded_adverse_line_is_cited(self, flat):
        """Without this, §D.7 would read as a hypothetical guard rather than a recorded refusal."""
        assert "PR #350 review `5000866476`" in flat
        assert "**FORMAL DISPOSITION: CHANGES REQUIRED — …**" in flat
        assert "would flip a real, recorded refusal" in flat

    def test_a_real_heading_form_adverse_line_is_cited(self, flat):
        assert "six times across PRs #344 and #345" in flat
        assert "grounded in the durable record" in flat

    def test_the_scan_and_the_grammar_clause_are_tied_in_both_directions(self, decision):
        """A count with no clause, or a clause with no evidence, is the failure this prevents."""
        scan = _section(decision, "### B. The defect, reproduced independently")
        grammar = _section(decision, "### D. The required safety boundary")
        assert "§D.7" in scan and "§D.17" in scan, "the scan must name the clauses it grounds"
        assert "Grounded in §B.7" in grammar, "the grammar clause must name its evidence"


class TestTheSkipVersusFailClosedHazardIsDemonstrated:
    """§B.8 -- the hazard is reproduced, not asserted."""

    def test_the_hazard_section_exists_and_names_the_naive_correction(self, flat):
        assert "B.8 — The skip-versus-fail-closed hazard, reproduced." in flat
        assert "strips a balanced bold wrapper but otherwise keeps the existing **skip** semantics" in flat

    def test_the_demonstrated_outcome_is_the_wrong_one(self, flat):
        assert "the adverse heading silently skipped" in flat
        assert "and the later approval winning" in flat

    def test_the_worked_body_is_recorded_verbatim(self, decision):
        section = _section(decision, "### B. The defect, reproduced independently")
        assert "## FORMAL DISPOSITION: CHANGES REQUIRED" in section
        assert "**FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE" in section

    def test_first_line_governs_is_declared_insufficient_on_its_own(self, flat):
        """The trap: 'first' silently means 'first *recognised*' under skip semantics."""
        assert "is **not** on its own sufficient" in flat
        assert "first line the parser happens to recognise" in flat

    def test_the_hazard_is_reproduced_rather_than_asserted(self, flat):
        assert "demonstrated rather than asserted" in flat

    def test_todays_parser_really_does_return_none_for_both_shapes(self):
        """Non-vacuity: the premise §B.8 rests on is checked against the live module."""
        assert A.parse_formal_disposition("## FORMAL DISPOSITION: CHANGES REQUIRED") is None
        assert A.parse_formal_disposition(DEFECTIVE_FORMAL_LINE) is None

    def test_a_naive_skip_semantics_correction_really_does_flip_the_verdict(self):
        """The exact failure §D.17 forbids, executed here so the clause is not taken on faith."""
        body = (
            "## FORMAL DISPOSITION: CHANGES REQUIRED\n"
            "   … later …\n"
            + DEFECTIVE_FORMAL_LINE
            + "\n"
        )

        def naive(text: str) -> str | None:
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("**") and stripped.endswith("**"):
                    stripped = stripped[2:-2].strip()
                if not stripped.upper().startswith(A.FORMAL_DISPOSITION_PREFIX):
                    continue  # <-- the skip that §D.17 forbids
                verdict = stripped[len(A.FORMAL_DISPOSITION_PREFIX):].strip()
                for separator in ("—", "--", " - ", "|"):
                    if separator in verdict:
                        verdict = verdict.split(separator, 1)[0].strip()
                return verdict
            return None

        assert naive(body) == A.APPROVING_REVIEW_DISPOSITION


class TestAllThreeProductionConsumersAreNamed:
    """§D.15 -- correctness at the function is not correctness at the consumers."""

    CONSUMERS = (
        "_derive_pr337_actor_ratification",
        "verify_lifecycle_against_truth",
        "_verify_selected_review_is_final",
    )

    @pytest.mark.parametrize("name", CONSUMERS)
    def test_each_named_consumer_is_cited_in_the_clause(self, decision, name):
        section = _section(decision, "### D. The required safety boundary")
        assert f"`{name}()`" in section, name

    @pytest.mark.parametrize("role", (
        "PR #337 ratification parsing",
        "the selected independent-review Gate 1",
        "later-review finality classification",
    ))
    def test_each_consumers_role_is_stated(self, flat, role):
        assert role in flat, role

    def test_the_clause_requires_exercising_all_three(self, flat):
        assert "must exercise the corrected behaviour through **all three**, not through the function alone" in flat
        assert "correct in isolation and wrong at one consumer is not corrected" in flat

    def test_the_named_consumers_are_exactly_the_live_call_sites(self):
        """Non-vacuity: the claim is re-derived from the module, not trusted from the prose."""
        tree = ast.parse((ROOT / AUTHORIZATION_MODULE_RELPATH).read_text())
        enclosing: list[str] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for inner in ast.walk(node):
                if (
                    isinstance(inner, ast.Call)
                    and isinstance(inner.func, ast.Name)
                    and inner.func.id == "parse_formal_disposition"
                ):
                    enclosing.append(node.name)
        # Nested definitions would double-count; the set is what the clause asserts.
        assert set(enclosing) == set(self.CONSUMERS), sorted(set(enclosing))


class TestTheAcceptedGrammarIsClosedAtTwoForms:
    """§D.16 -- the two demonstrated shapes, and no convenience generalisation."""

    def test_the_two_accepted_forms_are_bound_to_the_scan_counts(self, flat):
        assert "the **20** existing plain canonical lines and the" in flat
        assert "**8** precisely balanced whole-line `**…**` forms" in flat

    @pytest.mark.parametrize("rejected", (
        "Markdown headings", "blockquotes", "bullets", "inline prose", "code fences",
    ))
    def test_each_named_decoration_is_refused_by_default(self, flat, rejected):
        assert rejected in flat, rejected

    def test_expansion_requires_proof_and_governed_text_together(self, flat):
        assert "must **not** silently expand the accepted grammar" in flat
        assert "its own separate proof **and** its own explicit governed text" in flat

    def test_appearing_in_the_record_is_not_itself_admission(self, flat):
        """The heading form appears six times; that must not make it accepted."""
        assert "never because a rejected form happens to appear in the record" in flat
        assert "never by a convenience generalisation" in flat


class TestUnsupportedFormalLinesFailClosed:
    """§D.17 -- the clause the demonstration exists to justify."""

    def test_the_rule_is_stated_as_stopping_the_parse(self, flat):
        assert "must **stop the parse and yield no verdict**" in flat

    def test_skipping_is_named_as_the_failure_mode(self, flat):
        assert "may not be passed over so that a later, better-formed line wins" in flat
        assert "**Skipping is the failure mode; failing closed is the requirement.**" in flat

    def test_the_worked_example_is_present_in_the_clause(self, decision):
        section = _section(decision, "### D. The required safety boundary")
        assert "## FORMAL DISPOSITION: CHANGES REQUIRED" in section
        assert "this body must **not** authenticate" in _flat(section)

    def test_the_required_outcome_of_the_worked_example_is_stated(self, flat):
        assert "The unsupported first formal-looking line must prevent the later approval from winning." in flat

    @pytest.mark.parametrize("shape", (
        "blockquotes", "bullets", "malformed or unbalanced emphasis", "nested emphasis",
        "leading or trailing\nprose", "partial wrappers", "code-fenced lines",
    ))
    def test_the_rule_generalises_to_every_other_unsupported_shape(self, decision, shape):
        assert shape in decision, shape


class TestRequiredBehavioralCoverage:
    """§D.18 -- twelve cases, each its own directly-exercised item."""

    ITEMS = (
        "exact plain approval **accepted**",
        "exact balanced whole-line bold approval **accepted**",
        "exact bold `CHANGES REQUIRED` parsed as **adverse** and rejected",
        "an adverse first line followed by a later approval **rejected**",
        "native `CHANGES_REQUESTED` **independently** rejected",
        "approval appearing only in explanatory prose **rejected**",
        "heading, blockquote, bullet, code-fenced, nested, repeated, partial, and unbalanced wrappers",
        "the first valid formal line **remains governing**",
        "**all three** production consumers named in §D.15",
        "changes from **unparseable** to the **exact**",
        "**remain unedited**",
        "fingerprints remain unchanged",
    )

    @pytest.mark.parametrize("item", ITEMS)
    def test_each_coverage_item_is_present(self, decision, item):
        assert item in decision, item

    def test_exactly_twelve_items_are_enumerated(self, decision):
        section = _section(decision, "### D. The required safety boundary")
        body = section[section.index("**D.18"):]
        numbers = re.findall(r"^(\d+)\. ", body, flags=re.M)
        assert numbers == [str(n) for n in range(1, 13)], numbers

    def test_the_coverage_is_a_floor_not_a_ceiling(self, flat):
        assert "must cover, at minimum, each of the" in flat
        assert "must fail if any regresses" in flat


class TestTheMandatoryZeroWriteRehearsal:
    """§L -- the prevention rule the link-5 stop actually earns."""

    def test_the_section_states_why_part_checking_failed(self, flat):
        assert "a defect that only appears at the **whole" in flat
        assert "Checking the parts is what failed." in flat

    def test_the_rehearsal_is_bound_to_the_real_public_path(self, decision):
        section = _section(decision, "### L. Mandatory downstream prevention")
        assert "build_authorization_payload()" in section
        assert "validate_authorization_document()" in section

    def test_the_rehearsal_uses_complete_evidence_and_an_exhaustive_review_list(self, flat):
        assert "**complete live lifecycle evidence**" in flat
        assert "**exhaustive** review list" in flat

    def test_the_pass_condition_is_valid_true_and_exactly_zero_errors(self, flat):
        assert "**`valid = True` with exactly zero errors**" in flat
        assert "A single error is a stop" in flat

    def test_the_rehearsal_is_a_precondition_on_drift_and_link5(self, flat):
        assert "before a renewed drift check or a fresh link-5 authorization" in flat

    def test_the_rehearsal_is_zero_write_and_arms_nothing(self, flat):
        assert "It calls neither `write_authorization()` nor any lane-mutating function" in flat
        assert "Rehearsing is not arming." in flat

    def test_part_checking_is_explicitly_refused_as_a_substitute(self, flat):
        assert "**Checking individual identities and validators is not a substitute**" in flat

    def test_the_section_grants_nothing(self, flat):
        assert "**This section imposes a precondition; it grants nothing.**" in flat
        assert "each remains separately unauthorized under" in flat

    def test_a_second_error_class_is_a_finding_not_work(self, flat):
        assert "a finding to report under §G, never work to perform" in flat


class TestTheReviewFormatConvention:
    """§M -- fix the source, without licensing a narrower parser or an edited record."""

    def test_the_convention_is_stated_for_future_reviews(self, flat):
        assert "the operative formal disposition must be a standalone, unformatted plain-text line" in flat
        assert "beginning exactly with `FORMAL DISPOSITION:`" in flat

    @pytest.mark.parametrize("banned", ("no bold", "no\nheading", "no quotation", "no bullet", "no code formatting"))
    def test_each_banned_decoration_is_named(self, decision, banned):
        assert banned in decision, banned

    def test_the_convention_does_not_narrow_the_parser(self, flat):
        assert "deliberately **not** a licence to narrow the parser" in flat
        assert "§D.16 still" in flat
        assert "cannot be reformatted" in flat

    def test_the_convention_governs_forward_only(self, flat):
        assert "governs what is written from here" in flat
        assert "§D governs what must be read" in flat

    def test_the_convention_licenses_no_edit_to_history(self, flat):
        assert "**This section changes no historical record**" in flat
        assert "may be edited to conform to it" in flat


class TestTheCorrectionCannotRestoreOperationalAuthority:
    def test_section_e_states_the_load_bearing_consequence(self, flat):
        assert "load-bearing path #1" in flat
        assert "necessarily changes a load-bearing byte" in flat

    def test_the_consequence_is_framed_as_defining_not_incidental(self, flat):
        assert "not a side effect to be managed" in flat

    def test_a_correction_that_appeared_to_restore_authority_is_a_defect(self, flat):
        assert "would be a defect, not a success" in flat


class TestDownstreamConsequences:
    """All six §H items, each bound to its own operative wording."""

    def test_item_1_requires_its_own_reviewed_and_accepted_pr(self, flat):
        assert "requires its own separately reviewed and accepted implementation" in flat
        assert "own independent FULL exact-head review under `OPS-0007` §1" in flat

    def test_item_2_cannot_restore_operational_authority(self, flat):
        assert "it cannot itself\n   restore operational authority" in _flat(
            DECISION.read_text()
        ) or "it cannot itself restore operational authority" in flat
        assert "**arms nothing**" in flat

    def test_item_3_requires_a_separate_rebinding_on_a_derived_merge_identity(self, flat):
        assert "step-8-equivalent rebinding requires its own separately authorized and performed" in flat
        assert "never a predicted SHA" in flat

    def test_item_3_predicts_no_merge_sha_anywhere(self, decision):
        """A predicted merge identity would be an unverifiable constant."""
        for token in re.findall(r"\b[0-9a-f]{40}\b", decision):
            assert token in {
                BASE_SHA, BOUND_MERGE_SHA, BOUND_MERGE_PARENT_1, BOUND_MERGE_PARENT_2,
                BOUND_MERGE_TREE, XASSET0052_ACCEPTED_HEAD, XASSET0052_BASE,
                DEFECTIVE_REVIEW_HEAD, ADVERSE_REVIEW_HEAD,
                # a git BLOB id, not a merge SHA -- it pins the module this filing must not touch
                AUTHORIZATION_MODULE_BLOB,
            }, token

    def test_item_4_keeps_readiness_drift_and_link5_separately_unauthorized(self, flat):
        assert "Renewed readiness verification, renewed drift verification, and a fresh link-5" in flat
        assert "Completing any one of them authorizes none of the others" in flat

    def test_item_5_keeps_xasset0052_effective_but_spent(self, flat):
        assert "remains effective as a historical decision, but its one-shot operational grant is" in flat
        assert LINK5_STOP_DETERMINATION in flat

    def test_item_6_keeps_stage1_unarmed(self, flat):
        assert "Stage 1 remains UNARMED and NOT EXECUTABLE; `ATTEMPT_1` remains intact, unclaimed" in flat

    def test_all_six_items_are_numbered_and_present(self, decision):
        section = _section(decision, "### H. Downstream consequences")
        numbers = re.findall(r"^\d+\. \*\*", section, flags=re.M)
        assert len(numbers) == 6, section[:400]


class TestXasset0052GrantIsSpentButTheDecisionStandsAsHistory:
    def test_the_spent_grant_is_recorded_with_its_determination(self, flat):
        assert LINK5_STOP_COMMENT in flat
        assert LINK5_STOP_DETERMINATION in flat
        assert LINK5_STOP_BODY_SHA256 in flat

    def test_the_predecessor_file_is_not_edited(self):
        assert _blob_at(BASE_SHA, str(D0052.relative_to(ROOT))) == _git(
            "hash-object", str(D0052.relative_to(ROOT))
        ).strip()

    def test_xasset0052_is_not_revived(self, flat):
        assert "It is not revived, reinterpreted, extended, or re-opened" in flat
        assert "its `status` is not changed" in flat

    def test_reviving_it_was_considered_and_rejected(self, decision):
        assert "Revive `XASSET-0052` rather than file separately" in decision

    def test_the_predecessor_still_declares_its_grant_exhausted_on_any_outcome(self):
        text = D0052.read_text()
        assert "the unit's next act is to report and stop" in text
        assert "authorizes any successor unit" in text

    def test_the_earlier_spent_grant_stays_a_negative_pin(self, flat):
        """XASSET-0040 remains spent one generation earlier; it must not reappear as authority."""
        assert SPENT_STEP11_EVIDENCE_COMMENT not in flat or "XASSET-0040" in flat


class TestTheCorrectionIsNotPerformedHere:
    """The single most important guard: this PR must not touch the module it authorizes."""

    def test_the_authorization_module_blob_is_unchanged(self):
        assert _blob_at(BASE_SHA, AUTHORIZATION_MODULE_RELPATH) == AUTHORIZATION_MODULE_BLOB
        assert _git("hash-object", AUTHORIZATION_MODULE_RELPATH).strip() == \
            AUTHORIZATION_MODULE_BLOB

    def test_the_authorization_module_content_hash_is_unchanged(self):
        digest = hashlib.sha256((ROOT / AUTHORIZATION_MODULE_RELPATH).read_bytes()).hexdigest()
        assert digest == AUTHORIZATION_MODULE_SHA256

    def test_the_parser_still_has_its_uncorrected_contract(self):
        """Non-vacuity for the guard above: the defect is still live at this head."""
        body = f"{DEFECTIVE_FORMAL_LINE}\n"
        assert A.parse_formal_disposition(body) is None

    @pytest.mark.parametrize("relpath,digest", sorted(OUTCOME_CAPABLE_MODULE_WITNESS.items()))
    def test_every_outcome_capable_module_is_identical_to_the_bound_merge(self, relpath, digest):
        assert _sha256_at(BOUND_MERGE_SHA, relpath) == digest
        assert hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest() == digest

    def test_all_eighteen_load_bearing_paths_are_identical_to_the_bound_merge(self):
        assert len(A.LOAD_BEARING_RELPATHS) == EXPECTED_LOAD_BEARING_COUNT
        assert len(set(A.LOAD_BEARING_RELPATHS)) == EXPECTED_LOAD_BEARING_COUNT
        for relpath in A.LOAD_BEARING_RELPATHS:
            assert _blob_at(BOUND_MERGE_SHA, relpath) == _git("hash-object", relpath).strip(), relpath

    @pytest.mark.parametrize("relpath", PORTFOLIO_RELPATHS)
    def test_every_protected_portfolio_path_is_identical_to_the_bound_merge(self, relpath):
        assert _blob_at(BOUND_MERGE_SHA, relpath) == _git("hash-object", relpath).strip()

    @pytest.mark.parametrize("relpath,digest", sorted(CANONICAL_PINS.items()))
    def test_the_canonical_pins_match(self, relpath, digest):
        assert hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest() == digest

    def test_the_diff_against_the_base_touches_no_protected_or_load_bearing_path(self):
        changed = set(_git("diff", "--name-only", BASE_SHA).split())
        forbidden = set(A.LOAD_BEARING_RELPATHS) | set(PORTFOLIO_RELPATHS) | set(CANONICAL_PINS)
        assert not (changed & forbidden), sorted(changed & forbidden)


class TestTheAttestationMechanismIsClosedAndUnchanged:
    def test_the_bound_constants_did_not_move(self):
        assert A.AUTHORIZING_DECISION == BOUND_AUTHORIZING_DECISION
        assert A.AUTHORIZING_PULL_REQUEST == BOUND_AUTHORIZING_PULL_REQUEST
        assert A.REVIEWED_BASE_SHA == BOUND_REVIEWED_BASE_SHA

    def test_the_lifecycle_gate_tuple_is_unchanged(self):
        assert A.REQUIRED_LIFECYCLE_GATES == EXPECTED_LIFECYCLE_GATES

    def test_this_decision_is_not_inserted_into_the_mechanism(self):
        src = (ROOT / AUTHORIZATION_MODULE_RELPATH).read_text()
        assert DECISION_ID not in src

    def test_the_filing_forbids_rebinding_the_mechanism(self, decision):
        bullets = _bullets_under(decision, "The parser-correction unit, and this filing, **must not**:")
        assert any("perform a step-8-equivalent rebinding" in b for b in bullets)
        assert any("`REVIEWED_BASE_SHA`, or `LOAD_BEARING_RELPATHS`" in b for b in bullets)

    def test_the_bound_merge_structure_is_still_what_it_was(self):
        parents = _git("rev-list", "--parents", "-n1", BOUND_MERGE_SHA).split()[1:]
        assert parents == [BOUND_MERGE_PARENT_1, BOUND_MERGE_PARENT_2]
        assert _git("rev-parse", f"{BOUND_MERGE_SHA}^{{tree}}").strip() == BOUND_MERGE_TREE


class TestProhibitionsAreBoundToTheirGoverningClause:
    """Whole-line binding, so prefixing a permissive qualifier FAILS rather than survives."""

    REQUIRED_BULLETS = (
        "perform, arm, claim, execute, or complete any part of",
        "create an attestation, `AUTHORIZATION_ROOT`, lane state, `READY`, claim, completion,",
        "consume, claim, or touch `ATTEMPT_1`",
        "**perform a step-8-equivalent rebinding**",
        "perform renewed readiness verification or a renewed drift check;",
        "authorize any successor unit of any kind;",
        "edit any historical review, comment, acceptance record, or closure record;",
        "modify any runner, result validator, universe module, canonical artifact, or protected",
        "weaken any adverse-review rejection, any validator, or any test;",
        "change any construction identity, universe membership, ordering, cardinality,",
        "acquire market, fundamental, economic, or Stage-2 data",
        "read, list, open, or substantively reuse any `risk_lane_boundary` protected `RISK`",
        "create any endpoint, bound, point, range, percentage, weight, rank, target, ladder,",
    )


    def test_the_clause_parses_to_real_bullets(self, bullets):
        assert len(bullets) >= len(self.REQUIRED_BULLETS)

    @pytest.mark.parametrize("needle", REQUIRED_BULLETS)
    def test_each_prohibition_is_governed_by_the_must_not_clause(self, bullets, needle):
        assert any(needle in b for b in bullets), needle

    @pytest.mark.parametrize("qualifier", ["unless", "except where", "may, if", "at its discretion"])
    def test_no_bullet_carries_a_permissive_qualifier(self, bullets, qualifier):
        for b in bullets:
            assert qualifier not in b.lower(), b


class TestFailClosed:
    def test_uncertainty_is_failure(self, flat):
        assert "**Uncertainty is failure.**" in flat

    def test_the_unit_is_an_implementer_not_a_remediator(self, flat):
        assert "never a remediator of anything beyond" in flat

    def test_a_second_defect_is_a_finding_not_work(self, flat):
        assert "that is a finding to report, not work to perform" in flat

    def test_the_predecessors_finding_is_not_authority_rule_is_honoured(self, flat):
        assert "Finding the work is not authority to do the work" in flat


class TestEffectivityRequiresCompleteLifecycleClosure:
    def test_all_seven_conditions_are_enumerated(self, decision):
        section = _section(decision, "### J. Effectivity")
        numbers = re.findall(r"^\d+\. ", section, flags=re.M)
        assert len(numbers) == 7, section[:400]

    def test_no_single_step_is_sufficient(self, flat):
        assert "**None is individually sufficient.**" in flat
        assert "Only complete closure of all seven does" in flat

    def test_merge_commit_ci_must_be_the_exact_merge_sha(self, flat):
        assert "successful merge-commit CI whose `head_sha` is the exact merge SHA" in flat
        assert "not the PR head's own" in flat

    def test_even_after_closure_the_boundary_still_binds(self, flat):
        assert "which must still satisfy every clause of §D" in flat


class TestStage1RemainsUnarmedAndNotExecutable:
    def test_the_lane_is_absent(self):
        state, _ = A.lane_state_at(A.LanePaths())
        assert state == A.LANE_ABSENT

    def test_neither_authorization_predicate_is_true(self):
        assert A.new_execution_is_authorized()[0] is False
        assert A.active_execution_is_authorized()[0] is False

    def test_the_authorization_root_does_not_exist(self):
        assert not A.AUTHORIZATION_ROOT.exists()

    def test_the_attempt_identity_is_unchanged(self):
        assert A.EXECUTION_ATTEMPT_ID == ATTEMPT_ID

    def test_no_results_artifact_exists_anywhere_in_the_tree(self):
        tracked = [p for p in _git("ls-files").splitlines() if p.endswith("stage1_results.yaml")]
        assert tracked == []
        assert not (ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()

    def test_the_universe_identity_is_untouched(self):
        facts = A.live_construction_universe_facts()
        assert facts["count"] == CONSTRUCTION_COUNT
        assert facts["cell_count"] == CELL_COUNT
        assert facts["sha256"] == UNIVERSE_SHA
        assert A.CONSTRUCTION_UNIVERSE_SHA256 == UNIVERSE_SHA

    def test_the_filing_states_the_posture(self, flat):
        assert "Stage 1 remains UNARMED and NOT EXECUTABLE" in flat
        assert "`ATTEMPT_1` is intact, unclaimed, and unconsumed" in flat

    def test_the_reserved_results_pr_is_untouched(self, flat):
        assert "`XASSET-0027` §P.1 remains **one, unspent**" in flat


class TestPackagingAndEvidence:
    def test_the_filing_is_governance_only(self, flat):
        assert "**one** governance-only authorization filing" in flat
        assert "makes no production change" in flat

    def test_the_pr_number_is_never_predicted(self, flat):
        assert "Its pull-request number is never predicted" in flat
        assert "read back from the live API" in flat
        assert "fast-forward" in flat

    def test_the_sentinel_is_retained_as_a_negative_pin(self, flat):
        assert "retained afterwards as a **negative** pin" in flat


# =============================================================================================
# Register and catalog
# =============================================================================================


class TestRegisterSynchronisation:
    def test_the_workstream_is_untouched_in_status_and_priority(self, ws0014):
        assert ws0014["status"] == "proposed"
        assert ws0014["priority"] == "secondary"

    def test_exactly_zero_primary_workstreams(self):
        data = yaml.safe_load(WORKSTREAMS.read_text())
        assert sum(1 for w in data["workstreams"] if w.get("priority") == "primary") == 0

    def test_the_active_branch_names_this_unit(self, ws0014):
        assert ws0014["active_branch"] == BRANCH

    def test_the_last_verified_main_sha_advanced_and_is_bound_at_both_ends(self, ws0014):
        assert ws0014["last_verified_main_sha"] == BASE_SHA
        for finished in (XASSET0052_BASE, BOUND_MERGE_SHA, XASSET0052_ACCEPTED_HEAD):
            assert ws0014["last_verified_main_sha"] != finished, finished

    def test_the_active_pr_is_the_real_github_number_not_the_sentinel(self, ws0014):
        active = ws0014["active_pr"]
        assert active == THIS_PULL_REQUEST
        assert active != PR_SENTINEL, "the sentinel was never replaced"
        assert active not in PRIOR_SENTINELS
        assert active > BOUND_AUTHORIZING_PULL_REQUEST

    def test_the_finished_units_gate_is_not_rewritten(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == PRIOR_UNIT_GATE)
        assert gate["status"] == "in_progress" and gate["pr"] == 353

    def test_an_additive_closure_gate_records_the_finished_lifecycle_and_the_stop(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == PRIOR_CLOSURE_GATE)
        assert gate["status"] == "complete" and gate["pr"] == 353
        flat = _flat(gate["description"])
        assert BASE_SHA in flat
        assert XASSET0052_CLOSURE_COMMENT in flat
        assert LINK5_STOP_COMMENT in flat
        assert LINK5_STOP_DETERMINATION in flat
        assert XASSET0052_MERGE_CI_RUN in flat and XASSET0052_MERGE_CI_JOB in flat
        assert "LEFT BYTE-UNEDITED" in flat

    def test_this_units_gate_exists_and_is_in_progress(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)
        assert gate["status"] == "in_progress"
        assert gate["pr"] == THIS_PULL_REQUEST
        assert gate["pr"] != PR_SENTINEL, "the sentinel was never replaced"

    def test_this_units_gate_is_not_marked_complete_by_its_own_filing(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)
        assert gate["status"] != "complete"

    def test_the_registers_gate_records_the_authority_performance_distinction(self, ws0014):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert "AUTHORIZES" in gate
        assert "THIS FILING PERFORMS NONE OF THAT WORK" in gate
        assert "NOT EXERCISABLE UNLESS AND UNTIL" in gate

    def test_the_registers_gate_never_denies_the_authority_it_records(self, ws0014):
        """PR #353's probe M2-g, applied here from the start rather than after a miss."""
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        marker = "THREE CLAIMS ARE PROHIBITED"
        assert marker in gate, "the gate must carry the prohibition list"
        operative, prohibited = gate.split(marker, 1)
        for banned in (
            "NOT AUTHORIZED BY THIS FILING ITSELF",
            "ZERO correction authority",
            "zero correction authority",
        ):
            assert banned not in operative, banned
        assert "not authorized by this filing itself" in prohibited
        assert "zero correction authority" in prohibited

    def test_the_registers_gate_records_the_load_bearing_consequence(self, ws0014):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert "LOAD-BEARING" in gate
        assert "CANNOT ITSELF RESTORE OPERATIONAL AUTHORITY" in gate

    def test_the_registers_gate_records_the_spent_link5_grant(self, ws0014):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert LINK5_STOP_DETERMINATION in gate
        assert "SPENT" in gate

    def test_the_registers_gate_records_the_eighteen_clause_boundary(self, ws0014):
        """The count is load-bearing: a stale 'fourteen' would understate the boundary."""
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert "eighteen conjunctive clauses" in gate
        assert "fourteen conjunctive clauses" not in gate

    @pytest.mark.parametrize("fragment", (
        "EXACTLY THREE production call sites",
        "_derive_pr337_actor_ratification",
        "verify_lifecycle_against_truth",
        "_verify_selected_review_is_final",
        "34 FORMAL DISPOSITION lines",
        "20 plain canonical",
        "CLOSES THE ACCEPTED GRAMMAR",
        "FAIL CLOSED RATHER THAN BE SKIPPED",
        "END-TO-END, ZERO-WRITE REHEARSAL",
        "EXACTLY ZERO ERRORS",
        "NOT A SUBSTITUTE",
        "REVIEW-FORMAT CONVENTION",
    ))
    def test_the_registers_gate_records_the_audit_addendum(self, ws0014, fragment):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert fragment in gate, fragment

    def test_the_registers_gate_states_the_addendum_grants_nothing(self, ws0014):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert "THE ADDENDUM AUTHORIZES NOTHING" in gate
        assert "adds no authority" in gate

    @pytest.mark.parametrize("fragment", (
        "AN INCORPORATED READ-ONLY AUDIT ADDENDUM",
        "adding NO authority",
        "EXACTLY THREE production call sites (AST-confirmed)",
        "34 FORMAL DISPOSITION lines (20 plain, 8 balanced whole-line bold, 6 heading)",
        "FAIL CLOSED, never be skipped",
        "ZERO-WRITE rehearsal through the real public path",
        "EXACTLY ZERO ERRORS",
        "NOT a substitute",
        "rehearsing is not arming",
        "THE ADDENDUM AUTHORIZES NOTHING",
    ))
    def test_both_operative_blocks_carry_the_addendum(self, ws0014, fragment):
        for field in ("next_action", "blocker"):
            assert fragment in _flat(ws0014[field]), (field, fragment)

    def test_the_registers_latest_operative_blocks_carry_the_grant_and_its_bound(self, ws0014):
        for field in ("next_action", "blocker"):
            text = ws0014[field]
            assert "UPDATE, 2026-08-24" in text, field
            latest = _flat("UPDATE, 2026-08-24" + text.rsplit("UPDATE, 2026-08-24", 1)[1])
            assert "XASSET-0053" in latest, field
            assert "PARSER-CONTRACT CORRECTION" in latest, field
            assert "CANNOT ITSELF RESTORE OPERATIONAL AUTHORITY" in latest, field
            assert LINK5_STOP_DETERMINATION in latest, field
            assert "UNARMED" in latest, field

    def test_the_registers_latest_operative_blocks_never_deny_the_authority(self, ws0014):
        for field in ("next_action", "blocker"):
            text = ws0014[field]
            latest = _flat("UPDATE, 2026-08-24" + text.rsplit("UPDATE, 2026-08-24", 1)[1])
            assert "NOT AUTHORIZED BY THIS FILING ITSELF" not in latest, field

    def test_prior_history_is_preserved_additively(self, ws0014):
        """Earlier dated blocks keep their own accurate wording; nothing is rewritten."""
        for field in ("next_action", "blocker"):
            assert "UPDATE, 2026-08-23" in ws0014[field], field

    def test_no_sentinel_survives_anywhere_in_the_register(self):
        raw = WORKSTREAMS.read_text()
        for sentinel in (PR_SENTINEL, *PRIOR_SENTINELS):
            assert f"active_pr: {sentinel}" not in raw, sentinel
            assert f"pr: {sentinel}" not in raw, sentinel

    def test_no_sentinel_survives_anywhere_in_the_tracked_tree(self):
        tracked = _git("ls-files").splitlines()
        needle = f"active_pr: {PR_SENTINEL}"
        for rel in tracked:
            path = ROOT / rel
            if not path.is_file():
                continue
            try:
                text = path.read_text()
            except (UnicodeDecodeError, OSError):
                continue
            assert needle not in text, rel


class TestCatalogSynchronisation:
    def test_the_catalog_lists_this_decision_last_and_uniquely(self, catalog):
        ids = [d["decision_id"] for d in catalog]
        assert len(ids) == len(set(ids))
        assert ids[-1] == DECISION_ID
        assert ids.count(DECISION_ID) == 1

    def test_the_catalog_entry_points_at_the_real_file(self, catalog):
        entry = next(d for d in catalog if d["decision_id"] == DECISION_ID)
        assert (ROOT / entry["file"]).exists()
        assert entry["file"] == str(DECISION.relative_to(ROOT))
        assert entry["status"] == "Proposed"
        assert entry["supporting_artifact"] == Path(__file__).name

    def test_the_catalog_entry_relates_to_the_whole_chain(self, catalog):
        entry = next(d for d in catalog if d["decision_id"] == DECISION_ID)
        related = set(entry["related_decisions"])
        for required in ("XASSET-0040", "XASSET-0048", "XASSET-0049", "XASSET-0052"):
            assert required in related, required

    def test_the_catalog_has_no_open_issues(self):
        from portfolio_hq.dashboard import decisions as dash

        built = dash.build_catalog(ROOT)
        assert built.issues == ()


# =============================================================================================
# Non-vacuity
# =============================================================================================


class TestNonVacuityAgainstTheBaseTree:
    """A guard against a suite that would pass identically before this filing existed."""

    def test_the_decision_file_did_not_exist_at_the_base(self):
        rel = str(DECISION.relative_to(ROOT))
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{BASE_SHA}:{rel}"], cwd=ROOT, capture_output=True
        )
        assert result.returncode != 0, "the decision already existed at the base"

    def test_this_test_module_did_not_exist_at_the_base(self):
        rel = Path(__file__).name
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{BASE_SHA}:{rel}"], cwd=ROOT, capture_output=True
        )
        assert result.returncode != 0, "the suite already existed at the base"

    def test_the_gates_did_not_exist_at_the_base(self):
        raw = _git("show", f"{BASE_SHA}:operations/WORKSTREAMS.yaml")
        assert THIS_GATE not in raw
        assert PRIOR_CLOSURE_GATE not in raw

    def test_the_catalog_gained_exactly_one_entry(self, catalog):
        before = yaml.safe_load(_git("show", f"{BASE_SHA}:governance/decisions.yaml"))["decisions"]
        assert len(catalog) == len(before) + 1
        assert DECISION_ID not in {d["decision_id"] for d in before}

    def test_the_base_did_not_already_name_this_decision_anywhere(self):
        result = subprocess.run(
            ["git", "grep", "-l", DECISION_ID, BASE_SHA], cwd=ROOT, capture_output=True, text=True
        )
        assert result.returncode != 0, result.stdout

    def test_the_shared_register_fields_actually_moved(self):
        raw = _git("show", f"{BASE_SHA}:operations/WORKSTREAMS.yaml")
        before = next(w for w in yaml.safe_load(raw)["workstreams"] if w["id"] == "WS-0014")
        assert before["active_pr"] == 353
        assert before["last_verified_main_sha"] == XASSET0052_BASE
        assert before["active_branch"] != BRANCH
