"""Adversarial tests pinning the ``XASSET-0046`` post-merge-CI recovery REAUTHORIZATION.

``XASSET-0045`` merged with a drift-free tree, a clean final review, principal acceptance, and
post-merge verification -- and then its **merge-commit CI failed**, exactly as ``XASSET-0044``'s
had. ``XASSET-0045`` §M makes seven conditions conjunctively necessary; its sixth requires
*successful merge-commit CI whose ``head_sha`` is the exact merge SHA*. That run failed, the
seventh condition (final post-CI lifecycle closure) correctly never happened, and ``XASSET-0045``
is therefore **not effective**.

The danger this suite exists to prevent is not the recovery. It is the set of shortcuts a later
session could read into a filing that sits two merged-but-ineffective decisions away from an
armable Stage 1:

1. **``XASSET-0045`` treated as effective, or six-of-seven treated as seven.**
   ``TestPredecessorIsPermanentlyIneffective``.
2. **Either failed run relabelled, re-run in place, waived, or represented as successful.**
   ``TestBothFailedRunsAreImmutable``.
3. **A lifecycle closure posted retrospectively for a lifecycle that stopped.**
   ``TestClosureWasCorrectlyNotPosted``.
4. **``XASSET-0045``'s never-vested grant reached for as though it were still available.**
   ``TestPredecessorAuthorizesNoSuccessor`` -- the distinction from ``XASSET-0043``'s
   spent-by-use grant is stated, because the two fail in opposite ways.
5. **This decision authorizing its own enabling repair.** ``TestAuthorityIsNotCircular``.
6. **The corrections stretched into the production recovery.** ``TestFilingIsBounded``.
7. **Obligations built on an ineffective decision by cross-reference.**
   ``TestOperativePropertiesAreRestatedDirectly``.
8. **Activation authority acquired by implication.** ``TestZeroActivationAuthority``.
9. **A filing whose own effectivity its own contents make unreachable.**
   ``TestTheFilingCanAttainGreenCI`` -- the defect that stopped both predecessors.
10. **The register or catalog desynchronised, or a section left vacuous.**
    ``TestCatalogAndRegisterSynchronisation`` and ``TestNoSectionIsVacuous``.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No attestation, claim, completion, lane directory, or ledger entry is created or
read for authorization purposes. No ``risk_lane_boundary`` protected result path is read, listed,
opened, or referenced. No module capable of producing a Stage-1 outcome is imported.
"""

from __future__ import annotations

import ast
import re
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent

DECISION_ID = "XASSET-0046"
DECISION_PATH = ROOT / (
    "governance/decisions/"
    "XASSET-0046-endpoint-0001-stage-1-post-merge-ci-recovery-reauthorization.md"
)
CATALOG_PATH = ROOT / "governance/decisions.yaml"
REGISTER_PATH = ROOT / "operations/WORKSTREAMS.yaml"
SUITE_PATH = Path(__file__).resolve()
REGISTER_GATE = "xasset0046-post-merge-ci-recovery-reauthorization"

#: The corrected artifact this filing repairs. Not this suite -- the two defects live in
#: ``XASSET-0045``'s own supporting artifact, which is where the corrections had to go.
#: Over PR #345's closed range this file has status ``A``: it was ADDED by PR #345, so it has
#: no blob at the base.
CORRECTED_ARTIFACT_RELPATH = "test_level1_stage1_post_merge_ci_recovery_authorization.py"
#: The file the corrected assertions MEASURE -- ``XASSET-0045``'s own enabling correction, and
#: the only file carrying the ``M`` transition the blob constants below describe. Deliberately
#: kept distinct from ``CORRECTED_ARTIFACT_RELPATH``: conflating the two produces a proof that
#: cannot resolve, which is how the confusion was caught.
ENABLING_CORRECTION_RELPATH = "test_overlap_model_validator.py"

# ── The immutable facts this reauthorization is built on ────────────────────────────────────
#
# Every one was independently re-derived from live git and live GitHub during the filing
# session and is asserted here against the real object store, never taken on trust.

#: PR #345's base -- PR #344's merge commit.
PR345_BASE_SHA = "f5dedce1d1d3116ed8a6845c4447388c85a5414c"
#: PR #345's accepted head -- the exact commit final clean review 4993994386 examined.
PR345_ACCEPTED_HEAD = "61e629f0f655ce8ca4ccd7eaa370d132d593515c"
#: PR #345's merge commit -- and the ``head_sha`` of the FAILED merge-commit CI run.
PR345_MERGE_SHA = "2f8cdebe14925021171b9779453946be1f69b506"
#: The tree carried by BOTH the accepted head and the merge -- zero merge drift.
PR345_MERGE_TREE = "e5eb890550d55aa74c7430871f176761526b1ecf"

#: The enabling correction's exact one-use transition over that range, by object identity.
PR345_CORRECTION_OLD_BLOB = "5b916d881ed83db164233091863f2af87fa50828"
PR345_CORRECTION_NEW_BLOB = "536bf08bb7db81ffad15dcfa1de6e9ce4fca4899"

#: ``XASSET-0045``'s OWN failed merge-commit CI run and job, at PR345_MERGE_SHA.
XASSET0045_FAILED_CI_RUN = "32490789238"
XASSET0045_FAILED_CI_JOB = "96797667282"
#: ``XASSET-0044``'s failed merge-commit CI run and job, at PR345_BASE_SHA. Still immutable.
XASSET0044_FAILED_CI_RUN = "32439614683"
XASSET0044_FAILED_CI_JOB = "96647501864"

