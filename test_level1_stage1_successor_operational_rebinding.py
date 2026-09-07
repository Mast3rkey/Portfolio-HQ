"""Adversarial tests for the XASSET-0037 successor operational rebinding (XASSET-0030 §G.B step 8).

Each test pins an authorized boundary AND its nearest plausible overreach. The suite is built to
answer four questions that a rebinding, more than any other unit, can get quietly wrong:

  1. Can the OBSOLETE XASSET-0029 lifecycle still authorize the CURRENT package? It must not.
  2. Does the successor bind the EXACT reviewed base, accepted head, ordered merge parents, zero
     merge drift, exact pull-request identity, final clean review, principal acceptance, post-merge
     verification, exact-merge CI, ancestry, canonical pins, universe identity, and EVERY
     load-bearing byte? Removing any one must fail closed.
  3. Does missing, stale, adverse, mismatched, unreachable, or post-review-drift evidence fail
     CLOSED rather than being accepted or silently ignored?
  4. Can any committed value -- boolean or otherwise -- authorize execution, or any attestation
     validate before the successor lifecycle actually closes? Both must be impossible.

NO STAGE-1 EXECUTION OCCURS IN THIS FILE. No gate is evaluated for any registered construction, no
disposition is composed, no results document is produced, and no data is acquired. Every lane
record is written to a pytest ``tmp_path``; the REAL authorization root is never created, opened,
claimed, completed, or consumed, and dedicated tests assert that directly.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest
import yaml

import level1_construction_universe_closure_validator as CU
import level1_endpoint_evidence_preregistration_validator as PREREG
import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
DECISION = ROOT / (
    "governance/decisions/XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md"
)
PROTOCOL = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
PREREG_PATH = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"

FROZEN_UNIVERSE_SHA256 = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"

#: The module whose imported derivation surface MAJOR 1 (review 4955010993) requires be bound.
DERIVATION_RELPATH = "level1_endpoint_evidence_preregistration_validator.py"
DERIVATION_SOURCE = (ROOT / DERIVATION_RELPATH).read_text(encoding="utf-8")

#: The ACCEPTED EXECUTABLE-PACKAGE bytes of that module, read from the git object store. The
#: exact-transition model distinguishes the two package anchors from the three successor anchors,
#: so the stand-in git source must serve the true blob at each rather than one blob everywhere.
PACKAGE_SOURCE = subprocess.run(
    ["git", "show", f"{A.EXECUTABLE_PACKAGE_MERGE_SHA}:{DERIVATION_RELPATH}"],
    capture_output=True, cwd=str(ROOT), timeout=120, check=True,
).stdout.decode("utf-8")


#: The two OUTCOME-DERIVING consumers whose use of the derivation module defines the direct seed
#: surface. Held as test-local literals on purpose. Reading them from
#: ``A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS`` would let a production declaration be its own
#: oracle -- and, concretely, MAJOR 1's correction expanded that tuple to a third module, which
#: silently changed what this helper measured (18 -> 22 symbols) even though neither consumer had
#: changed. The seed surface is a property of these two consumers, so it is named here directly.
OUTCOME_DERIVING_CONSUMER_RELPATHS = (
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
)


def _independently_derived_seed_symbols(
    consumers: tuple[str, ...] = OUTCOME_DERIVING_CONSUMER_RELPATHS,
) -> set[str]:
    """Re-derive the outcome-producing seed set from the CONSUMERS' own source, by AST.

    Deliberately derived from the CONSUMERS rather than from any production declaration: the
    review's standing requirement is that a declaration must never be its own oracle. This walks
    ``level1_stage1_runner.py`` and ``level1_stage1_result_validator.py``, finds whatever alias each
    binds the derivation module to, and collects every attribute actually accessed through it. If a
    future edit starts consuming a new derivation symbol without declaring it, the equality
    assertion below fails.
    """
    import ast

    found: set[str] = set()
    for relative in consumers:
        tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
        aliases = {
            (entry.asname or entry.name)
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for entry in node.names
            if entry.name == "level1_endpoint_evidence_preregistration_validator"
        }
        assert aliases, f"{relative} does not import the derivation module"
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id in aliases
            ):
                found.add(node.attr)
    return found

#: The nine paths the XASSET-0036 executable package bound. XASSET-0037 removes none of them.
PACKAGE_LOAD_BEARING = (
    "level1_stage1_execution_authorization.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_construction_universe_closure_validator.py",
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
    "governance/decisions/XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
)

# Synthetic successor identities. They stand in for the real post-merge facts, which do not exist
# until XASSET-0037 has itself merged.
HEAD = "c" * 40
MERGE = "d" * 40
BASE = A.REVIEWED_BASE_SHA
REVIEW_ID = "4970000001"
ACCEPT_ID = "5970000001"
VERIFY_ID = "5970000002"
CLOSURE_ID = "5970000003"
RUN_ID = "3200000001"
JOB_ID = "9600000001"
REVIEWER_LOGIN = "independent-reviewer"
PRINCIPAL_LOGIN = A.PRINCIPAL_ACCOUNT_LOGIN
PR_URL = (
    f"https://api.github.com/repos/{A.REPOSITORY_IDENTITY}/issues/{A.AUTHORIZING_PULL_REQUEST}"
)


class FakeGit:
    """Stands in for the local git object store, answering only for commits that 'exist'."""

    def __init__(self, **overrides):
        self.parents = {
            MERGE: (BASE, HEAD),
            A.PREDECESSOR_MERGE_SHA: (
                A.PREDECESSOR_MERGE_BASE,
                A.PREDECESSOR_ACCEPTED_HEAD,
            ),
            A.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA: (
                A.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_BASE,
                A.HISTORICAL_OPERATIONAL_AUTHORIZATION_ACCEPTED_HEAD,
            ),
            A.PACKAGE_AUTHORIZING_MERGE_SHA: ("e" * 40, "f" * 40),
            A.EXECUTABLE_PACKAGE_MERGE_SHA: (
                A.EXECUTABLE_PACKAGE_MERGE_BASE,
                A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
            ),
            # EXTENDED BY XASSET-0044: the post-correction rebinding verifies four further merges
            # from git, so the stand-in vouches for each rather than letting an unknown anchor pass.
            A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA: (
                A.PRIOR_SUCCESSOR_REBINDING_MERGE_BASE,
                A.PRIOR_SUCCESSOR_REBINDING_ACCEPTED_HEAD,
            ),
            # AMENDED BY review 4986931575 MAJOR 1: PR #341's base and accepted head are now
            # BOUND, so its exact parent order and merge-tree identity are actually verified.
            A.CORRECTION_AUTHORIZING_MERGE_SHA: (
                A.CORRECTION_AUTHORIZING_MERGE_BASE,
                A.CORRECTION_AUTHORIZING_ACCEPTED_HEAD,
            ),
            A.CORRECTED_MODULE_MERGE_SHA: (
                A.CORRECTED_MODULE_MERGE_BASE,
                A.CORRECTED_MODULE_ACCEPTED_HEAD,
            ),
            A.REBINDING_AUTHORIZING_MERGE_SHA: (
                A.REBINDING_AUTHORIZING_MERGE_BASE,
                A.REBINDING_AUTHORIZING_ACCEPTED_HEAD,
            ),
            # EXTENDED BY XASSET-0047. The recovery verifies THREE further merges from git --
            # its own authority (XASSET-0046 / PR #346) and the two STOPPED lifecycles it
            # supersedes as the anchor (XASSET-0044 / PR #344 and XASSET-0045 / PR #345) -- so an
            # honest stand-in vouches for each separately rather than letting an unknown anchor
            # pass. These are the REAL identities, so the fixture agrees with the object store.
            # Serving the stopped merges here is NOT treating them as effective: the module
            # verifies them as history and refuses them as authority, and both facts are proven.
            A.RECOVERY_AUTHORIZING_MERGE_SHA: (
                A.RECOVERY_AUTHORIZING_MERGE_BASE,
                A.RECOVERY_AUTHORIZING_ACCEPTED_HEAD,
            ),
            A.STOPPED_REBINDING_MERGE_SHA: (
                A.STOPPED_REBINDING_MERGE_BASE,
                A.STOPPED_REBINDING_ACCEPTED_HEAD,
            ),
            A.STOPPED_RECOVERY_AUTHORIZATION_MERGE_SHA: (
                A.STOPPED_RECOVERY_AUTHORIZATION_MERGE_BASE,
                A.STOPPED_RECOVERY_AUTHORIZATION_ACCEPTED_HEAD,
            ),
            # EXTENDED BY XASSET-0049. The step-8-EQUIVALENT rebinding verifies TWO further
            # merges from git -- the PRIOR ANCHOR it supersedes (XASSET-0047 / PR #347, a CLOSED
            # predecessor) and its own AUTHORITY (XASSET-0048 / PR #348) -- so an honest stand-in
            # vouches for each separately rather than letting an unknown anchor pass.
            A.PRIOR_RECONCILIATION_MERGE_SHA: (
                A.PRIOR_RECONCILIATION_MERGE_BASE,
                A.PRIOR_RECONCILIATION_ACCEPTED_HEAD,
            ),
            A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA: (
                A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_BASE,
                A.STEP8_EQUIVALENT_AUTHORIZING_ACCEPTED_HEAD,
            ),
            # EXTENDED BY XASSET-0060. The post-parser-correction rebinding verifies FOUR further
            # merges from git -- the PRIOR ANCHOR it supersedes (XASSET-0049 / PR #349, a CLOSED
            # predecessor, not a stopped one), its own AUTHORITY (XASSET-0057 / PR #358), and the
            # TWO prerequisite lifecycles XASSET-0057 SS-F.0.3 makes conjunctive: Lifecycle A
            # (XASSET-0058 / PR #359) and Lifecycle B (XASSET-0059 / PR #360), whose B5 merge this
            # unit's base must EQUAL. An honest stand-in vouches for each separately rather than
            # letting an unknown anchor pass. These are the REAL identities, so the fixture agrees
            # with the object store.
            A.PRIOR_STEP8_EQUIVALENT_MERGE_SHA: (
                A.PRIOR_STEP8_EQUIVALENT_MERGE_BASE,
                A.PRIOR_STEP8_EQUIVALENT_ACCEPTED_HEAD,
            ),
            A.POST_PARSER_CORRECTION_AUTHORIZING_MERGE_SHA: (
                A.POST_PARSER_CORRECTION_AUTHORIZING_MERGE_BASE,
                A.POST_PARSER_CORRECTION_AUTHORIZING_ACCEPTED_HEAD,
            ),
            A.PARSER_CORRECTION_AUTHORIZING_MERGE_SHA: (
                A.PARSER_CORRECTION_AUTHORIZING_MERGE_BASE,
                A.PARSER_CORRECTION_AUTHORIZING_ACCEPTED_HEAD,
            ),
            A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA: (
                A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_BASE,
                A.PARSER_CORRECTION_IMPLEMENTATION_ACCEPTED_HEAD,
            ),
        }
        self.blobs = {}
        for rel in A.LOAD_BEARING_RELPATHS:
            digest = A.sha256_file(ROOT / rel)
            # Zero merge drift: reviewed head and merge carry identical bytes.
            self.blobs[(MERGE, rel)] = digest
            self.blobs[(HEAD, rel)] = digest
        # The outcome-producing bytes also exist, unchanged, in the accepted package.
        for rel in A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS:
            digest = A.sha256_file(ROOT / rel)
            self.blobs[(A.EXECUTABLE_PACKAGE_MERGE_SHA, rel)] = digest
            self.blobs[(A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, rel)] = digest
        self.trees = {
            MERGE: "t" * 40,
            HEAD: "t" * 40,
            A.EXECUTABLE_PACKAGE_MERGE_SHA: "p" * 40,
            A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD: "p" * 40,
            # XASSET-0044: each inherited merge's tree equals its accepted head's tree.
            A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA: "r" * 40,
            A.PRIOR_SUCCESSOR_REBINDING_ACCEPTED_HEAD: "r" * 40,
            A.CORRECTED_MODULE_MERGE_SHA: "c" * 40,
            A.CORRECTED_MODULE_ACCEPTED_HEAD: "c" * 40,
            A.REBINDING_AUTHORIZING_MERGE_SHA: "a" * 39 + "z",
            A.REBINDING_AUTHORIZING_ACCEPTED_HEAD: "a" * 39 + "z",
            # XASSET-0047: each added merge's tree equals its accepted head's tree, which is
            # exactly the zero-merge-drift property the module PROVES rather than assumes. Three
            # DISTINCT synthetic trees, so a swap between the three new entries is still caught.
            A.RECOVERY_AUTHORIZING_MERGE_SHA: "6" * 40,
            A.RECOVERY_AUTHORIZING_ACCEPTED_HEAD: "6" * 40,
            A.STOPPED_REBINDING_MERGE_SHA: "7" * 40,
            A.STOPPED_REBINDING_ACCEPTED_HEAD: "7" * 40,
            A.STOPPED_RECOVERY_AUTHORIZATION_MERGE_SHA: "8" * 40,
            A.STOPPED_RECOVERY_AUTHORIZATION_ACCEPTED_HEAD: "8" * 40,
            A.CORRECTION_AUTHORIZING_MERGE_SHA: "4" * 40,
            A.CORRECTION_AUTHORIZING_ACCEPTED_HEAD: "4" * 40,
            # XASSET-0049: each added merge's tree equals its accepted head's tree, which is the
            # zero-merge-drift property the module PROVES. TWO DISTINCT synthetic trees, so a
            # swap between the two new entries is still caught.
            A.PRIOR_RECONCILIATION_MERGE_SHA: "9" * 40,
            A.PRIOR_RECONCILIATION_ACCEPTED_HEAD: "9" * 40,
            A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA: "b" * 40,
            A.STEP8_EQUIVALENT_AUTHORIZING_ACCEPTED_HEAD: "b" * 40,
            # XASSET-0060: each added merge's tree equals its accepted head's tree, which is the
            # zero-merge-drift property the module PROVES rather than assumes. FOUR DISTINCT
            # synthetic trees, so a swap between any two of the four new entries is still caught.
            A.PRIOR_STEP8_EQUIVALENT_MERGE_SHA: "d" * 40,
            A.PRIOR_STEP8_EQUIVALENT_ACCEPTED_HEAD: "d" * 40,
            A.POST_PARSER_CORRECTION_AUTHORIZING_MERGE_SHA: "e" * 40,
            A.POST_PARSER_CORRECTION_AUTHORIZING_ACCEPTED_HEAD: "e" * 40,
            A.PARSER_CORRECTION_AUTHORIZING_MERGE_SHA: "f" * 40,
            A.PARSER_CORRECTION_AUTHORIZING_ACCEPTED_HEAD: "f" * 40,
            A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA: "5" * 40,
            A.PARSER_CORRECTION_IMPLEMENTATION_ACCEPTED_HEAD: "5" * 40,
        }
        # The exact transition needs blob TEXT, not a digest, and distinguishes the anchors: the
        # two PACKAGE anchors carry the accepted package bytes and the successor anchors carry
        # the reviewed successor bytes. The default posture is therefore the TRUE one, and each
        # negative test perturbs exactly one anchor.
        # EXTENDED BY XASSET-0044: the chain is package -> successor -> rebound, so the accepted
        # SUCCESSOR bytes now live at XASSET-0037's own anchors and the working tree carries the
        # REBOUND bytes. ``DERIVATION_SOURCE`` is the live file, which is the rebound blob.
        self.texts = {
            (MERGE, DERIVATION_RELPATH): DERIVATION_SOURCE,
            (HEAD, DERIVATION_RELPATH): DERIVATION_SOURCE,
            (A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA,
             DERIVATION_RELPATH): _successor_blob().decode("utf-8"),
            (A.PRIOR_SUCCESSOR_REBINDING_ACCEPTED_HEAD,
             DERIVATION_RELPATH): _successor_blob().decode("utf-8"),
            (A.EXECUTABLE_PACKAGE_MERGE_SHA, DERIVATION_RELPATH): PACKAGE_SOURCE,
            (A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, DERIVATION_RELPATH): PACKAGE_SOURCE,
        }
        self._head = MERGE
        self._ancestor = True
        self.__dict__.update(overrides)

    def blob_text_at(self, commit, relpath):
        return self.texts.get((commit, relpath))

    def commit_parents(self, sha):
        return self.parents.get(sha)

    def commit_tree(self, sha):
        return self.trees.get(sha)

    def is_ancestor(self, ancestor, descendant):
        return self._ancestor

    def blob_sha256_at(self, commit, relpath):
        return self.blobs.get((commit, relpath))

    def head(self):
        return self._head


class FakeGovernance:
    """Stands in for GitHub governance metadata. Unknown ids simply do not exist."""

    def __init__(self, **overrides):
        self.pulls = {
            A.AUTHORIZING_PULL_REQUEST: {
                "base": {"repo": {"full_name": A.REPOSITORY_IDENTITY}},
                "head": {"sha": HEAD},
                "merged": True,
                "merge_commit_sha": MERGE,
                "merged_at": "2026-08-17T12:00:00Z",
            }
        }
        self.review_records = {
            REVIEW_ID: {
                "commit_id": HEAD,
                "id": REVIEW_ID,
                "body": f"FORMAL DISPOSITION: {A.APPROVING_REVIEW_DISPOSITION} — 0 BLOCKING",
                "user": {"login": REVIEWER_LOGIN},
                "state": "COMMENTED",
                "submitted_at": "2026-08-17T10:00:00Z",
                "html_url": f"{PR_URL}#pullrequestreview-{REVIEW_ID}",
            }
        }
        self.comments = {
            ACCEPT_ID: {
                "body": (
                    f"Principal acceptance at exact head `{HEAD}`, relying on independent review "
                    f"{REVIEW_ID}."
                ),
                "issue_url": PR_URL,
                "created_at": "2026-08-17T11:00:00Z",
                "user": {"login": PRINCIPAL_LOGIN},
            },
            VERIFY_ID: {
                "body": f"Post-merge verification for merge `{MERGE}`.",
                "issue_url": PR_URL,
                "created_at": "2026-08-17T13:00:00Z",
                "user": {"login": PRINCIPAL_LOGIN},
            },
            # ADDED BY review 4986931575 BLOCKING 1: SS-L condition 7's own record -- lifecycle
            # operator, exact merge and CI identities, strictly after verification AND after the
            # CI job completed.
            CLOSURE_ID: {
                "body": f"Lifecycle closure for merge `{MERGE}`, run {RUN_ID}, job {JOB_ID}.",
                "issue_url": PR_URL,
                "created_at": "2026-08-17T14:00:00Z",
                "user": {"login": PRINCIPAL_LOGIN},
            },
        }
        self.runs = {
            RUN_ID: {
                "status": "completed", "conclusion": "success", "head_sha": MERGE,
                "updated_at": "2026-08-17T13:30:00Z",
            }
        }
        self.jobs = {
            JOB_ID: {
                "run_id": RUN_ID, "conclusion": "success", "head_sha": MERGE,
                "completed_at": "2026-08-17T13:30:00Z",
            }
        }
        self.__dict__.update(overrides)

    def pull_request(self, number):
        return self.pulls.get(number)

    def review(self, number, review_id):
        return self.review_records.get(str(review_id)) if number in self.pulls else None

    def reviews(self, number):
        return list(self.review_records.values()) if number in self.pulls else None

    def issue_comment(self, comment_id):
        return self.comments.get(str(comment_id))

    def workflow_run(self, run_id):
        return self.runs.get(str(run_id))

    def workflow_job(self, job_id):
        return self.jobs.get(str(job_id))


def sources(git=None, governance=None) -> A.TruthSources:
    return A.TruthSources(git=git or FakeGit(), governance=governance or FakeGovernance())


def lifecycle() -> dict:
    return {
        "gates_closed": list(A.REQUIRED_LIFECYCLE_GATES),
        "independent_review": {
            "review_id": REVIEW_ID,
            "formal_disposition": A.APPROVING_REVIEW_DISPOSITION,
            "blocking_count": 0,
            "major_count": 0,
            "reviewed_sha": HEAD,
            "reviewer_identity": REVIEWER_LOGIN,
        },
        "principal_acceptance": {"comment_id": ACCEPT_ID, "accepted_head": HEAD},
        "merge": {"merge_sha": MERGE, "parents": [BASE, HEAD]},
        "post_merge_verification": {"comment_id": VERIFY_ID, "verified_merge_sha": MERGE},
        "merge_commit_ci": {
            "run_id": RUN_ID,
            "job_id": JOB_ID,
            "status": "completed",
            "conclusion": "success",
            "head_sha": MERGE,
        },
        # ADDED BY review 4986931575 BLOCKING 1: XASSET-0044 SS-L condition 7, now a required,
        # closed, actor-bound, identity-bound and chronology-bound gate.
        "lifecycle_closure": {
            "comment_id": CLOSURE_ID,
            "closed_merge_sha": MERGE,
            "closed_run_id": RUN_ID,
            "closed_job_id": JOB_ID,
        },
    }


@pytest.fixture
def payload() -> dict:
    doc = A.build_authorization_payload(
        authorization_head=HEAD,
        lifecycle_evidence=lifecycle(),
        author_identity="implementation-author",
        generated_at_utc="2026-08-17T00:00:00Z",
        merge_sha=MERGE,
    )
    # build_authorization_payload derives load-bearing identity from the real tree, which does not
    # yet contain the unmerged XASSET-0037 head; align it with the fake merged tree.
    doc["load_bearing_identity"] = {
        rel: A.sha256_file(ROOT / rel) for rel in sorted(A.LOAD_BEARING_RELPATHS)
    }
    return doc


@pytest.fixture(scope="module")
def prereg() -> dict:
    return yaml.safe_load(PREREG_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION.read_text(encoding="utf-8")


def _rejected(doc, fragment, src=None):
    result = A.validate_authorization_document(doc, src or sources())
    assert not result.valid, f"expected refusal for {fragment!r}"
    assert any(fragment in e for e in result.errors), (
        f"expected an error containing {fragment!r}, got {result.errors}"
    )


def _lane(tmp_path: Path) -> A.LanePaths:
    return A.LanePaths(
        authorization=tmp_path / "authorization.json",
        claim=tmp_path / "claim.json",
        completion=tmp_path / "completion.json",
        ledger=tmp_path / "lane_ledger.jsonl",
    )


# ======================================================================================
# (1) The obsolete XASSET-0029 lifecycle cannot authorize the current package
# ======================================================================================


class TestObsoleteLifecycleCannotAuthorize:
    """The core fail-closed condition XASSET-0030 §D predicted, reproduced against real git."""

    def test_three_current_load_bearing_paths_are_absent_from_the_xasset_0029_merged_tree(self):
        git = A.LiveGitTruthSource()
        # RE-ANCHORED BY XASSET-0044: evaluated over XASSET-0037's OWN accepted boundary, which is
        # the set this assertion was written about. The live set is checked immediately below.
        absent = [
            rel
            for rel in _xasset_0037_load_bearing()
            if git.blob_sha256_at(A.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA, rel) is None
        ]
        live_absent = {
            rel
            for rel in A.LOAD_BEARING_RELPATHS
            if git.blob_sha256_at(A.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA, rel) is None
        }
        # Every path absent from XASSET-0037's set is still absent from the live one, and every
        # additional live absentee is a later decision file that could not have existed either.
        assert set(absent) <= live_absent
        for rel in live_absent - set(absent):
            assert rel.startswith("governance/decisions/XASSET-"), rel
        assert set(absent) == {
            "level1_stage1_runner.py",
            "level1_stage1_result_validator.py",
            "governance/decisions/"
            "XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
            # The successor's own decision, absent for the same reason: it did not exist either.
            "governance/decisions/"
            "XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md",
        }

    def test_three_of_the_packages_own_nine_paths_were_absent(self):
        """The exact drift XASSET-0030 §D predicted, over the set the package actually bound."""
        git = A.LiveGitTruthSource()
        absent = [
            rel
            for rel in PACKAGE_LOAD_BEARING
            if git.blob_sha256_at(A.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA, rel) is None
        ]
        assert set(absent) == {
            "level1_stage1_runner.py",
            "level1_stage1_result_validator.py",
            "governance/decisions/"
            "XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
        }

    def test_four_further_paths_drifted_from_the_xasset_0029_merged_tree(self):
        git = A.LiveGitTruthSource()
        drifted = []
        for rel in A.LOAD_BEARING_RELPATHS:
            merged = git.blob_sha256_at(A.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA, rel)
            if merged is not None and merged != A.sha256_file(ROOT / rel):
                drifted.append(rel)
        assert set(drifted) == {
            "level1_stage1_execution_authorization.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "research/level1_endpoint_evidence/PROTOCOL_V1.md",
            "research/level1_endpoint_evidence/pre_registration.yaml",
        }

    def test_an_attestation_naming_the_superseded_decision_is_refused(self, payload):
        payload["authorizing_decision"] = A.HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION
        _rejected(payload, "authorization.authorizing_decision")

    def test_an_attestation_naming_the_superseded_pull_request_is_refused(self, payload):
        payload["authorizing_pull_request"] = A.HISTORICAL_OPERATIONAL_AUTHORIZATION_PULL_REQUEST
        _rejected(payload, "authorization.authorizing_pull_request")

    def test_the_superseded_reviewed_base_no_longer_arms_the_lifecycle(self, payload):
        git = FakeGit()
        git.parents[MERGE] = (A.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_BASE, HEAD)
        payload["lifecycle_evidence"]["merge"]["parents"] = [
            A.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_BASE,
            HEAD,
        ]
        _rejected(payload, "is not the exact reviewed base", sources(git=git))

    def test_the_effective_source_is_the_successor_not_the_historical_authorization(self):
        # RE-ANCHORED BY XASSET-0044: XASSET-0037's identity now lives in
        # PRIOR_SUCCESSOR_REBINDING_*, and the property asserted is unchanged.
        assert A.PRIOR_SUCCESSOR_REBINDING_DECISION == "XASSET-0037"
        assert A.HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION == "XASSET-0029"
        assert (
            A.PRIOR_SUCCESSOR_REBINDING_DECISION
            != A.HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION
        )
        # ... and the effective source has itself moved on, to a decision distinct from both.
        assert A.AUTHORIZING_DECISION not in {
            A.PRIOR_SUCCESSOR_REBINDING_DECISION,
            A.HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION,
        }

    def test_the_bound_pull_request_is_the_successors_own(self):
        """Verified against the real draft after it was opened; see the constant's provenance note."""
        # RE-ANCHORED BY XASSET-0044, same property, on the constant that now carries #337.
        assert A.PRIOR_SUCCESSOR_REBINDING_PULL_REQUEST == 337
        assert (
            A.PRIOR_SUCCESSOR_REBINDING_PULL_REQUEST
            != A.HISTORICAL_OPERATIONAL_AUTHORIZATION_PULL_REQUEST
        )
        assert A.PRIOR_SUCCESSOR_REBINDING_PULL_REQUEST != A.PACKAGE_AUTHORIZING_PULL_REQUEST
        assert A.PRIOR_SUCCESSOR_REBINDING_PULL_REQUEST != A.EXECUTABLE_PACKAGE_PULL_REQUEST
        assert A.AUTHORIZING_PULL_REQUEST != A.PRIOR_SUCCESSOR_REBINDING_PULL_REQUEST

    def test_the_bound_pull_request_provenance_is_disclosed_not_flattered(self):
        """The constant must not claim an authoring order it did not have.

        ADVANCED BY XASSET-0047, and STRICTLY STRENGTHENED. XASSET-0037's disclosure was that the
        number was written in advance as the next-sequential guess and then verified. XASSET-0047's
        anchor was bound differently and says so: the branch's first commit carried an impossible
        sentinel, the real number was read back from live GitHub after the draft was opened, and
        only then was it bound. The property under test is unchanged -- the module must state its
        OWN true provenance and may not flatter it -- so this is bound at BOTH ends: the current
        disclosure must be present, and the superseded one must be gone, so a copy-forward of
        XASSET-0037's wording onto a differently-obtained number cannot pass.
        """
        raw = (ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        # The note is a wrapped comment block, so compare on content rather than line breaks.
        source = " ".join(raw.replace("#:", " ").split())
        assert "NOT written in advance as the next sequential guess" in source
        # RE-ANCHORED BY XASSET-0049. The property is that the sentinel's IMPOSSIBILITY is
        # disclosed in the module's own comment rather than flattered over. XASSET-0049 states it
        # more strongly -- the sentinel is NEGATIVE, so it "can never validate by accident" -- so
        # the assertion is pinned on the substance rather than on one generation's exact phrasing,
        # and both the impossibility and the read-back-not-guessed claim are asserted separately.
        assert "structurally impossible pull-request number" in source
        assert "can never validate by accident" in source
        assert "read back from live GitHub" in source
        assert "NOT written in advance as" in source
        assert "that number was read back from live GitHub" in source
        assert "only then was it bound here and re-verified against the live" in source
        # The superseded XASSET-0037 wording must NOT survive on a number it does not describe.
        assert "FIRST WRITTEN before the draft pull request existed" not in source


# ======================================================================================
# (2) Four structurally distinct identities, never overloaded
# ======================================================================================


class TestFourDistinctIdentities:
    def test_the_four_identities_are_pairwise_distinct(self):
        identities = {
            A.PREDECESSOR_DECISION,
            A.HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION,
            A.PACKAGE_AUTHORIZING_DECISION,
            A.AUTHORIZING_DECISION,
        }
        assert len(identities) == 4

    def test_the_structural_closure_predecessor_is_untouched(self):
        """Repointing PREDECESSOR_* at XASSET-0029 is the overloading this filing forbids."""
        assert A.PREDECESSOR_DECISION == "XASSET-0028"
        assert A.PREDECESSOR_MERGE_SHA == "c51e94609eff7ede2bdfa084844d59b8347561e5"
        assert A.PREDECESSOR_ACCEPTED_HEAD == "036606401ea569b0a03f2d716d87a057d07d71dc"
        assert A.PREDECESSOR_MERGE_BASE == "e4b6f0b810884fcb73d1b8ee053d8005db532f3e"

    def test_the_package_authority_is_not_the_package(self):
        assert A.PACKAGE_AUTHORIZING_PULL_REQUEST == 335
        assert A.EXECUTABLE_PACKAGE_PULL_REQUEST == 336
        assert A.PACKAGE_AUTHORIZING_PULL_REQUEST != A.EXECUTABLE_PACKAGE_PULL_REQUEST
        assert A.PACKAGE_AUTHORIZING_MERGE_SHA != A.EXECUTABLE_PACKAGE_MERGE_SHA

    def test_the_package_merge_is_the_successors_reviewed_base(self):
        """Not assumed: the successor branches from exactly the package it binds.

        RE-ANCHORED BY XASSET-0044: XASSET-0037's own reviewed base is now
        PRIOR_SUCCESSOR_REBINDING_MERGE_BASE, and it still equals the package merge exactly.
        """
        assert A.PRIOR_SUCCESSOR_REBINDING_MERGE_BASE == A.EXECUTABLE_PACKAGE_MERGE_SHA

    def test_the_package_base_is_the_package_authoritys_merge(self):
        assert A.EXECUTABLE_PACKAGE_MERGE_BASE == A.PACKAGE_AUTHORIZING_MERGE_SHA

    @pytest.mark.parametrize(
        "block",
        [
            "historical_operational_authorization",
            "package_authorization",
            "executable_package_identity",
        ],
    )
    def test_each_identity_block_is_required(self, payload, block):
        del payload[block]
        _rejected(payload, f"authorization.{block}: required key is absent")

    @pytest.mark.parametrize(
        ("block", "field"),
        [
            ("historical_operational_authorization", "decision"),
            ("historical_operational_authorization", "pull_request"),
            ("historical_operational_authorization", "merge_sha"),
            ("historical_operational_authorization", "accepted_head"),
            ("historical_operational_authorization", "merge_base"),
            ("package_authorization", "decision"),
            ("package_authorization", "pull_request"),
            ("package_authorization", "merge_sha"),
            ("executable_package_identity", "pull_request"),
            ("executable_package_identity", "merge_sha"),
            ("executable_package_identity", "accepted_head"),
            ("executable_package_identity", "merge_base"),
        ],
    )
    def test_every_identity_field_is_bound_exactly(self, payload, block, field):
        payload[block][field] = "z" * 40
        _rejected(payload, f"{block}.{field}")

    @pytest.mark.parametrize(
        "block",
        [
            "historical_operational_authorization",
            "package_authorization",
            "executable_package_identity",
        ],
    )
    def test_each_identity_block_is_a_closed_schema(self, payload, block):
        payload[block]["smuggled"] = "value"
        _rejected(payload, f"{block}.smuggled: unknown key")

    @pytest.mark.parametrize(
        "block",
        [
            "historical_operational_authorization",
            "package_authorization",
            "executable_package_identity",
        ],
    )
    def test_a_non_mapping_identity_block_is_refused(self, payload, block):
        payload[block] = "not-a-mapping"
        _rejected(payload, f"{block}: expected a mapping")


# ======================================================================================
# (3) The rebinding binds the exact merged package
# ======================================================================================


class TestExecutablePackageBinding:
    def test_the_happy_path_validates(self, payload):
        result = A.validate_authorization_document(payload, sources())
        assert result.valid, result.errors

    def test_a_package_merge_absent_from_git_fails_closed(self, payload):
        git = FakeGit()
        del git.parents[A.EXECUTABLE_PACKAGE_MERGE_SHA]
        _rejected(payload, "executable-package merge", sources(git=git))

    def test_package_merge_parents_must_be_exact_and_ordered(self, payload):
        git = FakeGit()
        git.parents[A.EXECUTABLE_PACKAGE_MERGE_SHA] = (
            A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
            A.EXECUTABLE_PACKAGE_MERGE_BASE,
        )
        _rejected(payload, "executable-package merge parents", sources(git=git))

    def test_a_squashed_package_merge_fails_closed(self, payload):
        git = FakeGit()
        git.parents[A.EXECUTABLE_PACKAGE_MERGE_SHA] = (A.EXECUTABLE_PACKAGE_MERGE_BASE,)
        _rejected(payload, "executable-package merge parents", sources(git=git))

    def test_package_merge_drift_fails_closed(self, payload):
        git = FakeGit()
        git.trees[A.EXECUTABLE_PACKAGE_MERGE_SHA] = "q" * 40
        _rejected(payload, "package merge drift", sources(git=git))

    def test_an_unresolvable_package_tree_fails_closed(self, payload):
        git = FakeGit()
        del git.trees[A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD]
        _rejected(payload, "zero merge drift cannot be proven for the package", sources(git=git))

    def test_a_package_outside_the_successors_history_fails_closed(self, payload):
        git = FakeGit(_ancestor=False)
        _rejected(payload, "is not an ancestor of the successor merge", sources(git=git))

    def test_the_historical_authorizations_own_parents_are_verified(self, payload):
        git = FakeGit()
        git.parents[A.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA] = ("1" * 40, "2" * 40)
        _rejected(payload, "historical operational-authorization merge parents", sources(git=git))

    def test_a_missing_historical_authorization_merge_fails_closed(self, payload):
        git = FakeGit()
        del git.parents[A.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA]
        _rejected(payload, "cannot prove what it is superseding", sources(git=git))

    def test_a_missing_package_authority_merge_fails_closed(self, payload):
        git = FakeGit()
        del git.parents[A.PACKAGE_AUTHORIZING_MERGE_SHA]
        _rejected(payload, "package-authorizing merge", sources(git=git))


# ======================================================================================
# (4) §G.B's invariant — outcome-producing code may not change inside its own rebinding
# ======================================================================================


class TestOutcomeProducingInvariant:
    def test_both_outcome_producing_paths_are_load_bearing(self):
        for relative in A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS:
            assert relative in A.LOAD_BEARING_RELPATHS

    @pytest.mark.parametrize("relative", A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS)
    def test_a_runner_edit_inside_the_rebinding_fails_closed(self, payload, relative):
        """The precise smuggling this check exists to catch."""
        git = FakeGit()
        git.blobs[(A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, relative)] = "0" * 64
        git.blobs[(A.EXECUTABLE_PACKAGE_MERGE_SHA, relative)] = "0" * 64
        _rejected(payload, "outcome-producing drift", sources(git=git))

    @pytest.mark.parametrize("relative", A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS)
    def test_an_outcome_producing_path_absent_from_the_package_fails_closed(
        self, payload, relative
    ):
        git = FakeGit()
        del git.blobs[(A.EXECUTABLE_PACKAGE_MERGE_SHA, relative)]
        _rejected(payload, "the outcome-producing bytes being rebound", sources(git=git))

    @pytest.mark.parametrize("relative", A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS)
    def test_the_live_bytes_match_the_accepted_package(self, relative):
        """Not synthetic: the real working tree against the real merged package."""
        git = A.LiveGitTruthSource()
        assert (
            git.blob_sha256_at(A.EXECUTABLE_PACKAGE_MERGE_SHA, relative)
            == A.sha256_file(ROOT / relative)
        ), f"{relative} is not byte-identical to the accepted PR #336 package"

    @pytest.mark.parametrize("relative", A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS)
    def test_the_package_merge_and_its_accepted_head_agree_on_the_live_bytes(self, relative):
        git = A.LiveGitTruthSource()
        assert git.blob_sha256_at(
            A.EXECUTABLE_PACKAGE_MERGE_SHA, relative
        ) == git.blob_sha256_at(A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, relative)

    def test_the_declared_relpaths_are_not_the_whole_outcome_producing_surface(self):
        """MAJOR 1's premise, asserted rather than assumed: both consumers import derivations."""
        seeds = _independently_derived_seed_symbols()
        assert seeds, "the consumers import no derivation symbols — premise broken"
        assert DERIVATION_RELPATH not in A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS
        assert DERIVATION_RELPATH in A.LOAD_BEARING_RELPATHS

    def test_this_rebinding_modified_neither_outcome_producing_module(self):
        """The claim is checked against git, not asserted in prose."""
        changed = subprocess.run(
            [
                "git",
                "diff",
                "--name-only",
                A.EXECUTABLE_PACKAGE_MERGE_SHA,
                "--",
                *A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert changed.returncode == 0
        assert changed.stdout.strip() == "", changed.stdout


# ======================================================================================
# (5) The trust boundary grows and nothing is removed
# ======================================================================================


class TestTrustBoundary:
    def test_every_package_load_bearing_path_is_retained(self):
        for relative in PACKAGE_LOAD_BEARING:
            assert relative in A.LOAD_BEARING_RELPATHS, f"{relative} was removed"

    def test_the_only_addition_is_the_successor_decision(self):
        """RE-ANCHORED BY XASSET-0044. What XASSET-0037 added is unchanged and still asserted
        exactly: its ONE addition over the package's nine. The live set has since grown again
        under XASSET-0030 SS-D, so the property is proven against XASSET-0037's own accepted
        boundary -- read from the module AS IT STOOD AT ITS OWN MERGE -- rather than against a live
        tuple a later generation owns. Every package path surviving into the live set is asserted
        separately below, so nothing about preservation is lost.
        """
        additions = set(_xasset_0037_load_bearing()) - set(PACKAGE_LOAD_BEARING)
        assert additions == {
            "governance/decisions/"
            "XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md"
        }
        # PRESERVATION, asserted against the LIVE set: no later generation may drop a path.
        assert set(PACKAGE_LOAD_BEARING) <= set(A.LOAD_BEARING_RELPATHS)
        assert set(_xasset_0037_load_bearing()) <= set(A.LOAD_BEARING_RELPATHS)

    def test_the_set_grew_from_nine_to_ten(self):
        """RE-ANCHORED BY XASSET-0044, same property against XASSET-0037's own accepted set."""
        assert len(PACKAGE_LOAD_BEARING) == 9
        assert len(_xasset_0037_load_bearing()) == 10
        assert len(set(_xasset_0037_load_bearing())) == 10
        # The live boundary only ever grows, and never contains a duplicate.
        assert len(A.LOAD_BEARING_RELPATHS) >= 10
        assert len(set(A.LOAD_BEARING_RELPATHS)) == len(A.LOAD_BEARING_RELPATHS)

    def test_the_successor_decision_is_load_bearing(self):
        assert any("XASSET-0037" in relative for relative in A.LOAD_BEARING_RELPATHS)

    def test_no_results_artifact_is_load_bearing(self):
        assert "stage1_results" not in " ".join(A.LOAD_BEARING_RELPATHS).lower()

    def test_every_load_bearing_path_exists(self):
        for relative in A.LOAD_BEARING_RELPATHS:
            assert (ROOT / relative).exists(), relative

    def test_load_bearing_identity_must_cover_exactly_the_set(self, payload):
        payload["load_bearing_identity"].pop(
            "governance/decisions/"
            "XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md"
        )
        _rejected(payload, "must cover exactly the load-bearing files")

    @pytest.mark.parametrize("relative", sorted(A.LOAD_BEARING_RELPATHS))
    def test_a_recorded_identity_that_disagrees_with_the_merged_tree_is_refused(
        self, payload, relative
    ):
        payload["load_bearing_identity"][relative] = "0" * 64
        _rejected(payload, f"load_bearing_identity[{relative!r}]")

    @pytest.mark.parametrize("relative", sorted(A.LOAD_BEARING_RELPATHS))
    def test_post_review_drift_in_any_load_bearing_byte_fails_closed(self, payload, relative):
        """The merged tree may never become its own source of truth."""
        git = FakeGit()
        git.blobs[(HEAD, relative)] = "0" * 64
        _rejected(payload, "merge drift", sources(git=git))

    @pytest.mark.parametrize("relative", sorted(A.LOAD_BEARING_RELPATHS))
    def test_working_tree_drift_in_any_load_bearing_byte_fails_closed(self, payload, relative):
        git = FakeGit()
        git.blobs[(MERGE, relative)] = "0" * 64
        git.blobs[(HEAD, relative)] = "0" * 64
        payload["load_bearing_identity"][relative] = "0" * 64
        _rejected(payload, "enforcement drift", sources(git=git))


# ======================================================================================
# (6) Lifecycle evidence — missing, stale, adverse, mismatched, unreachable all fail closed
# ======================================================================================


class TestLifecycleEvidenceFailsClosed:
    def test_an_unreachable_pull_request_fails_closed(self, payload):
        _rejected(payload, "could not be verified", sources(governance=FakeGovernance(pulls={})))

    def test_an_unmerged_pull_request_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.pulls[A.AUTHORIZING_PULL_REQUEST]["merged"] = False
        _rejected(payload, "is not merged", sources(governance=gov))

    def test_a_pull_request_in_another_repository_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.pulls[A.AUTHORIZING_PULL_REQUEST]["base"]["repo"]["full_name"] = "someone/else"
        _rejected(payload, "belongs to", sources(governance=gov))

    def test_a_stale_authorization_head_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.pulls[A.AUTHORIZING_PULL_REQUEST]["head"]["sha"] = "9" * 40
        _rejected(payload, "not the recorded authorization_head", sources(governance=gov))

    def test_a_nonexistent_but_well_formed_review_id_fails_closed(self, payload):
        _rejected(payload, "does not exist on pull request", sources(governance=FakeGovernance(review_records={})))

    def test_a_review_on_another_head_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.review_records[REVIEW_ID]["commit_id"] = "9" * 40
        _rejected(payload, "was submitted against", sources(governance=gov))

    def test_an_adverse_review_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.review_records[REVIEW_ID]["body"] = "FORMAL DISPOSITION: CHANGES REQUIRED"
        _rejected(payload, "formal disposition is", sources(governance=gov))

    def test_an_approval_phrase_quoted_in_explanatory_text_does_not_rescue_it(self, payload):
        gov = FakeGovernance()
        gov.review_records[REVIEW_ID]["body"] = (
            "FORMAL DISPOSITION: CHANGES REQUIRED\n\n"
            f"This is not {A.APPROVING_REVIEW_DISPOSITION}."
        )
        _rejected(payload, "formal disposition is", sources(governance=gov))

    def test_a_dismissed_review_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.review_records[REVIEW_ID]["state"] = "DISMISSED"
        _rejected(payload, "has been DISMISSED", sources(governance=gov))

    def test_a_later_adverse_exact_head_review_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.review_records["4970000002"] = {
            "commit_id": HEAD,
            "id": "4970000002",
            "body": "FORMAL DISPOSITION: CHANGES REQUIRED",
            "user": {"login": REVIEWER_LOGIN},
            "state": "CHANGES_REQUESTED",
            "submitted_at": "2026-08-17T10:30:00Z",
            "html_url": f"{PR_URL}#pullrequestreview-4970000002",
        }
        _rejected(payload, "later non-dismissed", sources(governance=gov))

    def test_an_unretrievable_review_listing_fails_closed(self, payload):
        class NoListing(FakeGovernance):
            def reviews(self, number):
                return None

        _rejected(payload, "finality cannot be established", sources(governance=NoListing()))

    def test_a_self_declared_reviewer_identity_fails_closed(self, payload):
        payload["lifecycle_evidence"]["independent_review"]["reviewer_identity"] = "someone-else"
        _rejected(payload, "reviewer identity may not be asserted")

    def test_an_absent_principal_acceptance_fails_closed(self, payload):
        gov = FakeGovernance()
        del gov.comments[ACCEPT_ID]
        _rejected(payload, "principal acceptance comment", sources(governance=gov))

    def test_an_acceptance_for_another_head_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.comments[ACCEPT_ID]["body"] = f"Principal acceptance, relying on review {REVIEW_ID}."
        _rejected(payload, "does not name the exact head", sources(governance=gov))

    def test_an_acceptance_not_certifying_the_review_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.comments[ACCEPT_ID]["body"] = f"Principal acceptance at exact head `{HEAD}`."
        _rejected(payload, "does not certify the independent review", sources(governance=gov))

    def test_an_acceptance_by_another_account_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.comments[ACCEPT_ID]["user"] = {"login": "impostor"}
        _rejected(payload, "not the principal", sources(governance=gov))

    def test_an_acceptance_from_another_pull_request_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.comments[ACCEPT_ID]["issue_url"] = (
            f"https://api.github.com/repos/{A.REPOSITORY_IDENTITY}/issues/1"
        )
        _rejected(payload, "does not belong to pull request", sources(governance=gov))

    def test_an_absent_post_merge_verification_fails_closed(self, payload):
        gov = FakeGovernance()
        del gov.comments[VERIFY_ID]
        _rejected(payload, "merge alone never authorizes execution", sources(governance=gov))

    def test_a_post_merge_verification_preceding_the_merge_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.comments[VERIFY_ID]["created_at"] = "2026-08-17T00:00:00Z"
        _rejected(payload, "precedes the merge", sources(governance=gov))

    def test_a_recorded_merge_that_is_not_the_real_merge_fails_closed(self, payload):
        payload["lifecycle_evidence"]["merge"]["merge_sha"] = "9" * 40
        _rejected(payload, "is not the real merge commit")

    def test_successor_merge_drift_fails_closed(self, payload):
        git = FakeGit()
        git.trees[MERGE] = "z" * 40
        _rejected(payload, "merging changed reviewed bytes", sources(git=git))

    def test_a_merge_outside_the_current_ancestry_fails_closed(self, payload):
        git = FakeGit(_ancestor=False)
        _rejected(payload, "not an ancestor", sources(git=git))

    def test_an_absent_ci_run_fails_closed(self, payload):
        _rejected(payload, "workflow run", sources(governance=FakeGovernance(runs={})))

    def test_a_ci_run_against_the_pr_head_rather_than_the_merge_fails_closed(self, payload):
        """The exact distinction §J condition 6 draws."""
        gov = FakeGovernance()
        gov.runs[RUN_ID]["head_sha"] = HEAD
        _rejected(payload, "ran against", sources(governance=gov))

    def test_an_unsuccessful_ci_run_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.runs[RUN_ID]["conclusion"] = "failure"
        _rejected(payload, "not completed/success", sources(governance=gov))

    def test_a_job_from_another_run_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.jobs[JOB_ID]["run_id"] = "3200000999"
        _rejected(payload, "belongs to run", sources(governance=gov))

    @pytest.mark.parametrize("gate", A.REQUIRED_LIFECYCLE_GATES)
    def test_every_lifecycle_gate_must_be_declared_closed(self, payload, gate):
        payload["lifecycle_evidence"]["gates_closed"] = [
            g for g in A.REQUIRED_LIFECYCLE_GATES if g != gate
        ]
        _rejected(payload, f"must include {gate!r}")

    @pytest.mark.parametrize("counter", ["blocking_count", "major_count"])
    def test_unresolved_findings_fail_closed(self, payload, counter):
        payload["lifecycle_evidence"]["independent_review"][counter] = 1
        _rejected(payload, f"independent_review.{counter}")


# ======================================================================================
# (7) Canonical pins, universe identity, and closed schema
# ======================================================================================


class TestCanonicalAndUniverseIdentity:
    def test_the_effective_pins_match_the_live_canonical_bytes(self):
        assert A.sha256_file(PROTOCOL) == A.CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH]
        assert A.sha256_file(PREREG_PATH) == A.CANONICAL_PINS[A.CANONICAL_PREREGISTRATION_RELPATH]

    def test_the_pins_are_not_placeholders(self):
        assert not A.pins_are_placeholders()

    @pytest.mark.parametrize(
        "predecessor",
        ["XASSET_0036_PACKAGE_CANONICAL_PINS", "XASSET_0029_CANONICAL_PINS", "PREDECESSOR_CANONICAL_PINS"],
    )
    def test_the_successor_pins_differ_from_every_predecessor_generation(self, predecessor):
        historical = getattr(A, predecessor)
        for relative, digest in A.CANONICAL_PINS.items():
            assert digest != historical[relative], (
                f"{relative} still carries the {predecessor} pin"
            )

    def test_predecessor_pins_are_retained_verbatim_as_history(self):
        assert A.XASSET_0036_PACKAGE_CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH] == (
            "86b2a5e8674247698ac592ce4734744f940b4a119ffda5fd702bc3cbf3e40c13"
        )
        assert A.XASSET_0036_PACKAGE_CANONICAL_PINS[A.CANONICAL_PREREGISTRATION_RELPATH] == (
            "e993df9f41d2f5352e51c9921dd006d50ab69518a730d37def106696b3f149d4"
        )
        assert A.XASSET_0029_CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH] == (
            "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
        )

    @pytest.mark.parametrize("relative", sorted(A.CANONICAL_PINS))
    def test_a_recorded_pin_that_disagrees_is_refused(self, payload, relative):
        payload["canonical_pins"][relative] = "0" * 64
        _rejected(payload, f"authorization.canonical_pins[{relative!r}]")

    def test_an_unknown_canonical_pin_is_refused(self, payload):
        payload["canonical_pins"]["research/level1_endpoint_evidence/other.yaml"] = "0" * 64
        _rejected(payload, "unknown canonical file")

    def test_the_universe_is_unchanged_by_the_rebinding(self):
        assert CU.universe_aggregate_sha256() == FROZEN_UNIVERSE_SHA256
        assert CU.derived_cardinality() == 680
        assert len(CU.per_cell_cardinality()) == 48

    @pytest.mark.parametrize("field", ["sha256", "count", "cell_count"])
    def test_a_wrong_universe_identity_is_refused(self, payload, field):
        payload["construction_universe"][field] = "0" * 64 if field == "sha256" else 1
        _rejected(payload, f"authorization.construction_universe.{field}")

    def test_the_attestation_schema_stays_closed(self, payload):
        payload["smuggled_key"] = True
        _rejected(payload, "authorization.smuggled_key: unknown key")

    def test_duplicate_json_keys_are_rejected(self):
        with pytest.raises(ValueError):
            json.loads(
                '{"a": 1, "a": 2}', object_pairs_hook=A._reject_duplicate_keys
            )


