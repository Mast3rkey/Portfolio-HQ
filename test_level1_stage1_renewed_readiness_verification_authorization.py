"""Adversarial tests pinning the ``XASSET-0050`` renewed step-9 readiness-verification authorization.

``XASSET-0049``'s complete seven-condition lifecycle closed, so ``XASSET-0041`` §I **link 2** -- the
``XASSET-0030`` §G.B step-8-equivalent successor operational / load-bearing rebinding -- is
discharged. **Link 3** is next, and it had **no authority**.

``XASSET-0038`` does not supply it, for two independent reasons either sufficient alone:

1. **Its grant is spent.** §A authorized "exactly one" step-9 unit; that unit ran and returned
   ``STEP_9_READINESS_VERIFICATION_PASS``, consumed as an input by ``XASSET-0039`` §C.
2. **Its anchor is dead.** It anchored to the PR #337 merge, a different accepted head, **ten**
   load-bearing paths, and canonical pins ``367583b6…``/``768b013c…``. ``XASSET-0042`` corrected
   load-bearing path #1, ``XASSET-0044`` amended both canonical artifacts, and the boundary has grown
   to **eighteen**.

Four filings after ``XASSET-0038`` named the renewed verification and four declined to grant it.
``XASSET-0050`` closes that gap for the renewed readiness verification and nothing else.

The whole risk of an authorization filing is that it grants more than it says, or that a future
session reads more out of it than it contains. Every test below therefore pins **an authorized
boundary and its nearest plausible overreach** -- the stronger permission a successor might infer
from the same text, which the decision must refuse.

The overreaches that matter most each have a dedicated guard:

1. **The verification performed now, or treated as authorized on filing.**
   ``TestVerificationIsNotPerformedHere`` and ``TestEffectivityRequiresCompleteLifecycleClosure``
   fail if the filing runs the checklist, issues a determination, or lets any single lifecycle step
   stand in for complete closure.
2. **Links 4 and 5 read as included.** ``TestLinks4And5RetainSeparateAuthority`` fails if either is
   granted, implied, or made reachable by a clean readiness finding.
3. **``XASSET-0038`` treated as still live.** ``TestXasset0038IsSpentAndItsAnchorIsDead`` fails if
   the filing revives it, or if the superseded anchor values are not pinned NEGATIVELY -- a silent
   reversion to the dead anchor must fail a test rather than pass unnoticed.
4. **"Read-only" drifting into repair.** ``TestReadOnlyMeansReadOnly`` and ``TestFailClosed`` fail if
   the authorized unit may create, edit, regenerate or correct anything, may declare a defect
   "fixed", or may continue past drift or uncertainty.
5. **The closed checklist quietly reopening, or its pins going stale.**
   ``TestClosedRenewedChecklist`` fails if any of the eleven conditions is dropped;
   ``TestChecklistPinsMatchTheLiveSystem`` fails if any recorded pin drifts from the value derived
   from the bound merge tree.
6. **Arming by implication.** ``TestXasset0029NoRegressIntact`` fails if the filing presents itself
   as an activation PR, adds an activation authorization, or lets merge imply an armed Stage 1.
7. **Silent consumption of the reserved results PR.** ``TestP1ResultsPRRemainsSeparate``.
8. **The register's structured fields advancing while its operative prose goes stale.**
   ``TestTheRegistersOperativeProseAgreesWithItsStructuredFields`` isolates each field's LATEST dated
   block, because an assertion over the whole field would be satisfied by the stale text.

They also pin the negative space that makes the filing honest: this authorization PR changes no
canonical file, no validator, no authorization module, no runner, no result validator, and no
load-bearing byte; all eighteen load-bearing paths, both canonical pins, the frozen universe, and the
construction-universe module identity are untouched; ``REQUIRED_LIFECYCLE_GATES`` is still the
six-element tuple; and Stage 1 is still ``UNARMED`` with lane state ``ABSENT`` and ``ATTEMPT_1``
unclaimed.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No results document, lane directory, attestation, claim, completion, or ledger entry
is created or read for authorization purposes. No ``risk_lane_boundary`` protected result path is
read, listed, opened, or referenced.
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
GOV = ROOT / "governance/decisions"
PREREG = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"
PROTOCOL = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
WORKSTREAMS = ROOT / "operations/WORKSTREAMS.yaml"
CATALOG = ROOT / "governance/decisions.yaml"

DECISION_ID = "XASSET-0050"
DECISION = (
    GOV
    / "XASSET-0050-endpoint-0001-stage-1-renewed-readiness-verification-authorization.md"
)

D0027 = GOV / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
D0029 = GOV / "XASSET-0029-endpoint-0001-stage-1-operational-authorization.md"
D0030 = GOV / "XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md"
D0036 = GOV / "XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md"
D0038 = (
    GOV
    / "XASSET-0038-endpoint-0001-stage-1-runner-execution-readiness-verification-authorization.md"
)
D0041 = (
    GOV
    / "XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md"
)
D0048 = GOV / "XASSET-0048-endpoint-0001-stage-1-step-8-equivalent-rebinding-authorization.md"
D0049 = (
    GOV
    / "XASSET-0049-endpoint-0001-stage-1-step-8-equivalent-successor-operational-rebinding.md"
)

# ---------------------------------------------------------------------------------------------
# The PR #349 lifecycle this authorization anchors its checklist to. Verified live in preflight.
# ---------------------------------------------------------------------------------------------

BOUND_MERGE_SHA = "a941455491cc5e4d3d868775fb6b4b88f0fe2ce3"
BOUND_ACCEPTED_HEAD = "b2059e80101fc6457f4004939d7d12886e6feedf"
BOUND_MERGE_BASE = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"
BOUND_MERGE_TREE = "b7015b271362ae0c2fe663e8bfda9c6d10de5e7e"

FULL_REVIEW = "5000502119"
DELTA_REVIEW = "5000581301"
PRINCIPAL_ACCEPTANCE = "5381488381"
POST_MERGE_VERIFICATION = "5381551149"
FINAL_CLOSURE = "5381561978"
MERGE_CI_RUN = "32585793843"
MERGE_CI_JOB = "97061842978"

#: An impossible sentinel, distinct from every sentinel used before (-1, -2). Committed first, then
#: replaced by the number GitHub actually issued in a fast-forward follow-up commit. RETAINED as a
#: negative pin so a revert to the unbound state still fails.
PR_SENTINEL = -50

#: The number GitHub ISSUED for this unit, read back from the live API after the draft was opened.
#: Never predicted, never guessed.
THIS_PULL_REQUEST = 350

# ---------------------------------------------------------------------------------------------
# NEGATIVE pins. XASSET-0038's anchor is dead on every axis; a silent reversion to it must FAIL.
# ---------------------------------------------------------------------------------------------

DEAD_MERGE_SHA = "637eaa30302f5a71f84ab1d215ecbd32c01399b5"
DEAD_ACCEPTED_HEAD = "f40c816223c78f1d1e436b718455df5fb3d77fa7"
DEAD_LOAD_BEARING_COUNT = 10
DEAD_PROTOCOL_PIN_PREFIX = "367583b6"
DEAD_PREREG_PIN_PREFIX = "768b013c"

# ---------------------------------------------------------------------------------------------
# C2 / C3 / C4 / C5 / C6 -- the pins the renewed checklist binds.
# ---------------------------------------------------------------------------------------------

EXPECTED_LOAD_BEARING_COUNT = 18

#: C3 -- the five outcome-capable modules, recorded here as the filing-time WITNESS. §G.1 makes the
#: value DERIVED from the bound merge tree operative; this table exists so a drift between the two
#: fails in CI instead of waiting to be noticed at verification time.
C3_MODULE_WITNESS = {
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

C4_CANONICAL_PINS = {
    "research/level1_endpoint_evidence/PROTOCOL_V1.md":
        "1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84",
    "research/level1_endpoint_evidence/pre_registration.yaml":
        "898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f",
}

C5_CONSTRUCTION_COUNT = 680
C5_CELL_COUNT = 48
C5_UNIVERSE_SHA = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
C6_UNIVERSE_MODULE_SHA = "1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5"

#: The production authorization module's identity, which this filing must leave BYTE-IDENTICAL.
AUTH_MODULE_SHA = "4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541"

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


# ---------------------------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------------------------


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

    def test_this_decision_is_the_newest_row(self, catalog):
        assert catalog[-1]["decision_id"] == DECISION_ID


class TestAuthorityGapIsGroundedInAcceptedText:
    """The gap must be shown from accepted text, never inferred from convenience."""

    def test_xasset0041_names_link_3_and_withholds_it(self):
        text = D0041.read_text()
        assert "renewed readiness" in text
        assert "separately authorized" in text
        assert "None of links 2 through 5 is authorized" in text

    @pytest.mark.parametrize("path", [D0048, D0049])
    def test_the_two_most_recent_filings_withhold_the_renewed_verification_by_name(self, path):
        text = path.read_text()
        assert "renewed readiness verification" in text
        assert "link 3" in text

    def test_the_decision_reproduces_the_withholdings_rather_than_asserting_a_gap(
        self, decision_text
    ):
        for cited in ("XASSET-0041", "XASSET-0043", "XASSET-0046", "XASSET-0048", "XASSET-0049"):
            assert cited in decision_text
        assert "established by accepted repository text, not inferred" in _flat(decision_text)

    def test_gb_still_authorizes_none_of_itself(self):
        assert "authorizes none of G.A or G.B" in D0030.read_text()


class TestXasset0038IsSpentAndItsAnchorIsDead:
    """The nearest plausible overreach is treating ``XASSET-0038`` as still live authority."""

    def test_the_decision_records_the_grant_as_spent(self, decision_text):
        assert "Its grant is spent" in decision_text
        assert "5336643459" in decision_text, "the completed PASS evidence must be cited"

    def test_the_decision_records_the_anchor_as_dead(self, decision_text):
        assert "Its anchor is dead" in decision_text
        for dead in (DEAD_MERGE_SHA, DEAD_ACCEPTED_HEAD,
                     DEAD_PROTOCOL_PIN_PREFIX, DEAD_PREREG_PIN_PREFIX):
            assert dead in decision_text, dead

    def test_xasset0038_is_not_revived_extended_or_amended(self, decision_text):
        section = _section(decision_text, "B.")
        assert "not** reopened, extended, amended, revived, or re-scoped" in section
        assert "spent grant is not restored" in section

    def test_the_completed_pass_is_not_relied_on_as_current_evidence(self, decision_text):
        section = _section(decision_text, "B.")
        assert "neither re-adjudicates it nor relies on it" in section

    def test_the_dead_anchor_is_not_the_live_anchor(self):
        """NEGATIVE pin: a silent reversion to XASSET-0038's anchor must fail here."""
        assert BOUND_MERGE_SHA != DEAD_MERGE_SHA
        assert BOUND_ACCEPTED_HEAD != DEAD_ACCEPTED_HEAD
        assert len(A.LOAD_BEARING_RELPATHS) != DEAD_LOAD_BEARING_COUNT
        for _, pin in C4_CANONICAL_PINS.items():
            assert not pin.startswith(DEAD_PROTOCOL_PIN_PREFIX)
            assert not pin.startswith(DEAD_PREREG_PIN_PREFIX)

    def test_xasset0038_itself_is_untouched_by_this_filing(self):
        assert _blob_sha256_at(
            "governance/decisions/"
            "XASSET-0038-endpoint-0001-stage-1-runner-execution-readiness-verification-"
            "authorization.md"
        ) == hashlib.sha256(D0038.read_bytes()).hexdigest()


