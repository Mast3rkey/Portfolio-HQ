"""Adversarial tests pinning the ``XASSET-0040`` §G.B step-11 activation/execution authorization.

``XASSET-0039``'s complete seven-condition lifecycle closed, the single unit it authorized then ran,
and it returned ``STEP_10_NO_DRIFT`` -- clean against both required anchors. ``XASSET-0030`` §G.B
**step 10 is done and its one authorized unit is consumed.** Step 11 is next, and it had **no
authority**: ``XASSET-0030`` §G.B authorizes none of itself; ``XASSET-0036`` §F withholds "performing
§G.B steps 8-11"; ``XASSET-0037`` §I and ``XASSET-0038`` §I withhold step 11 **by name**; and
``XASSET-0039`` both bars its own unit from performing or authorizing step 11 and forecloses the
nearest inference -- that a clean step-10 result might reach it. ``XASSET-0040`` closes that gap for
step 11 and nothing else.

Step 11 *is* the irreversible act. ``ATTEMPT_1`` cannot be re-run after claim, and completing one
result mechanically prevents publishing another, so every overreach that matters is sharper here than
at any prior link and each has a dedicated guard:

1. **Step 11 performed now, or treated as authorized on filing.**
   ``TestStep11NotPerformedHere`` and ``TestEffectivityRequiresCompleteLifecycleClosure`` fail if the
   filing attests, arms, claims, executes, or lets any single lifecycle step stand in for complete
   closure.
2. **Premature attestation or premature arming.** ``TestAttestationAndArmingAreGated`` fails if the
   attestation may be produced before every §H condition holds, or if merge is allowed to arm.
3. **Claim without exact authority, or execution before a lawful claim.**
   ``TestClaimAndExecutionOrdering`` fails if the claim may be taken without §H, if execution may
   precede the claim, or if the atomic-immediately-before-first-real-work rule is lost.
4. **A gap between merge and execution, or between attestation and claim.**
   ``TestNoMergeToExecutionAndNoAttestationToClaimGap``.
5. **Post-step-10 drift ignored, or the bound merge dropped as a reference.**
   ``TestExactBindingIsConjunctive`` and ``TestFailClosed``.
6. **Retry, recovery, repair, or rebinding read in from a failure.**
   ``TestNoRepairNoRebindingNoRetry`` and ``TestOneShotAttemptIsNotRerunnable``.
7. **The reserved §P.1 results PR consumed, or results applied rather than merely produced.**
   ``TestP1ResultsPRRemainsSeparate``.
8. **Arming by implication, or this decision inserted into the attestation.**
   ``TestXasset0029NoRegressIntact`` and ``TestDecisionNeverEntersTheAttestation``.
9. **The completed step 10 re-performed or reopened.** ``TestStep10DeterminationRecordedNotRePerformed``.
10. **Protected-path or RISK-boundary access.** ``TestProtectedBoundariesPreserved``.

They also pin the negative space that makes the filing honest: this authorization PR changes no
canonical file, no validator, no authorization module, no runner, no result validator, and no
load-bearing byte; all ten load-bearing paths, both V7 pins, the frozen universe, and the
construction-universe module identity are untouched; and Stage 1 is still ``UNARMED`` with lane state
``ABSENT`` and ``ATTEMPT_1`` unclaimed.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No results document, lane directory, attestation, claim, completion, or ledger entry
is created or read for authorization purposes. No ``risk_lane_boundary`` protected result path is
read, listed, opened, or referenced.
"""

from __future__ import annotations

import ast
import hashlib
import re
from pathlib import Path

import pytest
import yaml

import level1_construction_universe_closure_validator as CU
import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
GOV = ROOT / "governance/decisions"
PREREG = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"
PROTOCOL = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
WORKSTREAMS = ROOT / "operations/WORKSTREAMS.yaml"
CATALOG = ROOT / "governance/decisions.yaml"

D0027 = GOV / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
D0029 = GOV / "XASSET-0029-endpoint-0001-stage-1-operational-authorization.md"
D0030 = GOV / "XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md"
D0036 = GOV / "XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md"
D0037 = GOV / "XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md"
D0038 = (
    GOV
    / "XASSET-0038-endpoint-0001-stage-1-runner-execution-readiness-verification-authorization.md"
)
D0039 = (
    GOV
    / "XASSET-0039-endpoint-0001-stage-1-post-rebinding-drift-fail-closed-authorization.md"
)
D0040 = (
    GOV
    / "XASSET-0040-endpoint-0001-stage-1-step-11-activation-and-execution-authorization.md"
)

#: The effective PR #337 bound merge -- the exact bytes §G.B step 8 bound, and §H item 1.
BOUND_MERGE_SHA = "637eaa30302f5a71f84ab1d215ecbd32c01399b5"