# ======================================================================================
# (8) No committed value authorizes, and nothing validates before closure
# ======================================================================================


class TestNoCommittedValueAuthorizes:
    def test_the_canonical_executable_flag_stays_false(self, prereg):
        block = prereg["stage_1_executability"]
        assert block["executable"] is False
        assert block["executable_is_never_the_authorization_source"] is True

    def test_flipping_the_committed_flag_is_a_validation_error(self, prereg):
        mutated = yaml.safe_load(PREREG_PATH.read_text(encoding="utf-8"))
        mutated["stage_1_executability"]["executable"] = True
        result = PREREG.validate(mutated)
        assert not result.ok
        assert any("stage_1_executability.executable" in e for e in result.errors)

    def test_the_committed_authorization_block_never_claims_effectivity(self, prereg):
        block = prereg["stage_1_operational_authorization"]
        assert block["currently_effective"] is False
        assert block["authorization_is_committed_state"] is False
        assert block["authorization_is_external_runtime_evidence"] is True

    def test_no_attestation_means_the_lane_is_absent(self, tmp_path):
        state, reason = A.lane_state_at(_lane(tmp_path), sources())
        assert state == A.LANE_ABSENT
        assert "no attestation present" in reason

    def test_a_new_execution_is_not_authorized_without_an_attestation(self, tmp_path):
        authorized, reason = A.new_execution_is_authorized(_lane(tmp_path), sources())
        assert authorized is False
        assert A.AUTHORIZING_DECISION in reason

    def test_an_invalid_attestation_never_reaches_disk(self, tmp_path, payload):
        payload["authorizing_decision"] = A.HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION
        lane = _lane(tmp_path)
        with pytest.raises(ValueError):
            A.write_authorization(payload, lane.authorization, sources())
        assert not lane.authorization.exists()
        assert sorted(p.name for p in tmp_path.iterdir()) == []

    def test_an_attestation_before_lifecycle_closure_cannot_validate(self, payload):
        """Merge is not closure: an unconcluded CI run fails closed."""
        gov = FakeGovernance()
        gov.runs[RUN_ID]["status"] = "in_progress"
        gov.runs[RUN_ID]["conclusion"] = None
        _rejected(payload, "not completed/success", sources(governance=gov))

    def test_a_forged_local_claim_does_not_authorize(self, tmp_path):
        lane = _lane(tmp_path)
        lane.claim.parent.mkdir(parents=True, exist_ok=True)
        lane.claim.write_text(
            json.dumps(
                {
                    "event": A.LANE_CLAIMED,
                    "execution_attempt_id": A.EXECUTION_ATTEMPT_ID,
                    "authorization_sha256": "0" * 64,
                    "claimed_at_utc": "2026-08-17T00:00:00Z",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        authorized, reason = A.claimed_execution_is_authorized(lane, sources())
        assert authorized is False
        assert "attestation" in reason.lower()

    def test_claiming_a_non_ready_lane_raises_and_writes_nothing(self, tmp_path):
        lane = _lane(tmp_path)
        with pytest.raises(ValueError):
            A.claim_execution(claimed_at_utc="2026-08-17T00:00:00Z", paths=lane, sources=sources())
        assert not lane.claim.exists()
        assert not lane.ledger.exists()


# ======================================================================================
# (9) Nothing real was created, claimed, completed, or consumed
# ======================================================================================


class TestNoRealLaneOrArtifact:
    def test_the_real_authorization_root_does_not_exist(self):
        assert not A.AUTHORIZATION_ROOT.exists()

    @pytest.mark.parametrize(
        "path_attr", ["AUTHORIZATION_PATH", "CLAIM_PATH", "COMPLETION_PATH", "LEDGER_PATH"]
    )
    def test_no_real_lane_record_exists(self, path_attr):
        assert not getattr(A, path_attr).exists()

    def test_the_real_lane_reports_absent_and_unauthorized(self):
        state, _ = A.lane_state_at(A.LanePaths())
        assert state == A.LANE_ABSENT
        authorized, _ = A.new_execution_is_authorized()
        assert authorized is False

    def test_attempt_1_is_intact_and_unconsumed(self):
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"
        assert not A.COMPLETION_PATH.exists()
        assert not A.CLAIM_PATH.exists()

    @pytest.mark.parametrize(
        "relative",
        [
            "research/level1_endpoint_evidence/stage1_results.yaml",
            "research/level1_endpoint_evidence/attestation.yaml",
            "research/level1_endpoint_evidence/ATTEMPT_1",
        ],
    )
    def test_no_execution_artifact_exists(self, relative):
        assert not (ROOT / relative).exists()

    def test_no_stage1_results_artifact_exists_anywhere(self):
        assert list(ROOT.rglob("stage1_results.yaml")) == []


# ======================================================================================
# (10) The canonical amendment, and what it did NOT change
# ======================================================================================


class TestCanonicalAmendment:
    def test_the_canonical_files_validate(self):
        assert PREREG.validate_file().ok, PREREG.validate_file().errors

    def test_the_hash_version_advanced_to_v7(self, prereg):
        assert prereg["hash_version"] == "ENDPOINT-0001-PREREG-V7"
        assert prereg["predecessor_hash_version"] == "ENDPOINT-0001-PREREG-V6"

    def test_the_operative_lifecycle_names_the_successor(self, prereg):
        """RE-ANCHORED BY XASSET-0044. XASSET-0037's four values are unchanged and still asserted
        in full -- they now sit in the explicitly predecessor-named fields SS-J requires, which is
        exactly the retention this test exists to protect. That every operative field names ONE
        current source, and that it is no longer XASSET-0037, is asserted alongside.
        """
        effectivity = prereg["lifecycle_effectivity"]
        assert effectivity[
            "predecessor_stage_1_execution_may_begin_only_after_xasset_0037"
        ].startswith("XASSET_0037_")
        assert (
            effectivity["predecessor_stage_1_execution_precondition_amended_by_xasset_0037"]
            == "XASSET-0037"
        )
        assert prereg["stages"]["stage_1"][
            "predecessor_executable_only_after_xasset_0037"
        ].startswith("XASSET_0037_")
        assert prereg["stage_1_executability"][
            "predecessor_blocking_prerequisite_xasset_0037"
        ].startswith("XASSET_0037_")
        # Exactly one operative source, and it has moved past XASSET-0037.
        for operative in (
            effectivity["stage_1_execution_may_begin_only_after"],
            prereg["stages"]["stage_1"]["executable_only_after"],
            prereg["stage_1_executability"]["blocking_prerequisite"],
        ):
            assert not operative.startswith("XASSET_0037_")
        assert effectivity["stage_1_execution_precondition_amended_by"] != "XASSET-0037"

    def test_the_predecessor_lifecycle_is_retained_as_history(self, prereg):
        effectivity = prereg["lifecycle_effectivity"]
        assert effectivity[
            "predecessor_stage_1_execution_may_begin_only_after_xasset_0029"
        ].startswith("XASSET_0029_")
        assert (
            effectivity["predecessor_stage_1_execution_precondition_amended_by_xasset_0029"]
            == "XASSET-0029"
        )
        assert prereg["stages"]["stage_1"][
            "predecessor_executable_only_after_xasset_0029"
        ].startswith("XASSET_0029_")

    def test_the_mechanisms_establisher_is_not_rewritten(self, prereg):
        block = prereg["stage_1_operational_authorization"]
        # THE POINT OF THIS TEST IS UNCHANGED and is the assertion that matters: the MECHANISM's
        # establisher is historical truth and is never rewritten by any successor.
        assert block["established_by"] == "XASSET-0029"
        # RE-ANCHORED BY XASSET-0044: XASSET-0037's own values are retained in predecessor-named
        # fields, and the effective source has advanced past them.
        assert block["predecessor_rebound_by_xasset_0037"] == "XASSET-0037"
        assert (
            block["predecessor_effective_structural_authorization_source_xasset_0037"]
            == "XASSET-0037"
        )
        assert block["rebound_by"] != "XASSET-0037"
        assert block["effective_structural_authorization_source"] != "XASSET-0037"
        assert block["rebound_by"] == block["effective_structural_authorization_source"]

    def test_the_rebinding_block_records_four_distinct_identities(self, prereg):
        identities = prereg["stage_1_operational_authorization"][
            "successor_operational_rebinding"
        ]["distinct_identities"]
        assert identities == {
            "structural_closure_predecessor": "XASSET-0028",
            "historical_operational_authorization": "XASSET-0029",
            "package_authority": "XASSET-0036",
            "executable_package": "PULL_REQUEST_336",
        }
        assert len(set(identities.values())) == 4

    def test_the_rebinding_is_not_an_activation_step(self, prereg):
        block = prereg["stage_1_operational_authorization"]["successor_operational_rebinding"]
        assert block["is_an_activation_step"] is False
        assert block["is_an_attestation"] is False
        assert block["adds_activation_authorizations"] == 0
        assert block["no_infinite_authorization_regress_preserved"] is True

    def test_the_historical_authorization_is_not_invalidated(self, prereg):
        block = prereg["stage_1_operational_authorization"]["successor_operational_rebinding"]
        assert block["historical_operational_authorization_is_invalidated"] is False

    def test_nothing_was_removed_and_nothing_weakened(self, prereg):
        block = prereg["stage_1_operational_authorization"]["successor_operational_rebinding"]
        assert block["load_bearing_paths_removed"] == 0
        assert block["exact_byte_checking_weakened"] is False

    @pytest.mark.parametrize(
        "condition",
        [
            "SUPERSEDED_PREDECESSOR_AUTHORIZATION_DECISION_OR_PULL_REQUEST",
            "EXECUTABLE_PACKAGE_IDENTITY_ABSENT_MISMATCHED_OR_DRIFTED",
            "EXECUTABLE_PACKAGE_NOT_AN_ANCESTOR_OF_THE_SUCCESSOR_MERGE",
            "OUTCOME_PRODUCING_CODE_CHANGED_INSIDE_THE_REBINDING_THAT_BINDS_IT",
        ],
    )
    def test_the_successor_fail_closed_conditions_are_declared(self, prereg, condition):
        assert condition in prereg["stage_1_operational_authorization"]["must_fail_closed_on"]

    def test_dropping_a_fail_closed_condition_is_a_validation_error(self):
        mutated = yaml.safe_load(PREREG_PATH.read_text(encoding="utf-8"))
        block = mutated["stage_1_operational_authorization"]
        block["must_fail_closed_on"] = [
            c
            for c in block["must_fail_closed_on"]
            if c != "OUTCOME_PRODUCING_CODE_CHANGED_INSIDE_THE_REBINDING_THAT_BINDS_IT"
        ]
        result = PREREG.validate(mutated)
        assert not result.ok

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("is_an_activation_step", True),
            ("is_an_attestation", True),
            ("adds_activation_authorizations", 1),
            ("no_infinite_authorization_regress_preserved", False),
            ("historical_operational_authorization_is_invalidated", True),
            ("load_bearing_paths_removed", 1),
            ("exact_byte_checking_weakened", True),
            ("outcome_producing_paths_must_be_byte_identical_to_the_accepted_package", False),
        ],
    )
    def test_weakening_the_rebinding_block_is_a_validation_error(self, field, value):
        mutated = yaml.safe_load(PREREG_PATH.read_text(encoding="utf-8"))
        mutated["stage_1_operational_authorization"]["successor_operational_rebinding"][
            field
        ] = value
        result = PREREG.validate(mutated)
        assert not result.ok
        assert any("successor_operational_rebinding" in e for e in result.errors)

    def test_collapsing_the_distinct_identities_is_a_validation_error(self):
        mutated = yaml.safe_load(PREREG_PATH.read_text(encoding="utf-8"))
        identities = mutated["stage_1_operational_authorization"][
            "successor_operational_rebinding"
        ]["distinct_identities"]
        identities["historical_operational_authorization"] = identities[
            "structural_closure_predecessor"
        ]
        result = PREREG.validate(mutated)
        assert not result.ok

    def test_the_protocol_mirror_agrees_with_the_canonical_yaml(self):
        assert PREREG.validate_protocol_mirror(PROTOCOL.read_text(encoding="utf-8")).ok

    def test_the_decision_pin_block_matches_the_live_canonical_bytes(self, decision_text):
        result = PREREG.validate_xasset_0037_successor_hash_pins(decision_text)
        assert result.ok, result.errors

    def test_a_forged_decision_pin_block_fails_closed(self, decision_text):
        """RE-ANCHORED BY XASSET-0044: same property, against the pins this validator now asserts.

        XASSET-0037's pin validator was demoted from a live-byte check to a verbatim-history check
        when XASSET-0044 amended the canonical bytes -- exactly the treatment XASSET-0037 itself
        gave XASSET-0029's. Forging its accepted protocol pin must still fail closed, and it does.
        """
        forged = decision_text.replace(
            A.XASSET_0037_CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH], "0" * 64
        )
        assert forged != decision_text, "the forgery must actually change the text"
        assert not PREREG.validate_xasset_0037_successor_hash_pins(forged).ok

    def test_gate_identity_is_unchanged(self, prereg):
        gates = prereg["gate_sequence"]["gates"]
        assert len(gates) == 12
        assert [g["gate_index"] for g in gates] == list(range(1, 13))

    def test_the_b1_b2_b3_blocks_are_untouched(self, prereg):
        inventory = prereg["pair_consumption_rule"]["structural_inventory"]
        assert inventory["consuming_total"] == 480
        assert inventory["non_consuming_total"] == 200
        assert inventory["universe_total"] == 680
        assert sum(r["count"] for r in inventory["rows"]) == 680
        assert prereg["g12_modal_register"]["scope"] == "G12_ONLY"
        assert prereg["reserved_gate_recording_posture"]["recorded_value"] == "UNABLE_TO_DETERMINE"


