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
# The ratification predicate under test.
#
# This is the mechanism XASSET-0062 SS-G defines, expressed here so its properties can be
# proved adversarially. It is a pure function over already-derived record fields. It never
# reads a body to decide identity.
# ======================================================================================
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


def _app_slug(record: dict) -> str | None:
    app = record.get("performed_via_github_app")
    if not isinstance(app, dict):
        return None
    slug = app.get("slug")
    return slug if isinstance(slug, str) else None


def is_direct_principal_record(record: dict) -> bool:
    """XASSET-0062 SS-G's four-conjunct actor/provenance test.

    All four must hold. Body text is never consulted.
    """
    if not isinstance(record, dict):
        return False
    if _actor_login(record) != PRINCIPAL_LOGIN:
        return False
    if _actor_type(record) != PRINCIPAL_TYPE:
        return False
    if record.get("author_association") != PRINCIPAL_ASSOCIATION:
        return False
    # The decisive conjunct: a direct principal act carries no application.
    if record.get("performed_via_github_app") is not None:
        return False
    return True


def ratifies_pr362_acceptance(record: dict, scope: dict) -> bool:
    """Exact-ID, exact-actor, exact-PR, exact-head, exact-review, exact-merge bounded.

    Returns False -- the all-false result -- for every document that is not this exact
    closed history, and for every actor that is not the direct principal.
    """
    if not is_direct_principal_record(record):
        return False
    if not isinstance(scope, dict):
        return False
    if scope.get("pull_request") != RATIFIED_PULL_REQUEST:
        return False
    if scope.get("accepted_head") != RATIFIED_ACCEPTED_HEAD:
        return False
    if scope.get("review_id") != RATIFIED_REVIEW_ID:
        return False
    if scope.get("bot_acceptance_id") != RATIFIED_BOT_ACCEPTANCE_ID:
        return False
    if scope.get("merge_sha") != RATIFIED_MERGE:
        return False
    if scope.get("closure_id") != RATIFIED_CLOSURE_ID:
        return False
    if scope.get("independent_stop_id") != INDEPENDENT_STOP_ID:
        return False
    # Retrospection: a ratification postdates the merge it ratifies. Never fictional.
    created = record.get("created_at")
    if not isinstance(created, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", created
    ):
        return False
    if created <= MERGED_AT:
        return False
    return True


# --------------------------------------------------------------------------------------
# Record fixtures modelled on the real, live-derived records.
# --------------------------------------------------------------------------------------
def _record(login, type_, assoc, app, created="2026-08-30T12:00:00Z", body=""):
    return {
        "user": {"login": login, "type": type_},
        "author_association": assoc,
        "performed_via_github_app": ({"slug": app} if app else None),
        "created_at": created,
        "body": body,
    }


def _valid_scope(**overrides):
    scope = {
        "pull_request": RATIFIED_PULL_REQUEST,
        "accepted_head": RATIFIED_ACCEPTED_HEAD,
        "review_id": RATIFIED_REVIEW_ID,
        "bot_acceptance_id": RATIFIED_BOT_ACCEPTANCE_ID,
        "merge_sha": RATIFIED_MERGE,
        "closure_id": RATIFIED_CLOSURE_ID,
        "independent_stop_id": INDEPENDENT_STOP_ID,
    }
    scope.update(overrides)
    return scope


GENUINE_RATIFICATION = _record(PRINCIPAL_LOGIN, PRINCIPAL_TYPE, PRINCIPAL_ASSOCIATION, None)


