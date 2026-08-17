"""ENDPOINT-0001 Stage-1 operational execution authorization — XASSET-0029.

WHAT THIS MODULE IS
===================

XASSET-0028 closed the concrete construction universe STRUCTURALLY (680 registered
constructions across 48 cells). Structural closure is not operational authorization. This
module supplies the missing half: the mechanism by which exactly one Stage-1 execution
attempt may become operationally authorized, and the fail-closed machinery that decides
both "may a NEW execution start?" and "did THIS result come from the one lawful execution?"

WHY THE COMMITTED BOOLEAN IS NOT THE MECHANISM
==============================================

Flipping ``stage_1_executability.executable`` to true is wrong on three independent
grounds, the third dispositive: (1) a committed flag is effective the instant its PR
merges, before post-merge verification and before CI concludes; (2) a flag ASSERTS
authorization without demonstrating any gate closed; (3) it is already a validation error
-- ``_validate_stage_1_executability`` enforces ``_false(executable)``, so the canonical
file is INVALID in exactly the state that would authorize execution. XASSET-0029 preserves
that lock. ``executable`` stays false FOREVER: *no committed value in this repository
authorizes Stage-1 execution.*

CORRECTED AFTER INDEPENDENT FULL REVIEW 4946327932 (2 BLOCKING / 2 MAJOR)
========================================================================

BLOCKING 1 -- the previous form accepted the entire lifecycle from caller strings and
checked only internal consistency, so an entirely fictional review/acceptance/merge/CI
chain validated. Reproduced before correcting. Lifecycle facts are now DERIVED AND
RE-VERIFIED from two durable truth sources on every validation:

  * LOCAL GIT OBJECT STORE (``GitTruthSource``) -- merge SHA, both parents, ancestry, and
    the byte identity of load-bearing files AS THEY EXIST IN THE MERGED TREE. Content
    addressed and cryptographically durable; forging it means forging SHA-1/SHA-256
    preimages, not editing a JSON file.
  * GITHUB GOVERNANCE METADATA (``GovernanceTruthSource``) -- the review, its exact
    reviewed commit, its formal disposition, the reviewer's login, the principal
    acceptance comment, the post-merge verification comment, and the merge-commit CI
    run/job. This is GOVERNANCE metadata only. It is NOT market, price, fundamental, or
    any other economic data, and this module acquires none.

A recorded value is never accepted because its text is well-formed. Every recorded value
is compared against the independently fetched fact, and an unreachable source FAILS CLOSED.

BLOCKING 2 -- consuming the authorization made the public result validator reject the very
execution that consumed it, while deferring consumption until after the work left a replay
and concurrency window. Reproduced before correcting. The lane is now an explicit state
machine:

    ABSENT -> READY -> CLAIMED -> COMPLETED

and the two questions are separated, because they are genuinely different questions:

  * ``new_execution_is_authorized()``  -- may a NEW execution start?  READY only.
  * ``claimed_execution_is_authorized()`` -- did THIS result come from the one lawful
    claim? CLAIMED or COMPLETED, bound to the exact attestation hash and attempt id.

``validate_stage1_results()`` asks the SECOND question, so the lawfully claimed execution
can publish a valid result while a second execution remains impossible.

DURABILITY BOUNDARY -- STATED, NOT OVERCLAIMED
==============================================

``O_EXCL`` prevents a second creation only while the path exists, so "can never be
replayed" would be an overclaim. What is actually enforced:

  * The claim is recorded in TWO places -- ``claim.json`` and an append-only
    ``lane_ledger.jsonl``. Losing either one alone does NOT reopen the lane, because both
    are consulted and either is sufficient to establish CLAIMED.
  * Destroying the whole authorization directory destroys the attestation too, so the lane
    becomes ABSENT, which is NOT READY. Re-arming then requires passing the full
    authenticated lifecycle verification again from scratch.
  * A crash after CLAIM leaves the lane CLAIMED. It never returns to READY on its own.
    Recovery is a governed act, not an automatic transition.

A privileged operator who deletes the entire directory is outside any filesystem-based
enforcement boundary; that is disclosed here rather than papered over.

NOT A RISK MODULE. No RISK-0001 scenario, threshold, magnitude, window, parameter, attempt
identity, result value, or family conclusion is read, imported, or reused. Only neutral
engineering patterns are shared: canonical JSON hashing, duplicate-key rejection, immutable
preexecution metadata, exact-identity verification, O_EXCL one-shot creation, consuming
authorization at the first eligible work item, and fail-closed validation.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence

ROOT = Path(__file__).resolve().parent

# ======================================================================================
# Bound identity
# ======================================================================================

REPOSITORY_IDENTITY = "Mast3rkey/Portfolio-HQ"
STUDY_ID = "ENDPOINT-0001"
AUTHORIZING_DECISION = "XASSET-0029"
PREDECESSOR_DECISION = "XASSET-0028"

#: The XASSET-0029 pull request. Bound so an attestation cannot silently reference another.
AUTHORIZING_PULL_REQUEST = 328

#: The single Stage-1 execution lane XASSET-0027 SS-P.1 permits. Derived from repository
#: truth, not invented: no Stage-1 attempt has ever been executed or authorized.
EXECUTION_ATTEMPT_ID = "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

#: MAJOR 2 (review 4946397399): the exact base the XASSET-0029 lifecycle was reviewed against.
#: The real merge's FIRST parent must equal this. If main advances before merge, the lifecycle
#: cannot arm from the old review -- it requires a fresh exact-head/base review.
REVIEWED_BASE_SHA = "c51e94609eff7ede2bdfa084844d59b8347561e5"

#: XASSET-0028's exact historical identity. MAJOR 1: the canonical contract promises this
#: is bound, so it is now actually verified against the local git object store.
PREDECESSOR_MERGE_SHA = "c51e94609eff7ede2bdfa084844d59b8347561e5"
PREDECESSOR_ACCEPTED_HEAD = "036606401ea569b0a03f2d716d87a057d07d71dc"
PREDECESSOR_MERGE_BASE = "e4b6f0b810884fcb73d1b8ee053d8005db532f3e"

CONSTRUCTION_UNIVERSE_SHA256 = (
    "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
)
CONSTRUCTION_COUNT = 680
CONSTRUCTION_CELL_COUNT = 48

CANONICAL_PROTOCOL_RELPATH = "research/level1_endpoint_evidence/PROTOCOL_V1.md"
CANONICAL_PREREGISTRATION_RELPATH = "research/level1_endpoint_evidence/pre_registration.yaml"

PROTOCOL_PATH = ROOT / CANONICAL_PROTOCOL_RELPATH
PREREGISTRATION_PATH = ROOT / CANONICAL_PREREGISTRATION_RELPATH

#: EFFECTIVE pins for the canonical bytes, recomputed under XASSET-0036 SS-E.7 after the canonical,
#: enforcement, and outcome-producing bytes stabilized. Separate files from this module, so there
#: is no self-hashing circularity.
CANONICAL_PINS: dict[str, str] = {
    CANONICAL_PROTOCOL_RELPATH: (
        "3e1202b5ffccb35fdee52f18a8f6c1c92252adacbc32145acf59b9877ec40edc"
    ),
    CANONICAL_PREREGISTRATION_RELPATH: (
        "1fea41b5879a38cc4b54a9bc1bbd70e24bb759aecf05b3c6e00cb27ccb40b57e"
    ),
}

#: XASSET-0029's pins, retained as predecessor identity now that XASSET-0036's executable package
#: amends the canonical bytes under successor authority. History is never invalidated.
XASSET_0029_CANONICAL_PINS = {
    CANONICAL_PROTOCOL_RELPATH: (
        "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
    ),
    CANONICAL_PREREGISTRATION_RELPATH: (
        "6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c"
    ),
}

#: XASSET-0028's pins, retained as predecessor identity. History is never invalidated.
PREDECESSOR_CANONICAL_PINS = {
    CANONICAL_PROTOCOL_RELPATH: (
        "c02b4d519267b96ddb12500e6d1d55a47aeafd9437de8e41014c8871f631618c"
    ),
    CANONICAL_PREREGISTRATION_RELPATH: (
        "ffde86c1585050b2bf89e58033f37777a903ace86e97be46b6440a217c78ec4a"
    ),
}

#: MAJOR 1: load-bearing enforcement code. Expected identity is DERIVED FROM THE MERGED GIT
#: TREE at validation time, never from a hard-coded constant here -- a literal would have to
#: be edited in the same commit that changes the bytes it claims to verify, which is not a
#: check. Drift in any of these between the accepted/merged tree and the working tree is
#: refused.
#
# EXTENDED BY XASSET-0036 SS-E.6 / XASSET-0030 SS-G.B step 5. The prior set contained exactly six
# paths and NO outcome-producing code, because none existed when XASSET-0029 was accepted. An
# attestation could therefore have been perfectly authenticated while the code generating every one
# of the 680 dispositions was unbound, and ATTEMPT_1 is non-rerunnable after claim.
#
# The three added paths are exactly those whose bytes can materially decide, order, map, derive,
# serialize, write, or validate a Stage-1 outcome:
#   * the runner -- decides ordering, applies B1/B2/B3, composes dispositions, serializes, writes;
#   * the result validator -- decides whether a candidate result document may be published;
#   * XASSET-0036 itself -- the decision authorizing the package, on the same footing XASSET-0029
#     already occupies for its own authorization.
#
# The EXISTING exact-byte mechanism is reused unchanged (XASSET-0036 SS-E.6 states a preference for
# it, and no concrete technical reason to depart was found): expected identity is still DERIVED
# FROM THE MERGED GIT TREE at validation time, never from a hard-coded constant here.
LOAD_BEARING_RELPATHS = (
    "level1_stage1_execution_authorization.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_construction_universe_closure_validator.py",
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    CANONICAL_PROTOCOL_RELPATH,
    CANONICAL_PREREGISTRATION_RELPATH,
    "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
    "governance/decisions/XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
)

# ======================================================================================
# Lane storage — deliberately OUTSIDE the repository
# ======================================================================================

#: Outside the repository so no lane record can be committed, reviewed into existence, or
#: forged into a pull request. Deliberately NOT the RISK-0001 results location, which this
#: module never reads or references.
AUTHORIZATION_ROOT = Path("/var/tmp/phq-endpoint0001-stage1-authorization")
AUTHORIZATION_PATH = AUTHORIZATION_ROOT / "authorization.json"
CLAIM_PATH = AUTHORIZATION_ROOT / "claim.json"
COMPLETION_PATH = AUTHORIZATION_ROOT / "completion.json"
LEDGER_PATH = AUTHORIZATION_ROOT / "lane_ledger.jsonl"

# ======================================================================================
# Vocabulary
# ======================================================================================

REQUIRED_LIFECYCLE_GATES = (
    "INDEPENDENT_FULL_EXACT_HEAD_REVIEW",
    "PRINCIPAL_EXACT_HEAD_ACCEPTANCE",
    "MERGE",
    "POST_MERGE_VERIFICATION",
    "MERGE_COMMIT_CI_SUCCESS",
    "MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION",
)

AUTHORIZATION_MECHANISM = "EXTERNAL_ONE_SHOT_PREEXECUTION_ATTESTATION"
APPROVING_REVIEW_DISPOSITION = "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"

#: BLOCKING 2 (review 4946464366): the GitHub account that performs principal acceptance and
#: post-merge verification in this repository. Previously the acceptance and post-merge gates
#: checked only comment location and body text, so ANY account able to comment on the pull
#: request could impersonate them. This repository's principal, merge, and lifecycle-operator
#: account is the same login throughout its recorded history -- stated here honestly rather than
#: implying separate accounts exist.
PRINCIPAL_ACCOUNT_LOGIN = "Mast3rkey"
LIFECYCLE_OPERATOR_LOGIN = "Mast3rkey"

#: MAJOR 1: the repository's review grammar. The formal disposition is the FIRST formal line and
#: must match EXACTLY -- a substring test let an adverse review pass merely by containing the
#: approval phrase in later explanatory text.
FORMAL_DISPOSITION_PREFIX = "FORMAL DISPOSITION:"

#: GitHub's own review states. The NATIVE state is durable truth and is evaluated independently of
#: the repository's body grammar, so a later CHANGES_REQUESTED is adverse even with no formal line.
NATIVE_ADVERSE_REVIEW_STATES = frozenset({"CHANGES_REQUESTED"})

#: States that mechanically prove a later review is NOT an adverse finding. Anything outside both
#: sets, with no parseable formal disposition, is unclassifiable and fails closed.
NATIVE_NON_ADVERSE_REVIEW_STATES = frozenset({"APPROVED"})
SCHEMA_VERSION = 2

LANE_ABSENT = "ABSENT"
LANE_READY = "READY"
LANE_CLAIMED = "CLAIMED"
LANE_COMPLETED = "COMPLETED"

# Not a lane state: the marker :func:`_read_ledger` substitutes for any line it cannot read as
# exactly one mapping. Named because three separate sites must agree on it, and a divergence
# between them is precisely how MINOR 1 (review 4946706062) went unnoticed.
LEDGER_CORRUPT = "CORRUPT"

REQUIRED_TOP_KEYS = (
    "schema_version",
    "mechanism",
    "repository",
    "study_id",
    "authorizing_decision",
    "authorizing_pull_request",
    "predecessor_decision",
    "execution_attempt_id",
    "authorization_head",
    "predecessor_identity",
    "canonical_pins",
    "construction_universe",
    "lifecycle_evidence",
    "load_bearing_identity",
    "author_identity",
    "generated_at_utc",
)

REQUIRED_LIFECYCLE_EVIDENCE_KEYS = (
    "independent_review",
    "principal_acceptance",
    "merge",
    "post_merge_verification",
    "merge_commit_ci",
)


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()


# ======================================================================================
# Primitives
# ======================================================================================


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def stage1_result_identity(results: Any) -> str:
    """THE deterministic Stage-1 result SEMANTIC identity. One mechanism, every consumer.

    MAJOR 3 (review 4946464366): the canonical contract previously called this
    ``EXACT_RESULT_ARTIFACT_SHA256``, which was not truthful -- this is NOT the SHA-256 of the
    ``stage1_results.yaml`` file bytes. It is the SHA-256 of the canonical JSON serialization of
    the parsed result mapping, deliberately chosen so that key ordering and insignificant
    whitespace do not change identity while any content change does. Canonical wording is
    renamed to EXACT_STAGE1_RESULT_SEMANTIC_IDENTITY_SHA256 to match what the code computes.

    BLOCKING 2 (review 4946397399): completion recorded a result hash that nothing ever
    checked, so completing result A did not prevent publishing result B. This function is the
    single identity used by the future Stage-1 result writer, by ``complete_execution``, and by
    the PUBLIC ``validate_stage1_results`` gate, so "the exact completed artifact" is a
    mechanically decidable question rather than a promise.

    It hashes the canonical JSON serialization, so key order and insignificant whitespace do not
    change identity while any content change does. It invents no economic content.
    """
    return sha256_bytes(canonical_json(results).encode("utf-8"))


def _reject_duplicate_keys(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    """A duplicate key silently discards the earlier value in ordinary ``json.loads``."""
    seen: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key {key!r} in authorization document")
        seen[key] = value
    return seen


def _is_commit_sha(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value)
    )


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _mapping(value: Any, where: str, errors: list[str]) -> Mapping[str, Any] | None:
    if not isinstance(value, Mapping):
        errors.append(f"{where}: expected a mapping")
        return None
    return value


def _exact(value: Any, expected: Any, where: str, errors: list[str]) -> None:
    if value != expected:
        errors.append(f"{where}: expected {expected!r}, found {value!r}")


def pins_are_placeholders() -> bool:
    return any(not _is_sha256(value) for value in CANONICAL_PINS.values())


# ======================================================================================
# Truth sources — injectable so tests never touch live GitHub
# ======================================================================================


class GitTruthSource(Protocol):
    """The local git object store. Content-addressed, durable, offline."""

    def commit_parents(self, sha: str) -> tuple[str, ...] | None: ...
    def commit_tree(self, sha: str) -> str | None: ...
    def is_ancestor(self, ancestor: str, descendant: str) -> bool: ...
    def blob_sha256_at(self, commit: str, relpath: str) -> str | None: ...
    def head(self) -> str | None: ...


class GovernanceTruthSource(Protocol):
    """GitHub GOVERNANCE metadata only. Never market, price, or fundamental data."""

    def pull_request(self, number: int) -> Mapping[str, Any] | None: ...
    def review(self, number: int, review_id: str) -> Mapping[str, Any] | None: ...
    def reviews(self, number: int) -> Sequence[Mapping[str, Any]] | None: ...
    def issue_comment(self, comment_id: str) -> Mapping[str, Any] | None: ...
    def workflow_run(self, run_id: str) -> Mapping[str, Any] | None: ...
    def workflow_job(self, job_id: str) -> Mapping[str, Any] | None: ...


class LiveGitTruthSource:
    """Reads the real local git object store via plumbing commands."""

    def __init__(self, root: Path = ROOT) -> None:
        self._root = root

    def _run(self, *args: str) -> str | None:
        try:
            proc = subprocess.run(
                ["git", *args],
                cwd=self._root,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):  # pragma: no cover - defensive
            return None
        if proc.returncode != 0:
            return None
        return proc.stdout.strip()

    def commit_parents(self, sha: str) -> tuple[str, ...] | None:
        out = self._run("rev-list", "--parents", "-n", "1", sha)
        if not out:
            return None
        parts = out.split()
        return tuple(parts[1:]) if len(parts) > 1 else ()

    def commit_tree(self, sha: str) -> str | None:
        """The commit's tree SHA. Equal trees prove byte-identical content."""
        return self._run("rev-parse", f"{sha}^{{tree}}")

    def is_ancestor(self, ancestor: str, descendant: str) -> bool:
        try:
            proc = subprocess.run(
                ["git", "merge-base", "--is-ancestor", ancestor, descendant],
                cwd=self._root,
                capture_output=True,
                timeout=30,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):  # pragma: no cover - defensive
            return False
        return proc.returncode == 0

    def blob_sha256_at(self, commit: str, relpath: str) -> str | None:
        try:
            proc = subprocess.run(
                ["git", "cat-file", "blob", f"{commit}:{relpath}"],
                cwd=self._root,
                capture_output=True,
                timeout=30,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):  # pragma: no cover - defensive
            return None
        if proc.returncode != 0:
            return None
        return sha256_bytes(proc.stdout)

    def head(self) -> str | None:
        return self._run("rev-parse", "HEAD")


