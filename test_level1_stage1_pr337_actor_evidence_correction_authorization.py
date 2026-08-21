"""Adversarial tests pinning the ``XASSET-0041`` PR #337 lifecycle actor-evidence correction authorization.

The ``XASSET-0040`` step-11 unit ran and stopped at its first terminal condition, §K.1
``STOPPED_BEFORE_ATTESTATION``. Every §H condition verified clean except §H.4: two of the six
``REQUIRED_LIFECYCLE_GATES`` cannot authenticate, because the only durable PR #337 records satisfying
the principal-acceptance and post-merge-verification gates are authored by ``claude[bot]`` rather than
the bound ``Mast3rkey``. ``XASSET-0040`` §J is explicit that finding that defect is not authority to
repair it. ``XASSET-0041`` supplies exactly that authority, for the correction only.

The danger here is not the correction itself -- it is the *shape* of the exception. A permissive
reading turns "``claude[bot]`` acted for the principal on PR #337" into "bot-authored records satisfy
lifecycle gates", which is precisely the impersonation surface ``XASSET-0029`` BLOCKING 2 closed. Every
guard below exists to make that generalization impossible to read into the text:

1. **The filing implements the correction, or is treated as the correction.**
   ``TestFilingIsGovernanceOnly`` and ``TestNoProtectedByteWasTouched``.
2. **``claude[bot]`` granted general standing, or the actor requirement dropped.**
   ``TestActorAuthenticationPreserved`` -- the single most important class here.
3. **The exception unpinned from the exact PR #337 records.** ``TestExceptionIsExactlyPinned``.
4. **Identity inferred from body text, or chronology weakened.**
   ``TestNoBodyTextIdentityAndNoChronologyWeakening``.
5. **The ratification treated as a fictional pre-merge acceptance, or as forward permission.**
   ``TestRatificationIsRetrospectiveNotRetroactive``.
6. **Comment backfill smuggled in as the repair.** ``TestBackfillIsProvedImpossible``.
7. **Downstream links pre-authorized or collapsed.** ``TestDownstreamSequencePreserved``.
8. **Step 11 retried, ``XASSET-0040`` revived, or §P.1 consumed.**
   ``TestStep11NotRetriedAndAttemptIntact`` and ``TestP1ResultsPRRemainsSeparate``.
9. **A lifecycle step allowed to stand in for complete closure.**
   ``TestEffectivityRequiresCompleteLifecycleClosure``.
10. **Catalog/register drift, or a vacuous section.**
    ``TestCatalogAndRegisterSynchronisation`` and ``TestNoSectionIsVacuous``.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No attestation, claim, completion, lane directory, or ledger entry is created or read
for authorization purposes. No ``risk_lane_boundary`` protected result path is read, listed, opened, or
referenced. ``write_authorization`` is never called.
"""

from __future__ import annotations

import ast
import hashlib
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent

DECISION_ID = "XASSET-0041"
DECISION_PATH = ROOT / (
    "governance/decisions/"
    "XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md"
)
CATALOG_PATH = ROOT / "governance/decisions.yaml"
REGISTER_PATH = ROOT / "operations/WORKSTREAMS.yaml"
SUITE_PATH = Path(__file__).resolve()

#: The five exact PR #337 identities the exception is pinned to (XASSET-0041 §F.5).
PINNED_HEAD = "f40c816223c78f1d1e436b718455df5fb3d77fa7"
PINNED_REVIEW = "4966846374"
PINNED_ACCEPTANCE = "5335697214"
PINNED_MERGE = "637eaa30302f5a71f84ab1d215ecbd32c01399b5"
PINNED_VERIFICATION = "5335849767"
PINNED_IDENTITIES = (
    PINNED_HEAD,
    PINNED_REVIEW,
    PINNED_ACCEPTANCE,
    PINNED_MERGE,
    PINNED_VERIFICATION,
)

