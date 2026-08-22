"""Adversarial tests pinning the ``XASSET-0048`` step-8-equivalent rebinding AUTHORIZATION.

``XASSET-0047`` closed all seven of its own conditions and is **effective**: the
operational-authorization mechanism can authenticate its authorizing pull request's lifecycle from
durable truth again. What it did **not** do is bind a single byte of the corrected executable
package. Its §A says so -- "Nothing else moves" -- and its own closure comment names the successor
operational rebinding as still outstanding.

That rebinding is ``XASSET-0041`` §I **link 2**: the ``XASSET-0030`` §G.B step-8 **equivalent**
lifecycle. Step 8's *own* single budget was spent by ``XASSET-0037``; link 2's own grant
(``XASSET-0043`` §F) was spent by use on PR #344; ``XASSET-0045``'s grant never vested; and
``XASSET-0046``'s single recovery grant was spent by ``XASSET-0047``. So the step is mandatory,
unperformed, and -- until this filing -- unauthorized.

``XASSET-0048`` closes that gap and **nothing else**. It is design-only: it grants authority and
performs no production mutation.

The danger this suite exists to prevent is not the authorization. It is the set of shortcuts a
later session could read into a filing that sits one merge away from a rebinding:

1. **The grant read as permission to rebind now, here.**
   ``TestThisFilingPerformsNoRebinding`` -- proved against the production module's own bytes and
   symbols, not against prose.
2. **"Step 8" cited as unspent, re-consuming a budget three decisions record as spent.**
   ``TestTheAuthorityGapIsReproducedPrecisely``.
3. **A spent, never-vested, or withheld grant reached for as though it were live.**
   ``TestEverySupersededGrantIsRecordedAsUnavailable``.
4. **The granted boundary quietly widened, or a required property softened.**
   ``TestTheGrantIsBounded`` and ``TestTheRequiredPropertiesAreConditions``.
5. **A withheld action acquired by implication.** ``TestEveryWithheldActionIsWithheld`` and
   ``TestZeroActivationAuthority``.
6. **The outcome surface's semantics moved under cover of a byte-binding.**
   ``TestTheOutcomeSurfaceSemanticsArePreserved``.
7. **Adverse history relabelled, or a predecessor identity retired.**
   ``TestAdverseHistoryIsPreserved``.
8. **A filing whose own effectivity its own contents make unreachable.**
   ``TestNonDeadlock`` -- the defect that stopped ``XASSET-0045`` at its first reviewed head.
9. **A historical proof anchored to a reference that moves.** ``TestNoHistoricalProofMoves`` and
   ``test_declared_proofs_pass_under_every_real_repository_ref_state`` -- the defect that stopped
   PRs #344 and #345.
10. **The register or catalog desynchronised, or the pull-request number guessed.**
    ``TestCatalogAndRegisterSynchronisation`` and ``TestTheBoundPullRequestNumber``.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No attestation, claim, completion, lane directory, or ledger entry is created or
read for authorization purposes. No ``risk_lane_boundary`` protected result path is read, listed,
opened, or referenced. No module capable of producing a Stage-1 outcome is imported.
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

DECISION_ID = "XASSET-0048"
DECISION_RELPATH = (
    "governance/decisions/"
    "XASSET-0048-endpoint-0001-stage-1-step-8-equivalent-rebinding-authorization.md"
)
DECISION_PATH = ROOT / DECISION_RELPATH
CATALOG_RELPATH = "governance/decisions.yaml"
REGISTER_RELPATH = "operations/WORKSTREAMS.yaml"
AUTH_MODULE_RELPATH = "level1_stage1_execution_authorization.py"
REGISTER_GATE = "xasset0048-step8-equivalent-rebinding-authorization"
PRIOR_UNIT_GATE = "xasset0047-post-merge-verification"

# ── The impossible sentinel, and the number GitHub actually issued ──────────────────────────
#
# A pull-request number cannot be negative, so the sentinel can never be mistaken for a real one
# and can never accidentally validate. The branch's first commit carries it; the draft is then
# opened; GitHub issues the number; it is read back from live GitHub and only then bound here.
# Guessing "the next one" is exactly how a filing ends up authenticating against a pull request
# that belongs to someone else.
PULL_REQUEST_SENTINEL = -1
THIS_PULL_REQUEST = 348

# ── PR #347's own closed range -- every anchor an immutable git object ───────────────────────
#
# Independently re-derived from live git and live GitHub during the filing session and asserted
# here against the real object store, never taken on trust. This is also THIS unit's own base.

#: PR #347's base -- PR #346's merge commit.
PR347_BASE_SHA = "0b76c09f8d1aba01780b4f06fdd692f7393fbfd3"
#: The head the first independent FULL review examined, before the bounded correction.
PR347_FIRST_REVIEWED_HEAD = "1fb5941ce1f40ca24fa187289b318e4e266730cc"
#: PR #347's accepted head -- the exact commit the clean DELTA review examined.
PR347_ACCEPTED_HEAD = "8ae0988d4c1ffc551e7fa0a1d1ee1edfa7a49a9e"
#: PR #347's merge commit. Also THIS unit's own base, and the successful merge-commit CI head_sha.
PR347_MERGE_SHA = "bb95ed26964b1bc7a2e230c76060fec82752efa1"
#: The tree carried by BOTH the accepted head and the merge -- zero merge drift.
PR347_MERGE_TREE = "c8b677f8697660bef1122a83615845961457be89"

#: THIS unit's own base. Bound separately from PR347_MERGE_SHA by NAME so that a later unit
#: advancing one without the other is visible rather than silently absorbed.
THIS_UNIT_BASE_SHA = "bb95ed26964b1bc7a2e230c76060fec82752efa1"

#: PR #347's lifecycle evidence, all seven conditions.
PR347_FULL_REVIEW = "4997532748"
PR347_CLEAN_DELTA_REVIEW = "4997822429"
PR347_PRINCIPAL_ACCEPTANCE = "5375989065"
PR347_POST_MERGE_VERIFICATION = "5376014867"
PR347_FINAL_CLOSURE = "5376069596"
PR347_MERGE_CI_RUN = "32532487548"
PR347_MERGE_CI_JOB = "96927108608"

#: The two permanently failed merge-commit CI runs. Immutable adverse history: never re-run in
#: place, relabelled, waived, deleted, or represented as successful.
XASSET0044_FAILED_CI_RUN = "32439614683"
XASSET0044_FAILED_CI_JOB = "96647501864"
XASSET0045_FAILED_CI_RUN = "32490789238"
XASSET0045_FAILED_CI_JOB = "96797667282"

#: The frozen universe. Unchanged by this unit, and asserted so rather than assumed.
UNIVERSE_SHA256 = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
UNIVERSE_COUNT = 680
UNIVERSE_CELL_COUNT = 48

#: The lifecycle anchor as it stands at this unit's base. This filing is DESIGN-ONLY, so every
#: one of these must still hold at its own head -- that is the whole no-rebinding proof.
ANCHOR_DECISION_AT_BASE = "XASSET-0047"
ANCHOR_PULL_REQUEST_AT_BASE = 347
ANCHOR_REVIEWED_BASE_AT_BASE = "0b76c09f8d1aba01780b4f06fdd692f7393fbfd3"
LOAD_BEARING_COUNT_AT_BASE = 16

#: The production surface this design-only filing may not touch, compared byte-for-byte against
#: THIS unit's own base -- an immutable commit, so the comparison neither moves nor collapses to
#: empty once this branch merges.
FROZEN_AGAINST_BASE_RELPATHS = (
    AUTH_MODULE_RELPATH,
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    "level1_construction_universe_closure_validator.py",
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
    "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
    "governance/decisions/XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md",
    "governance/decisions/XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
    "governance/decisions/XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md",
    "governance/decisions/XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md",
    "governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md",
    "governance/decisions/XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md",
    "governance/decisions/XASSET-0044-endpoint-0001-stage-1-post-correction-operational-rebinding.md",
    "governance/decisions/XASSET-0045-endpoint-0001-stage-1-post-merge-ci-recovery-authorization.md",
    "governance/decisions/XASSET-0046-endpoint-0001-stage-1-post-merge-ci-recovery-reauthorization.md",
    "governance/decisions/XASSET-0047-endpoint-0001-stage-1-post-merge-ci-recovery-reconciliation.md",
)

#: The functions in THIS suite whose SUBJECT is immutable history. None may consult a moving
#: reference -- not in an assertion, and not in a skip guard, because a historical proof that a
#: live reference can silence is not a proof of history. This is the defect that stopped PRs
#: #344 and #345, encoded as a check rather than left as a promise.
HISTORICAL_PROOF_FUNCTIONS = frozenset({
    "_assert_pr347_closed_range_facts",
    "test_the_accepted_head_is_the_second_parent_of_this_units_base",
    "test_the_authority_merged_with_zero_drift",
    "test_the_first_reviewed_head_is_an_ancestor_of_the_accepted_head",
    "test_every_frozen_path_is_byte_identical_to_this_units_base",
    "test_the_decision_and_this_suite_did_not_exist_at_the_base",
})

#: String literals that name a MOVING reference. A small, explicit, closed set of REFERENCE
#: NAMES: a broad heuristic would flag the prose and the AST checks that must legitimately NAME
#: these references in order to refuse them.
#:
#: ``merge-base`` is deliberately ABSENT -- it is a subcommand, not a reference. It is also not
#: used by any declared proof here: every historical claim in this suite is anchored to two
#: explicit immutable commits, so no ``merge-base`` call appears in one at all.
MOVING_REFERENCE_LITERALS = frozenset({
    "HEAD", "origin/main", "origin/HEAD", "@{u}", "@{upstream}", "main", "refs/remotes/origin/main",
})

#: Git subcommands that write refs. A simulation must never run one against the real repository.
REF_MUTATING_GIT_SUBCOMMANDS = frozenset(
    {"update-ref", "branch", "reset", "checkout", "worktree", "switch"}
)

_SIM_ENV = {
    "GIT_AUTHOR_NAME": "sim", "GIT_AUTHOR_EMAIL": "sim@sim",
    "GIT_COMMITTER_NAME": "sim", "GIT_COMMITTER_EMAIL": "sim@sim",
}


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _git_in(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _commit_exists(sha: str, repo_root: Path = ROOT) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=repo_root, capture_output=True, text=True,
    ).returncode == 0


def _range_is_present(*shas: str, repo_root: Path = ROOT) -> bool:
    """Whether ANY of the named anchors is in this checkout.

    Deliberately ``any``, not ``all``. A checkout holding none of them is genuinely truncated and
    is an environment precondition; a checkout holding some but not all is a REFUSAL inside the
    proof, never a skip, so one unresolvable object cannot silence the whole thing.
    """
    return any(_commit_exists(sha, repo_root) for sha in shas)


def _blob_at(commit: str, relpath: str, repo_root: Path = ROOT) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", f"{commit}:{relpath}"],
        cwd=repo_root, capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _flat(text: str) -> str:
    """Collapse all runs of whitespace to single spaces, dropping blockquote markers.

    The decision is hard-wrapped prose, so an exact phrase can straddle a newline, and a quoted
    invariant carries a ``>`` marker on every wrapped line. Normalising both keeps every
    assertion an EXACT phrase match while making it insensitive to where a paragraph happens to
    wrap and to whether the sentence is quoted. Deliberately not a weakening: the full phrase
    must still be present, in order, verbatim -- only layout is normalised, never content.
    """
    unquoted = "\n".join(
        line[2:] if line.lstrip().startswith("> ") else line
        for line in (raw.lstrip() for raw in text.split("\n"))
    )
    return " ".join(unquoted.split())


def _section(text: str, letter: str) -> str:
    """The body of one lettered Decision subsection, flattened.

    Scoping an assertion to the section where a claim is OPERATIVE is what makes it
    mutation-sensitive: a phrase that also appears in a summary elsewhere can no longer satisfy a
    check on the section that actually carries the rule.
    """
    marker = f"\n### {letter}. "
    start = text.index(marker)
    rest = text[start + len(marker):]
    nxt = rest.find("\n### ")
    end = len(rest) if nxt == -1 else nxt
    return _flat(rest[:end])


def _function_source(source: str, name: str) -> str:
    fn = next(
        n for n in ast.walk(ast.parse(source))
        if isinstance(n, ast.FunctionDef) and n.name == name
    )
    return ast.get_source_segment(source, fn) or ""


def historical_proof_moving_ref_offenders(source: str, names: frozenset[str]) -> list[str]:
    """String literals naming a MOVING reference inside a declared historical proof.

    Module-level and shared, for the same reason the production module's own refusals are: a
    guard re-implemented inside its own proof can be disabled without anything noticing.

    Scoped BY NAME, not by shape. The same literal in a function whose subject genuinely IS live
    state is legitimate and must not be flagged -- flagging it would teach the wrong rule and
    produce exactly the false positives that get detectors switched off.
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


