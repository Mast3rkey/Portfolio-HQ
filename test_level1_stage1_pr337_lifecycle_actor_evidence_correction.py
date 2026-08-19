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
import contextlib
import copy
import hashlib
import json
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
T_MERGE_341 = "2026-08-19T16:49:16Z"
T_VERIFY_341 = "2026-08-19T16:50:40Z"
T_CI_COMPLETED = "2026-08-19T16:57:31Z"
T_CLOSURE_341 = "2026-08-19T16:59:15Z"
T_REVIEW_341 = "2026-08-19T16:12:45Z"

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
                "merged_at": T_MERGE_341,
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
                "submitted_at": T_REVIEW_341,
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
                "id": P341_RATIFY,
                "body": ratification_body(),
                "issue_url": _issue_url(P341),
                "created_at": T_RATIFY,
                "user": {"login": PRINCIPAL},
            },
            P341_VERIFY: {
                "id": P341_VERIFY,
                "body": f"Post-merge verification for merge `{P341_MERGE}`.",
                "issue_url": _issue_url(P341),
                "created_at": T_VERIFY_341,
                "user": {"login": PRINCIPAL},
            },
            P341_CLOSURE: {
                "id": P341_CLOSURE,
                "body": f"Closure for merge `{P341_MERGE}`, CI run {P341_RUN}.",
                "issue_url": _issue_url(P341),
                "created_at": T_CLOSURE_341,
                "user": {"login": PRINCIPAL},
            },
            # The retracted mis-attribution, present exactly as it is on the real PR.
            VOID_COMMENT_ID: {
                "id": VOID_COMMENT_ID,
                "body": "VOID — this comment is NOT a principal acceptance. " + ratification_body(),
                "issue_url": _issue_url(P341),
                "created_at": "2026-08-19T16:44:49Z",
                "user": {"login": BOT},
            },
        }
        self.runs = {
            P341_RUN: {"status": "completed", "conclusion": "success", "head_sha": P341_MERGE}
        }
        self.jobs = {
            P341_JOB: {
                "run_id": P341_RUN,
                "conclusion": "success",
                "completed_at": T_CI_COMPLETED,
            }
        }
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


# --------------------------------------------------------------------------------------
# Fingerprint pins for the ISOLATED fixture universe
# --------------------------------------------------------------------------------------
#
# The production constants pin the REAL merged PR #341 records, whose bodies this suite
# cannot reproduce -- that is the whole point of a body digest. So the fixture universe
# carries its own accepted records, and their fingerprints are derived ONCE from the
# BASELINE (unmutated) fixture below and swapped in for the duration of a call.
#
# Two things keep this honest:
#   * the baseline is computed before any test mutates anything, so ANY alteration a test
#     makes -- a negated body, a changed actor, a moved timestamp -- yields a different
#     fingerprint and must relock;
#   * the REAL production pins are asserted separately and UNPATCHED, against an
#     independent copy of the expected digests, in ``TestFingerprintPinsAreTheRealRecords``.
#     A mutation to any production constant is therefore still caught.

_BASELINE_GOV = Governance()

FIXTURE_FINGERPRINTS = {
    "RATIFICATION_REVIEW_FINGERPRINT": AUTH._review_record_fingerprint(
        _BASELINE_GOV.review_records[(P341, P341_REVIEW)]
    ),
    "RATIFICATION_COMMENT_FINGERPRINT": AUTH._comment_record_fingerprint(
        _BASELINE_GOV.comments[P341_RATIFY]
    ),
    "RATIFICATION_VERIFICATION_FINGERPRINT": AUTH._comment_record_fingerprint(
        _BASELINE_GOV.comments[P341_VERIFY]
    ),
    "RATIFICATION_CLOSURE_FINGERPRINT": AUTH._comment_record_fingerprint(
        _BASELINE_GOV.comments[P341_CLOSURE]
    ),
}


