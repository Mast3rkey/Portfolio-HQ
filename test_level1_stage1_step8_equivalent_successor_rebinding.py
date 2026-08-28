"""Adversarial tests pinning the ``XASSET-0049`` step-8-equivalent successor operational rebinding.

``XASSET-0048`` closed an authority gap six consecutive filings had left open: it granted, for the
first time, **exactly one** future pull request to perform the ``XASSET-0030`` §G.B **step-8
equivalent** successor operational-authorization / load-bearing rebinding. Granting it left one
thing outstanding -- actually performing it -- and that is the whole of this unit.

The danger this suite exists to prevent is not the rebinding. It is the set of ways a rebinding can
look correct while being wrong:

1. **A base that merely DESCENDS from the authorizing merge.** ``TestBaseEqualityIsOperative`` --
   the rule extracted as a pure function and driven against a REAL synthetic later descendant,
   with the superseded descent-only rule retained beside it and shown ACCEPTING what the corrected
   rule refuses. This is the MAJOR finding ``XASSET-0048``'s own review made, and it is enforced
   here rather than described.
2. **A moved value with one end unbound.** ``TestExactClosedTransitions`` -- every moved constant
   bound at BOTH ends, with the old value preserved and independently reachable.
3. **A predecessor identity destroyed by the move.** ``TestPredecessorIdentitiesArePreserved`` --
   reproduced against the base, where ``XASSET-0047``'s identity was reachable ONLY through the
   three values this unit moves.
4. **The boundary shrunk, swapped, or traded rather than extended.**
   ``TestTrustBoundaryGrewAdditively``.
5. **An outcome-producing byte changed under cover of a byte-binding.**
   ``TestNoOutcomeProducingByteChanged`` -- proved by blob comparison against this unit's own base.
6. **The authority mistaken for the unit, or the superseded anchor silently retained.**
   ``TestTheNewRefusalsAreIndependentlyRequired``.
7. **Adverse history relabelled, or a stopped lifecycle treated as authority.**
   ``TestAdverseHistoryIsPreserved``.
8. **Something armed, claimed, or executed.** ``TestNothingIsArmed`` and
   ``TestZeroActivationAuthority``.
9. **A historical proof anchored to a reference that moves.** ``TestNoHistoricalProofMoves`` --
   the defect that stopped PRs #344 and #345.
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
import re
import subprocess
from pathlib import Path

import pytest
import yaml

import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
SUITE_PATH = Path(__file__).resolve()

DECISION_ID = "XASSET-0049"
DECISION_RELPATH = (
    "governance/decisions/"
    "XASSET-0049-endpoint-0001-stage-1-step-8-equivalent-successor-operational-rebinding.md"
)
DECISION_PATH = ROOT / DECISION_RELPATH
AUTHORITY_RELPATH = (
    "governance/decisions/"
    "XASSET-0048-endpoint-0001-stage-1-step-8-equivalent-rebinding-authorization.md"
)
CATALOG_RELPATH = "governance/decisions.yaml"
REGISTER_RELPATH = "operations/WORKSTREAMS.yaml"
AUTH_MODULE_RELPATH = "level1_stage1_execution_authorization.py"
REGISTER_GATE = "xasset0049-step8-equivalent-successor-operational-rebinding"
PRIOR_UNIT_GATE = "xasset0048-post-merge-verification"

# ── The impossible sentinel, and the number GitHub actually issued ──────────────────────────
#
# A pull-request number cannot be negative, so the sentinel can never be mistaken for a real one
# and can never accidentally validate. ``-2`` is deliberately distinct from XASSET-0047's own ``0``
# and XASSET-0048's own ``-1``, so this unit's sentinel can never be mistaken for a predecessor's.
PULL_REQUEST_SENTINEL = -2
#: Read back from live GitHub AFTER the draft was opened. Never predicted.
THIS_PULL_REQUEST = 349

# ── XASSET-0048's own closed range -- every anchor an immutable git object ───────────────────
#
# Independently re-derived from live git and live GitHub during the filing session and asserted
# here against the real object store, never taken on trust. Its merge is ALSO this unit's own base,
# by EQUALITY (XASSET-0048 §F.2) rather than by descent.

#: PR #348's base -- PR #347's merge commit.
PR348_BASE_SHA = "bb95ed26964b1bc7a2e230c76060fec82752efa1"
#: The head the first independent FULL review examined, before the bounded correction.
PR348_FIRST_REVIEWED_HEAD = "1c103a4949b9db3944aa22110c5f97eafaeee1c2"
#: PR #348's accepted head -- the exact commit the clean DELTA review examined.
PR348_ACCEPTED_HEAD = "42e3a8aec1b36c4e5f22e4cdf4210a61ed781156"
#: PR #348's merge commit. Also THIS unit's own base, and the successful merge-commit CI head_sha.
PR348_MERGE_SHA = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"
#: The tree carried by BOTH the accepted head and the merge -- zero merge drift.
PR348_MERGE_TREE = "514d34c7ba7df5daa9b38b0ae820dba832401429"

#: The exact feature head independent FULL review 5000502119 examined, before the bounded
#: correction that review required. Bound so the register's own base-versus-head distinction can be
#: checked against a real commit rather than against prose.
REVIEWED_HEAD_SHA = "8ab773866c5959cd61a73dd48af197339c48754a"
#: This unit's branch, as the register's shared ``active_branch`` field records it.
BRANCH_NAME = "claude/xasset-0049-rebinding-ll6hzf"

#: THIS unit's own base. Bound separately from ``PR348_MERGE_SHA`` BY NAME so that a later unit
#: advancing one without the other is visible rather than silently absorbed. XASSET-0048 §F.2
#: makes the relationship an EQUALITY, which is asserted rather than assumed.
THIS_UNIT_BASE_SHA = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"

# ── RE-ANCHORED BY XASSET-0060 ──────────────────────────────────────────────────────────────
#
# XASSET-0057 authorized ONE post-parser-correction rebinding and XASSET-0060 is it. Every claim
# below about what THIS unit did is IMMUTABLE and stays exactly as strict; every claim that read
# the LIVE anchor as though it must still be this unit is re-anchored onto the successor, with
# this unit's own values retained as NEGATIVE pins so both ends stay bound. Nothing is relaxed
# into a subset test any future growth would satisfy.
SUCCESSOR_DECISION_ID = "XASSET-0060"
SUCCESSOR_REVIEWED_BASE_SHA = "301e79334876a4bda6e7b89a6156b34e8d38a605"
SUCCESSOR_LOAD_BEARING_COUNT = 25
SUCCESSOR_PULL_REQUEST = 361
#: XASSET-0060's own seven additions, named EXACTLY so this unit's own two stay an exact claim.
XASSET_0060_BOUNDARY_ADDITIONS = (
    "governance/decisions/"
    "XASSET-0053-endpoint-0001-formal-disposition-parser-contract-correction-authorization.md",
    "governance/decisions/"
    "XASSET-0055-endpoint-0001-formal-disposition-verdict-boundary-governance.md",
    "governance/decisions/XASSET-0056-endpoint-0001-formal-disposition-parser-correction.md",
    "governance/decisions/"
    "XASSET-0057-endpoint-0001-stage-1-post-parser-correction-rebinding-authorization.md",
    "governance/decisions/"
    "XASSET-0058-endpoint-0001-formal-disposition-parser-correction-authorization.md",
    "governance/decisions/XASSET-0059-endpoint-0001-formal-disposition-parser-correction.md",
    "governance/decisions/"
    "XASSET-0060-endpoint-0001-stage-1-post-parser-correction-operational-rebinding.md",
)

#: PR #348's lifecycle evidence, all seven conditions.
PR348_FULL_REVIEW = "4998661361"
PR348_CLEAN_DELTA_REVIEW = "4999458224"
PR348_PRINCIPAL_ACCEPTANCE = "5380255052"
PR348_POST_MERGE_VERIFICATION = "5380287468"
PR348_FINAL_CLOSURE = "5380368431"
PR348_MERGE_CI_RUN = "32571799154"
PR348_MERGE_CI_JOB = "97028166971"

# ── The superseded anchor: XASSET-0047 / PR #347, a CLOSED predecessor ───────────────────────
PR347_ACCEPTED_HEAD = "8ae0988d4c1ffc551e7fa0a1d1ee1edfa7a49a9e"
PR347_MERGE_SHA = "bb95ed26964b1bc7a2e230c76060fec82752efa1"
PR347_MERGE_BASE = "0b76c09f8d1aba01780b4f06fdd692f7393fbfd3"

#: The anchor as it stood at this unit's base -- the exact closed transition's OLD end.
ANCHOR_DECISION_AT_BASE = "XASSET-0047"
ANCHOR_PULL_REQUEST_AT_BASE = 347
ANCHOR_REVIEWED_BASE_AT_BASE = "0b76c09f8d1aba01780b4f06fdd692f7393fbfd3"
LOAD_BEARING_COUNT_AT_BASE = 16
LOAD_BEARING_COUNT_AFTER = 18

#: This unit's two boundary additions, named so they can be asserted EXACTLY as a set difference.
BOUNDARY_ADDITIONS = (AUTHORITY_RELPATH, DECISION_RELPATH)

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

#: Every path whose bytes this rebinding must NOT change, checked against this unit's own base.
#: Deliberately broader than ``LOAD_BEARING_RELPATHS``: a rebinding that quietly edited the
#: allocator or the holdings would be outside its grant even though those are not load-bearing.
FROZEN_AGAINST_BASE_RELPATHS = (
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    "level1_construction_universe_closure_validator.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
    "allocate.py",
    "margin_state.py",
    "levels.py",
    "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
    "governance/decisions/"
    "XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
    "governance/decisions/XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md",
    "governance/decisions/"
    "XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md",
    "governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md",
    "governance/decisions/"
    "XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md",
    "governance/decisions/"
    "XASSET-0044-endpoint-0001-stage-1-post-correction-operational-rebinding.md",
    "governance/decisions/"
    "XASSET-0045-endpoint-0001-stage-1-post-merge-ci-recovery-authorization.md",
    "governance/decisions/"
    "XASSET-0046-endpoint-0001-stage-1-post-merge-ci-recovery-reauthorization.md",
    "governance/decisions/"
    "XASSET-0047-endpoint-0001-stage-1-post-merge-ci-recovery-reconciliation.md",
    AUTHORITY_RELPATH,
)


# ======================================================================================
# Helpers -- immutable git facts only
# ======================================================================================


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _commit_exists(sha: str, repo_root: Path = ROOT) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=repo_root, capture_output=True, text=True,
    ).returncode == 0


def _range_is_present(*shas: str) -> bool:
    """Whether ANY of the named anchors is in this checkout.

    Deliberately ``any``, not ``all``. A checkout holding none of them is genuinely truncated and
    is an environment precondition; a checkout holding some but not all is a REFUSAL inside the
    proof, never a skip, so one unresolvable object cannot silence the whole thing.
    """
    return any(_commit_exists(sha) for sha in shas)


def _blob_at(commit: str, relpath: str) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", f"{commit}:{relpath}"],
        cwd=ROOT, capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _flat(text: str) -> str:
    """Collapse whitespace runs and drop blockquote markers, so an exact phrase match is
    insensitive to where hard-wrapped prose happens to break. Not a weakening: the full phrase
    must still be present, contiguously."""
    return re.sub(r"\s+", " ", text.replace("\n>", "\n")).strip()


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_flat(decision_text: str) -> str:
    return _flat(decision_text)


@pytest.fixture(scope="module")
def register_text() -> str:
    return (ROOT / REGISTER_RELPATH).read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def ws0014(register_text: str) -> dict:
    data = yaml.safe_load(register_text)
    return next(w for w in data["workstreams"] if w["id"] == "WS-0014")


# ======================================================================================
# 1 -- The base: EQUALITY is operative, descent is necessary and insufficient
# ======================================================================================


class TestBaseEqualityIsOperative:
    """``XASSET-0048`` §F.2, converted from prose into a decidable proposition.

    Its own independent review found the ancestry-only formulation defective and corrected it to
    equality BEFORE that decision was accepted. Prose corrections decay. These tests drive the
    rule -- including against a real synthetic later descendant -- and keep the superseded rule
    beside it, shown ACCEPTING what the corrected rule refuses.
    """

    def test_the_module_binds_this_units_base_by_equality(self):
        """RE-ANCHORED BY XASSET-0060, and bound at BOTH ends.

        THIS unit's base really was the XASSET-0048 merge, and that is immutable history: the
        constant carrying it is asserted exactly, unchanged. What moved is the LIVE anchor, and
        it moved because XASSET-0057 §F.2 WITHDREW the "base equals your own authorization's
        merge" rule -- §F.0 makes an intervening parser correction MANDATORY, and the two cannot
        both hold. The successor's own equality is asserted here on the rule that governs it.
        """
        assert A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA == THIS_UNIT_BASE_SHA
        assert A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA == PR348_MERGE_SHA
        assert A.PRIOR_STEP8_EQUIVALENT_MERGE_BASE == THIS_UNIT_BASE_SHA
        assert A.REVIEWED_BASE_SHA == SUCCESSOR_REVIEWED_BASE_SHA
        assert A.REVIEWED_BASE_SHA != THIS_UNIT_BASE_SHA
        assert A.REVIEWED_BASE_SHA == A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA

    def test_the_authorizing_merge_really_has_the_derived_identity(self):
        """§F.2 forbids ASSERTING this merge and requires DERIVING it. Derived here from the
        object store: ordered parents, and a merge tree byte-identical to the accepted head's."""
        if not _range_is_present(PR348_MERGE_SHA, PR348_ACCEPTED_HEAD, PR348_BASE_SHA):
            pytest.skip("PR #348's closed range is not present in this checkout")
        assert _commit_exists(PR348_MERGE_SHA)
        parents = _git("log", "-1", "--pretty=%P", PR348_MERGE_SHA).split()
        assert parents == [PR348_BASE_SHA, PR348_ACCEPTED_HEAD]
        assert _git("rev-parse", f"{PR348_MERGE_SHA}^{{tree}}") == PR348_MERGE_TREE
        assert _git("rev-parse", f"{PR348_ACCEPTED_HEAD}^{{tree}}") == PR348_MERGE_TREE

    def test_the_rule_accepts_the_bound_pair(self):
        """RE-ANCHORED BY XASSET-0060: the rule is unchanged and still accepts the pair IT
        governs, which is now driven with this unit's own historical values rather than with a
        live anchor that lawfully moved. The successor's own rule is exercised beside it."""
        assert A._verify_step8_equivalent_base_equality(
            THIS_UNIT_BASE_SHA, A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA, True
        ) == []
        assert A._verify_post_parser_correction_base_equality(
            A.REVIEWED_BASE_SHA, A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA, True
        ) == []
        # ... and the superseded pairing is now REFUSED, which is what "the rule moved" means.
        assert A._verify_step8_equivalent_base_equality(
            A.REVIEWED_BASE_SHA, A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA, True
        ) != []

    def test_the_rule_refuses_a_real_later_descendant_even_with_ancestry_granted(self):
        """THE MAJOR FINDING, reproduced against a REAL commit rather than a placeholder.

        A later commit on ``main`` genuinely descends from the authorizing merge. Under the
        superseded rule that was sufficient. Under the corrected rule it is refused, and the
        refusal survives ancestry being granted UNCONDITIONALLY -- which is the whole point: the
        defect was never that ancestry failed to hold, it was that ancestry was the wrong test.
        """
        if not _commit_exists(PR348_MERGE_SHA):
            pytest.skip("the authorizing merge is not present in this checkout")
        head = _git("rev-parse", "HEAD")
        if head == PR348_MERGE_SHA:
            pytest.skip("HEAD is the authorizing merge itself; no later descendant exists here")
        # A REAL descendant: this branch's own head descends from the authorizing merge.
        assert _git("merge-base", "--is-ancestor", PR348_MERGE_SHA, head) == ""
        errors = A._verify_step8_equivalent_base_equality(
            head, A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA, True
        )
        assert errors, "a later descendant must be refused"
        assert any("EQUALITY" in e for e in errors), errors
        assert any("descent alone never qualifies" in e for e in errors), errors

    def test_the_superseded_descent_only_rule_accepts_what_the_corrected_rule_refuses(self):
        """Retained beside the corrected rule and shown FAILING, so the correction is proved to
        be a real change in behaviour rather than a change in wording."""
        if not _commit_exists(PR348_MERGE_SHA):
            pytest.skip("the authorizing merge is not present in this checkout")
        head = _git("rev-parse", "HEAD")
        if head == PR348_MERGE_SHA:
            pytest.skip("HEAD is the authorizing merge itself")

        def superseded_descent_only_rule(base, authorizing_merge, descends):
            """The rule as XASSET-0048 first shipped it, before its own review corrected it."""
            return [] if descends else ["base does not descend from the authorizing merge"]

        assert superseded_descent_only_rule(
            head, A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA, True
        ) == []
        assert A._verify_step8_equivalent_base_equality(
            head, A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA, True
        ) != []

    def test_the_rule_refuses_an_unrelated_commit(self):
        errors = A._verify_step8_equivalent_base_equality(
            "0" * 40, A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA, True
        )
        assert any("EQUALITY" in e for e in errors), errors

    @pytest.mark.parametrize("bad", [None, "", "not-a-sha", "abc", 42, "0" * 39, "z" * 40])
    def test_the_rule_refuses_a_malformed_identity_at_either_end(self, bad):
        assert A._verify_step8_equivalent_base_equality(
            bad, A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA, True
        )
        assert A._verify_step8_equivalent_base_equality(A.REVIEWED_BASE_SHA, bad, True)

    def test_ancestry_remains_necessary(self):
        """Equality must not become a licence to drop the ancestry the predecessor rule carried."""
        errors = A._verify_step8_equivalent_base_equality(
            A.REVIEWED_BASE_SHA, A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA, False
        )
        assert any("ancestry remains NECESSARY" in e for e in errors), errors

    def test_an_unresolvable_ancestry_answer_is_not_itself_a_failure(self):
        """``None`` is the pre-merge case -- the rebinding merge does not exist yet. The
        surrounding verifier checks ancestry independently once a real merge exists.

        RE-ANCHORED BY XASSET-0060: driven with this unit's own historical pair, so the property
        stays proved about the rule rather than about whichever anchor is currently live.
        """
        assert A._verify_post_parser_correction_base_equality(
            A.REVIEWED_BASE_SHA, A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA, None
        ) == []
        assert A._verify_step8_equivalent_base_equality(
            THIS_UNIT_BASE_SHA, A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA, None
        ) == []
        # The live anchor's base is NOT this rule's subject any more, so an unresolvable ancestry
        # answer does not rescue it: the EQUALITY still fails, and that failure is the point.
        errors = A._verify_step8_equivalent_base_equality(
            A.REVIEWED_BASE_SHA, A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA, None
        )
        assert errors
        assert all("ancestry remains NECESSARY" not in e for e in errors), errors

    def test_the_rule_reads_no_external_source(self):
        """Pure and offline: it must not be silenceable by an unavailable git, GitHub, or clock.
        Proven structurally from the function's own AST, not from its docstring."""
        tree = ast.parse((ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8"))
        fn = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef)
            and n.name == "_verify_step8_equivalent_base_equality"
        )
        called = {
            node.func.attr for node in ast.walk(fn)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        for forbidden in ("run", "is_ancestor", "commit_parents", "now", "utcnow", "get"):
            assert forbidden not in called, forbidden

    def test_the_rule_takes_its_inputs_as_parameters_not_module_globals(self):
        """MUTATION PIN. A rule that read the globals directly could not be driven against a
        known-bad input at all, so every negative test above would be unwritable."""
        tree = ast.parse((ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8"))
        fn = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef)
            and n.name == "_verify_step8_equivalent_base_equality"
        )
        names = [a.arg for a in fn.args.args]
        assert names == [
            "reviewed_base", "authorizing_merge", "descends_from_authorizing_merge"
        ], names
        loaded = {
            n.id for n in ast.walk(fn) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
        }
        assert "REVIEWED_BASE_SHA" not in loaded
        assert "STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA" not in loaded


# ======================================================================================
# 2 -- Exact closed transitions, bound at BOTH ends
# ======================================================================================


class TestExactClosedTransitions:
    def test_the_anchor_decision_moved_and_both_ends_are_bound(self):
        # RE-ANCHORED BY XASSET-0060. THIS unit's move is immutable and stays fully asserted:
        # the predecessor it superseded is still bound, and its own identifier is still bound --
        # now as the PRIOR anchor, on the constant XASSET-0060 added for exactly that purpose.
        assert A.PRIOR_STEP8_EQUIVALENT_DECISION == DECISION_ID
        assert A.PRIOR_RECONCILIATION_DECISION == ANCHOR_DECISION_AT_BASE
        assert A.PRIOR_STEP8_EQUIVALENT_DECISION != ANCHOR_DECISION_AT_BASE
        assert A.AUTHORIZING_DECISION == SUCCESSOR_DECISION_ID
        assert A.AUTHORIZING_DECISION != DECISION_ID
        assert A.AUTHORIZING_DECISION != ANCHOR_DECISION_AT_BASE

    def test_the_anchor_pull_request_moved_and_both_ends_are_bound(self):
        # RE-ANCHORED BY XASSET-0060, on the same terms.
        assert A.PRIOR_STEP8_EQUIVALENT_PULL_REQUEST == THIS_PULL_REQUEST
        assert A.PRIOR_RECONCILIATION_PULL_REQUEST == ANCHOR_PULL_REQUEST_AT_BASE
        assert A.PRIOR_STEP8_EQUIVALENT_PULL_REQUEST != ANCHOR_PULL_REQUEST_AT_BASE
        assert A.AUTHORIZING_PULL_REQUEST != THIS_PULL_REQUEST
        assert A.AUTHORIZING_PULL_REQUEST != ANCHOR_PULL_REQUEST_AT_BASE

    def test_the_reviewed_base_moved_and_both_ends_are_bound(self):
        # RE-ANCHORED BY XASSET-0060, on the same terms: THIS unit's base is still bound exactly,
        # now on PRIOR_STEP8_EQUIVALENT_MERGE_BASE and STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA.
        assert A.PRIOR_STEP8_EQUIVALENT_MERGE_BASE == THIS_UNIT_BASE_SHA
        assert A.PRIOR_RECONCILIATION_MERGE_BASE == ANCHOR_REVIEWED_BASE_AT_BASE
        assert A.PRIOR_STEP8_EQUIVALENT_MERGE_BASE != ANCHOR_REVIEWED_BASE_AT_BASE
        assert A.REVIEWED_BASE_SHA == SUCCESSOR_REVIEWED_BASE_SHA
        assert A.REVIEWED_BASE_SHA != THIS_UNIT_BASE_SHA
        assert A.REVIEWED_BASE_SHA != ANCHOR_REVIEWED_BASE_AT_BASE
        assert A.RECOVERY_AUTHORIZING_MERGE_SHA == ANCHOR_REVIEWED_BASE_AT_BASE

    def test_the_old_end_really_was_the_old_end(self):
        """Read from the module's own bytes AT THE BASE, so the 'old' end is proved rather than
        recited from this suite's own constants."""
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        source = _git("show", f"{THIS_UNIT_BASE_SHA}:{AUTH_MODULE_RELPATH}")
        assert f'AUTHORIZING_DECISION = "{ANCHOR_DECISION_AT_BASE}"' in source
        assert f"AUTHORIZING_PULL_REQUEST = {ANCHOR_PULL_REQUEST_AT_BASE}" in source
        assert f'REVIEWED_BASE_SHA = "{ANCHOR_REVIEWED_BASE_AT_BASE}"' in source

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
        assert A.RECOVERY_AUTHORIZING_DECISION == "XASSET-0046"

    def test_the_execution_attempt_is_not_reminted(self):
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"


# ======================================================================================
# 3 -- Predecessor identities are PRESERVED, not overwritten
# ======================================================================================


class TestPredecessorIdentitiesArePreserved:
    def test_the_prior_anchors_identity_is_complete_and_real(self):
        assert A.PRIOR_RECONCILIATION_DECISION == "XASSET-0047"
        assert A.PRIOR_RECONCILIATION_PULL_REQUEST == 347
        assert A.PRIOR_RECONCILIATION_MERGE_SHA == PR347_MERGE_SHA
        assert A.PRIOR_RECONCILIATION_ACCEPTED_HEAD == PR347_ACCEPTED_HEAD
        assert A.PRIOR_RECONCILIATION_MERGE_BASE == PR347_MERGE_BASE

    def test_the_prior_anchors_merge_is_verifiable_from_git(self):
        if not _range_is_present(PR347_MERGE_SHA, PR347_ACCEPTED_HEAD):
            pytest.skip("PR #347's closed range is not present in this checkout")
        parents = _git("log", "-1", "--pretty=%P", PR347_MERGE_SHA).split()
        assert parents == [PR347_MERGE_BASE, PR347_ACCEPTED_HEAD]
        assert _git("rev-parse", f"{PR347_MERGE_SHA}^{{tree}}") == _git(
            "rev-parse", f"{PR347_ACCEPTED_HEAD}^{{tree}}"
        )

    def test_the_prior_anchor_was_unreachable_at_the_base(self):
        """THE REPRODUCTION. At this unit's own base, XASSET-0047's merge and accepted head
        appeared under NO constant: its identity was reachable only through the three values this
        unit moves. Preserving it is therefore mandatory, not decorative."""
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        source = _git("show", f"{THIS_UNIT_BASE_SHA}:{AUTH_MODULE_RELPATH}")
        assert PR347_MERGE_SHA not in source
        assert PR347_ACCEPTED_HEAD not in source
        # ... and it is reachable now.
        live = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert PR347_MERGE_SHA in live
        assert PR347_ACCEPTED_HEAD in live

    def test_the_prior_anchor_is_a_closed_predecessor_not_a_stopped_one(self):
        assert A.PRIOR_RECONCILIATION_DECISION not in A.PERMANENTLY_INEFFECTIVE_DECISIONS
        assert A.PRIOR_RECONCILIATION_PULL_REQUEST not in A.PERMANENTLY_INEFFECTIVE_PULL_REQUESTS

    def test_the_prior_anchor_family_is_not_folded_into_the_recovery_family(self):
        """``RECOVERY_AUTHORIZING_*`` names XASSET-0046, the decision that AUTHORIZED the
        reconciliation. XASSET-0047 is the reconciliation ITSELF. Different relationships."""
        assert A.RECOVERY_AUTHORIZING_DECISION != A.PRIOR_RECONCILIATION_DECISION
        assert A.RECOVERY_AUTHORIZING_PULL_REQUEST != A.PRIOR_RECONCILIATION_PULL_REQUEST
        assert A.RECOVERY_AUTHORIZING_MERGE_SHA != A.PRIOR_RECONCILIATION_MERGE_SHA

    def test_every_identity_family_is_mutually_distinct(self):
        """MUTATION PIN. Collapsing two families into one is the overloading XASSET-0037 §C named
        as the largest failure mode available to a rebinding."""
        merges = [
            A.PREDECESSOR_MERGE_SHA,
            A.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA,
            A.PACKAGE_AUTHORIZING_MERGE_SHA,
            A.EXECUTABLE_PACKAGE_MERGE_SHA,
            A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA,
            A.CORRECTION_AUTHORIZING_MERGE_SHA,
            A.CORRECTED_MODULE_MERGE_SHA,
            A.REBINDING_AUTHORIZING_MERGE_SHA,
            A.STOPPED_REBINDING_MERGE_SHA,
            A.STOPPED_RECOVERY_AUTHORIZATION_MERGE_SHA,
            A.RECOVERY_AUTHORIZING_MERGE_SHA,
            A.PRIOR_RECONCILIATION_MERGE_SHA,
            A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA,
        ]
        assert len(set(merges)) == len(merges)

    def test_the_step8_equivalent_authority_family_is_complete_and_real(self):
        assert A.STEP8_EQUIVALENT_AUTHORIZING_DECISION == "XASSET-0048"
        assert A.STEP8_EQUIVALENT_AUTHORIZING_PULL_REQUEST == 348
        assert A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA == PR348_MERGE_SHA
        assert A.STEP8_EQUIVALENT_AUTHORIZING_ACCEPTED_HEAD == PR348_ACCEPTED_HEAD
        assert A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_BASE == PR348_BASE_SHA


# ======================================================================================
# 4 -- The trust boundary grew ADDITIVELY, by direct membership
# ======================================================================================


class TestTrustBoundaryGrewAdditively:
    def test_the_set_grew_from_sixteen_to_eighteen(self):
        # RE-ANCHORED BY XASSET-0060, which added seven more under XASSET-0057 §F.7. THIS unit's
        # own growth -- sixteen to eighteen -- is immutable and is asserted exactly, from the base
        # tree, below. The LIVE size is pinned exactly at its current value and bound at both
        # ends, so neither a shrink back nor a further unexplained growth passes.
        assert len(A.LOAD_BEARING_RELPATHS) == SUCCESSOR_LOAD_BEARING_COUNT
        assert len(set(A.LOAD_BEARING_RELPATHS)) == SUCCESSOR_LOAD_BEARING_COUNT
        assert len(A.LOAD_BEARING_RELPATHS) != LOAD_BEARING_COUNT_AFTER
        assert len(A.LOAD_BEARING_RELPATHS) != LOAD_BEARING_COUNT_AT_BASE

    def test_the_additions_are_exactly_the_two_authority_chain_files(self):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        at_base = _load_bearing_declared_at(THIS_UNIT_BASE_SHA)
        assert len(at_base) == LOAD_BEARING_COUNT_AT_BASE
        # RE-ANCHORED BY XASSET-0060: THIS unit's two additions are still asserted EXACTLY, by
        # subtracting the successor's own seven BY NAME rather than relaxing to a subset test.
        additions = set(A.LOAD_BEARING_RELPATHS) - set(at_base)
        assert additions == set(BOUNDARY_ADDITIONS) | set(XASSET_0060_BOUNDARY_ADDITIONS)
        assert additions - set(XASSET_0060_BOUNDARY_ADDITIONS) == set(BOUNDARY_ADDITIONS)
        assert set(BOUNDARY_ADDITIONS).isdisjoint(XASSET_0060_BOUNDARY_ADDITIONS)
        assert len(XASSET_0060_BOUNDARY_ADDITIONS) == 7

    def test_nothing_was_removed(self):
        """Growth is additive. A path traded away is the defect this catches."""
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        assert set(_load_bearing_declared_at(THIS_UNIT_BASE_SHA)) <= set(A.LOAD_BEARING_RELPATHS)

    def test_the_predecessor_decision_files_are_all_retained(self):
        """A stopped lifecycle is not an invalidated one, and a superseded anchor is not a
        retired one."""
        for retained in (
            "governance/decisions/"
            "XASSET-0044-endpoint-0001-stage-1-post-correction-operational-rebinding.md",
            "governance/decisions/"
            "XASSET-0047-endpoint-0001-stage-1-post-merge-ci-recovery-reconciliation.md",
        ):
            assert retained in A.LOAD_BEARING_RELPATHS, retained

    def test_xasset_0045_is_still_deliberately_absent(self):
        """It authorizes nothing, so binding it would assert an authority relationship that does
        not exist. XASSET-0047 gave that reason and this unit does not disturb it."""
        assert not any("XASSET-0045" in p for p in A.LOAD_BEARING_RELPATHS)

    @pytest.mark.parametrize("relpath", BOUNDARY_ADDITIONS)
    def test_each_addition_is_a_real_file_bound_by_membership_not_citation(self, relpath):
        assert (ROOT / relpath).is_file(), relpath
        assert relpath in A.LOAD_BEARING_RELPATHS

    def test_neither_addition_was_load_bearing_at_the_base(self):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        at_base = _load_bearing_declared_at(THIS_UNIT_BASE_SHA)
        for relpath in BOUNDARY_ADDITIONS:
            assert relpath not in at_base, relpath

    def test_this_suite_is_not_load_bearing(self):
        """A test module may never enter the trust boundary."""
        assert SUITE_PATH.name not in A.LOAD_BEARING_RELPATHS

    def test_every_load_bearing_path_exists(self):
        for relative in A.LOAD_BEARING_RELPATHS:
            assert (ROOT / relative).is_file(), relative

    def test_no_results_artifact_is_load_bearing(self):
        assert "stage1_results" not in " ".join(A.LOAD_BEARING_RELPATHS).lower()


def _load_bearing_declared_at(commit: str) -> tuple[str, ...]:
    """The exact ``LOAD_BEARING_RELPATHS`` the production module DECLARED at a given commit.

    Parsed with ``ast`` and never imported or executed, so a historical module's code cannot run.
    Implicit string concatenation and module-level aliases are resolved from the SAME historical
    source, never from the live module.
    """
    source = subprocess.run(
        ["git", "show", f"{commit}:{AUTH_MODULE_RELPATH}"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    tree = ast.parse(source)

    def _module_string(name: str) -> str:
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets
            ):
                value = ast.literal_eval(node.value)
                assert isinstance(value, str), name
                return value
        raise AssertionError(f"{name} is not a module-level string assignment")

    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "LOAD_BEARING_RELPATHS" for t in node.targets
        ):
            assert isinstance(node.value, ast.Tuple)
            values: list[str] = []
            for element in node.value.elts:
                if isinstance(element, ast.Constant) and isinstance(element.value, str):
                    values.append(element.value)
                elif isinstance(element, ast.Name):
                    values.append(_module_string(element.id))
                else:  # pragma: no cover - defensive
                    raise AssertionError(f"unhandled element: {ast.dump(element)}")
            return tuple(values)
    raise AssertionError(f"LOAD_BEARING_RELPATHS not found at {commit}")


# ======================================================================================
# 5 -- Not one outcome-producing byte changed
# ======================================================================================


class TestNoOutcomeProducingByteChanged:
    def test_every_frozen_path_is_byte_identical_to_this_units_base(self):
        """Compared against an IMMUTABLE commit -- this unit's own base -- so the comparison
        neither depends on where ``HEAD`` points nor collapses to empty once this branch merges."""
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
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
        that consumes it still reports clean -- swap a genuinely sensitive path for any unchanged
        file and both the length check and the drift check stay green."""
        for required in (
            "level1_stage1_runner.py",
            "level1_stage1_result_validator.py",
            "level1_construction_universe_closure_validator.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "research/level1_endpoint_evidence/PROTOCOL_V1.md",
            "research/level1_endpoint_evidence/pre_registration.yaml",
            "targets.yaml",
            "holdings.yaml",
            "gates.yaml",
        ):
            assert required in FROZEN_AGAINST_BASE_RELPATHS, required

    def test_the_only_load_bearing_path_this_unit_changed_is_the_module_itself(self):
        """Every load-bearing path except the authorization module and this unit's own two
        additions must be byte-identical to the base."""
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        changed = []
        for relative in A.LOAD_BEARING_RELPATHS:
            # RE-ANCHORED BY XASSET-0060: its seven additions are likewise not paths THIS unit
            # bound, so they are skipped for the same reason this unit's own two are -- and their
            # identity is bound by XASSET-0060's own suite rather than left unchecked anywhere.
            if (
                relative == AUTH_MODULE_RELPATH
                or relative in BOUNDARY_ADDITIONS
                or relative in XASSET_0060_BOUNDARY_ADDITIONS
            ):
                continue
            at_base = _blob_at(THIS_UNIT_BASE_SHA, relative)
            assert at_base is not None, relative
            if _git("hash-object", relative) != at_base:
                changed.append(relative)
        assert changed == [], changed

    def test_the_universe_is_unchanged(self):
        assert A.CONSTRUCTION_UNIVERSE_SHA256 == UNIVERSE_SHA256
        assert A.CONSTRUCTION_COUNT == UNIVERSE_COUNT
        assert A.CONSTRUCTION_CELL_COUNT == UNIVERSE_CELL_COUNT

    def test_the_canonical_pins_still_match_the_live_canonical_files(self):
        for relative, pin in A.CANONICAL_PINS.items():
            live = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            assert live == pin, relative

    def test_the_canonical_pins_are_unchanged_from_the_base(self):
        """§F.7 determination: this rebinding amends no canonical byte, so the pins must not
        move -- and the refusal that enforces it must still be live."""
        assert A.CANONICAL_PINS == A.XASSET_0044_CANONICAL_PINS
        assert A._verify_recovery_lifecycle_anchor("0" * 40) == [] or not any(
            "canonical drift" in e for e in A._verify_recovery_lifecycle_anchor("0" * 40)
        )

    def test_the_canonical_drift_refusal_is_still_live(self, monkeypatch):
        drifted = dict(A.CANONICAL_PINS)
        drifted[A.CANONICAL_PROTOCOL_RELPATH] = "0" * 64
        monkeypatch.setattr(A, "CANONICAL_PINS", drifted)
        errors = A._verify_recovery_lifecycle_anchor("0" * 40)
        assert any("canonical drift" in e for e in errors), errors
        assert any("may not move a canonical byte" in e for e in errors), errors

    def test_the_outcome_producing_relpaths_are_all_load_bearing(self):
        for relative in A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS:
            assert relative in A.LOAD_BEARING_RELPATHS, relative
        assert A.OUTCOME_PRODUCING_DERIVATION_RELPATH in A.LOAD_BEARING_RELPATHS


# ======================================================================================
# 6 -- The two new refusals are independently required
# ======================================================================================


class TestTheNewRefusalsAreIndependentlyRequired:
    def test_an_anchor_still_naming_the_superseded_decision_is_refused(self, monkeypatch):
        monkeypatch.setattr(A, "AUTHORIZING_DECISION", A.PRIOR_RECONCILIATION_DECISION)
        errors = A._verify_recovery_lifecycle_anchor("0" * 40)
        assert any("PRIOR anchor this rebinding supersedes" in e for e in errors), errors

    def test_an_anchor_still_naming_the_superseded_pull_request_is_refused(self, monkeypatch):
        monkeypatch.setattr(A, "AUTHORIZING_PULL_REQUEST", A.PRIOR_RECONCILIATION_PULL_REQUEST)
        errors = A._verify_recovery_lifecycle_anchor("0" * 40)
        assert any("PRIOR anchor's own pull request" in e for e in errors), errors

    def test_an_anchor_naming_the_authorizing_decision_is_refused(self, monkeypatch):
        monkeypatch.setattr(A, "AUTHORIZING_DECISION", A.STEP8_EQUIVALENT_AUTHORIZING_DECISION)
        errors = A._verify_recovery_lifecycle_anchor("0" * 40)
        assert any("AUTHORIZED this rebinding, not the rebinding itself" in e for e in errors), (
            errors
        )

    def test_an_anchor_naming_the_authorizing_pull_request_is_refused(self, monkeypatch):
        monkeypatch.setattr(
            A, "AUTHORIZING_PULL_REQUEST", A.STEP8_EQUIVALENT_AUTHORIZING_PULL_REQUEST
        )
        errors = A._verify_recovery_lifecycle_anchor("0" * 40)
        assert any("the AUTHORIZING pull request" in e for e in errors), errors

    def test_the_pre_existing_refusals_are_all_retained(self, monkeypatch):
        monkeypatch.setattr(A, "AUTHORIZING_DECISION", "XASSET-0044")
        assert any(
            "permanently ineffective" in e for e in A._verify_recovery_lifecycle_anchor("0" * 40)
        )
        monkeypatch.undo()
        monkeypatch.setattr(A, "AUTHORIZING_PULL_REQUEST", 345)
        assert any(
            "lifecycle that stopped" in e for e in A._verify_recovery_lifecycle_anchor("0" * 40)
        )

    @pytest.mark.parametrize(
        "failed_merge",
        [
            "f5dedce1d1d3116ed8a6845c4447388c85a5414c",
            "2f8cdebe14925021171b9779453946be1f69b506",
        ],
    )
    def test_a_merge_with_failed_merge_commit_ci_is_still_refused(self, failed_merge):
        errors = A._verify_recovery_lifecycle_anchor(failed_merge)
        assert any("FAILED merge-commit CI run" in e for e in errors), errors
        assert any("immutable adverse history" in e for e in errors), errors

    def test_the_live_anchor_passes_every_refusal(self):
        assert A._verify_recovery_lifecycle_anchor("0" * 40) == []

    def test_the_anchor_check_reads_no_external_source(self):
        tree = ast.parse((ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8"))
        fn = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "_verify_recovery_lifecycle_anchor"
        )
        called = {
            node.func.attr for node in ast.walk(fn)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        for forbidden in ("run", "is_ancestor", "commit_parents", "now", "utcnow"):
            assert forbidden not in called, forbidden


# ======================================================================================
# 7 -- Adverse history is preserved
# ======================================================================================


class TestAdverseHistoryIsPreserved:
    def test_both_stopped_lifecycles_are_still_permanently_ineffective(self):
        assert A.STOPPED_REBINDING_DECISION in A.PERMANENTLY_INEFFECTIVE_DECISIONS
        assert A.STOPPED_RECOVERY_AUTHORIZATION_DECISION in A.PERMANENTLY_INEFFECTIVE_DECISIONS
        assert A.STOPPED_REBINDING_PULL_REQUEST in A.PERMANENTLY_INEFFECTIVE_PULL_REQUESTS
        assert (
            A.STOPPED_RECOVERY_AUTHORIZATION_PULL_REQUEST
            in A.PERMANENTLY_INEFFECTIVE_PULL_REQUESTS
        )

    def test_both_failed_runs_are_recorded_by_exact_identity(self):
        recorded = {(run, job, merge) for run, job, merge in A.FAILED_MERGE_COMMIT_CI_RUNS}
        assert (
            XASSET0044_FAILED_CI_RUN,
            XASSET0044_FAILED_CI_JOB,
            A.STOPPED_REBINDING_MERGE_SHA,
        ) in recorded
        assert (
            XASSET0045_FAILED_CI_RUN,
            XASSET0045_FAILED_CI_JOB,
            A.STOPPED_RECOVERY_AUTHORIZATION_MERGE_SHA,
        ) in recorded
        assert len(recorded) == 2

    def test_no_failed_run_is_ever_consulted_as_evidence_of_success(self, decision_flat):
        assert "immutable adverse history" in decision_flat
        assert "never re-run in place" in decision_flat

    def test_the_decision_does_not_relabel_either_stopped_lifecycle(self, decision_flat):
        assert "remain **not effective**" in decision_flat
        assert "remains **spent**" in decision_flat


# ======================================================================================
# 8 -- Nothing is armed
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

    def test_no_results_artifact_exists(self):
        assert list(ROOT.rglob("stage1_results.yaml")) == []


class TestZeroActivationAuthority:
    @pytest.mark.parametrize(
        "phrase",
        [
            "renewed readiness verification",
            "renewed drift verification",
            "generating, pre-staging, or validating any **attestation**",
            "**arming** Stage 1",
            "**claiming** or consuming any part of `ATTEMPT_1`",
            "evaluating any gate for any registered construction",
            "executing Stage 1, or performing any results work",
        ],
    )
    def test_each_withheld_action_is_withheld_in_terms(self, decision_flat, phrase):
        assert _flat(phrase) in decision_flat, phrase

    def test_the_decision_adds_zero_activation_authorizations(self, decision_flat):
        assert "**This decision adds ZERO activation authorizations.**" in decision_flat
        assert "No committed value in this repository" in decision_flat

    def test_the_reserved_results_pr_is_untouched(self, decision_flat):
        assert "**one, unspent.**" in decision_flat


# ======================================================================================
# 9 -- No historical proof moves
# ======================================================================================


class TestNoHistoricalProofMoves:
    """The defect that stopped PRs #344 and #345: a proof whose SUBJECT is closed history but
    whose EXPRESSION names a moving reference. Every historical claim in this suite is anchored to
    an immutable commit, and that is asserted structurally rather than promised in prose."""

    #: Functions in this module whose subject is immutable history.
    HISTORICAL_PROOF_FUNCTIONS = (
        "test_the_authorizing_merge_really_has_the_derived_identity",
        "test_the_old_end_really_was_the_old_end",
        "test_the_prior_anchors_merge_is_verifiable_from_git",
        "test_the_prior_anchor_was_unreachable_at_the_base",
        "test_the_additions_are_exactly_the_two_authority_chain_files",
        "test_nothing_was_removed",
        "test_neither_addition_was_load_bearing_at_the_base",
        "test_every_frozen_path_is_byte_identical_to_this_units_base",
        "test_the_only_load_bearing_path_this_unit_changed_is_the_module_itself",
    )

    def test_no_historical_proof_names_a_moving_reference(self):
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        by_name = {
            n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
        }
        for name in self.HISTORICAL_PROOF_FUNCTIONS:
            fn = by_name[name]
            literals = {
                n.value for n in ast.walk(fn)
                if isinstance(n, ast.Constant) and isinstance(n.value, str)
            }
            for moving in ("origin/main", "main", "HEAD~1", "@{upstream}"):
                assert moving not in literals, (name, moving)

    def test_the_declared_list_is_not_vacuous(self):
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        defined = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
        for name in self.HISTORICAL_PROOF_FUNCTIONS:
            assert name in defined, name
        assert len(self.HISTORICAL_PROOF_FUNCTIONS) >= 9

    def test_the_one_permitted_head_use_has_a_live_subject(self):
        """``HEAD`` appears exactly where the SUBJECT is live: constructing a real later
        descendant to prove the equality rule refuses one. That is a live fact by design."""
        # Read from the AST rather than the raw text, so this audit does not count its own
        # source line -- a self-counting scan is a vacuity hazard, not a proof.
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        auditor = "test_the_one_permitted_head_use_has_a_live_subject"
        uses = []
        for fn in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)):
            if fn.name == auditor:
                continue
            for call in (n for n in ast.walk(fn) if isinstance(n, ast.Call)):
                args = [
                    a.value for a in call.args
                    if isinstance(a, ast.Constant) and isinstance(a.value, str)
                ]
                if "HEAD" in args:
                    uses.append((fn.name, args))
        assert uses, "the descendant proof must really use HEAD"
        for name, args in uses:
            # Every HEAD use must be a read of a LIVE ref, never a historical anchor.
            assert args[0] in ("rev-parse", "merge-base"), (name, args)


# ======================================================================================
# 10 -- Catalog, register, and the bound pull-request number
# ======================================================================================


class TestCatalogAndRegisterSynchronisation:
    def test_the_catalog_row_exists_and_points_at_real_files(self):
        catalog = yaml.safe_load((ROOT / CATALOG_RELPATH).read_text(encoding="utf-8"))
        rows = [d for d in catalog["decisions"] if d["decision_id"] == DECISION_ID]
        assert len(rows) == 1
        row = rows[0]
        assert row["file"] == DECISION_RELPATH
        assert (ROOT / row["file"]).is_file()
        assert row["supporting_artifact"] == SUITE_PATH.name
        assert (ROOT / row["supporting_artifact"]).is_file()
        assert row["status"] == "Proposed"
        assert "XASSET-0048" in row["related_decisions"]

    def test_the_catalog_is_the_only_place_the_id_is_minted(self):
        """RE-ANCHORED BY XASSET-0050: the catalog is append-only, so "last row" names whichever
        decision was filed most recently, not this one forever. The invariant this test protects
        is that the id is minted EXACTLY ONCE and that this unit's row is present -- both of which
        survive a successor being appended after it."""
        catalog = yaml.safe_load((ROOT / CATALOG_RELPATH).read_text(encoding="utf-8"))
        ids = [d["decision_id"] for d in catalog["decisions"]]
        assert len(ids) == len(set(ids))
        assert DECISION_ID in ids
        assert ids.index(DECISION_ID) == len(ids) - 1 or ids[-1] > DECISION_ID

    def test_the_register_gate_exists_and_is_in_progress(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == REGISTER_GATE)
        assert gate["status"] == "in_progress"
        assert gate["pr"] == THIS_PULL_REQUEST

    def test_the_prior_units_gate_text_was_not_edited(self, register_text):
        """The XASSET-0048 gate is accepted history. Its confirmed merge is recorded by a NEW,
        additive gate rather than by rewriting what it said while it was live."""
        data = yaml.safe_load(register_text)
        ws = next(w for w in data["workstreams"] if w["id"] == "WS-0014")
        prior = next(
            g for g in ws["milestones"]
            if g["gate"] == "xasset0048-step8-equivalent-rebinding-authorization"
        )
        assert prior["status"] == "in_progress"
        assert prior["pr"] == 348

    def test_the_additive_post_merge_gate_records_the_prior_units_closure(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == PRIOR_UNIT_GATE)
        assert gate["status"] == "complete"
        assert gate["pr"] == 348
        for token in (
            PR348_ACCEPTED_HEAD, PR348_MERGE_SHA, PR348_MERGE_TREE,
            PR348_CLEAN_DELTA_REVIEW, PR348_MERGE_CI_RUN, PR348_MERGE_CI_JOB,
            PR348_PRINCIPAL_ACCEPTANCE, PR348_POST_MERGE_VERIFICATION, PR348_FINAL_CLOSURE,
        ):
            assert token in gate["description"], token

    def test_the_shared_live_fields_advanced(self, ws0014):
        """RE-ANCHORED BY XASSET-0050.

        These are WS-0014's SINGLE SHARED live self-reference fields. They advanced ONTO this
        unit while it was live, which is what the original assertion captured; they advance OFF
        it when a successor becomes live, which pinning them to this unit's own values forbade.
        This file already corrected exactly that error for the predecessor's suite -- "requiring
        them equal asserted that this unit is live forever" -- so the same correction is applied
        here rather than a new rule being invented.

        Both ends stay bound: while this unit is live the fields must be exactly its own, and once
        it is not, they must have moved strictly forward and never back onto any predecessor.
        """
        assert ws0014["last_verified_main_sha"] != PR347_MERGE_SHA
        if ws0014["active_pr"] == THIS_PULL_REQUEST:
            assert ws0014["last_verified_main_sha"] == THIS_UNIT_BASE_SHA
            assert ws0014["active_pr"] == A.AUTHORIZING_PULL_REQUEST
        else:
            # A successor is live. This unit's own merge is now what `main` points at, so the
            # shared field must have moved off this unit's BASE and onto something later.
            assert ws0014["last_verified_main_sha"] != THIS_UNIT_BASE_SHA
            active = ws0014["active_pr"]
            assert isinstance(active, int)
            if active < 0:
                live = [g for g in ws0014["milestones"] if g.get("pr") == active]
                assert live, "the register carries a sentinel active_pr that no gate claims"
                assert all(g["status"] == "in_progress" for g in live), live
            else:
                assert active > THIS_PULL_REQUEST

    def test_the_workstream_posture_is_unchanged(self, ws0014):
        assert ws0014["status"] == "proposed"
        assert ws0014["priority"] == "secondary"

    def test_exactly_zero_primary_workstreams(self, register_text):
        data = yaml.safe_load(register_text)
        assert [w["id"] for w in data["workstreams"] if w.get("priority") == "primary"] == []

    def test_the_register_records_this_units_module_identity(self, register_text):
        """This unit's OWN identity stays recorded; the LIVE one is not predicted.

        # RE-ANCHORED by XASSET-0057 §F.3 / XASSET-0058 §G.4 -- the XASSET-0059 parser
        # correction. The corrected module's identity is §F.3 **role 3**: "derived at the parser
        # correction's own merge ... never predicted here" and "never bound directly; it reaches
        # the register only through role 4's own derivation and proof". Recording the live digest
        # now would therefore VIOLATE the governing rule, so this test enforces that rule instead.
        # It is strictly harder to satisfy than the superseded form: that one passed on any
        # occurrence anywhere, this one fails if the value appears at all, AND still fails if the
        # register goes stale, because every previously recorded identity is still required.
        """
        flat = register_text.replace("\n", "").replace(" ", "")
        current = hashlib.sha256((ROOT / AUTH_MODULE_RELPATH).read_bytes()).hexdigest()
        this_unit = hashlib.sha256(
            subprocess.run(
                ["git", "show", f"{PR348_MERGE_SHA}:{AUTH_MODULE_RELPATH}"],
                cwd=ROOT, stdout=subprocess.PIPE, check=True,
            ).stdout
        ).hexdigest()
        assert this_unit in flat
        assert current not in flat
        assert current != this_unit


class TestTheRegistersOperativeProseAgreesWithItsStructuredFields:
    """MAJOR 1 of independent FULL review 5000502119, encoded so it cannot recur silently.

    ``XASSET-0048`` §E.7 requires synchronizing the ``WS-0014`` register. The structured fields
    (``active_branch``, ``active_pr``, the gate) were advanced, but the register's *operative*
    narrative fields -- ``next_action`` and ``blocker`` -- were not: their newest updates still
    named ``XASSET-0048`` as "the sole active mutation lane" and said the rebinding "remains
    unperformed and unauthorized". A future operator reading them would have concluded the exact
    opposite of what the same record's structured fields say.

    These fields are APPEND-ONLY dated logs, so the check has to be about the LATEST update rather
    than about the field as a whole -- an assertion over the whole string would be satisfied by the
    stale text and would therefore be vacuous. Each test below isolates the final dated update and
    asserts against that, and a companion test proves the older prose is still present.
    """

    #: The marker every dated update in these fields begins with.
    UPDATE_MARKER = "UPDATE, 2026-08-22"

    #: The dated block THIS unit appended. Once a successor appends its own, this unit's block is
    #: no longer the last one, so the tests below isolate it by its own opening phrase rather than
    #: by position. RE-ANCHORED BY XASSET-0050.
    OWN_BLOCK_OPENING = "UPDATE, 2026-08-22 (post-XASSET-0048 merge"

    @staticmethod
    def _latest_update(field_text: str) -> str:
        """The final dated update block, which is the operative one.

        Splitting on the marker rather than reading the whole field is what makes these
        assertions non-vacuous: the stale text sits in an EARLIER block and cannot satisfy them.
        """
        marker = TestTheRegistersOperativeProseAgreesWithItsStructuredFields.UPDATE_MARKER
        assert marker in field_text, "the field carries no dated update at all"
        return marker + field_text.rsplit(marker, 1)[1]

    @classmethod
    def _own_update(cls, field_text: str) -> str:
        """THIS unit's own dated block, isolated by its opening phrase.

        RE-ANCHORED BY XASSET-0050. These fields are append-only, so "the latest block" names
        whichever unit is currently live -- which was this one when the class was written and is
        a successor now. Re-pointing the checks at this unit's OWN block preserves each assertion
        in kind: it still verifies that what THIS unit wrote is present, correct and unrewritten.
        Whether the *newest* block correctly supersedes it is checked separately below, so the
        field ends up bound at BOTH ends rather than at neither.
        """
        assert cls.OWN_BLOCK_OPENING in field_text, "this unit's own dated block is missing"
        tail = cls.OWN_BLOCK_OPENING + field_text.split(cls.OWN_BLOCK_OPENING, 1)[1]
        nxt = tail.find(cls.UPDATE_MARKER, len(cls.OWN_BLOCK_OPENING))
        return tail if nxt == -1 else tail[:nxt]

    def test_the_fields_really_are_append_only_dated_logs(self, ws0014):
        """Non-vacuity guard for the splitting helper: if there were only one update block, the
        'latest' block would be the whole field and every assertion below would degrade into a
        whole-field test without anyone noticing."""
        for field in ("next_action", "blocker"):
            text = ws0014[field]
            assert text.count(self.UPDATE_MARKER) >= 2, field
            assert len(self._latest_update(text)) < len(text), field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_identifies_this_unit_as_the_active_lane(self, ws0014, field):
        latest = self._latest_update(ws0014[field])
        assert DECISION_ID in latest, field
        assert f"PR #{THIS_PULL_REQUEST}" in latest, field
        assert "SOLE ACTIVE" in latest, field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_records_the_authority_as_closed_and_effective(self, ws0014, field):
        # RE-ANCHORED BY XASSET-0050 onto THIS unit's own block; see ``_own_update``.
        latest = self._own_update(ws0014[field])
        assert "XASSET-0048" in latest, field
        assert "CLOSED" in latest, field
        assert "EFFECTIVE" in latest, field
        # Bound to the authority's own real identity, not merely to the words.
        assert PR348_MERGE_SHA in latest, field
        assert PR348_MERGE_CI_RUN in latest, field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_does_not_present_the_authority_as_the_active_lane(
        self, ws0014, field
    ):
        """The exact contradiction MAJOR 1 found: the stale text said XASSET-0048 was the sole
        active lane. The block must not say that of any decision but this one.

        RE-ANCHORED BY XASSET-0050 onto THIS unit's own block; see ``_own_update``.
        """
        latest = self._own_update(ws0014[field])
        # A superseded claim may legitimately be QUOTED in order to retire it -- that is the
        # honest way to supersede prose without deleting it. What must never happen is the
        # operative block ASSERTING it. So each stale phrase is required to be accompanied by
        # explicit supersession language, and the block's own active-lane claim must name THIS
        # unit. A blunt "phrase absent" test would have forbidden the honest form outright.
        supersession = (
            "SATISFIED AND SPENT",
            "SUPERSEDED BY EVENT",
            "no longer an active lane",
            "was true when written",
        )
        for stale in (
            "XASSET-0048, the sole active mutation lane",
            "XASSET-0048 is the sole active lane",
            "rebinding remains unperformed and unauthorized",
        ):
            if stale in latest:
                assert any(marker in latest for marker in supersession), (field, stale)
        # Whichever decision the operative block calls the sole active lane, it is THIS one.
        claims = ("SOLE ACTIVE LANE", "SOLE ACTIVE STEP-8-EQUIVALENT REBINDING LIFECYCLE")
        assert any(c in latest for c in claims), field
        for phrase in claims:
            if phrase in latest:
                head = latest[: latest.index(phrase)]
                assert head.rstrip().endswith(f"PR #{THIS_PULL_REQUEST} IS NOW THE") or (
                    head.rstrip().endswith(f"PR #{THIS_PULL_REQUEST} IS THE")
                ), (field, phrase, head[-60:])

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_latest_update_keeps_links_three_four_and_five_unauthorized(self, ws0014, field):
        # RE-ANCHORED BY XASSET-0050 onto THIS unit's own block; see ``_own_update``.
        latest = self._own_update(ws0014[field])
        assert "REMAIN SEPARATELY UNAUTHORIZED" in latest, field
        for link in ("readiness verification", "drift verification", "Step-11 authorization"):
            assert link in latest, (field, link)

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_older_dated_prose_is_preserved_not_rewritten(self, ws0014, field):
        """The correction APPENDS. Deleting or rewriting the superseded text would destroy an
        accurate dated record, which is exactly what the append-only convention exists to stop."""
        text = ws0014[field]
        # Each field carries its OWN earlier history, so the tokens differ per field. Asserting a
        # single shared list would have been satisfiable by whichever field happened to carry it.
        preserved_by_field = {
            "next_action": (
                "post-XASSET-0047 merge",
                "8ae0988d4c1ffc551e7fa0a1d1ee1edfa7a49a9e",
                "issuecomment-5376069596",
            ),
            "blocker": (
                "post-XASSET-0026 merge",
                "XASSET-0038",
                "XASSET-0044 and XASSET-0045 each permanently stopped",
            ),
        }
        for preserved in preserved_by_field[field]:
            assert preserved in text, (field, preserved)
        # ... and the superseded claims survive in the EARLIER block, just not the operative one.
        earlier = text[: text.rindex(self.UPDATE_MARKER)]
        assert "XASSET-0048" in earlier, field

    def test_the_gate_distinguishes_the_immutable_base_from_the_moving_head(self, ws0014):
        """The second half of MAJOR 1: the gate said main, origin/main, the base and ``HEAD``
        'are all' the base commit. That held only at the pre-authoring preflight; the offered head
        is a later commit by construction, because this unit's own commits advance it."""
        gate = next(g for g in ws0014["milestones"] if g["gate"] == REGISTER_GATE)
        description = gate["description"]
        # Targeted at the exact conflated CLAIM. "are all" appears legitimately elsewhere in this
        # gate -- the frozen outcome-producing paths "are all byte-identical to this pull request's
        # base" -- so a bare phrase ban would have failed on correct, unrelated text.
        assert "this branch's base and its HEAD are all" not in description
        assert "PRE-AUTHORING PREFLIGHT" in description
        assert "BASE REMAINS" in description
        assert THIS_UNIT_BASE_SHA in description
        # The offered feature head is named, and named as distinct from the base.
        assert REVIEWED_HEAD_SHA in description
        assert REVIEWED_HEAD_SHA != THIS_UNIT_BASE_SHA

    def test_the_gate_still_records_the_equality_rule_it_was_correcting(self, ws0014):
        """The correction narrows a temporal claim; it must not weaken §F.2 itself."""
        gate = next(g for g in ws0014["milestones"] if g["gate"] == REGISTER_GATE)
        description = gate["description"]
        assert "BASE BY EQUALITY, NOT DESCENT" in description
        assert "_verify_step8_equivalent_base_equality" in description

    def test_the_structured_fields_and_the_operative_prose_cannot_disagree(self, ws0014):
        """The single invariant MAJOR 1 reduces to, asserted directly.

        RE-ANCHORED BY XASSET-0050. ``active_pr`` and ``active_branch`` are WS-0014's SHARED live
        self-reference and move onto whichever unit is live, so pinning them to THIS unit's values
        asserted "this unit is live forever" -- the very error XASSET-0049 corrected elsewhere in
        this same file. What MAJOR 1 actually reduces to is that the structured fields and the
        OPERATIVE prose describe the same unit, whichever that is. That is asserted directly here,
        and this unit's own block is separately proved intact by ``_own_update``.
        """
        for field in ("next_action", "blocker"):
            own = self._own_update(ws0014[field])
            assert f"PR #{THIS_PULL_REQUEST}" in own, field
            latest = self._latest_update(ws0014[field])
            active = ws0014["active_pr"]
            if active == THIS_PULL_REQUEST:
                assert ws0014["active_branch"] == BRANCH_NAME
                assert f"PR #{active}" in latest, field
            else:
                # A successor is live. The operative block must name IT, and must record this
                # unit as finished rather than still active.
                assert ws0014["active_branch"] != BRANCH_NAME
                assert DECISION_ID in latest, field
                assert any(
                    m in latest for m in ("CLOSED", "SATISFIED AND SPENT", "SUPERSEDED BY EVENT")
                ), field


class TestTheNewestBlockSupersedesThisUnitRatherThanReviveIt:
    """ADDED BY XASSET-0050 -- the other end of the append-only invariant.

    ``_own_update`` proves this unit's block survives unrewritten. This class proves the NEWEST
    block, whichever successor wrote it, does not still present this finished unit as live work.
    Without it, re-anchoring the class above onto the own-block would have left the newest block
    unchecked entirely.
    """

    MARKER = TestTheRegistersOperativeProseAgreesWithItsStructuredFields.UPDATE_MARKER

    def _latest(self, text: str) -> str:
        assert self.MARKER in text
        return self.MARKER + text.rsplit(self.MARKER, 1)[1]

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_newest_block_does_not_call_this_finished_unit_the_active_lane(
        self, ws0014, field
    ):
        latest = self._latest(ws0014[field])
        if ws0014["active_pr"] == THIS_PULL_REQUEST:
            pytest.skip("this unit is still the live one")
        stale = f"{DECISION_ID} / PR #{THIS_PULL_REQUEST} IS THE SOLE ACTIVE"
        if stale in latest:
            assert any(
                m in latest for m in ("SUPERSEDED BY EVENT", "SATISFIED AND SPENT")
            ), field

    @pytest.mark.parametrize("field", ["next_action", "blocker"])
    def test_the_newest_block_records_this_units_lifecycle_as_closed(self, ws0014, field):
        latest = self._latest(ws0014[field])
        if ws0014["active_pr"] == THIS_PULL_REQUEST:
            pytest.skip("this unit is still the live one")
        assert DECISION_ID in latest, field
        assert "CLOSED" in latest and "EFFECTIVE" in latest, field


class TestTheBoundPullRequestNumber:
    def test_the_module_binds_the_number_github_actually_issued(self):
        """RE-ANCHORED BY XASSET-0060, bound at BOTH ends.

        THIS unit's number is immutable and is still bound exactly -- now on the constant
        XASSET-0060 added to preserve it. The LIVE anchor lawfully moved onto the successor, which
        is pinned positively, so a revert to this unit's number fails and so does a drift to any
        third value.
        """
        assert A.PRIOR_STEP8_EQUIVALENT_PULL_REQUEST == THIS_PULL_REQUEST
        assert A.AUTHORIZING_PULL_REQUEST == SUCCESSOR_PULL_REQUEST
        assert A.AUTHORIZING_PULL_REQUEST != THIS_PULL_REQUEST
        assert A.AUTHORIZING_PULL_REQUEST > THIS_PULL_REQUEST

    def test_the_sentinel_is_impossible_and_distinct_from_every_predecessors(self):
        """It cannot be positive, so it can never validate; and it is not 0 or -1, so it can
        never be mistaken for XASSET-0047's or XASSET-0048's own sentinel."""
        assert PULL_REQUEST_SENTINEL < 0
        assert PULL_REQUEST_SENTINEL not in (0, -1)

    def test_it_is_a_later_pull_request_than_every_predecessor_in_the_chain(self):
        """Monotonic by construction: GitHub issues numbers in order, so a number at or below any
        predecessor's would mean the constant was copied rather than read back."""
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
            A.PRIOR_RECONCILIATION_PULL_REQUEST,
            A.STEP8_EQUIVALENT_AUTHORIZING_PULL_REQUEST,
        ):
            assert A.AUTHORIZING_PULL_REQUEST > predecessor, predecessor

    def test_the_register_and_the_module_agree(self, ws0014):
        """RE-ANCHORED BY XASSET-0050.

        Equality held only while a REBINDING unit was live -- a rebinding binds its own number
        into the module, so the two coincided. ``XASSET-0050`` is a DESIGN-ONLY authorization: it
        changes no module constant, so the shared ``active_pr`` moves onto it while
        ``AUTHORIZING_PULL_REQUEST`` correctly stays on the last unit that actually rebound.
        Equality would assert "a rebinding is always live", which is false. The invariant
        underneath -- the shared field is never BEHIND the module's bound number, which is what a
        revert to finished work would look like -- is what is asserted, with the successor's
        sentinel window checked for consistency instead of skipped.
        """
        active = ws0014["active_pr"]
        assert isinstance(active, int)
        if active < 0:
            live = [g for g in ws0014["milestones"] if g.get("pr") == active]
            assert live, "the register carries a sentinel active_pr that no gate claims"
            assert all(g["status"] == "in_progress" for g in live), live
        else:
            assert active >= A.AUTHORIZING_PULL_REQUEST