# ======================================================================================
# (11) The decision record, the catalog, and the register
# ======================================================================================


class TestGovernanceRecord:
    def test_the_decision_file_exists_and_is_load_bearing(self):
        assert DECISION.exists()
        rel = DECISION.relative_to(ROOT).as_posix()
        assert rel in A.LOAD_BEARING_RELPATHS

    def test_the_catalog_records_the_decision_exactly_once(self):
        catalog = yaml.safe_load((ROOT / "governance/decisions.yaml").read_text(encoding="utf-8"))
        rows = [d for d in catalog["decisions"] if d["decision_id"] == "XASSET-0037"]
        assert len(rows) == 1
        assert rows[0]["file"] == DECISION.relative_to(ROOT).as_posix()
        assert rows[0]["supporting_artifact"] == Path(__file__).name

    @pytest.mark.parametrize(
        "claim",
        [
            "Stage 1 remains UNARMED and NOT EXECUTABLE",
            "`ATTEMPT_1` is intact, unclaimed, and unconsumed",
            "adds one rebinding and ZERO activation authorizations",
            "No load-bearing path is removed and no exact-byte check is weakened",
            "`XASSET-0029` is preserved, not invalidated",
            "not consumed, replaced, amended, or\ncounted against",
        ],
    )
    def test_the_decision_states_its_boundaries(self, decision_text, claim):
        assert claim in decision_text

    @pytest.mark.parametrize(
        "step",
        ["§G.B steps 9, 10, or 11", "generating any external attestation", "consuming any part of `ATTEMPT_1`"],
    )
    def test_the_decision_withholds_steps_9_to_11(self, decision_text, step):
        assert step in decision_text

    # AMENDED BY XASSET-0038. This test asserted the state as of THIS FILING, whose own PR was
    # still open — accurate then, and the same self-referential shape as the sibling test below
    # that pins the PREDECESSOR (XASSET-0036) gate as merged. PR #337 has since merged with all
    # six REQUIRED_LIFECYCLE_GATES closed, so the successor filing lawfully flipped this gate to
    # `complete` / 337, exactly as THIS session flipped the xasset0036 gate below. Nothing is
    # weakened: the completed values are checked exactly, the gate's own DESCRIPTION TEXT is
    # asserted byte-preserved as history, and the successor's additive post-merge gate is checked
    # to exist rather than merely assumed.
    def test_the_register_records_the_rebinding_as_merged(self):
        register = yaml.safe_load(
            (ROOT / "operations/WORKSTREAMS.yaml").read_text(encoding="utf-8")
        )
        ws = [w for w in register["workstreams"] if w["id"] == "WS-0014"][0]
        gates = {g["gate"]: g for g in ws["milestones"]}
        rebinding = gates["xasset0037-successor-operational-rebinding"]
        assert rebinding["status"] == "complete"
        assert rebinding["pr"] == 337
        # The drafting session's own historical narrative is retained verbatim, not rewritten.
        assert "STEP 8" in rebinding["description"]
        assert "SS-G.B steps 9-11 were not performed" in rebinding["description"]
        # The successor records completion additively rather than by editing the text above.
        post_merge = gates["xasset0037-post-merge-verification"]
        assert post_merge["status"] == "complete"
        assert post_merge["pr"] == 337

    def test_the_register_records_the_package_implementation_as_merged(self):
        register = yaml.safe_load(
            (ROOT / "operations/WORKSTREAMS.yaml").read_text(encoding="utf-8")
        )
        ws = [w for w in register["workstreams"] if w["id"] == "WS-0014"][0]
        gates = {g["gate"]: g for g in ws["milestones"]}
        assert gates["xasset0036-gb-executable-package-implementation"]["status"] == "complete"
        assert gates["xasset0036-gb-executable-package-implementation"]["pr"] == 336
        assert gates["xasset0036-implementation-post-merge-verification"]["pr"] == 336




