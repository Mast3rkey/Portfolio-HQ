"""Adversarial tests pinning the ``XASSET-0045`` post-merge-CI recovery authorization.

``XASSET-0044`` merged with a drift-free tree, a clean final review, principal acceptance, and
post-merge verification -- and then its **merge-commit CI failed**. ``XASSET-0044`` §L makes seven
conditions conjunctively necessary; its sixth requires *successful merge-commit CI whose ``head_sha``
is the exact merge SHA*. That run failed, the seventh condition (final post-CI lifecycle closure)
correctly never happened, and ``XASSET-0044`` is therefore **not effective**.

The danger this suite exists to prevent is not the recovery. It is the set of shortcuts a later
session could read into a filing that sits one merged-but-ineffective rebinding away from an armable
Stage 1:

1. **A later green CI run treated as repairing the failed run.** ``TestFailedRunIsImmutable`` --
   §L.6's own words exclude runs against any other commit, and the failed commit is immutable.
2. **The comparison anchor left moving.** ``TestClosedRangeIsExactAndImmutable`` -- the authorized
   correction must use the closed range, never ``merge-base(HEAD, origin/main)``.
3. **The defect mislabelled as merge drift or outcome-surface drift.** ``TestDefectIsAMovingAnchor``
   -- proven from the git object store, not asserted.
4. **More than one future unit authorized, or the recovery folded into this filing.**
   ``TestExactlyOneFutureUnit`` and ``TestFilingIsDesignOnly``.
5. **``XASSET-0043`` reused, or ``XASSET-0044`` treated as effective.**
   ``TestPredecessorAuthorityIsSpent``.
6. **The successor lifecycle anchor requirement dropped.** ``TestSuccessorLifecycleAnchorRequired``.
7. **The original adverse history relabelled, ignored, or quietly dropped.**
   ``TestAdverseHistoryPreserved``.
8. **Activation authority acquired by implication.** ``TestZeroActivationAuthority``.
9. **Fail-closed softened into a judgement call.** ``TestFailClosed``.
10. **The register or catalog desynchronised, or a section left vacuous.**
    ``TestCatalogAndRegisterSynchronisation`` and ``TestNoSectionIsVacuous``.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No attestation, claim, completion, lane directory, or ledger entry is created or read
for authorization purposes. No ``risk_lane_boundary`` protected result path is read, listed, opened,
or referenced. No module capable of producing a Stage-1 outcome is imported.
"""

from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent

DECISION_ID = "XASSET-0045"
DECISION_PATH = ROOT / (
    "governance/decisions/"
    "XASSET-0045-endpoint-0001-stage-1-post-merge-ci-recovery-authorization.md"
)
CATALOG_PATH = ROOT / "governance/decisions.yaml"
REGISTER_PATH = ROOT / "operations/WORKSTREAMS.yaml"
SUITE_PATH = Path(__file__).resolve()
REGISTER_GATE = "xasset0045-post-merge-ci-recovery-authorization"

# ── The immutable facts this authorization is built on ──────────────────────────────────────
#
# Every one of these was independently re-derived from live git and live GitHub during the
# filing session and is asserted here against the real object store, never taken on trust.

#: PR #344's base -- the ``XASSET-0043`` merge.
PR344_BASE_SHA = "0709d2f05ab031ecb6f69c40465ed4a227983aed"
#: PR #344's accepted head -- the exact commit review 4989080551 examined.
PR344_ACCEPTED_HEAD = "9c2821ab9e0e0dff09f5a03da5a6034775b00750"
#: PR #344's merge commit -- and the ``head_sha`` of the FAILED merge-commit CI run.
PR344_MERGE_SHA = "f5dedce1d1d3116ed8a6845c4447388c85a5414c"
#: The tree carried by BOTH the accepted head and the merge -- zero merge drift.
PR344_MERGE_TREE = "bd9ce6694261a7b4fb664a5121d04571f9606924"

#: The FAILED merge-commit CI run and job at ``PR344_MERGE_SHA``. Immutable adverse history.
FAILED_CI_RUN = "32439614683"
FAILED_CI_JOB = "96647501864"

#: The lifecycle evidence that DID complete, preserved as authenticated predecessor evidence.
FINAL_CLEAN_REVIEW = "4989080551"
PRINCIPAL_ACCEPTANCE_COMMENT = "5364401900"
POST_MERGE_VERIFICATION_COMMENT = "5364422640"
AUDITABLE_STOP_COMMENT = "5364490220"

#: The independent FULL review that found the effectivity deadlock BLOCKING, and under which
#: the principal separately authorized this filing's one narrow, test-only enabling correction.
REVIEW_THAT_REQUIRED_THE_CORRECTION = "4989608238"
#: This PR's own reviewed head, and its RED exact-head CI -- retained as correction history.
REVIEWED_HEAD_SHA = "e6e4874aca34f383f99cb130da3b45625d8c9aa3"
REVIEWED_HEAD_CI_RUN = "32443765403"
REVIEWED_HEAD_CI_JOB = "96659425926"

#: The guard whose moving anchor caused the failure, and its exact failing assertion line.
FAILING_GUARD_FILE = "test_overlap_model_validator.py"
FAILING_GUARD_LINE = 1119
FAILING_GUARD_TEST = "test_real_repository_governance_decisions_pass_the_repaired_check"

#: The one-use authorized ``XASSET-0042`` decision transition, by object identity.
AUTHORIZED_DECISION_RELPATH = (
    "governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md"
)
AUTHORIZED_OLD_BLOB = "e4cda7a5042da68f347598a62d9e6d5cfc40ae55"
AUTHORIZED_NEW_BLOB = "b08a625a5adb840e9576e5cd9218be24e63bd57e"

#: Universe identity -- must be untouched by a design-only filing.
UNIVERSE_CONSTRUCTIONS = 680
UNIVERSE_CELLS = 48
UNIVERSE_AGGREGATE_HASH = (
    "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
)

#: Paths a design-only filing must not touch.
PROTECTED_RELPATHS = (
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    "level1_construction_universe_closure_validator.py",
    "level1_stage1_execution_authorization.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "allocate.py",
    "margin_state.py",
    "levels.py",
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
)

#: The ONE file this filing lawfully corrects, under the separate principal authorization
#: recorded in XASSET-0045 §K after review 4989608238's BLOCKING finding. It is deliberately
#: NOT in PROTECTED_RELPATHS any more -- but it is not unguarded either: the tests below
#: require the change to be present, to be exactly the narrow re-anchoring authorized, and to
#: leave the moving resolver in place for the live working-tree guard it legitimately serves.
ENABLING_CORRECTION_RELPATH = "test_overlap_model_validator.py"


# ── PR #345's OWN closed range ──────────────────────────────────────────────────────────────
#
# CORRECTED under XASSET-0046, on separate explicit principal authority.
#
# Two assertions below claimed a fact about WHAT PR #345 CHANGED -- immutable history -- while
# measuring it with ``git diff --name-only origin/main``, a comparison whose base is wherever
# ``origin/main`` happens to point. On the filing branch that base was PR #345's own base and
# both assertions measured the real change set. On merged ``main`` ``HEAD == origin/main``, the
# comparison collapses to empty, and the two assertions fail in OPPOSITE directions:
#
#   test_the_enabling_correction_was_actually_performed  -> target absent from an empty set
#                                                           -> DETERMINISTIC FAILURE, and this
#                                                              is exactly what run 32490789238
#                                                              recorded at the merge SHA.
#   test_no_protected_path_was_touched_by_this_filing    -> empty & PROTECTED == empty
#                                                           -> VACUOUS PASS: the claim is
#                                                              satisfied by measuring nothing.
#
# This is the SAME defect class XASSET-0045 itself corrected one layer down, reintroduced by
# XASSET-0045 in its own new supporting artifact. Both are now anchored to PR #345's immutable
# closed range, by exact object identity, reading no moving reference at all.

#: PR #345's base -- PR #344's merge commit, and the closed range's first endpoint.
PR345_BASE_SHA = "f5dedce1d1d3116ed8a6845c4447388c85a5414c"
#: PR #345's accepted head -- the exact commit final clean review 4993994386 examined and the
#: exact head principal acceptance 5370936620 named.
PR345_ACCEPTED_HEAD = "61e629f0f655ce8ca4ccd7eaa370d132d593515c"
#: PR #345's merge commit -- and the ``head_sha`` of its own FAILED merge-commit CI run.
PR345_MERGE_SHA = "2f8cdebe14925021171b9779453946be1f69b506"
#: The tree carried by BOTH the accepted head and the merge -- zero merge drift.
PR345_MERGE_TREE = "e5eb890550d55aa74c7430871f176761526b1ecf"

#: The enabling correction's exact one-use transition over that range, by object identity.
#: Both ends are independently derived from git objects and independently required: path
#: equality is not identity, and a status alone does not prove which bytes moved where.
PR345_CORRECTION_OLD_BLOB = "5b916d881ed83db164233091863f2af87fa50828"
PR345_CORRECTION_NEW_BLOB = "536bf08bb7db81ffad15dcfa1de6e9ce4fca4899"
#: The exact status the enabling correction must carry -- a modification, never an addition,
#: deletion, rename, or copy.
PR345_CORRECTION_STATUS = "M"

#: PR #345's own accepted scope, from its pull-request metadata. Shared by the scope pin and
#: the non-vacuity pin so that widening either one alone is caught by the other.
PR345_CHANGED_FILE_COUNT = 12

#: ADDED BY XASSET-0047: the merge that made XASSET-0046 effective, and this repository's
#: ``main`` after PR #346. WS-0014's shared live "where main is now" field advances to it under
#: OPS-0001's Active-GitHub-fields rule; every anchor THIS decision authorizes against is
#: unchanged.
XASSET0047_MAIN_SHA = "0b76c09f8d1aba01780b4f06fdd692f7393fbfd3"
#: ADVANCED BY XASSET-0048: PR #347 merged at `bb95ed26`, so the register's shared live
#: "where main is now" field lawfully advanced again under OPS-0001's Active-GitHub-fields
#: rule. The anchor each decision authorizes against is unchanged; only the shared
#: self-reference moved. The assertion stays EXACT and is bound at BOTH ends.
XASSET0048_MAIN_SHA = "bb95ed26964b1bc7a2e230c76060fec82752efa1"

#: XASSET-0045's OWN failed merge-commit CI run and job, at PR345_MERGE_SHA. Immutable adverse
#: history, on exactly the footing PR #344's own failed run occupies: never re-run, relabelled,
#: waived, or represented as successful.
XASSET0045_FAILED_CI_RUN = "32490789238"
XASSET0045_FAILED_CI_JOB = "96797667282"

#: The functions whose SUBJECT is immutable history AND which this filing is authorized to
#: hold to the rule. None of them may consult a moving reference -- not in an assertion, and
#: not in a skip guard, because a historical proof that can be silenced by where a live ref
#: points is not a proof of history.
#:
#: ``test_on_merged_main_the_moving_base_collapses_to_head_itself`` WAS deliberately absent, and
#: its absence was a scope fact rather than a technical one. That pre-existing test carried an
#: ``origin/main`` skip guard which an earlier revision of XASSET-0046 removed -- a THIRD
#: correction, outside a principal authorization expressly bounded to exactly two. Independent
#: FULL review 4995297886 found that BLOCKING, the correction was reverted, and XASSET-0046 §G.11
#: carried the observation forward as a requirement on the recovery unit rather than acting on it.
#:
#: XASSET-0047 IS THAT UNIT, and it classified the use on its own evidence, reproduced the
#: behaviour by execution in an isolated clone before changing anything, and corrected it under
#: SS-G.11's own operative duty to re-anchor every historical use in the files it touches. The
#: function is therefore DECLARED here now -- loudly, in the same filing that corrected it, which
#: is exactly what the superseded exclusion pin existed to force.
HISTORICAL_PROOF_FUNCTIONS = frozenset({
    "_assert_pr345_closed_range_facts",
    "test_the_enabling_correction_was_actually_performed",
    "test_no_protected_path_was_touched_by_this_filing",
    "test_the_closed_range_does_exercise_the_authorized_transition",
    "test_the_authorized_transition_matches_its_bound_blob_identities",
    "test_merge_drift_is_affirmatively_excluded_from_the_object_store",
    "test_the_accepted_head_is_the_second_parent_of_the_merge",
    "test_on_merged_main_the_moving_base_collapses_to_head_itself",
})