class TestVerificationIsNotPerformedHere:
    """The filing must authorize without consuming any part of what it authorizes."""

    def test_the_decision_says_it_performs_no_part(self, decision_text):
        section = _section(decision_text, "A.")
        assert "performs no part of that verification" in section
        assert "consumes none of the authority it creates" in section

    def test_no_pass_or_fail_determination_is_issued(self, decision_text):
        assert "issues no `PASS` or `FAIL`" in _flat(decision_text)
        assert "STEP_9_READINESS_VERIFICATION_PASS" not in _section(decision_text, "A.")

    def test_no_checklist_condition_is_marked_satisfied(self, decision_text):
        """A condition table that carried outcomes would be a performed checklist."""
        section = _section(decision_text, "G.")
        for verdict in ("| PASS", "| FAIL", "PASS |", "FAIL |"):
            assert verdict not in section, verdict

    def test_no_results_artifact_exists(self):
        assert not (ROOT / "stage1_results.yaml").exists()
        assert not list(ROOT.rglob("stage1_results.yaml"))


class TestEffectivityRequiresCompleteLifecycleClosure:
    def test_all_seven_conditions_are_enumerated(self, decision_text):
        section = _section(decision_text, "J.")
        for n in range(1, 8):
            assert f"{n}." in section
        assert "merge-commit CI whose `head_sha` is the exact merge SHA" in section

    def test_no_single_condition_is_sufficient(self, decision_text):
        section = _section(decision_text, "J.")
        assert "None is individually sufficient" in section
        assert "Opening this PR authorizes nothing" in section
        assert "a green PR-head CI run does" in section

    def test_the_repository_lifecycle_gates_are_unchanged(self):
        assert tuple(A.REQUIRED_LIFECYCLE_GATES) == EXPECTED_LIFECYCLE_GATES
        assert len(A.REQUIRED_LIFECYCLE_GATES) == 6

    def test_even_full_closure_yields_only_a_read_only_verification(self, decision_text):
        section = _section(decision_text, "J.")
        assert "read-only verification**, never arming and never execution" in section