class LiveGovernanceTruthSource:
    """Reads GitHub governance metadata over HTTPS.

    GOVERNANCE ONLY. This fetches reviews, comments, pull-request state, and CI run/job
    status. It never fetches market, price, fundamental, or any other economic data, and it
    is not, and must not become, a Stage-1 data-acquisition path.
    """

    API = "https://api.github.com"
    REVIEW_PAGE_SIZE = 100
    #: A ceiling only, so a pathological listing cannot loop forever. Exceeding it returns None
    #: (fail closed), never a silently truncated list.
    MAX_REVIEW_PAGES = 50

    def __init__(self, repository: str = REPOSITORY_IDENTITY) -> None:
        self._repository = repository

    def _get(self, path: str) -> Mapping[str, Any] | None:
        import urllib.error
        import urllib.request

        request = urllib.request.Request(
            f"{self.API}{path}",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "phq-xasset-0029"},
        )
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception:  # pragma: no cover - network/permission failure fails closed
            return None
        return payload if isinstance(payload, Mapping) else None

    def _get_list(self, path: str) -> list[Mapping[str, Any]] | None:
        import urllib.request

        request = urllib.request.Request(
            f"{self.API}{path}",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "phq-xasset-0029"},
        )
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception:  # pragma: no cover - network/permission failure fails closed
            return None
        return payload if isinstance(payload, list) else None

    def pull_request(self, number: int) -> Mapping[str, Any] | None:
        return self._get(f"/repos/{self._repository}/pulls/{number}")

    def review(self, number: int, review_id: str) -> Mapping[str, Any] | None:
        return self._get(f"/repos/{self._repository}/pulls/{number}/reviews/{review_id}")

    def reviews(self, number: int) -> Sequence[Mapping[str, Any]] | None:
        """EVERY review on the pull request, for finality checking.

        MAJOR 1 (review 4946540894): this previously issued ONE request for the first 100
        reviews and returned it as though it were the whole list, so with enough history a later
        adverse exact-head review could sit on page 2 and never be seen. Pagination now continues
        until a short page proves exhaustion, and ANY page that fails to retrieve or decode
        returns ``None`` so the caller fails closed rather than reasoning over a partial list.
        """
        collected: list[Mapping[str, Any]] = []
        page = 1
        while page <= self.MAX_REVIEW_PAGES:
            payload = self._get_list(
                f"/repos/{self._repository}/pulls/{number}/reviews"
                f"?per_page={self.REVIEW_PAGE_SIZE}&page={page}"
            )
            if payload is None:
                return None  # a failed page means the list is NOT proven complete
            collected.extend(payload)
            if len(payload) < self.REVIEW_PAGE_SIZE:
                return collected  # a short page proves exhaustion
            page += 1
        # Ran past the page ceiling without proving exhaustion: refuse to assert completeness.
        return None

    def issue_comment(self, comment_id: str) -> Mapping[str, Any] | None:
        return self._get(f"/repos/{self._repository}/issues/comments/{comment_id}")

    def workflow_run(self, run_id: str) -> Mapping[str, Any] | None:
        return self._get(f"/repos/{self._repository}/actions/runs/{run_id}")

    def workflow_job(self, job_id: str) -> Mapping[str, Any] | None:
        return self._get(f"/repos/{self._repository}/actions/jobs/{job_id}")