#: The PR #339 merge that carried XASSET-0039 onto `main` and made it effective.
XASSET0039_MERGE_SHA = "6960ce5ddbfa8cff1ef591c58682341c4d4407c7"
#: PR #342's merge -- live `main` as XASSET-0043 was drafted. ADVANCED BY XASSET-0043:
#: PR #341 (`9c8647f9`) and then PR #342 have both merged, so WS-0014's single shared
#: `last_verified_main_sha` advances with them. The assertion stays exact.
XASSET0043_MAIN_SHA = "5fbfc94d7333e552bd2654261e0c57134a172e31"
#: ADVANCED BY XASSET-0044: PR #343 merged at `0709d2f0`, so the register's shared live
#: "where main is now" field lawfully advanced again. The anchor each decision authorizes
#: against is unchanged; only the shared self-reference moved.
XASSET0044_MAIN_SHA = "0709d2f05ab031ecb6f69c40465ed4a227983aed"
#: ADVANCED BY XASSET-0045: PR #344 merged at `f5dedce1`, so the register's shared live
#: "where main is now" field lawfully advanced again under OPS-0001's Active-GitHub-fields
#: rule. The anchor each decision authorizes against is unchanged; only the shared
#: self-reference moved. The assertion stays EXACT.
XASSET0045_MAIN_SHA = "f5dedce1d1d3116ed8a6845c4447388c85a5414c"
#: ADVANCED BY XASSET-0046: PR #345 merged at `2f8cdebe`, so the register's shared live
#: "where main is now" field lawfully advanced again under OPS-0001's Active-GitHub-fields
#: rule. The anchor each decision authorizes against is unchanged; only the shared
#: self-reference moved. The assertion stays EXACT, and gains a negative pin so the field is
#: bound at BOTH ends rather than only at one.
XASSET0046_MAIN_SHA = "2f8cdebe14925021171b9779453946be1f69b506"
#: ADVANCED BY XASSET-0047: PR #346 merged at `0b76c09f`, so the register's shared live
#: "where main is now" field lawfully advanced again under OPS-0001's Active-GitHub-fields
#: rule. The anchor each decision authorizes against is unchanged; only the shared
#: self-reference moved. The assertion stays EXACT and is bound at BOTH ends.
XASSET0047_MAIN_SHA = "0b76c09f8d1aba01780b4f06fdd692f7393fbfd3"
#: ADVANCED BY XASSET-0048: PR #347 merged at `bb95ed26`, so the register's shared live
#: "where main is now" field lawfully advanced again under OPS-0001's Active-GitHub-fields
#: rule. The anchor each decision authorizes against is unchanged; only the shared
#: self-reference moved. The assertion stays EXACT and is bound at BOTH ends.
XASSET0048_MAIN_SHA = "bb95ed26964b1bc7a2e230c76060fec82752efa1"
#: ADVANCED BY XASSET-0049. WS-0014's shared live "where main is now" / "which pull request is
#: live" fields move with EVERY unit under OPS-0001's Active-GitHub-fields rule. Each prior
#: generation's value is retained beside the current one as a NEGATIVE pin rather than deleted, so
#: a silent revert to any finished unit's state still fails.
XASSET0049_MAIN_SHA = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"
XASSET0049_ACTIVE_PR = 349
#: WS-0014's shared `active_pr` while THIS rebinding-authorization unit is the live work.
#: Set to the real GitHub number issued when the pull request was opened, verified
#: against live GitHub afterwards, never left as a guess.
#: ADVANCED BY XASSET-0050. PR #349 merged at `a9414554`, so WS-0014's shared live
#: "where main is now" / "which pull request is live" fields lawfully advanced again under
#: OPS-0001's Active-GitHub-fields rule. XASSET-0050 is a DESIGN-ONLY authorization: it changes
#: no module constant, so `REVIEWED_BASE_SHA` stays XASSET-0049's lawful rebinding base and only
#: the register's shared self-reference moved. Each prior generation's value is retained beside
#: the current one as a NEGATIVE pin rather than deleted, so a silent revert to any finished
#: unit's state still fails. The assertion stays EXACT and is bound at BOTH ends.
XASSET0050_MAIN_SHA = "a941455491cc5e4d3d868775fb6b4b88f0fe2ce3"
#: Committed as an impossible sentinel first, then replaced by the number GitHub actually issued
#: in a fast-forward follow-up commit. Never predicted. Distinct from every prior sentinel.
XASSET0050_ACTIVE_PR = 350
#: ADVANCED BY XASSET-0051. PR #350 merged at `6fd9a697...` and PR #351 (a test-only repair
#: touching none of the eighteen bound paths) then merged at `ea9e74a1...`, so WS-0014's shared
#: live "where main is now" / "which pull request is live" fields lawfully advanced again under
#: OPS-0001's Active-GitHub-fields rule. XASSET-0051 is a DESIGN-ONLY authorization: it changes
#: no module constant, so `REVIEWED_BASE_SHA` stays XASSET-0049's lawful rebinding base and only
#: the register's shared self-reference moved. Each prior generation's value is retained beside
#: the current one as a NEGATIVE pin rather than deleted, so a silent revert to any finished
#: unit's state still fails. The assertion stays EXACT and is bound at BOTH ends.
XASSET0051_MAIN_SHA = "ea9e74a1f4224a78df2416db9c872b0c5812894b"
#: Committed as an impossible sentinel first (-51), then replaced by the number GitHub actually
#: issued in a fast-forward follow-up commit. Never predicted. Distinct from every prior sentinel.
XASSET0051_ACTIVE_PR = 352
#: ADVANCED BY XASSET-0052. PR #352 merged at `8def8bd0...`, so WS-0014's shared live
#: "where main is now" / "which pull request is live" fields lawfully advanced again under
#: OPS-0001's Active-GitHub-fields rule. XASSET-0052 is a DESIGN-ONLY authorization: it changes
#: no module constant, so `REVIEWED_BASE_SHA` stays XASSET-0049's lawful rebinding base and only
#: the register's shared self-reference moved. Each prior generation's value is retained beside
#: the current one as a NEGATIVE pin rather than deleted, so a silent revert to any finished
#: unit's state still fails. The assertion stays EXACT and is bound at BOTH ends.
XASSET0052_MAIN_SHA = "8def8bd096b4edecbf10fc20870a6d03b6cb56fe"
#: Committed as an impossible sentinel first (-52), then replaced by the number GitHub actually
#: issued in a fast-forward follow-up commit. Never predicted. Distinct from every prior sentinel.
XASSET0052_ACTIVE_PR = -52
XASSET0043_ACTIVE_PR = 343
#: ADVANCED BY XASSET-0044. WS-0014's single shared `active_pr`, set from the real number
#: GitHub issued and verified against the live pull request after opening, never guessed.
XASSET0044_ACTIVE_PR = 344
#: ADVANCED BY XASSET-0045. WS-0014's single shared `active_pr`, set from the real number
#: GitHub issued and verified against the live pull request after opening, never guessed.
XASSET0045_ACTIVE_PR = 345
#: ADVANCED BY XASSET-0046. WS-0014's single shared `active_pr`, set from the real number
#: GitHub issued for this reauthorization unit and verified against the live pull request
#: after opening, never guessed.
XASSET0046_ACTIVE_PR = 346
#: ADVANCED BY XASSET-0047. WS-0014's single shared `active_pr`, set from the real number
#: GitHub issued for this recovery unit -- never guessed: the branch's first commit carried
#: the impossible sentinel 0, the draft was opened, and the issued number was read back from
#: live GitHub before being bound here.
XASSET0047_ACTIVE_PR = 347
#: ADVANCED BY XASSET-0048. WS-0014's single shared `active_pr`, carrying the impossible
#: sentinel ``None`` until GitHub issues this unit's number, which is then read back from
#: live GitHub and bound -- never guessed.
XASSET0048_ACTIVE_PR = 348

#: The completed step-10 evidence -- §H item 5 -- and its formal determination.
STEP10_EVIDENCE_COMMENT = "5341448714"
STEP10_DETERMINATION = "STEP_10_NO_DRIFT"

#: XASSET-0039's own lifecycle closure, which made the step-10 unit authorized.
XASSET0039_CLOSURE_COMMENT = "5341374154"

#: The values accepted authority already fixes as exact constants, and the only ones XASSET-0040
#: restates. Everything else in its verification derives from durable sources at run time.
PROTOCOL_SHA256 = "367583b616e1c6ab614bcf67d451fe27ce40507d073374190c57291e761d8971"
PREREG_SHA256 = "768b013c0129f02577fea3c2a1a3100b4340b9a42f48ee0d0dbd6e671894bce1"

#: ADDED BY XASSET-0044. The two constants above are what XASSET-0040's own ACCEPTED,
#: MERGED decision text restates, and that text is history: it is not edited, so they are
#: not either. XASSET-0044's post-correction rebinding lawfully amended the canonical
#: authorization language in lockstep (V7 -> V8) under XASSET-0030 SS-D, so the pins that
#: describe the LIVE files are these. The two roles were conflated in a single pair of
#: constants until the amendment forced them apart; keeping both is what lets the
#: decision-text checks and the live-byte checks each stay at full strength.
CURRENT_PROTOCOL_SHA256 = "1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84"
CURRENT_PREREG_SHA256 = "898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f"
FROZEN_UNIVERSE_SHA256 = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
CONSTRUCTION_UNIVERSE_MODULE_SHA256 = (
    "1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5"
)