class TestLinks4And5RetainSeparateAuthority:
    @pytest.mark.parametrize(
        "link,alias",
        [("Link 4", "step 10"), ("Link 5", "step 11")],
    )
    def test_each_link_is_withheld_individually(self, decision_text, link, alias):
        """A mutation probe found that asserting the withholding phrase appears SOMEWHERE in the
        section let one link be quietly released while the other kept the phrase alive. Each link
        is now bound to its own withholding, scoped to the text that actually describes it."""
        section = _section(decision_text, "K.")
        assert link in section and alias in section
        start = section.index(link)
        nxt = section.find("Link 5") if link == "Link 4" else len(section)
        clause = section[start: nxt if nxt > start else len(section)]
        assert "retains its own separate-authority requirement" in clause, (link, clause[:200])
        assert "not\n  authorized here" in clause or "not authorized here" in clause \
            or "entirely outside\nthis filing" in clause or "entirely outside this filing" in clause, \
            (link, clause[:200])

    def test_a_clean_pass_authorizes_nothing_further(self, decision_text):
        section = _section(decision_text, "K.")
        assert "authorizes nothing further" in section
        assert "not permission to arm, to claim, or to execute" in section

    def test_the_stop_and_report_rule_is_not_a_grant_of_link_4(self, decision_text):
        section = _section(decision_text, "K.")
        assert "not a grant of link 4" in section

    def test_xasset0040_stays_spent(self, decision_text):
        assert "stays spent as a stop and is not revived" in _flat(decision_text)

    def test_the_withheld_list_names_both_links(self, decision_text):
        section = _section(decision_text, "F.")
        assert "link 4 or link 5" in section
        assert "step 10 or step 11" in section