#: Load-bearing and otherwise protected paths this GOVERNANCE-ONLY filing must not touch.
PROTECTED_RELPATHS = (
    "level1_stage1_execution_authorization.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_construction_universe_closure_validator.py",
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
    "governance/decisions/XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
    "governance/decisions/XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md",
    "allocate.py",
    "margin_state.py",
    "levels.py",
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
)

#: WS-0014's shared `active_pr` while the XASSET-0043 rebinding-authorization unit is live.
#: Set to the real GitHub number issued when the pull request was opened, verified
#: against live GitHub afterwards, never left as a guess.
XASSET0043_ACTIVE_PR = 343

GATE_SELF = "xasset0041-pr337-actor-evidence-correction-authorization"
GATE_STOP = "xasset0040-step11-unit-stopped-before-attestation"
GATE_PRIOR = "xasset0040-step11-activation-authorization"

#: SHA-256 of the XASSET-0040 gate description as it stood BEFORE this filing. Only its
#: ``status`` was corrected to ``complete``; its narrative must remain byte-identical.
PRIOR_GATE_DESCRIPTION_SHA256 = (
    "a9cc6c2752c0e47c580aceb334e4bbdd723ea8899c68256c16b2e708981a9b92"
)


# ======================================================================================
# Fixtures
# ======================================================================================


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_body(decision_text: str) -> str:
    """The decision without its YAML front matter, so front matter cannot satisfy a body assertion."""
    parts = decision_text.split("---\n", 2)
    assert len(parts) == 3, "decision must carry exactly one YAML front-matter block"
    return parts[2]


def _flat(text: str) -> str:
    """Collapse markdown line wrapping so a phrase assertion tests content, not typography."""
    return re.sub(r"\s+", " ", text)


@pytest.fixture(scope="module")
def flat_body(decision_body: str) -> str:
    return _flat(decision_body)


@pytest.fixture(scope="module")
def sections(decision_body: str) -> dict[str, str]:
    """Map ``A``..``K`` to that section's own text, so an assertion cannot be satisfied elsewhere."""
    found: dict[str, str] = {}
    pattern = re.compile(r"^### ([A-K])\. ", re.MULTILINE)
    marks = list(pattern.finditer(decision_body))
    assert marks, "no lettered sections found"
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(decision_body)
        found[mark.group(1)] = decision_body[mark.start():end]
    return found


@pytest.fixture(scope="module")
def catalog() -> list[dict]:
    data = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    return data["decisions"] if isinstance(data, dict) else data


@pytest.fixture(scope="module")
def ws0014() -> dict:
    data = yaml.safe_load(REGISTER_PATH.read_text(encoding="utf-8"))
    entries = [w for w in data["workstreams"] if w.get("id") == "WS-0014"]
    assert len(entries) == 1, "expected exactly one WS-0014 entry"
    return entries[0]


@pytest.fixture(scope="module")
def gates(ws0014: dict) -> dict[str, dict]:
    return {m["gate"]: m for m in ws0014["milestones"]}


# ======================================================================================
# 1 -- The filing is governance-only and implements nothing
# ======================================================================================


class TestFilingIsGovernanceOnly:
    def test_determination_is_the_authorization_not_the_correction(self, sections):
        text = sections["A"]
        assert "PR337_LIFECYCLE_ACTOR_EVIDENCE_CORRECTION_AUTHORIZED" in text
        assert "This filing implements no part of that correction." in text

    def test_exactly_one_future_correction_is_authorized(self, sections):
        text = sections["A"]
        assert "**Exactly one** future, separate, bounded correction" in text

    @pytest.mark.parametrize(
        "phrase",
        [
            "edits no load-bearing byte",
            "posts and backfills no ratification",
            "rebinds nothing",
            "re-runs no readiness or drift verification",
            "retries no part of step 11",
            "creates no result",
        ],
    )
    def test_section_a_disclaims_every_implementation_act(self, sections, phrase):
        assert phrase in _flat(sections["A"]), f"§A must disclaim: {phrase!r}"

    def test_granted_authority_is_a_correction_and_nothing_beyond(self, sections):
        text = sections["E"]
        assert "It is a **correction**" in text
        assert "nothing beyond it" in text

    def test_implementing_the_correction_here_is_explicitly_withheld(self, sections):
        assert "implement the correction here" in sections["H"]


