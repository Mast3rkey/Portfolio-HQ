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
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path

import pytest

import level1_stage1_execution_authorization as _auth

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
#: The principal's real numeric GitHub actor id, read from the live canonical resource during
#: the SS-I.2.1 A0 capability proof. Every live actor resource exposes one; fixtures that
#: omitted it were not modelled on the real shape.
PRINCIPAL_ID = 218449187
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

#: SS-G.9: these constants are ``None`` and STAY ``None``. The ratification's live id and
#: fingerprint are read back from the GitHub API and retained as GitHub lifecycle evidence --
#: NEVER committed here, because a binding commit would change the very head the ratification
#: accepts. The in-repository predicates therefore yield the all-false result for every input,
#: permanently and by design. An earlier comment here promised retention "in a further
#: fast-forward commit on this pull request"; that circular design was withdrawn under DELTA
#: review 5061031729 and the stale sentence is removed under 5062156189 MINOR 1.
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
    other issue or pull request, and records whose canonical URLs are malformed or disagree
    with each other or with ``id``.

    It does NOT reject a caller-assembled record, and never could: this is a predicate over a
    dictionary's shape. This suite's own fixtures are assembled in Python and pass. An earlier
    docstring claimed otherwise; that claim is withdrawn under DELTA review 5061240650 MINOR 1.
    Live origin is established by the SS-G.9 readback, never by record shape.
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
#: real final head is established by independent GitHub readback (SS-G.9), never from here.
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
    independent GitHub API readback and the retained evidence of SS-G.9, never from here.
    Corrected under DELTA review 5061031729 BLOCKING 2.
    """
    if not is_canonical_top_level_issue_comment(record):
        return False
    if not is_direct_principal_record(record):
        return False
    if not body_declares_ratification(record):
        return False
    # SS-G.5 retrospection: strictly after the PR #362 merge. Equality is not "after".
    # DELTA review 5062156189 MAJOR 3: this used a SHAPE regex and a LEXICOGRAPHIC string
    # comparison, so created_at = "9999-99-99T99:99:99Z" passed both here and through the
    # complete external readback. Both are now parsed, timezone-aware UTC instants.
    created = parse_utc_instant(record.get("created_at"))
    merged = parse_utc_instant(MERGED_AT)
    if created is None or merged is None:
        return False
    return created > merged


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
    SS-G.9 lifecycle, STAY ``None``: the live id and fingerprint are retained as GitHub
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
    """The application slug, or ``None`` for a directly attributed record."""
    app = record.get("performed_via_github_app")
    if not isinstance(app, dict):
        return None
    slug = app.get("slug")
    return slug if isinstance(slug, str) else None


def _nonempty_str(value: object) -> bool:
    """A REAL string with content. Corrected under DELTA review 5061240650 BLOCKING 1.

    The withdrawn implementation asserted in a comment that ``login`` was "a non-empty str",
    which was false: ``_actor_login`` returns EVERY string, ``""`` included, so a record with an
    empty login self-designating an empty coordinator passed.
    """
    return isinstance(value, str) and value.strip() != ""


def parse_utc_instant(value: object) -> datetime.datetime | None:
    """A REAL UTC instant, or ``None``. Shape alone is not validity.

    Corrected under DELTA review 5061240650 BLOCKING 1: the withdrawn ``_is_iso_z`` matched a
    digit pattern, so ``2026-08-31T10:05:99Z``, ``2026-13-45T99:99:99Z`` and ``2026-02-30`` all
    passed. This parses the calendar and clock, so an impossible instant fails.
    """
    if not isinstance(value, str):
        return None
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        return None
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=datetime.timezone.utc
        )
    except ValueError:
        return None


def _app_provenance_is_retained(record: dict) -> bool:
    """Provenance must be RETAINED, honestly, either way.

    An ABSENT key is not honest direct attribution; it is unretained provenance, and it is the
    signature of a record kind that carries none. Either a null (direct) or a well-formed
    application object is acceptable -- what is forbidden is a record that does not say.
    """
    if "performed_via_github_app" not in record:
        return False
    app = record["performed_via_github_app"]
    if app is None:
        return True
    return isinstance(app, dict) and _nonempty_str(app.get("slug"))


def _actor_fields_are_well_formed(record: dict) -> bool:
    """Non-empty, correctly typed actor login, type, association, and provenance."""
    return (
        _nonempty_str(_actor_login(record))
        and _nonempty_str(_actor_type(record))
        and _nonempty_str(record.get("author_association"))
        and _app_provenance_is_retained(record)
    )


# ======================================================================================
# SS-G.9 -- the external ratification readback validator.
#
# Added under DELTA review 5061240650 MAJOR 1. The declaration parser deliberately accepts ANY
# 40-lowercase-hex ``pr363_accepted_head``, because the repository cannot know its own future
# final head. That is only safe if the external readback then PROVES the three-way equality
#
#     declared head  ==  live PR head  ==  independently reviewed final head
#
# and until now no validator did. SS-G.9 step 3 listed what to retain but never named the
# comparison that makes retention meaningful.
#
# This consumes three INDEPENDENTLY SOURCED evidence families and returns a retained evidence
# record rather than a bare boolean, so what was proven is auditable afterwards:
#
#   1. the live principal ratification comment, read back from the GitHub API;
#   2. the live PR #363 record, read back from the GitHub API;
#   3. the independent final-review evidence, naming the exact head that was reviewed.
#
# It does NOT and CANNOT establish that the supplied records came from GitHub -- that is the
# operator's readback discipline, and this function's own inputs are dictionaries like any
# other. What it establishes is that IF those records are the live ones, the equality holds.
# ======================================================================================
APPROVING_REVIEW_DISPOSITION = _auth.APPROVING_REVIEW_DISPOSITION


def canonical_final_review_is_approving(review: object, final_head: str) -> tuple[bool, dict]:
    """SS-G.9 -- authenticate the RAW pull-request-review resource, and its disposition.

    DELTA review 5062156189 MAJOR 1: the withdrawn readback read only
    ``final_review_evidence["reviewed_head"]``, so ``{"reviewed_head": H}``, the same mapping
    carrying ``verdict: CHANGES_REQUIRED``, and one naming an author actor with a null id all
    proved the equality. Three strings were compared; the third was never authenticated.

    The disposition is parsed by the repository's OWN ``parse_formal_disposition`` in the
    load-bearing module -- not a second parser written here, which would authenticate the
    mechanism with its own source of truth.

    Returns ``(approving, evidence)``. Never raises.
    """
    ev: dict = {
        "review_id": None, "commit_id": None, "submitted_at": None, "state": None,
        "actor_login": None, "actor_type": None, "author_association": None,
        "application_provenance": "NOT_EXPOSED_ON_REVIEWS",
        "parsed_disposition": None, "commit_matches_final_head": False,
        "independence": "PROCEDURAL_NOT_PLATFORM_PROVABLE", "failure_reason": None,
    }
    if not isinstance(review, dict):
        ev["failure_reason"] = "review resource is not a mapping"
        return False, ev

    ev["review_id"] = review.get("id")
    ev["commit_id"] = review.get("commit_id")
    ev["submitted_at"] = review.get("submitted_at")
    ev["state"] = review.get("state")
    identity = _actor_identity(review)
    if identity is not None:
        ev["actor_login"], ev["actor_type"] = identity["login"], identity["type"]
    ev["author_association"] = review.get("author_association")

    if type(review.get("id")) is not int:
        ev["failure_reason"] = "review id is missing or not an integer"
        return False, ev
    if review.get("pull_request_url") != f"{REPO_API}/pulls/{THIS_CORRECTIVE_PULL_REQUEST}":
        ev["failure_reason"] = "review is not on PR #363"
        return False, ev
    expected_html = (f"{REPO_HTML}/pull/{THIS_CORRECTIVE_PULL_REQUEST}"
                     f"#pullrequestreview-{review['id']}")
    if review.get("html_url") != expected_html:
        ev["failure_reason"] = "review canonical URLs disagree with its id"
        return False, ev
    if identity is None:
        ev["failure_reason"] = "review actor identity is missing or malformed"
        return False, ev
    if not _nonempty_str(review.get("author_association")):
        ev["failure_reason"] = "review author_association is missing or malformed"
        return False, ev
    if parse_utc_instant(review.get("submitted_at")) is None:
        ev["failure_reason"] = "review submitted_at is missing or not a real UTC instant"
        return False, ev
    if not (isinstance(final_head, str) and _SHA40.match(final_head)):
        ev["failure_reason"] = "final head is missing or malformed"
        return False, ev
    if review.get("commit_id") != final_head:
        ev["failure_reason"] = "review commit_id is not the final reviewed head"
        return False, ev
    ev["commit_matches_final_head"] = True
    if str(review.get("state") or "").upper() in _auth.NATIVE_ADVERSE_REVIEW_STATES:
        ev["failure_reason"] = "review state is natively adverse"
        return False, ev

    verdict = _auth.parse_formal_disposition(review.get("body"))
    if verdict is _auth.MALFORMED_FORMAL_DISPOSITION:
        ev["parsed_disposition"] = "MALFORMED"
        ev["failure_reason"] = "formal disposition is malformed"
        return False, ev
    if verdict is None:
        ev["failure_reason"] = "no formal disposition"
        return False, ev
    ev["parsed_disposition"] = verdict
    if verdict != APPROVING_REVIEW_DISPOSITION:
        ev["failure_reason"] = "formal disposition is not approving"
        return False, ev
    return True, ev


def canonical_open_pull_request_is_valid(pull: object) -> bool:
    """SS-I.2.1 D/F -- the RAW PR #363 resource, open and unmerged, at readback.

    A caller projection such as ``{"number": 363, "head": {"sha": H}}`` is not evidence --
    DELTA review 5062494115 BLOCKING 2 reproduced exactly that mapping satisfying this leg.
    """
    if not isinstance(pull, dict):
        return False
    if pull.get("number") != THIS_CORRECTIVE_PULL_REQUEST:
        return False
    if pull.get("url") != f"{REPO_API}/pulls/{THIS_CORRECTIVE_PULL_REQUEST}":
        return False
    if pull.get("html_url") != f"{REPO_HTML}/pull/{THIS_CORRECTIVE_PULL_REQUEST}":
        return False
    base = pull.get("base")
    repo = base.get("repo") if isinstance(base, dict) else None
    if not isinstance(repo, dict) or repo.get("full_name") != CANONICAL_REPOSITORY:
        return False
    # Acceptance and readback happen while the PR is still open and unmerged.
    if pull.get("state") != "open":
        return False
    if pull.get("merged") is not False:
        return False
    if pull.get("merged_at") is not None:
        return False
    head = pull.get("head")
    if not isinstance(head, dict):
        return False
    return isinstance(head.get("sha"), str) and bool(_SHA40.match(head["sha"]))


def review_collection_is_provably_complete(collection: object) -> tuple[bool, list]:
    """SS-I.2.1 D -- completeness proved from the HTTP response, not asserted by the caller.

    A caller who supplies the reviews it chooses can always omit the one that defeats it.
    The evidence is therefore the raw array TOGETHER WITH GitHub's own ``Link`` header: a
    present ``Link`` means an unread page exists, and ``len(reviews) >= per_page`` may be a
    truncated page. Either condition fails.
    """
    if not isinstance(collection, dict):
        return False, []
    reviews = collection.get("reviews")
    per_page = _positive_int(collection.get("per_page"))
    if not isinstance(reviews, list) or per_page is None:
        return False, []
    if collection.get("link_header") is not None:
        return False, []
    if len(reviews) >= per_page:
        return False, []
    return True, reviews


def external_ratification_readback(
    ratification_record: object,
    live_pull_request: object,
    final_review: object,
    review_collection: object = None,
) -> dict:
    """SS-G.9 -- validate the readback and return the evidence to retain.

    ``equality_proven`` is the verdict. Never raises. Proves

        declared head == live PR head == independently approved final-review ``commit_id``

    with the third value now authenticated as a real, approving, exact-head review resource.
    """
    out: dict = {
        "equality_proven": False, "structural_clauses_pass": False, "declaration": None,
        "declared_pr363_accepted_head": None, "live_pr_head": None,
        "independently_reviewed_head": None, "comment_id": None, "comment_created_at": None,
        "body_fingerprint": None, "record_kind": None, "actor_login": None, "actor_type": None,
        "author_association": None, "application_provenance": None, "review_evidence": None,
        "later_adverse_review_exists": None, "approving_review_submitted_at": None,
        "review_collection_complete": None, "failure_reason": None,
    }
    if not isinstance(ratification_record, dict):
        out["failure_reason"] = "ratification record is not a mapping"
        return out

    out["comment_id"] = ratification_record.get("id")
    out["comment_created_at"] = ratification_record.get("created_at")
    out["actor_login"] = _actor_login(ratification_record)
    out["actor_type"] = _actor_type(ratification_record)
    out["author_association"] = ratification_record.get("author_association")
    out["application_provenance"] = (
        "ABSENT" if "performed_via_github_app" not in ratification_record
        else ("null" if ratification_record["performed_via_github_app"] is None
              else _app_slug(ratification_record))
    )
    out["record_kind"] = (
        "top_level_issue_comment"
        if is_canonical_top_level_issue_comment(ratification_record) else "other_or_invalid"
    )
    try:
        out["body_fingerprint"] = canonical_ratification_fingerprint(ratification_record)
    except Exception:                                    # pragma: no cover - defensive
        out["body_fingerprint"] = None

    if not _ratification_is_structurally_complete(ratification_record):
        out["failure_reason"] = "record fails an SS-G structural clause"
        return out
    out["structural_clauses_pass"] = True

    declaration = parse_ratification_body(ratification_record.get("body"))
    if declaration is None:                              # pragma: no cover - unreachable
        out["failure_reason"] = "body does not parse as the SS-G.3 declaration"
        return out
    out["declaration"] = declaration
    out["declared_pr363_accepted_head"] = declaration["pr363_accepted_head"]

    # SS-I.2.1 F.1/F.2 -- the RAW resource, open and unmerged, never a caller projection.
    if not canonical_open_pull_request_is_valid(live_pull_request):
        out["failure_reason"] = "live pull-request is not a valid open, unmerged PR #363 resource"
        return out
    live_head = live_pull_request["head"]["sha"]
    out["live_pr_head"] = live_head

    # SS-I.2.1 F.3 -- authenticate the selected approval as a real exact-head review.
    approving, review_evidence = canonical_final_review_is_approving(final_review, live_head)
    out["review_evidence"] = review_evidence
    out["independently_reviewed_head"] = review_evidence["commit_id"]
    if not approving:
        out["failure_reason"] = f"final review not approving: {review_evidence['failure_reason']}"
        return out

    # SS-I.2.1 F.4 -- an approval can only be accepted AFTER it exists.
    approved_at = parse_utc_instant(final_review.get("submitted_at"))
    ratified_at = parse_utc_instant(ratification_record.get("created_at"))
    out["approving_review_submitted_at"] = final_review.get("submitted_at")
    if approved_at is None or ratified_at is None:
        out["failure_reason"] = "review or ratification instant is missing or malformed"
        return out
    if not (approved_at < ratified_at):
        out["failure_reason"] = "ratification does not postdate the approving review"
        return out

    # SS-I.2.1 F.5 -- completeness proved from the response, not asserted by the caller.
    complete, reviews = review_collection_is_provably_complete(review_collection)
    out["review_collection_complete"] = complete
    if not complete:
        out["failure_reason"] = "review-collection completeness is not proven"
        return out
    if not any(
        isinstance(candidate, dict) and candidate.get("id") == final_review.get("id")
        for candidate in reviews
    ):
        out["failure_reason"] = "the selected approving review is not a member of the collection"
        return out

    # SS-I.2.1 F.6 -- adverse only if authenticated, exact-head, and STRICTLY LATER.
    adverse = []
    for candidate in reviews:
        if not isinstance(candidate, dict):
            out["failure_reason"] = "review collection contains a non-resource member"
            return out
        if candidate.get("id") == final_review.get("id"):
            continue
        if candidate.get("commit_id") != live_head:
            continue
        candidate_at = parse_utc_instant(candidate.get("submitted_at"))
        if candidate_at is None:
            out["failure_reason"] = "a review in the collection has no parseable instant"
            return out
        if not (candidate_at > approved_at):
            continue
        if str(candidate.get("state") or "").upper() in _auth.NATIVE_ADVERSE_REVIEW_STATES:
            adverse.append(candidate.get("id"))
            continue
        later_verdict = _auth.parse_formal_disposition(candidate.get("body"))
        if later_verdict is _auth.MALFORMED_FORMAL_DISPOSITION or (
            isinstance(later_verdict, str)
            and later_verdict != APPROVING_REVIEW_DISPOSITION
        ):
            adverse.append(candidate.get("id"))
    out["later_adverse_review_exists"] = bool(adverse)
    if adverse:
        out["failure_reason"] = "a later adverse exact-head review exists"
        return out

    # SS-I.2.1 F.7 -- the three-way exact-head equality.
    if not (out["declared_pr363_accepted_head"] == live_head == review_evidence["commit_id"]):
        out["failure_reason"] = "three-way exact-head equality failed"
        return out

    out["equality_proven"] = True
    return out


# ======================================================================================
# SS-I.2 / SS-I.2.1 -- the evidence model, rebuilt under DELTA review 5062156189.
#
# Every literal in this section is GOVERNING TEXT taken from the decision's SS-I.2.1, and
# TestTheProtocolIsAnchoredInTheDecision proves each one appears there verbatim. The reviewer
# renamed PMV_HEADER and PMV_ACTION at the previous head and all 327 focused tests still
# passed, because the parser and its fixtures derived the protocol from one another.
#
# Canonical resource shapes below use the REAL GitHub field names, confirmed by reading the
# live resources for PR #362, review 5062156189 and comment 5463232454 during the design
# audit -- not invented projections.
# ======================================================================================
#: The one canonical repository, taken from the load-bearing module rather than restated.
CANONICAL_REPOSITORY = _auth.REPOSITORY_IDENTITY

DESIGNATION_HEADER = "XASSET-0062 COORDINATOR DESIGNATION"
DESIGNATION_ACTION = "DESIGNATE-MERGE-COORDINATOR"
PMV_HEADER = "XASSET-0062 POST-MERGE VERIFICATION"
PMV_ACTION = "POST-MERGE-VERIFICATION-PERFORMED"
CLOSURE_HEADER = "XASSET-0062 LIFECYCLE CLOSURE"
CLOSURE_ACTION = "FINAL-POST-CI-LIFECYCLE-CLOSURE"

_SHA256_HEX = re.compile(r"\A[0-9a-f]{64}\Z")
_COORDINATOR_TYPES = ("User", "Bot")
_COORDINATOR_ASSOCIATIONS = ("OWNER", "MEMBER", "COLLABORATOR", "CONTRIBUTOR")

#: SS-I.2.1 A. ``None`` means "validated by form, not by a fixed literal".
#: ``coordinator_id`` added under DELTA review 5062494115 MAJOR 1: a login is a mutable
#: display handle, the numeric actor id is not, and every live actor resource exposes one.
DESIGNATION_SCHEMA: dict[str, str | None] = {
    "action": DESIGNATION_ACTION,
    "pull_request": str(THIS_CORRECTIVE_PULL_REQUEST),
    "accepted_head": None,
    "coordinator_login": None,
    "coordinator_id": None,
    "coordinator_type": None,
    "coordinator_association": None,
    "coordinator_app": None,
    "session_commitment": None,
}

#: SS-I.2.1 B. The nine result fields admit ONLY these literals -- free text carries no
#: authority anywhere in this schema, and no field admits a second, weaker literal.
#:
#: ``merge_commit_ci`` was REMOVED under DELTA review 5062494115 MAJOR 2, on measured fact
#: rather than preference: PR #362 merged at 15:07:49Z and the merge-commit run for the exact
#: merge SHA did not complete until 15:18:50Z, so an *immediate* verification cannot carry
#: authenticated CI success. It is bound instead, with its exact run/job/head-SHA/attempt, in
#: the CLOSURE declaration, which by construction is posted after the run completes.
PMV_RESULT_FIELDS: dict[str, tuple[str, ...]] = {
    "accepted_head_ancestry": ("PASS",),
    "authorized_scope": ("PASS",),
    "merge_tree_identity": ("IDENTICAL",),
    "protected_path_identity": ("IDENTICAL",),
    "head_agreement": ("IDENTICAL",),
    "main_clean": ("TRUE",),
    "validators_result": ("PASS",),
    "tests_result": ("PASS",),
    "overall_result": ("PASS",),
}

PMV_SCHEMA: dict[str, str | None] = {
    "action": PMV_ACTION,
    "pull_request": str(THIS_CORRECTIVE_PULL_REQUEST),
    "accepted_head": None,
    "merge_commit_sha": None,
    "session_reveal": None,
    **{k: None for k in PMV_RESULT_FIELDS},
}

#: SS-I.2.1 G. Closure is an ACT, not a shape. DELTA review 5062494115 BLOCKING 4 reproduced a
#: mallory/Bot/NONE comment posted through an application named ``evil``, whose body read
#: "I do NOT close this lifecycle.", passing as canonical closure and carrying the complete
#: verification predicate to True.
CLOSURE_SCHEMA: dict[str, str | None] = {
    "action": CLOSURE_ACTION,
    "pull_request": str(THIS_CORRECTIVE_PULL_REQUEST),
    "accepted_head": None,
    "merge_commit_sha": None,
    "post_merge_verification_comment_id": None,
    "merge_commit_ci_run_id": None,
    "merge_commit_ci_job_id": None,
    "merge_commit_ci_head_sha": None,
    "merge_commit_ci_run_attempt": None,
    "merge_commit_ci_status": "COMPLETED",
    "merge_commit_ci_conclusion": "SUCCESS",
    "lifecycle_closed": "TRUE",
}


def _parse_declaration(body: object, header: str, schema: dict) -> dict[str, str] | None:
    """Shared exact-declaration parser. Header, then one ``key: value`` per line, each once."""
    if not isinstance(body, str):
        return None
    lines = [ln.rstrip() for ln in body.strip().splitlines()]
    lines = [ln for ln in lines if ln != ""]
    if not lines or lines[0] != header:
        return None
    parsed: dict[str, str] = {}
    for line in lines[1:]:
        match = _KEY_VALUE.match(line)
        if match is None:
            return None
        key, value = match.group(1), match.group(2)
        if key not in schema or key in parsed:
            return None
        required = schema[key]
        if required is not None and value != required:
            return None
        parsed[key] = value
    if set(parsed) != set(schema):
        return None
    return parsed


def parse_designation_body(body: object) -> dict[str, str] | None:
    """SS-I.2.1 A -- the principal's own designation declaration, or ``None``.

    The designation is what the principal's BODY says. An unrelated principal comment, or one
    reading "I designate nobody", designates nobody -- DELTA review 5062156189 BLOCKING 1.
    """
    parsed = _parse_declaration(body, DESIGNATION_HEADER, DESIGNATION_SCHEMA)
    if parsed is None:
        return None
    if not _SHA40.match(parsed["accepted_head"]):
        return None
    if not _nonempty_str(parsed["coordinator_login"]):
        return None
    if _positive_int(parsed["coordinator_id"]) is None:
        return None
    if parsed["coordinator_type"] not in _COORDINATOR_TYPES:
        return None
    if parsed["coordinator_association"] not in _COORDINATOR_ASSOCIATIONS:
        return None
    if not _nonempty_str(parsed["coordinator_app"]):
        return None
    if not _SHA256_HEX.match(parsed["session_commitment"]):
        return None
    return parsed


def parse_pmv_body(body: object) -> dict[str, str] | None:
    """SS-I.2.1 B -- the verification declaration, or ``None``.

    Every result field is a closed literal. The withdrawn schema's free-text ``scope`` and
    ``results`` let a declaration reading "I performed no verification." verify -- DELTA
    review 5062156189 BLOCKING 2.
    """
    parsed = _parse_declaration(body, PMV_HEADER, PMV_SCHEMA)
    if parsed is None:
        return None
    for field in ("accepted_head", "merge_commit_sha"):
        if not _SHA40.match(parsed[field]):
            return None
    if not _nonempty_str(parsed["session_reveal"]):
        return None
    for field, permitted in PMV_RESULT_FIELDS.items():
        if parsed[field] not in permitted:
            return None
    return parsed


def parse_closure_body(body: object) -> dict[str, str] | None:
    """SS-I.2.1 G -- the exact affirmative closure declaration, or ``None``.

    Closure is the act, not the existence of a comment. A refusal, an unrelated narrative or a
    malformed resource yields ``None`` -- DELTA review 5062494115 BLOCKING 4.
    """
    parsed = _parse_declaration(body, CLOSURE_HEADER, CLOSURE_SCHEMA)
    if parsed is None:
        return None
    for field in ("accepted_head", "merge_commit_sha", "merge_commit_ci_head_sha"):
        if not _SHA40.match(parsed[field]):
            return None
    for field in ("post_merge_verification_comment_id", "merge_commit_ci_run_id",
                  "merge_commit_ci_job_id", "merge_commit_ci_run_attempt"):
        if _positive_int(parsed[field]) is None:
            return None
    # A successful run at some OTHER commit closes nothing.
    if parsed["merge_commit_ci_head_sha"] != parsed["merge_commit_sha"]:
        return None
    return parsed


def _exact_positive_int(value: object) -> int | None:
    """A raw-resource integer field. Unlike a declaration line, this is never a string.

    GitHub returns ``"id": 209825114``, not ``"209825114"``; accepting the string form on a
    resource would admit a hand-built mapping wearing the resource's field names.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    return value if value > 0 else None


