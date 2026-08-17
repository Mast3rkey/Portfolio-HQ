"""Adversarial tests pinning the ``XASSET-0036`` §G.B executable-package authorization.

``XASSET-0035`` closed the last semantic blocker and left ``XASSET-0030`` §G.B **semantically
unlocked**. A read-only implementation preflight then found §G.B **unlocked but not authorized**:
six consecutive filings named it and six expressly declined to grant it. ``XASSET-0036`` closes that
gap and nothing else.

The whole risk of an authorization filing is that it grants more than it says, or that a future
implementing session reads more out of it than it contains. Every test below therefore pins **an
authorized boundary and its nearest plausible overreach** — the stronger permission a successor might
infer from the same text, which the decision must refuse.

The four overreaches that matter most each have a dedicated guard:

1. **"Unlocked" read as "authorized."** ``TestUnlockedIsNotAuthorized`` fails if the decision ever
   treats ``XASSET-0035``'s unlock as self-executing permission, or drops the six predecessor
   disclaimers that make the gap real.
2. **Scope creep from implementation into execution.** ``TestExecutionNotAuthorized`` and
   ``TestNoRealResultArtifact`` fail if the grant reaches attestation, arming, claiming, ``ATTEMPT_1``,
   any construction run, or any real results document.
3. **Silent consumption of the reserved results PR.** ``TestP1ResultsPRRemainsSeparate`` fails if
   ``XASSET-0027`` §P.1's exactly-one evaluation/results PR is merged into, replaced by, or counted
   against this authorization.
4. **Reopening the activation regress.** ``TestXasset0029NoRegressIntact`` fails if the filing presents
   itself as an activation PR, or weakens §E's runtime-operator-act rule.

They also pin the negative space that makes the filing honest: this authorization PR itself changes no
canonical file, no validator, no authorization module, and no load-bearing byte; the frozen universe and
both pins are untouched; and Stage 1 is still ``UNARMED`` with ``ATTEMPT_1`` unclaimed.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any construction.**
No results document, lane directory, attestation, claim, completion, or ledger entry is created or read
for authorization purposes. No ``risk_lane_boundary`` protected result path is read, listed, opened, or
referenced.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest
import yaml

import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
GOV = ROOT / "governance/decisions"
PREREG = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"
PROTOCOL = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"

D0027 = GOV / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
D0029 = GOV / "XASSET-0029-endpoint-0001-stage-1-operational-authorization.md"
D0030 = GOV / "XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md"
D0031 = GOV / "XASSET-0031-endpoint-0001-stage-1-g3-share-of-the-whole-semantic-determination.md"
D0034 = GOV / "XASSET-0034-endpoint-0001-stage-1-semantic-closure-and-execution-feasibility-determination.md"
D0035 = GOV / "XASSET-0035-endpoint-0001-stage-1-residual-semantic-blocker-determination.md"
D0036 = GOV / "XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md"

PROTOCOL_SHA256 = "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
PREREG_SHA256 = "6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c"
FROZEN_UNIVERSE_SHA256 = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"

#: The six load-bearing paths ``XASSET-0029`` bound. ``XASSET-0030`` §D records that **no** Stage-1
#: runner or result-production path is among them, which is why §G.B step 5 exists.
EXPECTED_LOAD_BEARING = (
    "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
    "level1_construction_universe_closure_validator.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_stage1_execution_authorization.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
)


def _norm(text: str) -> str:
    """Collapse whitespace and blockquote markers so a phrase match survives hard wrapping.

    These decisions are hard-wrapped at ~100 columns and state operative rules inside Markdown
    blockquotes, so an exact quoted phrase is routinely split across a newline with a ``>``
    continuation marker landing mid-phrase. Both are normalised away so each assertion below is a
    genuine requirement that the phrase be *present*, not a hostage to the wrap column.
    """
    without_quote_markers = re.sub(r"^\s*>\s?", " ", text, flags=re.MULTILINE)
    return re.sub(r"\s+", " ", without_quote_markers)


def _section(text: str, letter: str) -> str:
    """Return one top-level ``### <letter>.`` section body.

    Anchored at line start with exactly three hashes: a naive ``split("### E.")`` also matches inside
    a ``#### E.1`` sub-heading and would silently return a near-empty fragment, making any ``in``
    assertion over it vacuous. The length floor makes that failure loud instead.
    """
    match = re.search(
        rf"^### {re.escape(letter)}\..*?(?=^### [A-Z]\.|^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match is not None, f"XASSET-0036 section {letter} not found"
    body = match.group(0)
    assert len(body) > 200, f"section {letter} extracted suspiciously short ({len(body)} chars)"
    return body


def _suite_ast_excluding_hygiene() -> ast.Module:
    """This module's AST with ``TestSuiteHygiene`` removed.

    The hygiene class is the guard; it must scan everything *else*. Without this exclusion the
    guards below would trip on their own forbidden-pattern literals — a self-reference, not a
    genuine finding. Removal is asserted rather than assumed so the exclusion can never silently
    become a no-op that scans nothing.
    """
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    before = len(tree.body)
    tree.body = [
        node
        for node in tree.body
        if not (isinstance(node, ast.ClassDef) and node.name == "TestSuiteHygiene")
    ]
    assert len(tree.body) == before - 1, "TestSuiteHygiene not found; the guard exclusion is stale"
    assert tree.body, "excluding the hygiene class emptied the module; the scan would be vacuous"
    return tree


@pytest.fixture(scope="module")
def decision() -> str:
    return D0036.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def norm(decision: str) -> str:
    return _norm(decision)


# --------------------------------------------------------------------------------------------------
# 1. "Unlocked" is not "authorized"
# --------------------------------------------------------------------------------------------------


class TestUnlockedIsNotAuthorized:
    def test_decision_states_the_distinction_in_operative_text(self, norm: str) -> None:
        assert "Unlocked is not authorized" in norm

    def test_both_halves_are_required_and_neither_substitutes(self, norm: str) -> None:
        assert "Both are required" in norm
        assert "neither substitutes for the other" in norm

    def test_gap_section_names_every_predecessor_disclaimer(self, decision: str) -> None:
        """The gap is real only because six filings each declined. Dropping any weakens the case."""
        body = _section(decision, "B")
        for predecessor in (
            "XASSET-0030",
            "XASSET-0031",
            "XASSET-0032",
            "XASSET-0033",
            "XASSET-0034",
            "XASSET-0035",
        ):
            assert predecessor in body, f"{predecessor}'s disclaimer missing from the gap reproduction"

    def test_predecessor_disclaimers_are_quoted_not_merely_cited(self, decision: str) -> None:
        body = _norm(_section(decision, "B"))
        assert "authorizes none of G.A or G.B" in body
        assert "No part of §G.A or §G.B is authorized by this decision" in body
        assert "authorizes none of §G.B and performs no part of it" in body

    def test_predecessor_disclaimers_are_actually_present_in_those_files(self) -> None:
        """Guards against the gap being asserted from prose rather than read from committed bytes."""
        assert "authorizes none of G.A or G.B" in _norm(D0030.read_text(encoding="utf-8"))
        assert "No part of §G.A or §G.B is authorized by this decision" in _norm(
            D0031.read_text(encoding="utf-8")
        )
        assert "authorizes none of it and performs none of it" in _norm(
            D0034.read_text(encoding="utf-8")
        )
        assert "authorizes none of §G.B and performs no part of it" in _norm(
            D0035.read_text(encoding="utf-8")
        )

    def test_overreach_unlock_is_never_called_self_executing(self, norm: str) -> None:
        for overreach in (
            "unlocked therefore authorized",
            "unlock is authorization",
            "unlocking authorizes",
        ):
            assert overreach not in norm.lower()


# --------------------------------------------------------------------------------------------------
# 2. Implementation cannot begin before XASSET-0036's own lifecycle closes
# --------------------------------------------------------------------------------------------------


class TestEffectivityRequiresCompleteLifecycleClosure:
    def test_all_seven_conditions_are_stated(self, decision: str) -> None:
        body = _norm(_section(decision, "H"))
        for condition in (
            "independent **FULL** exact-head review",
            "bounded correction and exact-head re-review",
            "principal exact-head acceptance",
            "normal merge",
            "immediate post-merge verification",
            "final post-CI verification and lifecycle closure",
        ):
            assert condition in body, f"effectivity condition missing: {condition!r}"

    def test_merge_commit_ci_condition_names_the_exact_merge_sha(self, decision: str) -> None:
        """The exact omission XASSET-0035's own MINOR finding corrected. It must not recur."""
        body = _norm(_section(decision, "H"))
        assert "successful merge-commit CI whose `head_sha` is the exact merge SHA" in body

    def test_pr_head_ci_is_expressly_excluded(self, decision: str) -> None:
        body = _norm(_section(decision, "H"))
        assert "not the PR head's own CI run" in body
        assert "not a run against any other commit" in body

    def test_no_single_step_is_sufficient(self, decision: str) -> None:
        body = _norm(_section(decision, "H"))
        assert "None is individually sufficient" in body
        assert "Only complete closure of all seven does" in body

    def test_each_named_insufficient_step_is_enumerated(self, decision: str) -> None:
        body = _norm(_section(decision, "H"))
        for insufficient in (
            "Opening this PR does not authorize",
            "a green PR-head CI run does not",
            "principal acceptance does not",
            "merge does not",
            "post-merge verification without a successful exact merge-commit CI run does not",
        ):
            assert insufficient in body, f"insufficiency clause missing: {insufficient!r}"

    def test_effectivity_is_restated_in_consequences(self, norm: str) -> None:
        assert "the §G.B implementation PR is **not** authorized to begin" in norm

    def test_required_lifecycle_gates_is_cited_and_module_unchanged(self, decision: str) -> None:
        body = _norm(_section(decision, "H"))
        assert "REQUIRED_LIFECYCLE_GATES" in body
        assert "cited only and remains byte-unchanged" in body

    def test_the_cited_tuple_actually_has_those_six_members(self) -> None:
        """Cited authority must be real, not asserted."""
        assert A.REQUIRED_LIFECYCLE_GATES == (
            "INDEPENDENT_FULL_EXACT_HEAD_REVIEW",
            "PRINCIPAL_EXACT_HEAD_ACCEPTANCE",
            "MERGE",
            "POST_MERGE_VERIFICATION",
            "MERGE_COMMIT_CI_SUCCESS",
            "MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION",
        )


