"""Adversarial tests pinning the ``XASSET-0051`` renewed link-4 / step-10 drift-check authorization.

``XASSET-0050``'s complete seven-condition lifecycle closed, its single authorized unit ran, and
that unit returned ``STEP_9_READINESS_VERIFICATION_PASS``. ``XASSET-0041`` §I **link 3** is
therefore discharged. **Link 4** is next, and it had **no authority**.

``XASSET-0039`` does not supply it, for two independent reasons either sufficient alone:

1. **Its grant is spent.** §A authorized "exactly one" step-10 unit; that unit ran and returned
   ``STEP_10_NO_DRIFT``, consumed as an input by ``XASSET-0040`` §C.
2. **Both of its anchors are dead.** §H required the PR #337 bound merge and the *old* step-9
   evidence, over **ten** load-bearing paths. ``XASSET-0042`` corrected load-bearing path #1,
   ``XASSET-0044`` amended both canonical artifacts, ``XASSET-0049`` rebound the boundary to
   **eighteen**, and ``XASSET-0050``'s own unit superseded that step-9 evidence.

**Six** filings after ``XASSET-0039`` named the renewed drift verification and all six declined to
grant it -- ``XASSET-0041``, ``XASSET-0043``, ``XASSET-0046``, ``XASSET-0048``, ``XASSET-0049``,
``XASSET-0050``. ``XASSET-0051`` closes that gap for the renewed drift check and nothing else.

The whole risk of an authorization filing is that it grants more than it says, or that a future
session reads more out of it than it contains. Every test below therefore pins **an authorized
boundary and its nearest plausible overreach** -- the stronger permission a successor might infer
from the same text, which the decision must refuse.

The overreaches that matter most each have a dedicated guard:

1. **The drift check performed now, or treated as authorized on filing.**
   ``TestTheDriftCheckIsNotPerformedHere`` and ``TestEffectivityRequiresCompleteLifecycleClosure``
   fail if the filing runs a comparison, issues a determination, or lets any single lifecycle step
   stand in for complete closure.
2. **Link 5 read as included.** ``TestLink5RetainsSeparateAuthority`` fails if it is granted,
   implied, or made reachable by a clean no-drift finding.
3. **``XASSET-0039`` treated as still live.** ``TestXasset0039IsSpentAndBothAnchorsAreDead`` fails
   if the filing revives it, or if the superseded anchor values are not pinned NEGATIVELY -- a
   silent reversion to the dead anchors must fail a test rather than pass unnoticed.
4. **The link-3 evidence misread.** ``TestTheLink3EvidenceOrdering`` fails if the later
   duplicate-exercise stop is treated as a determination, as an anchor, or as something that
   invalidates the earlier valid ``PASS``; ``TestLink3IsNotRerunOrReadjudicated`` fails if the
   filing or its unit may rerun or reopen link 3.
5. **One anchor quietly sufficing.** ``TestBothComparisonAnchorsAreMandatory`` fails if a
   one-anchor comparison is anywhere permitted, and pins both anchors' exact identities against
   values derived from the live object store.
6. **A restated constant governing over the tree.** ``TestIdentitiesAreDerivedFromTheBoundMerge``
   fails if the eighteen paths are not derived from ``a941455…``, or if any recorded pin drifts
   from its derived value.
7. **"Fail-closed" drifting into repair.** ``TestFailClosedStopReportChangeNothing`` and
   ``TestNoRepairNoRebindingNoRenewedReadiness`` fail if the authorized unit may create, edit,
   regenerate or correct anything, may declare a defect "fixed", or may continue past drift or
   uncertainty.
8. **A clean result read as permission.** ``TestNoDriftAuthorizesNothingFurther``.
9. **Arming by implication.** ``TestXasset0029NoRegressIntact`` fails if the filing presents itself
   as an activation PR, adds an activation authorization, or lets merge imply an armed Stage 1.
10. **Silent consumption of the reserved results PR.** ``TestP1ResultsPRRemainsSeparate``.
11. **The register's structured fields advancing while its operative prose goes stale.**
    ``TestTheRegistersOperativeProseAgreesWithItsStructuredFields`` isolates each field's LATEST
    dated block, because an assertion over the whole field would be satisfied by the stale text.
12. **The sentinel surviving into the merged record.** ``TestRegisterSynchronisation``.
13. **A protected or load-bearing path slipping into the diff.** ``TestNoProtectedPathIsTouched``
    compares every one of them, byte for byte, against the bound merge.

They also pin the negative space that makes the filing honest: this authorization PR changes no
canonical file, no validator, no authorization module, no runner, no result validator, and no
load-bearing byte; all eighteen load-bearing paths, both canonical pins, the frozen universe, and
the construction-universe module identity are untouched; ``REQUIRED_LIFECYCLE_GATES`` is still the
six-element tuple; and Stage 1 is still ``UNARMED`` with lane state ``ABSENT`` and ``ATTEMPT_1``
unclaimed.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No results document, lane directory, attestation, claim, completion, or ledger
entry is created or read for authorization purposes. No ``risk_lane_boundary`` protected result
path is read, listed, opened, or referenced.
"""

from __future__ import annotations

import ast
import hashlib
import re
import subprocess
from pathlib import Path

import pytest
import yaml

import level1_construction_universe_closure_validator as CU
import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------------------------
# RE-ANCHORED BY XASSET-0054, following the XASSET-0044 / XASSET-0043 precedent.
#
# XASSET-0053 SS-C lawfully authorized exactly ONE of the eighteen bound paths to change --
# `level1_stage1_execution_authorization.py` -- and XASSET-0054 exercised that single grant. The
# resulting digest drift is the DESIGNED fail-closed hand-off to the separately authorized
# step-8-equivalent rebinding unit, which alone may re-pin; it is not a defect and is not repaired
# here. For that ONE path this filing's "I did not touch it" guards are taken at XASSET-0053's own
# closed merge -- an immutable anchor, so the comparison cannot be made to pass by editing a file.
# Every OTHER path is still read LIVE from the worktree, so the trust boundary keeps its teeth for
# the remaining seventeen. Nothing is deleted, skipped, xfailed, or relaxed.
# ---------------------------------------------------------------------------------------------

XASSET_0053_MERGE_SHA = "683c324629544a84d2cf75ebca37325e3375c479"
AUTHORIZED_CORRECTION_RELPATH = "level1_stage1_execution_authorization.py"