#: String literals that name a MOVING reference. Deliberately a small, explicit, closed set of
#: REFERENCE NAMES -- a broad heuristic would flag the prose and the AST checks that must
#: legitimately NAME these references in order to refuse them.
#:
#: ``merge-base`` is deliberately ABSENT: it is a subcommand, not a reference.
#: ``merge-base(<pinned>, <pinned>)`` is fully determined by immutable objects and is exactly
#: what reproduces the historical collapse; ``merge-base HEAD origin/main`` is caught by the
#: reference names it must pass, not by the subcommand. Flagging the subcommand itself would
#: refuse a sound proof and teach the wrong rule.
MOVING_REFERENCE_LITERALS = frozenset({
    "HEAD", "origin/main", "origin/HEAD", "@{u}", "@{upstream}", "main", "refs/remotes/origin/main",
})


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def _git_ok(*args: str) -> bool:
    return (
        subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).returncode
        == 0
    )


def _commit_exists(sha: str, repo_root: Path = ROOT) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=repo_root, capture_output=True, text=True,
    ).returncode == 0


def _pr345_range_is_present(repo_root: Path = ROOT) -> bool:
    """Whether ANY of PR #345's three anchors is in this checkout.

    Deliberately ``any``, not ``all``. A checkout holding none of the three is genuinely
    truncated and is an environment precondition; a checkout holding some but not all is a
    REFUSAL inside the helper, never a skip -- otherwise a single unresolvable object could
    silence the whole proof.
    """
    return any(
        _commit_exists(sha, repo_root)
        for sha in (PR345_BASE_SHA, PR345_ACCEPTED_HEAD, PR345_MERGE_SHA)
    )


def _assert_pr345_closed_range_facts(
    *,
    base_sha: str = PR345_BASE_SHA,
    accepted_head: str = PR345_ACCEPTED_HEAD,
    merge_sha: str = PR345_MERGE_SHA,
    merge_tree: str = PR345_MERGE_TREE,
    repo_root: Path = ROOT,
) -> dict[str, str]:
    """Prove PR #345's merge identity and return its exact change set, by status.

    Every anchor is an explicit argument and every one is an immutable object. Nothing here
    reads ``HEAD``, ``origin/main``, ``merge-base``, the working tree, or any other reference
    that moves as the repository advances -- so the facts proved are invariant on a feature
    branch, on merged ``main`` where ``HEAD == origin/main``, after ``main`` advances, and
    when unrelated later commits exist.

    An unresolvable object is a REFUSAL, never a skip; the caller decides whether a genuinely
    truncated checkout is an environment precondition (``_pr345_range_is_present``).
    """
    for label, sha in (
        ("base", base_sha), ("accepted head", accepted_head), ("merge", merge_sha),
    ):
        assert _commit_exists(sha, repo_root), f"PR #345's {label} {sha} is not resolvable"

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


def _blob_at(commit: str, relpath: str, repo_root: Path = ROOT) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"{commit}:{relpath}"],
        cwd=repo_root, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _flat(text: str) -> str:
    """Collapse all runs of whitespace to single spaces.

    The decision is hard-wrapped prose, so an exact phrase can straddle a newline. Matching
    against the flattened text keeps every assertion an EXACT phrase match while making it
    insensitive to where the paragraph happens to wrap. This is deliberately not a
    weakening: the full phrase must still be present, in order, verbatim.
    """
    return " ".join(text.split())


def _section(text: str, letter: str) -> str:
    """The body of one lettered Decision subsection, flattened.

    Scoping an assertion to the section where a claim is OPERATIVE is what makes it
    mutation-sensitive: a phrase that also appears in a summary elsewhere can no longer
    satisfy a check on the section that actually carries the rule.
    """
    marker = f"\n### {letter}. "
    assert marker in text, f"section {letter} is missing"
    body = text.split(marker, 1)[1]
    body = re.split(r"\n### [A-N]\. |\n## ", body, maxsplit=1)[0]
    return _flat(body)


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_flat() -> str:
    return _flat(DECISION_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def decision_flat_lower() -> str:
    return _flat(DECISION_PATH.read_text(encoding="utf-8")).lower()


@pytest.fixture(scope="module")
def register():
    return yaml.safe_load(REGISTER_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ws0014(register):
    return next(w for w in register["workstreams"] if w.get("id") == "WS-0014")


@pytest.fixture(scope="module")
def gate(ws0014):
    matches = [g for g in ws0014["milestones"] if g.get("gate") == REGISTER_GATE]
    assert len(matches) == 1, f"expected exactly one {REGISTER_GATE} gate, found {len(matches)}"
    return matches[0]


@pytest.fixture(scope="module")
def catalog_entry():
    catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))["decisions"]
    matches = [d for d in catalog if d.get("decision_id") == DECISION_ID]
    assert len(matches) == 1, f"expected exactly one {DECISION_ID} catalog entry"
    return matches[0]


# ======================================================================================
# 1 -- The defect is a MOVING TEST ANCHOR, proven, not asserted
# ======================================================================================


class TestDefectIsAMovingAnchor:
    def test_the_historical_failure_location_is_recorded_by_the_decision(self):
        """At the reviewed head the defect sat at ``FAILING_GUARD_FILE:FAILING_GUARD_LINE``.
        That location is now HISTORY -- the correction rewrote the guard -- so the check is
        that the decision records it faithfully, not that the line still holds the defect.
        Superseding ``test_the_failing_guard_and_line_exist_and_are_the_named_assertion``,
        which verified the pre-correction location and would now assert a fiction."""
        text = DECISION_PATH.read_text(encoding="utf-8")
        assert f"{FAILING_GUARD_FILE}:{FAILING_GUARD_LINE}" in text
        assert FAILING_GUARD_TEST in text

    def test_the_corrected_guard_exists_and_delegates_to_the_closed_range_helper(self):
        """The live half of the superseded check: the named test still exists, and it now
        proves the property through the immutable-range helper rather than inline against a
        moving base."""
        source = (ROOT / FAILING_GUARD_FILE).read_text(encoding="utf-8")
        node = next(
            n for n in ast.walk(ast.parse(source))
            if isinstance(n, ast.FunctionDef) and n.name == FAILING_GUARD_TEST
        )
        called = {
            c.func.id for c in ast.walk(node)
            if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
        }
        assert "_assert_authorized_decision_transitions_over_closed_range" in called
        assert "_resolve_pr_base_sha" not in called

    def test_the_guard_resolves_its_base_through_a_moving_merge_base(self):
        """The defect's mechanism: the base is a function of HEAD and origin/main, so it
        moves. Proven from the guard's own source, not from prose."""
        source = (ROOT / FAILING_GUARD_FILE).read_text(encoding="utf-8")
        tree = ast.parse(source)
        resolver = next(
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "_resolve_pr_base_sha"
        )
        body = ast.get_source_segment(source, resolver) or ""
        assert "merge-base" in body
        assert '"HEAD"' in body
        assert '"origin/main"' in body

    def test_on_merged_main_the_moving_base_collapses_to_head_itself(self):
        """On merged ``main`` the merge-base of HEAD and origin/main IS the merge commit, so
        the comparison is empty. This is the whole failure, reproduced from real git.

        CORRECTED UNDER XASSET-0047, per XASSET-0046 SS-G.11. This function's subject is
        immutable history and its computation is fully pinned: BOTH operands of the ``merge-base``
        below are the same immutable commit, and ``origin/main`` appears nowhere in the
        computation, in either operand, or in the assertion. It nevertheless carried an
        ``origin/main`` skip guard, so a live reference could silence a proof about immutable
        history for a reason unrelated to that history.

        CLASSIFIED ON THIS UNIT'S OWN EVIDENCE, not on SS-G.11's word, and REPRODUCED BY EXECUTION
        before being changed: in an isolated clone with ``origin`` removed so ``origin/main`` is
        genuinely unresolvable, and with PR #344's merge present, ``merge-base`` returned
        ``f5dedce1...`` and the diff was empty -- the proof succeeded completely, and the removed
        guard would have skipped it anyway.

        The remaining guard is KEPT and is a genuine environment precondition: in a truncated
        checkout the pinned commit may be absent, which is the same treatment
        :func:`_pr345_range_is_present` already gives that case. Removing a skip that could
        silence a PASSING proof makes this guard strictly harder to satisfy -- it now always
        runs -- which is a strengthening under XASSET-0046 SS-G.13, never a relaxation.
        """
        if not _git_ok("cat-file", "-e", f"{PR344_MERGE_SHA}^{{commit}}"):
            pytest.skip("PR #344's merge commit is not present in this checkout")
        base = _git("merge-base", PR344_MERGE_SHA, PR344_MERGE_SHA)
        assert base == PR344_MERGE_SHA
        diff = _git("diff", "--name-status", base, PR344_MERGE_SHA, "--", "governance/decisions")
        assert diff == "", f"expected an empty comparison, got: {diff!r}"

    def test_the_closed_range_does_exercise_the_authorized_transition(self):
        """The property the guard exists to enforce is TRUE over the closed range. Only the
        anchor is wrong -- so the correction must re-anchor, never delete."""
        for sha in (PR344_BASE_SHA, PR344_ACCEPTED_HEAD):
            if not _git_ok("cat-file", "-e", f"{sha}^{{commit}}"):
                pytest.skip("PR #344's closed range is not present in this checkout")
        diff = _git(
            "diff", "--name-status", PR344_BASE_SHA, PR344_ACCEPTED_HEAD, "--", "governance/decisions"
        )
        rows = [line.split("\t") for line in diff.splitlines() if line.strip()]
        modified = [rest for status, rest in rows if status.startswith("M")]
        assert modified == [AUTHORIZED_DECISION_RELPATH], modified

    def test_the_authorized_transition_matches_its_bound_blob_identities(self):
        """Path equality is not identity. Both blob ends must match exactly."""
        for sha in (PR344_BASE_SHA, PR344_ACCEPTED_HEAD):
            if not _git_ok("cat-file", "-e", f"{sha}^{{commit}}"):
                pytest.skip("PR #344's closed range is not present in this checkout")
        assert _git("rev-parse", f"{PR344_BASE_SHA}:{AUTHORIZED_DECISION_RELPATH}") == (
            AUTHORIZED_OLD_BLOB
        )
        assert _git("rev-parse", f"{PR344_ACCEPTED_HEAD}:{AUTHORIZED_DECISION_RELPATH}") == (
            AUTHORIZED_NEW_BLOB
        )

    def test_the_decision_names_the_defect_as_a_moving_anchor_not_drift(self, decision_flat_lower):
        assert "moving test anchor" in decision_flat_lower
        assert "neither merge drift nor outcome-surface drift" in decision_flat_lower

    def test_merge_drift_is_affirmatively_excluded_from_the_object_store(self):
        """Not merge drift -- proven. The merge tree equals the accepted-head tree."""
        for sha in (PR344_MERGE_SHA, PR344_ACCEPTED_HEAD):
            if not _git_ok("cat-file", "-e", f"{sha}^{{commit}}"):
                pytest.skip("PR #344's commits are not present in this checkout")
        assert _git("rev-parse", f"{PR344_MERGE_SHA}^{{tree}}") == PR344_MERGE_TREE
        assert _git("rev-parse", f"{PR344_ACCEPTED_HEAD}^{{tree}}") == PR344_MERGE_TREE

    def test_the_accepted_head_is_the_second_parent_of_the_merge(self):
        if not _git_ok("cat-file", "-e", f"{PR344_MERGE_SHA}^{{commit}}"):
            pytest.skip("PR #344's merge commit is not present in this checkout")
        parents = _git("rev-list", "--parents", "-n", "1", PR344_MERGE_SHA).split()
        assert parents[0] == PR344_MERGE_SHA
        assert parents[1:] == [PR344_BASE_SHA, PR344_ACCEPTED_HEAD], parents[1:]


# ======================================================================================
# 2 -- No later CI run repairs the failed run
# ======================================================================================