class TestReadOnlyMeansReadOnly:
    @pytest.mark.parametrize(
        "prohibition",
        [
            "declare any defect \"fixed\"",
            "extend, reduce, re-order, or re-derive `LOAD_BEARING_RELPATHS`",
            "produce an attestation",
            "create `stage1_results.yaml`",
            "evaluate or decide any gate",
            "portfolio construction, target-allocation calculation",
            "risk_lane_boundary",
            "consume `XASSET-0027` §P.1's reserved results PR",
        ],
    )
    def test_each_prohibition_is_present(self, decision_text, prohibition):
        assert prohibition in _section(decision_text, "F.")

    def test_the_production_module_constants_may_not_be_changed(self, decision_text):
        section = _section(decision_text, "F.")
        assert "`REQUIRED_LIFECYCLE_GATES`" in section
        assert "`REVIEWED_BASE_SHA`" in section

    def test_the_xasset0036_read_only_line_is_reused_not_widened(self, decision_text):
        section = _section(decision_text, "F.")
        assert "traversing frozen construction identities is not execution" in section
        assert "does not widen by one step" in _flat(decision_text)

    def test_an_actual_run_over_the_real_680_stays_prohibited(self, decision_text):
        assert "actual Stage-1 run over the real 680 remains absolutely prohibited" in _flat(decision_text)


class TestClosedRenewedChecklist:
    @pytest.mark.parametrize("condition", [f"C{n}" for n in range(1, 12)])
    def test_every_condition_is_present(self, decision_text, condition):
        assert f"**{condition}**" in _section(decision_text, "G.")

    def test_the_checklist_is_closed(self, decision_text):
        section = _section(decision_text, "G.")
        assert "**Closed**" in section
        assert "adds no further condition of its own invention" in section
        assert "a finding to report, not a checklist item to add" in section

    def test_c2_derives_identity_from_the_merged_tree(self, decision_text):
        section = _section(decision_text, "G.")
        assert "derived from the merged tree at verification time" in section

    def test_c3_records_a_witness_and_still_derives(self, decision_text):
        """§G.1 is what makes the redundancy safe rather than a second source of truth."""
        assert "#### G.1" in decision_text
        g1 = _flat(decision_text.split("#### G.1", 1)[1].split("### H.", 1)[0])
        assert "The derived value governs" in g1
        assert "stop" in g1
        assert "pinned by test" in g1