def _declared_historical_proofs(relative: str) -> frozenset[str]:
    """A module's own declared set, read from its source without importing it."""
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


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_flat(decision_text: str) -> str:
    return _flat(decision_text)


@pytest.fixture(scope="module")
def register_text() -> str:
    return (ROOT / REGISTER_RELPATH).read_text(encoding="utf-8")


# ======================================================================================
# 1 -- The authority: PR #347's own closed range, re-derived from the object store
# ======================================================================================


def _assert_pr347_closed_range_facts(
    *,
    base_sha: str = PR347_BASE_SHA,
    accepted_head: str = PR347_ACCEPTED_HEAD,
    merge_sha: str = PR347_MERGE_SHA,
    merge_tree: str = PR347_MERGE_TREE,
    repo_root: Path = ROOT,
) -> dict[str, str]:
    """Prove PR #347's merge identity and return its exact change set, by status.

    Every anchor is an explicit argument and every one is an immutable object. Nothing here reads
    ``HEAD``, ``origin/main``, ``merge-base``, the working tree, or any other reference that moves
    as the repository advances -- so the facts proved are invariant on a feature branch, on merged
    ``main`` where ``HEAD`` equals ``origin/main``, after ``main`` advances, and when unrelated
    later commits exist.

    An unresolvable object is a REFUSAL, never a skip; the caller decides whether a genuinely
    truncated checkout is an environment precondition (:func:`_range_is_present`).
    """
    for label, sha in (
        ("base", base_sha), ("accepted head", accepted_head), ("merge", merge_sha),
    ):
        assert _commit_exists(sha, repo_root), f"PR #347's {label} {sha} is not resolvable"

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
        """This unit's base IS PR #347's merge. Proven from the object store, not assumed."""
        if not _range_is_present(PR347_BASE_SHA, PR347_ACCEPTED_HEAD, PR347_MERGE_SHA):
            pytest.skip("PR #347's closed range is not present in this checkout")
        changed = _assert_pr347_closed_range_facts()
        assert len(changed) == 21, sorted(changed)
        assert PR347_MERGE_SHA == THIS_UNIT_BASE_SHA

    def test_the_authority_merged_with_zero_drift(self):
        """The tree that merged is exactly the tree the clean DELTA review examined."""
        if not _range_is_present(PR347_ACCEPTED_HEAD, PR347_MERGE_SHA):
            pytest.skip("PR #347's closed range is not present in this checkout")
        _assert_pr347_closed_range_facts()

    def test_the_first_reviewed_head_is_an_ancestor_of_the_accepted_head(self):
        """The bounded correction moved FORWARD from the reviewed head -- never a force-push.

        Both endpoints are immutable commits, so this is a statement about history and stays
        true wherever ``HEAD`` and ``origin/main`` happen to point.
        """
        if not _range_is_present(PR347_FIRST_REVIEWED_HEAD, PR347_ACCEPTED_HEAD):
            pytest.skip("PR #347's closed range is not present in this checkout")
        for sha in (PR347_FIRST_REVIEWED_HEAD, PR347_ACCEPTED_HEAD):
            assert _commit_exists(sha), sha
        assert subprocess.run(
            ["git", "merge-base", "--is-ancestor", PR347_FIRST_REVIEWED_HEAD, PR347_ACCEPTED_HEAD],
            cwd=ROOT, capture_output=True, text=True,
        ).returncode == 0
        assert PR347_FIRST_REVIEWED_HEAD != PR347_ACCEPTED_HEAD

    def test_the_decision_records_the_exact_lifecycle_identities(self, decision_flat):
        for identity in (
            PR347_BASE_SHA, PR347_FIRST_REVIEWED_HEAD, PR347_ACCEPTED_HEAD,
            PR347_MERGE_SHA, PR347_MERGE_TREE,
            PR347_FULL_REVIEW, PR347_CLEAN_DELTA_REVIEW, PR347_PRINCIPAL_ACCEPTANCE,
            PR347_POST_MERGE_VERIFICATION, PR347_FINAL_CLOSURE,
            PR347_MERGE_CI_RUN, PR347_MERGE_CI_JOB,
        ):
            assert identity in decision_flat, identity


# ======================================================================================
# 2 -- The authority gap, reproduced PRECISELY -- including the citation correction
# ======================================================================================


class TestTheAuthorityGapIsReproducedPrecisely:
    def test_step_8s_own_budget_is_recorded_as_spent_by_xasset_0037(self, decision_text):
        b = _section(decision_text, "B")
        # Pinned at the FULL sentence, not the shared fragment. The fragment occurs twice in
        # §B.1 -- once summarising and once quoting `XASSET-0043` §C -- so a check on the
        # fragment alone survives mutating either occurrence. That is a recorded miss class in
        # this programme, and it was reproduced against this very assertion before it was
        # tightened.
        assert (
            "**`XASSET-0037` performed that one, and this decision does not reopen, "
            "re-consume, or re-issue it.**"
        ) in b
        assert "Step 8's own single rebinding remains spent" in b
        assert "step-8 **equivalent**" in b
        assert "link 2" in b
        assert "never a second draw on step 8's own spent budget" in b

    def test_the_looser_reading_is_refused_rather_than_adopted(self, decision_text):
        """The correction must be OPERATIVE, not merely mentioned.

        A filing that quietly adopts "step 8 is unperformed" teaches the next session to draw on
        a budget three accepted decisions record as spent. Pinned in §B, where the correction is
        made, and again in the Rationale, where it is explained.
        """
        b = _section(decision_text, "B")
        assert "**wrong on the accepted record**, and this filing declines to adopt it" in b
        assert (
            "**The substance of the gap is unchanged by this correction; only the citation is.**"
        ) in b
        assert "corrects that citation openly rather than quietly adopting" in _flat(decision_text)

    def test_every_gap_finding_cites_the_decision_it_comes_from(self, decision_text):
        b = _section(decision_text, "B")
        for citation in (
            "`XASSET-0043` §C", "`XASSET-0044` §C", "`XASSET-0041` §I",
            "`XASSET-0036` §A", "`XASSET-0043` §F", "`XASSET-0045` §E",
            "`XASSET-0046` §F", "`XASSET-0047` §I", "`XASSET-0047` §A",
            "`XASSET-0030` §D",
        ):
            assert citation in b, citation

    def test_section_d_is_a_provision_not_a_grant(self, decision_text):
        b = _section(decision_text, "B")
        assert "is a provision, not a grant" in b.lower()
        assert "never said who may open one" in b

    def test_the_conclusion_is_that_no_live_authority_existed(self, decision_text):
        b = _section(decision_text, "B")
        assert "**No accepted authority currently permits a future step-8-equivalent rebinding unit**" in b
        assert "rather than by inference or by exhaustion" in b