@contextlib.contextmanager
def fixture_pins():
    """Swap the four production fingerprint pins for the fixture universe's own."""
    originals = {name: getattr(AUTH, name) for name in FIXTURE_FINGERPRINTS}
    try:
        for name, digest in FIXTURE_FINGERPRINTS.items():
            setattr(AUTH, name, digest)
        yield
    finally:
        for name, value in originals.items():
            setattr(AUTH, name, value)


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
    """Validate against the BASELINE fixture pins.

    Any alteration a test makes to a fingerprinted record relocks here -- which is exactly
    what MAJOR 1 requires, and what these tests assert.
    """
    with fixture_pins():
        return AUTH.verify_lifecycle_against_truth(
            doc if doc is not None else document(), sources(git, governance)
        )


def run_repinned(doc=None, git=None, governance=None):
    """Validate with the fingerprints RECOMPUTED from the (possibly mutated) fixture.

    This deliberately removes the fingerprint gate from the picture so a chronology or
    finality test proves its OWN mechanism rather than piggy-backing on MAJOR 1's digest.
    A test that relocks under this helper relocks because the ORDER is wrong, full stop.
    """
    gov = governance or Governance()
    pins = {
        "RATIFICATION_REVIEW_FINGERPRINT": AUTH._review_record_fingerprint(
            gov.review_records.get((P341, P341_REVIEW)) or {}
        ),
        "RATIFICATION_COMMENT_FINGERPRINT": AUTH._comment_record_fingerprint(
            gov.comments.get(P341_RATIFY) or {}
        ),
        "RATIFICATION_VERIFICATION_FINGERPRINT": AUTH._comment_record_fingerprint(
            gov.comments.get(P341_VERIFY) or {}
        ),
        "RATIFICATION_CLOSURE_FINGERPRINT": AUTH._comment_record_fingerprint(
            gov.comments.get(P341_CLOSURE) or {}
        ),
    }
    originals = {name: getattr(AUTH, name) for name in pins}
    try:
        for name, digest in pins.items():
            setattr(AUTH, name, digest)
        return AUTH.verify_lifecycle_against_truth(
            doc if doc is not None else document(), sources(git, gov)
        )
    finally:
        for name, value in originals.items():
            setattr(AUTH, name, value)


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


# ======================================================================================
# 14. MAJOR 1 (review 4975556072) — an ALTERED record never authenticates,
#     however faithfully it still quotes the identities
# ======================================================================================