class TestChecklistPinsMatchTheLiveSystem:
    """Every recorded pin must equal the value derived from the bound merge tree."""

    def test_load_bearing_count_and_uniqueness(self):
        assert len(A.LOAD_BEARING_RELPATHS) == EXPECTED_LOAD_BEARING_COUNT
        assert len(set(A.LOAD_BEARING_RELPATHS)) == EXPECTED_LOAD_BEARING_COUNT

    def test_every_load_bearing_path_matches_the_bound_merge(self):
        for relpath in A.LOAD_BEARING_RELPATHS:
            worktree = hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest()
            assert worktree == _blob_sha256_at(relpath), relpath

    @pytest.mark.parametrize("relpath,expected", sorted(C3_MODULE_WITNESS.items()))
    def test_c3_witness_equals_the_derived_identity(self, relpath, expected):
        assert _blob_sha256_at(relpath) == expected, relpath

    @pytest.mark.parametrize("relpath,expected", sorted(C4_CANONICAL_PINS.items()))
    def test_c4_canonical_pins_equal_the_derived_identity(self, relpath, expected):
        assert _blob_sha256_at(relpath) == expected, relpath

    def test_c4_pins_match_the_modules_live_canonical_pin_table(self):
        assert dict(A.CANONICAL_PINS) == C4_CANONICAL_PINS

    def test_c5_universe_is_unchanged(self):
        assert A.CONSTRUCTION_COUNT == C5_CONSTRUCTION_COUNT
        assert A.CONSTRUCTION_CELL_COUNT == C5_CELL_COUNT
        assert A.CONSTRUCTION_UNIVERSE_SHA256 == C5_UNIVERSE_SHA

    def test_c6_universe_module_identity_is_unchanged(self):
        assert _blob_sha256_at(
            "level1_construction_universe_closure_validator.py"
        ) == C6_UNIVERSE_MODULE_SHA

    def test_the_decision_records_each_pin_it_claims_to_bind(self, decision_text):
        section = _section(decision_text, "G.")
        for expected in C3_MODULE_WITNESS.values():
            assert expected in section
        for expected in C4_CANONICAL_PINS.values():
            assert expected in section
        assert C5_UNIVERSE_SHA in section
        assert C6_UNIVERSE_MODULE_SHA in section

    def test_the_decision_states_the_same_path_count_the_module_has(self, decision_text):
        """A mutation probe found this gap: the decision could state "**10**" while the module
        held 18 and every other assertion still passed, because they measured the module rather
        than the claim. The document's own count is now bound to the live one, so a stale or
        copied count fails here."""
        flat = _flat(decision_text)
        counts = re.findall(r"\*\*(\d+)\*\*,? [^.|]{0,40}?`?LOAD_BEARING_RELPATHS`?", flat)
        assert counts, "the decision states no LOAD_BEARING_RELPATHS count at all"
        # XASSET-0038's superseded count is legitimately CITED, but only inside the passage that
        # retires it. Every count outside that passage is a claim about THIS system and must be
        # the live one. Splitting on the dead-anchor sentence is what keeps the check honest
        # rather than simply tolerating any number that happens to appear.
        dead_passage = flat.split("Its anchor is dead", 1)
        assert len(dead_passage) == 2, "the dead-anchor passage is missing"
        head, tail = dead_passage
        retired = re.findall(r"\*\*(\d+)\*\*,? [^.|]{0,40}?`?LOAD_BEARING_RELPATHS`?", tail[:600])
        assert retired == [str(DEAD_LOAD_BEARING_COUNT)], retired
        live_claims = [c for c in counts if c != str(DEAD_LOAD_BEARING_COUNT)]
        assert live_claims, "the decision never states this system's own count"
        assert set(live_claims) == {str(EXPECTED_LOAD_BEARING_COUNT)}, set(live_claims)
        assert counts.count(str(DEAD_LOAD_BEARING_COUNT)) == 1, (
            "the superseded count appears outside the passage that retires it"
        )

    def test_the_decision_records_the_full_pr349_lifecycle_identities(self, decision_text):
        for identity in (
            BOUND_MERGE_SHA, BOUND_ACCEPTED_HEAD, BOUND_MERGE_BASE, BOUND_MERGE_TREE,
            FULL_REVIEW, DELTA_REVIEW, PRINCIPAL_ACCEPTANCE,
            POST_MERGE_VERIFICATION, FINAL_CLOSURE, MERGE_CI_RUN, MERGE_CI_JOB,
        ):
            assert identity in decision_text, identity


class TestFailClosed:
    def test_any_uncertainty_stops_the_unit(self, decision_text):
        section = _section(decision_text, "H.")
        assert "Uncertainty is failure" in section
        assert "may not resolve an ambiguous state in favour of readiness" in section

    def test_a_defect_forces_a_separately_authorized_correction(self, decision_text):
        section = _section(decision_text, "H.")
        assert "separately authorized correction" in section
        assert "must itself be redone under its own separate authority" in section

    def test_the_prohibition_is_not_relaxed_by_finding_a_defect(self, decision_text):
        section = _section(decision_text, "H.")
        assert "not relaxed by the discovery of a defect" in section

    def test_a_stopped_unit_may_not_issue_a_pass(self, decision_text):
        assert "**not** issue a `PASS`" in _section(decision_text, "H.")


class TestEvidenceIsExternalAndNonMutating:
    def test_the_unit_creates_no_branch_commit_or_pull_request(self, decision_text):
        section = _section(decision_text, "I.")
        assert "no branch, no commit, and no pull request" in section

    def test_the_result_is_posted_externally(self, decision_text):
        section = _section(decision_text, "I.")
        assert "durable, externally posted evidence" in section

    def test_a_repository_mutation_to_record_the_result_is_not_authorized(self, decision_text):
        section = _section(decision_text, "I.")
        assert "neither required nor authorized" in section
        assert "a finding to report under §H, not scope to assume" in section


class TestXasset0029NoRegressIntact:
    def test_zero_activation_authorizations_are_added(self, decision_text):
        section = _section(decision_text, "D.")
        assert "**zero** activation authorizations" in section

    def test_merging_does_not_arm_stage_1(self, decision_text):
        section = _section(decision_text, "D.")
        assert "does not make Stage 1 armed or executable" in section

    def test_activation_remains_the_external_attestation(self, decision_text):
        section = _section(decision_text, "D.")
        assert "one-shot runtime attestation and the operator's" in section
        assert "not a merged activation PR" in section

    def test_no_committed_value_authorizes_execution(self, decision_text):
        assert "No committed value in this repository authorizes Stage-1 execution" in _flat(decision_text)