#: PR #345's lifecycle evidence that DID complete, preserved as authenticated predecessor
#: evidence.
PR345_FINAL_CLEAN_REVIEW = "4993994386"
PR345_FIRST_FULL_REVIEW = "4989608238"
PR345_DELTA_REVIEW = "4993351528"
PR345_PRINCIPAL_ACCEPTANCE = "5370936620"
PR345_POST_MERGE_VERIFICATION = "5370989769"
PR345_AUDITABLE_STOP = "5371158269"

#: THIS unit's own pull request, set from the real number GitHub issued and verified against
#: live GitHub after opening, never predicted.
THIS_PULL_REQUEST = 346

#: The guard whose moving anchor caused the failure, and its exact failing assertion line.
FAILING_GUARD_LINE = 662
FAILING_GUARD_TEST = "test_the_enabling_correction_was_actually_performed"
#: The second, quieter defect of the same class -- a VACUOUS PASS, never reported by CI.
VACUOUS_GUARD_TEST = "test_no_protected_path_was_touched_by_this_filing"

#: Universe identity -- must be untouched by a governance-plus-test-correction filing.
UNIVERSE_CONSTRUCTIONS = 680
UNIVERSE_CELLS = 48
UNIVERSE_AGGREGATE_HASH = (
    "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
)