# --------------------------------------------------------------------------------------------------
# 3. One authorization → one coherent implementation PR, covering steps 2–7 only
# --------------------------------------------------------------------------------------------------


class TestOneCoherentImplementationPR:
    def test_exactly_one_future_pr_is_authorized(self, decision: str) -> None:
        body = _norm(_section(decision, "A"))
        assert "Exactly one future, separate, bounded" in body
        assert "implementation PR is authorized" in body

    def test_grant_is_bounded_to_steps_2_through_7(self, decision: str) -> None:
        body = _norm(_section(decision, "A"))
        assert "steps 2 through 7" in body

    def test_steps_8_through_11_are_expressly_withheld(self, decision: str) -> None:
        body = _norm(_section(decision, "A"))
        assert "steps 8 through 11" in body
        assert "are NOT authorized here" in body

    def test_packaging_forbids_per_component_authorization(self, decision: str) -> None:
        body = _norm(_section(decision, "G"))
        assert "Not** a separate authorization or a separate PR per component" in body

    def test_packaging_requires_stop_and_disclose_rather_than_silent_split(
        self, decision: str
    ) -> None:
        body = _norm(_section(decision, "G"))
        assert "stop and disclose" in body
        assert "silently splitting the package" in body

    def test_coherent_pass_ordering_is_stated(self, decision: str) -> None:
        body = _norm(_section(decision, "G"))
        for stage in (
            "canonical reconciliation",
            "enforcement correction",
            "trust-boundary extension",
            "final identities and pins",
        ):
            assert stage in body, f"packaging ordering missing: {stage!r}"