class TestP1ResultsPRRemainsSeparate:
    def test_p1_is_not_consumed(self, decision_text):
        section = _section(decision_text, "C.")
        assert "not consumed, replaced, amended, or counted" in section
        assert "one, unspent" in section

    def test_the_three_grounds_are_stated(self, decision_text):
        section = _section(decision_text, "C.")
        assert "results document" in section
        assert "after arming" in section
        assert "no production configuration change" in section


class TestThisFilingMutatesNothingLoadBearing:
    """The negative space that makes the filing honest."""

    def test_the_authorization_module_is_byte_identical_to_the_bound_merge(self):
        live = hashlib.sha256((ROOT / "level1_stage1_execution_authorization.py").read_bytes())
        assert live.hexdigest() == AUTH_MODULE_SHA
        assert _blob_sha256_at("level1_stage1_execution_authorization.py") == AUTH_MODULE_SHA

    def test_the_rebinding_constants_are_untouched(self):
        assert A.AUTHORIZING_DECISION == BOUND_AUTHORIZING_DECISION
        assert A.AUTHORIZING_PULL_REQUEST == BOUND_AUTHORIZING_PULL_REQUEST
        assert A.REVIEWED_BASE_SHA == BOUND_REVIEWED_BASE_SHA

    def test_reviewed_base_sha_is_the_rebinding_base_not_current_main(self):
        """NEGATIVE pin: REVIEWED_BASE_SHA must not drift onto the merge that carried XASSET-0049."""
        assert A.REVIEWED_BASE_SHA != BOUND_MERGE_SHA

    @pytest.mark.parametrize("relpath", sorted(C3_MODULE_WITNESS) + sorted(C4_CANONICAL_PINS))
    def test_no_load_bearing_file_is_modified_by_this_filing(self, relpath):
        worktree = hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest()
        assert worktree == _blob_sha256_at(relpath), relpath

    def test_the_new_decision_is_not_added_to_the_trust_boundary(self):
        """An authorization filing must not quietly extend the enforcement surface."""
        assert not any(DECISION_ID in p for p in A.LOAD_BEARING_RELPATHS)

    def test_the_universe_closure_validator_is_untouched_by_this_filing(self):
        """It is the C6 module; its identity is pinned, and it is not imported for its constants."""
        module_path = Path(CU.__file__).name
        assert module_path == "level1_construction_universe_closure_validator.py"
        assert _blob_sha256_at(module_path) == C6_UNIVERSE_MODULE_SHA


class TestStage1PostureUnchanged:
    def test_execution_is_not_authorized(self):
        authorized = A.new_execution_is_authorized()
        ok = authorized[0] if isinstance(authorized, tuple) else authorized
        assert ok is False

    def test_the_lane_is_absent(self):
        assert not Path(A.AUTHORIZATION_ROOT).exists()

    def test_attempt_1_is_intact(self):
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

    def test_the_decision_states_the_posture(self, decision_text):
        flat = _flat(decision_text)
        assert "Stage 1 remains UNARMED and NOT EXECUTABLE" in flat
        assert "intact, unclaimed, and unconsumed" in flat


class TestTheRegistersOperativeProseAgreesWithItsStructuredFields:
    """``next_action`` and ``blocker`` are APPEND-ONLY dated logs.

    An assertion over the whole field would be satisfied by the stale text and would therefore be
    vacuous. Each test isolates the LATEST dated block; a companion test proves the older prose
    survives and that the fields really are multi-block logs, so the isolation cannot silently
    degrade into a whole-field test.
    """

    UPDATE_MARKER = "UPDATE, 2026-08-22"

    @staticmethod
    def _latest_update(field_text: str) -> str:
        marker = TestTheRegistersOperativeProseAgreesWithItsStructuredFields.UPDATE_MARKER
        assert marker in field_text, "the field carries no dated update at all"
        return marker + field_text.rsplit(marker, 1)[1]

    def test_the_fields_really_are_append_only_dated_logs(self, ws0014):
        for field in ("next_action", "blocker"):
            text = ws0014[field]
            assert text.count(self.UPDATE_MARKER) >= 2, field
            assert len(self._latest_update(text)) < len(text), field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_names_this_unit_as_the_sole_active_lane(self, ws0014, field):
        """A mutation probe found that asserting the phrase merely APPEARS was not enough: the
        block names several decisions, so rewriting the active-lane sentence to name a finished
        one left both tokens present and the check passed. The claim is now bound to whichever
        decision the sentence actually attributes it to."""
        latest = self._latest_update(ws0014[field])
        assert DECISION_ID in latest, field
        claim = "SOLE ACTIVE GOVERNANCE LANE"
        assert claim in latest, field
        head = latest[: latest.index(claim)]
        # Whatever wording precedes it, the subject of the claim must be THIS decision, and the
        # sentence must not have been re-pointed at a predecessor.
        sentence = head.rsplit(".", 1)[-1]
        assert DECISION_ID in sentence, (field, sentence[-160:])
        for finished in ("XASSET-0049", "XASSET-0048", "XASSET-0047"):
            assert finished not in sentence, (field, finished, sentence[-160:])

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_records_the_authority_as_closed_and_effective(self, ws0014, field):
        latest = self._latest_update(ws0014[field])
        assert "XASSET-0049" in latest, field
        assert "CLOSED" in latest and "EFFECTIVE" in latest, field
        assert BOUND_MERGE_SHA in latest, field
        assert MERGE_CI_RUN in latest and MERGE_CI_JOB in latest, field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_does_not_call_the_finished_unit_the_active_lane(
        self, ws0014, field
    ):
        """The exact MAJOR-1 defect from review 5000502119, encoded so it cannot recur."""
        latest = self._latest_update(ws0014[field])
        stale = "XASSET-0049 / PR #349 IS THE SOLE ACTIVE"
        if stale in latest:
            assert "SUPERSEDED BY EVENT" in latest or "SATISFIED AND SPENT" in latest, field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_authorizes_link_3_without_performing_it(self, ws0014, field):
        latest = self._latest_update(ws0014[field])
        assert "LINK 3" in latest.upper(), field
        assert "NOT PERFORMED" in latest.upper() or "PERFORMS NO PART" in latest.upper(), field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_keeps_links_4_and_5_unauthorized(self, ws0014, field):
        latest = self._latest_update(ws0014[field])
        assert "LINKS 4 AND 5" in latest.upper(), field
        assert "SEPARATELY UNAUTHORIZED" in latest.upper(), field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_states_the_stage_1_posture(self, ws0014, field):
        latest = self._latest_update(ws0014[field])
        assert "UNARMED" in latest and "NOT EXECUTABLE" in latest, field
        assert "ATTEMPT_1 is intact" in latest, field

    def test_the_older_dated_prose_survives(self, ws0014):
        """Append-only means the superseded blocks are retained, not deleted."""
        for field in ("next_action", "blocker"):
            assert "XASSET-0048" in ws0014[field], field


