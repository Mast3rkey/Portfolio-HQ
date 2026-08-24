"""XASSET-0047 -- the post-merge-CI recovery/reconciliation XASSET-0046 SS-F authorized.

WHAT THIS SUITE PROVES
======================

XASSET-0046 closed all seven of its own SS-M conditions and became EFFECTIVE, and its SS-F grant
authorizes EXACTLY ONE recovery/reconciliation unit. This is that unit. Its substantive act is
narrow and mechanical: the operational-authorization mechanism's LIFECYCLE ANCHOR is rebound from
XASSET-0044 / PR #344 -- whose own merge-commit CI failed permanently at the exact merge SHA its
effectivity condition names -- onto this decision and this pull request.

THE ONE RULE THIS SUITE IS BUILT AROUND
=======================================

Three filings in a row were stopped or corrected over the same defect: a claim about IMMUTABLE
HISTORY measured against a reference that MOVES. XASSET-0045 wrote two such assertions and its
merge-commit CI failed on one of them at line 662. XASSET-0046 repaired both, and its own audit
found a third instance it had no authority to touch.

So the rule here is mechanical, not editorial:

  * every claim about history is anchored to an immutable object identity;
  * every claim about live state is one that stays TRUE and NON-VACUOUS when HEAD == origin/main;
  * a detector refuses the moving-reference shape inside any declared historical proof, and is
    itself proved falsifiable against known-bad AND known-good synthetic source;
  * and the declared proofs are RUN, for real, under five simulated repository ref states, each in
    an ISOLATED CLONE -- never a ``git worktree``, which shares the ref namespace.

NOTHING HERE ARMS ANYTHING. No attestation, no lane, no claim, no gate evaluation, no execution,
no results work, and no activation authority of any kind. ``stage_1_executability.executable``
stays false permanently and ``ATTEMPT_1`` stays intact, unclaimed and unconsumed.
"""

from __future__ import annotations

import ast
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
SUITE_PATH = Path(__file__).resolve()

DECISION_ID = "XASSET-0047"
DECISION_RELPATH = (
    "governance/decisions/"
    "XASSET-0047-endpoint-0001-stage-1-post-merge-ci-recovery-reconciliation.md"
)
DECISION_PATH = ROOT / DECISION_RELPATH
AUTHORITY_RELPATH = (
    "governance/decisions/"
    "XASSET-0046-endpoint-0001-stage-1-post-merge-ci-recovery-reauthorization.md"
)
AUTH_MODULE_RELPATH = "level1_stage1_execution_authorization.py"
CORRECTED_ARTIFACT_RELPATH = "test_level1_stage1_post_merge_ci_recovery_authorization.py"
OVERLAP_ARTIFACT_RELPATH = "test_overlap_model_validator.py"
REGISTER_RELPATH = "operations/WORKSTREAMS.yaml"
CATALOG_RELPATH = "governance/decisions.yaml"

# ======================================================================================
# Immutable anchors. Every one was re-derived from live git and live GitHub during the
# filing session and is re-derived from the object store below, never taken on trust.
# ======================================================================================

#: PR #346's base -- PR #345's merge commit, and the head_sha of XASSET-0045's FAILED CI.
PR346_BASE_SHA = "2f8cdebe14925021171b9779453946be1f69b506"
#: PR #346's accepted head -- the exact commit clean DELTA review 4995648329 examined and the
#: exact head principal acceptance 5372996734 named.
PR346_ACCEPTED_HEAD = "0964dc2bd6ab3be8282193f76fa04c764198db0f"
#: PR #346's merge commit -- THIS pull request's own base, and the head_sha of the SUCCESSFUL
#: merge-commit CI that made XASSET-0046 effective.
PR346_MERGE_SHA = "0b76c09f8d1aba01780b4f06fdd692f7393fbfd3"

#: ADDED BY XASSET-0048. THIS unit's own merge -- and where `main` is now. Bound so the shared
#: -field assertions below stay EXACT at both ends once the register's live self-reference
#: lawfully advanced past this unit onto its successor.
XASSET0048_MAIN_SHA = "bb95ed26964b1bc7a2e230c76060fec82752efa1"
#: RE-ANCHORED BY XASSET-0049. This unit's own merge -- XASSET-0047's merge -- is now an
#: IMMUTABLE historical anchor rather than "where main is". Every claim below whose SUBJECT is
#: this unit's own delta is re-anchored onto it, which is exactly the classification
#: XASSET-0046 SS-G.11 requires and the discipline that stopped PRs #344 and #345 being provable.
PR347_MERGE_SHA = "bb95ed26964b1bc7a2e230c76060fec82752efa1"
#: The authorization module's exact bytes AT that merge. Immutable, and therefore a claim that
#: stays true after a lawful successor rebinding moves the live module.
PR347_MODULE_SHA256 = (
    "e5b509ca74734bffea788d4e7499699356395216285e941164ccf21b6159c924"
)
#: The successor that lawfully moved the live anchor off this unit. Bound so the transition is
#: visible at BOTH ends rather than inferred from an inequality.
XASSET0049_DECISION_ID = "XASSET-0049"
#: ADDED BY XASSET-0048. WS-0014's single shared `active_pr` now points at the successor unit,
#: which carries the impossible sentinel ``None`` until GitHub issues its number.
XASSET0048_ACTIVE_PR = 348
#: ADVANCED BY XASSET-0049. The register's SHARED live fields move with every unit; each prior
#: generation's value is retained beside the current one as a negative pin rather than deleted.
XASSET0049_MAIN_SHA = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"
XASSET0049_ACTIVE_PR = 349
#: The tree carried by BOTH the accepted head and the merge -- zero merge drift.
#: ADVANCED BY XASSET-0050. PR #349 merged at `a9414554`, so WS-0014's shared live
#: "where main is now" / "which pull request is live" fields lawfully advanced again under
#: OPS-0001's Active-GitHub-fields rule. XASSET-0050 is a DESIGN-ONLY authorization: it changes
#: no module constant, so `REVIEWED_BASE_SHA` stays XASSET-0049's lawful rebinding base and only
#: the register's shared self-reference moved. Each prior generation's value is retained beside
#: the current one as a NEGATIVE pin rather than deleted, so a silent revert to any finished
#: unit's state still fails. The assertion stays EXACT and is bound at BOTH ends.
XASSET0050_MAIN_SHA = "a941455491cc5e4d3d868775fb6b4b88f0fe2ce3"
#: Committed as an impossible sentinel first, then replaced by the number GitHub actually issued
#: in a fast-forward follow-up commit. Never predicted. Distinct from every prior sentinel.
XASSET0050_ACTIVE_PR = 350
#: ADVANCED BY XASSET-0051. PR #350 merged at `6fd9a697...` and PR #351 (a test-only repair
#: touching none of the eighteen bound paths) then merged at `ea9e74a1...`, so WS-0014's shared
#: live "where main is now" / "which pull request is live" fields lawfully advanced again under
#: OPS-0001's Active-GitHub-fields rule. XASSET-0051 is a DESIGN-ONLY authorization: it changes
#: no module constant, so `REVIEWED_BASE_SHA` stays XASSET-0049's lawful rebinding base and only
#: the register's shared self-reference moved. Each prior generation's value is retained beside
#: the current one as a NEGATIVE pin rather than deleted, so a silent revert to any finished
#: unit's state still fails. The assertion stays EXACT and is bound at BOTH ends.
XASSET0051_MAIN_SHA = "ea9e74a1f4224a78df2416db9c872b0c5812894b"
#: Committed as an impossible sentinel first (-51), then replaced by the number GitHub actually
#: issued in a fast-forward follow-up commit. Never predicted. Distinct from every prior sentinel.
XASSET0051_ACTIVE_PR = 352
#: ADVANCED BY XASSET-0052. PR #352 merged at `8def8bd0...`, so WS-0014's shared live
#: "where main is now" / "which pull request is live" fields lawfully advanced again under
#: OPS-0001's Active-GitHub-fields rule. XASSET-0052 is a DESIGN-ONLY authorization: it changes
#: no module constant, so `REVIEWED_BASE_SHA` stays XASSET-0049's lawful rebinding base and only
#: the register's shared self-reference moved. Each prior generation's value is retained beside
#: the current one as a NEGATIVE pin rather than deleted, so a silent revert to any finished
#: unit's state still fails. The assertion stays EXACT and is bound at BOTH ends.
XASSET0052_MAIN_SHA = "8def8bd096b4edecbf10fc20870a6d03b6cb56fe"
#: Committed as an impossible sentinel first (-52), then replaced by the number GitHub actually
#: issued in a fast-forward follow-up commit. Never predicted. Distinct from every prior sentinel.
XASSET0052_ACTIVE_PR = 353
#: ADVANCED BY XASSET-0053. PR #353 merged at `cc1d1b62...`, so WS-0014's shared live
#: "where main is now" / "which pull request is live" fields lawfully advanced again under
#: OPS-0001's Active-GitHub-fields rule. XASSET-0053 is a DESIGN-ONLY authorization: it changes
#: no module constant, so `REVIEWED_BASE_SHA` stays XASSET-0049's lawful rebinding base and only
#: the register's shared self-reference moved. Each prior generation's value is retained beside
#: the current one as a NEGATIVE pin rather than deleted, so a silent revert to any finished
#: unit's state still fails. The assertion stays EXACT and is bound at BOTH ends.
XASSET0053_MAIN_SHA = "cc1d1b62b8b48c7123b73e05e7ea04af89c89cd6"
#: Committed as an impossible sentinel first (-53), then replaced by the number GitHub actually
#: issued in a fast-forward follow-up commit. Never predicted. Distinct from every prior sentinel.
XASSET0053_ACTIVE_PR = 354
#: ADVANCED BY XASSET-0054. PR #354 merged at `683c3246...`, making XASSET-0053 EFFECTIVE, so
#: WS-0014's shared live "where main is now" / "which pull request is live" fields lawfully
#: advanced again under OPS-0001's Active-GitHub-fields rule. XASSET-0054 is the IMPLEMENTATION
#: unit XASSET-0053 SS-C authorized: it lawfully changes exactly one of the eighteen bound paths
#: (`level1_stage1_execution_authorization.py`) and re-pins NOTHING -- `REVIEWED_BASE_SHA` stays
#: XASSET-0049's lawful rebinding base, and the resulting digest drift is the designed fail-closed
#: hand-off to the separately authorized step-8-equivalent rebinding unit. Each prior generation's
#: value is retained beside the current one as a NEGATIVE pin rather than deleted, so a silent
#: revert to any finished unit's state still fails. The assertion stays EXACT and bound at BOTH ends.
XASSET0054_MAIN_SHA = "683c324629544a84d2cf75ebca37325e3375c479"
#: Committed as an impossible sentinel first (-54), then replaced by the number GitHub issued
#: issued in a fast-forward follow-up commit. Never predicted. Distinct from every prior sentinel.
XASSET0054_ACTIVE_PR = 355
XASSET0054_BRANCH = "claude/xasset-0054-parser-contract-correction-h3nq7p"
PR346_MERGE_TREE = "a2a05c8308b3d6efe27e2517d0859934c65660a6"

#: XASSET-0046's own completed lifecycle evidence, preserved by exact identity.
PR346_SUPERSEDED_FULL_REVIEW = "4995297886"
PR346_FINAL_CLEAN_REVIEW = "4995648329"
PR346_PRINCIPAL_ACCEPTANCE = "5372996734"
PR346_POST_MERGE_VERIFICATION = "5373011071"
PR346_FINAL_CLOSURE = "5373106008"
PR346_MERGE_CI_RUN = "32507225897"
PR346_MERGE_CI_JOB = "96849995233"

#: PR #345's closed range -- the range XASSET-0046's two corrected guards are anchored to, and
#: which SS-G.2 requires this unit to PRESERVE and INDEPENDENTLY RE-PROVE.
PR345_BASE_SHA = "f5dedce1d1d3116ed8a6845c4447388c85a5414c"
PR345_ACCEPTED_HEAD = "61e629f0f655ce8ca4ccd7eaa370d132d593515c"
PR345_MERGE_TREE = "e5eb890550d55aa74c7430871f176761526b1ecf"
PR345_CORRECTION_OLD_BLOB = "5b916d881ed83db164233091863f2af87fa50828"
PR345_CORRECTION_NEW_BLOB = "536bf08bb7db81ffad15dcfa1de6e9ce4fca4899"

#: PR #344's closed range -- the range the guard XASSET-0045 repaired in
#: ``test_overlap_model_validator.py`` is anchored to, which SS-G.2 likewise protects.
PR344_BASE_SHA = "0709d2f05ab031ecb6f69c40465ed4a227983aed"
PR344_ACCEPTED_HEAD = "9c2821ab9e0e0dff09f5a03da5a6034775b00750"

#: Both permanently failed merge-commit CI runs. Immutable adverse history: never re-run in
#: place, relabelled, deleted, suppressed, waived, or represented as successful.
XASSET0044_FAILED_CI_RUN = "32439614683"
XASSET0044_FAILED_CI_JOB = "96647501864"
XASSET0045_FAILED_CI_RUN = "32490789238"
XASSET0045_FAILED_CI_JOB = "96797667282"
#: Both auditable stop records, on their own pull requests.
XASSET0044_STOP_COMMENT = "5364490220"
XASSET0045_STOP_COMMENT = "5371158269"

#: The two decision files XASSET-0047 adds to the trust boundary, and the exact prior size.
LOAD_BEARING_SIZE_BEFORE = 14
LOAD_BEARING_SIZE_AFTER = 16
XASSET_0047_BOUNDARY_ADDITIONS = (AUTHORITY_RELPATH, DECISION_RELPATH)

#: The frozen universe. Unchanged by this unit, and asserted so rather than assumed.
UNIVERSE_SHA256 = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
UNIVERSE_COUNT = 680
UNIVERSE_CELL_COUNT = 48

#: Files whose bytes XASSET-0046 SS-G.9 requires this unit to preserve UNCHANGED. Compared
#: against PR346_MERGE_SHA -- an immutable commit that is this pull request's own base -- so the
#: comparison neither moves nor collapses to empty once this branch merges.
FROZEN_AGAINST_BASE_RELPATHS = (
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    "level1_construction_universe_closure_validator.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    OVERLAP_ARTIFACT_RELPATH,
    "allocate.py",
    "margin_state.py",
    "levels.py",
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
    "governance/decisions/XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md",
    "governance/decisions/XASSET-0044-endpoint-0001-stage-1-post-correction-operational-rebinding.md",
    "governance/decisions/XASSET-0045-endpoint-0001-stage-1-post-merge-ci-recovery-authorization.md",
    AUTHORITY_RELPATH,
)

#: The functions in THIS suite whose SUBJECT is immutable history. None may consult a moving
#: reference -- not in an assertion, and not in a skip guard, because a historical proof that a
#: live reference can silence is not a proof of history.
HISTORICAL_PROOF_FUNCTIONS = frozenset({
    "_assert_pr346_closed_range_facts",
    "test_the_accepted_head_is_the_second_parent_of_this_units_base",
    "test_the_authority_merged_with_zero_drift",
    "test_the_preserved_pr345_range_still_carries_its_enabling_correction",
    "test_the_preserved_pr344_range_still_carries_its_enabling_correction",
    "test_every_frozen_path_is_byte_identical_to_this_units_base",
    "test_the_two_boundary_additions_did_not_exist_at_the_base",
})

#: String literals that name a MOVING reference. Deliberately a small, explicit, closed set of
#: REFERENCE NAMES: a broad heuristic would flag the prose and the AST checks that must
#: legitimately NAME these references in order to refuse them.
#:
#: ``merge-base`` is deliberately ABSENT -- it is a subcommand, not a reference, and
#: ``merge-base(<pinned>, <pinned>)`` is fully determined by immutable objects.
MOVING_REFERENCE_LITERALS = frozenset({
    "HEAD", "origin/main", "origin/HEAD", "@{u}", "@{upstream}", "main", "refs/remotes/origin/main",
})

