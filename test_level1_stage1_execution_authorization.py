"""Adversarial tests for the ENDPOINT-0001 Stage-1 authorization mechanism (XASSET-0029).

CORRECTED AFTER INDEPENDENT FULL REVIEWS 4946327932, 4946397399, 4946464366 AND 4946540894.

The previous suite's "happy path" proved only that an internally consistent FICTION passes:
synthetic SHAs, invented review/acceptance/verification/CI ids, and a self-declared reviewer.
The review correctly called that the principal flaw. This suite is rebuilt so the happy path
runs against a MECHANICALLY AUTHENTICATED seam, and so that fiction fails.

Review 4946397399 then found that the CLAIMED/COMPLETED side bypassed that authentication
entirely -- a forged local claim made the PUBLIC result gate return authorized with no
attestation at all -- and that nothing bound the supplied result to the completed one. Both were
reproduced before correcting, and classes ``TestClaimAuthentication``, ``TestExactResultProvenance``
and ``TestPublicResultBoundary`` below attack the corrected paths directly.

Truth is injected through ``TruthSources`` rather than fetched live, so tests never touch
GitHub. The fake sources below are honest stand-ins for durable truth: they answer only for
identities that "exist", and the negative tests remove or alter exactly one fact at a time.

NO STAGE-1 EXECUTION OCCURS IN THIS FILE. No gate is evaluated, no construction is
dispositioned, no results document is produced, and no data is acquired. Lane records are
written to pytest ``tmp_path``, never to the real authorization location.
"""

from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest
import yaml

import level1_construction_universe_closure_validator as CU
import level1_endpoint_evidence_preregistration_validator as PREREG
import level1_stage1_execution_authorization as AUTH

REPO_ROOT = Path(__file__).resolve().parent

# Identities the fake truth sources will vouch for. They stand in for the real post-merge
# facts, which do not exist yet because XASSET-0029 has not merged.
HEAD = "a" * 40
MERGE = "b" * 40
BASE = AUTH.REVIEWED_BASE_SHA  # MAJOR 2: merge parent[0] must be the EXACT reviewed base
REVIEW_ID = "4900000001"
ACCEPT_ID = "5900000001"
VERIFY_ID = "5900000002"
RUN_ID = "3100000001"
JOB_ID = "9500000001"
REVIEWER_LOGIN = "independent-reviewer"
PRINCIPAL_LOGIN = AUTH.PRINCIPAL_ACCOUNT_LOGIN
AUTHOR_LOGIN = "implementation-author"
PR_URL = f"https://api.github.com/repos/{AUTH.REPOSITORY_IDENTITY}/issues/{AUTH.AUTHORIZING_PULL_REQUEST}"


class FakeGit:
    """Stands in for the local git object store. Answers only for commits that 'exist'."""

    def __init__(self, **overrides):
        self.parents = {
            MERGE: (BASE, HEAD),
            AUTH.PREDECESSOR_MERGE_SHA: (
                AUTH.PREDECESSOR_MERGE_BASE,
                AUTH.PREDECESSOR_ACCEPTED_HEAD,
            ),
            # EXTENDED BY XASSET-0037. The successor rebinding verifies three further identities
            # from git, so an honest stand-in must vouch for them too. Each is kept SEPARATE, in
            # exactly the shape the module distinguishes them: the HISTORICAL operational
            # authorization, the PACKAGE AUTHORITY, and the EXECUTABLE PACKAGE itself.
            AUTH.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA: (
                AUTH.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_BASE,
                AUTH.HISTORICAL_OPERATIONAL_AUTHORIZATION_ACCEPTED_HEAD,
            ),
            AUTH.PACKAGE_AUTHORIZING_MERGE_SHA: ("e" * 40, "f" * 40),
            AUTH.EXECUTABLE_PACKAGE_MERGE_SHA: (
                AUTH.EXECUTABLE_PACKAGE_MERGE_BASE,
                AUTH.EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
            ),
        }
        self.blobs = {}
        for rel in AUTH.LOAD_BEARING_RELPATHS:
            digest = AUTH.sha256_file(REPO_ROOT / rel)
            # Zero merge drift: the reviewed head and the merge carry identical bytes.
            self.blobs[(MERGE, rel)] = digest
            self.blobs[(HEAD, rel)] = digest
        # XASSET-0037 §G.B's invariant: the outcome-producing bytes are the accepted package's,
        # unchanged. The stand-in reproduces that rather than asserting it.
        for rel in AUTH.EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS:
            digest = AUTH.sha256_file(REPO_ROOT / rel)
            self.blobs[(AUTH.EXECUTABLE_PACKAGE_MERGE_SHA, rel)] = digest
            self.blobs[(AUTH.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, rel)] = digest
        self.trees = {
            MERGE: "t" * 40,
            HEAD: "t" * 40,
            AUTH.EXECUTABLE_PACKAGE_MERGE_SHA: "p" * 40,
            AUTH.EXECUTABLE_PACKAGE_ACCEPTED_HEAD: "p" * 40,
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
            AUTH.AUTHORIZING_PULL_REQUEST: {
                "base": {"repo": {"full_name": AUTH.REPOSITORY_IDENTITY}},
                "head": {"sha": HEAD},
                "merged": True,
                "merge_commit_sha": MERGE,
                "user": {"login": AUTHOR_LOGIN},
                "merged_at": "2026-08-16T12:00:00Z",
            }
        }
        self.review_records = {
            REVIEW_ID: {
                "commit_id": HEAD,
                "id": REVIEW_ID,
                "body": f"FORMAL DISPOSITION: {AUTH.APPROVING_REVIEW_DISPOSITION} — 0 BLOCKING",
                "user": {"login": REVIEWER_LOGIN},
                "state": "COMMENTED",
                "submitted_at": "2026-08-16T10:00:00Z",
                "html_url": f"{PR_URL}#pullrequestreview-{REVIEW_ID}",
            }
        }
        self.comments = {
            # MAJOR 1: the principal's acceptance must CERTIFY the exact independent review pass.
            ACCEPT_ID: {
                "body": f"Principal acceptance at exact head `{HEAD}`, relying on independent "
                        f"review {REVIEW_ID}.",
                "issue_url": PR_URL,
                "created_at": "2026-08-16T11:00:00Z",
                # BLOCKING 2: lifecycle gates must authenticate their ACTOR.
                "user": {"login": PRINCIPAL_LOGIN},
            },
            VERIFY_ID: {
                "body": f"Post-merge verification for merge `{MERGE}`.",
                "issue_url": PR_URL,
                "created_at": "2026-08-16T13:00:00Z",
                "user": {"login": PRINCIPAL_LOGIN},
            },
        }
        self.runs = {
            RUN_ID: {"status": "completed", "conclusion": "success", "head_sha": MERGE}
        }
        self.jobs = {
            JOB_ID: {"run_id": RUN_ID, "conclusion": "success", "head_sha": MERGE}
        }
        self.__dict__.update(overrides)

    def pull_request(self, number):
        return self.pulls.get(number)

    def review(self, number, review_id):
        return self.review_records.get(str(review_id)) if number in self.pulls else None

    def reviews(self, number):
        """MAJOR 2: the full review set, for finality checking."""
        return list(self.review_records.values()) if number in self.pulls else None

    def issue_comment(self, comment_id):
        return self.comments.get(str(comment_id))

    def workflow_run(self, run_id):
        return self.runs.get(str(run_id))

    def workflow_job(self, job_id):
        return self.jobs.get(str(job_id))


def sources(git=None, governance=None) -> AUTH.TruthSources:
    return AUTH.TruthSources(git=git or FakeGit(), governance=governance or FakeGovernance())