@dataclass(frozen=True)
class TruthSources:
    git: GitTruthSource = field(default_factory=LiveGitTruthSource)
    governance: GovernanceTruthSource = field(default_factory=LiveGovernanceTruthSource)


# ======================================================================================
# Live repository facts
# ======================================================================================


def live_canonical_hashes() -> dict[str, str]:
    return {relative: sha256_file(ROOT / relative) for relative in sorted(CANONICAL_PINS)}


def live_construction_universe_facts() -> dict[str, Any]:
    import level1_construction_universe_closure_validator as closure

    return {
        "sha256": closure.universe_aggregate_sha256(),
        "count": closure.derived_cardinality(),
        "cell_count": len(closure.per_cell_cardinality()),
    }


def live_load_bearing_hashes() -> dict[str, str]:
    return {relative: sha256_file(ROOT / relative) for relative in sorted(LOAD_BEARING_RELPATHS)}


# ======================================================================================
# Authenticated lifecycle verification — BLOCKING 1
# ======================================================================================


def parse_formal_disposition(body: str) -> str | None:
    """Return the review's FORMAL DISPOSITION verdict, parsed exactly from the first formal line.

    MAJOR 1 (review 4946464366): the previous check was ``APPROVING_REVIEW_DISPOSITION in body``,
    so a review whose formal line read ``CHANGES REQUIRED`` still passed if any later explanatory
    sentence quoted the approval phrase. Reproduced before correcting.

    Only the FIRST ``FORMAL DISPOSITION:`` line counts, and only the verdict up to the first
    finding-count separator, so trailing counts such as ``— 0 BLOCKING / 0 MAJOR`` do not change
    the verdict while a different verdict always does.
    """
    if not isinstance(body, str):
        return None
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.upper().startswith(FORMAL_DISPOSITION_PREFIX):
            continue
        verdict = stripped[len(FORMAL_DISPOSITION_PREFIX):].strip()
        for separator in ("—", "--", " - ", "|"):
            if separator in verdict:
                verdict = verdict.split(separator, 1)[0].strip()
        return verdict
    return None


def _actor_login(record: Mapping[str, Any]) -> str | None:
    user = record.get("user")
    if isinstance(user, Mapping):
        login = user.get("login")
        return login if isinstance(login, str) and login.strip() else None
    return None


def _belongs_to_pull_request(record: Mapping[str, Any], number: Any) -> bool:
    """Does this durable record actually belong to the authorizing pull request?

    MAJOR 1: acceptance and post-merge verification were fetched as repository-wide comment
    ids and only their body text was inspected, so a comment from any other pull request or
    issue satisfied the gate. GitHub records carry their own owning URL; a record without one
    cannot prove ownership and is refused.
    """
    if not isinstance(number, int):
        return False
    marker = f"/{number}"
    for key in ("issue_url", "pull_request_url", "html_url", "_links"):
        value = record.get(key)
        if isinstance(value, str) and (value.endswith(marker) or f"{marker}#" in value):
            return True
    return False


