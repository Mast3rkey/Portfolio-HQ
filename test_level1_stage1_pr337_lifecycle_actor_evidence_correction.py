"""XASSET-0042 — adversarial proof that the PR #337 actor-evidence exception cannot generalize.

WHAT IS UNDER TEST
==================

Two comments in PR #337's completed lifecycle -- principal acceptance ``5335697214`` and
post-merge verification ``5335849767`` -- were posted through an App-token write path GitHub
attributes to ``claude[bot]``. XASSET-0041 authorizes exactly ONE bounded correction, under ten
conjunctive properties. This suite proves the implemented correction satisfies them.

HOW IT TESTS
============

Through the PUBLIC validator :func:`verify_lifecycle_against_truth`, never by reaching into the
exception's internals, and always with ISOLATED Git/GitHub truth stand-ins. Nothing here touches
live GitHub, the lane, the filesystem, or any outcome-producing module.

THE PROPERTY EVERY TEST DEFENDS
===============================

The exception is a CONJUNCTION over the five exact PR #337 identities, the exact ratified actor,
and XASSET-0041's entire completed lifecycle. Break any single conjunct and the ordinary actor
error returns with its wording unchanged. That is what "cannot generalize" means mechanically.
"""

from __future__ import annotations

import ast
import copy
from pathlib import Path

import pytest

import level1_stage1_execution_authorization as AUTH

REPO_ROOT = Path(__file__).resolve().parent

# --------------------------------------------------------------------------------------
# The real, exactly pinned identities. Taken from the module so a pin change breaks here.
# --------------------------------------------------------------------------------------

P337 = AUTH.RATIFIED_PULL_REQUEST
P337_HEAD = AUTH.RATIFIED_HEAD_SHA
P337_REVIEW = AUTH.RATIFIED_REVIEW_ID
P337_ACCEPT = AUTH.RATIFIED_ACCEPTANCE_COMMENT_ID
P337_MERGE = AUTH.RATIFIED_MERGE_SHA
P337_VERIFY = AUTH.RATIFIED_POST_MERGE_VERIFICATION_COMMENT_ID
BOT = AUTH.RATIFIED_HISTORICAL_ACTOR

P341 = AUTH.RATIFICATION_PULL_REQUEST
P341_HEAD = AUTH.RATIFICATION_HEAD_SHA
P341_BASE = AUTH.RATIFICATION_BASE_SHA
P341_REVIEW = AUTH.RATIFICATION_REVIEW_ID
P341_RATIFY = AUTH.RATIFICATION_COMMENT_ID
P341_MERGE = AUTH.RATIFICATION_MERGE_SHA
P341_VERIFY = AUTH.RATIFICATION_POST_MERGE_VERIFICATION_COMMENT_ID
P341_CLOSURE = AUTH.RATIFICATION_FINAL_CLOSURE_COMMENT_ID
P341_RUN = AUTH.RATIFICATION_CI_RUN_ID
P341_JOB = AUTH.RATIFICATION_CI_JOB_ID

PRINCIPAL = AUTH.PRINCIPAL_ACCOUNT_LOGIN

#: The retracted, mis-attributed acceptance attempt. It must never qualify as anything.
VOID_COMMENT_ID = "5345204885"

#: Real PR #337 merge parents, so git truth in the fixtures is not invented.
P337_BASE = AUTH.REVIEWED_BASE_SHA

# Real timestamps, so chronology is exercised against the true ordering.
T_REVIEW_337 = "2026-08-18T23:10:37Z"
T_ACCEPT_337 = "2026-08-18T23:50:29Z"
T_MERGE_337 = "2026-08-18T23:50:58Z"
T_VERIFY_337 = "2026-08-19T00:12:40Z"
T_RATIFY = "2026-08-19T16:47:08Z"

APPROVING = f"FORMAL DISPOSITION: {AUTH.APPROVING_REVIEW_DISPOSITION} — 0 BLOCKING"


def _issue_url(number: int) -> str:
    return f"https://api.github.com/repos/{AUTH.REPOSITORY_IDENTITY}/issues/{number}"


def ratification_body() -> str:
    """A faithful stand-in for the real XASSET-0041 §G ratification."""
    return (
        f"Principal exact-head acceptance at `{P341_HEAD}`, relying on independent review "
        f"{P341_REVIEW}.\n\n"
        f"I retrospectively ratify the PR #{P337} lifecycle: final head `{P337_HEAD}`, "
        f"review {P337_REVIEW}, acceptance comment {P337_ACCEPT}, merge "
        f"`{P337_MERGE}`, post-merge verification {P337_VERIFY}.\n\n"
        f"Acceptance comment {P337_ACCEPT} and post-merge-verification comment {P337_VERIFY}, "
        f"both authored by `{BOT}`, were {AUTH.RATIFICATION_REQUIRED_PHRASE} me, the principal."
    )


# --------------------------------------------------------------------------------------
# Isolated truth stand-ins
# --------------------------------------------------------------------------------------


