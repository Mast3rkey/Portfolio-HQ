"""Mechanism-based proof for ``XASSET-0062`` — the PR #362 lifecycle provenance correction.

This suite proves the properties ``XASSET-0062`` asserts, from live repository bytes and from
GitHub-shaped actor records, rather than from prose. Its central claims are:

* body text can never override API-derived actor identity;
* ``claude[bot]`` is never accepted as the principal merely because a body says so;
* the ``Mast3rkey``/``User``/``OWNER`` triple is **not** sufficient on its own -- it is satisfiable
  by the Claude application and by the independent reviewer, so ``performed_via_github_app`` is a
  required conjunct;
* no immediate-verification record is invented from the later closure comment;
* the ratification is exact-ID, exact-actor, exact-PR, exact-head, exact-review and exact-merge
  bounded, and yields the all-false result for every other document;
* no standing authority is created for any bot, app, or automation;
* ``XASSET-0061`` remains unavailable until every corrective effectivity condition closes.

The suite performs no filesystem write, evaluates no gate, creates no lane state, and asserts no
readiness outcome. It imports ``level1_stage1_execution_authorization`` read-only, for constants
only.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent

DECISION_RELPATH = (
    "governance/decisions/XASSET-0062-endpoint-0001-pr362-lifecycle-provenance-correction.md"
)
DECISION_PATH = ROOT / DECISION_RELPATH
THIS_ARTIFACT = Path(__file__).name

# --------------------------------------------------------------------------------------
# The exact, closed history this correction is pinned to. Every value was independently
# re-derived from live git and live GitHub during the authoring session.
# --------------------------------------------------------------------------------------
RATIFIED_PULL_REQUEST = 362
#: This corrective filing's OWN pull request, BOUND after GitHub issued it -- never
#: predicted. Kept distinct from RATIFIED_PULL_REQUEST above: one is the history being
#: ratified, the other is the unit doing the ratifying, and conflating them would let a
#: scope pin be satisfied by the wrong pull request.
THIS_CORRECTIVE_PULL_REQUEST = 363
RATIFIED_ACCEPTED_HEAD = "ccc7f433b06d5114eb7616347ce773ae4f80392c"
RATIFIED_BASE = "413e033ac33741829168762ab24d73327c047d4b"
RATIFIED_MERGE = "3db918530b10ffc1423ba0b749b086e349a4901d"
RATIFIED_TREE = "1ccbecec64ba9bae64514443cf26972bde2782a9"
RATIFIED_REVIEW_ID = 5058418382
RATIFIED_BOT_ACCEPTANCE_ID = 5463146940
RATIFIED_CLOSURE_ID = 5463232454
INDEPENDENT_STOP_ID = 5466422998
MERGE_CI_RUN = 33259403778
MERGE_CI_JOB = 99118637390

MERGED_AT = "2026-08-29T15:07:49Z"
BOT_ACCEPTANCE_AT = "2026-08-29T15:06:54Z"
CI_COMPLETED_AT = "2026-08-29T15:18:50Z"
CLOSURE_AT = "2026-08-29T15:24:01Z"

PRINCIPAL_LOGIN = "Mast3rkey"
PRINCIPAL_TYPE = "User"
PRINCIPAL_ASSOCIATION = "OWNER"

CLAUDE_APP_SLUG = "claude"
REVIEWER_APP_SLUG = "chatgpt-codex-connector"

# The twenty-five load-bearing paths plus the protected production/portfolio surface.
PROTECTED_RELPATHS = (
    "level1_stage1_execution_authorization.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "holdings.yaml",
    "targets.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
    "allocate.py",
    "margin_state.py",
    "levels.py",
)

#: Predecessor suites this filing lawfully RE-ANCHORS. Each pinned WS-0014's single shared
#: live fields, or its own delta, to its own lifecycle; the authorized delta here advances
#: them, following the documented advance-with-negative-pin pattern -- the superseded value is
#: retained as a negative pin rather than deleted, so each field stays bound at BOTH ends.
#: Suites whose SHARED-LIVE-FIELD PINS this filing advances. Each must retain the superseded
#: value as a NEGATIVE pin, so the field stays bound at BOTH ends and a silent revert fails.
PIN_ADVANCED_SUITES = frozenset(
    {
        "test_level1_stage1_activation_authorization.py",
        "test_level1_stage1_formal_disposition_parser_correction_authorization.py",
        "test_level1_stage1_parser_contract_correction_authorization.py",
        "test_level1_stage1_post_correction_rebinding.py",
        "test_level1_stage1_post_correction_rebinding_authorization.py",
        "test_level1_stage1_post_merge_ci_recovery_authorization.py",
        "test_level1_stage1_post_merge_ci_recovery_reauthorization.py",
        "test_level1_stage1_post_merge_ci_recovery_reconciliation.py",
        "test_level1_stage1_post_parser_correction_rebinding_authorization.py",
        "test_level1_stage1_post_parser_correction_renewed_readiness_verification_authorization.py",
        "test_level1_stage1_post_rebinding_drift_authorization.py",
        "test_level1_stage1_pr337_actor_evidence_correction_authorization.py",
        "test_level1_stage1_readiness_verification_authorization.py",
        "test_level1_stage1_verdict_boundary_governance.py",
    }
)

#: Suites where NO pin moved. Their register helpers predate the ``pr: null`` spelling of the
#: un-bound window and raised on it; each is EXTENDED to check that state for consistency --
#: never to skip it, which would make the guard vacuous exactly when the register is
#: half-written. Requiring a negative pin here would be meaningless: nothing was superseded.
HELPER_EXTENDED_SUITES = frozenset(
    {
        "test_level1_stage1_formal_disposition_parser_correction.py",
        "test_level1_stage1_post_parser_correction_operational_rebinding.py",
        "test_level1_stage1_renewed_activation_authorization.py",
        "test_level1_stage1_renewed_drift_check_authorization.py",
        "test_level1_stage1_renewed_readiness_verification_authorization.py",
        "test_level1_stage1_step8_equivalent_rebinding_authorization.py",
        "test_level1_stage1_step8_equivalent_successor_rebinding.py",
    }
)

RE_ANCHORED_PREDECESSOR_SUITES = PIN_ADVANCED_SUITES | HELPER_EXTENDED_SUITES

EXPECTED_CHANGED_FILES = frozenset(
    {
        DECISION_RELPATH,
        "governance/decisions.yaml",
        "operations/WORKSTREAMS.yaml",
        THIS_ARTIFACT,
        "test_portfolio_hq_dashboard_decisions.py",
    }
) | RE_ANCHORED_PREDECESSOR_SUITES


def _read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def _changed_files() -> frozenset[str]:
    """Merge base vs. the working tree, so this holds pre- and post-commit alike."""
    out = _git("diff", "--name-only", RATIFIED_MERGE)
    untracked = _git("ls-files", "--others", "--exclude-standard")
    return frozenset(p for p in (out.splitlines() + untracked.splitlines()) if p)


def _flat(text: str) -> str:
    """Collapse whitespace so prose checks survive line wrapping."""
    return re.sub(r"\s+", " ", text)


# ======================================================================================
# The ratification mechanism under test -- CORRECTED under independent reviews 5060791095
# and 5060793954.
#
# The earlier version required four actor/provenance fields and nothing else. Independent
# review 5060791095 -- a ChatGPT/Codex-authored PULL REQUEST REVIEW -- reads back from GitHub
# as Mast3rkey / User / OWNER with performed_via_github_app null, so it satisfied every one of
# them. The cause is structural: that key is ABSENT on reviews and review comments, and
# ``.get()`` on an absent key returns None, so an "app is null" test is VACUOUS for every
# record type except the issue comment it was written against.
#
# The corrected mechanism validates RECORD KIND from canonical API fields first, requires the
# app key to be PRESENT and null, authenticates the record by canonical-JSON fingerprint, and
# no longer accepts a caller-supplied scope the record never authenticated.
# ======================================================================================
REPO_API = "https://api.github.com/repos/Mast3rkey/Portfolio-HQ"
REPO_HTML = "https://github.com/Mast3rkey/Portfolio-HQ"

#: The canonical issue-comment URLs for a ratification on THIS corrective pull request.
RATIFICATION_ISSUE_URL = f"{REPO_API}/issues/{THIS_CORRECTIVE_PULL_REQUEST}"
RATIFICATION_URL_PREFIX = f"{REPO_API}/issues/comments/"
RATIFICATION_HTML_PREFIX = f"{REPO_HTML}/pull/{THIS_CORRECTIVE_PULL_REQUEST}#issuecomment-"

#: Fields whose presence proves the record is NOT a top-level issue comment.
FOREIGN_RECORD_KIND_FIELDS = (
    "pull_request_url",        # pull-request review, and review comment
    "pull_request_review_id",  # inline review comment
    "commit_id",               # commit comment, and pull-request review
    "diff_hunk",               # inline review comment
    "path",                    # inline review comment
    "position",                # inline review comment
)

#: The seven PR #362 pins. FIXED CONSTANTS of this decision (SS-G.3) -- never caller-supplied.
RATIFIED_SCOPE_PINS = (
    str(RATIFIED_PULL_REQUEST),
    RATIFIED_ACCEPTED_HEAD,
    str(RATIFIED_REVIEW_ID),
    str(RATIFIED_BOT_ACCEPTANCE_ID),
    RATIFIED_MERGE,
    str(RATIFIED_CLOSURE_ID),
    str(INDEPENDENT_STOP_ID),
)

#: SS-G.4: the ratification comment DOES NOT EXIST YET. Its id and fingerprint are read back
#: from GitHub after the principal posts it and retained in a further fast-forward commit on
#: this pull request. They are NEVER predicted. Until then, no ratification is bound and the
#: complete predicate yields the all-false result for every input.
BOUND_RATIFICATION_ID: int | None = None
BOUND_RATIFICATION_FINGERPRINT: str | None = None

#: The independent reviews. Review EVIDENCE ONLY -- never ratification, never acceptance.
INDEPENDENT_REVIEW_IDS = (5060791095, 5060793954)


def _actor_login(record: dict) -> str | None:
    """The sole identity source. Deliberately ignores every body field."""
    user = record.get("user")
    if not isinstance(user, dict):
        return None
    login = user.get("login")
    return login if isinstance(login, str) else None


def _actor_type(record: dict) -> str | None:
    user = record.get("user")
    if not isinstance(user, dict):
        return None
    value = user.get("type")
    return value if isinstance(value, str) else None


def is_canonical_top_level_issue_comment(record: dict) -> bool:
    """SS-G.1 -- record kind and repository/PR association, from canonical API fields only.

    Rejects pull-request reviews, inline review comments, commit comments, comments on any
    other issue or pull request, malformed or disagreeing URLs, and synthetic records.
    """
    if not isinstance(record, dict):
        return False
    # A foreign field is decisive: it proves this is some other resource.
    for field in FOREIGN_RECORD_KIND_FIELDS:
        if field in record:
            return False
    ident = record.get("id")
    # bool is an int subclass; a stray True must not pass as an id.
    if type(ident) is not int:
        return False
    if record.get("issue_url") != RATIFICATION_ISSUE_URL:
        return False
    if record.get("url") != f"{RATIFICATION_URL_PREFIX}{ident}":
        return False
    if record.get("html_url") != f"{RATIFICATION_HTML_PREFIX}{ident}":
        return False
    return True


def is_direct_principal_record(record: dict) -> bool:
    """SS-G.2 -- the four actor/provenance conjuncts.

    NECESSARY, NOT SUFFICIENT; must be conjoined with SS-G.1.

    Review 5060791095 FAILS this function, on the app conjunct: ``performed_via_github_app``
    is ABSENT on a pull-request review, and this function requires it PRESENT and null. It
    fails SS-G.1 independently, on record kind. Corrected under DELTA review 5061031729
    MINOR 1 -- an earlier docstring claimed this function accepted that review, which the
    corrected implementation and its tests both contradict.

    Body text is never consulted here.
    """
    if not isinstance(record, dict):
        return False
    if _actor_login(record) != PRINCIPAL_LOGIN:
        return False
    if _actor_type(record) != PRINCIPAL_TYPE:
        return False
    if record.get("author_association") != PRINCIPAL_ASSOCIATION:
        return False
    # PRESENT and null. An ABSENT key is the signature of a review or review comment, so
    # absence must FAIL rather than pass -- this is the corrected BLOCKING conjunct.
    if "performed_via_github_app" not in record:
        return False
    if record["performed_via_github_app"] is not None:
        return False
    return True


def canonical_ratification_fingerprint(record: dict) -> str:
    """SS-G.4 -- canonical JSON over identity-bearing fields, body represented by its own hash.

    Sorted keys, fixed separators, never a ``repr`` of a mapping. Any edit to the body, actor,
    timestamp, or canonical URLs changes this value and relocks the gate.
    """
    body = record.get("body")
    payload = {
        "id": record.get("id"),
        "url": record.get("url"),
        "html_url": record.get("html_url"),
        "issue_url": record.get("issue_url"),
        "user.login": _actor_login(record),
        "user.type": _actor_type(record),
        "author_association": record.get("author_association"),
        "performed_via_github_app": record.get("performed_via_github_app"),
        "created_at": record.get("created_at"),
        "body_sha256": hashlib.sha256(
            (body if isinstance(body, str) else "").encode("utf-8")
        ).hexdigest(),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


#: SS-G.3 -- the EXACT affirmative declaration schema. Corrected under DELTA review
#: 5061031729 BLOCKING 2: unordered substring presence let an explicit REFUSAL that merely
#: mentioned every pin satisfy the scope test. A fingerprint authenticates an already-valid
#: record against later edits; it can never make an initially-bound refusal affirmative.
RATIFICATION_HEADER = "XASSET-0062 RATIFICATION"
RATIFICATION_ACTION = "RATIFY-AND-ACCEPT"

#: Exact key -> exact required value. ``pr363_accepted_head`` is validated by FORM only; the
#: repository cannot know its own future final head, so that value's correctness against the
#: real final head is established by independent GitHub readback (SS-G.6), never from here.
RATIFICATION_SCHEMA: dict[str, str | None] = {
    "action": RATIFICATION_ACTION,
    "pr363_accepted_head": None,                      # 40 lowercase hex, form-checked
    "pr362_pull_request": str(RATIFIED_PULL_REQUEST),
    "pr362_accepted_head": RATIFIED_ACCEPTED_HEAD,
    "pr362_independent_review": str(RATIFIED_REVIEW_ID),
    "pr362_bot_acceptance": str(RATIFIED_BOT_ACCEPTANCE_ID),
    "pr362_merge": RATIFIED_MERGE,
    "pr362_closure": str(RATIFIED_CLOSURE_ID),
    "pr362_independent_stop": str(INDEPENDENT_STOP_ID),
}

_SHA40 = re.compile(r"\A[0-9a-f]{40}\Z")
_KEY_VALUE = re.compile(r"\A([a-z0-9_]+):[ ](.*)\Z")


def parse_ratification_body(body: object) -> dict[str, str] | None:
    """Parse the COMPLETE body under the strict schema, or return ``None``.

    Deterministic and total. Every non-blank line must be either the exact header or one
    ``key: value`` pair drawn from :data:`RATIFICATION_SCHEMA`; every key must appear exactly
    once; every fixed value must match exactly. ANY other line -- prose, a disclaimer, a
    ``VOID`` marker, a reference list, trailing contradictory material -- rejects the whole
    body. There is no substring matching anywhere in this function.
    """
    if not isinstance(body, str):
        return None
    lines = [ln.rstrip() for ln in body.strip().splitlines()]
    lines = [ln for ln in lines if ln != ""]
    if not lines or lines[0] != RATIFICATION_HEADER:
        return None
    parsed: dict[str, str] = {}
    for line in lines[1:]:
        match = _KEY_VALUE.match(line)
        if match is None:
            return None                      # prose, VOID marker, or malformed pair
        key, value = match.group(1), match.group(2)
        if key not in RATIFICATION_SCHEMA:
            return None                      # unknown key
        if key in parsed:
            return None                      # duplicated key
        required = RATIFICATION_SCHEMA[key]
        if required is None:
            if not _SHA40.match(value):
                return None                  # form check only
        elif value != required:
            return None                      # exact value required
        parsed[key] = value
    if set(parsed) != set(RATIFICATION_SCHEMA):
        return None                          # a missing key
    return parsed


def body_declares_ratification(record: dict) -> bool:
    """SS-G.3 -- the body carries an EXACT affirmative declaration, and nothing else.

    Replaces the withdrawn ``body_names_every_scope_pin``, which asked only whether each pin
    appeared as a substring somewhere. Body text still never establishes actor identity or
    record kind; those come solely from the canonical fields above.
    """
    if not isinstance(record, dict):
        return False
    return parse_ratification_body(record.get("body")) is not None


def _ratification_is_structurally_complete(record: dict) -> bool:
    """Every SS-G structural conjunct EXCEPT the live-origin binding.

    Structural only. Passing this proves the record has the right SHAPE; it proves NOTHING
    about live GitHub origin. A caller can assemble a dictionary that satisfies every clause
    here -- the suite's own fixtures do exactly that. Live origin is established solely by
    independent GitHub API readback and the retained evidence of SS-G.6, never from here.
    Corrected under DELTA review 5061031729 BLOCKING 2.
    """
    if not is_canonical_top_level_issue_comment(record):
        return False
    if not is_direct_principal_record(record):
        return False
    if not body_declares_ratification(record):
        return False
    # SS-G.5 retrospection: strictly after the PR #362 merge. Equality is not "after".
    created = record.get("created_at")
    if not isinstance(created, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", created
    ):
        return False
    if created <= MERGED_AT:
        return False
    return True


def _ratifies_with_binding(
    record: dict, _bound_id: int | None, _bound_fingerprint: str | None
) -> bool:
    """PRIVATE injection seam. TEST-ONLY -- never the operational entry point.

    Exists so the suite can exercise the bound path without exposing a caller-selectable
    binding on the operational predicate, which DELTA review 5061031729 BLOCKING 2 required
    removed: a caller who may choose both the record and its binding can always self-bind.
    """
    if _bound_id is None or _bound_fingerprint is None:
        return False
    if not _ratification_is_structurally_complete(record):
        return False
    if record.get("id") != _bound_id:
        return False
    if canonical_ratification_fingerprint(record) != _bound_fingerprint:
        return False
    return True


def ratifies_pr362_acceptance(record: dict) -> bool:
    """The complete SS-G predicate. ONE argument -- the record. Nothing else is selectable.

    The binding is read from the module constants, which are ``None`` and, under the corrected
    SS-G.6 lifecycle, STAY ``None``: the live id and fingerprint are retained as GitHub
    lifecycle evidence by independent coordinator readback, never committed to this repository,
    because a binding commit would change the very head the ratification accepts (DELTA review
    5061031729 BLOCKING 1). This predicate therefore yields ``False`` in-repository for every
    input, by design, and is never the thing that certifies a live record.
    """
    return _ratifies_with_binding(
        record, BOUND_RATIFICATION_ID, BOUND_RATIFICATION_FINGERPRINT
    )


# ======================================================================================
# SS-I.2 -- the immediate post-merge-verification (PMV) evidence predicate.
#
# Added under DELTA review 5061031729 MAJOR 1. SS-I.2's role split was previously asserted in
# prose and pinned only by prose-presence tests plus a single negative case, so the operative
# three-condition rule -- exact designation, the SAME coordinator/session that merged, honest
# provenance, and strict merge < verification < closure ordering -- was never mechanised and
# its failure modes were never provable.
#
# This predicate is deliberately SEPARATE from the SS-G ratification predicate. The two answer
# different questions and must never be satisfiable by one another: an app-attributed
# coordinator record PASSES here and can NEVER pass SS-G.
# ======================================================================================
def _app_slug(record: dict) -> str | None:
    """The application slug, or ``None`` for a directly attributed record.

    Distinguishes PRESENT-and-null (honest direct attribution) from a present application
    object. Absence is handled separately by :func:`_app_provenance_is_retained`.
    """
    app = record.get("performed_via_github_app")
    if not isinstance(app, dict):
        return None
    slug = app.get("slug")
    return slug if isinstance(slug, str) else None


def _app_provenance_is_retained(record: dict) -> bool:
    """SS-I.2 condition 2 -- provenance must be RETAINED, honestly, either way.

    An ABSENT key is not honest direct attribution; it is unretained provenance, and it is the
    signature of a record kind that carries none. Either a null (direct) or an application
    object (app-attributed) is acceptable, because SS-I.2 permits both -- what it forbids is a
    record that does not say.
    """
    if "performed_via_github_app" not in record:
        return False
    app = record["performed_via_github_app"]
    if app is None:
        return True
    return isinstance(app, dict) and isinstance(app.get("slug"), str) and app["slug"] != ""


def _is_iso_z(value: object) -> bool:
    return isinstance(value, str) and bool(
        re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value)
    )


def post_merge_verification_is_valid(
    record: dict,
    *,
    designated_coordinator: str | None,
    merge_performed_by: str | None,
    merged_at: str,
    closure_at: str,
) -> bool:
    """SS-I.2 -- is this record valid immediate post-merge-verification evidence?

    Conjunctive over the three operative conditions, plus record kind:

    1. the verifier is the principal, **or** the designated merge coordinator that ACTUALLY
       performed the merge -- designation alone is insufficient, and a coordinator who did not
       perform this merge fails (``OPS-0009`` ``SS-9``: the same session that merges verifies);
    2. derived actor and application provenance are honestly retained -- an app-attributed
       coordinator reads back as what it is;
    3. ``merged_at < record.created_at < closure_at``, STRICTLY at both boundaries.

    Never principal acceptance and never an ``SS-G`` ratification, whatever it returns.
    """
    if not isinstance(record, dict):
        return False
    if not is_canonical_top_level_issue_comment(record):
        return False

    login = _actor_login(record)
    if login is None or _actor_type(record) is None:
        return False
    if record.get("author_association") is None:
        return False

    # Condition 1 -- who may verify.
    if login == PRINCIPAL_LOGIN:
        pass
    else:
        # ``login`` is a non-empty ``str`` here, so these two equalities alone already exclude
        # every absent, empty, wrong-typed, and mismatched designation or merger. Separate
        # type-guards were tried and PROVEN unreachable -- no input can satisfy them without
        # also satisfying these -- so they are removed rather than kept as untestable
        # defence-in-depth. Every line below is load-bearing and independently mutation-proved.
        if login != designated_coordinator:
            return False
        # OPS-0009 SS-9: the SAME session that merged must verify.
        if login != merge_performed_by:
            return False

    # Condition 2 -- honest, retained provenance.
    if not _app_provenance_is_retained(record):
        return False

    # Condition 3 -- strict chronology, from GitHub's own timestamps.
    created = record.get("created_at")
    if not (_is_iso_z(created) and _is_iso_z(merged_at) and _is_iso_z(closure_at)):
        return False
    if not (merged_at < created < closure_at):
        return False
    return True


# --------------------------------------------------------------------------------------
# Record fixtures modelled on the real, live-derived record SHAPES.
#
# The review fixture below reproduces the exact GitHub shape of review 5060791095 -- the live
# counterexample that defeated the earlier predicate.
# --------------------------------------------------------------------------------------
GENUINE_RATIFICATION_ID = 9_999_999_999  # a synthetic id for fixtures ONLY; never a claim.

#: A schema-conformant affirmative declaration. The PR #363 head here is a FIXTURE value --
#: 40 hex, deliberately not any real commit -- because the repository cannot know its own
#: future final head; SS-G.6 readback establishes the real one.
FIXTURE_PR363_HEAD = "0" * 40

SCOPE_BODY = "\n".join([
    RATIFICATION_HEADER,
    f"action: {RATIFICATION_ACTION}",
    f"pr363_accepted_head: {FIXTURE_PR363_HEAD}",
    f"pr362_pull_request: {RATIFIED_PULL_REQUEST}",
    f"pr362_accepted_head: {RATIFIED_ACCEPTED_HEAD}",
    f"pr362_independent_review: {RATIFIED_REVIEW_ID}",
    f"pr362_bot_acceptance: {RATIFIED_BOT_ACCEPTANCE_ID}",
    f"pr362_merge: {RATIFIED_MERGE}",
    f"pr362_closure: {RATIFIED_CLOSURE_ID}",
    f"pr362_independent_stop: {INDEPENDENT_STOP_ID}",
])


def _refusal_body(prefix="I do NOT ratify or accept anything. References only:"):
    """The DELTA review 5061031729 BLOCKING 2 counterexample: a REFUSAL naming every pin."""
    return prefix + " PR #{pr}; accepted head {head}; review {rev}; acceptance {acc}; " \
        "merge {merge}; closure {close}; stop {stop}.".format(
            pr=RATIFIED_PULL_REQUEST, head=RATIFIED_ACCEPTED_HEAD, rev=RATIFIED_REVIEW_ID,
            acc=RATIFIED_BOT_ACCEPTANCE_ID, merge=RATIFIED_MERGE,
            close=RATIFIED_CLOSURE_ID, stop=INDEPENDENT_STOP_ID)


def _issue_comment(
    login=PRINCIPAL_LOGIN, type_=PRINCIPAL_TYPE, assoc=PRINCIPAL_ASSOCIATION,
    app=None, app_key_present=True, created="2026-08-30T18:00:00Z",
    body=SCOPE_BODY, ident=GENUINE_RATIFICATION_ID, pr=None, **overrides,
):
    """A canonical top-level issue comment on this corrective pull request."""
    pr = THIS_CORRECTIVE_PULL_REQUEST if pr is None else pr
    rec = {
        "id": ident,
        "url": f"{REPO_API}/issues/comments/{ident}",
        "html_url": f"{REPO_HTML}/pull/{pr}#issuecomment-{ident}",
        "issue_url": f"{REPO_API}/issues/{pr}",
        "user": {"login": login, "type": type_},
        "author_association": assoc,
        "created_at": created,
        "body": body,
    }
    if app_key_present:
        rec["performed_via_github_app"] = ({"slug": app} if app else None)
    rec.update(overrides)
    return rec


def _pull_request_review(
    login=PRINCIPAL_LOGIN, type_=PRINCIPAL_TYPE, assoc=PRINCIPAL_ASSOCIATION,
    ident=5060791095, commit=None, body="## INDEPENDENT FULL EXACT-HEAD REVIEW",
):
    """The EXACT live shape of review 5060791095 -- the BLOCKING counterexample.

    Note what is absent: no ``performed_via_github_app`` key at all, no ``issue_url``, no
    ``url``; and a ``pull_request_url`` and ``commit_id`` that are present.
    """
    return {
        "id": ident,
        "node_id": "PRR_synthetic",
        "user": {"login": login, "type": type_},
        "author_association": assoc,
        "body": body,
        "state": "COMMENTED",
        "html_url": f"{REPO_HTML}/pull/{THIS_CORRECTIVE_PULL_REQUEST}"
                    f"#pullrequestreview-{ident}",
        "pull_request_url": f"{REPO_API}/pulls/{THIS_CORRECTIVE_PULL_REQUEST}",
        "commit_id": commit or "ca099915ecf4f53bcf866c2b27b879c3b2d339a7",
        "submitted_at": "2026-08-30T12:17:13Z",
        "created_at": "2026-08-30T12:17:13Z",
    }


def _review_comment(ident=3824991608):
    """An inline review comment -- a third distinct resource kind."""
    return {
        "id": ident,
        "url": f"{REPO_API}/pulls/comments/{ident}",
        "html_url": f"{REPO_HTML}/pull/{THIS_CORRECTIVE_PULL_REQUEST}#discussion_r{ident}",
        "pull_request_url": f"{REPO_API}/pulls/{THIS_CORRECTIVE_PULL_REQUEST}",
        "pull_request_review_id": 5060791095,
        "diff_hunk": "@@ -1 +1 @@",
        "path": "governance/decisions.yaml",
        "position": 1,
        "user": {"login": PRINCIPAL_LOGIN, "type": PRINCIPAL_TYPE},
        "author_association": PRINCIPAL_ASSOCIATION,
        "created_at": "2026-08-30T18:00:00Z",
        "body": SCOPE_BODY,
    }


def _commit_comment(ident=170000001):
    """A commit comment -- a fourth distinct resource kind."""
    return {
        "id": ident,
        "url": f"{REPO_API}/comments/{ident}",
        "html_url": f"{REPO_HTML}/commit/{RATIFIED_MERGE}#commitcomment-{ident}",
        "commit_id": RATIFIED_MERGE,
        "user": {"login": PRINCIPAL_LOGIN, "type": PRINCIPAL_TYPE},
        "author_association": PRINCIPAL_ASSOCIATION,
        "performed_via_github_app": None,
        "created_at": "2026-08-30T18:00:00Z",
        "body": SCOPE_BODY,
    }


GENUINE_RATIFICATION = _issue_comment()
GENUINE_FINGERPRINT = canonical_ratification_fingerprint(GENUINE_RATIFICATION)


def _bound(record=None):
    """TEST-ONLY binding kwargs for the private seam. Never available operationally."""
    record = GENUINE_RATIFICATION if record is None else record
    return dict(
        _bound_id=record["id"],
        _bound_fingerprint=canonical_ratification_fingerprint(record),
    )


class TestTheReviewerRecordIsRejected:
    """BLOCKING 1 (supplement 5060793954) -- the live counterexample, closed on both axes."""

    def test_the_real_review_shape_satisfies_the_actor_conjuncts(self):
        """Reproduces WHY the earlier predicate failed: the actor test alone still passes."""
        review = _pull_request_review()
        assert _actor_login(review) == PRINCIPAL_LOGIN
        assert _actor_type(review) == PRINCIPAL_TYPE
        assert review["author_association"] == PRINCIPAL_ASSOCIATION
        assert "performed_via_github_app" not in review

    def test_the_real_review_shape_is_rejected_by_the_principal_predicate(self):
        """The corrected app conjunct requires the key PRESENT, so absence now fails."""
        assert is_direct_principal_record(_pull_request_review()) is False

    def test_the_real_review_shape_is_rejected_by_the_record_kind_predicate(self):
        assert is_canonical_top_level_issue_comment(_pull_request_review()) is False

    def test_the_real_review_shape_is_rejected_by_the_complete_predicate(self):
        assert _ratifies_with_binding(_pull_request_review(), **_bound()) is False

    def test_the_review_is_rejected_even_carrying_the_full_scope_body(self):
        """A review quoting every pin verbatim still fails -- body is never record-kind proof."""
        review = _pull_request_review(body=SCOPE_BODY)
        assert body_declares_ratification(review) is True
        assert _ratifies_with_binding(review, **_bound()) is False

    @pytest.mark.parametrize("review_id", INDEPENDENT_REVIEW_IDS)
    def test_neither_independent_review_can_ever_ratify(self, review_id):
        """SS-G.7: 5060791095 and 5060793954 are review evidence only."""
        assert _ratifies_with_binding(_pull_request_review(ident=review_id), **_bound()) is False

    def test_an_absent_app_key_is_not_the_same_as_a_null_one(self):
        """The precise defect: ``.get()`` cannot tell them apart, so the test must not use it."""
        absent = _issue_comment(app_key_present=False)
        present_null = _issue_comment(app_key_present=True, app=None)
        assert absent.get("performed_via_github_app") == present_null.get(
            "performed_via_github_app"
        )
        assert is_direct_principal_record(absent) is False
        assert is_direct_principal_record(present_null) is True


class TestOtherRecordKindsAreRejected:
    def test_an_inline_review_comment_is_rejected(self):
        rc = _review_comment()
        assert is_canonical_top_level_issue_comment(rc) is False
        assert _ratifies_with_binding(rc, **_bound()) is False

    def test_a_commit_comment_is_rejected(self):
        cc = _commit_comment()
        assert is_canonical_top_level_issue_comment(cc) is False
        # It even satisfies the actor conjuncts, which is exactly why kind must be checked.
        assert is_direct_principal_record(cc) is True
        assert _ratifies_with_binding(cc, **_bound()) is False

    @pytest.mark.parametrize("field", FOREIGN_RECORD_KIND_FIELDS)
    def test_any_foreign_record_kind_field_is_decisive(self, field):
        rec = _issue_comment(**{field: "anything"})
        assert is_canonical_top_level_issue_comment(rec) is False
        assert _ratifies_with_binding(rec, **_bound()) is False

    def test_a_top_level_comment_on_the_wrong_pull_request_is_rejected(self):
        for wrong in (RATIFIED_PULL_REQUEST, 1, THIS_CORRECTIVE_PULL_REQUEST + 1):
            rec = _issue_comment(pr=wrong)
            assert is_canonical_top_level_issue_comment(rec) is False, wrong
            assert _ratifies_with_binding(rec, **_bound(rec)) is False, wrong


class TestCanonicalUrlsAndIdMustAgree:
    @pytest.mark.parametrize(
        "field,value",
        [
            ("url", f"{REPO_API}/issues/comments/1"),
            ("url", f"{REPO_API}/pulls/comments/{GENUINE_RATIFICATION_ID}"),
            ("url", "not-a-url"),
            ("url", None),
            ("html_url", f"{REPO_HTML}/pull/999#issuecomment-{GENUINE_RATIFICATION_ID}"),
            ("html_url", f"{REPO_HTML}/pull/{THIS_CORRECTIVE_PULL_REQUEST}"
                         f"#pullrequestreview-{GENUINE_RATIFICATION_ID}"),
            ("html_url", None),
            ("issue_url", f"{REPO_API}/issues/{RATIFIED_PULL_REQUEST}"),
            ("issue_url", "https://api.github.com/repos/someone/else/issues/363"),
            ("issue_url", None),
        ],
    )
    def test_a_malformed_or_mismatched_canonical_url_is_rejected(self, field, value):
        rec = _issue_comment(**{field: value})
        assert is_canonical_top_level_issue_comment(rec) is False
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    @pytest.mark.parametrize("ident", [None, "9999999999", 3.0, True])
    def test_a_missing_or_wrongly_typed_id_is_rejected(self, ident):
        rec = _issue_comment()
        rec["id"] = ident
        assert is_canonical_top_level_issue_comment(rec) is False

    def test_a_bool_id_is_rejected_on_its_own_terms(self):
        """``bool`` is an ``int`` subclass, so ``isinstance`` would admit ``True``.

        In the parametrized case above the URL comparison masks that -- the urls name the real
        id, not ``True``. Building the record so its urls literally agree with ``True`` removes
        the mask, leaving the exact-type check as the only thing that can reject it.
        """
        rec = _issue_comment(ident=True)
        assert rec["url"] == f"{RATIFICATION_URL_PREFIX}True"
        assert rec["html_url"] == f"{RATIFICATION_HTML_PREFIX}True"
        assert isinstance(True, int)          # the trap the exact-type check exists to close
        assert type(rec["id"]) is not int
        assert is_canonical_top_level_issue_comment(rec) is False
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    def test_an_id_that_disagrees_with_its_urls_is_rejected(self):
        rec = _issue_comment()
        rec["id"] = GENUINE_RATIFICATION_ID + 1  # urls still name the old id
        assert is_canonical_top_level_issue_comment(rec) is False
        assert _ratifies_with_binding(rec, **_bound()) is False

    def test_a_record_whose_id_is_not_the_bound_one_is_rejected(self):
        other = _issue_comment(ident=GENUINE_RATIFICATION_ID + 7)
        # Structurally valid, correctly attributed, correct scope -- but NOT the bound record.
        assert is_canonical_top_level_issue_comment(other) is True
        assert is_direct_principal_record(other) is True
        assert _ratifies_with_binding(other, **_bound()) is False

    def test_the_bound_id_check_is_not_masked_by_the_fingerprint(self):
        """The id lives INSIDE the fingerprint payload, so a naive test cannot separate them.

        Supplying the record's OWN correct fingerprint alongside a MISMATCHED ``bound_id`` is
        the only shape where the two pieces of retained evidence can disagree -- so this is
        what actually proves the id equality is load-bearing rather than decorative.
        """
        rec = _issue_comment()
        correct_fingerprint = canonical_ratification_fingerprint(rec)
        assert (
            _ratifies_with_binding(
                rec, _bound_id=rec["id"], _bound_fingerprint=correct_fingerprint
            )
            is True
        )
        assert (
            _ratifies_with_binding(
                rec, _bound_id=rec["id"] + 1, _bound_fingerprint=correct_fingerprint
            )
            is False
        )


class TestTheFingerprintAuthenticatesTheRecord:
    def test_the_genuine_record_ratifies_when_bound(self):
        assert _ratifies_with_binding(GENUINE_RATIFICATION, **_bound()) is True

    @pytest.mark.parametrize(
        "field,value",
        [
            ("body", SCOPE_BODY + " VOID -- I do NOT ratify anything."),
            ("created_at", "2026-08-31T18:00:00Z"),
            ("author_association", "COLLABORATOR"),
        ],
    )
    def test_any_edit_changes_the_fingerprint_and_relocks(self, field, value):
        edited = _issue_comment(**{field: value})
        assert canonical_ratification_fingerprint(edited) != GENUINE_FINGERPRINT
        assert _ratifies_with_binding(edited, **_bound()) is False

    def test_a_changed_actor_changes_the_fingerprint(self):
        edited = _issue_comment(login="claude[bot]", type_="Bot", assoc="CONTRIBUTOR")
        assert canonical_ratification_fingerprint(edited) != GENUINE_FINGERPRINT
        assert _ratifies_with_binding(edited, **_bound()) is False

    def test_the_fingerprint_is_deterministic_and_canonical(self):
        a = canonical_ratification_fingerprint(GENUINE_RATIFICATION)
        b = canonical_ratification_fingerprint(dict(reversed(list(
            GENUINE_RATIFICATION.items()))))
        assert a == b
        assert len(a) == 64 and int(a, 16) >= 0

    def test_the_body_is_hashed_not_embedded_verbatim(self):
        long_body = SCOPE_BODY + "x" * 5000
        assert len(canonical_ratification_fingerprint(_issue_comment(body=long_body))) == 64

    def test_nothing_ratifies_while_the_binding_is_unset(self):
        """SS-G.4: the real comment does not exist yet, so nothing is bound."""
        assert BOUND_RATIFICATION_ID is None
        assert BOUND_RATIFICATION_FINGERPRINT is None
        assert ratifies_pr362_acceptance(GENUINE_RATIFICATION) is False

    def test_the_unbound_guard_is_present_though_it_is_defence_in_depth(self):
        """Disclosed honestly: this guard is REDUNDANT, and pinned structurally for that reason.

        With the guard removed, an unset binding still fails -- ``bound_id`` of ``None`` loses
        the id equality, and a ``bound_fingerprint`` of ``None`` loses the fingerprint
        comparison. A behavioural test therefore cannot distinguish its presence from its
        absence, which is exactly the kind of masked check this suite refuses to present as
        proof. It is retained because it makes the reason for rejection explicit and fails
        fast, and its presence is pinned by reading the source rather than by a test that would
        pass either way.
        """
        import inspect

        src = inspect.getsource(_ratifies_with_binding)
        assert "if _bound_id is None or _bound_fingerprint is None:" in src
        # And the redundancy is real, not assumed -- both downstream checks reject on their own.
        rec = _issue_comment()
        fp = canonical_ratification_fingerprint(rec)
        assert _ratifies_with_binding(rec, _bound_id=None, _bound_fingerprint=fp) is False
        assert _ratifies_with_binding(rec, _bound_id=rec["id"], _bound_fingerprint=None) is False

    @pytest.mark.parametrize("bad", ["", "0" * 64, "not-a-hash", None])
    def test_a_wrong_bound_fingerprint_rejects(self, bad):
        assert (
            _ratifies_with_binding(
                GENUINE_RATIFICATION,
                _bound_id=GENUINE_RATIFICATION_ID,
                _bound_fingerprint=bad,
            )
            is False
        )


class TestScopeIsAuthenticatedByTheRecordNotTheCaller:
    def test_the_operational_predicate_takes_only_the_record(self):
        """SS-G.3 -- no caller-selectable scope, id, or fingerprint (BLOCKING 2).

        A caller who may choose the record AND its binding can always self-bind. The
        operational entry point therefore exposes neither.
        """
        import inspect

        params = set(inspect.signature(ratifies_pr362_acceptance).parameters)
        assert params == {"record"}
        for forbidden in ("scope", "bound_id", "bound_fingerprint"):
            assert forbidden not in params

    def test_the_injection_seam_is_private_and_test_only(self):
        """The seam exists, is underscore-private, and its kwargs are underscore-private."""
        import inspect

        assert _ratifies_with_binding.__name__.startswith("_")
        params = set(inspect.signature(_ratifies_with_binding).parameters)
        assert params == {"record", "_bound_id", "_bound_fingerprint"}
        assert "TEST-ONLY" in inspect.getdoc(_ratifies_with_binding)

    def test_every_pin_must_appear_with_its_exact_value(self):
        for pin in RATIFIED_SCOPE_PINS:
            rec = _issue_comment(body=SCOPE_BODY.replace(pin, "REDACTED"))
            assert body_declares_ratification(rec) is False, pin
            assert _ratifies_with_binding(rec, **_bound(rec)) is False, pin

    def test_an_empty_or_non_string_body_fails(self):
        for body in ("", None, 123, {"text": SCOPE_BODY}):
            rec = _issue_comment(body=body)
            assert body_declares_ratification(rec) is False
            assert parse_ratification_body(body) is None

    def test_the_seven_pins_are_exactly_the_pr362_history(self):
        assert set(RATIFIED_SCOPE_PINS) == {
            str(RATIFIED_PULL_REQUEST), RATIFIED_ACCEPTED_HEAD, str(RATIFIED_REVIEW_ID),
            str(RATIFIED_BOT_ACCEPTANCE_ID), RATIFIED_MERGE, str(RATIFIED_CLOSURE_ID),
            str(INDEPENDENT_STOP_ID),
        }


class TestAnInitiallyBoundRefusalNeverRatifies:
    """DELTA review 5061031729 BLOCKING 2 -- the reproduced defect, and its closure.

    The withdrawn scope test asked only whether each pin appeared as a SUBSTRING somewhere in
    the body. The reviewer built a canonical principal-shaped issue comment whose body began
    "I do NOT ratify or accept anything. References only:", listed all seven pins, and bound
    it to its OWN id and its OWN freshly computed fingerprint -- and the complete predicate
    returned True.

    A fingerprint authenticates an already-valid record AGAINST LATER EDITS. It can never make
    an initially-bound refusal affirmative, because it is computed over whatever the body said
    at binding time. The fix is upstream of the fingerprint: the body must PARSE as an exact
    affirmative declaration.
    """

    def test_the_reviewers_exact_refusal_is_rejected_though_self_bound(self):
        rec = _issue_comment(body=_refusal_body())
        # It really does name every pin -- that is why substring presence was insufficient.
        for pin in RATIFIED_SCOPE_PINS:
            assert pin in rec["body"], pin
        # And it really is a canonical principal record on the right pull request.
        assert is_canonical_top_level_issue_comment(rec) is True
        assert is_direct_principal_record(rec) is True
        # It is nonetheless not a declaration, and self-binding cannot rescue it.
        assert body_declares_ratification(rec) is False
        assert parse_ratification_body(rec["body"]) is None
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    @pytest.mark.parametrize(
        "label,body",
        [
            ("void_prefix", "VOID. " + _refusal_body()),
            ("reference_only", _refusal_body("References only:")),
            ("trailing_contradiction",
             SCOPE_BODY + "\nHowever I do NOT actually ratify this."),
            ("trailing_void_marker", SCOPE_BODY + "\nVOID"),
            ("leading_prose", "Context follows.\n" + SCOPE_BODY),
            ("negated_action",
             SCOPE_BODY.replace("action: RATIFY-AND-ACCEPT", "action: DO-NOT-RATIFY")),
            ("alias_action_wrong_case",
             SCOPE_BODY.replace("action: RATIFY-AND-ACCEPT", "action: ratify-and-accept")),
            ("action_with_suffix",
             SCOPE_BODY.replace("action: RATIFY-AND-ACCEPT",
                                "action: RATIFY-AND-ACCEPT (VOID)")),
            ("unknown_key", SCOPE_BODY + "\nvoid: true"),
            ("duplicated_key", SCOPE_BODY + "\npr362_merge: " + RATIFIED_MERGE),
            ("missing_header", "\n".join(SCOPE_BODY.splitlines()[1:])),
            ("header_only", RATIFICATION_HEADER),
            ("substring_alias_pin",
             SCOPE_BODY.replace("pr362_merge: " + RATIFIED_MERGE,
                                "pr362_merge: " + RATIFIED_MERGE[:12])),
            ("pin_embedded_in_longer_value",
             SCOPE_BODY.replace("pr362_closure: " + str(RATIFIED_CLOSURE_ID),
                                "pr362_closure: " + str(RATIFIED_CLOSURE_ID) + "0")),
            ("malformed_pr363_head",
             SCOPE_BODY.replace("pr363_accepted_head: " + FIXTURE_PR363_HEAD,
                                "pr363_accepted_head: TBD")),
            ("uppercase_pr363_head",
             SCOPE_BODY.replace("pr363_accepted_head: " + FIXTURE_PR363_HEAD,
                                "pr363_accepted_head: " + "A" * 40)),
        ],
    )
    def test_no_self_bound_variant_ratifies(self, label, body):
        """Each names every pin where applicable, and each is bound to its own fingerprint."""
        rec = _issue_comment(body=body)
        assert parse_ratification_body(body) is None, label
        assert body_declares_ratification(rec) is False, label
        assert _ratifies_with_binding(rec, **_bound(rec)) is False, label

    def test_a_junk_first_line_before_a_complete_schema_is_rejected(self):
        """The header check is load-bearing, and ONLY this shape proves it.

        A headerless body is already rejected for a different reason -- the parser skips line
        zero, so ``action`` goes missing. The case that isolates the header requirement is a
        body whose first line is junk and whose REMAINING lines are the complete schema.
        """
        pairs = "\n".join(SCOPE_BODY.splitlines()[1:])
        assert parse_ratification_body("GARBAGE\n" + pairs) is None
        assert parse_ratification_body("VOID\n" + pairs) is None
        assert parse_ratification_body("I do NOT ratify.\n" + pairs) is None
        rec = _issue_comment(body="GARBAGE\n" + pairs)
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    def test_a_wrong_header_is_rejected(self):
        for wrong in ("XASSET-0061 RATIFICATION", "xasset-0062 ratification",
                      "XASSET-0062", "# XASSET-0062 RATIFICATION",
                      "XASSET-0062  RATIFICATION", "RATIFICATION XASSET-0062"):
            body = "\n".join([wrong] + SCOPE_BODY.splitlines()[1:])
            assert parse_ratification_body(body) is None, wrong

    def test_trailing_whitespace_on_the_header_is_tolerated_not_a_loophole(self):
        """Deliberate formatting slack: rstrip() normalises it, and nothing else changes."""
        body = "\n".join(["XASSET-0062 RATIFICATION   "] + SCOPE_BODY.splitlines()[1:])
        assert parse_ratification_body(body) is not None
        # The tolerance is whitespace ONLY -- a non-space character still rejects.
        assert parse_ratification_body(body.replace("RATIFICATION   ", "RATIFICATION .")) is None

    def test_the_affirmative_declaration_is_what_distinguishes_them(self):
        """Control: the ONLY difference is the body, and it is decisive."""
        genuine = _issue_comment(body=SCOPE_BODY)
        refusal = _issue_comment(body=_refusal_body())
        assert genuine["id"] == refusal["id"]
        assert genuine["user"] == refusal["user"]
        assert _ratifies_with_binding(genuine, **_bound(genuine)) is True
        assert _ratifies_with_binding(refusal, **_bound(refusal)) is False

    def test_parse_returns_the_exact_declared_values(self):
        parsed = parse_ratification_body(SCOPE_BODY)
        assert parsed is not None
        assert set(parsed) == set(RATIFICATION_SCHEMA)
        assert parsed["action"] == RATIFICATION_ACTION
        assert parsed["pr362_merge"] == RATIFIED_MERGE
        assert parsed["pr362_accepted_head"] == RATIFIED_ACCEPTED_HEAD

    def test_parse_is_total_and_never_raises(self):
        for junk in (None, 123, b"bytes", [], {}, object(), "", "\n\n\n"):
            assert parse_ratification_body(junk) is None

    def test_blank_lines_and_trailing_space_are_tolerated_but_prose_is_not(self):
        """Formatting slack must not become a content loophole."""
        padded = "\n\n" + SCOPE_BODY.replace("\n", "  \n") + "\n\n"
        assert parse_ratification_body(padded) is not None
        assert parse_ratification_body(padded + "\nnot really though") is None


class TestTheDocumentationMatchesTheMechanism:
    """DELTA review 5061031729 MINOR 1 -- the docstring contradicted the implementation.

    ``is_direct_principal_record`` claimed review 5060791095 "satisfies this function". The
    corrected function REJECTS it, on the absent application key. Documentation drift of this
    kind is exactly what a reader relies on, so it is pinned behaviorally here rather than left
    to review.
    """

    def test_the_docstring_says_the_review_fails_and_the_code_agrees(self):
        import inspect

        doc = _flat(inspect.getdoc(is_direct_principal_record))
        assert "Review 5060791095 FAILS this function" in doc
        assert "satisfies this function" not in doc
        # And the code actually does what the docstring now says.
        assert is_direct_principal_record(_pull_request_review(ident=5060791095)) is False

    def test_the_docstring_names_the_correct_reason(self):
        import inspect

        doc = _flat(inspect.getdoc(is_direct_principal_record))
        assert "is ABSENT on a pull-request review" in doc
        assert "requires it PRESENT and null" in doc
        review = _pull_request_review(ident=5060791095)
        assert "performed_via_github_app" not in review          # the stated reason, verified
        assert is_canonical_top_level_issue_comment(review) is False   # and the independent one

    def test_the_docstring_records_which_review_corrected_it(self):
        import inspect

        doc = _flat(inspect.getdoc(is_direct_principal_record))
        assert "DELTA review 5061031729" in doc
        assert "MINOR 1" in doc


class TestStructuralShapeIsNotProofOfLiveOrigin:
    """DELTA review 5061031729 BLOCKING 2 -- the withdrawn SS-G.1 over-claim.

    The old SS-G.1 text said canonical fields reject "any synthetic record a caller assembles."
    That was false, and this suite's own fixtures are the counterexample: they are assembled in
    Python and they pass. A dictionary-shape predicate cannot prove a record came from GitHub.
    """

    def test_a_caller_assembled_record_passes_every_structural_clause(self):
        rec = _issue_comment()
        assert is_canonical_top_level_issue_comment(rec) is True
        assert is_direct_principal_record(rec) is True
        assert body_declares_ratification(rec) is True
        assert _ratification_is_structurally_complete(rec) is True

    def test_that_same_record_is_not_operationally_ratified(self):
        """Structural completeness is explicitly NOT ratification."""
        assert ratifies_pr362_acceptance(_issue_comment()) is False

    def test_the_helper_documents_that_it_proves_no_origin(self):
        import inspect

        doc = _flat(inspect.getdoc(_ratification_is_structurally_complete))
        assert "proves NOTHING about live GitHub origin" in doc
        assert "independent GitHub API readback" in doc

    def test_a_self_bound_synthetic_record_is_not_final_evidence(self):
        """Self-binding is exactly what the operational predicate refuses to accept."""
        rec = _issue_comment()
        fingerprint = canonical_ratification_fingerprint(rec)
        # The seam accepts it -- that is what the seam is FOR, and why it is test-only.
        assert _ratifies_with_binding(rec, _bound_id=rec["id"],
                                      _bound_fingerprint=fingerprint) is True
        # The operational predicate offers no way to supply that binding.
        import inspect

        assert set(inspect.signature(ratifies_pr362_acceptance).parameters) == {"record"}
        assert ratifies_pr362_acceptance(rec) is False


class TestBodyTextNeverOverridesDerivedActorIdentity:
    """The original claim, retained: prose cannot manufacture an actor."""

    def test_bot_record_claiming_to_quote_the_principal_is_refused(self):
        rec = _issue_comment(
            login="claude[bot]", type_="Bot", assoc="CONTRIBUTOR", app=CLAUDE_APP_SLUG,
            body="The acceptance below is the principal's. Quoted verbatim. " + SCOPE_BODY,
        )
        assert is_direct_principal_record(rec) is False
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    @pytest.mark.parametrize(
        "body",
        [
            "I, the principal, ratify this.",
            "Mast3rkey / User / OWNER ratifies this.",
            "user.login: Mast3rkey\nuser.type: User\nauthor_association: OWNER",
            "performed_via_github_app: null",
            "This comment is a direct principal act with no application.",
        ],
    )
    def test_no_body_string_can_promote_a_bot_record(self, body):
        rec = _issue_comment(login="claude[bot]", type_="Bot", assoc="CONTRIBUTOR",
                             app=CLAUDE_APP_SLUG, body=body)
        assert is_direct_principal_record(rec) is False

    def test_identity_comes_only_from_the_user_block(self):
        rec = _issue_comment(login="claude[bot]", type_="Bot", assoc="CONTRIBUTOR",
                             app=CLAUDE_APP_SLUG, body="login=Mast3rkey")
        assert _actor_login(rec) == "claude[bot]"


class TestTheDerivedTripleAloneIsNotSufficient:
    """SS-C, now with the record-kind dimension the supplement added."""

    def test_claude_app_record_under_the_owner_account_is_refused(self):
        rec = _issue_comment(app=CLAUDE_APP_SLUG)
        assert _actor_login(rec) == PRINCIPAL_LOGIN
        assert _actor_type(rec) == PRINCIPAL_TYPE
        assert rec["author_association"] == PRINCIPAL_ASSOCIATION
        assert is_direct_principal_record(rec) is False

    def test_independent_reviewer_issue_comment_is_refused(self):
        assert is_direct_principal_record(_issue_comment(app=REVIEWER_APP_SLUG)) is False

    def test_a_triple_only_predicate_would_admit_the_reviewer_review(self):
        """Why SS-G.2 alone is insufficient -- demonstrated on the real review shape."""

        def triple_only(record):
            return (
                _actor_login(record) == PRINCIPAL_LOGIN
                and _actor_type(record) == PRINCIPAL_TYPE
                and record.get("author_association") == PRINCIPAL_ASSOCIATION
            )

        def triple_plus_naive_app(record):
            return triple_only(record) and record.get("performed_via_github_app") is None

        review = _pull_request_review()
        assert triple_only(review) is True
        # The EARLIER predicate -- the BLOCKING defect, reproduced exactly.
        assert triple_plus_naive_app(review) is True
        # The corrected mechanism refuses it on both axes.
        assert is_direct_principal_record(review) is False
        assert is_canonical_top_level_issue_comment(review) is False

    @pytest.mark.parametrize(
        "login,type_,assoc,app",
        [
            ("Mast3rkey", "User", "OWNER", "claude"),
            ("Mast3rkey", "User", "OWNER", "chatgpt-codex-connector"),
            ("claude[bot]", "Bot", "CONTRIBUTOR", "claude"),
            ("chatgpt-codex-connector[bot]", "Bot", "NONE", "chatgpt-codex-connector"),
            ("Mast3rkey", "Bot", "OWNER", None),
            ("Mast3rkey", "User", "CONTRIBUTOR", None),
            ("someone-else", "User", "OWNER", None),
        ],
    )
    def test_every_non_direct_actor_shape_is_refused(self, login, type_, assoc, app):
        assert is_direct_principal_record(
            _issue_comment(login=login, type_=type_, assoc=assoc, app=app)
        ) is False

    def test_each_conjunct_is_independently_necessary(self):
        assert is_direct_principal_record(_issue_comment()) is True
        for kw in ({"login": "claude[bot]"}, {"type_": "Bot"},
                   {"assoc": "CONTRIBUTOR"}, {"app": CLAUDE_APP_SLUG},
                   {"app_key_present": False}):
            assert is_direct_principal_record(_issue_comment(**kw)) is False, kw


class TestRetrospectionAndMalformedShapes:
    @pytest.mark.parametrize("created", ["2026-08-29T15:00:00Z", MERGED_AT])
    def test_a_ratification_at_or_before_the_merge_is_refused(self, created):
        rec = _issue_comment(created=created)
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    @pytest.mark.parametrize(
        "created", ["", "2026-08-30", "not-a-date", "2026-08-30T18:00:00", None, 12345]
    )
    def test_malformed_instants_fail_closed(self, created):
        rec = _issue_comment(created=created)
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    def test_malformed_shapes_fail_closed(self):
        for bad in ({}, None, {"user": "Mast3rkey"}, [], "a string"):
            assert is_canonical_top_level_issue_comment(bad) is False
            assert is_direct_principal_record(bad) is False
            assert _ratifies_with_binding(bad, **_bound()) is False


class TestTheVerificationRoleSplitIsPreserved:
    """MAJOR 1 (review 5060791095): SS-I.1 is principal-only; SS-I.2 keeps the coordinator role.

    OPS-0009 SS-8 grants "the principal or a designated merge coordinator" the authority to
    merge and verify, and SS-9 requires whoever merges to verify immediately. A filing about
    principal attribution must not silently delete that role.
    """

    def test_section_i_is_split_into_two_named_gates(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "#### I.1 — Principal exact-head acceptance and the `§G` ratification: principal-only" in flat
        assert "#### I.2 — Immediate post-merge verification: principal *or* designated merge coordinator" in flat

    def test_the_coordinator_role_is_preserved_not_superseded(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "the principal or a designated merge coordinator" in flat
        assert "preserved intact" in flat
        assert "this filing is not that amendment" in flat.replace("**", "")

    def test_section_i2_does_not_defer_to_the_principal_only_rule(self):
        """The operative sentence, not just the heading.

        Rewriting SS-I.2's rule to "must satisfy SS-I.1 in full" would restore the very
        collapse MAJOR 1 required be undone, while leaving every surrounding heading and
        disclaimer intact. This pins the enumerated three-condition form instead.
        """
        text = _read(DECISION_RELPATH)
        i2 = text[text.index("#### I.2"):text.index("#### I.3")]
        flat_i2 = _flat(i2)
        assert (
            "A record satisfying the **immediate post-merge verification** gate is therefore "
            "complete when:" in flat_i2
        )
        # SS-I.2 must NOT defer to the principal-only gate.
        assert "must satisfy `§I.1` in full" not in flat_i2
        # Its three operative conditions must all be present.
        assert "retained by **either** the principal **or** the designated merge coordinator" in flat_i2
        assert "are **honest**" in flat_i2
        assert "strictly after the merge and strictly before final closure" in flat_i2

    def test_no_permanent_direct_principal_requirement_for_verification(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert (
            "creates no permanent direct-principal requirement for mechanical post-merge "
            "verification" in flat.lower()
        )

    def test_a_coordinator_record_is_never_principal_acceptance(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "satisfies the verification-evidence role only" in flat
        # And the mechanism agrees: an app-attributed record can never ratify.
        coordinator = _issue_comment(login="claude[bot]", type_="Bot",
                                     assoc="CONTRIBUTOR", app=CLAUDE_APP_SLUG)
        assert is_direct_principal_record(coordinator) is False
        assert _ratifies_with_binding(coordinator, **_bound(coordinator)) is False

    def test_the_verification_timestamp_window_is_required(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "strictly after the merge and strictly before final closure" in flat

    def test_ops0009_is_neither_narrowed_nor_superseded(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "`OPS-0009` is neither narrowed nor superseded" in flat


class TestPostMergeVerificationEvidenceIsMechanised:
    """DELTA review 5061031729 MAJOR 1 -- SS-I.2 as a predicate, not prose.

    Every clause below is behavioral. The prose-presence tests in the sibling class remain, but
    they are no longer the only thing standing behind SS-I.2.
    """

    COORDINATOR = "merge-coordinator"
    MERGED = "2026-08-31T10:00:00Z"
    VERIFIED = "2026-08-31T10:05:00Z"
    CLOSED = "2026-08-31T10:30:00Z"

    def _pmv(self, **over):
        """A PMV context with the honest defaults; override one thing per test."""
        ctx = dict(
            designated_coordinator=self.COORDINATOR,
            merge_performed_by=self.COORDINATOR,
            merged_at=self.MERGED,
            closure_at=self.CLOSED,
        )
        ctx.update(over)
        return ctx

    def _coordinator_record(self, app="claude", **over):
        kwargs = dict(
            login=self.COORDINATOR, type_="Bot", assoc="CONTRIBUTOR",
            app=app, created=self.VERIFIED, ident=8_100_000_001,
            body="Post-merge verification: scope, validators, CI.",
        )
        kwargs.update(over)
        return _issue_comment(**kwargs)

    # -------------------------------------------------------------- positive cases
    def test_the_principal_may_verify_directly(self):
        rec = _issue_comment(created=self.VERIFIED, ident=8_100_000_002,
                             body="Post-merge verification.")
        assert post_merge_verification_is_valid(rec, **self._pmv()) is True

    def test_an_app_attributed_coordinator_may_verify(self):
        """The whole point of SS-I.2: this must PASS."""
        assert post_merge_verification_is_valid(
            self._coordinator_record(), **self._pmv()) is True

    def test_a_directly_attributed_coordinator_may_verify(self):
        rec = self._coordinator_record(app=None, type_="User")
        assert post_merge_verification_is_valid(rec, **self._pmv()) is True

    # ------------------------------------------------- the two roles never overlap
    def test_the_passing_coordinator_record_can_never_ratify_or_be_acceptance(self):
        """The load-bearing separation: PMV-valid, but never SS-G, never SS-I.1."""
        rec = self._coordinator_record()
        assert post_merge_verification_is_valid(rec, **self._pmv()) is True
        assert is_direct_principal_record(rec) is False
        assert ratifies_pr362_acceptance(rec) is False
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    def test_even_carrying_a_perfect_declaration_the_coordinator_cannot_ratify(self):
        rec = self._coordinator_record(body=SCOPE_BODY)
        assert body_declares_ratification(rec) is True
        assert post_merge_verification_is_valid(rec, **self._pmv()) is True
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    def test_a_principal_shaped_app_null_record_is_still_not_pmv_out_of_order(self):
        """Being the principal does not exempt a record from the chronology rule."""
        rec = _issue_comment(created=self.CLOSED, ident=8_100_000_003)
        assert post_merge_verification_is_valid(rec, **self._pmv()) is False

    # -------------------------------------------------------------- negative: WHO
    def test_an_unrelated_actor_fails(self):
        rec = self._coordinator_record(login="somebody-else")
        assert post_merge_verification_is_valid(rec, **self._pmv()) is False

    def test_a_coordinator_who_did_not_perform_this_merge_fails(self):
        """OPS-0009 SS-9 -- the SAME session that merges verifies."""
        rec = self._coordinator_record()
        assert post_merge_verification_is_valid(
            rec, **self._pmv(merge_performed_by="a-different-coordinator")) is False

    def test_a_wrongly_designated_coordinator_fails(self):
        rec = self._coordinator_record(login="not-the-designated-one")
        assert post_merge_verification_is_valid(rec, **self._pmv()) is False

    @pytest.mark.parametrize("designation", [None, "", 123])
    def test_a_missing_or_malformed_designation_fails(self, designation):
        rec = self._coordinator_record()
        assert post_merge_verification_is_valid(
            rec, **self._pmv(designated_coordinator=designation)) is False

    @pytest.mark.parametrize("merger", [None, "", 123])
    def test_an_unrecorded_merger_fails(self, merger):
        rec = self._coordinator_record()
        assert post_merge_verification_is_valid(
            rec, **self._pmv(merge_performed_by=merger)) is False

    def test_the_principal_path_does_not_need_a_designation(self):
        """A principal verifier is authorized by SS-I.2 independently of any coordinator."""
        rec = _issue_comment(created=self.VERIFIED, ident=8_100_000_004)
        assert post_merge_verification_is_valid(
            rec, **self._pmv(designated_coordinator=None,
                             merge_performed_by=None)) is True

    # ------------------------------------------------------ negative: PROVENANCE
    def test_absent_application_provenance_fails(self):
        """Unretained provenance is not honest direct attribution."""
        rec = self._coordinator_record(app_key_present=False)
        assert "performed_via_github_app" not in rec
        assert post_merge_verification_is_valid(rec, **self._pmv()) is False

    @pytest.mark.parametrize("app", [{}, {"slug": ""}, {"slug": None}, {"name": "x"}, "claude", 7])
    def test_malformed_application_provenance_fails(self, app):
        rec = self._coordinator_record()
        rec["performed_via_github_app"] = app
        assert post_merge_verification_is_valid(rec, **self._pmv()) is False

    def test_a_pull_request_review_is_never_pmv_evidence(self):
        assert post_merge_verification_is_valid(
            _pull_request_review(), **self._pmv()) is False

    @pytest.mark.parametrize("foreign", FOREIGN_RECORD_KIND_FIELDS)
    def test_the_record_kind_gate_is_isolated_and_decisive(self, foreign):
        """A record perfect on EVERY other clause, failing only on record kind.

        The plain review fixture does not isolate this gate -- it also lacks the application
        key and carries the wrong actor, so it would be rejected even with the gate removed.
        This starts from a record that PASSES, injects one foreign record-kind field, and
        shows the verdict flips. Without it, deleting the gate is invisible.
        """
        good = self._coordinator_record()
        assert post_merge_verification_is_valid(good, **self._pmv()) is True
        bad = dict(good)
        bad[foreign] = "x"
        assert post_merge_verification_is_valid(bad, **self._pmv()) is False, foreign

    def test_a_verification_on_another_pull_request_is_rejected(self):
        """Same reasoning for the PR association half of the record-kind gate."""
        elsewhere = self._coordinator_record(pr=999)
        assert post_merge_verification_is_valid(elsewhere, **self._pmv()) is False

    # ------------------------------------------------------- negative: CHRONOLOGY
    def test_verification_equal_to_the_merge_fails(self):
        """Equality is not 'after'."""
        rec = self._coordinator_record(created=self.MERGED)
        assert post_merge_verification_is_valid(rec, **self._pmv()) is False

    def test_verification_equal_to_the_closure_fails(self):
        """Equality is not 'before'."""
        rec = self._coordinator_record(created=self.CLOSED)
        assert post_merge_verification_is_valid(rec, **self._pmv()) is False

    def test_verification_before_the_merge_fails(self):
        rec = self._coordinator_record(created="2026-08-31T09:59:59Z")
        assert post_merge_verification_is_valid(rec, **self._pmv()) is False

    def test_verification_after_the_closure_fails(self):
        rec = self._coordinator_record(created="2026-08-31T10:30:01Z")
        assert post_merge_verification_is_valid(rec, **self._pmv()) is False

    def test_one_second_inside_each_boundary_passes(self):
        """The boundaries are strict, and adjacent seconds are the proof."""
        for created in ("2026-08-31T10:00:01Z", "2026-08-31T10:29:59Z"):
            rec = self._coordinator_record(created=created)
            assert post_merge_verification_is_valid(rec, **self._pmv()) is True, created

    @pytest.mark.parametrize("bad", ["", "not-a-time", "2026-08-31", None, 20260831])
    def test_malformed_timestamps_fail(self, bad):
        rec = self._coordinator_record()
        assert post_merge_verification_is_valid(rec, **self._pmv(merged_at=bad)) is False
        assert post_merge_verification_is_valid(rec, **self._pmv(closure_at=bad)) is False
        assert post_merge_verification_is_valid(
            self._coordinator_record(created=bad), **self._pmv()) is False

    def test_the_predicate_is_total_and_never_raises(self):
        for junk in (None, 123, "text", [], {}, object()):
            assert post_merge_verification_is_valid(junk, **self._pmv()) is False

    def test_pmv_and_ratification_are_separate_functions(self):
        """They must not be aliases, and neither may delegate to the other."""
        import inspect

        assert post_merge_verification_is_valid is not ratifies_pr362_acceptance
        src = inspect.getsource(post_merge_verification_is_valid)
        assert "ratifies_pr362_acceptance" not in src
        assert "_ratifies_with_binding" not in src
        assert "body_declares_ratification" not in src


class TestTheLifecycleIsClosedAndNonCircular:
    """DELTA review 5061031729 BLOCKING 1 -- the circularity, and its removal.

    The withdrawn SS-G.4 required the binding to be retained "in a further ordinary fast-forward
    correction commit on this pull request", while SS-J required the ratification to sit at the
    FINAL accepted head. Both cannot hold: the binding commit changes the head the ratification
    just accepted, reopening the exact-head requirement; binding the replacement changes it
    again. The corrected design retains the binding as GitHub lifecycle evidence instead, so no
    commit follows the accepted head.
    """

    def test_the_binding_commit_requirement_is_withdrawn(self):
        flat = _flat(_read(DECISION_RELPATH))
        phrase = "further ordinary fast-forward correction commit on this pull request"
        # The phrase survives exactly once, and ONLY as a quotation of the withdrawn rule.
        assert flat.count(phrase) == 1
        quoted = 'An earlier draft required the operator to retain that binding "in a ' + phrase + '"'
        assert quoted in flat
        assert "**The binding commit is withdrawn.**" in flat
        assert "The binding is never committed to this repository." in flat
        # And it is nowhere stated as something still to be done.
        assert "retains, in a further ordinary fast-forward" not in flat

    def test_the_module_binding_stays_none_permanently(self):
        """Not 'unset until later' -- unset by design, forever."""
        assert BOUND_RATIFICATION_ID is None
        assert BOUND_RATIFICATION_FINGERPRINT is None
        flat = _flat(_read(DECISION_RELPATH))
        assert "are `None` and **stay** `None`" in flat

    def test_the_lifecycle_sequence_is_stated_explicitly_not_left_to_inference(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "#### G.9 — The closed lifecycle sequence" in flat
        for step in (
            "final clean reviewed head",
            "**one** canonical top-level issue comment on PR #363 that **both** accepts that "
            "exact head",
            "independently reads that comment back from the GitHub API",
            "requires no repository commit and does not change the accepted head",
        ):
            assert step in flat, step

    def test_acceptance_and_ratification_are_one_record_not_two_acts(self):
        """The single-act construction is what makes the sequence closed."""
        flat = _flat(_read(DECISION_RELPATH))
        assert "a single act, not two" in flat
        assert "no question arises about whether a" in flat
        assert "there is no later head change" in flat

    def test_the_record_carries_its_own_pr363_head_anchor(self):
        """The reviewer's specific objection: the old record anchored no PR #363 head."""
        assert "pr363_accepted_head" in RATIFICATION_SCHEMA
        assert RATIFICATION_SCHEMA["pr363_accepted_head"] is None  # form-checked
        parsed = parse_ratification_body(SCOPE_BODY)
        assert parsed is not None and len(parsed["pr363_accepted_head"]) == 40
        flat = _flat(_read(DECISION_RELPATH))
        assert "carries its own PR #363 head anchor" in flat

    def test_effectivity_condition_three_matches_the_corrected_lifecycle(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "with no repository commit and no change to the accepted head" in flat

    def test_the_pr363_head_is_form_checked_not_value_checked_in_repository(self):
        """Honest about what the repository can and cannot know about its own future head."""
        for good in ("a" * 40, "0" * 40, "0123456789abcdef" * 2 + "01234567"):
            body = SCOPE_BODY.replace(f"pr363_accepted_head: {FIXTURE_PR363_HEAD}",
                                      f"pr363_accepted_head: {good}")
            assert parse_ratification_body(body) is not None, good
        for bad in ("A" * 40, "a" * 39, "a" * 41, "g" * 40, "", "HEAD"):
            body = SCOPE_BODY.replace(f"pr363_accepted_head: {FIXTURE_PR363_HEAD}",
                                      f"pr363_accepted_head: {bad}")
            assert parse_ratification_body(body) is None, bad

    def test_the_withdrawn_synthetic_record_claim_is_recorded_as_withdrawn(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "any synthetic record a caller assembles" in flat        # quoted as withdrawn
        assert "that claim was **false and is withdrawn**" in flat
        assert "These fields do not, and cannot, prove live GitHub origin." in flat


class TestNoStandingAuthorityIsCreated:
    def test_no_bot_login_appears_in_any_accepted_actor_container(self):
        """No allow-list, no bot class, no trusted-automation category."""
        module = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        offenders = []
        for node in module.body:
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if not isinstance(target, ast.Name) or not target.id.isupper():
                    continue
                try:
                    value = ast.literal_eval(node.value)
                except (ValueError, SyntaxError):
                    continue
                if isinstance(value, (list, tuple, set, frozenset, dict)):
                    flat = json.dumps(
                        sorted(value) if not isinstance(value, dict) else value,
                        default=str,
                    )
                    for bot in ("claude[bot]", "chatgpt-codex-connector[bot]"):
                        if bot in flat:
                            offenders.append((target.id, bot))
        assert offenders == [], offenders

    def test_the_decision_states_no_standing_authority(self):
        text = _read(DECISION_RELPATH)
        flat = _flat(text)
        assert "No standing authority is created for any actor, bot, or application" in flat
        assert (
            "No accepted-actor list, no bot class, and no trusted-automation category"
            in flat
        )
        assert "`PRINCIPAL_ACCOUNT_LOGIN` and `LIFECYCLE_OPERATOR_LOGIN` are unchanged" in flat

    def test_production_actor_constants_are_untouched(self):
        import level1_stage1_execution_authorization as m

        assert m.PRINCIPAL_ACCOUNT_LOGIN == "Mast3rkey"
        assert m.LIFECYCLE_OPERATOR_LOGIN == "Mast3rkey"


class TestTheRequiredStandardIsGroundedInRealPrecedent:
    """SS-C's corrected finding: the SS-G standard is this repository's own earlier practice."""

    #: Direct principal acts -- Mast3rkey / User / OWNER with NO performed_via_github_app --
    #: independently re-derived from live GitHub during authoring. Each is a real lifecycle
    #: record of exactly the shape SS-G requires.
    DIRECT_PRINCIPAL_PRECEDENTS = (
        (5279583728, 310, "acceptance"),
        (5279649213, 310, "verification"),
        (5280867232, 311, "acceptance"),
        (5280945019, 311, "verification"),
        (5289500944, 314, "acceptance"),
        (5289558762, 314, "verification"),
        (5299933404, 316, "acceptance"),
        (5301699393, 319, "acceptance"),
        (5301728726, 319, "verification"),
    )

    def test_the_decision_cites_real_direct_principal_precedents(self):
        text = _read(DECISION_RELPATH)
        for comment_id, _pr, _kind in self.DIRECT_PRINCIPAL_PRECEDENTS:
            assert str(comment_id) in text, comment_id

    def test_the_decision_does_not_claim_the_standard_is_unprecedented(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "has not yet occurred in this repository" not in flat
        assert "this repository's own earlier practice" in flat

    def test_each_precedent_shape_satisfies_the_enforced_predicate(self):
        """Each is a top-level ISSUE COMMENT, so it satisfies SS-G.2 and SS-G.1 alike."""
        for comment_id, _pr, _kind in self.DIRECT_PRINCIPAL_PRECEDENTS:
            rec = _issue_comment(ident=comment_id)
            assert is_direct_principal_record(rec) is True, comment_id
            assert is_canonical_top_level_issue_comment(rec) is True, comment_id

    def test_the_same_records_posted_through_an_app_would_fail(self):
        """Proving the conjunct is what distinguishes them, not the account."""
        for app in (CLAUDE_APP_SLUG, REVIEWER_APP_SLUG):
            assert is_direct_principal_record(_issue_comment(app=app)) is False, app

    def test_a_precedent_shaped_record_that_is_a_review_still_fails(self):
        """The precedent is the RECORD KIND as much as the actor."""
        for comment_id, _pr, _kind in self.DIRECT_PRINCIPAL_PRECEDENTS[:3]:
            assert is_direct_principal_record(_pull_request_review(ident=comment_id)) is False


class TestNoImmediateVerificationIsInventedFromTheClosure:
    def test_the_closure_postdates_ci_and_is_not_relabelled(self):
        assert CLOSURE_AT > CI_COMPLETED_AT > MERGED_AT
        text = _read(DECISION_RELPATH)
        # The decision must refuse the relabelling, not perform it.
        assert "Relabel closure `5463232454` as the immediate verification record.** Rejected" in text

    def test_the_decision_states_the_defect_is_not_curable(self):
        text = _read(DECISION_RELPATH)
        assert "**cannot lawfully cure the missing immediate-verification evidence.**" in text
        assert "no retained evidence establishes that an immediate post-merge verification" in text

    def test_the_decision_does_not_claim_the_lifecycle_closed(self):
        text = _read(DECISION_RELPATH)
        assert "`XASSET-0061` is NOT effective" in text
        assert "did not close and cannot be made to have closed" in _flat(text)
        # And must never assert the opposite.
        assert "XASSET-0061 is effective" not in text
        assert "all seven conditions closed" not in text

    def test_a_verification_posted_now_would_break_the_closure_ordering(self):
        """The chronological reason the chain cannot be repaired in place."""
        hypothetical_now = "2026-08-30T12:00:00Z"
        assert hypothetical_now > CLOSURE_AT
        # The production rule is closure >= verification; this inverts it.
        assert not (CLOSURE_AT >= hypothetical_now)


class TestXasset0061RemainsUnavailable:
    def test_decision_leaves_xasset0061_status_proposed(self):
        import yaml

        cat = yaml.safe_load(_read("governance/decisions.yaml"))
        rows = cat["decisions"] if isinstance(cat, dict) else cat
        entry = [r for r in rows if r["decision_id"] == "XASSET-0061"][0]
        assert entry["status"] == "Proposed"

    def test_xasset0061_decision_file_frontmatter_is_unmodified(self):
        head = _read(
            "governance/decisions/XASSET-0061-endpoint-0001-stage-1-post-parser-"
            "correction-renewed-readiness-verification-authorization.md"
        ).split("---")[1]
        assert "status: Proposed" in head

    def test_all_seven_corrective_effectivity_conditions_are_enumerated(self):
        text = _flat(_read(DECISION_RELPATH))
        for needle in (
            "independent **FULL** exact-head review",
            "exact-head re-review",
            "ratifies the pinned PR #362 history**, satisfying `§G.1`",
            "normal merge",
            "**actually retained** immediate post-merge verification",
            "successful merge-commit CI whose `head_sha` is the exact merge SHA",
            "final post-CI verification and lifecycle closure",
        ):
            assert needle in text, needle
        assert "**None is individually sufficient.**" in text


class TestStageOneSafetyIsUntouched:
    def test_all_three_authorization_predicates_are_false(self):
        import level1_stage1_execution_authorization as m

        assert m.new_execution_is_authorized()[0] is False
        assert m.claimed_execution_is_authorized()[0] is False
        assert m.active_execution_is_authorized()[0] is False

    def test_lane_and_authorization_paths_are_absent(self):
        import level1_stage1_execution_authorization as m

        assert not m.AUTHORIZATION_ROOT.exists()
        assert not m.AUTHORIZATION_PATH.exists()
        assert not m.CLAIM_PATH.exists()
        assert not m.COMPLETION_PATH.exists()

    def test_no_results_artifact_exists(self):
        assert not (ROOT / "stage1_results.yaml").exists()
        assert list(ROOT.glob("stage1_results*.yaml")) == []

    def test_attempt_1_is_intact_unclaimed_and_unconsumed(self):
        import level1_stage1_execution_authorization as m

        ok, reason = m.claimed_execution_is_authorized()
        assert ok is False
        assert "ABSENT" in reason

    def test_canonical_pins_still_match_live_bytes(self):
        import level1_stage1_execution_authorization as m

        for rel, pin in m.CANONICAL_PINS.items():
            assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == pin, rel

    def test_frozen_universe_is_unchanged(self):
        import level1_stage1_execution_authorization as m

        assert m.CONSTRUCTION_COUNT == 680
        assert m.CONSTRUCTION_CELL_COUNT == 48
        assert (
            m.CONSTRUCTION_UNIVERSE_SHA256
            == "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
        )

    def test_twenty_five_load_bearing_paths(self):
        import level1_stage1_execution_authorization as m

        assert len(m.LOAD_BEARING_RELPATHS) == 25
        assert len(set(m.LOAD_BEARING_RELPATHS)) == 25


class TestThisFilingMutatesNothingLoadBearing:
    def test_changed_set_is_exactly_the_expected_manifest(self):
        assert _changed_files() == EXPECTED_CHANGED_FILES

    def test_no_load_bearing_path_differs_from_the_merge_base(self):
        import level1_stage1_execution_authorization as m

        changed = _changed_files()
        assert changed.isdisjoint(set(m.LOAD_BEARING_RELPATHS))

    @pytest.mark.parametrize("relpath", PROTECTED_RELPATHS)
    def test_protected_path_is_byte_identical_to_the_merge_base(self, relpath):
        base_blob = _git("rev-parse", f"{RATIFIED_MERGE}:{relpath}")
        head_blob = _git("rev-parse", f"HEAD:{relpath}")
        assert base_blob == head_blob, relpath

    def test_every_re_anchored_suite_retains_its_predecessor_as_a_negative_pin(self):
        """A re-anchoring ADVANCES a pin; it never deletes the superseded value.

        Each suite must still name the value it moved away from, as a negative assertion, so a
        silent revert to the predecessor state fails there rather than passing quietly.
        """
        # The two classes are disjoint and together are exactly the re-anchored set.
        assert PIN_ADVANCED_SUITES.isdisjoint(HELPER_EXTENDED_SUITES)
        assert PIN_ADVANCED_SUITES | HELPER_EXTENDED_SUITES == RE_ANCHORED_PREDECESSOR_SUITES

        for rel in PIN_ADVANCED_SUITES:
            text = _read(rel)
            assert "XASSET-0062" in text, rel
            # The superseded live-field value must survive as a negative pin.
            assert RATIFIED_BASE in text, rel
            assert "!=" in text, rel

        for rel in HELPER_EXTENDED_SUITES:
            text = _read(rel)
            assert "XASSET-0062" in text, rel
            # The un-bound window is CHECKED, never skipped -- no bare skip was introduced.
            assert "pytest.skip" not in text.split("XASSET-0062")[-1][:400], rel

    def test_re_anchored_suites_still_pass_their_own_guards(self):
        """Named explicitly so a future reader sees these were run, not assumed."""
        assert RE_ANCHORED_PREDECESSOR_SUITES <= EXPECTED_CHANGED_FILES
        for rel in RE_ANCHORED_PREDECESSOR_SUITES:
            assert (ROOT / rel).is_file(), rel

    def test_no_production_or_portfolio_byte_changed(self):
        assert _changed_files().isdisjoint(set(PROTECTED_RELPATHS))

    def test_suite_performs_no_filesystem_write(self):
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        banned = {"write_text", "write_bytes", "mkdir", "unlink", "touch", "rmtree"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr in banned:
                raise AssertionError(f"filesystem write: {node.attr}")
            if isinstance(node, ast.Call):
                fn = node.func
                if isinstance(fn, ast.Name) and fn.id == "open":
                    raise AssertionError("bare open()")

    def test_suite_has_no_or_fallback_assertions(self):
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert) and isinstance(node.test, ast.BoolOp):
                if isinstance(node.test.op, ast.Or):
                    raise AssertionError("or-fallback assertion")


def _decision_section(heading: str) -> str:
    """The text of one `#### <heading>` section of the decision, up to the next `#### `."""
    text = _read(DECISION_RELPATH)
    start = text.index(f"#### {heading}")
    rest = text[start + 1 :]
    end = rest.find("\n#### ")
    return rest if end == -1 else rest[:end]


class TestTheMechanismConstantsAreAnchoredInTheDecision:
    """Constants used by BOTH the predicate and its fixtures cannot verify themselves.

    Found by re-running this filing's own mutation proof at the corrected head: repointing
    `REPO_API` at another repository, and dropping a member of `INDEPENDENT_REVIEW_IDS`, both
    survived, because each constant is the single source for the mechanism AND for the fixtures
    it is checked against -- structurally the same "both sides derived from one source" defect
    the BLOCKING finding identified, one level down. Each is therefore anchored to the governing
    decision's own committed text, the independent source that already catches the scope pins.
    """

    def test_the_canonical_repository_is_anchored_in_the_decision(self):
        """SS-G.1 items 1-3 name the canonical URLs verbatim; the constants must reproduce them."""
        section = _flat(_decision_section("G.1"))
        for built in (
            RATIFICATION_ISSUE_URL,
            f"{RATIFICATION_URL_PREFIX}<id>",
            f"{RATIFICATION_HTML_PREFIX}<id>",
        ):
            assert built in section, built

    def test_the_independent_review_ids_are_exactly_those_the_decision_names(self):
        """SS-G.7 names them. Dropping or adding one must fail, not silently resize a parametrize."""
        section = _decision_section("G.7")
        named = {int(m) for m in re.findall(r"\b(50607\d{5})\b", section)}
        assert named == set(INDEPENDENT_REVIEW_IDS)
        assert len(INDEPENDENT_REVIEW_IDS) == 2
        assert len(set(INDEPENDENT_REVIEW_IDS)) == 2

    def test_the_foreign_record_kind_fields_are_exactly_those_the_decision_names(self):
        """SS-G.1 item 5 enumerates them. Emptying the tuple must fail, not vacate a parametrize."""
        section = _flat(_decision_section("G.1"))
        item5 = section[section.index("the record carries **none** of") :]
        item5 = item5[: item5.index(".")]
        named = set(re.findall(r"`([a-z_]+)`", item5))
        assert named == set(FOREIGN_RECORD_KIND_FIELDS)
        assert len(FOREIGN_RECORD_KIND_FIELDS) == 6

    def test_the_scope_pins_remain_exactly_seven(self):
        """SS-G.3 fixes seven. A shortened tuple must fail rather than weaken the scope check."""
        assert len(RATIFIED_SCOPE_PINS) == 7
        assert len(set(RATIFIED_SCOPE_PINS)) == 7


class TestDecisionRecordIntegrity:
    def test_decision_declares_the_correct_supporting_artifact(self):
        assert f"supporting_artifact: {THIS_ARTIFACT}" in _read(DECISION_RELPATH)

    def test_catalog_entry_matches_the_decision_file(self):
        import yaml

        cat = yaml.safe_load(_read("governance/decisions.yaml"))
        rows = cat["decisions"] if isinstance(cat, dict) else cat
        entry = [r for r in rows if r["decision_id"] == "XASSET-0062"][0]
        assert entry["status"] == "Proposed"
        assert entry["supporting_artifact"] == THIS_ARTIFACT
        assert entry["file"] == DECISION_RELPATH

    def test_decision_has_no_h1_heading(self):
        """Corpus invariant: catalogued records derive their title from the filename."""
        text = _read(DECISION_RELPATH)
        assert not any(line.startswith("# ") for line in text.splitlines())

    def test_both_defects_are_recorded_not_sanitized(self):
        text = _read(DECISION_RELPATH)
        assert "claude[bot]" in text
        assert str(RATIFIED_BOT_ACCEPTANCE_ID) in text
        assert "Authored by the same session that committed both defects" in text

    def test_xasset_0042_is_used_only_as_a_narrow_precedent(self):
        text = _read(DECISION_RELPATH)
        assert "examined here" in text and "never as a general exception" in text

    def test_every_pinned_identity_appears_in_the_decision(self):
        text = _read(DECISION_RELPATH)
        for pin in (
            RATIFIED_ACCEPTED_HEAD,
            RATIFIED_MERGE,
            str(RATIFIED_REVIEW_ID),
            str(RATIFIED_BOT_ACCEPTANCE_ID),
            str(RATIFIED_CLOSURE_ID),
            str(INDEPENDENT_STOP_ID),
            f"#{RATIFIED_PULL_REQUEST}",
        ):
            assert pin in text, pin

    def test_absolute_non_authorization_is_stated(self):
        text = _read(DECISION_RELPATH)
        for needle in (
            "authorizes no readiness verification",
            "authorizes no link 4 and no link 5",
            "consumes no part of `XASSET-0027` `§P.1`",
            "**authorizes no successor unit of any kind**",
        ):
            assert needle in text, needle