# ======================================================================================
# (13) MINOR 1 and MINOR 2 (review 4955010993)
# ======================================================================================


class TestReviewedMinorFindings:
    # --- MINOR 1: the durable register told a different history from every other surface ---

    @pytest.mark.parametrize(
        "relative",
        [
            "operations/WORKSTREAMS.yaml",
            "governance/decisions/"
            "XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md",
            "level1_stage1_execution_authorization.py",
        ],
    )
    def test_no_surface_claims_the_number_was_bound_after_the_draft(self, relative):
        """The false claim must not remain and must not return."""
        text = (ROOT / relative).read_text(encoding="utf-8").lower()
        collapsed = " ".join(text.split())
        assert "bound after the draft" not in collapsed, (
            f"{relative} still carries the false PR-number provenance"
        )

    @pytest.mark.parametrize(
        "relative",
        [
            "operations/WORKSTREAMS.yaml",
            "governance/decisions/"
            "XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md",
        ],
    )
    def test_every_surface_states_the_true_provenance(self, relative):
        """XASSET-0037's own surfaces, which describe XASSET-0037's own number.

        NARROWED BY XASSET-0047 -- in coverage of THIS phrase only, never in coverage of the
        property. ``level1_stage1_execution_authorization.py`` no longer carries XASSET-0037's
        number and must not carry XASSET-0037's provenance sentence for a number obtained a
        different way; its own current provenance is pinned, at both ends, by
        :meth:`TestObsoleteLifecycleCannotAuthorize.
        test_the_bound_pull_request_provenance_is_disclosed_not_flattered` and by
        :meth:`test_the_module_surface_states_its_own_current_provenance` immediately below, so
        no surface lost a provenance assertion. The two register/decision surfaces here are
        accepted history and are unchanged.
        """
        collapsed = " ".join(
            (ROOT / relative).read_text(encoding="utf-8").replace("#:", " ").replace("*", "").split()
        ).lower()
        assert "first written before the draft" in collapsed, relative
        assert "verified against the real draft" in collapsed, relative

    def test_the_module_surface_states_its_own_current_provenance(self):
        """The coverage the parametrisation above gave up, restored in its current true form.

        Written as its own test rather than as a third parameter because the module's provenance
        sentence is NOT the same sentence, and pretending it were is exactly the copy-forward this
        pair of guards exists to refuse.
        """
        collapsed = " ".join(
            (ROOT / "level1_stage1_execution_authorization.py")
            .read_text(encoding="utf-8")
            .replace("#:", " ")
            .replace("*", "")
            .split()
        ).lower()
        assert "not written in advance as the next sequential guess" in collapsed
        assert "read back from live github" in collapsed
        assert "first written before the draft" not in collapsed

    def test_the_register_names_the_verified_number(self):
        register = (ROOT / "operations/WORKSTREAMS.yaml").read_text(encoding="utf-8")
        assert "AUTHORIZING_PULL_REQUEST is 337" in register

    # --- MINOR 2: both rebinding mappings are exact closed schemas ---

    @pytest.fixture
    def canonical(self) -> dict:
        return yaml.safe_load(PREREG_PATH.read_text(encoding="utf-8"))

    def test_the_canonical_baseline_still_validates(self, canonical):
        assert PREREG.validate(canonical).ok

    def test_an_unknown_key_in_the_rebinding_block_is_rejected(self, canonical):
        canonical["stage_1_operational_authorization"]["successor_operational_rebinding"][
            "smuggled"
        ] = "value"
        result = PREREG.validate(canonical)
        assert not result.ok
        assert any("unexpected key(s)" in e for e in result.errors), result.errors

    def test_an_unknown_key_in_distinct_identities_is_rejected(self, canonical):
        canonical["stage_1_operational_authorization"]["successor_operational_rebinding"][
            "distinct_identities"
        ]["smuggled"] = "value"
        result = PREREG.validate(canonical)
        assert not result.ok
        assert any("unexpected key(s)" in e for e in result.errors), result.errors

    @pytest.mark.parametrize("key", list(PREREG.SUCCESSOR_REBINDING_KEYS))
    def test_a_missing_rebinding_key_is_rejected(self, canonical, key):
        del canonical["stage_1_operational_authorization"]["successor_operational_rebinding"][key]
        assert not PREREG.validate(canonical).ok

    @pytest.mark.parametrize("key", list(PREREG.SUCCESSOR_REBINDING_IDENTITY_KEYS))
    def test_a_missing_identity_key_is_rejected(self, canonical, key):
        del canonical["stage_1_operational_authorization"]["successor_operational_rebinding"][
            "distinct_identities"
        ][key]
        assert not PREREG.validate(canonical).ok

    def test_key_order_drift_is_rejected(self, canonical):
        block = canonical["stage_1_operational_authorization"]["successor_operational_rebinding"]
        block["distinct_identities"] = dict(reversed(list(block["distinct_identities"].items())))
        result = PREREG.validate(canonical)
        assert not result.ok
        assert any("key order differs" in e for e in result.errors), result.errors

    def test_the_identity_schema_still_names_exactly_four_relationships(self):
        assert len(PREREG.SUCCESSOR_REBINDING_IDENTITY_KEYS) == 4
        assert len(set(PREREG.SUCCESSOR_REBINDING_IDENTITY_KEYS)) == 4