class TestFailedRunIsImmutable:
    def test_the_decision_states_a_later_run_cannot_retroactively_satisfy_l6(self, decision_flat_lower):
        assert "cannot retroactively satisfy" in decision_flat_lower
        assert "permanently unsatisfiable" in decision_flat_lower

    def test_the_decision_quotes_l6s_own_exclusion_of_other_commits(self, decision_flat):
        """The exclusion must rest on §L.6's own words, not on this filing's preference."""
        assert "not a run against any other commit" in decision_flat

    def test_the_decision_never_claims_a_later_run_repairs_the_failed_one(self, decision_text):
        """Mutation pin: the decision must contain no sentence licensing repair by re-run."""
        lowered = decision_text.lower()
        forbidden = (
            "a later green run satisfies",
            "a subsequent successful run satisfies",
            "re-running the failed job satisfies",
            "may be treated as satisfying",
            "retroactively satisfies",
            "retroactively satisfied",
        )
        for phrase in forbidden:
            assert phrase not in lowered, phrase

    def test_xasset_0044_is_never_described_as_effective(self, decision_text):
        lowered = _flat(decision_text).lower()
        # The §D statement, verbatim: not merely "not effective now", but incapable of
        # becoming effective through the pull request that failed its own §L.6 condition.
        assert (
            "`xasset-0044` is **not effective and cannot become effective through pr #344**"
            in lowered
        )
        for phrase in (
            "xasset-0044 is effective",
            "xasset-0044 becomes effective",
            "xasset-0044 is now effective",
            "provisionally effective",
        ):
            # "provisionally effective" may only appear inside an explicit prohibition.
            if phrase == "provisionally effective":
                idx = lowered.find(phrase)
                if idx != -1:
                    window = lowered[max(0, idx - 200) : idx + 60]
                    assert "may not" in window or "no session" in window, window
                continue
            assert phrase not in lowered, phrase

    def test_the_exact_failed_run_and_job_identities_are_recorded(self, decision_text):
        assert FAILED_CI_RUN in decision_text
        assert FAILED_CI_JOB in decision_text

    def test_the_failed_run_is_bound_to_the_exact_merge_sha(self, decision_text):
        """A run identity with no commit identity beside it proves nothing."""
        assert PR344_MERGE_SHA in decision_text
        idx = decision_text.find(FAILED_CI_RUN)
        assert idx != -1
        window = decision_text[max(0, idx - 400) : idx + 400]
        assert "f5dedce1" in window, window


# ======================================================================================
# 3 -- Exactly one future unit, and it is separate
# ======================================================================================


class TestExactlyOneFutureUnit:
    def test_the_grant_is_exactly_one(self, decision_flat):
        assert "**exactly one** future, separate, bounded pull request" in decision_flat

    def test_no_second_unit_is_authorized_by_completing_the_first(self, decision_flat):
        assert "completing the authorized unit does not authorize another" in decision_flat

    def test_the_future_unit_must_file_its_own_decision(self, decision_flat_lower):
        assert "file its own decision" in decision_flat_lower

    def test_the_successor_identifier_is_not_predicted_or_reserved(self, decision_flat_lower):
        """A reserved identifier is a second authorization by another name."""
        assert "verified unused against live repository state" in decision_flat_lower
        assert "never predicted, reserved, or assumed here" in decision_flat_lower
        assert "names no successor identifier" in decision_flat_lower

    def test_no_xasset_identifier_beyond_0045_is_named_anywhere(self, decision_text):
        """Mutation pin: naming XASSET-0046 would silently pre-authorize it."""
        named = set(re.findall(r"XASSET-00\d\d", decision_text))
        beyond = {n for n in named if int(n.split("-")[1]) > 45}
        assert beyond == set(), beyond


# ======================================================================================
# 4 -- Predecessor authority is spent; nothing is reused
# ======================================================================================


class TestPredecessorAuthorityIsSpent:
    def test_xasset_0043s_single_grant_is_recorded_as_spent(self, decision_flat_lower):
        assert "spent" in decision_flat_lower
        assert "consumed by being used" in decision_flat_lower

    def test_xasset_0043_may_not_be_reused(self, decision_flat_lower):
        assert "may not be reused" in decision_flat_lower

    def test_the_reason_the_grant_is_spent_does_not_depend_on_effectivity(self, decision_flat_lower):
        """The distinction that makes §E sound: a grant is spent by use, while effectivity
        governs whether the rebinding takes effect. Collapsing the two would revive §F."""
        assert "whether or not" in decision_flat_lower
        assert "effectivity governs whether the *rebinding takes effect*" in decision_flat_lower

    def test_authority_derives_from_this_decision_and_nothing_else(self, decision_flat):
        assert "from **this** decision, and from nothing else" in decision_flat


# ======================================================================================
# 5 -- The closed range is exact and immutable
# ======================================================================================


class TestClosedRangeIsExactAndImmutable:
    def test_both_endpoints_are_named_exactly(self, decision_text):
        assert PR344_BASE_SHA in decision_text
        assert PR344_ACCEPTED_HEAD in decision_text

    def test_the_correction_is_required_against_the_closed_range(self, decision_flat_lower):
        assert "closed" in decision_flat_lower
        assert "immutable" in decision_flat_lower
        assert "rather than any moving merge-base" in decision_flat_lower

    def test_a_moving_head_or_origin_main_guard_is_forbidden(self, decision_flat):
        assert (
            "**No moving `HEAD`/`origin/main` guard may claim historical byte identity**"
            in decision_flat
        )

    def test_the_corrected_guard_must_not_depend_on_where_head_points(self, decision_flat_lower):
        assert (
            "still does not depend on where `head` or `origin/main` point when it runs"
            in decision_flat_lower
        )

    def test_the_one_use_transition_conjuncts_stay_independently_required(self, decision_text):
        assert AUTHORIZED_OLD_BLOB in decision_text
        assert AUTHORIZED_NEW_BLOB in decision_text
        assert "each conjunct independently required" in decision_text.lower()

    def test_dead_permission_protection_is_retained_not_dropped(self, decision_text):
        assert "dead permission" in decision_text.lower()

    def test_other_pre_existing_decisions_stay_protected(self, decision_flat_lower):
        assert "every other pre-existing decision file must remain protected" in decision_flat_lower


# ======================================================================================
# 6 -- The successor lifecycle anchor is required
# ======================================================================================


