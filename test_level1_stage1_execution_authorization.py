"""Adversarial tests for the ENDPOINT-0001 Stage-1 authorization mechanism (XASSET-0029).

CORRECTED AFTER INDEPENDENT FULL REVIEW 4946327932.

The previous suite's "happy path" proved only that an internally consistent FICTION passes:
synthetic SHAs, invented review/acceptance/verification/CI ids, and a self-declared reviewer.
The review correctly called that the principal flaw. This suite is rebuilt so the happy path
runs against a MECHANICALLY AUTHENTICATED seam, and so that fiction fails.

Truth is injected through ``TruthSources`` rather than fetched live, so tests never touch
GitHub. The fake sources below are honest stand-ins for durable truth: they answer only for
identities that "exist", and the negative tests remove or alter exactly one fact at a time.

NO STAGE-1 EXECUTION OCCURS IN THIS FILE. No gate is evaluated, no construction is
dispositioned, no results document is produced, and no data is acquired. Lane records are
written to pytest ``tmp_path``, never to the real authorization location.
"""

from __future__ import annotations

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
BASE = "c" * 40
REVIEW_ID = "4900000001"
ACCEPT_ID = "5900000001"
VERIFY_ID = "5900000002"
RUN_ID = "3100000001"
JOB_ID = "9500000001"
REVIEWER_LOGIN = "independent-reviewer"
AUTHOR_LOGIN = "implementation-author"


class FakeGit:
    """Stands in for the local git object store. Answers only for commits that 'exist'."""

    def __init__(self, **overrides):
        self.parents = {
            MERGE: (BASE, HEAD),
            AUTH.PREDECESSOR_MERGE_SHA: (
                AUTH.PREDECESSOR_MERGE_BASE,
                AUTH.PREDECESSOR_ACCEPTED_HEAD,
            ),
        }
        self.blobs = {
            (MERGE, rel): AUTH.sha256_file(REPO_ROOT / rel)
            for rel in AUTH.LOAD_BEARING_RELPATHS
        }
        self._head = MERGE
        self._ancestor = True
        self.__dict__.update(overrides)

    def commit_parents(self, sha):
        return self.parents.get(sha)

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
            }
        }
        self.reviews = {
            REVIEW_ID: {
                "commit_id": HEAD,
                "body": f"FORMAL DISPOSITION: {AUTH.APPROVING_REVIEW_DISPOSITION} — 0 BLOCKING",
                "user": {"login": REVIEWER_LOGIN},
            }
        }
        self.comments = {
            ACCEPT_ID: {"body": f"Principal acceptance at exact head `{HEAD}`."},
            VERIFY_ID: {"body": f"Post-merge verification for merge `{MERGE}`."},
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
        return self.reviews.get(str(review_id)) if number in self.pulls else None

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
        gov.reviews[REVIEW_ID] = dict(gov.reviews[REVIEW_ID], commit_id="9" * 40)
        _rejected(payload, "was submitted against", sources(governance=gov))

    def test_08b_adverse_disposition_fails(self, payload):
        gov = FakeGovernance()
        gov.reviews[REVIEW_ID] = dict(gov.reviews[REVIEW_ID], body="CHANGES REQUIRED")
        _rejected(payload, "approving formal", sources(governance=gov))

    def test_09_reviewer_identity_cannot_be_self_declared(self, payload):
        """Claiming a different reviewer than the durable metadata reports is refused."""
        payload["lifecycle_evidence"]["independent_review"]["reviewer_identity"] = "I_SAY_SO"
        _rejected(payload, "reviewer identity may not be asserted")

    def test_10_reviewer_identity_is_derived_from_durable_truth(self, payload):
        """The accepted value must equal the login the source reports, not the caller's."""
        gov = FakeGovernance()
        gov.reviews[REVIEW_ID] = dict(gov.reviews[REVIEW_ID], user={"login": "someone-else"})
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
            result_identity_sha256="a" * 64,
            paths=paths,
            sources=sources(),
        )
        assert record["execution_attempt_id"] == AUTH.EXECUTION_ATTEMPT_ID
        assert record["authorization_sha256"] == AUTH.sha256_file(paths.authorization)
        assert record["result_identity_sha256"] == "a" * 64

    def test_18b_completion_without_a_claim_fails(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        with pytest.raises(ValueError):
            AUTH.complete_execution(
                completed_at_utc="t2", result_identity_sha256="a" * 64, paths=paths, sources=sources()
            )

    def test_18c_completion_requires_a_real_result_identity(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        with pytest.raises(ValueError):
            AUTH.complete_execution(
                completed_at_utc="t2", result_identity_sha256="not-a-digest", paths=paths, sources=sources()
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
        assert "different attestation" in reason

    def test_20_wrong_attempt_rejected(self, tmp_path, payload):
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        forged = json.loads(paths.claim.read_text(encoding="utf-8"))
        forged["execution_attempt_id"] = "ENDPOINT-0001::STAGE_1::ATTEMPT_2"
        paths.claim.write_text(AUTH.canonical_json(forged) + "\n", encoding="utf-8")
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is False
        assert "not 'ENDPOINT-0001::STAGE_1::ATTEMPT_1'" in reason

    def test_21_lawfully_claimed_execution_can_have_its_result_validated(self, tmp_path, payload):
        """BLOCKING 2 regression: claiming must NOT make the resulting output unvalidatable."""
        paths = _arm(tmp_path, payload)
        AUTH.claim_execution(claimed_at_utc="t1", paths=paths, sources=sources())
        ok, reason = AUTH.claimed_execution_is_authorized(paths, sources())
        assert ok is True, reason
        AUTH.complete_execution(
            completed_at_utc="t2", result_identity_sha256="b" * 64, paths=paths, sources=sources()
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
            completed_at_utc="t2", result_identity_sha256="c" * 64, paths=paths, sources=sources()
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

    def test_canonical_v5_has_exactly_one_current_lifecycle_state(self, prereg):
        """MAJOR 2: no operative field may still name the spent XASSET-0028 condition."""
        lifecycle_block = prereg["lifecycle_effectivity"]
        assert "XASSET_0029" in lifecycle_block["stage_1_execution_may_begin_only_after"]
        assert lifecycle_block["stage_1_execution_precondition_amended_by"] == "XASSET-0029"
        for key, value in lifecycle_block.items():
            if key.startswith("predecessor_") or not isinstance(value, str):
                continue
            assert "XASSET-0028 six-gate lifecycle above" not in value

    def test_stage_2_and_application_authority_withheld(self, prereg):
        assert prereg["stages"]["stage_2"]["authorized_by_xasset_0027"] is False
        assert PREREG.validate(prereg).ok

    def test_dropping_a_fail_closed_condition_rejected(self, prereg):
        prereg["stage_1_operational_authorization"]["must_fail_closed_on"] = ["NO_ATTESTATION_PRESENT"]
        assert not PREREG.validate(prereg).ok

    def test_removing_the_mechanism_block_rejected(self, prereg):
        del prereg["stage_1_operational_authorization"]
        assert not PREREG.validate(prereg).ok