def _with_module_level_line(text: str) -> str:
    """Insert one module-level statement immediately after the ``__future__`` import.

    Deliberately the smallest possible edit: it adds a line and touches nothing else, so any change
    in projected identity is attributable to that line alone.
    """
    lines = DERIVATION_SOURCE.splitlines(keepends=True)
    index = next(i for i, line in enumerate(lines) if line.startswith("from __future__ import"))
    mutated = "".join(lines[: index + 1] + [text] + lines[index + 1 :])
    assert mutated != DERIVATION_SOURCE
    return mutated


def _execute_derivation_in_subprocess(source: str) -> str:
    """Run a mutated derivation in a DISPOSABLE subprocess and return its disposition.

    Mandatory isolation, not caution: ``builtins.__dict__.update(any=min)`` mutates the running
    interpreter's own builtins. Executing it in-process would corrupt every later test in this
    session -- and would prove nothing about the module under test.
    """
    import subprocess
    import sys as _sys
    import tempfile
    import textwrap

    directory = Path(tempfile.mkdtemp())
    module_path = directory / "mutated_derivation.py"
    module_path.write_text(source, encoding="utf-8")
    driver = directory / "driver.py"
    driver.write_text(
        textwrap.dedent(
            """
            import importlib.util, sys
            spec = importlib.util.spec_from_file_location("mutated_derivation", sys.argv[1])
            module = importlib.util.module_from_spec(spec)
            sys.modules["mutated_derivation"] = module
            spec.loader.exec_module(module)
            gates = dict.fromkeys(module.GATE_IDS, "PASS")
            gates[sorted(module.CATEGORICAL_GATES)[0]] = "FAIL"
            print(module.derive_candidate_disposition(gates))
            """
        ).strip(),
        encoding="utf-8",
    )
    completed = subprocess.run(
        [_sys.executable, str(driver), str(module_path)],
        capture_output=True, text=True, cwd=str(ROOT), timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout.strip()


# ======================================================================================
# (12) The EXACT package-to-successor transition (architectural correction, review 4963386313)
# ======================================================================================


def _xasset_0037_load_bearing() -> tuple[str, ...]:
    """``LOAD_BEARING_RELPATHS`` AS XASSET-0037 ACCEPTED IT, read from the git object store.

    Added by XASSET-0044's re-anchoring. Two of the ten entries are ``Name`` references to the
    canonical relpath constants rather than string literals, so the tuple is resolved element by
    element from the module's own AST at that commit rather than ``literal_eval``'d whole.
    """
    import ast as _ast

    out = subprocess.run(
        ["git", "show",
         f"{A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA}:level1_stage1_execution_authorization.py"],
        cwd=ROOT, capture_output=True, check=False,
    )
    if out.returncode != 0:
        pytest.skip("the XASSET-0037 merge is unavailable in this checkout")
    tree = _ast.parse(out.stdout.decode("utf-8"))
    literals: dict[str, str] = {}
    paths: tuple[str, ...] | None = None
    for node in tree.body:
        if not isinstance(node, _ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, _ast.Name):
            continue
        if isinstance(node.value, _ast.Constant) and isinstance(node.value.value, str):
            literals[target.id] = node.value.value
        elif target.id == "LOAD_BEARING_RELPATHS" and isinstance(node.value, _ast.Tuple):
            resolved = []
            for element in node.value.elts:
                if isinstance(element, _ast.Constant):
                    resolved.append(element.value)
                elif isinstance(element, _ast.Name):
                    resolved.append(literals[element.id])
                else:  # pragma: no cover - defensive
                    raise AssertionError(f"unresolvable entry {_ast.dump(element)}")
            paths = tuple(resolved)
    assert paths is not None, "LOAD_BEARING_RELPATHS not found at the XASSET-0037 merge"
    return paths


def _package_blob() -> bytes:
    """The accepted executable-package blob, from the git object store."""
    return PACKAGE_SOURCE.encode("utf-8")


def _successor_blob() -> bytes:
    """The accepted SUCCESSOR blob, from the git object store at XASSET-0037's own merge.

    RE-ANCHORED BY XASSET-0044. This read the working tree, which was the accepted successor blob
    while XASSET-0037 was the current generation. XASSET-0044 lawfully rebound that file under
    XASSET-0030 SS-D, appending a second closed transition, so the working tree now carries the
    REBOUND bytes. XASSET-0037's accepted transition is unchanged and still fully proven here --
    against the immutable commit that actually carries its bytes.
    """
    out = subprocess.run(
        ["git", "show", f"{A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA}:{DERIVATION_RELPATH}"],
        cwd=ROOT, capture_output=True, check=False,
    )
    if out.returncode != 0:
        pytest.skip("the XASSET-0037 merge is unavailable in this checkout")
    return out.stdout


def _flip(data: bytes, at: int) -> bytes:
    return data[:at] + bytes([data[at] ^ 0x01]) + data[at + 1:]


class TestExactPackageToSuccessorTransition:
    """The authorization boundary is BYTES, and the proposition is finite.

    Review 4963386313 established that the predecessor semantic projection was NONCONVERGENT: to
    answer "did the outcome surface change" from source alone it had to decide arbitrary Python
    runtime behaviour statically, and four reviews closing sixteen bypass forms each produced more.
    The projection is retired. What replaces it is decidable:

        these exact accepted package bytes became these exact successor bytes
        through only this exact reviewed transition.

    No parsing, importing, executing, ``eval``, ``difflib``, or version-dependent diff algorithm
    participates in any assertion below.
    """

    # --- the transition itself ---

    def test_the_real_package_becomes_the_real_successor(self):
        A.verify_exact_transition(_package_blob(), _successor_blob())

    def test_the_pinned_identities_match_the_real_blobs(self):
        package, successor = _package_blob(), _successor_blob()
        assert A.sha256_bytes(package) == A.OUTCOME_PRODUCING_PACKAGE_SHA256
        assert A.sha256_bytes(successor) == A.OUTCOME_PRODUCING_SUCCESSOR_SHA256
        assert len(package) == A.OUTCOME_PRODUCING_PACKAGE_LENGTH
        assert len(successor) == A.OUTCOME_PRODUCING_SUCCESSOR_LENGTH

    def test_the_manifest_is_closed_and_consumes_both_files(self):
        """Ordered, non-overlapping, gapless, and complete -- checked here, not taken on trust."""
        package, successor = _package_blob(), _successor_blob()
        p_cursor = s_cursor = 0
        rebuilt = bytearray()
        for p_at, p_len, _pd, s_at, s_len, _sd in A.OUTCOME_PRODUCING_TRANSITION:
            assert p_at >= p_cursor and s_at >= s_cursor
            assert package[p_cursor:p_at] == successor[s_cursor:s_at]
            rebuilt += package[p_cursor:p_at]
            rebuilt += successor[s_at:s_at + s_len]
            p_cursor, s_cursor = p_at + p_len, s_at + s_len
        assert package[p_cursor:] == successor[s_cursor:]
        rebuilt += package[p_cursor:]
        assert bytes(rebuilt) == successor, "manifest does not reconstruct the successor exactly"

    def test_the_transition_declares_seventeen_reviewed_regions(self):
        assert len(A.OUTCOME_PRODUCING_TRANSITION) == 17

    # --- five-anchor enforcement through the PUBLIC validator ---

    def test_the_public_validator_accepts_the_exact_transition(self, payload):
        result = A.validate_authorization_document(payload, sources(git=FakeGit()))
        assert not [e for e in result.errors if DERIVATION_RELPATH in e], result.errors

    @pytest.mark.parametrize("anchor", ["package_head", "package_merge"])
    def test_a_package_anchor_must_carry_the_exact_package_blob(self, payload, anchor):
        commit = (A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD if anchor == "package_head"
                  else A.EXECUTABLE_PACKAGE_MERGE_SHA)
        git = FakeGit()
        git.texts[(commit, DERIVATION_RELPATH)] = _package_blob().decode("utf-8") + "\n# drift\n"
        _rejected(payload, DERIVATION_RELPATH, sources(git=git))

    @pytest.mark.parametrize("anchor", ["successor_head", "successor_merge"])
    def test_a_successor_anchor_must_carry_the_exact_successor_blob(self, payload, anchor):
        commit = HEAD if anchor == "successor_head" else MERGE
        git = FakeGit()
        git.texts[(commit, DERIVATION_RELPATH)] = DERIVATION_SOURCE + "\n# drift\n"
        _rejected(payload, DERIVATION_RELPATH, sources(git=git))

    @pytest.mark.parametrize("anchor", ["package_head", "package_merge", "successor_head",
                                        "successor_merge"])
    def test_an_unreadable_anchor_fails_closed(self, payload, anchor):
        commit = {"package_head": A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
                  "package_merge": A.EXECUTABLE_PACKAGE_MERGE_SHA,
                  "successor_head": HEAD, "successor_merge": MERGE}[anchor]
        git = FakeGit()
        git.texts[(commit, DERIVATION_RELPATH)] = None
        _rejected(payload, DERIVATION_RELPATH, sources(git=git))

    # --- one-byte mutations, inside and outside declared regions ---

    def test_a_one_byte_mutation_inside_a_declared_region_is_refused(self):
        package, successor = _package_blob(), _successor_blob()
        at = A.OUTCOME_PRODUCING_TRANSITION[0][3] + 1
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(package, _flip(successor, at))

    def test_a_one_byte_mutation_outside_every_declared_region_is_refused(self):
        package, successor = _package_blob(), _successor_blob()
        at = A.OUTCOME_PRODUCING_TRANSITION[0][3] - 50
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(package, _flip(successor, at))

    def test_a_one_byte_mutation_in_the_package_is_refused(self):
        package, successor = _package_blob(), _successor_blob()
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(_flip(package, 100), successor)

    @pytest.mark.parametrize("where", ["head", "middle", "tail"])
    def test_a_one_byte_successor_mutation_anywhere_is_refused(self, where):
        package, successor = _package_blob(), _successor_blob()
        at = {"head": 10, "middle": len(successor) // 2, "tail": len(successor) - 10}[where]
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(package, _flip(successor, at))

    def test_appended_and_truncated_bytes_are_refused(self):
        package, successor = _package_blob(), _successor_blob()
        for altered in (successor + b"# appended\n", successor[:-1]):
            with pytest.raises(A.TransitionError):
                A.verify_exact_transition(package, altered)

    # --- manifest tampering ---

    def _regions(self):
        return list(A.OUTCOME_PRODUCING_TRANSITION)

    def test_a_removed_region_is_refused(self):
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(_package_blob(), _successor_blob(), self._regions()[1:])

    def test_a_duplicated_region_is_refused(self):
        regions = self._regions()
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(_package_blob(), _successor_blob(), [regions[0]] + regions)

    def test_reordered_regions_are_refused(self):
        regions = self._regions()
        swapped = [regions[1], regions[0]] + regions[2:]
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(_package_blob(), _successor_blob(), swapped)

    @pytest.mark.parametrize("field,delta", [(1, 5), (1, -5), (4, 5), (4, -5)])
    def test_a_resized_region_is_refused(self, field, delta):
        regions = self._regions()
        first = list(regions[0]); first[field] += delta
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(_package_blob(), _successor_blob(),
                                      [tuple(first)] + regions[1:])

    @pytest.mark.parametrize("field", [0, 3])
    def test_a_wrong_offset_is_refused(self, field):
        regions = self._regions()
        first = list(regions[0]); first[field] += 1
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(_package_blob(), _successor_blob(),
                                      [tuple(first)] + regions[1:])

    @pytest.mark.parametrize("field,label", [(2, "before-digest"), (5, "after-digest")])
    def test_a_wrong_digest_is_refused(self, field, label):
        regions = self._regions()
        first = list(regions[0]); first[field] = "0" * 64
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(_package_blob(), _successor_blob(),
                                      [tuple(first)] + regions[1:])

    def test_an_overlapping_region_is_refused(self):
        regions = self._regions()
        a, b = list(regions[0]), list(regions[1])
        b[0] = a[0]; b[3] = a[3]          # start the second region where the first began
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(_package_blob(), _successor_blob(),
                                      [tuple(a), tuple(b)] + regions[2:])

    def test_an_empty_manifest_is_refused(self):
        with pytest.raises(A.TransitionError, match="empty"):
            A.verify_exact_transition(_package_blob(), _successor_blob(), [])

    # --- isolating checks that a companion check would otherwise mask ---

    def test_an_identical_edit_to_BOTH_blobs_still_fails_the_whole_blob_pins(self):
        """Isolates the whole-blob pins.

        Editing the same span in both files leaves every gap byte-identical, every region digest
        intact, and the trailing spans equal -- so the structural checks all pass and ONLY the
        pinned blob identities catch it. Without them, an attacker who could supply both anchors
        could move the pair anywhere.
        """
        package, successor = _package_blob(), _successor_blob()
        at = A.OUTCOME_PRODUCING_TRANSITION[0][0] - 40      # inside the shared leading span
        with pytest.raises(A.TransitionError, match="digest"):
            A.verify_exact_transition(_flip(package, at), _flip(successor, at))

    def test_dropping_the_LAST_region_is_refused_by_the_trailing_span_check(self):
        """Isolates the trailing-span check.

        Removing the first region is caught by gap identity; removing the LAST one is not -- the
        cursors simply stop early, and only the after-the-last-region comparison notices that the
        remainder of the two files disagrees.
        """
        with pytest.raises(A.TransitionError, match="after the last declared region"):
            A.verify_exact_transition(_package_blob(), _successor_blob(),
                                      self._regions()[:-1])

    def test_a_wrong_length_blob_is_refused_by_the_length_pins(self):
        """Defence in depth: subsumed by the digest pins for any real blob, pinned here anyway."""
        with pytest.raises(A.TransitionError, match="bytes, expected"):
            A.verify_exact_transition(_package_blob()[:-1], _successor_blob())
        with pytest.raises(A.TransitionError, match="bytes, expected"):
            A.verify_exact_transition(_package_blob(), _successor_blob()[:-1])

    def test_a_region_declaring_no_change_is_refused(self):
        empty = hashlib.sha256(b"").hexdigest()
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(
                _package_blob(), _successor_blob(),
                [(0, 0, empty, 0, 0, empty)] + self._regions(),
            )

    def test_a_malformed_region_is_refused(self):
        for bad in ((0, 0, "x"), (-1, 1, "a" * 64, 0, 1, "b" * 64), ("0", 1, "a" * 64, 0, 1, "b" * 64)):
            with pytest.raises((A.TransitionError, TypeError)):
                A.verify_exact_transition(_package_blob(), _successor_blob(), [bad])

    def test_a_region_past_the_end_of_its_file_is_refused(self):
        """Appended AFTER the real regions, so every gap still matches and only bounds can catch it.

        Placed first instead, the same region is caught by gap identity -- which would have left the
        bounds check unpinned while appearing to test it.
        """
        package, successor = _package_blob(), _successor_blob()
        empty = hashlib.sha256(b"").hexdigest()
        with pytest.raises(A.TransitionError, match="past the end"):
            A.verify_exact_transition(
                package, successor,
                self._regions() + [(len(package), 10, empty, len(successor), 10, empty)],
            )

    # --- the bypass families every prior review chased, now ordinary byte changes ---

    _BYPASS_FAMILIES = [
        # review 4963386313
        ("deferred-through-container-and-call-result",
         "import builtins as _rb\n_g = (_rb.__dict__.update(any=min) for _ in (1,))\n"
         "_box = (_g,)\n_c = list(next(iter(_box)))\n"),
        ("callback-to-higher-order-builtin",
         "import builtins as _rb\ndef _f(x):\n    _rb.__dict__.update(any=min)\n"
         "_c = list(map(_f, (1,)))\n"),
        ("attributed-local-class-member",
         "import builtins as _rb\nclass _D:\n    def run():\n        _rb.__dict__.update(any=min)\n"
         "_D.run()\n"),
        ("local-class-attribute-decorator",
         "import builtins as _rb\nclass _D:\n    def deco(f):\n        _rb.__dict__.update(any=min)\n"
         "        return f\n@_D.deco\ndef _x():\n    pass\n"),
        ("init-subclass-creation-hook",
         "import builtins as _rb\nclass _Base:\n    def __init_subclass__(cls):\n"
         "        _rb.__dict__.update(any=min)\nclass _Sub(_Base):\n    pass\n"),
        # review 4962377217
        ("generator-aliased-then-consumed",
         "import builtins as _rb\n_g = (_rb.__dict__.update(any=min) for _i in (1,))\n_c = list(_g)\n"),
        ("lambda-decorator",
         "import builtins as _rb\n@(lambda _f: (_rb.__dict__.update(any=min), _f)[1])\n"
         "def _d():\n    pass\n"),
        ("class-constructor", "import builtins as _rb\nclass _C:\n    def __init__(self):\n"
         "        _rb.__dict__.update(any=min)\n_i = _C()\n"),
        ("conditional-duplicate-definitions",
         "import builtins as _rb\nif True:\n    def _p():\n        _rb.__dict__.update(any=min)\n"
         "else:\n    def _p():\n        pass\n_p()\n"),
        ("namespace-in-container-subscript",
         "import builtins as _rb\nfrom operator import setitem as _si\n_b = (_rb.__dict__,)\n"
         "_si(_b[0], 'any', min)\n"),
        # reviews 4958940810 / 4960897843 / 4961431702 / 4957056810
        ("direct-namespace-update", "import builtins as _rb\n_rb.__dict__.update(any=min)\n"),
        ("helper-called-eagerly",
         "import builtins as _rb\ndef _h():\n    _rb.__dict__.update(any=min)\n_h()\n"),
        ("class-body-mutation",
         "import builtins as _rb\nclass _P:\n    _rb.__dict__.update(any=min)\n"),
        ("exec-alias", "_e = exec\n_e('any=min')\n"),
        ("getattr-call", "import builtins as _rb\ngetattr(_rb, 'exec')('any=min')\n"),
        ("conditional-import", "if True:\n    from builtins import min as any\n"),
        ("destructuring-rebinding", "any, _unused = min, None\n"),
    ]

    @pytest.mark.parametrize("label,block", _BYPASS_FAMILIES,
                             ids=[e[0] for e in _BYPASS_FAMILIES])
    def test_every_bypass_family_is_refused_as_an_ordinary_byte_change(self, label, block):
        """No analyzer decides these. They are simply not the reviewed successor bytes.

        This is the architectural point: sixteen forms that each required their own semantic
        modelling are now one case, and a seventeenth nobody has thought of is the same case.
        """
        mutated = _with_module_level_line(block).encode("utf-8")
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(_package_blob(), mutated)

    @pytest.mark.parametrize("label,block", _BYPASS_FAMILIES,
                             ids=[e[0] for e in _BYPASS_FAMILIES])
    def test_the_public_validator_refuses_every_bypass_family(self, payload, label, block):
        mutated = _with_module_level_line(block)
        git = FakeGit()
        git.texts[(HEAD, DERIVATION_RELPATH)] = mutated
        git.texts[(MERGE, DERIVATION_RELPATH)] = mutated
        _rejected(payload, DERIVATION_RELPATH, sources(git=git))

    # --- what the reviewed transition actually contains ---

    #: The complete transitive outcome-consumed surface, stated as an INDEPENDENT expectation.
    #:
    #: MINOR 1 (FULL review 4965914272): the predecessor test derived the 18 direct consumer seeds
    #: and compared only those 18 definitions, while the decision and report claimed all 26
    #: transitive symbols were verified. Eight symbols the consumers reach only INDIRECTLY --
    #: ``BOUNDS``, ``CANDIDATE_DISPOSITIONS``, ``CELL_OUTCOMES``, ``CONSTRUCTION_FAMILIES``,
    #: ``DRIVER_CLASSES``, ``cell_id_of``, ``generate_family_slot_grid`` and ``map_g2_reading`` --
    #: were never compared. The closure is now computed here to a fixed point over BOTH exact blobs
    #: and every definition in it is compared.
    #:
    #: This literal is written out so the closure computation has an oracle that is neither the
    #: production declaration nor the governance claim. It is checked in BOTH directions: the
    #: computed closure must equal it exactly.
    _EXPECTED_TRANSITIVE_SURFACE = frozenset({
        "BOUNDS",
        "CANDIDATE_DISPOSITIONS",
        "CATEGORICAL_GATES",
        "CELL_OUTCOMES",
        "CONSTRUCTION_FAMILIES",
        "DERIVED_IDENTITIES",
        "DRIVER_CLASSES",
        "G2_RECORD_REJECTED",
        "GATE_IDS",
        "GATE_RESULT_VOCABULARY",
        "POINT_RANGE_VALUES",
        "PREREQUISITE_GATES",
        "READING_VOCABULARY",
        "REGISTERED_CONSTRUCTION_COUNT",
        "REQUIRED_CANDIDATE_RESULT_KEYS",
        "SLEEVES",
        "ValidationResult",
        "cell_id_of",
        "derive_candidate_disposition",
        "derive_cell_outcome",
        "derive_roll_up_outcome",
        "generate_cell_universe",
        "generate_family_slot_grid",
        "is_reading_dependent",
        "map_g2_reading",
        "required_g2_gate_result",
    })

    @staticmethod
    def _top_level_table(source: str):
        """Every top-level definition in one blob, by bound name. Test-only; no production code."""
        import ast as _ast

        out = {}
        for node in _ast.parse(source).body:
            if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef)):
                out[node.name] = node
            elif isinstance(node, _ast.Assign):
                for target in node.targets:
                    if isinstance(target, _ast.Name):
                        out[target.id] = node
            elif isinstance(node, _ast.AnnAssign) and isinstance(node.target, _ast.Name):
                out[node.target.id] = node
        return out

    @classmethod
    def _transitive_closure(cls, seeds, table):
        """Close ``seeds`` over top-level names referenced inside their own definitions.

        Iterated to a FIXED POINT, so a symbol reached only through several hops is included.

        STRICT in the seeds: a consumed symbol that is absent from the blob is an error, never a
        silent omission. Filtering it out instead would make a DELETED outcome-consumed definition
        invisible to the comparison below -- the precise failure mode this test exists to prevent.
        """
        import ast as _ast

        absent = sorted(name for name in seeds if name not in table)
        assert absent == [], f"consumed symbols absent from the blob: {absent}"
        closure = set(seeds)
        while True:
            discovered = set()
            for name in closure:
                for node in _ast.walk(table[name]):
                    if isinstance(node, _ast.Name) and node.id in table:
                        discovered.add(node.id)
                    elif isinstance(node, _ast.Attribute) and node.attr in table:
                        discovered.add(node.attr)
            if discovered <= closure:
                return closure
            closure |= discovered

    def test_the_direct_consumer_seed_set_is_eighteen_symbols(self):
        """Derived from the runner and result validator, never from a production declaration."""
        seeds = _independently_derived_seed_symbols()
        assert len(seeds) == 18, sorted(seeds)
        assert seeds <= self._EXPECTED_TRANSITIVE_SURFACE

    def test_the_transitive_closure_is_exactly_the_twenty_six_symbol_surface(self):
        """Computed independently in BOTH blobs, and equal to the stated surface in each."""
        seeds = _independently_derived_seed_symbols()
        for label, blob in (
            ("package", _package_blob()),
            ("successor", _successor_blob()),
        ):
            table = self._top_level_table(blob.decode("utf-8"))
            closure = self._transitive_closure(seeds, table)
            assert closure == self._EXPECTED_TRANSITIVE_SURFACE, (
                f"{label} closure differs: "
                f"missing={sorted(self._EXPECTED_TRANSITIVE_SURFACE - closure)} "
                f"unexpected={sorted(closure - self._EXPECTED_TRANSITIVE_SURFACE)}"
            )
            assert len(closure) == 26, f"{label}: {len(closure)}"

    def test_the_closure_strictly_exceeds_the_direct_seeds(self):
        """The precise gap MINOR 1 reported: eight symbols reached only indirectly.

        Derived from the COMPUTED closure, not by subtracting two constants -- otherwise a
        degenerate closure would still satisfy this test and the gap would go unmeasured.
        """
        seeds = _independently_derived_seed_symbols()
        table = self._top_level_table(_successor_blob().decode("utf-8"))
        closure = self._transitive_closure(seeds, table)
        assert seeds < closure, "the closure reached nothing the direct seeds did not"
        indirect = closure - seeds
        assert len(indirect) == 8
        assert indirect == {
            "BOUNDS", "CANDIDATE_DISPOSITIONS", "CELL_OUTCOMES", "CONSTRUCTION_FAMILIES",
            "DRIVER_CLASSES", "cell_id_of", "generate_family_slot_grid", "map_g2_reading",
        }, sorted(indirect)

    def test_no_outcome_consumed_symbol_changed_across_the_transition(self):
        """Evidence, not authorization: the seventeen regions touch authorization-only code.

        MINOR 1 (FULL review 4965914272) corrected. Every definition in the COMPLETE transitive
        closure is compared, not just the 18 direct seeds. The seeds are re-derived from the
        CONSUMERS' own source and the closure is computed here, so neither the manifest, nor any
        production declaration, nor the governance claim is its own oracle. Authorization remains
        byte-exact; this test records what those reviewed bytes mean.
        """
        import ast as _ast

        seeds = _independently_derived_seed_symbols()
        assert seeds, "no consumed symbols were derived"

        package = self._top_level_table(_package_blob().decode("utf-8"))
        successor = self._top_level_table(_successor_blob().decode("utf-8"))
        closure = self._transitive_closure(seeds, successor)
        assert closure == self._EXPECTED_TRANSITIVE_SURFACE
        assert len(closure) == 26

        missing = sorted(name for name in closure if name not in package or name not in successor)
        assert missing == [], f"closure symbols absent from a blob: {missing}"
        changed = [
            name
            for name in sorted(closure)
            if _ast.dump(package[name]) != _ast.dump(successor[name])
        ]
        assert changed == [], f"outcome-consumed definitions changed: {changed}"

    def test_representative_bypasses_would_have_changed_a_real_disposition(self):
        """Disposable evidence only -- never part of the authorization proof, never the real lane.

        Retiring the analyzer does not mean these forms became harmless; it means byte identity
        refuses them without anyone having to model why.
        """
        gate_results = dict.fromkeys(PREREG.GATE_IDS, "PASS")
        gate_results[sorted(PREREG.CATEGORICAL_GATES)[0]] = "FAIL"
        assert PREREG.derive_candidate_disposition(gate_results) == "BLOCKED_CATEGORICALLY"
        for _label, block in self._BYPASS_FAMILIES[:3]:
            assert (
                _execute_derivation_in_subprocess(_with_module_level_line(block))
                == "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"
            )

    # --- the retired mechanism is genuinely gone ---

    @pytest.mark.parametrize("symbol", [
        "ProjectionError", "OUTCOME_PRODUCING_PROJECTION_SEEDS",
        "project_outcome_producing_surface", "outcome_producing_projection_digest",
        "_module_scope_binders", "_symtable_module_globals", "_value_origins", "_name_origins",
        "_build_module_scope_context", "_origin_is_safe_callee", "_deferred_values_for_name",
        "_iter_eager_module_scope_nodes", "_reject_dynamic_namespace_mutation",
        "_reject_call_mediated_namespace_mutation", "_SAFE_BUILTIN_CALLABLES",
        "_SAFE_IMPORTED_CALLABLES", "_PROJECTION_BEARING_MODULES",
        "_NAMESPACE_EXPOSING_ATTRIBUTES", "_verify_outcome_producing_projection",
    ])
    def test_the_retired_projection_subsystem_is_absent(self, symbol):
        """One authoritative mechanism, not two competing authorization paths."""
        assert not hasattr(A, symbol), f"{symbol} survived the architectural correction"

    def test_the_authorization_module_no_longer_parses_or_executes_the_audited_module(self):
        """Checked against EXECUTABLE code, not prose -- the rationale legitimately names them."""
        import ast as _ast

        source = (ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        tree = _ast.parse(source)
        imported = {
            alias.name.split(".")[0]
            for node in _ast.walk(tree)
            if isinstance(node, _ast.Import)
            for alias in node.names
        } | {
            node.module.split(".")[0]
            for node in _ast.walk(tree)
            if isinstance(node, _ast.ImportFrom) and node.module
        }
        for banned in ("ast", "symtable", "difflib"):
            assert banned not in imported, f"{banned} is still imported"
        called = {
            node.func.id
            for node in _ast.walk(tree)
            if isinstance(node, _ast.Call) and isinstance(node.func, _ast.Name)
        }
        for banned in ("eval", "exec", "compile", "__import__"):
            assert banned not in called, f"{banned}() is still called"


# ======================================================================================
# (13) MAJOR 1 (FULL review 4965914272) — the construction-universe module joins the
#      exact FIVE-ANCHOR executable-package equality boundary
# ======================================================================================

#: The direct outcome-producing dependency the reviewed head left outside the package boundary.
CONSTRUCTION_UNIVERSE_RELPATH = "level1_construction_universe_closure_validator.py"

#: Its verified identity, unchanged from the accepted package through this head. Asserted against
#: the real git objects below rather than trusted as a literal.
CONSTRUCTION_UNIVERSE_SHA256 = (
    "1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5"
)


class TestConstructionUniverseIsPackageBound:
    """MAJOR 1 (FULL review 4965914272): a direct consumer dependency was unproven at the package.

    ``level1_stage1_runner.py`` imports this module as ``CU`` and calls
    ``generate_construction_universe``, ``frozen_construction_universe`` and
    ``universe_aggregate_sha256`` — the actual 680-cell traversal, its exact order, the frozen
    mapping, the per-construction identities, and the aggregate hash. ``level1_stage1_result_validator.py``
    consumes the same module.

    It was already load-bearing, but that boundary compares only the successor's reviewed head, the
    successor's merge, and the working tree. **The two EXECUTABLE-PACKAGE anchors did not prove it.**
    Reproduced through the real mechanism before correcting: withholding its blob at both package
    anchors, with every other input valid, ``_verify_successor_rebinding_identity`` returned ``[]``.

    Each test below perturbs exactly ONE anchor and leaves every other load-bearing declaration
    coherent, so a generic earlier failure cannot mask the component under test, and each asserts the
    RELEVANT error rather than merely ``valid=False``.
    """

    def test_it_is_now_inside_the_exact_package_equality_boundary(self):
        assert (
            CONSTRUCTION_UNIVERSE_RELPATH in A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS
        ), "the construction-universe module must be package-bound, not merely load-bearing"

    def test_the_load_bearing_boundary_is_unchanged_at_ten_paths(self):
        """The correction ADDS a package binding; it removes nothing.

        RE-ANCHORED BY XASSET-0044: proven against XASSET-0037's own accepted boundary, with the
        removes-nothing property additionally asserted against the live set.
        """
        assert CONSTRUCTION_UNIVERSE_RELPATH in _xasset_0037_load_bearing()
        assert len(_xasset_0037_load_bearing()) == 10
        assert len(set(_xasset_0037_load_bearing())) == 10
        assert CONSTRUCTION_UNIVERSE_RELPATH in A.LOAD_BEARING_RELPATHS
        assert set(_xasset_0037_load_bearing()) <= set(A.LOAD_BEARING_RELPATHS)

    def test_the_consumers_really_do_import_it(self):
        """The premise, re-derived from the consumers rather than asserted."""
        import ast as _ast

        for relative in ("level1_stage1_runner.py", "level1_stage1_result_validator.py"):
            tree = _ast.parse((ROOT / relative).read_text(encoding="utf-8"))
            imported = {
                entry.name
                for node in _ast.walk(tree)
                if isinstance(node, _ast.Import)
                for entry in node.names
            }
            assert "level1_construction_universe_closure_validator" in imported, relative

    def test_its_live_bytes_match_the_accepted_package_and_the_recorded_identity(self):
        """Not synthetic: the real working tree against the real merged package."""
        git = A.LiveGitTruthSource()
        live = A.sha256_file(ROOT / CONSTRUCTION_UNIVERSE_RELPATH)
        assert live == CONSTRUCTION_UNIVERSE_SHA256
        for anchor in (
            A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
            A.EXECUTABLE_PACKAGE_MERGE_SHA,
        ):
            assert git.blob_sha256_at(anchor, CONSTRUCTION_UNIVERSE_RELPATH) == live

    # --- the eight required anchor cases, each independently diagnostic ---

    @pytest.mark.parametrize(
        "anchor",
        ["package_accepted_head", "package_merge"],
        ids=["missing-at-package-accepted-head", "missing-at-package-merge"],
    )
    def test_a_missing_construction_universe_blob_at_a_package_anchor_fails_closed(
        self, payload, anchor
    ):
        commit = {
            "package_accepted_head": A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
            "package_merge": A.EXECUTABLE_PACKAGE_MERGE_SHA,
        }[anchor]
        git = FakeGit()
        del git.blobs[(commit, CONSTRUCTION_UNIVERSE_RELPATH)]
        _rejected(payload, "the outcome-producing bytes being rebound", sources(git=git))

    @pytest.mark.parametrize(
        "anchor",
        ["package_accepted_head", "package_merge", "successor_head", "successor_merge"],
        ids=[
            "mismatched-at-package-accepted-head",
            "mismatched-at-package-merge",
            "mismatched-at-successor-head",
            "mismatched-at-successor-merge",
        ],
    )
    def test_a_mismatched_construction_universe_blob_at_any_commit_anchor_fails_closed(
        self, payload, anchor
    ):
        commit = {
            "package_accepted_head": A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
            "package_merge": A.EXECUTABLE_PACKAGE_MERGE_SHA,
            "successor_head": HEAD,
            "successor_merge": MERGE,
        }[anchor]
        git = FakeGit()
        git.blobs[(commit, CONSTRUCTION_UNIVERSE_RELPATH)] = "0" * 64
        result = A.validate_authorization_document(payload, sources(git=git))
        assert not result.valid
        assert any(
            CONSTRUCTION_UNIVERSE_RELPATH in error for error in result.errors
        ), f"no error named the construction-universe module: {result.errors}"

    def test_a_mismatched_construction_universe_blob_in_the_working_tree_fails_closed(
        self, payload, tmp_path, monkeypatch
    ):
        """The fifth anchor. The real file is never touched; only the ROOT the check reads is."""
        shadow = tmp_path / "shadow"
        shadow.mkdir()
        for relative in A.LOAD_BEARING_RELPATHS:
            target = shadow / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())
        (shadow / CONSTRUCTION_UNIVERSE_RELPATH).write_text(
            (ROOT / CONSTRUCTION_UNIVERSE_RELPATH).read_text(encoding="utf-8") + "\n# drift\n",
            encoding="utf-8",
        )
        monkeypatch.setattr(A, "ROOT", shadow)
        result = A.validate_authorization_document(payload, sources(git=FakeGit()))
        assert not result.valid
        assert any(
            CONSTRUCTION_UNIVERSE_RELPATH in error for error in result.errors
        ), f"no error named the construction-universe module: {result.errors}"
        assert (
            A.sha256_file(ROOT / CONSTRUCTION_UNIVERSE_RELPATH) == CONSTRUCTION_UNIVERSE_SHA256
        ), "the real construction-universe module must remain untouched"

    def test_the_happy_path_is_still_accepted(self, payload):
        """Precision: with every anchor coherent, the added binding refuses nothing."""
        result = A.validate_authorization_document(payload, sources(git=FakeGit()))
        assert not [
            error for error in result.errors if CONSTRUCTION_UNIVERSE_RELPATH in error
        ], result.errors

    def test_each_anchor_is_independently_diagnostic(self, payload):
        """Perturbing ONE anchor must not be masked by, or masquerade as, another failure."""
        for commit in (
            A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
            A.EXECUTABLE_PACKAGE_MERGE_SHA,
            HEAD,
            MERGE,
        ):
            git = FakeGit()
            git.blobs[(commit, CONSTRUCTION_UNIVERSE_RELPATH)] = "0" * 64
            named = [
                error
                for error in A.validate_authorization_document(
                    payload, sources(git=git)
                ).errors
                if CONSTRUCTION_UNIVERSE_RELPATH in error
            ]
            assert named, f"anchor {commit} produced no construction-universe error"