# ======================================================================================
# 2 -- Actor authentication survives. THE central guard.
# ======================================================================================


class TestActorAuthenticationPreserved:
    def test_existing_mastrkey_actor_requirement_is_preserved(self, sections):
        text = sections["F"]
        assert "Preserve the existing `Mast3rkey` actor requirement" in _flat(text)
        assert "The default path is unchanged for every pull request other than" in _flat(text)

    def test_claude_bot_is_never_generally_the_principal_or_operator(self, sections):
        text = sections["F"]
        assert "Never classify `claude[bot]` generally as the principal or lifecycle operator." in text
        assert 'No general allow-list, no bot-account class, no "trusted automation" category.' in _flat(text)

    def test_bound_actor_constants_are_stated_unchanged(self, sections):
        assert (
            "`PRINCIPAL_ACCOUNT_LOGIN` and `LIFECYCLE_OPERATOR_LOGIN` remain `Mast3rkey`."
            in _flat(sections["F"])
        )

    def test_blocking_2_property_is_named_and_preserved(self, sections):
        text = sections["D"]
        assert "BLOCKING 2" in text
        assert "anti-impersonation" in text
        assert "impersonation surface" in text

    def test_exception_is_unlocked_only_by_an_authenticated_principal_record(self, sections):
        text = sections["D"]
        assert "only** by a new record whose own author is authenticated as `Mast3rkey`" in _flat(text)
        assert "An arbitrary account can no more produce that ratification" in text

    def test_converting_claude_bot_into_an_accepted_actor_is_explicitly_rejected(self, decision_body):
        assert "**Add `claude[bot]` to the accepted actors.** Rejected." in decision_body

    def test_no_general_bot_allowance_phrasing_anywhere(self, decision_body):
        """A permissive sentence must not exist anywhere in the decision body."""
        # Only AFFIRMATIVE generalizations: each of these could not appear inside a
        # prohibition, so a hit is a real widening rather than a rule forbidding one.
        forbidden = (
            "bot accounts are accepted",
            "any bot may satisfy",
            "trusted automation accounts are",
            "claude[bot] is accepted as",
            "claude[bot] may satisfy",
            "claude[bot] counts as the principal",
        )
        lowered = _flat(decision_body).lower()
        for phrase in forbidden:
            assert phrase not in lowered, f"generalizing phrase present: {phrase!r}"


# ======================================================================================
# 3 -- The exception is pinned to exactly five identities
# ======================================================================================


