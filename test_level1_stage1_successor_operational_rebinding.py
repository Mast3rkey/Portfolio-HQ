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
        }
        self._head = MERGE
        self._ancestor = True
        self.__dict__.update(overrides)

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
        }
        self.runs = {RUN_ID: {"status": "completed", "conclusion": "success", "head_sha": MERGE}}
        self.jobs = {JOB_ID: {"run_id": RUN_ID, "conclusion": "success", "head_sha": MERGE}}
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
        absent = [
            rel
            for rel in A.LOAD_BEARING_RELPATHS
            if git.blob_sha256_at(A.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA, rel) is None
        ]
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
        assert A.AUTHORIZING_DECISION == "XASSET-0037"
        assert A.HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION == "XASSET-0029"
        assert A.AUTHORIZING_DECISION != A.HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION


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
        """Not assumed: the successor branches from exactly the package it binds."""
        assert A.REVIEWED_BASE_SHA == A.EXECUTABLE_PACKAGE_MERGE_SHA

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
        additions = set(A.LOAD_BEARING_RELPATHS) - set(PACKAGE_LOAD_BEARING)
        assert additions == {
            "governance/decisions/"
            "XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md"
        }

    def test_the_set_grew_from_nine_to_ten(self):
        assert len(PACKAGE_LOAD_BEARING) == 9
        assert len(A.LOAD_BEARING_RELPATHS) == 10
        assert len(set(A.LOAD_BEARING_RELPATHS)) == 10

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
        effectivity = prereg["lifecycle_effectivity"]
        assert effectivity["stage_1_execution_may_begin_only_after"].startswith("XASSET_0037_")
        assert effectivity["stage_1_execution_precondition_amended_by"] == "XASSET-0037"
        assert prereg["stages"]["stage_1"]["executable_only_after"].startswith("XASSET_0037_")
        assert prereg["stage_1_executability"]["blocking_prerequisite"].startswith("XASSET_0037_")

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
        assert block["established_by"] == "XASSET-0029"
        assert block["rebound_by"] == "XASSET-0037"
        assert block["effective_structural_authorization_source"] == "XASSET-0037"

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
        forged = decision_text.replace(
            A.CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH], "0" * 64
        )
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

    def test_the_register_records_the_rebinding_as_in_progress(self):
        register = yaml.safe_load(
            (ROOT / "operations/WORKSTREAMS.yaml").read_text(encoding="utf-8")
        )
        ws = [w for w in register["workstreams"] if w["id"] == "WS-0014"][0]
        gates = {g["gate"]: g for g in ws["milestones"]}
        assert gates["xasset0037-successor-operational-rebinding"]["status"] == "in_progress"
        assert gates["xasset0037-successor-operational-rebinding"]["pr"] is None

    def test_the_register_records_the_package_implementation_as_merged(self):
        register = yaml.safe_load(
            (ROOT / "operations/WORKSTREAMS.yaml").read_text(encoding="utf-8")
        )
        ws = [w for w in register["workstreams"] if w["id"] == "WS-0014"][0]
        gates = {g["gate"]: g for g in ws["milestones"]}
        assert gates["xasset0036-gb-executable-package-implementation"]["status"] == "complete"
        assert gates["xasset0036-gb-executable-package-implementation"]["pr"] == 336
        assert gates["xasset0036-implementation-post-merge-verification"]["pr"] == 336