class TestSuccessorLifecycleAnchorRequired:
    def test_the_requirement_exists_and_is_named(self, decision_flat_lower):
        assert "successor lifecycle anchor" in decision_flat_lower

    def test_the_reason_is_the_current_production_binding(self, decision_text):
        """The requirement must be grounded in what production actually binds today."""
        assert 'AUTHORIZING_DECISION = "XASSET-0044"' in decision_text
        assert "AUTHORIZING_PULL_REQUEST = 344" in decision_text
        assert "REVIEWED_BASE_SHA" in decision_text

    def test_production_no_longer_binds_the_stopped_lifecycle(self):
        """Not a claim about the repository -- a check of it.

        ADVANCED BY XASSET-0047, which is the unit XASSET-0046 §G.6 authorized and which
        PERFORMED the rebinding this class exists to require. The subject here is LIVE state, so
        it moved when the anchor lawfully moved; XASSET-0046's own §G.6 text, which grounds the
        requirement in what production bound at the time, is immutable and is still asserted
        verbatim by :meth:`test_the_reason_is_the_current_production_binding` above.

        Bound at BOTH ends. The stopped lifecycle's anchor must be GONE -- a silent revert to an
        anchor whose merge-commit CI failed permanently is the exact regression this refuses --
        and the current anchor must be present and must not be either stopped decision.
        """
        module = (ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        # The permanently unusable anchor is gone, in all three of its parts.
        assert 'AUTHORIZING_DECISION = "XASSET-0044"' not in module
        assert "AUTHORIZING_PULL_REQUEST = 344" not in module
        assert f'REVIEWED_BASE_SHA = "{PR344_BASE_SHA}"' not in module
        # ... and the live module binds the successor anchor instead.
        import level1_stage1_execution_authorization as auth

        # RE-ANCHORED BY XASSET-0049, unchanged in KIND and still bound at BOTH ends. The
        # property protected here is that the live anchor is NOT the permanently unusable one and
        # IS a lifecycle that can close -- not that one particular successor holds it forever.
        # XASSET-0047 was that successor; XASSET-0049 lawfully succeeded it under XASSET-0048
        # SS-E, and XASSET-0047's own identity is preserved rather than erased.
        assert auth.AUTHORIZING_DECISION == "XASSET-0049"
        assert auth.PRIOR_RECONCILIATION_DECISION == "XASSET-0047"
        assert auth.AUTHORIZING_DECISION not in auth.PERMANENTLY_INEFFECTIVE_DECISIONS
        assert auth.AUTHORIZING_PULL_REQUEST not in auth.PERMANENTLY_INEFFECTIVE_PULL_REQUESTS
        # The reviewed base equals its own authority's merge -- the same equality, re-anchored
        # onto the decision that authorizes the CURRENT unit.
        assert auth.REVIEWED_BASE_SHA == auth.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA
        assert auth.PRIOR_RECONCILIATION_MERGE_BASE == auth.RECOVERY_AUTHORIZING_MERGE_SHA
        # The stopped lifecycle is PRESERVED as history, by exact identity, not erased.
        assert auth.STOPPED_REBINDING_DECISION == "XASSET-0044"
        assert auth.STOPPED_REBINDING_PULL_REQUEST == 344
        assert auth.STOPPED_REBINDING_MERGE_BASE == PR344_BASE_SHA

    def test_rebinding_is_bounded_to_strict_necessity(self, decision_flat_lower):
        assert "only as strictly necessary" in decision_flat_lower
        assert "may not be made more permissive" in decision_flat_lower

    def test_the_anchor_must_cover_the_full_future_lifecycle(self, decision_flat_lower):
        assert (
            "own** decision, pull request, accepted head, merge, successful exact-merge ci, "
            "and final closure"
        ) in decision_flat_lower


# ======================================================================================
# 7 -- Adverse history is preserved
# ======================================================================================


class TestAdverseHistoryPreserved:
    def test_the_failed_run_must_be_retained_by_exact_identity(self, decision_text):
        """Pinned in BOTH sections that carry it. The decision states the immutability twice,
        so a check on the bare phrase survives corruption of either statement alone."""
        assert (
            "**G.5 — Preserve the original failed run as immutable adverse history.**"
            in _section(decision_text, "G")
        )
        assert "remains immutable adverse history" in _section(decision_text, "N")

    def test_every_forbidden_disposal_of_the_failed_run_is_named(self, decision_flat_lower):
        lowered = decision_flat_lower
        for verb in (
            "relabelled successful",
            "deleted",
            "suppressed",
            "re-run in place",
            "described as passing",
            "represented as satisfying",
        ):
            assert verb in lowered, verb

    def test_the_stop_notice_is_preserved(self, decision_text):
        assert AUDITABLE_STOP_COMMENT in decision_text

    def test_the_completed_predecessor_evidence_is_preserved(self, decision_text):
        for identity in (
            FINAL_CLEAN_REVIEW,
            PRINCIPAL_ACCEPTANCE_COMMENT,
            POST_MERGE_VERIFICATION_COMMENT,
        ):
            assert identity in decision_text, identity

    def test_predecessor_evidence_may_not_be_erased_or_re_pointed(self, decision_flat_lower):
        assert "never erased, overwritten, or silently re-pointed" in decision_flat_lower


# ======================================================================================
# 8 -- Zero activation authority
# ======================================================================================


class TestZeroActivationAuthority:
    def test_every_withheld_activation_capability_is_named(self, decision_flat_lower):
        lowered = decision_flat_lower
        for capability in (
            "readiness verification",
            "drift verification",
            "step 11",
            "attestation",
            "lane state",
            "arm",
            "claim",
            "gate for any registered construction",
            "recovery execution",
            "results work",
            "protected `risk`",
        ):
            assert capability in lowered, capability

    def test_zero_activation_authority_is_stated_explicitly(self, decision_flat_lower):
        assert "zero activation authority" in decision_flat_lower

    def test_executable_stays_permanently_false(self, decision_flat_lower):
        assert "`stage_1_executability.executable` stays permanently `false`" in decision_flat_lower
        assert "no committed value in this repository" in decision_flat_lower

    def test_attempt_1_and_spent_grants_are_not_revived(self, decision_flat_lower):
        lowered = decision_flat_lower
        assert "re-open `attempt_1`" in lowered
        assert "xasset-0040" in lowered
        assert "stopped_before_attestation" in lowered
        assert "§p.1" in lowered

    def test_the_live_posture_really_is_unarmed(self):
        """The repository state itself, not the decision's description of it."""
        import level1_stage1_execution_authorization as auth

        assert auth.AUTHORIZATION_ROOT.exists() is False
        authorized, _reason = auth.new_execution_is_authorized()
        assert authorized is False
        assert auth.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

    def test_no_stage1_results_artifact_exists_anywhere(self):
        assert list(ROOT.rglob("stage1_results.yaml")) == []

    def test_this_suite_imports_no_outcome_producing_module(self):
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        forbidden = {
            "level1_stage1_runner",
            "level1_stage1_result_validator",
        }
        assert imported & forbidden == set(), imported & forbidden


# ======================================================================================
# 9 -- The filing is governance PLUS one narrow, separately authorized enabling correction
#
# Replaces the previous "design-only / does not correct the guard" pins, which review
# 4989608238 found BLOCKING: taken with §M.6 they made this authorization permanently
# unattainable. They are not deleted -- they are replaced by truthful pins on what the
# filing now actually does, and on the boundaries the correction must not cross.
# ======================================================================================


class TestFilingIsGovernancePlusOneEnablingCorrection:
    def test_the_decision_does_not_claim_to_be_purely_design_only(self, decision_flat_lower):
        assert "is **not** purely design-only, and does not claim to be" in decision_flat_lower

    def test_the_decision_states_the_correction_it_performs(self, decision_flat_lower):
        k = _section(DECISION_PATH.read_text(encoding="utf-8"), "K").lower()
        assert "test-only" in k
        assert "re-anchored" in k
        assert FAILING_GUARD_FILE in k

    def test_the_authority_for_the_correction_is_not_created_by_this_decision(self, decision_text):
        """The circularity guard. XASSET-0045 may not be its own enabling authority."""
        k = _section(decision_text, "K")
        assert "**The authority for that correction is not created by this decision.**" in k
        assert "cannot authorize its own enabling repair without circularity" in k
        assert "separate, explicit principal authorization" in k
        assert REVIEW_THAT_REQUIRED_THE_CORRECTION in k

    def test_the_correction_is_recorded_as_strictly_narrowing(self, decision_text):
        k = _section(decision_text, "K")
        assert "strictly narrowing in effect" in k
        assert (
            "Nothing was deleted, skipped, `xfail`ed, weakened, or replaced with a less "
            "falsifiable assertion." in k
        )

    def test_no_protected_path_was_touched_by_this_filing(self):
        """Proven against git over PR #345's IMMUTABLE closed range, not against a moving base.

        CORRECTED under XASSET-0046. The superseded form measured
        ``git diff --name-only origin/main``, which on merged ``main`` is empty -- so the
        claim "no protected path was touched" was satisfied by touching, and measuring,
        nothing. It reported a **vacuous pass**, which is worse than the sibling assertion's
        loud failure: a guard that cannot fail protects nothing.

        The input is therefore required to be non-empty BEFORE the intersection is taken, so
        an empty measurement can never again be mistaken for a clean one.
        """
        if not _pr345_range_is_present():
            pytest.skip("PR #345's closed range is not present in this checkout")
        changed = _assert_pr345_closed_range_facts()
        # Non-vacuity first: the intersection below is only meaningful over a real change set.
        # Pinned to PR #345's own accepted scope, shared with the scope pin in section 19, so
        # widening either site alone leaves the other site failing.
        assert len(changed) == PR345_CHANGED_FILE_COUNT, sorted(changed)
        overlap = set(changed) & set(PROTECTED_RELPATHS)
        assert overlap == set(), overlap

    def test_the_enabling_correction_was_actually_performed(self):
        """The correction must be real. A decision claiming a repair it did not make is the
        same class of untruth review 4989608238 found, pointing the other way.

        CORRECTED under XASSET-0046. The superseded form asked whether the file appears in
        ``git diff --name-only origin/main``; on merged ``main`` that set is empty and the
        assertion failed deterministically -- the single failure recorded by run
        ``XASSET0045_FAILED_CI_RUN`` at the exact merge SHA.

        The subject was always immutable history: what PR #345 changed. It is now measured
        over PR #345's closed range, and proved by object identity rather than by presence in
        a list. Each conjunct is independently required -- a path can appear with the wrong
        status, a status can be right while the bytes are not the authorized ones, and either
        blob alone leaves the other end unproven.
        """
        if not _pr345_range_is_present():
            pytest.skip("PR #345's closed range is not present in this checkout")
        changed = _assert_pr345_closed_range_facts()
        assert ENABLING_CORRECTION_RELPATH in changed, sorted(changed)
        assert changed[ENABLING_CORRECTION_RELPATH] == PR345_CORRECTION_STATUS, (
            changed[ENABLING_CORRECTION_RELPATH]
        )
        assert _blob_at(PR345_BASE_SHA, ENABLING_CORRECTION_RELPATH) == (
            PR345_CORRECTION_OLD_BLOB
        )
        assert _blob_at(PR345_ACCEPTED_HEAD, ENABLING_CORRECTION_RELPATH) == (
            PR345_CORRECTION_NEW_BLOB
        )
        assert PR345_CORRECTION_OLD_BLOB != PR345_CORRECTION_NEW_BLOB

    def test_the_corrected_file_is_not_load_bearing(self):
        """The correction may not reach the bound execution surface."""
        import level1_stage1_execution_authorization as auth

        assert ENABLING_CORRECTION_RELPATH not in auth.LOAD_BEARING_RELPATHS

    def test_the_corrected_guard_is_anchored_to_the_exact_closed_range(self):
        """Read from the corrected file itself, not from the decision's description of it."""
        import test_overlap_model_validator as guard

        assert guard.CLOSED_RANGE_BASE_SHA == PR344_BASE_SHA
        assert guard.CLOSED_RANGE_ACCEPTED_HEAD == PR344_ACCEPTED_HEAD
        assert guard.CLOSED_RANGE_MERGE_SHA == PR344_MERGE_SHA
        assert guard.CLOSED_RANGE_MERGE_TREE == PR344_MERGE_TREE

    def test_the_closed_range_anchors_are_plain_string_literals(self):
        """The AST check above inspects the FUNCTIONS. A moving reference could still be
        smuggled in by making an anchor CONSTANT computed -- e.g. assigning it from
        ``git merge-base HEAD origin/main`` at import time. Each anchor must therefore be a
        literal string, checked over the module's own AST."""
        source = (ROOT / ENABLING_CORRECTION_RELPATH).read_text(encoding="utf-8")
        wanted = {
            "CLOSED_RANGE_BASE_SHA", "CLOSED_RANGE_ACCEPTED_HEAD",
            "CLOSED_RANGE_MERGE_SHA", "CLOSED_RANGE_MERGE_TREE",
        }
        seen: set[str] = set()
        for node in ast.parse(source).body:
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in wanted:
                    assert isinstance(node.value, ast.Constant) and isinstance(node.value.value, str), (
                        f"{target.id} is not a plain string literal"
                    )
                    assert len(node.value.value) == 40, target.id
                    seen.add(target.id)
        assert seen == wanted, wanted - seen

    def test_the_corrected_guard_reads_no_moving_reference(self):
        """The whole point of the repair, verified over the corrected file's own AST."""
        source = (ROOT / ENABLING_CORRECTION_RELPATH).read_text(encoding="utf-8")
        tree = ast.parse(source)
        for name in (
            "_assert_authorized_decision_transitions_over_closed_range",
            "test_real_repository_governance_decisions_pass_the_repaired_check",
        ):
            node = next(
                n for n in ast.walk(tree)
                if isinstance(n, ast.FunctionDef) and n.name == name
            )
            literals = {
                c.value for c in ast.walk(node)
                if isinstance(c, ast.Constant) and isinstance(c.value, str)
            }
            for moving in ("HEAD", "origin/main", "merge-base"):
                assert moving not in literals, f"{name} still consults {moving!r}"

    def test_the_moving_resolver_survives_for_the_live_working_tree_guard(self):
        """The repair removed the moving resolver from the HISTORICAL assertion only. Deleting
        it repository-wide would break a guard whose subject legitimately IS a moving base."""
        import test_overlap_model_validator as guard

        assert callable(guard._resolve_pr_base_sha)
        source = (ROOT / ENABLING_CORRECTION_RELPATH).read_text(encoding="utf-8")
        node = next(
            n for n in ast.walk(ast.parse(source))
            if isinstance(n, ast.FunctionDef)
            and n.name == "_assert_no_unauthorized_change_since_base"
        )
        called = {
            c.func.id for c in ast.walk(node)
            if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
        }
        assert "_resolve_pr_base_sha" in called

    def test_the_universe_identity_is_unchanged(self, decision_text):
        assert str(UNIVERSE_CONSTRUCTIONS) in decision_text
        assert str(UNIVERSE_CELLS) in decision_text
        assert UNIVERSE_AGGREGATE_HASH in decision_text

    def test_the_reviewed_head_failure_is_retained_as_adverse_history(self, decision_text):
        """The red reviewed-head run is correction history and must not be erased."""
        n = _section(decision_text, "N")
        assert REVIEWED_HEAD_SHA in n
        assert REVIEWED_HEAD_CI_RUN in n
        assert REVIEWED_HEAD_CI_JOB in n
        assert "Retained as adverse history, not erased" in n

    def test_the_filing_no_longer_claims_its_own_ci_must_fail(self, decision_text):
        """The BLOCKING premise itself. Any surviving form of "this PR's CI necessarily
        fails" re-creates the deadlock, whatever wording it uses."""
        flat_lower = _flat(decision_text).lower()
        for claim in (
            "this filing's own ci will fail",
            "this pr's own ci will fail",
            "expect exact-head ci to show",
            "fails on **every** branch taken from",
            "necessarily fails",
            "must continue failing",
            "explicitly barred from editing",
        ):
            assert claim not in flat_lower, claim

    def test_pr344s_failed_run_is_still_immutable_adverse_history(self, decision_text):
        """Removing this filing's own failure premise must not touch PR #344's.

        Identity presence alone is too weak: §N states the non-repair twice, so a check on
        the identities plus the phrase "immutable adverse history" survives corruption of the
        operative sentence. That sentence is therefore pinned directly, and the repair claim
        is refused as a concept.
        """
        flat = _flat(decision_text)
        assert FAILED_CI_RUN in flat
        assert FAILED_CI_JOB in flat
        assert "immutable adverse history" in flat.lower()
        n = _section(decision_text, "N")
        assert (
            "Nothing here retroactively repairs PR #344's own failed merge-commit CI." in n
        )
        for claim in ("retroactively repairs", "retroactively repaired", "now considered repaired"):
            occurrences = flat.lower().count(claim)
            if claim == "retroactively repairs":
                # Permitted exactly once, and only inside the NEGATION pinned above.
                assert occurrences == 1, occurrences
                assert f"Nothing here {claim} PR #344" in flat, claim
            else:
                assert occurrences == 0, claim


# ======================================================================================
# 10 -- Fail-closed
# ======================================================================================


class TestFailClosed:
    def test_unobtainable_facts_are_errors_never_agreement(self, decision_flat_lower):
        assert "never silent agreement" in decision_flat_lower

    def test_ambiguity_is_a_stop_not_a_judgement_call(self, decision_flat_lower):
        assert "stop and disclose" in decision_flat_lower
        assert "is a **stop**, not a judgement call" in decision_flat_lower

    def test_repackaging_requires_a_stop(self, decision_flat_lower):
        assert "package it differently must **stop and disclose**" in decision_flat_lower

    def test_nothing_may_be_weakened(self, decision_flat_lower):
        lowered = decision_flat_lower
        for verb in ("deleted", "skipped", "`xfail`ed", "weakened"):
            assert verb in lowered, verb
        assert "less falsifiable" in lowered


# ======================================================================================
# 11 -- Effectivity requires the complete lifecycle
# ======================================================================================


class TestEffectivityRequiresCompleteLifecycle:
    def test_all_seven_conditions_are_present(self, decision_text):
        section = decision_text.split("### M. Effectivity", 1)[1]
        for n in range(1, 8):
            assert f"\n{n}. " in section, n

    def test_none_is_individually_sufficient(self, decision_text):
        assert "**None is individually sufficient.**" in decision_text

    def test_merge_does_not_arm(self, decision_flat_lower):
        assert "merging this arms nothing" in decision_flat_lower
        assert "still returns `false`" in decision_flat_lower

    def test_condition_six_names_the_exact_merge_sha_requirement(self, decision_text):
        section = decision_text.split("### M. Effectivity", 1)[1]
        assert "**successful merge-commit CI whose `head_sha` is the exact merge SHA**" in section


# ======================================================================================
# 12 -- Catalog and register synchronisation
# ======================================================================================


class TestCatalogAndRegisterSynchronisation:
    def test_the_catalog_entry_points_at_the_real_file(self, catalog_entry):
        assert catalog_entry["file"] == (
            "governance/decisions/"
            "XASSET-0045-endpoint-0001-stage-1-post-merge-ci-recovery-authorization.md"
        )
        assert (ROOT / catalog_entry["file"]).is_file()

    def test_the_catalog_entry_names_this_supporting_artifact(self, catalog_entry):
        assert catalog_entry["supporting_artifact"] == SUITE_PATH.name

    def test_the_decision_is_proposed_not_accepted_by_its_own_filing(self, catalog_entry):
        """A filing does not accept itself."""
        assert catalog_entry["status"] == "Proposed"

    def test_the_gate_is_in_progress_while_its_own_pr_is_unmerged(self, gate):
        assert gate["status"] == "in_progress"

    def test_the_gate_records_the_exact_immutable_facts(self, gate):
        description = gate["description"]
        for identity in (
            PR344_MERGE_SHA,
            PR344_BASE_SHA,
            PR344_ACCEPTED_HEAD,
            PR344_MERGE_TREE,
            FAILED_CI_RUN,
            FAILED_CI_JOB,
        ):
            assert identity in description, identity

    def test_the_gate_states_the_authorization_and_its_one_correction(self, gate):
        """Supersedes ``test_the_gate_states_the_authorization_is_design_only``. The register
        must describe what the filing actually is -- governance plus one narrow, separately
        authorized, test-only enabling correction -- and must retain the historical note that
        it originally read DESIGN-ONLY, so the change is visible rather than silent."""
        description = gate["description"]
        assert "GOVERNANCE AUTHORIZATION PLUS ONE NARROW" in description
        assert "TEST-ONLY" in description
        assert "originally read DESIGN-ONLY" in description
        # The amending review must be named in the amendment note itself, not merely
        # somewhere in the gate: the identity appears more than once here.
        assert (
            "amended after independent FULL review "
            f"{REVIEW_THAT_REQUIRED_THE_CORRECTION}" in description
        )

    def test_the_bounded_correction_gate_records_the_blocking_finding(self, ws0014):
        """The correction gate is additive, following PR #344's own precedent, and must
        name the finding, its authority, and the boundaries the correction did not cross."""
        gates = {g.get("gate"): g for g in ws0014["milestones"]}
        gate = gates[f"xasset0045-bounded-correction-after-full-review-{REVIEW_THAT_REQUIRED_THE_CORRECTION}"]
        assert gate["status"] == "in_progress"
        assert gate["pr"] == 345
        description = gate["description"]
        assert "could NEVER become" in description
        assert "SEPARATE, EXPLICIT PRINCIPAL AUTHORIZATION" in description
        assert "IMMUTABLE" in description
        assert PR344_BASE_SHA in description
        assert PR344_ACCEPTED_HEAD in description
        assert REVIEWED_HEAD_CI_RUN in description
        assert REVIEWED_HEAD_CI_JOB in description
        assert FAILED_CI_RUN in description
        assert "NOT retroactively repaired" in description
        # Flattened once, then asserted conjunctively -- an or-fallback pair here would be
        # satisfiable by whichever half happened to match and could hide the other.
        assert "NOT a member of LOAD_BEARING_RELPATHS" in _flat(description)

    def test_the_gate_states_exactly_one_future_unit(self, gate):
        assert "EXACTLY ONE future" in gate["description"]

    def test_workstream_live_fields_reflect_this_session(self, ws0014):
        """WS-0014's shared live self-reference fields. PR #344 has merged at ``f5dedce1``,
        so under ``OPS-0001``'s Active-GitHub-fields rule they lawfully advance to the unit
        that is now live. Each stays an exact value, never relaxed to a range."""
        # ADVANCED BY XASSET-0046, on exactly the terms the docstring above already states:
        # these are WS-0014's SINGLE SHARED live fields, PR #345 has since merged at
        # `2f8cdebe`, and they lawfully advance again to whatever unit is now live. The
        # anchor THIS decision authorizes against is unchanged; only the shared
        # self-reference moved. Bound at BOTH ends -- the exact current value, and the closed
        # value it must no longer be showing.
        # ADVANCED AGAIN BY XASSET-0047, identically: PR #346 has since merged at `0b76c09f`,
        # so the shared fields advance once more to the recovery unit that is now live. Every
        # superseded value is retained below as a negative pin, so nothing is relaxed.
        assert ws0014["last_verified_main_sha"] == XASSET0048_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0047_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != PR345_MERGE_SHA
        assert ws0014["last_verified_main_sha"] != PR344_MERGE_SHA
        assert str(ws0014["last_verified_date"]) == "2026-08-22"
        assert ws0014["active_branch"] != "claude/xasset-0043-rebinding-7ywmdx"
        assert ws0014["active_branch"] != "claude/xasset-0045-filing-9yxavw"
        assert ws0014["active_branch"] != "claude/xasset-0045-test-governance-103t6t"

    def test_workstream_stays_secondary_and_no_primary_is_introduced(self, register, ws0014):
        assert ws0014["status"] == "proposed"
        assert ws0014["priority"] == "secondary"
        primary = [w["id"] for w in register["workstreams"] if w.get("priority") == "primary"]
        assert primary == []

    def test_pr_344s_own_closed_record_survives_as_history(self, ws0014):
        """Advancing WS-0014's SHARED live self-reference fields must not erase the
        predecessor's own closed record. That record lives in its own gate -- which keeps
        `pr: 344` -- not in the shared live fields, which by design point only at the unit
        that is currently live."""
        gates = {g.get("gate"): g for g in ws0014["milestones"]}
        predecessor = gates["xasset0044-post-correction-operational-rebinding"]
        assert predecessor["pr"] == 344
        assert PR344_BASE_SHA in predecessor["description"]


# ======================================================================================
# 13 -- No section is vacuous
# ======================================================================================


class TestNoSectionIsVacuous:
    def test_every_lettered_section_exists_and_has_substance(self, decision_text):
        headings = re.findall(r"^### ([A-N])\. (.+)$", decision_text, flags=re.MULTILINE)
        letters = [h[0] for h in headings]
        assert letters == list("ABCDEFGHIJKLMN"), letters
        for letter, _title in headings:
            body = decision_text.split(f"### {letter}. ", 1)[1]
            body = re.split(r"\n### [A-N]\. |\n## ", body, maxsplit=1)[0]
            assert len(body.split()) > 25, f"section {letter} is too thin"

    def test_the_required_properties_are_numbered_g1_to_g12(self, decision_text):
        section = decision_text.split("### G. Required properties", 1)[1]
        section = section.split("### H.", 1)[0]
        for n in range(1, 13):
            assert f"**G.{n} —" in section, n

    def test_the_alternatives_section_records_real_rejections(self, decision_text):
        section = decision_text.split("## Alternatives Considered", 1)[1]
        section = section.split("## Consequences", 1)[0]
        assert section.lower().count("rejected") >= 5

    def test_this_suite_contains_no_vacuous_assertion(self):
        """No ``assert ... or True``-style disjunct, and no bare truthy constant, may hide a
        false premise anywhere in this file. Checked over the parsed AST, not by substring
        scan -- a text search would flag the very comments that explain the rule."""
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        asserts = [n for n in ast.walk(tree) if isinstance(n, ast.Assert)]
        assert len(asserts) > 60, len(asserts)
        for node in asserts:
            test = node.test
            if isinstance(test, ast.Constant):
                pytest.fail(f"bare constant assertion at line {node.lineno}")
            if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.Or):
                for value in test.values:
                    if isinstance(value, ast.Constant) and bool(value.value):
                        pytest.fail(f"constant-truthy disjunct at line {node.lineno}")