class TestAlteredRecordsAreRefusedEvenWithEveryTokenRetained:
    """Reproduced before the fix: each of these produced ZERO actor errors.

    The failure was that token presence proves names are PRESENT, not that the record
    affirmatively ratifies, verifies, or closes anything. PR #341 comment 5345204885 is a
    live instance of the shape -- retracted by editing its body into a VOID notice while
    retaining its historical text.
    """

    def test_ratification_voided_in_place_while_retaining_every_token(self):
        gov = Governance()
        gov.comments[P341_RATIFY] = {
            **gov.comments[P341_RATIFY],
            "body": (
                "## VOID. I do NOT ratify anything.\n\n"
                "It is FALSE that those comments were authorized acts performed for the "
                "principal. This notice RETRACTS the ratification in full.\n\n"
                "Historical text retained for audit only:\n" + ratification_body()
            ),
        }
        # Every required token is still present -- the old mechanism's entire test.
        assert AUTH._names_all(
            gov.comments[P341_RATIFY]["body"],
            (
                P341_HEAD, P341_REVIEW, P337_HEAD, P337_REVIEW, P337_ACCEPT,
                P337_MERGE, P337_VERIFY, BOT, AUTH.RATIFICATION_REQUIRED_PHRASE,
            ),
        )
        assert len(actor_errors(run(governance=gov))) == 2

    def test_post_merge_verification_negated_while_retaining_the_merge_sha(self):
        gov = Governance()
        gov.comments[P341_VERIFY] = {
            **gov.comments[P341_VERIFY],
            "body": f"VOID; this does NOT verify merge `{P341_MERGE}`. No verification occurred.",
        }
        assert AUTH._names_all(gov.comments[P341_VERIFY]["body"], (P341_MERGE,))
        assert len(actor_errors(run(governance=gov))) == 2

    def test_closure_negated_while_retaining_the_merge_and_ci_ids(self):
        gov = Governance()
        gov.comments[P341_CLOSURE] = {
            **gov.comments[P341_CLOSURE],
            "body": f"VOID; NO closure for `{P341_MERGE}`; CI {P341_RUN} referenced only.",
        }
        assert AUTH._names_all(gov.comments[P341_CLOSURE]["body"], (P341_MERGE, P341_RUN))
        assert len(actor_errors(run(governance=gov))) == 2

    @pytest.mark.parametrize("record_id", ["ratify", "verify", "closure"])
    def test_a_single_appended_character_relocks(self, record_id):
        gov = Governance()
        key = {"ratify": P341_RATIFY, "verify": P341_VERIFY, "closure": P341_CLOSURE}[record_id]
        gov.comments[key] = {**gov.comments[key], "body": gov.comments[key]["body"] + "."}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_review_body_altered_while_keeping_the_approving_line(self):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)],
            "body": APPROVING + "\n\nRETRACTED: this review is withdrawn.",
        }
        # Still parses as approving, so the disposition check alone cannot catch it.
        assert AUTH.parse_formal_disposition(
            gov.review_records[(P341, P341_REVIEW)]["body"]
        ) == AUTH.APPROVING_REVIEW_DISPOSITION
        assert len(actor_errors(run(governance=gov))) == 2

    @pytest.mark.parametrize("field,value", [
        ("commit_id", "9" * 40),
        ("state", "APPROVED"),
        ("submitted_at", "2026-08-19T16:12:46Z"),
        ("id", "4900000000"),
    ])
    def test_any_selected_review_field_change_relocks(self, field, value):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)], field: value,
        }
        assert len(actor_errors(run(governance=gov))) == 2

    @pytest.mark.parametrize("field,value", [
        ("id", "5900000000"),
        ("created_at", "2026-08-19T16:47:09Z"),
    ])
    def test_any_selected_comment_field_change_relocks(self, field, value):
        gov = Governance()
        gov.comments[P341_RATIFY] = {**gov.comments[P341_RATIFY], field: value}
        assert len(actor_errors(run(governance=gov))) == 2

    def test_the_mechanism_is_not_a_natural_language_parser(self):
        """A body containing VOID is not what relocks -- an ALTERED body is.

        The accepted PR #341 acceptance itself contains the word VOID (it discloses the
        retracted attempt). If the mechanism keyed on that word it would refuse the genuine
        record. The baseline fixture body is accepted unchanged; only alteration relocks.
        """
        assert "VOID" in Governance().comments[VOID_COMMENT_ID]["body"]
        assert actor_errors(run()) == []
        gov = Governance()
        gov.comments[P341_RATIFY] = {
            **gov.comments[P341_RATIFY],
            "body": ratification_body() + "\n\nNote: an earlier attempt was VOID.",
        }
        # Relocks because it is ALTERED, not because it says VOID.
        assert len(actor_errors(run(governance=gov))) == 2