class TestRegisterStructuredFieldsAdvanced:
    def test_the_live_self_reference_fields_moved(self, ws0014):
        assert ws0014["active_branch"] == "claude/xasset-0050-renewed-readiness-authorization"
        assert ws0014["last_verified_main_sha"] == BOUND_MERGE_SHA

    def test_the_active_pr_is_the_sentinel_or_the_issued_number(self, ws0014):
        """Never predicted: the sentinel is replaced only after GitHub issues the real number."""
        active = ws0014["active_pr"]
        assert active == THIS_PULL_REQUEST
        assert active != PR_SENTINEL, "the sentinel was never replaced"
        assert active > BOUND_AUTHORIZING_PULL_REQUEST

    def test_the_finished_units_gate_is_not_rewritten(self, ws0014):
        gate = next(
            g for g in ws0014["milestones"]
            if g["gate"] == "xasset0049-step8-equivalent-successor-operational-rebinding"
        )
        assert gate["status"] == "in_progress" and gate["pr"] == 349

    def test_an_additive_closure_gate_records_the_finished_lifecycle(self, ws0014):
        gate = next(
            g for g in ws0014["milestones"] if g["gate"] == "xasset0049-post-merge-verification"
        )
        assert gate["status"] == "complete" and gate["pr"] == 349
        assert BOUND_MERGE_SHA in gate["description"]
        assert "LEFT BYTE-UNEDITED" in gate["description"]

    def test_this_units_gate_exists_and_is_in_progress(self, ws0014):
        gate = next(
            g for g in ws0014["milestones"]
            if g["gate"] == "xasset0050-renewed-readiness-verification-authorization"
        )
        assert gate["status"] == "in_progress"
        assert gate["pr"] == THIS_PULL_REQUEST
        assert gate["pr"] != PR_SENTINEL, "the sentinel was never replaced"
        assert "PERFORMS NO PART" in gate["description"]

    def test_this_units_gate_is_not_marked_complete_by_its_own_filing(self, ws0014):
        gate = next(
            g for g in ws0014["milestones"]
            if g["gate"] == "xasset0050-renewed-readiness-verification-authorization"
        )
        assert gate["status"] != "complete"


class TestAbsoluteNonAuthorization:
    @pytest.mark.parametrize(
        "phrase",
        [
            "generates no attestation",
            "creates no `AUTHORIZATION_ROOT`",
            "performs no portfolio construction and no target-allocation calculation",
            "consumes nothing of `ATTEMPT_1`",
            "rewrites no accepted history",
        ],
    )
    def test_each_non_authorization_clause_is_present(self, decision_text, phrase):
        assert phrase in _section(decision_text, "L.")