def verify_lifecycle_against_truth(
    document: Mapping[str, Any], sources: TruthSources
) -> tuple[str, ...]:
    """Re-derive every lifecycle fact from durable truth and compare.

    Nothing is accepted because a recorded string is well-formed. Every claim is checked
    against an independently fetched fact, and an unreachable source fails closed.
    """
    errors: list[str] = []
    evidence = document.get("lifecycle_evidence")
    if not isinstance(evidence, Mapping):
        return ("lifecycle_evidence: expected a mapping",)

    head = document.get("authorization_head")
    number = document.get("authorizing_pull_request")

    # --- The pull request itself -------------------------------------------------------
    pull = sources.governance.pull_request(number) if isinstance(number, int) else None
    if pull is None:
        errors.append(
            f"governance truth: pull request #{number!r} could not be verified; an "
            "unverifiable lifecycle never authorizes execution"
        )
        return tuple(errors)

    repo_full = ((pull.get("base") or {}).get("repo") or {}).get("full_name")
    if repo_full != REPOSITORY_IDENTITY:
        errors.append(f"governance truth: pull request belongs to {repo_full!r}")
    if pull.get("merged") is not True:
        errors.append("governance truth: pull request is not merged")
    real_head = (pull.get("head") or {}).get("sha")
    if real_head != head:
        errors.append(
            f"governance truth: pull request head is {real_head!r}, not the recorded "
            f"authorization_head {head!r}"
        )
    real_merge = pull.get("merge_commit_sha")

    # --- Gate 1: the review really exists, on the exact head ---------------------------
    recorded_review = evidence.get("independent_review") or {}
    review_id = str(recorded_review.get("review_id") or "")
    review = sources.governance.review(number, review_id) if review_id else None
    if review is None:
        errors.append(
            f"governance truth: independent review {review_id!r} does not exist on pull "
            f"request #{number}; a well-formed but nonexistent review id never authorizes "
            "execution"
        )
    else:
        if review.get("commit_id") != head:
            errors.append(
                f"governance truth: review {review_id} was submitted against "
                f"{review.get('commit_id')!r}, not the authorization head {head!r}"
            )
        verdict = parse_formal_disposition(review.get("body") or "")
        if verdict is None:
            errors.append(
                f"governance truth: review {review_id} carries no parseable "
                f"'{FORMAL_DISPOSITION_PREFIX}' line, so its verdict cannot be authenticated"
            )
        elif verdict != APPROVING_REVIEW_DISPOSITION:
            errors.append(
                f"governance truth: review {review_id}'s formal disposition is {verdict!r}, not "
                f"{APPROVING_REVIEW_DISPOSITION!r}; an adverse review never authorizes execution "
                "even if its explanatory text quotes the approval phrase"
            )
        # Reviewer identity is DERIVED from durable metadata, never self-declared.
        derived_reviewer = (review.get("user") or {}).get("login")
        if recorded_review.get("reviewer_identity") != derived_reviewer:
            errors.append(
                "governance truth: reviewer_identity is self-declared as "
                f"{recorded_review.get('reviewer_identity')!r} but the durable review "
                f"metadata says {derived_reviewer!r}; reviewer identity may not be asserted"
            )
        # MAJOR 1: a dismissed or adverse review is not a lifecycle gate.
        if str(review.get("state") or "").upper() == "DISMISSED":
            errors.append(
                f"governance truth: review {review_id} has been DISMISSED and cannot certify a "
                "lifecycle gate"
            )
        # The review must belong to THIS pull request, not merely exist somewhere.
        if not _belongs_to_pull_request(review, number):
            errors.append(
                f"governance truth: review {review_id} does not belong to pull request #{number}"
            )

    # --- Gate 1b: the selected review must be the FINAL clean exact-head review ---------
    # MAJOR 2 (review 4946464366): only the certified review id was consulted, so a clean pass
    # followed by a later CHANGES REQUIRED review on the SAME head still armed the lifecycle.
    # Historical adverse reviews BEFORE the final clean pass are legitimate and are preserved.
    errors.extend(
        _verify_selected_review_is_final(
            sources, number, head, review_id, (review or {}).get("submitted_at"), pull
        )
    )

    # --- Gate 2: principal acceptance really exists and names the exact head -----------
    acceptance_id = str((evidence.get("principal_acceptance") or {}).get("comment_id") or "")
    acceptance = sources.governance.issue_comment(acceptance_id) if acceptance_id else None
    if acceptance is None:
        errors.append(
            f"governance truth: principal acceptance comment {acceptance_id!r} does not exist"
        )
    else:
        acceptance_body = acceptance.get("body") or ""
        if isinstance(head, str) and head not in acceptance_body:
            errors.append(
                f"governance truth: acceptance comment {acceptance_id} does not name the exact "
                f"head {head!r}"
            )
        if not _belongs_to_pull_request(acceptance, number):
            errors.append(
                f"governance truth: acceptance comment {acceptance_id} does not belong to pull "
                f"request #{number}"
            )
        # BLOCKING 2: the acceptance must be the PRINCIPAL's, not merely a qualifying comment.
        acceptance_actor = _actor_login(acceptance)
        if acceptance_actor is None:
            errors.append(
                f"governance truth: acceptance comment {acceptance_id} carries no durable author "
                "identity, so the principal gate cannot be authenticated"
            )
        elif acceptance_actor != PRINCIPAL_ACCOUNT_LOGIN:
            errors.append(
                f"governance truth: acceptance comment {acceptance_id} was authored by "
                f"{acceptance_actor!r}, not the principal {PRINCIPAL_ACCOUNT_LOGIN!r}"
            )
        # MAJOR 1 -- PRINCIPAL CERTIFICATION replaces the unobservable independence property.
        # Same-account GitHub means login inequality cannot prove independent session authorship,
        # so the honest, mechanically verifiable substitute is that the principal's own durable
        # acceptance record NAMES the exact independent review pass being relied upon.
        if review_id and review_id not in acceptance_body:
            errors.append(
                f"governance truth: acceptance comment {acceptance_id} does not certify the "
                f"independent review {review_id!r} it relies upon; the principal must durably "
                "identify the exact review pass"
            )
        # Chronology: review, then acceptance, then merge.
        submitted = (review or {}).get("submitted_at")
        accepted = acceptance.get("created_at")
        merged_at = pull.get("merged_at")
        if submitted and accepted and str(accepted) < str(submitted):
            errors.append(
                f"governance truth: acceptance {accepted} precedes review {submitted}; the "
                "principal cannot certify a review that had not yet been submitted"
            )
        if accepted and merged_at and str(merged_at) < str(accepted):
            errors.append(
                f"governance truth: merge {merged_at} precedes acceptance {accepted}"
            )

    # --- Gate 3: the merge, its real SHA, and its real parents -------------------------
    recorded_merge = evidence.get("merge") or {}
    merge_sha = recorded_merge.get("merge_sha")
    if real_merge and merge_sha != real_merge:
        errors.append(
            f"governance truth: recorded merge {merge_sha!r} is not the real merge commit "
            f"{real_merge!r}"
        )
    real_parents = sources.git.commit_parents(merge_sha) if _is_commit_sha(merge_sha) else None
    if real_parents is None:
        errors.append(
            f"git truth: merge commit {merge_sha!r} does not exist in the local object store"
        )
    else:
        if list(recorded_merge.get("parents") or []) != list(real_parents):
            errors.append(
                f"git truth: recorded parents {list(recorded_merge.get('parents') or [])!r} do "
                f"not equal the real parents {list(real_parents)!r}"
            )
        if len(real_parents) != 2:
            errors.append(
                f"git truth: merge {merge_sha} has {len(real_parents)} parent(s); a squash or "
                "rebase does not carry the accepted head as a parent"
            )
        else:
            # MAJOR 2: bind BOTH parents exactly. Binding only the second let the base drift
            # after review, so a different base -- or a merge resolution -- could silently
            # become the authorized implementation.
            if real_parents[0] != REVIEWED_BASE_SHA:
                errors.append(
                    f"git truth: merge first parent {real_parents[0]!r} is not the exact reviewed "
                    f"base {REVIEWED_BASE_SHA!r}; base drift requires a fresh exact-head/base "
                    "review and cannot arm from the old one"
                )
            if real_parents[1] != head:
                errors.append(
                    f"git truth: merge second parent {real_parents[1]!r} is not the accepted head "
                    f"{head!r}; the merged bytes are not the accepted bytes"
                )
            # ZERO MERGE DRIFT: equal trees prove merging changed no reviewed byte.
            merge_tree = sources.git.commit_tree(str(merge_sha))
            head_tree = sources.git.commit_tree(str(head)) if _is_commit_sha(head) else None
            if merge_tree is None or head_tree is None:
                errors.append(
                    "git truth: merge or accepted-head tree could not be resolved, so zero merge "
                    "drift cannot be proven"
                )
            elif merge_tree != head_tree:
                errors.append(
                    f"git truth: merge tree {merge_tree} differs from the accepted head tree "
                    f"{head_tree}; merging changed reviewed bytes, so the merged tree may not "
                    "become its own source of truth"
                )

    # --- Gate 4: the post-merge verification record really exists ----------------------
    verification_id = str(
        (evidence.get("post_merge_verification") or {}).get("comment_id") or ""
    )
    verification = (
        sources.governance.issue_comment(verification_id) if verification_id else None
    )
    if verification is None:
        errors.append(
            f"governance truth: post-merge verification comment {verification_id!r} does not "
            "exist; merge alone never authorizes execution"
        )
    else:
        if isinstance(merge_sha, str) and merge_sha not in (verification.get("body") or ""):
            errors.append(
                f"governance truth: post-merge verification {verification_id} does not name the "
                f"merge SHA {merge_sha!r}"
            )
        if not _belongs_to_pull_request(verification, number):
            errors.append(
                f"governance truth: post-merge verification {verification_id} does not belong to "
                f"pull request #{number}"
            )
        verification_actor = _actor_login(verification)
        if verification_actor is None:
            errors.append(
                f"governance truth: post-merge verification {verification_id} carries no durable "
                "author identity, so the verification gate cannot be authenticated"
            )
        elif verification_actor != LIFECYCLE_OPERATOR_LOGIN:
            errors.append(
                f"governance truth: post-merge verification {verification_id} was authored by "
                f"{verification_actor!r}, not the lifecycle operator "
                f"{LIFECYCLE_OPERATOR_LOGIN!r}"
            )
        verified_at = verification.get("created_at")
        merged_at = pull.get("merged_at")
        if verified_at and merged_at and str(verified_at) < str(merged_at):
            errors.append(
                f"governance truth: post-merge verification {verified_at} precedes the merge "
                f"{merged_at}; it cannot verify a merge that had not happened"
            )

    # --- Gate 5: the merge-commit CI run AND its job, correctly paired ------------------
    recorded_ci = evidence.get("merge_commit_ci") or {}
    run_id = str(recorded_ci.get("run_id") or "")
    job_id = str(recorded_ci.get("job_id") or "")
    run = sources.governance.workflow_run(run_id) if run_id else None
    if run is None:
        errors.append(f"governance truth: workflow run {run_id!r} does not exist")
    else:
        if run.get("status") != "completed" or run.get("conclusion") != "success":
            errors.append(
                f"governance truth: workflow run {run_id} is "
                f"{run.get('status')!r}/{run.get('conclusion')!r}, not completed/success"
            )
        if run.get("head_sha") != merge_sha:
            errors.append(
                f"governance truth: workflow run {run_id} ran against {run.get('head_sha')!r}, "
                f"not the merge commit {merge_sha!r}"
            )
    job = sources.governance.workflow_job(job_id) if job_id else None
    if job is None:
        errors.append(f"governance truth: workflow job {job_id!r} does not exist")
    else:
        if str(job.get("run_id")) != run_id:
            errors.append(
                f"governance truth: job {job_id} belongs to run {job.get('run_id')!r}, not the "
                f"recorded run {run_id!r}"
            )
        if job.get("conclusion") != "success":
            errors.append(f"governance truth: job {job_id} concluded {job.get('conclusion')!r}")

    # --- Gate 6: ancestry, predecessor identity, load-bearing byte identity -------------
    errors.extend(_verify_git_anchored_identity(document, merge_sha, sources))
    return tuple(errors)