class TestFingerprintIsCanonicalAndDeterministic:
    def test_fingerprint_is_stable_across_key_ordering(self):
        a = AUTH._canonical_record_fingerprint({"x": "1", "y": "2"})
        b = AUTH._canonical_record_fingerprint({"y": "2", "x": "1"})
        assert a == b

    def test_fingerprint_is_not_a_repr_of_the_mapping(self):
        digest = AUTH._canonical_record_fingerprint({"x": "1"})
        assert digest != hashlib.sha256(str({"x": "1"}).encode()).hexdigest()
        assert digest == hashlib.sha256(
            json.dumps({"x": "1"}, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

    def test_fingerprint_changes_when_any_selected_value_changes(self):
        base = AUTH._canonical_record_fingerprint({"x": "1", "y": "2"})
        assert AUTH._canonical_record_fingerprint({"x": "1", "y": "3"}) != base

    @pytest.mark.parametrize("missing", ["body", "user"])
    def test_unusable_records_fingerprint_to_none(self, missing):
        record = {"id": "1", "body": "x", "user": {"login": "a"}, "created_at": "t"}
        record.pop(missing)
        assert AUTH._comment_record_fingerprint(record) is None
        assert AUTH._review_record_fingerprint(record) is None


class TestFingerprintPinsAreTheRealRecords:
    """UNPATCHED. An independent copy of the digests derived from the live PR #341 records.

    The isolated tests above swap these for the fixture universe's own, so this class is
    what catches a mutation to the production constants themselves.
    """

    EXPECTED = {
        "RATIFICATION_REVIEW_FINGERPRINT":
            "904f4cb4642f0f7b8bcd6bb33be92d72678270b122402e5d423789960aa33067",
        "RATIFICATION_COMMENT_FINGERPRINT":
            "acbd2bb2a9ccb9c71475dab83d2ab62cfc1b9110ed5a597e232cd6aaa620b0c6",
        "RATIFICATION_VERIFICATION_FINGERPRINT":
            "763e4e2fbd2559bb4e4e6e04dd782e4f1d1840e750e23ab776cb44de74d9ed0d",
        "RATIFICATION_CLOSURE_FINGERPRINT":
            "4e39a8b16248ebe616f5262b6c476f3b6780eedfaf9df2e85d7113272a26f568",
    }

    @pytest.mark.parametrize("name", sorted(EXPECTED))
    def test_pin_matches_the_independently_recorded_digest(self, name):
        assert getattr(AUTH, name) == self.EXPECTED[name]

    def test_pins_are_well_formed_and_distinct(self):
        values = [getattr(AUTH, name) for name in self.EXPECTED]
        assert len(set(values)) == len(values)
        for value in values:
            assert len(value) == 64
            assert all(c in "0123456789abcdef" for c in value)

    def test_pins_are_not_the_fixture_values(self):
        for name, fixture_value in FIXTURE_FINGERPRINTS.items():
            assert getattr(AUTH, name) != fixture_value


# ======================================================================================
# 15. MAJOR 2 (review 4975556072) — XASSET-0041's own lifecycle is an ORDERED chain
# ======================================================================================


class TestRatificationLifecycleOrdering:
    """Every case below is run REPINNED, so it proves ordering alone -- not the digest."""

    def test_the_unmutated_baseline_still_passes_repinned(self):
        """Guards this whole class from becoming vacuously green."""
        assert actor_errors(run_repinned()) == []

    def test_acceptance_before_the_review_it_certifies(self):
        gov = Governance()
        gov.comments[P341_RATIFY] = {**gov.comments[P341_RATIFY], "created_at": "2026-08-19T16:00:00Z"}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_acceptance_after_the_merge_it_authorized(self):
        gov = Governance()
        gov.comments[P341_RATIFY] = {**gov.comments[P341_RATIFY], "created_at": "2026-08-19T17:30:00Z"}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_acceptance_exactly_at_the_merge_instant_is_refused(self):
        """Strict: an acceptance simultaneous with its own merge did not precede it."""
        gov = Governance()
        gov.comments[P341_RATIFY] = {**gov.comments[P341_RATIFY], "created_at": T_MERGE_341}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_post_merge_verification_predating_the_merge(self):
        gov = Governance()
        gov.comments[P341_VERIFY] = {**gov.comments[P341_VERIFY], "created_at": "2026-08-19T16:00:00Z"}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_post_merge_verification_exactly_at_the_merge_instant_is_allowed(self):
        """Only an EARLIER verification is impossible; a same-second one is real."""
        gov = Governance()
        gov.comments[P341_VERIFY] = {**gov.comments[P341_VERIFY], "created_at": T_MERGE_341}
        assert actor_errors(run_repinned(governance=gov)) == []

    def test_closure_before_the_post_merge_verification(self):
        gov = Governance()
        gov.comments[P341_CLOSURE] = {**gov.comments[P341_CLOSURE], "created_at": "2026-08-19T16:49:30Z"}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_closure_before_ci_completion(self):
        gov = Governance()
        gov.comments[P341_CLOSURE] = {**gov.comments[P341_CLOSURE], "created_at": "2026-08-19T16:52:00Z"}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_ratification_exactly_at_the_pr337_merge_instant_is_refused(self):
        """Strict retrospection: equality is not 'after'."""
        gov = Governance()
        gov.comments[P341_RATIFY] = {**gov.comments[P341_RATIFY], "created_at": T_MERGE_337}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    @pytest.mark.parametrize("target", ["ratify", "verify", "closure"])
    def test_a_missing_required_timestamp_fails_closed(self, target):
        gov = Governance()
        key = {"ratify": P341_RATIFY, "verify": P341_VERIFY, "closure": P341_CLOSURE}[target]
        gov.comments[key] = {k: v for k, v in gov.comments[key].items() if k != "created_at"}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    @pytest.mark.parametrize(
        "malformed",
        ["2026-08-19", "2026-08-19T16:47:08", "2026-08-19 16:47:08Z", "", "not-a-time", 17,
         "2026-08-19T16:47:08+00:00", "20260819T164708Z"],
    )
    def test_a_malformed_timestamp_fails_closed(self, malformed):
        gov = Governance()
        gov.comments[P341_RATIFY] = {**gov.comments[P341_RATIFY], "created_at": malformed}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_missing_review_submission_time_fails_closed(self):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            k: v for k, v in gov.review_records[(P341, P341_REVIEW)].items()
            if k != "submitted_at"
        }
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_missing_ci_job_completion_time_fails_closed(self):
        gov = Governance()
        gov.jobs[P341_JOB] = {k: v for k, v in gov.jobs[P341_JOB].items() if k != "completed_at"}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_missing_ratification_merge_time_fails_closed(self):
        gov = Governance()
        gov.pulls[P341] = {k: v for k, v in gov.pulls[P341].items() if k != "merged_at"}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_missing_pr337_merge_time_fails_closed(self):
        gov = Governance()
        gov.pulls[P337] = {k: v for k, v in gov.pulls[P337].items() if k != "merged_at"}
        assert len(actor_errors(run_repinned(governance=gov))) == 2


class TestInstantParsing:
    @pytest.mark.parametrize("good", ["2026-08-19T16:47:08Z", "1999-01-01T00:00:00Z"])
    def test_accepts_exact_utc_instants(self, good):
        assert AUTH._instant(good) == good

    @pytest.mark.parametrize(
        "bad",
        ["2026-08-19T16:47:08", "2026-08-19T16:47:08.000Z", "2026-08-19T16:47:08+00:00",
         "2026-08-19 16:47:08Z", "20260819T164708Z", "", None, 17, "xxxx-xx-xxTxx:xx:xxZ",
         "2026/08/19T16:47:08Z"],
    )
    def test_rejects_everything_else(self, bad):
        assert AUTH._instant(bad) is None


class TestRatificationReviewFinality:
    def test_native_changes_requested_selected_review_is_refused(self):
        """Native state is durable truth; approving prose cannot override it."""
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)], "state": "CHANGES_REQUESTED",
        }
        assert AUTH.parse_formal_disposition(
            gov.review_records[(P341, P341_REVIEW)]["body"]
        ) == AUTH.APPROVING_REVIEW_DISPOSITION
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def _later_review(self, submitted_at, state="CHANGES_REQUESTED", commit=None, rid="4979999999"):
        return {
            "commit_id": commit or P341_HEAD,
            "id": rid,
            "body": "FORMAL DISPOSITION: CHANGES REQUIRED — 1 BLOCKING",
            "user": {"login": PRINCIPAL},
            "state": state,
            "submitted_at": submitted_at,
            "html_url": f"{_issue_url(P341)}#pullrequestreview-{rid}",
        }

    def test_later_adverse_exact_head_review_before_merge_is_refused(self):
        gov = Governance()
        gov.review_records[(P341, "4979999999")] = self._later_review("2026-08-19T16:30:00Z")
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_later_adverse_review_after_the_merge_is_outside_the_lifecycle(self):
        gov = Governance()
        gov.review_records[(P341, "4979999999")] = self._later_review("2026-08-19T18:00:00Z")
        assert actor_errors(run_repinned(governance=gov)) == []

    def test_later_adverse_review_on_a_different_head_is_history(self):
        gov = Governance()
        gov.review_records[(P341, "4979999999")] = self._later_review(
            "2026-08-19T16:30:00Z", commit="9" * 40
        )
        assert actor_errors(run_repinned(governance=gov)) == []

    def test_a_dismissed_later_adverse_review_is_not_a_live_finding(self):
        gov = Governance()
        gov.review_records[(P341, "4979999999")] = self._later_review(
            "2026-08-19T16:30:00Z", state="DISMISSED"
        )
        assert actor_errors(run_repinned(governance=gov)) == []

    def test_an_earlier_adverse_review_is_legitimate_history(self):
        gov = Governance()
        gov.review_records[(P341, "4979999999")] = self._later_review("2026-08-19T16:00:00Z")
        assert actor_errors(run_repinned(governance=gov)) == []

    def test_an_unavailable_review_list_fails_closed(self):
        class NoList(Governance):
            def reviews(self, number):
                return None

        assert len(actor_errors(run_repinned(governance=NoList()))) == 2

    def test_finality_reuses_the_shared_machinery_not_a_parallel_definition(self):
        source = (REPO_ROOT / "level1_stage1_execution_authorization.py").read_text(
            encoding="utf-8"
        )
        derivation = source.split("def _derive_pr337_actor_ratification")[1].split(
            "\ndef verify_lifecycle_against_truth"
        )[0]
        assert "_verify_selected_review_is_final(" in derivation
        assert "NATIVE_ADVERSE_REVIEW_STATES" in derivation