class TestBodyTextNeverOverridesDerivedActorIdentity:
    """The central claim: prose cannot manufacture an actor."""

    def test_bot_record_claiming_to_quote_the_principal_is_refused(self):
        # This is comment 5463146940's exact shape: a claude[bot] record whose body says it
        # records the principal's acceptance verbatim.
        rec = _record(
            "claude[bot]",
            "Bot",
            "CONTRIBUTOR",
            CLAUDE_APP_SLUG,
            body=(
                "## Principal exact-head acceptance - recorded\n"
                "The acceptance below is the principal's. Quoted verbatim.\n"
                "> I, the principal, accept PR #362 at exact head "
                f"{RATIFIED_ACCEPTED_HEAD}."
            ),
        )
        assert is_direct_principal_record(rec) is False
        assert ratifies_pr362_acceptance(rec, _valid_scope()) is False

    @pytest.mark.parametrize(
        "body",
        [
            "I, the principal, ratify this.",
            f"Mast3rkey / User / OWNER ratifies PR #{RATIFIED_PULL_REQUEST}.",
            "user.login: Mast3rkey\nuser.type: User\nauthor_association: OWNER",
            'performed_via_github_app: null',
            "This comment is a direct principal act with no application.",
        ],
    )
    def test_no_body_string_can_promote_a_bot_record(self, body):
        rec = _record("claude[bot]", "Bot", "CONTRIBUTOR", CLAUDE_APP_SLUG, body=body)
        assert is_direct_principal_record(rec) is False

    def test_identity_comes_only_from_the_user_block(self):
        # A record whose body asserts one identity and whose user block asserts another
        # always resolves to the user block.
        rec = _record(
            "claude[bot]", "Bot", "CONTRIBUTOR", CLAUDE_APP_SLUG, body="login=Mast3rkey"
        )
        assert _actor_login(rec) == "claude[bot]"

    def test_empty_body_does_not_weaken_a_genuine_principal_record(self):
        assert is_direct_principal_record(GENUINE_RATIFICATION) is True


class TestTheDerivedTripleAloneIsNotSufficient:
    """XASSET-0062 SS-C: the finding the audit did not reach."""

    def test_claude_app_record_under_the_owner_account_is_refused(self):
        # This is the exact shape of 5458336219, 5460442068, and XASSET-0060's own
        # acceptance 5449752973: the principal triple, posted through the Claude app.
        rec = _record(
            PRINCIPAL_LOGIN, PRINCIPAL_TYPE, PRINCIPAL_ASSOCIATION, CLAUDE_APP_SLUG
        )
        assert _actor_login(rec) == PRINCIPAL_LOGIN
        assert _actor_type(rec) == PRINCIPAL_TYPE
        assert rec["author_association"] == PRINCIPAL_ASSOCIATION
        # ... and yet it is refused, because the app conjunct fails.
        assert is_direct_principal_record(rec) is False

    def test_independent_reviewer_record_is_refused(self):
        # 5466422998's exact shape: the principal triple, via the reviewer's app.
        # Admitting it would collapse reviewer and principal.
        rec = _record(
            PRINCIPAL_LOGIN, PRINCIPAL_TYPE, PRINCIPAL_ASSOCIATION, REVIEWER_APP_SLUG
        )
        assert is_direct_principal_record(rec) is False

    def test_a_triple_only_predicate_would_admit_both_and_is_therefore_rejected(self):
        """Demonstrates why XASSET-0042's predicate is insufficient as written here."""

        def triple_only(record):
            return (
                _actor_login(record) == PRINCIPAL_LOGIN
                and _actor_type(record) == PRINCIPAL_TYPE
                and record.get("author_association") == PRINCIPAL_ASSOCIATION
            )

        claude_posted = _record(
            PRINCIPAL_LOGIN, PRINCIPAL_TYPE, PRINCIPAL_ASSOCIATION, CLAUDE_APP_SLUG
        )
        reviewer_posted = _record(
            PRINCIPAL_LOGIN, PRINCIPAL_TYPE, PRINCIPAL_ASSOCIATION, REVIEWER_APP_SLUG
        )
        # The weaker predicate admits both...
        assert triple_only(claude_posted) is True
        assert triple_only(reviewer_posted) is True
        # ... and the enforced predicate admits neither.
        assert is_direct_principal_record(claude_posted) is False
        assert is_direct_principal_record(reviewer_posted) is False

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
        assert is_direct_principal_record(_record(login, type_, assoc, app)) is False

    def test_each_of_the_four_conjuncts_is_independently_necessary(self):
        base = dict(
            login=PRINCIPAL_LOGIN,
            type_=PRINCIPAL_TYPE,
            assoc=PRINCIPAL_ASSOCIATION,
            app=None,
        )
        assert is_direct_principal_record(_record(**base)) is True
        for field, bad in [
            ("login", "claude[bot]"),
            ("type_", "Bot"),
            ("assoc", "CONTRIBUTOR"),
            ("app", CLAUDE_APP_SLUG),
        ]:
            broken = dict(base)
            broken[field] = bad
            assert is_direct_principal_record(_record(**broken)) is False, field