# --------------------------------------------------------------------------------------------------
# 4. XASSET-0027 §P.1's results PR remains separate and unconsumed
# --------------------------------------------------------------------------------------------------


class TestP1ResultsPRRemainsSeparate:
    def test_this_creates_a_pre_execution_implementation_pr(self, decision: str) -> None:
        body = _norm(_section(decision, "C"))
        assert "pre-execution implementation PR" in body

    def test_p1_budget_is_expressly_not_consumed(self, decision: str) -> None:
        body = _norm(_section(decision, "C"))
        assert "does not consume, replace, amend, or count against" in body

    def test_p1_remains_reserved_and_unspent(self, decision: str) -> None:
        body = _norm(_section(decision, "C"))
        assert "remains separately reserved" in body
        assert "one, unspent" in body

    def test_gap_reproduction_gives_three_independent_grounds(self, decision: str) -> None:
        body = _norm(_section(decision, "B"))
        assert "any one sufficient" in body
        assert "The prohibition is dispositive" in body
        assert "The deliverable is an output, not an implementation" in body
        assert "They sit on opposite sides of arming" in body

    def test_p1_prohibition_is_quoted_verbatim(self, decision: str) -> None:
        body = _norm(_section(decision, "B"))
        assert "That PR may make no production configuration change" in body

    def test_p1_prohibition_actually_exists_in_xasset_0027(self) -> None:
        """The dispositive ground must be read from committed bytes, not asserted."""
        assert "That PR may make no production configuration change" in _norm(
            D0027.read_text(encoding="utf-8")
        )