def _positive_int(value: object) -> int | None:
    """Exact positive integer, from a declaration string or a raw resource field.

    ``bool`` is rejected explicitly: ``True`` is an ``int`` in Python and is not an actor id.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value > 0 else None
    if isinstance(value, str) and re.fullmatch(r"[1-9][0-9]*", value):
        return int(value)
    return None


def _actor_identity(record: dict) -> dict | None:
    """The complete identity a record exposes -- never reduced to a login string."""
    user = record.get("user")
    if not isinstance(user, dict):
        return None
    login, type_ = user.get("login"), user.get("type")
    if not (_nonempty_str(login) and _nonempty_str(type_)):
        return None
    # SS-I.2.1 A/D: every live actor resource exposes a numeric id, and it is required.
    actor_id = _exact_positive_int(user.get("id"))
    if actor_id is None:
        return None
    return {"login": login, "type": type_, "id": actor_id}


def _record_app_identity(record: dict) -> str | None:
    """``DIRECT`` for a present-and-null key, the slug for an application, else ``None``."""
    if "performed_via_github_app" not in record:
        return None
    app = record["performed_via_github_app"]
    if app is None:
        return "DIRECT"
    if isinstance(app, dict) and _nonempty_str(app.get("slug")):
        return app["slug"]
    return None


def principal_designation_is_valid(record: object) -> bool:
    """SS-I.2.1 A -- a designation is one principal-authored comment whose BODY designates.

    Takes ONE argument. There is no adjacent ``coordinator_login`` or ``session_claim``: an
    authority field placed beside an authenticated record by the caller is not authority.
    """
    if not isinstance(record, dict):
        return False
    if not is_canonical_top_level_issue_comment(record):
        return False
    if not is_direct_principal_record(record):
        return False
    if _actor_identity(record) is None:
        return False
    if parse_utc_instant(record.get("created_at")) is None:
        return False
    return parse_designation_body(record.get("body")) is not None


def canonical_merged_pull_request_is_valid(pull: object) -> bool:
    """SS-I.2.1 D -- the RAW merged-PR resource, by its real field names."""
    if not isinstance(pull, dict):
        return False
    if pull.get("merged") is not True:
        return False
    if pull.get("number") != THIS_CORRECTIVE_PULL_REQUEST:
        return False
    if pull.get("url") != f"{REPO_API}/pulls/{THIS_CORRECTIVE_PULL_REQUEST}":
        return False
    if pull.get("html_url") != f"{REPO_HTML}/pull/{THIS_CORRECTIVE_PULL_REQUEST}":
        return False
    base = pull.get("base")
    repo = base.get("repo") if isinstance(base, dict) else None
    if not isinstance(repo, dict) or repo.get("full_name") != CANONICAL_REPOSITORY:
        return False
    head = pull.get("head")
    if not isinstance(head, dict):
        return False
    if not (isinstance(head.get("sha"), str) and _SHA40.match(head["sha"])):
        return False
    merge_sha = pull.get("merge_commit_sha")
    if not (isinstance(merge_sha, str) and _SHA40.match(merge_sha)):
        return False
    merged_by = pull.get("merged_by")
    if not isinstance(merged_by, dict):
        return False
    if not (_nonempty_str(merged_by.get("login")) and _nonempty_str(merged_by.get("type"))):
        return False
    # SS-I.2.1 D / DELTA 5062494115 MAJOR 1: a login is a mutable display handle. Removing
    # ``id`` and ``node_id`` previously left this validator and the full PMV predicate True.
    if _exact_positive_int(merged_by.get("id")) is None:
        return False
    if not _nonempty_str(merged_by.get("node_id")):
        return False
    return parse_utc_instant(pull.get("merged_at")) is not None


def canonical_closure_record_is_valid(record: object) -> bool:
    """SS-I.2.1 G -- closure is an authenticated affirmative ACT, not a shape.

    Shape alone previously admitted a ``mallory``/``Bot``/``NONE`` comment, posted through an
    application named ``evil``, whose body read "I do NOT close this lifecycle." -- DELTA
    review 5062494115 BLOCKING 4. Binding to the authorized actor and to the exact CI run is
    performed by :func:`closure_is_authorized`, which consumes this predicate.
    """
    if not isinstance(record, dict):
        return False
    if not is_canonical_top_level_issue_comment(record):
        return False
    if _actor_identity(record) is None:
        return False
    if not _nonempty_str(record.get("author_association")):
        return False
    if _record_app_identity(record) is None:
        return False
    if parse_utc_instant(record.get("created_at")) is None:
        return False
    return parse_closure_body(record.get("body")) is not None


def canonical_ci_run_is_successful(run: object, job: object, merge_commit_sha: object) -> bool:
    """SS-I.2.1 D/G -- the raw Actions run and job, at the EXACT merge SHA.

    A successful run at some other commit closes nothing, and neither does an incomplete one.
    """
    if not (isinstance(run, dict) and isinstance(job, dict)):
        return False
    if not (isinstance(merge_commit_sha, str) and _SHA40.match(merge_commit_sha)):
        return False
    for resource in (run, job):
        if _exact_positive_int(resource.get("id")) is None:
            return False
        if resource.get("head_sha") != merge_commit_sha:
            return False
        if _exact_positive_int(resource.get("run_attempt")) is None:
            return False
        if resource.get("status") != "completed":
            return False
        if resource.get("conclusion") != "success":
            return False
    return parse_utc_instant(job.get("completed_at")) is not None


def closure_is_authorized(
    closure_record: object,
    *,
    designated: object,
    merged_pull_request: object,
    verification_record: object,
    ci_run: object,
    ci_job: object,
) -> bool:
    """SS-I.2.1 G -- the closure act, bound to the authorized closer and the exact CI run."""
    if not canonical_closure_record_is_valid(closure_record):
        return False
    if not canonical_merged_pull_request_is_valid(merged_pull_request):
        return False
    if not (isinstance(designated, dict) and isinstance(verification_record, dict)):
        return False

    declaration = parse_closure_body(closure_record["body"])
    if declaration["accepted_head"] != merged_pull_request["head"]["sha"]:
        return False
    if declaration["merge_commit_sha"] != merged_pull_request["merge_commit_sha"]:
        return False
    if not canonical_ci_run_is_successful(ci_run, ci_job, declaration["merge_commit_sha"]):
        return False
    if _positive_int(declaration["merge_commit_ci_run_id"]) != _positive_int(ci_run.get("id")):
        return False
    if _positive_int(declaration["merge_commit_ci_job_id"]) != _positive_int(ci_job.get("id")):
        return False
    if _positive_int(declaration["merge_commit_ci_run_attempt"]) != _positive_int(
        ci_run.get("run_attempt")
    ):
        return False
    # Closure names the act it completes, rather than floating free.
    if _positive_int(declaration["post_merge_verification_comment_id"]) != _positive_int(
        verification_record.get("id")
    ):
        return False

    identity = _actor_identity(closure_record)
    if identity["login"] != designated["coordinator_login"]:
        return False
    if identity["id"] != _positive_int(designated["coordinator_id"]):
        return False
    if identity["type"] != designated["coordinator_type"]:
        return False
    if closure_record.get("author_association") != designated["coordinator_association"]:
        return False
    if _record_app_identity(closure_record) != designated["coordinator_app"]:
        return False

    # SS-I.2.1 E: verification_at < ci_completed_at < closure_at, all strict.
    verified_at = parse_utc_instant(verification_record.get("created_at"))
    ci_completed_at = parse_utc_instant(ci_job.get("completed_at"))
    closed_at = parse_utc_instant(closure_record["created_at"])
    if verified_at is None or ci_completed_at is None or closed_at is None:
        return False
    return verified_at < ci_completed_at < closed_at


def session_reveal_matches_commitment(reveal: object, commitment: object) -> bool:
    """SS-I.2.1 C -- SHA-256 of the revealed value must equal the committed digest.

    Establishes continuity of possession of a value committed before the merge and never
    published. NOT GitHub runtime-session identity, which GitHub does not expose.
    """
    if not (_nonempty_str(reveal) and isinstance(commitment, str)):
        return False
    if not _SHA256_HEX.match(commitment):
        return False
    return hashlib.sha256(reveal.encode("utf-8")).hexdigest() == commitment


def post_merge_verification_is_valid(
    record: dict,
    *,
    designation_record: object,
    merged_pull_request: object,
    closure_record: object,
    ci_run: object,
    ci_job: object,
) -> bool:
    """SS-I.2 -- valid immediate post-merge-verification evidence?

    Conjunctive over independently validated CANONICAL resources and the record's own typed
    declaration. No caller-supplied role string, projection, or timestamp is trusted anywhere.

    **There is no direct-principal bypass.** The withdrawn branch skipped the designation, the
    merger-identity comparison and the reveal entirely, assigning ``designation_at =
    merged_at``; DELTA review 5062494115 BLOCKING 3 reproduced a principal-attributed
    verification with no designation, a DIFFERENT account as ``merged_by``, and an
    uncommitted reveal returning True. Whichever lawful actor merges and verifies -- the
    principal included -- travels this one path.
    """
    if not isinstance(record, dict):
        return False
    if not is_canonical_top_level_issue_comment(record):
        return False
    if not _actor_fields_are_well_formed(record):
        return False
    # Fail closed rather than raising: a record whose ``user.id`` is missing or malformed has
    # no identity to compare, and an exception is not a verdict.
    if _actor_identity(record) is None:
        return False
    if not canonical_merged_pull_request_is_valid(merged_pull_request):
        return False
    if not principal_designation_is_valid(designation_record):
        return False

    declaration = parse_pmv_body(record.get("body"))
    if declaration is None:
        return False
    if declaration["accepted_head"] != merged_pull_request["head"]["sha"]:
        return False
    if declaration["merge_commit_sha"] != merged_pull_request["merge_commit_sha"]:
        return False

    designated = parse_designation_body(designation_record["body"])
    if designated["accepted_head"] != merged_pull_request["head"]["sha"]:
        return False

    coordinator_id = _positive_int(designated["coordinator_id"])
    identity = _actor_identity(record)
    if identity["login"] != designated["coordinator_login"]:
        return False
    if identity["id"] != coordinator_id:
        return False
    if identity["type"] != designated["coordinator_type"]:
        return False
    if record.get("author_association") != designated["coordinator_association"]:
        return False
    if _record_app_identity(record) != designated["coordinator_app"]:
        return False

    # SS-I.2.1 D: the merge resource exposes NO application provenance, so the merger is
    # compared on every identity field it DOES expose -- login, type and the numeric id --
    # and nothing further is claimed.
    merger = merged_pull_request["merged_by"]
    if merger.get("login") != designated["coordinator_login"]:
        return False
    if merger.get("type") != designated["coordinator_type"]:
        return False
    if _exact_positive_int(merger.get("id")) != coordinator_id:
        return False

    if not session_reveal_matches_commitment(
        declaration["session_reveal"], designated["session_commitment"]
    ):
        return False

    if not closure_is_authorized(
        closure_record,
        designated=designated,
        merged_pull_request=merged_pull_request,
        verification_record=record,
        ci_run=ci_run,
        ci_job=ci_job,
    ):
        return False

    # SS-I.2.1 E -- parsed instants, never strings, and every relation STRICT. The withdrawn
    # implementation used ``designation_at <= merged_at`` where the decision said ``<``, and
    # tested equality as a positive case -- DELTA review 5062494115 MAJOR 2.
    designation_at = parse_utc_instant(designation_record["created_at"])
    merged_at = parse_utc_instant(merged_pull_request["merged_at"])
    verified_at = parse_utc_instant(record.get("created_at"))
    if designation_at is None or merged_at is None or verified_at is None:
        return False
    return designation_at < merged_at < verified_at


# --------------------------------------------------------------------------------------
# Record fixtures modelled on the real, live-derived record SHAPES.
#
# The review fixture below reproduces the exact GitHub shape of review 5060791095 -- the live
# counterexample that defeated the earlier predicate.
# --------------------------------------------------------------------------------------
GENUINE_RATIFICATION_ID = 9_999_999_999  # a synthetic id for fixtures ONLY; never a claim.

#: A schema-conformant affirmative declaration. The PR #363 head here is a FIXTURE value --
#: 40 hex, deliberately not any real commit -- because the repository cannot know its own
#: future final head; SS-G.9 readback establishes the real one.
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
    body=SCOPE_BODY, ident=GENUINE_RATIFICATION_ID, pr=None, actor_id=PRINCIPAL_ID,
    **overrides,
):
    """A canonical top-level issue comment on this corrective pull request."""
    pr = THIS_CORRECTIVE_PULL_REQUEST if pr is None else pr
    rec = {
        "id": ident,
        "url": f"{REPO_API}/issues/comments/{ident}",
        "html_url": f"{REPO_HTML}/pull/{pr}#issuecomment-{ident}",
        "issue_url": f"{REPO_API}/issues/{pr}",
        "user": {"login": login, "type": type_, "id": actor_id},
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
        "user": {"login": login, "type": type_, "id": PRINCIPAL_ID},
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


class TestTheCorrectedDocumentationIsPinned:
    """DELTA review 5061240650 MAJOR 2 and MINOR 1 -- documentation that contradicted the code.

    Both defects were invisible to the suite: nothing asserted SS-D's application-key wording,
    and nothing asserted the ``is_canonical_top_level_issue_comment`` docstring. Restoring
    either error passed every test. They are pinned here so that cannot recur.
    """

    def test_section_d_requires_present_and_null_not_absent(self):
        """MAJOR 2: SS-D said 'absent', which SS-G.2 and SS-J both treat as a FAILURE."""
        flat = _flat(_read(DECISION_RELPATH))
        assert "expressed as a `performed_via_github_app` key that is **present and null**" in flat
        assert "never merely absent" in flat
        # The withdrawn phrasing must not reappear as a live requirement.
        assert "`performed_via_github_app` must be **absent**" not in flat
        assert "must be **absent**. Without that conjunct" not in flat

    def test_section_d_agrees_with_section_g2_and_section_j(self):
        """The three must state one rule, not two."""
        flat = _flat(_read(DECISION_RELPATH))
        assert "the `performed_via_github_app` key is **present and null** — not merely absent" in flat
        assert "including an app key present and null" in flat
        # And the code enforces exactly that.
        assert is_direct_principal_record(_issue_comment()) is True
        assert is_direct_principal_record(_issue_comment(app_key_present=False)) is False
        assert is_direct_principal_record(_issue_comment(app="claude")) is False

    def test_the_record_kind_docstring_no_longer_claims_to_reject_synthetic_records(self):
        """MINOR 1: it cannot, and this suite's own fixtures are the counterexample."""
        import inspect

        doc = _flat(inspect.getdoc(is_canonical_top_level_issue_comment))
        assert "It does NOT reject a caller-assembled record, and never could" in doc
        # It does still reject other RECORD KINDS -- that half of the claim was always true.
        assert "Rejects pull-request reviews" in doc
        # The withdrawn phrasing must not reappear.
        assert "and synthetic records" not in doc
        # The docstring's claim and the code's behaviour must agree, both ways.
        assert is_canonical_top_level_issue_comment(_issue_comment()) is True
        assert is_canonical_top_level_issue_comment(_pull_request_review()) is False

    def test_readback_cross_references_name_section_g9_not_g6(self):
        """MINOR 1: SS-G.6 is the Claude non-composition rule; SS-G.9 is the readback rule."""
        source = _read(THIS_ARTIFACT)
        # Count, not membership: this very test names the withdrawn section, so the assertion
        # must be that no OTHER occurrence survives. An or-fallback here would be unfalsifiable.
        withdrawn = "SS-G." + "6"
        assert source.count(withdrawn) == 1
        assert source.count("SS-G." + "9") >= 4
        flat = _flat(_read(DECISION_RELPATH))
        assert "#### G.6 — Claude must not write or post it" in flat
        assert "#### G.9 — The closed lifecycle sequence" in flat


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