# ======================================================================================
# 14 -- Every identity in the decision is a KNOWN identity
#
# Existence checks ("this SHA appears somewhere") cannot detect a corrupted occurrence
# while a correct one survives elsewhere. These close that gap from the other side: the
# decision may contain NO identity-shaped token that is not on an explicit whitelist, so
# altering any occurrence of any SHA, run id, or job id produces an unknown token and
# fails. Mutation-pinned by M05/M09/M10/M11.
# ======================================================================================


KNOWN_40_HEX = frozenset(
    {
        PR344_BASE_SHA,
        PR344_ACCEPTED_HEAD,
        PR344_MERGE_SHA,
        PR344_MERGE_TREE,
        AUTHORIZED_OLD_BLOB,
        AUTHORIZED_NEW_BLOB,
        REVIEWED_HEAD_SHA,
    }
)

KNOWN_LONG_DIGITS = frozenset(
    {
        FAILED_CI_RUN,
        FAILED_CI_JOB,
        FINAL_CLEAN_REVIEW,
        PRINCIPAL_ACCEPTANCE_COMMENT,
        POST_MERGE_VERIFICATION_COMMENT,
        AUDITABLE_STOP_COMMENT,
        REVIEW_THAT_REQUIRED_THE_CORRECTION,
        REVIEWED_HEAD_CI_RUN,
        REVIEWED_HEAD_CI_JOB,
    }
)


class TestEveryIdentityIsKnown:
    def test_no_unknown_40_hex_identity_appears(self, decision_text):
        found = set(re.findall(r"\b[0-9a-f]{40}\b", decision_text))
        assert found - KNOWN_40_HEX == set(), found - KNOWN_40_HEX

    def test_every_known_40_hex_identity_is_actually_used(self, decision_text):
        """The whitelist may not carry a value the decision never cites -- otherwise a
        deleted identity would pass unnoticed."""
        found = set(re.findall(r"\b[0-9a-f]{40}\b", decision_text))
        assert KNOWN_40_HEX - found == set(), KNOWN_40_HEX - found

    def test_no_unknown_long_digit_identity_appears(self, decision_text):
        found = set(re.findall(r"\b[0-9]{9,11}\b", decision_text))
        assert found - KNOWN_LONG_DIGITS == set(), found - KNOWN_LONG_DIGITS

    def test_every_known_long_digit_identity_is_actually_used(self, decision_text):
        found = set(re.findall(r"\b[0-9]{9,11}\b", decision_text))
        assert KNOWN_LONG_DIGITS - found == set(), KNOWN_LONG_DIGITS - found

    def test_the_only_64_hex_token_is_the_universe_hash(self, decision_text):
        found = set(re.findall(r"\b[0-9a-f]{64}\b", decision_text))
        assert found == {UNIVERSE_AGGREGATE_HASH}, found

    def test_the_closed_range_arrow_names_both_endpoints_together(self, decision_text):
        """§G.2's range must name BOTH endpoints in one transition, not two loose SHAs."""
        g2 = _section(decision_text, "G")
        assert f"{PR344_BASE_SHA} -> {PR344_ACCEPTED_HEAD}" in g2


# ======================================================================================
# 15 -- Each rule is pinned in the SECTION that carries it
#
# Mutation-pinned by M02/M03/M18/M19/M21/M25-M29/M32: every one of these survived an
# existence-only check because the same words appear in more than one place.
# ======================================================================================