# --------------------------------------------------------------------------------------------------
# 5–9. What the implementation PR is affirmatively authorized to do
# --------------------------------------------------------------------------------------------------


class TestAuthorityGranted:
    def test_canonical_reconciliation_is_authorized(self, decision: str) -> None:
        body = _norm(_section(decision, "E"))
        assert "Reconcile" in body
        assert "PROTOCOL_V1.md" in body
        assert "pre_registration.yaml" in body

    def test_enforcement_correction_is_authorized_and_bounded(self, decision: str) -> None:
        body = _norm(_section(decision, "E"))
        assert "`XASSET-0030` §C enforcement-conformance defect" in body
        assert "only such other conformance defects as the final accepted semantics mechanically require" in body

    def test_runner_result_writer_and_result_validator_are_authorized(self, decision: str) -> None:
        body = _norm(_section(decision, "E"))
        for component in ("runner", "result writer/serializer", "dedicated result validator"):
            assert component in body, f"authorized component missing: {component!r}"

    def test_outcome_producing_byte_binding_is_authorized(self, decision: str) -> None:
        body = _norm(_section(decision, "E"))
        assert "bind all outcome-producing executable bytes exactly" in body

    def test_load_bearing_extension_prefers_the_existing_mechanism(self, decision: str) -> None:
        body = _norm(_section(decision, "E"))
        assert "Extend `LOAD_BEARING_RELPATHS`" in body
        assert "exact-byte load-bearing mechanism is preferred" in body
        assert "must be argued in the implementation PR rather than assumed" in body

    def test_final_pin_recomputation_is_authorized_only_after_stabilization(
        self, decision: str
    ) -> None:
        body = _norm(_section(decision, "E"))
        assert "Recompute" in body
        assert "only after** all relevant canonical, enforcement, and outcome-producing bytes have stabilized" in body

    def test_b1_b2_b3_are_implemented_without_reopening(self, decision: str) -> None:
        body = _norm(_section(decision, "E"))
        assert "without reopening, re-deriving, or re-arguing them" in body
        for semantic in ("lawful-satisfiability register", "480 consuming / 200 non-consuming", "UNABLE_TO_DETERMINE"):
            assert semantic in body, f"accepted semantic missing from the grant: {semantic!r}"

    def test_governing_invariant_is_restated_unchanged(self, decision: str) -> None:
        body = _norm(_section(decision, "E"))
        assert (
            "no outcome-producing executable code may be created, changed, or left outside the bound "
            "execution identity after the final rebinding and before `ATTEMPT_1`" in body
        )


# --------------------------------------------------------------------------------------------------
# 10. Operational rebinding is NOT performed, and not authorized, by this filing
# --------------------------------------------------------------------------------------------------