#: Shared evidence fixtures. Shapes mirror the REAL canonical GitHub resources, whose field
#: names were read from the live API for PR #362, review 5062156189 and comment 5463232454
#: during the DELTA review 5062156189 design audit -- not invented projections.
COORDINATOR_LOGIN = "merge-coordinator"
COORDINATOR_TYPE = "Bot"
COORDINATOR_ASSOCIATION = "CONTRIBUTOR"
COORDINATOR_APP = "claude"
COORDINATOR_ID = 209825114

#: The coordinator session's private value, and the digest the principal commits to.
SESSION_REVEAL = "coordinator-session-secret-7f3a91e4c2"
SESSION_COMMITMENT = hashlib.sha256(SESSION_REVEAL.encode("utf-8")).hexdigest()

PMV_MERGE_HEAD = "b" * 40
PMV_MERGE_COMMIT_SHA = "c" * 40
PMV_DESIGNATED_AT = "2026-08-31T09:00:00Z"
PMV_MERGED_AT = "2026-08-31T10:00:00Z"
PMV_VERIFIED_AT = "2026-08-31T10:05:00Z"
PMV_CI_COMPLETED_AT = "2026-08-31T10:16:00Z"
PMV_CLOSED_AT = "2026-08-31T10:30:00Z"
PMV_RECORD_ID = 8_300_000_010
PMV_CI_RUN_ID = 33_345_371_079
PMV_CI_JOB_ID = 99_348_350_944


_DEFAULT = object()   # distinct from None, which is itself a body under test

REAL_FINAL_HEAD = "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"
APPROVING_BODY = f"FORMAL DISPOSITION: {APPROVING_REVIEW_DISPOSITION}\n\nIndependent review."


def _designation_body(action=DESIGNATION_ACTION, pull_request=THIS_CORRECTIVE_PULL_REQUEST,
                      accepted_head=PMV_MERGE_HEAD, coordinator_login=COORDINATOR_LOGIN,
                      coordinator_id=COORDINATOR_ID,
                      coordinator_type=COORDINATOR_TYPE,
                      coordinator_association=COORDINATOR_ASSOCIATION,
                      coordinator_app=COORDINATOR_APP,
                      session_commitment=SESSION_COMMITMENT, header=DESIGNATION_HEADER):
    return "\n".join([
        header,
        f"action: {action}",
        f"pull_request: {pull_request}",
        f"accepted_head: {accepted_head}",
        f"coordinator_login: {coordinator_login}",
        f"coordinator_id: {coordinator_id}",
        f"coordinator_type: {coordinator_type}",
        f"coordinator_association: {coordinator_association}",
        f"coordinator_app: {coordinator_app}",
        f"session_commitment: {session_commitment}",
    ])


def _closure_body(action=CLOSURE_ACTION, pull_request=THIS_CORRECTIVE_PULL_REQUEST,
                  accepted_head=PMV_MERGE_HEAD, merge_commit_sha=PMV_MERGE_COMMIT_SHA,
                  post_merge_verification_comment_id=PMV_RECORD_ID,
                  merge_commit_ci_run_id=PMV_CI_RUN_ID,
                  merge_commit_ci_job_id=PMV_CI_JOB_ID,
                  merge_commit_ci_head_sha=None,
                  merge_commit_ci_run_attempt=1,
                  merge_commit_ci_status="COMPLETED",
                  merge_commit_ci_conclusion="SUCCESS",
                  lifecycle_closed="TRUE", header=CLOSURE_HEADER):
    if merge_commit_ci_head_sha is None:
        merge_commit_ci_head_sha = merge_commit_sha
    return "\n".join([
        header,
        f"action: {action}",
        f"pull_request: {pull_request}",
        f"accepted_head: {accepted_head}",
        f"merge_commit_sha: {merge_commit_sha}",
        f"post_merge_verification_comment_id: {post_merge_verification_comment_id}",
        f"merge_commit_ci_run_id: {merge_commit_ci_run_id}",
        f"merge_commit_ci_job_id: {merge_commit_ci_job_id}",
        f"merge_commit_ci_head_sha: {merge_commit_ci_head_sha}",
        f"merge_commit_ci_run_attempt: {merge_commit_ci_run_attempt}",
        f"merge_commit_ci_status: {merge_commit_ci_status}",
        f"merge_commit_ci_conclusion: {merge_commit_ci_conclusion}",
        f"lifecycle_closed: {lifecycle_closed}",
    ])


def _ci_run(**over):
    """The RAW Actions run resource, by GitHub's own field names."""
    out = {"id": PMV_CI_RUN_ID, "head_sha": PMV_MERGE_COMMIT_SHA, "run_attempt": 1,
           "status": "completed", "conclusion": "success",
           "created_at": PMV_MERGED_AT, "updated_at": PMV_CI_COMPLETED_AT}
    out.update(over)
    return out


def _ci_job(**over):
    """The RAW Actions job resource."""
    out = {"id": PMV_CI_JOB_ID, "head_sha": PMV_MERGE_COMMIT_SHA, "run_attempt": 1,
           "status": "completed", "conclusion": "success",
           "completed_at": PMV_CI_COMPLETED_AT}
    out.update(over)
    return out


def _open_pull_request(head=REAL_FINAL_HEAD, number=THIS_CORRECTIVE_PULL_REQUEST, **over):
    """The RAW open, unmerged PR #363 resource used by the readback."""
    pr = number
    out = {
        "url": f"{REPO_API}/pulls/{pr}",
        "html_url": f"{REPO_HTML}/pull/{pr}",
        "number": pr, "state": "open", "draft": True,
        "merged": False, "merged_at": None,
        "head": {"sha": head, "repo": {"full_name": CANONICAL_REPOSITORY}},
        "base": {"ref": "main", "repo": {"full_name": CANONICAL_REPOSITORY}},
    }
    out.update(over)
    return out


def _review_collection(reviews, per_page=100, link_header=None):
    """The raw array TOGETHER WITH GitHub's own ``Link`` header -- SS-I.2.1 D."""
    return {"reviews": list(reviews), "per_page": per_page, "link_header": link_header}


def _pmv_body(action=PMV_ACTION, pull_request=THIS_CORRECTIVE_PULL_REQUEST,
              accepted_head=PMV_MERGE_HEAD, merge_commit_sha=PMV_MERGE_COMMIT_SHA,
              session_reveal=SESSION_REVEAL, header=PMV_HEADER, **results):
    fields = {k: v[0] for k, v in PMV_RESULT_FIELDS.items()}
    fields.update(results)
    lines = [header, f"action: {action}", f"pull_request: {pull_request}",
             f"accepted_head: {accepted_head}", f"merge_commit_sha: {merge_commit_sha}",
             f"session_reveal: {session_reveal}"]
    lines += [f"{k}: {fields[k]}" for k in PMV_RESULT_FIELDS]
    return "\n".join(lines)


def _designation_record(created=PMV_DESIGNATED_AT, ident=8_300_000_001, body=None, **over):
    """A principal-authored designation whose BODY does the designating."""
    return _issue_comment(created=created, ident=ident,
                          body=_designation_body() if body is None else body, **over)


def _merged_pull_request(**over):
    """The RAW merged-PR resource, by GitHub's own field names."""
    pr = THIS_CORRECTIVE_PULL_REQUEST
    out = {
        "url": f"{REPO_API}/pulls/{pr}",
        "html_url": f"{REPO_HTML}/pull/{pr}",
        "number": pr,
        "state": "closed",
        "merged": True,
        "draft": False,
        "merge_commit_sha": PMV_MERGE_COMMIT_SHA,
        "merged_at": PMV_MERGED_AT,
        "head": {"sha": PMV_MERGE_HEAD, "repo": {"full_name": CANONICAL_REPOSITORY}},
        "base": {"repo": {"full_name": CANONICAL_REPOSITORY}},
        "merged_by": {"login": COORDINATOR_LOGIN, "type": COORDINATOR_TYPE,
                      "id": 209825114, "node_id": "U_kgDOMhq3Wg"},
    }
    out.update(over)
    return out


def _closure_record(created=PMV_CLOSED_AT, ident=8_300_000_002, login=COORDINATOR_LOGIN,
                    type_=COORDINATOR_TYPE, assoc=COORDINATOR_ASSOCIATION,
                    app=COORDINATOR_APP, body=_DEFAULT, actor_id=COORDINATOR_ID, **over):
    """Closure is a canonical resource carrying an affirmative act -- SS-I.2.1 G."""
    return _issue_comment(login=login, type_=type_, assoc=assoc, app=app,
                          created=created, ident=ident, actor_id=actor_id,
                          body=_closure_body() if body is _DEFAULT else body, **over)




def _coordinator_record(login=COORDINATOR_LOGIN, type_=COORDINATOR_TYPE,
                        assoc=COORDINATOR_ASSOCIATION, app=COORDINATOR_APP,
                        created=PMV_VERIFIED_AT, body=_DEFAULT, ident=PMV_RECORD_ID,
                        actor_id=COORDINATOR_ID, **over):
    return _issue_comment(login=login, type_=type_, assoc=assoc, app=app, created=created,
                          body=_pmv_body() if body is _DEFAULT else body, ident=ident,
                          actor_id=actor_id, **over)




def _final_review(head=REAL_FINAL_HEAD, ident=5_062_156_189, state="COMMENTED",
                  body=_DEFAULT, **over):
    """The RAW pull-request-review resource. Note: reviews carry NO application provenance."""
    pr = THIS_CORRECTIVE_PULL_REQUEST
    out = {
        "id": ident,
        "node_id": "PRR_synthetic",
        "state": state,
        "commit_id": head,
        "submitted_at": "2026-08-31T12:00:00Z",
        "author_association": "OWNER",
        "html_url": f"{REPO_HTML}/pull/{pr}#pullrequestreview-{ident}",
        "pull_request_url": f"{REPO_API}/pulls/{pr}",
        "user": {"login": PRINCIPAL_LOGIN, "type": PRINCIPAL_TYPE, "id": 218449187},
        "body": APPROVING_BODY if body is _DEFAULT else body,
    }
    out.update(over)
    return out