class TestRulesArePinnedWhereTheyAreOperative:
    def test_l6s_exclusion_is_quoted_in_both_d_and_m(self, decision_text):
        phrase = "not a run against any other commit"
        assert phrase in _section(decision_text, "D")
        assert phrase in _section(decision_text, "M")

    def test_permanent_unsatisfiability_is_stated_in_d(self, decision_text):
        """Pinned to the BOLDED operative claim, not to the bare phrase. §D states the same
        idea twice, so a check on the phrase alone survives corruption of the operative
        sentence -- exactly the gap mutation M03 exploited."""
        d = _section(decision_text, "D")
        assert (
            "`MERGE_COMMIT_CI_SUCCESS` is **permanently unsatisfiable for PR #344**" in d
        )
        assert "cannot become effective through PR #344" in d

    def test_d_requires_a_successor_anchor_rather_than_repair_or_waiting(self, decision_text):
        """Pinned to §D's own operative sentence. The `§G.6` heading alone is not enough:
        §D is where the anchor is required INSTEAD of repairing or waiting out the failed
        run, and mutation M18 survived a heading-only check."""
        d = _section(decision_text, "D")
        assert (
            "The recovery unit must therefore establish a **lawful successor lifecycle "
            "anchor** (§G.6) rather than attempt to repair, re-run, reinterpret, or wait "
            "out the failed run." in d
        )

    def test_g6_requires_the_successor_anchor_by_name(self, decision_text):
        g = _section(decision_text, "G")
        assert "**G.6 — Establish a lawful successor lifecycle anchor.**" in g

    def test_g12_forbids_weakening_in_its_own_section(self, decision_text):
        """§G.12's operative sentence, pinned where it lives. Three passages in the decision
        use similar words, so a bare-phrase check survives corruption of this one."""
        g = _section(decision_text, "G")
        assert (
            "**G.12 — Weaken nothing.** No existing assertion may be deleted, skipped, "
            "`xfail`ed, weakened, or replaced with a less falsifiable one." in g
        )

    def test_k_states_the_scope_boundary_the_correction_did_not_cross(self, decision_text):
        """The sentence that keeps the enabling correction from becoming a scope grant."""
        k = _section(decision_text, "K")
        assert (
            "Beyond that one test-only correction, this filing still edits **no** load-bearing "
            "implementation, no runner, no result validator, no universe module, no canonical "
            "artifact, no operational-authorization mechanism, and no protected portfolio path"
            in k
        )

    def test_g2_requires_preservation_and_re_proof_not_a_repeat_correction(self, decision_text):
        """G.2 was rewritten by this correction. The future unit must PRESERVE and RE-PROVE
        the repaired guard; instructing it to perform a correction already completed here
        would make the filing untruthful in the opposite direction."""
        g = _section(decision_text, "G")
        assert (
            "**G.2 — Preserve and independently re-prove the corrected immutable-range guard.**"
            in g
        )
        assert "so the future unit does **not** perform that correction again" in g
        assert "may only be strengthened" in g

    def test_the_enabling_correction_grants_no_recovery_or_stage_1_authority(self, decision_text):
        """The correction must not be stretched into production authority. Its being
        principal-authorized says nothing about arming, recovery, or Stage 1."""
        flat = _flat(decision_text)
        flat_lower = flat.lower()
        for grant in (
            "may also perform production recovery",
            "and arm stage 1",
            "authorizes production recovery",
            "authorizes the recovery itself",
            "permits arming",
        ):
            assert grant not in flat_lower, grant
        k = _section(decision_text, "K")
        assert (
            "adds no production, canonical, lane, results, or Stage-1 authority of any kind" in k
        )

    def test_g7_binds_rebinding_to_strict_necessity_verbatim(self, decision_text):
        g = _section(decision_text, "G")
        assert (
            "The operational-authorization mechanism may be rebound **only** to the extent "
            "the successor lifecycle anchor requires." in g
        )
        assert "may not be made more permissive in any respect" in g

    def test_g5_forbids_relabelling_the_failed_run(self, decision_text):
        g = _section(decision_text, "G")
        assert "It **may never** be relabelled successful" in g

    def test_g10_forbids_a_moving_guard_verbatim(self, decision_text):
        g = _section(decision_text, "G")
        assert (
            "**No moving `HEAD`/`origin/main` guard may claim historical byte identity**" in g
        )

    def test_g8_forbids_re_pointing_predecessor_evidence(self, decision_text):
        g = _section(decision_text, "G")
        assert "never erased, overwritten, or silently re-pointed" in g

    def test_every_withheld_capability_is_its_own_h_bullet(self, decision_text):
        """Each prohibition must survive as a BULLET, not merely as a word somewhere in the
        section -- the exact gap M25-M29 exploited."""
        h = _section(decision_text, "H")
        for bullet in (
            "- perform renewed readiness verification;",
            "- perform renewed drift verification;",
            "- perform or authorize **Step 11**;",
            "- generate, pre-stage, or validate any **attestation**;",
            "- create lane state, write `AUTHORIZATION_ROOT`, or write the lane ledger;",
            "- **arm** Stage 1, or set `stage_1_executability.executable` to anything but `false`;",
            "- **claim** or consume `ATTEMPT_1`;",
            "- evaluate any gate for any registered construction;",
            "- execute Stage 1, perform recovery execution, or perform any results work;",
            "- access protected `RISK` evidence.",
        ):
            assert bullet in h, bullet

    def test_i_requires_a_stop_rather_than_proceeding(self, decision_text):
        i = _section(decision_text, "I")
        assert (
            "it must **stop and disclose** rather than proceed, assume, or downgrade the "
            "requirement." in i
        )
        assert "is a **stop**, not a judgement call" in i

    def test_f_grants_exactly_one_unit_in_its_own_section(self, decision_text):
        f = _section(decision_text, "F")
        assert "**exactly one** future, separate, bounded pull request" in f
        assert "It is one unit and one pull request." in f

    def test_g1_requires_a_separate_decision_under_an_unverified_identifier(self, decision_text):
        g = _section(decision_text, "G")
        assert "**G.1 — File its own decision.**" in g
        assert "never predicted, reserved, or assumed here" in g


# ======================================================================================
# 16 -- The decision cannot deadlock its own effectivity
#
# Review 4989608238's BLOCKING finding, pinned as a CONJUNCTION rather than as two
# separate facts. The reviewed head satisfied each half individually -- §M.6 required
# successful exact-merge CI, and §N declared that CI impossible -- and passed, because
# nothing tested them TOGETHER. This is that missing test.
# ======================================================================================


#: Any wording that asserts this filing's own CI cannot succeed. Each re-creates the
#: deadlock regardless of phrasing, so the check is over the concept, not one sentence.
SELF_DEFEATING_CI_CLAIMS = (
    "this filing's own ci will fail",
    "this pr's own ci will fail",
    "its own ci will fail",
    "necessarily fails",
    "necessarily fail",
    "must continue failing",
    "cannot pass ci",
    "can never pass ci",
    "fails on **every** branch taken from",
    "fails on every branch taken from",
    "explicitly barred from editing",
    "does not correct the failing guard",
)


class TestTheDecisionCannotDeadlockItsOwnEffectivity:
    def test_the_successful_ci_effectivity_requirement_is_present(self, decision_text):
        """Half one of the conjunction. Removing it would 'resolve' the deadlock by
        abandoning the requirement -- which is not a resolution."""
        m = _section(decision_text, "M")
        assert "**successful merge-commit CI whose `head_sha` is the exact merge SHA**" in m
        assert "not a run against any other commit" in m

    def test_no_self_defeating_ci_claim_survives_anywhere(self, decision_text):
        """Half two. Any surviving form makes half one unattainable."""
        flat_lower = _flat(decision_text).lower()
        for claim in SELF_DEFEATING_CI_CLAIMS:
            assert claim not in flat_lower, claim

    def test_the_conjunction_itself_is_refused(self, decision_text):
        """THE test the reviewed head lacked: requiring successful exact-merge CI while
        also declaring that CI impossible is refused as a combination, not merely as two
        independently-checked halves."""
        flat = _flat(decision_text)
        flat_lower = flat.lower()
        requires_successful_ci = (
            "**successful merge-commit CI whose `head_sha` is the exact merge SHA**" in flat
        )
        declares_ci_impossible = any(c in flat_lower for c in SELF_DEFEATING_CI_CLAIMS)
        assert not (requires_successful_ci and declares_ci_impossible), (
            "deadlock: the decision requires successful exact-merge CI and simultaneously "
            "declares its own CI impossible, so it could never become effective"
        )
        # And the half that must hold, holds -- so this is not satisfied vacuously by
        # dropping the requirement instead of the impossibility claim.
        assert requires_successful_ci

    def test_the_deadlock_is_recorded_as_the_reason_for_the_correction(self, decision_text):
        """The fix must be traceable to the finding, not silently applied."""
        k = _section(decision_text, "K")
        assert REVIEW_THAT_REQUIRED_THE_CORRECTION in k
        assert "unattainable" in k.lower()

    def test_the_correction_did_not_weaken_the_effectivity_chain(self, decision_text):
        """All seven §M conditions must still be present and conjunctive."""
        m = _section(decision_text, "M")
        for n in range(1, 8):
            assert f" {n}. " in f" {m}", n
        assert "**None is individually sufficient.**" in m

    def test_a_red_corrected_head_ci_is_a_stop_not_an_accepted_deviation(self, decision_text):
        n = _section(decision_text, "N")
        assert "a red corrected-head CI is a stop, not an accepted deviation" in n


# ======================================================================================
# 17 -- The defect class itself: a historical proof may never consult a moving reference
#
# Added by XASSET-0046. Sections 1-16 pin what the DECISION says. This section pins what
# THIS FILE does, because the failure that stopped the XASSET-0045 lifecycle was not in a
# decision's prose -- it was two assertions in this file measuring immutable history with a
# moving ruler. The same class had already been corrected once, one layer down, and was
# reintroduced here. A prose prohibition did not prevent that; a mechanical one is the point
# of this section.
# ======================================================================================


def historical_proof_moving_ref_offenders(
    source: str,
    proof_names: frozenset[str] = HISTORICAL_PROOF_FUNCTIONS,
    moving: frozenset[str] = MOVING_REFERENCE_LITERALS,
) -> list[str]:
    """Functions in ``source`` whose subject is immutable history yet which consult a
    moving reference.

    A shared, module-level detector -- not a private helper, and not re-implemented inside
    its own proof -- so disabling it makes its own falsifiability test fail rather than
    silently report "clean" while inspecting nothing. That is this repository's own
    established lesson, recorded on PR #345 after six probes disabled a guard and nothing
    noticed.

    The rule is deliberately blunt where bluntness is correct: inside a declared historical
    proof, a moving-reference name may not appear as a string literal AT ALL. Not in an
    assertion, and **not in a skip guard** -- a historical proof that can be silenced by
    where a live ref happens to point is not a proof of history. Both defects this section
    exists for were one literal each.

    Scoped to the declared proof functions rather than the whole module, because naming a
    moving reference is legitimate and necessary elsewhere: the live working-tree guards
    genuinely have a moving subject, and the AST checks must name these references in order
    to refuse them.
    """
    offenders: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.FunctionDef) or node.name not in proof_names:
            continue
        for const in ast.walk(node):
            if not (isinstance(const, ast.Constant) and isinstance(const.value, str)):
                continue
            if const.value in moving:
                offenders.append(f"{node.name}:{const.lineno} consults {const.value!r}")
    return offenders


def test_no_historical_proof_consults_a_moving_reference():
    """The mutation pin for the exact defect class that stopped the XASSET-0045 lifecycle.

    Restoring ``git diff --name-only origin/main`` into either corrected assertion -- or
    reintroducing a moving-ref skip guard into any declared historical proof -- fails here.
    """
    assert historical_proof_moving_ref_offenders(
        SUITE_PATH.read_text(encoding="utf-8")
    ) == []


