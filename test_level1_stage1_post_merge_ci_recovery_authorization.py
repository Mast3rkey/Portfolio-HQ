"""Adversarial tests pinning the ``XASSET-0045`` post-merge-CI recovery authorization.

``XASSET-0044`` merged with a drift-free tree, a clean final review, principal acceptance, and
post-merge verification -- and then its **merge-commit CI failed**. ``XASSET-0044`` §L makes seven
conditions conjunctively necessary; its sixth requires *successful merge-commit CI whose ``head_sha``
is the exact merge SHA*. That run failed, the seventh condition (final post-CI lifecycle closure)
correctly never happened, and ``XASSET-0044`` is therefore **not effective**.

The danger this suite exists to prevent is not the recovery. It is the set of shortcuts a later
session could read into a filing that sits one merged-but-ineffective rebinding away from an armable
Stage 1:

1. **A later green CI run treated as repairing the failed run.** ``TestFailedRunIsImmutable`` --
   §L.6's own words exclude runs against any other commit, and the failed commit is immutable.
2. **The comparison anchor left moving.** ``TestClosedRangeIsExactAndImmutable`` -- the authorized
   correction must use the closed range, never ``merge-base(HEAD, origin/main)``.
3. **The defect mislabelled as merge drift or outcome-surface drift.** ``TestDefectIsAMovingAnchor``
   -- proven from the git object store, not asserted.
4. **More than one future unit authorized, or the recovery folded into this filing.**
   ``TestExactlyOneFutureUnit`` and ``TestFilingIsDesignOnly``.
5. **``XASSET-0043`` reused, or ``XASSET-0044`` treated as effective.**
   ``TestPredecessorAuthorityIsSpent``.
6. **The successor lifecycle anchor requirement dropped.** ``TestSuccessorLifecycleAnchorRequired``.
7. **The original adverse history relabelled, ignored, or quietly dropped.**
   ``TestAdverseHistoryPreserved``.
8. **Activation authority acquired by implication.** ``TestZeroActivationAuthority``.
9. **Fail-closed softened into a judgement call.** ``TestFailClosed``.
10. **The register or catalog desynchronised, or a section left vacuous.**
    ``TestCatalogAndRegisterSynchronisation`` and ``TestNoSectionIsVacuous``.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No attestation, claim, completion, lane directory, or ledger entry is created or read
for authorization purposes. No ``risk_lane_boundary`` protected result path is read, listed, opened,
or referenced. No module capable of producing a Stage-1 outcome is imported.
"""

from __future__ import annotations

import ast
import re
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent

DECISION_ID = "XASSET-0045"
DECISION_PATH = ROOT / (
    "governance/decisions/"
    "XASSET-0045-endpoint-0001-stage-1-post-merge-ci-recovery-authorization.md"
)
CATALOG_PATH = ROOT / "governance/decisions.yaml"
REGISTER_PATH = ROOT / "operations/WORKSTREAMS.yaml"
SUITE_PATH = Path(__file__).resolve()
REGISTER_GATE = "xasset0045-post-merge-ci-recovery-authorization"

# ── The immutable facts this authorization is built on ──────────────────────────────────────
#
# Every one of these was independently re-derived from live git and live GitHub during the
# filing session and is asserted here against the real object store, never taken on trust.

#: PR #344's base -- the ``XASSET-0043`` merge.
PR344_BASE_SHA = "0709d2f05ab031ecb6f69c40465ed4a227983aed"
#: PR #344's accepted head -- the exact commit review 4989080551 examined.
PR344_ACCEPTED_HEAD = "9c2821ab9e0e0dff09f5a03da5a6034775b00750"
#: PR #344's merge commit -- and the ``head_sha`` of the FAILED merge-commit CI run.
PR344_MERGE_SHA = "f5dedce1d1d3116ed8a6845c4447388c85a5414c"
#: The tree carried by BOTH the accepted head and the merge -- zero merge drift.
PR344_MERGE_TREE = "bd9ce6694261a7b4fb664a5121d04571f9606924"