class TestNoCorruptedIdentityCanHideInTheDecision:
    """ADDED after a mutation probe found a real gap.

    ``test_the_decision_records_the_full_pr349_lifecycle_identities`` asserts each identity is
    PRESENT. That is necessary but not sufficient: these identities appear several times each, so
    corrupting ONE occurrence left the others to satisfy the presence check and the probe passed
    while the document was wrong.

    The invariant that actually bites is the converse -- every identity-shaped token in the
    document must be one this filing verified. Anything else is either a typo or an unverified
    claim, and both are defects in a record whose entire job is to pin exact identities.
    """

    #: Every 40-hex commit identity the decision is entitled to name, and why.
    ALLOWED_COMMITS = {
        BOUND_MERGE_SHA,          # PR #349 merge -- the bound anchor
        BOUND_ACCEPTED_HEAD,      # PR #349 accepted head
        BOUND_MERGE_BASE,         # PR #349 base == XASSET-0048's merge
        BOUND_MERGE_TREE,         # merge tree, identical to the accepted-head tree
        "8ab773866c5959cd61a73dd48af197339c48754a",  # PR #349 pre-correction head
        DEAD_MERGE_SHA,           # XASSET-0038's superseded anchor, cited to retire it
        DEAD_ACCEPTED_HEAD,       # ditto
    }

    #: Every 64-hex content identity, all re-derived from the bound merge tree in preflight.
    ALLOWED_DIGESTS = set(C3_MODULE_WITNESS.values()) | set(C4_CANONICAL_PINS.values()) | {
        C5_UNIVERSE_SHA,
        C6_UNIVERSE_MODULE_SHA,
    }

    #: Every GitHub review / comment / run / job id.
    ALLOWED_GITHUB_IDS = {
        FULL_REVIEW, DELTA_REVIEW, PRINCIPAL_ACCEPTANCE,
        POST_MERGE_VERIFICATION, FINAL_CLOSURE, MERGE_CI_RUN, MERGE_CI_JOB,
        "5336643459",  # XASSET-0038's completed step-9 PASS evidence, cited as spent
    }

    def test_every_commit_identity_is_one_this_filing_verified(self, decision_text):
        found = set(re.findall(r"\b[0-9a-f]{40}\b", decision_text))
        assert found <= self.ALLOWED_COMMITS, found - self.ALLOWED_COMMITS

    def test_every_content_digest_is_one_this_filing_verified(self, decision_text):
        found = set(re.findall(r"\b[0-9a-f]{64}\b", decision_text))
        assert found <= self.ALLOWED_DIGESTS, found - self.ALLOWED_DIGESTS

    def test_every_github_id_is_one_this_filing_verified(self, decision_text):
        found = set(re.findall(r"\b\d{8,}\b", decision_text))
        assert found <= self.ALLOWED_GITHUB_IDS, found - self.ALLOWED_GITHUB_IDS

    def test_the_allowlists_are_not_vacuously_permissive(self):
        """A guard that allowed everything would pass silently. Each list is finite and small."""
        assert len(self.ALLOWED_COMMITS) == 7
        assert len(self.ALLOWED_DIGESTS) == 8
        assert len(self.ALLOWED_GITHUB_IDS) == 8

    def test_every_allowed_digest_is_actually_derivable_from_the_bound_merge(self):
        """The allowlist may not become a place to park an unverified value: every digest in it
        except the two universe aggregates is the real content hash of a real bound path."""
        derivable = {
            _blob_sha256_at(rel)
            for rel in list(C3_MODULE_WITNESS) + list(C4_CANONICAL_PINS)
        }
        assert derivable == self.ALLOWED_DIGESTS - {C5_UNIVERSE_SHA}


class TestSuiteHygiene:
    def test_this_module_performs_no_filesystem_write(self):
        """AST-level, not a substring scan -- this file's own prose mentions writing."""
        tree = ast.parse(Path(__file__).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                assert node.func.attr not in {
                    "write_text", "write_bytes", "mkdir", "unlink", "touch", "rmdir",
                }, ast.dump(node.func)

    def test_this_module_never_reads_a_protected_risk_result(self):
        tree = ast.parse(Path(__file__).read_text())
        names = {
            n.id for n in ast.walk(tree) if isinstance(n, ast.Name)
        } | {
            n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)
        }
        assert "risk_lane_boundary" not in names

    def test_the_negative_pins_are_genuinely_different_from_the_live_values(self):
        """A negative pin equal to the live value would be a silently vacuous guard."""
        assert DEAD_MERGE_SHA != BOUND_MERGE_SHA
        assert DEAD_ACCEPTED_HEAD != BOUND_ACCEPTED_HEAD
        assert DEAD_LOAD_BEARING_COUNT != EXPECTED_LOAD_BEARING_COUNT

    def test_the_pr_sentinel_is_impossible_and_distinct_from_prior_sentinels(self):
        assert PR_SENTINEL < 0
        assert PR_SENTINEL not in (-1, -2)

    def test_the_issued_number_is_later_than_every_predecessor(self):
        """Monotonic by construction: GitHub issues numbers in order, so a number at or below a
        predecessor's would mean the constant was copied rather than read back."""
        assert THIS_PULL_REQUEST > BOUND_AUTHORIZING_PULL_REQUEST
        assert THIS_PULL_REQUEST > 348