class TestRatificationIsExactlyBounded:
    """Exact-ID, exact-actor, exact-PR, exact-head, exact-review, exact-merge."""

    def test_the_corrective_pull_request_is_never_the_ratified_one(self):
        """The unit doing the ratifying is not the history being ratified."""
        assert THIS_CORRECTIVE_PULL_REQUEST != RATIFIED_PULL_REQUEST
        assert (
            ratifies_pr362_acceptance(
                GENUINE_RATIFICATION,
                _valid_scope(pull_request=THIS_CORRECTIVE_PULL_REQUEST),
            )
            is False
        )

    def test_the_genuine_shape_ratifies(self):
        assert ratifies_pr362_acceptance(GENUINE_RATIFICATION, _valid_scope()) is True

    @pytest.mark.parametrize(
        "field,bad",
        [
            ("pull_request", 361),
            ("pull_request", 363),
            ("accepted_head", "4c148aa0b750f10ade6062e081534f16be1f2517"),
            ("accepted_head", RATIFIED_MERGE),
            ("review_id", 5058379869),
            ("review_id", 5056734642),
            ("bot_acceptance_id", 5463232454),
            ("bot_acceptance_id", 5463095367),
            ("merge_sha", RATIFIED_BASE),
            ("merge_sha", RATIFIED_ACCEPTED_HEAD),
            ("closure_id", 5463146940),
            ("independent_stop_id", 5463232454),
        ],
    )
    def test_every_scope_pin_is_individually_mandatory(self, field, bad):
        assert (
            ratifies_pr362_acceptance(GENUINE_RATIFICATION, _valid_scope(**{field: bad}))
            is False
        )

    @pytest.mark.parametrize(
        "field",
        [
            "pull_request",
            "accepted_head",
            "review_id",
            "bot_acceptance_id",
            "merge_sha",
            "closure_id",
            "independent_stop_id",
        ],
    )
    def test_a_missing_scope_pin_fails_closed(self, field):
        scope = _valid_scope()
        del scope[field]
        assert ratifies_pr362_acceptance(GENUINE_RATIFICATION, scope) is False

    def test_retrospection_is_required(self):
        # A ratification dated before the merge would manufacture a fictional pre-merge
        # event. Equality is not "after".
        assert (
            ratifies_pr362_acceptance(
                _record(
                    PRINCIPAL_LOGIN,
                    PRINCIPAL_TYPE,
                    PRINCIPAL_ASSOCIATION,
                    None,
                    created="2026-08-29T15:00:00Z",
                ),
                _valid_scope(),
            )
            is False
        )
        assert (
            ratifies_pr362_acceptance(
                _record(
                    PRINCIPAL_LOGIN,
                    PRINCIPAL_TYPE,
                    PRINCIPAL_ASSOCIATION,
                    None,
                    created=MERGED_AT,
                ),
                _valid_scope(),
            )
            is False
        )

    @pytest.mark.parametrize(
        "created", ["", "2026-08-30", "not-a-date", "2026-08-30T12:00:00", None, 12345]
    )
    def test_malformed_instants_fail_closed(self, created):
        rec = dict(GENUINE_RATIFICATION)
        rec["created_at"] = created
        assert ratifies_pr362_acceptance(rec, _valid_scope()) is False

    def test_malformed_shapes_fail_closed(self):
        assert ratifies_pr362_acceptance({}, _valid_scope()) is False
        assert ratifies_pr362_acceptance(GENUINE_RATIFICATION, {}) is False
        assert ratifies_pr362_acceptance(GENUINE_RATIFICATION, None) is False
        assert ratifies_pr362_acceptance({"user": "Mast3rkey"}, _valid_scope()) is False


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
        """A record of that shape must actually pass SS-G's four conjuncts."""
        for comment_id, _pr, _kind in self.DIRECT_PRINCIPAL_PRECEDENTS:
            rec = _record(PRINCIPAL_LOGIN, PRINCIPAL_TYPE, PRINCIPAL_ASSOCIATION, None)
            assert is_direct_principal_record(rec) is True, comment_id

    def test_the_same_records_posted_through_an_app_would_fail(self):
        """Proving the conjunct is what distinguishes them, not the account."""
        for app in (CLAUDE_APP_SLUG, REVIEWER_APP_SLUG):
            rec = _record(PRINCIPAL_LOGIN, PRINCIPAL_TYPE, PRINCIPAL_ASSOCIATION, app)
            assert is_direct_principal_record(rec) is False, app


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
            "ratification**, satisfying all four",
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