class Git:
    """Local git object store stand-in. Unknown commits simply do not exist."""

    def __init__(self, **overrides):
        self.parents = {
            P337_MERGE: (P337_BASE, P337_HEAD),
            P341_MERGE: (P341_BASE, P341_HEAD),
        }
        self.trees = {
            P337_MERGE: "t337",
            P337_HEAD: "t337",
            P341_MERGE: "t341",
            P341_HEAD: "t341",
        }
        self.__dict__.update(overrides)

    def commit_parents(self, sha):
        return self.parents.get(sha)

    def commit_tree(self, sha):
        return self.trees.get(sha)

    def is_ancestor(self, ancestor, descendant):
        return True

    def blob_sha256_at(self, commit, relpath):
        return None

    def blob_text_at(self, commit, relpath):
        return None

    def head(self):
        return P337_MERGE


class Governance:
    """GitHub governance-metadata stand-in. Unknown ids simply do not exist."""

    def __init__(self, **overrides):
        self.pulls = {
            P337: {
                "base": {"repo": {"full_name": AUTH.REPOSITORY_IDENTITY}},
                "head": {"sha": P337_HEAD},
                "merged": True,
                "merge_commit_sha": P337_MERGE,
                "merged_at": T_MERGE_337,
            },
            P341: {
                "base": {"repo": {"full_name": AUTH.REPOSITORY_IDENTITY}},
                "head": {"sha": P341_HEAD},
                "merged": True,
                "merge_commit_sha": P341_MERGE,
                "merged_at": "2026-08-19T16:49:16Z",
            },
        }
        self.review_records = {
            (P337, P337_REVIEW): {
                "commit_id": P337_HEAD,
                "id": P337_REVIEW,
                "body": APPROVING,
                "user": {"login": PRINCIPAL},
                "state": "COMMENTED",
                "submitted_at": T_REVIEW_337,
                "html_url": f"{_issue_url(P337)}#pullrequestreview-{P337_REVIEW}",
            },
            (P341, P341_REVIEW): {
                "commit_id": P341_HEAD,
                "id": P341_REVIEW,
                "body": APPROVING,
                "user": {"login": PRINCIPAL},
                "state": "COMMENTED",
                "submitted_at": "2026-08-19T16:12:45Z",
                "html_url": f"{_issue_url(P341)}#pullrequestreview-{P341_REVIEW}",
            },
        }
        self.comments = {
            # The two ratified historical records: durably authored by the BOT.
            P337_ACCEPT: {
                "body": f"Acceptance at exact head `{P337_HEAD}` on review {P337_REVIEW}.",
                "issue_url": _issue_url(P337),
                "created_at": T_ACCEPT_337,
                "user": {"login": BOT},
            },
            P337_VERIFY: {
                "body": f"Post-merge verification for merge `{P337_MERGE}`.",
                "issue_url": _issue_url(P337),
                "created_at": T_VERIFY_337,
                "user": {"login": BOT},
            },
            # XASSET-0041's own lifecycle records: durably authored by the PRINCIPAL.
            P341_RATIFY: {
                "body": ratification_body(),
                "issue_url": _issue_url(P341),
                "created_at": T_RATIFY,
                "user": {"login": PRINCIPAL},
            },
            P341_VERIFY: {
                "body": f"Post-merge verification for merge `{P341_MERGE}`.",
                "issue_url": _issue_url(P341),
                "created_at": "2026-08-19T16:50:40Z",
                "user": {"login": PRINCIPAL},
            },
            P341_CLOSURE: {
                "body": f"Closure for merge `{P341_MERGE}`, CI run {P341_RUN}.",
                "issue_url": _issue_url(P341),
                "created_at": "2026-08-19T16:59:15Z",
                "user": {"login": PRINCIPAL},
            },
            # The retracted mis-attribution, present exactly as it is on the real PR.
            VOID_COMMENT_ID: {
                "body": "VOID — this comment is NOT a principal acceptance. " + ratification_body(),
                "issue_url": _issue_url(P341),
                "created_at": "2026-08-19T16:44:49Z",
                "user": {"login": BOT},
            },
        }
        self.runs = {
            P341_RUN: {"status": "completed", "conclusion": "success", "head_sha": P341_MERGE}
        }
        self.jobs = {P341_JOB: {"run_id": P341_RUN, "conclusion": "success"}}
        self.__dict__.update(overrides)

    def pull_request(self, number):
        return self.pulls.get(number)

    def review(self, number, review_id):
        return self.review_records.get((number, str(review_id)))

    def reviews(self, number):
        return [r for (n, _), r in self.review_records.items() if n == number]

    def issue_comment(self, comment_id):
        return self.comments.get(str(comment_id))

    def workflow_run(self, run_id):
        return self.runs.get(str(run_id))

    def workflow_job(self, job_id):
        return self.jobs.get(str(job_id))


def sources(git=None, governance=None) -> AUTH.TruthSources:
    return AUTH.TruthSources(git=git or Git(), governance=governance or Governance())


def document(**overrides) -> dict:
    """The PR #337 lifecycle document, in exactly the shape the validator reads."""
    doc = {
        "authorizing_pull_request": P337,
        "authorization_head": P337_HEAD,
        "lifecycle_evidence": {
            "independent_review": {"review_id": P337_REVIEW, "reviewer_identity": PRINCIPAL},
            "principal_acceptance": {"comment_id": P337_ACCEPT},
            "merge": {"merge_sha": P337_MERGE, "parents": [P337_BASE, P337_HEAD]},
            "post_merge_verification": {"comment_id": P337_VERIFY},
            "merge_commit_ci": {"run_id": "32198881652", "job_id": "95908324747"},
        },
    }
    doc.update(overrides)
    return doc