#: The FAILED merge-commit CI run and job at ``PR344_MERGE_SHA``. Immutable adverse history.
FAILED_CI_RUN = "32439614683"
FAILED_CI_JOB = "96647501864"

#: The lifecycle evidence that DID complete, preserved as authenticated predecessor evidence.
FINAL_CLEAN_REVIEW = "4989080551"
PRINCIPAL_ACCEPTANCE_COMMENT = "5364401900"
POST_MERGE_VERIFICATION_COMMENT = "5364422640"
AUDITABLE_STOP_COMMENT = "5364490220"

#: The guard whose moving anchor caused the failure, and its exact failing assertion line.
FAILING_GUARD_FILE = "test_overlap_model_validator.py"
FAILING_GUARD_LINE = 1119
FAILING_GUARD_TEST = "test_real_repository_governance_decisions_pass_the_repaired_check"

#: The one-use authorized ``XASSET-0042`` decision transition, by object identity.
AUTHORIZED_DECISION_RELPATH = (
    "governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md"
)
AUTHORIZED_OLD_BLOB = "e4cda7a5042da68f347598a62d9e6d5cfc40ae55"
AUTHORIZED_NEW_BLOB = "b08a625a5adb840e9576e5cd9218be24e63bd57e"

#: Universe identity -- must be untouched by a design-only filing.
UNIVERSE_CONSTRUCTIONS = 680
UNIVERSE_CELLS = 48
UNIVERSE_AGGREGATE_HASH = (
    "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
)

#: Paths a design-only filing must not touch.
PROTECTED_RELPATHS = (
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    "level1_construction_universe_closure_validator.py",
    "level1_stage1_execution_authorization.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "test_overlap_model_validator.py",
    "allocate.py",
    "margin_state.py",
    "levels.py",
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
)


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def _git_ok(*args: str) -> bool:
    return (
        subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).returncode
        == 0
    )


def _flat(text: str) -> str:
    """Collapse all runs of whitespace to single spaces.

    The decision is hard-wrapped prose, so an exact phrase can straddle a newline. Matching
    against the flattened text keeps every assertion an EXACT phrase match while making it
    insensitive to where the paragraph happens to wrap. This is deliberately not a
    weakening: the full phrase must still be present, in order, verbatim.
    """
    return " ".join(text.split())


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_flat() -> str:
    return _flat(DECISION_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def decision_flat_lower() -> str:
    return _flat(DECISION_PATH.read_text(encoding="utf-8")).lower()


@pytest.fixture(scope="module")
def register():
    return yaml.safe_load(REGISTER_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ws0014(register):
    return next(w for w in register["workstreams"] if w.get("id") == "WS-0014")


@pytest.fixture(scope="module")
def gate(ws0014):
    matches = [g for g in ws0014["milestones"] if g.get("gate") == REGISTER_GATE]
    assert len(matches) == 1, f"expected exactly one {REGISTER_GATE} gate, found {len(matches)}"
    return matches[0]


@pytest.fixture(scope="module")
def catalog_entry():
    catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))["decisions"]
    matches = [d for d in catalog if d.get("decision_id") == DECISION_ID]
    assert len(matches) == 1, f"expected exactly one {DECISION_ID} catalog entry"
    return matches[0]


# ======================================================================================
# 1 -- The defect is a MOVING TEST ANCHOR, proven, not asserted
# ======================================================================================