class TestOperationalRebindingNotPerformed:
    def test_rebinding_is_a_distinct_downstream_lifecycle(self, decision: str) -> None:
        body = _norm(_section(decision, "B"))
        assert "The future operational rebinding remains distinct from this implementation authorization" in body

    def test_authorizing_the_package_does_not_authorize_the_rebinding(self, decision: str) -> None:
        body = _norm(_section(decision, "B"))
        assert "Authorizing the package does not authorize the rebinding" in body

    def test_rebinding_appears_in_work_not_created(self, decision: str) -> None:
        body = _norm(_section(decision, "I"))
        assert "Authorizing §G.B step 8's rebinding" in body

    def test_this_filing_performs_no_rebinding(self, norm: str) -> None:
        assert "performs no load-bearing reauthorization or rebinding" in norm


# --------------------------------------------------------------------------------------------------
# 11–12. Attestation / arm / claim / execution and real results are NOT authorized
# --------------------------------------------------------------------------------------------------


class TestExecutionNotAuthorized:
    @pytest.mark.parametrize(
        "withheld",
        [
            "generating any real external attestation",
            "claiming or consuming any part of `ATTEMPT_1`",
            "executing any construction, or evaluating any gate for any construction",
            "any Stage 2 work",
        ],
    )
    def test_withheld_item_is_enumerated(self, decision: str, withheld: str) -> None:
        body = _norm(_section(decision, "F"))
        assert withheld in body, f"withheld item missing: {withheld!r}"

    def test_lane_state_creation_is_withheld(self, decision: str) -> None:
        body = _norm(_section(decision, "F"))
        assert "creating `READY`, `CLAIMED`, or `COMPLETED` lane state" in body
        assert "AUTHORIZATION_ROOT" in body

    def test_the_dry_run_shortcut_is_rejected_by_name(self, decision: str) -> None:
        """The single most likely well-intentioned breach: 'just run it once to check.'"""
        body = _norm(_section(decision, "F"))
        assert "may build and fully validate the runner against **synthetic or isolated inputs**" in body
        assert "may **not** run it over the real 680-construction universe" in body
        assert "consumes the non-rerunnable `ATTEMPT_1` lane's subject matter" in body

    def test_steps_8_through_11_are_in_the_withheld_list(self, decision: str) -> None:
        body = _norm(_section(decision, "F"))
        assert "performing §G.B steps 8–11" in body


class TestNoRealResultArtifact:
    def test_no_real_results_artifact_may_be_produced(self, decision: str) -> None:
        body = _norm(_section(decision, "F"))
        assert "producing a real `stage1_results.yaml`" in body
        assert "per-construction disposition, cell outcome, or roll-up" in body

    def test_the_same_bar_is_restated_in_the_p1_reconciliation(self, decision: str) -> None:
        body = _norm(_section(decision, "C"))
        assert "No real result artifact may be produced by the implementation PR" in body


# --------------------------------------------------------------------------------------------------
# 13. No data acquisition, Stage 2, or portfolio-policy effect
# --------------------------------------------------------------------------------------------------


class TestNoDataAcquisitionOrPortfolioEffect:
    @pytest.mark.parametrize(
        "withheld",
        [
            "acquiring market, fundamental, economic, or Stage-2 data",
            "any Level-2 change",
            "any endpoint, bound, point, range, percentage, weight, rank, target, or allocation",
        ],
    )
    def test_withheld_item_is_enumerated(self, decision: str, withheld: str) -> None:
        body = _norm(_section(decision, "F"))
        assert withheld in body, f"withheld item missing: {withheld!r}"

    def test_production_configuration_is_withheld(self, decision: str) -> None:
        body = _norm(_section(decision, "F"))
        for path in ("targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml"):
            assert path in body, f"protected production path missing from withheld list: {path!r}"

    def test_risk_lane_boundary_reuse_is_withheld(self, decision: str) -> None:
        body = _norm(_section(decision, "F"))
        assert "risk_lane_boundary" in body


# --------------------------------------------------------------------------------------------------
# 14. No §K.1 / §E.1 / B1 / B2 / B3 reopening
# --------------------------------------------------------------------------------------------------