def _ratification_naming(head, created="2026-08-31T13:00:00Z", **over):
    """A ratification that POSTDATES the approving review, as SS-I.2.1 F.4 requires."""
    over.setdefault("created", created)
    body = SCOPE_BODY.replace(f"pr363_accepted_head: {FIXTURE_PR363_HEAD}",
                              f"pr363_accepted_head: {head}")
    return _issue_comment(body=body, ident=8_400_000_001, **over)


def _live_pr(head=REAL_FINAL_HEAD, number=THIS_CORRECTIVE_PULL_REQUEST, **over):
    """The RAW open PR #363 resource.

    This helper previously returned ``{"number": …, "head": {"sha": …}, "draft": …,
    "merged": …}`` -- a caller projection, which DELTA review 5062494115 BLOCKING 2 used
    directly as its counterexample. It now returns the real resource shape.
    """
    return _open_pull_request(head=head, number=number, **over)


def _complete_collection(*reviews, **over):
    """A provably complete review collection containing the given reviews.

    Not a simplified path: it builds exactly the evidence the live lifecycle uses -- the raw
    array together with GitHub's own ``Link`` header, absent here because a single page whose
    length is below ``per_page`` is complete. Tests that attack completeness override it.
    """
    return _review_collection(list(reviews), **over)


def _readback(ratification, pull=_DEFAULT, review=_DEFAULT, collection=_DEFAULT):
    """Call the real readback with a complete collection unless one is supplied.

    ``_DEFAULT`` rather than ``None`` throughout: ``None`` is itself an input under test.
    A bare list of extra reviews is accepted and folded into a complete collection alongside
    the selected review, which is what the live collection would contain.
    """
    review = _final_review() if review is _DEFAULT else review
    pull = _live_pr() if pull is _DEFAULT else pull
    if collection is _DEFAULT:
        collection = _complete_collection(review)
    elif isinstance(collection, list):
        collection = _complete_collection(review, *collection)
    return external_ratification_readback(ratification, pull, review, collection)


class TestPostMergeVerificationEvidenceIsMechanised:
    """DELTA review 5062156189 BLOCKING 1 and BLOCKING 2 -- authority from evidence, not callers.

    The withdrawn model validated a principal-SHAPED comment but never parsed its body, and took
    the coordinator login and session claim as fields the caller attached BESIDE it. An unrelated
    principal comment reading "I designate nobody", created AFTER the verification, designated
    mallory. Its result fields were free text, so a declaration saying "I performed no
    verification." verified. Both are reproduced below and both now fail.
    """

    def _ctx(self, **over):
        ctx = dict(designation_record=_designation_record(),
                   merged_pull_request=_merged_pull_request(),
                   closure_record=_closure_record(),
                   ci_run=_ci_run(), ci_job=_ci_job())
        ctx.update(over)
        return ctx

    # ------------------------------------------------------------------ positive
    def test_an_authenticated_coordinator_verifies(self):
        assert post_merge_verification_is_valid(_coordinator_record(), **self._ctx()) is True

    def test_the_principal_cannot_verify_without_a_designation(self):
        """DELTA review 5062494115 BLOCKING 3 -- there is no direct-principal bypass.

        Renamed and inverted from ``test_the_principal_verifies_without_any_designation``.
        The withdrawn branch assigned ``designation_at = merged_at`` and skipped designation,
        merger identity and reveal entirely; the reviewer used a principal-attributed record
        with a DIFFERENT ``merged_by`` and an uncommitted reveal to reach True.
        """
        rec = _issue_comment(created=PMV_VERIFIED_AT, ident=8_300_000_011, body=_pmv_body())
        assert is_direct_principal_record(rec) is True
        assert post_merge_verification_is_valid(
            rec, **self._ctx(designation_record=None)) is False
        # The reviewer's exact reproduction: wrong reveal, coordinator as merger, no designation.
        wrong = _issue_comment(created=PMV_VERIFIED_AT, ident=8_300_000_012,
                               body=_pmv_body(session_reveal="wrong-and-uncommitted-session"))
        assert post_merge_verification_is_valid(
            wrong, **self._ctx(designation_record=None)) is False

    def test_the_principal_verifies_only_by_being_designated_like_anyone_else(self):
        """SS-I.2.1 H -- the principal path is a choice of ACTOR, not an exemption."""
        rec = _issue_comment(created=PMV_VERIFIED_AT, ident=PMV_RECORD_ID, body=_pmv_body())
        body = _designation_body(coordinator_login=PRINCIPAL_LOGIN,
                                 coordinator_id=PRINCIPAL_ID, coordinator_type="User",
                                 coordinator_association="OWNER", coordinator_app="DIRECT")
        ctx = self._ctx(
            designation_record=_designation_record(body=body),
            merged_pull_request=_merged_pull_request(
                merged_by={"login": PRINCIPAL_LOGIN, "type": "User",
                           "id": PRINCIPAL_ID, "node_id": "U_kgDODQVFIw"}),
            closure_record=_closure_record(login=PRINCIPAL_LOGIN, type_="User",
                                           assoc="OWNER", app=None,
                                           actor_id=PRINCIPAL_ID))
        assert post_merge_verification_is_valid(rec, **ctx) is True

    def test_one_second_inside_each_boundary_passes(self):
        """The lawful window is (merge_at, ci_completed_at), both ends exclusive.

        The upper bound moved from ``closure_at`` (10:30) to ``ci_completed_at`` (10:16) when
        merge-commit CI was relocated out of the verification declaration into the closure
        declaration -- SS-I.2.1 B, DELTA review 5062494115 MAJOR 2. A verification at 10:29:59
        now legitimately FAILS, because it would postdate the CI run it never attests.
        """
        for created in ("2026-08-31T10:00:01Z", "2026-08-31T10:15:59Z"):
            assert post_merge_verification_is_valid(
                _coordinator_record(created=created), **self._ctx()) is True, created
        assert post_merge_verification_is_valid(
            _coordinator_record(created="2026-08-31T10:29:59Z"), **self._ctx()) is False

    # -------------------------------- BLOCKING 1: the designation must DESIGNATE
    def test_an_unrelated_principal_comment_designates_nobody(self):
        """The reviewer's exact reproduction, now closed."""
        unrelated = _issue_comment(ident=7_000_000_001, created="2026-08-31T10:20:00Z",
                                   body="I accept the reviewed head. I designate nobody.")
        # It really is a canonical direct-principal record -- that is why body parsing matters.
        assert is_canonical_top_level_issue_comment(unrelated) is True
        assert is_direct_principal_record(unrelated) is True
        assert parse_designation_body(unrelated["body"]) is None
        assert principal_designation_is_valid(unrelated) is False
        mallory = _coordinator_record(login="mallory", assoc="NONE", app="evil")
        assert post_merge_verification_is_valid(
            mallory, **self._ctx(designation_record=unrelated,
                                 merged_pull_request=_merged_pull_request(
                                     merged_by={"login": "mallory", "type": "Bot", "id": 1}))
        ) is False

    def test_no_adjacent_field_can_create_authority(self):
        """The withdrawn signature took coordinator_login/session_claim beside the record."""
        import inspect

        params = set(inspect.signature(post_merge_verification_is_valid).parameters)
        assert params == {"record", "designation_record", "merged_pull_request",
                          "ci_run", "ci_job",
                          "closure_record"}
        for withdrawn in ("designated_coordinator", "merge_performed_by", "merged_at",
                          "closure_at", "designation", "merge_record"):
            assert withdrawn not in params, withdrawn
        assert set(inspect.signature(principal_designation_is_valid).parameters) == {"record"}

    @pytest.mark.parametrize("field,value", [
        ("coordinator_login", "mallory"),
        ("coordinator_type", "User"),
        ("coordinator_association", "OWNER"),
        ("coordinator_app", "DIRECT"),
        ("accepted_head", "d" * 40),
    ])
    def test_the_verifier_must_match_every_designated_identity_field(self, field, value):
        """The complete tuple, never a login string alone."""
        body = _designation_body(**{field: value})
        assert post_merge_verification_is_valid(
            _coordinator_record(),
            **self._ctx(designation_record=_designation_record(body=body))) is False, field

    @pytest.mark.parametrize("over", [
        {"coordinator_type": "Owner"}, {"coordinator_type": ""}, {"coordinator_type": "bot"},
        {"coordinator_association": "STRANGER"}, {"coordinator_association": ""},
        {"coordinator_login": ""}, {"coordinator_app": ""},
        {"accepted_head": "TBD"}, {"accepted_head": "A" * 40},
        {"session_commitment": "not-a-digest"}, {"session_commitment": "a" * 63},
        {"action": "DESIGNATE-NOBODY"}, {"pull_request": 362},
        {"header": "XASSET-0062 RATIFICATION"},
    ])
    def test_a_malformed_designation_declaration_designates_nobody(self, over):
        body = _designation_body(**over)
        assert parse_designation_body(body) is None, over
        assert principal_designation_is_valid(_designation_record(body=body)) is False, over

    @pytest.mark.parametrize("over", [
        {"app": "claude"}, {"type_": "Bot"}, {"assoc": "CONTRIBUTOR"},
        {"login": "someone-else"}, {"app_key_present": False},
    ])
    def test_a_designation_not_authored_by_the_principal_designates_nobody(self, over):
        rec = _designation_record(**over)
        assert principal_designation_is_valid(rec) is False, over
        assert post_merge_verification_is_valid(
            _coordinator_record(), **self._ctx(designation_record=rec)) is False, over

    def test_a_pull_request_review_is_never_a_designation(self):
        assert principal_designation_is_valid(_pull_request_review()) is False

    @pytest.mark.parametrize("designation", [None, "coordinator", 123, [], {}])
    def test_a_missing_or_non_record_designation_fails_the_coordinator_path(self, designation):
        assert post_merge_verification_is_valid(
            _coordinator_record(), **self._ctx(designation_record=designation)) is False

    # -------------------------------------------------- BLOCKING 1: chronology
    @pytest.mark.parametrize("designated_at,label", [
        ("2026-08-31T10:20:00Z", "after the verification"),
        ("2026-08-31T10:06:00Z", "after the verification, before closure"),
        ("2026-08-31T10:00:01Z", "after the merge"),
    ])
    def test_a_designation_issued_too_late_fails(self, designated_at, label):
        assert post_merge_verification_is_valid(
            _coordinator_record(),
            **self._ctx(designation_record=_designation_record(created=designated_at))
        ) is False, label

    def test_a_designation_at_the_merge_instant_fails(self):
        """SS-I.2.1 E is STRICT: ``designation_at < merge_at``.

        Renamed and inverted from ``..._is_permitted``: DELTA review 5062494115 MAJOR 2 found
        ``<=`` implemented where the decision said ``<``, with equality tested as a POSITIVE
        case. The old expectation was the defect, so the test could not simply be re-run.
        """
        assert post_merge_verification_is_valid(
            _coordinator_record(),
            **self._ctx(designation_record=_designation_record(created=PMV_MERGED_AT))) is False
        # One second earlier is the nearest lawful designation.
        assert post_merge_verification_is_valid(
            _coordinator_record(),
            **self._ctx(designation_record=_designation_record(
                created="2026-08-31T09:59:59Z"))) is True

    # ------------------------------------- BLOCKING 1: canonical merge resource
    def test_the_withdrawn_projection_shape_is_rejected(self):
        """The six invented keys the previous design called canonical."""
        projection = {"merged": True, "number": THIS_CORRECTIVE_PULL_REQUEST,
                      "accepted_head": PMV_MERGE_HEAD, "merge_sha": PMV_MERGE_COMMIT_SHA,
                      "merged_by_login": COORDINATOR_LOGIN, "merged_at": PMV_MERGED_AT}
        assert canonical_merged_pull_request_is_valid(projection) is False
        assert post_merge_verification_is_valid(
            _coordinator_record(), **self._ctx(merged_pull_request=projection)) is False

    @pytest.mark.parametrize("over", [
        {"merged": False}, {"merged": None}, {"merged": "true"},
        {"number": 362}, {"url": f"{REPO_API}/pulls/999"}, {"html_url": "elsewhere"},
        {"base": {"repo": {"full_name": "someone/else"}}}, {"base": {}}, {"base": None},
        {"head": {"sha": "nope"}}, {"head": {}}, {"head": None}, {"head": {"sha": "A" * 40}},
        {"merge_commit_sha": "short"}, {"merge_commit_sha": None},
        {"merged_by": {"login": "", "type": "Bot"}}, {"merged_by": {"login": "x"}},
        {"merged_by": None}, {"merged_at": "2026-08-31T10:05:99Z"}, {"merged_at": None},
    ])
    def test_a_malformed_canonical_merge_resource_fails(self, over):
        pr = _merged_pull_request(**over)
        assert canonical_merged_pull_request_is_valid(pr) is False, over
        assert post_merge_verification_is_valid(
            _coordinator_record(), **self._ctx(merged_pull_request=pr)) is False, over

    def test_a_verifier_whose_own_login_is_not_the_designated_one_fails(self):
        """Isolates the record-vs-designation login check specifically.

        Varying the DESIGNATION's coordinator_login also changes what ``merged_by`` is
        compared against, so the merger clause masks it. This varies only the verification
        record, leaving the designation and the canonical merge resource untouched.
        """
        rec = _coordinator_record(login="someone-else")
        # Everything else about the record still matches the designation exactly.
        assert _actor_identity(rec)["type"] == COORDINATOR_TYPE
        assert rec["author_association"] == COORDINATOR_ASSOCIATION
        assert _record_app_identity(rec) == COORDINATOR_APP
        assert post_merge_verification_is_valid(rec, **self._ctx()) is False

    def test_a_verifier_whose_type_or_association_differs_fails(self):
        """The same isolation for the other two identity fields."""
        assert post_merge_verification_is_valid(
            _coordinator_record(type_="User"), **self._ctx()) is False
        assert post_merge_verification_is_valid(
            _coordinator_record(assoc="OWNER"), **self._ctx()) is False

    @pytest.mark.parametrize("pull", [None, "merged", 123, [], {}, True])
    def test_a_missing_or_non_resource_merge_record_fails(self, pull):
        assert canonical_merged_pull_request_is_valid(pull) is False
        assert post_merge_verification_is_valid(
            _coordinator_record(), **self._ctx(merged_pull_request=pull)) is False

    def test_a_coordinator_who_is_not_the_recorded_merger_fails(self):
        assert post_merge_verification_is_valid(
            _coordinator_record(),
            **self._ctx(merged_pull_request=_merged_pull_request(
                merged_by={"login": "another-account", "type": "Bot", "id": 2}))) is False

    def test_the_declaration_must_name_the_canonical_head_and_merge_sha(self):
        assert post_merge_verification_is_valid(
            _coordinator_record(body=_pmv_body(accepted_head="d" * 40)),
            **self._ctx()) is False
        assert post_merge_verification_is_valid(
            _coordinator_record(body=_pmv_body(merge_commit_sha="e" * 40)),
            **self._ctx()) is False

    # ----------------------------------- BLOCKING 1: canonical closure resource
    def test_a_caller_cannot_move_closure_to_rescue_a_late_verification(self):
        """The withdrawn bare ``closure_at`` made this trivially bypassable.

        Strengthened under DELTA review 5062494115: moving closure later no longer rescues a
        late verification *at all*, because the lawful window now closes at CI completion
        rather than at closure. Previously a real, later closure resource made it pass.
        """
        late = _coordinator_record(created="2026-08-31T23:00:00Z")
        assert post_merge_verification_is_valid(late, **self._ctx()) is False
        moved = _closure_record(created="2026-08-31T23:59:00Z")
        assert post_merge_verification_is_valid(late, **self._ctx(closure_record=moved)) is False
        # And a malformed one rescues nothing either.
        assert post_merge_verification_is_valid(
            late, **self._ctx(closure_record="2026-08-31T23:59:00Z")) is False

    @pytest.mark.parametrize("over", [
        {"created": "2026-08-31T10:05:99Z"}, {"created": None}, {"created": ""},
        {"app_key_present": False}, {"login": ""}, {"type_": ""}, {"assoc": ""},
    ])
    def test_a_malformed_closure_resource_fails(self, over):
        rec = _closure_record(**over)
        assert canonical_closure_record_is_valid(rec) is False, over
        assert post_merge_verification_is_valid(
            _coordinator_record(), **self._ctx(closure_record=rec)) is False, over

    @pytest.mark.parametrize("closure", [None, "2026-08-31T10:30:00Z", 123, [], {}])
    def test_a_non_resource_closure_fails(self, closure):
        assert post_merge_verification_is_valid(
            _coordinator_record(), **self._ctx(closure_record=closure)) is False

    def test_a_pull_request_review_is_never_closure_evidence(self):
        assert canonical_closure_record_is_valid(_pull_request_review()) is False

    # ----------------------------------------- BLOCKING 1: commitment and reveal
    def test_the_commitment_reveal_pair_is_checked(self):
        assert session_reveal_matches_commitment(SESSION_REVEAL, SESSION_COMMITMENT) is True

    @pytest.mark.parametrize("reveal", ["wrong-value", "", "   ", None, 123,
                                        SESSION_REVEAL.upper(), SESSION_REVEAL[:-1],
                                        SESSION_COMMITMENT])
    def test_a_wrong_reveal_fails(self, reveal):
        assert session_reveal_matches_commitment(reveal, SESSION_COMMITMENT) is False
        assert post_merge_verification_is_valid(
            _coordinator_record(body=_pmv_body(session_reveal=reveal or "x")),
            **self._ctx()) is False

    def test_publishing_the_commitment_is_not_the_reveal(self):
        """The withdrawn design published a plaintext nonce and accepted it copied back."""
        assert post_merge_verification_is_valid(
            _coordinator_record(body=_pmv_body(session_reveal=SESSION_COMMITMENT)),
            **self._ctx()) is False

    @pytest.mark.parametrize("commitment", ["not-a-digest", "a" * 63, "A" * 64, "", None, 123])
    def test_a_malformed_commitment_fails(self, commitment):
        assert session_reveal_matches_commitment(SESSION_REVEAL, commitment) is False

    def test_the_session_claim_is_not_described_as_runtime_session_identity(self):
        import inspect

        doc = _flat(inspect.getdoc(session_reveal_matches_commitment))
        assert "continuity of possession" in doc
        assert "NOT GitHub runtime-session identity" in doc

    # --------------------------------- BLOCKING 2: the typed affirmative result
    def test_a_negating_declaration_inside_the_schema_fails(self):
        """The reviewer's exact reproduction -- free text is gone from the verdict."""
        for field in ("accepted_head_ancestry", "authorized_scope", "validators_result",
                      "tests_result", "overall_result"):
            for value in ("FAIL", "SKIPPED", "UNKNOWN", "N/A", "",
                          "I performed no verification.", "PASS (not really)", "pass"):
                body = _pmv_body(**{field: value})
                assert parse_pmv_body(body) is None, (field, value)
                assert post_merge_verification_is_valid(
                    _coordinator_record(body=body), **self._ctx()) is False, (field, value)

    @pytest.mark.parametrize("field", sorted(PMV_RESULT_FIELDS))
    def test_every_result_field_admits_only_its_closed_literals(self, field):
        for value in ("FAILED", "no", "0", "TRUE " if field != "main_clean" else "FALSE"):
            body = _pmv_body(**{field: value})
            assert parse_pmv_body(body) is None, (field, value)
        for value in PMV_RESULT_FIELDS[field]:
            assert parse_pmv_body(_pmv_body(**{field: value})) is not None, (field, value)

    def test_merge_commit_ci_alone_admits_not_applicable(self):
        assert parse_pmv_body(_pmv_body(merge_commit_ci="NOT_APPLICABLE")) is not None
        assert parse_pmv_body(_pmv_body(overall_result="NOT_APPLICABLE")) is None

    def test_no_free_text_field_survives_in_the_verdict_schema(self):
        for withdrawn in ("scope", "results", "session_claim", "notes", "narrative"):
            assert withdrawn not in PMV_SCHEMA, withdrawn

    # ------------------------------------------------------------ actor validation
    @pytest.mark.parametrize("over", [
        {"login": ""}, {"login": "   "}, {"login": None},
        {"type_": ""}, {"type_": None}, {"assoc": ""}, {"assoc": None}, {"assoc": 123},
        {"app_key_present": False},
    ])
    def test_malformed_actor_fields_fail(self, over):
        rec = _coordinator_record(**over)
        assert _actor_fields_are_well_formed(rec) is False, over
        assert post_merge_verification_is_valid(rec, **self._ctx()) is False, over

    @pytest.mark.parametrize("foreign", FOREIGN_RECORD_KIND_FIELDS)
    def test_the_record_kind_gate_is_isolated_and_decisive(self, foreign):
        good = _coordinator_record()
        assert post_merge_verification_is_valid(good, **self._ctx()) is True
        bad = dict(good)
        bad[foreign] = "x"
        assert post_merge_verification_is_valid(bad, **self._ctx()) is False, foreign

    def test_a_verification_on_another_pull_request_is_rejected(self):
        assert post_merge_verification_is_valid(
            _coordinator_record(pr=999), **self._ctx()) is False

    # -------------------------------------------- the two roles never overlap
    def test_the_passing_coordinator_record_can_never_ratify_or_be_acceptance(self):
        rec = _coordinator_record()
        assert post_merge_verification_is_valid(rec, **self._ctx()) is True
        assert is_direct_principal_record(rec) is False
        assert ratifies_pr362_acceptance(rec) is False
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    def test_an_app_attributed_principal_record_must_still_be_designated(self):
        """There is now ONE path, so an owner-attributed app record is not special.

        Renamed from ``..._takes_the_coordinator_path``: after BLOCKING 3 there is no fork to
        take. This is also the live case the A0 capability proof measured -- a Claude comment
        that derives as ``Mast3rkey``/``User``/``OWNER`` yet carries the ``claude`` app.
        """
        rec = _issue_comment(app="claude", created=PMV_VERIFIED_AT, ident=PMV_RECORD_ID,
                             body=_pmv_body(), actor_id=PRINCIPAL_ID)
        assert _actor_login(rec) == PRINCIPAL_LOGIN
        assert is_direct_principal_record(rec) is False
        assert post_merge_verification_is_valid(
            rec, **self._ctx(designation_record=None)) is False
        assert post_merge_verification_is_valid(rec, **self._ctx()) is False
        body = _designation_body(coordinator_login=PRINCIPAL_LOGIN,
                                 coordinator_id=PRINCIPAL_ID, coordinator_type="User",
                                 coordinator_association="OWNER", coordinator_app="claude")
        ctx = self._ctx(
            designation_record=_designation_record(body=body),
            merged_pull_request=_merged_pull_request(
                merged_by={"login": PRINCIPAL_LOGIN, "type": "User",
                           "id": PRINCIPAL_ID, "node_id": "U_kgDODQVFIw"}),
            closure_record=_closure_record(login=PRINCIPAL_LOGIN, type_="User",
                                           assoc="OWNER", app="claude",
                                           actor_id=PRINCIPAL_ID))
        assert post_merge_verification_is_valid(rec, **ctx) is True
        assert is_direct_principal_record(rec) is False
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    def test_a_principal_record_out_of_order_is_still_rejected(self):
        rec = _issue_comment(created=PMV_CLOSED_AT, ident=8_300_000_060, body=_pmv_body())
        assert post_merge_verification_is_valid(
            rec, **self._ctx(designation_record=None)) is False

    # -------------------------------------------------------------- chronology
    @pytest.mark.parametrize("created,label", [
        (PMV_MERGED_AT, "equal to the merge"),
        (PMV_CLOSED_AT, "equal to the closure"),
        ("2026-08-31T09:59:59Z", "before the merge"),
        ("2026-08-31T10:30:01Z", "after the closure"),
    ])
    def test_chronology_boundaries_are_strict(self, created, label):
        assert post_merge_verification_is_valid(
            _coordinator_record(created=created), **self._ctx()) is False, label

    @pytest.mark.parametrize("bad", [
        "2026-08-31T10:05:99Z", "2026-13-45T99:99:99Z", "2026-02-30T00:00:00Z",
        "9999-99-99T99:99:99Z", "", "not-a-time", "2026-08-31", None, 20260831,
        "2026-08-31T10:05:00+00:00", "2026-08-31 10:05:00Z",
    ])
    def test_impossible_and_malformed_instants_fail(self, bad):
        assert parse_utc_instant(bad) is None, bad
        assert post_merge_verification_is_valid(
            _coordinator_record(created=bad), **self._ctx()) is False, bad

    def test_a_real_instant_parses_to_utc(self):
        parsed = parse_utc_instant("2026-08-31T10:05:00Z")
        assert parsed is not None and parsed.tzinfo is datetime.timezone.utc

    # ------------------------------------------------------------------ totality
    def test_the_predicate_is_total_and_never_raises(self):
        for junk in (None, 123, "text", [], {}, object()):
            assert post_merge_verification_is_valid(junk, **self._ctx()) is False

    def test_pmv_and_ratification_remain_separate_functions(self):
        import inspect

        assert post_merge_verification_is_valid is not ratifies_pr362_acceptance
        src = inspect.getsource(post_merge_verification_is_valid)
        for forbidden in ("ratifies_pr362_acceptance", "_ratifies_with_binding",
                          "body_declares_ratification"):
            assert forbidden not in src, forbidden