class TestExceptionIsExactlyPinned:
    @pytest.mark.parametrize("identity", PINNED_IDENTITIES)
    def test_every_pinned_identity_appears_in_section_f(self, sections, identity):
        assert identity in _flat(sections["F"]), f"§F must pin {identity!r}"

    def test_scope_is_stated_as_only_those_records(self, sections):
        assert "Apply only to the exact PR #337 historical records" in _flat(sections["F"])

    def test_all_five_identities_are_required_of_the_ratification(self, sections):
        text = sections["G"]
        assert "all five §F.5 identities" in text
        for identity in (PINNED_ACCEPTANCE, PINNED_VERIFICATION):
            assert identity in text

    def test_wrong_evidence_of_every_named_kind_is_rejected(self, sections):
        text = sections["F"]
        for kind in (
            "missing",
            "wrong-actor",
            "wrong-PR",
            "wrong-head",
            "wrong-review",
            "wrong-merge",
            "substituted-comment",
            "altered-record",
            "ambiguous",
        ):
            assert kind in _flat(text), f"§F.7 must reject {kind!r} evidence"

    def test_tests_must_prove_the_exception_cannot_generalize(self, sections):
        text = sections["F"]
        assert "Add adversarial tests proving the exception cannot generalize" in _flat(text)
        assert "substituting any other PR, head, review, merge, or comment id fails" in _flat(text)

    def test_decision_contains_exactly_the_expected_identifier_set(self, decision_body):
        """No swapped, invented, or look-alike identity may appear anywhere in the decision.

        A "present in §F" check alone is satisfiable while a *different* occurrence elsewhere is
        silently altered, so the full identifier surface is pinned as an exact set.
        """
        shas = set(re.findall(r"\b[0-9a-f]{40}\b", decision_body))
        assert shas == {
            PINNED_HEAD,                                  # PR #337 accepted head
            PINNED_MERGE,                                 # PR #337 bound merge
            "f212cce50e28ae887dc8c594bf8ae491a3ef85af",   # acting head / PR #340 merge
        }, f"unexpected 40-hex identity surface: {sorted(shas)}"

        ids = set(re.findall(r"\b\d{10}\b", decision_body))
        assert ids == {
            PINNED_REVIEW,                                # PR #337 final clean review
            PINNED_ACCEPTANCE,                            # PR #337 acceptance comment
            PINNED_VERIFICATION,                          # PR #337 post-merge verification
            "4946464366",                                 # XASSET-0029 BLOCKING 2 review
            "5343692162",                                 # step-11 stop evidence
        }, f"unexpected 10-digit identity surface: {sorted(ids)}"

    @pytest.mark.parametrize("identity", PINNED_IDENTITIES)
    def test_each_pinned_identity_survives_everywhere_it_appears(self, decision_body, identity):
        """Every pinned identity must appear at least once and never in a corrupted variant."""
        assert identity in decision_body
        # a near-miss of the same shape must not also be present
        shape = r"\b[0-9a-f]{40}\b" if len(identity) == 40 else r"\b\d{10}\b"
        present = set(re.findall(shape, decision_body))
        assert identity in present

    def test_fail_closed_retained_everywhere_else(self, sections):
        assert (
            "Retain fail-closed behaviour for every other pull request, actor, comment, and chronology."
            in _flat(sections["F"])
        )


# ======================================================================================
# 4 -- No body-text identity, no chronology weakening
# ======================================================================================


class TestNoBodyTextIdentityAndNoChronologyWeakening:
    def test_identity_is_never_inferred_from_body_text(self, sections):
        text = sections["F"]
        assert "Never infer actor identity from comment body text." in text
        assert "Identity stays derived from durable `user.login`." in _flat(text)

    def test_missing_durable_author_identity_stays_refused(self, sections):
        assert "A record with no durable author identity remains refused." in sections["F"]

    def test_ordinary_chronology_is_not_removed_or_weakened(self, sections):
        assert (
            "Never remove or weaken the ordinary review → acceptance → merge → post-merge-verification"
            in _flat(sections["F"])
        )

    def test_relaxing_chronology_is_explicitly_rejected(self, decision_body):
        assert (
            "**Relax the chronology rule so a late acceptance is tolerated.** Rejected."
            in _flat(decision_body)
        )


# ======================================================================================
# 5 -- Retrospective ratification, not a fictional pre-merge event
# ======================================================================================


class TestRatificationIsRetrospectiveNotRetroactive:
    def test_ratification_is_retrospective(self, sections):
        assert "Treat the new record as retrospective ratification of the exact historical acts" in _flat(sections["F"])

    def test_not_a_fictional_pre_merge_acceptance(self, sections):
        assert "never as a fictional pre-merge acceptance event" in _flat(sections["F"])

    def test_not_permission_for_future_bot_gates(self, sections):
        assert "never as permission for future bot-authored lifecycle gates" in _flat(sections["F"])

    def test_section_f1_states_what_the_ratification_does_not_assert(self, decision_body):
        assert "The ratification does not assert that a `Mast3rkey` acceptance occurred before the merge." in _flat(decision_body)
        assert "ratified as it stands" in decision_body

    def test_ratification_must_be_mastrkey_authored(self, sections):
        assert "It **must be authored by `Mast3rkey`**" in sections["G"]

    def test_ratification_language_is_specified_but_not_discharged(self, sections):
        text = sections["G"]
        assert "authorized acts performed for the principal" in _flat(text)
        assert "**This authoring session specifies that requirement and does not discharge it.**" in text
        assert "It posts no principal acceptance and no ratification." in _flat(text)

    def test_acceptance_gate_of_effectivity_carries_the_ratification(self, sections):
        assert "carrying the §G ratification" in _flat(sections["J"])