# --------------------------------------------------------------------------------------
# Error predicates. The mechanism under test is exactly these two messages.
# --------------------------------------------------------------------------------------

ACTOR_MARKER = "was authored by"


def actor_errors(errors) -> list[str]:
    return [e for e in errors if ACTOR_MARKER in e]


def acceptance_actor_error(errors) -> list[str]:
    return [e for e in errors if "acceptance comment" in e and ACTOR_MARKER in e]


def verification_actor_error(errors) -> list[str]:
    return [e for e in errors if "post-merge verification" in e and ACTOR_MARKER in e]


def run(doc=None, git=None, governance=None):
    return AUTH.verify_lifecycle_against_truth(
        doc if doc is not None else document(), sources(git, governance)
    )


# ======================================================================================
# 1. The authentic evidence closes exactly the two historical actor errors
# ======================================================================================


class TestAuthenticEvidenceClosesExactlyTwoGates:
    def test_no_acceptance_actor_error(self):
        assert acceptance_actor_error(run()) == []

    def test_no_post_merge_verification_actor_error(self):
        assert verification_actor_error(run()) == []

    def test_no_actor_error_of_any_kind(self):
        assert actor_errors(run()) == []

    def test_the_pinned_actor_is_still_not_the_principal(self):
        """The exception ratifies acts; it does not promote the actor."""
        assert AUTH.PRINCIPAL_ACCOUNT_LOGIN == "Mast3rkey"
        assert AUTH.LIFECYCLE_OPERATOR_LOGIN == "Mast3rkey"
        assert AUTH.RATIFIED_HISTORICAL_ACTOR != AUTH.PRINCIPAL_ACCOUNT_LOGIN
        assert AUTH.RATIFIED_HISTORICAL_ACTOR != AUTH.LIFECYCLE_OPERATOR_LOGIN


# ======================================================================================
# 2. Ordinary lifecycles are untouched — the default path is exactly as it was
# ======================================================================================


class TestOrdinaryPathUnchanged:
    def test_ordinary_principal_authored_records_pass(self):
        """A Mast3rkey-authored PR #337 lifecycle needs no exception at all."""
        gov = Governance()
        gov.comments[P337_ACCEPT] = {**gov.comments[P337_ACCEPT], "user": {"login": PRINCIPAL}}
        gov.comments[P337_VERIFY] = {**gov.comments[P337_VERIFY], "user": {"login": PRINCIPAL}}
        assert actor_errors(run(governance=gov)) == []

    def test_bot_authored_records_on_another_pull_request_still_fail(self):
        """The whole point: nothing generalizes to a different pull request."""
        other = 999
        gov = Governance()
        gov.pulls[other] = {
            "base": {"repo": {"full_name": AUTH.REPOSITORY_IDENTITY}},
            "head": {"sha": "c" * 40},
            "merged": True,
            "merge_commit_sha": "d" * 40,
            "merged_at": T_MERGE_337,
        }
        gov.review_records[(other, "4900000009")] = {
            "commit_id": "c" * 40,
            "body": APPROVING,
            "user": {"login": PRINCIPAL},
            "state": "COMMENTED",
            "submitted_at": T_REVIEW_337,
            "html_url": f"{_issue_url(other)}#pullrequestreview-4900000009",
        }
        gov.comments["5900000009"] = {
            "body": f"Acceptance at `{'c' * 40}` on review 4900000009.",
            "issue_url": _issue_url(other),
            "created_at": T_ACCEPT_337,
            "user": {"login": BOT},
        }
        gov.comments["5900000010"] = {
            "body": f"Post-merge verification for `{'d' * 40}`.",
            "issue_url": _issue_url(other),
            "created_at": T_VERIFY_337,
            "user": {"login": BOT},
        }
        doc = document(
            authorizing_pull_request=other,
            authorization_head="c" * 40,
            lifecycle_evidence={
                "independent_review": {"review_id": "4900000009"},
                "principal_acceptance": {"comment_id": "5900000009"},
                "merge": {"merge_sha": "d" * 40, "parents": []},
                "post_merge_verification": {"comment_id": "5900000010"},
                "merge_commit_ci": {"run_id": "1", "job_id": "1"},
            },
        )
        errors = run(doc=doc, governance=gov)
        assert len(acceptance_actor_error(errors)) == 1
        assert len(verification_actor_error(errors)) == 1

    def test_a_third_actor_is_never_ratified(self):
        """Only the exact pinned historical actor. Any other login fails closed."""
        gov = Governance()
        gov.comments[P337_ACCEPT] = {
            **gov.comments[P337_ACCEPT],
            "user": {"login": "some-other-account"},
        }
        assert len(acceptance_actor_error(run(governance=gov))) == 1

    @pytest.mark.parametrize("lookalike", ["Claude[bot]", "claude[bot] ", "claude-bot", "claude"])
    def test_actor_lookalikes_are_not_the_pinned_actor(self, lookalike):
        gov = Governance()
        gov.comments[P337_ACCEPT] = {**gov.comments[P337_ACCEPT], "user": {"login": lookalike}}
        assert len(acceptance_actor_error(run(governance=gov))) == 1

    def test_a_record_with_no_durable_author_is_still_refused(self):
        gov = Governance()
        gov.comments[P337_ACCEPT] = {
            k: v for k, v in gov.comments[P337_ACCEPT].items() if k != "user"
        }
        errors = run(governance=gov)
        assert any("carries no durable author identity" in e for e in errors)