def _verify_selected_review_is_final(
    sources: TruthSources,
    number: Any,
    head: Any,
    selected_review_id: str,
    selected_submitted_at: Any,
    pull: Mapping[str, Any],
) -> list[str]:
    """Reject a later non-dismissed adverse review on the EXACT accepted head.

    Scope, stated precisely:

      * only reviews on the exact accepted head matter -- reviews on older heads are history and
        never invalidate the current head;
      * only reviews submitted AFTER the selected approving review and BEFORE the merge matter;
      * a DISMISSED later review does not count as a live adverse finding;
      * a later APPROVING review is not adverse.
    """
    errors: list[str] = []
    listing = sources.governance.reviews(number) if isinstance(number, int) else None
    if listing is None:
        errors.append(
            "governance truth: the pull request's review list could not be retrieved, so the "
            "selected review's finality cannot be established; this fails closed"
        )
        return errors

    merged_at = str(pull.get("merged_at") or "")
    selected_at = str(selected_submitted_at or "")
    for entry in listing:
        if not isinstance(entry, Mapping):
            continue
        if str(entry.get("id")) == str(selected_review_id):
            continue
        if entry.get("commit_id") != head:
            continue  # a different head: historical, not a live finding on this one
        if str(entry.get("state") or "").upper() == "DISMISSED":
            continue
        submitted = str(entry.get("submitted_at") or "")
        if selected_at and submitted and submitted <= selected_at:
            continue  # precedes the final clean pass: legitimate history
        if merged_at and submitted and submitted > merged_at:
            continue  # after the merge: outside this lifecycle
        state = str(entry.get("state") or "").upper()
        verdict = parse_formal_disposition(entry.get("body") or "")

        # GitHub's NATIVE state is durable truth and must never be weaker than the repository's
        # own body grammar. A later CHANGES_REQUESTED is adverse whether or not it carries a
        # formal line.
        if state in NATIVE_ADVERSE_REVIEW_STATES:
            errors.append(
                f"governance truth: review {entry.get('id')} on the exact accepted head is a "
                f"later non-dismissed {state} review submitted after the certified review "
                f"{selected_review_id}; principal certification of an earlier clean pass does "
                "not erase a later exact-head finding"
            )
            continue
        if verdict == APPROVING_REVIEW_DISPOSITION:
            continue  # a later approving pass is not adverse
        if verdict is None:
            # Unclassifiable: neither a native adverse state nor a parseable formal disposition.
            # Finality cannot be asserted over a review whose verdict is unknown, so this fails
            # closed rather than being silently ignored.
            if state in NATIVE_NON_ADVERSE_REVIEW_STATES:
                continue
            errors.append(
                f"governance truth: review {entry.get('id')} on the exact accepted head, "
                f"submitted after the certified review {selected_review_id}, carries neither a "
                f"recognised native state ({state or 'unset'!r}) nor a parseable formal "
                "disposition, so it cannot be proven non-adverse; finality fails closed"
            )
            continue
        errors.append(
            f"governance truth: review {entry.get('id')} on the exact accepted head carries "
            f"the later adverse formal disposition {verdict!r}, submitted after the certified "
            f"review {selected_review_id}; principal certification of an earlier clean pass "
            "does not erase a later exact-head finding"
        )
    return errors


def _verify_git_anchored_identity(
    document: Mapping[str, Any], merge_sha: Any, sources: TruthSources
) -> list[str]:
    """MAJOR 1: predecessor identity, current ancestry, and load-bearing byte identity."""
    errors: list[str] = []

    # Predecessor XASSET-0028 identity, verified from git rather than merely declared.
    recorded_predecessor = document.get("predecessor_identity")
    if not isinstance(recorded_predecessor, Mapping):
        errors.append("predecessor_identity: expected a mapping")
    else:
        _exact(
            recorded_predecessor.get("merge_sha"),
            PREDECESSOR_MERGE_SHA,
            "predecessor_identity.merge_sha",
            errors,
        )
        _exact(
            recorded_predecessor.get("accepted_head"),
            PREDECESSOR_ACCEPTED_HEAD,
            "predecessor_identity.accepted_head",
            errors,
        )
        _exact(
            recorded_predecessor.get("merge_base"),
            PREDECESSOR_MERGE_BASE,
            "predecessor_identity.merge_base",
            errors,
        )
    predecessor_parents = sources.git.commit_parents(PREDECESSOR_MERGE_SHA)
    if predecessor_parents is None:
        errors.append(
            f"git truth: predecessor merge {PREDECESSOR_MERGE_SHA} is absent from the local "
            "object store"
        )
    elif list(predecessor_parents) != [PREDECESSOR_MERGE_BASE, PREDECESSOR_ACCEPTED_HEAD]:
        errors.append(
            f"git truth: predecessor merge parents {list(predecessor_parents)!r} do not match "
            f"XASSET-0028's accepted identity"
        )

    # Current ancestry: the authorizing merge must be reachable from the working HEAD.
    head_now = sources.git.head()
    if not head_now:
        errors.append("git truth: current HEAD could not be resolved")
    elif _is_commit_sha(merge_sha) and not sources.git.is_ancestor(merge_sha, head_now):
        errors.append(
            f"git truth: the authorizing merge {merge_sha} is not an ancestor of the current "
            f"HEAD {head_now}; the working tree is not on the authorized history"
        )

    # Load-bearing byte identity: expected values come from the MERGED TREE, not a constant.
    recorded = document.get("load_bearing_identity")
    if not isinstance(recorded, Mapping):
        errors.append("load_bearing_identity: expected a mapping")
        return errors
    if sorted(recorded) != sorted(LOAD_BEARING_RELPATHS):
        errors.append(
            "load_bearing_identity: must cover exactly the load-bearing files "
            f"{sorted(LOAD_BEARING_RELPATHS)!r}"
        )
    accepted_head = document.get("authorization_head")
    for relative in sorted(LOAD_BEARING_RELPATHS):
        if not _is_commit_sha(merge_sha):
            continue
        merged = sources.git.blob_sha256_at(str(merge_sha), relative)
        if merged is None:
            errors.append(
                f"git truth: {relative} is absent from the authorized merged tree {merge_sha}"
            )
            continue
        # MAJOR 2: the merged tree may not become its own source of truth. Every load-bearing
        # blob must ALSO equal the same blob in the independently reviewed head.
        if _is_commit_sha(accepted_head):
            reviewed = sources.git.blob_sha256_at(str(accepted_head), relative)
            if reviewed is None:
                errors.append(
                    f"git truth: {relative} is absent from the reviewed head {accepted_head}"
                )
            elif reviewed != merged:
                errors.append(
                    f"merge drift: {relative} differs between the reviewed head "
                    f"({reviewed}) and the merged tree ({merged}); merging changed a "
                    "load-bearing file that independent review never saw"
                )
        if recorded.get(relative) != merged:
            errors.append(
                f"load_bearing_identity[{relative!r}]: recorded {recorded.get(relative)!r} but "
                f"the authorized merged tree has {merged!r}"
            )
        working = sha256_file(ROOT / relative) if (ROOT / relative).exists() else None
        if working != merged:
            errors.append(
                f"enforcement drift: {relative} in the working tree hashes to {working!r} but "
                f"the authorized merged tree has {merged!r}; load-bearing code has changed "
                "since the authorized merge"
            )
    return errors


# ======================================================================================
# Document validation
# ======================================================================================