# ======================================================================================
# 11 -- The decision's own operative claims
# ======================================================================================


class TestTheDecisionsOperativeClaims:
    @pytest.mark.parametrize(
        "phrase",
        [
            "STEP_8_EQUIVALENT_REBINDING_PERFORMED",
            "**Step 8 is not re-consumed.**",
            "equality, derived from the completed lifecycle and proved from the object store",
            "**No intervening byte is absorbed by descent**",
            "This unit changes not one outcome-producing byte.",
            "**This unit determines that it requires none, and amends neither canonical artifact.**",
            "Performing this rebinding authorizes **nothing further**",
            "Stage 1 remains **UNARMED** and **NOT EXECUTABLE**",
        ],
    )
    def test_each_operative_claim_is_present(self, decision_flat, phrase):
        assert _flat(phrase) in decision_flat, phrase

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
        # ADVANCED BY XASSET-0056: this declaration is accepted merged history describing the
        # module AS THIS UNIT LEFT IT. The single replacement parser-correction implementation
        # XASSET-0055 §H authorized lawfully changed that byte, so the declaration must now no
        # longer match the LIVE module, and asserting that inequality is what proves the
        # correction really landed. The declaration is NOT re-pinned -- this filing performs no
        # rebinding -- and the value it still declares is asserted EXACTLY, so nothing is
        # relaxed to a mere "differs".
        assert tokens[0] == "4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541"
        assert tokens[0] != hashlib.sha256(
            (ROOT / AUTH_MODULE_RELPATH).read_bytes()
        ).hexdigest()

    def test_the_decision_names_no_predicted_future_identity(self, decision_text):
        """This unit may cite CLOSED history freely -- including its own base, which is
        XASSET-0048's merge -- but must not name a commit that does not yet exist."""
        known = {
            PR348_BASE_SHA, PR348_FIRST_REVIEWED_HEAD, PR348_ACCEPTED_HEAD, PR348_MERGE_SHA,
            PR348_MERGE_TREE, THIS_UNIT_BASE_SHA,
            PR347_ACCEPTED_HEAD, PR347_MERGE_SHA, PR347_MERGE_BASE,
            "f5dedce1d1d3116ed8a6845c4447388c85a5414c",
            "2f8cdebe14925021171b9779453946be1f69b506",
            # The authorization module's own BLOB identity at this unit's base, cited in the
            # preflight table. A blob, not a commit, and closed history either way.
            "b23d762ff1f9f4c87fb1475741d61e1b49d47625",
        }
        found = set(re.findall(r"\b[0-9a-f]{40}\b", decision_text))
        assert found - known == set(), found - known
        # Every 40-hex identity this decision names must already EXIST in the object store, as a
        # commit or as a blob. A predicted future identity would resolve to neither.
        for sha in found:
            if not _range_is_present(*known):
                pytest.skip("this checkout is truncated")
            exists = subprocess.run(
                ["git", "cat-file", "-e", sha], cwd=ROOT, capture_output=True,
            ).returncode == 0
            assert exists, sha

    def test_the_decision_records_the_boundary_transition_at_both_ends(self, decision_flat):
        assert "| `LOAD_BEARING_RELPATHS` | **16** | **18** — additive only" in decision_flat

    def test_the_decision_states_its_own_effectivity_as_seven_conjunctive_conditions(
        self, decision_flat
    ):
        assert "**None is individually sufficient.**" in decision_flat
        assert "successful merge-commit CI whose `head_sha` is the exact merge SHA" in (
            decision_flat
        )

    def test_the_decision_does_not_disclaim_its_own_attainability(self, decision_flat):
        """The deadlock XASSET-0045 shipped at its first reviewed head, refused in terms."""
        assert "can attain both green PR-head and green merge-commit CI" in decision_flat