class TestEverySupersededGrantIsRecordedAsUnavailable:
    """Each superseded grant fails in a DIFFERENT way, and the differences are load-bearing.

    ``XASSET-0043``'s was spent by USE. ``XASSET-0045``'s NEVER VESTED. ``XASSET-0046``'s was
    spent by ``XASSET-0047``. Collapsing them into one word is how a future session reaches for
    an unspent-looking grant by analogy to a spent one -- the exact confusion ``XASSET-0046`` §E
    was written to prevent.
    """

    @pytest.mark.parametrize(
        "phrase",
        (
            "the *authorized unit was expended*",
            "**may not be reused**",
            "**never vested**",
            "**Completing this unit authorizes no further unit**",
            "spent by use",
        ),
    )
    def test_the_distinct_failure_modes_are_stated(self, decision_text, phrase):
        assert phrase in _section(decision_text, "B"), phrase

    def test_the_alternatives_table_rejects_each_one_by_name(self, decision_flat):
        for rejected in (
            "Reuse `XASSET-0043` §F for a second attempt",
            "Reuse `XASSET-0045` §F or `XASSET-0046` §F",
            "Treat `XASSET-0030` §D as self-executing authority",
            "Treat `XASSET-0030` §G.B step 8 as still unspent",
        ):
            assert rejected in decision_flat, rejected


# ======================================================================================
# 3 -- The grant: exactly one unit, and exactly what it may do
# ======================================================================================


class TestTheGrantIsBounded:
    def test_the_determination_is_the_expected_one(self, decision_text):
        a = _section(decision_text, "A")
        assert "`STEP_8_EQUIVALENT_REBINDING_AUTHORIZED`" in _flat(decision_text)
        assert "**Exactly one future, separate, bounded pull request is authorized**" in a
        assert "step-8-equivalent" in a

    def test_the_determination_says_design_only_and_arms_nothing(self, decision_text):
        a = _section(decision_text, "A")
        assert "**Design only.**" in a
        assert "adds **zero activation authority**" in a
        assert "**Merging this decision performs no rebinding and arms nothing.**" in a

    def test_the_grant_names_exactly_one_unit(self, decision_text):
        e = _section(decision_text, "E")
        assert "**exactly one** future, separate, bounded pull request may" in e

    def test_the_successor_identifier_is_never_predicted(self, decision_text):
        e = _section(decision_text, "E")
        assert "**verified unused against live repository state at the time it is filed**" in e
        assert "never predicted, reserved, or named here" in e

    def test_no_identifier_beyond_this_one_is_named(self, decision_text):
        """MUTATION PIN. Naming ``XASSET-0049`` would silently pre-authorize the successor,
        which is exactly what §E forbids two lines above."""
        import re

        named = {int(m.split("-")[1]) for m in re.findall(r"XASSET-00\d\d", decision_text)}
        beyond = {n for n in named if n > 48}
        assert beyond == set(), beyond

    @pytest.mark.parametrize(
        "permitted",
        (
            "file its **own** rebinding decision record",
            "rebind the effective structural authorization source",
            "`AUTHORIZING_PULL_REQUEST` and `REVIEWED_BASE_SHA`",
            "extend\n   `LOAD_BEARING_RELPATHS` **additively**",
            "**only** in authorization language, in lockstep",
            "recompute stale identities and pins **once**",
            "**without weakening any of them**",
        ),
    )
    def test_each_permitted_act_is_enumerated(self, decision_text, permitted):
        assert _flat(permitted) in _section(decision_text, "E"), permitted


# ======================================================================================
# 4 -- The required properties are CONDITIONS, not advice
# ======================================================================================


class TestTheRequiredPropertiesAreConditions:
    def test_they_are_conditions_and_unwaivable(self, decision_text):
        f = _section(decision_text, "F")
        assert "**None is satisfied by this filing**" in f
        assert "none may be waived by the unit that performs it" in f

    def test_exact_closed_transitions_are_required_at_both_ends(self, decision_text):
        f = _section(decision_text, "F")
        assert "**exact closed transition**" in f
        assert "the old value and the new value, both explicit, both bound" in f
        assert "with the old value preserved rather than overwritten" in f
        assert "drift wearing a rebinding's label" in f
        # The anchor itself is inside the rule, not exempt from it.
        assert "`AUTHORIZING_DECISION`, `AUTHORIZING_PULL_REQUEST`, `REVIEWED_BASE_SHA`" in f

    def test_the_transition_rule_names_every_class_of_moved_value(self, decision_text):
        f = _section(decision_text, "F")
        for kind in (
            "each rebound constant", "each hash pin", "each identity family member",
            "`LOAD_BEARING_RELPATHS` membership change", "the lifecycle anchor itself",
        ):
            assert kind in f, kind

    def test_canonical_enforcement_and_outcome_producing_bytes_must_all_be_bound(
        self, decision_text
    ):
        f = _section(decision_text, "F")
        assert (
            "No outcome-producing executable code may be created, changed, or left outside the "
            "bound execution identity after the final rebinding and before `ATTEMPT_1`."
        ) in f
        for component in (
            "the canonical artifacts", "the enforcement/validator surface",
            "the deterministic runner", "the result writer/serializer",
            "the result validator", "the deterministic derivation surface",
        ):
            assert component in f, component
        assert "proved by exact byte identity, never asserted by naming" in f

    def test_the_base_must_be_derived_and_proved_rather_than_asserted(self, decision_text):
        """Renamed and re-pointed by the MAJOR 1 correction. The prior name described the
        superseded ancestry-only rule; the requirement is now derivation plus PROOF of the
        equality §F.2 makes operative."""
        f = _section(decision_text, "F")
        assert "prove the equality from the git object store" in f
        assert "**The operative rule is equality, not descent.**" in f
        assert "is not a verified base" in f

    def test_the_base_rule_is_equality_to_this_decisions_own_merge(self, decision_text):
        """MAJOR 1 (review 4998661361). The prior §F.2 required only that the future base
        DESCEND from this filing's own pre-authoring `main`, so any later commit qualified and
        the future unit could absorb bytes no review of this grant ever saw. The operative rule
        is now EQUALITY to this decision's own lifecycle-closing merge."""
        f = _section(decision_text, "F")
        assert "**The operative rule is equality, not descent.**" in f
        assert (
            "must **equal** the exact normal-merge commit that closes this decision's own §J "
            "lifecycle"
        ) in f
        # The identity must be DERIVED from the closed lifecycle, never predicted.
        for element in (
            "whose first parent is", "whose second parent is this decision's independently",
            "byte-identical to that accepted head's own", "merge-commit CI succeeded at that exact merge SHA",
            "final post-CI closure was\nrecorded",
        ):
            assert _flat(element) in f, element
        assert "**not stated here as a literal SHA and must never be predicted**" in f
        assert "derive it from this decision's completed" in f

    def test_ancestry_is_stated_necessary_but_explicitly_insufficient(self, decision_text):
        f = _section(decision_text, "F")
        assert "**Ancestry is necessary history and explicitly insufficient authority.**" in f
        assert f"must still descend from `{THIS_UNIT_BASE_SHA}`" in f
        assert "descent alone never qualifies a base" in f
        assert "it does not prove scope identity" in f

    def test_any_intervening_main_commit_is_drift_and_a_stop(self, decision_text):
        f = _section(decision_text, "F")
        assert "**Any intervening `main` commit is drift, and drift is a stop.**" in f
        assert "**may not proceed on the strength of this authorization**" in f
        assert "It must stop and obtain new authority" in f
        assert "**explicit closed identity transition** under §F.3" in f
        assert (
            "**Intervening bytes are never absorbed merely because the base descends from "
            "`bb95ed26…`.**"
        ) in f

    def test_the_determination_does_not_diverge_from_the_base_rule(self, decision_text):
        """§A and §F.2 must not drift apart: §A is where a future author reads the grant first."""
        a = _section(decision_text, "A")
        assert "**this decision's own lifecycle-closing merge**" in a
        assert "the base §F.2 closes by equality, never a later descendant of it" in a

    def test_the_boundary_may_only_grow(self, decision_text):
        f = _section(decision_text, "F")
        assert "may only be extended" in f
        assert "No existing member may be removed, swapped, or traded away" in f

    def test_pins_are_recomputed_once_and_last(self, decision_text):
        f = _section(decision_text, "F")
        assert "recomputed exactly once, strictly after every authorized byte has stabilized" in f

    def test_one_unit_one_pull_request_and_the_full_lifecycle(self, decision_text):
        f = _section(decision_text, "F")
        for gate in (
            "independent **FULL** exact-head review under `OPS-0007` §1",
            "bounded correction and exact-head re-review",
            "explicit principal exact-head acceptance at the final head",
            "normal merge",
            "immediate post-merge verification",
            "**successful merge-commit CI whose `head_sha` is the exact merge SHA**",
            "final post-CI verification and lifecycle closure",
        ):
            assert gate in f, gate
        assert "**stop and disclose**, never decide it silently" in f