# ======================================================================================
# 3. Each of the five PR #337 identities is independently mandatory
# ======================================================================================


class TestEachRatifiedIdentityIsMandatory:
    def test_wrong_head_relocks_both_gates(self):
        doc = document(authorization_head="9" * 40)
        assert len(actor_errors(run(doc=doc))) == 2

    def test_wrong_review_id_relocks_both_gates(self):
        doc = document()
        doc["lifecycle_evidence"]["independent_review"]["review_id"] = "4900000000"
        assert len(actor_errors(run(doc=doc))) == 2

    def test_wrong_merge_sha_relocks_both_gates(self):
        doc = document()
        doc["lifecycle_evidence"]["merge"]["merge_sha"] = "9" * 40
        assert len(actor_errors(run(doc=doc))) == 2

    def test_wrong_acceptance_comment_id_relocks_both_gates(self):
        gov = Governance()
        gov.comments["5900000099"] = dict(gov.comments[P337_ACCEPT])
        doc = document()
        doc["lifecycle_evidence"]["principal_acceptance"]["comment_id"] = "5900000099"
        assert len(actor_errors(run(doc=doc, governance=gov))) == 2

    def test_wrong_verification_comment_id_relocks_both_gates(self):
        gov = Governance()
        gov.comments["5900000098"] = dict(gov.comments[P337_VERIFY])
        doc = document()
        doc["lifecycle_evidence"]["post_merge_verification"]["comment_id"] = "5900000098"
        assert len(actor_errors(run(doc=doc, governance=gov))) == 2

    def test_wrong_pull_request_number_relocks_both_gates(self):
        gov = Governance()
        gov.pulls[338] = dict(gov.pulls[P337])
        gov.review_records[(338, P337_REVIEW)] = gov.review_records[(P337, P337_REVIEW)]
        doc = document(authorizing_pull_request=338)
        assert len(actor_errors(run(doc=doc, governance=gov))) == 2

    def test_live_head_disagreeing_with_the_pin_relocks(self):
        gov = Governance()
        gov.pulls[P337] = {**gov.pulls[P337], "head": {"sha": "9" * 40}}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_live_merge_disagreeing_with_the_pin_relocks(self):
        gov = Governance()
        gov.pulls[P337] = {**gov.pulls[P337], "merge_commit_sha": "9" * 40}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_unmerged_pull_request_relocks(self):
        gov = Governance()
        gov.pulls[P337] = {**gov.pulls[P337], "merged": False}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_foreign_repository_relocks(self):
        gov = Governance()
        gov.pulls[P337] = {
            **gov.pulls[P337],
            "base": {"repo": {"full_name": "someone-else/Portfolio-HQ"}},
        }
        assert len(actor_errors(run(governance=gov))) == 2


# ======================================================================================
# 4. Each XASSET-0041 lifecycle identity is independently mandatory
# ======================================================================================