class TestDefectIsAMovingAnchor:
    def test_the_failing_guard_and_line_exist_and_are_the_named_assertion(self):
        """The named file/line must really carry the named assertion. A stale line number
        would let this whole authorization describe something that no longer exists."""
        source = (ROOT / FAILING_GUARD_FILE).read_text(encoding="utf-8").splitlines()
        line = source[FAILING_GUARD_LINE - 1]
        assert "assert modified ==" in line, line
        assert "AUTHORIZED_DECISION_MODIFICATIONS" in line, line

    def test_the_guard_resolves_its_base_through_a_moving_merge_base(self):
        """The defect's mechanism: the base is a function of HEAD and origin/main, so it
        moves. Proven from the guard's own source, not from prose."""
        source = (ROOT / FAILING_GUARD_FILE).read_text(encoding="utf-8")
        tree = ast.parse(source)
        resolver = next(
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "_resolve_pr_base_sha"
        )
        body = ast.get_source_segment(source, resolver) or ""
        assert "merge-base" in body
        assert '"HEAD"' in body
        assert '"origin/main"' in body

    def test_on_merged_main_the_moving_base_collapses_to_head_itself(self):
        """On merged ``main`` the merge-base of HEAD and origin/main IS the merge commit, so
        the comparison is empty. This is the whole failure, reproduced from real git."""
        if not _git_ok("rev-parse", "--verify", "origin/main"):
            pytest.skip("origin/main not resolvable in this environment")
        if not _git_ok("cat-file", "-e", f"{PR344_MERGE_SHA}^{{commit}}"):
            pytest.skip("PR #344's merge commit is not present in this checkout")
        base = _git("merge-base", PR344_MERGE_SHA, PR344_MERGE_SHA)
        assert base == PR344_MERGE_SHA
        diff = _git("diff", "--name-status", base, PR344_MERGE_SHA, "--", "governance/decisions")
        assert diff == "", f"expected an empty comparison, got: {diff!r}"

    def test_the_closed_range_does_exercise_the_authorized_transition(self):
        """The property the guard exists to enforce is TRUE over the closed range. Only the
        anchor is wrong -- so the correction must re-anchor, never delete."""
        for sha in (PR344_BASE_SHA, PR344_ACCEPTED_HEAD):
            if not _git_ok("cat-file", "-e", f"{sha}^{{commit}}"):
                pytest.skip("PR #344's closed range is not present in this checkout")
        diff = _git(
            "diff", "--name-status", PR344_BASE_SHA, PR344_ACCEPTED_HEAD, "--", "governance/decisions"
        )
        rows = [line.split("\t") for line in diff.splitlines() if line.strip()]
        modified = [rest for status, rest in rows if status.startswith("M")]
        assert modified == [AUTHORIZED_DECISION_RELPATH], modified

    def test_the_authorized_transition_matches_its_bound_blob_identities(self):
        """Path equality is not identity. Both blob ends must match exactly."""
        for sha in (PR344_BASE_SHA, PR344_ACCEPTED_HEAD):
            if not _git_ok("cat-file", "-e", f"{sha}^{{commit}}"):
                pytest.skip("PR #344's closed range is not present in this checkout")
        assert _git("rev-parse", f"{PR344_BASE_SHA}:{AUTHORIZED_DECISION_RELPATH}") == (
            AUTHORIZED_OLD_BLOB
        )
        assert _git("rev-parse", f"{PR344_ACCEPTED_HEAD}:{AUTHORIZED_DECISION_RELPATH}") == (
            AUTHORIZED_NEW_BLOB
        )

    def test_the_decision_names_the_defect_as_a_moving_anchor_not_drift(self, decision_flat_lower):
        assert "moving test anchor" in decision_flat_lower
        assert "neither merge drift nor outcome-surface drift" in decision_flat_lower

    def test_merge_drift_is_affirmatively_excluded_from_the_object_store(self):
        """Not merge drift -- proven. The merge tree equals the accepted-head tree."""
        for sha in (PR344_MERGE_SHA, PR344_ACCEPTED_HEAD):
            if not _git_ok("cat-file", "-e", f"{sha}^{{commit}}"):
                pytest.skip("PR #344's commits are not present in this checkout")
        assert _git("rev-parse", f"{PR344_MERGE_SHA}^{{tree}}") == PR344_MERGE_TREE
        assert _git("rev-parse", f"{PR344_ACCEPTED_HEAD}^{{tree}}") == PR344_MERGE_TREE

    def test_the_accepted_head_is_the_second_parent_of_the_merge(self):
        if not _git_ok("cat-file", "-e", f"{PR344_MERGE_SHA}^{{commit}}"):
            pytest.skip("PR #344's merge commit is not present in this checkout")
        parents = _git("rev-list", "--parents", "-n", "1", PR344_MERGE_SHA).split()
        assert parents[0] == PR344_MERGE_SHA
        assert parents[1:] == [PR344_BASE_SHA, PR344_ACCEPTED_HEAD], parents[1:]