#: Paths this filing must not touch.
PROTECTED_RELPATHS = (
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    "level1_construction_universe_closure_validator.py",
    "level1_stage1_execution_authorization.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "allocate.py",
    "margin_state.py",
    "levels.py",
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def _commit_exists(sha: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=ROOT, capture_output=True, text=True,
    ).returncode == 0


def _pr345_range_is_present() -> bool:
    return any(
        _commit_exists(sha)
        for sha in (PR345_BASE_SHA, PR345_ACCEPTED_HEAD, PR345_MERGE_SHA)
    )


def _flat(text: str) -> str:
    """Collapse all runs of whitespace to single spaces.

    The decision is hard-wrapped prose, so an exact phrase can straddle a newline. Matching
    against the flattened text keeps every assertion an EXACT phrase match while making it
    insensitive to where the paragraph happens to wrap. Deliberately not a weakening: the
    full phrase must still be present, in order, verbatim.
    """
    return " ".join(text.split())


def _section(text: str, letter: str) -> str:
    """The body of one lettered Decision subsection, flattened.

    Scoping an assertion to the section where a claim is OPERATIVE is what makes it
    mutation-sensitive: a phrase that also appears in a summary elsewhere can no longer
    satisfy a check on the section that actually carries the rule.
    """
    marker = f"\n### {letter}. "
    assert marker in text, f"section {letter} is missing"
    body = text.split(marker, 1)[1]
    body = re.split(r"\n### [A-N]\. |\n## ", body, maxsplit=1)[0]
    return _flat(body)


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
# 1 -- XASSET-0045 is PERMANENTLY not effective
# ======================================================================================


class TestPredecessorIsPermanentlyIneffective:
    def test_the_decision_states_the_sixth_condition_failed(self, decision_flat_lower):
        assert "the sixth" in decision_flat_lower
        assert "failed" in decision_flat_lower

    def test_ineffectivity_is_stated_as_PERMANENT_not_pending(self, decision_text):
        d = _section(decision_text, "D")
        assert "permanently unsatisfiable" in d
        assert "not effective and cannot become effective through PR #345" in d

    def test_the_decision_quotes_the_conditions_own_exclusion_of_other_commits(self, decision_flat):
        """The exclusion must rest on §M.6's own words, not on this filing's preference."""
        assert "not a run against any other commit" in decision_flat

    def test_a_later_green_run_is_excluded_by_the_condition_itself(self, decision_text):
        d = _section(decision_text, "D")
        assert "excluded by the condition itself" in d
        for claim in ("retroactively satisfy", "later run repairs", "now considered effective"):
            assert claim not in d.lower(), claim

    def test_six_of_seven_is_not_seven(self, decision_flat_lower):
        assert "none is individually sufficient" in decision_flat_lower
        assert "six of seven" in decision_flat_lower

    def test_the_exact_failing_run_and_job_are_named(self, decision_flat):
        assert XASSET0045_FAILED_CI_RUN in decision_flat
        assert XASSET0045_FAILED_CI_JOB in decision_flat

    def test_the_exact_merge_sha_the_condition_names_is_recorded(self, decision_flat):
        assert PR345_MERGE_SHA in decision_flat

    def test_the_recorded_failure_counts_match_the_immutable_job_log(self, decision_flat):
        assert "1 failed, 10348 passed" in decision_flat

    def test_the_merge_identity_is_proven_from_the_object_store(self):
        """Not asserted: the merge really does carry exactly two parents in order, and its
        tree really is the accepted head's."""
        if not _pr345_range_is_present():
            pytest.skip("PR #345's closed range is not present in this checkout")
        parents = _git("rev-list", "--parents", "-n", "1", PR345_MERGE_SHA).split()
        assert parents[1:] == [PR345_BASE_SHA, PR345_ACCEPTED_HEAD], parents[1:]
        assert _git("rev-parse", f"{PR345_MERGE_SHA}^{{tree}}") == PR345_MERGE_TREE
        assert _git("rev-parse", f"{PR345_ACCEPTED_HEAD}^{{tree}}") == PR345_MERGE_TREE


# ======================================================================================
# 2 -- BOTH failed runs are immutable adverse history
# ======================================================================================


class TestBothFailedRunsAreImmutable:
    def test_xasset0045s_failed_run_is_named_immutable(self, decision_text):
        d = _section(decision_text, "D")
        assert XASSET0045_FAILED_CI_RUN in d
        assert XASSET0045_FAILED_CI_JOB in d
        assert "immutable adverse history" in d.lower()

    def test_xasset0044s_failed_run_is_preserved_on_the_same_footing(self, decision_text):
        """Correcting the newer stop must not quietly drop the older one."""
        d = _section(decision_text, "D")
        assert XASSET0044_FAILED_CI_RUN in d
        assert XASSET0044_FAILED_CI_JOB in d

    def test_every_form_of_rewriting_a_failed_run_is_refused(self, decision_text):
        d = _section(decision_text, "D")
        for verb in ("re-run in place", "relabelled successful", "deleted", "suppressed",
                     "waived", "described as passing"):
            assert verb in d, verb

    def test_the_run_is_never_claimed_to_satisfy_the_condition(self, decision_flat):
        lowered = decision_flat.lower()
        for claim in ("now satisfies", "retroactively repaired", "may be re-run"):
            assert claim not in lowered, claim

    def test_the_no_retry_reasoning_is_recorded_not_assumed(self, decision_text):
        """A deterministic test failure is not an infrastructure fault, and the decision must
        say why rather than simply not retrying."""
        d = _section(decision_text, "D")
        assert "not retried" in d.lower() or "correctly not retried" in d.lower()
        assert "deterministic" in d.lower()

    def test_the_auditable_stop_is_preserved(self, decision_flat):
        assert PR345_AUDITABLE_STOP in decision_flat

    def test_the_recovery_unit_must_preserve_both_runs(self, decision_text):
        g = _section(decision_text, "G")
        assert "**G.5 —" in g
        assert XASSET0045_FAILED_CI_RUN in g
        assert XASSET0044_FAILED_CI_RUN in g


# ======================================================================================
# 3 -- The final closure was correctly not posted, and must never be posted
# ======================================================================================


class TestClosureWasCorrectlyNotPosted:
    def test_the_decision_records_that_closure_never_occurred(self, decision_flat_lower):
        assert "never occurred and was correctly not manufactured" in decision_flat_lower

    def test_closure_may_not_be_posted_retrospectively(self, decision_text):
        d = _section(decision_text, "D")
        assert "correctly not posted" in d
        assert "never be posted retrospectively" in d

    def test_the_stop_comment_is_cited_as_the_auditable_record(self, decision_flat):
        assert PR345_AUDITABLE_STOP in decision_flat


# ======================================================================================
# 4 -- XASSET-0045 authorizes no successor unit
#
# Its grant NEVER VESTED. XASSET-0043's was SPENT BY USE. Both end in "no authority", but
# for opposite reasons, and conflating them is how a future session reaches for the unspent
# one by analogy to the spent one.
# ======================================================================================


class TestPredecessorAuthorizesNoSuccessor:
    def test_the_grant_is_stated_to_have_never_taken_effect(self, decision_text):
        e = _section(decision_text, "E")
        assert "never took effect" in e
        assert "authorizes no unit" in e

    def test_the_never_vested_and_spent_by_use_failure_modes_are_distinguished(self, decision_text):
        e = _section(decision_text, "E")
        assert "spent by being used" in e
        assert "never spent, because it never became available to spend" in e
        assert "opposite reasons" in e

    def test_an_unspent_grant_is_explicitly_not_a_grant_in_reserve(self, decision_flat):
        assert "an unspent grant that never vested is not a grant in reserve" in decision_flat

    def test_each_predecessor_is_given_its_own_correct_status(self, decision_text):
        e = _section(decision_text, "E")
        assert "**`XASSET-0043` remains spent**" in e
        assert "**`XASSET-0044` remains not effective**" in e
        assert "**`XASSET-0045` remains not effective**" in e

    def test_no_predecessor_may_be_cited_as_authority(self, decision_text):
        e = _section(decision_text, "E")
        assert "may not be cited as the authority for any unit" in e

    def test_the_withheld_section_refuses_reuse_of_each_predecessor(self, decision_text):
        h = _section(decision_text, "H")
        assert "reuse `XASSET-0043`" in h
        assert "reuse `XASSET-0045`" in h
        assert "treat `XASSET-0044` or `XASSET-0045` as effective" in h


# ======================================================================================
# 5 -- The authority for the corrections is NOT created by this decision
# ======================================================================================


class TestAuthorityIsNotCircular:
    def test_the_circularity_is_refused_explicitly(self, decision_text):
        k = _section(decision_text, "K")
        assert "**The authority for those corrections is not created by this decision.**" in k
        assert "cannot authorize its own enabling repair without circularity" in k

    def test_the_ineffective_predecessor_is_refused_as_a_source_too(self, decision_text):
        """The obvious wrong answer: cite XASSET-0045 §K's authorization instead."""
        k = _section(decision_text, "K")
        assert "an ineffective `XASSET-0045` cannot supply it either" in k

    def test_the_real_source_is_named_as_a_separate_principal_authorization(self, decision_text):
        k = _section(decision_text, "K")
        assert "separate, explicit principal authorization" in k
        assert "given after run" in k
        assert XASSET0045_FAILED_CI_RUN in k

    def test_a_decision_minting_its_own_authority_is_named_as_the_refused_shape(self, decision_text):
        k = _section(decision_text, "K")
        assert "exercising authority it minted in the same document" in k

    def test_every_other_prohibition_remains_operative(self, decision_text):
        k = _section(decision_text, "K")
        assert "remained, and remains, fully operative" in k


# ======================================================================================
# 6 -- The filing is bounded: two test-only corrections plus governance
# ======================================================================================


class TestFilingIsBounded:
    def test_the_decision_does_not_claim_to_be_purely_design_only(self, decision_flat_lower):
        assert "is **not** purely design-only, and does not claim to be" in decision_flat_lower

    def test_the_scope_section_names_both_corrections_and_the_corrected_file(self, decision_text):
        k = _section(decision_text, "K")
        assert "**two** narrow, **test-only** corrections" in k
        assert CORRECTED_ARTIFACT_RELPATH in k

    def test_the_corrections_are_recorded_as_strictly_narrowing(self, decision_text):
        k = _section(decision_text, "K")
        assert "strictly narrowing in effect" in k
        assert (
            "Nothing was deleted, skipped, `xfail`ed, weakened, or replaced with a less "
            "falsifiable assertion." in k
        )

    def test_the_third_audit_finding_is_disclosed_not_hidden(self, decision_text):
        """The removed skip guard was not reported by CI and had to be disclosed, not
        silently folded in."""
        k = _section(decision_text, "K")
        assert "One further audit finding is disclosed" in k
        assert "skip guard" in k

    def test_the_filing_edits_no_production_or_canonical_byte(self, decision_text):
        k = _section(decision_text, "K")
        for phrase in ("**no** load-bearing implementation", "no runner",
                       "no result validator", "no universe module", "no canonical artifact",
                       "no protected portfolio path"):
            assert phrase in k, phrase

    def test_the_corrected_file_is_not_load_bearing(self):
        """The corrections may not reach the bound execution surface."""
        import level1_stage1_execution_authorization as auth

        assert CORRECTED_ARTIFACT_RELPATH not in auth.LOAD_BEARING_RELPATHS

    def test_no_protected_path_was_touched_over_pr345s_closed_range(self):
        """Independent confirmation, from the object store, that the range this filing's
        corrections are anchored to contains no protected path -- proven over a NON-EMPTY
        change set, so it cannot pass by measuring nothing."""
        if not _pr345_range_is_present():
            pytest.skip("PR #345's closed range is not present in this checkout")
        rows = [
            line.split("\t")
            for line in _git(
                "diff", "--name-status", PR345_BASE_SHA, PR345_ACCEPTED_HEAD
            ).splitlines()
            if line.strip()
        ]
        changed = {path for _status, path in rows}
        assert len(changed) == 12, sorted(changed)
        assert changed & set(PROTECTED_RELPATHS) == set()

    def test_the_recovery_itself_is_not_performed(self, decision_text):
        a = _section(decision_text, "A")
        assert "performs **no** part of the recovery" in a


# ======================================================================================
# 7 -- Operative properties are RESTATED, never inherited from an ineffective decision
# ======================================================================================


class TestOperativePropertiesAreRestatedDirectly:
    def test_the_restatement_rule_is_stated(self, decision_text):
        e = _section(decision_text, "E")
        assert "restates directly" in e
        assert "derives its obligations from **this** decision" in e

    def test_the_predecessor_is_preserved_as_design_input_not_authority(self, decision_text):
        e = _section(decision_text, "E")
        assert "historical design input, not as effective authority" in e
        assert "may consult `XASSET-0045` for reasoning; a future unit may not cite it for authority" in e

    def test_the_required_properties_are_numbered_g1_to_g13(self, decision_text):
        section = decision_text.split("### G. Required properties", 1)[1]
        section = section.split("### H.", 1)[0]
        for n in range(1, 14):
            assert f"**G.{n} —" in section, n

    def test_the_properties_are_stated_directly_in_this_decision(self, decision_text):
        g = _section(decision_text, "G")
        assert "Stated directly and completely here" in g

    def test_the_closed_range_arrow_names_both_endpoints_together(self, decision_text):
        """§G.2's range must name BOTH endpoints in one transition, not two loose SHAs."""
        g = _section(decision_text, "G")
        assert f"{PR345_BASE_SHA} -> {PR345_ACCEPTED_HEAD}" in g

    def test_the_predecessors_own_repaired_guard_is_protected_from_reversion(self, decision_text):
        """The XASSET-0045 repair is merged content and survives its decision's
        ineffectivity -- it may not be reverted on the theory that its authority lapsed."""
        g = _section(decision_text, "G")
        assert "survives its authorizing decision's ineffectivity" in g
        assert "may not be reverted" in g

    def test_the_moving_anchor_prohibition_is_restated_as_a_requirement(self, decision_text):
        g = _section(decision_text, "G")
        assert (
            "**No moving `HEAD`/`origin/main` guard may claim historical byte identity**" in g
        )

    def test_the_defect_class_audit_requirement_exists(self, decision_text):
        """§G.11 is the lesson from this stop: fixing the reported line is not enough."""
        g = _section(decision_text, "G")
        assert "**G.11 —" in g
        assert "Fixing only the assertion a failure names is not sufficient." in g

    def test_hollowing_out_a_guard_is_named_as_a_weakening(self, decision_text):
        g = _section(decision_text, "G")
        assert "still runs while proving less" in g
        assert "is a weakening, not a re-anchoring" in g

    def test_no_property_is_delegated_by_bare_cross_reference(self, decision_text):
        """A §G that said "as XASSET-0045 §G required" would build obligations on an
        ineffective decision."""
        g = _section(decision_text, "G")
        for delegation in (
            "as `XASSET-0045` §G requires",
            "per `XASSET-0045` §G",
            "unchanged from `XASSET-0045`",
        ):
            assert delegation not in g, delegation


# ======================================================================================
# 8 -- Zero activation authority
# ======================================================================================


class TestZeroActivationAuthority:
    def test_the_withheld_list_is_absolute(self, decision_text):
        h = _section(decision_text, "H")
        assert "adds **zero activation authority**" in h

    @pytest.mark.parametrize(
        "prohibition",
        [
            "perform renewed readiness verification",
            "perform renewed drift verification",
            "perform or authorize **Step 11**",
            "generate, pre-stage, or validate any **attestation**",
            "create lane state, write `AUTHORIZATION_ROOT`, or write the lane ledger",
            "**arm** Stage 1",
            "**claim** or consume `ATTEMPT_1`",
            "evaluate any gate for any registered construction",
            "execute Stage 1, perform recovery execution, or perform any results work",
            "access protected `RISK` evidence",
        ],
    )
    def test_each_prohibition_is_pinned_individually(self, decision_text, prohibition):
        """Individually, because a bare-word check survives corruption of the sentence: the
        mutated text still contains "arm", "claim", "Step 11"."""
        h = _section(decision_text, "H")
        assert prohibition in h, prohibition

    def test_executability_stays_permanently_false(self, decision_text):
        h = _section(decision_text, "H")
        assert "`stage_1_executability.executable` stays permanently `false`" in h
        assert "**No committed value in this repository\nauthorizes Stage-1 execution**" in (
            DECISION_PATH.read_text(encoding="utf-8")
        ) or "No committed value in this repository authorizes Stage-1 execution" in h

    def test_the_reserved_predecessor_budgets_are_untouched(self, decision_text):
        h = _section(decision_text, "H")
        assert "`XASSET-0040`" in h
        assert "STOPPED_BEFORE_ATTESTATION" in h
        assert "`XASSET-0027` §P.1" in h
        assert "one and unspent" in h

    def test_this_is_not_an_activation_pull_request(self, decision_text):
        section = _section(decision_text, "L")
        assert "not an activation pull request" in section
        assert "arms nothing" in section
        assert "never a merged authorization PR" in section

    def test_the_live_posture_is_actually_unarmed(self):
        """Proven against the real module, not asserted by the decision."""
        import level1_stage1_execution_authorization as auth

        authorized, _reason = auth.new_execution_is_authorized()
        assert authorized is False
        assert not Path(auth.AUTHORIZATION_ROOT).exists()
        assert auth.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

    def test_no_stage1_results_artifact_exists(self):
        assert list(ROOT.rglob("stage1_results.yaml")) == []

    def test_the_universe_identity_is_unchanged(self, decision_text):
        assert str(UNIVERSE_CONSTRUCTIONS) in decision_text
        assert str(UNIVERSE_CELLS) in decision_text
        assert UNIVERSE_AGGREGATE_HASH in decision_text


# ======================================================================================
# 9 -- Exactly one future unit, and it is separate
# ======================================================================================


class TestExactlyOneFutureUnit:
    def test_exactly_one_unit_is_authorized(self, decision_text):
        f = _section(decision_text, "F")
        assert "**exactly one** future," in f
        assert "It is one unit and one pull request." in f

    def test_completing_it_does_not_authorize_another(self, decision_text):
        f = _section(decision_text, "F")
        assert (
            "**No second unit is authorized by this decision, and completing the authorized "
            "unit does not authorize another.**" in f
        )

    def test_the_grant_is_conditioned_on_complete_lifecycle_closure(self, decision_text):
        f = _section(decision_text, "F")
        assert "Effective only on this decision's own complete lifecycle closure" in f

    def test_repackaging_requires_a_stop(self, decision_flat_lower):
        assert "package it differently must **stop and disclose**" in decision_flat_lower

    def test_the_successor_identifier_is_not_predicted_or_reserved(self, decision_flat_lower):
        assert "verified unused against live repository state" in decision_flat_lower
        assert "never predicted, reserved, or assumed here" in decision_flat_lower
        assert "names no successor identifier" in decision_flat_lower

    def test_no_xasset_identifier_beyond_0046_is_named_anywhere(self, decision_text):
        """Mutation pin: naming XASSET-0047 would silently pre-authorize it."""
        named = set(re.findall(r"XASSET-00\d\d", decision_text))
        beyond = {n for n in named if int(n.split("-")[1]) > 46}
        assert beyond == set(), beyond


# ======================================================================================
# 10 -- Fail-closed
# ======================================================================================


class TestFailClosed:
    def test_unobtainable_facts_are_errors_never_agreement(self, decision_flat_lower):
        assert "never silent agreement" in decision_flat_lower

    def test_ambiguity_is_a_stop_not_a_judgement_call(self, decision_flat_lower):
        assert "stop and disclose" in decision_flat_lower
        assert "is a **stop**, not a judgement call" in decision_flat_lower

    def test_nothing_may_be_weakened(self, decision_flat_lower):
        for verb in ("deleted", "skipped", "`xfail`ed", "weakened"):
            assert verb in decision_flat_lower, verb
        assert "less falsifiable" in decision_flat_lower


# ======================================================================================
# 11 -- Effectivity requires the complete lifecycle
# ======================================================================================


class TestEffectivityRequiresCompleteLifecycle:
    def test_all_seven_conditions_are_present(self, decision_text):
        m = _section(decision_text, "M")
        for n in range(1, 8):
            assert f" {n}. " in f" {m}", n

    def test_none_is_individually_sufficient(self, decision_text):
        m = _section(decision_text, "M")
        assert "**None is individually sufficient.**" in m

    def test_the_sixth_condition_names_the_exact_merge_sha_requirement(self, decision_text):
        m = _section(decision_text, "M")
        assert "successful merge-commit CI whose `head_sha` is the exact merge SHA" in m
        assert "not the PR head's own run, and not a run against any other commit" in m

    def test_merging_arms_nothing(self, decision_text):
        m = _section(decision_text, "M")
        assert "**Merging this arms nothing.**" in m
        assert "still returns `False`" in m

    def test_the_review_standard_is_named(self, decision_text):
        m = _section(decision_text, "M")
        assert "`OPS-0007` §1" in m
        assert "**FULL**" in m


# ======================================================================================
# 12 -- The filing can attain green CI: the non-deadlock condition
#
# This is the condition BOTH predecessors failed. XASSET-0045 failed it twice: once by
# declaring its own CI impossible, and once by merging with a fresh assertion that could
# not survive its own merge.
# ======================================================================================


#: Any surviving form of "this PR's CI cannot succeed" recreates the deadlock, whatever
#: wording it uses.
SELF_DEFEATING_CI_CLAIMS = (
    "this filing's own ci will fail",
    "this pr's own ci will fail",
    "necessarily fails",
    "must continue failing",
    "cannot be green",
    "expected to fail",
)


class TestTheFilingCanAttainGreenCI:
    def test_the_decision_does_not_claim_its_own_ci_must_fail(self, decision_flat_lower):
        for claim in SELF_DEFEATING_CI_CLAIMS:
            assert claim not in decision_flat_lower, claim

    def test_the_combined_non_deadlock_guard(self, decision_flat_lower):
        """The conjunction is refused directly, and NOT vacuously: satisfying it by dropping
        the successful-CI requirement instead of the impossibility claim is itself a failure.
        """
        requires_successful_ci = (
            "successful merge-commit ci whose `head_sha` is the exact merge sha"
            in decision_flat_lower
        )
        declares_ci_impossible = any(
            c in decision_flat_lower for c in SELF_DEFEATING_CI_CLAIMS
        )
        assert not (requires_successful_ci and declares_ci_impossible), (
            "deadlock: the decision requires successful exact-merge CI and simultaneously "
            "declares its own CI impossible, so it could never become effective"
        )
        # And the half that must hold, holds.
        assert requires_successful_ci

    def test_the_attainability_is_argued_not_asserted(self, decision_text):
        n = _section(decision_text, "N")
        assert "read **no** moving reference at all" in n
        for proof in ("structurally", "behaviourally", "adversarially"):
            assert proof in n, proof

    def test_the_five_ref_states_are_named(self, decision_text):
        n = _section(decision_text, "N")
        assert "**five**" in n
        for state in ("feature branch", "merged `main`", "a later `main`",
                      "unrelated later commits"):
            assert state in n, state

    def test_the_isolated_clone_discipline_is_recorded(self, decision_text):
        n = _section(decision_text, "N")
        assert "isolated clone" in n
        assert "never a `git worktree`" in n

    def test_a_red_ci_is_a_stop_not_an_accepted_deviation(self, decision_text):
        n = _section(decision_text, "N")
        assert "is a stop, not an accepted deviation" in n

    def test_the_predecessors_failed_runs_are_not_repaired_by_this_filing(self, decision_text):
        n = _section(decision_text, "N")
        assert "Nothing here retroactively repairs" in n
        assert XASSET0045_FAILED_CI_RUN in n
        assert XASSET0044_FAILED_CI_RUN in n

    def test_the_corrected_artifact_actually_passes_here_and_now(self):
        """The strongest available form of the claim: run the two corrected proofs in THIS
        checkout, which is merged ``main`` -- the exact ref state that failed."""
        result = subprocess.run(
            ["python3", "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider",
             f"{CORRECTED_ARTIFACT_RELPATH}::TestFilingIsGovernancePlusOneEnablingCorrection"],
            cwd=ROOT, capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stdout[-3000:]


# ======================================================================================
# 13 -- The defect is recorded truthfully, including the half CI never reported
# ======================================================================================


class TestTheDefectIsRecordedTruthfully:
    def test_the_failure_location_is_recorded_exactly(self, decision_text):
        assert f"{CORRECTED_ARTIFACT_RELPATH}:{FAILING_GUARD_LINE}" in decision_text
        assert FAILING_GUARD_TEST in decision_text

    def test_the_defect_is_named_a_moving_anchor_not_drift(self, decision_flat_lower):
        assert "moving test anchor" in decision_flat_lower
        assert "neither merge drift nor outcome-surface drift" in decision_flat_lower

    def test_the_recurrence_is_admitted_not_glossed(self, decision_text):
        b = _section(decision_text, "B")
        assert "same defect class" in b
        assert "reintroduced by `XASSET-0045`" in b

    def test_the_second_vacuous_defect_is_disclosed(self, decision_text):
        """The half CI never reported. Omitting it would leave a guard that cannot fail."""
        b = _section(decision_text, "B")
        assert VACUOUS_GUARD_TEST in b
        assert "vacuous pass" in b.lower()
        assert "A guard that cannot fail protects nothing" in b

    def test_the_two_defects_are_shown_to_share_one_cause(self, decision_text):
        b = _section(decision_text, "B")
        assert "opposite directions from one cause" in b

    def test_the_underlying_properties_are_recorded_as_true(self, decision_text):
        b = _section(decision_text, "B")
        assert PR345_CORRECTION_OLD_BLOB in b
        assert PR345_CORRECTION_NEW_BLOB in b
        assert "only the anchor they measured\nagainst was wrong" in (
            DECISION_PATH.read_text(encoding="utf-8")
        ) or "only the anchor they measured against was wrong" in b

    def test_the_blob_identities_are_real(self):
        """Proven from the object store, not from the decision's own prose."""
        if not _pr345_range_is_present():
            pytest.skip("PR #345's closed range is not present in this checkout")
        assert _git(
            "rev-parse", f"{PR345_BASE_SHA}:{ENABLING_CORRECTION_RELPATH}"
        ) == PR345_CORRECTION_OLD_BLOB
        assert _git(
            "rev-parse", f"{PR345_ACCEPTED_HEAD}:{ENABLING_CORRECTION_RELPATH}"
        ) == PR345_CORRECTION_NEW_BLOB
        # The corrected artifact itself was ADDED by PR #345 and has NO blob at the base --
        # the exact confusion this separation exists to prevent.
        rows = dict(
            (line.split("\t")[1], line.split("\t")[0])
            for line in _git(
                "diff", "--name-status", PR345_BASE_SHA, PR345_ACCEPTED_HEAD
            ).splitlines() if line.strip()
        )
        assert rows[ENABLING_CORRECTION_RELPATH] == "M"
        assert rows[CORRECTED_ARTIFACT_RELPATH] == "A"


# ======================================================================================
# 14 -- Catalog and register synchronisation
# ======================================================================================


class TestCatalogAndRegisterSynchronisation:
    def test_the_catalog_entry_exists_and_is_consistent(self, catalog_entry):
        assert catalog_entry["decision_id"] == DECISION_ID
        assert catalog_entry["status"] == "Proposed"
        assert catalog_entry["category"] == "cross_asset_allocation_architecture"
        assert catalog_entry["file"] == f"governance/decisions/{DECISION_PATH.name}"

    def test_the_catalog_has_no_duplicate_identifier(self):
        catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))["decisions"]
        ids = [d["decision_id"] for d in catalog]
        assert len(ids) == len(set(ids))

    def test_the_register_gate_exists_and_is_not_marked_complete(self, gate):
        """A filing may not mark its own unmerged work complete -- a MAJOR finding on
        ``TIER-0001`` for exactly this shape."""
        assert gate["status"] == "in_progress"
        assert gate["status"] != "complete"

    def test_the_register_gate_records_the_bounded_scope(self, gate):
        text = " ".join(str(v) for v in gate.values()).lower()
        assert "reauthoriz" in text
        assert "exactly one" in text

    def test_the_workstream_keeps_its_own_status_and_priority(self, ws0014):
        """Read from the live register, not assumed: this filing must not silently promote
        WS-0014's own status or priority under cover of a gate addition."""
        assert ws0014["status"] == "proposed"
        assert ws0014["priority"] == "secondary"

    def test_at_most_one_workstream_carries_primary_priority(self, register):
        """`OPS-0001`'s priority rule. Checked here because this filing touches the register
        and must not disturb it."""
        primary = [w["id"] for w in register["workstreams"] if w.get("priority") == "primary"]
        assert len(primary) <= 1, primary

    def test_the_shared_live_fields_advanced_to_this_units_verified_state(self, ws0014):
        """`active_branch`, `active_pr` and `last_verified_main_sha` are WS-0014's SINGLE
        SHARED live fields. PR #345 has merged at `2f8cdebe`, so they lawfully advance under
        `OPS-0001`'s Active-GitHub-fields rule."""
        assert ws0014["last_verified_main_sha"] == PR345_MERGE_SHA
        assert ws0014["last_verified_main_sha"] != PR345_BASE_SHA
        # Exact, set from the real number GitHub issued and verified against the live pull
        # request after opening -- never guessed, and never relaxed to a range.
        assert ws0014["active_pr"] == THIS_PULL_REQUEST
        assert ws0014["active_pr"] != 345
        assert ws0014["active_branch"] != "claude/xasset-0045-filing-9yxavw"

    def test_the_gate_records_this_units_own_pull_request(self, gate):
        assert gate["pr"] == THIS_PULL_REQUEST