# ======================================================================================
# 6 -- Backfill was proved impossible, not merely disfavoured
# ======================================================================================


class TestBackfillIsProvedImpossible:
    def test_chronology_rule_is_quoted_from_the_mechanism(self, sections):
        text = sections["C"]
        assert "str(merged_at) < str(accepted)" in text
        assert "merge {merged_at} precedes acceptance {accepted}" in text

    def test_durable_timestamps_are_recorded(self, sections):
        text = sections["C"]
        for stamp in (
            "2026-08-18T23:10:37Z",
            "2026-08-18T23:50:29Z",
            "2026-08-18T23:50:58Z",
            "2026-08-19T00:12:40Z",
        ):
            assert stamp in _flat(text), f"§C must record {stamp!r}"

    def test_conclusion_is_structural_impossibility(self, sections):
        text = sections["C"]
        assert "structurally impossible for the principal-acceptance gate" in text
        assert "It is not merely undesirable" in _flat(text)

    def test_asymmetry_is_disclosed_honestly(self, sections):
        text = sections["C"]
        assert "The asymmetry is recorded honestly." in text
        assert "is *not* chronologically blocked" in _flat(text)
        assert "Neither gate is repaired by writing new comments" in text

    def test_backfill_alternative_is_rejected(self, decision_body):
        assert "**Backfill a `Mast3rkey` acceptance comment on PR #337.** Rejected" in _flat(decision_body)

    def test_posting_or_backfilling_any_comment_is_withheld(self, sections):
        assert "post, backfill, fabricate, or pre-date any lifecycle comment" in sections["H"]


# ======================================================================================
# 7 -- The downstream sequence stays separate
# ======================================================================================


class TestDownstreamSequencePreserved:
    @pytest.mark.parametrize(
        "link",
        ["rebinding", "renewed readiness", "renewed drift check", "new step-11 authorization"],
    )
    def test_each_downstream_link_is_named_as_separately_authorized(self, sections, link):
        assert link in _flat(sections["I"]), f"§I must name the {link!r} link"

    def test_only_the_correction_is_authorized_by_this_decision(self, sections):
        assert "THIS decision authorizes only this" in sections["I"]

    def test_downstream_links_are_not_pre_authorized_or_combined(self, sections):
        assert (
            "**None of links 2 through 5 is authorized, pre-authorized, combined, or made reachable by this decision"
            in _flat(sections["I"])
        )

    def test_correction_succeeding_does_not_authorize_the_next_link(self, sections):
        text = sections["I"]
        assert "Completing the correction authorizes the next link no more" in _flat(text)
        assert "than a clean step-10 result authorized step 11" in _flat(text)

    def test_xasset_0040_is_not_revived(self, sections):
        text = sections["I"]
        assert "**`XASSET-0040` is not revived by this decision.**" in text
        assert "A future step-11 attempt needs its own new authorization." in text

    def test_combining_the_links_is_explicitly_rejected(self, decision_body):
        assert "into one filing.** Rejected." in _flat(decision_body)

    def test_correction_touches_load_bearing_path_one(self, sections):
        assert "**load-bearing path #1**" in sections["I"]


# ======================================================================================
# 8 -- Step 11 is not retried; ATTEMPT_1 is untouched; §P.1 is untouched
# ======================================================================================