# ======================================================================================
# 2 -- No later CI run repairs the failed run
# ======================================================================================


class TestFailedRunIsImmutable:
    def test_the_decision_states_a_later_run_cannot_retroactively_satisfy_l6(self, decision_flat_lower):
        assert "cannot retroactively satisfy" in decision_flat_lower
        assert "permanently unsatisfiable" in decision_flat_lower

    def test_the_decision_quotes_l6s_own_exclusion_of_other_commits(self, decision_flat):
        """The exclusion must rest on §L.6's own words, not on this filing's preference."""
        assert "not a run against any other commit" in decision_flat

    def test_the_decision_never_claims_a_later_run_repairs_the_failed_one(self, decision_text):
        """Mutation pin: the decision must contain no sentence licensing repair by re-run."""
        lowered = decision_text.lower()
        forbidden = (
            "a later green run satisfies",
            "a subsequent successful run satisfies",
            "re-running the failed job satisfies",
            "may be treated as satisfying",
            "retroactively satisfies",
            "retroactively satisfied",
        )
        for phrase in forbidden:
            assert phrase not in lowered, phrase

    def test_xasset_0044_is_never_described_as_effective(self, decision_text):
        lowered = _flat(decision_text).lower()
        # The §D statement, verbatim: not merely "not effective now", but incapable of
        # becoming effective through the pull request that failed its own §L.6 condition.
        assert (
            "`xasset-0044` is **not effective and cannot become effective through pr #344**"
            in lowered
        )
        for phrase in (
            "xasset-0044 is effective",
            "xasset-0044 becomes effective",
            "xasset-0044 is now effective",
            "provisionally effective",
        ):
            # "provisionally effective" may only appear inside an explicit prohibition.
            if phrase == "provisionally effective":
                idx = lowered.find(phrase)
                if idx != -1:
                    window = lowered[max(0, idx - 200) : idx + 60]
                    assert "may not" in window or "no session" in window, window
                continue
            assert phrase not in lowered, phrase

    def test_the_exact_failed_run_and_job_identities_are_recorded(self, decision_text):
        assert FAILED_CI_RUN in decision_text
        assert FAILED_CI_JOB in decision_text

    def test_the_failed_run_is_bound_to_the_exact_merge_sha(self, decision_text):
        """A run identity with no commit identity beside it proves nothing."""
        assert PR344_MERGE_SHA in decision_text
        idx = decision_text.find(FAILED_CI_RUN)
        assert idx != -1
        window = decision_text[max(0, idx - 400) : idx + 400]
        assert "f5dedce1" in window, window


# ======================================================================================
# 3 -- Exactly one future unit, and it is separate
# ======================================================================================


class TestExactlyOneFutureUnit:
    def test_the_grant_is_exactly_one(self, decision_flat):
        assert "**exactly one** future, separate, bounded pull request" in decision_flat

    def test_no_second_unit_is_authorized_by_completing_the_first(self, decision_flat):
        assert "completing the authorized unit does not authorize another" in decision_flat

    def test_the_future_unit_must_file_its_own_decision(self, decision_flat_lower):
        assert "file its own decision" in decision_flat_lower

    def test_the_successor_identifier_is_not_predicted_or_reserved(self, decision_flat_lower):
        """A reserved identifier is a second authorization by another name."""
        assert "verified unused against live repository state" in decision_flat_lower
        assert "never predicted, reserved, or assumed here" in decision_flat_lower
        assert "names no successor identifier" in decision_flat_lower

    def test_no_xasset_identifier_beyond_0045_is_named_anywhere(self, decision_text):
        """Mutation pin: naming XASSET-0046 would silently pre-authorize it."""
        named = set(re.findall(r"XASSET-00\d\d", decision_text))
        beyond = {n for n in named if int(n.split("-")[1]) > 45}
        assert beyond == set(), beyond