# ======================================================================================
# 15 -- No section is vacuous, and every identity is a KNOWN identity
# ======================================================================================


KNOWN_40_HEX = frozenset(
    {
        PR345_BASE_SHA,
        PR345_ACCEPTED_HEAD,
        PR345_MERGE_SHA,
        PR345_MERGE_TREE,
        PR345_CORRECTION_OLD_BLOB,
        PR345_CORRECTION_NEW_BLOB,
        "0709d2f05ab031ecb6f69c40465ed4a227983aed",
        "9c2821ab9e0e0dff09f5a03da5a6034775b00750",
    }
)

KNOWN_LONG_DIGITS = frozenset(
    {
        XASSET0045_FAILED_CI_RUN,
        XASSET0045_FAILED_CI_JOB,
        XASSET0044_FAILED_CI_RUN,
        XASSET0044_FAILED_CI_JOB,
        PR345_FINAL_CLEAN_REVIEW,
        PR345_FIRST_FULL_REVIEW,
        PR345_DELTA_REVIEW,
        PR345_PRINCIPAL_ACCEPTANCE,
        PR345_POST_MERGE_VERIFICATION,
        PR345_AUDITABLE_STOP,
    }
)


class TestNoSectionIsVacuous:
    def test_every_lettered_section_exists_and_has_substance(self, decision_text):
        headings = re.findall(r"^### ([A-N])\. (.+)$", decision_text, flags=re.MULTILINE)
        letters = [h[0] for h in headings]
        assert letters == list("ABCDEFGHIJKLMN"), letters
        for letter, _title in headings:
            body = decision_text.split(f"### {letter}. ", 1)[1]
            body = re.split(r"\n### [A-N]\. |\n## ", body, maxsplit=1)[0]
            assert len(body.split()) > 25, f"section {letter} is too thin"

    def test_the_alternatives_section_records_real_rejections(self, decision_text):
        section = decision_text.split("## Alternatives Considered", 1)[1]
        section = section.split("## Consequences", 1)[0]
        assert section.lower().count("rejected") >= 6

    def test_no_unknown_40_hex_identity_appears(self, decision_text):
        found = set(re.findall(r"\b[0-9a-f]{40}\b", decision_text))
        assert found - KNOWN_40_HEX == set(), found - KNOWN_40_HEX

    def test_every_known_40_hex_identity_is_actually_used(self, decision_text):
        found = set(re.findall(r"\b[0-9a-f]{40}\b", decision_text))
        assert KNOWN_40_HEX - found == set(), KNOWN_40_HEX - found

    def test_no_unknown_long_digit_identity_appears(self, decision_text):
        found = set(re.findall(r"\b[0-9]{9,11}\b", decision_text))
        assert found - KNOWN_LONG_DIGITS == set(), found - KNOWN_LONG_DIGITS

    def test_every_known_long_digit_identity_is_actually_used(self, decision_text):
        found = set(re.findall(r"\b[0-9]{9,11}\b", decision_text))
        assert KNOWN_LONG_DIGITS - found == set(), KNOWN_LONG_DIGITS - found

    def test_the_only_64_hex_token_is_the_universe_hash(self, decision_text):
        found = set(re.findall(r"\b[0-9a-f]{64}\b", decision_text))
        assert found == {UNIVERSE_AGGREGATE_HASH}, found

    def test_this_suite_contains_no_vacuous_assertion(self):
        """No ``assert ... or True``-style disjunct, and no bare truthy constant, may hide a
        false premise anywhere in this file. Checked over the parsed AST, not by substring
        scan -- a text search would flag the very comments that explain the rule."""
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        asserts = [n for n in ast.walk(tree) if isinstance(n, ast.Assert)]
        assert len(asserts) > 80, len(asserts)
        for node in asserts:
            test = node.test
            if isinstance(test, ast.Constant):
                pytest.fail(f"bare constant assertion at line {node.lineno}")
            if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.Or):
                for value in test.values:
                    if isinstance(value, ast.Constant) and bool(value.value):
                        pytest.fail(f"constant-truthy disjunct at line {node.lineno}")


