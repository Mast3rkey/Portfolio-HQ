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

#: RE-ANCHOR (XASSET-0056). THIS unit's own closed merge -- PR #354, merged with a merge tree
#: byte-identical to its accepted head. This filing AUTHORIZED the parser correction and did not
#: perform it; that remains permanently true OF THIS UNIT and is now asserted against this
#: immutable merge instead of against a live working tree that the lawfully authorized successor
#: correction now also occupies. Every superseded value below is retained, and each re-anchored
#: assertion is additionally pinned at its live end so a silent revert still fails.
DECISION_MERGE_SHA = "683c324629544a84d2cf75ebca37325e3375c479"
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

#: RE-ANCHORED BY XASSET-0055. `active_branch`, `active_pr` and `last_verified_main_sha` are
#: WS-0014's SINGLE SHARED live self-reference fields, not this unit's own. PR #354 -- this
#: unit's own pull request -- merged at `683c3246...`, so under OPS-0001's Active-GitHub-fields
#: rule the shared fields lawfully advanced onto the successor that is now live. This unit's own
#: values are retained below as NEGATIVE pins rather than deleted, and its own GATE still carries
#: its own real number, which is the immutable fact those assertions were really protecting.
#: There is deliberately no XASSET-0054 generation: XASSET-0054's pull request #355 was CLOSED
#: UNMERGED after independent DELTA review 5010334966, so it never became `main` state.
#: RE-ANCHORED AGAIN BY XASSET-0056, the single replacement parser-correction implementation
#: XASSET-0055 §H authorized. The shared live fields moved on once more; the XASSET-0055
#: generation joins the negative pins below rather than being deleted, so the fields stay bound
#: at BOTH ends across every generation and a silent revert to ANY finished unit still fails.
#: Named with the generational constant this corpus uses everywhere else, so every re-anchored
#: suite states the SAME positive pin under the SAME name and can be checked uniformly.
XASSET0056_MAIN_SHA = "29e4969885970d942a5acecc1424fb2e2b080d60"

#: ADVANCED BY XASSET-0057. WS-0014's SINGLE SHARED live self-reference field advances
#: with every generation; XASSET-0056's own value is retained above as a NEGATIVE pin, so
#: a silent revert to that finished unit's state still fails here.
XASSET0057_MAIN_SHA = "583022a5f2106d61f82d270edadd3520d8b0c55d"
#: RETAINED above as a negative pin rather than deleted, so every field stays bound at BOTH
#: ends and a silent revert to ANY finished unit's state still fails here.
#: ADVANCED BY XASSET-0058. WS-0014's SINGLE SHARED live self-reference field advances with
#: every generation; XASSET-0057's own value is retained above as a NEGATIVE pin, so a silent
#: revert to that finished unit's state still fails here.
XASSET0058_MAIN_SHA = "556a43cf91679d3e8ca95703c8d49e672b662b73"
#: ADVANCED BY XASSET-0059 -- the Lifecycle B parser correction XASSET-0058 SS-F authorized.
#: WS-0014's live self-reference fields are SHARED under OPS-0001's Active-GitHub-fields
#: rule, so they name whichever unit is live. The superseded value is retained BESIDE the
#: new one as a NEGATIVE pin -- bound at both ends, so a silent revert to finished work
#: still fails -- and nothing is deleted, skipped or relaxed.
XASSET0059_MAIN_SHA = "34c45900ce23742d04d80cf12471c34aabe9682d"
#: ADVANCED BY XASSET-0058. The shared live fields moved once more onto the successor;
#: XASSET-0057's own values are RETAINED as negative pins rather than deleted, so every
#: field stays bound at BOTH ends.
#: ADVANCED BY XASSET-0059: the shared field moved onto the Lifecycle B unit's own base.
SUCCESSOR_MAIN_SHA = XASSET0059_MAIN_SHA
#: ADVANCED BY XASSET-0059: WS-0014's SHARED live branch moved onto the Lifecycle B unit;
#: the XASSET-0058 generation is retained beside it as a NEGATIVE pin.
SUCCESSOR_BRANCH = "claude/xasset-0058-parser-correction-a2kteq"
XASSET0058_BRANCH = "claude/parser-correction-xasset-auth-w91gse"
XASSET0057_BRANCH = "claude/xasset-successor-authorization-3b0btg"
#: The generation this one superseded, retained as a negative pin.
XASSET0055_MAIN_SHA = "683c324629544a84d2cf75ebca37325e3375c479"
XASSET0055_BRANCH = "claude/xasset-0055-parser-contract-conflict-w4kp2n"
#: The branch of the unit that was closed unmerged. Preserved history, never live state.
CLOSED_UNMERGED_BRANCH = "claude/xasset-0054-parser-contract-correction-h3nq7p"
#: Every decision appended to the catalog AFTER this one. The catalog assertions below stay
#: EXACT by naming this set explicitly rather than being relaxed to "somewhere in the list".
#: ADVANCED BY XASSET-0059, appended after XASSET-0058 and named EXACTLY, so "last"
#: stays an EXACT index rather than being relaxed to "present".
SUCCESSORS_APPENDED_SINCE = ("XASSET-0055", "XASSET-0056", "XASSET-0057", "XASSET-0058", "XASSET-0059")


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


#: Historical modules are immutable, so one import per commit is enough.
_HISTORICAL_MODULE_CACHE: dict = {}