# ======================================================================================
# 16. Each individual check, ISOLATED from the fingerprint
# ======================================================================================


class TestEachCheckIsIndependentlyLoadBearing:
    """Run REPINNED, so the fingerprint matches and only the named check can relock.

    Without this, the digest masks every field it covers: a dismissed review, an adverse
    body, or a swapped actor all change the fingerprint too, so a test using the baseline
    pins would pass even if the specific check were deleted. These prove each check does
    its own work.
    """

    def test_baseline_is_not_vacuously_green(self):
        assert actor_errors(run_repinned()) == []

    def test_review_exact_head_check_alone(self):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)], "commit_id": "9" * 40,
        }
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_dismissed_review_check_alone(self):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)], "state": "DISMISSED",
        }
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_approving_disposition_check_alone(self):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)],
            "body": "FORMAL DISPOSITION: CHANGES REQUIRED — 1 BLOCKING",
        }
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_unparseable_disposition_check_alone(self):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)], "body": "Looks fine to me.",
        }
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    @pytest.mark.parametrize("who", ["ratify", "verify", "closure"])
    def test_actor_check_alone(self, who):
        gov = Governance()
        key = {"ratify": P341_RATIFY, "verify": P341_VERIFY, "closure": P341_CLOSURE}[who]
        gov.comments[key] = {**gov.comments[key], "user": {"login": BOT}}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    @pytest.mark.parametrize("token", [
        P341_HEAD, P341_REVIEW, P337_HEAD, P337_REVIEW, P337_ACCEPT,
        P337_MERGE, P337_VERIFY, BOT, AUTH.RATIFICATION_REQUIRED_PHRASE,
    ])
    def test_required_token_check_alone(self, token):
        """SS-G.3/SS-G.4's content requirement does its own work, not the digest's."""
        gov = Governance()
        gov.comments[P341_RATIFY] = {
            **gov.comments[P341_RATIFY],
            "body": ratification_body().replace(token, "REDACTED"),
        }
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_verification_merge_naming_check_alone(self):
        gov = Governance()
        gov.comments[P341_VERIFY] = {**gov.comments[P341_VERIFY], "body": "Verified."}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_closure_ci_naming_check_alone(self):
        gov = Governance()
        gov.comments[P341_CLOSURE] = {
            **gov.comments[P341_CLOSURE], "body": f"Closure for merge `{P341_MERGE}`.",
        }
        assert len(actor_errors(run_repinned(governance=gov))) == 2