# ======================================================================================
# 16 -- This suite's own historical proofs read no moving reference either
#
# The defect this decision exists for was born in a supporting artifact. This suite is a
# supporting artifact. The same rule therefore binds it, mechanically, not by intention.
# ======================================================================================


#: Functions here whose subject is immutable history.
HISTORICAL_PROOF_FUNCTIONS = frozenset({
    "test_the_merge_identity_is_proven_from_the_object_store",
    "test_no_protected_path_was_touched_over_pr345s_closed_range",
    "test_the_blob_identities_are_real",
})

MOVING_REFERENCE_LITERALS = frozenset({
    "HEAD", "origin/main", "origin/HEAD", "@{u}", "@{upstream}", "main",
    "refs/remotes/origin/main",
})


def historical_proof_moving_ref_offenders(
    source: str,
    proof_names: frozenset[str] = HISTORICAL_PROOF_FUNCTIONS,
    moving: frozenset[str] = MOVING_REFERENCE_LITERALS,
) -> list[str]:
    """Functions in ``source`` whose subject is immutable history yet which consult a moving
    reference. Shared and module-level so that disabling it fails its own falsifiability
    test rather than silently reporting clean."""
    offenders: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.FunctionDef) or node.name not in proof_names:
            continue
        for const in ast.walk(node):
            if isinstance(const, ast.Constant) and const.value in moving:
                offenders.append(f"{node.name}:{const.lineno} consults {const.value!r}")
    return offenders