def lifecycle() -> dict:
    return {
        "gates_closed": list(AUTH.REQUIRED_LIFECYCLE_GATES),
        "independent_review": {
            "review_id": REVIEW_ID,
            "formal_disposition": AUTH.APPROVING_REVIEW_DISPOSITION,
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
    doc = AUTH.build_authorization_payload(
        authorization_head=HEAD,
        lifecycle_evidence=lifecycle(),
        author_identity=AUTHOR_LOGIN,
        generated_at_utc="2026-08-16T00:00:00Z",
        merge_sha=MERGE,
    )
    # build_authorization_payload derives load-bearing identity from the real git tree, which
    # does not contain the not-yet-merged XASSET-0029 head; align it with the fake merged tree.
    doc["load_bearing_identity"] = {
        rel: AUTH.sha256_file(REPO_ROOT / rel) for rel in sorted(AUTH.LOAD_BEARING_RELPATHS)
    }
    return doc


@pytest.fixture
def prereg() -> dict:
    return yaml.safe_load(
        (REPO_ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
            encoding="utf-8"
        )
    )


def _rejected(doc, fragment, src=None):
    result = AUTH.validate_authorization_document(doc, src or sources())
    assert not result.valid, f"expected refusal for {fragment!r}"
    assert any(fragment in e for e in result.errors), (
        f"expected error containing {fragment!r}, got {result.errors}"
    )


def _lane(tmp_path: Path) -> AUTH.LanePaths:
    return AUTH.LanePaths(
        authorization=tmp_path / "authorization.json",
        claim=tmp_path / "claim.json",
        completion=tmp_path / "completion.json",
        ledger=tmp_path / "lane_ledger.jsonl",
    )


def _arm(tmp_path: Path, doc) -> AUTH.LanePaths:
    paths = _lane(tmp_path)
    AUTH.write_authorization(doc, paths.authorization, sources())
    return paths


# =============================================================================================
# The authenticated happy path — and proof that fiction is NOT enough
# =============================================================================================


class TestAuthenticatedHappyPath:
    def test_authenticated_attestation_validates(self, payload):
        """The gate is passable against VERIFIED truth — otherwise the refusals prove nothing."""
        result = AUTH.validate_authorization_document(payload, sources())
        assert result.valid, result.errors

    def test_the_old_synthetic_fiction_now_fails(self):
        """Regression for BLOCKING 1: the previous suite's happy path must no longer pass.

        Identical shape to the pre-correction fixture — synthetic SHAs, invented ids, a
        self-declared reviewer — validated against truth sources that have never heard of any
        of it.
        """
        fiction = {
            "gates_closed": list(AUTH.REQUIRED_LIFECYCLE_GATES),
            "independent_review": {
                "review_id": "9999999999",
                "formal_disposition": AUTH.APPROVING_REVIEW_DISPOSITION,
                "blocking_count": 0,
                "major_count": 0,
                "reviewed_sha": "1" * 40,
                "reviewer_identity": "SYNTHETIC_INDEPENDENT_REVIEWER",
            },
            "principal_acceptance": {"comment_id": "8888888888", "accepted_head": "1" * 40},
            "merge": {"merge_sha": "2" * 40, "parents": ["3" * 40, "1" * 40]},
            "post_merge_verification": {
                "comment_id": "7777777777",
                "verified_merge_sha": "2" * 40,
            },
            "merge_commit_ci": {
                "run_id": "6666666666",
                "job_id": "5555555555",
                "status": "completed",
                "conclusion": "success",
                "head_sha": "2" * 40,
            },
        }
        doc = AUTH.build_authorization_payload(
            authorization_head="1" * 40,
            lifecycle_evidence=fiction,
            author_identity="SYNTHETIC_AUTHOR",
            generated_at_utc="2026-08-16T00:00:00Z",
            merge_sha="2" * 40,
        )
        result = AUTH.validate_authorization_document(doc, sources())
        assert not result.valid
        assert any("does not exist" in e or "is not the recorded" in e for e in result.errors)

    def test_unreachable_truth_source_fails_closed(self, payload):
        class Dead:
            def pull_request(self, number):
                return None

            def review(self, number, review_id):
                return None

            def issue_comment(self, comment_id):
                return None

            def workflow_run(self, run_id):
                return None

            def workflow_job(self, job_id):
                return None

        _rejected(payload, "could not be verified", sources(governance=Dead()))


# =============================================================================================
# 1-12 — lifecycle truth
# =============================================================================================


class TestLifecycleTruth:
    def test_01_fictional_but_well_formed_review_fails(self, payload):
        payload["lifecycle_evidence"]["independent_review"]["review_id"] = "4900000999"
        _rejected(payload, "does not exist on pull request")

    def test_02_fictional_acceptance_fails(self, payload):
        payload["lifecycle_evidence"]["principal_acceptance"]["comment_id"] = "5900009999"
        _rejected(payload, "principal acceptance comment")

    def test_02b_acceptance_not_naming_the_exact_head_fails(self, payload):
        gov = FakeGovernance()
        gov.comments[ACCEPT_ID] = {"body": "Principal acceptance at some other head."}
        _rejected(payload, "does not name the exact head", sources(governance=gov))

    def test_03_fictional_merge_fails(self, payload):
        payload["lifecycle_evidence"]["merge"]["merge_sha"] = "d" * 40
        _rejected(payload, "is not the real merge commit")

    def test_04_wrong_actual_parents_fail(self, payload):
        payload["lifecycle_evidence"]["merge"]["parents"] = [BASE, "e" * 40]
        _rejected(payload, "do not equal the real parents")

    def test_04b_squash_merge_without_the_accepted_head_fails(self, payload):
        git = FakeGit()
        git.parents[MERGE] = (BASE,)
        payload["lifecycle_evidence"]["merge"]["parents"] = [BASE]
        _rejected(payload, "parent(s); a squash", sources(git=git))

    def test_04c_second_parent_not_the_accepted_head_fails(self, payload):
        git = FakeGit()
        git.parents[MERGE] = (BASE, "f" * 40)
        payload["lifecycle_evidence"]["merge"]["parents"] = [BASE, "f" * 40]
        _rejected(payload, "is not the accepted head", sources(git=git))

    def test_05_fictional_postmerge_record_fails(self, payload):
        payload["lifecycle_evidence"]["post_merge_verification"]["comment_id"] = "5900009998"
        _rejected(payload, "post-merge verification comment")

    def test_06_fictional_ci_run_fails(self, payload):
        payload["lifecycle_evidence"]["merge_commit_ci"]["run_id"] = "3100009999"
        _rejected(payload, "workflow run")

    def test_06b_fictional_ci_job_fails(self, payload):
        payload["lifecycle_evidence"]["merge_commit_ci"]["job_id"] = "9500009999"
        _rejected(payload, "workflow job")

    @pytest.mark.parametrize(
        "status,conclusion", [("completed", "failure"), ("in_progress", None), ("completed", "cancelled")]
    )
    def test_06c_unsuccessful_ci_fails(self, payload, status, conclusion):
        gov = FakeGovernance()
        gov.runs[RUN_ID] = {"status": status, "conclusion": conclusion, "head_sha": MERGE}
        _rejected(payload, "not completed/success", sources(governance=gov))

    def test_06d_ci_for_another_commit_fails(self, payload):
        gov = FakeGovernance()
        gov.runs[RUN_ID] = {"status": "completed", "conclusion": "success", "head_sha": "9" * 40}
        _rejected(payload, "ran against", sources(governance=gov))

    def test_07_wrong_ci_job_run_pairing_fails(self, payload):
        gov = FakeGovernance()
        gov.jobs[JOB_ID] = {"run_id": "3100000777", "conclusion": "success", "head_sha": MERGE}
        _rejected(payload, "belongs to run", sources(governance=gov))

    def test_08_stale_reviewed_head_fails(self, payload):
        gov = FakeGovernance()
        gov.review_records[REVIEW_ID] = dict(gov.review_records[REVIEW_ID], commit_id="9" * 40)
        _rejected(payload, "was submitted against", sources(governance=gov))

    def test_08b_adverse_disposition_fails(self, payload):
        gov = FakeGovernance()
        gov.review_records[REVIEW_ID] = dict(
            gov.review_records[REVIEW_ID],
            body="FORMAL DISPOSITION: CHANGES REQUIRED — 1 BLOCKING",
        )
        _rejected(payload, "formal disposition is 'CHANGES REQUIRED'", sources(governance=gov))

    def test_09_reviewer_identity_cannot_be_self_declared(self, payload):
        """Claiming a different reviewer than the durable metadata reports is refused."""
        payload["lifecycle_evidence"]["independent_review"]["reviewer_identity"] = "I_SAY_SO"
        _rejected(payload, "reviewer identity may not be asserted")

    def test_10_reviewer_identity_is_derived_from_durable_truth(self, payload):
        """The accepted value must equal the login the source reports, not the caller's."""
        gov = FakeGovernance()
        gov.review_records[REVIEW_ID] = dict(gov.review_records[REVIEW_ID], user={"login": "someone-else"})
        _rejected(payload, "durable review metadata says", sources(governance=gov))

    def test_11_load_bearing_code_drift_fails(self, payload):
        """A merged tree whose enforcement code differs from the working tree is refused."""
        git = FakeGit()
        git.blobs[(MERGE, "level1_stage1_execution_authorization.py")] = "0" * 64
        _rejected(payload, "enforcement drift", sources(git=git))

    def test_11b_recorded_load_bearing_identity_must_match_the_merged_tree(self, payload):
        payload["load_bearing_identity"]["level1_stage1_execution_authorization.py"] = "1" * 64
        _rejected(payload, "load_bearing_identity")

    def test_11c_load_bearing_coverage_is_closed(self, payload):
        payload["load_bearing_identity"].pop("level1_stage1_execution_authorization.py")
        _rejected(payload, "must cover exactly the load-bearing files")

    def test_12_current_ancestry_drift_fails(self, payload):
        git = FakeGit()
        git._ancestor = False
        _rejected(payload, "is not an ancestor of the current HEAD", sources(git=git))

    def test_12b_predecessor_identity_is_verified_against_git(self, payload):
        """MAJOR 1: the contract promises the XASSET-0028 identity is bound, so it is."""
        git = FakeGit()
        git.parents[AUTH.PREDECESSOR_MERGE_SHA] = ("9" * 40, "8" * 40)
        _rejected(payload, "predecessor merge parents", sources(git=git))

    def test_12c_predecessor_identity_cannot_be_restated_wrongly(self, payload):
        payload["predecessor_identity"]["merge_sha"] = "7" * 40
        _rejected(payload, "predecessor_identity.merge_sha")

    def test_12d_wrong_pull_request_fails(self, payload):
        payload["authorizing_pull_request"] = 999
        _rejected(payload, "authorization.authorizing_pull_request")


# =============================================================================================
# 13-24 — the execution state machine
# =============================================================================================


class TestExecutionStateMachine:
    def test_13_no_attestation_means_not_ready(self, tmp_path):
        paths = _lane(tmp_path)
        state, reason = AUTH.lane_state_at(paths, sources())
        assert state == AUTH.LANE_ABSENT
        assert AUTH.new_execution_is_authorized(paths, sources())[0] is False
        assert "no attestation present" in reason

    def test_14_ready_permits_exactly_one_atomic_claim(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        assert AUTH.lane_state_at(paths, sources())[0] == AUTH.LANE_READY
        record = AUTH.claim_execution(claimed_at_utc="2026-08-16T01:00:00Z", paths=paths, sources=sources())
        assert record["execution_attempt_id"] == AUTH.EXECUTION_ATTEMPT_ID
        assert AUTH.lane_state_at(paths, sources())[0] == AUTH.LANE_CLAIMED

    def test_15_second_claim_fails(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        with pytest.raises((ValueError, FileExistsError)):
            AUTH.claim_execution(claimed_at_utc="t2", paths=paths, sources=sources())

    def test_16_claimed_lane_cannot_start_another_executor(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        allowed, reason = AUTH.new_execution_is_authorized(paths, sources())
        assert allowed is False
        assert "already claimed" in reason

    def test_17_crash_after_claim_does_not_reopen_the_lane(self, tmp_path, payload):
        """A process dying mid-execution leaves CLAIMED; recovery is a governed act."""
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        # Simulate a crash: nothing else was written, no completion exists.
        assert not paths.completion.exists()
        state, _ = AUTH.lane_state_at(paths, sources())
        assert state == AUTH.LANE_CLAIMED
        assert AUTH.new_execution_is_authorized(paths, sources())[0] is False

    def test_18_completion_must_match_the_claim_and_attempt(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        record = AUTH.complete_execution(
            completed_at_utc="t2",
            results=RESULT_A,
            paths=paths,
            sources=sources(),
        )
        assert record["execution_attempt_id"] == AUTH.EXECUTION_ATTEMPT_ID
        assert record["authorization_sha256"] == AUTH.sha256_file(paths.authorization)
        # MAJOR 3: the identity is DERIVED from the actual result, never caller-chosen.
        assert record["result_identity_sha256"] == AUTH.stage1_result_identity(RESULT_A)

    def test_18b_completion_without_a_claim_fails(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        with pytest.raises(ValueError):
            AUTH.complete_execution(
                completed_at_utc="t2", results=RESULT_A, paths=paths, sources=sources()
            )

    def test_18c_completion_cannot_accept_a_caller_chosen_digest(self, tmp_path, payload):
        """MAJOR 3: there is no public completion API taking a precomputed final digest."""
        import inspect

        parameters = inspect.signature(AUTH.complete_execution).parameters
        assert "result_identity_sha256" not in parameters
        assert "results" in parameters

        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        with pytest.raises(TypeError):
            AUTH.complete_execution(  # type: ignore[call-arg]
                completed_at_utc="t2",
                result_identity_sha256="a" * 64,
                paths=paths,
                sources=sources(),
            )

    def test_19_wrong_claim_hash_rejected(self, tmp_path, payload):
        """A claim bound to a different attestation cannot validate the current one."""
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        forged = json.loads(paths.claim.read_text(encoding="utf-8"))
        forged["authorization_sha256"] = "0" * 64
        paths.claim.write_text(AUTH.canonical_json(forged) + "\n", encoding="utf-8")
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is False
        # BLOCKING 1 (4946464366): rewriting claim.json alone now trips the ledger-mirror
        # consistency check FIRST -- strictly stronger than the previous hash comparison.
        assert "disagree" in reason

    def test_20_wrong_attempt_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        forged = json.loads(paths.claim.read_text(encoding="utf-8"))
        forged["execution_attempt_id"] = "ENDPOINT-0001::STAGE_1::ATTEMPT_2"
        paths.claim.write_text(AUTH.canonical_json(forged) + "\n", encoding="utf-8")
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is False
        assert "disagree" in reason

    def test_21_lawfully_claimed_execution_can_have_its_result_validated(self, tmp_path, payload):
        """BLOCKING 2 regression: claiming must NOT make the resulting output unvalidatable."""
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is True, reason
        AUTH.complete_execution(
            completed_at_utc="t2", results=RESULT_A, paths=paths, sources=sources()
        )
        assert AUTH.claimed_execution_is_authorized(paths, sources())[0] is True

    def test_22_result_without_a_lawful_claim_cannot_pass(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is False
        assert "no lawfully claimed Stage-1 execution exists" in reason

    def test_23_second_execution_after_completion_fails(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        AUTH.complete_execution(
            completed_at_utc="t2", results=RESULT_A, paths=paths, sources=sources()
        )
        allowed, reason = AUTH.new_execution_is_authorized(paths, sources())
        assert allowed is False
        assert "already completed" in reason
        with pytest.raises((ValueError, FileExistsError)):
            AUTH.claim_execution(claimed_at_utc="t3", paths=paths, sources=sources())

    def test_24_deleting_one_record_cannot_reset_the_lane(self, tmp_path, payload):
        """Durability boundary: the ledger independently establishes CLAIMED."""
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        paths.claim.unlink()
        state, reason = AUTH.lane_state_at(paths, sources())
        assert state == AUTH.LANE_CLAIMED
        assert AUTH.new_execution_is_authorized(paths, sources())[0] is False

    def test_24b_deleting_the_ledger_alone_cannot_reset_the_lane(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        paths.ledger.unlink()
        assert AUTH.lane_state_at(paths, sources())[0] == AUTH.LANE_CLAIMED

    def test_24c_destroying_everything_fails_closed_to_absent_not_ready(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        for path in (paths.claim, paths.ledger, paths.authorization):
            path.unlink()
        state, _ = AUTH.lane_state_at(paths, sources())
        assert state == AUTH.LANE_ABSENT
        assert AUTH.new_execution_is_authorized(paths, sources())[0] is False


# =============================================================================================
# Schema, identity, and bypass resistance (retained)
# =============================================================================================


class TestSchemaAndIdentity:
    def test_wrong_universe_hash_rejected(self, payload):
        payload["construction_universe"]["sha256"] = "0" * 64
        _rejected(payload, "construction_universe.sha256")

    def test_wrong_construction_count_rejected(self, payload):
        payload["construction_universe"]["count"] = 679
        _rejected(payload, "construction_universe.count")

    def test_wrong_canonical_pin_rejected(self, payload):
        payload["canonical_pins"][AUTH.CANONICAL_PROTOCOL_RELPATH] = "0" * 64
        _rejected(payload, "canonical_pins")

    def test_wrong_repository_rejected(self, payload):
        payload["repository"] = "SomeoneElse/Portfolio-HQ"
        _rejected(payload, "authorization.repository")

    def test_wrong_study_rejected(self, payload):
        payload["study_id"] = "RISK-0001"
        _rejected(payload, "authorization.study_id")

    def test_wrong_attempt_id_rejected(self, payload):
        payload["execution_attempt_id"] = "ENDPOINT-0001::STAGE_1::ATTEMPT_2"
        _rejected(payload, "authorization.execution_attempt_id")

    def test_unknown_key_rejected(self, payload):
        payload["extra_override"] = True
        _rejected(payload, "the schema is closed")

    def test_missing_key_rejected(self, payload):
        payload.pop("load_bearing_identity")
        _rejected(payload, "required key is absent")

    def test_non_mapping_rejected(self):
        _rejected(["nope"], "expected a mapping")

    def test_duplicate_json_keys_rejected(self, tmp_path):
        paths = _lane(tmp_path)
        paths.authorization.parent.mkdir(parents=True, exist_ok=True)
        paths.authorization.write_text('{"study_id": "A", "study_id": "B"}', encoding="utf-8")
        state, reason = AUTH.lane_state_at(paths, sources())
        assert state == AUTH.LANE_ABSENT
        assert "duplicate key" in reason

    def test_invalid_payload_never_reaches_disk(self, tmp_path, payload):
        payload["study_id"] = "WRONG"
        paths = _lane(tmp_path)
        with pytest.raises(ValueError):
            AUTH.write_authorization(payload, paths.authorization, sources())
        assert not paths.authorization.exists()

    def test_attestation_cannot_be_regenerated(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        with pytest.raises(FileExistsError):
            AUTH.write_authorization(payload, paths.authorization, sources())

    def test_public_predicates_take_no_bypass_parameter(self):
        with pytest.raises(TypeError):
            PREREG.validate_stage1_results({"candidate_results": []}, {})  # type: ignore[call-arg]

    def test_results_document_cannot_self_authorize(self):
        forged = {
            "candidate_results": [],
            "stage_1_executability": {"executable": True},
            "operationally_authorized": True,
            "claim": {"execution_attempt_id": AUTH.EXECUTION_ATTEMPT_ID},
        }
        result = PREREG.validate_stage1_results(forged)
        assert not result.ok
        assert any("not operationally authorized" in e for e in result.errors)

    def test_private_seam_confers_no_authorization(self):
        PREREG._validate_stage1_results_against_universe(
            {"candidate_results": []}, CU.frozen_construction_universe()
        )
        assert PREREG.stage_1_operational_authorization_is_effective()[0] is False
        assert PREREG.new_stage_1_execution_is_authorized()[0] is False


# =============================================================================================
# Preserved postures and non-execution
# =============================================================================================


class TestPreservedPostures:
    def test_current_repository_state_is_not_executable(self):
        assert PREREG.new_stage_1_execution_is_authorized()[0] is False
        assert PREREG.stage_1_operational_authorization_is_effective()[0] is False
        assert PREREG.validate_stage1_results({"candidate_results": []}).ok is False

    def test_no_real_lane_record_exists(self):
        for path in (
            AUTH.AUTHORIZATION_PATH,
            AUTH.CLAIM_PATH,
            AUTH.COMPLETION_PATH,
            AUTH.LEDGER_PATH,
        ):
            assert not path.exists(), f"{path} must not exist in this PR"

    def test_lane_records_live_outside_the_repository(self):
        for path in (AUTH.AUTHORIZATION_PATH, AUTH.CLAIM_PATH, AUTH.LEDGER_PATH):
            assert not str(path).startswith(str(REPO_ROOT))

    def test_universe_unchanged(self):
        assert CU.derived_cardinality() == 680
        assert len(CU.per_cell_cardinality()) == 48
        assert CU.universe_aggregate_sha256() == AUTH.CONSTRUCTION_UNIVERSE_SHA256

    def test_no_stage_1_result_or_application_artifact(self):
        assert list(REPO_ROOT.rglob("stage1_results.yaml")) == []
        assert not (REPO_ROOT / "intelligence/level1_application").exists()

    def test_no_market_or_economic_data_acquisition(self):
        """Governance metadata is permitted; market/economic data acquisition is not."""
        source = (REPO_ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        for banned in ("yfinance", "alpaca", "pandas_datareader", "quandl", "finance.yahoo"):
            assert banned not in source
        # The only network host is the GitHub governance API.
        assert "api.github.com" in source
        assert source.count("https://") == 1

    def test_no_risk_substance_reused(self):
        source = (REPO_ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        assert "phq-risk0001-results" not in source
        assert "import risk_level1" not in source
        assert "/private/tmp" not in source

    def test_no_allocator_or_margin_coupling(self):
        source = (REPO_ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        for banned in ("import allocate", "import margin_state", "import levels"):
            assert banned not in source

    def test_committed_boolean_posture(self, prereg):
        block = prereg["stage_1_executability"]
        assert block["executable"] is False
        assert block["executable_is_never_the_authorization_source"] is True
        assert block["authorized_by_xasset_0029"] is False

    def test_mechanism_block_never_claims_effectivity(self, prereg):
        mechanism = prereg["stage_1_operational_authorization"]
        assert mechanism["currently_effective"] is False
        assert mechanism["authorization_is_committed_state"] is False
        assert mechanism["authorization_is_external_runtime_evidence"] is True
        assert mechanism["one_shot"] is True
        assert mechanism["no_merge_to_execution_gap"] is True

    def test_state_machine_is_canonically_declared(self, prereg):
        machine = prereg["stage_1_operational_authorization"]["execution_state_machine"]
        assert machine["states"] == ["ABSENT", "READY", "CLAIMED", "COMPLETED"]
        assert machine["new_execution_permitted_in"] == "READY"
        assert machine["result_validation_permitted_in"] == ["CLAIMED", "COMPLETED"]

    def test_durability_boundary_is_canonically_stated(self, prereg):
        boundary = prereg["stage_1_operational_authorization"]["durability_boundary"]
        assert boundary["single_record_loss_reopens_lane"] is False
        assert boundary["total_directory_loss_state"] == "ABSENT"
        assert boundary["total_directory_loss_is_ready"] is False
        assert boundary["crash_after_claim_reopens_lane"] is False

    def test_canonical_has_exactly_one_current_lifecycle_state(self, prereg):
        """MAJOR 2: no operative field may still name a SPENT condition.

        AMENDED BY XASSET-0037. The property this test protects is unchanged and is what actually
        matters: exactly ONE operative lifecycle, with every superseded one confined to explicitly
        predecessor-named fields. The operative value moved XASSET-0029 -> XASSET-0037 when
        XASSET-0030 §G.B step 8's rebinding bound the XASSET-0036 executable package, so this now
        asserts the CURRENT operative source AND that XASSET-0029 survives exactly as history.
        Neither the check nor its strictness is weakened -- it gained an assertion.
        """
        lifecycle_block = prereg["lifecycle_effectivity"]
        assert "XASSET_0037" in lifecycle_block["stage_1_execution_may_begin_only_after"]
        assert lifecycle_block["stage_1_execution_precondition_amended_by"] == "XASSET-0037"
        # This filing's own accepted value, retained as HISTORY rather than rewritten.
        assert "XASSET_0029" in lifecycle_block[
            "predecessor_stage_1_execution_may_begin_only_after_xasset_0029"
        ]
        assert (
            lifecycle_block["predecessor_stage_1_execution_precondition_amended_by_xasset_0029"]
            == "XASSET-0029"
        )
        for key, value in lifecycle_block.items():
            if key.startswith("predecessor_") or not isinstance(value, str):
                continue
            assert "XASSET-0028 six-gate lifecycle above" not in value
            # No operative field may name a spent lifecycle as though it were current.
            assert not value.startswith("XASSET_0029_LIFECYCLE_CLOSURE")

    def test_stage_2_and_application_authority_withheld(self, prereg):
        assert prereg["stages"]["stage_2"]["authorized_by_xasset_0027"] is False
        assert PREREG.validate(prereg).ok

    def test_dropping_a_fail_closed_condition_rejected(self, prereg):
        prereg["stage_1_operational_authorization"]["must_fail_closed_on"] = ["NO_ATTESTATION_PRESENT"]
        assert not PREREG.validate(prereg).ok

    def test_removing_the_mechanism_block_rejected(self, prereg):
        del prereg["stage_1_operational_authorization"]
        assert not PREREG.validate(prereg).ok


# =============================================================================================
# A — CLAIM/ATTESTATION AUTHENTICATION (review 4946397399, BLOCKING 1)
# =============================================================================================


class TestClaimAuthentication:
    """A surviving claim record must never substitute for a valid attestation."""

    @staticmethod
    def _forged_claim(paths: AUTH.LanePaths, digest: str = "0" * 64) -> dict:
        return {
            "event": AUTH.LANE_CLAIMED,
            "execution_attempt_id": AUTH.EXECUTION_ATTEMPT_ID,
            "authorization_sha256": digest,
            "claimed_at_utc": "whenever",
        }

    def test_a1_forged_claim_without_attestation_rejected(self, tmp_path):
        paths = _lane(tmp_path)
        paths.claim.parent.mkdir(parents=True, exist_ok=True)
        paths.claim.write_text(AUTH.canonical_json(self._forged_claim(paths)) + "\n")
        # State detection may still report CLAIMED; lawful provenance must not follow from it.
        assert AUTH.lane_state_at(paths, sources())[0] == AUTH.LANE_CLAIMED
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is False
        assert "no longer exists" in reason

    def test_a2_forged_ledger_claim_without_attestation_rejected(self, tmp_path):
        paths = _lane(tmp_path)
        paths.ledger.parent.mkdir(parents=True, exist_ok=True)
        paths.ledger.write_text(AUTH.canonical_json(self._forged_claim(paths)) + "\n")
        assert AUTH.lane_state_at(paths, sources())[0] == AUTH.LANE_CLAIMED
        assert AUTH.claimed_execution_is_authorized(paths, sources())[0] is False

    def test_a3_claim_bound_to_malformed_attestation_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        paths.authorization.write_text("{ not json", encoding="utf-8")
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is False
        assert "not the one this claim bound" in reason or "unusable" in reason

    def test_a4_claim_bound_to_unauthenticated_lifecycle_rejected(self, tmp_path, payload):
        """The attestation survives byte-for-byte, but GitHub truth no longer supports it."""
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        gov = FakeGovernance()
        gov.review_records.pop(REVIEW_ID)
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources(governance=gov))
        assert ok is False
        assert "no longer validates against durable truth" in reason

    def test_a5_attestation_deleted_after_claim_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        paths.authorization.unlink()
        assert AUTH.claimed_execution_is_authorized(paths, sources())[0] is False

    def test_a6_canonical_drift_after_claim_rejected(self, tmp_path, payload, monkeypatch):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        monkeypatch.setattr(
            AUTH, "CANONICAL_PINS", dict(AUTH.CANONICAL_PINS, **{AUTH.CANONICAL_PROTOCOL_RELPATH: "9" * 64})
        )
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is False
        assert "canonical" in reason

    def test_a7_load_bearing_drift_after_claim_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        git = FakeGit()
        git.blobs[(MERGE, "level1_stage1_execution_authorization.py")] = "0" * 64
        assert AUTH.claimed_execution_is_authorized(paths, sources(git=git))[0] is False

    def test_a8_governance_drift_after_claim_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        gov = FakeGovernance()
        gov.runs[RUN_ID] = {"status": "completed", "conclusion": "failure", "head_sha": MERGE}
        assert AUTH.claimed_execution_is_authorized(paths, sources(governance=gov))[0] is False

    def test_a9_ancestry_drift_after_claim_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        git = FakeGit()
        git._ancestor = False
        assert AUTH.claimed_execution_is_authorized(paths, sources(git=git))[0] is False


# =============================================================================================
# B — EXACT RESULT PROVENANCE (review 4946397399, BLOCKING 2)
# =============================================================================================

RESULT_A = {"candidate_results": [], "note": "A"}
RESULT_B = {"candidate_results": [], "note": "B"}


class TestExactResultProvenance:
    @staticmethod
    def _complete(paths, results):
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        return AUTH.complete_execution(
            completed_at_utc="t2",
            results=results,
            paths=paths,
            sources=sources(),
        )

    def test_b1_exact_completed_result_authorized(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        self._complete(paths, RESULT_A)
        ok, reason = AUTH.completed_result_is_authorized(RESULT_A, paths, sources())
        assert ok is True, reason

    def test_b2_substituted_result_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        self._complete(paths, RESULT_A)
        ok, reason = AUTH.completed_result_is_authorized(RESULT_B, paths, sources())
        assert ok is False
        assert "may not be published" in reason

    def test_b3_one_field_change_after_completion_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        self._complete(paths, RESULT_A)
        mutated = dict(RESULT_A, note="A ")
        assert AUTH.completed_result_is_authorized(mutated, paths, sources())[0] is False

    def test_b4_claimed_but_not_completed_rejects_publication(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        ok, reason = AUTH.completed_result_is_authorized(RESULT_A, paths, sources())
        assert ok is False
        assert "has not been completed" in reason

    def test_b5_wrong_completion_result_hash_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        self._complete(paths, RESULT_A)
        forged = json.loads(paths.completion.read_text(encoding="utf-8"))
        forged["result_identity_sha256"] = "5" * 64
        paths.completion.write_text(AUTH.canonical_json(forged) + "\n", encoding="utf-8")
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is False

    def test_b6_wrong_completion_attempt_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        self._complete(paths, RESULT_A)
        forged = json.loads(paths.completion.read_text(encoding="utf-8"))
        forged["execution_attempt_id"] = "ENDPOINT-0001::STAGE_1::ATTEMPT_2"
        paths.completion.write_text(AUTH.canonical_json(forged) + "\n", encoding="utf-8")
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is False

    def test_b7_completion_after_claim_file_loss_preserves_exact_binding(self, tmp_path, payload):
        """Claim-file loss must not produce null binding fields; the ledger carries identity."""
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        expected_claim_sha = AUTH.sha256_file(paths.claim)
        paths.claim.unlink()
        record = AUTH.complete_execution(
            completed_at_utc="t2",
            results=RESULT_A,
            paths=paths,
            sources=sources(),
        )
        assert record["authorization_sha256"] is not None
        assert record["claim_sha256"] == expected_claim_sha
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is True

    def test_b8_corrupt_ledger_cannot_substitute_for_the_claim(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        paths.claim.unlink()
        paths.ledger.write_text("{ not json\n", encoding="utf-8")
        with pytest.raises(ValueError):
            AUTH.complete_execution(
                completed_at_utc="t2",
                results=RESULT_A,
                paths=paths,
                sources=sources(),
            )

    def test_b9_ambiguous_ledger_claims_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        conflicting = json.loads(paths.claim.read_text(encoding="utf-8"))
        conflicting["claimed_at_utc"] = "a-different-time"
        with paths.ledger.open("a", encoding="utf-8") as handle:
            handle.write(AUTH.canonical_json(conflicting) + "\n")
        paths.claim.unlink()
        record, claim_sha, problem = AUTH._recover_claim_record(paths)
        # Review 4946540894 MINOR 1: two events now fail closed on COUNT before the distinct-value
        # comparison is reached -- strictly stronger, and the message names which shape it saw.
        assert record is None
        assert "conflicting" in problem and "fails closed" in problem


# =============================================================================================
# C — GOVERNANCE TRUTH IDENTITY, CHRONOLOGY AND FINALITY (review 4946397399, MAJOR 1)
# =============================================================================================


class TestGovernanceIdentity:
    def test_c1_acceptance_belonging_to_another_pr_rejected(self, payload):
        gov = FakeGovernance()
        gov.comments[ACCEPT_ID] = dict(
            gov.comments[ACCEPT_ID], issue_url="https://api.github.com/repos/x/y/issues/999"
        )
        _rejected(payload, "does not belong to pull request", sources(governance=gov))

    def test_c2_postmerge_belonging_to_another_pr_rejected(self, payload):
        gov = FakeGovernance()
        gov.comments[VERIFY_ID] = dict(
            gov.comments[VERIFY_ID], issue_url="https://api.github.com/repos/x/y/issues/999"
        )
        _rejected(payload, "does not belong to pull request", sources(governance=gov))

    def test_c3_acceptance_omitting_the_review_id_rejected(self, payload):
        """MAJOR 1: the principal must certify the exact independent review pass."""
        gov = FakeGovernance()
        gov.comments[ACCEPT_ID] = dict(
            gov.comments[ACCEPT_ID], body=f"Principal acceptance at exact head `{HEAD}`."
        )
        _rejected(payload, "does not certify the independent review", sources(governance=gov))

    def test_c4_dismissed_review_rejected(self, payload):
        gov = FakeGovernance()
        gov.review_records[REVIEW_ID] = dict(gov.review_records[REVIEW_ID], state="DISMISSED")
        _rejected(payload, "DISMISSED", sources(governance=gov))

    def test_c5_acceptance_before_review_rejected(self, payload):
        gov = FakeGovernance()
        gov.comments[ACCEPT_ID] = dict(gov.comments[ACCEPT_ID], created_at="2026-08-16T09:00:00Z")
        _rejected(payload, "precedes review", sources(governance=gov))

    def test_c6_merge_before_acceptance_rejected(self, payload):
        gov = FakeGovernance()
        gov.pulls[AUTH.AUTHORIZING_PULL_REQUEST] = dict(
            gov.pulls[AUTH.AUTHORIZING_PULL_REQUEST], merged_at="2026-08-16T10:30:00Z"
        )
        _rejected(payload, "precedes acceptance", sources(governance=gov))

    def test_c7_postmerge_verification_before_merge_rejected(self, payload):
        gov = FakeGovernance()
        gov.comments[VERIFY_ID] = dict(gov.comments[VERIFY_ID], created_at="2026-08-16T11:30:00Z")
        _rejected(payload, "precedes the merge", sources(governance=gov))

    def test_c8_review_not_owned_by_the_pull_request_rejected(self, payload):
        gov = FakeGovernance()
        gov.review_records[REVIEW_ID] = dict(gov.review_records[REVIEW_ID], html_url="https://example.invalid/x")
        _rejected(payload, "does not belong to pull request", sources(governance=gov))

    def test_c9_author_identity_is_not_an_authorization_fact(self, payload):
        """Changing informational author metadata must not change the verdict either way."""
        payload["author_identity"] = "someone-entirely-different"
        assert AUTH.validate_authorization_document(payload, sources()).valid is True


# =============================================================================================
# D — EXACT REVIEWED BASE AND ZERO MERGE DRIFT (review 4946397399, MAJOR 2)
# =============================================================================================


class TestExactBaseAndMergeDrift:
    def test_d1_first_parent_not_the_reviewed_base_rejected(self, payload):
        git = FakeGit()
        git.parents[MERGE] = ("9" * 40, HEAD)
        payload["lifecycle_evidence"]["merge"]["parents"] = ["9" * 40, HEAD]
        _rejected(payload, "is not the exact reviewed base", sources(git=git))

    def test_d2_second_parent_not_the_accepted_head_rejected(self, payload):
        git = FakeGit()
        git.parents[MERGE] = (BASE, "8" * 40)
        payload["lifecycle_evidence"]["merge"]["parents"] = [BASE, "8" * 40]
        _rejected(payload, "is not the accepted head", sources(git=git))

    def test_d3_merge_tree_differing_from_accepted_head_tree_rejected(self, payload):
        git = FakeGit()
        git.trees[MERGE] = "z" * 40
        _rejected(payload, "differs from the accepted head tree", sources(git=git))

    def test_d4_load_bearing_blob_changed_by_the_merge_rejected(self, payload):
        """The merged tree may not become its own source of truth."""
        git = FakeGit()
        git.blobs[(HEAD, "level1_stage1_execution_authorization.py")] = "4" * 64
        _rejected(payload, "merge drift", sources(git=git))

    def test_d5_reviewed_base_is_bound_to_the_current_lifecycles_own_base(self):
        """AMENDED BY XASSET-0037. The base a lifecycle is reviewed against is per-lifecycle.

        This filing's own accepted value, `c51e9460…`, was XASSET-0029's base and is retained
        below as history. XASSET-0030 §G.B step 8's rebinding branches from the XASSET-0036
        executable package's merge, so THAT is what the current lifecycle must bind. Asserting
        the equality mechanically -- rather than repeating a literal twice -- is what makes a
        rebinding to some OTHER commit fail here.
        """
        assert AUTH.REVIEWED_BASE_SHA == AUTH.EXECUTABLE_PACKAGE_MERGE_SHA
        assert AUTH.REVIEWED_BASE_SHA == "3e5de8f85c69c2e5dc2b75421446b5db996d7cf1"
        # XASSET-0029's own accepted base, retained verbatim as history.
        assert (
            AUTH.HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_BASE
            == "c51e94609eff7ede2bdfa084844d59b8347561e5"
        )


# =============================================================================================
# E — THE ACTUAL PUBLIC BOUNDARY (review 4946397399, BLOCKING 2 / MINOR 2)
# =============================================================================================


class TestPublicResultBoundary:
    """These call the REAL public validator, not a helper predicate."""

    @staticmethod
    def _publish(tmp_path, payload, completed, monkeypatch):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        AUTH.complete_execution(
            completed_at_utc="t2",
            results=completed,
            paths=paths,
            sources=sources(),
        )
        # Point the module's DEFAULT lane and truth sources at the synthetic fixture, so the
        # public validator is exercised through its real no-argument boundary. Build the sources
        # object before patching, since the helper constructs AUTH.TruthSources itself.
        fixture_sources = sources()
        monkeypatch.setattr(AUTH, "AUTHORIZATION_PATH", paths.authorization)
        monkeypatch.setattr(AUTH, "CLAIM_PATH", paths.claim)
        monkeypatch.setattr(AUTH, "COMPLETION_PATH", paths.completion)
        monkeypatch.setattr(AUTH, "LEDGER_PATH", paths.ledger)
        monkeypatch.setattr(AUTH, "LanePaths", lambda: paths)
        monkeypatch.setattr(AUTH, "TruthSources", lambda: fixture_sources)
        return paths

    def test_e1_exact_completed_result_clears_the_public_authorization_gate(
        self, tmp_path, payload, monkeypatch
    ):
        """The exact completed artifact passes AUTHORIZATION and reaches structural validation.

        Deliberately asserted this way rather than ``outcome.ok``. Reaching a fully-passing
        result would require 680 fabricated dispositions, and this PR must execute no
        construction and produce no Stage-1 content. The precise, honest proof is that the
        authorization half is cleared -- no authorization error survives -- and the ONLY
        remaining failure is structural completeness, which is exactly what a real Stage-1
        execution would supply. Compare ``test_e2``, where an authorization error DOES appear.
        """
        result = {"candidate_results": []}
        self._publish(tmp_path, payload, result, monkeypatch)
        outcome = PREREG.validate_stage1_results(result)
        assert not any("not operationally authorized" in e for e in outcome.errors), outcome.errors
        assert all("registered construction" in e for e in outcome.errors), outcome.errors

    def test_e2_substituted_result_fails_the_public_validator(
        self, tmp_path, payload, monkeypatch
    ):
        self._publish(tmp_path, payload, {"candidate_results": []}, monkeypatch)
        outcome = PREREG.validate_stage1_results({"candidate_results": [], "note": "substituted"})
        assert not outcome.ok
        assert any("not operationally authorized" in e for e in outcome.errors)

    def test_e3_unauthenticated_result_fails_the_public_validator(self):
        assert PREREG.validate_stage1_results({"candidate_results": []}).ok is False

    def test_e4_no_bypass_parameter_exists_on_the_public_boundary(self):
        import inspect

        signature = inspect.signature(PREREG.validate_stage1_results)
        assert list(signature.parameters) == ["results"]


# =============================================================================================
# F — MIRROR CONSISTENCY, ACTOR AUTHENTICATION, REVIEW FINALITY, RESULT-IDENTITY CONTRACT
# (review 4946464366: BLOCKING 1, BLOCKING 2, MAJOR 1, MAJOR 2, MAJOR 3)
# =============================================================================================


class TestMirrorConsistency:
    """BLOCKING 1: the file and its ledger mirror are a consistency check, not alternatives."""

    @staticmethod
    def _completed(tmp_path, payload, results=RESULT_A):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        AUTH.complete_execution(
            completed_at_utc="t2", results=results, paths=paths, sources=sources()
        )
        return paths

    def test_f1_completion_retarget_from_a_to_b_rejected(self, tmp_path, payload):
        """THE reproduction: rewrite only completion.json to bind B; B must still fail."""
        paths = self._completed(tmp_path, payload, RESULT_A)
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is True

        retargeted = json.loads(paths.completion.read_text(encoding="utf-8"))
        retargeted["result_identity_sha256"] = AUTH.stage1_result_identity(RESULT_B)
        paths.completion.write_text(AUTH.canonical_json(retargeted) + "\n", encoding="utf-8")

        ok, reason = AUTH.completed_result_is_authorized(RESULT_B, paths, sources())
        assert ok is False, "retargeting the lawful run from A to B must fail"
        assert "consistent, mirror-verified" in reason
        # ...and A is not silently resurrected either: the record is now inconsistent.
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is False

    def test_f2_appended_conflicting_completion_rejected(self, tmp_path, payload):
        paths = self._completed(tmp_path, payload, RESULT_A)
        rogue = {
            "event": AUTH.LANE_COMPLETED,
            "execution_attempt_id": AUTH.EXECUTION_ATTEMPT_ID,
            "authorization_sha256": AUTH.sha256_file(paths.authorization),
            "claim_sha256": AUTH.sha256_file(paths.claim),
            "result_identity_sha256": AUTH.stage1_result_identity(RESULT_B),
            "completed_at_utc": "t9",
        }
        with paths.ledger.open("a", encoding="utf-8") as handle:
            handle.write(AUTH.canonical_json(rogue) + "\n")
        assert AUTH.completed_result_is_authorized(RESULT_B, paths, sources())[0] is False
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is False

    def test_f3_completion_file_ledger_mismatch_rejected(self, tmp_path, payload):
        paths = self._completed(tmp_path, payload, RESULT_A)
        altered = json.loads(paths.completion.read_text(encoding="utf-8"))
        altered["completed_at_utc"] = "tampered"
        paths.completion.write_text(AUTH.canonical_json(altered) + "\n", encoding="utf-8")
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is False

    def test_f4_claim_file_ledger_mismatch_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        altered = json.loads(paths.claim.read_text(encoding="utf-8"))
        altered["claimed_at_utc"] = "tampered"
        paths.claim.write_text(AUTH.canonical_json(altered) + "\n", encoding="utf-8")
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is False and "disagree" in reason

    def test_f5_corrupt_claimed_ledger_with_claim_file_present_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        with paths.ledger.open("a", encoding="utf-8") as handle:
            handle.write("{ not json\n")
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is False and "corrupt" in reason

    def test_f6_corrupt_completed_ledger_with_completion_file_present_rejected(
        self, tmp_path, payload
    ):
        paths = self._completed(tmp_path, payload, RESULT_A)
        with paths.ledger.open("a", encoding="utf-8") as handle:
            handle.write("{ not json\n")
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is False

    def test_f7_single_record_loss_behaves_exactly_as_the_durability_contract_promises(
        self, tmp_path, payload
    ):
        """Losing ONE record is the disclosed, permitted case and must still work."""
        paths = self._completed(tmp_path, payload, RESULT_A)
        paths.completion.unlink()  # file lost, ledger survives
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is True
        assert AUTH.completed_result_is_authorized(RESULT_B, paths, sources())[0] is False


class TestCompletionIsAlsoOneShot:
    """BLOCKING 1 (review 4953842000). The one CLAIMED -> COMPLETED transition may happen once.

    Every lane here is an ISOLATED ``tmp_path`` lane with the fake truth sources. The real
    ``AUTHORIZATION_ROOT`` is never created, read as authority, or touched, and no real
    attestation, claim, completion, or ledger entry is produced -- and therefore the real
    ``ATTEMPT_1`` is never claimed, completed, or consumed.
    """

    @staticmethod
    def _claimed(tmp_path, payload) -> AUTH.LanePaths:
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        return paths

    def test_the_real_authorization_root_is_absent_throughout(self):
        assert not AUTH.AUTHORIZATION_ROOT.exists()

    def test_completion_gates_on_the_active_predicate(self):
        """Checked against the parsed CODE, so the docstring's historical explanation of the
        superseded predicate cannot decide this either way."""
        import ast

        source = inspect.getsource(AUTH.complete_execution)
        called = [
            node.func.id
            for node in ast.walk(ast.parse(source.lstrip()))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        ]
        assert "active_execution_is_authorized" in called
        assert "claimed_execution_is_authorized" not in called
        # ...and the gate must be asked BEFORE binding any identity or writing anything.
        assert called.index("active_execution_is_authorized") < called.index(
            "stage1_result_identity"
        )
        assert called.index("active_execution_is_authorized") < called.index("_write_once")

    def test_the_broader_predicate_is_still_broad_for_completed_result_authentication(self):
        assert "LANE_CLAIMED, LANE_COMPLETED" in inspect.getsource(
            AUTH.claimed_execution_is_authorized
        )
        assert "claimed_execution_is_authorized" in inspect.getsource(
            AUTH.completed_result_is_authorized
        )

    def test_an_authenticated_claim_completes_exactly_once(self, tmp_path, payload):
        paths = self._claimed(tmp_path, payload)
        assert AUTH.active_execution_is_authorized(paths, sources())[0] is True
        record = AUTH.complete_execution(
            completed_at_utc="t2", results=RESULT_A, paths=paths, sources=sources()
        )
        assert record["result_identity_sha256"] == AUTH.stage1_result_identity(RESULT_A)
        assert AUTH.lane_state_at(paths, sources())[0] == AUTH.LANE_COMPLETED
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is True

    def test_completed_cannot_complete_again(self, tmp_path, payload):
        paths = self._claimed(tmp_path, payload)
        AUTH.complete_execution(
            completed_at_utc="t2", results=RESULT_A, paths=paths, sources=sources()
        )
        # The broader predicate is deliberately still true here; the narrower one is not.
        assert AUTH.claimed_execution_is_authorized(paths, sources())[0] is True
        assert AUTH.active_execution_is_authorized(paths, sources())[0] is False
        with pytest.raises(ValueError) as excinfo:
            AUTH.complete_execution(
                completed_at_utc="t3", results=RESULT_B, paths=paths, sources=sources()
            )
        assert "not actively claimed" in str(excinfo.value)
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is True

    def test_after_completion_mirror_loss_a_second_completion_is_rejected(
        self, tmp_path, payload, monkeypatch
    ):
        """THE reproduction. The permitted single-record loss must not become a second
        transition: with completion.json gone, O_EXCL no longer protects it, so the GATE has
        to refuse -- before any identity is bound, any file is created, or the ledger grows."""
        paths = self._claimed(tmp_path, payload)
        AUTH.complete_execution(
            completed_at_utc="t2", results=RESULT_A, paths=paths, sources=sources()
        )
        paths.completion.unlink()
        ledger_before = paths.ledger.read_bytes()
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is True

        bound = []
        monkeypatch.setattr(
            AUTH, "stage1_result_identity", lambda r: bound.append(r) or ("0" * 64)
        )
        with pytest.raises(ValueError) as excinfo:
            AUTH.complete_execution(
                completed_at_utc="t3", results=RESULT_B, paths=paths, sources=sources()
            )
        assert "not actively claimed" in str(excinfo.value)
        assert bound == [], "no result identity may be computed before the gate passes"
        assert not paths.completion.exists(), "no completion file may be created"
        assert paths.ledger.read_bytes() == ledger_before, "the ledger must be byte-unchanged"

    def test_the_surviving_ledger_event_still_authorizes_a_and_rejects_b(
        self, tmp_path, payload
    ):
        """The durability contract survives the rejected call, rather than being poisoned."""
        paths = self._claimed(tmp_path, payload)
        AUTH.complete_execution(
            completed_at_utc="t2", results=RESULT_A, paths=paths, sources=sources()
        )
        paths.completion.unlink()
        with pytest.raises(ValueError):
            AUTH.complete_execution(
                completed_at_utc="t3", results=RESULT_B, paths=paths, sources=sources()
            )
        events = [entry.get("event") for entry in AUTH._read_ledger(paths.ledger)]
        assert events.count(AUTH.LANE_COMPLETED) == 1
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is True
        assert AUTH.completed_result_is_authorized(RESULT_B, paths, sources())[0] is False

    def test_reverting_only_the_completion_gate_reproduces_the_failure(
        self, tmp_path, payload, monkeypatch
    ):
        """Mutation proof, in-suite: restore the pre-correction predicate and nothing else."""
        paths = self._claimed(tmp_path, payload)
        AUTH.complete_execution(
            completed_at_utc="t2", results=RESULT_A, paths=paths, sources=sources()
        )
        paths.completion.unlink()
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is True

        monkeypatch.setattr(
            AUTH, "active_execution_is_authorized", AUTH.claimed_execution_is_authorized
        )
        AUTH.complete_execution(
            completed_at_utc="t3", results=RESULT_B, paths=paths, sources=sources()
        )
        events = [entry.get("event") for entry in AUTH._read_ledger(paths.ledger)]
        assert events.count(AUTH.LANE_COMPLETED) == 2, "the second transition went through"
        # Duplicated completion provenance now authorizes NEITHER result.
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is False
        assert AUTH.completed_result_is_authorized(RESULT_B, paths, sources())[0] is False


class TestLifecycleActorAuthentication:
    """BLOCKING 2: a qualifying comment from the wrong account may not impersonate a gate."""

    def test_f8_acceptance_from_the_wrong_user_rejected(self, payload):
        gov = FakeGovernance()
        gov.comments[ACCEPT_ID] = dict(gov.comments[ACCEPT_ID], user={"login": "impostor"})
        _rejected(payload, "not the principal", sources(governance=gov))

    def test_f9_postmerge_verification_from_the_wrong_user_rejected(self, payload):
        gov = FakeGovernance()
        gov.comments[VERIFY_ID] = dict(gov.comments[VERIFY_ID], user={"login": "impostor"})
        _rejected(payload, "not the lifecycle operator", sources(governance=gov))

    def test_f10_acceptance_without_any_user_identity_rejected(self, payload):
        gov = FakeGovernance()
        gov.comments[ACCEPT_ID] = {
            k: v for k, v in gov.comments[ACCEPT_ID].items() if k != "user"
        }
        _rejected(payload, "carries no durable author identity", sources(governance=gov))

    def test_f11_postmerge_without_any_user_identity_rejected(self, payload):
        gov = FakeGovernance()
        gov.comments[VERIFY_ID] = {
            k: v for k, v in gov.comments[VERIFY_ID].items() if k != "user"
        }
        _rejected(payload, "carries no durable author identity", sources(governance=gov))

    def test_f12_correct_principal_identity_passes(self, payload):
        assert AUTH.validate_authorization_document(payload, sources()).valid is True


class TestExactFormalDisposition:
    """MAJOR 1: the verdict is parsed exactly, not matched as a substring."""

    def test_f13_adverse_formal_line_with_later_approval_phrase_rejected(self, payload):
        gov = FakeGovernance()
        gov.review_records[REVIEW_ID] = dict(
            gov.review_records[REVIEW_ID],
            body=(
                "FORMAL DISPOSITION: CHANGES REQUIRED — 2 BLOCKING\n\n"
                "The prior pass was APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE, but this one "
                "is not."
            ),
        )
        _rejected(payload, "formal disposition is 'CHANGES REQUIRED'", sources(governance=gov))

    def test_f14_exact_approving_formal_line_passes(self, payload):
        assert AUTH.validate_authorization_document(payload, sources()).valid is True

    def test_f15_self_reported_zero_counts_cannot_rescue_an_adverse_review(self, payload):
        """The attestation says 0 BLOCKING / 0 MAJOR; the durable review says otherwise."""
        assert payload["lifecycle_evidence"]["independent_review"]["blocking_count"] == 0
        gov = FakeGovernance()
        gov.review_records[REVIEW_ID] = dict(
            gov.review_records[REVIEW_ID],
            body="FORMAL DISPOSITION: CHANGES REQUIRED — 3 BLOCKING",
        )
        _rejected(payload, "formal disposition is 'CHANGES REQUIRED'", sources(governance=gov))

    def test_f16_body_without_a_formal_line_rejected(self, payload):
        gov = FakeGovernance()
        gov.review_records[REVIEW_ID] = dict(
            gov.review_records[REVIEW_ID], body="looks fine to me"
        )
        _rejected(payload, "no parseable", sources(governance=gov))

    @pytest.mark.parametrize(
        "body,expected",
        [
            ("FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE", True),
            ("FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE — 0 BLOCKING", True),
            ("FORMAL DISPOSITION: CHANGES REQUIRED — 1 BLOCKING", False),
            ("FORMAL DISPOSITION: BLOCKING", False),
        ],
    )
    def test_f17_disposition_parser_grammar(self, body, expected):
        verdict = AUTH.parse_formal_disposition(body)
        assert (verdict == AUTH.APPROVING_REVIEW_DISPOSITION) is expected


class TestReviewFinality:
    """MAJOR 2: a later adverse exact-head review invalidates an earlier certified pass."""

    @staticmethod
    def _extra(gov, review_id, commit, submitted, verdict, state="COMMENTED"):
        gov.review_records[review_id] = {
            "id": review_id,
            "commit_id": commit,
            "body": f"FORMAL DISPOSITION: {verdict}",
            "user": {"login": REVIEWER_LOGIN},
            "state": state,
            "submitted_at": submitted,
            "html_url": f"{PR_URL}#pullrequestreview-{review_id}",
        }
        return gov

    def test_f18_earlier_adverse_then_selected_clean_passes(self, payload):
        gov = self._extra(
            FakeGovernance(), "4900000000", HEAD, "2026-08-16T09:00:00Z", "CHANGES REQUIRED"
        )
        assert AUTH.validate_authorization_document(payload, sources(governance=gov)).valid is True

    def test_f19_later_adverse_same_head_rejected(self, payload):
        gov = self._extra(
            FakeGovernance(), "4900000002", HEAD, "2026-08-16T10:30:00Z", "CHANGES REQUIRED"
        )
        _rejected(payload, "later adverse formal disposition", sources(governance=gov))

    def test_f20_later_adverse_on_an_older_head_does_not_invalidate(self, payload):
        gov = self._extra(
            FakeGovernance(), "4900000003", "9" * 40, "2026-08-16T10:30:00Z", "CHANGES REQUIRED"
        )
        assert AUTH.validate_authorization_document(payload, sources(governance=gov)).valid is True

    def test_f21_later_dismissed_adverse_does_not_invalidate(self, payload):
        gov = self._extra(
            FakeGovernance(),
            "4900000004",
            HEAD,
            "2026-08-16T10:30:00Z",
            "CHANGES REQUIRED",
            state="DISMISSED",
        )
        assert AUTH.validate_authorization_document(payload, sources(governance=gov)).valid is True

    def test_f22_unavailable_review_list_fails_closed(self, payload):
        class NoList(FakeGovernance):
            def reviews(self, number):
                return None

        _rejected(payload, "finality cannot be established", sources(governance=NoList()))


class TestResultIdentityContract:
    """MAJOR 3: the canonical name and the implementation must agree exactly."""

    def test_f23_completion_derives_identity_from_the_actual_result(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        record = AUTH.complete_execution(
            completed_at_utc="t2", results=RESULT_A, paths=paths, sources=sources()
        )
        assert record["result_identity_sha256"] == AUTH.stage1_result_identity(RESULT_A)

    def test_f24_reordered_keys_have_the_same_semantic_identity(self):
        assert AUTH.stage1_result_identity({"a": 1, "b": 2}) == AUTH.stage1_result_identity(
            {"b": 2, "a": 1}
        )

    def test_f25_changed_content_changes_identity(self):
        assert AUTH.stage1_result_identity(RESULT_A) != AUTH.stage1_result_identity(RESULT_B)

    def test_f26_canonical_wording_matches_the_implementation(self, prereg):
        mechanism = prereg["stage_1_operational_authorization"]
        identity = mechanism["result_identity"]
        assert identity["is_artifact_byte_hash"] is False
        assert identity["derived_by_completion_not_supplied"] is True
        binds = mechanism["execution_state_machine"]["completion_binds"]
        assert "EXACT_STAGE1_RESULT_SEMANTIC_IDENTITY_SHA256" in binds
        # The misleading artifact-byte wording must be gone everywhere.
        assert "EXACT_RESULT_ARTIFACT_SHA256" not in yaml.safe_dump(prereg)

    def test_f27_canonical_actor_binding_is_stated(self, prereg):
        actors = prereg["stage_1_operational_authorization"]["lifecycle_actor_authentication"]
        assert actors["principal_acceptance_author_must_be"] == AUTH.PRINCIPAL_ACCOUNT_LOGIN
        assert actors["post_merge_verification_author_must_be"] == AUTH.LIFECYCLE_OPERATOR_LOGIN
        assert actors["formal_disposition_parsed_exactly"] is True
        assert actors["selected_review_must_be_final"] is True


# =============================================================================================
# G — REVIEW-LIST COMPLETENESS AND FINALITY CLASSIFICATION (review 4946540894, MAJOR 1)
# =============================================================================================


class PagedGovernance(FakeGovernance):
    """A governance source whose review listing is genuinely paginated.

    ``pages`` maps 1-indexed page number -> list of review records, or ``None`` to simulate a page
    whose retrieval/decoding failed. ``reviews()`` mirrors the production contract: walk pages
    until a short page proves exhaustion, and return ``None`` if ANY page fails.
    """

    PAGE_SIZE = 100

    def __init__(self, pages, **overrides):
        super().__init__(**overrides)
        self._pages = pages

    def reviews(self, number):
        if number not in self.pulls:
            return None
        collected = []
        page = 1
        while True:
            payload = self._pages.get(page)
            if payload is None:
                return None
            collected.extend(payload)
            if len(payload) < self.PAGE_SIZE:
                return collected
            page += 1


def _review(review_id, commit, submitted, *, body=None, state="COMMENTED"):
    return {
        "id": review_id,
        "commit_id": commit,
        "body": body if body is not None else f"FORMAL DISPOSITION: {AUTH.APPROVING_REVIEW_DISPOSITION}",
        "user": {"login": REVIEWER_LOGIN},
        "state": state,
        "submitted_at": submitted,
        "html_url": f"{PR_URL}#pullrequestreview-{review_id}",
    }


SELECTED = _review(REVIEW_ID, HEAD, "2026-08-16T10:00:00Z")


class TestReviewListCompleteness:
    def test_g1_more_than_one_hundred_reviews_are_all_seen(self, payload):
        """A full first page must not be mistaken for the whole list."""
        page1 = [
            _review(f"49000{i:05d}", "9" * 40, "2026-08-15T00:00:00Z")
            for i in range(PagedGovernance.PAGE_SIZE - 1)
        ] + [SELECTED]
        page2 = [_review("4900099999", "8" * 40, "2026-08-15T01:00:00Z")]
        gov = PagedGovernance({1: page1, 2: page2})
        assert len(gov.reviews(AUTH.AUTHORIZING_PULL_REQUEST)) == PagedGovernance.PAGE_SIZE + 1
        assert AUTH.validate_authorization_document(payload, sources(governance=gov)).valid is True

    def test_g2_adverse_review_on_a_later_page_is_detected(self, payload):
        """The reproduction: an adverse exact-head review hiding on page 2."""
        page1 = [
            _review(f"49000{i:05d}", "9" * 40, "2026-08-15T00:00:00Z")
            for i in range(PagedGovernance.PAGE_SIZE - 1)
        ] + [SELECTED]
        page2 = [
            _review(
                "4900088888",
                HEAD,
                "2026-08-16T10:30:00Z",
                body="FORMAL DISPOSITION: CHANGES REQUIRED — 1 BLOCKING",
            )
        ]
        gov = PagedGovernance({1: page1, 2: page2})
        _rejected(payload, "later adverse formal disposition", sources(governance=gov))

    def test_g3_failed_later_page_retrieval_fails_closed(self, payload):
        page1 = [
            _review(f"49000{i:05d}", "9" * 40, "2026-08-15T00:00:00Z")
            for i in range(PagedGovernance.PAGE_SIZE - 1)
        ] + [SELECTED]
        gov = PagedGovernance({1: page1, 2: None})  # page 2 fails
        assert gov.reviews(AUTH.AUTHORIZING_PULL_REQUEST) is None
        _rejected(payload, "finality cannot be established", sources(governance=gov))

    def test_g4_clean_multi_page_history_passes(self, payload):
        page1 = [
            _review(f"49000{i:05d}", "9" * 40, "2026-08-15T00:00:00Z")
            for i in range(PagedGovernance.PAGE_SIZE - 1)
        ] + [SELECTED]
        page2 = [
            _review("4900077777", HEAD, "2026-08-16T09:00:00Z"),  # earlier: legitimate history
            _review("4900077778", HEAD, "2026-08-16T10:30:00Z", state="APPROVED"),
        ]
        gov = PagedGovernance({1: page1, 2: page2})
        assert AUTH.validate_authorization_document(payload, sources(governance=gov)).valid is True

    def test_g5_live_source_paginates_and_fails_closed(self):
        """The production source's contract, exercised without touching the network."""
        source = AUTH.LiveGovernanceTruthSource()
        assert source.REVIEW_PAGE_SIZE == 100

        pages, calls = {}, []
        pages[1] = [{"id": i} for i in range(100)]
        pages[2] = [{"id": 100}]

        def fake_get_list(path):
            calls.append(path)
            page = int(path.rsplit("page=", 1)[1])
            return pages.get(page)

        source._get_list = fake_get_list  # type: ignore[assignment]
        assert len(source.reviews(328)) == 101
        assert len(calls) == 2 and "page=2" in calls[1]

        pages.pop(2)  # page 2 now fails
        calls.clear()
        assert source.reviews(328) is None

    def test_g6_page_ceiling_refuses_to_assert_completeness(self):
        source = AUTH.LiveGovernanceTruthSource()
        source._get_list = lambda path: [{"id": 0}] * source.REVIEW_PAGE_SIZE  # never short
        assert source.reviews(328) is None


class TestFinalityClassification:
    def test_g7_native_changes_requested_without_formal_text_is_adverse(self, payload):
        """GitHub's native state is durable truth and must not be weaker than body grammar."""
        gov = FakeGovernance()
        gov.review_records["4900000009"] = _review(
            "4900000009",
            HEAD,
            "2026-08-16T10:30:00Z",
            body="no formal line here at all",
            state="CHANGES_REQUESTED",
        )
        _rejected(payload, "non-dismissed CHANGES_REQUESTED", sources(governance=gov))

    def test_g8_malformed_later_exact_head_review_fails_closed(self, payload):
        gov = FakeGovernance()
        gov.review_records["4900000010"] = _review(
            "4900000010", HEAD, "2026-08-16T10:30:00Z", body="FORMAL DISPOSITION", state="COMMENTED"
        )
        _rejected(payload, "cannot be proven non-adverse", sources(governance=gov))

    def test_g9_later_native_approved_without_formal_text_is_not_adverse(self, payload):
        gov = FakeGovernance()
        gov.review_records["4900000011"] = _review(
            "4900000011", HEAD, "2026-08-16T10:30:00Z", body="looks good", state="APPROVED"
        )
        assert AUTH.validate_authorization_document(payload, sources(governance=gov)).valid is True

    def test_g10_dismissed_native_changes_requested_remains_non_live(self, payload):
        gov = FakeGovernance()
        gov.review_records["4900000012"] = _review(
            "4900000012",
            HEAD,
            "2026-08-16T10:30:00Z",
            body="no formal line",
            state="DISMISSED",
        )
        assert AUTH.validate_authorization_document(payload, sources(governance=gov)).valid is True

    def test_g11_earlier_unclassifiable_review_remains_history(self, payload):
        """Only reviews AFTER the certified pass are in scope."""
        gov = FakeGovernance()
        gov.review_records["4900000013"] = _review(
            "4900000013",
            HEAD,
            "2026-08-16T09:00:00Z",
            body="unparseable",
            state="CHANGES_REQUESTED",
        )
        assert AUTH.validate_authorization_document(payload, sources(governance=gov)).valid is True

    def test_g12_native_changes_requested_on_an_older_head_does_not_invalidate(self, payload):
        gov = FakeGovernance()
        gov.review_records["4900000014"] = _review(
            "4900000014", "7" * 40, "2026-08-16T10:30:00Z", body="", state="CHANGES_REQUESTED"
        )
        assert AUTH.validate_authorization_document(payload, sources(governance=gov)).valid is True


# =============================================================================================
# H — LEDGER STRICTNESS (review 4946540894, MINOR 1)
# =============================================================================================


class TestLedgerStrictness:
    @pytest.mark.parametrize(
        "line,label", [("[]", "list"), ('"junk"', "string"), ("null", "null"), ("42", "scalar")]
    )
    def test_h1_valid_json_that_is_not_a_mapping_is_corrupt(self, tmp_path, line, label):
        """Silently dropping these was weaker than the canonical fail-closed promise."""
        paths = _lane(tmp_path)
        paths.ledger.parent.mkdir(parents=True, exist_ok=True)
        paths.ledger.write_text(line + "\n", encoding="utf-8")
        entries = AUTH._read_ledger(paths.ledger)
        assert any(e.get("event") == "CORRUPT" for e in entries), f"{label} must be corrupt"

    @pytest.mark.parametrize("line", ["[]", '"junk"', "null", "42"])
    def test_h2_non_mapping_ledger_line_blocks_claim_provenance(self, tmp_path, payload, line):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        with paths.ledger.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is False and "corrupt" in reason

    def test_h3_duplicate_identical_claimed_events_fail_closed(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        duplicate = paths.ledger.read_text(encoding="utf-8")
        with paths.ledger.open("a", encoding="utf-8") as handle:
            handle.write(duplicate)  # byte-identical second CLAIMED
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is False
        assert "identical duplicate" in reason and "fails closed" in reason

    def test_h4_duplicate_identical_completed_events_fail_closed(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        AUTH.complete_execution(
            completed_at_utc="t2", results=RESULT_A, paths=paths, sources=sources()
        )
        completed_line = [
            line
            for line in paths.ledger.read_text(encoding="utf-8").splitlines()
            if '"COMPLETED"' in line
        ][0]
        with paths.ledger.open("a", encoding="utf-8") as handle:
            handle.write(completed_line + "\n")
        ok, reason = AUTH.completed_result_is_authorized(RESULT_A, paths, sources())
        assert ok is False
        assert "identical duplicate" in reason or "mirror-verified" in reason

    def test_h5_single_record_loss_still_behaves_as_governed(self, tmp_path, payload):
        """The already-accepted durability behaviour must be unchanged by this hardening."""
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        expected_claim_sha = AUTH.sha256_file(paths.claim)
        paths.claim.unlink()  # one mirror lost, the other survives
        record, claim_sha, problem = AUTH._recover_claim_record(paths)
        assert record is not None and problem == ""
        assert claim_sha == expected_claim_sha
        assert AUTH.claimed_execution_is_authorized(paths, sources())[0] is True

    def test_h6_ledger_absent_with_surviving_file_still_recovers(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        paths.ledger.unlink()
        assert AUTH.claimed_execution_is_authorized(paths, sources())[0] is True


# =============================================================================================
# I. A ledger already known to be corrupt must block READY -> CLAIMED
#
# MINOR 1 (review 4946706062). Reproduced before correcting: with a valid attestation and a
# pre-seeded corrupt ledger line, lane_state_at() returned READY, new_execution_is_authorized()
# returned true, and claim_execution() wrote claim.json and appended CLAIMED onto the corrupt
# ledger -- consuming the ONE authorized attempt under already-invalid audit state. Only the
# later claimed_execution_is_authorized() noticed.
# =============================================================================================


CORRUPT_LINES = ["{not json", "[]", '"junk"', "null", "42"]


class TestCorruptLedgerBlocksNewExecution:
    @pytest.mark.parametrize("line", CORRUPT_LINES)
    def test_i1_corrupt_ledger_prevents_ready_despite_valid_attestation(
        self, tmp_path, payload, line
    ):
        """The exact reproduction: a VALID attestation must not make a corrupt lane READY."""
        paths = _arm(tmp_path, payload)
        paths.ledger.write_text(line + "\n", encoding="utf-8")

        # The attestation itself is still perfectly good -- so this proves the ledger, not the
        # attestation, is what refuses.
        assert AUTH.validate_authorization_document(payload, sources()).valid

        state, reason = AUTH.lane_state_at(paths, sources())
        assert state == AUTH.LANE_ABSENT, f"{line!r} must not leave the lane READY"
        assert state != AUTH.LANE_READY
        assert "corrupt" in reason

    @pytest.mark.parametrize("line", CORRUPT_LINES)
    def test_i2_new_execution_is_not_authorized_over_a_corrupt_ledger(
        self, tmp_path, payload, line
    ):
        paths = _arm(tmp_path, payload)
        paths.ledger.write_text(line + "\n", encoding="utf-8")
        authorized, reason = AUTH.new_execution_is_authorized(paths, sources())
        assert authorized is False
        assert "corrupt" in reason and "governed act" in reason

    @pytest.mark.parametrize("line", CORRUPT_LINES)
    def test_i3_claim_refuses_and_writes_nothing_at_all(self, tmp_path, payload, line):
        """The whole point: refusal must happen BEFORE any side effect, not after."""
        paths = _arm(tmp_path, payload)
        paths.ledger.write_text(line + "\n", encoding="utf-8")
        before = paths.ledger.read_bytes()

        with pytest.raises(ValueError, match="corrupt"):
            AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())

        assert not paths.claim.exists(), "no claim file may be created"
        assert not paths.completion.exists()
        assert paths.ledger.read_bytes() == before, "no ledger event may be appended"

    def test_i4_corrupt_entry_alongside_a_valid_entry_is_still_refused(self, tmp_path, payload):
        """One well-formed line must not launder a corrupt sibling."""
        paths = _arm(tmp_path, payload)
        paths.ledger.write_text(
            AUTH.canonical_json({"event": "NOTE", "detail": "benign"}) + "\n[]\n",
            encoding="utf-8",
        )
        assert AUTH.new_execution_is_authorized(paths, sources())[0] is False

    def test_i5_corrupt_ledger_without_any_attestation_still_fails_closed(self, tmp_path):
        """No attestation AND a corrupt ledger is still not READY -- fail-closed either way."""
        paths = _lane(tmp_path)
        paths.ledger.parent.mkdir(parents=True, exist_ok=True)
        paths.ledger.write_text("[]\n", encoding="utf-8")
        state, reason = AUTH.lane_state_at(paths, sources())
        assert state == AUTH.LANE_ABSENT and reason
        with pytest.raises(ValueError):
            AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        assert not paths.claim.exists()

    def test_i6_an_already_claimed_lane_still_reports_claimed(self, tmp_path, payload):
        """PRESERVED: the CLAIMED/COMPLETED mirror logic is deliberately untouched.

        Had the corrupt check been placed BEFORE the claim determination, this lane would
        report ABSENT and `claimed_execution_is_authorized` would lose its precise
        corrupt-ledger provenance error in favour of a bare "lane state ABSENT".
        """
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        with paths.ledger.open("a", encoding="utf-8") as handle:
            handle.write("[]\n")

        state, _ = AUTH.lane_state_at(paths, sources())
        assert state == AUTH.LANE_CLAIMED

        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is False
        assert "corrupt" in reason and "provenance" in reason

    def test_i7_an_already_completed_lane_still_reports_completed(self, tmp_path, payload):
        """PRESERVED: a completed lane is COMPLETED, not retroactively ABSENT."""
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        AUTH.complete_execution(
            completed_at_utc="t2", results=RESULT_A, paths=paths, sources=sources()
        )
        with paths.ledger.open("a", encoding="utf-8") as handle:
            handle.write("[]\n")

        state, reason = AUTH.lane_state_at(paths, sources())
        assert state == AUTH.LANE_COMPLETED
        assert "already completed" in reason
        assert AUTH.completed_result_is_authorized(RESULT_A, paths, sources())[0] is False

    @pytest.mark.parametrize("body", ["", "\n", "   \n\n"])
    def test_i8_a_clean_or_empty_ledger_does_not_over_fire(self, tmp_path, payload, body):
        """The refusal must fire on corruption ONLY -- an empty or blank ledger is not corrupt."""
        paths = _arm(tmp_path, payload)
        paths.ledger.write_text(body, encoding="utf-8")
        assert AUTH.new_execution_is_authorized(paths, sources()) == (True, "")

    def test_i9_an_absent_ledger_is_still_ready(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        assert not paths.ledger.exists()
        assert AUTH.lane_state_at(paths, sources())[0] == AUTH.LANE_READY

    def test_i10_the_corrupt_marker_constant_matches_what_the_reader_emits(self, tmp_path):
        """Three sites must agree on the marker; a divergence is how MINOR 1 stayed hidden."""
        paths = _lane(tmp_path)
        paths.ledger.parent.mkdir(parents=True, exist_ok=True)
        paths.ledger.write_text("{not json\n", encoding="utf-8")
        assert AUTH._read_ledger(paths.ledger) == [{"event": AUTH.LEDGER_CORRUPT}]
        assert AUTH.LEDGER_CORRUPT not in (
            AUTH.LANE_ABSENT,
            AUTH.LANE_READY,
            AUTH.LANE_CLAIMED,
            AUTH.LANE_COMPLETED,
        ), "the corrupt marker must not collide with a lane state"