class TestClosureOrderingChecksAreSeparable:
    """The two closure comparisons are separate rules and must each stand alone.

    In the real ordering the CI completes AFTER the verification, so "closure precedes the
    verification" also implies "closure precedes CI" -- one rule hides behind the other.
    These fixtures put the CI completion BEFORE the verification so each comparison can be
    violated on its own.
    """

    def _ci_before_verification(self):
        gov = Governance()
        gov.jobs[P341_JOB] = {**gov.jobs[P341_JOB], "completed_at": "2026-08-19T16:49:30Z"}
        return gov

    def test_closure_between_ci_and_verification_violates_only_the_verification_rule(self):
        gov = self._ci_before_verification()
        # after CI (16:49:30), before the verification (16:50:40)
        gov.comments[P341_CLOSURE] = {**gov.comments[P341_CLOSURE], "created_at": "2026-08-19T16:50:00Z"}
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_closure_after_both_is_accepted(self):
        gov = self._ci_before_verification()
        assert actor_errors(run_repinned(governance=gov)) == []


class TestStrictRetrospectionIsSeparable:
    """Isolate rule 6 from rule 5.1.

    Stamping the acceptance at the PR #337 merge instant normally makes it PRECEDE the
    PR #341 review, so rule 5.1 fires first and rule 6 is never reached. Shifting the whole
    PR #341 lifecycle earlier keeps 5.1-5.4 satisfied, leaving strict retrospection as the
    only rule that can relock.
    """

    def _shifted(self, acceptance_at):
        gov = Governance()
        gov.review_records[(P341, P341_REVIEW)] = {
            **gov.review_records[(P341, P341_REVIEW)], "submitted_at": "2026-08-18T23:00:00Z",
        }
        gov.comments[P341_RATIFY] = {**gov.comments[P341_RATIFY], "created_at": acceptance_at}
        gov.pulls[P341] = {**gov.pulls[P341], "merged_at": "2026-08-19T00:00:00Z"}
        gov.comments[P341_VERIFY] = {**gov.comments[P341_VERIFY], "created_at": "2026-08-19T00:05:00Z"}
        gov.jobs[P341_JOB] = {**gov.jobs[P341_JOB], "completed_at": "2026-08-19T00:10:00Z"}
        gov.comments[P341_CLOSURE] = {**gov.comments[P341_CLOSURE], "created_at": "2026-08-19T00:15:00Z"}
        return gov

    def test_acceptance_exactly_at_the_pr337_merge_is_refused_by_retrospection_alone(self):
        gov = self._shifted(T_MERGE_337)  # 2026-08-18T23:50:58Z
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_acceptance_one_second_before_the_pr337_merge_is_refused(self):
        gov = self._shifted("2026-08-18T23:50:57Z")
        assert len(actor_errors(run_repinned(governance=gov))) == 2

    def test_acceptance_one_second_after_the_pr337_merge_is_accepted(self):
        """Guards the two above from passing for an unrelated reason."""
        gov = self._shifted("2026-08-18T23:50:59Z")
        assert actor_errors(run_repinned(governance=gov)) == []
