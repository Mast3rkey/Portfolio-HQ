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

#: The module whose imported derivation surface MAJOR 1 (review 4955010993) requires be bound.
DERIVATION_RELPATH = "level1_endpoint_evidence_preregistration_validator.py"
DERIVATION_SOURCE = (ROOT / DERIVATION_RELPATH).read_text(encoding="utf-8")


def _independently_derived_seed_symbols() -> set[str]:
    """Re-derive the outcome-producing seed set from the CONSUMERS' own source, by AST.

    Deliberately NOT read from ``A.OUTCOME_PRODUCING_PROJECTION_SEEDS``: the review's explicit
    requirement is that the production tuple must not be its own test oracle. This walks
    ``level1_stage1_runner.py`` and ``level1_stage1_result_validator.py``, finds whatever alias each
    binds the derivation module to, and collects every attribute actually accessed through it. If a
    future edit starts consuming a new derivation symbol without declaring it, the equality
    assertion below fails.
    """
    import ast

    found: set[str] = set()
    for relative in A.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS:
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
        # MAJOR 1 (review 4955010993): the projection needs blob TEXT, not a digest. The stand-in
        # serves the module's real current source at every anchor, so the default posture is the
        # true one and each negative test perturbs exactly one anchor.
        self.texts = {
            (commit, DERIVATION_RELPATH): DERIVATION_SOURCE
            for commit in (
                MERGE,
                HEAD,
                A.EXECUTABLE_PACKAGE_MERGE_SHA,
                A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
            )
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

    def test_the_bound_pull_request_is_the_successors_own(self):
        """Verified against the real draft after it was opened; see the constant's provenance note."""
        assert A.AUTHORIZING_PULL_REQUEST == 337
        assert A.AUTHORIZING_PULL_REQUEST != A.HISTORICAL_OPERATIONAL_AUTHORIZATION_PULL_REQUEST
        assert A.AUTHORIZING_PULL_REQUEST != A.PACKAGE_AUTHORIZING_PULL_REQUEST
        assert A.AUTHORIZING_PULL_REQUEST != A.EXECUTABLE_PACKAGE_PULL_REQUEST

    def test_the_bound_pull_request_provenance_is_disclosed_not_flattered(self):
        """The constant must not claim an authoring order it did not have."""
        raw = (ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        # The note is a wrapped comment block, so compare on content rather than line breaks.
        source = " ".join(raw.replace("#:", " ").split())
        assert "FIRST WRITTEN before the draft pull request existed" in source
        assert "VERIFIED against the real draft once it was opened" in source
        assert "The load-bearing property is the verification, not the authoring order" in source


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


# ======================================================================================
# (12) MAJOR 1 (review 4955010993) — the TRANSITIVE outcome-producing surface
# ======================================================================================


class TestOutcomeProducingProjection:
    """The imported derivation surface must be bound, not merely the two declared files.

    The reviewed head's defect: injecting different package-anchor bytes for
    ``level1_endpoint_evidence_preregistration_validator.py`` returned ``valid=True`` with
    ``errors=()``, while the identical mismatch on either declared path was refused. These tests
    pin the corrected boundary and its nearest overreaches.
    """

    # --- the seed set is independently derived, never read from the production tuple ---

    def test_the_declared_seeds_equal_the_independently_derived_consumption(self):
        """Non-circular: the production tuple is checked against the consumers' real source."""
        derived = _independently_derived_seed_symbols()
        assert set(A.OUTCOME_PRODUCING_PROJECTION_SEEDS) == derived, (
            "declared outcome-producing seeds disagree with what the runner and result validator "
            f"actually consume; declared-only={set(A.OUTCOME_PRODUCING_PROJECTION_SEEDS) - derived}, "
            f"consumed-only={derived - set(A.OUTCOME_PRODUCING_PROJECTION_SEEDS)}"
        )

    def test_every_declared_seed_exists_in_the_derivation_module(self):
        surface = A.project_outcome_producing_surface(DERIVATION_SOURCE)
        for seed in A.OUTCOME_PRODUCING_PROJECTION_SEEDS:
            assert f"{seed}::" in surface, f"{seed} absent from the projection"

    def test_the_projection_is_transitively_closed_beyond_the_seeds(self):
        """A seed's own module-level dependencies are part of the surface, not stopped at the edge."""
        projected = {
            line.split("::", 1)[0]
            for line in A.project_outcome_producing_surface(DERIVATION_SOURCE).splitlines()
        }
        assert projected > set(A.OUTCOME_PRODUCING_PROJECTION_SEEDS)
        # Real transitive dependencies of the seeds, named independently of the implementation.
        for dependency in ("SLEEVES", "BOUNDS", "DRIVER_CLASSES", "CONSTRUCTION_FAMILIES",
                           "CANDIDATE_DISPOSITIONS", "CELL_OUTCOMES", "cell_id_of",
                           "generate_family_slot_grid", "map_g2_reading"):
            assert dependency in projected, f"{dependency} missing from the transitive closure"

    # --- determinism and fail-closed behaviour ---

    def test_the_projection_is_deterministic(self):
        first = A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        for _ in range(3):
            assert A.outcome_producing_projection_digest(DERIVATION_SOURCE) == first

    def test_reordering_definitions_does_not_change_identity(self):
        """Identity is the SURFACE, not the file layout — otherwise the check is byte equality."""
        assert A.outcome_producing_projection_digest(DERIVATION_SOURCE) == (
            A.outcome_producing_projection_digest(DERIVATION_SOURCE + "\n\nUNRELATED = 1\n")
        )

    def test_a_docstring_only_edit_does_not_trip_the_projection(self):
        """The one deliberate, disclosed exclusion: prose cannot decide an outcome."""
        mutated = DERIVATION_SOURCE.replace(
            '"""Aggregate identity hash of the XASSET-0028 construction universe, recomputed live.',
            '"""AGGREGATE identity hash of the XASSET-0028 construction universe, recomputed live.',
            1,
        )
        assert mutated != DERIVATION_SOURCE
        assert A.outcome_producing_projection_digest(mutated) == (
            A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        )

    @pytest.mark.parametrize(
        ("old", "new"),
        [
            ("REGISTERED_CONSTRUCTION_COUNT = 680", "REGISTERED_CONSTRUCTION_COUNT = 679"),
            ("def derive_candidate_disposition(", "def derive_candidate_disposition_X("),
            ("def derive_cell_outcome(", "def derive_cell_outcome_X("),
            ("def generate_cell_universe(", "def generate_cell_universe_X("),
        ],
    )
    def test_a_real_semantic_edit_does_change_identity_or_fails_closed(self, old, new):
        mutated = DERIVATION_SOURCE.replace(old, new, 1)
        assert mutated != DERIVATION_SOURCE, f"fixture did not mutate: {old!r}"
        try:
            assert A.outcome_producing_projection_digest(mutated) != (
                A.outcome_producing_projection_digest(DERIVATION_SOURCE)
            )
        except A.ProjectionError:
            pass  # a renamed seed fails closed, which is the stronger outcome

    def test_a_missing_seed_fails_closed(self):
        with pytest.raises(A.ProjectionError, match="absent or renamed"):
            A.project_outcome_producing_surface(
                DERIVATION_SOURCE, seeds=("NoSuchSymbolAnywhere",)
            )

    def test_an_empty_seed_set_fails_closed(self):
        with pytest.raises(A.ProjectionError, match="seed set is empty"):
            A.project_outcome_producing_surface(DERIVATION_SOURCE, seeds=())

    def test_unparseable_source_fails_closed(self):
        with pytest.raises(A.ProjectionError, match="does not parse"):
            A.project_outcome_producing_surface("def broken(:\n")

    def test_a_duplicated_top_level_symbol_fails_closed(self):
        """An ambiguous surface is refused rather than silently resolved to the last definition."""
        mutated = DERIVATION_SOURCE + "\n\nREGISTERED_CONSTRUCTION_COUNT = 1\n"
        with pytest.raises(A.ProjectionError, match="defined more than once"):
            A.project_outcome_producing_surface(mutated)

    # --- the real corpus: identical to the accepted PR #336 package ---

    @pytest.mark.parametrize(
        "anchor",
        ["EXECUTABLE_PACKAGE_ACCEPTED_HEAD", "EXECUTABLE_PACKAGE_MERGE_SHA"],
    )
    def test_the_live_projection_is_identical_to_the_accepted_package(self, anchor):
        """Against real git, not a stand-in: this rebinding changed no outcome-producing semantics."""
        git = A.LiveGitTruthSource()
        source = git.blob_text_at(getattr(A, anchor), DERIVATION_RELPATH)
        assert source is not None, f"{DERIVATION_RELPATH} unreadable at {anchor}"
        assert A.outcome_producing_projection_digest(source) == (
            A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        )

    def test_the_live_projection_is_identical_at_the_successor_head(self):
        git = A.LiveGitTruthSource()
        source = git.blob_text_at("HEAD", DERIVATION_RELPATH)
        assert source is not None
        assert A.outcome_producing_projection_digest(source) == (
            A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        )

    # --- the adversarial mutation proof through the REAL public validator ---

    def test_the_reviewed_head_defect_is_closed(self, payload):
        """The exact injection that previously returned valid=True with errors=()."""
        mutated = DERIVATION_SOURCE.replace(
            "REGISTERED_CONSTRUCTION_COUNT = 680", "REGISTERED_CONSTRUCTION_COUNT = 679", 1
        )
        assert mutated != DERIVATION_SOURCE
        git = FakeGit()
        git.texts[(A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, DERIVATION_RELPATH)] = mutated
        git.texts[(A.EXECUTABLE_PACKAGE_MERGE_SHA, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection drift", sources(git=git))

    @pytest.mark.parametrize(
        "anchor",
        ["EXECUTABLE_PACKAGE_ACCEPTED_HEAD", "EXECUTABLE_PACKAGE_MERGE_SHA"],
    )
    def test_drift_at_either_package_anchor_alone_is_rejected(self, payload, anchor):
        mutated = DERIVATION_SOURCE.replace(
            "REGISTERED_CONSTRUCTION_COUNT = 680", "REGISTERED_CONSTRUCTION_COUNT = 678", 1
        )
        git = FakeGit()
        git.texts[(getattr(A, anchor), DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection drift", sources(git=git))

    def test_drift_introduced_at_the_successor_head_is_rejected(self, payload):
        """Symmetric: the rebinding may not quietly alter the surface it is binding either."""
        mutated = DERIVATION_SOURCE.replace(
            "REGISTERED_CONSTRUCTION_COUNT = 680", "REGISTERED_CONSTRUCTION_COUNT = 677", 1
        )
        git = FakeGit()
        git.texts[(HEAD, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection drift", sources(git=git))

    def test_a_transitive_dependency_edit_is_rejected(self, payload):
        """Not just the seeds: a change one level deeper is caught too.

        ``CANDIDATE_DISPOSITIONS`` is not a seed — it is reached only because
        ``derive_candidate_disposition`` and ``derive_cell_outcome`` depend on it.
        """
        assert "CANDIDATE_DISPOSITIONS" not in A.OUTCOME_PRODUCING_PROJECTION_SEEDS
        anchor = 'CANDIDATE_DISPOSITIONS = (\n    "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED",'
        assert DERIVATION_SOURCE.count(anchor) == 1, "fixture anchor is not unique"
        mutated = DERIVATION_SOURCE.replace(
            anchor, 'CANDIDATE_DISPOSITIONS = (\n    "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED_X",', 1
        )
        git = FakeGit()
        git.texts[(A.EXECUTABLE_PACKAGE_MERGE_SHA, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection drift", sources(git=git))

    def test_an_edit_outside_the_closure_correctly_does_not_fire(self, payload):
        """PRECISION, not only sensitivity — and the reason this projection is not whole-file equality.

        ``FAILURE_DISPOSITIONS`` is a real top-level constant that no outcome-producing seed reaches.
        A projection that fired on it would be byte equality wearing a different name, and would make
        the authorization-only edits this rebinding must lawfully make impossible.
        """
        anchor = 'FAILURE_DISPOSITIONS = ("BLOCKED_CATEGORICALLY", '
        assert DERIVATION_SOURCE.count(anchor) == 1
        projected = {
            line.split("::", 1)[0]
            for line in A.project_outcome_producing_surface(DERIVATION_SOURCE).splitlines()
        }
        assert "FAILURE_DISPOSITIONS" not in projected
        mutated = DERIVATION_SOURCE.replace(
            anchor, 'FAILURE_DISPOSITIONS = ("BLOCKED_CATEGORICALLY_X", ', 1
        )
        assert mutated != DERIVATION_SOURCE
        assert A.outcome_producing_projection_digest(mutated) == (
            A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        )
        git = FakeGit()
        git.texts[(A.EXECUTABLE_PACKAGE_MERGE_SHA, DERIVATION_RELPATH)] = mutated
        assert A.validate_authorization_document(payload, sources(git=git)).valid

    @pytest.mark.parametrize(
        "anchor_attr", ["EXECUTABLE_PACKAGE_ACCEPTED_HEAD", "EXECUTABLE_PACKAGE_MERGE_SHA"]
    )
    def test_an_unreadable_anchor_fails_closed(self, payload, anchor_attr):
        git = FakeGit()
        del git.texts[(getattr(A, anchor_attr), DERIVATION_RELPATH)]
        _rejected(payload, "could not be read at the executable-package", sources(git=git))

    def test_a_renamed_seed_at_an_anchor_fails_closed(self, payload):
        mutated = DERIVATION_SOURCE.replace(
            "def derive_roll_up_outcome(", "def derive_roll_up_outcome_RENAMED(", 1
        )
        git = FakeGit()
        git.texts[(A.EXECUTABLE_PACKAGE_MERGE_SHA, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection failed", sources(git=git))

    def test_an_unparseable_anchor_fails_closed(self, payload):
        git = FakeGit()
        git.texts[(A.EXECUTABLE_PACKAGE_MERGE_SHA, DERIVATION_RELPATH)] = "def broken(:\n"
        _rejected(payload, "outcome-producing projection failed", sources(git=git))

    def test_the_happy_path_still_validates_with_the_new_gate(self, payload):
        result = A.validate_authorization_document(payload, sources())
        assert result.valid, result.errors


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
            "level1_stage1_execution_authorization.py",
        ],
    )
    def test_every_surface_states_the_true_provenance(self, relative):
        collapsed = " ".join(
            (ROOT / relative).read_text(encoding="utf-8").replace("#:", " ").replace("*", "").split()
        ).lower()
        assert "first written before the draft" in collapsed, relative
        assert "verified against the real draft" in collapsed, relative

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


def _independently_derived_ambient_names() -> tuple[set[str], set[str]]:
    """Re-derive, from the derivation module's OWN source, what the closure resolves ambiently.

    Deliberately NOT read from any production constant, tuple, or helper output: the delta review's
    requirement is that the production binding declaration must not be its own oracle. This walks
    the module directly, reconstructs the seed closure by attribute reachability, and splits the
    names it resolves outside its own top-level symbols into import-bound and builtin.
    """
    import ast as _ast
    import builtins as _builtins

    tree = _ast.parse(DERIVATION_SOURCE)
    table: dict[str, _ast.AST] = {}
    for node in tree.body:
        if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef)):
            table[node.name] = node
        elif isinstance(node, _ast.Assign):
            for target in node.targets:
                if isinstance(target, _ast.Name):
                    table[target.id] = node
        elif isinstance(node, _ast.AnnAssign) and isinstance(node.target, _ast.Name):
            table[node.target.id] = node

    closure: set[str] = set()
    stack = list(_independently_derived_seed_symbols())
    while stack:
        name = stack.pop()
        if name in closure or name not in table:
            continue
        closure.add(name)
        for sub in _ast.walk(table[name]):
            if isinstance(sub, _ast.Name) and sub.id in table and sub.id not in closure:
                stack.append(sub.id)

    imported: set[str] = set()
    for node in tree.body:
        if isinstance(node, (_ast.Import, _ast.ImportFrom)):
            for alias in node.names:
                imported.add(alias.asname or alias.name.split(".")[0])

    referenced: set[str] = set()
    for name in closure:
        for sub in _ast.walk(table[name]):
            if isinstance(sub, _ast.Name) and isinstance(sub.ctx, _ast.Load):
                referenced.add(sub.id)
    outside = referenced - set(table)
    return ({n for n in outside if n in imported}, {n for n in outside if hasattr(_builtins, n)})


class TestAmbientBindingIdentity:
    """A projected AST can be identical while the MEANING of the names inside it changes.

    Delta review 4955476669 demonstrated the case end to end: inserting only
    ``from builtins import min as any`` left every projected symbol byte-for-byte identical, turned
    one categorical FAIL from BLOCKED_CATEGORICALLY into CONSTRUCTIBLE_CANDIDATE_IDENTIFIED, and the
    real public validator returned ``valid=True`` with ``errors=()``. These tests pin the corrected
    boundary, its precision, and its fail-closed edges.
    """

    # --- the exact reported case, proved through the REAL public validator ---

    def test_the_import_shadow_flips_a_real_disposition(self):
        """Establish that the mutation is genuinely outcome-changing before demanding refusal."""
        import importlib.util
        import sys
        import tempfile

        mutated_source = _with_module_level_line("from builtins import min as any\n")
        directory = Path(tempfile.mkdtemp())
        path = directory / "_shadowed_derivation.py"
        path.write_text(mutated_source, encoding="utf-8")
        spec = importlib.util.spec_from_file_location("_shadowed_derivation", path)
        shadowed = importlib.util.module_from_spec(spec)
        # ``@dataclass`` resolves ``cls.__module__`` through ``sys.modules`` while executing.
        sys.modules["_shadowed_derivation"] = shadowed
        try:
            spec.loader.exec_module(shadowed)
        finally:
            sys.modules.pop("_shadowed_derivation", None)

        gate_results = dict.fromkeys(PREREG.GATE_IDS, "PASS")
        gate_results[sorted(PREREG.CATEGORICAL_GATES)[0]] = "FAIL"
        assert PREREG.derive_candidate_disposition(gate_results) == "BLOCKED_CATEGORICALLY"
        assert (
            shadowed.derive_candidate_disposition(gate_results)
            == "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"
        )

    def test_the_import_shadow_changes_the_projected_identity(self):
        mutated = _with_module_level_line("from builtins import min as any\n")
        assert A.outcome_producing_projection_digest(
            mutated
        ) != A.outcome_producing_projection_digest(DERIVATION_SOURCE)

    def test_the_public_validator_refuses_the_import_shadow_at_the_successor(self, payload):
        """The reported reproduction, exactly: package anchors accepted, successor anchors mutated."""
        mutated = _with_module_level_line("from builtins import min as any\n")
        git = FakeGit()
        git.texts[(HEAD, DERIVATION_RELPATH)] = mutated
        git.texts[(MERGE, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection drift", sources(git=git))

    def test_the_public_validator_refuses_the_import_shadow_at_the_package(self, payload):
        """Symmetric: a package anchor whose ambient surface differs is equally unacceptable."""
        mutated = _with_module_level_line("from builtins import min as any\n")
        git = FakeGit()
        git.texts[(A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, DERIVATION_RELPATH)] = mutated
        git.texts[(A.EXECUTABLE_PACKAGE_MERGE_SHA, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection drift", sources(git=git))

    # --- import aliases and rebindings ---

    @pytest.mark.parametrize(
        "line",
        [
            "from builtins import min as any\n",
            "from builtins import min as sorted\n",
            "from builtins import list as set\n",
        ],
    )
    def test_shadowing_a_builtin_the_closure_calls_changes_identity(self, line):
        assert A.outcome_producing_projection_digest(
            _with_module_level_line(line)
        ) != A.outcome_producing_projection_digest(DERIVATION_SOURCE)

    def test_changing_where_a_used_import_comes_from_changes_identity(self):
        """Same bound name, different source module -- a different object, so a different identity."""
        mutated = DERIVATION_SOURCE.replace(
            "from typing import Any, Iterable, Mapping, Sequence",
            "from collections.abc import Iterable, Mapping, Sequence\nfrom typing import Any",
            1,
        )
        assert mutated != DERIVATION_SOURCE
        assert A.outcome_producing_projection_digest(
            mutated
        ) != A.outcome_producing_projection_digest(DERIVATION_SOURCE)

    def test_a_name_the_closure_uses_bound_twice_fails_closed(self):
        with pytest.raises(A.ProjectionError, match="bound by more than one binder"):
            A.outcome_producing_projection_digest(
                _with_module_level_line("import typing as Mapping\n")
            )

    # --- precision: lawful authorization-only edits must remain possible ---

    def test_a_new_import_the_closure_never_uses_does_not_change_identity(self):
        """Otherwise this would be whole-file equality, which would make a lawful rebinding impossible."""
        for line in ("import json\n", "import itertools as _it\n", "from decimal import Decimal\n"):
            assert A.outcome_producing_projection_digest(
                _with_module_level_line(line)
            ) == A.outcome_producing_projection_digest(DERIVATION_SOURCE)

    def test_shadowing_a_builtin_the_closure_never_calls_does_not_change_identity(self):
        """The boundary is 'capable of changing how the projected closure executes', not 'any import'."""
        assert A.outcome_producing_projection_digest(
            _with_module_level_line("from builtins import min as filter\n")
        ) == A.outcome_producing_projection_digest(DERIVATION_SOURCE)

    def test_reordering_the_import_block_does_not_change_identity(self):
        """Renderings come from AST fields, so grouping and order are not identity."""
        mutated = DERIVATION_SOURCE.replace(
            "import hashlib\nimport re\nimport sys\n", "import sys\nimport re\nimport hashlib\n", 1
        )
        assert mutated != DERIVATION_SOURCE
        assert A.outcome_producing_projection_digest(
            mutated
        ) == A.outcome_producing_projection_digest(DERIVATION_SOURCE)

    # --- unsupported dynamic namespace mutation must never be assumed harmless ---

    @pytest.mark.parametrize(
        "line",
        [
            "from typing import *\n",
            "_smuggled = globals()\n",
            "_smuggled = exec('pass')\n",
            "_smuggled = eval('1')\n",
            "_smuggled = vars()\n",
            "_smuggled = setattr(object, 'x', 1)\n",
            "_smuggled = delattr(object, 'x')\n",
            "_tmp = 1\n_tmp += 1\n",
            "_tmp = 1\ndel _tmp\n",
        ],
    )
    def test_unsupported_namespace_mutation_fails_closed(self, line):
        with pytest.raises(A.ProjectionError):
            A.outcome_producing_projection_digest(_with_module_level_line(line))

    def test_a_nonlocal_or_global_declaration_anywhere_fails_closed(self):
        mutated = _with_module_level_line("def _smuggle():\n    global REGISTERED_CONSTRUCTION_COUNT\n")
        with pytest.raises(A.ProjectionError, match="dynamic namespace mutation"):
            A.outcome_producing_projection_digest(mutated)

    def test_an_unresolvable_referenced_name_fails_closed(self):
        """Removing an import the closure relies on leaves a name resolving to nothing nameable."""
        mutated = DERIVATION_SOURCE.replace(
            "from dataclasses import dataclass, field", "from dataclasses import dataclass", 1
        )
        assert mutated != DERIVATION_SOURCE
        with pytest.raises(A.ProjectionError, match="resolve to neither a top-level symbol"):
            A.outcome_producing_projection_digest(mutated)

    # --- the ambient surface itself, derived independently of the production helpers ---

    def test_the_projected_ambient_surface_matches_an_independent_derivation(self):
        imported, builtin = _independently_derived_ambient_names()
        assert imported and builtin, "the independent derivation found nothing to compare"
        projected = {
            line.split("::")[1]
            for line in A.project_outcome_producing_surface(DERIVATION_SOURCE).splitlines()
            if line.startswith("@ambient::")
        }
        assert projected == imported | builtin, (
            f"ambient surface disagrees with an independent derivation; "
            f"projected-only={projected - (imported | builtin)}, "
            f"derived-only={(imported | builtin) - projected}"
        )

    def test_the_shadowed_builtin_is_actually_in_the_ambient_surface(self):
        """Names the reported case turns on must be present, not merely presumed present."""
        surface = A.project_outcome_producing_surface(DERIVATION_SOURCE)
        assert "@ambient::any::builtin" in surface

    def test_every_ambient_entry_is_resolved_rather_than_merely_listed(self):
        for line in A.project_outcome_producing_surface(DERIVATION_SOURCE).splitlines():
            if not line.startswith("@ambient::"):
                continue
            resolution = line.split("::", 2)[2]
            assert resolution == "builtin" or resolution.startswith("bound::") or (
                resolution == "module-attribute"
            ), line

    # --- the real anchors carry no ambient drift ---

    def test_the_live_ambient_surface_is_identical_to_the_accepted_package(self):
        """Requirement 9: confirm the fact the rebinding relies on, rather than assume it."""
        live = A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        for anchor in (A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, A.EXECUTABLE_PACKAGE_MERGE_SHA):
            blob = subprocess.run(
                ["git", "show", f"{anchor}:{DERIVATION_RELPATH}"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout
            assert A.outcome_producing_projection_digest(blob) == live

    def test_the_real_module_import_nodes_are_identical_to_the_accepted_package(self):
        """A second, independent check of the same fact: the import nodes themselves."""
        import ast as _ast

        def import_nodes(source):
            return [
                _ast.dump(node, include_attributes=False)
                for node in _ast.parse(source).body
                if isinstance(node, (_ast.Import, _ast.ImportFrom))
            ]

        live = import_nodes(DERIVATION_SOURCE)
        assert live, "the derivation module has no module-level imports to compare"
        for anchor in (A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, A.EXECUTABLE_PACKAGE_MERGE_SHA):
            blob = subprocess.run(
                ["git", "show", f"{anchor}:{DERIVATION_RELPATH}"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout
            assert import_nodes(blob) == live

    # --- the correction must not have loosened anything ---

    def test_the_happy_path_still_validates(self, payload):
        assert A.validate_authorization_document(payload, sources()).valid

    def test_the_docstring_exclusion_is_unchanged_and_still_narrow(self):
        """Prose still cannot decide an outcome, and the ambient work did not widen the exclusion."""
        mutated = DERIVATION_SOURCE.replace(
            '"""Compose already-decided gate results into a candidate disposition.',
            '"""COMPLETELY REWRITTEN PROSE that decides nothing.',
            1,
        )
        assert mutated != DERIVATION_SOURCE
        assert A.outcome_producing_projection_digest(
            mutated
        ) == A.outcome_producing_projection_digest(DERIVATION_SOURCE)


def _independently_derived_module_globals() -> set[str]:
    """Every module-global binding CPython's OWN symbol table reports for the derivation module.

    Deliberately NOT read from ``A._module_scope_binders`` or ``A._symtable_module_globals``: the
    review's standing requirement is that a production declaration must never be its own oracle.
    This calls :mod:`symtable` directly from the test.
    """
    import symtable as _symtable

    table = _symtable.symtable(DERIVATION_SOURCE, DERIVATION_RELPATH, "exec")
    return {
        symbol.get_name()
        for symbol in table.get_symbols()
        if symbol.is_assigned() or symbol.is_imported()
    }


def _load_mutated_derivation(source: str, name: str):
    """Execute a mutated derivation module so a disposition claim is demonstrated, not asserted."""
    import importlib.util
    import sys
    import tempfile

    path = Path(tempfile.mkdtemp()) / f"{name}.py"
    path.write_text(source, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    # ``@dataclass`` resolves ``cls.__module__`` through ``sys.modules`` while executing.
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(name, None)
    return module


def _one_categorical_failure() -> dict:
    gate_results = dict.fromkeys(PREREG.GATE_IDS, "PASS")
    gate_results[sorted(PREREG.CATEGORICAL_GATES)[0]] = "FAIL"
    return gate_results


#: The binder matrix. Each entry inserts ONE module-scope statement that binds ``any`` -- a builtin
#: the projected closure really calls -- through a different Python binding form. None of these is
#: a direct ``Import`` or a simple-``Name`` ``Assign``, which is exactly why the predecessor model
#: missed them. Named independently of the production model's own vocabulary.
_BINDER_MATRIX = [
    ("conditional-import", "if True:\n    from builtins import min as any\n"),
    ("try-except-import", "try:\n    from builtins import min as any\nexcept ImportError:\n    pass\n"),
    ("try-else-import", "try:\n    pass\nexcept ImportError:\n    pass\nelse:\n    from builtins import min as any\n"),
    ("try-finally-import", "try:\n    pass\nfinally:\n    from builtins import min as any\n"),
    (
        "while-body-import",
        "_looping = True\nwhile _looping:\n    from builtins import min as any\n"
        "    _looping = False\n",
    ),
    ("tuple-assignment", "any, _unused = min, None\n"),
    ("list-assignment", "[any, _unused] = [min, None]\n"),
    ("starred-assignment", "any, *_rest = min, None\n"),
    ("nested-tuple-assignment", "(_a, (any, _b)) = (None, (min, None))\n"),
    ("annotated-assignment", "any: object = min\n"),
    ("loop-target", "for any in (min,):\n    pass\n"),
    ("with-target", "import contextlib as _ctx\nwith _ctx.nullcontext(min) as any:\n    pass\n"),
    ("exception-name", "try:\n    pass\nexcept Exception as any:\n    pass\n"),
    ("named-expression", "_seen = (any := min)\n"),
    ("conditional-tuple-assignment", "if True:\n    any, _unused = min, None\n"),
    ("nested-conditional-import", "if True:\n    if True:\n        from builtins import min as any\n"),
]

_MATCH_STATEMENT_BINDER = (
    "match [min]:\n    case [any]:\n        pass\n    case _:\n        pass\n"
)

#: Module-scope side effects that can reach imported modules, builtins, or globals. Each must fail
#: closed rather than be assumed harmless.
_NAMESPACE_MUTATION_MATRIX = [
    ("attribute-store", "import sys as _s\n_s.maxsize = 1\n"),
    ("attribute-store-conditional", "import sys as _s\nif True:\n    _s.maxsize = 1\n"),
    ("attribute-delete", "import sys as _s\ndel _s.maxsize\n"),
    ("subscript-store", "_registry = {}\n_registry['any'] = min\n"),
    ("subscript-delete", "_registry = {'x': 1}\ndel _registry['x']\n"),
    ("conditional-globals-call", "if True:\n    _smuggled = globals()\n"),
    ("conditional-exec-call", "if True:\n    _smuggled = exec('pass')\n"),
    ("conditional-augmented-assignment", "_tmp = 1\nif True:\n    _tmp += 1\n"),
    ("conditional-delete", "_tmp = 1\nif True:\n    del _tmp\n"),
    ("nested-star-import", "if True:\n    from typing import *\n"),
]


class TestModuleScopeBinderCompleteness:
    """Indirect module-scope binders must not change outcome semantics without changing identity.

    Delta review 4957056810 demonstrated two spellings end to end -- a conditional import and a
    destructuring assignment -- each of which left the projection byte-identical, flipped one
    categorical FAIL from BLOCKED_CATEGORICALLY to CONSTRUCTIBLE_CANDIDATE_IDENTIFIED, and was
    accepted by the real public validator with ``valid=True, errors=()``. These tests pin the whole
    semantic class rather than those two spellings, and pin the precision boundary that keeps the
    correction from collapsing into whole-file equality.
    """

    # --- the two reported reproductions, driven through the REAL public validator ---

    @pytest.mark.parametrize(
        "label,line",
        [
            ("conditional-import", "if True:\n    from builtins import min as any\n"),
            ("destructuring-assignment", "any, _unused = min, None\n"),
        ],
    )
    def test_the_reported_binder_actually_flips_a_disposition(self, label, line):
        """Establish the mutation is genuinely outcome-changing before demanding refusal."""
        mutated = _load_mutated_derivation(_with_module_level_line(line), f"_binder_{label}")
        gate_results = _one_categorical_failure()
        assert PREREG.derive_candidate_disposition(gate_results) == "BLOCKED_CATEGORICALLY"
        assert (
            mutated.derive_candidate_disposition(gate_results)
            == "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"
        )

    @pytest.mark.parametrize(
        "line",
        [
            "if True:\n    from builtins import min as any\n",
            "any, _unused = min, None\n",
        ],
    )
    def test_the_public_validator_refuses_the_reported_binder_at_the_successor(self, payload, line):
        """Accepted source at BOTH package anchors, mutated source at the successor anchors."""
        mutated = _with_module_level_line(line)
        git = FakeGit()
        git.texts[(HEAD, DERIVATION_RELPATH)] = mutated
        git.texts[(MERGE, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection drift", sources(git=git))

    @pytest.mark.parametrize(
        "line",
        [
            "if True:\n    from builtins import min as any\n",
            "any, _unused = min, None\n",
        ],
    )
    def test_the_public_validator_refuses_the_reported_binder_at_the_package(self, payload, line):
        mutated = _with_module_level_line(line)
        git = FakeGit()
        git.texts[(A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, DERIVATION_RELPATH)] = mutated
        git.texts[(A.EXECUTABLE_PACKAGE_MERGE_SHA, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection drift", sources(git=git))

    # --- the whole binder class, not the two reported spellings ---

    @pytest.mark.parametrize("label,line", _BINDER_MATRIX, ids=[e[0] for e in _BINDER_MATRIX])
    def test_every_module_scope_binder_form_changes_or_refuses_the_identity(self, label, line):
        """Each form binds ``any``; none may leave the projected identity untouched."""
        mutated = _with_module_level_line(line)
        baseline = A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        try:
            assert A.outcome_producing_projection_digest(mutated) != baseline, label
        except A.ProjectionError:
            pass  # refusing is an equally acceptable outcome; silently accepting is not

    def test_a_match_statement_capture_changes_or_refuses_the_identity(self):
        mutated = _with_module_level_line(_MATCH_STATEMENT_BINDER)
        baseline = A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        try:
            assert A.outcome_producing_projection_digest(mutated) != baseline
        except A.ProjectionError:
            pass

    def test_the_controlling_condition_is_part_of_the_identity(self):
        """A conditional binding must carry enough controlling AST to detect a semantic change."""
        enabled = A.outcome_producing_projection_digest(
            _with_module_level_line("if True:\n    from builtins import min as any\n")
        )
        disabled = A.outcome_producing_projection_digest(
            _with_module_level_line("if False:\n    from builtins import min as any\n")
        )
        assert enabled != disabled

    def test_a_conditional_rebinding_of_a_projected_symbol_fails_closed(self):
        """Which definition the closure runs would be order-dependent, so it cannot be projected."""
        with pytest.raises(A.ProjectionError, match="order-dependent"):
            A.outcome_producing_projection_digest(
                _with_module_level_line("if True:\n    SLEEVES = ()\n")
            )

    # --- namespace mutation must never be assumed harmless ---

    @pytest.mark.parametrize(
        "label,line", _NAMESPACE_MUTATION_MATRIX, ids=[e[0] for e in _NAMESPACE_MUTATION_MATRIX]
    )
    def test_module_scope_namespace_mutation_fails_closed(self, label, line):
        with pytest.raises(A.ProjectionError):
            A.outcome_producing_projection_digest(_with_module_level_line(line))

    # --- precision: the correction must not become whole-file equality ---

    @pytest.mark.parametrize(
        "line",
        [
            "import json\n",
            "if True:\n    import json\n",
            "if True:\n    from builtins import min as filter\n",
            "_unrelated, _also = 1, 2\n",
            "for _index in range(1):\n    pass\n",
            "if __name__ == '__main__':\n    pass\n",
        ],
    )
    def test_a_binder_the_closure_never_resolves_does_not_change_identity(self, line):
        assert A.outcome_producing_projection_digest(
            _with_module_level_line(line)
        ) == A.outcome_producing_projection_digest(DERIVATION_SOURCE)

    def test_the_real_module_keeps_its_lawful_cli_guard(self):
        """Requirement: do not broadly reject harmless existing module control flow."""
        import ast as _ast

        guards = [
            node
            for node in _ast.parse(DERIVATION_SOURCE).body
            if isinstance(node, _ast.If)
        ]
        assert guards, "the derivation module no longer has the module-level CLI guard"
        assert A.outcome_producing_projection_digest(DERIVATION_SOURCE)  # projects without refusal

    # --- the binder model is complete, checked against an independent oracle ---

    def test_the_binder_model_covers_every_binding_symtable_reports(self):
        """Non-circular: :mod:`symtable` is called directly here, not through production code."""
        import ast as _ast

        tree = _ast.parse(DERIVATION_SOURCE)
        modelled = set(A._module_scope_binders(tree, DERIVATION_RELPATH))
        reported = _independently_derived_module_globals()
        assert reported, "the independent oracle found no module-global bindings"
        assert not (reported - modelled), (
            f"symtable reports module-global binding(s) the binder model misses: "
            f"{sorted(reported - modelled)}"
        )

    @pytest.mark.parametrize("label,line", _BINDER_MATRIX, ids=[e[0] for e in _BINDER_MATRIX])
    def test_the_binder_model_records_the_bound_name_for_every_form(self, label, line):
        import ast as _ast

        tree = _ast.parse(_with_module_level_line(line))
        assert "any" in A._module_scope_binders(tree, DERIVATION_RELPATH), label

    def test_the_completeness_oracle_is_enforced_not_merely_available(self):
        """A binding the model cannot represent must fail closed, not fall through to a builtin."""
        import ast as _ast

        real = A._module_scope_binders

        def blinded(tree, where):
            recorded = real(tree, where)
            return {name: value for name, value in recorded.items() if name != "any"}

        mutated = _with_module_level_line("any, _unused = min, None\n")
        A._module_scope_binders = blinded
        try:
            with pytest.raises(A.ProjectionError, match="symbol table reports"):
                A.outcome_producing_projection_digest(mutated)
        finally:
            A._module_scope_binders = real

    # --- target unpacking, exercised directly ---

    @pytest.mark.parametrize(
        "source,expected",
        [
            ("a = 1", {"a"}),
            ("a, b = 1, 2", {"a", "b"}),
            ("[a, b] = [1, 2]", {"a", "b"}),
            ("a, *b = 1, 2, 3", {"a", "b"}),
            ("(a, (b, c)) = (1, (2, 3))", {"a", "b", "c"}),
            ("a.b = 1", set()),
            ("a[0] = 1", set()),
        ],
    )
    def test_assignment_targets_are_unpacked_recursively(self, source, expected):
        import ast as _ast

        statement = _ast.parse(source).body[0]
        assert set(A._target_names(statement.targets[0])) == expected

    # --- everything the earlier corrections established still holds ---

    def test_the_projection_shape_is_unchanged(self):
        surface = A.project_outcome_producing_surface(DERIVATION_SOURCE)
        symbols = {
            line.split("::", 1)[0]
            for line in surface.splitlines()
            if not line.startswith("@ambient::")
        }
        assert len(A.OUTCOME_PRODUCING_PROJECTION_SEEDS) == 18
        assert len(symbols) == 26
        assert set(A.OUTCOME_PRODUCING_PROJECTION_SEEDS) <= symbols

    def test_the_direct_import_fix_still_holds(self):
        assert A.outcome_producing_projection_digest(
            _with_module_level_line("from builtins import min as any\n")
        ) != A.outcome_producing_projection_digest(DERIVATION_SOURCE)

    def test_the_live_projection_is_still_identical_to_the_accepted_package(self):
        live = A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        for anchor in (A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, A.EXECUTABLE_PACKAGE_MERGE_SHA):
            blob = subprocess.run(
                ["git", "show", f"{anchor}:{DERIVATION_RELPATH}"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout
            assert A.outcome_producing_projection_digest(blob) == live


#: The exact spelling DELTA review 4958940810 reported. Two lines, no ``Store`` node anywhere.
_REPORTED_CALL_MEDIATED_MUTATION = (
    "import builtins as _review_builtins\n_review_builtins.__dict__.update(any=min)\n"
)

#: Materially distinct call-mediated routes to the same effect. Written from Python's own semantics,
#: NOT from any production constant, tuple, or allowlist, so production and tests cannot drift
#: together unnoticed: if a future edit narrows the gate, these still describe real mutations.
_CALL_MEDIATED_MUTATION_MATRIX = [
    ("reported-dunder-dict-update", _REPORTED_CALL_MEDIATED_MUTATION),
    ("aliased-namespace-then-update",
     "import builtins as _b\n_ns = _b.__dict__\n_ns.update(any=min)\n"),
    ("from-import-of-the-namespace",
     "from builtins import __dict__ as _ns\n_ns.update(any=min)\n"),
    ("vars-receiver", "import builtins as _b\nvars(_b).update(any=min)\n"),
    ("setattr-on-builtins", "import builtins as _b\nsetattr(_b, 'any', min)\n"),
    ("getattr-chain-then-update",
     "import builtins as _b\ngetattr(_b, '__dict__').update(any=min)\n"),
    ("sys-modules-route",
     "import sys as _s\n_s.modules['builtins'].__dict__.update(any=min)\n"),
    ("class-mro-walk", "_x = ().__class__.__bases__[0].__subclasses__()\n"),
    ("unbound-method-form", "import builtins as _b\ndict.update(_b.__dict__, any=min)\n"),
    ("mapping-mutator-any-receiver", "_scratch = {}\n_scratch.update(any=min)\n"),
    ("namespace-handed-to-callee", "import builtins as _b\n_ = dict(_b.__dict__)\n"),
    ("importlib-reload", "import importlib as _il\nimport typing as _t\n_il.reload(_t)\n"),
    ("subscript-callee", "_reg = {'f': print}\n_reg['f']('x')\n"),
    ("conditional-callee", "(print or print)('x')\n"),
    ("nested-in-if", "import builtins as _b\nif True:\n    _b.__dict__.update(any=min)\n"),
    ("nested-in-try",
     "import builtins as _b\ntry:\n    _b.__dict__.update(any=min)\nexcept Exception:\n    pass\n"),
]

#: Calls that mutate no namespace the projection resolves through. Refusing any of these would mean
#: the gate rejects code merely for BEING a call, which the review expressly forbids.
_HARMLESS_CALL_MATRIX = [
    ("lawful-cli-guard", "if __name__ == '__main__':\n    import sys as _s2\n    _s2.exit(0)\n"),
    ("ordinary-builtin-call", "_x = sorted([3, 1, 2])\n"),
    ("chained-safe-call", "from pathlib import Path as _P\n_y = _P(__file__).resolve()\n"),
    ("stdlib-factory-call", "import re as _re\n_pat = _re.compile('x')\n"),
    ("generator-consumed-by-call", "_t2 = tuple(g for g in (1, 2))\n"),
    ("nested-safe-calls", "_z = len(sorted([1]))\n"),
    ("unused-import", "import json\n"),
]


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


class TestCallMediatedNamespaceMutation:
    """A module-scope CALL can mutate a namespace without any ``Store`` node existing anywhere.

    DELTA review 4958940810 demonstrated the whole chain with two lines,
    ``import builtins as _review_builtins`` / ``_review_builtins.__dict__.update(any=min)``: the
    projected identity did not move, one categorical FAIL turned from BLOCKED_CATEGORICALLY into
    CONSTRUCTIBLE_CANDIDATE_IDENTIFIED, and the real public validator returned ``valid=True,
    errors=()`` with the mutation at the successor anchors AND again with it at both package
    anchors. CPython's ``symtable`` oracle cannot see this class at all -- it binds no new module
    global. These tests pin the semantic class and the precision boundary that keeps the gate from
    rejecting code merely for being a call.
    """

    # --- the reported case, executed and driven through the REAL public validator ---

    def test_the_reported_mutation_actually_flips_a_disposition(self):
        """Established by EXECUTION in a disposable subprocess, never assumed."""
        gate_results = dict.fromkeys(PREREG.GATE_IDS, "PASS")
        gate_results[sorted(PREREG.CATEGORICAL_GATES)[0]] = "FAIL"
        assert PREREG.derive_candidate_disposition(gate_results) == "BLOCKED_CATEGORICALLY"
        mutated = _with_module_level_line(_REPORTED_CALL_MEDIATED_MUTATION)
        assert (
            _execute_derivation_in_subprocess(mutated) == "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"
        )

    def test_the_public_validator_refuses_the_reported_mutation_at_the_successor(self, payload):
        """Accepted source at BOTH package anchors, mutated source at the successor anchors."""
        mutated = _with_module_level_line(_REPORTED_CALL_MEDIATED_MUTATION)
        git = FakeGit()
        git.texts[(HEAD, DERIVATION_RELPATH)] = mutated
        git.texts[(MERGE, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection", sources(git=git))

    def test_the_public_validator_refuses_the_reported_mutation_at_the_package(self, payload):
        """The review's fourth proof: mutated at both PACKAGE anchors was also accepted before."""
        mutated = _with_module_level_line(_REPORTED_CALL_MEDIATED_MUTATION)
        git = FakeGit()
        git.texts[(A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, DERIVATION_RELPATH)] = mutated
        git.texts[(A.EXECUTABLE_PACKAGE_MERGE_SHA, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection", sources(git=git))

    def test_the_public_validator_refuses_the_reported_mutation_at_every_anchor(self, payload):
        """Mutated everywhere: internally consistent, and still unacceptable."""
        mutated = _with_module_level_line(_REPORTED_CALL_MEDIATED_MUTATION)
        git = FakeGit()
        for commit in (
            HEAD, MERGE, A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, A.EXECUTABLE_PACKAGE_MERGE_SHA,
        ):
            git.texts[(commit, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection", sources(git=git))

    # --- the semantic class, not the reported spelling ---

    @pytest.mark.parametrize(
        "label,line",
        _CALL_MEDIATED_MUTATION_MATRIX,
        ids=[entry[0] for entry in _CALL_MEDIATED_MUTATION_MATRIX],
    )
    def test_every_call_mediated_mutation_route_fails_closed(self, label, line):
        with pytest.raises(A.ProjectionError):
            A.outcome_producing_projection_digest(_with_module_level_line(line))

    def test_the_symtable_oracle_cannot_see_this_class(self):
        """Stated because it matters: the completeness oracle is real but does not cover calls."""
        import symtable as _symtable

        accepted = {
            symbol.get_name()
            for symbol in _symtable.symtable(DERIVATION_SOURCE, "m.py", "exec").get_symbols()
            if symbol.is_assigned() or symbol.is_imported()
        }
        mutated_source = _with_module_level_line("import builtins as _b\n_b.__dict__.update()\n")
        mutated = {
            symbol.get_name()
            for symbol in _symtable.symtable(mutated_source, "m.py", "exec").get_symbols()
            if symbol.is_assigned() or symbol.is_imported()
        }
        # The ONLY new module-global is the alias itself; the mutation binds nothing.
        assert mutated - accepted == {"_b"}
        # ...and the gate refuses it regardless, which is the point.
        with pytest.raises(A.ProjectionError):
            A.outcome_producing_projection_digest(mutated_source)

    # --- precision: a call is not refused merely for being a call ---

    @pytest.mark.parametrize(
        "label,line", _HARMLESS_CALL_MATRIX, ids=[entry[0] for entry in _HARMLESS_CALL_MATRIX]
    )
    def test_harmless_calls_do_not_change_or_block_the_identity(self, label, line):
        assert A.outcome_producing_projection_digest(
            _with_module_level_line(line)
        ) == A.outcome_producing_projection_digest(DERIVATION_SOURCE), label

    def test_the_real_module_still_projects_with_its_own_module_scope_calls(self):
        """The derivation module really does call Path(...).resolve(), re.compile(...), sys.exit()."""
        import ast as _ast

        calls = [
            node
            for statement in _ast.parse(DERIVATION_SOURCE).body
            if not isinstance(
                statement, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef)
            )
            for node in _ast.walk(statement)
            if isinstance(node, _ast.Call)
        ]
        assert calls, "the derivation module has no module-scope calls to protect"
        assert A.outcome_producing_projection_digest(DERIVATION_SOURCE)

    def test_the_lawful_cli_guard_survives_verbatim(self):
        """`sys.exit(main())` is an Attribute callee too -- it must not be caught by association."""
        import ast as _ast

        guard = [
            node
            for node in _ast.parse(DERIVATION_SOURCE).body
            if isinstance(node, _ast.If)
            and "__name__" in _ast.dump(node.test)
        ]
        assert guard, "the derivation module no longer has its module-level CLI guard"
        assert "sys.exit" in _ast.unparse(guard[0])
        assert A.outcome_producing_projection_digest(DERIVATION_SOURCE)

    # --- the correction did not disturb what came before ---

    def test_the_identity_is_unchanged_by_this_correction(self):
        """This gate REFUSES; it does not restate the surface, so the digest must not move."""
        surface = A.project_outcome_producing_surface(DERIVATION_SOURCE)
        symbols = {
            line.split("::", 1)[0]
            for line in surface.splitlines()
            if not line.startswith("@ambient::")
        }
        assert len(A.OUTCOME_PRODUCING_PROJECTION_SEEDS) == 18
        assert len(symbols) == 26

    def test_the_live_projection_is_still_identical_to_the_accepted_package(self):
        live = A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        for anchor in (A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, A.EXECUTABLE_PACKAGE_MERGE_SHA):
            blob = subprocess.run(
                ["git", "show", f"{anchor}:{DERIVATION_RELPATH}"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout
            assert A.outcome_producing_projection_digest(blob) == live

    def test_the_earlier_binder_and_import_protections_still_hold(self):
        baseline = A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        assert A.outcome_producing_projection_digest(
            _with_module_level_line("from builtins import min as any\n")
        ) != baseline
        assert A.outcome_producing_projection_digest(
            _with_module_level_line("if True:\n    from builtins import min as any\n")
        ) != baseline
        assert A.outcome_producing_projection_digest(
            _with_module_level_line("any, _unused = min, None\n")
        ) != baseline


#: The two eager-execution forms DELTA review 4960897843 reported for MAJOR 1. Neither is a
#: deferred function body: Python runs both while creating the module.
_REPORTED_EAGER_DEFAULT = (
    "import builtins as _rb\ndef _review_probe(_x=_rb.__dict__.update(any=min)):\n    pass\n"
)
_REPORTED_EAGER_CLASS_BODY = (
    "import builtins as _rb\nclass _ReviewProbe:\n    _rb.__dict__.update(any=min)\n"
)

#: Every module-initialization boundary that executes eagerly. Enumerated from Python's own
#: execution semantics -- decorators, defaults, annotations, class bases/keywords, class bodies --
#: NOT from any production constant, so production and tests cannot drift together unnoticed.
_EAGER_EXECUTION_MATRIX = [
    ("function-default", _REPORTED_EAGER_DEFAULT),
    ("class-body", _REPORTED_EAGER_CLASS_BODY),
    ("function-decorator",
     "import builtins as _rb\ndef _d(f):\n    return f\n"
     "@_rb.__dict__.update(any=min) or _d\ndef _q():\n    pass\n"),
    ("class-decorator",
     "import builtins as _rb\n@(_rb.__dict__.update(any=min) or (lambda c: c))\n"
     "class _R:\n    pass\n"),
    ("class-base-expression",
     "import builtins as _rb\nclass _S((_rb.__dict__.update(any=min) or object)):\n    pass\n"),
    ("class-keyword-expression",
     "import builtins as _rb\n"
     "class _T(object, metaclass=(_rb.__dict__.update(any=min) or type)):\n    pass\n"),
    ("keyword-only-default",
     "import builtins as _rb\ndef _u(*, _k=_rb.__dict__.update(any=min)):\n    pass\n"),
    ("return-annotation",
     "import builtins as _rb\ndef _v() -> (_rb.__dict__.update(any=min) or None):\n    pass\n"),
    ("argument-annotation",
     "import builtins as _rb\ndef _w(_a: (_rb.__dict__.update(any=min) or int)):\n    pass\n"),
    ("lambda-default",
     "import builtins as _rb\n_l = lambda _x=_rb.__dict__.update(any=min): None\n"),
    ("nested-class-in-class-body",
     "import builtins as _rb\nclass _X:\n    class _Y:\n        _rb.__dict__.update(any=min)\n"),
    ("module-scope-listcomp", "import builtins as _rb\n_c = [_rb.__dict__.update(any=min)]\n"),
    ("async-function-default",
     "import builtins as _rb\nasync def _z(_x=_rb.__dict__.update(any=min)):\n    pass\n"),
]

#: MAJOR 2: a dangerous callable reached by alias or returned by another call.
_ALIASED_AND_RETURNED_CALLABLE_MATRIX = [
    ("aliased-exec", "from builtins import exec as _rexec\n_rexec('any=min')\n"),
    ("call-returned-callable", "import builtins as _rb\ngetattr(_rb, 'exec')('any=min')\n"),
    ("aliased-eval", "from builtins import eval as _rev\n_rev('1')\n"),
    ("aliased-setattr", "from builtins import setattr as _rsa\n_rsa(object, 'x', 1)\n"),
    ("aliased-globals", "from builtins import globals as _rg\n_rg()\n"),
    ("aliased-vars", "from builtins import vars as _rv\n_rv(object)\n"),
    ("import-from-projection-module",
     "from importlib import reload as _rl\nimport typing as _t\n_rl(_t)\n"),
    ("lambda-returned-callable", "_mk = lambda: print\n_mk()('x')\n"),
    ("attributed-alias-exec", "import builtins as _rb\n_rb.exec('any=min')\n"),
]

#: Calls and definitions that execute eagerly and mutate nothing. Refusing any of these would mean
#: the traversal rejects code merely for being reachable at import time.
_EAGER_PRECISION_MATRIX = [
    ("lawful-cli-guard", "if __name__ == '__main__':\n    import sys as _s2\n    _s2.exit(0)\n"),
    ("ordinary-builtin-call", "_x = sorted([3, 1, 2])\n"),
    ("chained-safe-method", "from pathlib import Path as _P\n_y = _P(__file__).resolve()\n"),
    ("stdlib-factory", "import re as _re\n_pat = _re.compile('x')\n"),
    ("generator-consumed", "_t2 = tuple(g for g in (1, 2))\n"),
    ("def-with-safe-defaults", "def _safe(_a=1, _b=sorted([2, 1])):\n    return _a\n"),
    ("plain-class",
     "class _Plain(object):\n    VALUE = 3\n    def m(self):\n        return __import__('os')\n"),
    ("decorated-function",
     "import functools as _ft\n@_ft.lru_cache(maxsize=1)\ndef _cached():\n    return 1\n"),
    ("deferred-body-is-pruned",
     "def _deferred():\n    import builtins as _rb\n    _rb.__dict__.update(any=min)\n"),
    ("safe-import-alias-call", "from builtins import sorted as _rsorted\n_s = _rsorted([2, 1])\n"),
]


class TestEagerExecutionAndAliasedCallables:
    """Import-time execution reaches far beyond ``tree.body`` statements.

    DELTA review 4960897843 raised two independent MAJORs against the call gate. **MAJOR 1**: the
    scanner did ``continue`` on every top-level ``def`` and ``class``, skipping decorators,
    defaults, annotations, class bases/keywords, and the class body -- all of which Python executes
    while creating the module, before any projected outcome function is ever called. **MAJOR 2**: a
    bare call was judged by its written root name only, so ``from builtins import exec as _rexec``
    was waved through; and ``_callee_chain`` walked through an intermediate call unconditionally, so
    ``getattr(m, "x")()`` was reported as rooted at ``getattr`` rather than unnameable -- against
    that function's own contract.

    All four reported forms preserved the accepted projection digest and flipped one categorical
    FAIL from BLOCKED_CATEGORICALLY to CONSTRUCTIBLE_CANDIDATE_IDENTIFIED, and the default-expression
    form was accepted by the real public validator at both anchor arrangements.
    """

    # --- the four reported forms, executed and driven through the REAL public validator ---

    @pytest.mark.parametrize(
        "label,block",
        [
            ("eager-default", _REPORTED_EAGER_DEFAULT),
            ("eager-class-body", _REPORTED_EAGER_CLASS_BODY),
            ("aliased-exec", "from builtins import exec as _rexec\n_rexec('any=min')\n"),
            ("call-returned", "import builtins as _rb\ngetattr(_rb, 'exec')('any=min')\n"),
        ],
    )
    def test_each_reported_form_actually_flips_a_disposition(self, label, block):
        """Established by EXECUTION in a disposable subprocess, never assumed."""
        gate_results = dict.fromkeys(PREREG.GATE_IDS, "PASS")
        gate_results[sorted(PREREG.CATEGORICAL_GATES)[0]] = "FAIL"
        assert PREREG.derive_candidate_disposition(gate_results) == "BLOCKED_CATEGORICALLY"
        assert (
            _execute_derivation_in_subprocess(_with_module_level_line(block))
            == "CONSTRUCTIBLE_CANDIDATE_IDENTIFIED"
        )

    @pytest.mark.parametrize(
        "label,block",
        [
            ("eager-default", _REPORTED_EAGER_DEFAULT),
            ("eager-class-body", _REPORTED_EAGER_CLASS_BODY),
            ("aliased-exec", "from builtins import exec as _rexec\n_rexec('any=min')\n"),
            ("call-returned", "import builtins as _rb\ngetattr(_rb, 'exec')('any=min')\n"),
        ],
    )
    def test_the_public_validator_refuses_each_reported_form_at_the_successor(
        self, payload, label, block
    ):
        """Accepted source at BOTH package anchors, mutated at the successor anchors."""
        mutated = _with_module_level_line(block)
        git = FakeGit()
        git.texts[(HEAD, DERIVATION_RELPATH)] = mutated
        git.texts[(MERGE, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection", sources(git=git))

    @pytest.mark.parametrize(
        "label,block",
        [
            ("eager-default", _REPORTED_EAGER_DEFAULT),
            ("eager-class-body", _REPORTED_EAGER_CLASS_BODY),
            ("aliased-exec", "from builtins import exec as _rexec\n_rexec('any=min')\n"),
            ("call-returned", "import builtins as _rb\ngetattr(_rb, 'exec')('any=min')\n"),
        ],
    )
    def test_the_public_validator_refuses_each_reported_form_at_every_anchor(
        self, payload, label, block
    ):
        """The review's second arrangement: mutated at ALL FOUR anchors, internally consistent."""
        mutated = _with_module_level_line(block)
        git = FakeGit()
        for commit in (
            HEAD, MERGE, A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, A.EXECUTABLE_PACKAGE_MERGE_SHA,
        ):
            git.texts[(commit, DERIVATION_RELPATH)] = mutated
        _rejected(payload, "outcome-producing projection", sources(git=git))

    # --- MAJOR 1: every eager boundary ---

    @pytest.mark.parametrize(
        "label,block", _EAGER_EXECUTION_MATRIX, ids=[e[0] for e in _EAGER_EXECUTION_MATRIX]
    )
    def test_every_eager_execution_boundary_fails_closed(self, label, block):
        with pytest.raises(A.ProjectionError):
            A.outcome_producing_projection_digest(_with_module_level_line(block))

    def test_deferred_bodies_are_pruned_rather_than_scanned(self):
        """The other half of execution-awareness: a body that only runs when CALLED is not scanned."""
        for block in (
            "def _deferred():\n    import builtins as _rb\n    _rb.__dict__.update(any=min)\n",
            "class _C:\n    def m(self):\n        import builtins as _rb\n"
            "        _rb.__dict__.update(any=min)\n",
            "_lazy = lambda: __import__('builtins').__dict__.update(any=min)\n",
        ):
            assert A.outcome_producing_projection_digest(
                _with_module_level_line(block)
            ) == A.outcome_producing_projection_digest(DERIVATION_SOURCE), block

    def test_the_traversal_is_execution_aware_not_ast_walk(self):
        """Independent of the production traversal: derived from Python's own execution semantics."""
        import ast as _ast

        source = (
            "import builtins as _rb\n"
            "def _f(_d=_rb.__dict__.update(any=min)):\n"
            "    _rb.__dict__.update(deferred=1)\n"
        )
        tree = _ast.parse(source)
        reached = {
            _ast.dump(node, include_attributes=False)
            for statement in tree.body
            for node in A._iter_eager_module_scope_nodes(statement)
            if isinstance(node, _ast.Call)
        }
        assert any("any" in entry for entry in reached), "the eager default was not reached"
        assert not any("deferred" in entry for entry in reached), "a deferred body was scanned"

    # --- MAJOR 2: aliased and call-returned callables ---

    @pytest.mark.parametrize(
        "label,block",
        _ALIASED_AND_RETURNED_CALLABLE_MATRIX,
        ids=[e[0] for e in _ALIASED_AND_RETURNED_CALLABLE_MATRIX],
    )
    def test_aliased_or_returned_dangerous_callables_fail_closed(self, label, block):
        with pytest.raises(A.ProjectionError):
            A.outcome_producing_projection_digest(_with_module_level_line(block))

    def test_a_call_returned_callable_is_unnameable_but_a_named_method_is_not(self):
        """The precise distinction MAJOR 2 required, checked on the decomposition directly."""
        import ast as _ast

        returned = _ast.parse("getattr(m, 'x')()").body[0].value
        assert A._callee_chain(returned.func) is None

        named_method = _ast.parse("Path(__file__).resolve()").body[0].value
        assert A._callee_chain(named_method.func) == ("Path", ("resolve",))

    def test_an_import_alias_resolves_to_the_imported_symbol(self):
        """Derived from the rendering grammar, not from any production allowlist."""
        assert A._imported_origin("from builtins import exec as _rexec") == ("builtins", "exec")
        assert A._imported_origin("from builtins import exec") == ("builtins", "exec")
        assert A._imported_origin("import builtins as _rb") == ("builtins", None)
        assert A._imported_origin("import builtins") == ("builtins", None)

    # --- precision: eager code is not refused merely for being eager ---

    @pytest.mark.parametrize(
        "label,block", _EAGER_PRECISION_MATRIX, ids=[e[0] for e in _EAGER_PRECISION_MATRIX]
    )
    def test_harmless_eager_code_is_neither_refused_nor_identity_changing(self, label, block):
        assert A.outcome_producing_projection_digest(
            _with_module_level_line(block)
        ) == A.outcome_producing_projection_digest(DERIVATION_SOURCE), label

    def test_the_real_module_has_eager_definition_time_code_that_still_projects(self):
        """The derivation module really does carry decorators and annotated defs."""
        import ast as _ast

        tree = _ast.parse(DERIVATION_SOURCE)
        definitions = [
            node
            for node in tree.body
            if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef))
        ]
        assert definitions, "the derivation module has no module-level definitions to protect"
        assert any(getattr(node, "decorator_list", None) for node in definitions)
        assert A.outcome_producing_projection_digest(DERIVATION_SOURCE)

    # --- nothing earlier was disturbed ---

    def test_the_identity_is_unchanged_by_this_correction(self):
        surface = A.project_outcome_producing_surface(DERIVATION_SOURCE)
        symbols = {
            line.split("::", 1)[0]
            for line in surface.splitlines()
            if not line.startswith("@ambient::")
        }
        assert len(A.OUTCOME_PRODUCING_PROJECTION_SEEDS) == 18
        assert len(symbols) == 26

    def test_the_live_projection_is_still_identical_to_the_accepted_package(self):
        live = A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        for anchor in (A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, A.EXECUTABLE_PACKAGE_MERGE_SHA):
            blob = subprocess.run(
                ["git", "show", f"{anchor}:{DERIVATION_RELPATH}"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout
            assert A.outcome_producing_projection_digest(blob) == live

    def test_all_earlier_protections_still_hold(self):
        baseline = A.outcome_producing_projection_digest(DERIVATION_SOURCE)
        for changing in (
            "from builtins import min as any\n",
            "if True:\n    from builtins import min as any\n",
            "any, _unused = min, None\n",
        ):
            assert A.outcome_producing_projection_digest(
                _with_module_level_line(changing)
            ) != baseline, changing
        for refusing in (
            _REPORTED_CALL_MEDIATED_MUTATION,
            "import builtins as _b\nvars(_b).update(any=min)\n",
        ):
            with pytest.raises(A.ProjectionError):
                A.outcome_producing_projection_digest(_with_module_level_line(refusing))