#: Git subcommands that write refs. A simulation must never run one against the real repository.
REF_MUTATING_GIT_SUBCOMMANDS = frozenset(
    {"update-ref", "branch", "reset", "checkout", "worktree", "switch"}
)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _blob_sha256_at(commit: str, relpath: str) -> str:
    """SHA-256 of a tracked path's EXACT bytes at an immutable commit.

    ADDED BY XASSET-0049. Historical module-identity claims are re-anchored onto closed commits
    rather than onto the working tree, so a lawful successor rebinding cannot falsify a
    predecessor's own accurate record of what it produced.
    """
    blob = subprocess.run(
        ["git", "show", f"{commit}:{relpath}"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    return hashlib.sha256(blob).hexdigest()


def _commit_exists(sha: str, repo_root: Path = ROOT) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=repo_root, capture_output=True, text=True,
    ).returncode == 0


def _range_is_present(*shas: str, repo_root: Path = ROOT) -> bool:
    """Whether ANY of the named anchors is in this checkout.

    Deliberately ``any``, not ``all``. A checkout holding none of them is genuinely truncated
    and is an environment precondition; a checkout holding some but not all is a REFUSAL inside
    the proof, never a skip, so one unresolvable object cannot silence the whole thing.
    """
    return any(_commit_exists(sha, repo_root) for sha in shas)


def _blob_at(commit: str, relpath: str, repo_root: Path = ROOT) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"{commit}:{relpath}"],
        cwd=repo_root, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _flat(text: str) -> str:
    """Collapse all runs of whitespace to single spaces.

    The decision is hard-wrapped prose, so an exact phrase can straddle a newline. Matching the
    flattened text keeps every assertion an EXACT phrase match while making it insensitive to
    where a paragraph happens to wrap. Deliberately not a weakening: the full phrase must still
    be present, in order, verbatim.
    """
    return " ".join(text.split())


def _section(text: str, letter: str) -> str:
    """The body of one lettered Decision subsection, flattened.

    Scoping an assertion to the section where a claim is OPERATIVE is what makes it
    mutation-sensitive: a phrase that also appears in a summary elsewhere can no longer satisfy
    a check on the section that actually carries the rule.
    """
    marker = f"\n### {letter}. "
    start = text.index(marker)
    rest = text[start + len(marker):]
    nxt = rest.find("\n### ")
    end = len(rest) if nxt == -1 else nxt
    return _flat(rest[:end])


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_flat_lower(decision_text: str) -> str:
    return _flat(decision_text).lower()


@pytest.fixture(scope="module")
def register_text() -> str:
    return (ROOT / REGISTER_RELPATH).read_text(encoding="utf-8")


# ======================================================================================
# 1 -- The authority: XASSET-0046's own closed range, re-derived from the object store
# ======================================================================================


def _assert_pr346_closed_range_facts(
    *,
    base_sha: str = PR346_BASE_SHA,
    accepted_head: str = PR346_ACCEPTED_HEAD,
    merge_sha: str = PR346_MERGE_SHA,
    merge_tree: str = PR346_MERGE_TREE,
    repo_root: Path = ROOT,
) -> dict[str, str]:
    """Prove PR #346's merge identity and return its exact change set, by status.

    Every anchor is an explicit argument and every one is an immutable object. Nothing here
    reads ``HEAD``, ``origin/main``, ``merge-base``, the working tree, or any other reference
    that moves as the repository advances -- so the facts proved are invariant on a feature
    branch, on merged ``main`` where ``HEAD == origin/main``, after ``main`` advances, and when
    unrelated later commits exist.

    An unresolvable object is a REFUSAL, never a skip; the caller decides whether a genuinely
    truncated checkout is an environment precondition (:func:`_range_is_present`).
    """
    for label, sha in (
        ("base", base_sha), ("accepted head", accepted_head), ("merge", merge_sha),
    ):
        assert _commit_exists(sha, repo_root), f"PR #346's {label} {sha} is not resolvable"

    def _g(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=repo_root, capture_output=True, text=True, check=True,
        ).stdout.strip()

    # -- exact two-parent ordering: base first, accepted head second ----------------------
    parents = _g("rev-list", "--parents", "-n", "1", merge_sha).split()
    assert parents[0] == merge_sha, parents
    assert len(parents[1:]) == 2, f"expected exactly two parents, got {parents[1:]}"
    assert parents[1] == base_sha, f"first parent is {parents[1]}, expected {base_sha}"
    assert parents[2] == accepted_head, (
        f"second parent is {parents[2]}, expected {accepted_head}"
    )

    # -- byte-identical accepted-head and merge trees: zero merge drift -------------------
    assert _g("rev-parse", f"{merge_sha}^{{tree}}") == merge_tree
    assert _g("rev-parse", f"{accepted_head}^{{tree}}") == merge_tree

    # -- the exact change set over the closed range ---------------------------------------
    rows = [
        line.split("\t")
        for line in _g("diff", "--name-status", base_sha, accepted_head).splitlines()
        if line.strip()
    ]
    changed = {path: status for status, path in rows}
    assert changed, "the closed range is empty -- the proof would be vacuous"
    return changed


class TestTheAuthorityIsRealAndClosed:
    def test_the_accepted_head_is_the_second_parent_of_this_units_base(self):
        """This unit's base IS XASSET-0046's merge. Proven, not assumed."""
        if not _range_is_present(PR346_BASE_SHA, PR346_ACCEPTED_HEAD, PR346_MERGE_SHA):
            pytest.skip("PR #346's closed range is not present in this checkout")
        _assert_pr346_closed_range_facts()
        # RE-ANCHORED BY XASSET-0049, unchanged in KIND. ``A.REVIEWED_BASE_SHA`` is a LIVE value
        # naming whichever unit currently holds the anchor; this unit's own base is IMMUTABLE
        # history and is now carried by the constant that records it. Both equalities are kept.
        assert A.PRIOR_RECONCILIATION_MERGE_BASE == PR346_MERGE_SHA
        assert A.RECOVERY_AUTHORIZING_MERGE_SHA == PR346_MERGE_SHA

    def test_the_authority_merged_with_zero_drift(self):
        if not _range_is_present(PR346_ACCEPTED_HEAD, PR346_MERGE_SHA):
            pytest.skip("PR #346's closed range is not present in this checkout")
        assert _git("rev-parse", f"{PR346_MERGE_SHA}^{{tree}}") == PR346_MERGE_TREE
        assert _git("rev-parse", f"{PR346_ACCEPTED_HEAD}^{{tree}}") == PR346_MERGE_TREE

    @pytest.mark.parametrize(
        "wrong",
        [
            {"base_sha": PR345_BASE_SHA},
            {"accepted_head": PR345_ACCEPTED_HEAD},
            {"merge_sha": PR346_BASE_SHA},
            {"merge_tree": PR345_MERGE_TREE},
        ],
    )
    def test_each_anchor_of_the_closed_range_is_independently_required(self, wrong):
        """Every conjunct is load-bearing: substituting any ONE real-but-wrong anchor fails."""
        if not _range_is_present(PR346_BASE_SHA, PR346_ACCEPTED_HEAD, PR346_MERGE_SHA):
            pytest.skip("PR #346's closed range is not present in this checkout")
        with pytest.raises(AssertionError):
            _assert_pr346_closed_range_facts(**wrong)

    def test_an_unresolvable_anchor_is_a_refusal_not_a_skip(self):
        with pytest.raises(AssertionError):
            _assert_pr346_closed_range_facts(base_sha="0" * 40)

    def test_the_authority_lifecycle_evidence_is_preserved_by_exact_identity(
        self, decision_text
    ):
        for token in (
            PR346_SUPERSEDED_FULL_REVIEW,
            PR346_FINAL_CLEAN_REVIEW,
            PR346_PRINCIPAL_ACCEPTANCE,
            PR346_POST_MERGE_VERIFICATION,
            PR346_FINAL_CLOSURE,
            PR346_MERGE_CI_RUN,
            PR346_MERGE_CI_JOB,
        ):
            assert token in decision_text, token

    def test_the_decision_records_the_authority_as_effective(self, decision_flat_lower):
        assert "conditions closed — **effective**" in decision_flat_lower
        assert "`xasset-0046`** | all seven" in decision_flat_lower


# ======================================================================================
# 2 -- The rebinding: exact closed transitions, bound at BOTH ends
# ======================================================================================


class TestTheAnchorMovedExactly:
    def test_the_authorizing_decision_is_this_unit(self):
        """RE-ANCHORED BY XASSET-0049, unchanged in KIND.

        This unit really WAS the anchor, and its identity is preserved rather than erased: the
        successor bound it into its own ``PRIOR_RECONCILIATION_*`` family precisely so this claim
        stays provable. Asserting the LIVE anchor still equals this unit would assert that no
        lawful successor may ever exist, which is not what this test was written to protect.
        """
        assert A.PRIOR_RECONCILIATION_DECISION == DECISION_ID
        assert A.PRIOR_RECONCILIATION_PULL_REQUEST == THIS_PULL_REQUEST
        assert A.PRIOR_RECONCILIATION_MERGE_SHA == PR347_MERGE_SHA
        assert A.PRIOR_RECONCILIATION_DECISION != "XASSET-0044"
        # The live anchor moved to the successor, and to nothing else.
        assert A.AUTHORIZING_DECISION == XASSET0049_DECISION_ID
        assert A.AUTHORIZING_DECISION not in A.PERMANENTLY_INEFFECTIVE_DECISIONS

    def test_the_reviewed_base_is_the_authoritys_merge_and_not_the_stopped_ones(self):
        """RE-ANCHORED BY XASSET-0049 onto the constants that now carry this unit's own base.

        The KIND of claim is unchanged: this unit branched from its own authority's merge and
        from neither stopped lifecycle's base. That is immutable history and stays asserted. The
        LIVE ``REVIEWED_BASE_SHA`` now belongs to the successor, and is checked separately below
        against its own authority -- so neither claim is dropped.
        """
        assert A.PRIOR_RECONCILIATION_MERGE_BASE == A.RECOVERY_AUTHORIZING_MERGE_SHA
        assert A.PRIOR_RECONCILIATION_MERGE_BASE == PR346_MERGE_SHA
        assert A.PRIOR_RECONCILIATION_MERGE_BASE != PR344_BASE_SHA
        assert A.PRIOR_RECONCILIATION_MERGE_BASE != PR345_BASE_SHA
        assert A.PRIOR_RECONCILIATION_MERGE_BASE != PR346_BASE_SHA
        # The successor's own base is likewise neither stopped lifecycle's, and is bound to its
        # own authority by EQUALITY (XASSET-0048 SS-F.2), not by descent.
        assert A.REVIEWED_BASE_SHA == A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA
        assert A.REVIEWED_BASE_SHA != PR344_BASE_SHA
        assert A.REVIEWED_BASE_SHA != PR345_BASE_SHA

    def test_the_authorizing_pull_request_is_neither_stopped_pull_request(self):
        assert A.AUTHORIZING_PULL_REQUEST != 344
        assert A.AUTHORIZING_PULL_REQUEST != 345
        assert A.AUTHORIZING_PULL_REQUEST != 346
        assert A.AUTHORIZING_PULL_REQUEST not in A.PERMANENTLY_INEFFECTIVE_PULL_REQUESTS

    def test_the_predecessor_and_package_identities_are_untouched(self):
        """A rebinding that repointed these would be overloading, not rebinding."""
        assert A.PREDECESSOR_DECISION == "XASSET-0028"
        assert A.PREDECESSOR_MERGE_SHA == "c51e94609eff7ede2bdfa084844d59b8347561e5"
        assert A.HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION == "XASSET-0029"
        assert A.HISTORICAL_OPERATIONAL_AUTHORIZATION_PULL_REQUEST == 328
        assert A.PACKAGE_AUTHORIZING_DECISION == "XASSET-0036"
        assert A.PACKAGE_AUTHORIZING_PULL_REQUEST == 335
        assert A.EXECUTABLE_PACKAGE_PULL_REQUEST == 336
        assert A.PRIOR_SUCCESSOR_REBINDING_DECISION == "XASSET-0037"
        assert A.CORRECTION_AUTHORIZING_DECISION == "XASSET-0041"
        assert A.CORRECTED_MODULE_DECISION == "XASSET-0042"
        assert A.REBINDING_AUTHORIZING_DECISION == "XASSET-0043"
        assert A.REBINDING_AUTHORIZING_PULL_REQUEST == 343

    def test_the_attempt_identity_is_not_reminted(self):
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

    def test_the_recovery_authority_family_is_its_own_relationship(self):
        assert A.RECOVERY_AUTHORIZING_DECISION == "XASSET-0046"
        assert A.RECOVERY_AUTHORIZING_PULL_REQUEST == 346
        assert A.RECOVERY_AUTHORIZING_MERGE_SHA == PR346_MERGE_SHA
        assert A.RECOVERY_AUTHORIZING_ACCEPTED_HEAD == PR346_ACCEPTED_HEAD
        assert A.RECOVERY_AUTHORIZING_MERGE_BASE == PR346_BASE_SHA
        # ... and it is NOT any of the identities that already existed.
        distinct = {
            A.PREDECESSOR_DECISION,
            A.HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION,
            A.PACKAGE_AUTHORIZING_DECISION,
            A.PRIOR_SUCCESSOR_REBINDING_DECISION,
            A.CORRECTION_AUTHORIZING_DECISION,
            A.CORRECTED_MODULE_DECISION,
            A.REBINDING_AUTHORIZING_DECISION,
            A.RECOVERY_AUTHORIZING_DECISION,
            A.STOPPED_REBINDING_DECISION,
            A.STOPPED_RECOVERY_AUTHORIZATION_DECISION,
            A.AUTHORIZING_DECISION,
        }
        assert len(distinct) == 11


# ======================================================================================
# 3 -- Both stopped lifecycles: preserved as history, refused as authority
# ======================================================================================