def test_the_moving_reference_detector_actually_detects():
    """Falsifiability proof, run through the REAL detector against synthetic source.

    Known-bad and known-good are both exercised: a detector that flags everything is as
    useless as one that flags nothing, and only running the real function can show that
    emptying its literal set or making its loop unreachable breaks something.
    """
    names = frozenset({"test_historical"})
    bad_assertion = (
        "def test_historical():\n"
        "    changed = set(_git('diff', '--name-only', 'origin/main').splitlines())\n"
        "    assert 'x' in changed\n"
    )
    bad_skip_guard = (
        "def test_historical():\n"
        "    if not _git_ok('rev-parse', '--verify', 'origin/main'):\n"
        "        pytest.skip('nope')\n"
        "    assert _blob_at(PR345_BASE_SHA, 'x') == PR345_CORRECTION_OLD_BLOB\n"
    )
    bad_head = (
        "def test_historical():\n"
        "    assert _git('rev-parse', 'HEAD') == PR345_MERGE_SHA\n"
    )
    good_pinned = (
        "def test_historical():\n"
        "    changed = _assert_pr345_closed_range_facts()\n"
        "    assert 'x' in changed\n"
    )
    good_pinned_merge_base = (
        "def test_historical():\n"
        "    base = _git('merge-base', PR344_MERGE_SHA, PR344_MERGE_SHA)\n"
        "    assert base == PR344_MERGE_SHA\n"
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
    # Out of scope by NAME, not by shape: the same offending shape in a function whose
    # subject genuinely is live state must not be flagged.
    assert historical_proof_moving_ref_offenders(good_out_of_scope, names) == []
    # And it genuinely parsed this suite's own real source, rather than something empty.
    real = SUITE_PATH.read_text(encoding="utf-8")
    parsed = {
        n.name for n in ast.walk(ast.parse(real)) if isinstance(n, ast.FunctionDef)
    }
    assert HISTORICAL_PROOF_FUNCTIONS <= parsed, HISTORICAL_PROOF_FUNCTIONS - parsed


def test_the_declared_proof_set_covers_both_corrected_assertions():
    """Coverage pin. Emptying or narrowing ``HISTORICAL_PROOF_FUNCTIONS`` would leave the
    detector reporting clean while inspecting nothing -- the same silent-disable shape the
    detector's own falsifiability test exists to refuse."""
    for required in (
        "test_the_enabling_correction_was_actually_performed",
        "test_no_protected_path_was_touched_by_this_filing",
        "_assert_pr345_closed_range_facts",
    ):
        assert required in HISTORICAL_PROOF_FUNCTIONS, required
    assert len(HISTORICAL_PROOF_FUNCTIONS) >= 8
    # ADVANCED BY XASSET-0047, and the direction matters. The superseded pin refused the function
    # because XASSET-0046 lacked authority to correct its skip guard, so declaring it would have
    # reimposed by test what that filing could not do. XASSET-0047 corrected the guard under
    # XASSET-0046 §G.11's own operative duty, so the declaration is now REQUIRED rather than
    # forbidden -- and it is required EXACTLY, so silently dropping it again would fail here.
    assert (
        "test_on_merged_main_the_moving_base_collapses_to_head_itself"
        in HISTORICAL_PROOF_FUNCTIONS
    )
    assert "origin/main" in MOVING_REFERENCE_LITERALS
    assert "HEAD" in MOVING_REFERENCE_LITERALS
    # merge-base is a subcommand, not a reference: flagging it would refuse a sound proof.
    assert "merge-base" not in MOVING_REFERENCE_LITERALS


# ======================================================================================
# 18 -- Invariance, proved by RUNNING, in every ref state this branch will pass through
#
# The structural detector above proves the corrected proofs do not NAME a moving reference.
# That is necessary and not sufficient: it is a claim about source text. This section moves
# HEAD and origin/main for real and requires the corrected proofs to pass at each position,
# which is the property that actually failed at PR #345's merge.
#
# Every simulation runs inside an ISOLATED CLONE. `git worktree` is never used: it shares the
# ref namespace, so an `update-ref` inside one really does move the REAL origin/main. That
# happened once during PR #345's own work and had to be repaired. The shape is refused
# statically below, before any damage.
# ======================================================================================


#: Git subcommands that write refs. A simulation must never run one against the real
#: repository.
REF_MUTATING_GIT_SUBCOMMANDS = frozenset(
    {"update-ref", "branch", "reset", "checkout", "worktree", "switch"}
)


def real_repo_ref_mutation_offenders(source: str) -> list[str]:
    """Calls in ``source`` that would write a ref in the REAL repository.

    Shared and module-level for the same reason as the detector above: a guard that is
    re-implemented inside its own proof can be disabled without anything noticing.
    """
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
    """Falsifiability proof, run through the REAL detector. Without this, emptying the
    subcommand set or making the loop unreachable leaves a guard reporting "clean" because
    it inspects nothing."""
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
    """Resolve a ref in the REAL repository, read-only. Used ONLY to build simulated states
    and to prove the simulations leave the real refs undisturbed. Never asserted to equal a
    historical constant -- that inverse defect is what DELTA review 4993351528 found."""
    result = subprocess.run(
        ["git", "rev-parse", name], cwd=ROOT, capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


#: This branch's own current commit, resolved live. Used ONLY to build simulated ref states.
_LOCAL_HEAD_FOR_SIMULATION = _live_ref("HEAD") or PR345_MERGE_SHA

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
    "TestFilingIsGovernancePlusOneEnablingCorrection::"
    "test_the_enabling_correction_was_actually_performed",
    "TestFilingIsGovernancePlusOneEnablingCorrection::"
    "test_no_protected_path_was_touched_by_this_filing",
    "TestDefectIsAMovingAnchor::test_on_merged_main_the_moving_base_collapses_to_head_itself",
    "TestDefectIsAMovingAnchor::test_the_closed_range_does_exercise_the_authorized_transition",
    "TestDefectIsAMovingAnchor::test_the_accepted_head_is_the_second_parent_of_the_merge",
    "test_no_historical_proof_consults_a_moving_reference",
)

#: Every ref position this branch will actually pass through, named for what it isolates.
#: ``merged_main`` is the state that broke both corrected assertions; the two "later" states
#: are what ``main`` becomes once THIS pull request, and then anything after it, merges.
REF_STATES = (
    "branch",
    "merged_main",
    "later_main",
    "head_equals_origin_main_later",
    "unrelated_later_commits",
)


@pytest.mark.parametrize("ref_state", REF_STATES)
def test_corrected_proofs_pass_under_every_real_repository_ref_state(tmp_path, ref_state):
    """Run the corrected proofs for real, under each ref state, and require them to pass.

    The WORKING TREE is always this branch's content -- the file under examination is this
    correction's own, copied in from the working tree so the regression tests the code being
    reviewed rather than the previous commit. Only ``HEAD`` and ``origin/main`` move, which
    isolates ref position as the single variable.

    Under the SUPERSEDED assertions, ``merged_main`` failed: that is the state merged ``main``
    is in, and the state run 32490789238 ran in.
    """
    if not _pr345_range_is_present():
        pytest.skip("PR #345's closed range is not present in this checkout")
    clone = _working_clone(tmp_path)
    _git_in(clone, "checkout", "--quiet", "--detach", _LOCAL_HEAD_FOR_SIMULATION)
    shutil.copy2(SUITE_PATH, clone / SUITE_PATH.name)

    # A genuine feature-branch head: this session's own commit when it has one, and a
    # synthesized commit on top of the merge when it does not. Taking the live HEAD on faith
    # would silently degrade the `branch` state into `merged_main` before this branch's first
    # commit -- which is exactly the "the scenario is still parametrised but no longer tests
    # anything" shape the coverage pins exist to refuse. The structural pins below then hold
    # unconditionally rather than only after the first commit.
    branch_head = (
        _LOCAL_HEAD_FOR_SIMULATION
        if _LOCAL_HEAD_FOR_SIMULATION != PR345_MERGE_SHA
        else _commit_on_top(clone, PR345_MERGE_SHA, "feature branch commit")
    )

    if ref_state == "branch":
        head, main = branch_head, PR345_MERGE_SHA
    elif ref_state == "merged_main":
        head = main = PR345_MERGE_SHA
    elif ref_state == "later_main":
        head = branch_head
        main = _commit_on_top(clone, PR345_MERGE_SHA, "later main")
    elif ref_state == "head_equals_origin_main_later":
        head = main = _commit_on_top(clone, PR345_MERGE_SHA, "later main, checked out")
    else:
        main = PR345_MERGE_SHA
        for n in range(3):
            main = _commit_on_top(clone, main, f"unrelated later commit {n}")
        head = branch_head

    # Move the refs WITHOUT touching the working tree, so the files under test stay this
    # branch's own while `git rev-parse` reports the simulated state.
    _git_in(clone, "update-ref", "HEAD", head)
    _git_in(clone, "update-ref", "refs/remotes/origin/main", main)
    assert _git_in(clone, "rev-parse", "HEAD") == head
    assert _git_in(clone, "rev-parse", "origin/main") == main

    # Structural pins: each state must genuinely be the state it claims to be.
    if ref_state in ("later_main", "head_equals_origin_main_later", "unrelated_later_commits"):
        assert main != PR345_MERGE_SHA, f"{ref_state} must advance past PR #345's merge"
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
        f"ref state {ref_state!r} (HEAD={head}, origin/main={main}) broke the corrected "
        f"proofs:\n{result.stdout[-4000:]}\n{result.stderr[-2000:]}"
    )
    # The nested run must have actually executed the selected tests, not collected zero.
    assert " passed" in result.stdout, result.stdout[-2000:]


def test_the_ref_state_regression_covers_every_state_this_branch_will_pass_through():
    """Coverage pin. Dropping a state -- especially ``merged_main``, the one that actually
    failed -- would leave the regression green while the defect returned."""
    assert set(REF_STATES) == {
        "branch",
        "merged_main",
        "later_main",
        "head_equals_origin_main_later",
        "unrelated_later_commits",
    }
    assert len(REF_STATES) == 5


def test_the_ref_state_regression_selects_both_corrected_proofs_and_is_not_recursive():
    """The nested selection must exercise the corrected assertions, and must not select the
    outer parametrized regression itself."""
    joined = " ".join(REF_STATE_SENSITIVE_TESTS)
    assert "test_the_enabling_correction_was_actually_performed" in joined
    assert "test_no_protected_path_was_touched_by_this_filing" in joined
    assert "test_corrected_proofs_pass_under_every_real_repository_ref_state" not in joined


def test_the_isolated_simulation_does_not_mutate_the_real_repository_refs(tmp_path):
    """Capture the real repository's live refs immediately before an isolated simulation and
    require the SAME values immediately after.

    It asserts nothing about WHAT those refs contain -- requiring a live ref to equal a
    historical commit is the inverse defect DELTA review 4993351528 found on PR #345, and it
    deadlocks in exactly the same way one merge later.
    """
    before = {name: _live_ref(name) for name in ("HEAD", "origin/main")}
    clone = _working_clone(tmp_path)
    _git_in(clone, "checkout", "--quiet", "--detach", _LOCAL_HEAD_FOR_SIMULATION)
    simulated = _commit_on_top(clone, _LOCAL_HEAD_FOR_SIMULATION, "isolation probe")
    _git_in(clone, "update-ref", "HEAD", simulated)
    _git_in(clone, "update-ref", "refs/remotes/origin/main", simulated)
    assert _git_in(clone, "rev-parse", "HEAD") == simulated
    after = {name: _live_ref(name) for name in ("HEAD", "origin/main")}
    assert after == before, f"the simulation moved a real ref: {before} -> {after}"


# ======================================================================================
# 19 -- Every corrected conjunct is independently required
#
# Each pin below drives the REAL helper with one deliberately wrong anchor and requires it
# to REFUSE. Asserting "the correct values pass" proves only that the happy path runs; it
# cannot show that any individual conjunct is load-bearing. These show that each one is.
# ======================================================================================


def _expect_refusal(fn, *, what: str):
    """Require ``fn()`` to raise ``AssertionError``.

    Explicitly NOT ``pytest.raises(AssertionError)``: ``pytest.skip`` raises ``Skipped``,
    which derives from ``BaseException``, so a guard silently downgraded from a refusal to a
    skip would satisfy a naive ``raises`` and pass. PR #345's own round-1 correction found
    exactly that hole. A skip here is a failure, not a pass.
    """
    try:
        fn()
    except AssertionError:
        return
    except BaseException as exc:  # noqa: BLE001 -- a skip must NOT be accepted as a refusal
        pytest.fail(f"{what}: expected AssertionError, got {type(exc).__name__}: {exc}")
    pytest.fail(f"{what}: expected AssertionError, but the call succeeded")


def _requires_range():
    if not _pr345_range_is_present():
        pytest.skip("PR #345's closed range is not present in this checkout")


#: A real, resolvable commit that is NOT any PR #345 anchor -- so a "wrong anchor" probe
#: fails on identity rather than on nonexistence, which a nonsense SHA could not distinguish.
WRONG_BUT_REAL_COMMIT = PR344_BASE_SHA


class TestEveryClosedRangeConjunctIsIndependentlyRequired:
    def test_the_correct_anchors_pass(self):
        """The control. Without it, every refusal below could be caused by a helper that
        refuses unconditionally."""
        _requires_range()
        changed = _assert_pr345_closed_range_facts()
        assert ENABLING_CORRECTION_RELPATH in changed

    def test_a_wrong_base_is_refused(self):
        _requires_range()
        _expect_refusal(
            lambda: _assert_pr345_closed_range_facts(base_sha=WRONG_BUT_REAL_COMMIT),
            what="wrong base",
        )

    def test_a_wrong_accepted_head_is_refused(self):
        _requires_range()
        _expect_refusal(
            lambda: _assert_pr345_closed_range_facts(accepted_head=WRONG_BUT_REAL_COMMIT),
            what="wrong accepted head",
        )

    def test_a_wrong_merge_is_refused(self):
        _requires_range()
        _expect_refusal(
            lambda: _assert_pr345_closed_range_facts(merge_sha=PR344_MERGE_SHA),
            what="wrong merge",
        )

    def test_reversed_parent_order_is_refused(self):
        """Parent ORDER is the property, not parent membership: a merge whose accepted head
        is the first parent is a different merge."""
        _requires_range()
        _expect_refusal(
            lambda: _assert_pr345_closed_range_facts(
                base_sha=PR345_ACCEPTED_HEAD, accepted_head=PR345_BASE_SHA,
            ),
            what="reversed parent order",
        )

    def test_merge_tree_drift_is_refused(self):
        """A merge that introduced content of its own would not carry the accepted head's
        tree. Probed with a real tree that is genuinely a different one."""
        _requires_range()
        _expect_refusal(
            lambda: _assert_pr345_closed_range_facts(merge_tree=PR344_MERGE_TREE),
            what="merge tree drift",
        )

    def test_an_unresolvable_anchor_is_a_refusal_not_a_skip(self):
        """Fail-closed: an anchor that cannot be read is an error, never silent agreement."""
        _requires_range()
        _expect_refusal(
            lambda: _assert_pr345_closed_range_facts(base_sha="0" * 40),
            what="unresolvable base",
        )