def _xasset0054_reference_sha256(relpath: str) -> str:
    """The digest a "this filing did not touch it" guard must compare against. See the note above."""
    if str(relpath) == AUTHORIZED_CORRECTION_RELPATH:
        raw = subprocess.run(
            ["git", "show", f"{XASSET_0053_MERGE_SHA}:{relpath}"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout
        return hashlib.sha256(raw).hexdigest()
    return hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest()
GOV = ROOT / "governance/decisions"
PREREG = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"
PROTOCOL = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
WORKSTREAMS = ROOT / "operations/WORKSTREAMS.yaml"
CATALOG = ROOT / "governance/decisions.yaml"

DECISION_ID = "XASSET-0051"
DECISION = (
    GOV
    / "XASSET-0051-endpoint-0001-stage-1-renewed-drift-check-fail-closed-authorization.md"
)

D0027 = GOV / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
D0029 = GOV / "XASSET-0029-endpoint-0001-stage-1-operational-authorization.md"
D0030 = GOV / "XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md"
D0036 = GOV / "XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md"
D0039 = (
    GOV
    / "XASSET-0039-endpoint-0001-stage-1-post-rebinding-drift-fail-closed-authorization.md"
)
D0040 = (
    GOV / "XASSET-0040-endpoint-0001-stage-1-step-11-activation-and-execution-authorization.md"
)
D0041 = (
    GOV
    / "XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md"
)
D0043 = (
    GOV / "XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md"
)
D0046 = (
    GOV / "XASSET-0046-endpoint-0001-stage-1-post-merge-ci-recovery-reauthorization.md"
)
D0048 = GOV / "XASSET-0048-endpoint-0001-stage-1-step-8-equivalent-rebinding-authorization.md"
D0049 = (
    GOV
    / "XASSET-0049-endpoint-0001-stage-1-step-8-equivalent-successor-operational-rebinding.md"
)
D0050 = (
    GOV
    / "XASSET-0050-endpoint-0001-stage-1-renewed-readiness-verification-authorization.md"
)

# ---------------------------------------------------------------------------------------------
# ANCHOR 1 -- the effective XASSET-0049 bound merge. Verified live in preflight.
# ---------------------------------------------------------------------------------------------

BOUND_MERGE_SHA = "a941455491cc5e4d3d868775fb6b4b88f0fe2ce3"
BOUND_MERGE_PARENT_1 = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"
BOUND_MERGE_PARENT_2 = "b2059e80101fc6457f4004939d7d12886e6feedf"
BOUND_MERGE_TREE = "b7015b271362ae0c2fe663e8bfda9c6d10de5e7e"

# ---------------------------------------------------------------------------------------------
# ANCHOR 2 -- the successful RENEWED step-9 evidence, and the later duplicate-exercise stop.
# ---------------------------------------------------------------------------------------------

#: The valid FIRST and only exercise of XASSET-0050's one-shot authority.
LINK3_PASS_COMMENT = "5384453102"
LINK3_PASS_DETERMINATION = "STEP_9_READINESS_VERIFICATION_PASS"
LINK3_OBSERVATION_CHECKOUT = "ea9e74a1f4224a78df2416db9c872b0c5812894b"
LINK3_OBSERVATION_TREE = "e0ee2d4c25066cdc3d1c936015c3ada62bed74e8"

#: A LATER, separate concurrent session's correct fail-closed stop. Carries NO PASS, is NOT an
#: anchor, and does not invalidate the determination above. Pinned so it can never be promoted.
LINK3_DUPLICATE_STOP_COMMENT = "5384471997"

# ---------------------------------------------------------------------------------------------
# NEGATIVE pins. XASSET-0039's grant is spent and BOTH its anchors are dead; a silent reversion
# to any of them must FAIL rather than pass unnoticed.
# ---------------------------------------------------------------------------------------------

DEAD_MERGE_SHA = "637eaa30302f5a71f84ab1d215ecbd32c01399b5"
DEAD_STEP9_EVIDENCE_COMMENT = "5336643459"
DEAD_LOAD_BEARING_COUNT = 10
SPENT_STEP10_EVIDENCE_COMMENT = "5341448714"
SPENT_STEP10_DETERMINATION = "STEP_10_NO_DRIFT"

# ---------------------------------------------------------------------------------------------
# The pins the two anchors bind.
# ---------------------------------------------------------------------------------------------

EXPECTED_LOAD_BEARING_COUNT = 18

#: The five outcome-capable modules §F.3 names individually, recorded as the filing-time WITNESS.
#: §H.3 makes the value DERIVED from the bound merge tree operative; this table exists so a drift
#: between the two fails in CI instead of waiting to be noticed at verification time.
OUTCOME_CAPABLE_MODULE_WITNESS = {
    "level1_stage1_runner.py":
        "4a88cf6d0271da0dc3a6ca175fadb0223bf7ff8843479733cbcf0effd47ba5d9",
    "level1_stage1_result_validator.py":
        "b4773eb767158434136b72316e9802308b9e6fb47b6e45f8f10445c02cee3b7a",
    "level1_endpoint_evidence_preregistration_validator.py":
        "b3a87e4f8b828d420795348642c977a9f0585eafa9262a4be48df406f770233d",
    "level1_construction_universe_closure_validator.py":
        "1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5",
    "level1_stage1_execution_authorization.py":
        "4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541",
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

#: XASSET-0049's lawful rebinding, which this filing must not touch. REVIEWED_BASE_SHA is that
#: rebinding base -- NOT a "current main" field that advances with every merge.
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

#: An impossible sentinel, distinct from every sentinel used before (-1, -2, -50). Committed
#: first, then replaced by the number GitHub actually issued in a fast-forward follow-up commit.
#: RETAINED as a negative pin so a revert to the unbound state still fails.
PR_SENTINEL = -51
PRIOR_SENTINELS = (-1, -2, -50)

#: The number GitHub ISSUED for this unit, read back from the live API after the draft was opened.
#: Never predicted, never guessed.
THIS_PULL_REQUEST = 352

THIS_GATE = "xasset0051-renewed-drift-check-authorization"
PRIOR_UNIT_GATE = "xasset0050-renewed-readiness-verification-authorization"
PRIOR_CLOSURE_GATE = "xasset0050-post-merge-verification"


# ---------------------------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------------------------


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=True, text=True
    ).stdout.strip()


def _blob_sha256_at(relpath: str, rev: str = BOUND_MERGE_SHA) -> str:
    """SHA-256 of ``relpath`` as it exists in the git tree at ``rev``.

    Reading from an immutable commit rather than the worktree is what keeps these assertions
    anchored: a claim measured against a moving ref is the defect that stopped PRs #344 and #345.
    """
    blob = subprocess.run(
        ["git", "show", f"{rev}:{relpath}"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    return hashlib.sha256(blob).hexdigest()


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION.read_text()


@pytest.fixture(scope="module")
def ws0014() -> dict:
    data = yaml.safe_load(WORKSTREAMS.read_text())
    return next(w for w in data["workstreams"] if w["id"] == "WS-0014")


@pytest.fixture(scope="module")
def catalog() -> list:
    data = yaml.safe_load(CATALOG.read_text())
    return data["decisions"] if isinstance(data, dict) else data


def _flat(text: str) -> str:
    """Collapse runs of whitespace.

    The decision file is hard-wrapped at ~100 columns, so a multi-word phrase can fall across a
    line break. Normalizing means a phrase assertion tests the PROSE rather than where the
    wrapper happened to break it; `|` and other structural characters survive intact.
    """
    return " ".join(text.split())


def _flat_prose(text: str) -> str:
    """``_flat`` with markdown blockquote markers removed first.

    §A.1 states the canonical distinction as a blockquote so it can be lifted verbatim into a
    summary. Collapsing whitespace alone leaves the ``>`` markers embedded mid-sentence, which
    would make a prose assertion fail for a purely typographic reason.
    """
    stripped = "\n".join(re.sub(r"^\s*>\s?", "", line) for line in text.split("\n"))
    return _flat(stripped)


def _demphasize(text: str) -> str:
    """Strip markdown emphasis markers so a prose assertion tests words, not typography."""
    return text.replace("**", "").replace("`", "")


def _subsection(text: str, heading: str) -> str:
    """The whitespace-normalized body of one ``#### X`` subsection.

    ``_section`` matches ``### `` only; a subsection assertion scoped with it silently matches
    nothing and raises, which is how ``G.1`` was found to need its own accessor.
    """
    pattern = rf"^#### {re.escape(heading)}.*?(?=^#### |^### |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    assert match, f"subsection {heading!r} not found"
    return _flat(match.group(0))


def _section(text: str, heading: str) -> str:
    """The whitespace-normalized body of one ``### X.`` section.

    Scoping to one section is what stops a claim being satisfied by identical words elsewhere in
    the document.
    """
    pattern = rf"^### {re.escape(heading)}.*?(?=^### |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    assert match, f"section {heading!r} not found"
    return _flat(match.group(0))


# ---------------------------------------------------------------------------------------------


class TestTheFilingExistsAndIsWellFormed:
    def test_decision_file_exists_with_correct_frontmatter(self, decision_text):
        assert decision_text.startswith("---\n")
        front = yaml.safe_load(decision_text.split("---")[1])
        assert front["decision_id"] == DECISION_ID
        assert front["status"] == "Proposed"
        assert front["supporting_artifact"] == Path(__file__).name

    def test_catalog_carries_exactly_one_row_for_this_decision(self, catalog):
        rows = [r for r in catalog if r["decision_id"] == DECISION_ID]
        assert len(rows) == 1
        assert Path(ROOT / rows[0]["file"]).exists()

    def test_catalog_ids_remain_unique(self, catalog):
        ids = [r["decision_id"] for r in catalog]
        assert len(ids) == len(set(ids))

    def test_this_decision_is_a_unique_row_and_a_successor_is_newest(self, catalog):
        """RE-ANCHORED BY XASSET-0052.

        This was ``test_this_decision_is_the_newest_row``. The catalog is append-only, so "newest
        row" names whichever filing is most recent -- this one when the class was written, a
        successor now. Asserting it here would assert "no successor may ever be filed". What is
        preserved is the invariant that actually mattered: this decision has exactly one row, it
        is still present, and anything after it is a strictly LATER identifier rather than a
        reordering or a duplicate. The field stays bound at BOTH ends.
        """
        ids = [r["decision_id"] for r in catalog]
        assert ids.count(DECISION_ID) == 1
        idx = ids.index(DECISION_ID)
        for later in ids[idx + 1:]:
            assert later.startswith("XASSET-"), later
            assert int(later.split("-")[1]) > int(DECISION_ID.split("-")[1]), later

    def test_the_identifier_was_previously_unused(self, catalog):
        """The row this filing adds must be the ONLY occurrence anywhere in the catalog."""
        raw = CATALOG.read_text()
        assert raw.count(f"decision_id: {DECISION_ID}") == 1


class TestAuthorityGapIsGroundedInAcceptedText:
    """The gap must be shown from accepted text, never inferred from convenience."""

    def test_xasset0041_names_link_4_and_withholds_it(self):
        text = D0041.read_text()
        assert "renewed drift check" in text
        assert "step-10 equivalent, fail-closed" in text
        assert "None of links 2 through 5 is authorized" in text

    @pytest.mark.parametrize(
        "path,phrase",
        [
            (D0043, "any renewed readiness verification or renewed post-rebinding drift check"),
            (D0046, "perform renewed drift verification"),
            (D0048, "renewed drift verification (§G.B step 10 / link 4)"),
            (D0049, "renewed drift verification (`§G.B` step 10 / link 4)"),
        ],
    )
    def test_each_predecessor_withholds_the_renewed_drift_check_by_name(self, path, phrase):
        assert phrase in _flat(path.read_text()), path.name

    def test_xasset0050_withholds_link_4_and_forecloses_the_nearest_inference(self):
        flat = _flat(D0050.read_text())
        assert "retains its own separate-authority requirement" in flat
        assert "it is not a grant of link 4" in flat
        assert "authorizes nothing further" in flat

    def test_the_decision_reproduces_the_six_express_withholdings(self, decision_text):
        flat = _flat(decision_text)
        assert "**Six** filings after `XASSET-0039`" in flat
        assert "**all six** declined to grant it" in flat
        for named in ("XASSET-0041", "XASSET-0043", "XASSET-0046",
                      "XASSET-0048", "XASSET-0049", "XASSET-0050"):
            assert named in flat, named

    def test_the_cardinality_word_matches_the_enumeration(self, decision_text):
        """A mutation probe showed a bare phrase check survives 'six' becoming 'five' if only
        one of the two statements is edited. Both cardinality statements are bound."""
        flat = _flat(decision_text)
        assert "**Six** filings" in flat and "**all six** declined" in flat
        assert "**Five** filings" not in flat
        assert "**all five** declined" not in flat


class TestTheDriftCheckIsNotPerformedHere:
    """The single most important boundary: this filing AUTHORIZES, it does not PERFORM."""

    @pytest.mark.parametrize(
        "phrase",
        [
            "This decision performs no part of link 4",
            "runs no comparison, detects no drift",
            "consumes none of the authority it creates",
        ],
    )
    def test_the_determination_disclaims_performance(self, decision_text, phrase):
        assert phrase.lower() in _flat(decision_text).lower(), phrase

    def test_the_determination_is_an_authorization_not_a_finding(self, decision_text):
        section = _section(decision_text, "A.")
        assert "RENEWED_STEP_10_DRIFT_FAIL_CLOSED_AUTHORIZED" in section
        # The finding vocabulary a performed unit would use must NOT be asserted as an outcome.
        assert "issues no `STEP_10_NO_DRIFT` and no drift finding" in section

    def test_the_filing_issues_no_determination_anywhere(self, decision_text):
        """``STEP_10_NO_DRIFT`` may be DISCUSSED, but never asserted as this filing's outcome."""
        flat = _flat(decision_text)
        for forbidden in (
            "FORMAL DETERMINATION: STEP_10_NO_DRIFT",
            "this filing determines STEP_10_NO_DRIFT",
            "no drift was found",
        ):
            assert forbidden.lower() not in flat.lower(), forbidden

    def test_no_drift_comparison_artifact_is_created(self):
        """A performed unit would leave an artifact. None may exist."""
        assert not (ROOT / "stage1_results.yaml").exists()
        assert not list(ROOT.glob("**/step10_*.yaml"))
        assert not list(ROOT.glob("**/stage1_results.yaml"))


class TestTheCanonicalDistinctionIsStated:
    """``XASSET-0050``'s independent FULL review found a summary that both granted and denied its
    own link. §A.1 states the distinction verbatim so no summary of THIS filing can repeat it."""

    #: Phrases that would place link 4 on the withheld side of the line.
    FORBIDDEN_DENIALS = (
        "link 4, or link 5 is authorized",
        "links 4 and 5 remain separately unauthorized",
        "links 3, 4 and 5 remain separately unauthorized",
        "no readiness verification, drift verification",
        "neither performs nor authorizes links 4 or 5",
    )

    def test_the_decision_states_the_canonical_distinction(self, decision_text):
        assert "#### A.1" in decision_text
        flat = _flat_prose(decision_text)
        assert "authorizes** exactly one future, separate **link-4** fail-closed drift check" in flat
        assert "performs no part of it" in flat
        assert "neither performed nor authorized" in flat

    def test_the_decision_says_link_4_never_belongs_in_a_withheld_list(self, decision_text):
        flat = _flat(decision_text)
        assert 'Link 4 never belongs inside a "not authorized" list' in flat
        assert "It is the one thing this decision grants" in flat

    def test_the_decision_never_denies_the_link_4_authority(self, decision_text):
        flat = _flat(decision_text).lower()
        for phrase in self.FORBIDDEN_DENIALS:
            assert phrase.lower() not in flat, phrase

    def test_the_register_gate_carries_the_same_distinction(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)
        flat = _flat(gate["description"]).lower()
        assert "performs no part of that check" in flat
        assert "link 5" in flat and "neither performed nor authorized" in flat
        for phrase in self.FORBIDDEN_DENIALS:
            assert phrase.lower() not in flat, phrase


class TestXasset0039IsSpentAndBothAnchorsAreDead:
    def test_the_decision_records_the_spent_grant(self, decision_text):
        flat = _flat(decision_text)
        assert SPENT_STEP10_EVIDENCE_COMMENT in flat
        assert SPENT_STEP10_DETERMINATION in flat
        assert "its one\n   authorized unit is consumed" in decision_text or \
               "its one authorized unit is consumed" in flat

    def test_the_decision_records_both_dead_anchors_negatively(self, decision_text):
        flat = _flat(decision_text)
        assert DEAD_MERGE_SHA in flat
        assert DEAD_STEP9_EVIDENCE_COMMENT in flat
        assert "**Neither\n   `XASSET-0039` anchor still describes this system.**" in decision_text \
            or "Neither `XASSET-0039` anchor still describes this system" in flat

    def test_the_dead_anchors_are_not_the_live_ones(self):
        assert DEAD_MERGE_SHA != BOUND_MERGE_SHA
        assert DEAD_STEP9_EVIDENCE_COMMENT != LINK3_PASS_COMMENT
        assert DEAD_LOAD_BEARING_COUNT != EXPECTED_LOAD_BEARING_COUNT

    def test_the_decision_does_not_revive_any_spent_authority(self, decision_text):
        section = _section(decision_text, "B.")
        assert "is **not** reopened, extended, amended, revived, or re-scoped" in section
        assert "its spent grant is not restored" in section
        for spent in ("XASSET-0038", "XASSET-0040"):
            assert spent in section, spent
        assert "None is revived" in section

    def test_xasset0039_really_did_authorize_exactly_one_unit(self):
        """Non-vacuity: the 'spent' claim rests on the predecessor's own accepted text."""
        flat = _flat(D0039.read_text())
        assert "**Exactly one** future, separate, bounded `XASSET-0030` §G.B **step-10** unit" in flat

    def test_xasset0040_records_the_step10_unit_as_consumed(self):
        flat = _flat(D0040.read_text())
        assert SPENT_STEP10_EVIDENCE_COMMENT in flat
        assert "its one\nauthorized unit is consumed" in D0040.read_text() or \
               "its one authorized unit is consumed" in flat


class TestTheLink3EvidenceOrdering:
    """Two comments bear on link 3. Their order is load-bearing, and the later one is NOT a
    determination. A future reader must never be able to promote it into one."""

    @staticmethod
    def _ordering_table_rows(decision_text: str) -> dict[str, str]:
        """The §C.1 ordering table, keyed by its own row number.

        A mutation probe (P3) proved that comparing FIRST-OCCURRENCE positions across the whole
        of §C was vacuous: the prose above the table already names the PASS first, so swapping
        the two table rows left the ordering assertion passing. The rows themselves are bound
        here, so a swap fails.
        """
        rows = {}
        for line in decision_text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("| 1 |") or stripped.startswith("| 2 |"):
                rows[stripped[2]] = stripped
        return rows

    def test_the_decision_records_both_comments_in_order(self, decision_text):
        section = _section(decision_text, "C.")
        assert LINK3_PASS_COMMENT in section
        assert LINK3_DUPLICATE_STOP_COMMENT in section
        assert section.index(LINK3_PASS_COMMENT) < section.index(LINK3_DUPLICATE_STOP_COMMENT)

    def test_the_ordering_table_binds_each_comment_to_its_own_row(self, decision_text):
        rows = self._ordering_table_rows(decision_text)
        assert set(rows) == {"1", "2"}, sorted(rows)
        assert LINK3_PASS_COMMENT in rows["1"], rows["1"]
        assert LINK3_DUPLICATE_STOP_COMMENT not in rows["1"], rows["1"]
        assert LINK3_DUPLICATE_STOP_COMMENT in rows["2"], rows["2"]
        assert LINK3_PASS_COMMENT not in rows["2"], rows["2"]

    def test_the_ordering_table_binds_each_row_to_its_own_determination(self, decision_text):
        rows = self._ordering_table_rows(decision_text)
        assert "05:40:46Z" in rows["1"] and "05:46:28Z" in rows["2"]
        assert LINK3_PASS_DETERMINATION in rows["1"]
        assert "NO PASS ISSUED" in rows["2"]
        assert LINK3_PASS_DETERMINATION not in rows["2"]

    def test_the_first_comment_is_named_the_operative_pass(self, decision_text):
        section = _section(decision_text, "C.")
        assert "valid first and only exercise" in section
        assert LINK3_PASS_DETERMINATION in section
        assert "operative renewed step-9 `PASS`" in section

    def test_the_second_comment_is_named_a_stop_and_carries_no_pass(self, decision_text):
        section = _section(decision_text, "C.")
        assert "NO PASS ISSUED" in section
        assert "fail-closed stop" in section.lower()
        assert "duplicate-exercise stop evidence" in section

    def test_the_second_comment_does_not_invalidate_the_first(self, decision_text):
        section = _section(decision_text, "C.")
        assert "does not invalidate, supersede, contradict, or weaken comment" in section

    def test_the_second_comment_is_explicitly_not_an_anchor(self, decision_text):
        anchors = _section(decision_text, "H.")
        assert f"Comment `{LINK3_DUPLICATE_STOP_COMMENT}` is not an anchor" in anchors
        assert "must not be substituted for, blended with, or weighed against" in anchors

    def test_the_stop_is_never_treated_as_a_second_pass(self, decision_text):
        """The nearest plausible overreach: reading the stop's clean C1-C10 observations as
        corroborating evidence. Its own text disclaims that, and so must this filing."""
        flat = _demphasize(_flat(decision_text)).lower()
        assert 'carrying "no authority whatsoever' in flat
        assert '"factual observations only"' in flat
        assert "is not a readiness determination" in flat
        # The reading is NAMED and REJECTED in Alternatives Considered, so a blunt "the words
        # never appear" check would fail on correct text. What must never appear is an
        # AFFIRMATIVE construction treating the stop as a determination.
        assert "as a second pass" in flat, "the overreach is not even named"
        assert "it disclaims that reading itself" in flat
        for forbidden in (
            f"{LINK3_DUPLICATE_STOP_COMMENT} corroborates",
            "is a second pass",
            "constitutes a second pass",
            "issues a second pass",
            "two passes",
            "two valid determinations",
            "both determinations stand",
        ):
            assert forbidden not in flat, forbidden
        # The Rationale raises the same overreach and refuses it in the same breath; that
        # refusal is the operative text, and its absence would leave the mention unanswered.
        assert "corroborating pass. they are not, by their own terms" in flat

    def test_the_register_records_the_same_ordering(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == PRIOR_CLOSURE_GATE)
        desc = _flat(gate["description"])
        assert LINK3_PASS_COMMENT in desc and LINK3_DUPLICATE_STOP_COMMENT in desc
        assert desc.index(LINK3_PASS_COMMENT) < desc.index(LINK3_DUPLICATE_STOP_COMMENT)
        assert "DOES NOT invalidate" in desc


class TestLink3IsNotRerunOrReadjudicated:
    def test_the_withholding_bars_rerunning_link_3(self, decision_text):
        section = _section(decision_text, "G.")
        assert "**rerun link 3 / step 9**" in section
        assert "reopen, re-adjudicate, or overturn" in section
        assert LINK3_PASS_COMMENT in section

    def test_the_no_repair_section_bars_rerunning_to_clear_a_finding(self, decision_text):
        section = _section(decision_text, "J.")
        assert "rerun link 3 / step 9 to \"clear\" what it found" in section

    def test_the_filing_does_not_re_perform_link_3(self, decision_text):
        section = _section(decision_text, "C.")
        assert "re-performs no part of it" in section
        assert "does not re-run the C1–C11 checklist" in section
        assert "**Link 3 is complete and closed**" in section

    def test_no_renewed_link_3_authority_is_created(self, decision_text):
        section = _section(decision_text, "C.")
        assert "`XASSET-0050` is spent" in section
        assert "No renewed link-3\n  authority is required, and none is created here." in \
            DECISION.read_text() or "none is created here" in section


class TestBothComparisonAnchorsAreMandatory:
    def test_the_section_requires_both_and_fails_on_one(self, decision_text):
        section = _section(decision_text, "H.")
        assert "must compare all 18 current bound paths against **both**" in section
        assert "**A comparison against only one must fail**" in section
        assert "it is a failure of the step, not a partial success" in section

    def test_anchor_1_records_the_exact_bound_merge_identity(self, decision_text):
        section = _section(decision_text, "H.")
        for value in (BOUND_MERGE_SHA, BOUND_MERGE_PARENT_1,
                      BOUND_MERGE_PARENT_2, BOUND_MERGE_TREE):
            assert value in section, value
        assert "third parent | **none**" in section

    def test_anchor_2_records_the_exact_renewed_evidence_identity(self, decision_text):
        section = _section(decision_text, "H.")
        for value in (LINK3_PASS_COMMENT, LINK3_PASS_DETERMINATION,
                      LINK3_OBSERVATION_CHECKOUT, LINK3_OBSERVATION_TREE):
            assert value in section, value
        assert "C1–C11 `PASS`" in section

    def test_anchor_2_must_be_read_live_not_taken_from_this_record(self, decision_text):
        section = _section(decision_text, "H.")
        assert "must independently read the\nlive comment" in DECISION.read_text() or \
            "must independently read the live comment" in section
        assert "is context, not evidence" in section

    def test_the_two_anchors_are_stated_to_be_non_redundant(self, decision_text):
        section = _section(decision_text, "H.")
        assert "The two anchors are not redundant" in section
        assert "**Drift against either anchor is drift.**" in section

    def test_anchor_1_matches_the_live_object_store(self):
        """Non-vacuity: the recorded anchor is checked against git, not merely restated."""
        parents = _git("rev-list", "--parents", "-n", "1", BOUND_MERGE_SHA).split()
        assert parents[0] == BOUND_MERGE_SHA
        assert parents[1:] == [BOUND_MERGE_PARENT_1, BOUND_MERGE_PARENT_2]
        assert len(parents) == 3, "a third parent appeared"
        assert _git("rev-parse", f"{BOUND_MERGE_SHA}^{{tree}}") == BOUND_MERGE_TREE

    def test_anchor_1_is_an_ancestor_of_the_current_checkout(self):
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", BOUND_MERGE_SHA, "HEAD"],
            cwd=ROOT, check=True,
        )


class TestIdentitiesAreDerivedFromTheBoundMerge:
    def test_the_boundary_is_exactly_eighteen_unique_paths(self):
        paths = list(A.LOAD_BEARING_RELPATHS)
        assert len(paths) == EXPECTED_LOAD_BEARING_COUNT
        assert len(set(paths)) == EXPECTED_LOAD_BEARING_COUNT

    @pytest.mark.parametrize("relpath", sorted(A.LOAD_BEARING_RELPATHS))
    def test_every_bound_path_is_byte_identical_to_the_bound_merge(self, relpath):
        derived = _blob_sha256_at(relpath)
        current = _xasset0054_reference_sha256(relpath)
        assert current == derived, relpath

    def test_the_decision_requires_derivation_rather_than_restatement(self, decision_text):
        section = _section(decision_text, "H.")
        assert "derived from this\nimmutable git tree at verification time" in DECISION.read_text() \
            or "derived from this immutable git tree at verification time" in section
        assert "never governed by the constants restated above" in section

    def test_where_a_restated_constant_disagrees_the_derived_value_governs(self, decision_text):
        section = _section(decision_text, "H.")
        assert "the derived value governs" in section
        assert "the disagreement is itself a §I stop" in section

    @pytest.mark.parametrize("relpath,expected", sorted(OUTCOME_CAPABLE_MODULE_WITNESS.items()))
    def test_each_outcome_capable_module_witness_matches_the_derived_value(self, relpath, expected):
        assert _blob_sha256_at(relpath) == expected, relpath

    @pytest.mark.parametrize("relpath,expected", sorted(CANONICAL_PINS.items()))
    def test_each_canonical_pin_matches_the_derived_value(self, relpath, expected):
        assert _blob_sha256_at(relpath) == expected, relpath
        assert hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest() == expected, relpath

    def test_the_five_outcome_capable_modules_are_inside_the_boundary(self):
        for relpath in OUTCOME_CAPABLE_MODULE_WITNESS:
            assert relpath in A.LOAD_BEARING_RELPATHS, relpath

    def test_the_decision_names_the_five_outcome_capable_modules(self, decision_text):
        section = _section(decision_text, "F.")
        for label in ("runner", "result validator", "preregistration derivation module",
                      "construction-universe module", "execution-authorization module"):
            assert label in section, label


class TestFilingTimeBytesAreUnchanged:
    """This is a governance filing. It must move no production byte."""

    def test_the_authorization_module_is_byte_identical_to_the_bound_merge(self):
        assert _blob_sha256_at("level1_stage1_execution_authorization.py") == \
            OUTCOME_CAPABLE_MODULE_WITNESS["level1_stage1_execution_authorization.py"]
        assert _xasset0054_reference_sha256("level1_stage1_execution_authorization.py") == \
            OUTCOME_CAPABLE_MODULE_WITNESS["level1_stage1_execution_authorization.py"]

    def test_the_module_constants_are_untouched(self):
        assert A.AUTHORIZING_DECISION == BOUND_AUTHORIZING_DECISION
        assert A.AUTHORIZING_PULL_REQUEST == BOUND_AUTHORIZING_PULL_REQUEST
        assert A.REVIEWED_BASE_SHA == BOUND_REVIEWED_BASE_SHA
        assert tuple(A.REQUIRED_LIFECYCLE_GATES) == EXPECTED_LIFECYCLE_GATES

    def test_the_frozen_universe_is_untouched(self):
        universe = CU.frozen_construction_universe()
        assert len(universe) == CONSTRUCTION_COUNT == A.CONSTRUCTION_COUNT
        assert len({e["cell_id"] for e in universe.values()}) == CELL_COUNT == \
            A.CONSTRUCTION_CELL_COUNT
        assert A.CONSTRUCTION_UNIVERSE_SHA256 == UNIVERSE_SHA
        assert CU.universe_aggregate_sha256() == UNIVERSE_SHA

    def test_no_gate_is_evaluated_by_this_module(self):
        """Traversal is authorized; gate evaluation is not.

        Bound structurally rather than by substring: the runner is NAMED here as one of the five
        outcome-capable modules whose identity is pinned, which is a read of its bytes and not a
        call into it. What must never appear is an IMPORT of it or a call to its entry point.
        """
        tree = ast.parse(Path(__file__).read_text())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        assert "level1_stage1_runner" not in imported
        called = {
            n.func.id for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        } | {
            n.func.attr for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
        }
        for forbidden in ("run_stage1", "evaluate_gate", "evaluate_gates"):
            assert forbidden not in called, forbidden


class TestNoProtectedPathIsTouched:
    PROTECTED = (
        "allocate.py",
        "margin_state.py",
        "levels.py",
        "targets.yaml",
        "holdings.yaml",
        "gates.yaml",
        "issuer_lookthrough.yaml",
    )

    @pytest.mark.parametrize("relpath", PROTECTED)
    def test_each_protected_path_is_byte_identical_to_the_bound_merge(self, relpath):
        assert hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest() == \
            _blob_sha256_at(relpath), relpath

    def test_no_protected_or_load_bearing_path_appears_in_this_units_diff(self):
        """The operative scope check: whatever this branch changed, it changed none of them."""
        changed = set(
            _git("diff", "--name-only", BOUND_MERGE_SHA, "HEAD").split("\n")
        ) - {""}
        forbidden = set(self.PROTECTED) | set(A.LOAD_BEARING_RELPATHS)
        assert not (changed & forbidden), sorted(changed & forbidden)


class TestFailClosedStopReportChangeNothing:
    @pytest.mark.parametrize(
        "phrase",
        [
            "**stop** — not continue to the remaining comparisons as though the condition were minor",
            "**report** the exact condition in its externally posted evidence",
            "**change nothing** — the prohibition in §G is not relaxed by the discovery of a defect",
            "**not** issue a `STEP_10_NO_DRIFT` determination, and **not** permit `READY` or claim",
        ],
    )
    def test_each_fail_closed_step_is_operative(self, decision_text, phrase):
        assert phrase in _section(decision_text, "I."), phrase

    def test_uncertainty_is_failure(self, decision_text):
        section = _section(decision_text, "I.")
        assert "**Uncertainty is failure.**" in section
        assert "may not resolve an ambiguous state in favour of no-drift" in section

    def test_missing_evidence_is_a_stop_condition(self, decision_text):
        section = _section(decision_text, "I.")
        assert "missing evidence" in section


class TestNoRepairNoRebindingNoRenewedReadiness:
    def test_the_unit_is_a_detector_and_a_refusal(self, decision_text):
        section = _section(decision_text, "J.")
        assert "**detector and a refusal**, never a remediator" in section

    #: Each remediation, as it appears verbatim in the §J prohibition list.
    BARRED = (
        "- correct, revert, regenerate, or re-pin the drifted byte;",
        "- rebind the drifted path, or perform any part of a rebinding;",
        '- rerun link 3 / step 9 to "clear" what it found.',
    )

    @staticmethod
    def _prohibition_block(decision_text: str) -> str:
        """The §J bullet list, TOGETHER WITH the clause that governs it.

        A mutation probe (P9) proved that asserting each bullet's words are present is vacuous:
        prefixing "it may " to a bullet leaves every asserted substring intact while inverting
        its meaning. The block is therefore extracted from its governing "it **must not**:" and
        each bullet is bound as a WHOLE LINE inside it.
        """
        body = re.search(r"^### J\..*?(?=^### |\Z)", decision_text, re.M | re.S).group(0)
        lead = "defect, it **must not**:"
        assert lead in body, "the §J prohibition list lost its governing clause"
        after = body.split(lead, 1)[1]
        return after.split("\n\nInstead", 1)[0]

    @pytest.mark.parametrize("bullet", BARRED)
    def test_each_remediation_is_barred(self, decision_text, bullet):
        block = self._prohibition_block(decision_text)
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        assert bullet in lines, (bullet, lines)

    def test_no_permissive_construction_appears_in_the_prohibition_block(self, decision_text):
        block = _flat(self._prohibition_block(decision_text)).lower()
        for permissive in ("it may ", "is permitted", "may correct", "may rebind", "may rerun"):
            assert permissive not in block, permissive

    def test_remediation_requires_three_separately_authorized_things(self, decision_text):
        section = _section(decision_text, "J.")
        assert "**three separately authorized\nthings**" in DECISION.read_text() or \
            "three separately authorized things" in section
        assert "a **separately authorized correction**" in section
        assert "a **separately authorized rebinding**" in section
        assert "any **renewed readiness verification**" in section

    def test_discovery_is_not_authorization(self, decision_text):
        section = _section(decision_text, "J.")
        assert "**Discovery is not authorization." in section
        assert "Finding the work is not authority to\ndo the work.**" in DECISION.read_text() or \
            "Finding the work is not authority to do the work" in section

    def test_the_withholding_bars_repair_in_passing(self, decision_text):
        section = _section(decision_text, "G.")
        assert "**declare any defect \"fixed\"**, or repair one in passing" in section
        assert "never work to perform" in section


class TestNoDriftAuthorizesNothingFurther:
    def test_a_clean_result_is_evidence_not_permission(self, decision_text):
        section = _section(decision_text, "K.")
        assert "**A clean `STEP_10_NO_DRIFT` determination must explicitly authorize nothing further.**" \
            in section
        assert "It is evidence that the bound bytes are still the bound bytes" in section

    @pytest.mark.parametrize(
        "phrase",
        [
            "permission to produce an attestation",
            "permission to arm Stage 1, to reach `READY`, or to claim `ATTEMPT_1`",
            "permission to execute the 680-construction run",
            "a substitute for link 5's own separate authority",
        ],
    )
    def test_each_thing_a_clean_result_is_not(self, decision_text, phrase):
        assert phrase in _section(decision_text, "K."), phrase

    def test_the_unit_must_say_so_in_its_own_evidence(self, decision_text):
        section = _section(decision_text, "K.")
        assert "The unit's own posted evidence must say so in terms" in section


class TestLink5RetainsSeparateAuthority:
    def test_link_5_is_entirely_outside_this_filing(self, decision_text):
        section = _section(decision_text, "L.")
        assert "retains its own separate-authority requirement\nand is entirely outside this filing" \
            in DECISION.read_text() or \
            "retains its own separate-authority requirement and is entirely outside this filing" \
            in section

    def test_link_5_is_not_reachable_by_a_clean_result_or_by_merge(self, decision_text):
        section = _section(decision_text, "L.")
        assert "is not made reachable by a clean link-4 result" in section
        assert "not made reachable by this decision's own merge" in section

    def test_xasset0040_stays_spent_as_a_stop(self, decision_text):
        section = _section(decision_text, "L.")
        assert "stays **spent as a\nstop**" in DECISION.read_text() or \
            "stays **spent as a stop**" in section
        assert "is not revived" in section

    def test_the_stop_rule_is_not_a_grant_of_link_5(self, decision_text):
        section = _section(decision_text, "L.")
        assert "neither is a grant of link 5" in section

    def test_the_withholding_bars_performing_or_authorizing_link_5(self, decision_text):
        section = _section(decision_text, "G.")
        assert "**perform or authorize `XASSET-0041` §I link 5" in section
        assert "step 11 — in any part.**" in section


class TestXasset0029NoRegressIntact:
    @pytest.mark.parametrize(
        "phrase",
        [
            "generates **no** attestation and authorizes none",
            "adds **zero** activation authorizations",
            "leaves `stage_1_executability.executable` permanently `false`",
        ],
    )
    def test_each_no_regress_clause_is_present(self, decision_text, phrase):
        assert phrase in _section(decision_text, "E."), phrase

    def test_merging_does_not_arm_stage_1(self, decision_text):
        section = _section(decision_text, "E.")
        assert "**No committed value in this repository authorizes Stage-1 execution**" in section
        assert "it does not make Stage 1 armed or executable" in section

    def test_final_activation_remains_the_external_attestation(self, decision_text):
        section = _section(decision_text, "E.")
        assert "the\nexternal one-shot runtime attestation and the operator's act" in \
            DECISION.read_text() or \
            "external one-shot runtime attestation and the operator's act" in section
        assert "not a merged activation PR" in section


class TestP1ResultsPRRemainsSeparate:
    def test_p1_remains_one_unspent(self, decision_text):
        section = _section(decision_text, "D.")
        assert "**one, unspent**" in section

    @pytest.mark.parametrize(
        "phrase",
        [
            "produces **no result of any kind**",
            "sits **after arming**",
            "makes **no repository\nchange at all**",
        ],
    )
    def test_each_independent_ground_is_recorded(self, phrase):
        text = DECISION.read_text()
        assert phrase in text or _flat(phrase) in _flat(text), phrase


class TestReadOnlyMeansReadOnly:
    def test_the_xasset0036_line_is_reused_not_widened(self, decision_text):
        section = _subsection(decision_text, "G.1")
        assert "traversing frozen construction\nidentities is not execution" in DECISION.read_text() \
            or "traversing frozen construction identities is not execution" in section
        assert "That line is adopted here unchanged" in section

    def test_a_real_stage_1_run_remains_absolutely_prohibited(self, decision_text):
        section = _subsection(decision_text, "G.1")
        assert "**An actual Stage-1 run over the real 680 remains absolutely prohibited**" in section

    def test_traversal_is_granted_without_gate_evaluation(self, decision_text):
        section = _section(decision_text, "F.")
        assert "**No gate may be evaluated.**" in section

    def test_the_unit_may_write_nothing_at_all(self, decision_text):
        section = _subsection(decision_text, "G.1")
        assert "permitted to write nothing at all" in section


class TestEffectivityRequiresCompleteLifecycleClosure:
    REQUIRED = (
        "independent **FULL** exact-head review under `OPS-0007` §1",
        "any required bounded correction and exact-head re-review",
        "explicit principal exact-head acceptance at that final head",
        "normal merge",
        "immediate post-merge verification",
        "**successful merge-commit CI whose `head_sha` is the exact merge SHA**",
        "final post-CI verification and lifecycle closure",
    )

    @pytest.mark.parametrize("phrase", REQUIRED)
    def test_each_of_the_seven_conditions_is_present(self, decision_text, phrase):
        assert phrase in _section(decision_text, "N."), phrase

    def test_no_condition_is_individually_sufficient(self, decision_text):
        section = _section(decision_text, "N.")
        assert "**None is individually sufficient.**" in section
        for insufficient in (
            "Opening this PR authorizes nothing",
            "a green PR-head CI run does\nnot",
            "principal acceptance does not",
            "merge does not",
        ):
            assert insufficient in section or _flat(insufficient) in section, insufficient

    def test_the_seven_conditions_are_numbered_one_through_seven(self, decision_text):
        body = re.search(r"^### N\..*?(?=^### |\Z)", decision_text, re.M | re.S).group(0)
        for n in range(1, 8):
            assert f"\n{n}. " in body, n
        assert "\n8. " not in body

    def test_even_complete_closure_authorizes_only_a_check(self, decision_text):
        section = _section(decision_text, "N.")
        assert "what\nbecomes authorized is a **fail-closed drift check**, never arming and never execution" \
            in DECISION.read_text() or \
            "becomes authorized is a **fail-closed drift check**, never arming and never execution" \
            in section


class TestStage1RemainsUnarmed:
    def test_lane_state_is_absent(self):
        state, _ = A.lane_state_at(A.LanePaths())
        assert state == A.LANE_ABSENT

    def test_no_lane_artifact_exists(self):
        assert not A.AUTHORIZATION_ROOT.exists()
        lp = A.LanePaths()
        for path in (lp.authorization, lp.claim, lp.completion, lp.ledger):
            assert not path.exists(), path

    def test_new_execution_is_not_authorized(self):
        authorized, _ = A.new_execution_is_authorized()
        assert authorized is False

    def test_active_execution_is_not_authorized(self):
        authorized, _ = A.active_execution_is_authorized()
        assert authorized is False

    def test_executable_is_false_in_the_canonical_artifact(self):
        prereg = yaml.safe_load(PREREG.read_text())
        assert prereg["stage_1_executability"]["executable"] is False

    def test_attempt_1_is_intact_and_unconsumed(self):
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"
        assert not (ROOT / "stage1_results.yaml").exists()

    def test_the_decision_states_the_posture(self, decision_text):
        flat = _flat(decision_text)
        assert "**Stage 1 remains UNARMED and NOT EXECUTABLE." in flat
        assert "`ATTEMPT_1` is intact, unclaimed, and unconsumed.**" in flat


class TestAbsoluteNonAuthorization:
    @pytest.mark.parametrize(
        "phrase",
        [
            "generates no attestation",
            "creates no `AUTHORIZATION_ROOT`",
            "performs no part of `XASSET-0041` §I link 4",
            "neither performs nor authorizes link 5",
            "re-adjudicates neither comment `5384453102` nor its\nC1–C11 determination",
            "consumes nothing\nof `ATTEMPT_1`",
            "rewrites no accepted history",
        ],
    )
    def test_each_non_authorization_clause_is_present(self, decision_text, phrase):
        section = _section(decision_text, "O.")
        assert phrase in section or _flat(phrase) in section, phrase

    def test_the_section_is_read_against_a_1(self, decision_text):
        section = _section(decision_text, "O.")
        assert "**Read this section against §A.1.**" in section
        assert "link 4 is authorized and unperformed; link 5 is neither" in section


class TestTheRegistersOperativeProseAgreesWithItsStructuredFields:
    """``next_action`` and ``blocker`` are APPEND-ONLY dated logs.

    An assertion over the whole field would be satisfied by the stale text and would therefore be
    vacuous. Each test isolates the LATEST dated block; a companion test proves the older prose
    survives and that the fields really are multi-block logs, so the isolation cannot silently
    degrade into a whole-field test.
    """

    UPDATE_MARKER = "UPDATE, 2026-08-23"

    #: THIS unit's own dated block, isolated by its opening phrase. A successor filed on the SAME
    #: calendar date shares the marker, so the date alone no longer identifies whose block it is.
    OWN_BLOCK_OPENING = "UPDATE, 2026-08-23 (post-XASSET-0050 merge and post-link-3 PASS"

    @classmethod
    def _latest_update(cls, field_text: str) -> str:
        assert cls.UPDATE_MARKER in field_text, "the field carries no dated update at all"
        return cls.UPDATE_MARKER + field_text.rsplit(cls.UPDATE_MARKER, 1)[1]

    @classmethod
    def _own_update(cls, field_text: str) -> str:
        """THIS unit's own dated block.

        RE-ANCHORED BY XASSET-0052. These fields are append-only, so "the latest block" names
        whichever unit is currently live -- which was this one when the class was written and is
        a successor now. Re-pointing the own-content checks at this unit's OWN block preserves
        each assertion in kind: it still verifies that what THIS unit wrote is present, correct
        and unrewritten. Whether the *newest* block correctly supersedes it is checked separately
        in ``TestTheNewestBlockSupersedesThisUnit``, so the field ends up bound at BOTH ends
        rather than at neither.
        """
        assert cls.OWN_BLOCK_OPENING in field_text, "this unit's own dated block is missing"
        tail = cls.OWN_BLOCK_OPENING + field_text.split(cls.OWN_BLOCK_OPENING, 1)[1]
        nxt = tail.find(cls.UPDATE_MARKER, len(cls.OWN_BLOCK_OPENING))
        return tail if nxt == -1 else tail[:nxt]

    def test_the_fields_really_are_append_only_dated_logs(self, ws0014):
        for field in ("next_action", "blocker"):
            text = ws0014[field]
            assert text.count("UPDATE, ") >= 2, field
            assert len(self._latest_update(text)) < len(text), field

    def test_the_older_dated_prose_survives(self, ws0014):
        for field in ("next_action", "blocker"):
            assert "UPDATE, 2026-08-22" in ws0014[field], field

    #: The active-lane claim, as it appears in both fields.
    CLAIM = "SOLE ACTIVE GOVERNANCE LANE"

    @classmethod
    def _claim_occurrences(cls, latest: str) -> list[tuple[int, str]]:
        """Every occurrence of the active-lane claim, with the 240 characters preceding it.

        The latest block deliberately QUOTES the superseded claim in order to mark it superseded,
        so a naive "the nearest sentence must name this unit" heuristic reads the quotation and
        fails on correct text -- which is exactly what the first draft of this guard did. Each
        occurrence is classified instead: one attributed to a finished unit inside the
        superseded-by-event quotation is history; any other occurrence is OPERATIVE and must
        name this unit.
        """
        flat = _flat(latest)
        out, idx = [], flat.find(cls.CLAIM)
        while idx != -1:
            out.append((idx, flat[max(0, idx - 240): idx]))
            idx = flat.find(cls.CLAIM, idx + 1)
        return out

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_names_this_unit_as_the_sole_active_lane(self, ws0014, field):
        latest = self._own_update(ws0014[field])  # RE-ANCHORED BY XASSET-0052; see _own_update
        assert DECISION_ID in latest, field
        occurrences = self._claim_occurrences(latest)
        assert occurrences, (field, "the active-lane claim is absent entirely")
        operative = [
            (i, head) for i, head in occurrences
            if "SUPERSEDED BY EVENT" not in _flat(latest)[i: i + 400]
        ]
        assert operative, (field, "every occurrence is a superseded quotation")
        for _, head in operative:
            sentence = head.rsplit(". ", 1)[-1]
            assert DECISION_ID in sentence, (field, sentence[-200:])
            for finished in ("XASSET-0050", "XASSET-0049", "XASSET-0048"):
                assert finished not in sentence, (field, finished, sentence[-200:])

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_claim_guard_is_not_vacuous(self, ws0014, field):
        """Both a quoted-superseded occurrence AND an operative one must really be present, or
        the classification above would be testing nothing."""
        latest = self._own_update(ws0014[field])  # RE-ANCHORED BY XASSET-0052; see _own_update
        occurrences = self._claim_occurrences(latest)
        assert len(occurrences) >= 2, (field, len(occurrences))

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_records_the_authority_as_closed_and_effective(self, ws0014, field):
        latest = self._own_update(ws0014[field])  # RE-ANCHORED BY XASSET-0052; see _own_update
        assert "XASSET-0050" in latest, field
        assert "CLOSED" in latest and "EFFECTIVE" in latest, field
        assert "6fd9a6973a3ae2788d5823508dcb32d7f73d6c3d" in latest, field
        assert "32603595964" in latest, field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_records_link_3_as_discharged_and_spent(self, ws0014, field):
        latest = self._own_update(ws0014[field])  # RE-ANCHORED BY XASSET-0052; see _own_update
        assert "LINK 3 IS DISCHARGED" in latest, field
        assert LINK3_PASS_COMMENT in latest, field
        assert LINK3_PASS_DETERMINATION in latest, field
        assert "SPENT" in latest, field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_records_the_duplicate_stop_without_promoting_it(
        self, ws0014, field
    ):
        latest = self._own_update(ws0014[field])  # RE-ANCHORED BY XASSET-0052; see _own_update
        assert LINK3_DUPLICATE_STOP_COMMENT in latest, field
        assert "NO PASS" in latest, field
        lowered = latest.lower()
        assert "does not invalidate" in lowered, field
        assert "must not be rerun or re-adjudicated" in lowered, field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_keeps_link_5_unauthorized(self, ws0014, field):
        latest = self._own_update(ws0014[field])  # RE-ANCHORED BY XASSET-0052; see _own_update
        assert "LINK 5" in latest, field
        assert "SEPARATELY\n      UNAUTHORIZED" in latest or \
            "SEPARATELY UNAUTHORIZED" in _flat(latest), field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_finished_units_claim_survives_only_as_a_marked_quotation(self, ws0014, field):
        """The exact MAJOR-1 defect from review 5000502119, encoded so it cannot recur.

        The finished unit's active-lane sentence is PRESERVED verbatim -- this register is
        append-only and never rewrites accurate history -- so the guard is not "the words are
        absent" but "wherever they appear, they are marked superseded". A future edit that
        re-asserted them operatively would drop the marker and fail here.
        """
        # RE-ANCHORED BY XASSET-0052 onto THIS unit's own block; see ``_own_update``.
        flat = _flat(self._own_update(ws0014[field]))
        stale = "XASSET-0050 AND ITS GITHUB-ISSUED PULL REQUEST ARE"
        idx = flat.find(stale)
        assert idx != -1, (field, "the superseded quotation was deleted rather than marked")
        window = flat[idx: idx + 400]
        assert "SUPERSEDED BY EVENT" in window, (field, window[:240])
        assert "was true when written" in window, (field, window[:240])

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_keeps_stage_1_unarmed(self, ws0014, field):
        latest = _flat(self._latest_update(ws0014[field]))
        assert "Stage 1 remains UNARMED and NOT EXECUTABLE" in latest, field
        assert "ATTEMPT_1 is intact, unclaimed and unconsumed" in latest, field


class TestTheNewestBlockSupersedesThisUnit:
    """ADDED BY XASSET-0052 -- the other end of the ``_own_update`` re-anchor.

    Pointing this unit's own-content checks at its own block would, on its own, leave the newest
    block untested: a successor could append anything, or nothing, and every assertion above
    would still pass. This class binds that end. It asserts what a correct successor block must
    do -- name itself as the live lane and record THIS unit as finished rather than still active
    -- without asserting WHICH successor it is, so it keeps holding as the chain continues.
    """

    UPDATE_MARKER = TestTheRegistersOperativeProseAgreesWithItsStructuredFields.UPDATE_MARKER
    OWN_OPENING = TestTheRegistersOperativeProseAgreesWithItsStructuredFields.OWN_BLOCK_OPENING

    @classmethod
    def _newest(cls, field_text: str) -> str:
        return cls.UPDATE_MARKER + field_text.rsplit(cls.UPDATE_MARKER, 1)[1]

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_a_newer_block_exists_and_is_not_this_units_own(self, ws0014, field):
        newest = self._newest(ws0014[field])
        assert self.OWN_OPENING not in newest, (
            field, "the newest block is still this finished unit's own"
        )

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_newest_block_records_this_unit_as_finished(self, ws0014, field):
        newest = _flat(self._newest(ws0014[field]))
        assert DECISION_ID in newest, field
        assert any(
            marker in newest
            for marker in ("SPENT", "DISCHARGED", "SUPERSEDED BY EVENT", "CLOSED")
        ), (field, newest[:240])

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_newest_block_does_not_revive_this_unit_as_the_live_lane(self, ws0014, field):
        """This unit's active-lane claim may survive only as a marked-superseded quotation."""
        newest = _flat(self._newest(ws0014[field]))
        claim = "SOLE ACTIVE GOVERNANCE LANE"
        idx = newest.find(claim)
        while idx != -1:
            head = newest[max(0, idx - 240): idx]
            sentence = head.rsplit(". ", 1)[-1]
            if DECISION_ID in sentence:
                window = newest[max(0, idx - 400): idx + 400]
                assert "SUPERSEDED BY EVENT" in window or "SATISFIED AND SPENT" in window, (
                    field, sentence[-200:]
                )
            idx = newest.find(claim, idx + 1)

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_newest_block_keeps_stage_1_unarmed(self, ws0014, field):
        newest = _flat(self._newest(ws0014[field]))
        assert "Stage 1 remains UNARMED and NOT EXECUTABLE" in newest, field
        assert "ATTEMPT_1 is intact, unclaimed and unconsumed" in newest, field


class TestRegisterSynchronisation:
    def test_the_workstream_is_untouched_in_status_and_priority(self, ws0014):
        assert ws0014["status"] == "proposed"
        assert ws0014["priority"] == "secondary"

    def test_exactly_zero_primary_workstreams(self):
        data = yaml.safe_load(WORKSTREAMS.read_text())
        assert sum(1 for w in data["workstreams"] if w.get("priority") == "primary") == 0

    def test_the_active_branch_moved_off_this_finished_unit(self, ws0014):
        """RE-ANCHORED BY XASSET-0052.

        ``active_branch`` is WS-0014's SINGLE SHARED live self-reference, not this filing's own.
        PR #352 merged at `8def8bd0`, so under ``OPS-0001``'s Active-GitHub-fields rule it
        lawfully advanced onto the successor unit. Asserting it at this unit's own value would
        assert "this finished unit is still live", which is false. What survives -- and is
        asserted here -- is that it moved OFF this unit and did not revert to any predecessor's
        state, so the field stays bound at BOTH ends. This unit's OWN gate still carries its own
        number, which is history and does not move; that is pinned separately below.
        """
        assert ws0014["active_branch"] != "claude/xasset-0051-link4-auth-bjlfya"
        assert ws0014["active_branch"] != "claude/xasset-0050-renewed-readiness-authorization"
        assert ws0014["active_branch"] != "claude/xasset-0049-rebinding-ll6hzf"

    def test_the_last_verified_main_sha_advanced_and_is_bound_at_both_ends(self, ws0014):
        """RE-ANCHORED BY XASSET-0052, for the same reason as the field above.

        The shared field advanced from this unit's observation checkout onto the successor's.
        Every superseded value is retained as a NEGATIVE pin rather than deleted, so a silent
        revert to any finished unit's state still fails here.
        """
        assert ws0014["last_verified_main_sha"] != LINK3_OBSERVATION_CHECKOUT
        for finished in (BOUND_MERGE_SHA, "6fd9a6973a3ae2788d5823508dcb32d7f73d6c3d"):
            assert ws0014["last_verified_main_sha"] != finished, finished

    def test_the_shared_active_pr_moved_off_this_finished_unit(self, ws0014):
        """RE-ANCHORED BY XASSET-0052, for the same reason as the fields above.

        This was ``test_the_active_pr_is_the_real_github_number_not_the_sentinel``, asserting the
        shared field still equalled THIS unit's number. Never predicted then and not predicted
        now: what remains asserted is that the shared field is no longer this finished unit's,
        that no sentinel survived unclaimed into the merged record, and that it never reverted to
        a predecessor. During a successor's own sentinel window the field is negative, which is a
        real state and is checked for consistency rather than skipped.
        """
        active = ws0014["active_pr"]
        assert active != THIS_PULL_REQUEST
        assert active != BOUND_AUTHORIZING_PULL_REQUEST
        if active < 0:
            live = [g for g in ws0014["milestones"] if g.get("pr") == active]
            assert live, "the register carries a sentinel active_pr that no gate claims"
            assert all(g["status"] == "in_progress" for g in live), live
        else:
            assert active > THIS_PULL_REQUEST
            assert active not in PRIOR_SENTINELS
            assert active != PR_SENTINEL

    def test_the_finished_units_gate_is_not_rewritten(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == PRIOR_UNIT_GATE)
        assert gate["status"] == "in_progress" and gate["pr"] == 350

    def test_an_additive_closure_gate_records_the_finished_lifecycle(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == PRIOR_CLOSURE_GATE)
        assert gate["status"] == "complete" and gate["pr"] == 350
        assert "6fd9a6973a3ae2788d5823508dcb32d7f73d6c3d" in gate["description"]
        assert "LEFT BYTE-UNEDITED" in gate["description"]

    def test_this_units_gate_exists_and_is_in_progress(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)
        assert gate["status"] == "in_progress"
        assert gate["pr"] == THIS_PULL_REQUEST
        assert gate["pr"] != PR_SENTINEL, "the sentinel was never replaced"
        assert "PERFORMS NO PART" in gate["description"]

    def test_this_units_gate_is_not_marked_complete_by_its_own_filing(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)
        assert gate["status"] != "complete"

    def test_no_sentinel_survives_anywhere_in_the_register(self):
        raw = WORKSTREAMS.read_text()
        for sentinel in (PR_SENTINEL, *PRIOR_SENTINELS):
            assert f"active_pr: {sentinel}" not in raw, sentinel
            assert f"pr: {sentinel}" not in raw, sentinel

    def test_the_registers_gate_records_both_anchors(self, ws0014):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert BOUND_MERGE_SHA in gate
        assert LINK3_PASS_COMMENT in gate
        assert "MUST FAIL" in gate


class TestNegativePinsAreImpossibleValues:
    def test_the_pr_sentinel_is_impossible_and_distinct_from_prior_sentinels(self):
        assert PR_SENTINEL < 0
        assert PR_SENTINEL not in PRIOR_SENTINELS

    def test_the_dead_anchor_pins_are_distinct_from_every_live_value(self):
        live = {BOUND_MERGE_SHA, BOUND_MERGE_PARENT_1, BOUND_MERGE_PARENT_2, BOUND_MERGE_TREE,
                LINK3_OBSERVATION_CHECKOUT, LINK3_OBSERVATION_TREE}
        assert DEAD_MERGE_SHA not in live
        assert DEAD_STEP9_EVIDENCE_COMMENT not in {LINK3_PASS_COMMENT,
                                                   LINK3_DUPLICATE_STOP_COMMENT}
        assert SPENT_STEP10_EVIDENCE_COMMENT not in {LINK3_PASS_COMMENT,
                                                     LINK3_DUPLICATE_STOP_COMMENT}