class TestTheOutcomeSurfaceSemanticsArePreserved:
    @pytest.mark.parametrize(
        "preserved",
        (
            "The runner, the result validator, the universe closure validator",
            "the deterministic derivation surface",
            "the frozen construction identities",
            "the cardinality **680 / 48**",
            "`73c0965e…5224`",
            "`comparison_subject_kind`",
            "`unordered_pair_id`",
            "the accepted B1 / B2 / B3 semantics",
        ),
    )
    def test_each_preserved_element_is_named(self, decision_text, preserved):
        assert preserved in _section(decision_text, "F"), preserved

    def test_the_rule_is_that_binding_bytes_does_not_move_meaning(self, decision_text):
        f = _section(decision_text, "F")
        assert "are **preserved unchanged**" in f
        assert "The rebinding binds bytes; it does not get to move meaning." in f
        assert "requires its **own separate, express** authorization" in f


class TestAdverseHistoryIsPreserved:
    @pytest.mark.parametrize(
        "identifier",
        (
            XASSET0044_FAILED_CI_RUN, XASSET0044_FAILED_CI_JOB,
            XASSET0045_FAILED_CI_RUN, XASSET0045_FAILED_CI_JOB,
        ),
    )
    def test_both_failed_runs_are_named_by_exact_identity(
        self, decision_text, decision_flat, identifier
    ):
        """Pinned PER SECTION, not once for the whole document.

        Each identifier occurs twice -- in §B.3, establishing why the prior grants are gone, and
        in §F.9, preserving them as immutable adverse history. A whole-document check survives
        corrupting either occurrence, which is the same miss class the §B.1 fragment showed and
        which was reproduced against this very assertion before it was tightened.
        """
        assert identifier in decision_flat, identifier
        assert identifier in _section(decision_text, "B"), f"§B: {identifier}"
        assert identifier in _section(decision_text, "F"), f"§F: {identifier}"

    def test_every_way_of_erasing_them_is_refused(self, decision_text):
        f = _section(decision_text, "F")
        for forbidden in (
            "re-run in place", "relabelled successful", "deleted", "suppressed", "waived",
            "described as passing",
            "represented as satisfying its decision's own effectivity condition",
        ):
            assert forbidden in f, forbidden
        assert "closure may be posted retrospectively" in f

    def test_every_predecessor_identity_family_is_carried_forward(self, decision_text):
        f = _section(decision_text, "F")
        for family in (
            "`XASSET-0029`", "`XASSET-0036`", "the executable package", "`XASSET-0037`",
            "`XASSET-0041`", "`XASSET-0042`", "`XASSET-0043`", "`XASSET-0044`",
            "`XASSET-0045`", "`XASSET-0046`", "`XASSET-0047`",
        ):
            assert family in f, family
        assert "none is retired, weakened, or collapsed into another" in f

    def test_the_stopped_and_spent_states_are_restated(self, decision_text):
        f = _section(decision_text, "F")
        assert "remain **not effective**" in f
        assert "remains **spent**" in f
        assert "`STOPPED_BEFORE_ATTESTATION`" in f


# ======================================================================================
# 5 -- Everything withheld stays withheld
# ======================================================================================


class TestEveryWithheldActionIsWithheld:
    @pytest.mark.parametrize(
        "withheld",
        (
            "renewed readiness verification",
            "renewed drift verification",
            "**Step 11** in any part",
            "generating, pre-staging, or validating any **attestation**",
            "creating `READY`, `CLAIMED`, or `COMPLETED` lane state",
            "writing `AUTHORIZATION_ROOT`",
            "**arming** Stage 1",
            "**claiming** or consuming any part of `ATTEMPT_1`",
            "evaluating any gate for any registered construction",
            "executing Stage 1, or performing any results work",
            "producing a `stage1_results.yaml`",
            "acquiring market, fundamental, economic, or Stage-2 data",
            "reading, listing, opening, or substantively reusing any `risk_lane_boundary`",
            "consuming any part of `XASSET-0027` §P.1",
        ),
    )
    def test_each_withheld_action_is_named_in_the_withholding_section(
        self, decision_text, withheld
    ):
        assert withheld in _section(decision_text, "G"), withheld

    def test_links_three_four_and_five_each_keep_their_own_authority(self, decision_text):
        g = _section(decision_text, "G")
        assert (
            "**Links 3, 4 and 5 each require their own separate authority and their own complete "
            "lifecycle.**" in g
        )
        assert "`XASSET-0039` §K already foreclosed" in g

    def test_p1_remains_one_and_unspent(self, decision_text):
        c = _section(decision_text, "C")
        assert "**not consumed, replaced, amended, or counted against**" in c
        assert "**one, unspent.**" in c


class TestZeroActivationAuthority:
    def test_the_decision_adds_zero_activation_authorizations(self, decision_text):
        d = _section(decision_text, "D")
        assert (
            "**This decision adds one authorized rebinding and ZERO activation authorizations.**"
        ) in d
        assert "**No committed value in this repository authorizes Stage-1 execution**" in d
        assert "stays permanently `false`" in d
        assert "never a merged pull request" in d

    def test_the_regress_argument_is_stated_rather_than_assumed(self, decision_text):
        d = _section(decision_text, "D")
        assert "**changes no repository state**" in d
        assert "categorically outside the step §E terminates" in d


# ======================================================================================
# 6 -- THIS filing performs no rebinding: proved against bytes and symbols
# ======================================================================================