#: The ten paths XASSET-0037 bound. XASSET-0040 must change none of them.
#: EXTENDED BY XASSET-0044, 10 -> 14. The four additions are the decision files that jointly make
#: the corrected bytes lawful, bound by DIRECT MEMBERSHIP so none can be edited after an
#: attestation authenticates. Nothing is removed: the original ten are all still here, and the
#: sorted comparison below is unchanged in kind and still exact.
EXPECTED_LOAD_BEARING = tuple(sorted((
    "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
    "governance/decisions/XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
    "governance/decisions/XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md",
    "level1_construction_universe_closure_validator.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_stage1_execution_authorization.py",
    "level1_stage1_result_validator.py",
    "level1_stage1_runner.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "governance/decisions/"
    "XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md",
    "governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md",
    "governance/decisions/"
    "XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md",
    "governance/decisions/"
    "XASSET-0044-endpoint-0001-stage-1-post-correction-operational-rebinding.md",
    # EXTENDED AGAIN BY XASSET-0047, 14 -> 16, under XASSET-0046 SS-G.6. The two additions are the
    # authority for the post-merge-CI recovery and the recovery's own decision, bound by DIRECT
    # MEMBERSHIP on the footing XASSET-0043 and XASSET-0044 already occupy. Nothing is removed:
    # the original ten and XASSET-0044's own four are all still here, and the sorted comparison
    # below is unchanged in kind and still EXACT.
    "governance/decisions/"
    "XASSET-0046-endpoint-0001-stage-1-post-merge-ci-recovery-reauthorization.md",
    "governance/decisions/"
    "XASSET-0047-endpoint-0001-stage-1-post-merge-ci-recovery-reconciliation.md",
    # EXTENDED AGAIN BY XASSET-0049, 16 -> 18, under XASSET-0048 SS-E.4 / SS-F.6. The two
    # additions are the authority for the step-8-EQUIVALENT rebinding and that rebinding's own
    # decision, bound by DIRECT MEMBERSHIP on the footing XASSET-0043/XASSET-0044 and
    # XASSET-0046/XASSET-0047 already occupy. NOTHING IS REMOVED: the original ten,
    # XASSET-0044's four, and XASSET-0047's two are all still here, and the sorted comparison
    # below is unchanged in kind and still EXACT -- so a removal, swap, or trade is still caught.
    "governance/decisions/"
    "XASSET-0048-endpoint-0001-stage-1-step-8-equivalent-rebinding-authorization.md",
    "governance/decisions/"
    "XASSET-0049-endpoint-0001-stage-1-step-8-equivalent-successor-operational-rebinding.md",
)))

#: The five Python modules inside those ten paths, each independently able to affect the 680
#: outcomes. Step 11 executes them; it may not edit one.
OUTCOME_CAPABLE_MODULES = (
    "level1_construction_universe_closure_validator.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_stage1_execution_authorization.py",
    "level1_stage1_result_validator.py",
    "level1_stage1_runner.py",
)

#: Every top-level section the decision must carry. A section that exists but is reachable by no
#: assertion can be weakened with nothing failing, so the vacuity guard covers all of them.
ALL_SECTIONS = tuple("ABCDEFGHIJKLMNO")


def _norm(text: str) -> str:
    """Collapse whitespace and blockquote markers so a phrase match survives hard wrapping.

    These decisions are hard-wrapped at ~100 columns and state operative rules inside Markdown
    blockquotes and tables, so an exact quoted phrase is routinely split across a newline with a
    ``>`` continuation marker landing mid-phrase. Both are normalised away, so each assertion below
    is a genuine requirement that the phrase be *present* rather than a hostage to the wrap column.
    """
    without_quote_markers = re.sub(r"^\s*>\s?", " ", text, flags=re.MULTILINE)
    return re.sub(r"\s+", " ", without_quote_markers)