# ======================================================================================
# 4 -- Predecessor authority is spent; nothing is reused
# ======================================================================================


class TestPredecessorAuthorityIsSpent:
    def test_xasset_0043s_single_grant_is_recorded_as_spent(self, decision_flat_lower):
        assert "spent" in decision_flat_lower
        assert "consumed by being used" in decision_flat_lower

    def test_xasset_0043_may_not_be_reused(self, decision_flat_lower):
        assert "may not be reused" in decision_flat_lower

    def test_the_reason_the_grant_is_spent_does_not_depend_on_effectivity(self, decision_flat_lower):
        """The distinction that makes §E sound: a grant is spent by use, while effectivity
        governs whether the rebinding takes effect. Collapsing the two would revive §F."""
        assert "whether or not" in decision_flat_lower
        assert "effectivity governs whether the *rebinding takes effect*" in decision_flat_lower

    def test_authority_derives_from_this_decision_and_nothing_else(self, decision_flat):
        assert "from **this** decision, and from nothing else" in decision_flat


# ======================================================================================
# 5 -- The closed range is exact and immutable
# ======================================================================================


class TestClosedRangeIsExactAndImmutable:
    def test_both_endpoints_are_named_exactly(self, decision_text):
        assert PR344_BASE_SHA in decision_text
        assert PR344_ACCEPTED_HEAD in decision_text

    def test_the_correction_is_required_against_the_closed_range(self, decision_flat_lower):
        assert "closed" in decision_flat_lower
        assert "immutable" in decision_flat_lower
        assert "rather than any moving merge-base" in decision_flat_lower

    def test_a_moving_head_or_origin_main_guard_is_forbidden(self, decision_flat):
        assert (
            "**No moving `HEAD`/`origin/main` guard may claim historical byte identity**"
            in decision_flat
        )

    def test_the_corrected_guard_must_not_depend_on_where_head_points(self, decision_flat_lower):
        assert "must not depend on where `head` or `origin/main` point" in decision_flat_lower

    def test_the_one_use_transition_conjuncts_stay_independently_required(self, decision_text):
        assert AUTHORIZED_OLD_BLOB in decision_text
        assert AUTHORIZED_NEW_BLOB in decision_text
        assert "each conjunct independently required" in decision_text.lower()

    def test_dead_permission_protection_is_retained_not_dropped(self, decision_text):
        assert "dead permission" in decision_text.lower()

    def test_other_pre_existing_decisions_stay_protected(self, decision_flat_lower):
        assert "every other pre-existing decision file must remain protected" in decision_flat_lower


# ======================================================================================
# 6 -- The successor lifecycle anchor is required
# ======================================================================================