class TestEachRatificationLifecycleIdentityIsMandatory:
    def test_missing_ratification_pull_request(self):
        gov = Governance()
        del gov.pulls[P341]
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_pull_request_not_merged(self):
        gov = Governance()
        gov.pulls[P341] = {**gov.pulls[P341], "merged": False}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_pull_request_wrong_head(self):
        gov = Governance()
        gov.pulls[P341] = {**gov.pulls[P341], "head": {"sha": "9" * 40}}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_pull_request_wrong_merge(self):
        gov = Governance()
        gov.pulls[P341] = {**gov.pulls[P341], "merge_commit_sha": "9" * 40}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_pull_request_foreign_repository(self):
        gov = Governance()
        gov.pulls[P341] = {
            **gov.pulls[P341],
            "base": {"repo": {"full_name": "someone-else/Portfolio-HQ"}},
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_missing_ratification_review(self):
        gov = Governance()
        del gov.review_records[(P341, P341_REVIEW)]
        assert len(actor_errors(run(governance=gov))) == 2

    @pytest.mark.parametrize("nonmapping", ["a review", ["a", "review"], 17, True])
    def test_a_present_but_non_mapping_ratification_review_is_refused_without_raising(
        self, nonmapping
    ):
        """Independently covers the shape guard: a non-mapping record must fail closed,
        not raise, and must never be treated as a review."""
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = nonmapping
        assert len(actor_errors(run(governance=gov))) == 2

    def test_a_fully_valid_review_at_the_wrong_id_does_not_substitute(self):
        """The pinned review id is what is required -- not merely 'some approving review'."""
        gov = Governance()
        valid = gov.review_records.pop((P341, P341_REVIEW))
        gov.review_records[(P341, "4900000777")] = valid
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_review_on_the_wrong_head(self):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)],
            "commit_id": "9" * 40,
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_dismissed_ratification_review(self):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)],
            "state": "DISMISSED",
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_adverse_ratification_review(self):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)],
            "body": "FORMAL DISPOSITION: CHANGES REQUIRED — 1 BLOCKING",
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_review_with_no_formal_disposition(self):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)],
            "body": "Looks fine to me.",
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_review_belonging_to_another_pull_request(self):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)],
            "html_url": f"{_issue_url(999)}#pullrequestreview-{P341_REVIEW}",
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_missing_ratification_comment(self):
        gov = Governance()
        del gov.comments[P341_RATIFY]
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_comment_belonging_to_another_pull_request(self):
        gov = Governance()
        gov.comments[P341_RATIFY] = {
            **gov.comments[P341_RATIFY],
            "issue_url": _issue_url(999),
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_missing_ratification_post_merge_verification(self):
        gov = Governance()
        del gov.comments[P341_VERIFY]
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_post_merge_verification_wrong_actor(self):
        gov = Governance()
        gov.comments[P341_VERIFY] = {**gov.comments[P341_VERIFY], "user": {"login": BOT}}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_post_merge_verification_not_naming_the_merge(self):
        gov = Governance()
        gov.comments[P341_VERIFY] = {**gov.comments[P341_VERIFY], "body": "Verified."}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_missing_final_closure(self):
        gov = Governance()
        del gov.comments[P341_CLOSURE]
        assert len(actor_errors(run(governance=gov))) == 2

    def test_final_closure_wrong_actor(self):
        gov = Governance()
        gov.comments[P341_CLOSURE] = {**gov.comments[P341_CLOSURE], "user": {"login": BOT}}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_final_closure_not_naming_the_merge_commit_ci_run(self):
        gov = Governance()
        gov.comments[P341_CLOSURE] = {
            **gov.comments[P341_CLOSURE],
            "body": f"Closure for merge `{P341_MERGE}`.",
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_missing_merge_commit_ci_run(self):
        gov = Governance()
        del gov.runs[P341_RUN]
        assert len(actor_errors(run(governance=gov))) == 2

    def test_unsuccessful_merge_commit_ci_run(self):
        gov = Governance()
        gov.runs[P341_RUN] = {**gov.runs[P341_RUN], "conclusion": "failure"}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_incomplete_merge_commit_ci_run(self):
        gov = Governance()
        gov.runs[P341_RUN] = {**gov.runs[P341_RUN], "status": "in_progress"}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_merge_commit_ci_run_against_the_wrong_sha(self):
        """A green PR-head run is not a merge-commit run."""
        gov = Governance()
        gov.runs[P341_RUN] = {**gov.runs[P341_RUN], "head_sha": P341_HEAD}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_missing_merge_commit_ci_job(self):
        gov = Governance()
        del gov.jobs[P341_JOB]
        assert len(actor_errors(run(governance=gov))) == 2

    def test_merge_commit_ci_job_from_another_run(self):
        gov = Governance()
        gov.jobs[P341_JOB] = {**gov.jobs[P341_JOB], "run_id": "99999999"}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_unsuccessful_merge_commit_ci_job(self):
        gov = Governance()
        gov.jobs[P341_JOB] = {**gov.jobs[P341_JOB], "conclusion": "failure"}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_missing_ratification_merge_in_git(self):
        git = Git()
        del git.parents[P341_MERGE]
        assert len(actor_errors(run(git=git))) == 2

    def test_ratification_merge_with_one_parent(self):
        git = Git()
        git.parents[P341_MERGE] = (P341_BASE,)
        assert len(actor_errors(run(git=git))) == 2

    def test_ratification_merge_with_the_wrong_base_parent(self):
        git = Git()
        git.parents[P341_MERGE] = ("9" * 40, P341_HEAD)
        assert len(actor_errors(run(git=git))) == 2

    def test_ratification_merge_with_the_wrong_head_parent(self):
        git = Git()
        git.parents[P341_MERGE] = (P341_BASE, "9" * 40)
        assert len(actor_errors(run(git=git))) == 2

    def test_ratification_merge_drift(self):
        git = Git()
        git.trees[P341_MERGE] = "drifted"
        assert len(actor_errors(run(git=git))) == 2

    def test_unresolvable_ratification_trees(self):
        git = Git()
        del git.trees[P341_HEAD]
        assert len(actor_errors(run(git=git))) == 2


# ======================================================================================
# 5. The ratification record's own content requirements
# ======================================================================================


class TestRatificationContentIsMandatory:
    @pytest.mark.parametrize(
        "token",
        [
            P341_HEAD,
            P341_REVIEW,
            P337_HEAD,
            P337_REVIEW,
            P337_ACCEPT,
            P337_MERGE,
            P337_VERIFY,
            BOT,
            AUTH.RATIFICATION_REQUIRED_PHRASE,
        ],
    )
    def test_every_required_token_is_independently_mandatory(self, token):
        gov = Governance()
        gov.comments[P341_RATIFY] = {
            **gov.comments[P341_RATIFY],
            "body": ratification_body().replace(token, "REDACTED"),
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_an_empty_ratification_body_unlocks_nothing(self):
        gov = Governance()
        gov.comments[P341_RATIFY] = {**gov.comments[P341_RATIFY], "body": ""}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_a_non_string_ratification_body_unlocks_nothing(self):
        gov = Governance()
        gov.comments[P341_RATIFY] = {**gov.comments[P341_RATIFY], "body": None}
        assert len(actor_errors(run(governance=gov))) == 2


# ======================================================================================
# 6. The retracted comment 5345204885 is refused, on two independent grounds
# ======================================================================================


class TestVoidCommentIsRefused:
    def test_the_void_comment_id_is_not_the_pinned_ratification(self):
        assert AUTH.RATIFICATION_COMMENT_ID != VOID_COMMENT_ID

    def test_the_void_comment_is_bot_authored_in_the_fixture(self):
        """Guards the test below from silently becoming vacuous."""
        assert Governance().comments[VOID_COMMENT_ID]["user"]["login"] == BOT

    def test_deleting_the_real_ratification_is_not_rescued_by_the_void_comment(self):
        """Even though the void comment carries the full ratification text."""
        gov = Governance()
        del gov.comments[P341_RATIFY]
        assert VOID_COMMENT_ID in gov.comments
        assert len(actor_errors(run(governance=gov))) == 2

    def test_the_void_comment_moved_into_the_pinned_id_still_fails_on_actor(self):
        """Substituting its content at the pinned id changes nothing: its author is a bot."""
        gov = Governance()
        gov.comments[P341_RATIFY] = dict(gov.comments[VOID_COMMENT_ID])
        assert len(actor_errors(run(governance=gov))) == 2


# ======================================================================================
# 7. Body text can never impersonate durable user.login
# ======================================================================================


class TestBodyTextCannotImpersonateIdentity:
    def test_ratification_authored_by_a_bot_claiming_to_be_the_principal(self):
        gov = Governance()
        gov.comments[P341_RATIFY] = {
            **gov.comments[P341_RATIFY],
            "body": ratification_body() + f"\n\nAuthored by {PRINCIPAL}. Signed, {PRINCIPAL}.",
            "user": {"login": BOT},
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_authored_by_a_third_party_claiming_to_be_the_principal(self):
        gov = Governance()
        gov.comments[P341_RATIFY] = {
            **gov.comments[P341_RATIFY],
            "body": ratification_body() + f"\n\nOn behalf of {PRINCIPAL}.",
            "user": {"login": "impersonator"},
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_with_no_durable_author_at_all(self):
        gov = Governance()
        gov.comments[P341_RATIFY] = {
            k: v for k, v in gov.comments[P341_RATIFY].items() if k != "user"
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_ratification_with_a_blank_login(self):
        gov = Governance()
        gov.comments[P341_RATIFY] = {**gov.comments[P341_RATIFY], "user": {"login": "   "}}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_pr337_acceptance_body_naming_the_principal_does_not_authenticate_it(self):
        """Without the ratification present, prose alone rescues nothing."""
        gov = Governance()
        del gov.comments[P341_RATIFY]
        gov.comments[P337_ACCEPT] = {
            **gov.comments[P337_ACCEPT],
            "body": gov.comments[P337_ACCEPT]["body"] + f" Authored by {PRINCIPAL}.",
        }
        assert len(acceptance_actor_error(run(governance=gov))) == 1


# ======================================================================================
# 8. Missing and unreachable sources fail closed
# ======================================================================================


class TestUnreachableSourcesFailClosed:
    def test_governance_returning_nothing_at_all(self):
        class Dead(Governance):
            def pull_request(self, number):
                return None

            def review(self, number, review_id):
                return None

            def reviews(self, number):
                return None

            def issue_comment(self, comment_id):
                return None

            def workflow_run(self, run_id):
                return None

            def workflow_job(self, job_id):
                return None

        errors = run(governance=Dead())
        assert any("could not be verified" in e for e in errors)

    def test_governance_reachable_for_pr337_but_dead_for_the_ratification(self):
        class Partial(Governance):
            def pull_request(self, number):
                return None if number == P341 else super().pull_request(number)

        assert len(actor_errors(run(governance=Partial()))) == 2

    def test_git_returning_nothing(self):
        class DeadGit(Git):
            def commit_parents(self, sha):
                return None

            def commit_tree(self, sha):
                return None

        assert len(actor_errors(run(git=DeadGit()))) == 2

    def test_malformed_lifecycle_evidence_block(self):
        doc = document(lifecycle_evidence="not a mapping")
        errors = AUTH.verify_lifecycle_against_truth(doc, sources())
        assert errors == ("lifecycle_evidence: expected a mapping",)

    @pytest.mark.parametrize("malformed", [{}, [], "", None])
    def test_malformed_sub_blocks_do_not_unlock(self, malformed):
        """A malformed acceptance block cannot satisfy the pin, so the exception stays locked."""
        doc = document()
        doc["lifecycle_evidence"]["principal_acceptance"] = malformed
        errors = run(doc=doc)
        # The acceptance id is now empty, so it fails earlier, on existence.
        assert any("principal acceptance comment" in e and "does not exist" in e for e in errors)
        # The verification gate proves the exception did not unlock: its actor error returns.
        assert len(verification_actor_error(errors)) == 1

    @pytest.mark.parametrize(
        "malformed", ["not a mapping", ["not", "a", "mapping"], 17, {"comment_id": {}}]
    )
    def test_the_correction_itself_survives_truthy_non_mapping_sub_blocks(self, malformed):
        """DISCLOSED: Gate 2's own pre-existing ``(x or {}).get(...)`` raises on a TRUTHY
        non-mapping sub-block. That fragility predates this correction, lives outside the two
        lines it touches, and is deliberately NOT repaired here -- repairing unrelated
        production behaviour is outside XASSET-0041's authorized scope. What IS in scope is
        that the correction adds no such fragility of its own, which is what this asserts.
        """
        doc = document()
        doc["lifecycle_evidence"]["principal_acceptance"] = malformed
        ratification = AUTH._derive_pr337_actor_ratification(
            doc, sources(), Governance().pull_request(P337)
        )
        assert ratification.acceptance is False
        assert ratification.post_merge_verification is False

    def test_missing_sub_blocks_do_not_unlock(self):
        doc = document()
        del doc["lifecycle_evidence"]["merge"]
        assert len(actor_errors(run(doc=doc))) == 2


# ======================================================================================
# 9. Retrospective, never a fictional pre-merge acceptance
# ======================================================================================


class TestRetrospectiveNotRetroactive:
    def test_a_ratification_predating_the_ratified_merge_is_refused(self):
        gov = Governance()
        gov.comments[P341_RATIFY] = {
            **gov.comments[P341_RATIFY],
            "created_at": "2026-08-18T00:00:00Z",
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_a_ratification_with_no_timestamp_is_refused(self):
        gov = Governance()
        gov.comments[P341_RATIFY] = {
            k: v for k, v in gov.comments[P341_RATIFY].items() if k != "created_at"
        }
        assert len(actor_errors(run(governance=gov))) == 2

    def test_the_ratification_really_does_postdate_the_merge_in_the_fixture(self):
        """Guards the two tests above from becoming vacuous."""
        gov = Governance()
        assert gov.comments[P341_RATIFY]["created_at"] > gov.pulls[P337]["merged_at"]

    def test_backfilling_a_principal_acceptance_after_the_merge_still_fails_chronology(self):
        """The ordinary chronology rule is untouched: no fictional pre-merge acceptance."""
        gov = Governance()
        gov.comments[P337_ACCEPT] = {
            **gov.comments[P337_ACCEPT],
            "user": {"login": PRINCIPAL},
            "created_at": "2026-08-19T15:03:07Z",  # after the merge
        }
        errors = run(governance=gov)
        assert any("precedes acceptance" in e for e in errors)

    def test_the_exception_does_not_suppress_that_chronology_error(self):
        """Even with the full ratification present, a backfilled acceptance is still refused."""
        gov = Governance()
        gov.comments[P337_ACCEPT] = {
            **gov.comments[P337_ACCEPT],
            "created_at": "2026-08-19T15:03:07Z",
        }
        errors = run(governance=gov)
        assert any("precedes acceptance" in e for e in errors)


# ======================================================================================
# 10. Everything else the ordinary gates check still runs for PR #337
# ======================================================================================


class TestOrdinaryChecksStillRunUnderTheException:
    def test_acceptance_must_still_name_the_exact_head(self):
        gov = Governance()
        gov.comments[P337_ACCEPT] = {
            **gov.comments[P337_ACCEPT],
            "body": f"Acceptance on review {P337_REVIEW}.",
        }
        errors = run(governance=gov)
        assert any("does not name the exact head" in e for e in errors)

    def test_acceptance_must_still_certify_the_review(self):
        gov = Governance()
        gov.comments[P337_ACCEPT] = {
            **gov.comments[P337_ACCEPT],
            "body": f"Acceptance at exact head `{P337_HEAD}`.",
        }
        errors = run(governance=gov)
        assert any("does not certify the independent review" in e for e in errors)

    def test_acceptance_must_still_belong_to_the_pull_request(self):
        gov = Governance()
        gov.comments[P337_ACCEPT] = {
            **gov.comments[P337_ACCEPT],
            "issue_url": _issue_url(999),
        }
        errors = run(governance=gov)
        assert any(
            "acceptance comment" in e and "does not belong to pull request" in e for e in errors
        )

    def test_post_merge_verification_must_still_name_the_merge(self):
        gov = Governance()
        gov.comments[P337_VERIFY] = {**gov.comments[P337_VERIFY], "body": "Verified."}
        errors = run(governance=gov)
        assert any("does not name the merge SHA" in e for e in errors)

    def test_post_merge_verification_must_still_postdate_the_merge(self):
        gov = Governance()
        gov.comments[P337_VERIFY] = {
            **gov.comments[P337_VERIFY],
            "created_at": "2026-08-01T00:00:00Z",
        }
        errors = run(governance=gov)
        assert any("precedes the merge" in e for e in errors)

    def test_a_missing_acceptance_comment_is_still_refused(self):
        gov = Governance()
        del gov.comments[P337_ACCEPT]
        errors = run(governance=gov)
        assert any("principal acceptance comment" in e and "does not exist" in e for e in errors)

    def test_a_missing_verification_comment_is_still_refused(self):
        gov = Governance()
        del gov.comments[P337_VERIFY]
        errors = run(governance=gov)
        assert any(
            "post-merge verification comment" in e and "does not exist" in e for e in errors
        )


# ======================================================================================
# 11. The exception is structurally bounded to exactly two gates
# ======================================================================================


class TestExceptionScopeIsStructurallyBounded:
    def test_it_ratifies_exactly_two_gates_and_no_third(self):
        fields = set(AUTH._Pr337ActorRatification.__dataclass_fields__)
        assert fields == {"acceptance", "post_merge_verification"}

    def test_the_default_instance_ratifies_nothing(self):
        default = AUTH._Pr337ActorRatification()
        assert default.acceptance is False
        assert default.post_merge_verification is False
        assert default.ratifies_acceptance(P337_ACCEPT, BOT) is False
        assert default.ratifies_post_merge_verification(P337_VERIFY, BOT) is False

    def test_a_ratified_instance_still_re_checks_the_record_identity(self):
        granted = AUTH._Pr337ActorRatification(acceptance=True, post_merge_verification=True)
        assert granted.ratifies_acceptance(P337_ACCEPT, BOT) is True
        assert granted.ratifies_acceptance("5900000000", BOT) is False
        assert granted.ratifies_acceptance(P337_ACCEPT, PRINCIPAL) is False
        assert granted.ratifies_post_merge_verification(P337_VERIFY, BOT) is True
        assert granted.ratifies_post_merge_verification("5900000000", BOT) is False
        assert granted.ratifies_post_merge_verification(P337_VERIFY, "other") is False

    def test_acceptance_and_verification_ids_are_not_interchangeable(self):
        granted = AUTH._Pr337ActorRatification(acceptance=True, post_merge_verification=True)
        assert granted.ratifies_acceptance(P337_VERIFY, BOT) is False
        assert granted.ratifies_post_merge_verification(P337_ACCEPT, BOT) is False

    def test_the_module_defines_no_accepted_actor_container_holding_the_bot(self):
        """No allow-list, no bot class, no 'trusted automation' category."""
        for name in dir(AUTH):
            if name.startswith("__"):
                continue
            value = getattr(AUTH, name)
            if isinstance(value, (list, tuple, set, frozenset)) and BOT in value:
                pytest.fail(f"{name} contains {BOT!r}; the correction must not build an allow-list")

    def test_the_bot_login_appears_only_as_the_pinned_historical_actor(self):
        matches = [
            name
            for name in dir(AUTH)
            if not name.startswith("__") and getattr(AUTH, name, None) == BOT
        ]
        assert matches == ["RATIFIED_HISTORICAL_ACTOR"]


# ======================================================================================
# 12. No filesystem, lane, or outcome-producing side effect
# ======================================================================================


class TestNoSideEffects:
    def test_validation_never_writes_authorization_claim_or_completion(self, monkeypatch):
        for name in (
            "write_authorization",
            "claim_execution",
            "record_completion",
        ):
            if hasattr(AUTH, name):
                monkeypatch.setattr(
                    AUTH,
                    name,
                    lambda *a, **k: pytest.fail(f"{name} was called during validation"),
                )
        run()

    def test_lane_paths_remain_absent(self):
        run()
        for path in (
            AUTH.AUTHORIZATION_ROOT,
            AUTH.AUTHORIZATION_PATH,
            AUTH.CLAIM_PATH,
            AUTH.COMPLETION_PATH,
            AUTH.LEDGER_PATH,
        ):
            assert not path.exists(), f"{path} must not exist"

    def test_new_execution_is_still_not_authorized(self):
        run()
        authorized, _ = AUTH.new_execution_is_authorized()
        assert authorized is False

    def test_no_stage1_results_artifact_is_created(self):
        run()
        assert not (REPO_ROOT / "stage1_results.yaml").exists()

    def test_the_attempt_id_is_unchanged(self):
        assert AUTH.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

    def test_the_binding_constants_are_untouched_by_this_correction(self):
        """The correction corrects; it does not rebind. Rebinding is a separate unit."""
        assert AUTH.AUTHORIZING_DECISION == "XASSET-0037"
        assert AUTH.AUTHORIZING_PULL_REQUEST == 337
        assert len(AUTH.LOAD_BEARING_RELPATHS) == 10
        assert AUTH.LOAD_BEARING_RELPATHS[0] == "level1_stage1_execution_authorization.py"


# ======================================================================================
# 13. Suite hygiene — these guards caught real defects during development
# ======================================================================================


class TestSuiteHygiene:
    def _tree(self):
        return ast.parse(Path(__file__).read_text(encoding="utf-8"))

    def test_this_suite_imports_no_outcome_producing_module(self):
        forbidden = {
            "level1_stage1_runner",
            "level1_stage1_result_validator",
            "level1_construction_universe_closure_validator",
        }
        for node in ast.walk(self._tree()):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] not in forbidden
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert node.module.split(".")[0] not in forbidden

    def test_this_suite_opens_no_file_for_writing(self):
        for node in ast.walk(self._tree()):
            if isinstance(node, ast.Call):
                name = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
                assert name not in {"write_text", "write_bytes", "mkdir", "unlink", "touch"}

    def test_this_suite_references_no_protected_risk_results_path(self):
        # Built by concatenation so the guard's own source does not contain the token it bans.
        forbidden = "risk_lane" + "_boundary"
        text = Path(__file__).read_text(encoding="utf-8")
        assert text.count(forbidden) == 0

    def test_no_or_fallback_assertions(self):
        """An ``assert x or True``-shaped assertion proves nothing and must not exist."""
        offenders = []
        for node in ast.walk(self._tree()):
            if isinstance(node, ast.Assert) and isinstance(node.test, ast.BoolOp):
                if isinstance(node.test.op, ast.Or):
                    offenders.append(node.lineno)
        assert offenders == [], f"or-fallback assertions at lines {offenders}"

    def test_the_module_section_is_documented_as_bounded(self):
        source = (REPO_ROOT / "level1_stage1_execution_authorization.py").read_text(
            encoding="utf-8"
        )
        assert "XASSET-0042" in source
        assert "It is NOT an accepted-actor list" in source
        assert "It is NOT identity inference from comment text" in source
        assert "It is NOT a fictional pre-merge acceptance" in source