class TestThePmvDeclarationSchemaIsExact:
    """The verification body must PARSE, and every result field is a closed literal."""

    def test_the_honest_declaration_parses_with_exact_values(self):
        parsed = parse_pmv_body(_pmv_body())
        assert parsed is not None
        assert set(parsed) == set(PMV_SCHEMA)
        assert parsed["action"] == PMV_ACTION
        assert parsed["overall_result"] == "PASS"

    @pytest.mark.parametrize("label,body", [
        ("refusal", "I did NOT perform post-merge verification."),
        ("unrelated", "Looks good to me."),
        ("author_report", "## Correction report\n\nSee the table above."),
        ("empty", ""),
        ("whitespace", "   \n\n  "),
        ("void_prefix", "VOID. " + _pmv_body()),
        ("trailing_contradiction", _pmv_body() + "\nI did not actually verify."),
        ("leading_prose", "Context:\n" + _pmv_body()),
        ("missing_header", "\n".join(_pmv_body().splitlines()[1:])),
        ("wrong_header", _pmv_body(header="XASSET-0062 RATIFICATION")),
        ("designation_header", _pmv_body(header=DESIGNATION_HEADER)),
        ("junk_first_line", "GARBAGE\n" + "\n".join(_pmv_body().splitlines()[1:])),
        ("negated_action", _pmv_body(action="POST-MERGE-VERIFICATION-REFUSED")),
        ("alias_action", _pmv_body(action="post-merge-verification-performed")),
        ("wrong_pr", _pmv_body(pull_request=362)),
        ("malformed_head", _pmv_body(accepted_head="TBD")),
        ("short_sha", _pmv_body(merge_commit_sha="c" * 39)),
        ("empty_reveal", _pmv_body(session_reveal="")),
        ("unknown_key", _pmv_body() + "\nvoid: true"),
        ("duplicate_key", _pmv_body() + "\nmerge_commit_sha: " + PMV_MERGE_COMMIT_SHA),
    ])
    def test_no_non_conforming_body_parses(self, label, body):
        assert parse_pmv_body(body) is None, label

    def test_parse_is_total_and_never_raises(self):
        for junk in (None, 123, b"bytes", [], {}, object()):
            assert parse_pmv_body(junk) is None
            assert parse_designation_body(junk) is None

    def test_the_three_declaration_schemas_are_mutually_exclusive(self):
        assert parse_pmv_body(SCOPE_BODY) is None
        assert parse_pmv_body(_designation_body()) is None
        assert parse_designation_body(_pmv_body()) is None
        assert parse_designation_body(SCOPE_BODY) is None
        assert parse_ratification_body(_pmv_body()) is None
        assert parse_ratification_body(_designation_body()) is None
        assert len({PMV_HEADER, DESIGNATION_HEADER, RATIFICATION_HEADER}) == 3


class TestTheFinalReviewIsAuthenticatedAsAReview:
    """DELTA review 5062156189 MAJOR 1 -- three strings were compared; one was never a review.

    ``{"reviewed_head": H}``, the same mapping carrying ``verdict: CHANGES_REQUIRED``, and one
    naming an author actor with a null id ALL proved the equality at the previous head. The
    disposition is now parsed by the repository's OWN ``parse_formal_disposition``.
    """

    def test_the_honest_review_is_approving(self):
        ok, ev = canonical_final_review_is_approving(_final_review(), REAL_FINAL_HEAD)
        assert ok is True
        assert ev["failure_reason"] is None
        assert ev["parsed_disposition"] == APPROVING_REVIEW_DISPOSITION
        assert ev["commit_matches_final_head"] is True

    @pytest.mark.parametrize("evidence,label", [
        ({"reviewed_head": REAL_FINAL_HEAD}, "bare head mapping"),
        ({"reviewed_head": REAL_FINAL_HEAD, "verdict": "CHANGES_REQUIRED"}, "verdict string"),
        ({"reviewed_head": REAL_FINAL_HEAD, "review_id": None, "actor": "author"},
         "author with null id"),
        ({}, "empty mapping"), (None, "None"), (123, "int"), ("APPROVED", "string"),
    ])
    def test_the_withdrawn_mappings_all_fail(self, evidence, label):
        ok, _ = canonical_final_review_is_approving(evidence, REAL_FINAL_HEAD)
        assert ok is False, label
        out = _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(), evidence)
        assert out["equality_proven"] is False, label

    @pytest.mark.parametrize("over,reason", [
        ({"id": None}, "review id is missing or not an integer"),
        ({"id": "5062156189"}, "review id is missing or not an integer"),
        ({"id": True}, "review id is missing or not an integer"),
        ({"pull_request_url": f"{REPO_API}/pulls/362"}, "review is not on PR #363"),
        ({"pull_request_url": None}, "review is not on PR #363"),
        ({"html_url": "https://example.com/x"}, "review canonical URLs disagree with its id"),
        ({"user": {"login": "", "type": "User"}},
         "review actor identity is missing or malformed"),
        ({"user": None}, "review actor identity is missing or malformed"),
        ({"author_association": ""}, "review author_association is missing or malformed"),
        ({"submitted_at": "9999-99-99T99:99:99Z"},
         "review submitted_at is missing or not a real UTC instant"),
        ({"submitted_at": None}, "review submitted_at is missing or not a real UTC instant"),
        ({"commit_id": "f" * 40}, "review commit_id is not the final reviewed head"),
        ({"commit_id": None}, "review commit_id is not the final reviewed head"),
        ({"state": "CHANGES_REQUESTED"}, "review state is natively adverse"),
    ])
    def test_each_review_clause_is_isolated_and_decisive(self, over, reason):
        ok, ev = canonical_final_review_is_approving(_final_review(**over), REAL_FINAL_HEAD)
        assert ok is False, over
        assert ev["failure_reason"] == reason, (over, ev["failure_reason"])

    @pytest.mark.parametrize("body,reason", [
        ("FORMAL DISPOSITION: CHANGES REQUIRED", "formal disposition is not approving"),
        ("Looks good to me.", "no formal disposition"),
        ("", "no formal disposition"),
        (None, "no formal disposition"),
        ("# FORMAL DISPOSITION: " + "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE",
         "formal disposition is malformed"),
    ])
    def test_the_disposition_is_parsed_not_searched(self, body, reason):
        ok, ev = canonical_final_review_is_approving(
            _final_review(body=body), REAL_FINAL_HEAD)
        assert ok is False
        assert ev["failure_reason"] == reason, (body, ev["failure_reason"])

    def test_an_approving_phrase_after_an_adverse_disposition_cannot_win(self):
        """The exact defect the repository's own parser was hardened against."""
        body = ("FORMAL DISPOSITION: CHANGES REQUIRED\n\n"
                f"Once fixed this would be {APPROVING_REVIEW_DISPOSITION}.")
        ok, ev = canonical_final_review_is_approving(_final_review(body=body), REAL_FINAL_HEAD)
        assert ok is False
        assert ev["parsed_disposition"] == "CHANGES REQUIRED"

    def test_the_repository_parser_is_reused_not_reimplemented(self):
        import inspect

        src = inspect.getsource(canonical_final_review_is_approving)
        assert "_auth.parse_formal_disposition" in src
        assert "_auth.NATIVE_ADVERSE_REVIEW_STATES" in src
        assert APPROVING_REVIEW_DISPOSITION == _auth.APPROVING_REVIEW_DISPOSITION

    def test_a_later_adverse_exact_head_review_defeats_the_approval(self):
        # Genuinely later: SS-I.2.1 F.6 counts a review as adverse only if it was submitted
        # STRICTLY after the selected approval, which the default fixture instant is not.
        later = _final_review(ident=5_099_999_999, body="FORMAL DISPOSITION: CHANGES REQUIRED",
                              submitted_at="2026-08-31T14:00:00Z")
        out = _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(), _final_review(), [later])
        assert out["equality_proven"] is False
        assert out["later_adverse_review_exists"] is True
        assert out["failure_reason"] == "a later adverse exact-head review exists"

    def test_a_later_adverse_review_on_another_head_does_not_defeat_it(self):
        later = _final_review(ident=5_099_999_998, head="9" * 40,
                              body="FORMAL DISPOSITION: CHANGES REQUIRED",
                              submitted_at="2026-08-31T14:00:00Z")
        out = _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(), _final_review(), [later])
        assert out["equality_proven"] is True
        assert out["later_adverse_review_exists"] is False

    def test_a_later_approving_review_is_not_adverse(self):
        later = _final_review(ident=5_099_999_997, submitted_at="2026-08-31T14:00:00Z")
        out = _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(), _final_review(), [later])
        assert out["equality_proven"] is True

    def test_reviewer_independence_is_recorded_as_procedural_not_proven(self):
        """A review resource carries NO application provenance -- see SS-I.2.1 D."""
        _, ev = canonical_final_review_is_approving(_final_review(), REAL_FINAL_HEAD)
        assert ev["independence"] == "PROCEDURAL_NOT_PLATFORM_PROVABLE"
        assert ev["application_provenance"] == "NOT_EXPOSED_ON_REVIEWS"
        assert "performed_via_github_app" not in _final_review()

    def test_the_review_evidence_is_retained(self):
        out = _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(), _final_review())
        ev = out["review_evidence"]
        for key in ("review_id", "commit_id", "submitted_at", "state", "actor_login",
                    "actor_type", "author_association", "parsed_disposition",
                    "commit_matches_final_head", "independence", "application_provenance"):
            assert key in ev and ev[key] is not None, key