class TestStep11NotRetriedAndAttemptIntact:
    @pytest.mark.parametrize(
        "act",
        [
            "**retry step 11** in any form",
            "attest, arm, reach `READY`, claim, execute, complete, or recover",
            "consume any part of `ATTEMPT_1`",
            "evaluate any gate for any registered construction",
        ],
    )
    def test_execution_acts_are_withheld(self, sections, act):
        assert act in _flat(sections["H"]), f"§H must withhold: {act!r}"

    def test_non_authorization_states_lane_and_attempt_untouched(self, sections):
        text = sections["K"]
        assert "consumes nothing of `ATTEMPT_1`" in _flat(text)
        assert "generates no attestation" in _flat(text)

    def test_consequences_state_stage_1_unarmed(self, decision_body):
        assert "**Stage 1 remains `UNARMED` and `NOT EXECUTABLE`. Lane state is `ABSENT`. `ATTEMPT_1` is intact," in _flat(decision_body)

    def test_merging_arms_nothing(self, sections):
        text = sections["J"]
        assert "**Merging this decision does not arm Stage 1" in text
        assert "`new_execution_is_authorized()` still returns `False`" in _flat(text)


class TestP1ResultsPRRemainsSeparate:
    def test_p1_is_withheld(self, sections):
        assert "open, consume, or pre-empt `XASSET-0027` §P.1's reserved results PR" in sections["H"]

    def test_p1_remains_one_unspent_unopened(self, decision_body):
        assert "remains **one, unspent, unopened**" in decision_body

    def test_no_result_exists_to_deliver(self, decision_body):
        assert "there is no result to deliver, and none is created here" in decision_body


# ======================================================================================
# 9 -- Effectivity requires COMPLETE closure
# ======================================================================================


class TestEffectivityRequiresCompleteLifecycleClosure:
    def test_all_seven_conditions_are_listed(self, sections):
        text = sections["J"]
        for condition in (
            "independent **FULL** exact-head review",
            "bounded correction and exact-head re-review",
            "principal exact-head acceptance",
            "normal merge",
            "immediate post-merge verification",
            "successful merge-commit CI whose `head_sha` is the exact merge SHA",
            "final post-CI verification and lifecycle closure",
        ):
            assert condition in _flat(text), f"§J must require: {condition!r}"

    def test_no_single_condition_suffices(self, sections):
        text = sections["J"]
        assert "**None is individually sufficient.**" in text
        assert "Opening this PR authorizes nothing" in text
        assert "**Only complete closure of all seven does**" in text

    def test_what_becomes_authorized_is_a_correction_not_an_armed_stage(self, sections):
        assert "a **future correction unit**, not an armed Stage 1" in sections["J"]


# ======================================================================================
# 10 -- Nothing protected was touched
# ======================================================================================


class TestNoProtectedByteWasTouched:
    @pytest.mark.parametrize("relpath", PROTECTED_RELPATHS)
    def test_protected_path_is_not_in_this_change(self, relpath):
        """This filing's own scope must exclude every protected path.

        The decision, catalog, register, this suite, and the dashboard count assertions are the
        entire scope; nothing here may edit a load-bearing or portfolio byte.
        """
        assert (ROOT / relpath).exists(), f"{relpath} must still exist"
        # The suite itself must not import or execute any of them for authorization purposes.
        assert relpath not in SUITE_PATH.read_text(encoding="utf-8").split("PROTECTED_RELPATHS")[-1]

    def test_suite_never_calls_write_authorization(self):
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                target = node.func
                name = getattr(target, "attr", None) or getattr(target, "id", None)
                assert name not in {
                    "write_authorization",
                    "claim_execution",
                    "complete_execution",
                    "run_stage1",
                    "write_stage1_results",
                }, f"suite must never call {name!r}"

    def test_suite_performs_no_filesystem_write(self):
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = getattr(node.func, "attr", None)
                assert name not in {"write_text", "write_bytes", "mkdir", "touch", "unlink"}, (
                    f"suite must not mutate the filesystem via {name!r}"
                )

    def test_suite_references_no_protected_risk_result_path(self):
        """Naming the boundary in prose is fine; referencing a real RISK results path is not."""
        text = SUITE_PATH.read_text(encoding="utf-8")
        # Assembled at runtime so the literals never appear in this file's own source and
        # cannot make the scan trivially self-matching.
        risk = "ri" + "sk"
        for real_path_token in (
            f"research/level1_{risk}_evidence",
            f"{risk}_level1_result",
            f"{risk}_results",
            "attempt2_" + "results",
        ):
            assert real_path_token not in text

    def test_decision_withholds_touching_the_lane_and_preserved_artifacts(self, sections):
        assert "touch `AUTHORIZATION_ROOT`, any lane path, or the preserved step-11 clone" in _flat(sections["H"])