# ======================================================================================
# 12 -- Nothing outside this unit's grant was touched
# ======================================================================================


class TestNoProtectedByteWasTouched:
    @pytest.mark.parametrize(
        "relpath",
        [
            "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
            "allocate.py", "margin_state.py", "levels.py",
        ],
    )
    def test_protected_path_is_unchanged_against_the_base(self, relpath):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        at_base = _blob_at(THIS_UNIT_BASE_SHA, relpath)
        assert at_base is not None, relpath
        assert _git("hash-object", relpath) == at_base, relpath

    def test_no_risk_lane_boundary_path_is_referenced(self):
        # The token appears only in this module's own DISCLAIMERS -- the header docstring and
        # this test's own name and body -- never as a path that is opened, listed, or globbed.
        source = SUITE_PATH.read_text(encoding="utf-8")
        assert "risk_lane_boundary" in source, "the disclaimer must actually be present"
        tree = ast.parse(source)
        auditor = "test_no_risk_lane_boundary_path_is_referenced"
        offenders = []
        for fn in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)):
            if fn.name == auditor:
                continue  # this audit names the token to look for it; that is not a reference
            for node in ast.walk(fn):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    # Nothing outside this audit may name a protected-result token at all --
                    # not the lane boundary, not a results directory, not the RISK study.
                    for forbidden in ("risk_lane_boundary", "results/", "RISK-0001"):
                        if forbidden in node.value:
                            offenders.append((fn.name, forbidden, node.value[:60]))
        assert offenders == [], offenders

    def test_no_outcome_producing_module_is_imported_here(self):
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        for forbidden in (
            "level1_stage1_runner",
            "level1_stage1_result_validator",
            "level1_construction_universe_closure_validator",
        ):
            assert forbidden not in imported, forbidden