def test_this_suites_historical_proofs_consult_no_moving_reference():
    assert historical_proof_moving_ref_offenders(
        SUITE_PATH.read_text(encoding="utf-8")
    ) == []


def test_the_moving_reference_detector_actually_detects():
    """Falsifiability proof, run through the REAL detector against synthetic source."""
    names = frozenset({"test_historical"})
    bad = (
        "def test_historical():\n"
        "    changed = _git('diff', '--name-only', 'origin/main')\n"
        "    assert changed\n"
    )
    bad_head = (
        "def test_historical():\n"
        "    assert _git('rev-parse', 'HEAD') == PR345_MERGE_SHA\n"
    )
    good = (
        "def test_historical():\n"
        "    assert _git('rev-parse', PR345_MERGE_SHA) == PR345_MERGE_SHA\n"
    )
    out_of_scope = (
        "def test_live():\n"
        "    assert _git('diff', '--name-only', 'origin/main') == ''\n"
    )
    assert historical_proof_moving_ref_offenders(bad, names) != []
    assert historical_proof_moving_ref_offenders(bad_head, names) != []
    assert historical_proof_moving_ref_offenders(good, names) == []
    assert historical_proof_moving_ref_offenders(out_of_scope, names) == []
    # And it genuinely parsed this suite's own real source, rather than something empty.
    parsed = {
        n.name for n in ast.walk(ast.parse(SUITE_PATH.read_text(encoding="utf-8")))
        if isinstance(n, ast.FunctionDef)
    }
    assert HISTORICAL_PROOF_FUNCTIONS <= parsed, HISTORICAL_PROOF_FUNCTIONS - parsed


def test_the_declared_proof_set_is_not_empty():
    """Coverage pin: emptying the set leaves the detector inspecting nothing."""
    assert len(HISTORICAL_PROOF_FUNCTIONS) >= 3
    assert "origin/main" in MOVING_REFERENCE_LITERALS