# ======================================================================================
# 11 -- Catalog and register synchronisation
# ======================================================================================


class TestCatalogAndRegisterSynchronisation:
    def test_catalog_has_exactly_one_entry_for_this_decision(self, catalog):
        matches = [d for d in catalog if d.get("decision_id") == DECISION_ID]
        assert len(matches) == 1

    def test_catalog_entry_is_accurate(self, catalog):
        entry = [d for d in catalog if d.get("decision_id") == DECISION_ID][0]
        assert entry["status"] == "Proposed"
        assert str(entry["date"]) == "2026-08-19"
        assert entry["category"] == "cross_asset_allocation_architecture"
        assert entry["file"] == str(DECISION_PATH.relative_to(ROOT))
        assert entry["supporting_artifact"] == SUITE_PATH.name
        assert "XASSET-0040" in entry["related_decisions"]

    def test_catalog_file_reference_resolves(self, catalog):
        entry = [d for d in catalog if d.get("decision_id") == DECISION_ID][0]
        assert (ROOT / entry["file"]).exists()

    def test_catalog_ids_are_unique(self, catalog):
        ids = [d.get("decision_id") for d in catalog]
        assert len(ids) == len(set(ids))

    def test_self_gate_is_complete_only_on_merged_lifecycle_evidence(self, gates):
        """ADVANCED BY XASSET-0042.

        This asserted `in_progress` because, at authoring time, PR #341 was an unmerged draft
        and no session may mark its own unmerged work complete. PR #341 has since merged and
        its seven-condition lifecycle closed, so `complete` is now the truthful state. The
        guard is STRENGTHENED rather than relaxed: `complete` is no longer accepted on its own
        word -- the gate must additionally carry the merged-lifecycle evidence that justifies
        it, so a premature or unevidenced `complete` still fails here.
        """
        gate = gates[GATE_SELF]
        assert gate["status"] == "complete"
        assert gate["pr"] == 341, "the self-gate must name its own PR"
        description = gate["description"]
        for evidence in (
            "9c8647f9dddacdf63825f569097214ba65299fe8",  # the merge
            "5345229177",  # the principal acceptance carrying the ratification
            "4974291044",  # the independent exact-head review
            "32278094960",  # merge-commit CI at the exact merge SHA
            "5345376547",  # final post-CI closure
        ):
            assert evidence in description, f"completion is unevidenced: {evidence} missing"

    def test_stop_evidence_gate_records_the_terminal_outcome(self, gates):
        description = gates[GATE_STOP]["description"]
        assert "STOPPED_BEFORE_ATTESTATION" in description
        assert "5343692162" in description
        assert "ATTEMPT_1 IS INTACT" in description

    def test_prior_gate_status_corrected_but_narrative_byte_identical(self, gates):
        gate = gates[GATE_PRIOR]
        assert gate["status"] == "complete"
        assert gate["pr"] == 340
        digest = hashlib.sha256(gate["description"].encode("utf-8")).hexdigest()
        assert digest == PRIOR_GATE_DESCRIPTION_SHA256, (
            "the XASSET-0040 gate narrative must be preserved byte-identically"
        )

    def test_self_gate_names_the_pinned_identities(self, gates):
        description = gates[GATE_SELF]["description"]
        for identity in PINNED_IDENTITIES:
            assert identity in description

    def test_self_gate_records_the_downstream_boundary(self, gates):
        description = gates[GATE_SELF]["description"]
        assert "SEPARATELY AUTHORIZED rebinding" in description
        assert "NEW step-11 authorization" in description
        assert "none of which is authorized" in description

    def test_self_gate_does_not_generalize_the_bot_exception(self, gates):
        description = gates[GATE_SELF]["description"]
        assert "NEVER classify claude[bot] generally as" in description

    def test_register_live_fields_point_at_the_currently_live_work(self, ws0014):
        """ADVANCED BY XASSET-0043.

        `active_branch`, `active_pr`, and `last_verified_main_sha` are WS-0014's SINGLE SHARED
        live self-reference fields, not any one filing's own. PR #341 merged at `9c8647f9`
        and PR #342 has since merged at `5fbfc94d`, so under `OPS-0001`'s Active-GitHub-fields
        rule they lawfully advance to the rebinding-authorization unit that is now live. Each
        is strengthened to an exact value, never relaxed to a range or a placeholder.
        """
        # ADVANCED AGAIN BY XASSET-0045, on exactly the terms the docstring above sets out:
        # PR #344 has since merged at `f5dedce1`, so these shared fields lawfully advance once
        # more, to the post-merge-CI recovery-authorization unit that is now live. Each stays
        # an exact value, never relaxed to a range or a placeholder.
        assert ws0014["active_branch"] == "claude/xasset-0045-filing-9yxavw"
        assert ws0014["last_verified_main_sha"] == (
            "f5dedce1d1d3116ed8a6845c4447388c85a5414c"
        )
        assert str(ws0014["last_verified_date"]) == "2026-08-21"
        assert ws0014["active_pr"] == 345
        # PR #343's and PR #344's own closed records survive in the register as history, not
        # as live state.
        assert ws0014["active_pr"] != XASSET0043_ACTIVE_PR
        assert ws0014["active_pr"] != 344

    def test_register_still_parses_and_ws0014_is_unique(self, ws0014):
        assert ws0014["id"] == "WS-0014"