class TestThisFilingPerformsNoRebinding:
    """The single most important property here, and the one prose alone cannot establish.

    A design-only authorization that quietly moved one constant would be a rebinding wearing an
    authorization's label. So this is checked against the production module's own imported values
    and against its bytes at an immutable base -- never against the decision's description of
    itself.
    """

    def test_the_lifecycle_anchor_is_untouched(self):
        assert A.AUTHORIZING_DECISION == ANCHOR_DECISION_AT_BASE
        assert A.AUTHORIZING_PULL_REQUEST == ANCHOR_PULL_REQUEST_AT_BASE
        assert A.REVIEWED_BASE_SHA == ANCHOR_REVIEWED_BASE_AT_BASE

    def test_the_anchor_is_not_this_decision(self):
        """The inverse of the test above, and not redundant with it: this one fails for ANY
        value that names this unit, including one a future edit invents."""
        assert A.AUTHORIZING_DECISION != DECISION_ID
        assert A.AUTHORIZING_PULL_REQUEST != THIS_PULL_REQUEST

    def test_the_trust_boundary_is_unchanged(self):
        assert len(A.LOAD_BEARING_RELPATHS) == LOAD_BEARING_COUNT_AT_BASE
        assert DECISION_RELPATH not in A.LOAD_BEARING_RELPATHS
        assert SUITE_PATH.name not in A.LOAD_BEARING_RELPATHS

    def test_the_universe_is_unchanged(self):
        assert A.CONSTRUCTION_UNIVERSE_SHA256 == UNIVERSE_SHA256
        assert A.CONSTRUCTION_COUNT == UNIVERSE_COUNT
        assert A.CONSTRUCTION_CELL_COUNT == UNIVERSE_CELL_COUNT

    def test_the_canonical_pins_still_match_the_live_canonical_files(self):
        for relative, pin in A.CANONICAL_PINS.items():
            live = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            assert live == pin, relative

    def test_every_frozen_path_is_byte_identical_to_this_units_base(self):
        """Compared against an IMMUTABLE commit -- this unit's own base -- so the comparison
        neither depends on where ``HEAD`` points nor collapses to empty once this branch merges."""
        if not _range_is_present(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        assert _commit_exists(THIS_UNIT_BASE_SHA)
        drifted = []
        for relative in FROZEN_AGAINST_BASE_RELPATHS:
            at_base = _blob_at(THIS_UNIT_BASE_SHA, relative)
            assert at_base is not None, f"{relative} does not exist at the base"
            live = _git("hash-object", relative)
            if live != at_base:
                drifted.append(relative)
        assert drifted == [], drifted
        # Non-vacuity: the list really was walked and really resolved blobs.
        assert len(FROZEN_AGAINST_BASE_RELPATHS) >= 20

    def test_the_frozen_vocabulary_is_pinned_by_content(self):
        """MUTATION PIN. A declared vocabulary that nothing pins can be GUTTED while the check
        that consumes it still reports clean -- swap a genuinely load-bearing path for any
        unchanged file and both the length check and the drift check stay green. Reproduced
        against this suite before this pin existed."""
        for required in (
            AUTH_MODULE_RELPATH,
            "level1_stage1_runner.py",
            "level1_stage1_result_validator.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "research/level1_endpoint_evidence/PROTOCOL_V1.md",
            "research/level1_endpoint_evidence/pre_registration.yaml",
            "targets.yaml",
            "holdings.yaml",
            "gates.yaml",
        ):
            assert required in FROZEN_AGAINST_BASE_RELPATHS, required
        # Every path the production module itself declares load-bearing must be frozen here.
        missing = [r for r in A.LOAD_BEARING_RELPATHS if r not in FROZEN_AGAINST_BASE_RELPATHS]
        assert missing == [], missing
        # Non-vacuity: the module really declared a boundary to check against.
        assert len(A.LOAD_BEARING_RELPATHS) == LOAD_BEARING_COUNT_AT_BASE

    def test_the_load_bearing_cross_check_is_falsifiable(self):
        """MUTATION PIN. The cross-check above can be hollowed out to a truthy expression and
        still pass, so the RULE it applies is extracted and driven against a known-bad list as
        well as the real one. Reproduced against this suite before this test existed."""

        def missing_from(frozen):
            return [r for r in A.LOAD_BEARING_RELPATHS if r not in frozen]

        assert missing_from(FROZEN_AGAINST_BASE_RELPATHS) == []
        gutted = tuple(r for r in FROZEN_AGAINST_BASE_RELPATHS if r != AUTH_MODULE_RELPATH)
        assert missing_from(gutted) == [AUTH_MODULE_RELPATH]

    def test_the_decision_and_this_suite_did_not_exist_at_the_base(self):
        """The converse of the frozen check: this unit's OWN additions must be genuinely new,
        so the frozen list cannot be quietly satisfied by a file that never changed anywhere."""
        if not _range_is_present(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        for relative in (DECISION_RELPATH, SUITE_PATH.name):
            assert _blob_at(THIS_UNIT_BASE_SHA, relative) is None, relative
            assert (ROOT / relative).exists(), relative

    def test_the_decision_says_it_edits_the_module_not_at_all(self, decision_flat):
        assert "edits `level1_stage1_execution_authorization.py` not at all" in decision_flat
        assert "**performs no rebinding**" in decision_flat


# ======================================================================================
# 6b -- MAJOR 1 (review 4998661361): the future base is closed to THIS decision's own merge
#
# The reviewed head's §F.2 required only that the future rebinding base **descend from**
# `bb95ed26…` -- this filing's own PRE-AUTHORING `main`. Reproduced before correcting: under
# that rule a synthetic LATER descendant of this decision's own merge still qualified, so the
# future unit could have absorbed and rebound intervening bytes that were never present in the
# head independently reviewed and principal-accepted for this grant. Ancestry proves history,
# not scope identity.
#
# The rule is extracted here as a PURE function so it can be driven against known-good and
# known-bad inputs rather than only asserted in prose, and so the pre-correction rule can be
# run side by side and shown to accept what the corrected rule refuses. That side-by-side is
# the point: a guard that is never shown accepting something is a guard whose discrimination
# has not been demonstrated.
#
# THIS DECISION HAS NOT MERGED, so its own merge SHA is neither stated nor predicted anywhere.
# Every test below supplies the authorizing-merge identity as an explicit argument, over
# synthetic git objects built in an isolated clone.
# ======================================================================================


#: A 40-character lowercase hex commit name. Anything else is malformed, and malformed is a
#: REFUSAL rather than a best-effort match -- an identity that cannot be resolved cannot be
#: proved equal to anything.
def _is_commit_name(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(c in "0123456789abcdef" for c in value)
    )


def ancestry_only_base_is_acceptable(candidate_base, historical_base, *, is_ancestor):
    """The PRE-CORRECTION rule, kept so the correction is demonstrable rather than asserted.

    This is exactly what the reviewed head's §F.2 required: descent from the filing's own
    pre-authoring ``main``. It is retained ONLY to be driven alongside the corrected rule and
    shown accepting a later descendant. It is never the operative rule.
    """
    if not (_is_commit_name(candidate_base) and _is_commit_name(historical_base)):
        return False
    return is_ancestor(historical_base, candidate_base)


def authorizing_merge_base_is_acceptable(
    candidate_base, authorizing_merge, historical_base, *, is_ancestor
):
    """The CORRECTED §F.2 rule. Returns ``(accepted, reason)``.

    ``authorizing_merge`` is the exact normal-merge commit that closes this decision's own §J
    lifecycle. It is a REQUIRED ARGUMENT and is never defaulted, derived from a ref, or guessed
    -- this decision has not merged, and a rule that could invent that identity would be the
    same defect it exists to refuse.

    Equality is the operative test. Ancestry from ``historical_base`` is additionally required
    as necessary history, but is never sufficient on its own.
    """
    if not _is_commit_name(authorizing_merge):
        return False, "authorizing merge identity missing or malformed"
    if not _is_commit_name(candidate_base):
        return False, "candidate base missing or malformed"
    if not _is_commit_name(historical_base):
        return False, "historical base missing or malformed"
    if candidate_base != authorizing_merge:
        return False, (
            "candidate base does not EQUAL this authorization's own lifecycle-closing merge; "
            "descent is not sufficient authority"
        )
    if not is_ancestor(historical_base, candidate_base):
        return False, "candidate base does not descend from the historical base"
    return True, "candidate base equals the authorizing merge and descends from history"


class TestTheFutureBaseIsClosedByEquality:
    """Pure-function coverage. No git required, so the rule itself is under test."""

    #: An ``is_ancestor`` that says yes to everything. Any acceptance below is therefore due to
    #: the EQUALITY test and never to ancestry -- which is the property in dispute.
    ALWAYS_ANCESTOR = staticmethod(lambda a, d: True)

    MERGE = "a" * 40
    LATER = "b" * 40
    UNRELATED = "c" * 40
    HISTORICAL = "d" * 40

    def test_it_accepts_the_exact_authorizing_merge(self):
        ok, reason = authorizing_merge_base_is_acceptable(
            self.MERGE, self.MERGE, self.HISTORICAL, is_ancestor=self.ALWAYS_ANCESTOR
        )
        assert ok is True, reason
        # The acceptance must state BOTH conditions it actually checked. A bare "ok" would let
        # a future reader believe descent alone had been established.
        assert "equals the authorizing merge" in reason
        assert "descends from history" in reason

    def test_it_refuses_a_later_descendant_even_with_valid_ancestry(self):
        """The MAJOR 1 defect, stated as a test. Ancestry is granted unconditionally here, so
        only equality can be doing the refusing."""
        ok, reason = authorizing_merge_base_is_acceptable(
            self.LATER, self.MERGE, self.HISTORICAL, is_ancestor=self.ALWAYS_ANCESTOR
        )
        assert ok is False
        assert "does not EQUAL" in reason

    def test_it_refuses_an_unrelated_commit(self):
        ok, _ = authorizing_merge_base_is_acceptable(
            self.UNRELATED, self.MERGE, self.HISTORICAL, is_ancestor=self.ALWAYS_ANCESTOR
        )
        assert ok is False

    def test_it_refuses_a_base_that_equals_the_merge_but_lacks_ancestry(self):
        """Ancestry stays NECESSARY. Dropping it would trade one half-rule for another."""
        ok, reason = authorizing_merge_base_is_acceptable(
            self.MERGE, self.MERGE, self.HISTORICAL, is_ancestor=lambda a, d: False
        )
        assert ok is False
        assert "does not descend" in reason

    @pytest.mark.parametrize(
        "candidate, merge",
        (
            (None, "a" * 40),
            ("a" * 40, None),
            ("", "a" * 40),
            ("a" * 39, "a" * 40),
            ("A" * 40, "A" * 40),
            ("z" * 40, "z" * 40),
            (123456, "a" * 40),
            ("a" * 41, "a" * 40),
        ),
    )
    def test_it_refuses_missing_or_malformed_identities(self, candidate, merge):
        ok, _ = authorizing_merge_base_is_acceptable(
            candidate, merge, self.HISTORICAL, is_ancestor=self.ALWAYS_ANCESTOR
        )
        assert ok is False

    @pytest.mark.parametrize("merge", (None, "", "a" * 39, "A" * 40, 123456))
    def test_a_malformed_authorizing_identity_is_reported_as_such(self, merge):
        """MUTATION PIN. Dropping the authorizing-identity check leaves the refusal intact --
        an unresolvable identity can never equal a valid candidate -- but degrades the REASON
        from "identity missing or malformed" to "does not EQUAL". Those are different failures:
        the first is a stop because the authorization's own merge cannot be resolved, the second
        is a scope violation by a resolvable base. Reproduced before this pin existed."""
        ok, reason = authorizing_merge_base_is_acceptable(
            "a" * 40, merge, self.HISTORICAL, is_ancestor=self.ALWAYS_ANCESTOR
        )
        assert ok is False
        assert reason == "authorizing merge identity missing or malformed", reason

    def test_the_authorizing_merge_identity_has_no_default(self):
        """A rule that could supply this argument itself could invent the very identity §F.2
        forbids predicting. It is positional and required, and this pins that."""
        import inspect

        sig = inspect.signature(authorizing_merge_base_is_acceptable)
        merge = sig.parameters["authorizing_merge"]
        assert merge.default is inspect.Parameter.empty
        assert merge.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
        with pytest.raises(TypeError):
            authorizing_merge_base_is_acceptable("a" * 40, is_ancestor=self.ALWAYS_ANCESTOR)

    def test_equality_not_ancestry_is_the_operative_rule(self):
        """The two rules driven side by side on the SAME later descendant. The pre-correction
        rule accepts it; the corrected rule refuses it. If both agreed, the correction would be
        cosmetic."""
        assert ancestry_only_base_is_acceptable(
            self.LATER, self.HISTORICAL, is_ancestor=self.ALWAYS_ANCESTOR
        ) is True
        ok, _ = authorizing_merge_base_is_acceptable(
            self.LATER, self.MERGE, self.HISTORICAL, is_ancestor=self.ALWAYS_ANCESTOR
        )
        assert ok is False


def test_the_corrected_base_rule_refuses_a_real_later_descendant(tmp_path):
    """The same discrimination, over REAL git objects rather than synthetic strings.

    Builds, in an isolated clone: a stand-in for this decision's own merge (a genuine
    ``--no-ff`` merge of this branch's head into its base), and a real later commit on top of
    it. Then runs both rules against both candidates using real ``git merge-base --is-ancestor``.

    The stand-in is built here and used only as an argument -- nothing is written to the real
    repository and no merge SHA is recorded anywhere in this filing.
    """
    if not _range_is_present(THIS_UNIT_BASE_SHA):
        pytest.skip("this unit's base is not present in this checkout")
    clone = _working_clone(tmp_path)
    branch_head = _git_in(clone, "rev-parse", "HEAD")
    if branch_head == THIS_UNIT_BASE_SHA:
        branch_head = _commit_on_top(clone, THIS_UNIT_BASE_SHA, "feature branch commit")
    _git_in(clone, "checkout", "--quiet", "-B", "sim-main", THIS_UNIT_BASE_SHA)
    subprocess.run(
        ["git", "merge", "--no-ff", "--quiet", "-m", "simulated authorization merge", branch_head],
        cwd=clone, capture_output=True, text=True, check=True,
        env={**os.environ, **_SIM_ENV},
    )
    authorizing_merge = _git_in(clone, "rev-parse", "HEAD")
    later = _commit_on_top(clone, authorizing_merge, "unrelated later main commit")
    assert later != authorizing_merge

    def real_is_ancestor(a, d):
        return subprocess.run(
            ["git", "merge-base", "--is-ancestor", a, d], cwd=clone, capture_output=True
        ).returncode == 0

    # The later commit genuinely IS a descendant -- so the refusal below is about identity.
    assert real_is_ancestor(THIS_UNIT_BASE_SHA, later)
    assert real_is_ancestor(authorizing_merge, later)

    # Pre-correction rule: the later descendant qualifies. This is the reproduced defect.
    assert ancestry_only_base_is_acceptable(
        later, THIS_UNIT_BASE_SHA, is_ancestor=real_is_ancestor
    ) is True

    # Corrected rule: only the authorizing merge itself qualifies.
    ok, _ = authorizing_merge_base_is_acceptable(
        authorizing_merge, authorizing_merge, THIS_UNIT_BASE_SHA, is_ancestor=real_is_ancestor
    )
    assert ok is True
    ok, reason = authorizing_merge_base_is_acceptable(
        later, authorizing_merge, THIS_UNIT_BASE_SHA, is_ancestor=real_is_ancestor
    )
    assert ok is False
    assert "does not EQUAL" in reason


def test_this_filing_records_no_predicted_merge_identity(self=None):
    """§F.2 forbids predicting this decision's own merge SHA, so neither the decision nor this
    suite may contain a bound one. Checked structurally: the only 40-hex commit names present
    must be ones this filing legitimately cites from CLOSED history."""
    known = {
        PR347_BASE_SHA, PR347_FIRST_REVIEWED_HEAD, PR347_ACCEPTED_HEAD, PR347_MERGE_SHA,
        THIS_UNIT_BASE_SHA, PR347_MERGE_TREE,
    }
    import re

    for relative in (DECISION_RELPATH, SUITE_PATH.name):
        text = (ROOT / relative).read_text(encoding="utf-8")
        found = set(re.findall(r"\b[0-9a-f]{40}\b", text))
        unexpected = found - known
        assert unexpected == set(), (relative, unexpected)
    # Non-vacuity: the scan really found the identities this filing does cite.
    assert PR347_MERGE_SHA in set(
        re.findall(r"\b[0-9a-f]{40}\b", DECISION_PATH.read_text(encoding="utf-8"))
    )


# ======================================================================================
# 7 -- Nothing is armed
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
        class that gets detectors switched off.
        """
        source = SUITE_PATH.read_text(encoding="utf-8")
        invoked: set[str] = set()
        for call in (c for c in ast.walk(ast.parse(source)) if isinstance(c, ast.Call)):
            if isinstance(call.func, ast.Attribute):
                invoked.add(call.func.attr)
            elif isinstance(call.func, ast.Name):
                invoked.add(call.func.id)
        for forbidden in (
            "write_authorization", "claim_execution", "complete_execution",
            "build_authorization_payload",
        ):
            assert forbidden not in invoked, forbidden
        # Non-vacuity: the parse really found this suite's calls.
        assert "_git" in invoked and len(invoked) > 20

    def test_the_final_section_closes_on_the_unarmed_state(self, decision_text):
        el = _section(decision_text, "L")
        assert "**Stage 1 remains UNARMED and NOT EXECUTABLE." in el
        assert "The lane is ABSENT." in el
        assert "`ATTEMPT_1` is intact, unclaimed, and unconsumed.**" in el


# ======================================================================================
# 8 -- No historical proof may consult a moving reference
#
# This is the defect class that stopped PRs #344 and #345: a proof about IMMUTABLE HISTORY
# whose answer changed with where ``HEAD`` or ``origin/main`` happened to point. Checked in
# BOTH directions -- a declared proof may not NAME a moving ref, and a function that names one
# may not be DECLARED a historical proof.
# ======================================================================================


class TestNoHistoricalProofMoves:
    def test_no_declared_proof_names_a_moving_reference(self):
        source = SUITE_PATH.read_text(encoding="utf-8")
        offenders = historical_proof_moving_ref_offenders(source, HISTORICAL_PROOF_FUNCTIONS)
        assert offenders == [], offenders

    def test_the_detector_is_falsifiable_in_both_directions(self):
        """Without this, emptying ``MOVING_REFERENCE_LITERALS`` or narrowing the name set leaves
        a detector that reports clean because it looks at nothing."""
        names = frozenset({"test_historical"})
        bad = (
            "def test_historical():\n"
            "    base = _git('rev-parse', 'origin/main')\n"
            "    assert base\n"
        )
        good = (
            "def test_historical():\n"
            "    base = _git('rev-parse', PR347_MERGE_SHA)\n"
            "    assert base\n"
        )
        assert historical_proof_moving_ref_offenders(bad, names) != []
        assert historical_proof_moving_ref_offenders(good, names) == []

    def test_a_moving_ref_function_is_not_declared_a_historical_proof(self):
        """The inverse direction. ``_live_ref`` genuinely reads live state and is legitimate --
        it must simply never be declared a proof about history."""
        assert "_live_ref" not in HISTORICAL_PROOF_FUNCTIONS
        assert "test_the_simulations_leave_the_real_repository_refs_undisturbed" not in (
            HISTORICAL_PROOF_FUNCTIONS
        )

    def test_the_declared_set_is_pinned_by_content_not_only_by_size(self):
        """MUTATION PIN. A declared vocabulary that nothing pins can be gutted while every
        consumer still reports clean -- a recorded miss class in this programme."""
        assert _declared_historical_proofs(SUITE_PATH.name) == HISTORICAL_PROOF_FUNCTIONS
        for required in (
            "_assert_pr347_closed_range_facts",
            "test_every_frozen_path_is_byte_identical_to_this_units_base",
            "test_the_decision_and_this_suite_did_not_exist_at_the_base",
        ):
            assert required in HISTORICAL_PROOF_FUNCTIONS, required
        assert len(HISTORICAL_PROOF_FUNCTIONS) >= 6

    def test_the_moving_reference_vocabulary_is_pinned_by_content(self):
        """MUTATION PIN, same class. Emptying this set silences every check that consumes it."""
        assert "HEAD" in MOVING_REFERENCE_LITERALS
        assert "origin/main" in MOVING_REFERENCE_LITERALS
        assert "refs/remotes/origin/main" in MOVING_REFERENCE_LITERALS
        # merge-base is a SUBCOMMAND, not a reference: flagging it would refuse a sound proof.
        assert "merge-base" not in MOVING_REFERENCE_LITERALS
        assert len(MOVING_REFERENCE_LITERALS) >= 6

    def test_no_simulation_mutates_a_ref_in_the_real_repository(self):
        """Every ref-writing subcommand must be reached through ``_git_in`` against a CLONE,
        never through ``_git``, which runs in ``ROOT``."""
        source = SUITE_PATH.read_text(encoding="utf-8")
        offenders = []
        for call in (c for c in ast.walk(ast.parse(source)) if isinstance(c, ast.Call)):
            if not (isinstance(call.func, ast.Name) and call.func.id == "_git"):
                continue
            for arg in call.args:
                if (
                    isinstance(arg, ast.Constant)
                    and isinstance(arg.value, str)
                    and arg.value in REF_MUTATING_GIT_SUBCOMMANDS
                ):
                    offenders.append(f"line {call.lineno}: _git({arg.value!r})")
        assert offenders == [], offenders
        assert len(REF_MUTATING_GIT_SUBCOMMANDS) >= 5


# ======================================================================================
# 9 -- The declared proofs really pass under every ref state, including merged main
# ======================================================================================


def _live_ref(name: str) -> str | None:
    """Resolve a ref in the REAL repository, READ-ONLY.

    Used ONLY to build simulated states and to prove the simulations leave the real refs
    undisturbed. Never asserted to equal a historical constant -- that inverse deadlock is a
    recorded finding on PR #345.
    """
    result = subprocess.run(
        ["git", "rev-parse", name], cwd=ROOT, capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


_LOCAL_HEAD_FOR_SIMULATION = _live_ref("HEAD") or PR347_MERGE_SHA


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
    "TestTheAuthorityIsRealAndClosed::"
    "test_the_first_reviewed_head_is_an_ancestor_of_the_accepted_head",
    "TestThisFilingPerformsNoRebinding::"
    "test_every_frozen_path_is_byte_identical_to_this_units_base",
    "TestThisFilingPerformsNoRebinding::test_the_decision_and_this_suite_did_not_exist_at_the_base",
    "TestNoHistoricalProofMoves::test_no_declared_proof_names_a_moving_reference",
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

    The WORKING TREE is always this branch's content -- every file under examination is copied in
    from the working tree, so the regression tests the code being reviewed rather than the
    previous commit. Only ``HEAD`` and ``origin/main`` move, which isolates ref position as the
    single variable.
    """
    if not _range_is_present(PR347_BASE_SHA, PR347_ACCEPTED_HEAD, PR347_MERGE_SHA):
        pytest.skip("this unit's closed range is not present in this checkout")
    clone = _working_clone(tmp_path)
    _git_in(clone, "checkout", "--quiet", "--detach", _LOCAL_HEAD_FOR_SIMULATION)
    for relative in (SUITE_PATH.name, DECISION_RELPATH, AUTH_MODULE_RELPATH):
        destination = clone / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)

    # A genuine feature-branch head: this session's own commit when it has one, and a synthesized
    # commit on top of the base when it does not. Taking the live HEAD on faith would silently
    # degrade the ``branch`` state into ``merged_main`` before this branch's first commit -- the
    # "still parametrised but no longer testing anything" shape the structural pins below refuse.
    branch_head = (
        _LOCAL_HEAD_FOR_SIMULATION
        if _LOCAL_HEAD_FOR_SIMULATION != PR347_MERGE_SHA
        else _commit_on_top(clone, PR347_MERGE_SHA, "feature branch commit")
    )

    if ref_state == "branch":
        head, main = branch_head, PR347_MERGE_SHA
    elif ref_state == "merged_main":
        head = main = PR347_MERGE_SHA
    elif ref_state == "later_main":
        head = branch_head
        main = _commit_on_top(clone, PR347_MERGE_SHA, "later main")
    elif ref_state == "head_equals_origin_main_later":
        head = main = _commit_on_top(clone, PR347_MERGE_SHA, "later main, checked out")
    else:
        main = PR347_MERGE_SHA
        for n in range(3):
            main = _commit_on_top(clone, main, f"unrelated later commit {n}")
        head = branch_head

    # Move the refs WITHOUT touching the working tree, so the files under test stay this branch's
    # own while ``git rev-parse`` reports the simulated state.
    _git_in(clone, "update-ref", "HEAD", head)
    _git_in(clone, "update-ref", "refs/remotes/origin/main", main)
    assert _git_in(clone, "rev-parse", "HEAD") == head
    assert _git_in(clone, "rev-parse", "origin/main") == main

    # Structural pins: each state must genuinely be the state it claims to be.
    if ref_state in ("later_main", "head_equals_origin_main_later", "unrelated_later_commits"):
        assert main != PR347_MERGE_SHA, f"{ref_state} must advance past this unit's base"
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


def test_the_ref_state_vocabulary_is_pinned_by_content():
    """MUTATION PIN. Deleting ``merged_main`` -- the exact state that broke PR #345 -- would
    leave the regression still parametrised and no longer testing the case that matters."""
    assert "merged_main" in REF_STATES
    assert "head_equals_origin_main_later" in REF_STATES
    assert "branch" in REF_STATES
    assert len(REF_STATES) == 5
    assert len(REF_STATE_SENSITIVE_TESTS) >= 5
    for required in (
        "TestThisFilingPerformsNoRebinding::"
        "test_every_frozen_path_is_byte_identical_to_this_units_base",
        "TestNoHistoricalProofMoves::test_no_declared_proof_names_a_moving_reference",
    ):
        assert required in REF_STATE_SENSITIVE_TESTS, required


def test_the_simulations_leave_the_real_repository_refs_undisturbed(tmp_path):
    """Before/after invariant on the REAL refs, WITHOUT requiring either to equal any historical
    commit -- that inverse deadlock is a recorded finding on PR #345."""
    before = (_live_ref("HEAD"), _live_ref("origin/main"))
    clone = _working_clone(tmp_path)
    _git_in(clone, "update-ref", "refs/remotes/origin/main", PR347_BASE_SHA)
    assert _git_in(clone, "rev-parse", "origin/main") == PR347_BASE_SHA
    after = (_live_ref("HEAD"), _live_ref("origin/main"))
    assert before == after, (before, after)
    # Non-vacuity: the real refs actually resolved, so this is a comparison, not two Nones.
    assert before[0] is not None


# ======================================================================================
# 10 -- Non-deadlock: this filing can actually attain its own §J.6
# ======================================================================================


#: Statements that would make this filing's own §J.6 unreachable. A decision may not both
#: REQUIRE successful exact-merge CI and say its own cannot be obtained -- that is the deadlock
#: XASSET-0045 shipped at its first reviewed head. A closed, explicit set, so the guard is
#: falsifiable rather than a vibe.
SELF_DEFEATING_PHRASES = (
    "cannot obtain successful merge-commit ci",
    "cannot obtain a successful merge-commit ci",
    "merge-commit ci cannot succeed",
    "its own merge-commit ci will fail",
    "this filing cannot satisfy condition 6",
)


class TestNonDeadlock:
    def test_the_decision_makes_no_self_defeating_claim(self, decision_text):
        lowered = _flat(decision_text).lower()
        for phrase in SELF_DEFEATING_PHRASES:
            assert phrase not in lowered, phrase
        assert len(SELF_DEFEATING_PHRASES) >= 5

    def test_the_self_defeating_vocabulary_is_pinned_by_content(self):
        """MUTATION PIN, same class as the frozen-path vocabulary. Replacing a real phrase with
        one that can never occur leaves the loop green while the guard checks nothing."""
        for required in (
            "cannot obtain successful merge-commit ci",
            "merge-commit ci cannot succeed",
            "this filing cannot satisfy condition 6",
        ):
            assert required in SELF_DEFEATING_PHRASES, required

    def test_the_self_defeating_detector_is_falsifiable(self):
        """Driven against a known-bad text, so the guard cannot pass by looking at nothing."""
        bad = "this filing cannot obtain successful merge-commit CI at its own merge SHA".lower()
        assert any(phrase in bad for phrase in SELF_DEFEATING_PHRASES)
        good = _flat(DECISION_PATH.read_text(encoding="utf-8")).lower()
        assert not any(phrase in good for phrase in SELF_DEFEATING_PHRASES)

    def test_attainability_is_stated_rather_than_assumed(self, decision_text):
        k = _section(decision_text, "K")
        assert "so this filing states its attainability rather than assuming it" in k
        assert "immutable commit ranges only" in k
        assert "simulated merged-`main` state where `HEAD` equals `origin/main`" in k
        assert "it is refused here in terms" in k

    def test_the_filing_changes_no_production_module(self, decision_text):
        k = _section(decision_text, "K")
        assert (
            "It changes no production module, no canonical artifact, no validator, no runner, "
            "and no universe value." in k
        )

    def test_the_effectivity_conditions_are_conjunctive_and_name_the_exact_merge_sha(
        self, decision_text
    ):
        j = _section(decision_text, "J")
        assert "**None is individually sufficient.**" in j
        assert "**successful merge-commit CI whose `head_sha` is the exact merge SHA**" in j
        assert "not a run against any other commit" in j
        assert "**Only complete closure of all seven does.**" in j
        assert "**Merging this decision performs no rebinding and arms nothing.**" in j
        for step in ("1.", "2.", "3.", "4.", "5.", "6.", "7."):
            assert step in j, step

    def test_the_effectivity_conditions_mirror_the_committed_gate_tuple(self, decision_text):
        j = _section(decision_text, "J")
        assert "`level1_stage1_execution_authorization.REQUIRED_LIFECYCLE_GATES`" in j
        assert "**That module is cited only and is byte-unchanged by this filing.**" in j
        # MINOR 1 (review 4998661361): a tuple is not a repository path. §J previously said the
        # tuple "is itself one of the sixteen load-bearing paths"; the load-bearing path is the
        # MODULE that contains it. Both halves are pinned in text and proved against the module.
        assert "a **six-element tuple**" in j
        assert "The tuple is not itself a repository path" in j
        assert (
            "the **module that contains it**, `level1_stage1_execution_authorization.py`, is one "
            "of the sixteen load-bearing paths"
        ) in j
        assert len(A.REQUIRED_LIFECYCLE_GATES) == 6
        assert AUTH_MODULE_RELPATH in A.LOAD_BEARING_RELPATHS


# ======================================================================================
# 11 -- No section is vacuous
# ======================================================================================


DECISION_SECTIONS = tuple("ABCDEFGHIJKL")


def test_every_lettered_section_exists_and_carries_substance(decision_text):
    """MUTATION PIN. A section reduced to its heading would satisfy every ``in`` check that
    happens to be scoped elsewhere; requiring real length refuses that shape."""
    for letter in DECISION_SECTIONS:
        body = _section(decision_text, letter)
        assert len(body) > 300, (letter, len(body))
    assert len(DECISION_SECTIONS) == 12


def test_the_decision_has_the_house_closing_sections(decision_text):
    for heading in ("## Rationale", "## Alternatives considered", "## Consequences"):
        assert heading in decision_text, heading
    tail = decision_text.split("## Consequences", 1)[1]
    assert "UNARMED and NOT EXECUTABLE" in tail
    assert len(_flat(tail)) > 600


# ======================================================================================
# 12 -- Catalog and register synchronisation
# ======================================================================================


class TestCatalogAndRegisterSynchronisation:
    def test_the_decision_is_indexed_exactly_once(self):
        catalog = yaml.safe_load((ROOT / CATALOG_RELPATH).read_text(encoding="utf-8"))
        rows = [d for d in catalog["decisions"] if d["decision_id"] == DECISION_ID]
        assert len(rows) == 1
        row = rows[0]
        assert row["file"] == DECISION_RELPATH
        assert row["supporting_artifact"] == SUITE_PATH.name
        assert row["status"] == "Proposed"
        assert row["category"] == "cross_asset_allocation_architecture"

    def test_the_catalog_row_relates_this_unit_to_its_authority_chain(self):
        catalog = yaml.safe_load((ROOT / CATALOG_RELPATH).read_text(encoding="utf-8"))
        row = next(d for d in catalog["decisions"] if d["decision_id"] == DECISION_ID)
        for related in (
            "XASSET-0030", "XASSET-0036", "XASSET-0037", "XASSET-0041", "XASSET-0043",
            "XASSET-0044", "XASSET-0045", "XASSET-0046", "XASSET-0047",
            "OPS-0001", "OPS-0007", "OPS-0009",
        ):
            assert related in row["related_decisions"], related

    def test_the_indexed_file_and_artifact_both_exist(self):
        assert DECISION_PATH.is_file()
        assert SUITE_PATH.is_file()

    def test_this_units_gate_is_in_progress_while_its_pull_request_is_unmerged(
        self, register_text
    ):
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        gate = next(g for g in ws["milestones"] if g["gate"] == REGISTER_GATE)
        assert gate["status"] == "in_progress"
        assert "a filing does not mark its own unmerged work complete" in gate["description"]

    def test_the_prior_units_post_merge_gate_is_additive_and_complete(self, register_text):
        """The prior gate's own accepted text is NOT edited. Its confirmed merged state is
        recorded by a NEW, additive gate -- the convention XASSET-0046 and XASSET-0047 each used."""
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        prior = next(g for g in ws["milestones"] if g["gate"] == PRIOR_UNIT_GATE)
        assert prior["status"] == "complete"
        assert prior["pr"] == 347
        for identity in (
            PR347_ACCEPTED_HEAD, PR347_MERGE_SHA, PR347_MERGE_TREE,
            PR347_CLEAN_DELTA_REVIEW, PR347_PRINCIPAL_ACCEPTANCE, PR347_FINAL_CLOSURE,
            PR347_MERGE_CI_RUN, PR347_MERGE_CI_JOB,
        ):
            assert identity in prior["description"], identity
        # The superseded gate's own text still says what it said.
        superseded = next(
            g for g in ws["milestones"]
            if g["gate"] == "xasset0047-post-merge-ci-recovery-reconciliation"
        )
        assert superseded["status"] == "in_progress"

    def test_the_shared_live_fields_advanced_to_this_units_verified_state(self, register_text):
        """``active_branch``, ``active_pr`` and ``last_verified_main_sha`` are WS-0014's SINGLE
        SHARED live self-reference. Leaving them pointed at a merged pull request would assert
        finished work as active."""
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        assert ws["last_verified_main_sha"] == THIS_UNIT_BASE_SHA
        assert ws["last_verified_main_sha"] != PR347_BASE_SHA
        assert ws["last_verified_date"] == "2026-08-22"
        assert ws["active_branch"] != "claude/xasset-0046-recovery-b31nba"
        assert ws["active_pr"] != 347

    def test_the_register_records_this_units_authority_gap_and_boundary(self, register_text):
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        gate = next(g for g in ws["milestones"] if g["gate"] == REGISTER_GATE)
        for phrase in (
            "DESIGN-ONLY", "STEP-8-EQUIVALENT", "EXACT CLOSED TRANSITIONS",
            "ZERO ACTIVATION AUTHORITY", "PERFORMS NO PART OF THAT REBINDING",
            "ONE AND UNSPENT",
        ):
            assert phrase in gate["description"], phrase

    def test_the_register_carries_the_corrected_base_rule_in_lockstep(self, register_text):
        """MAJOR 1 (review 4998661361). The register described the same ancestry-only rule the
        decision did. A register that still says "descend from" while the decision says "equals"
        is exactly the inconsistent-specification shape this programme has been bitten by, so
        both are pinned and both must move together."""
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        gate = next(g for g in ws["milestones"] if g["gate"] == REGISTER_GATE)
        described = " ".join(gate["description"].split())
        for phrase in (
            "EQUALS the exact normal-merge commit closing XASSET-0048's own SS-J lifecycle",
            "never predicted, since XASSET-0048 has not merged",
            "remains NECESSARY HISTORY but is EXPLICITLY INSUFFICIENT AUTHORITY",
            "any intervening main commit is DRIFT requiring a stop and new authority",
            "explicit closed identity transition",
            "NEVER absorbed merely because the base descends from",
        ):
            assert phrase in described, phrase
        # The superseded ancestry-only formulation must be gone, not merely supplemented.
        assert "shown to descend from bb95ed26" not in described

    def test_the_workstream_posture_is_unchanged(self, register_text):
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        assert ws["status"] == "proposed"
        assert ws["priority"] == "secondary"
        assert [w["id"] for w in data["workstreams"] if w.get("priority") == "primary"] == []

    def test_the_blocker_and_next_action_record_the_current_state(self, register_text):
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        for field in ("blocker", "next_action"):
            assert "UPDATE, 2026-08-22" in ws[field], field
            assert "XASSET-0048" in ws[field], field
            assert "UNARMED and NOT EXECUTABLE" in ws[field], field


# ======================================================================================
# 13 -- The bound pull-request number: sentinel, then read back, never guessed
# ======================================================================================


class TestTheBoundPullRequestNumber:
    def test_the_sentinel_is_impossible_as_a_real_number(self):
        """A pull-request number cannot be negative, so the sentinel can never validate by
        accident. That is exactly what makes it safe to commit before the draft is opened."""
        assert PULL_REQUEST_SENTINEL < 0

    def test_the_number_is_consistently_bound_or_consistently_unbound(self, register_text):
        """The genuine invariant, and it holds at BOTH ends of the sentinel-then-bind sequence.

        A half-bound state -- this suite naming a number the register does not, or the reverse --
        is how a filing ends up citing a pull request that is not its own.
        """
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        gate = next(g for g in ws["milestones"] if g["gate"] == REGISTER_GATE)
        if THIS_PULL_REQUEST == PULL_REQUEST_SENTINEL:
            assert gate["pr"] is None
            assert ws["active_pr"] is None
        else:
            assert gate["pr"] == THIS_PULL_REQUEST
            assert ws["active_pr"] == THIS_PULL_REQUEST

    def test_once_bound_it_is_later_than_every_predecessor_in_the_chain(self):
        """Monotonic by construction: GitHub issues numbers in order, so a number at or below any
        predecessor's would mean the constant was copied rather than read back."""
        if THIS_PULL_REQUEST == PULL_REQUEST_SENTINEL:
            pytest.skip("the number has not been issued yet")
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
            A.AUTHORIZING_PULL_REQUEST,
        ):
            assert THIS_PULL_REQUEST > predecessor, predecessor

    def test_binding_the_number_does_not_bind_it_into_the_production_module(self):
        """This is a DESIGN-ONLY filing, so its own pull-request number must appear nowhere in
        the operational-authorization module. A rebinding puts it there; an authorization does not."""
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert f"AUTHORIZING_PULL_REQUEST = {THIS_PULL_REQUEST}" not in source
        assert A.AUTHORIZING_PULL_REQUEST == ANCHOR_PULL_REQUEST_AT_BASE