class TestStoppedLifecyclesArePreservedAndRefused:
    def test_both_stopped_identities_are_bound_exactly(self):
        assert A.STOPPED_REBINDING_DECISION == "XASSET-0044"
        assert A.STOPPED_REBINDING_PULL_REQUEST == 344
        assert A.STOPPED_REBINDING_MERGE_SHA == PR345_BASE_SHA
        assert A.STOPPED_REBINDING_ACCEPTED_HEAD == PR344_ACCEPTED_HEAD
        assert A.STOPPED_REBINDING_MERGE_BASE == PR344_BASE_SHA
        assert A.STOPPED_RECOVERY_AUTHORIZATION_DECISION == "XASSET-0045"
        assert A.STOPPED_RECOVERY_AUTHORIZATION_PULL_REQUEST == 345
        assert A.STOPPED_RECOVERY_AUTHORIZATION_MERGE_SHA == PR346_BASE_SHA
        assert A.STOPPED_RECOVERY_AUTHORIZATION_ACCEPTED_HEAD == PR345_ACCEPTED_HEAD
        assert A.STOPPED_RECOVERY_AUTHORIZATION_MERGE_BASE == PR345_BASE_SHA

    def test_both_failed_runs_are_retained_by_exact_identity(self):
        assert A.STOPPED_REBINDING_FAILED_CI_RUN == XASSET0044_FAILED_CI_RUN
        assert A.STOPPED_REBINDING_FAILED_CI_JOB == XASSET0044_FAILED_CI_JOB
        assert A.STOPPED_RECOVERY_AUTHORIZATION_FAILED_CI_RUN == XASSET0045_FAILED_CI_RUN
        assert A.STOPPED_RECOVERY_AUTHORIZATION_FAILED_CI_JOB == XASSET0045_FAILED_CI_JOB
        # ... and each is paired with the exact merge SHA whose CI it is, so the two can never
        # be silently swapped between the two lifecycles.
        assert (XASSET0044_FAILED_CI_RUN, XASSET0044_FAILED_CI_JOB, PR345_BASE_SHA) in (
            A.FAILED_MERGE_COMMIT_CI_RUNS
        )
        assert (XASSET0045_FAILED_CI_RUN, XASSET0045_FAILED_CI_JOB, PR346_BASE_SHA) in (
            A.FAILED_MERGE_COMMIT_CI_RUNS
        )
        assert len(A.FAILED_MERGE_COMMIT_CI_RUNS) == 2

    def test_both_decisions_are_refused_as_authority(self):
        assert A.PERMANENTLY_INEFFECTIVE_DECISIONS == frozenset({"XASSET-0044", "XASSET-0045"})
        assert A.PERMANENTLY_INEFFECTIVE_PULL_REQUESTS == frozenset({344, 345})
        assert A.AUTHORIZING_DECISION not in A.PERMANENTLY_INEFFECTIVE_DECISIONS

    def test_the_decision_forbids_every_disposal_of_the_failed_runs(self, decision_flat_lower):
        for verb in (
            "re-run in place",
            "relabelled successful",
            "deleted",
            "suppressed",
            "waived",
            "described as passing",
        ):
            assert verb in decision_flat_lower, verb
        assert "immutable adverse history" in decision_flat_lower
        assert (
            "neither lifecycle closure may be posted retrospectively" in decision_flat_lower
        )

    def test_both_auditable_stops_are_preserved(self, decision_text):
        assert XASSET0044_STOP_COMMENT in decision_text
        assert XASSET0045_STOP_COMMENT in decision_text

    def test_the_spent_versus_never_vested_distinction_survives(self, decision_flat_lower):
        assert "spent by use" in decision_flat_lower
        assert "never vested" in decision_flat_lower
        assert "`xasset-0043` remains **spent by use**" in decision_flat_lower

    def test_no_stopped_decision_file_was_edited(self):
        """Accepted merged history is untouched, proven against this unit's own immutable base."""
        if not _commit_exists(PR346_MERGE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        for relative in (
            "governance/decisions/"
            "XASSET-0044-endpoint-0001-stage-1-post-correction-operational-rebinding.md",
            "governance/decisions/"
            "XASSET-0045-endpoint-0001-stage-1-post-merge-ci-recovery-authorization.md",
            AUTHORITY_RELPATH,
        ):
            live = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            at_base = hashlib.sha256(
                subprocess.run(
                    ["git", "cat-file", "blob", f"{PR346_MERGE_SHA}:{relative}"],
                    cwd=ROOT, capture_output=True, check=True,
                ).stdout
            ).hexdigest()
            assert live == at_base, relative


# ======================================================================================
# 4 -- The four new refusals, each independently required
# ======================================================================================


class TestTheNewRefusalsAreIndependentlyRequired:
    def test_the_live_configuration_produces_no_anchor_error(self):
        assert A._verify_recovery_lifecycle_anchor("0" * 40) == []

    def test_an_ineffective_decision_is_refused(self, monkeypatch):
        monkeypatch.setattr(A, "AUTHORIZING_DECISION", "XASSET-0044")
        errors = A._verify_recovery_lifecycle_anchor("0" * 40)
        assert any("permanently ineffective" in e for e in errors), errors

    def test_a_stopped_pull_request_is_refused(self, monkeypatch):
        monkeypatch.setattr(A, "AUTHORIZING_PULL_REQUEST", 345)
        errors = A._verify_recovery_lifecycle_anchor("0" * 40)
        assert any("lifecycle that stopped" in e for e in errors), errors

    @pytest.mark.parametrize("failed_merge", [PR345_BASE_SHA, PR346_BASE_SHA])
    def test_a_merge_with_failed_merge_commit_ci_is_refused(self, failed_merge):
        errors = A._verify_recovery_lifecycle_anchor(failed_merge)
        assert any("FAILED merge-commit CI run" in e for e in errors), errors
        assert any("immutable adverse history" in e for e in errors), errors

    def test_canonical_drift_is_refused(self, monkeypatch):
        drifted = dict(A.CANONICAL_PINS)
        drifted[A.CANONICAL_PROTOCOL_RELPATH] = "0" * 64
        monkeypatch.setattr(A, "CANONICAL_PINS", drifted)
        errors = A._verify_recovery_lifecycle_anchor("0" * 40)
        # RE-GROUNDED BY XASSET-0049, NOT WEAKENED. The comparison is byte-for-byte the same one
        # -- effective pins against XASSET-0044's own historical literals -- and it still fires on
        # exactly the same input. Only its stated GROUND changed: it rested on XASSET-0046 SS-G.9's
        # freeze, which no longer governs, and now rests on XASSET-0048 SS-F.7's "only to the
        # extent the rebinding requires", under which XASSET-0049 amends no canonical byte. The
        # assertion is pinned on the refusal's substance rather than on either citation, and the
        # substance is asserted explicitly so a future edit cannot quietly drop the refusal while
        # keeping a plausible sentence.
        assert any("canonical drift" in e for e in errors), errors
        assert any("may not move a canonical byte" in e for e in errors), errors

    def test_the_anchor_check_reads_no_external_source(self):
        """Pure and offline: it must not be silenceable by an unavailable git, GitHub, or clock.

        Proven structurally from the function's own AST, not from its docstring.
        """
        tree = ast.parse((ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8"))
        fn = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "_verify_recovery_lifecycle_anchor"
        )
        called = {
            node.func.attr for node in ast.walk(fn)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        } | {
            node.func.id for node in ast.walk(fn)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        for forbidden in ("run", "commit_parents", "commit_tree", "is_ancestor", "head",
                          "pull_request", "review", "reviews", "issue_comment", "now", "today"):
            assert forbidden not in called, forbidden

    def test_the_refusals_are_wired_into_the_real_public_path(self):
        """A refusal that is never invoked protects nothing."""
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert "errors.extend(_verify_recovery_lifecycle_anchor(merge_sha))" in source
        tree = ast.parse(source)
        caller = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "_verify_successor_rebinding_identity"
        )
        called = {
            node.func.id for node in ast.walk(caller)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        assert "_verify_recovery_lifecycle_anchor" in called


# ======================================================================================
# 5 -- The trust boundary grew additively, by direct membership, and nothing was removed
# ======================================================================================


class TestTrustBoundaryGrewAdditively:
    def test_the_set_grew_from_fourteen_to_sixteen(self):
        """RE-ANCHORED BY XASSET-0049 onto this unit's OWN immutable merge.

        The claim is about what THIS unit did -- fourteen paths in, sixteen out -- which is a fact
        about a closed commit range and is true forever. Reading it off the LIVE tuple made it a
        claim that no lawful successor may ever extend the boundary, which is not what it was
        written to protect and is exactly the moving-reference defect that stopped PRs #344/#345.
        """
        if not _commit_exists(PR347_MERGE_SHA):
            pytest.skip("this unit's own merge is not present in this checkout")
        at_this_merge = _load_bearing_at(PR347_MERGE_SHA)
        assert len(at_this_merge) == LOAD_BEARING_SIZE_AFTER
        assert len(set(at_this_merge)) == LOAD_BEARING_SIZE_AFTER
        assert len(at_this_merge) != LOAD_BEARING_SIZE_BEFORE
        # Additive forever: whatever the live boundary is now, it still CONTAINS all sixteen.
        assert set(at_this_merge) <= set(A.LOAD_BEARING_RELPATHS)

    def test_the_additions_are_exactly_the_two_authority_chain_files(self):
        """RE-ANCHORED BY XASSET-0049 onto this unit's own base->merge range, which is closed.

        THIS unit added exactly two paths. Diffing the live tuple against the base measured a
        different quantity -- every addition by every later unit as well -- so the claim is now
        taken over the immutable range it was always about.
        """
        if not _range_is_present(PR346_MERGE_SHA, PR347_MERGE_SHA):
            pytest.skip("this unit's closed range is not present in this checkout")
        at_base = _load_bearing_at(PR346_MERGE_SHA)
        at_merge = _load_bearing_at(PR347_MERGE_SHA)
        assert len(at_base) == LOAD_BEARING_SIZE_BEFORE
        additions = set(at_merge) - set(at_base)
        assert additions == set(XASSET_0047_BOUNDARY_ADDITIONS)
        # Nothing this unit added has since been removed.
        assert additions <= set(A.LOAD_BEARING_RELPATHS)

    def test_nothing_was_removed(self):
        """Growth is additive. A path traded away is the defect this catches."""
        if not _commit_exists(PR346_MERGE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        assert set(_load_bearing_at(PR346_MERGE_SHA)) <= set(A.LOAD_BEARING_RELPATHS)

    def test_the_two_boundary_additions_did_not_exist_at_the_base(self):
        """The two additions have genuinely DIFFERENT histories, and both are proved.

        At this unit's immutable base, XASSET-0046's decision file already existed -- PR #346
        added it -- while XASSET-0047's did not exist at all. Asserting both directions is what
        distinguishes "this unit added its own decision" from "this unit re-listed a file that
        was already there", which is the difference between binding and citing.
        """
        if not _commit_exists(PR346_MERGE_SHA):
            pytest.skip("this unit's base is not present in this checkout")

        def _exists_at_base(relative: str) -> bool:
            return subprocess.run(
                ["git", "cat-file", "-e", f"{PR346_MERGE_SHA}:{relative}"],
                cwd=ROOT, capture_output=True,
            ).returncode == 0

        assert _exists_at_base(AUTHORITY_RELPATH)
        assert not _exists_at_base(DECISION_RELPATH)
        # ... and neither was inside the trust boundary at the base.
        at_base = _load_bearing_at(PR346_MERGE_SHA)
        assert AUTHORITY_RELPATH not in at_base
        assert DECISION_RELPATH not in at_base

    def test_the_stopped_decisions_own_file_is_retained(self):
        """A stopped lifecycle is not an invalidated one."""
        assert any("XASSET-0044" in relative for relative in A.LOAD_BEARING_RELPATHS)

    def test_the_ineffective_recovery_authorization_is_deliberately_not_bound(self):
        """XASSET-0045 authorizes nothing, so binding it would assert a relationship that
        does not exist. Its ABSENCE is a decision, and is pinned as one."""
        assert not any("XASSET-0045" in relative for relative in A.LOAD_BEARING_RELPATHS)

    @pytest.mark.parametrize("relative", XASSET_0047_BOUNDARY_ADDITIONS)
    def test_each_addition_is_a_real_file_bound_by_membership_not_citation(self, relative):
        assert (ROOT / relative).is_file(), relative
        assert relative in A.LOAD_BEARING_RELPATHS

    def test_every_load_bearing_path_exists(self):
        for relative in A.LOAD_BEARING_RELPATHS:
            assert (ROOT / relative).exists(), relative

    def test_no_results_artifact_is_load_bearing(self):
        assert "stage1_results" not in " ".join(A.LOAD_BEARING_RELPATHS).lower()

    def test_the_authorizing_decisions_own_file_is_inside_the_identity_it_authorizes(self):
        """XASSET-0037 SS-E's principle, applied to the current anchor: an attestation must not
        be able to authenticate while its own governing text stays editable."""
        assert DECISION_RELPATH in A.LOAD_BEARING_RELPATHS
        assert AUTHORITY_RELPATH in A.LOAD_BEARING_RELPATHS

    def test_expected_identity_is_still_derived_from_the_merged_tree(self):
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert "expected values come from the MERGED TREE, not a constant" in source


def _load_bearing_at(commit: str) -> tuple[str, ...]:
    """``LOAD_BEARING_RELPATHS`` as it stood at an IMMUTABLE commit, read from the object store.

    Parsed out of that commit's own module source with ``ast.literal_eval``, never executed and
    never imported, so reading a historical revision cannot run historical code.
    """
    source = subprocess.run(
        ["git", "show", f"{commit}:{AUTH_MODULE_RELPATH}"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "LOAD_BEARING_RELPATHS" for t in node.targets
        ):
            resolved: list[str] = []
            assert isinstance(node.value, ast.Tuple)
            for element in node.value.elts:
                if isinstance(element, ast.Constant):
                    resolved.append(element.value)
                elif isinstance(element, ast.Name):
                    resolved.append(getattr(A, element.id))
                else:  # pragma: no cover - defensive
                    raise AssertionError(f"unexpected member: {ast.dump(element)}")
            return tuple(resolved)
    raise AssertionError(f"LOAD_BEARING_RELPATHS not found at {commit}")


# ======================================================================================
# 6 -- SS-G.9: the frozen surface is byte-identical to this unit's own immutable base
# ======================================================================================


class TestFrozenSurfaceIsUnchanged:
    def test_every_frozen_path_is_byte_identical_to_this_units_base(self):
        """Compared against PR346_MERGE_SHA -- an IMMUTABLE commit that is this pull request's
        own base -- so the comparison neither moves nor collapses to empty once this branch
        merges. That is the whole difference from the guard that stopped PR #345.
        """
        if not _commit_exists(PR346_MERGE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        changed = []
        for relative in FROZEN_AGAINST_BASE_RELPATHS:
            live = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            at_base = hashlib.sha256(
                subprocess.run(
                    ["git", "cat-file", "blob", f"{PR346_MERGE_SHA}:{relative}"],
                    cwd=ROOT, capture_output=True, check=True,
                ).stdout
            ).hexdigest()
            if live != at_base:
                changed.append(relative)
        assert changed == [], changed
        # Non-vacuity: the list is real, and covers every category SS-G.9 names.
        assert len(FROZEN_AGAINST_BASE_RELPATHS) >= 18

    def test_the_universe_is_unchanged(self):
        assert A.CONSTRUCTION_UNIVERSE_SHA256 == UNIVERSE_SHA256
        assert A.CONSTRUCTION_COUNT == UNIVERSE_COUNT
        assert A.CONSTRUCTION_CELL_COUNT == UNIVERSE_CELL_COUNT

    def test_the_universe_regenerates_to_the_same_identity(self):
        import level1_construction_universe_closure_validator as CU

        universe = CU.frozen_construction_universe()
        assert len(universe) == UNIVERSE_COUNT
        assert CU.universe_aggregate_sha256() == UNIVERSE_SHA256

    def test_the_canonical_pins_still_equal_the_pins_the_last_amender_left(self):
        assert A.CANONICAL_PINS == A.XASSET_0044_CANONICAL_PINS
        live = A.live_canonical_hashes()
        for relative, pinned in A.CANONICAL_PINS.items():
            assert live[relative] == pinned, relative

    def test_the_pin_succession_refusal_was_not_relaxed(self):
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        for label in (
            "(PACKAGE_AUTHORIZING_DECISION, XASSET_0036_PACKAGE_CANONICAL_PINS)",
            "(HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION, XASSET_0029_CANONICAL_PINS)",
            "(PREDECESSOR_DECISION, PREDECESSOR_CANONICAL_PINS)",
        ):
            assert label in source, label

    def test_the_outcome_producing_transition_chain_is_untouched(self):
        """Both links of ``package -> successor -> rebound`` survive verbatim: this unit adds no
        third link, because it changes no byte of the derivation surface."""
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert "verify_exact_transition(package_bytes, successor_bytes)" in source
        assert "verify_exact_rebound_transition(successor_bytes, rebound_bytes)" in source
        live = hashlib.sha256(
            (ROOT / A.OUTCOME_PRODUCING_DERIVATION_RELPATH).read_bytes()
        ).hexdigest()
        assert live == A.OUTCOME_PRODUCING_REBOUND_SHA256


# ======================================================================================
# 7 -- SS-G.2: the preserved historical guards, RE-PROVED from repository truth
#
# "Re-proving means running the guards and confirming the property from repository truth --
# never citing this filing's word for it." So these re-derive the facts independently rather
# than importing the predecessor's conclusions.
# ======================================================================================


class TestPreservedGuardsAreReProved:
    def test_the_preserved_pr345_range_still_carries_its_enabling_correction(self):
        """PR #345's merge identity and the enabling correction's exact transition, re-derived.

        Each conjunct is independently required: path equality is not identity, and a status
        alone does not prove which bytes moved where.
        """
        if not _range_is_present(PR345_BASE_SHA, PR345_ACCEPTED_HEAD, PR346_BASE_SHA):
            pytest.skip("PR #345's closed range is not present in this checkout")
        parents = _git("rev-list", "--parents", "-n", "1", PR346_BASE_SHA).split()
        assert parents[1] == PR345_BASE_SHA
        assert parents[2] == PR345_ACCEPTED_HEAD
        assert _git("rev-parse", f"{PR346_BASE_SHA}^{{tree}}") == PR345_MERGE_TREE
        assert _git("rev-parse", f"{PR345_ACCEPTED_HEAD}^{{tree}}") == PR345_MERGE_TREE
        rows = [
            line.split("\t")
            for line in _git(
                "diff", "--name-status", PR345_BASE_SHA, PR345_ACCEPTED_HEAD
            ).splitlines()
            if line.strip()
        ]
        changed = {path: status for status, path in rows}
        assert changed, "the closed range is empty -- the proof would be vacuous"
        assert changed.get(OVERLAP_ARTIFACT_RELPATH) == "M"
        assert _blob_at(PR345_BASE_SHA, OVERLAP_ARTIFACT_RELPATH) == PR345_CORRECTION_OLD_BLOB
        assert (
            _blob_at(PR345_ACCEPTED_HEAD, OVERLAP_ARTIFACT_RELPATH)
            == PR345_CORRECTION_NEW_BLOB
        )

    def test_the_preserved_pr344_range_still_carries_its_enabling_correction(self):
        """The range the guard XASSET-0045 repaired in ``test_overlap_model_validator.py`` is
        anchored to. SS-G.2 protects that repair from reversion on the theory that its
        authorizing decision's authority lapsed."""
        if not _range_is_present(PR344_BASE_SHA, PR344_ACCEPTED_HEAD):
            pytest.skip("PR #344's closed range is not present in this checkout")
        diff = _git(
            "diff", "--name-status", PR344_BASE_SHA, PR344_ACCEPTED_HEAD,
            "--", "governance/decisions",
        )
        rows = [line.split("\t") for line in diff.splitlines() if line.strip()]
        modified = [rest for status, rest in rows if status.startswith("M")]
        assert modified == [
            "governance/decisions/"
            "XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md"
        ], modified

    def test_the_overlap_guard_still_names_its_closed_range_and_no_moving_reference(self):
        source = (ROOT / OVERLAP_ARTIFACT_RELPATH).read_text(encoding="utf-8")
        assert PR344_BASE_SHA in source
        assert PR344_ACCEPTED_HEAD in source

    def test_the_two_corrected_guards_are_still_anchored_to_the_closed_range(self):
        import test_level1_stage1_post_merge_ci_recovery_authorization as corrected

        assert corrected.PR345_BASE_SHA == PR345_BASE_SHA
        assert corrected.PR345_ACCEPTED_HEAD == PR345_ACCEPTED_HEAD
        assert corrected.PR345_MERGE_TREE == PR345_MERGE_TREE
        assert corrected.PR345_CORRECTION_OLD_BLOB == PR345_CORRECTION_OLD_BLOB
        assert corrected.PR345_CORRECTION_NEW_BLOB == PR345_CORRECTION_NEW_BLOB
        for name in (
            "test_the_enabling_correction_was_actually_performed",
            "test_no_protected_path_was_touched_by_this_filing",
            "_assert_pr345_closed_range_facts",
        ):
            assert name in corrected.HISTORICAL_PROOF_FUNCTIONS, name

    def test_the_corrected_guards_still_pass_when_run_for_real(self):
        """The property, confirmed by RUNNING rather than by reading the source."""
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest", "-q", "--no-header",
                "-p", "no:cacheprovider",
                f"{CORRECTED_ARTIFACT_RELPATH}::TestFilingIsGovernancePlusOneEnablingCorrection",
            ],
            cwd=ROOT, capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stdout[-3000:]
        assert " passed" in result.stdout


# ======================================================================================
# 8 -- SS-G.11: the origin/main skip guard, classified and corrected
# ======================================================================================


class TestTheSkipGuardWasClassifiedAndCorrected:
    def test_the_corrected_function_names_no_moving_reference_at_all(self):
        source = (ROOT / CORRECTED_ARTIFACT_RELPATH).read_text(encoding="utf-8")
        fn = next(
            n for n in ast.walk(ast.parse(source))
            if isinstance(n, ast.FunctionDef)
            and n.name == "test_on_merged_main_the_moving_base_collapses_to_head_itself"
        )
        literals = {
            node.value for node in ast.walk(fn)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        assert not (literals & MOVING_REFERENCE_LITERALS), literals & MOVING_REFERENCE_LITERALS

    def test_the_genuine_environment_precondition_was_kept(self):
        """Only the inappropriate guard went. An unresolvable pinned object is still a skip,
        exactly as ``_pr345_range_is_present`` already treats that case."""
        source = (ROOT / CORRECTED_ARTIFACT_RELPATH).read_text(encoding="utf-8")
        fn_src = _function_source(source, "test_on_merged_main_the_moving_base_collapses_to_head_itself")
        assert "PR #344's merge commit is not present in this checkout" in fn_src
        assert "origin/main not resolvable in this environment" not in fn_src

    def test_the_function_is_now_a_declared_historical_proof(self):
        import test_level1_stage1_post_merge_ci_recovery_authorization as corrected

        assert (
            "test_on_merged_main_the_moving_base_collapses_to_head_itself"
            in corrected.HISTORICAL_PROOF_FUNCTIONS
        )

    def test_the_correction_is_reproduced_in_the_decision_by_execution_not_assertion(
        self, decision_flat_lower
    ):
        assert "reproduced by execution before anything was changed" in decision_flat_lower
        assert "origin/main resolvable: no" in decision_flat_lower
        assert "the proof succeeds completely" in decision_flat_lower

    def test_the_authority_for_the_correction_is_stated_not_assumed(self, decision_text):
        g = _section(decision_text, "G")
        assert "re-anchor every historical one" in g
        assert "Guards may be re-anchored and strengthened; they may not be relaxed" in g
        assert "This decision is the authority that covers it" in g
        assert "§G.11 is not relied on alone" in g

    def test_the_classification_is_the_units_own_not_inherited(self, decision_text):
        g = _section(decision_text, "G")
        assert "Classified from the function's own source, not from the paragraph." in g
        assert "The independent evidence agrees with" in g


def _function_source(source: str, name: str) -> str:
    fn = next(
        n for n in ast.walk(ast.parse(source))
        if isinstance(n, ast.FunctionDef) and n.name == name
    )
    return ast.get_source_segment(source, fn) or ""


# ======================================================================================
# 9 -- The structural moving-reference detector, and its own falsifiability proof
# ======================================================================================


def historical_proof_moving_ref_offenders(source: str, names: frozenset[str]) -> list[str]:
    """String literals naming a MOVING reference inside a declared historical proof.

    Module-level and shared, for the same reason the module's own refusals are: a guard
    re-implemented inside its own proof can be disabled without anything noticing.

    Scoped BY NAME, not by shape. The same literal in a function whose subject genuinely is
    live state is legitimate and must not be flagged -- flagging it would teach the wrong rule
    and produce exactly the false positives that get detectors switched off.
    """
    offenders: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.FunctionDef) or node.name not in names:
            continue
        for literal in ast.walk(node):
            if (
                isinstance(literal, ast.Constant)
                and isinstance(literal.value, str)
                and literal.value in MOVING_REFERENCE_LITERALS
            ):
                offenders.append(f"{node.name}: {literal.value!r} at line {literal.lineno}")
    return offenders


def test_no_historical_proof_consults_a_moving_reference():
    assert historical_proof_moving_ref_offenders(
        SUITE_PATH.read_text(encoding="utf-8"), HISTORICAL_PROOF_FUNCTIONS
    ) == []


def test_the_moving_reference_detector_actually_detects():
    """Falsifiability proof, run through the REAL detector against synthetic source.

    Without this, emptying ``MOVING_REFERENCE_LITERALS`` or narrowing the name set leaves a
    guard reporting "clean" because it inspects nothing -- the same silent-disable shape the
    whole defect class is made of.
    """
    names = frozenset({"test_historical"})
    bad_assertion = (
        "def test_historical():\n"
        "    changed = _git('diff', '--name-only', 'origin/main')\n"
        "    assert 'x' in changed\n"
    )
    bad_skip_guard = (
        "def test_historical():\n"
        "    if not _git_ok('rev-parse', 'origin/main'):\n"
        "        pytest.skip('nope')\n"
        "    assert True\n"
    )
    bad_head = (
        "def test_historical():\n"
        "    assert _git('rev-parse', 'HEAD') == PINNED\n"
    )
    good_pinned = (
        "def test_historical():\n"
        "    assert _git('rev-parse', PR346_MERGE_SHA) == PR346_MERGE_SHA\n"
    )
    good_pinned_merge_base = (
        "def test_historical():\n"
        "    base = _git('merge-base', PR346_MERGE_SHA, PR346_MERGE_SHA)\n"
        "    assert base == PR346_MERGE_SHA\n"
    )
    good_out_of_scope = (
        "def test_live_working_tree():\n"
        "    assert _git('diff', '--name-only', 'origin/main') == ''\n"
    )
    assert historical_proof_moving_ref_offenders(bad_assertion, names) != []
    assert historical_proof_moving_ref_offenders(bad_skip_guard, names) != []
    assert historical_proof_moving_ref_offenders(bad_head, names) != []
    assert historical_proof_moving_ref_offenders(good_pinned, names) == []
    assert historical_proof_moving_ref_offenders(good_pinned_merge_base, names) == []
    # Out of scope BY NAME, not by shape.
    assert historical_proof_moving_ref_offenders(good_out_of_scope, names) == []
    # And it genuinely parsed this suite's own real source, rather than something empty.
    real = SUITE_PATH.read_text(encoding="utf-8")
    parsed = {n.name for n in ast.walk(ast.parse(real)) if isinstance(n, ast.FunctionDef)}
    assert HISTORICAL_PROOF_FUNCTIONS <= parsed, HISTORICAL_PROOF_FUNCTIONS - parsed


def test_the_declared_proof_set_is_not_empty_or_narrowed():
    """Coverage pin. Emptying or narrowing the set would leave the detector inspecting nothing
    while still reporting clean."""
    for required in (
        "_assert_pr346_closed_range_facts",
        "test_the_accepted_head_is_the_second_parent_of_this_units_base",
        "test_the_preserved_pr345_range_still_carries_its_enabling_correction",
        "test_every_frozen_path_is_byte_identical_to_this_units_base",
    ):
        assert required in HISTORICAL_PROOF_FUNCTIONS, required
    assert len(HISTORICAL_PROOF_FUNCTIONS) >= 7
    assert "origin/main" in MOVING_REFERENCE_LITERALS
    assert "HEAD" in MOVING_REFERENCE_LITERALS
    # merge-base is a subcommand, not a reference: flagging it would refuse a sound proof.
    assert "merge-base" not in MOVING_REFERENCE_LITERALS


def test_no_declared_historical_proof_reads_the_working_tree_for_its_subject():
    """A working-tree read is a MOVING subject just as surely as ``origin/main`` is.

    This is the instance XASSET-0047's own audit found in XASSET-0046's artifact: a claim about
    what a merged pull request did, measured half against an immutable blob and half against the
    live file. The name detector catches reference NAMES; this catches the other shape.

    The scan itself lives in :func:`working_tree_subject_offenders` at module level and has its
    own falsifiability proof, because an in-test version could be made unreachable while still
    reporting clean -- which is exactly what mutation probe A08 demonstrated.
    """
    offenders = working_tree_subject_offenders(
        SUITE_PATH.read_text(encoding="utf-8"), HISTORICAL_PROOF_FUNCTIONS
    )
    assert offenders == [], offenders


# ======================================================================================
# 10 -- Invariance, proved by RUNNING, in every ref state this branch will pass through
#
# The structural detectors above prove the declared proofs do not NAME a moving reference and
# do not read a moving subject. That is necessary and not sufficient: both are claims about
# source text. This section moves HEAD and origin/main for real and requires the declared
# proofs to pass at each position -- the property that actually failed at PR #345's merge.
#
# Every simulation runs inside an ISOLATED CLONE. ``git worktree`` is never used: it shares the
# ref namespace, so an ``update-ref`` inside one really does move the REAL origin/main. That
# happened once during PR #345's own work and had to be repaired; the shape is refused
# statically below, before any damage.
# ======================================================================================


def real_repo_ref_mutation_offenders(source: str) -> list[str]:
    """Calls in ``source`` that would write a ref in the REAL repository."""
    # A container constructor is a VOCABULARY declaration, not an invocation -- without this
    # the detector flags its own REF_MUTATING_GIT_SUBCOMMANDS definition.
    containers = {"frozenset", "set", "list", "tuple", "dict"}
    offenders: list[str] = []
    for call in (c for c in ast.walk(ast.parse(source)) if isinstance(c, ast.Call)):
        if isinstance(call.func, ast.Name) and call.func.id in containers:
            continue
        literals = {
            a.value for a in ast.walk(call)
            if isinstance(a, ast.Constant) and isinstance(a.value, str)
        }
        if "worktree" in literals:
            offenders.append(f"worktree created at line {call.lineno}")
            continue
        if not (literals & REF_MUTATING_GIT_SUBCOMMANDS):
            continue
        targets_real_repo = any(
            kw.arg == "cwd" and isinstance(kw.value, ast.Name) and kw.value.id == "ROOT"
            for kw in call.keywords
        ) or (
            bool(call.args)
            and isinstance(call.args[0], ast.Name)
            and call.args[0].id == "ROOT"
        )
        if targets_real_repo:
            offenders.append(f"ref-mutating git call against ROOT at line {call.lineno}")
    return offenders


def test_no_simulation_writes_a_ref_in_the_real_repository():
    assert real_repo_ref_mutation_offenders(SUITE_PATH.read_text(encoding="utf-8")) == []


def test_the_ref_mutation_detector_actually_detects():
    """Falsifiability proof, run through the REAL detector."""
    bad_worktree = 'subprocess.run(["git", "worktree", "add", d], cwd=other)'
    bad_update = 'subprocess.run(["git", "update-ref", "HEAD", x], cwd=ROOT)'
    bad_positional = '_git_in(ROOT, "update-ref", "refs/remotes/origin/main", x)'
    clean_kw = 'subprocess.run(["git", "update-ref", "HEAD", x], cwd=clone)'
    clean_positional = '_git_in(clone, "update-ref", "refs/remotes/origin/main", x)'
    vocabulary_only = 'frozenset({"update-ref", "worktree"})'
    assert real_repo_ref_mutation_offenders(bad_worktree) != []
    assert real_repo_ref_mutation_offenders(bad_update) != []
    assert real_repo_ref_mutation_offenders(bad_positional) != []
    assert real_repo_ref_mutation_offenders(clean_kw) == []
    assert real_repo_ref_mutation_offenders(clean_positional) == []
    assert real_repo_ref_mutation_offenders(vocabulary_only) == []
    real = SUITE_PATH.read_text(encoding="utf-8")
    assert len([c for c in ast.walk(ast.parse(real)) if isinstance(c, ast.Call)]) > 150


def _git_in(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _live_ref(name: str) -> str | None:
    """Resolve a ref in the REAL repository, READ-ONLY.

    Used ONLY to build simulated states and to prove the simulations leave the real refs
    undisturbed. Never asserted to equal a historical constant -- that inverse deadlock is what
    DELTA review 4993351528 found on PR #345.
    """
    result = subprocess.run(
        ["git", "rev-parse", name], cwd=ROOT, capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


#: This branch's own current commit, resolved live. Used ONLY to build simulated ref states.
_LOCAL_HEAD_FOR_SIMULATION = _live_ref("HEAD") or PR346_MERGE_SHA

_SIM_ENV = {
    "GIT_AUTHOR_NAME": "sim", "GIT_AUTHOR_EMAIL": "sim@sim",
    "GIT_COMMITTER_NAME": "sim", "GIT_COMMITTER_EMAIL": "sim@sim",
}


def _working_clone(tmp_path: Path) -> Path:
    dst = tmp_path / "working-clone"
    result = subprocess.run(
        ["git", "clone", "--quiet", "--shared", str(ROOT), str(dst)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        pytest.skip(f"could not create an isolated working clone: {result.stderr.strip()}")
    return dst


def _commit_on_top(repo: Path, parent: str, message: str) -> str:
    """An empty-delta commit on top of ``parent``, built with plumbing inside ``repo``."""
    tree = _git_in(repo, "rev-parse", f"{parent}^{{tree}}")
    return subprocess.run(
        ["git", "commit-tree", tree, "-p", parent, "-m", message],
        cwd=repo, capture_output=True, text=True, check=True,
        env={**os.environ, **_SIM_ENV},
    ).stdout.strip()


#: The real-repository proofs whose behaviour must not depend on where HEAD or origin/main
#: point. Run as a nested pytest inside an isolated clone under each ref state below.
#: Deliberately does NOT include the outer parametrized regression itself -- a recursive
#: selection would spawn clones inside clones and prove nothing about ref position.
REF_STATE_SENSITIVE_TESTS = (
    "TestTheAuthorityIsRealAndClosed::"
    "test_the_accepted_head_is_the_second_parent_of_this_units_base",
    "TestTheAuthorityIsRealAndClosed::test_the_authority_merged_with_zero_drift",
    "TestPreservedGuardsAreReProved::"
    "test_the_preserved_pr345_range_still_carries_its_enabling_correction",
    "TestPreservedGuardsAreReProved::"
    "test_the_preserved_pr344_range_still_carries_its_enabling_correction",
    "TestFrozenSurfaceIsUnchanged::test_every_frozen_path_is_byte_identical_to_this_units_base",
    "TestTrustBoundaryGrewAdditively::test_the_additions_are_exactly_the_two_authority_chain_files",
    "TestTrustBoundaryGrewAdditively::test_the_two_boundary_additions_did_not_exist_at_the_base",
    "test_no_historical_proof_consults_a_moving_reference",
)

#: Every ref position this branch will actually pass through, named for what it isolates.
#: ``merged_main`` is the state that broke PR #345's assertions; the two "later" states are what
#: ``main`` becomes once THIS pull request, and then anything after it, merges.
REF_STATES = (
    "branch",
    "merged_main",
    "later_main",
    "head_equals_origin_main_later",
    "unrelated_later_commits",
)


@pytest.mark.parametrize("ref_state", REF_STATES)
def test_declared_proofs_pass_under_every_real_repository_ref_state(tmp_path, ref_state):
    """Run the declared proofs for real, under each ref state, and require them to pass.

    The WORKING TREE is always this branch's content -- every file under examination is copied
    in from the working tree, so the regression tests the code being reviewed rather than the
    previous commit. Only ``HEAD`` and ``origin/main`` move, which isolates ref position as the
    single variable.
    """
    if not _range_is_present(PR346_BASE_SHA, PR346_ACCEPTED_HEAD, PR346_MERGE_SHA):
        pytest.skip("this unit's closed range is not present in this checkout")
    clone = _working_clone(tmp_path)
    _git_in(clone, "checkout", "--quiet", "--detach", _LOCAL_HEAD_FOR_SIMULATION)
    for relative in (
        SUITE_PATH.name,
        CORRECTED_ARTIFACT_RELPATH,
        AUTH_MODULE_RELPATH,
        DECISION_RELPATH,
    ):
        destination = clone / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)

    # A genuine feature-branch head: this session's own commit when it has one, and a
    # synthesized commit on top of the base when it does not. Taking the live HEAD on faith
    # would silently degrade the ``branch`` state into ``merged_main`` before this branch's
    # first commit -- the "still parametrised but no longer testing anything" shape the
    # structural pins below exist to refuse.
    branch_head = (
        _LOCAL_HEAD_FOR_SIMULATION
        if _LOCAL_HEAD_FOR_SIMULATION != PR346_MERGE_SHA
        else _commit_on_top(clone, PR346_MERGE_SHA, "feature branch commit")
    )

    if ref_state == "branch":
        head, main = branch_head, PR346_MERGE_SHA
    elif ref_state == "merged_main":
        head = main = PR346_MERGE_SHA
    elif ref_state == "later_main":
        head = branch_head
        main = _commit_on_top(clone, PR346_MERGE_SHA, "later main")
    elif ref_state == "head_equals_origin_main_later":
        head = main = _commit_on_top(clone, PR346_MERGE_SHA, "later main, checked out")
    else:
        main = PR346_MERGE_SHA
        for n in range(3):
            main = _commit_on_top(clone, main, f"unrelated later commit {n}")
        head = branch_head

    # Move the refs WITHOUT touching the working tree, so the files under test stay this
    # branch's own while ``git rev-parse`` reports the simulated state.
    _git_in(clone, "update-ref", "HEAD", head)
    _git_in(clone, "update-ref", "refs/remotes/origin/main", main)
    assert _git_in(clone, "rev-parse", "HEAD") == head
    assert _git_in(clone, "rev-parse", "origin/main") == main

    # Structural pins: each state must genuinely be the state it claims to be.
    if ref_state in ("later_main", "head_equals_origin_main_later", "unrelated_later_commits"):
        assert main != PR346_MERGE_SHA, f"{ref_state} must advance past this unit's base"
    if ref_state in ("merged_main", "head_equals_origin_main_later"):
        assert head == main, f"{ref_state} must place HEAD at origin/main"
    if ref_state in ("branch", "later_main", "unrelated_later_commits"):
        assert head != main, f"{ref_state} must place HEAD off origin/main"

    node_ids = [f"{SUITE_PATH.name}::{name}" for name in REF_STATE_SENSITIVE_TESTS]
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider", *node_ids],
        cwd=clone, capture_output=True, text=True,
    )
    assert result.returncode == 0, (
        f"ref state {ref_state!r} (HEAD={head}, origin/main={main}) broke the declared "
        f"proofs:\n{result.stdout[-4000:]}\n{result.stderr[-2000:]}"
    )
    # The nested run must have actually executed the selected tests, not collected zero.
    assert " passed" in result.stdout, result.stdout[-2000:]


def test_the_simulations_leave_the_real_repository_refs_undisturbed(tmp_path):
    """Before/after invariant on the REAL refs, WITHOUT requiring either to equal any
    historical commit -- that inverse deadlock is what DELTA review 4993351528 found."""
    before = (_live_ref("HEAD"), _live_ref("origin/main"))
    clone = _working_clone(tmp_path)
    _git_in(clone, "update-ref", "refs/remotes/origin/main", PR346_BASE_SHA)
    assert _git_in(clone, "rev-parse", "origin/main") == PR346_BASE_SHA
    after = (_live_ref("HEAD"), _live_ref("origin/main"))
    assert before == after, (before, after)
    # Non-vacuity: the real refs actually resolved, so this is a comparison, not two Nones.
    assert before[0] is not None


# ======================================================================================
# 11 -- The decision's operative claims, pinned at the sentence that CARRIES each rule
#
# Pinned per-section rather than by bare ``phrase in text``. That looser shape is a
# recorded miss class in this programme: a phrase occurring three times survives mutating
# one occurrence, and identity presence without the operative sentence lets a preservation
# clause be dropped while both identities survive.
# ======================================================================================


class TestTheDecisionsOperativeClaims:
    def test_the_determination_is_named(self, decision_text):
        a = _section(decision_text, "A")
        assert "`SUCCESSOR_LIFECYCLE_ANCHOR_REBOUND`" in a
        assert "adds **zero activation authority of any kind**" in a

    def test_the_old_anchor_is_recorded_as_permanently_unusable(self, decision_text):
        b = _section(decision_text, "B")
        assert "**Both remain immutable adverse history.**" in b
        assert "excludes *\"a run against any other commit.\"*" in b
        assert "`XASSET-0043` remains **spent by use**" in b
        assert "`XASSET-0045`'s grant **never vested**" in b
        assert "its sole authority is `XASSET-0046` §F" in b

    @pytest.mark.parametrize(
        "identity",
        [
            "f5dedce1d1d3116ed8a6845c4447388c85a5414c",
            "2f8cdebe14925021171b9779453946be1f69b506",
            XASSET0044_FAILED_CI_RUN,
            XASSET0044_FAILED_CI_JOB,
            XASSET0045_FAILED_CI_RUN,
            XASSET0045_FAILED_CI_JOB,
            XASSET0044_STOP_COMMENT,
            XASSET0045_STOP_COMMENT,
        ],
    )
    def test_every_adverse_identity_is_carried_in_the_section_that_records_it(
        self, decision_text, identity
    ):
        assert identity in _section(decision_text, "B"), identity

    def test_the_complete_moved_list_is_exhaustive_and_named(self, decision_text):
        d = _section(decision_text, "D")
        for constant in (
            "`AUTHORIZING_DECISION`",
            "`AUTHORIZING_PULL_REQUEST`",
            "`REVIEWED_BASE_SHA`",
            "`LOAD_BEARING_RELPATHS`",
        ):
            assert constant in d, constant
        assert "**14 → 16**" in d
        assert "**The pull-request number was never guessed.**" in d
        assert "an impossible pull-request number that can never validate" in d
        assert "`XASSET-0044`'s own decision file **stays**" in d
        assert "decision file is deliberately **not** added" in d

    def test_the_mechanism_is_recorded_as_stricter_never_more_permissive(self, decision_text):
        e = _section(decision_text, "E")
        assert "It is measurably stricter" in e
        assert "**four** new refusals" in e
        assert "Verifying a stopped lifecycle is not treating it as effective." in e

    def test_strict_necessity_and_the_canonical_freeze_are_argued_not_asserted(
        self, decision_text
    ):
        f = _section(decision_text, "F")
        assert "**That is forbidden, not merely unnecessary.**" in f
        assert "must be preserved unchanged*" in f
        assert "**The residual tension is disclosed rather than smoothed over.**" in f
        assert "no authority to reword a frozen canonical input" in f

    def test_the_withheld_authority_is_absolute_and_complete(self, decision_text):
        i = _section(decision_text, "I")
        for forbidden in (
            "renewed readiness verification",
            "renewed drift verification",
            "**Step 11**",
            "attestation",
            "**arm** Stage 1",
            "**claim** or consume `ATTEMPT_1`",
            "evaluate any gate",
            "`stage1_results.yaml`",
            "protected `RISK` evidence",
        ):
            assert forbidden in i, forbidden
        assert "**Completing this unit authorizes no further unit**" in i
        assert "granted exactly one, and this is it" in i

    def test_effectivity_is_conjunctive_and_names_the_exact_merge_sha_rule(self, decision_text):
        m = _section(decision_text, "M")
        assert "**None is individually sufficient.**" in m
        assert (
            "**successful merge-commit CI whose `head_sha` is the exact merge SHA**" in m
        )
        assert "not a run against any other commit" in m
        assert "**Merging this arms nothing.**" in m
        for step in ("1.", "2.", "3.", "4.", "5.", "6.", "7."):
            assert step in m, step

    def test_the_carried_forward_observations_are_not_authority(self, decision_text):
        k = _section(decision_text, "K")
        assert "recorded, not acted on" in _flat(decision_text)
        assert "Neither is authority on its own" in k
        assert "may be acted on by citing this section alone" in k
        assert "XASSET-0037" in k

    def test_no_xasset_identifier_beyond_this_one_is_named(self, decision_text):
        """Mutation pin: naming XASSET-0048 would silently pre-authorize a successor."""
        import re

        named = set(re.findall(r"XASSET-00\d\d", decision_text))
        beyond = {n for n in named if int(n.split("-")[1]) > 47}
        assert beyond == set(), beyond

    def test_the_decision_declares_exactly_one_current_module_identity(self, decision_text):
        declared = [
            ln for ln in decision_text.split("\n")
            if ln.strip().startswith("CURRENT_MODULE_SHA256:")
        ]
        assert len(declared) == 1, declared
        tokens = [
            token for token in declared[0].replace("`", " ").split()
            if len(token) == 64 and all(c in "0123456789abcdef" for c in token)
        ]
        assert len(tokens) == 1, tokens
        # RE-ANCHORED BY XASSET-0049. The SUBJECT of this decision's declaration is the module
        # as THIS unit left it -- an immutable fact about a closed merge -- not "whatever the
        # module is now". Comparing against the working tree made the claim false the moment a
        # lawful successor rebinding touched the module, which is precisely the live-vs-historical
        # confusion XASSET-0046 SS-G.11 requires to be classified and re-anchored.
        assert tokens[0] == PR347_MODULE_SHA256
        if _commit_exists(PR347_MERGE_SHA):
            assert tokens[0] == _blob_sha256_at(PR347_MERGE_SHA, AUTH_MODULE_RELPATH)


# ======================================================================================
# 12 -- Non-deadlock: this filing can actually attain its own SS-M.6
# ======================================================================================


#: Statements that would make this filing's own SS-M.6 unreachable. A decision may not both
#: REQUIRE successful exact-merge CI and say its own cannot be obtained -- that is the deadlock
#: XASSET-0045 shipped at its first reviewed head. Kept as an explicit closed set of phrases so
#: the guard is falsifiable rather than a vibe.
SELF_DEFEATING_CI_CLAIMS = (
    "own ci cannot succeed",
    "own merge-commit ci cannot succeed",
    "own merge-commit ci will fail",
    "cannot attain green merge-commit ci",
    "its own ci is unattainable",
)

#: The requirement whose ABSENCE is the other half of the deadlock: dropping it is not a fix.
REQUIRED_CI_CONDITION = "successful merge-commit ci whose `head_sha` is the exact merge sha"


def non_deadlock_offenders(flat_lower: str) -> list[str]:
    """Why the given decision text would be a deadlock, or an empty list.

    BOTH directions are offences: keeping the requirement while disclaiming the ability to meet
    it, and quietly dropping the requirement so nothing has to be met.
    """
    offenders: list[str] = []
    if REQUIRED_CI_CONDITION not in flat_lower:
        offenders.append("the successful-exact-merge-CI requirement is absent")
    for phrase in SELF_DEFEATING_CI_CLAIMS:
        if phrase in flat_lower:
            offenders.append(f"self-defeating claim: {phrase!r}")
    return offenders


def test_the_non_deadlock_detector_actually_detects():
    """Falsifiability proof, in BOTH directions, against synthetic text."""
    good = f"this filing requires {REQUIRED_CI_CONDITION} and meets it."
    dropped = "this filing requires nothing in particular."
    self_defeating = f"requires {REQUIRED_CI_CONDITION}, but its own ci cannot succeed."
    assert non_deadlock_offenders(good) == []
    assert non_deadlock_offenders(dropped) != []
    assert non_deadlock_offenders(self_defeating) != []
    # Both halves must be independently detectable, not merely one of them.
    assert non_deadlock_offenders(dropped + " own ci cannot succeed") != []
    assert len(SELF_DEFEATING_CI_CLAIMS) >= 5


class TestNonDeadlock:
    def test_the_filing_requires_successful_exact_merge_ci(self, decision_flat_lower):
        assert "successful merge-commit ci whose `head_sha` is the exact merge sha" in (
            decision_flat_lower
        )

    def test_the_filing_makes_no_claim_that_its_own_ci_cannot_succeed(
        self, decision_flat_lower
    ):
        """Combined non-deadlock guard, run through the shared module-level detector."""
        assert non_deadlock_offenders(decision_flat_lower) == [], (
            non_deadlock_offenders(decision_flat_lower)
        )

    def test_red_ci_is_a_stop_not_an_accepted_deviation(self, decision_text):
        n = _section(decision_text, "N")
        assert (
            "**A red exact-head or merge-commit CI result is a stop, not an accepted "
            "deviation.**" in n
        )
        assert "§M.6 is unchanged and remains fully required" in n

    def test_the_three_proof_modes_are_all_named(self, decision_text):
        n = _section(decision_text, "N")
        for mode in ("**structurally**", "**behaviourally**", "**adversarially**"):
            assert mode in n, mode
        assert "**five** simulated repository ref states" in n
        assert "never a `git worktree`" in n


# ======================================================================================
# 13 -- Nothing here arms anything
# ======================================================================================


class TestNothingIsArmed:
    def test_no_execution_is_authorized(self):
        authorized, reason = A.new_execution_is_authorized()
        assert authorized is False
        assert A.AUTHORIZING_DECISION in reason

    def test_the_lane_is_absent(self):
        assert not A.AUTHORIZATION_ROOT.exists()
        for path in (A.AUTHORIZATION_PATH, A.CLAIM_PATH, A.COMPLETION_PATH, A.LEDGER_PATH):
            assert not path.exists()

    def test_the_attempt_is_intact_unclaimed_and_unconsumed(self):
        state, _ = A.lane_state_at(A.LanePaths())
        assert state == A.LANE_ABSENT
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

    def test_the_canonical_executability_flag_is_still_false(self):
        data = yaml.safe_load(
            (ROOT / A.CANONICAL_PREREGISTRATION_RELPATH).read_text(encoding="utf-8")
        )
        assert data["stage_1_executability"]["executable"] is False

    def test_no_results_artifact_exists_anywhere(self):
        assert list(ROOT.rglob("stage1_results.yaml")) == []

    def test_this_suite_creates_no_attestation_and_no_lane_state(self):
        """Structural, and checked on CALLS rather than on substrings.

        A substring scan would flag its own vocabulary declaration -- the exact false-positive
        class that gets detectors switched off, and the one the ref-mutation detector below
        also had to solve. So this parses the AST and looks at what is actually INVOKED.
        """
        source = SUITE_PATH.read_text(encoding="utf-8")
        invoked: set[str] = set()
        for call in (c for c in ast.walk(ast.parse(source)) if isinstance(c, ast.Call)):
            if isinstance(call.func, ast.Attribute):
                invoked.add(call.func.attr)
            elif isinstance(call.func, ast.Name):
                invoked.add(call.func.id)
        for forbidden in (
            "write_authorization",
            "claim_execution",
            "complete_execution",
            "build_authorization_payload",
        ):
            assert forbidden not in invoked, forbidden
        # Non-vacuity: the parse really found this suite's calls.
        assert "_git" in invoked and len(invoked) > 20

    def test_the_decision_withholds_activation_authority_in_terms(self, decision_flat_lower):
        assert "adds **zero activation authority**" in decision_flat_lower
        assert "no committed value in this repository" in decision_flat_lower
        assert "stays permanently `false`" in decision_flat_lower


# ======================================================================================
# 14 -- Catalog and register synchronisation
# ======================================================================================



def _assert_shared_active_pr_is_not_behind_the_bound_rebinding(ws):
    """RE-ANCHORED BY XASSET-0050.

    ``XASSET-0049`` asserted ``ws["active_pr"] == A.AUTHORIZING_PULL_REQUEST`` and said why in
    its own comment: "*because the live unit is a REBINDING and therefore does bind its own
    number*." That premise is conditional, and ``XASSET-0050`` is the case it excludes -- a
    DESIGN-ONLY authorization that changes no module constant. The register's shared ``active_pr``
    moves onto it; ``A.AUTHORIZING_PULL_REQUEST`` correctly stays on the last unit that actually
    rebound. Equality would therefore assert "a rebinding is always live", which is false.

    The invariant underneath it survives intact and is what is asserted here: the shared field is
    never BEHIND the module's bound number. A value below it would mean the register was reverted
    to finished work -- the failure the equality was really guarding against. This is the same
    form ``XASSET-0048``'s own suite already uses for the same reason, so nothing is invented.

    During the sentinel window the field is negative and the ordering cannot be evaluated. Rather
    than skip -- which would make the guard vacuous exactly when the register is half-written --
    the sentinel state is checked for CONSISTENCY: the live gate must carry the same sentinel, so
    a half-bound register still fails.
    """
    active = ws["active_pr"]
    if active < 0:
        live = [g for g in ws["milestones"] if g.get("pr") == active]
        assert live, "the register carries a sentinel active_pr that no gate claims"
        assert all(g["status"] == "in_progress" for g in live), live
    else:
        assert active >= A.AUTHORIZING_PULL_REQUEST

class TestCatalogAndRegisterSynchronisation:
    def test_the_decision_is_indexed_exactly_once(self):
        catalog = yaml.safe_load((ROOT / CATALOG_RELPATH).read_text(encoding="utf-8"))
        rows = [d for d in catalog["decisions"] if d["decision_id"] == DECISION_ID]
        assert len(rows) == 1
        row = rows[0]
        assert row["file"] == DECISION_RELPATH
        assert row["supporting_artifact"] == SUITE_PATH.name
        assert row["category"] == "cross_asset_allocation_architecture"
        assert "XASSET-0046" in row["related_decisions"]

    def test_the_supporting_artifact_the_catalog_names_exists(self):
        catalog = yaml.safe_load((ROOT / CATALOG_RELPATH).read_text(encoding="utf-8"))
        row = next(d for d in catalog["decisions"] if d["decision_id"] == DECISION_ID)
        assert (ROOT / row["supporting_artifact"]).is_file()

    def test_every_filed_decision_is_indexed(self):
        catalog = yaml.safe_load((ROOT / CATALOG_RELPATH).read_text(encoding="utf-8"))
        indexed = {d["file"] for d in catalog["decisions"]}
        assert DECISION_RELPATH in indexed

    def test_the_register_records_this_unit(self, register_text):
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        gates = {g["gate"]: g for g in ws["milestones"]}
        assert "xasset0047-post-merge-ci-recovery-reconciliation" in gates
        assert "xasset0046-post-merge-verification" in gates

    def test_the_units_own_gate_is_not_marked_complete_while_unmerged(self, register_text):
        """A filing does not mark its own unmerged work complete."""
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        gate = next(
            g for g in ws["milestones"]
            if g["gate"] == "xasset0047-post-merge-ci-recovery-reconciliation"
        )
        assert gate["status"] == "in_progress"

    def test_the_prior_gates_own_text_was_not_edited(self, register_text):
        """The XASSET-0046 gate is accepted history. Its confirmed merge is recorded by a NEW,
        additive gate rather than by rewriting what it said while it was live."""
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        prior = next(
            g for g in ws["milestones"]
            if g["gate"] == "xasset0046-post-merge-ci-recovery-reauthorization"
        )
        assert prior["status"] == "in_progress"
        assert prior["pr"] == 346
        assert "AUTHORIZING_DECISION remains XASSET-0044" in prior["description"]

    def test_the_shared_live_fields_advanced(self, register_text):
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        # ADVANCED BY XASSET-0048: this unit merged at `bb95ed26`, so the register's shared
        # "where main is now" field advanced onto THIS unit's own merge, and its `active_pr`
        # onto the successor. Bound at BOTH ends rather than relaxed to an inequality.
        # ADVANCED AGAIN BY XASSET-0049: PR #349 is the live unit, so the shared fields moved
        # onto its own base and its own number. Bound at BOTH ends, with every prior generation's
        # value retained as a negative pin -- and the module/register agreement is now an
        # EQUALITY, because the live unit is a REBINDING and therefore does bind its own number.
        assert ws["last_verified_main_sha"] == XASSET0054_MAIN_SHA
        assert ws["last_verified_main_sha"] != XASSET0053_MAIN_SHA
        assert ws["last_verified_main_sha"] != XASSET0052_MAIN_SHA
        assert ws["last_verified_main_sha"] != XASSET0051_MAIN_SHA
        assert ws["last_verified_main_sha"] != XASSET0050_MAIN_SHA
        assert ws["last_verified_main_sha"] != XASSET0049_MAIN_SHA
        assert ws["last_verified_main_sha"] != XASSET0048_MAIN_SHA
        assert ws["last_verified_main_sha"] != PR346_MERGE_SHA
        assert ws["last_verified_main_sha"] != PR346_BASE_SHA
        assert ws["last_verified_main_sha"] != PR345_BASE_SHA
        assert ws["active_pr"] == XASSET0054_ACTIVE_PR
        assert ws["active_pr"] != XASSET0053_ACTIVE_PR
        assert ws["active_pr"] != XASSET0052_ACTIVE_PR
        assert ws["active_pr"] != XASSET0051_ACTIVE_PR
        assert ws["active_pr"] != XASSET0050_ACTIVE_PR
        assert ws["active_pr"] != XASSET0049_ACTIVE_PR
        assert ws["active_pr"] != XASSET0048_ACTIVE_PR
        _assert_shared_active_pr_is_not_behind_the_bound_rebinding(ws)

    def test_the_workstream_posture_is_unchanged(self, register_text):
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        assert ws["status"] == "proposed"
        assert ws["priority"] == "secondary"

    def test_exactly_zero_primary_workstreams(self, register_text):
        data = yaml.safe_load(register_text)
        assert [w["id"] for w in data["workstreams"] if w.get("priority") == "primary"] == []

    def test_the_register_records_the_current_module_identity(self, register_text):
        """RE-ANCHORED BY XASSET-0049, for the same reason as the decision's own declaration.

        This unit's gate records the module identity THIS unit produced. That is immutable, and
        it must still be present; a successor's own gate records the successor's, separately.
        """
        flat = register_text.replace("\n", "").replace(" ", "")
        assert PR347_MODULE_SHA256 in flat
        if _commit_exists(PR347_MERGE_SHA):
            assert _blob_sha256_at(PR347_MERGE_SHA, AUTH_MODULE_RELPATH) in flat


# ======================================================================================
# 15 -- The cross-file audit XASSET-0046 SS-G.11 requires, encoded durably
#
# SS-G.11's first paragraph is operative on this unit: classify every use of HEAD,
# origin/main, merge-base and any working-tree comparison in the files it touches by whether
# that use's SUBJECT is live state or immutable history, and re-anchor every historical one.
# Running that audit once at a console proves nothing after the session ends, so the
# classification is encoded here instead.
# ======================================================================================


#: The two artifacts whose declared historical proofs this unit is responsible for. Each
#: publishes its OWN ``HISTORICAL_PROOF_FUNCTIONS``, so the invariant can be checked against the
#: file's own declaration rather than against a list maintained here.
AUDITED_ARTIFACTS = (
    CORRECTED_ARTIFACT_RELPATH,
    "test_level1_stage1_post_merge_ci_recovery_reauthorization.py",
    SUITE_PATH.name,
)


def _declared_historical_proofs(relative: str) -> frozenset[str]:
    """The module's own declared set, read from its source without importing it."""
    source = (ROOT / relative).read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "HISTORICAL_PROOF_FUNCTIONS"
            for t in node.targets
        ):
            call = node.value
            assert isinstance(call, ast.Call), ast.dump(call)
            return frozenset(
                element.value
                for element in ast.walk(call)
                if isinstance(element, ast.Constant) and isinstance(element.value, str)
            )
    return frozenset()


@pytest.mark.parametrize("relative", AUDITED_ARTIFACTS)
def test_no_declared_historical_proof_in_an_audited_artifact_names_a_moving_reference(
    relative,
):
    """The audit's result, encoded so it survives the session that performed it."""
    source = (ROOT / relative).read_text(encoding="utf-8")
    declared = _declared_historical_proofs(relative)
    assert declared, f"{relative} declares no historical proofs at all"
    assert historical_proof_moving_ref_offenders(source, declared) == [], relative


@pytest.mark.parametrize("relative", AUDITED_ARTIFACTS)
def test_every_moving_reference_user_in_an_audited_artifact_is_a_live_state_function(
    relative,
):
    """The converse direction, which is what actually makes the audit complete.

    A function that NAMES a moving reference must not also be declared a historical proof.
    Checking only one direction would let a historical proof be quietly un-declared instead of
    re-anchored -- which passes the first check by shrinking its own scope.
    """
    source = (ROOT / relative).read_text(encoding="utf-8")
    declared = _declared_historical_proofs(relative)
    offenders = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.FunctionDef):
            continue
        names_moving = any(
            isinstance(literal, ast.Constant)
            and isinstance(literal.value, str)
            and literal.value in MOVING_REFERENCE_LITERALS
            for literal in ast.walk(node)
        )
        if names_moving and node.name in declared:
            offenders.append(f"{relative}::{node.name}")
    assert offenders == [], offenders


def test_the_audit_would_catch_a_reintroduced_moving_anchor():
    """Falsifiability for the pair above, against synthetic source carrying both shapes."""
    bad = (
        "HISTORICAL_PROOF_FUNCTIONS = frozenset({'test_historical'})\n"
        "def test_historical():\n"
        "    assert _git('diff', '--name-only', 'origin/main') == ''\n"
    )
    good = (
        "HISTORICAL_PROOF_FUNCTIONS = frozenset({'test_historical'})\n"
        "def test_historical():\n"
        "    assert _git('rev-parse', PINNED) == PINNED\n"
    )
    declared = frozenset({"test_historical"})
    assert historical_proof_moving_ref_offenders(bad, declared) != []
    assert historical_proof_moving_ref_offenders(good, declared) == []
    # ... and the declaration reader really extracts a non-empty set from real source.
    assert _declared_historical_proofs(CORRECTED_ARTIFACT_RELPATH)
    assert _declared_historical_proofs(SUITE_PATH.name) == HISTORICAL_PROOF_FUNCTIONS


def test_the_two_predecessor_working_tree_guards_are_deliberately_left_alone():
    """Two pre-existing guards compare the WORKING TREE against ``HEAD``.

    Classified, not corrected: their subject is genuinely LIVE -- "are there uncommitted edits
    to a protected path" -- so they fire while a branch is mid-edit and pass once it is
    committed, which is exactly the behaviour their own docstrings describe and exactly the
    behaviour XASSET-0044's own report recorded for them. Re-anchoring them to a closed range
    would DESTROY the property they exist for. This test pins that classification so a future
    reader does not mistake them for instances of the defect class.
    """
    source = (ROOT / "test_level1_stage1_post_correction_rebinding.py").read_text(
        encoding="utf-8"
    )
    live_state_guard = _function_source(source, "test_portfolio_path_is_unchanged_against_head")
    assert "Worktree cleanliness" in live_state_guard
    # The other shape in that file pins the LOWER bound and lets only the far end move, so it
    # can never collapse to empty the way `diff origin/main` on a merged branch does.
    widening = _function_source(source, "test_portfolio_path_is_unchanged_from_the_pr_base_to_head")
    assert "PR_BASE_SHA" in widening
    assert '"HEAD"' in widening


# ======================================================================================
# 16 -- Coverage pins found by mutation testing
#
# Five probes MISSED on the first pass and are fixed here rather than dropped. Every one was
# the same shape: a declared VOCABULARY -- a ref-state list, a selection tuple, a frozen-path
# list, an audited-file list -- that could be gutted while every guard consuming it still
# reported clean, because nothing pinned the vocabulary itself. A guard that inspects an empty
# list is not a guard, and that is precisely the silent-disable shape this whole programme
# exists to refuse.
# ======================================================================================


def test_every_ref_state_this_branch_will_pass_through_is_actually_parametrised():
    """MUTATION PIN (probe A03). Deleting ``merged_main`` -- the exact state that broke PR
    #345 -- left every other assertion passing, because nothing pinned the state list."""
    assert set(REF_STATES) == {
        "branch",
        "merged_main",
        "later_main",
        "head_equals_origin_main_later",
        "unrelated_later_commits",
    }
    assert len(REF_STATES) == 5
    # The two states where HEAD equals origin/main are the ones that collapse a moving base,
    # so their presence is pinned individually rather than only through the set above.
    assert "merged_main" in REF_STATES
    assert "head_equals_origin_main_later" in REF_STATES


def test_the_ref_state_selection_runs_the_declared_proofs_and_nothing_instead_of_them():
    """MUTATION PIN (probe A04). The selection could be padded or emptied while the nested
    run still reported ``passed``, so it is pinned to the declared historical proofs."""
    selected_leaves = {name.split("::")[-1] for name in REF_STATE_SENSITIVE_TESTS}
    # Every selected leaf is either a declared historical proof, the detector that guards them,
    # or one of exactly two LIVE-state checks whose comparison is anchored to an immutable base
    # and which must therefore also survive every ref position. The permitted set is CLOSED:
    # nothing else may be smuggled in to make the selection look populated.
    REF_STATE_INVARIANT_LIVE_CHECKS = {
        "test_the_additions_are_exactly_the_two_authority_chain_files",
    }
    permitted = (
        set(HISTORICAL_PROOF_FUNCTIONS)
        | {"test_no_historical_proof_consults_a_moving_reference"}
        | REF_STATE_INVARIANT_LIVE_CHECKS
    )
    assert selected_leaves <= permitted, selected_leaves - permitted
    assert REF_STATE_INVARIANT_LIVE_CHECKS <= selected_leaves
    # ... and the ones that matter most are individually required, so the selection cannot be
    # quietly reduced to a single cheap case.
    for required in (
        "test_the_accepted_head_is_the_second_parent_of_this_units_base",
        "test_the_preserved_pr345_range_still_carries_its_enabling_correction",
        "test_every_frozen_path_is_byte_identical_to_this_units_base",
        "test_no_historical_proof_consults_a_moving_reference",
    ):
        assert required in selected_leaves, required
    assert len(REF_STATE_SENSITIVE_TESTS) >= 8


def test_the_frozen_path_list_actually_names_the_surface_it_claims_to_freeze():
    """MUTATION PIN (probe A06). Swapping one entry for an unrelated unchanged file kept the
    length and kept the comparison green, so the list's CONTENT is pinned, not just its size."""
    frozen = set(FROZEN_AGAINST_BASE_RELPATHS)
    for required in (
        "level1_stage1_runner.py",
        "level1_stage1_result_validator.py",
        "level1_construction_universe_closure_validator.py",
        "level1_endpoint_evidence_preregistration_validator.py",
        "research/level1_endpoint_evidence/PROTOCOL_V1.md",
        "research/level1_endpoint_evidence/pre_registration.yaml",
        OVERLAP_ARTIFACT_RELPATH,
        "allocate.py",
        "targets.yaml",
        "holdings.yaml",
        AUTHORITY_RELPATH,
    ):
        assert required in frozen, required
    # Every outcome-producing path the module itself names must be frozen here too, so the
    # two lists cannot drift apart.
    assert set(A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS) <= frozen
    assert A.OUTCOME_PRODUCING_DERIVATION_RELPATH in frozen
    assert set(A.CANONICAL_PINS) <= frozen


def test_the_audited_artifact_list_is_exactly_the_three_this_unit_is_responsible_for():
    """MUTATION PIN (probe A09). The list could be padded or narrowed unnoticed."""
    assert set(AUDITED_ARTIFACTS) == {
        CORRECTED_ARTIFACT_RELPATH,
        "test_level1_stage1_post_merge_ci_recovery_reauthorization.py",
        SUITE_PATH.name,
    }
    assert len(AUDITED_ARTIFACTS) == 3


def working_tree_subject_offenders(source: str, names: frozenset[str]) -> list[str]:
    """Declared historical proofs that read the LIVE working tree as their SUBJECT.

    Extracted to module level, and given its own falsifiability proof below, because the
    in-test version could be made unreachable while still reporting clean -- probe A08.

    A live read is permitted ONLY inside a function that also resolves the immutable blob it
    compares against, which is what makes it a comparison rather than a measurement of a
    moving thing.
    """
    offenders: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.FunctionDef) or node.name not in names:
            continue
        enclosing = ast.get_source_segment(source, node) or ""
        resolves_immutable = "cat-file" in enclosing or "git show" in enclosing
        for call in ast.walk(node):
            if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Attribute):
                continue
            if call.func.attr not in {"read_text", "read_bytes"}:
                continue
            if not resolves_immutable:
                offenders.append(f"{node.name}: live read at line {call.lineno}")
    return offenders


def test_the_working_tree_subject_detector_actually_detects():
    """MUTATION PIN (probe A08). Falsifiability proof against synthetic source, in both
    directions, so making the scan unreachable fails its own test rather than reporting clean."""
    names = frozenset({"test_historical"})
    bad = (
        "def test_historical():\n"
        "    live = (ROOT / REL).read_text()\n"
        "    assert live == EXPECTED\n"
    )
    good = (
        "def test_historical():\n"
        "    live = (ROOT / REL).read_text()\n"
        "    at_base = subprocess.run(['git', 'cat-file', 'blob', PINNED]).stdout\n"
        "    assert live == at_base\n"
    )
    out_of_scope = (
        "def test_live_state():\n"
        "    assert (ROOT / REL).read_text()\n"
    )
    assert working_tree_subject_offenders(bad, names) != []
    assert working_tree_subject_offenders(good, names) == []
    assert working_tree_subject_offenders(out_of_scope, names) == []
    # ... and it genuinely inspects this suite's own real source.
    real = SUITE_PATH.read_text(encoding="utf-8")
    assert working_tree_subject_offenders(real, HISTORICAL_PROOF_FUNCTIONS) == []
    assert len([n for n in ast.walk(ast.parse(real)) if isinstance(n, ast.FunctionDef)]) > 80


# ======================================================================================
# 17 -- The bound pull-request number, verified rather than asserted
#
# The branch's first commit carried the impossible sentinel ``0``. GitHub then issued the real
# number, it was read back from live GitHub, and only then was it bound. These pins hold the
# bound value to what a real, distinct, later pull request must look like -- so a copied,
# guessed, or reverted number fails here rather than at an attestation nobody is watching.
# ======================================================================================


#: The number GitHub issued for this unit's own pull request, read back after the draft was
#: opened. Never predicted: the first commit on this branch bound ``0``.
THIS_PULL_REQUEST = 347


class TestTheBoundPullRequestNumber:
    def test_the_module_binds_the_number_github_actually_issued(self):
        """RE-ANCHORED BY XASSET-0049 onto the constant that now carries this unit's number.

        The point of the assertion is that the number was READ BACK rather than guessed, and that
        it is bound somewhere the mechanism actually authenticates against. Both survive the
        anchor move; only which constant holds it changed.
        """
        assert A.PRIOR_RECONCILIATION_PULL_REQUEST == THIS_PULL_REQUEST
        # The live anchor moved to a strictly later, real pull request.
        assert A.AUTHORIZING_PULL_REQUEST > THIS_PULL_REQUEST

    def test_the_sentinel_is_gone(self):
        """``0`` can never validate, which is exactly why it was safe to commit first."""
        assert A.AUTHORIZING_PULL_REQUEST != 0
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert "AUTHORIZING_PULL_REQUEST = 0" not in source

    def test_it_is_a_later_pull_request_than_every_predecessor_in_the_chain(self):
        """Monotonic by construction: GitHub issues numbers in order, so a number at or below
        any predecessor's would mean the constant was copied rather than read back."""
        for predecessor in (
            A.HISTORICAL_OPERATIONAL_AUTHORIZATION_PULL_REQUEST,
            A.PACKAGE_AUTHORIZING_PULL_REQUEST,
            A.EXECUTABLE_PACKAGE_PULL_REQUEST,
            A.PRIOR_SUCCESSOR_REBINDING_PULL_REQUEST,
            A.CORRECTION_AUTHORIZING_PULL_REQUEST,
            A.CORRECTED_MODULE_PULL_REQUEST,
            A.REBINDING_AUTHORIZING_PULL_REQUEST,
            A.STOPPED_REBINDING_PULL_REQUEST,
            A.STOPPED_RECOVERY_AUTHORIZATION_PULL_REQUEST,
            A.RECOVERY_AUTHORIZING_PULL_REQUEST,
        ):
            # RE-ANCHORED BY XASSET-0049: this unit's own number is the subject, and it is now
            # carried by PRIOR_RECONCILIATION_PULL_REQUEST. The live anchor is checked too, so
            # monotonicity is asserted for BOTH rather than traded from one to the other.
            assert A.PRIOR_RECONCILIATION_PULL_REQUEST > predecessor, predecessor
            assert A.AUTHORIZING_PULL_REQUEST > predecessor, predecessor
        assert A.AUTHORIZING_PULL_REQUEST > A.PRIOR_RECONCILIATION_PULL_REQUEST
        assert A.AUTHORIZING_PULL_REQUEST > A.STEP8_EQUIVALENT_AUTHORIZING_PULL_REQUEST

    def test_the_register_and_the_module_agree(self, register_text):
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        gate = next(
            g for g in ws["milestones"]
            if g["gate"] == "xasset0047-post-merge-ci-recovery-reconciliation"
        )
        # This unit's OWN gate still names this unit's own pull request -- that is history and
        # does not move. The SHARED live fields lawfully advanced onto the successor unit under
        # XASSET-0048, so they are asserted against the successor's values, not this unit's.
        assert gate["pr"] == THIS_PULL_REQUEST
        # ADVANCED BY XASSET-0049: the register's shared active_pr now names the LIVE unit, and
        # the live unit is a rebinding, so it and the module agree exactly.
        assert ws["active_pr"] == XASSET0054_ACTIVE_PR
        assert ws["active_pr"] != XASSET0053_ACTIVE_PR
        assert ws["active_pr"] != XASSET0052_ACTIVE_PR
        assert ws["active_pr"] != XASSET0051_ACTIVE_PR
        assert ws["active_pr"] != XASSET0050_ACTIVE_PR
        assert ws["active_pr"] != XASSET0049_ACTIVE_PR
        _assert_shared_active_pr_is_not_behind_the_bound_rebinding(ws)
        assert ws["active_pr"] != THIS_PULL_REQUEST
        assert ws["active_branch"] != "claude/xasset-0046-recovery-b31nba"

    def test_every_surface_that_names_the_number_names_the_same_one(self):
        """Three predecessor suites carry it too. Divergence between any of them and the
        module is how a rebinding starts authenticating against the wrong pull request."""
        for relative in (
            "test_level1_stage1_activation_authorization.py",
            "test_level1_stage1_post_rebinding_drift_authorization.py",
            "test_level1_stage1_readiness_verification_authorization.py",
        ):
            source = (ROOT / relative).read_text(encoding="utf-8")
            assert f"XASSET0047_ACTIVE_PR = {THIS_PULL_REQUEST}" in source, relative
            assert "XASSET0047_ACTIVE_PR = 0" not in source, relative


# ======================================================================================
# 18 -- MAJOR 1 (review 4997532748): the canonical-freeze refusal is genuinely INDEPENDENT
#
# The independent full review found the fourth refusal SOURCE-VACUOUS. The historical
# identity was ``dict(CANONICAL_PINS)``, so a SOURCE-LEVEL edit to a current pin literal was
# rebuilt into the historical mapping during import, the two stayed equal, and the refusal
# returned clean. It detected only a post-import monkeypatch of one name -- which is exactly
# and only what the runtime negative test above exercises.
#
# Reproduced through the real mechanism BEFORE correcting: an isolated copy, one current pin
# literal changed in SOURCE, a fresh import, the historical mapping observed following the
# edit, and ``_verify_recovery_lifecycle_anchor`` observed returning ``[]``.
#
# The correction binds the historical mapping to XASSET-0044's exact literals. This section
# proves that independently three ways -- structurally from the AST, behaviourally through a
# real source edit and re-import, and by pinning the literal values themselves -- because a
# guard that can only be checked one way is a guard whose one check can be removed.
# ======================================================================================


#: XASSET-0044's exact historical canonical pins, written here INDEPENDENTLY of the module.
#: These are the mutation pins for adversarial case 6: changing either literal in the module
#: without changing it here is caught, and changing BOTH current and historical in lockstep is
#: caught too, because this suite holds the third, external copy.
XASSET0044_HISTORICAL_PROTOCOL_SHA256 = (
    "1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84"
)
XASSET0044_HISTORICAL_PREREGISTRATION_SHA256 = (
    "898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f"
)

#: The name whose independence is the whole point, and the name it may never be derived from.
HISTORICAL_PINS_NAME = "XASSET_0044_CANONICAL_PINS"
CURRENT_PINS_NAME = "CANONICAL_PINS"


def historical_pins_is_independent(source: str) -> bool:
    """True iff ``XASSET_0044_CANONICAL_PINS`` is a literal mapping of constant strings that
    does not mention ``CANONICAL_PINS`` anywhere in its own defining expression.

    Takes SOURCE rather than the imported object on purpose. Two mappings that are equal at
    runtime are indistinguishable by value; the defect this refuses is visible only in how the
    second one is CONSTRUCTED. Written to accept a source string so it can be driven against
    synthetic known-bad and known-good inputs, not only against the real module.
    """
    tree = ast.parse(source)
    values = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == HISTORICAL_PINS_NAME
            for target in node.targets
        )
    ]
    if len(values) != 1:
        return False
    value = values[0]
    if not isinstance(value, ast.Dict):
        return False
    if any(key is None for key in value.keys):
        return False
    if not all(isinstance(item, ast.Constant) and isinstance(item.value, str)
               for item in value.values):
        return False
    return not any(
        isinstance(node, ast.Name) and node.id == CURRENT_PINS_NAME
        for node in ast.walk(value)
    )


def _run_isolated_pin_probe(tmp_path: Path, replacements: tuple[tuple[str, str], ...]) -> dict:
    """Copy the module ALONE into ``tmp_path``, apply exact source replacements, import it in a
    FRESH interpreter, and report what the real refusal says.

    A fresh interpreter, not ``importlib.reload``: a reload can leave the old module object
    reachable and is exactly the kind of half-measure that produced the finding. The module's
    imports are stdlib-only and ``_verify_recovery_lifecycle_anchor`` is pure and offline
    (proved separately from its own AST above), so it runs standalone.

    The REAL repository is never touched: only ``tmp_path`` is written.
    """
    source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
    for old, new in replacements:
        assert source.count(old) == 1, (old, source.count(old))
        source = source.replace(old, new)
    module_copy = tmp_path / AUTH_MODULE_RELPATH
    module_copy.write_text(source, encoding="utf-8")
    driver = tmp_path / "_probe_driver.py"
    driver.write_text(
        "import json, sys, pathlib\n"
        "sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))\n"
        "import level1_stage1_execution_authorization as M\n"
        "print(json.dumps({\n"
        "    'current': M.CANONICAL_PINS,\n"
        "    'historical': M.XASSET_0044_CANONICAL_PINS,\n"
        "    'errors': M._verify_recovery_lifecycle_anchor(M.RECOVERY_AUTHORIZING_MERGE_SHA),\n"
        "}))\n",
        encoding="utf-8",
    )
    completed = subprocess.run(
        [sys.executable, str(driver)], capture_output=True, text=True, check=True, cwd=tmp_path
    )
    import json as _json

    return _json.loads(completed.stdout)


#: The exact current-pin literal, and a value that is a well-formed sha256 but not that one.
_CURRENT_PROTOCOL_LITERAL_BLOCK = (
    "CANONICAL_PINS: dict[str, str] = {\n"
    "    CANONICAL_PROTOCOL_RELPATH: (\n"
    f'        "{XASSET0044_HISTORICAL_PROTOCOL_SHA256}"\n'
    "    ),"
)
_MUTANT_SHA256 = "0" * 63 + "1"


#: Known-bad ways a later edit could re-derive the historical mapping. Declared at module level
#: and PINNED by its own coverage test below: mutation probe C25 showed that a vocabulary only
#: consumed by a parametrize decorator can be gutted while every consumer still reports clean.
#:
#: The list is deliberately split. The first group is refused by an earlier SHAPE check (not a
#: literal dict of constant strings). The second group PASSES every shape check and is refused
#: only by the final scan for a ``CANONICAL_PINS`` reference -- without at least one of those,
#: that scan has no coverage at all, which is exactly how probe C9 first survived.
DERIVED_FORMS_REJECTED_BY_SHAPE = (
    "XASSET_0044_CANONICAL_PINS = dict(CANONICAL_PINS)",
    "XASSET_0044_CANONICAL_PINS = CANONICAL_PINS",
    "XASSET_0044_CANONICAL_PINS = {**CANONICAL_PINS}",
    "XASSET_0044_CANONICAL_PINS = CANONICAL_PINS.copy()",
    "XASSET_0044_CANONICAL_PINS = dict(CANONICAL_PINS.items())",
    "XASSET_0044_CANONICAL_PINS = {k: v for k, v in CANONICAL_PINS.items()}",
)

#: Literal dicts of constant strings whose KEYS are derived from the current mapping -- the
#: shape a plausible half-independent rewrite actually takes, and the only shape that exercises
#: the reference scan.
DERIVED_FORMS_REJECTED_ONLY_BY_THE_REFERENCE_SCAN = (
    'XASSET_0044_CANONICAL_PINS = {\n'
    '    list(CANONICAL_PINS)[0]: "aa",\n'
    '    list(CANONICAL_PINS)[1]: "bb",\n'
    "}",
    'XASSET_0044_CANONICAL_PINS = {\n'
    '    next(iter(CANONICAL_PINS)): "aa",\n'
    "}",
)

ALL_DERIVED_FORMS = (
    DERIVED_FORMS_REJECTED_BY_SHAPE + DERIVED_FORMS_REJECTED_ONLY_BY_THE_REFERENCE_SCAN
)


class TestTheCanonicalFreezeRefusalIsIndependent:
    def test_the_historical_mapping_is_not_derived_from_the_current_one(self):
        """Adversarial cases 4 and 5, structurally: the definition may not name CANONICAL_PINS."""
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert historical_pins_is_independent(source)
        assert f"{HISTORICAL_PINS_NAME} = dict({CURRENT_PINS_NAME})" not in source
        assert f"{HISTORICAL_PINS_NAME} = {CURRENT_PINS_NAME}\n" not in source

    @pytest.mark.parametrize("bad_form", ALL_DERIVED_FORMS)
    def test_the_structural_guard_rejects_every_derived_form(self, bad_form):
        """Falsifiability, known-bad half. Adversarial cases 4 and 5 are the first two of these;
        the rest are the near-misses a later edit would more plausibly reach for."""
        assert not historical_pins_is_independent(
            'CANONICAL_PINS = {"a": "b"}\n' + bad_form + "\n"
        )

    def test_the_structural_guard_accepts_a_genuinely_independent_form(self):
        """Falsifiability, known-good half. Without this, deleting the guard's body and
        returning False would 'pass' every case above while proving nothing."""
        assert historical_pins_is_independent(
            'CANONICAL_PINS = {"a": "b"}\n'
            'XASSET_0044_CANONICAL_PINS = {\n'
            '    "a": "b",\n'
            '}\n'
        )

    def test_the_known_bad_vocabulary_actually_covers_the_reference_scan(self):
        """MUTATION-FOUND (probe C25). A parametrize list is a DECLARED VOCABULARY, and a
        vocabulary nothing pins can be gutted while every consumer still reports clean.

        Pin the PROPERTY rather than the count: at least one known-bad form must survive every
        earlier shape check, so that the final ``CANONICAL_PINS``-reference scan is the thing
        actually refusing it. Without this, the list could shrink to shape-rejected forms only
        and ``return True`` in place of that scan would pass again, exactly as it first did.
        """
        assert DERIVED_FORMS_REJECTED_ONLY_BY_THE_REFERENCE_SCAN
        # MUTATION-FOUND (probe C28). Pinning a vocabulary's CONTENTS proves nothing if the
        # vocabulary is not the one actually driven. Both groups must reach the parametrize.
        for form in DERIVED_FORMS_REJECTED_BY_SHAPE:
            assert form in ALL_DERIVED_FORMS, form
        for form in DERIVED_FORMS_REJECTED_ONLY_BY_THE_REFERENCE_SCAN:
            assert form in ALL_DERIVED_FORMS, form
        # MUTATION-FOUND (probe C27). The vocabulary must still contain the EXACT form the
        # review found in production. A generic "some derived form" list can drift until the
        # one real historical defect is no longer among the things it refuses.
        assert (
            "XASSET_0044_CANONICAL_PINS = dict(CANONICAL_PINS)"
            in DERIVED_FORMS_REJECTED_BY_SHAPE
        )
        assert "XASSET_0044_CANONICAL_PINS = CANONICAL_PINS" in DERIVED_FORMS_REJECTED_BY_SHAPE
        for form in DERIVED_FORMS_REJECTED_ONLY_BY_THE_REFERENCE_SCAN:
            value = ast.parse('CANONICAL_PINS = {"a": "b"}\n' + form + "\n").body[1].value
            assert isinstance(value, ast.Dict), form
            assert all(key is not None for key in value.keys), form
            assert all(
                isinstance(item, ast.Constant) and isinstance(item.value, str)
                for item in value.values
            ), form
            assert any(
                isinstance(node, ast.Name) and node.id == CURRENT_PINS_NAME
                for node in ast.walk(value)
            ), form
        for form in DERIVED_FORMS_REJECTED_BY_SHAPE:
            assert not historical_pins_is_independent(
                'CANONICAL_PINS = {"a": "b"}\n' + form + "\n"
            ), form

    def test_the_historical_literals_are_exactly_xasset_0044s(self):
        """Adversarial case 6, and the lockstep case: this suite holds an INDEPENDENT third
        copy, so moving current and historical together is still caught here."""
        assert A.XASSET_0044_CANONICAL_PINS == {
            A.CANONICAL_PROTOCOL_RELPATH: XASSET0044_HISTORICAL_PROTOCOL_SHA256,
            A.CANONICAL_PREREGISTRATION_RELPATH: XASSET0044_HISTORICAL_PREREGISTRATION_SHA256,
        }

    def test_case_1_equal_at_the_start_is_accepted(self):
        """Adversarial case 1: XASSET-0046 SS-G.9 froze the canonical inputs, so the two
        mappings are EQUAL IN VALUE right now -- and that must not be an error."""
        assert A.CANONICAL_PINS == A.XASSET_0044_CANONICAL_PINS
        assert A._verify_recovery_lifecycle_anchor(A.RECOVERY_AUTHORIZING_MERGE_SHA) == []

    def test_case_2_a_source_level_current_pin_edit_drives_the_real_refusal(self, tmp_path):
        """Adversarial case 2, and the correction's whole point.

        This is the case the previous implementation could not see. It is driven through a real
        source edit and a real re-import, NOT a monkeypatch, because a monkeypatch of one name
        is satisfied by a mapping that was copied from that same name.
        """
        result = _run_isolated_pin_probe(
            tmp_path,
            ((_CURRENT_PROTOCOL_LITERAL_BLOCK,
              _CURRENT_PROTOCOL_LITERAL_BLOCK.replace(
                  XASSET0044_HISTORICAL_PROTOCOL_SHA256, _MUTANT_SHA256)),),
        )
        assert result["current"][A.CANONICAL_PROTOCOL_RELPATH] == _MUTANT_SHA256
        assert (
            result["historical"][A.CANONICAL_PROTOCOL_RELPATH]
            == XASSET0044_HISTORICAL_PROTOCOL_SHA256
        ), "the historical identity FOLLOWED the current edit -- it is not independent"
        assert any("canonical drift" in e for e in result["errors"]), result["errors"]

    def test_case_3_a_source_level_historical_pin_edit_is_also_refused(self, tmp_path):
        """Adversarial case 3, the other direction: rewriting HISTORY while the current pins
        stay correct is equally a succession failure, and must not pass either."""
        historical_block = (
            "XASSET_0044_CANONICAL_PINS = {\n"
            "    CANONICAL_PROTOCOL_RELPATH: (\n"
            f'        "{XASSET0044_HISTORICAL_PROTOCOL_SHA256}"\n'
            "    ),"
        )
        result = _run_isolated_pin_probe(
            tmp_path,
            ((historical_block,
              historical_block.replace(
                  XASSET0044_HISTORICAL_PROTOCOL_SHA256, _MUTANT_SHA256)),),
        )
        assert result["current"][A.CANONICAL_PROTOCOL_RELPATH] == (
            XASSET0044_HISTORICAL_PROTOCOL_SHA256
        )
        assert result["historical"][A.CANONICAL_PROTOCOL_RELPATH] == _MUTANT_SHA256
        assert any("canonical drift" in e for e in result["errors"]), result["errors"]

    def test_the_probe_harness_is_itself_falsifiable(self, tmp_path):
        """An unedited copy must come back CLEAN. Without this, a harness that silently failed
        to apply its replacement -- or a refusal that fired unconditionally -- would make both
        cases above pass while proving nothing."""
        result = _run_isolated_pin_probe(tmp_path, ())
        assert result["current"] == result["historical"]
        assert result["errors"] == []

    def test_case_7_the_canonical_files_are_untouched_and_still_match_the_current_pins(self):
        """Adversarial case 7: the finding was about the PROTECTION, never about the bytes.
        Live hashes still equal the current pins, and both files are byte-identical to this
        pull request's own immutable base."""
        live = A.live_canonical_hashes()
        assert live == dict(A.CANONICAL_PINS)
        for relative in (A.CANONICAL_PROTOCOL_RELPATH, A.CANONICAL_PREREGISTRATION_RELPATH):
            at_base = hashlib.sha256(
                subprocess.run(
                    ["git", "cat-file", "blob", f"{PR346_MERGE_SHA}:{relative}"],
                    cwd=ROOT, capture_output=True, check=True,
                ).stdout
            ).hexdigest()
            assert at_base == A.CANONICAL_PINS[relative], relative

    def test_the_runtime_monkeypatch_test_was_kept_not_replaced(self):
        """Review 4997532748 called the one-sided monkeypatch INSUFFICIENT, not wrong. It stays
        -- it is the only case that covers a runtime substitution -- and the source-level cases
        above are ADDED alongside it. Deleting it would trade one blind spot for another."""
        # MUTATION-FOUND (probe C16). This was a substring search for the test's own
        # signature -- and the search string is ITSELF a literal in this file, so the file
        # always contained it and renaming the real test away survived. Read the AST
        # instead: a name that is only mentioned cannot satisfy a check for a name that is
        # DEFINED, in the class that is supposed to define it.
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        owner = next(
            node for node in tree.body
            if isinstance(node, ast.ClassDef)
            and node.name == "TestTheNewRefusalsAreIndependentlyRequired"
        )
        kept = [
            node for node in owner.body
            if isinstance(node, ast.FunctionDef) and node.name == "test_canonical_drift_is_refused"
        ]
        assert len(kept) == 1, [n.name for n in owner.body if isinstance(n, ast.FunctionDef)]
        assert any(arg.arg == "monkeypatch" for arg in kept[0].args.args)
        patched = {
            node.args[1].value
            for node in ast.walk(kept[0])
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "setattr"
            and len(node.args) >= 2
            and isinstance(node.args[1], ast.Constant)
        }
        assert CURRENT_PINS_NAME in patched, patched

    def test_the_refusal_itself_still_compares_the_two_mappings(self):
        """The comparison is the load-bearing line. Independence of the operands is worthless
        if the ``!=`` is deleted, so pin the refusal's own shape too."""
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert "if CANONICAL_PINS != XASSET_0044_CANONICAL_PINS:" in source

    def test_the_decision_records_the_correction_truthfully(self, decision_text):
        """The decision may not keep claiming an invariant the implementation never had.
        Pinned at the sentences that CARRY the corrected claim, not at a heading."""
        e = _section(decision_text, "E")
        assert "Bounded correction — MAJOR 1 of independent full review `4997532748`" in e
        assert "was source-vacuous" in e
        assert "`dict(CANONICAL_PINS)`" in e
        assert "never derived, copied, aliased, unpacked, or comprehended from `CANONICAL_PINS`" in e
        assert "being equal is fine, being equal *by construction*" in e
        assert "fixed **independently** of them" in e

    def test_the_correction_is_in_the_exhaustive_moved_list(self, decision_text):
        """SS-D claims to be exhaustive. A constant that moved and is not listed there would
        make that claim false, which is the same failure mode as an unstated rebinding."""
        d = _section(decision_text, "D")
        assert "`XASSET_0044_CANONICAL_PINS`" in d
        assert "`dict(CANONICAL_PINS)` → the two exact historical **literals**" in d
        assert XASSET0044_HISTORICAL_PROTOCOL_SHA256[:8] in d
        assert XASSET0044_HISTORICAL_PREREGISTRATION_SHA256[:8] in d

    def test_the_decision_does_not_still_assert_the_uncorrected_claim(self, decision_text):
        """The review's finding was that SS-E/Rationale asserted a protection the code did not
        implement. Assert the repaired text is present AND that it is qualified, so a future
        edit cannot quietly restore the unqualified version."""
        assert "the freeze is\nnow mechanical" in decision_text
        assert "A check is only as real as the\nindependence of what it compares against" in (
            decision_text
        )

    def test_the_register_records_the_correction(self, register_text):
        """The register is the operational surface a later session reads first. A correction
        that changed a load-bearing guard and is invisible there is a correction that a
        successor will not know happened."""
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        gate = next(
            g for g in ws["milestones"]
            if g["gate"] == "xasset0047-post-merge-ci-recovery-reconciliation"
        )
        text = " ".join(gate["description"].split())
        assert "BOUNDED CORRECTION, MAJOR 1 of independent full review 4997532748" in text
        assert "SOURCE-VACUOUS" in text
        assert "dict(CANONICAL_PINS)" in text
        assert "EQUAL IN VALUE" in text
        assert "being equal BY CONSTRUCTION was" in text
        assert "No canonical byte, current pin value, universe value," in text