# ======================================================================================
# 12 -- No section is vacuous; suite hygiene
# ======================================================================================


class TestNoSectionIsVacuous:
    @pytest.mark.parametrize("letter", list("ABCDEFGHIJK"))
    def test_every_section_has_substantive_content(self, sections, letter):
        assert letter in sections, f"§{letter} is missing"
        body = sections[letter]
        # strip the heading line itself before measuring
        content = body.split("\n", 1)[1] if "\n" in body else ""
        assert len(content.strip()) > 200, f"§{letter} is vacuous"

    def test_decision_has_rationale_alternatives_and_consequences(self, decision_body):
        for heading in ("## Rationale", "## Alternatives Considered", "## Consequences"):
            assert heading in decision_body

    def test_front_matter_declares_the_supporting_artifact(self, decision_text):
        assert f"supporting_artifact: {SUITE_PATH.name}" in decision_text

    def test_front_matter_status_is_proposed(self, decision_text):
        assert "status: Proposed" in decision_text.split("---\n", 2)[1]


class TestSuiteHygiene:
    def test_no_or_fallback_assertions(self):
        """An ``assert X or Y`` can be satisfied by the wrong half and proves nothing."""
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert) and isinstance(node.test, ast.BoolOp):
                assert not isinstance(node.test.op, ast.Or), (
                    f"or-fallback assertion at line {node.lineno}"
                )

    def test_suite_imports_no_outcome_producing_module(self):
        """The suite must not import any module capable of producing a Stage-1 outcome."""
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        for outcome_module in (
            "level1_stage1_runner",
            "level1_stage1_result_validator",
            "level1_stage1_execution_authorization",
            "level1_construction_universe_closure_validator",
        ):
            assert outcome_module not in imported, (
                f"suite must not import outcome-producing module {outcome_module!r}"
            )