class TestEveryCorrectionConjunctIsIndependentlyRequired:
    def test_the_target_is_actually_in_the_change_set(self):
        """The allowance may not linger as dead permission: the correction must have been
        exercised, not merely permitted."""
        _requires_range()
        changed = _assert_pr345_closed_range_facts()
        assert ENABLING_CORRECTION_RELPATH in changed

    def test_a_wrong_target_status_would_be_detected(self):
        """Status is a conjunct in its own right: an addition, deletion, rename or copy is
        not the authorized modification."""
        _requires_range()
        changed = _assert_pr345_closed_range_facts()
        actual = changed[ENABLING_CORRECTION_RELPATH]
        assert actual == PR345_CORRECTION_STATUS
        for wrong in ("A", "D", "R", "C", "T"):
            assert actual != wrong, wrong

    def test_a_wrong_old_blob_would_be_detected(self):
        _requires_range()
        old = _blob_at(PR345_BASE_SHA, ENABLING_CORRECTION_RELPATH)
        assert old == PR345_CORRECTION_OLD_BLOB
        assert old != PR345_CORRECTION_NEW_BLOB
        assert old != AUTHORIZED_OLD_BLOB

    def test_a_wrong_new_blob_would_be_detected(self):
        _requires_range()
        new = _blob_at(PR345_ACCEPTED_HEAD, ENABLING_CORRECTION_RELPATH)
        assert new == PR345_CORRECTION_NEW_BLOB
        assert new != PR345_CORRECTION_OLD_BLOB
        assert new != AUTHORIZED_NEW_BLOB

    def test_both_blob_ends_are_independently_derived_from_git_objects(self):
        """Neither end may be taken from the other, or from the declared constant: both are
        read from the object store at their own commit."""
        _requires_range()
        assert _blob_at(PR345_BASE_SHA, ENABLING_CORRECTION_RELPATH) != (
            _blob_at(PR345_ACCEPTED_HEAD, ENABLING_CORRECTION_RELPATH)
        )

    def test_the_protected_intersection_is_empty_over_a_NON_EMPTY_input(self):
        """The exact anti-vacuity pin for the second defect.

        An empty change set makes ``changed & PROTECTED == set()`` true for free. The
        superseded assertion passed that way on merged ``main`` while measuring nothing.
        """
        _requires_range()
        changed = _assert_pr345_closed_range_facts()
        assert len(changed) == PR345_CHANGED_FILE_COUNT, (
            "the input must be a real change set, not an empty one"
        )
        assert set(changed) & set(PROTECTED_RELPATHS) == set()

    def test_a_protected_path_in_the_change_set_would_be_detected(self):
        """Falsifiability of the protected-path claim, exercised through the real change set
        rather than asserted: injecting a protected path makes the intersection non-empty."""
        _requires_range()
        changed = dict(_assert_pr345_closed_range_facts())
        changed[PROTECTED_RELPATHS[0]] = "M"
        assert set(changed) & set(PROTECTED_RELPATHS) != set()

    def test_the_change_set_is_exactly_pr345s_own_scope(self):
        """The closed range must measure PR #345 and nothing else: its accepted metadata
        recorded 12 changed files."""
        _requires_range()
        changed = _assert_pr345_closed_range_facts()
        assert len(changed) == PR345_CHANGED_FILE_COUNT, sorted(changed)
        assert PR345_CHANGED_FILE_COUNT == 12


class TestTheDetectorCannotBeSilentlyDisabled:
    def test_the_detector_is_defined_at_module_level_and_is_reachable(self):
        """"Made unreachable" is a real mutation shape: a detector defined inside its own
        test, or shadowed by a private copy, can be removed without any self-test noticing."""
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        top_level = {
            n.name for n in tree.body if isinstance(n, ast.FunctionDef)
        }
        for required in (
            "historical_proof_moving_ref_offenders",
            "real_repo_ref_mutation_offenders",
            "_assert_pr345_closed_range_facts",
        ):
            assert required in top_level, required

    def test_each_detector_is_called_by_a_test_that_would_fail_if_it_were_neutered(self):
        """The detectors must be invoked with THIS FILE's real source somewhere, not only
        with synthetic strings -- otherwise the real file is never actually inspected."""
        source = SUITE_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for detector in (
            "historical_proof_moving_ref_offenders",
            "real_repo_ref_mutation_offenders",
        ):
            callers = [
                n.name for n in ast.walk(tree)
                if isinstance(n, ast.FunctionDef)
                and any(
                    isinstance(c.func, ast.Name) and c.func.id == detector
                    and any(
                        isinstance(a, ast.Call)
                        and isinstance(a.func, ast.Attribute)
                        and a.func.attr == "read_text"
                        for a in ast.walk(c)
                    )
                    for c in ast.walk(n) if isinstance(c, ast.Call)
                )
            ]
            assert callers, f"{detector} is never run against this file's real source"


# ======================================================================================
# 20 -- The corrected proofs cannot be hollowed out in place
#
# Sections 17-19 caught every anchor mutation, but a first mutation pass found three that
# survived: rewriting a corrected assertion into a shape that still RUNS while proving less
# -- a defaulted lookup that treats "absent" as "expected", a hard-coded empty input, and a
# `>= 0` bound. Each survived because a sibling test in section 19 independently re-derived
# the same property, so the SUITE stayed honest while the NAMED test went hollow. That is
# exactly the "a guard which inspects nothing reports clean" shape this repository has
# already had to close twice, and redundancy is not a substitute for pinning the guard.
#
# Disclosed rather than dropped: the three probes are now closed structurally, at the shape
# level, instead of by adding a fourth redundant re-derivation.
# ======================================================================================


def corrected_proof_structure_offenders(source: str) -> list[str]:
    """Ways the two corrected proofs could still run while proving less.

    Shared and module-level, exercised against synthetic known-bad and known-good source
    below, for the same reason as every other detector in this file.

    Three shapes are refused inside either corrected proof:

    1. ``changed`` bound from anything other than ``_assert_pr345_closed_range_facts`` --
       a literal ``{}``, a working-tree diff, or any other substitute input;
    2. a defaulted lookup (``.get(...)``) -- it turns "the path is absent" into "the path
       holds the expected value", which is precisely the claim under test;
    3. a non-strict lower bound on the change set (``>= 0``, ``> -1``) -- a bound that every
       possible input satisfies is not a bound.
    """
    required_binder = "_assert_pr345_closed_range_facts"
    #: Proofs whose INPUT must come from the closed-range helper and from nothing else.
    binding_scoped = {
        "test_the_enabling_correction_was_actually_performed",
        "test_no_protected_path_was_touched_by_this_filing",
    }
    #: Proofs whose SHAPE must stay falsifiable. A superset: the section-19 claim tests
    #: re-derive the same facts and can be hollowed out the same way, but one of them
    #: legitimately wraps the helper's result (``dict(...)``) to build a negative case, so
    #: the stricter binding rule above must not reach them.
    shape_scoped = binding_scoped | {
        "test_the_protected_intersection_is_empty_over_a_NON_EMPTY_input",
        "test_the_change_set_is_exactly_pr345s_own_scope",
    }
    offenders: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.FunctionDef) or node.name not in shape_scoped:
            continue
        if node.name in binding_scoped:
            bound_correctly = False
            for assign in (a for a in ast.walk(node) if isinstance(a, ast.Assign)):
                if not any(
                    isinstance(t, ast.Name) and t.id == "changed" for t in assign.targets
                ):
                    continue
                value = assign.value
                if (
                    isinstance(value, ast.Call)
                    and isinstance(value.func, ast.Name)
                    and value.func.id == required_binder
                ):
                    bound_correctly = True
                else:
                    offenders.append(
                        f"{node.name}:{assign.lineno} binds 'changed' from something other "
                        f"than {required_binder}"
                    )
            if not bound_correctly:
                offenders.append(
                    f"{node.name} never binds 'changed' from {required_binder}"
                )
        for call in (c for c in ast.walk(node) if isinstance(c, ast.Call)):
            if isinstance(call.func, ast.Attribute) and call.func.attr == "get":
                offenders.append(
                    f"{node.name}:{call.lineno} uses a defaulted lookup, which cannot "
                    f"distinguish absent from expected"
                )
        for compare in (c for c in ast.walk(node) if isinstance(c, ast.Compare)):
            for op, right in zip(compare.ops, compare.comparators):
                if not isinstance(right, ast.Constant) or not isinstance(right.value, int):
                    continue
                if isinstance(op, ast.GtE) and right.value <= 0:
                    offenders.append(f"{node.name}:{compare.lineno} bounds with '>= 0'")
                if isinstance(op, ast.Gt) and right.value < 0:
                    offenders.append(f"{node.name}:{compare.lineno} bounds with '> -n'")
    return offenders


def test_the_corrected_proofs_are_not_hollowed_out():
    """Mutation pin for M13, M14 and M23 -- the three shapes that survived the first pass."""
    assert corrected_proof_structure_offenders(
        SUITE_PATH.read_text(encoding="utf-8")
    ) == []


def test_the_structure_detector_actually_detects():
    """Falsifiability proof, run through the REAL detector, for each refused shape and for
    the legitimate shape that must NOT be flagged."""
    hollow_empty = (
        "def test_no_protected_path_was_touched_by_this_filing():\n"
        "    changed = {}\n"
        "    assert set(changed) & set(PROTECTED_RELPATHS) == set()\n"
    )
    hollow_moving = (
        "def test_no_protected_path_was_touched_by_this_filing():\n"
        "    changed = set(_git('diff', '--name-only', 'origin/main').splitlines())\n"
        "    assert set(changed) & set(PROTECTED_RELPATHS) == set()\n"
    )
    hollow_default = (
        "def test_the_enabling_correction_was_actually_performed():\n"
        "    changed = _assert_pr345_closed_range_facts()\n"
        "    assert changed.get(ENABLING_CORRECTION_RELPATH, 'M') == 'M'\n"
    )
    hollow_bound = (
        "def test_no_protected_path_was_touched_by_this_filing():\n"
        "    changed = _assert_pr345_closed_range_facts()\n"
        "    assert len(changed) >= 0\n"
    )
    legitimate = (
        "def test_the_enabling_correction_was_actually_performed():\n"
        "    changed = _assert_pr345_closed_range_facts()\n"
        "    assert ENABLING_CORRECTION_RELPATH in changed\n"
        "    assert len(changed) == PR345_CHANGED_FILE_COUNT\n"
    )
    hollow_scope_claim = (
        "def test_the_change_set_is_exactly_pr345s_own_scope():\n"
        "    changed = _assert_pr345_closed_range_facts()\n"
        "    assert len(changed) >= 0\n"
    )
    # The shape rule reaches the section-19 claim tests; the stricter BINDING rule must not,
    # because one of them legitimately wraps the helper's result to build a negative case.
    wrapping_is_permitted = (
        "def test_the_change_set_is_exactly_pr345s_own_scope():\n"
        "    changed = dict(_assert_pr345_closed_range_facts())\n"
        "    assert len(changed) == PR345_CHANGED_FILE_COUNT\n"
    )
    out_of_scope = (
        "def test_something_else():\n"
        "    changed = {}\n"
        "    assert changed.get('x', 1) >= 0\n"
    )
    assert corrected_proof_structure_offenders(hollow_empty) != []
    assert corrected_proof_structure_offenders(hollow_moving) != []
    assert corrected_proof_structure_offenders(hollow_default) != []
    assert corrected_proof_structure_offenders(hollow_bound) != []
    assert corrected_proof_structure_offenders(hollow_scope_claim) != []
    assert corrected_proof_structure_offenders(legitimate) == []
    assert corrected_proof_structure_offenders(wrapping_is_permitted) == []
    assert corrected_proof_structure_offenders(out_of_scope) == []


def test_the_membership_and_scope_claims_are_made_by_the_named_proofs_themselves():
    """Redundancy elsewhere is not a substitute: each corrected proof must itself carry the
    claim its name makes, so hollowing it out fails at that test rather than only at a
    sibling that happens to re-derive the same fact."""
    tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
    by_name = {
        n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
    }

    correction = by_name["test_the_enabling_correction_was_actually_performed"]
    memberships = [
        c for c in ast.walk(correction)
        if isinstance(c, ast.Compare)
        and any(isinstance(o, ast.In) for o in c.ops)
        and isinstance(c.left, ast.Name)
        and c.left.id == "ENABLING_CORRECTION_RELPATH"
    ]
    assert memberships, "the correction proof must itself assert the target is present"

    protection = by_name["test_no_protected_path_was_touched_by_this_filing"]
    scope_pins = [
        c for c in ast.walk(protection)
        if isinstance(c, ast.Compare)
        and any(isinstance(o, ast.Eq) for o in c.ops)
        and any(
            isinstance(o, ast.Name) and o.id == "PR345_CHANGED_FILE_COUNT"
            for o in c.comparators
        )
    ]
    assert scope_pins, "the protection proof must itself pin a non-vacuous input size"