class TestNoSemanticReopening:
    @pytest.mark.parametrize(
        "preserved",
        [
            "resolving `XASSET-0024` §K.1",
            "amending `XASSET-0020` §E.1",
            "reopening, re-deriving, or re-arguing B1, B2, or B3",
        ],
    )
    def test_reopening_is_withheld(self, decision: str, preserved: str) -> None:
        body = _norm(_section(decision, "F"))
        assert preserved in body, f"preservation missing from withheld list: {preserved!r}"

    def test_frozen_identities_are_withheld_from_change(self, decision: str) -> None:
        body = _norm(_section(decision, "F"))
        assert "changing the frozen construction identities, universe, cardinality, or universe hash" in body

    def test_reanalysis_appears_in_work_not_created(self, decision: str) -> None:
        body = _norm(_section(decision, "I"))
        assert "Re-analysis of B1 / B2 / B3" in body


# --------------------------------------------------------------------------------------------------
# 15. XASSET-0029's no-infinite-activation-regress rule remains intact
# --------------------------------------------------------------------------------------------------


class TestXasset0029NoRegressIntact:
    def test_this_is_expressly_not_an_activation_pr(self, decision: str) -> None:
        body = _norm(_section(decision, "D"))
        assert "not** an activation PR" in body
        assert "not** an arming step" in body

    def test_no_regress_rule_is_named_as_intact(self, decision: str) -> None:
        body = _norm(_section(decision, "D"))
        assert "no-infinite-regress rule **remains intact and unweakened**" in body

    def test_final_activation_stays_a_runtime_operator_act(self, decision: str) -> None:
        body = _norm(_section(decision, "D"))
        assert "external one-shot runtime attestation and the operator's act" in body
        assert "not another merged activation PR" in body

    def test_zero_activation_authorizations_are_added(self, decision: str) -> None:
        body = _norm(_section(decision, "D"))
        assert "adds **zero** activation authorizations" in body

    def test_executable_stays_permanently_false(self, decision: str) -> None:
        body = _norm(_section(decision, "D"))
        assert "stays permanently `false`" in body
        assert "no committed value in this repository authorizes Stage-1" in body

    def test_reconciliation_quotes_the_regress_terminating_condition(self, decision: str) -> None:
        body = _norm(_section(decision, "B"))
        assert "The regress terminates because the final step changes no repository state" in body

    def test_that_terminating_condition_actually_exists_in_xasset_0029(self) -> None:
        assert "The regress terminates because the final step changes no" in _norm(
            D0029.read_text(encoding="utf-8")
        )

    def test_amending_xasset_0029_was_considered_and_rejected(self, norm: str) -> None:
        assert "Amend `XASSET-0029` to cover implementation" in norm
        assert "There is no conflict to resolve" in norm


# --------------------------------------------------------------------------------------------------
# 16. This authorization PR changes no canonical, load-bearing, or implementation byte
# --------------------------------------------------------------------------------------------------