def validate_authorization_document(
    document: Any, sources: TruthSources | None = None
) -> ValidationResult:
    """Validate an attestation: closed schema, bound identity, and AUTHENTICATED lifecycle."""
    errors: list[str] = []

    root = _mapping(document, "authorization", errors)
    if root is None:
        return ValidationResult(False, tuple(errors))

    for key in sorted(set(root) - set(REQUIRED_TOP_KEYS)):
        errors.append(f"authorization.{key}: unknown key; the schema is closed")
    for key in REQUIRED_TOP_KEYS:
        if key not in root:
            errors.append(f"authorization.{key}: required key is absent")
    if errors:
        return ValidationResult(False, tuple(errors))

    _exact(root.get("schema_version"), SCHEMA_VERSION, "authorization.schema_version", errors)
    _exact(root.get("mechanism"), AUTHORIZATION_MECHANISM, "authorization.mechanism", errors)
    _exact(root.get("repository"), REPOSITORY_IDENTITY, "authorization.repository", errors)
    _exact(root.get("study_id"), STUDY_ID, "authorization.study_id", errors)
    _exact(
        root.get("authorizing_decision"),
        AUTHORIZING_DECISION,
        "authorization.authorizing_decision",
        errors,
    )
    _exact(
        root.get("authorizing_pull_request"),
        AUTHORIZING_PULL_REQUEST,
        "authorization.authorizing_pull_request",
        errors,
    )
    _exact(
        root.get("predecessor_decision"),
        PREDECESSOR_DECISION,
        "authorization.predecessor_decision",
        errors,
    )
    _exact(
        root.get("execution_attempt_id"),
        EXECUTION_ATTEMPT_ID,
        "authorization.execution_attempt_id",
        errors,
    )
    if not _is_commit_sha(root.get("authorization_head")):
        errors.append("authorization.authorization_head: expected a 40-character commit SHA")

    _validate_canonical_pins(root.get("canonical_pins"), errors)
    _validate_construction_universe(root.get("construction_universe"), errors)
    _validate_lifecycle_shape(root.get("lifecycle_evidence"), errors)

    if not isinstance(root.get("author_identity"), str) or not root["author_identity"].strip():
        errors.append("authorization.author_identity: expected a non-empty string")
    if not isinstance(root.get("generated_at_utc"), str) or not root["generated_at_utc"].strip():
        errors.append("authorization.generated_at_utc: expected a non-empty string")

    # AUTHENTICATION. Structural shape alone never authorizes.
    errors.extend(verify_lifecycle_against_truth(root, sources or TruthSources()))
    return ValidationResult(not errors, tuple(errors))


def _validate_canonical_pins(block: Any, errors: list[str]) -> None:
    pins = _mapping(block, "authorization.canonical_pins", errors)
    if pins is None:
        return
    if pins_are_placeholders():
        errors.append(
            "authorization.canonical_pins: XASSET-0029 successor pins have not been refreshed "
            "to real digests, so no attestation can be validated"
        )
        return
    live = live_canonical_hashes()
    for relative, bound in sorted(CANONICAL_PINS.items()):
        if pins.get(relative) != bound:
            errors.append(
                f"authorization.canonical_pins[{relative!r}]: recorded {pins.get(relative)!r} "
                f"but the bound XASSET-0029 pin is {bound!r}"
            )
        if live.get(relative) != bound:
            errors.append(
                f"canonical drift: {relative} on disk hashes to {live.get(relative)!r} but the "
                f"bound XASSET-0029 pin is {bound!r}"
            )
    for relative in sorted(set(pins) - set(CANONICAL_PINS)):
        errors.append(
            f"authorization.canonical_pins[{relative!r}]: unknown canonical file; the pin set "
            "is closed"
        )


def _validate_construction_universe(block: Any, errors: list[str]) -> None:
    recorded = _mapping(block, "authorization.construction_universe", errors)
    if recorded is None:
        return
    _exact(
        recorded.get("sha256"),
        CONSTRUCTION_UNIVERSE_SHA256,
        "authorization.construction_universe.sha256",
        errors,
    )
    _exact(
        recorded.get("count"), CONSTRUCTION_COUNT, "authorization.construction_universe.count", errors
    )
    _exact(
        recorded.get("cell_count"),
        CONSTRUCTION_CELL_COUNT,
        "authorization.construction_universe.cell_count",
        errors,
    )
    try:
        live = live_construction_universe_facts()
    except Exception as exc:  # pragma: no cover - defensive
        errors.append(f"construction universe could not be recomputed live: {exc}")
        return
    if live["sha256"] != CONSTRUCTION_UNIVERSE_SHA256:
        errors.append(f"universe drift: live universe hashes to {live['sha256']!r}")
    if live["count"] != CONSTRUCTION_COUNT:
        errors.append(f"universe drift: live universe has {live['count']} constructions")
    if live["cell_count"] != CONSTRUCTION_CELL_COUNT:
        errors.append(f"universe drift: live universe has {live['cell_count']} cells")


def _validate_lifecycle_shape(block: Any, errors: list[str]) -> None:
    """Structural shape only. Authenticity is established by verify_lifecycle_against_truth."""
    evidence = _mapping(block, "authorization.lifecycle_evidence", errors)
    if evidence is None:
        return
    where = "authorization.lifecycle_evidence"
    for key in REQUIRED_LIFECYCLE_EVIDENCE_KEYS:
        if key not in evidence:
            errors.append(f"{where}.{key}: required gate evidence is absent")
    for key in sorted(set(evidence) - set(REQUIRED_LIFECYCLE_EVIDENCE_KEYS) - {"gates_closed"}):
        errors.append(f"{where}.{key}: unknown gate evidence; the schema is closed")
    declared = evidence.get("gates_closed") or ()
    if not isinstance(declared, (list, tuple)):
        errors.append(f"{where}.gates_closed: expected a list")
        declared = ()
    for gate in REQUIRED_LIFECYCLE_GATES:
        if gate not in declared:
            errors.append(f"{where}.gates_closed: must include {gate!r}")
    for gate in declared:
        if gate not in REQUIRED_LIFECYCLE_GATES:
            errors.append(f"{where}.gates_closed: unknown gate {gate!r}")
    review = evidence.get("independent_review")
    if isinstance(review, Mapping):
        for counter in ("blocking_count", "major_count"):
            if review.get(counter) != 0:
                errors.append(
                    f"{where}.independent_review.{counter}: expected 0 unresolved, found "
                    f"{review.get(counter)!r}"
                )


# ======================================================================================
# Lane state machine — BLOCKING 2
# ======================================================================================


@dataclass(frozen=True)
class LanePaths:
    authorization: Path = AUTHORIZATION_PATH
    claim: Path = CLAIM_PATH
    completion: Path = COMPLETION_PATH
    ledger: Path = LEDGER_PATH