def _module_at(commit: str):
    """Import the authorization module EXACTLY as it existed at ``commit``.

    RE-ANCHOR support (XASSET-0056). The defect this filing reproduced is a property of those
    historical bytes, so it is re-proved by executing them, not by matching text. Nothing is
    written to the repository: the blob is materialised in a private temporary directory.
    """
    import importlib.util
    import sys
    import tempfile

    cached = _HISTORICAL_MODULE_CACHE.get(commit)
    if cached is not None:
        return cached

    source = subprocess.run(
        ["git", "show", f"{commit}:{AUTHORIZATION_MODULE_RELPATH}"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    directory = tempfile.mkdtemp(prefix="phq-historical-module-")
    path = Path(directory) / f"_historical_{commit[:12]}.py"
    path.write_bytes(source)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    # ``@dataclass`` resolves ``sys.modules[cls.__module__].__dict__`` while the class body is
    # executing, so the module must be registered BEFORE ``exec_module`` runs.
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    _HISTORICAL_MODULE_CACHE[commit] = module
    return module


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


def _clause_body(text: str, clause: str) -> str:
    """One '**D.n — ...' clause's body, up to the next clause or the next section heading."""
    start = text.index(f"**{clause} \u2014 ")
    rest = text[start:]
    ends = [i for i in (rest.find("\n**D.", 1), rest.find("\n### ", 1)) if i > 0]
    return rest if not ends else rest[:min(ends)]


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
        """RE-ANCHORED (XASSET-0056): the defect, re-proved by EXECUTING this unit's own bytes.

        Not relaxed to a text match. The historical module is imported and its parser called, so
        the reproduction is still behavioural -- it simply runs the bytes this unit actually
        shipped rather than bytes the authorized successor has since lawfully corrected.
        """
        body = f"## header\n\n{DEFECTIVE_FORMAL_LINE}\n\nexplanatory text\n"
        assert _module_at(DECISION_MERGE_SHA).parse_formal_disposition(body) is None

    def test_the_defective_line_now_parses_under_the_authorized_successor(self):
        """NEGATIVE PIN for the re-anchor above: the defect is fixed, and must stay fixed."""
        body = f"## header\n\n{DEFECTIVE_FORMAL_LINE}\n\nexplanatory text\n"
        assert A.parse_formal_disposition(body) == A.APPROVING_REVIEW_DISPOSITION

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
    """All twenty §D clauses, bound as whole lines."""

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
        "D.11": "Preserve every surrounding protection unchanged in behaviour",
        "D.12": "Add behavioral and mutation tests",
        "D.13": "Do not edit review `5000581301`, any historical review, comment, acceptance",
        "D.14": "Do not repair any other parser (the three named consumers are not",
        "D.15": "Exercise all three production consumers",
        "D.16": "The accepted grammar is exactly the two demonstrated forms, and no more",
        "D.17": "An unsupported formal-looking line FAILS CLOSED; it is never skipped",
        "D.18": "Required behavioral coverage",
        "D.19": "ABSENT and MALFORMED / UNSUPPORTED must be distinguishable end to end",
        "D.20": "Required end-to-end proofs",
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

    def test_the_grammar_bound_is_tied_to_this_mismatch_specifically(self, decision):
        """Probe P10: 'beyond what this demonstrated mismatch requires' is the operative bound."""
        body = _flat(_clause_body(decision, "D.14"))
        assert "beyond what this demonstrated mismatch requires" in body
        assert "A second genuine mismatch, if one is ever demonstrated, is its own separate" in body

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
        """RE-ANCHORED (XASSET-0056): the §B.8 premise, re-proved against this unit's own bytes."""
        historical = _module_at(DECISION_MERGE_SHA)
        assert historical.parse_formal_disposition("## FORMAL DISPOSITION: CHANGES REQUIRED") is None
        assert historical.parse_formal_disposition(DEFECTIVE_FORMAL_LINE) is None

    def test_the_two_shapes_are_now_separated_by_the_authorized_successor(self):
        """NEGATIVE PIN: the skip-versus-fail-closed hazard §B.8 named is actually closed."""
        assert A.parse_formal_disposition("## FORMAL DISPOSITION: CHANGES REQUIRED") is \
            A.MALFORMED_FORMAL_DISPOSITION
        assert A.parse_formal_disposition(DEFECTIVE_FORMAL_LINE) == A.APPROVING_REVIEW_DISPOSITION

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
        body = _clause_body(decision, "D.18")
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


class TestTheParserOnlySurfaceWasProvedInsufficient:
    """§B.9 -- the unsatisfiability is reproduced against the live module, not asserted."""

    MALFORMED = (
        "## FORMAL DISPOSITION: CHANGES REQUIRED\n"
        "**FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE "
        "— 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE**\n"
    )
    ABSENT = "Looks good to me. No formal line at all."

    def test_the_finding_is_recorded_with_its_review_id(self, flat):
        assert "B.9 — Why a parser-only surface is not sufficient, reproduced." in flat
        assert "review `5004478133`" in flat
        assert "internally unsatisfiable" in flat

    def test_the_consumer_and_its_line_numbers_are_named(self, flat):
        assert "`_verify_selected_review_is_final()`" in flat
        assert "level1_stage1_execution_authorization.py:3387" in flat
        assert "lines 3446–3451" in flat

    def test_the_two_conflated_meanings_are_named(self, flat):
        assert "**ABSENT**" in flat
        assert "**MALFORMED / UNSUPPORTED**" in flat
        assert "carries **two different meanings at once**" in flat

    def test_the_native_state_set_is_quoted_exactly(self, flat):
        assert '`frozenset({"APPROVED"})`' in flat

    def test_the_named_consumer_really_exists_at_that_line(self):
        """RE-ANCHORED (XASSET-0056): the line citation is checked at this unit's own merge.

        A line NUMBER is only meaningful against the bytes that unit cited. The consumer's
        continued existence is additionally asserted in the live tree, so nothing is lost.
        """
        lines = _git("show", f"{DECISION_MERGE_SHA}:{AUTHORIZATION_MODULE_RELPATH}").splitlines()
        assert lines[3386].startswith("def _verify_selected_review_is_final("), lines[3386]
        live = (ROOT / AUTHORIZATION_MODULE_RELPATH).read_text()
        assert "\ndef _verify_selected_review_is_final(" in live

    def test_the_native_non_adverse_set_is_exactly_approved(self):
        assert set(A.NATIVE_NON_ADVERSE_REVIEW_STATES) == {"APPROVED"}

    def test_the_conflation_is_real_today(self):
        """RE-ANCHORED (XASSET-0056): the conflation §C item 2 rests on, at this unit's bytes."""
        historical = _module_at(DECISION_MERGE_SHA)
        assert historical.parse_formal_disposition(self.ABSENT) is None
        assert historical.parse_formal_disposition(self.MALFORMED) is None

    def test_the_conflation_is_resolved_by_the_authorized_successor(self):
        """NEGATIVE PIN: one value no longer stands for both meanings."""
        assert A.parse_formal_disposition(self.ABSENT) is None
        assert A.parse_formal_disposition(self.MALFORMED) is A.MALFORMED_FORMAL_DISPOSITION

    def test_the_consumer_would_accept_both_as_non_adverse(self):
        """Replays the consumer's own branch order; both reach 'accepted', which §D.17 forbids."""

        def consumer(state: str, verdict: str | None) -> str:
            if state in A.NATIVE_ADVERSE_REVIEW_STATES:
                return "rejected"
            if verdict == A.APPROVING_REVIEW_DISPOSITION:
                return "accepted"
            if verdict is None:
                return "accepted" if state in A.NATIVE_NON_ADVERSE_REVIEW_STATES else "rejected"
            return "rejected"

        # A corrected parser obeying §D.17 yields no verdict for BOTH bodies.
        assert consumer("APPROVED", None) == "accepted"
        # ...so a parser-only correction cannot make the malformed case fail closed.

    def test_the_consumer_branch_order_pinned_here_matches_the_module(self):
        """If the real branch order changes, this reproduction stops being faithful."""
        src = (ROOT / AUTHORIZATION_MODULE_RELPATH).read_text()
        body = src[src.index("def _verify_selected_review_is_final("):]
        body = body[: body.index("\n    return errors")]
        assert "verdict = parse_formal_disposition(" in body
        assert "if state in NATIVE_ADVERSE_REVIEW_STATES:" in body
        assert "if verdict == APPROVING_REVIEW_DISPOSITION:" in body
        assert "if verdict is None:" in body
        assert "if state in NATIVE_NON_ADVERSE_REVIEW_STATES:" in body


class TestTheWidenedSurfaceIsBoundedAndEnumerated:
    """§C item 2 -- a reasoned exception, not an open door into the module."""

    def test_the_permitted_surface_points_at_its_exhaustive_enumeration(self, flat):
        assert "smallest necessary production-contract adjustment that distinguishes ABSENT from" in flat
        assert "The permitted surface is enumerated exhaustively below, under" in flat
        assert "**The permitted set**, and stops there" in flat

    @pytest.mark.parametrize("piece", (
        "`parse_formal_disposition()` itself",
        "**the selected minimal result representation**",
        "exactly one newly introduced narrow helper devoted solely to distinguishing",
        "**the minimum necessary changes in its three existing production consumers**",
    ))
    def test_each_permitted_piece_is_named(self, flat, piece):
        assert piece in flat, piece

    CONSUMERS = (
        "_derive_pr337_actor_ratification",
        "verify_lifecycle_against_truth",
        "_verify_selected_review_is_final",
    )

    @pytest.mark.parametrize("consumer", CONSUMERS)
    def test_each_consumer_is_named_inside_the_grant(self, decision, consumer):
        section = _section(decision, "### C. Authority granted")
        assert consumer in section, consumer

    @pytest.mark.parametrize("consumer", CONSUMERS)
    def test_each_consumer_is_named_in_BOTH_the_grant_bullet_and_the_permitted_set(
        self, decision, consumer
    ):
        """Probe P44: item 2's bullet could lose a consumer while the permitted set kept it.

        Section-wide presence survived that, because the name still appeared elsewhere in §C.
        Both places are now bound independently, so the two lists cannot drift apart.
        """
        section = _section(decision, "### C. Authority granted")
        bullet = _flat(section[section.index("**the minimum necessary changes in its three existing"):
                               section.index("3. **Add or extend focused adversarial tests**")])
        assert consumer in bullet, ("item 2 bullet", consumer)
        assert consumer in self._permitted_set(decision), ("permitted set", consumer)

    def test_the_grant_bullet_and_the_permitted_set_name_the_same_three(self, decision):
        section = _section(decision, "### C. Authority granted")
        bullet = _flat(section[section.index("**the minimum necessary changes in its three existing"):
                               section.index("3. **Add or extend focused adversarial tests**")])
        permitted = self._permitted_set(decision)
        assert sum(c in bullet for c in self.CONSUMERS) == 3, bullet
        assert sum(c in permitted for c in self.CONSUMERS) == 3, permitted

    def test_a_general_parsing_framework_is_refused(self, flat):
        assert "general-purpose parsing framework is **not** permitted by any route" in flat

    def test_the_exception_is_declared_narrow_not_general(self, flat):
        assert "item 2 is a narrowly reasoned exception, not a general licence to" in flat

    # ------------------------------------------------------------------ the permitted set

    @staticmethod
    def _permitted_set(decision: str) -> str:
        """The exhaustive four-item permitted set, as its own span."""
        section = _section(decision, "### C. Authority granted")
        start = section.index("**The permitted set, stated once and exhaustively.**")
        rest = section[start:]
        return _flat(rest[: rest.index("**Everything outside that set is forbidden.**")])

    def test_the_permitted_set_is_declared_exhaustive(self, decision):
        span = self._permitted_set(decision)
        assert "Exactly four things may change inside" in span
        assert "and nothing else" in span

    @pytest.mark.parametrize("item", (
        "`parse_formal_disposition()`",
        "**selected minimal result representation** (one added value, one small typed result, or one sentinel)",
        "**at most one** newly introduced narrow helper",
        "**minimum necessary lines** in the three named existing consumers",
    ))
    def test_each_permitted_item_is_in_the_permitted_set(self, decision, item):
        assert item in self._permitted_set(decision), item

    def test_the_helper_is_conditional_not_an_entitlement(self, flat):
        assert "the helper is an option, not an entitlement" in flat
        assert "only if it is genuinely the smallest solution" in flat

    # ------------------------------------------------------------------ the exclusion

    EXCLUDED = (
        "any change to any other existing production function",
        "any fourth `parse_formal_disposition()` consumer or call site",
        "more than one newly introduced helper",
        "a general-purpose parsing framework",
        "review selection, chronology, pagination, exhaustion, reviewer-identity derivation",
        "redesign of the lifecycle-evidence",
        "`NATIVE_ADVERSE_REVIEW_STATES` or `NATIVE_NON_ADVERSE_REVIEW_STATES`",
        "unrelated parsing, lifecycle, review, execution, portfolio, or risk change",
    )

    @staticmethod
    def _excluded_clause(decision: str) -> str:
        """The span governed by 'it does **not** authorize:', up to its terminating sentence.

        Bound as a span, not as loose presence: probe P45 flipped the governing verb from
        'does **not** authorize' to 'permits' while every listed item stayed word-for-word
        intact, and a presence-only assertion survived it. Same defect class as P02/P03.
        """
        section = _section(decision, "### C. Authority granted")
        start = section.index("this filing does **not** authorize:")
        rest = section[start:]
        end = rest.index("No other module,")
        return _flat(rest[:end])

    def test_the_exclusions_are_governed_by_a_does_not_authorize_clause(self, decision):
        section = _section(decision, "### C. Authority granted")
        assert "**Everything outside that set is forbidden.**" in section
        assert "this filing does **not** authorize:" in section

    @pytest.mark.parametrize("excluded", EXCLUDED)
    def test_each_still_excluded_area_is_inside_that_clause(self, decision, excluded):
        assert excluded in self._excluded_clause(decision), excluded

    @pytest.mark.parametrize("permissive", ("permits:", "may also", "is free to", "authorizes:"))
    def test_the_governing_verb_is_never_permissive(self, decision, permissive):
        section = _flat(_section(decision, "### C. Authority granted"))
        assert f"Specifically, this filing {permissive}" not in section, permissive

    # ------------------------------------------------------------------ DELTA review 5004859164

    def test_the_retired_self_contradicting_exclusion_is_gone(self, decision):
        """DELTA review 5004859164 MINOR 1.

        'any function that is not one of the three named above' forbade the helper item 2
        permits -- and, read literally, item 1's own parse_formal_disposition() grant too,
        since the parser is not one of the three consumers.
        """
        section = _flat(_section(decision, "### C. Authority granted"))
        assert "any function that is not one of the three named above" not in section

    def test_the_helper_permission_and_the_exclusion_cannot_conflict(self, decision):
        """The binding regression assertion: permitted and prohibited at once must FAIL.

        Reproduces the finding's own literal reading mechanically rather than trusting prose:
        anything the permitted set grants is checked against what the exclusion forbids, and
        an overlap is an error.
        """
        permitted = self._permitted_set(decision)
        excluded = self._excluded_clause(decision)

        # What the permitted set actually grants, as concrete subjects.
        grants = {
            "parser": "`parse_formal_disposition()`" in permitted,
            "representation": "selected minimal result representation" in permitted,
            "helper": "newly introduced narrow helper" in permitted,
            "consumers": "three named existing consumers" in permitted,
        }
        assert all(grants.values()), grants

        # A blanket "every function outside the three consumers" ban would re-forbid the
        # parser AND the helper. It must not appear in any wording.
        for blanket in (
            "any function that is not one of the three named",
            "any function other than the three named",
            "no function outside the three named",
        ):
            assert blanket not in excluded, blanket

        # The exclusion's own function ban must be scoped to EXISTING OTHER functions, and
        # must say so -- so a newly introduced helper is outside its reach by construction.
        assert "any change to any other existing production function" in excluded
        assert "other than `parse_formal_disposition()` and the three named consumers above" in excluded
        assert "about *existing* functions" in excluded
        assert "does **not** reach items 2 and 3" in excluded
        assert "nothing in this list withdraws them" in excluded

        # And the helper ceiling is a COUNT limit, never a prohibition on the first one.
        assert "more than one newly introduced helper" in excluded
        assert "one is the ceiling" in excluded
        assert "at most one" in permitted

    def test_the_two_clauses_are_declared_to_be_read_together(self, flat):
        assert "written to be read together" in flat
        assert "nothing the permitted set grants may be read back out of it by this list" in flat
        assert "nothing this list forbids may be read back in by the permitted set" in flat

    def test_a_fourth_call_site_is_forbidden_explicitly(self, decision):
        excluded = self._excluded_clause(decision)
        assert "any fourth `parse_formal_disposition()` consumer or call site" in excluded
        assert "may not add a new call site" in excluded
        assert "may not route an existing function through the parser for the first time" in excluded

    def test_the_live_module_really_has_exactly_three_call_sites(self):
        """Non-vacuity for the 'fourth call site' prohibition: three exist today, so a
        fourth is a real thing the correction could add, not a hypothetical."""
        tree = ast.parse((ROOT / AUTHORIZATION_MODULE_RELPATH).read_text())
        sites = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for inner in ast.walk(node):
                if (
                    isinstance(inner, ast.Call)
                    and isinstance(inner.func, ast.Name)
                    and inner.func.id == "parse_formal_disposition"
                ):
                    sites.append(node.name)
        assert set(sites) == {
            "_derive_pr337_actor_ratification",
            "verify_lifecycle_against_truth",
            "_verify_selected_review_is_final",
        }, sorted(set(sites))

    def test_widening_is_declared_a_larger_correction_not_a_lighter_one(self, flat):
        assert "**A widened surface is a larger correction, not a lighter one.**" in flat
        assert "applies with more force, not less" in flat

    def test_h2_carries_the_same_consequence(self, flat):
        assert "This holds **more** strongly under §C item 2's widened surface, not less" in flat
        assert "moves more load-bearing bytes than a parser-only one" in flat
        assert "never closer to armed" in flat

    def test_d11_no_longer_claims_the_parse_and_nothing_else(self, decision):
        """The retired absolute would now contradict §C item 2."""
        body = _flat(_clause_body(decision, "D.11"))
        assert "touches the disposition *parse* and nothing else" not in body
        assert "the minimum necessary lines in exactly the three named consumers" in body
        assert "**and nothing else**" in body

    def test_d14_no_longer_reads_the_consumers_as_another_parser(self, decision):
        body = _clause_body(decision, "D.14")
        assert 'the three named consumers are not "another parser"' in body


class TestTheAbsentVersusMalformedDistinction:
    """§D.19 -- the clause the reproduction earns."""

    def test_both_states_are_defined(self, decision):
        body = _flat(_clause_body(decision, "D.19"))
        assert "carrying **no** formal-looking disposition is **ABSENT**" in body
        assert "not** in an accepted form (§D.16) is **MALFORMED / UNSUPPORTED**" in body

    def test_one_value_may_not_stand_for_both(self, decision):
        body = _flat(_clause_body(decision, "D.19"))
        assert "**separately observable** by every consumer" in body
        assert "one value may not stand for both" in body

    def test_malformed_fails_closed_even_under_native_approved(self, decision):
        body = _clause_body(decision, "D.19")
        assert "including where the review's native GitHub state is `APPROVED`" in _flat(body)
        assert "a native state may never rescue a refused formal line" in body

    def test_the_absent_policy_is_deliberately_preserved(self, decision):
        body = _flat(_clause_body(decision, "D.19"))
        assert "is **preserved**, not silently repurposed" in body
        assert "a finding to report under §G — never work to perform" in body

    def test_the_clause_is_tied_to_its_evidence_and_its_grant(self, decision):
        body = _flat(_clause_body(decision, "D.19"))
        assert "§B.9" in body
        assert "§C item 2" in body


class TestTheSevenEndToEndProofs:
    """§D.20 -- proved through the real production path, not against the parser alone."""

    PROOFS = (
        "genuinely **no** formal-looking disposition retains the existing non-adverse policy",
        "**unsupported formal-looking adverse line** fails finality",
        "balanced whole-line bold approval from PR #349 review `5000581301` is **accepted**",
        "wrapped **and** unwrapped adverse dispositions remain **rejected**",
        "**heading-form adverse line before a later valid-looking approval cannot be skipped**",
        "**all three** production consumers",
        "unsupported formal-looking lines are **never silently treated as absent**",
    )

    @pytest.mark.parametrize("proof", PROOFS)
    def test_each_proof_is_required(self, decision, proof):
        assert proof in _flat(_clause_body(decision, "D.20")), proof

    def test_exactly_seven_proofs_are_enumerated(self, decision):
        body = _clause_body(decision, "D.20")
        numbers = re.findall(r"^\d+\. ", body, flags=re.M)
        assert len(numbers) == 7, numbers

    def test_the_proofs_must_run_through_the_real_production_path(self, decision):
        body = _flat(_clause_body(decision, "D.20"))
        assert "**through the real production path**" in body
        assert "not against the parser in isolation" in body

    def test_all_three_consumers_are_named_in_the_proof_clause(self, decision):
        body = _flat(_clause_body(decision, "D.20"))
        for name in ("_derive_pr337_actor_ratification", "verify_lifecycle_against_truth",
                     "_verify_selected_review_is_final"):
            assert name in body, name


class TestTheWideningIsReasonedNotAssumed:
    """The Rationale and Alternatives must show the narrowing branch was actually weighed."""

    def test_the_rationale_states_the_two_honest_moves(self, flat):
        assert "there were two honest moves — narrow" in flat
        assert "the *less* safe option, not the smaller one" in flat

    def test_narrowing_the_requirement_is_a_rejected_alternative(self, decision):
        alts = decision[decision.index("## Alternatives Considered"):]
        assert "narrow §D.15 / §D.17 instead" in alts
        assert "Narrowing the requirement is the less safe branch" in alts

    def test_an_open_ended_surface_is_a_rejected_alternative(self, decision):
        alts = decision[decision.index("## Alternatives Considered"):]
        assert 'Widen §C to "whatever the correction needs inside the module"' in alts
        assert "unreviewable" in alts

    def test_changing_the_native_state_set_is_a_rejected_alternative(self, decision):
        alts = decision[decision.index("## Alternatives Considered"):]
        assert "Change `NATIVE_NON_ADVERSE_REVIEW_STATES`" in alts

    def test_the_consequences_state_the_widened_but_bounded_surface(self, flat):
        assert "only to the smallest extent" in flat
        assert "§D.19's distinction and §D.20's" in flat


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
        """RE-ANCHORED (XASSET-0056) onto this unit's own closed merge; values retained."""
        assert _blob_at(BASE_SHA, AUTHORIZATION_MODULE_RELPATH) == AUTHORIZATION_MODULE_BLOB
        assert _blob_at(DECISION_MERGE_SHA, AUTHORIZATION_MODULE_RELPATH) == \
            AUTHORIZATION_MODULE_BLOB

    def test_the_authorization_module_blob_is_pinned_at_both_ends(self):
        """NEGATIVE PIN: the superseded live reading is bound too, so a silent revert fails."""
        assert _git("hash-object", AUTHORIZATION_MODULE_RELPATH).strip() != \
            AUTHORIZATION_MODULE_BLOB

    def test_the_authorization_module_content_hash_is_unchanged(self):
        """RE-ANCHORED (XASSET-0056) onto this unit's own closed merge; value retained."""
        assert _sha256_at(DECISION_MERGE_SHA, AUTHORIZATION_MODULE_RELPATH) == \
            AUTHORIZATION_MODULE_SHA256

    def test_the_authorization_module_content_hash_is_pinned_at_both_ends(self):
        """NEGATIVE PIN: the superseded live reading is bound too."""
        digest = hashlib.sha256((ROOT / AUTHORIZATION_MODULE_RELPATH).read_bytes()).hexdigest()
        assert digest != AUTHORIZATION_MODULE_SHA256

    def test_the_parser_still_has_its_uncorrected_contract(self):
        """RE-ANCHORED (XASSET-0056): non-vacuity, re-proved by executing this unit's bytes."""
        body = f"{DEFECTIVE_FORMAL_LINE}\n"
        assert _module_at(DECISION_MERGE_SHA).parse_formal_disposition(body) is None

    def test_the_parser_contract_is_corrected_by_the_authorized_successor(self):
        """NEGATIVE PIN: this filing authorized a correction that has since been performed."""
        body = f"{DEFECTIVE_FORMAL_LINE}\n"
        assert A.parse_formal_disposition(body) == A.APPROVING_REVIEW_DISPOSITION

    @pytest.mark.parametrize("relpath,digest", sorted(OUTCOME_CAPABLE_MODULE_WITNESS.items()))
    def test_every_outcome_capable_module_is_identical_to_the_bound_merge(self, relpath, digest):
        """RE-ANCHORED (XASSET-0056) onto this unit's own closed merge; both values retained.

        The bound-merge witness is unchanged. The live comparison moves to this unit's merge,
        where it is permanently true. The ONE module the authorized successor lawfully changes
        is `level1_stage1_execution_authorization.py`; every other outcome-capable module must
        STILL be byte-identical in the live tree, and that is asserted here rather than dropped.
        """
        assert _sha256_at(BOUND_MERGE_SHA, relpath) == digest
        assert _sha256_at(DECISION_MERGE_SHA, relpath) == digest
        live = hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest()
        if relpath == AUTHORIZATION_MODULE_RELPATH:
            assert live != digest  # NEGATIVE PIN: the authorized correction really landed
        else:
            assert live == digest

    def test_all_eighteen_load_bearing_paths_are_identical_to_the_bound_merge(self):
        """RE-ANCHORED (XASSET-0056) onto this unit's own closed merge; nothing dropped.

        Seventeen of the eighteen must STILL match in the live tree and are asserted to. The
        eighteenth -- the authorization module itself, LOAD_BEARING_RELPATHS[0] -- is the byte
        the authorized successor correction changes, and its live divergence is the designed
        fail-closed hand-off, pinned here as such rather than silently excused.
        """
        assert len(A.LOAD_BEARING_RELPATHS) == EXPECTED_LOAD_BEARING_COUNT
        assert len(set(A.LOAD_BEARING_RELPATHS)) == EXPECTED_LOAD_BEARING_COUNT
        for relpath in A.LOAD_BEARING_RELPATHS:
            at_bound = _blob_at(BOUND_MERGE_SHA, relpath)
            assert at_bound == _blob_at(DECISION_MERGE_SHA, relpath), relpath
            live = _git("hash-object", relpath).strip()
            if relpath == AUTHORIZATION_MODULE_RELPATH:
                assert live != at_bound, relpath  # NEGATIVE PIN: designed, authorized drift
            else:
                assert live == at_bound, relpath

    @pytest.mark.parametrize("relpath", PORTFOLIO_RELPATHS)
    def test_every_protected_portfolio_path_is_identical_to_the_bound_merge(self, relpath):
        assert _blob_at(BOUND_MERGE_SHA, relpath) == _git("hash-object", relpath).strip()

    @pytest.mark.parametrize("relpath,digest", sorted(CANONICAL_PINS.items()))
    def test_the_canonical_pins_match(self, relpath, digest):
        assert hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest() == digest

    def test_the_diff_against_the_base_touches_no_protected_or_load_bearing_path(self):
        """RE-ANCHORED (XASSET-0056): measured over THIS unit's own closed base..merge range.

        The live reading was correct while this unit was the live one. Now that it is merged and
        closed, the working tree also carries a lawfully authorized successor, so the live
        reading no longer measures THIS unit. The closed range does, exactly and permanently.
        """
        changed = set(_git("diff", "--name-only", BASE_SHA, DECISION_MERGE_SHA).split())
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
        """RE-ANCHORED (XASSET-0056). Whole-file check retained against this unit's own merge.

        In the live tree the identifier now appears, lawfully and ONLY as a comment citation
        inside the successor's authorized parser correction, following the module's own
        long-standing convention of citing its governing decisions. The operative property is
        asserted directly, and more precisely than a whole-file substring ever did.
        """
        assert DECISION_ID not in _git(
            "show", f"{DECISION_MERGE_SHA}:{AUTHORIZATION_MODULE_RELPATH}"
        )
        live = (ROOT / AUTHORIZATION_MODULE_RELPATH).read_text()
        tree = ast.parse(live)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                assert node.value != DECISION_ID
        for name in (
            "build_authorization_payload",
            "validate_authorization_document",
            "write_authorization",
            "new_execution_is_authorized",
            "active_execution_is_authorized",
        ):
            fn = next(
                n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name
            )
            assert DECISION_ID not in ast.get_source_segment(live, fn), name

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
        """RE-ANCHORED BY XASSET-0055 -- see `SUCCESSOR_BRANCH`. The shared live field moved
        onto the successor; this unit's own branch survives in the register as history, which
        is what this assertion was really protecting. Bound at BOTH ends."""
        assert ws0014["active_branch"] == SUCCESSOR_BRANCH
        assert ws0014["active_branch"] != XASSET0058_BRANCH
        assert ws0014["active_branch"] != XASSET0057_BRANCH
        assert ws0014["active_branch"] != BRANCH
        assert ws0014["active_branch"] != CLOSED_UNMERGED_BRANCH
        assert ws0014["active_branch"] != XASSET0055_BRANCH
        # This unit's own record in the register is its GATE, which does not move and still
        # carries this unit's own real pull-request number. The register does not store a
        # per-gate branch string, so that -- not the branch text -- is the durable anchor.
        gate = next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)
        assert gate["pr"] == THIS_PULL_REQUEST

    def test_the_last_verified_main_sha_advanced_and_is_bound_at_both_ends(self, ws0014):
        """RE-ANCHORED BY XASSET-0055 -- see `SUCCESSOR_MAIN_SHA`. This unit's own base joins
        the negative pins rather than being deleted, so the field stays bound at BOTH ends."""
        assert ws0014["last_verified_main_sha"] == SUCCESSOR_MAIN_SHA == XASSET0059_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0058_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0057_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0056_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0055_MAIN_SHA
        for finished in (
            BASE_SHA, XASSET0052_BASE, BOUND_MERGE_SHA, XASSET0052_ACCEPTED_HEAD,
            XASSET0055_MAIN_SHA,
        ):
            assert ws0014["last_verified_main_sha"] != finished, finished

    def test_the_active_pr_is_the_real_github_number_not_the_sentinel(self, ws0014):
        """RE-ANCHORED BY XASSET-0055. The shared live `active_pr` moved onto the successor, so
        it no longer names this unit. What this test actually protects -- that THIS unit's own
        number is the real one GitHub issued and never its sentinel -- is immutable history and
        is asserted here against this unit's OWN gate, which does not move."""
        gate = next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)
        assert gate["pr"] == THIS_PULL_REQUEST
        assert gate["pr"] != PR_SENTINEL, "the sentinel was never replaced"
        assert gate["pr"] not in PRIOR_SENTINELS
        assert gate["pr"] > BOUND_AUTHORIZING_PULL_REQUEST
        # The shared field has advanced off this unit and must not silently revert onto it.
        assert ws0014["active_pr"] != THIS_PULL_REQUEST

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

    def test_the_registers_gate_records_the_twenty_clause_boundary(self, ws0014):
        """The count is load-bearing: a stale count would understate the boundary."""
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert "twenty conjunctive clauses" in gate
        assert "eighteen conjunctive clauses" not in gate
        assert "fourteen conjunctive clauses" not in gate

    @pytest.mark.parametrize("fragment", (
        "SECOND BOUNDED CORRECTION",
        "INDEPENDENT FULL EXACT-HEAD REVIEW 5004478133",
        "FIRST COMPLETED FULL GitHub review",
        "INTERNALLY UNSATISFIABLE",
        "reproduced it at source and executably before widening anything",
        "frozenset({APPROVED})",
        "WIDENED BY THE SMALLEST AMOUNT THAT MAKES THE DISTINCTION EXPRESSIBLE AND NO MORE",
        "the permitted set is now stated ONCE AND EXHAUSTIVELY",
        "A GENERAL-PURPOSE PARSING FRAMEWORK",
        "EVERYTHING OUTSIDE THAT SET IS FORBIDDEN",
        "A WIDENED SURFACE IS A LARGER CORRECTION, NOT A LIGHTER ONE",
        "SEVEN END-TO-END PROOFS",
        "THIS CORRECTION IMPLEMENTS NO PARSER OR CONSUMER CHANGE",
    ))
    def test_the_registers_gate_records_the_major1_correction(self, ws0014, fragment):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert fragment in gate, fragment

    @pytest.mark.parametrize("fragment", (
        "DELTA review 5004859164 MINOR 1",
        "the permitted set is now stated ONCE AND EXHAUSTIVELY",
        "EXACTLY FOUR THINGS",
        "AT MOST ONE newly introduced narrow helper",
        "an option, not an entitlement",
        "ANY CHANGE TO ANY OTHER EXISTING PRODUCTION FUNCTION",
        "ABOUT EXISTING FUNCTIONS",
        "nothing in this list withdraws them",
        "ANY FOURTH parse_formal_disposition() CONSUMER OR CALL SITE",
        "MORE THAN ONE newly introduced helper",
        "A GENERAL-PURPOSE PARSING FRAMEWORK",
        "ANY UNRELATED PARSING, LIFECYCLE, REVIEW, EXECUTION, PORTFOLIO OR RISK CHANGE",
        "READ TOGETHER",
        "regression test binds the positive helper permission",
    ))
    def test_the_registers_gate_records_the_delta_correction(self, ws0014, fragment):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert fragment in gate, fragment

    def test_the_registers_gate_retires_the_self_contradicting_wording(self, ws0014):
        """DELTA review 5004859164 MINOR 1: the register must not still assert the retired scope."""
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert "the permitted surface is exactly three things" not in gate
        # It may only appear as the QUOTED retired wording being corrected, never as live scope.
        i = gate.find('"any function that is not one of the three named above"')
        assert i > 0, "the retired wording must be quoted as corrected, not silently dropped"
        assert "was self-contradicting" in gate

    @pytest.mark.parametrize("fragment", (
        "THIRD BOUNDED CORRECTION",
        "INDEPENDENT EXACT-HEAD DELTA REVIEW 5004859164",
        "0 BLOCKING / 0 MAJOR / 1 MINOR / 0 NOTE",
        "ONE RESIDUAL SCOPE CONTRADICTION",
        "PERMITTED AND PROHIBITED IN THE SAME SECTION",
        "EXACTLY FOUR THINGS",
        "AT MOST ONE newly introduced narrow helper",
        "ANY CHANGE TO ANY OTHER EXISTING PRODUCTION FUNCTION",
        "ANY FOURTH parse_formal_disposition() CONSUMER OR CALL SITE",
        "READ TOGETHER",
        "REGRESSION TEST binds the positive helper permission",
        "NO PARSER, REPRESENTATION, HELPER OR CONSUMER CHANGE IS IMPLEMENTED HERE",
    ))
    def test_both_operative_blocks_carry_the_delta_correction(self, ws0014, fragment):
        for field in ("next_action", "blocker"):
            assert fragment in _flat(ws0014[field]), (field, fragment)

    @pytest.mark.parametrize("consumer", (
        "_derive_pr337_actor_ratification",
        "verify_lifecycle_against_truth",
        "_verify_selected_review_is_final",
    ))
    def test_the_registers_gate_names_all_three_consumers(self, ws0014, consumer):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert consumer in gate, consumer

    @pytest.mark.parametrize("fragment", (
        "SECOND BOUNDED CORRECTION",
        "5004478133",
        "the FIRST completed FULL GitHub review on PR #354",
        "INTERNALLY UNSATISFIABLE",
        "None means BOTH ABSENT and MALFORMED/UNSUPPORTED",
        "widened by the smallest amount that makes the distinction expressible and no more",
        "every SS-D clause still binding",
        "seven end-to-end proofs through the real production path",
        "NO PARSER OR CONSUMER CHANGE IS IMPLEMENTED HERE",
    ))
    def test_both_operative_blocks_carry_the_major1_correction(self, ws0014, fragment):
        for field in ("next_action", "blocker"):
            assert fragment in _flat(ws0014[field]), (field, fragment)

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

    def test_no_yaml_fold_split_a_hyphenated_token_in_this_units_text(self, ws0014):
        """A folded block scalar turns a wrapped hyphenated word into 'END-TO- END'.

        Caught live while writing this correction, so it is pinned rather than remembered.
        """
        gate = next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"]
        texts = {"gate": gate}
        for field in ("next_action", "blocker"):
            texts[field] = ws0014[field].split("UPDATE, 2026-08-24")[-1]
        for name, text in texts.items():
            splits = re.findall(r"\w+- \w+", _flat(text))
            assert not splits, (name, splits)

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
        """RE-ANCHORED BY XASSET-0055. Successors append after this decision, so "last" is
        stated EXACTLY against the named successor set rather than relaxed to "present"."""
        ids = [d["decision_id"] for d in catalog]
        assert len(ids) == len(set(ids))
        assert ids.count(DECISION_ID) == 1
        assert ids[len(ids) - 1 - len(SUCCESSORS_APPENDED_SINCE)] == DECISION_ID
        assert tuple(ids[ids.index(DECISION_ID) + 1:]) == SUCCESSORS_APPENDED_SINCE

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
        # RE-ANCHORED BY XASSET-0055: successors append too, so the growth this unit itself
        # caused stays EXACT by naming them, rather than being relaxed to an inequality.
        assert len(catalog) == len(before) + 1 + len(SUCCESSORS_APPENDED_SINCE)
        assert DECISION_ID not in {d["decision_id"] for d in before}
        for successor in SUCCESSORS_APPENDED_SINCE:
            assert successor not in {d["decision_id"] for d in before}

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