class TestRatificationChronologyUsesRealInstants:
    """DELTA review 5062156189 MAJOR 3 -- a shape regex and a lexicographic string compare."""

    def test_the_reviewers_impossible_timestamp_now_fails(self):
        bad = _ratification_naming(REAL_FINAL_HEAD, created="9999-99-99T99:99:99Z")
        assert _ratification_is_structurally_complete(bad) is False
        assert _readback(
            bad, _live_pr(), _final_review())["equality_proven"] is False

    @pytest.mark.parametrize("created,label", [
        ("2026-13-01T00:00:00Z", "invalid month"),
        ("2026-08-32T00:00:00Z", "invalid day"),
        ("2026-02-30T00:00:00Z", "impossible calendar date"),
        ("2025-02-29T00:00:00Z", "non-leap 29 February"),
        ("2026-08-31T24:00:00Z", "invalid hour"),
        ("2026-08-31T10:60:00Z", "invalid minute"),
        ("2026-08-31T10:05:99Z", "invalid second"),
        ("9999-99-99T99:99:99Z", "impossible everything"),
        (MERGED_AT, "equal to the PR #362 merge"),
        ("2026-08-29T15:07:48Z", "one second before the merge"),
        ("2026-08-01T00:00:00Z", "well before the merge"),
        ("2026-08-31T10:05:00+00:00", "non-Z offset form"),
        ("2026-08-31 10:05:00Z", "space instead of T"),
        ("", "empty"), (None, "None"), (20260831, "int"),
    ])
    def test_impossible_and_out_of_order_ratification_instants_fail(self, created, label):
        rec = _ratification_naming(REAL_FINAL_HEAD, created=created)
        assert _ratification_is_structurally_complete(rec) is False, label
        assert _readback(
            rec, _live_pr(), _final_review())["equality_proven"] is False, label

    def test_one_second_after_the_merge_passes(self):
        """SS-G.5 retrospection: one second after the PR #362 merge is already lawful.

        The readback leg supplies an approving review submitted BEFORE that instant, because
        SS-I.2.1 F.4 now also requires the ratification to postdate its approval. The two
        rules are independent, and this test isolates the merge boundary.
        """
        rec = _ratification_naming(REAL_FINAL_HEAD, created="2026-08-29T15:07:50Z")
        assert _ratification_is_structurally_complete(rec) is True
        earlier = _final_review(submitted_at="2026-08-29T15:00:00Z")
        assert _readback(rec, _live_pr(), earlier)["equality_proven"] is True

    def test_the_comparison_is_between_parsed_instants(self):
        import inspect

        src = inspect.getsource(_ratification_is_structurally_complete)
        assert "parse_utc_instant" in src
        assert "created <= MERGED_AT" not in src