def _section(text: str, letter: str) -> str:
    """Return one top-level ``### <letter>.`` section body, normalised.

    Anchored at line start with exactly three hashes: a naive ``split("### G.")`` also matches
    inside a ``#### G.1`` sub-heading and would silently return a near-empty fragment, making any
    ``in`` assertion over it vacuous. The length floor makes that failure loud instead.
    """
    match = re.search(
        rf"^### {re.escape(letter)}\..*?(?=^### [A-Z]\.|^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match is not None, f"XASSET-0040 section {letter} not found"
    body = match.group(0)
    assert len(body) > 200, f"section {letter} extracted suspiciously short ({len(body)} chars)"
    return _norm(body)


def _part(text: str, heading: str) -> str:
    """Return one top-level ``## <heading>`` part body, normalised.

    Companion to :func:`_section` for the parts that are not lettered decision sections. The same
    length floor applies, so a heading rename cannot silently yield an empty fragment and turn every
    ``in`` assertion over it vacuous.
    """
    match = re.search(
        rf"^## {re.escape(heading)}\b.*?(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL
    )
    assert match is not None, f"XASSET-0040 part {heading!r} not found"
    body = match.group(0)
    assert len(body) > 200, f"part {heading!r} extracted suspiciously short ({len(body)} chars)"
    return _norm(body)


def _suite_ast_excluding_hygiene() -> ast.Module:
    """This module's AST with ``TestSuiteHygiene`` removed.

    The hygiene class is the guard; it must scan everything *else*. Without this exclusion the
    guards below would trip on their own forbidden-pattern literals -- a self-reference, not a
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


def _ws0014_gate(gate_id: str) -> dict:
    data = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
    for workstream in data["workstreams"]:
        if workstream.get("id") == "WS-0014":
            for gate in workstream["milestones"]:
                if gate["gate"] == gate_id:
                    return gate
    raise AssertionError(f"WS-0014 gate {gate_id!r} not found")


@pytest.fixture(scope="module")
def decision() -> str:
    return D0040.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def norm(decision: str) -> str:
    return _norm(decision)


# --------------------------------------------------------------------------------------------------
# 1. The authority gap is real, and rests on accepted text rather than convenience
# --------------------------------------------------------------------------------------------------


class TestAuthorityGapIsGroundedInAcceptedText:
    def test_step_11_text_is_quoted_verbatim_from_xasset_0030(self, norm: str) -> None:
        step_11 = (
            "Only then may the external one-shot attestation be produced and Stage 1 armed "
            "— arm, claim, and the 680-construction run."
        )
        assert _norm(step_11) in _norm(D0030.read_text(encoding="utf-8"))
        assert _norm(step_11) in norm

    @pytest.mark.parametrize(
        "path, phrase",
        [
            (D0030, "This decision authorizes none of G.A or G.B"),
            (D0036, "performing §G.B steps 8–11."),
            (D0037, "`XASSET-0030` §G.B steps 9, 10, or 11"),
            (D0037, "each requires its own separate authority"),
            (D0038, "perform or authorize `XASSET-0030` §G.B step 10 or step 11."),
            (D0039, "perform or authorize `XASSET-0030` §G.B step 11."),
            (
                D0039,
                "retains its own separate-authority requirement and is entirely outside this "
                "filing.",
            ),
            (D0039, "A step-10 no-drift determination, however clean, authorizes nothing further."),
            (D0039, "is not made reachable by a clean step-10 result"),
        ],
    )
    def test_each_withholding_is_verbatim_in_its_own_source(self, path: Path, phrase: str) -> None:
        """A paraphrase drifting from source, or a source edit, must fail rather than survive."""
        assert _norm(phrase) in _norm(path.read_text(encoding="utf-8"))

    @pytest.mark.parametrize(
        "phrase",
        [
            "This decision authorizes none of G.A or G.B",
            "performing §G.B steps 8–11.",
            "`XASSET-0030` §G.B steps 9, 10, or 11",
            "each requires its own separate authority",
            "perform or authorize `XASSET-0030` §G.B step 10 or step 11.",
            "perform or authorize `XASSET-0030` §G.B step 11.",
            "A step-10 no-drift determination, however clean, authorizes nothing further.",
        ],
    )
    def test_each_withholding_is_still_cited_by_the_decision(self, norm: str, phrase: str) -> None:
        """The citation must remain in the decision, not merely in the source."""
        assert _norm(phrase) in norm

    def test_five_filings_named_step_11_and_five_declined(self, decision: str) -> None:
        section = _section(decision, "B")
        assert "Five filings named step 11 and five declined to grant it" in section
        for name in ("XASSET-0030", "XASSET-0036", "XASSET-0037", "XASSET-0038", "XASSET-0039"):
            assert name in section

    def test_decision_does_not_rest_on_self_authorization(self, decision: str) -> None:
        section = _section(decision, "B")
        assert (
            "does not rest on the weaker claim that step 11 might be self-authorizing, or that a "
            "clean step-10 result reached it" in section
        )


# --------------------------------------------------------------------------------------------------
# 2. This filing performs no part of step 11
# --------------------------------------------------------------------------------------------------


class TestStep11NotPerformedHere:
    def test_determination_says_the_filing_performs_no_part_of_step_11(self, decision: str) -> None:
        section = _section(decision, "A")
        assert "This filing performs no part of step 11." in section
        assert "Merging it arms nothing" in section

    @pytest.mark.parametrize(
        "phrase",
        [
            "generates no attestation",
            "arms nothing",
            "creates no lane state",
            "reaches no `READY`",
            "claims nothing",
            "evaluates no gate",
            "executes nothing",
            "produces no result",
            "persists nothing",
        ],
    )
    def test_each_prohibited_act_is_disclaimed_in_the_determination(
        self, decision: str, phrase: str
    ) -> None:
        assert phrase in _section(decision, "A")

    def test_absolute_non_authorization_covers_the_whole_activation_surface(
        self, decision: str
    ) -> None:
        section = _section(decision, "O")
        for phrase in (
            "generates no attestation",
            "creates no `AUTHORIZATION_ROOT`",
            "arms, claims, completes, executes, or recovers no Stage-1 execution",
            "performs no part of §G.B step 11",
            "re-performs no part of the completed step 9 or step 10",
            "creates no `stage1_results.yaml`",
            "consumes nothing of `ATTEMPT_1`",
            "consumes no `XASSET-0027` §P.1 results PR",
        ):
            assert phrase in section

    def test_no_lane_artifact_exists_after_this_filing(self) -> None:
        """The filing must not have created any lane state as a side effect."""
        for path in (A.AUTHORIZATION_ROOT, A.AUTHORIZATION_PATH, A.CLAIM_PATH, A.COMPLETION_PATH, A.LEDGER_PATH):
            assert not Path(path).exists(), f"{path} exists; the filing armed or claimed something"

    def test_no_results_document_exists_anywhere(self) -> None:
        assert list(ROOT.rglob("stage1_results.yaml")) == []


# --------------------------------------------------------------------------------------------------
# 3. Attestation and arming are gated, never implied by merge
# --------------------------------------------------------------------------------------------------


class TestAttestationAndArmingAreGated:
    def test_attestation_is_permitted_only_when_every_h_condition_holds(self, decision: str) -> None:
        section = _section(decision, "F")
        assert "Produce the external one-shot attestation" in section
        assert (
            "Items **3–6** are each permitted only when every §H condition and every §I condition "
            "still holds at the moment it is taken." in section
        )

    def test_activation_authority_ends_at_item_6(self, decision: str) -> None:
        """The four act-kinds §F actually grants must be named, and their ceiling stated."""
        section = _section(decision, "F")
        assert (
            "**Items 1–6 are the whole of the activation, execution, result-production, and "
            "lane-transition authority granted here, and that authority ends at item 6.**" in section
        )
        assert "No act of any of those four kinds is authorized beyond item 6" in section

    def test_items_7_and_8_are_mandatory_duties_not_withdrawn(self, decision: str) -> None:
        """§F numbers the fail-closed response and the external report; it must not then deny them.

        The pre-correction text closed with an absolute "No step beyond 6 is authorized", which
        withdrew the two items it had just granted (independent review 4972220888, MAJOR 1). At an
        irreversible boundary where §I makes uncertainty a stop condition, a future executor cannot
        safely resolve that by inference — so both halves are pinned here.
        """
        section = _section(decision, "F")
        assert "**Items 7 and 8 are duties, not further steps.**" in section
        assert "are **mandatory**, owed on every path" in section
        assert "not weakened by the sentence above and are not exceptions to it" in section

    def test_the_withdrawn_absolute_wording_is_gone(self, decision: str) -> None:
        """Pins the exact contradictory sentence out of §F so it cannot silently return."""
        section = _section(decision, "F")
        assert "No step beyond 6 is authorized" not in section
        assert "each of 3–6 is permitted" not in section

    def test_duties_do_not_extend_the_sequence_or_authorize_successors(
        self, decision: str
    ) -> None:
        section = _section(decision, "F")
        assert (
            "they do not extend the execution sequence, do not move the lane, do not produce, "
            "publish, commit, or deliver any result, and authorize no successor work of any kind."
            in section
        )
        assert "Discharging them is how the unit ends, never how it continues." in section

    def test_merge_alone_arms_nothing(self, decision: str) -> None:
        section = _section(decision, "N")
        assert (
            "Merging this decision does not arm Stage 1, does not create lane state, does not "
            "claim `ATTEMPT_1`, and executes nothing." in section
        )
        assert (
            "Immediately after this decision merges, `new_execution_is_authorized()` still returns "
            "`False` and the lane is still `ABSENT`." in section
        )

    def test_the_allowed_sequence_starts_from_absent_and_only_moves_forward(
        self, decision: str
    ) -> None:
        section = _section(decision, "F")
        assert "ABSENT ──▶ READY ──▶ CLAIMED ──▶ COMPLETED" in section
        assert "may move the lane only along the accepted path, and only forwards" in section

    def test_live_state_is_still_absent_and_unauthorized(self) -> None:
        authorized, reason = A.new_execution_is_authorized()
        assert authorized is False
        assert "no attestation present" in reason


# --------------------------------------------------------------------------------------------------
# 4. Claim requires exact authority; execution requires a lawful claim first
# --------------------------------------------------------------------------------------------------


class TestClaimAndExecutionOrdering:
    def test_claim_is_atomic_and_immediately_before_the_first_real_work(
        self, decision: str
    ) -> None:
        section = _section(decision, "F")
        assert (
            "Take the single lawful claim** of `ATTEMPT_1` (`claim_execution`), atomically and "
            "immediately before the first real work" in section
        )

    def test_execution_before_a_lawful_claim_is_prohibited(self, decision: str) -> None:
        section = _section(decision, "G")
        assert (
            "execute before a lawful claim**, evaluate any gate for any registered construction "
            "before the claim is taken" in section
        )

    def test_the_sequence_places_the_run_after_the_claim(self, decision: str) -> None:
        section = _section(decision, "F")
        claim_at = section.index("Re-verify continuity, then claim")
        run_at = section.index("**Run** the 680 constructions")
        complete_at = section.index("**Complete**")
        assert claim_at < run_at < complete_at

    def test_atomic_claim_rule_is_verbatim_in_xasset_0029(self) -> None:
        assert (
            _norm("The claim is taken **atomically immediately before the first real work**")
            in _norm(D0029.read_text(encoding="utf-8"))
        )


# --------------------------------------------------------------------------------------------------
# 5. No merge-to-execution gap, and no attestation-to-claim gap
# --------------------------------------------------------------------------------------------------


class TestNoMergeToExecutionAndNoAttestationToClaimGap:
    def test_both_gaps_are_addressed_by_name(self, decision: str) -> None:
        section = _norm(decision)
        assert "No merge-to-execution gap, and no attestation-to-claim gap" in section

    def test_merge_to_execution_gap_is_closed(self, norm: str) -> None:
        assert (
            "this decision's own §N lifecycle must close in full before the unit may begin, and "
            "the unit must re-verify §H against live state **immediately before it acts**" in norm
        )

    def test_attestation_to_claim_gap_is_closed(self, norm: str) -> None:
        assert (
            "**No unverified interval may separate the attestation from the claim.**" in norm
        )
        assert "it must re-verify §H before claiming" in norm

    def test_uncertainty_in_the_interval_is_failure_not_a_reason_to_proceed(
        self, norm: str
    ) -> None:
        assert (
            "uncertainty there is failure, not a reason to proceed" in norm
        )


# --------------------------------------------------------------------------------------------------
# 6. Exact binding is conjunctive
# --------------------------------------------------------------------------------------------------


class TestExactBindingIsConjunctive:
    def test_binding_is_stated_as_conjunctive_with_any_failure_a_stop(self, decision: str) -> None:
        section = _section(decision, "H")
        assert (
            "These are conjunctive: **failure or uncertainty on any one is a stop (§I).**"
            in section
        )

    @pytest.mark.parametrize(
        "phrase",
        [
            "The ten `LOAD_BEARING_RELPATHS`, byte-identical to the effective PR #337 bound merge",
            "The V7 canonical pins",
            "The frozen construction universe",
            "The `XASSET-0037` lifecycle evidence",
            "No drift since the completed step-10 determination",
            "Lane state exactly `ABSENT`",
            "This decision's own §N lifecycle closed in full",
        ],
    )
    def test_every_binding_item_is_present(self, decision: str, phrase: str) -> None:
        assert phrase in _section(decision, "H")

    def test_bound_merge_and_step_10_evidence_are_both_named(self, decision: str) -> None:
        section = _section(decision, "H")
        assert BOUND_MERGE_SHA in section
        assert STEP10_EVIDENCE_COMMENT in section
        assert STEP10_DETERMINATION in section

    def test_exact_constants_are_the_only_ones_restated(self, decision: str) -> None:
        # §H names the pins in their conventional truncated form; the full 64-character values
        # appear once in the preflight table. Both are required, so neither can quietly drift.
        section = _section(decision, "H")
        assert f"{PROTOCOL_SHA256[:8]}…{PROTOCOL_SHA256[-5:]}" in section
        assert f"{PREREG_SHA256[:8]}…{PREREG_SHA256[-5:]}" in section
        assert FROZEN_UNIVERSE_SHA256 in section
        assert "**680**" in section
        assert "**48**" in section
        whole = _norm(decision)
        assert PROTOCOL_SHA256 in whole
        assert PREREG_SHA256 in whole

    def test_expected_identity_derives_from_durable_sources_not_restated_constants(
        self, decision: str
    ) -> None:
        section = _section(decision, "H")
        assert (
            "derived from that merged git tree at verification time, never from a constant "
            "restated in a decision record" in section
        )

    def test_the_mechanism_governs_and_the_unit_verifies_on_top_of_it(self, decision: str) -> None:
        section = _section(decision, "H")
        assert (
            "The mechanism's fail-closed behaviour governs; the unit's own pre-attestation "
            "verification is required on top of it, not instead of it." in section
        )

    def test_dropping_the_step_9_anchor_is_reasoned_rather_than_silent(self, decision: str) -> None:
        section = _section(decision, "H")
        assert "Why two references and not three." in section
        assert "already closes the step-9 window" in section
        assert "**Drift against either is drift.**" in section


# --------------------------------------------------------------------------------------------------
# 7. Fail-closed
# --------------------------------------------------------------------------------------------------


class TestFailClosed:
    @pytest.mark.parametrize(
        "trigger",
        [
            "drift",
            "missing identity",
            "failed validation",
            "authentication failure",
            "unexpected lane state",
            "stale evidence",
            "state the unit cannot determine with certainty",
        ],
    )
    def test_every_named_trigger_stops_the_unit(self, decision: str, trigger: str) -> None:
        assert trigger in _section(decision, "I")

    def test_the_four_required_responses_are_all_present(self, decision: str) -> None:
        section = _section(decision, "I")
        assert "**stop**" in section
        assert "**report** the exact condition" in section
        assert "**change nothing further**" in section
        assert "**not attest, not arm, not claim, and not execute.**" in section

    def test_uncertainty_is_failure(self, decision: str) -> None:
        section = _section(decision, "I")
        assert "**Uncertainty is failure.**" in section
        assert "may not resolve an ambiguous state in favour of proceeding" in section
        assert "may not treat an unreachable durable source as though it had confirmed" in section


# --------------------------------------------------------------------------------------------------
# 8. No repair, no rebinding, no retry
# --------------------------------------------------------------------------------------------------


class TestNoRepairNoRebindingNoRetry:
    def test_the_unit_is_an_executor_never_a_remediator(self, decision: str) -> None:
        section = _section(decision, "J")
        assert "an **executor under exact conditions**, never a remediator" in section

    @pytest.mark.parametrize(
        "prohibition",
        [
            "correct, revert, regenerate, or re-pin the drifted byte",
            "rebind the drifted path, or perform any part of a rebinding",
            're-run readiness verification, or re-run the step-10 drift check, to "clear" what it found',
            "retry, re-attest, re-claim, recover, or reset the lane",
            "delete or recreate `AUTHORIZATION_ROOT` or any lane path",
        ],
    )
    def test_each_remediation_route_is_closed(self, decision: str, prohibition: str) -> None:
        assert prohibition in _section(decision, "J")

    def test_remediation_requires_separately_authorized_things(self, decision: str) -> None:
        section = _section(decision, "J")
        for remedy in ("**correction**", "**rebinding**", "renewed readiness", "**governed recovery**"):
            assert remedy in section

    def test_finding_the_work_is_not_authority_to_do_the_work(self, decision: str) -> None:
        section = _section(decision, "J")
        assert (
            "None of those is authorized by this decision, and none becomes authorized by the "
            "step-11 unit discovering that it is needed. Finding the work is not authority to do "
            "the work." in section
        )


# --------------------------------------------------------------------------------------------------
# 9. One-shot: ATTEMPT_1 is not rerunnable
# --------------------------------------------------------------------------------------------------


class TestOneShotAttemptIsNotRerunnable:
    def test_authorization_is_spent_by_the_first_lawful_claim(self, decision: str) -> None:
        section = _section(decision, "L")
        assert (
            "This authorization is spent by the first lawful claim, whatever follows it." in section
        )

    def test_no_second_attempt_of_any_framing(self, decision: str) -> None:
        section = _section(decision, "L")
        assert (
            "does not authorize a second attempt, a second attestation after a consumed claim, a "
            "re-run under any framing, or a substituted result" in section
        )

    def test_a_post_claim_failure_yields_a_consumed_attempt_not_a_retry(
        self, decision: str
    ) -> None:
        section = _section(decision, "L")
        assert (
            "the correct outcome is a consumed attempt and a reported failure — not a retry"
            in section
        )

    def test_the_attempt_identity_is_the_repository_constant(self, decision: str) -> None:
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"
        assert A.EXECUTION_ATTEMPT_ID in _section(decision, "L")

    def test_durability_boundary_is_preserved_not_papered_over(self, decision: str) -> None:
        section = _section(decision, "L")
        assert "Reconstructing a lane that was destroyed is not authorized here." in section

    def test_terminal_stop_conditions_all_end_in_report_and_stop(self, decision: str) -> None:
        section = _section(decision, "K")
        assert (
            "In every one of the four, the unit's next act is to report and stop." in section
        )
        assert (
            "No outcome of step 11 — including the cleanest possible one — authorizes any "
            "successor unit." in section
        )

    def test_post_claim_failure_records_the_attempt_as_consumed(self, decision: str) -> None:
        section = _section(decision, "K")
        assert "`ATTEMPT_1` is consumed." in section
        assert "must not retry, re-claim, recover, reset, or re-run" in section

    def test_the_completed_terminal_condition_stops_rather_than_continues(
        self, decision: str
    ) -> None:
        """The cleanest outcome is where an unbounded reading is most tempting, so pin it."""
        section = _section(decision, "K")
        assert (
            "It does not commit the artifact, does not open `XASSET-0027` §P.1's PR, does not "
            "interpret or apply the results, and does not authorize anything further (§G.1)."
            in section
        )


# --------------------------------------------------------------------------------------------------
# 10. The reserved §P.1 results PR stays reserved, and results are produced but not applied
# --------------------------------------------------------------------------------------------------


class TestP1ResultsPRRemainsSeparate:
    def test_p1_text_is_quoted_verbatim_from_xasset_0027(self, decision: str) -> None:
        phrase = (
            "That PR may make no production configuration change, must pass "
            "`validate_stage1_results()` against the closed universe, and its own result lifecycle "
            "requires independent exact-head review and principal acceptance."
        )
        assert _norm(phrase) in _norm(D0027.read_text(encoding="utf-8"))
        assert _norm(phrase) in _norm(decision)

    def test_the_boundary_is_derived_from_both_accepted_texts(self, decision: str) -> None:
        section = _section(decision, "E")
        assert "`XASSET-0030` §G.B step 11 ends at the run.**" in section
        assert "`XASSET-0027` §P.1 is the vehicle for that delivery" in section

    def test_p1_remains_one_unspent(self, decision: str) -> None:
        section = _section(decision, "E")
        assert "neither consumes nor pre-authorizes §P.1's PR, and does not open it" in section
        assert "**one, unspent.**" in section

    def test_p1_precondition_satisfaction_is_not_authority(self, decision: str) -> None:
        section = _section(decision, "E")
        assert (
            "That satisfaction is not authority for step 11, and this decision's authority for "
            "step 11 is not authority to open §P.1's PR." in section
        )

    def test_the_unit_may_not_open_or_consume_the_results_pr(self, decision: str) -> None:
        section = _section(decision, "G")
        assert (
            "open, consume, or pre-empt `XASSET-0027` §P.1's reserved results PR**, or commit the "
            "result artifact to the repository" in section
        )

    def test_producing_results_is_not_applying_them(self, decision: str) -> None:
        norm_all = _norm(decision)
        assert "Producing results is not applying them" in norm_all
        assert "**A completed run is a result, not a conclusion.**" in norm_all


# --------------------------------------------------------------------------------------------------
# 11. XASSET-0029 §E is intact, and this decision never enters the attestation
# --------------------------------------------------------------------------------------------------


class TestXasset0029NoRegressIntact:
    def test_the_rule_is_quoted_verbatim(self, decision: str) -> None:
        phrase = (
            "Arming is a **runtime operator act**, not a further merged governance PR."
        )
        assert _norm(phrase) in _norm(D0029.read_text(encoding="utf-8"))
        assert _norm(phrase) in _norm(decision)

    def test_the_filing_is_not_an_activation_event(self, decision: str) -> None:
        section = _section(decision, "D")
        assert "This filing is not an arming step and not an activation event." in section
        assert "**Merging this decision arms nothing.**" in section

    def test_zero_activation_factors_are_added(self, decision: str) -> None:
        section = _section(decision, "D")
        assert "It adds zero activation factors." in section
        assert "stays permanently `false`" in section
        assert (
            "no committed value in this repository — this decision included — authorizes Stage-1 "
            "execution." in section
        )

    def test_the_regress_is_shown_to_terminate(self, decision: str) -> None:
        section = _section(decision, "D")
        assert "The regress terminates here, and demonstrably." in section
        assert "has eleven steps and no twelfth" in section
        assert (
            "This decision is the final governance authorization the §G.B sequence names" in section
        )

    def test_the_removal_is_of_a_later_withholding_not_a_new_factor(self, decision: str) -> None:
        section = _section(decision, "D")
        assert (
            "What this filing supplies is the removal of a later, express withholding — not a new "
            "activation factor." in section
        )

    def test_the_unit_may_not_authorize_any_successor_unit(self, decision: str) -> None:
        assert "- **authorize any successor unit of any kind.**" in _section(decision, "G")

    def test_no_successor_authorization_is_created(self, decision: str) -> None:
        """Region-scoped: a document-wide check passes while one copy of the claim is flipped."""
        assert "authorizes no successor authorization of any kind" in _section(decision, "D")
        assert "it authorizes no successor authorization." in _part(decision, "Rationale")
        assert (
            "It authorizes no successor authorization, and no outcome of step 11"
            in _part(decision, "Consequences")
        )


class TestDecisionNeverEntersTheAttestation:
    def test_the_mechanism_binds_xasset_0037_not_this_decision(self) -> None:
        """RE-ANCHORED BY XASSET-0044. The property is unchanged and is what matters: this
        decision (XASSET-0040) is never what the mechanism binds. XASSET-0037's identity now
        lives in PRIOR_SUCCESSOR_REBINDING_*, and the effective source has moved on again.
        """
        assert A.PRIOR_SUCCESSOR_REBINDING_DECISION == "XASSET-0037"
        assert A.PRIOR_SUCCESSOR_REBINDING_PULL_REQUEST == 337
        assert A.AUTHORIZING_DECISION != "XASSET-0040"
        assert A.AUTHORIZING_PULL_REQUEST != 340

    def test_the_decision_states_it_must_not_be_inserted(self, decision: str) -> None:
        # §D.1 is a `####` subsection of §D, so §D's own region covers it.
        section = _section(decision, "D")
        assert "This decision never enters the attestation" in section
        assert "**`XASSET-0040` must not be inserted into that mechanism.**" in section

    def test_editing_the_binding_constants_is_prohibited(self, decision: str) -> None:
        section = _section(decision, "G")
        assert (
            "alter `AUTHORIZING_DECISION` or `AUTHORIZING_PULL_REQUEST`" in section
        )

    def test_governance_authority_and_execution_identity_are_kept_distinct(
        self, decision: str
    ) -> None:
        assert (
            "This decision is the **governance precondition** for the unit to act. The "
            "attestation's **content** remains fixed by the accepted mechanism exactly as it "
            "stands today." in _section(decision, "D")
        )


# --------------------------------------------------------------------------------------------------
# 12. The completed step 10 is recorded, not re-performed
# --------------------------------------------------------------------------------------------------


class TestStep10DeterminationRecordedNotRePerformed:
    def test_the_determination_is_recorded_in_the_sections_whose_job_it_is(
        self, decision: str
    ) -> None:
        """Section-scoped: a document-wide check would pass while §C lost the record entirely."""
        for letter in ("C", "H"):
            section = _section(decision, letter)
            assert STEP10_DETERMINATION in section
            assert STEP10_EVIDENCE_COMMENT in section

    def test_it_is_recorded_as_a_completed_fact_and_not_re_performed(self, decision: str) -> None:
        section = _section(decision, "C")
        assert (
            "This decision records that determination as a completed fact and re-performs no part "
            "of it." in section
        )
        assert "does not re-run the comparison" in section
        assert "does not reopen either anchor" in section

    def test_the_step_10_unit_is_recorded_as_consumed(self, decision: str) -> None:
        section = _section(decision, "C")
        assert (
            "That unit is complete and consumed, and may not be rerun without new authority"
            in section
        )

    def test_the_clean_result_grants_nothing_here(self, decision: str) -> None:
        section = _section(decision, "C")
        assert (
            "the authority for step 11 comes from **this decision's own lifecycle** (§N) and from "
            "nowhere else" in section
        )

    def test_reopening_prior_determinations_is_prohibited(self, decision: str) -> None:
        section = _section(decision, "G")
        assert (
            "reopen, re-adjudicate, or overturn the completed step-9 `PASS` or the completed "
            "step-10 `STEP_10_NO_DRIFT`" in section
        )


# --------------------------------------------------------------------------------------------------
# 13. Protected boundaries preserved
# --------------------------------------------------------------------------------------------------


class TestProtectedBoundariesPreserved:
    @pytest.mark.parametrize(
        "prohibition",
        [
            "read, list, open, or substantively reuse any `risk_lane_boundary` protected `RISK` result",
            "acquire market, fundamental, economic, or Stage-2 data",
            "governance metadata only",
            "change `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`",
        ],
    )
    def test_each_protected_boundary_is_restated(self, decision: str, prohibition: str) -> None:
        assert prohibition in _section(decision, "G")

    def test_results_may_not_be_interpreted_applied_or_ranked(self, decision: str) -> None:
        section = _section(decision, "G")
        assert (
            "interpret, apply, aggregate, rank, or act on the results it produces" in section
        )
        assert (
            "no endpoint, bound, point, range, percentage, weight, rank, target, or allocation "
            "follows from the run" in section
        )

    def test_no_load_bearing_or_canonical_byte_may_be_edited(self, decision: str) -> None:
        section = _section(decision, "G")
        assert (
            "edit any load-bearing, canonical, validator, authorization, runner, "
            "result-production, universe, governance, or protected portfolio byte" in section
        )
        assert "the mechanism is used exactly as it stands" in section


# --------------------------------------------------------------------------------------------------
# 14. Effectivity requires complete lifecycle closure
# --------------------------------------------------------------------------------------------------


class TestEffectivityRequiresCompleteLifecycleClosure:
    @pytest.mark.parametrize(
        "condition",
        [
            "independent **FULL** exact-head review",
            "any required bounded correction and exact-head re-review",
            "explicit principal exact-head acceptance",
            "normal merge",
            "immediate post-merge verification",
            "successful merge-commit CI whose `head_sha` is the exact merge SHA",
            "final post-CI verification and lifecycle closure",
        ],
    )
    def test_each_of_the_seven_conditions_is_required(self, decision: str, condition: str) -> None:
        assert condition in _section(decision, "N")

    def test_no_single_step_is_sufficient(self, decision: str) -> None:
        section = _section(decision, "N")
        assert "**None is individually sufficient.**" in section
        assert "Opening this PR authorizes nothing" in section
        assert "principal acceptance does not; merge does not" in section
        assert "**Only complete closure of all seven does**" in section

    def test_even_full_closure_yields_a_unit_that_may_lawfully_arm_nothing(
        self, decision: str
    ) -> None:
        section = _section(decision, "N")
        assert (
            "a **future unit that must still satisfy every §H condition at the moment it acts**, "
            "and that may lawfully end without arming anything" in section
        )

    def test_the_six_required_lifecycle_gates_are_the_repository_constant(self) -> None:
        assert A.REQUIRED_LIFECYCLE_GATES == (
            "INDEPENDENT_FULL_EXACT_HEAD_REVIEW",
            "PRINCIPAL_EXACT_HEAD_ACCEPTANCE",
            "MERGE",
            "POST_MERGE_VERIFICATION",
            "MERGE_COMMIT_CI_SUCCESS",
            "MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION",
        )

    def test_register_gate_records_the_closed_lifecycle(self) -> None:
        """ADVANCED BY XASSET-0041. `in_progress` was the fact while PR #340 was open; it merged.

        This originally asserted `pr is None` (accurate only before PR #340 opened), then
        `in_progress` / `pr: 340` (accurate while it was live). PR #340 has since merged at
        `f212cce5`, closing XASSET-0040's own seven-condition lifecycle, so the gate lawfully
        advanced to `complete`. STRENGTHENED to the exact terminal value rather than relaxed: the
        gate narrative is separately asserted byte-identical below, so only `status` moved.
        """
        gate = _ws0014_gate("xasset0040-step11-activation-authorization")
        assert gate["status"] == "complete"
        assert gate["pr"] == 340

    def test_xasset0040_authorized_unit_ran_and_stopped_before_attestation(self) -> None:
        """ADDED BY XASSET-0041. The unit XASSET-0040 authorized ran and reached SS-K.1.

        Recording the terminal outcome is what makes the `complete` status above truthful: the
        lifecycle closed AND its single authorized unit is spent. `ATTEMPT_1` is still intact,
        because the unit stopped before attesting.
        """
        gate = _ws0014_gate("xasset0040-step11-unit-stopped-before-attestation")
        assert gate["status"] == "complete"
        assert gate["pr"] == 340
        assert "STOPPED_BEFORE_ATTESTATION" in gate["description"]
        assert "ATTEMPT_1 IS INTACT" in gate["description"]


# --------------------------------------------------------------------------------------------------
# 15. The filing changed nothing it must not change
# --------------------------------------------------------------------------------------------------


class TestNoProtectedByteWasTouched:
    def test_load_bearing_set_is_exactly_the_ten_bound_paths(self) -> None:
        assert tuple(sorted(A.LOAD_BEARING_RELPATHS)) == EXPECTED_LOAD_BEARING

    def test_every_load_bearing_path_exists(self) -> None:
        for relative in EXPECTED_LOAD_BEARING:
            assert (ROOT / relative).is_file(), relative

    def test_canonical_pins_match_their_files(self) -> None:
        assert hashlib.sha256(PROTOCOL.read_bytes()).hexdigest() == CURRENT_PROTOCOL_SHA256
        assert hashlib.sha256(PREREG.read_bytes()).hexdigest() == CURRENT_PREREG_SHA256

    def test_construction_universe_module_is_unchanged(self) -> None:
        digest = hashlib.sha256(
            (ROOT / "level1_construction_universe_closure_validator.py").read_bytes()
        ).hexdigest()
        assert digest == CONSTRUCTION_UNIVERSE_MODULE_SHA256

    def test_frozen_universe_is_unchanged(self) -> None:
        universe = CU.frozen_construction_universe()
        assert len(universe) == 680
        assert len({tuple(key.split("::")[:3]) for key in universe}) == 48
        assert CU.universe_aggregate_sha256() == FROZEN_UNIVERSE_SHA256

    def test_outcome_capable_modules_are_all_load_bearing(self) -> None:
        for module in OUTCOME_CAPABLE_MODULES:
            assert module in EXPECTED_LOAD_BEARING


# --------------------------------------------------------------------------------------------------
# 16. Catalog and register synchronisation
# --------------------------------------------------------------------------------------------------


class TestCatalogAndRegisterSynchronisation:
    def test_catalog_entry_is_present_and_points_at_the_real_file(self) -> None:
        entries = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["decisions"]
        entry = next(e for e in entries if e["decision_id"] == "XASSET-0040")
        assert entry["status"] == "Proposed"
        assert (ROOT / entry["file"]).is_file()
        assert entry["supporting_artifact"] == Path(__file__).name

    def test_catalog_entry_relates_to_its_immediate_predecessor(self) -> None:
        entries = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["decisions"]
        entry = next(e for e in entries if e["decision_id"] == "XASSET-0040")
        assert "XASSET-0039" in entry["related_decisions"]

    def test_prior_step10_gate_is_marked_complete_without_losing_its_history(self) -> None:
        gate = _ws0014_gate("xasset0039-step10-drift-fail-closed-authorization")
        assert gate["status"] == "complete"
        assert gate["pr"] == 339
        # The drafting session's own narrative is retained verbatim, not rewritten.
        assert "THIS FILING PERFORMS NO PART OF STEP 10" in gate["description"]
        assert "NEVER A REMEDIATOR" in gate["description"]

    def test_prior_gate_description_is_byte_identical_to_its_merged_form(self) -> None:
        """Only status and pr were factually corrected; the narrative text is untouched."""
        gate = _ws0014_gate("xasset0039-step10-drift-fail-closed-authorization")
        digest = hashlib.sha256(gate["description"].encode("utf-8")).hexdigest()
        assert digest == "595e05839eb7cb44d3c394863c3e046c884c5254a94e0d72764f5b015e0eb4c1"

    def test_post_merge_gate_records_the_step_10_determination(self) -> None:
        gate = _ws0014_gate("xasset0039-post-merge-verification")
        assert gate["status"] == "complete"
        assert gate["pr"] == 339
        assert XASSET0039_MERGE_SHA in gate["description"]
        assert XASSET0039_CLOSURE_COMMENT in gate["description"]
        assert STEP10_EVIDENCE_COMMENT in gate["description"]
        assert STEP10_DETERMINATION in gate["description"]
        assert "STEP 10 IS THEREFORE COMPLETE" in gate["description"]

    def test_step11_gate_states_the_non_authorization_boundary(self) -> None:
        description = _ws0014_gate("xasset0040-step11-activation-authorization")["description"]
        assert "THIS FILING PERFORMS NO PART OF STEP 11" in description
        assert "MERGING IT ARMS NOTHING" in description
        assert "RE-PERFORMS NO PART OF THE COMPLETED STEP 10" in description
        assert "ATTEMPT_1 IS ONE-SHOT" in description
        assert "NEVER ENTERS THE ATTESTATION" in description
        assert BOUND_MERGE_SHA in description
        assert STEP10_EVIDENCE_COMMENT in description

    def test_workstream_live_fields_reflect_this_session(self) -> None:
        data = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
        workstream = next(w for w in data["workstreams"] if w.get("id") == "WS-0014")
        # ADVANCED BY XASSET-0041. PR #340 merged at `f212cce5`, so the register's live
        # "where main is now" field lawfully advanced. The anchor this decision authorizes
        # against is unchanged; only the shared live self-reference moved.
        # ADVANCED BY XASSET-0049: this is the register's SHARED live field, so it names the
        # currently-live unit. Bound at BOTH ends -- every prior generation's value is a negative
        # pin, so a silent revert to finished work still fails here.
        assert workstream["last_verified_main_sha"] == XASSET0052_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0051_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0050_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0049_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0048_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0047_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0046_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0045_MAIN_SHA
        assert XASSET0039_MERGE_SHA != XASSET0043_MAIN_SHA
        # ADVANCED BY XASSET-0051, with the shared fields above: the register's single
        # shared verification date moved to this unit's own live preflight date. Bound at
        # BOTH ends -- the superseded date is a negative pin, so a silent revert fails.
        assert str(workstream["last_verified_date"]).startswith("2026-08-23")
        assert not str(workstream["last_verified_date"]).startswith("2026-08-22")
        # ADVANCED AGAIN BY XASSET-0042: PR #341 has merged, so WS-0014's single shared
        # `active_pr` now points at THIS correction unit's own pull request. Pinned to a
        # module constant, set from the real number GitHub issued rather than guessed.
        assert workstream["active_pr"] == XASSET0052_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0051_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0050_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0049_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0048_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0047_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0046_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0045_ACTIVE_PR

    def test_workstream_stays_secondary_and_no_primary_is_introduced(self) -> None:
        data = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
        workstream = next(w for w in data["workstreams"] if w.get("id") == "WS-0014")
        assert workstream["priority"] == "secondary"
        primary = [w["id"] for w in data["workstreams"] if w.get("priority") == "primary"]
        assert primary == []


# --------------------------------------------------------------------------------------------------
# 17. No section is unreachable, and the suite guards itself
# --------------------------------------------------------------------------------------------------


class TestNoSectionIsVacuous:
    @pytest.mark.parametrize("letter", ALL_SECTIONS)
    def test_every_section_exists_and_is_substantive(self, decision: str, letter: str) -> None:
        """A section reachable by no assertion could be weakened with nothing failing."""
        assert len(_section(decision, letter)) > 200

    def test_the_preflight_table_records_the_completed_step_10_facts(self, decision: str) -> None:
        """The preflight table is a factual record; it must not be silently falsifiable either.

        A §C-scoped guard alone leaves the table's own copy of these facts unpinned, which mutation
        M38 demonstrated: flipping the table's "complete and consumed" survived while §C's copy held.
        """
        preflight = _norm(decision.split("### The question this unit answers")[0])
        assert STEP10_EVIDENCE_COMMENT in preflight
        assert STEP10_DETERMINATION in preflight
        assert "unit **complete and consumed**" in preflight
        assert XASSET0039_MERGE_SHA in preflight
        assert XASSET0039_CLOSURE_COMMENT in preflight
        assert BOUND_MERGE_SHA in preflight
        assert "`new_execution_is_authorized()` **`False`**" in preflight
        assert "`ABSENT`, all four lane paths absent" in preflight

    def test_frontmatter_declares_this_file_as_the_supporting_artifact(self, decision: str) -> None:
        assert f"supporting_artifact: {Path(__file__).name}" in decision
        assert "decision_id: XASSET-0040" in decision
        assert "status: Proposed" in decision


class TestSuiteHygiene:
    def test_no_or_fallback_assertions(self) -> None:
        """``assert a or b`` passes when either half is true, hiding a broken half."""
        for node in ast.walk(_suite_ast_excluding_hygiene()):
            if isinstance(node, ast.Assert) and isinstance(node.test, ast.BoolOp):
                assert not isinstance(node.test.op, ast.Or), (
                    f"or-fallback assertion at line {node.lineno}"
                )

    def test_suite_performs_no_filesystem_write(self) -> None:
        """Detects real mutating *calls*, not source substrings, and not read-only ``.open``."""
        forbidden = {
            "write_text",
            "write_bytes",
            "mkdir",
            "makedirs",
            "touch",
            "unlink",
            "remove",
            "rmdir",
            "rmtree",
            "rename",
            "replace",
        }
        offenders = [
            f"{node.func.attr}:{node.lineno}"
            for node in ast.walk(_suite_ast_excluding_hygiene())
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in forbidden
        ]
        assert offenders == [], f"suite must not mutate the filesystem; found: {offenders}"

    def test_suite_never_references_a_protected_risk_result_path(self) -> None:
        """Scans string constants for the real protected results PATH.

        The governance term ``risk_lane_boundary`` legitimately appears in prose stating the
        prohibition, so scanning for it would flag the guard's own subject rather than a finding.
        The forensic root is the thing that must never be reachable from here.
        """
        needle = "phq-risk0001-results"
        offenders = [
            node.lineno
            for node in ast.walk(_suite_ast_excluding_hygiene())
            if isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and needle in node.value
        ]
        assert offenders == [], f"protected RISK results path referenced at lines {offenders}"

    def test_suite_evaluates_no_gate_and_arms_nothing(self) -> None:
        forbidden = {
            "run_stage1",
            "write_stage1_results",
            "claim_execution",
            "complete_execution",
            "write_authorization",
            "build_authorization_payload",
            "determined_gate_results",
            "serialize_stage1_results",
        }
        for node in ast.walk(_suite_ast_excluding_hygiene()):
            if isinstance(node, ast.Attribute):
                assert node.attr not in forbidden, f"activation call at line {node.lineno}"
            if isinstance(node, ast.Name):
                assert node.id not in forbidden, f"activation call at line {node.lineno}"