class TestSuccessorLifecycleAnchorRequired:
    def test_the_requirement_exists_and_is_named(self, decision_flat_lower):
        assert "successor lifecycle anchor" in decision_flat_lower

    def test_the_reason_is_the_current_production_binding(self, decision_text):
        """The requirement must be grounded in what production actually binds today."""
        assert 'AUTHORIZING_DECISION = "XASSET-0044"' in decision_text
        assert "AUTHORIZING_PULL_REQUEST = 344" in decision_text
        assert "REVIEWED_BASE_SHA" in decision_text

    def test_production_really_does_bind_pr_344_today(self):
        """Not a claim about the repository -- a check of it."""
        module = (ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        assert 'AUTHORIZING_DECISION = "XASSET-0044"' in module
        assert "AUTHORIZING_PULL_REQUEST = 344" in module
        assert f'REVIEWED_BASE_SHA = "{PR344_BASE_SHA}"' in module

    def test_rebinding_is_bounded_to_strict_necessity(self, decision_flat_lower):
        assert "only as strictly necessary" in decision_flat_lower
        assert "may not be made more permissive" in decision_flat_lower

    def test_the_anchor_must_cover_the_full_future_lifecycle(self, decision_flat_lower):
        assert (
            "own** decision, pull request, accepted head, merge, successful exact-merge ci, "
            "and final closure"
        ) in decision_flat_lower


# ======================================================================================
# 7 -- Adverse history is preserved
# ======================================================================================


class TestAdverseHistoryPreserved:
    def test_the_failed_run_must_be_retained_by_exact_identity(self, decision_flat_lower):
        assert "immutable adverse history" in decision_flat_lower

    def test_every_forbidden_disposal_of_the_failed_run_is_named(self, decision_flat_lower):
        lowered = decision_flat_lower
        for verb in (
            "relabelled successful",
            "deleted",
            "suppressed",
            "re-run in place",
            "described as passing",
            "represented as satisfying",
        ):
            assert verb in lowered, verb

    def test_the_stop_notice_is_preserved(self, decision_text):
        assert AUDITABLE_STOP_COMMENT in decision_text

    def test_the_completed_predecessor_evidence_is_preserved(self, decision_text):
        for identity in (
            FINAL_CLEAN_REVIEW,
            PRINCIPAL_ACCEPTANCE_COMMENT,
            POST_MERGE_VERIFICATION_COMMENT,
        ):
            assert identity in decision_text, identity

    def test_predecessor_evidence_may_not_be_erased_or_re_pointed(self, decision_flat_lower):
        assert "never erased, overwritten, or silently re-pointed" in decision_flat_lower


# ======================================================================================
# 8 -- Zero activation authority
# ======================================================================================


class TestZeroActivationAuthority:
    def test_every_withheld_activation_capability_is_named(self, decision_flat_lower):
        lowered = decision_flat_lower
        for capability in (
            "readiness verification",
            "drift verification",
            "step 11",
            "attestation",
            "lane state",
            "arm",
            "claim",
            "gate for any registered construction",
            "recovery execution",
            "results work",
            "protected `risk`",
        ):
            assert capability in lowered, capability

    def test_zero_activation_authority_is_stated_explicitly(self, decision_flat_lower):
        assert "zero activation authority" in decision_flat_lower

    def test_executable_stays_permanently_false(self, decision_flat_lower):
        assert "`stage_1_executability.executable` stays permanently `false`" in decision_flat_lower
        assert "no committed value in this repository" in decision_flat_lower

    def test_attempt_1_and_spent_grants_are_not_revived(self, decision_flat_lower):
        lowered = decision_flat_lower
        assert "re-open `attempt_1`" in lowered
        assert "xasset-0040" in lowered
        assert "stopped_before_attestation" in lowered
        assert "§p.1" in lowered

    def test_the_live_posture_really_is_unarmed(self):
        """The repository state itself, not the decision's description of it."""
        import level1_stage1_execution_authorization as auth

        assert auth.AUTHORIZATION_ROOT.exists() is False
        authorized, _reason = auth.new_execution_is_authorized()
        assert authorized is False
        assert auth.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

    def test_no_stage1_results_artifact_exists_anywhere(self):
        assert list(ROOT.rglob("stage1_results.yaml")) == []

    def test_this_suite_imports_no_outcome_producing_module(self):
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        forbidden = {
            "level1_stage1_runner",
            "level1_stage1_result_validator",
        }
        assert imported & forbidden == set(), imported & forbidden


# ======================================================================================
# 9 -- The filing itself is design-only
# ======================================================================================


class TestFilingIsDesignOnly:
    def test_the_decision_declares_itself_design_only(self, decision_flat_lower):
        assert "design-only" in decision_flat_lower

    def test_the_decision_does_not_correct_the_guard_itself(self, decision_flat_lower):
        assert "does not correct the failing guard" in decision_flat_lower

    def test_no_protected_path_was_touched_by_this_filing(self):
        """Proven against git, not asserted: this branch changes none of them."""
        if not _git_ok("rev-parse", "--verify", "origin/main"):
            pytest.skip("origin/main not resolvable in this environment")
        changed = set(_git("diff", "--name-only", "origin/main").splitlines())
        overlap = changed & set(PROTECTED_RELPATHS)
        assert overlap == set(), overlap

    def test_the_universe_identity_is_unchanged(self, decision_text):
        assert str(UNIVERSE_CONSTRUCTIONS) in decision_text
        assert str(UNIVERSE_CELLS) in decision_text
        assert UNIVERSE_AGGREGATE_HASH in decision_text

    def test_the_pre_existing_guard_failure_is_disclosed_not_worked_around(self, decision_text):
        """Honesty pin: the filing must disclose that its own CI fails on the same defect,
        and must not claim to have fixed, skipped, or avoided it."""
        flat_lower = _flat(decision_text).lower()
        assert "pre-existing, reproduced, disclosed, and not introduced by this pr" in flat_lower
        assert "explicitly barred" in flat_lower
        assert FAILING_GUARD_TEST in decision_text
        assert FAILING_GUARD_FILE in decision_text

    def test_the_disclosed_failure_mechanism_is_correct(self, decision_flat):
        """The disclosure must name the real reason -- status ``A`` is skipped -- rather than
        a vague 'CI may fail'."""
        assert "status `A`" in decision_flat
        assert "modified == []" in decision_flat


# ======================================================================================
# 10 -- Fail-closed
# ======================================================================================


class TestFailClosed:
    def test_unobtainable_facts_are_errors_never_agreement(self, decision_flat_lower):
        assert "never silent agreement" in decision_flat_lower

    def test_ambiguity_is_a_stop_not_a_judgement_call(self, decision_flat_lower):
        assert "stop and disclose" in decision_flat_lower
        assert "is a **stop**, not a judgement call" in decision_flat_lower

    def test_repackaging_requires_a_stop(self, decision_flat_lower):
        assert "package it differently must **stop and disclose**" in decision_flat_lower

    def test_nothing_may_be_weakened(self, decision_flat_lower):
        lowered = decision_flat_lower
        for verb in ("deleted", "skipped", "`xfail`ed", "weakened"):
            assert verb in lowered, verb
        assert "less falsifiable" in lowered


# ======================================================================================
# 11 -- Effectivity requires the complete lifecycle
# ======================================================================================


class TestEffectivityRequiresCompleteLifecycle:
    def test_all_seven_conditions_are_present(self, decision_text):
        section = decision_text.split("### M. Effectivity", 1)[1]
        for n in range(1, 8):
            assert f"\n{n}. " in section, n

    def test_none_is_individually_sufficient(self, decision_text):
        assert "**None is individually sufficient.**" in decision_text

    def test_merge_does_not_arm(self, decision_flat_lower):
        assert "merging this arms nothing" in decision_flat_lower
        assert "still returns `false`" in decision_flat_lower

    def test_condition_six_names_the_exact_merge_sha_requirement(self, decision_text):
        section = decision_text.split("### M. Effectivity", 1)[1]
        assert "**successful merge-commit CI whose `head_sha` is the exact merge SHA**" in section


# ======================================================================================
# 12 -- Catalog and register synchronisation
# ======================================================================================


class TestCatalogAndRegisterSynchronisation:
    def test_the_catalog_entry_points_at_the_real_file(self, catalog_entry):
        assert catalog_entry["file"] == (
            "governance/decisions/"
            "XASSET-0045-endpoint-0001-stage-1-post-merge-ci-recovery-authorization.md"
        )
        assert (ROOT / catalog_entry["file"]).is_file()

    def test_the_catalog_entry_names_this_supporting_artifact(self, catalog_entry):
        assert catalog_entry["supporting_artifact"] == SUITE_PATH.name

    def test_the_decision_is_proposed_not_accepted_by_its_own_filing(self, catalog_entry):
        """A filing does not accept itself."""
        assert catalog_entry["status"] == "Proposed"

    def test_the_gate_is_in_progress_while_its_own_pr_is_unmerged(self, gate):
        assert gate["status"] == "in_progress"

    def test_the_gate_records_the_exact_immutable_facts(self, gate):
        description = gate["description"]
        for identity in (
            PR344_MERGE_SHA,
            PR344_BASE_SHA,
            PR344_ACCEPTED_HEAD,
            PR344_MERGE_TREE,
            FAILED_CI_RUN,
            FAILED_CI_JOB,
        ):
            assert identity in description, identity

    def test_the_gate_states_the_authorization_is_design_only(self, gate):
        assert "DESIGN-ONLY AUTHORIZATION" in gate["description"]

    def test_the_gate_states_exactly_one_future_unit(self, gate):
        assert "EXACTLY ONE future" in gate["description"]

    def test_workstream_live_fields_reflect_this_session(self, ws0014):
        """WS-0014's shared live self-reference fields. PR #344 has merged at ``f5dedce1``,
        so under ``OPS-0001``'s Active-GitHub-fields rule they lawfully advance to the unit
        that is now live. Each stays an exact value, never relaxed to a range."""
        assert ws0014["last_verified_main_sha"] == PR344_MERGE_SHA
        assert str(ws0014["last_verified_date"]) == "2026-08-21"
        assert ws0014["active_branch"] != "claude/xasset-0043-rebinding-7ywmdx"

    def test_workstream_stays_secondary_and_no_primary_is_introduced(self, register, ws0014):
        assert ws0014["status"] == "proposed"
        assert ws0014["priority"] == "secondary"
        primary = [w["id"] for w in register["workstreams"] if w.get("priority") == "primary"]
        assert primary == []

    def test_pr_344s_own_closed_record_survives_as_history(self, ws0014):
        """Advancing WS-0014's SHARED live self-reference fields must not erase the
        predecessor's own closed record. That record lives in its own gate -- which keeps
        `pr: 344` -- not in the shared live fields, which by design point only at the unit
        that is currently live."""
        gates = {g.get("gate"): g for g in ws0014["milestones"]}
        predecessor = gates["xasset0044-post-correction-operational-rebinding"]
        assert predecessor["pr"] == 344
        assert PR344_BASE_SHA in predecessor["description"]


# ======================================================================================
# 13 -- No section is vacuous
# ======================================================================================


class TestNoSectionIsVacuous:
    def test_every_lettered_section_exists_and_has_substance(self, decision_text):
        headings = re.findall(r"^### ([A-N])\. (.+)$", decision_text, flags=re.MULTILINE)
        letters = [h[0] for h in headings]
        assert letters == list("ABCDEFGHIJKLMN"), letters
        for letter, _title in headings:
            body = decision_text.split(f"### {letter}. ", 1)[1]
            body = re.split(r"\n### [A-N]\. |\n## ", body, maxsplit=1)[0]
            assert len(body.split()) > 25, f"section {letter} is too thin"

    def test_the_required_properties_are_numbered_g1_to_g12(self, decision_text):
        section = decision_text.split("### G. Required properties", 1)[1]
        section = section.split("### H.", 1)[0]
        for n in range(1, 13):
            assert f"**G.{n} —" in section, n

    def test_the_alternatives_section_records_real_rejections(self, decision_text):
        section = decision_text.split("## Alternatives Considered", 1)[1]
        section = section.split("## Consequences", 1)[0]
        assert section.lower().count("rejected") >= 5

    def test_this_suite_contains_no_vacuous_assertion(self):
        """No ``assert ... or True``-style disjunct, and no bare truthy constant, may hide a
        false premise anywhere in this file. Checked over the parsed AST, not by substring
        scan -- a text search would flag the very comments that explain the rule."""
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        asserts = [n for n in ast.walk(tree) if isinstance(n, ast.Assert)]
        assert len(asserts) > 60, len(asserts)
        for node in asserts:
            test = node.test
            if isinstance(test, ast.Constant):
                pytest.fail(f"bare constant assertion at line {node.lineno}")
            if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.Or):
                for value in test.values:
                    if isinstance(value, ast.Constant) and bool(value.value):
                        pytest.fail(f"constant-truthy disjunct at line {node.lineno}")