def _read_ledger(path: Path) -> list[Mapping[str, Any]]:
    if not path.exists():
        return []
    entries: list[Mapping[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line, object_pairs_hook=_reject_duplicate_keys)
        except (ValueError, json.JSONDecodeError):
            entries.append({"event": LEDGER_CORRUPT})
            continue
        # MINOR 1 (review 4946540894): a syntactically valid line that is not a mapping -- `[]`,
        # `"junk"`, `null`, `42` -- was SILENTLY DROPPED rather than treated as corruption, which
        # is weaker than the canonical promise that malformed entries fail closed. Every
        # non-empty line must decode to exactly one mapping or the ledger is corrupt.
        entries.append(entry if isinstance(entry, Mapping) else {"event": LEDGER_CORRUPT})
    return entries


def _append_ledger(path: Path, entry: Mapping[str, Any]) -> None:
    """Append-only. Losing claim.json alone therefore cannot reopen the lane."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(descriptor, "a", encoding="utf-8") as handle:
        handle.write(canonical_json(entry) + "\n")


def _load_authorization(path: Path) -> tuple[Mapping[str, Any] | None, str]:
    if not path.exists():
        return None, "no attestation present"
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"attestation unreadable: {exc}"
    try:
        document = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
    except (ValueError, json.JSONDecodeError) as exc:
        return None, f"attestation malformed: {exc}"
    if not isinstance(document, Mapping):
        return None, "attestation is not a mapping"
    return document, ""


def lane_state_at(
    paths: LanePaths, sources: TruthSources | None = None
) -> tuple[str, str]:
    """Return the lane state and, when not READY, why a new execution may not start.

    A claim recorded in EITHER ``claim.json`` OR the append-only ledger establishes CLAIMED,
    so losing one record alone does not reopen the lane. No attestation means ABSENT, which
    is not READY -- destroying the directory fails closed rather than resetting.
    """
    ledger = _read_ledger(paths.ledger)
    ledger_events = {str(entry.get("event")) for entry in ledger}

    if paths.completion.exists() or LANE_COMPLETED in ledger_events:
        return LANE_COMPLETED, (
            f"the single authorized attempt ({EXECUTION_ATTEMPT_ID}) has already completed; a "
            "second execution requires new governance authority"
        )
    if paths.claim.exists() or LANE_CLAIMED in ledger_events:
        return LANE_CLAIMED, (
            f"the single authorized attempt ({EXECUTION_ATTEMPT_ID}) is already claimed; a "
            "crash after claiming does not reopen the lane, and recovery is a governed act"
        )

    # MINOR 1 (review 4946706062): a ledger ALREADY KNOWN to be corrupt did not block
    # READY -> CLAIMED. `_read_ledger` marked the bad line and `_ledger_events` rejected it, but
    # that rejection was only ever consulted while RECOVERING claim/completion provenance -- here
    # a lone CORRUPT entry fell straight through to the attestation check. Reproduced before
    # correcting: with a valid attestation plus a pre-seeded `[]` ledger line, this returned
    # READY, `new_execution_is_authorized()` returned true, and `claim_execution()` wrote
    # claim.json and appended CLAIMED onto the corrupt ledger. Only the LATER
    # `claimed_execution_is_authorized()` noticed -- after the one authorized attempt had begun.
    #
    # Deliberately placed AFTER the CLAIMED/COMPLETED determination, not before: an already
    # claimed or completed lane is non-READY either way, and reordering would replace
    # `_authenticated_claim`'s precise corrupt-ledger error with a bare "lane state ABSENT",
    # weakening a message the mirror logic already gets right. The mirror rules, the
    # single-record-loss semantics, and the lane states themselves are untouched -- this only
    # refuses to call a lane READY when its provenance ledger is already unreadable.
    if LEDGER_CORRUPT in ledger_events:
        return LANE_ABSENT, (
            "the append-only ledger contains a corrupt entry, so this lane's provenance is "
            "already unreadable and no new execution may start in it. The single authorized "
            f"attempt ({EXECUTION_ATTEMPT_ID}) must not begin under invalid audit state; "
            "repairing the ledger is a governed act, not an automatic recovery"
        )

    document, problem = _load_authorization(paths.authorization)
    if document is None:
        return LANE_ABSENT, (
            f"{problem}. Structural closure of the construction universe is not authorization: "
            f"the {AUTHORIZING_DECISION} lifecycle must close in full "
            f"({', '.join(REQUIRED_LIFECYCLE_GATES)}) and an authenticated one-shot attestation "
            "must then be generated. There is no merge-to-execution gap"
        )
    result = validate_authorization_document(document, sources)
    if not result.valid:
        return LANE_ABSENT, "attestation invalid: " + "; ".join(result.errors)
    return LANE_READY, ""


def new_execution_is_authorized(
    paths: LanePaths | None = None, sources: TruthSources | None = None
) -> tuple[bool, str]:
    """May a NEW Stage-1 execution start? READY only. PUBLIC and fail-closed."""
    state, reason = lane_state_at(paths or LanePaths(), sources)
    return (state == LANE_READY), reason


def _ledger_events(paths: LanePaths, event: str) -> tuple[list[Mapping[str, Any]], str]:
    """Return the ledger's events of one kind, or an error if the ledger is unusable."""
    entries = _read_ledger(paths.ledger)
    if any(e.get("event") == LEDGER_CORRUPT for e in entries):
        return [], "the append-only ledger contains a corrupt entry"
    return [e for e in entries if e.get("event") == event], ""


def _recover_mirrored_record(
    paths: LanePaths, path: Path, event: str
) -> tuple[Mapping[str, Any] | None, str, str]:
    """Recover a lane record from its file and its ledger mirror, requiring them to AGREE.

    BLOCKING 1 (review 4946464366): the file was treated as authoritative whenever present and
    the ledger mirror was never consulted, so rewriting only ``completion.json`` retargeted the
    lawful run from result A to result B while the ledger still bound A. Reproduced before
    correcting. The two copies are a CONSISTENCY CHECK, not interchangeable alternatives:

      * both present  -> they must be the same canonical record, byte for byte;
      * file missing  -> recover only from exactly ONE unique uncorrupted ledger event;
      * ledger event missing but file present -> permitted, and ONLY this case, because it is
        exactly the single-record loss the disclosed durability model already covers;
      * conflicting, duplicated-different, malformed, or corrupt entries -> FAIL CLOSED.

    Returns ``(record, identity_sha256, error)``. The identity hash is the SHA-256 of the exact
    canonical bytes the file holds (or would hold), so it is identical whichever copy survives.
    """
    events, ledger_problem = _ledger_events(paths, event)
    distinct = {canonical_json(e) for e in events}

    file_record: Mapping[str, Any] | None = None
    if path.exists():
        file_record, problem = _load_authorization(path)
        if file_record is None:
            return None, "", f"{event.lower()} record unreadable: {problem}"

    if ledger_problem:
        # A corrupt ledger participates in provenance; it may never be silently ignored.
        return None, "", (
            f"{ledger_problem}; {event.lower()} provenance cannot be established"
        )

    # MINOR 1: canonical V5 says DUPLICATED entries fail closed, so the test is "at most one
    # event", not "one distinct value". Two byte-identical CLAIMED/COMPLETED events are still
    # duplicated provenance history and are refused.
    if len(events) > 1:
        identical = len(distinct) == 1
        shape = "identical duplicate" if identical else "conflicting"
        return None, "", (
            f"the ledger holds {len(events)} {event} events ({shape}); duplicated or conflicting "
            f"{event.lower()} provenance fails closed, and identical duplicates are refused too"
        )

    if file_record is not None and events:
        if len(distinct) != 1:
            return None, "", (
                f"the ledger holds conflicting {event} events; {event.lower()} provenance is "
                "ambiguous and fails closed"
            )
        if canonical_json(file_record) != next(iter(distinct)):
            return None, "", (
                f"the {event.lower()} record and its append-only ledger mirror disagree; the "
                "record has been altered after it was written"
            )
        return file_record, sha256_file(path), ""

    if file_record is not None:
        # Single-record loss: the ledger event is gone but the file survives.
        return file_record, sha256_file(path), ""

    if not events:
        return None, "", f"no {event.lower()} record and no ledger {event} entry exists"
    if len(distinct) != 1:
        return None, "", (
            f"the ledger holds conflicting {event} events; exact {event.lower()} identity cannot "
            "be recovered"
        )
    record = events[-1]
    return record, sha256_bytes((canonical_json(record) + "\n").encode("utf-8")), ""


def _recover_claim_record(paths: LanePaths) -> tuple[Mapping[str, Any] | None, str, str]:
    """Recover the canonical claim record and its exact identity hash, mirror-checked."""
    return _recover_mirrored_record(paths, paths.claim, LANE_CLAIMED)


def _recover_completion_record(paths: LanePaths) -> tuple[Mapping[str, Any] | None, str, str]:
    """Recover the canonical completion record and its exact identity hash, mirror-checked."""
    return _recover_mirrored_record(paths, paths.completion, LANE_COMPLETED)


def _authenticated_claim(
    paths: LanePaths, sources: TruthSources | None
) -> tuple[Mapping[str, Any] | None, str, str]:
    """Prove a CLAIMED/COMPLETED lane is LAWFUL, not merely present.

    BLOCKING 1 (review 4946397399): ``lane_state_at`` recognised claim/ledger state BEFORE
    loading the attestation, and this predicate then accepted any syntactically valid 64-hex
    ``authorization_sha256`` -- skipping the hash comparison entirely when the attestation file
    was absent. A local ``claim.json`` with the registered attempt id was therefore enough to
    make the PUBLIC result gate return authorized with no review, acceptance, merge, or CI ever
    consulted. Reproduced before correcting.

    State detection and authorization validity are different questions. The lane may report
    CLAIMED from a surviving record; lawful provenance additionally requires that the exact
    attestation still exists, still hashes to what the claim bound, and STILL passes full
    durable-truth validation -- so post-claim canonical, load-bearing, ancestry, or governance
    drift fails closed rather than being grandfathered in by an old claim.
    """
    record, claim_sha, problem = _recover_claim_record(paths)
    if record is None:
        return None, "", problem
    if record.get("execution_attempt_id") != EXECUTION_ATTEMPT_ID:
        return None, "", (
            f"claim names attempt {record.get('execution_attempt_id')!r}, not "
            f"{EXECUTION_ATTEMPT_ID!r}"
        )
    bound = record.get("authorization_sha256")
    if not _is_sha256(bound):
        return None, "", "claim does not bind an attestation hash"

    # The attestation must STILL exist. A surviving claim never substitutes for it.
    if not paths.authorization.exists():
        return None, "", (
            "the attestation this claim binds no longer exists; a claim record alone never "
            "establishes lawful authorization, so this fails closed"
        )
    actual = sha256_file(paths.authorization)
    if actual != bound:
        return None, "", (
            "the present attestation is not the one this claim bound; the claimed execution "
            "and the current authorization are not the same"
        )

    # ...and it must STILL authenticate against durable truth.
    document, load_problem = _load_authorization(paths.authorization)
    if document is None:
        return None, "", f"attestation unusable: {load_problem}"
    result = validate_authorization_document(document, sources)
    if not result.valid:
        return None, "", (
            "the attestation this claim binds no longer validates against durable truth: "
            + "; ".join(result.errors)
        )
    return record, claim_sha, ""


def claimed_execution_is_authorized(
    paths: LanePaths | None = None, sources: TruthSources | None = None
) -> tuple[bool, str]:
    """Did THIS execution come from the one LAWFUL, still-authenticated claim?

    A different question from "may a new execution start", and conflating them was the earlier
    BLOCKING 2. CLAIMED and COMPLETED both answer yes here -- but only after the attestation
    behind the claim is re-proved, never from claim-file existence alone.
    """
    paths = paths or LanePaths()
    state, _ = lane_state_at(paths, sources)
    if state not in (LANE_CLAIMED, LANE_COMPLETED):
        return False, (
            f"no lawfully claimed Stage-1 execution exists (lane state {state}); a results "
            "document may only be validated when it originates from the one claimed attempt"
        )
    record, _, problem = _authenticated_claim(paths, sources)
    if record is None:
        return False, problem
    return True, ""


def completed_result_is_authorized(
    results: Any, paths: LanePaths | None = None, sources: TruthSources | None = None
) -> tuple[bool, str]:
    """Is THIS EXACT results artifact the one the lawful execution completed?

    BLOCKING 2 (review 4946397399): completion recorded a result hash that nothing ever read,
    and the public validator never computed any identity for the document handed to it, so
    completing result A did not prevent publishing result B. Reproduced before correcting.

    Final publication therefore requires a COMPLETED record whose bound attempt, attestation,
    claim identity, and RESULT identity all match -- the last computed from the supplied
    artifact with :func:`stage1_result_identity`.
    """
    paths = paths or LanePaths()
    authorized, reason = claimed_execution_is_authorized(paths, sources)
    if not authorized:
        return False, reason

    completion, _, completion_problem = _recover_completion_record(paths)
    if completion is None:
        return False, (
            "the lawful execution has not been completed with a consistent, mirror-verified "
            f"record, so no exact result identity is bound and no result may be published "
            f"({completion_problem})"
        )

    claim, claim_sha, claim_problem = _recover_claim_record(paths)
    if claim is None:
        return False, claim_problem
    if completion.get("execution_attempt_id") != EXECUTION_ATTEMPT_ID:
        return False, (
            f"completion names attempt {completion.get('execution_attempt_id')!r}, not "
            f"{EXECUTION_ATTEMPT_ID!r}"
        )
    if completion.get("authorization_sha256") != claim.get("authorization_sha256"):
        return False, "completion binds a different attestation than the claim"
    if completion.get("claim_sha256") != claim_sha:
        return False, "completion binds a different claim than the one on record"

    expected = completion.get("result_identity_sha256")
    if not _is_sha256(expected):
        return False, "completion does not bind an exact result identity"
    supplied = stage1_result_identity(results)
    if supplied != expected:
        return False, (
            f"the supplied results artifact hashes to {supplied}, but the lawful execution "
            f"completed {expected}; a substituted or modified result may not be published"
        )
    return True, ""


def _write_once(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
    except BaseException:  # pragma: no cover - defensive
        try:
            path.unlink()
        except OSError:
            pass
        raise


def claim_execution(
    *,
    claimed_at_utc: str,
    paths: LanePaths | None = None,
    sources: TruthSources | None = None,
) -> Mapping[str, Any]:
    """Atomically claim the single authorized attempt IMMEDIATELY BEFORE the first real work.

    The claim is written with ``O_EXCL`` and mirrored into the append-only ledger, so a
    second claim always fails and losing one record alone does not reopen the lane. This is
    the neutral structural pattern the RISK runner also uses -- authorization is consumed at
    the first eligible work item, before computation -- with no RISK substance reused.
    """
    paths = paths or LanePaths()
    authorized, reason = new_execution_is_authorized(paths, sources)
    if not authorized:
        raise ValueError(f"refusing to claim a non-READY execution lane: {reason}")

    record = {
        "event": LANE_CLAIMED,
        "execution_attempt_id": EXECUTION_ATTEMPT_ID,
        "authorization_sha256": sha256_file(paths.authorization),
        "claimed_at_utc": claimed_at_utc,
    }
    # O_EXCL first: if a concurrent process already claimed, this raises and no ledger entry
    # is written, so the two records cannot disagree about who holds the lane.
    _write_once(paths.claim, canonical_json(record) + "\n")
    _append_ledger(paths.ledger, record)
    return record


def complete_execution(
    *,
    completed_at_utc: str,
    results: Any,
    paths: LanePaths | None = None,
    sources: TruthSources | None = None,
) -> Mapping[str, Any]:
    """Record completion, bound to the exact claim and the SEMANTIC identity of the real result.

    MAJOR 3 (review 4946464366): this previously accepted a caller-supplied
    ``result_identity_sha256``, so completion could bind any 64-hex digest rather than the
    artifact actually produced. It now takes the RESULT ITSELF and computes the identity
    internally with :func:`stage1_result_identity`, so the bound identity is derived, never
    chosen. There is deliberately no public completion API accepting a precomputed digest.
    """
    paths = paths or LanePaths()
    ok, reason = claimed_execution_is_authorized(paths, sources)
    if not ok:
        raise ValueError(f"refusing to complete an unclaimed execution: {reason}")
    result_identity_sha256 = stage1_result_identity(results)

    # BLOCKING 2: the previous form read the claim from paths.claim only, so completing after a
    # claim-file loss emitted authorization_sha256=None and claim_sha256=None -- directly
    # violating the canonical completion_binds contract. The exact identities are now recovered
    # (from the ledger when necessary) or the completion fails closed.
    claim, claim_sha, problem = _recover_claim_record(paths)
    if claim is None:
        raise ValueError(
            f"refusing to complete without a consistent, mirror-verified claim identity: {problem}"
        )
    bound_attestation = claim.get("authorization_sha256")
    if not _is_sha256(bound_attestation) or not _is_sha256(claim_sha):
        raise ValueError(
            "refusing to complete with a null or malformed attestation/claim identity"
        )
    record = {
        "event": LANE_COMPLETED,
        "execution_attempt_id": EXECUTION_ATTEMPT_ID,
        "authorization_sha256": bound_attestation,
        "claim_sha256": claim_sha,
        "result_identity_sha256": result_identity_sha256,
        "completed_at_utc": completed_at_utc,
    }
    _write_once(paths.completion, canonical_json(record) + "\n")
    _append_ledger(paths.ledger, record)
    return record


# ======================================================================================
# Arming
# ======================================================================================


def build_authorization_payload(
    *,
    authorization_head: str,
    lifecycle_evidence: Mapping[str, Any],
    author_identity: str,
    generated_at_utc: str,
    merge_sha: str,
) -> dict[str, Any]:
    """Assemble an attestation from live repository facts.

    Canonical pins, universe identity, predecessor identity, and load-bearing byte identity
    are all recomputed here rather than accepted from a caller. The lifecycle block is still
    supplied by the operator, but supplying it proves nothing: every field is re-derived and
    compared against durable truth at validation time.
    """
    universe = live_construction_universe_facts()
    git = LiveGitTruthSource()
    load_bearing = {
        relative: (git.blob_sha256_at(merge_sha, relative) or sha256_file(ROOT / relative))
        for relative in sorted(LOAD_BEARING_RELPATHS)
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "mechanism": AUTHORIZATION_MECHANISM,
        "repository": REPOSITORY_IDENTITY,
        "study_id": STUDY_ID,
        "authorizing_decision": AUTHORIZING_DECISION,
        "authorizing_pull_request": AUTHORIZING_PULL_REQUEST,
        "predecessor_decision": PREDECESSOR_DECISION,
        "execution_attempt_id": EXECUTION_ATTEMPT_ID,
        "authorization_head": authorization_head,
        "predecessor_identity": {
            "merge_sha": PREDECESSOR_MERGE_SHA,
            "accepted_head": PREDECESSOR_ACCEPTED_HEAD,
            "merge_base": PREDECESSOR_MERGE_BASE,
        },
        "canonical_pins": live_canonical_hashes(),
        "construction_universe": {
            "sha256": universe["sha256"],
            "count": universe["count"],
            "cell_count": universe["cell_count"],
        },
        "lifecycle_evidence": dict(lifecycle_evidence),
        "load_bearing_identity": load_bearing,
        "author_identity": author_identity,
        "generated_at_utc": generated_at_utc,
    }


def write_authorization(
    payload: Mapping[str, Any],
    authorization_path: Path = AUTHORIZATION_PATH,
    sources: TruthSources | None = None,
) -> None:
    """Validate against durable truth, then persist once. Invalid bytes never reach disk."""
    result = validate_authorization_document(payload, sources)
    if not result.valid:
        raise ValueError(
            "refusing to write an invalid Stage-1 authorization attestation: "
            + "; ".join(result.errors)
        )
    _write_once(authorization_path, canonical_json(payload) + "\n")


def main(argv: Sequence[str] | None = None) -> int:  # pragma: no cover - CLI
    state, reason = lane_state_at(LanePaths())
    print(f"study: {STUDY_ID}")
    print(f"attempt: {EXECUTION_ATTEMPT_ID}")
    print(f"mechanism: {AUTHORIZATION_MECHANISM}")
    print(f"lane state: {state}")
    print(f"new execution authorized: {state == LANE_READY}")
    if reason:
        print(f"reason: {reason}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())
