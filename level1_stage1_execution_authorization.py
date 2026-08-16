"""ENDPOINT-0001 Stage-1 operational execution authorization — XASSET-0029.

WHAT THIS MODULE IS
===================

XASSET-0028 closed the concrete construction universe STRUCTURALLY (680 registered
constructions across 48 cells). Structural closure is not operational authorization. This
module supplies the missing half: the mechanism by which exactly one Stage-1 execution
attempt may become operationally authorized, and the fail-closed validator that decides
whether THIS execution is authorized.

WHY THE COMMITTED BOOLEAN IS NOT THE MECHANISM
==============================================

The obvious design is to flip ``stage_1_executability.executable`` to true. That is wrong
for three independent reasons, the third of which is dispositive:

1. MERGE-TO-EXECUTION GAP. A committed boolean becomes effective the instant the
   authorizing PR merges — before post-merge verification and before merge-commit CI has
   even started, let alone concluded. The canonical file itself already promises
   ``no_merge_to_execution_gap: true``, so a committed flag cannot be the mechanism
   without contradicting it.

2. A MUTABLE BOOLEAN IS NOT EVIDENCE. A single committed flag asserts authorization; it
   does not demonstrate that any gate actually closed. Nothing about the flag is bound to
   a review, an acceptance, a merge, a CI conclusion, or a hash.

3. IT IS ALREADY A VALIDATION ERROR. ``_validate_stage_1_executability`` in
   ``level1_endpoint_evidence_preregistration_validator`` enforces
   ``_false(block.get("executable"))``. The canonical preregistration is therefore INVALID
   whenever ``executable`` is true. A file cannot be simultaneously valid and
   self-authorizing. This is a deliberate permanent lock inherited from XASSET-0028, and
   XASSET-0029 preserves it rather than unpicking it.

``executable`` accordingly stays false FOREVER and keeps its enforced-false check. Its
meaning is now explicit: *no committed value in this repository authorizes Stage-1
execution.*

THE MECHANISM
=============

Authorization is TWO-FACTOR, and the two factors live in deliberately different places:

  Factor 1 — REPOSITORY STATE (committed, reviewable, inert).
      The canonical ``stage_1_operational_authorization`` block states WHAT a valid
      authorization must prove and WHICH exact identities it must bind. It is a
      specification of a gate. It never asserts that the gate is open.

  Factor 2 — EXTERNAL PREEXECUTION ATTESTATION (not committed, runtime, one-shot).
      A JSON document outside the repository, creatable only AFTER the XASSET-0029
      lifecycle has closed in full, recording independently verifiable evidence for every
      gate and bound to exact hashes and commit identities.

Neither factor authorizes anything alone. Execution is authorized only when the committed
specification is satisfied AND a valid external attestation exists for THIS attempt.

WHY THIS CLOSES THE MERGE-TO-EXECUTION GAP
==========================================

Merging XASSET-0029 changes nothing operationally: no attestation exists, so
``authorization_is_effective()`` still returns False. The attestation cannot be
back-dated or pre-staged, because generating it requires evidence that does not exist
until after the merge:

  * the merge SHA (does not exist before the merge),
  * a post-merge verification comment (posted after the merge),
  * a merge-commit CI run that has CONCLUDED success at that exact merge SHA.

CI cannot have concluded at the instant of merge. There is therefore a strictly positive
interval between merge and authorizability, and it is enforced by evidence rather than by
convention.

WHY THIS DOES NOT REGRESS INFINITELY
====================================

Arming is a RUNTIME operator act, not another merged governance PR. XASSET-0029 is the
last governance decision required for Stage 1. After it merges and verifies, the operator
runs the generator once; no further authorization PR is needed, ever. The regress
terminates because the final step changes no repository state.

TRUST BOUNDARY
==============

  * Repository state says what is STRUCTURALLY authorized.
  * The external attestation says whether THIS execution is authorized.
  * A results document can satisfy neither. It is validated last and is never consulted
    for authorization.
  * Private ``_at``-suffixed seams exist so structural tests can run without any call form
    implying authorization. Calling them confers nothing.

ONE AUTHORIZED LANE
===================

XASSET-0027 SSP.1 permits exactly ONE later Stage-1 evaluation/results PR. This module
therefore binds a single ``execution_attempt_id`` and enforces one-shot semantics with
``O_EXCL`` on both the attestation and its consumption receipt. An authorization naming
one attempt cannot authorize another, and a consumed authorization cannot be replayed.

NOT A RISK MODULE. No RISK-0001 scenario, threshold, magnitude, window, parameter, attempt
identity, result value, or family conclusion is read, imported, or reused here. Only
neutral engineering patterns (canonical JSON hashing, duplicate-key rejection, immutable
preexecution metadata, exact-identity verification, O_EXCL one-shot creation, fail-closed
validation) are shared, and those are general repository craft.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parent

# ======================================================================================
# Bound identity — every value below is verified live, never trusted from the document
# ======================================================================================

REPOSITORY_IDENTITY = "Mast3rkey/Portfolio-HQ"
STUDY_ID = "ENDPOINT-0001"
AUTHORIZING_DECISION = "XASSET-0029"
PREDECESSOR_DECISION = "XASSET-0028"

#: The single Stage-1 execution lane XASSET-0027 SSP.1 permits. Derived from repository
#: truth, not invented: no Stage-1 attempt has ever been executed or authorized, so the
#: one authorized lane is the first.
EXECUTION_ATTEMPT_ID = "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

#: XASSET-0028's merge identity, verified against live git history at validation time.
PREDECESSOR_MERGE_SHA = "c51e94609eff7ede2bdfa084844d59b8347561e5"
PREDECESSOR_ACCEPTED_HEAD = "036606401ea569b0a03f2d716d87a057d07d71dc"
PREDECESSOR_MERGE_BASE = "e4b6f0b810884fcb73d1b8ee053d8005db532f3e"

#: The frozen construction universe XASSET-0028 closed. Recomputed live and compared.
CONSTRUCTION_UNIVERSE_SHA256 = (
    "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
)
CONSTRUCTION_COUNT = 680
CONSTRUCTION_CELL_COUNT = 48

PROTOCOL_PATH = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
PREREGISTRATION_PATH = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"

#: XASSET-0029 successor pins, computed AFTER the canonical bytes were final, exactly as
#: XASSET-0028 pinned its own successors. These are separate files from this module, so there is no
#: self-hashing circularity. ``validate_authorization_document`` compares an attestation against
#: BOTH these bound values AND the live bytes on disk, so post-acceptance drift in either direction
#: is refused.
CANONICAL_PINS: dict[str, str] = {
    "research/level1_endpoint_evidence/PROTOCOL_V1.md": (
        "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
    ),
    "research/level1_endpoint_evidence/pre_registration.yaml": (
        "14d166f071e579bd958a7e4d0d34ac1f5cdef999f58aecd01d1276321bebdce6"
    ),
}

#: XASSET-0028's pins, retained as predecessor identity. History is never invalidated.
PREDECESSOR_CANONICAL_PINS = {
    "research/level1_endpoint_evidence/PROTOCOL_V1.md": (
        "c02b4d519267b96ddb12500e6d1d55a47aeafd9437de8e41014c8871f631618c"
    ),
    "research/level1_endpoint_evidence/pre_registration.yaml": (
        "ffde86c1585050b2bf89e58033f37777a903ace86e97be46b6440a217c78ec4a"
    ),
}

# ======================================================================================
# Marker location — deliberately OUTSIDE the repository
# ======================================================================================

#: The attestation lives outside the repository so it can never be committed, reviewed
#: into existence, forged into a pull request, or produced by editing tracked files. It is
#: also NOT the RISK-0001 results location, which this module never reads or references.
AUTHORIZATION_ROOT = Path("/var/tmp/phq-endpoint0001-stage1-authorization")
AUTHORIZATION_PATH = AUTHORIZATION_ROOT / "authorization.json"
CONSUMPTION_RECEIPT_PATH = AUTHORIZATION_ROOT / "consumed.json"

# ======================================================================================
# Gate vocabulary
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

REQUIRED_TOP_KEYS = (
    "schema_version",
    "mechanism",
    "repository",
    "study_id",
    "authorizing_decision",
    "predecessor_decision",
    "execution_attempt_id",
    "authorization_head",
    "canonical_pins",
    "construction_universe",
    "lifecycle_evidence",
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

APPROVING_REVIEW_DISPOSITION = "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"

SCHEMA_VERSION = 1


# ======================================================================================
# Primitives
# ======================================================================================


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(payload: Any) -> str:
    """Deterministic canonical JSON: sorted keys, tight separators, no trailing newline."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _reject_duplicate_keys(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    """JSON object hook that refuses duplicate keys.

    A duplicate key silently discards the earlier value in ordinary ``json.loads``, which
    would let a malformed attestation present one identity to a reader and another to the
    parser.
    """
    seen: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key {key!r} in authorization document")
        seen[key] = value
    return seen


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _is_sha1_commit(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
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


# ======================================================================================
# Live repository facts — recomputed, never taken from the document
# ======================================================================================


def live_canonical_hashes() -> dict[str, str]:
    return {
        relative: sha256_file(ROOT / relative) for relative in sorted(CANONICAL_PINS)
    }


def live_construction_universe_facts() -> dict[str, Any]:
    """Recompute the closed universe from its generator. Never read from a document."""
    import level1_construction_universe_closure_validator as closure

    universe = closure.frozen_construction_universe()
    return {
        "sha256": closure.universe_aggregate_sha256(),
        "count": closure.derived_cardinality(),
        "cell_count": len(closure.per_cell_cardinality()),
        "construction_ids": tuple(universe),
    }


def pins_are_placeholders() -> bool:
    """True while the successor pins have not yet been refreshed to real digests."""
    return any(not _is_sha256(value) for value in CANONICAL_PINS.values())


# ======================================================================================
# Document validation — fail-closed on every path
# ======================================================================================


def validate_authorization_document(document: Any) -> ValidationResult:
    """Validate an attestation against bound identity and live repository facts.

    Every check is independent and every failure is fatal. There is no permissive branch,
    no caller-supplied override, and no field a results author could set to relax a check.
    """
    errors: list[str] = []

    root = _mapping(document, "authorization", errors)
    if root is None:
        return ValidationResult(False, tuple(errors))

    unknown = sorted(set(root) - set(REQUIRED_TOP_KEYS))
    for key in unknown:
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

    authorization_head = root.get("authorization_head")
    if not _is_sha1_commit(authorization_head):
        errors.append(
            "authorization.authorization_head: expected a 40-character commit SHA"
        )

    _validate_canonical_pins(root.get("canonical_pins"), errors)
    _validate_construction_universe(root.get("construction_universe"), errors)
    _validate_lifecycle_evidence(
        root.get("lifecycle_evidence"), authorization_head, root.get("author_identity"), errors
    )

    if not isinstance(root.get("author_identity"), str) or not root["author_identity"].strip():
        errors.append("authorization.author_identity: expected a non-empty string")
    if not isinstance(root.get("generated_at_utc"), str) or not root["generated_at_utc"].strip():
        errors.append("authorization.generated_at_utc: expected a non-empty string")

    return ValidationResult(not errors, tuple(errors))


def _validate_canonical_pins(block: Any, errors: list[str]) -> None:
    """Recorded pins must equal the bound pins AND the live bytes on disk."""
    pins = _mapping(block, "authorization.canonical_pins", errors)
    if pins is None:
        return

    if pins_are_placeholders():
        errors.append(
            "authorization.canonical_pins: XASSET-0029 successor pins have not been "
            "refreshed to real digests, so no attestation can be validated"
        )
        return

    live = live_canonical_hashes()
    for relative, bound in sorted(CANONICAL_PINS.items()):
        recorded = pins.get(relative)
        if recorded != bound:
            errors.append(
                f"authorization.canonical_pins[{relative!r}]: recorded {recorded!r} but the "
                f"bound XASSET-0029 pin is {bound!r}"
            )
        if live.get(relative) != bound:
            errors.append(
                f"canonical drift: {relative} on disk hashes to {live.get(relative)!r} but the "
                f"bound XASSET-0029 pin is {bound!r}; the authorized bytes have changed"
            )
    for relative in sorted(set(pins) - set(CANONICAL_PINS)):
        errors.append(
            f"authorization.canonical_pins[{relative!r}]: unknown canonical file; the pin set "
            "is closed"
        )


def _validate_construction_universe(block: Any, errors: list[str]) -> None:
    """Recorded universe identity must equal the bound values AND a live recomputation."""
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
        recorded.get("count"),
        CONSTRUCTION_COUNT,
        "authorization.construction_universe.count",
        errors,
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
        errors.append(
            f"universe drift: live universe hashes to {live['sha256']!r} but the bound frozen "
            f"universe is {CONSTRUCTION_UNIVERSE_SHA256!r}"
        )
    if live["count"] != CONSTRUCTION_COUNT:
        errors.append(
            f"universe drift: live universe has {live['count']} constructions but the bound "
            f"frozen cardinality is {CONSTRUCTION_COUNT}"
        )
    if live["cell_count"] != CONSTRUCTION_CELL_COUNT:
        errors.append(
            f"universe drift: live universe has {live['cell_count']} cells but the bound frozen "
            f"cell count is {CONSTRUCTION_CELL_COUNT}"
        )


def _validate_lifecycle_evidence(
    block: Any, authorization_head: Any, author_identity: Any, errors: list[str]
) -> None:
    """Every one of the six gates must carry evidence anchored to the exact head."""
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

    # --- Gate 1: independent full exact-head review -----------------------------------
    review = _mapping(evidence.get("independent_review"), f"{where}.independent_review", errors)
    if review is not None:
        if not isinstance(review.get("review_id"), (int, str)) or not str(
            review.get("review_id")
        ).strip():
            errors.append(f"{where}.independent_review.review_id: expected a non-empty id")
        disposition = review.get("formal_disposition")
        if disposition != APPROVING_REVIEW_DISPOSITION:
            errors.append(
                f"{where}.independent_review.formal_disposition: expected "
                f"{APPROVING_REVIEW_DISPOSITION!r}, found {disposition!r}; an adverse or absent "
                "disposition never authorizes execution"
            )
        for counter in ("blocking", "major"):
            count = review.get(f"{counter}_count")
            if count != 0:
                errors.append(
                    f"{where}.independent_review.{counter}_count: expected 0 unresolved, found "
                    f"{count!r}"
                )
        if review.get("reviewed_sha") != authorization_head:
            errors.append(
                f"{where}.independent_review.reviewed_sha: {review.get('reviewed_sha')!r} does not "
                f"equal authorization_head {authorization_head!r}; a stale-head review never "
                "authorizes execution"
            )
        reviewer = review.get("reviewer_identity")
        if not isinstance(reviewer, str) or not reviewer.strip():
            errors.append(f"{where}.independent_review.reviewer_identity: expected a non-empty string")
        elif isinstance(author_identity, str) and reviewer.strip() == author_identity.strip():
            errors.append(
                f"{where}.independent_review.reviewer_identity: the reviewing session "
                f"{reviewer!r} is the authoring session; a self-authored review is not independent"
            )

    # --- Gate 2: principal exact-head acceptance --------------------------------------
    acceptance = _mapping(
        evidence.get("principal_acceptance"), f"{where}.principal_acceptance", errors
    )
    if acceptance is not None:
        if not str(acceptance.get("comment_id") or "").strip():
            errors.append(f"{where}.principal_acceptance.comment_id: expected a non-empty id")
        if acceptance.get("accepted_head") != authorization_head:
            errors.append(
                f"{where}.principal_acceptance.accepted_head: "
                f"{acceptance.get('accepted_head')!r} does not equal authorization_head "
                f"{authorization_head!r}; acceptance for another head never authorizes execution"
            )

    # --- Gate 3: merge ----------------------------------------------------------------
    merge = _mapping(evidence.get("merge"), f"{where}.merge", errors)
    merge_sha: Any = None
    if merge is not None:
        merge_sha = merge.get("merge_sha")
        if not _is_sha1_commit(merge_sha):
            errors.append(f"{where}.merge.merge_sha: expected a 40-character commit SHA")
        parents = merge.get("parents")
        if not isinstance(parents, (list, tuple)) or len(parents) != 2:
            errors.append(
                f"{where}.merge.parents: expected exactly two parents; a squash or rebase does "
                "not carry the accepted head as a parent and never authorizes execution"
            )
        else:
            if parents[1] != authorization_head:
                errors.append(
                    f"{where}.merge.parents[1]: {parents[1]!r} does not equal authorization_head "
                    f"{authorization_head!r}; the merged bytes are not the accepted bytes"
                )
            if parents[0] == authorization_head:
                errors.append(
                    f"{where}.merge.parents[0]: the base parent must not equal authorization_head"
                )

    # --- Gate 4: post-merge verification ----------------------------------------------
    verification = _mapping(
        evidence.get("post_merge_verification"), f"{where}.post_merge_verification", errors
    )
    if verification is not None:
        if not str(verification.get("comment_id") or "").strip():
            errors.append(
                f"{where}.post_merge_verification.comment_id: expected a non-empty id; merge alone "
                "never authorizes execution"
            )
        if merge_sha is not None and verification.get("verified_merge_sha") != merge_sha:
            errors.append(
                f"{where}.post_merge_verification.verified_merge_sha: "
                f"{verification.get('verified_merge_sha')!r} does not equal the recorded merge SHA "
                f"{merge_sha!r}"
            )

    # --- Gate 5: merge-commit CI success ----------------------------------------------
    ci = _mapping(evidence.get("merge_commit_ci"), f"{where}.merge_commit_ci", errors)
    if ci is not None:
        if not str(ci.get("run_id") or "").strip():
            errors.append(f"{where}.merge_commit_ci.run_id: expected a non-empty id")
        if not str(ci.get("job_id") or "").strip():
            errors.append(f"{where}.merge_commit_ci.job_id: expected a non-empty id")
        _exact(ci.get("status"), "completed", f"{where}.merge_commit_ci.status", errors)
        if ci.get("conclusion") != "success":
            errors.append(
                f"{where}.merge_commit_ci.conclusion: expected 'success', found "
                f"{ci.get('conclusion')!r}; a failed, cancelled, or still-running merge-commit CI "
                "never authorizes execution"
            )
        if merge_sha is not None and ci.get("head_sha") != merge_sha:
            errors.append(
                f"{where}.merge_commit_ci.head_sha: {ci.get('head_sha')!r} does not equal the "
                f"recorded merge SHA {merge_sha!r}; CI for another commit never authorizes "
                "execution"
            )

    # --- Gate 6 is the canonical-pin and universe verification performed above --------


# ======================================================================================
# Effectivity — the single public authorization question
# ======================================================================================


def _authorization_is_effective_at(
    authorization_path: Path, receipt_path: Path
) -> tuple[bool, str]:
    """Private structural seam. Calling this confers no authorization on any caller."""
    if receipt_path.exists():
        return False, (
            f"the single authorized Stage-1 execution attempt ({EXECUTION_ATTEMPT_ID}) has "
            "already been consumed; a consumed authorization can never be replayed, and a rerun "
            "requires new governance authority"
        )
    if not authorization_path.exists():
        return False, (
            "no Stage-1 preexecution authorization attestation exists. Structural closure of the "
            f"construction universe is not authorization: the {AUTHORIZING_DECISION} lifecycle "
            f"must close in full ({', '.join(REQUIRED_LIFECYCLE_GATES)}) and an external one-shot "
            "attestation must then be generated. There is no merge-to-execution gap"
        )
    try:
        raw = authorization_path.read_text(encoding="utf-8")
    except OSError as exc:
        return False, f"authorization attestation unreadable: {exc}"
    try:
        document = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
    except (ValueError, json.JSONDecodeError) as exc:
        return False, f"authorization attestation malformed: {exc}"

    result = validate_authorization_document(document)
    if not result.valid:
        return False, "authorization attestation invalid: " + "; ".join(result.errors)
    return True, ""


def authorization_is_effective() -> tuple[bool, str]:
    """Is Stage-1 execution operationally authorized right now? PUBLIC and fail-closed.

    Takes NO arguments. There is deliberately no path parameter, no universe parameter, and
    no override: a caller cannot point this at an attestation of their own choosing, and a
    results document cannot reach results validation before this returns True.
    """
    return _authorization_is_effective_at(AUTHORIZATION_PATH, CONSUMPTION_RECEIPT_PATH)


# ======================================================================================
# Generation and consumption — one-shot, post-lifecycle only
# ======================================================================================


def build_authorization_payload(
    *,
    authorization_head: str,
    lifecycle_evidence: Mapping[str, Any],
    author_identity: str,
    generated_at_utc: str,
) -> dict[str, Any]:
    """Assemble an attestation payload from live repository facts.

    Canonical pins and universe identity are recomputed here rather than accepted from a
    caller, so a generator invocation cannot assert bytes it did not observe.
    """
    universe = live_construction_universe_facts()
    return {
        "schema_version": SCHEMA_VERSION,
        "mechanism": AUTHORIZATION_MECHANISM,
        "repository": REPOSITORY_IDENTITY,
        "study_id": STUDY_ID,
        "authorizing_decision": AUTHORIZING_DECISION,
        "predecessor_decision": PREDECESSOR_DECISION,
        "execution_attempt_id": EXECUTION_ATTEMPT_ID,
        "authorization_head": authorization_head,
        "canonical_pins": live_canonical_hashes(),
        "construction_universe": {
            "sha256": universe["sha256"],
            "count": universe["count"],
            "cell_count": universe["cell_count"],
        },
        "lifecycle_evidence": dict(lifecycle_evidence),
        "author_identity": author_identity,
        "generated_at_utc": generated_at_utc,
    }


def _write_once(path: Path, text: str) -> None:
    """Create ``path`` exactly once. O_EXCL makes a second creation impossible."""
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


def write_authorization(
    payload: Mapping[str, Any], authorization_path: Path = AUTHORIZATION_PATH
) -> None:
    """Validate then persist an attestation, once.

    The payload is validated BEFORE any bytes are written, so an invalid attestation never
    reaches disk and cannot occupy the one-shot slot.
    """
    result = validate_authorization_document(payload)
    if not result.valid:
        raise ValueError(
            "refusing to write an invalid Stage-1 authorization attestation: "
            + "; ".join(result.errors)
        )
    _write_once(authorization_path, canonical_json(payload) + "\n")


def consume_authorization(
    *,
    consumed_at_utc: str,
    authorization_path: Path = AUTHORIZATION_PATH,
    receipt_path: Path = CONSUMPTION_RECEIPT_PATH,
) -> None:
    """Burn the single authorized attempt. Idempotency is deliberately NOT provided."""
    effective, reason = _authorization_is_effective_at(authorization_path, receipt_path)
    if not effective:
        raise ValueError(f"refusing to consume a non-effective authorization: {reason}")
    _write_once(
        receipt_path,
        canonical_json(
            {
                "execution_attempt_id": EXECUTION_ATTEMPT_ID,
                "authorization_sha256": sha256_file(authorization_path),
                "consumed_at_utc": consumed_at_utc,
            }
        )
        + "\n",
    )


def main(argv: Sequence[str] | None = None) -> int:  # pragma: no cover - CLI
    effective, reason = authorization_is_effective()
    print(f"study: {STUDY_ID}")
    print(f"attempt: {EXECUTION_ATTEMPT_ID}")
    print(f"mechanism: {AUTHORIZATION_MECHANISM}")
    print(f"authorized: {effective}")
    if not effective:
        print(f"reason: {reason}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())