class TestThisFilingMutatesNothingLoadBearing:
    def test_canonical_pins_are_unchanged(self) -> None:
        import hashlib

        assert hashlib.sha256(PROTOCOL.read_bytes()).hexdigest() == PROTOCOL_SHA256
        assert hashlib.sha256(PREREG.read_bytes()).hexdigest() == PREREG_SHA256

    def test_load_bearing_relpaths_still_the_same_six(self) -> None:
        assert tuple(sorted(A.LOAD_BEARING_RELPATHS)) == EXPECTED_LOAD_BEARING

    def test_no_runner_or_result_path_is_load_bearing_yet(self) -> None:
        """§G.B step 5 exists precisely because this is still true today."""
        for relative in A.LOAD_BEARING_RELPATHS:
            lowered = relative.lower()
            assert "runner" not in lowered
            assert "result" not in lowered

    def test_frozen_universe_is_unchanged(self) -> None:
        data = yaml.safe_load(PREREG.read_text(encoding="utf-8"))
        closure = data["construction_universe_closure"]
        assert closure["registered_construction_count"] == 680
        assert closure["construction_universe_sha256"] == FROZEN_UNIVERSE_SHA256
        assert data["trial_inventory"]["derived_cells"] == 48

    def test_stage_1_still_not_executable(self) -> None:
        block = yaml.safe_load(PREREG.read_text(encoding="utf-8"))["stage_1_executability"]
        assert block["executable"] is False
        assert block["executable_is_never_the_authorization_source"] is True

    def test_new_execution_still_not_authorized(self) -> None:
        authorized, _reason = A.new_execution_is_authorized()
        assert authorized is False

    def test_authorization_root_absent(self) -> None:
        assert not A.AUTHORIZATION_ROOT.exists()
        assert not A.CLAIM_PATH.exists()
        assert not A.LEDGER_PATH.exists()

    def test_no_endpoint_stage1_runner_or_results_document_exists(self) -> None:
        assert not (ROOT / "stage1_results.yaml").exists()
        assert not (ROOT / "level1_stage1_runner.py").exists()
        assert not (ROOT / "level1_stage1_result_writer.py").exists()
        assert not (ROOT / "level1_stage1_result_validator.py").exists()

    def test_decision_declares_it_mutates_nothing_load_bearing(self, decision: str) -> None:
        body = _norm(_section(decision, "J"))
        assert "corrects no validator, extends no `LOAD_BEARING_RELPATHS`" in body
        assert "amends no canonical file and changes no hash pin" in body

    def test_decision_declares_stage_1_still_unarmed(self, norm: str) -> None:
        assert "Stage 1 remains UNARMED and NOT EXECUTABLE" in norm
        assert "`ATTEMPT_1` is intact, unclaimed, and unconsumed" in norm


# --------------------------------------------------------------------------------------------------
# Suite hygiene — guards that make the assertions above non-vacuous
# --------------------------------------------------------------------------------------------------


class TestSuiteHygiene:
    def test_no_assertion_uses_an_or_fallback(self) -> None:
        """An ``assert a or b`` survives mutation of ``a`` and silently stops testing it.

        ``XASSET-0035``'s own suite found seventeen such assertions passing against a mutated
        decision. This suite carries **zero**: every phrase is matched against the
        whitespace-and-blockquote-normalised text, so no wrap-tolerance fallback is needed.
        """
        or_asserts = [
            node
            for node in ast.walk(_suite_ast_excluding_hygiene())
            if isinstance(node, ast.Assert)
            and isinstance(node.test, ast.BoolOp)
            and isinstance(node.test.op, ast.Or)
        ]
        assert not or_asserts, (
            f"{len(or_asserts)} assertions use an `or` fallback; each weakens its own substantive "
            "clause and must be rewritten conjunctively"
        )

    def test_suite_performs_no_filesystem_write(self) -> None:
        """Detects real write *calls*, not source substrings.

        A substring scan would match the guard's own pattern list, so this walks the AST for
        actual mutating calls instead — which is also the stronger check, since it cannot be
        evaded by aliasing the call through a differently-spelled name.
        """
        forbidden_attrs = {
            "write_text",
            "write_bytes",
            "mkdir",
            "unlink",
            "touch",
            "rmtree",
            "remove",
            "makedirs",
        }
        offenders = [
            node.func.attr
            for node in ast.walk(_suite_ast_excluding_hygiene())
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in forbidden_attrs
        ]
        assert not offenders, f"suite must not mutate the filesystem; found calls: {offenders}"

    def test_suite_never_references_the_protected_risk_result_path(self) -> None:
        """Scans string *constants*, excluding this guard class's own needle."""
        needle = "phq-risk0001-results"
        offenders = [
            node.value
            for node in ast.walk(_suite_ast_excluding_hygiene())
            if isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and needle in node.value
        ]
        assert not offenders, f"suite must not reference the protected RISK result path: {offenders}"

    def test_section_extractor_is_not_vacuous(self, decision: str) -> None:
        """If ``_section`` ever silently returned a fragment, every ``in`` assertion would pass."""
        for letter in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
            body = _section(decision, letter)
            assert len(body) > 200
            assert body.lstrip().startswith(f"### {letter}.")

    def test_decision_file_declares_this_module_as_its_supporting_artifact(
        self, decision: str
    ) -> None:
        assert f"supporting_artifact: {Path(__file__).name}" in decision