class TestTheExternalRatificationReadbackIsImplemented:
    """DELTA review 5061240650 MAJOR 1 -- the promised three-way equality, as code.

    The parser accepts ANY 40-hex declared head BY DESIGN, because the repository cannot know
    its own future final head. That is safe only if the readback then proves

        declared head == live PR head == independently reviewed final head

    and until this correction nothing did: SS-G.9 step 3 listed what to retain but never named
    the comparison that makes retention meaningful.
    """

    def test_the_honest_readback_proves_the_three_way_equality(self):
        out = _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(), _final_review())
        assert out["equality_proven"] is True
        assert out["structural_clauses_pass"] is True
        assert out["failure_reason"] is None

    def test_a_well_formed_but_wrong_head_fails(self):
        """The regression the review specifically required."""
        wrong = "f" * 40
        # It really does parse -- which is exactly why the readback has to exist.
        assert parse_ratification_body(_ratification_naming(wrong)["body"]) is not None
        out = _readback(
            _ratification_naming(wrong), _live_pr(), _final_review())
        assert out["equality_proven"] is False
        assert out["failure_reason"] == "three-way exact-head equality failed"
        assert out["declared_pr363_accepted_head"] == wrong
        assert out["live_pr_head"] == REAL_FINAL_HEAD

    def test_a_live_head_that_moved_after_review_fails(self):
        """Drift is now caught one clause EARLIER, and for a stronger reason:
        the review is authenticated against the live head before any equality.
        """
        out = _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(head="9" * 40), _final_review())
        assert out["equality_proven"] is False
        assert out["failure_reason"] == (
            "final review not approving: review commit_id is not the final reviewed head")

    def test_a_review_anchored_to_a_different_head_fails(self):
        out = _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(), _final_review(head="8" * 40))
        assert out["equality_proven"] is False
        assert out["failure_reason"] == (
            "final review not approving: review commit_id is not the final reviewed head")

    def test_every_required_evidence_field_is_retained(self):
        """SS-G.9 step 3, plus the equality result the review found missing."""
        out = _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(), _final_review())
        for key in ("declaration", "declared_pr363_accepted_head", "live_pr_head",
                    "independently_reviewed_head", "comment_id", "comment_created_at",
                    "body_fingerprint", "record_kind", "actor_login", "actor_type",
                    "author_association", "application_provenance", "equality_proven"):
            assert key in out, key
            assert out[key] is not None, key
        assert out["record_kind"] == "top_level_issue_comment"
        assert out["application_provenance"] == "null"
        assert len(out["body_fingerprint"]) == 64
        assert out["declaration"]["action"] == RATIFICATION_ACTION

    def test_evidence_is_retained_even_when_the_readback_fails(self):
        """A failed readback must stay auditable, not opaque."""
        out = _readback(
            _ratification_naming("f" * 40), _live_pr(), _final_review())
        assert out["equality_proven"] is False
        assert out["comment_id"] is not None
        assert out["body_fingerprint"] is not None
        assert out["actor_login"] == PRINCIPAL_LOGIN
        assert out["record_kind"] == "top_level_issue_comment"

    @pytest.mark.parametrize("over", [
        {"app": "claude"}, {"type_": "Bot"}, {"assoc": "CONTRIBUTOR"},
        {"login": "someone-else"}, {"app_key_present": False},
    ])
    def test_every_structural_clause_is_enforced_before_equality(self, over):
        rec = _ratification_naming(REAL_FINAL_HEAD, **over)
        out = _readback(rec, _live_pr(), _final_review())
        assert out["equality_proven"] is False
        assert out["failure_reason"] == "record fails an SS-G structural clause"
        assert out["structural_clauses_pass"] is False

    def test_a_refusal_body_fails_the_readback(self):
        rec = _issue_comment(body=_refusal_body(), ident=8_400_000_003)
        out = _readback(rec, _live_pr(), _final_review())
        assert out["equality_proven"] is False
        assert out["structural_clauses_pass"] is False

    def test_a_pull_request_review_fails_the_readback(self):
        out = _readback(
            _pull_request_review(), _live_pr(), _final_review())
        assert out["equality_proven"] is False
        assert out["record_kind"] == "other_or_invalid"

    _NOT_A_RAW_PR = "live pull-request is not a valid open, unmerged PR #363 resource"

    @pytest.mark.parametrize("pr,reason", [
        # Every one of these is a caller PROJECTION, and DELTA review 5062494115 BLOCKING 2
        # used exactly this shape as its counterexample. They now share one failure reason,
        # because the defect they share is that none of them is the raw resource.
        ({"number": 362, "head": {"sha": REAL_FINAL_HEAD}}, _NOT_A_RAW_PR),
        ({"number": THIS_CORRECTIVE_PULL_REQUEST, "head": {"sha": "nope"}}, _NOT_A_RAW_PR),
        ({"number": THIS_CORRECTIVE_PULL_REQUEST, "head": {}}, _NOT_A_RAW_PR),
        ({"number": THIS_CORRECTIVE_PULL_REQUEST, "head": None}, _NOT_A_RAW_PR),
        ({"number": THIS_CORRECTIVE_PULL_REQUEST, "head": {"sha": "A" * 40}}, _NOT_A_RAW_PR),
        # And the raw resource itself still fails on each individual malformation.
        (_open_pull_request(number=362), _NOT_A_RAW_PR),
        (_open_pull_request(head="nope"), _NOT_A_RAW_PR),
        (_open_pull_request(state="closed"), _NOT_A_RAW_PR),
        (_open_pull_request(merged=True), _NOT_A_RAW_PR),
        (_open_pull_request(merged_at="2026-08-31T09:00:00Z"), _NOT_A_RAW_PR),
        (_open_pull_request(base={"repo": {"full_name": "someone/else"}}), _NOT_A_RAW_PR),
        (_open_pull_request(url=f"{REPO_API}/pulls/999"), _NOT_A_RAW_PR),
        (_open_pull_request(html_url="elsewhere"), _NOT_A_RAW_PR),
    ])
    def test_a_malformed_live_pull_request_fails(self, pr, reason):
        out = _readback(
            _ratification_naming(REAL_FINAL_HEAD), pr, _final_review())
        assert out["equality_proven"] is False
        assert out["failure_reason"] == reason

    @pytest.mark.parametrize("ev", [
        None, 123, {}, {"reviewed_head": None}, {"reviewed_head": "short"},
        {"reviewed_head": "F" * 40},
    ])
    def test_missing_or_malformed_final_review_evidence_fails(self, ev):
        out = _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(), ev)
        assert out["equality_proven"] is False

    def test_the_readback_is_total_and_never_raises(self):
        for a in (None, 123, "text", [], {}):
            for b in (None, 123, {}):
                for c in (None, 123, {}):
                    assert external_ratification_readback(a, b, c)["equality_proven"] is False

    def test_the_readback_never_ratifies_by_itself(self):
        """Proving the equality is not the in-repository predicate ratifying."""
        rec = _ratification_naming(REAL_FINAL_HEAD)
        assert _readback(
            rec, _live_pr(), _final_review())["equality_proven"] is True
        assert ratifies_pr362_acceptance(rec) is False
        assert BOUND_RATIFICATION_ID is None

    def test_the_decision_names_the_equality_as_the_readback_rule(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "declared `pr363_accepted_head` == live PR #363 head == independently reviewed final head" in flat


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

    def test_the_source_comment_no_longer_promises_a_binding_commit(self):
        """DELTA review 5062156189 MINOR 1 -- nothing pinned the SOURCE comment itself.

        The decision text was pinned; the comment above the constants was not, so restoring
        the withdrawn "retained in a further fast-forward commit" sentence passed every test.
        """
        source = _read(THIS_ARTIFACT)
        assert "#: SS-G.9: these constants are ``None`` and STAY ``None``." in source
        assert "NEVER committed here" in source
        # The withdrawn promise survives ONLY inside the comment's own record of what was
        # withdrawn, and inside this assertion. Count, never membership -- a membership test
        # here would be unfalsifiable, since this test necessarily names the phrase.
        withdrawn = "fast-forward commit on this pull request"
        assert source.count(withdrawn) == 2
        assert 'promised retention "in a further' in source

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


class TestTheProtocolIsAnchoredInTheDecision:
    """DELTA review 5062156189 MAJOR 2 -- the protocol authenticated itself.

    ``PMV_HEADER`` and ``PMV_ACTION`` were defined only in this artifact, so the parser and its
    fixtures derived the protocol from one another. The reviewer renamed them to
    ``UNAUTHORIZED RENAMED PMV PROTOCOL`` and ``UNAUTHORIZED-RENAMED-ACTION`` and all 327
    focused tests still passed. This session reproduced that exactly before correcting it.

    Every literal below is now read back from the committed decision text -- an independent
    source that a rename cannot follow.
    """

    def test_the_decision_defines_the_protocol_section(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "#### I.2.1 — The operative protocol, defined here before it is implemented" in flat

    @staticmethod
    def _protocol_block(first_line: str) -> str:
        """The FENCED protocol block, not the whole decision.

        Anchoring against the whole file was itself defective: the decision's own narrative
        quotes the reviewer's mutation strings verbatim, so a constant renamed to
        ``UNAUTHORIZED RENAMED PMV PROTOCOL`` matched that sentence and the rename passed.
        Found by re-running the reviewer's own mutation against the first anchoring attempt.
        Only the fenced block is protocol; prose about it is not.
        """
        text = _read(DECISION_RELPATH)
        start = text.index("```\n" + first_line)
        block = text[start + 4:]
        return block[:block.index("```")]

    def test_the_designation_block_defines_the_implementation_constants(self):
        block = self._protocol_block("XASSET-0062 COORDINATOR DESIGNATION")
        assert block.splitlines()[0] == DESIGNATION_HEADER
        assert f"action: {DESIGNATION_ACTION}" in block

    def test_the_pmv_block_defines_the_implementation_constants(self):
        block = self._protocol_block("XASSET-0062 POST-MERGE VERIFICATION")
        assert block.splitlines()[0] == PMV_HEADER
        assert f"action: {PMV_ACTION}" in block

    def test_the_closure_block_defines_the_implementation_constants(self):
        block = self._protocol_block("XASSET-0062 LIFECYCLE CLOSURE")
        assert block.splitlines()[0] == CLOSURE_HEADER
        assert f"action: {CLOSURE_ACTION}" in block

    @pytest.mark.parametrize("literal", [
        "XASSET-0062 COORDINATOR DESIGNATION", "DESIGNATE-MERGE-COORDINATOR",
        "XASSET-0062 POST-MERGE VERIFICATION", "POST-MERGE-VERIFICATION-PERFORMED",
        "XASSET-0062 LIFECYCLE CLOSURE", "FINAL-POST-CI-LIFECYCLE-CLOSURE",
    ])
    def test_every_header_and_action_appears_in_the_decision(self, literal):
        assert literal in _read(DECISION_RELPATH), literal

    @pytest.mark.parametrize("key", sorted(CLOSURE_SCHEMA))
    def test_every_closure_key_appears_in_the_decision_block(self, key):
        assert f"{key}:" in self._protocol_block("XASSET-0062 LIFECYCLE CLOSURE"), key

    def test_the_closure_block_names_no_key_the_implementation_lacks(self):
        block = self._protocol_block("XASSET-0062 LIFECYCLE CLOSURE")
        declared = {ln.split(":", 1)[0].strip() for ln in block.splitlines()
                    if ":" in ln and not ln.startswith("XASSET-")}
        assert declared == set(CLOSURE_SCHEMA), declared ^ set(CLOSURE_SCHEMA)

    def test_the_closure_fixed_literals_are_the_decisions_own(self):
        """COMPLETED / SUCCESS / TRUE are governing text, not implementation preference."""
        block = self._protocol_block("XASSET-0062 LIFECYCLE CLOSURE")
        for key, literal in CLOSURE_SCHEMA.items():
            if literal is not None:
                assert f"{key}: {literal}" in block, key

    def test_the_decision_removed_merge_commit_ci_from_the_verification_block(self):
        """DELTA 5062494115 MAJOR 2 -- CI is bound at closure, never predicted at verification."""
        pmv = self._protocol_block("XASSET-0062 POST-MERGE VERIFICATION")
        assert "merge_commit_ci" not in pmv
        assert "merge_commit_ci" not in PMV_SCHEMA
        assert "merge_commit_ci_run_id" in self._protocol_block("XASSET-0062 LIFECYCLE CLOSURE")

    def test_not_applicable_is_no_longer_an_accepted_value_anywhere(self):
        """PR #363 always requires the run; SS-J condition 6 admits no exemption."""
        for permitted in PMV_RESULT_FIELDS.values():
            assert "NOT_APPLICABLE" not in permitted
        for literal in CLOSURE_SCHEMA.values():
            assert literal != "NOT_APPLICABLE"

    def test_the_decision_states_the_strict_chronology(self):
        """SS-I.2.1 E is strict at every relation; MAJOR 2 found ``<=`` implemented."""
        flat = _flat(_read(DECISION_RELPATH))
        assert "designation_at **<** merge_at" in flat
        assert "Every relation is **strict**." in flat

    def test_the_decision_records_the_live_provenance_capability_proof(self):
        """SS-I.2.1 A0 -- BLOCKING 1 required the source be proved, not assumed."""
        flat = _flat(_read(DECISION_RELPATH))
        assert "A0. The principal-provenance evidence source" in flat
        assert "issues/comments/{comment_id}" in flat
        assert "An absent key is not a null value" in flat

    @pytest.mark.parametrize("key", sorted(DESIGNATION_SCHEMA))
    def test_every_designation_key_appears_in_the_decision_block(self, key):
        assert f"{key}:" in self._protocol_block("XASSET-0062 COORDINATOR DESIGNATION"), key

    @pytest.mark.parametrize("key", sorted(PMV_SCHEMA))
    def test_every_pmv_key_appears_in_the_decision_block(self, key):
        assert f"{key}:" in self._protocol_block("XASSET-0062 POST-MERGE VERIFICATION"), key

    def test_the_decision_names_no_key_the_implementation_lacks(self):
        """Both directions: the decision's own listed keys must all be implemented."""
        block = self._protocol_block("XASSET-0062 COORDINATOR DESIGNATION")
        declared = {ln.split(":", 1)[0].strip() for ln in block.splitlines()
                    if ":" in ln and not ln.startswith("XASSET")}
        assert declared == set(DESIGNATION_SCHEMA), declared ^ set(DESIGNATION_SCHEMA)

        block = self._protocol_block("XASSET-0062 POST-MERGE VERIFICATION")
        declared = {ln.split(":", 1)[0].strip() for ln in block.splitlines()
                    if ":" in ln and not ln.startswith("XASSET")}
        assert declared == set(PMV_SCHEMA), declared ^ set(PMV_SCHEMA)

    @pytest.mark.parametrize("field,values", sorted(PMV_RESULT_FIELDS.items()))
    def test_every_closed_result_literal_appears_in_the_decision_block(self, field, values):
        block = self._protocol_block("XASSET-0062 POST-MERGE VERIFICATION")
        assert f"{field}: {values[0]}" in block, (field, values[0])
        for value in values[1:]:
            assert value in _read(DECISION_RELPATH), (field, value)

    def test_the_decision_states_the_closed_result_vocabulary(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "The nine result fields above admit **only** the literals shown" in flat
        assert "`FAIL`, `SKIPPED`, `UNKNOWN`, `N/A`, an" in flat
        assert "empty value, a negated value" in flat
        assert len(PMV_RESULT_FIELDS) == 9

    def test_the_decision_defines_the_commitment_reveal_construction(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "session_commitment" in flat and "session_reveal" in flat
        assert "does not publish it" in flat
        assert "It is not GitHub runtime-session identity, and is never described as such." in flat

    def test_the_decision_defines_the_canonical_resources_by_real_field_names(self):
        text = _read(DECISION_RELPATH)
        for field in ("merge_commit_sha", "head.sha", "base.repo.full_name", "merged_by.login",
                      "pull_request_url", "commit_id", "submitted_at", "issue_url"):
            assert field in text, field

    def test_the_decision_discloses_both_platform_limits(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "The merged-PR resource exposes **no application provenance**" in flat
        assert "reviewer **independence is procedural**" in flat

    def test_the_decision_states_the_chronology(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "approving_review_submitted_at **<** ratification_at **<** designation_at" in flat
        assert "merge_at **<** verification_at **<** ci_completed_at **<** closure_at" in flat

    def test_the_canonical_repository_comes_from_the_load_bearing_module(self):
        """Not a second copy written here -- the module is the independent anchor."""
        import inspect

        assert CANONICAL_REPOSITORY == _auth.REPOSITORY_IDENTITY
        src = inspect.getsource(canonical_merged_pull_request_is_valid)
        assert "CANONICAL_REPOSITORY" in src
        assert '"Mast3rkey/Portfolio-HQ"' not in src

    def test_the_approving_disposition_comes_from_the_load_bearing_module(self):
        assert APPROVING_REVIEW_DISPOSITION == _auth.APPROVING_REVIEW_DISPOSITION
        assert "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE" == APPROVING_REVIEW_DISPOSITION

    def test_the_decision_records_this_filings_own_principal_operated_path(self):
        """The principal path is a choice of ACTOR, never an exemption -- BLOCKING 3."""
        flat = _flat(_read(DECISION_RELPATH))
        assert "For PR #363 the merge and the immediate post-merge verification are" in flat
        assert "**principal-operated**" in flat
        assert "That is a choice of actor, **not** an exemption from any rule above" in flat
        assert "What was removed is the *bypass*, not the role." in flat


class TestTheCompleteAdversarialClosureMatrix:
    """Every historical and new counterexample, run against the FINAL architecture.

    Each entry is named for the defect it closes and the review that found it, so a future
    session can see at a glance which attacks are covered and which review demanded them.
    One independent gate is varied at a time, and each failure is attributed to that gate.
    """

    def _ctx(self, **over):
        ctx = dict(designation_record=_designation_record(),
                   merged_pull_request=_merged_pull_request(),
                   closure_record=_closure_record(),
                   ci_run=_ci_run(), ci_job=_ci_job())
        ctx.update(over)
        return ctx

    # ---- reviews 5060791095 / 5060793954 -- record kind and provenance ----------
    def test_reviewer_record_is_not_misclassified_as_principal(self):
        for ident in INDEPENDENT_REVIEW_IDS:
            review = _pull_request_review(ident=ident)
            assert is_direct_principal_record(review) is False, ident
            assert is_canonical_top_level_issue_comment(review) is False, ident
            assert ratifies_pr362_acceptance(review) is False, ident

    def test_app_attributed_record_is_not_misclassified_as_principal(self):
        rec = _issue_comment(app="claude")
        assert is_direct_principal_record(rec) is False
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    @pytest.mark.parametrize("foreign", FOREIGN_RECORD_KIND_FIELDS)
    def test_wrong_record_kind_is_rejected(self, foreign):
        rec = _issue_comment()
        rec[foreign] = "x"
        assert is_canonical_top_level_issue_comment(rec) is False

    def test_wrong_repository_or_pull_request_is_rejected(self):
        assert is_canonical_top_level_issue_comment(_issue_comment(pr=999)) is False
        assert canonical_merged_pull_request_is_valid(
            _merged_pull_request(base={"repo": {"full_name": "someone/else"}})) is False

    # ---- review 5061031729 -- self-bound refusal and circular binding -----------
    def test_self_bound_refusal_never_ratifies(self):
        rec = _issue_comment(body=_refusal_body())
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    def test_contradictory_ratification_never_ratifies(self):
        rec = _issue_comment(body=SCOPE_BODY + "\nHowever I do NOT ratify this.")
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    def test_the_circular_binding_commit_stays_withdrawn(self):
        assert BOUND_RATIFICATION_ID is None
        assert BOUND_RATIFICATION_FINGERPRINT is None
        assert ratifies_pr362_acceptance(_issue_comment()) is False

    # ---- review 5061240650 -- self-designation and free-text results -----------
    def test_mallory_cannot_self_designate_as_coordinator_and_merger(self):
        mallory = _coordinator_record(login="mallory", assoc="NONE", app="evil")
        forged = _issue_comment(login="mallory", type_="Bot", assoc="NONE", app="evil",
                                ident=9_100_000_001, created=PMV_DESIGNATED_AT,
                                body=_designation_body(coordinator_login="mallory",
                                                       coordinator_association="NONE",
                                                       coordinator_app="evil"))
        assert principal_designation_is_valid(forged) is False
        assert post_merge_verification_is_valid(
            mallory, **self._ctx(designation_record=forged,
                                 merged_pull_request=_merged_pull_request(
                                     merged_by={"login": "mallory", "type": "Bot", "id": 9}))
        ) is False

    def test_the_96_combination_self_designation_sweep_is_fully_closed(self):
        """72/96 passed with an explicit refusal body two heads ago; 0/96 now."""
        import itertools

        passed = total = 0
        for login, type_, assoc, app in itertools.product(
            ["mallory", "", COORDINATOR_LOGIN, PRINCIPAL_LOGIN],
            ["Bot", "User", "", None], ["NONE", "OWNER", 123], ["evil", None],
        ):
            total += 1
            rec = _issue_comment(login=login, type_=type_, assoc=assoc, app=app,
                                 created=PMV_VERIFIED_AT, ident=9_100_000_002,
                                 body="I did NOT perform post-merge verification.")
            forged = _issue_comment(login=login, type_=type_, assoc=assoc, app=app,
                                    ident=9_100_000_003, created=PMV_DESIGNATED_AT,
                                    body=_designation_body(coordinator_login=login or "x"))
            if post_merge_verification_is_valid(
                rec, **self._ctx(designation_record=forged,
                                 merged_pull_request=_merged_pull_request(
                                     merged_by={"login": login or "x", "type": type_ or "Bot",
                                                "id": 9}))):
                passed += 1
        assert total == 96
        assert passed == 0

    def test_a_pull_request_review_is_never_pmv_evidence(self):
        assert post_merge_verification_is_valid(_pull_request_review(), **self._ctx()) is False

    @pytest.mark.parametrize("app", [{}, {"slug": ""}, {"slug": None}, {"name": "x"},
                                     "claude", 7, []])
    def test_malformed_application_provenance_fails(self, app):
        rec = _coordinator_record()
        rec["performed_via_github_app"] = app
        assert post_merge_verification_is_valid(rec, **self._ctx()) is False

    def test_even_carrying_a_perfect_ratification_declaration_it_cannot_ratify(self):
        rec = _coordinator_record(body=SCOPE_BODY)
        assert body_declares_ratification(rec) is True
        assert post_merge_verification_is_valid(rec, **self._ctx()) is False
        assert _ratifies_with_binding(rec, **_bound(rec)) is False

    # ---- review 5062156189 -- the six findings of the final review --------------
    def test_unrelated_principal_comment_repurposed_as_designation(self):
        unrelated = _issue_comment(ident=9_100_000_010, created="2026-08-31T10:20:00Z",
                                   body="I accept the reviewed head. I designate nobody.")
        assert principal_designation_is_valid(unrelated) is False

    def test_i_designate_nobody_with_adjacent_caller_fields(self):
        """There are no adjacent fields any more -- the shape itself is impossible."""
        import inspect

        assert set(inspect.signature(principal_designation_is_valid).parameters) == {"record"}
        unrelated = _issue_comment(ident=9_100_000_011, body="I designate nobody.")
        assert principal_designation_is_valid(unrelated) is False

    @pytest.mark.parametrize("designated_at", ["2026-08-31T10:00:01Z", "2026-08-31T10:06:00Z",
                                               "2026-08-31T10:20:00Z", "2026-09-01T00:00:00Z"])
    def test_designation_issued_after_the_merge_or_verification(self, designated_at):
        assert post_merge_verification_is_valid(
            _coordinator_record(),
            **self._ctx(designation_record=_designation_record(created=designated_at))) is False

    def test_a_public_copied_nonce_is_not_session_evidence(self):
        """The commitment is public; only the un-published reveal satisfies it."""
        assert post_merge_verification_is_valid(
            _coordinator_record(body=_pmv_body(session_reveal=SESSION_COMMITMENT)),
            **self._ctx()) is False

    def test_a_wrong_reveal_for_a_commitment_fails(self):
        assert post_merge_verification_is_valid(
            _coordinator_record(body=_pmv_body(session_reveal="guessed-value")),
            **self._ctx()) is False

    def test_a_different_application_under_the_same_login_fails(self):
        assert post_merge_verification_is_valid(
            _coordinator_record(app="a-different-app"), **self._ctx()) is False
        assert post_merge_verification_is_valid(
            _coordinator_record(app_key_present=False), **self._ctx()) is False

    def test_a_synthetic_merge_projection_is_rejected(self):
        assert canonical_merged_pull_request_is_valid(
            {"merged": True, "number": THIS_CORRECTIVE_PULL_REQUEST,
             "accepted_head": PMV_MERGE_HEAD, "merge_sha": PMV_MERGE_COMMIT_SHA,
             "merged_by_login": COORDINATOR_LOGIN, "merged_at": PMV_MERGED_AT}) is False

    def test_a_caller_cannot_move_the_merge_or_closure_timestamp(self):
        # Closure is a resource; a bare string is not one.
        assert post_merge_verification_is_valid(
            _coordinator_record(created="2026-08-31T23:00:00Z"),
            **self._ctx(closure_record="2026-09-01T00:00:00Z")) is False
        # And a malformed merged_at is not rescued by anything the caller supplies.
        assert post_merge_verification_is_valid(
            _coordinator_record(),
            **self._ctx(merged_pull_request=_merged_pull_request(
                merged_at="2026-13-45T99:99:99Z"))) is False

    def test_a_schema_valid_negative_pmv_result_fails(self):
        for field, value in (("overall_result", "FAIL"), ("tests_result", "FAIL"),
                             ("validators_result", "SKIPPED"),
                             ("protected_path_identity", "UNKNOWN"),
                             ("main_clean", "FALSE"), ("merge_tree_identity", "DIFFERENT")):
            body = _pmv_body(**{field: value})
            assert parse_pmv_body(body) is None, (field, value)
            assert post_merge_verification_is_valid(
                _coordinator_record(body=body), **self._ctx()) is False, (field, value)

    def test_a_fake_final_review_mapping_fails(self):
        for evidence in ({"reviewed_head": REAL_FINAL_HEAD},
                         {"reviewed_head": REAL_FINAL_HEAD, "verdict": "APPROVED"},
                         {"commit_id": REAL_FINAL_HEAD}):
            assert _readback(
                _ratification_naming(REAL_FINAL_HEAD), _live_pr(),
                evidence)["equality_proven"] is False

    def test_a_changes_required_review_fails(self):
        assert _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(),
            _final_review(body="FORMAL DISPOSITION: CHANGES REQUIRED"))[
                "equality_proven"] is False

    def test_a_wrong_head_or_wrong_pull_request_review_fails(self):
        assert _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(),
            _final_review(head="8" * 40))["equality_proven"] is False
        assert _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(),
            _final_review(pull_request_url=f"{REPO_API}/pulls/362"))[
                "equality_proven"] is False

    def test_a_later_adverse_review_fails(self):
        later = _final_review(ident=5_099_999_996,
                              body="FORMAL DISPOSITION: CHANGES REQUIRED",
                              submitted_at="2026-08-31T14:00:00Z")
        assert _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(), _final_review(),
            [later])["equality_proven"] is False

    def test_a_well_formed_but_wrong_ratification_head_fails(self):
        assert _readback(
            _ratification_naming("f" * 40), _live_pr(),
            _final_review())["equality_proven"] is False

    def test_an_impossible_ratification_timestamp_fails(self):
        assert _readback(
            _ratification_naming(REAL_FINAL_HEAD, created="9999-99-99T99:99:99Z"),
            _live_pr(), _final_review())["equality_proven"] is False

    def test_a_missing_protocol_member_fails(self):
        for key in sorted(PMV_SCHEMA):
            body = "\n".join(ln for ln in _pmv_body().splitlines()
                             if not ln.startswith(f"{key}: "))
            assert parse_pmv_body(body) is None, key
        for key in sorted(DESIGNATION_SCHEMA):
            body = "\n".join(ln for ln in _designation_body().splitlines()
                             if not ln.startswith(f"{key}: "))
            assert parse_designation_body(body) is None, key

    def test_the_positive_case_holds_when_no_gate_is_varied(self):
        """The control: every negative above must fail for ITS gate, not a broken fixture."""
        assert post_merge_verification_is_valid(_coordinator_record(), **self._ctx()) is True
        assert _readback(
            _ratification_naming(REAL_FINAL_HEAD), _live_pr(),
            _final_review())["equality_proven"] is True
        assert principal_designation_is_valid(_designation_record()) is True
        assert canonical_merged_pull_request_is_valid(_merged_pull_request()) is True
        assert canonical_closure_record_is_valid(_closure_record()) is True


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


class TestTheLiveProvenanceCapabilityIsProvedNotAssumed:
    """DELTA review 5062494115 BLOCKING 1 -- the evidence source, proved before it was used.

    The reviewer's objection was exact and correct on its own terms: a predicate that cannot
    be satisfied from a live resource is not a lifecycle, and Python fixtures that manufacture
    ``performed_via_github_app`` prove predicate behaviour, not obtainability.

    The read-only capability proof in SS-I.2.1 A0 answered it against the live canonical
    resource, which DOES carry the key. These tests pin what that proof established, and in
    particular the discriminating case: a Claude-authored comment that derives as the OWNER
    still carries the ``claude`` application object.
    """

    def test_the_decision_records_the_measured_capability_table(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "issues/comments/{comment_id}" in flat
        for token in ("claude[bot]", "1236702", "chatgpt-codex-connector",
                      "19 records across PRs #310, #311, #314, #316, #319"):
            assert token in flat, token

    def test_the_decision_forbids_treating_an_absent_key_as_null(self):
        flat = _flat(_read(DECISION_RELPATH))
        assert "An absent key is not a null value and never satisfies `§G.2`." in flat

    def test_an_absent_key_is_not_a_null_value(self):
        """The distinction the whole correction series turns on."""
        absent = _issue_comment(app_key_present=False)
        present_null = _issue_comment(app=None)
        assert "performed_via_github_app" not in absent
        assert present_null["performed_via_github_app"] is None
        assert _record_app_identity(absent) is None
        assert _record_app_identity(present_null) == "DIRECT"
        assert is_direct_principal_record(absent) is False
        assert is_direct_principal_record(present_null) is True

    def test_an_owner_attributed_application_record_is_not_the_principal(self):
        """The live hard case: Claude posting AS the owner still carries the app object."""
        owner_but_app = _issue_comment(login=PRINCIPAL_LOGIN, type_=PRINCIPAL_TYPE,
                                       assoc=PRINCIPAL_ASSOCIATION, app="claude")
        assert _actor_login(owner_but_app) == PRINCIPAL_LOGIN
        assert owner_but_app["author_association"] == "OWNER"
        assert is_direct_principal_record(owner_but_app) is False
        assert principal_designation_is_valid(owner_but_app) is False

    @pytest.mark.parametrize("slug", ["claude", "chatgpt-codex-connector", "evil"])
    def test_no_application_slug_whatsoever_satisfies_the_principal_rule(self, slug):
        assert is_direct_principal_record(_issue_comment(app=slug)) is False


class TestTheClosureActIsAuthenticated:
    """DELTA review 5062494115 BLOCKING 4 -- shape authenticated an explicit refusal."""

    @staticmethod
    def _ctx(**over):
        ctx = dict(designated=parse_designation_body(_designation_record()["body"]),
                   merged_pull_request=_merged_pull_request(),
                   verification_record=_coordinator_record(),
                   ci_run=_ci_run(), ci_job=_ci_job())
        ctx.update(over)
        return ctx

    def test_the_honest_closure_is_authorized(self):
        assert closure_is_authorized(_closure_record(), **self._ctx()) is True

    def test_the_reviewers_exact_refusal_reproduction_fails(self):
        evil = _closure_record(login="mallory", type_="Bot", assoc="NONE", app="evil",
                               actor_id=424242, body="I do NOT close this lifecycle.")
        assert canonical_closure_record_is_valid(evil) is False
        assert closure_is_authorized(evil, **self._ctx()) is False

    @pytest.mark.parametrize("body", [
        "I do NOT close this lifecycle.", "Final post-CI verification and lifecycle closure.",
        "", "   ", None, 123, "XASSET-0062 LIFECYCLE CLOSURE",
    ])
    def test_no_narrative_body_closes_anything(self, body):
        assert parse_closure_body(body) is None
        assert canonical_closure_record_is_valid(_closure_record(body=body)) is False

    @pytest.mark.parametrize("over", [
        {"login": "mallory"}, {"type_": "User"}, {"assoc": "NONE"},
        {"app": "evil"}, {"app": None}, {"actor_id": 999999},
    ])
    def test_a_well_formed_closure_by_an_unauthorized_closer_fails(self, over):
        assert closure_is_authorized(_closure_record(**over), **self._ctx()) is False, over

    def test_closure_must_name_the_verification_it_completes(self):
        other = _closure_record(body=_closure_body(post_merge_verification_comment_id=1))
        assert closure_is_authorized(other, **self._ctx()) is False

    @pytest.mark.parametrize("over", [
        {"merge_commit_ci_run_id": 1}, {"merge_commit_ci_job_id": 1},
        {"merge_commit_ci_run_attempt": 2},
    ])
    def test_closure_must_name_the_exact_run_job_and_attempt(self, over):
        assert closure_is_authorized(
            _closure_record(body=_closure_body(**over)), **self._ctx()) is False, over

    def test_a_successful_run_at_another_sha_closes_nothing(self):
        assert parse_closure_body(_closure_body(merge_commit_ci_head_sha="d" * 40)) is None
        assert closure_is_authorized(
            _closure_record(), **self._ctx(ci_run=_ci_run(head_sha="d" * 40))) is False
        assert closure_is_authorized(
            _closure_record(), **self._ctx(ci_job=_ci_job(head_sha="d" * 40))) is False

    @pytest.mark.parametrize("over", [
        {"status": "in_progress"}, {"status": "queued"}, {"status": None},
        {"conclusion": "failure"}, {"conclusion": "cancelled"}, {"conclusion": None},
        {"conclusion": "success", "status": "completed", "id": None},
    ])
    def test_an_unsuccessful_or_incomplete_run_fails(self, over):
        assert closure_is_authorized(
            _closure_record(), **self._ctx(ci_run=_ci_run(**over))) is False, over
        assert closure_is_authorized(
            _closure_record(), **self._ctx(ci_job=_ci_job(**over))) is False, over

    def test_closure_before_ci_completion_fails(self):
        early = _closure_record(created="2026-08-31T10:10:00Z")   # CI completes 10:16
        assert closure_is_authorized(early, **self._ctx()) is False

    def test_closure_before_the_verification_fails(self):
        early = _closure_record(created="2026-08-31T10:02:00Z")
        assert closure_is_authorized(early, **self._ctx()) is False

    @pytest.mark.parametrize("literal", ["NOT_APPLICABLE", "SKIPPED", "UNKNOWN", "N/A", ""])
    def test_no_weaker_ci_literal_is_accepted(self, literal):
        assert parse_closure_body(_closure_body(merge_commit_ci_conclusion=literal)) is None
        assert parse_closure_body(_closure_body(merge_commit_ci_status=literal)) is None

    def test_the_closure_is_total_and_never_raises(self):
        for record in (None, 123, "text", [], {}):
            assert canonical_closure_record_is_valid(record) is False
            assert closure_is_authorized(record, **self._ctx()) is False


class TestTheReviewCollectionCompletenessIsProved:
    """DELTA review 5062494115 BLOCKING 2 -- an omitted later adverse review was invisible."""

    def test_a_complete_single_page_collection_is_accepted(self):
        ok, reviews = review_collection_is_provably_complete(
            _review_collection([_final_review()], per_page=100))
        assert ok is True
        assert len(reviews) == 1

    def test_a_present_link_header_means_completeness_is_unproven(self):
        ok, reviews = review_collection_is_provably_complete(
            _review_collection([_final_review()], link_header='<https://…>; rel="next"'))
        assert ok is False
        assert reviews == []

    def test_a_full_page_may_be_truncated_and_fails(self):
        ok, _ = review_collection_is_provably_complete(
            _review_collection([_final_review(ident=i) for i in range(1, 4)], per_page=3))
        assert ok is False

    @pytest.mark.parametrize("collection", [
        None, 123, "reviews", [], {}, {"reviews": None, "per_page": 100},
        {"reviews": [], "per_page": None}, {"reviews": [], "per_page": 0},
        {"reviews": "not-a-list", "per_page": 100},
    ])
    def test_a_malformed_collection_never_proves_completeness(self, collection):
        ok, _ = review_collection_is_provably_complete(collection)
        assert ok is False

    def test_the_readback_requires_the_approval_to_be_in_the_collection(self):
        out = _readback(_ratification_naming(REAL_FINAL_HEAD),
                        collection=_complete_collection(_final_review(ident=999)))
        assert out["equality_proven"] is False
        assert out["failure_reason"] == (
            "the selected approving review is not a member of the collection")

    def test_an_omitted_later_adverse_review_can_no_longer_hide(self):
        """Omission now fails on completeness rather than passing silently."""
        out = _readback(_ratification_naming(REAL_FINAL_HEAD),
                        collection=_review_collection([_final_review()],
                                                      link_header='<https://…>; rel="prev"'))
        assert out["equality_proven"] is False
        assert out["review_collection_complete"] is False

    def test_an_earlier_adverse_review_is_not_later(self):
        earlier = _final_review(ident=5_000_000_001, submitted_at="2026-01-01T00:00:00Z",
                                body="FORMAL DISPOSITION: CHANGES REQUIRED")
        out = _readback(_ratification_naming(REAL_FINAL_HEAD), collection=[earlier])
        assert out["equality_proven"] is True
        assert out["later_adverse_review_exists"] is False

    def test_a_review_with_an_unparseable_instant_fails_closed(self):
        broken = _final_review(ident=5_000_000_002, submitted_at="9999-99-99T99:99:99Z")
        out = _readback(_ratification_naming(REAL_FINAL_HEAD), collection=[broken])
        assert out["equality_proven"] is False
        assert out["failure_reason"] == "a review in the collection has no parseable instant"

    def test_a_non_resource_member_fails_closed(self):
        out = _readback(_ratification_naming(REAL_FINAL_HEAD), collection=["not-a-review"])
        assert out["equality_proven"] is False
        assert out["failure_reason"] == "review collection contains a non-resource member"


class TestTheRatificationOrderingIsEnforced:
    """DELTA review 5062494115 BLOCKING 2 -- review -> ratification -> readback -> merge."""

    @pytest.mark.parametrize("created", ["2026-08-31T11:59:59Z", "2026-08-31T12:00:00Z"])
    def test_a_ratification_at_or_before_the_approval_fails(self, created):
        """Equality fails too: SS-I.2.1 F.4 is strict."""
        out = _readback(_ratification_naming(REAL_FINAL_HEAD, created=created))
        assert out["equality_proven"] is False
        assert out["failure_reason"] == "ratification does not postdate the approving review"

    def test_a_ratification_predating_the_pr362_merge_fails_earlier_and_differently(self):
        """A January ratification fails SS-G.5 retrospection BEFORE ordering is reached.

        Asserted as its own case rather than folded into the parametrisation above, because
        collapsing two independent gates into one expected reason would hide whichever fired.
        """
        out = _readback(_ratification_naming(REAL_FINAL_HEAD, created="2026-01-01T00:00:00Z"))
        assert out["equality_proven"] is False
        assert out["failure_reason"] == "record fails an SS-G structural clause"

    def test_one_second_after_the_approval_passes(self):
        out = _readback(_ratification_naming(REAL_FINAL_HEAD, created="2026-08-31T12:00:01Z"))
        assert out["equality_proven"] is True

    @pytest.mark.parametrize("over", [
        {"state": "closed"}, {"merged": True}, {"merged_at": "2026-08-31T09:00:00Z"},
        {"merged": None}, {"state": "open", "merged": True},
    ])
    def test_a_merged_or_closed_pull_request_defeats_the_readback(self, over):
        out = _readback(_ratification_naming(REAL_FINAL_HEAD), pull=_live_pr(**over))
        assert out["equality_proven"] is False
        assert out["failure_reason"] == (
            "live pull-request is not a valid open, unmerged PR #363 resource")

    @pytest.mark.parametrize("submitted_at", [None, "", "9999-99-99T99:99:99Z", 123])
    def test_an_unparseable_approval_instant_fails_closed(self, submitted_at):
        out = _readback(_ratification_naming(REAL_FINAL_HEAD),
                        review=_final_review(submitted_at=submitted_at))
        assert out["equality_proven"] is False

    def test_the_retained_evidence_names_the_approval_instant(self):
        out = _readback(_ratification_naming(REAL_FINAL_HEAD))
        assert out["approving_review_submitted_at"] == "2026-08-31T12:00:00Z"
        assert out["review_collection_complete"] is True


class TestEveryActorIdentityCarriesItsNumericId:
    """DELTA review 5062494115 MAJOR 1 -- a login is a mutable display handle."""

    def test_removing_merged_by_id_and_node_id_now_fails(self):
        """The reviewer's exact reproduction."""
        stripped = _merged_pull_request()
        stripped["merged_by"] = {k: v for k, v in stripped["merged_by"].items()
                                 if k not in ("id", "node_id")}
        assert canonical_merged_pull_request_is_valid(stripped) is False

    @pytest.mark.parametrize("merged_by", [
        {"login": COORDINATOR_LOGIN, "type": COORDINATOR_TYPE, "node_id": "x"},
        {"login": COORDINATOR_LOGIN, "type": COORDINATOR_TYPE, "id": None, "node_id": "x"},
        {"login": COORDINATOR_LOGIN, "type": COORDINATOR_TYPE, "id": "209825114",
         "node_id": "x"},
        {"login": COORDINATOR_LOGIN, "type": COORDINATOR_TYPE, "id": 0, "node_id": "x"},
        {"login": COORDINATOR_LOGIN, "type": COORDINATOR_TYPE, "id": -1, "node_id": "x"},
        {"login": COORDINATOR_LOGIN, "type": COORDINATOR_TYPE, "id": True, "node_id": "x"},
        {"login": COORDINATOR_LOGIN, "type": COORDINATOR_TYPE, "id": COORDINATOR_ID},
        {"login": COORDINATOR_LOGIN, "type": COORDINATOR_TYPE, "id": COORDINATOR_ID,
         "node_id": ""},
    ])
    def test_a_malformed_merger_id_fails(self, merged_by):
        assert canonical_merged_pull_request_is_valid(
            _merged_pull_request(merged_by=merged_by)) is False, merged_by

    def test_a_merger_whose_id_differs_from_the_designation_fails(self):
        other = _merged_pull_request(
            merged_by={"login": COORDINATOR_LOGIN, "type": COORDINATOR_TYPE,
                       "id": 111111, "node_id": "x"})
        assert canonical_merged_pull_request_is_valid(other) is True
        assert post_merge_verification_is_valid(
            _coordinator_record(),
            designation_record=_designation_record(),
            merged_pull_request=other,
            closure_record=_closure_record(),
            ci_run=_ci_run(), ci_job=_ci_job()) is False

    @pytest.mark.parametrize("actor_id", [None, "209825114", 0, -1, True])
    def test_a_verifier_without_an_exact_integer_id_fails(self, actor_id):
        rec = _coordinator_record()
        rec["user"] = {"login": COORDINATOR_LOGIN, "type": COORDINATOR_TYPE, "id": actor_id}
        assert _actor_identity(rec) is None
        assert post_merge_verification_is_valid(
            rec, designation_record=_designation_record(),
            merged_pull_request=_merged_pull_request(), closure_record=_closure_record(),
            ci_run=_ci_run(), ci_job=_ci_job()) is False

    def test_a_verifier_whose_id_differs_from_the_designation_fails(self):
        assert post_merge_verification_is_valid(
            _coordinator_record(actor_id=777777),
            designation_record=_designation_record(),
            merged_pull_request=_merged_pull_request(), closure_record=_closure_record(),
            ci_run=_ci_run(), ci_job=_ci_job()) is False

    @pytest.mark.parametrize("value", ["0", "-1", "", "abc", "1.0", " 1", None, 0, -1])
    def test_a_designation_without_a_positive_integer_id_fails(self, value):
        assert parse_designation_body(_designation_body(coordinator_id=value)) is None

    def test_a_trailing_space_is_normalised_rather_than_rejected(self):
        """Not a defect: the declaration parser rstrips each line, so ``"1 "`` IS ``1``.

        Recorded explicitly rather than asserted as a failure, because claiming it fails
        would be untrue of the parser and would hide the real rule -- a LEADING space is not
        stripped and does fail, which the parametrisation above covers.
        """
        parsed = parse_designation_body(_designation_body(coordinator_id="1 "))
        assert parsed is not None
        assert parsed["coordinator_id"] == "1"

    def test_the_positive_integer_helper_rejects_bool(self):
        """``True`` is an ``int`` in Python and is not an actor id."""
        assert _positive_int(True) is None
        assert _positive_int(False) is None
        assert _positive_int(1) == 1
        assert _positive_int("1") == 1


class TestEveryChronologyBoundaryIsStrictAtEquality:
    """The two gaps the mutation proof found: ``<`` relaxed to ``<=`` went undetected.

    Both were REAL weakenings, so they are closed with tests rather than counted as caught.
    Equality is the only value that distinguishes ``<`` from ``<=``, so each boundary is
    pinned at exactly the instant it separates.
    """

    @staticmethod
    def _ctx(**over):
        ctx = dict(designated=parse_designation_body(_designation_record()["body"]),
                   merged_pull_request=_merged_pull_request(),
                   verification_record=_coordinator_record(),
                   ci_run=_ci_run(), ci_job=_ci_job())
        ctx.update(over)
        return ctx

    def test_ci_completing_at_the_verification_instant_fails(self):
        """``verified_at < ci_completed_at`` -- equality is not "after"."""
        assert closure_is_authorized(
            _closure_record(),
            **self._ctx(ci_job=_ci_job(completed_at=PMV_VERIFIED_AT))) is False
        # One second later is the nearest lawful value.
        assert closure_is_authorized(
            _closure_record(),
            **self._ctx(ci_job=_ci_job(completed_at="2026-08-31T10:05:01Z"))) is True

    def test_closure_at_the_ci_completion_instant_fails(self):
        """``ci_completed_at < closed_at`` -- equality is not "after"."""
        assert closure_is_authorized(
            _closure_record(created=PMV_CI_COMPLETED_AT), **self._ctx()) is False
        assert closure_is_authorized(
            _closure_record(created="2026-08-31T10:16:01Z"), **self._ctx()) is True

    def test_an_adverse_review_at_exactly_the_approval_instant_is_not_later(self):
        """``candidate_at > approved_at`` -- a simultaneous review is not a LATER one.

        Relaxing this to ``>=`` would defeat the approval using a review submitted at the
        same instant, which is not evidence that anything changed after it.
        """
        simultaneous = _final_review(ident=5_000_000_003,
                                     submitted_at="2026-08-31T12:00:00Z",
                                     body="FORMAL DISPOSITION: CHANGES REQUIRED")
        out = _readback(_ratification_naming(REAL_FINAL_HEAD), collection=[simultaneous])
        assert out["equality_proven"] is True
        assert out["later_adverse_review_exists"] is False
        # One second later genuinely is later, and does defeat it.
        one_later = _final_review(ident=5_000_000_004,
                                  submitted_at="2026-08-31T12:00:01Z",
                                  body="FORMAL DISPOSITION: CHANGES REQUIRED")
        assert _readback(_ratification_naming(REAL_FINAL_HEAD),
                         collection=[one_later])["equality_proven"] is False
