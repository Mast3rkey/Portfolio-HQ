"""Adversarial tests pinning the ``XASSET-0038`` §G.B step-9 readiness-verification authorization.

``XASSET-0037``'s complete seven-condition lifecycle closed, so ``XASSET-0030`` §G.B **step 8** — the
one successor operational-authorization / load-bearing rebinding — is done. Step 9 is next, and it
had **no authority**: ``XASSET-0030`` §G.B authorizes none of itself, ``XASSET-0036`` §F withholds
"performing §G.B steps 8-11", and ``XASSET-0037`` §I withholds "steps 9, 10, or 11" **by name** while
its Consequences require separate authority for each. ``XASSET-0038`` closes that gap for step 9 and
nothing else.

The whole risk of an authorization filing is that it grants more than it says, or that a future
session reads more out of it than it contains. Every test below therefore pins **an authorized
boundary and its nearest plausible overreach** — the stronger permission a successor might infer from
the same text, which the decision must refuse.

The overreaches that matter most each have a dedicated guard:

1. **Step 9 performed now, or treated as authorized on filing.**
   ``TestStep9NotPerformedHere`` and ``TestEffectivityRequiresCompleteLifecycleClosure`` fail if the
   filing runs the checklist, issues a determination, or lets any single lifecycle step stand in for
   complete closure.
2. **Steps 10 and 11 read as included.** ``TestSteps10And11RetainSeparateAuthority`` fails if either
   is granted, implied, or made reachable by a step-9 ``PASS``.
3. **"Read-only" drifting into repair.** ``TestReadOnlyMeansReadOnly`` and
   ``TestFailClosed`` fail if the authorized unit may create, edit, regenerate or correct anything,
   may declare a defect "fixed", or may continue past drift or uncertainty.
4. **The closed checklist quietly reopening.** ``TestClosedReadinessChecklist`` fails if any of the
   eleven conditions is dropped, or if the list stops being closed.
5. **Arming by implication.** ``TestXasset0029NoRegressIntact`` fails if the filing presents itself
   as an activation PR, adds an activation authorization, or lets merge imply an armed Stage 1.
6. **Silent consumption of the reserved results PR.** ``TestP1ResultsPRRemainsSeparate``.

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

#: The exact PR #337 lifecycle identities this authorization anchors to, verified live in preflight.
MERGE_SHA = "637eaa30302f5a71f84ab1d215ecbd32c01399b5"
ACCEPTED_HEAD = "f40c816223c78f1d1e436b718455df5fb3d77fa7"
MERGE_BASE = "3e5de8f85c69c2e5dc2b75421446b5db996d7cf1"
MERGE_TREE = "a370ecb9f24ecbc1f1f83f31042990f706ead20c"

#: ADDED BY XASSET-0039 -- the PR #338 merge that carried this decision onto `main`. Distinct from
#: ``MERGE_SHA`` above, which remains the PR #337 bound merge this decision anchors its checklist to.
SUCCESSOR_MERGE_SHA = "b0361ce74dea357715b2ec2b4ce36b47c4f3cffc"

#: ADVANCED BY XASSET-0040 -- the PR #339 merge, which is where `main` is now. The register's live
#: "where main is now" field lawfully advances with each successor merge; this constant tracks it so
#: the assertion stays exact rather than being relaxed. Neither ``MERGE_SHA`` (this decision's own
#: anchor) nor ``SUCCESSOR_MERGE_SHA`` (its own merge) is changed by that advance.
CURRENT_MAIN_SHA = "5fbfc94d7333e552bd2654261e0c57134a172e31"
#: ADVANCED BY XASSET-0044: PR #343 merged at `0709d2f0`, so the register's shared live
#: "where main is now" field lawfully advanced again. The anchor this decision authorizes
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
XASSET0052_ACTIVE_PR = 353
#: ADVANCED BY XASSET-0053. PR #353 merged at `cc1d1b62...`, so WS-0014's shared live
#: "where main is now" / "which pull request is live" fields lawfully advanced again under
#: OPS-0001's Active-GitHub-fields rule. XASSET-0053 is a DESIGN-ONLY authorization: it changes
#: no module constant, so `REVIEWED_BASE_SHA` stays XASSET-0049's lawful rebinding base and only
#: the register's shared self-reference moved. Each prior generation's value is retained beside
#: the current one as a NEGATIVE pin rather than deleted, so a silent revert to any finished
#: unit's state still fails. The assertion stays EXACT and is bound at BOTH ends.
XASSET0053_MAIN_SHA = "cc1d1b62b8b48c7123b73e05e7ea04af89c89cd6"
#: Committed as an impossible sentinel first (-53), then replaced by the number GitHub actually
#: issued in a fast-forward follow-up commit. Never predicted. Distinct from every prior sentinel.
XASSET0053_ACTIVE_PR = 354
#: ADVANCED BY XASSET-0055. PR #354 merged at `683c3246...`, so WS-0014's shared live
#: "where main is now" / "which pull request is live" fields lawfully advanced again under
#: OPS-0001's Active-GitHub-fields rule. XASSET-0055 is a GOVERNANCE-ONLY authorization: it
#: changes no module constant and touches no production authorization code, so
#: `REVIEWED_BASE_SHA` stays XASSET-0049's lawful rebinding base and only the register's
#: shared self-reference moved. There is deliberately NO XASSET0054 generation: XASSET-0054's
#: pull request #355 was CLOSED UNMERGED after independent DELTA review 5010334966, so it
#: never became `main` state and has no merge SHA to pin. Each prior generation's value is
#: retained beside the current one as a NEGATIVE pin rather than deleted, so a silent revert
#: to any finished unit's state still fails. The assertion stays EXACT and is bound at BOTH
#: ends.
XASSET0055_MAIN_SHA = "683c324629544a84d2cf75ebca37325e3375c479"
#: Committed as an impossible sentinel first (-55), then replaced by the number GitHub actually
#: issued in a fast-forward follow-up commit. Never predicted. Distinct from every prior sentinel.
XASSET0055_ACTIVE_PR = 356

#: RE-ANCHORED BY XASSET-0056, the single replacement parser-correction implementation
#: XASSET-0055 §H authorized. `active_branch`, `active_pr` and `last_verified_main_sha` are
#: WS-0014's SINGLE SHARED live self-reference fields under OPS-0001's Active-GitHub-fields
#: rule, so they lawfully advance to whichever unit is live. The XASSET-0055 generation is
#: RETAINED below as a negative pin rather than deleted, so every field stays bound at BOTH
#: ends and a silent revert to ANY finished unit's state still fails here.
XASSET0056_MAIN_SHA = "29e4969885970d942a5acecc1424fb2e2b080d60"

#: ADVANCED BY XASSET-0057. WS-0014's SINGLE SHARED live self-reference field advances
#: with every generation; XASSET-0056's own value is retained above as a NEGATIVE pin, so
#: a silent revert to that finished unit's state still fails here.
XASSET0057_MAIN_SHA = "583022a5f2106d61f82d270edadd3520d8b0c55d"
#: Read back from the live pull request AFTER GitHub issued it, never predicted. The
#: branch's first commit carried the impossible sentinel -56 (negative, so structurally
#: cannot be a real pull-request number); this value replaced it in a fast-forward
#: follow-up commit, with no amend and no force-push.
XASSET0056_ACTIVE_PR = 357
XASSET0057_ACTIVE_PR = -57

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

#: The three values accepted authority already fixes as exact constants, and the only three
#: ``XASSET-0038`` restates. Everything else in its checklist derives from the merged tree.
PROTOCOL_SHA256 = "367583b616e1c6ab614bcf67d451fe27ce40507d073374190c57291e761d8971"
PREREG_SHA256 = "768b013c0129f02577fea3c2a1a3100b4340b9a42f48ee0d0dbd6e671894bce1"

#: ADDED BY XASSET-0044. The two constants above are what XASSET-0038's own ACCEPTED,
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

#: The ten paths ``XASSET-0037`` bound. ``XASSET-0038`` must change none of them.
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
    # EXTENDED AGAIN BY XASSET-0049 / XASSET-0048 SS-E, 16 -> 18: the step-8-EQUIVALENT successor
    # rebinding's own authority and the rebinding itself, both by DIRECT MEMBERSHIP. Nothing was
    # removed and no existing member changed, so the sorted EXACT comparison still catches a
    # removal, a swap, or a trade.
    "governance/decisions/"
    "XASSET-0048-endpoint-0001-stage-1-step-8-equivalent-rebinding-authorization.md",
    "governance/decisions/"
    "XASSET-0049-endpoint-0001-stage-1-step-8-equivalent-successor-operational-rebinding.md",
)))

#: The five Python modules inside those ten paths, each independently able to affect the 680
#: outcomes. ``XASSET-0038`` §G C3 names each individually rather than relying on C2's aggregate.
OUTCOME_CAPABLE_MODULES = (
    "level1_construction_universe_closure_validator.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_stage1_execution_authorization.py",
    "level1_stage1_result_validator.py",
    "level1_stage1_runner.py",
)


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
    """Return one top-level ``### <letter>.`` section body.

    Anchored at line start with exactly three hashes: a naive ``split("### F.")`` also matches
    inside a ``#### F.1`` sub-heading and would silently return a near-empty fragment, making any
    ``in`` assertion over it vacuous. The length floor makes that failure loud instead.
    """
    match = re.search(
        rf"^### {re.escape(letter)}\..*?(?=^### [A-Z]\.|^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match is not None, f"XASSET-0038 section {letter} not found"
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
    return D0038.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def norm(decision: str) -> str:
    return _norm(decision)


# --------------------------------------------------------------------------------------------------
# 1. The authority gap is real, and rests on accepted text rather than convenience
# --------------------------------------------------------------------------------------------------


class TestAuthorityGapIsGroundedInAcceptedText:
    def test_predecessors_actually_withhold_step_9(self) -> None:
        """The gap must be verifiable in the predecessors themselves, not merely asserted."""
        assert "performing §G.B steps 8–11" in _norm(D0036.read_text(encoding="utf-8"))
        norm_0037 = _norm(D0037.read_text(encoding="utf-8"))
        assert "`XASSET-0030` §G.B steps 9, 10, or 11" in norm_0037
        assert "each requires its own separate authority" in norm_0037
        assert (
            "This decision authorizes none of G.A or G.B" in _norm(D0030.read_text(encoding="utf-8"))
        )

    @pytest.mark.parametrize(
        "section, source, quote",
        [
            ("B", D0030, "**This decision authorizes none of G.A or G.B**, and performs no part of either."),
            ("B", D0036, "performing §G.B steps 8–11"),
            ("B", D0037, "`XASSET-0030` §G.B steps 9, 10, or 11"),
            ("B", D0037, "steps 9, 10, and 11 remain unperformed and unauthorized"),
            ("B", D0037, "each requires its own separate authority"),
            ("C", D0027, "may make no production configuration change"),
        ],
    )
    def test_every_quoted_predecessor_phrase_is_verbatim_in_its_source(
        self, decision: str, section: str, source: Path, quote: str
    ) -> None:
        """§B claims each predecessor was "read at its live merged bytes". Prove it both ways.

        A governance record that quotes its own authority is only as good as the quotation. This
        checks the phrase appears **in the citing section itself** — not merely somewhere in the
        decision, which an earlier draft did and which a mutation test showed was too weak, since
        several of these phrases also appear in the Context preamble — and **verbatim in the live
        predecessor file**. So a paraphrase that drifts from the source in the citation table, or a
        source edit that silently invalidates the citation, fails here rather than surviving as a
        plausible-looking quote. Markdown emphasis is preserved on both sides, not normalised away.
        """
        assert _norm(quote) in _norm(_section(decision, section)), (
            f"§{section} does not carry the quote verbatim: {quote}"
        )
        assert _norm(quote) in _norm(source.read_text(encoding="utf-8")), (
            f"quote is not verbatim in {source.name}: {quote}"
        )

    def test_decision_cites_each_withholding(self, decision: str) -> None:
        body = _norm(_section(decision, "B"))
        assert "XASSET-0036` §F" in body
        assert "XASSET-0037` §I" in body
        assert "Three filings named step 9 and three declined to grant it" in body

    def test_decision_does_not_claim_step_9_is_self_authorizing(self, decision: str) -> None:
        """The honest ground is the express withholding, not that read-only work needs no grant."""
        body = _norm(_section(decision, "B"))
        assert "A read-only unit is not automatically self-authorizing here" in body
        assert "does not rest on the weaker claim" in body


# --------------------------------------------------------------------------------------------------
# 2. This filing performs no part of step 9
# --------------------------------------------------------------------------------------------------


class TestStep9NotPerformedHere:
    def test_decision_states_it_performs_no_part_of_step_9(self, norm: str) -> None:
        assert "This decision performs no part of step 9" in norm
        assert "It runs no readiness checklist and issues no step-9 `PASS` or `FAIL`" in norm

    def test_determination_is_an_authorization_not_a_verification_result(self, norm: str) -> None:
        assert "STEP_9_READINESS_VERIFICATION_AUTHORIZED" in norm
        assert "It authorizes and defines; a later unit verifies" in norm

    def test_decision_issues_no_pass_or_fail_verdict(self, decision: str) -> None:
        """A step-9 determination would read as a verdict line; none may exist."""
        forbidden = (
            "STEP_9_PASS",
            "STEP 9 PASS",
            "READINESS VERIFIED",
            "READINESS_VERIFIED",
            "STEP_9_READINESS_PASS",
        )
        upper = decision.upper()
        assert not [phrase for phrase in forbidden if phrase in upper]

    def test_no_step_9_evidence_artifact_was_committed(self) -> None:
        """Step-9 evidence is externally posted; a committed artifact would mean it ran."""
        assert not (ROOT / "governance/audits/ENDPOINT0001_STEP9_READINESS.md").exists()
        assert not (ROOT / "step9_readiness.json").exists()
        assert not (ROOT / "governance/audits/ENDPOINT0001_STEP9_READINESS_VERIFICATION.md").exists()


# --------------------------------------------------------------------------------------------------
# 3. Effectivity — no single lifecycle step suffices
# --------------------------------------------------------------------------------------------------


class TestEffectivityRequiresCompleteLifecycleClosure:
    def test_all_seven_conditions_are_stated(self, decision: str) -> None:
        body = _norm(_section(decision, "J"))
        for phrase in (
            "independent **FULL** exact-head review",
            "exact-head re-review",
            "principal exact-head acceptance",
            "normal merge",
            "immediate post-merge verification",
            "successful merge-commit CI whose `head_sha` is the exact merge SHA",
            "final post-CI verification and lifecycle closure",
        ):
            assert phrase in body, f"missing effectivity condition: {phrase}"

    def test_no_single_condition_is_sufficient(self, decision: str) -> None:
        body = _norm(_section(decision, "J"))
        assert "**None is individually sufficient.**" in body
        assert "Opening this PR authorizes nothing" in body
        assert "a green PR-head CI run does not" in body
        assert "merge does not" in body
        assert "**Only complete closure of all seven does**" in body

    def test_effectivity_matches_the_repositorys_own_lifecycle_gate_count(self) -> None:
        """Six committed gates plus OPS-0009 §6's exact-head re-review discipline is seven."""
        assert len(A.REQUIRED_LIFECYCLE_GATES) == 6
        body = _norm(_section(D0038.read_text(encoding="utf-8"), "J"))
        assert "six `REQUIRED_LIFECYCLE_GATES`" in body

    def test_even_full_closure_yields_only_a_read_only_verification(self, decision: str) -> None:
        body = _norm(_section(decision, "J"))
        assert "what becomes authorized is a **read-only verification**" in body
        assert "never arming and never execution" in body

    # AMENDED BY XASSET-0039. This test asserted the state as of THIS FILING, whose own PR was
    # still open -- accurate then, and the same self-referential shape as the sibling tests below
    # that pin the PREDECESSOR (XASSET-0037) gate as merged. PR #338 has since merged with all
    # seven effectivity conditions closed, so the successor filing lawfully flipped this gate to
    # `complete` / 338, exactly as THIS session flipped the xasset0037 gate. Nothing is weakened:
    # the completed values are checked exactly, the gate's own DESCRIPTION TEXT is asserted
    # byte-preserved as history, and the successor's additive post-merge gate is checked to exist
    # rather than merely assumed.
    def test_the_register_records_the_step9_authorization_as_merged(self) -> None:
        gate = _ws0014_gate("xasset0038-step9-readiness-verification-authorization")
        assert gate["status"] == "complete"
        assert gate["pr"] == 338
        # The drafting session's own historical narrative is retained verbatim, not rewritten.
        assert "THIS FILING PERFORMS NO PART OF STEP 9" in gate["description"]
        assert "eleven conditions C1-C11" in gate["description"]
        # The successor records completion additively rather than by editing the text above.
        post_merge = _ws0014_gate("xasset0038-post-merge-verification")
        assert post_merge["status"] == "complete"
        assert post_merge["pr"] == 338
        assert "STEP_9_READINESS_VERIFICATION_PASS" in post_merge["description"]


# --------------------------------------------------------------------------------------------------
# 4. Steps 10 and 11 retain their own separate authority
# --------------------------------------------------------------------------------------------------


class TestSteps10And11RetainSeparateAuthority:
    def test_step_10_is_explicitly_withheld(self, decision: str) -> None:
        body = _norm(_section(decision, "K"))
        assert "**Step 10**" in body
        assert "retains its own separate-authority requirement" in body
        assert "is not authorized here" in body

    def test_step_11_is_explicitly_withheld_and_enumerated(self, decision: str) -> None:
        body = _norm(_section(decision, "K"))
        assert "**Step 11**" in body
        assert "the external one-shot attestation, arming, the claim, and the 680-construction run" in body
        assert "entirely outside this filing" in body

    def test_a_step_9_pass_authorizes_nothing_further(self, decision: str) -> None:
        """The single most likely misreading: treating a clean check as permission to arm."""
        body = _norm(_section(decision, "K"))
        assert "**authorizes nothing further.**" in body
        assert "it is not permission to arm, to claim, or to execute" in body

    def test_fail_closed_stop_rule_is_not_a_grant_of_step_10(self, decision: str) -> None:
        body = _norm(_section(decision, "K"))
        assert "it is not a grant of step 10" in body

    def test_authority_withheld_bars_performing_or_authorizing_steps_10_and_11(
        self, decision: str
    ) -> None:
        body = _norm(_section(decision, "F"))
        assert "**perform or authorize `XASSET-0030` §G.B step 10 or step 11.**" in body

    def test_non_authorization_section_repeats_the_bar(self, decision: str) -> None:
        body = _norm(_section(decision, "L"))
        assert "performs no part of §G.B step 9 and no part of steps 10 or 11" in body


# --------------------------------------------------------------------------------------------------
# 5. Read-only means read-only
# --------------------------------------------------------------------------------------------------


class TestReadOnlyMeansReadOnly:
    def test_grant_is_strictly_read_only_and_anchored(self, decision: str) -> None:
        body = _norm(_section(decision, "A"))
        assert (
            "**strictly read-only execution-readiness verification of already-reviewed, already-bound bytes**"
            in body
        )
        assert MERGE_SHA in body
        assert ACCEPTED_HEAD in body

    def test_every_prohibited_mutation_class_is_named(self, decision: str) -> None:
        body = _norm(_section(decision, "F"))
        for token in (
            "canonical",
            "validator",
            "authorization",
            "runner",
            "result-production",
            "universe",
            "governance",
            "protected portfolio",
        ):
            assert token in body, f"prohibited mutation class not named: {token}"
        assert "create, edit, regenerate, correct, reformat, or re-pin" in body

    def test_declaring_a_defect_fixed_is_barred(self, decision: str) -> None:
        body = _norm(_section(decision, "F"))
        assert '**declare any defect "fixed"**' in body
        assert "never work to perform" in body

    def test_outcome_producing_acts_are_barred(self, decision: str) -> None:
        body = _norm(_section(decision, "F"))
        for phrase in (
            "produce an attestation",
            "`AUTHORIZATION_ROOT`",
            "lane state",
            "a claim",
            "a ledger entry",
            "create `stage1_results.yaml`",
            "**evaluate or decide any gate (`G1`–`G12`) for any registered construction**",
            "consume any part of\n`ATTEMPT_1`",
        ):
            normalised = _norm(phrase)
            assert normalised in body, f"prohibition missing: {phrase}"

    def test_protected_risk_results_are_barred(self, decision: str) -> None:
        body = _norm(_section(decision, "F"))
        assert "read, list, open, or substantively reuse any `risk_lane_boundary` protected `RISK` result" in body

    def test_f1_adopts_the_existing_boundary_without_widening_it(self, decision: str) -> None:
        body = _norm(_section(decision, "F"))
        assert "traversing frozen construction identities is not execution" in body
        assert "applying gate-evaluation semantics to them to derive Stage-1 outcomes" in body
        assert "step 9 is permitted to write nothing at all" in body

    def test_grant_reuses_rather_than_rewrites_the_traversal_permission(self, decision: str) -> None:
        body = _norm(_section(decision, "E"))
        assert "by reference and does not widen by one step" in body

    def test_real_680_run_remains_absolutely_prohibited(self, decision: str) -> None:
        body = _norm(_section(decision, "F"))
        assert "**An actual Stage-1 run over the real 680 remains absolutely prohibited**" in body


# --------------------------------------------------------------------------------------------------
# 6. The closed readiness checklist
# --------------------------------------------------------------------------------------------------


class TestClosedReadinessChecklist:
    def test_checklist_declares_itself_closed(self, decision: str) -> None:
        body = _norm(_section(decision, "G"))
        assert "**Closed**" in body
        assert "adds no further condition of its own invention" in body
        assert "a finding to report, not a checklist item to add" in body

    def test_all_eleven_conditions_are_present_and_numbered(self, decision: str) -> None:
        body = _section(decision, "G")
        found = re.findall(r"\*\*C(\d+)\*\*", body)
        assert [int(n) for n in found] == list(range(1, 12)), f"checklist ids: {found}"

    @pytest.mark.parametrize(
        "condition, phrase",
        [
            ("C1", "zero post-review and post-merge drift"),
            ("C2", "All **10** `LOAD_BEARING_RELPATHS` match the effective bound merge"),
            ("C3", "preregistration derivation module"),
            ("C4", "V7 canonical pins unchanged"),
            ("C5", "Frozen universe exactly **680** constructions, **48** cells"),
            ("C6", "Construction-universe module SHA-256"),
            ("C7", "without executing Stage 1"),
            ("C8", "fail-closed while no attestation exists"),
            ("C9", "Lane state remains `ABSENT`"),
            ("C10", "No output and no persistent execution artifact is created"),
            ("C11", "without a repository mutation"),
        ],
    )
    def test_each_condition_states_its_substance(
        self, decision: str, condition: str, phrase: str
    ) -> None:
        body = _norm(_section(decision, "G"))
        assert _norm(phrase) in body, f"{condition} substance missing: {phrase}"

    def test_c3_names_all_five_outcome_capable_modules(self, decision: str) -> None:
        body = _norm(_section(decision, "G"))
        for label in (
            "**runner**",
            "**result validator**",
            "**preregistration derivation module**",
            "**construction-universe module**",
            "**execution-authorization module**",
        ):
            assert label in body, f"C3 does not name {label}"

    def test_the_three_restated_constants_are_exactly_the_ones_authority_fixes(
        self, decision: str
    ) -> None:
        body = _norm(_section(decision, "G"))
        assert PROTOCOL_SHA256[:8] in body
        assert PREREG_SHA256[:8] in body
        assert FROZEN_UNIVERSE_SHA256 in body
        assert CONSTRUCTION_UNIVERSE_MODULE_SHA256 in body
        assert "**C4, C5 and C6 are the only constants this decision restates**" in body

    def test_identity_derives_from_the_merged_tree_not_from_this_record(
        self, decision: str
    ) -> None:
        """A restated module hash would be a second source of truth that can silently diverge."""
        body = _norm(_section(decision, "G"))
        assert "derived from the merged tree at verification time" in body
        assert "can never become a stale second source of truth" in body

    def test_no_module_hash_other_than_the_authorized_constant_is_restated(
        self, decision: str
    ) -> None:
        """Guard against the record accreting hashes it is not authorised to fix."""
        hashes = set(re.findall(r"\b[0-9a-f]{64}\b", decision))
        assert hashes <= {
            PROTOCOL_SHA256,
            PREREG_SHA256,
            FROZEN_UNIVERSE_SHA256,
            CONSTRUCTION_UNIVERSE_MODULE_SHA256,
        }, f"unexpected full hashes restated: {hashes}"


# --------------------------------------------------------------------------------------------------
# 7. Fail-closed
# --------------------------------------------------------------------------------------------------


class TestFailClosed:
    def test_every_trigger_class_stops_the_unit(self, decision: str) -> None:
        body = _norm(_section(decision, "H"))
        for trigger in (
            "drift",
            "missing identity",
            "validation failure",
            "unexpected lane state",
            "state the unit cannot determine with certainty",
        ):
            assert trigger in body, f"fail-closed trigger missing: {trigger}"

    def test_the_four_required_responses_are_stated(self, decision: str) -> None:
        body = _norm(_section(decision, "H"))
        assert "**stop**" in body
        assert "**report** the exact condition" in body
        assert "**change nothing**" in body
        assert "**not** issue a step-9 `PASS`" in body

    def test_a_defect_requires_separately_authorized_correction_and_redone_rebinding(
        self, decision: str
    ) -> None:
        body = _norm(_section(decision, "H"))
        assert "**A defect found at step 9 requires a separately authorized correction**" in body
        assert "any rebinding invalidated by that correction must itself be redone" in body

    def test_uncertainty_is_failure(self, decision: str) -> None:
        body = _norm(_section(decision, "H"))
        assert "**Uncertainty is failure.**" in body
        assert "may not resolve an ambiguous state in favour of readiness" in body

    def test_prohibition_is_not_relaxed_by_finding_a_defect(self, decision: str) -> None:
        body = _norm(_section(decision, "H"))
        assert "not relaxed by the discovery of a defect" in body


# --------------------------------------------------------------------------------------------------
# 8. Evidence is external, and creates no repository mutation
# --------------------------------------------------------------------------------------------------


class TestEvidenceIsExternalAndNonMutating:
    def test_unit_creates_no_branch_commit_or_pr(self, decision: str) -> None:
        body = _norm(_section(decision, "I"))
        assert "creates **no branch, no commit, and no pull request**" in body
        assert "makes **no repository mutation**" in body

    def test_unit_does_not_contend_for_the_single_mutation_lane(self, decision: str) -> None:
        body = _norm(_section(decision, "I"))
        assert "does not contend for the `OPS-0014` §D single mutation" in body

    def test_a_mutation_to_record_the_result_is_not_authorized(self, decision: str) -> None:
        body = _norm(_section(decision, "I"))
        assert "neither required nor authorized" in body
        assert "a finding to report under §H, not scope to assume" in body


# --------------------------------------------------------------------------------------------------
# 9. XASSET-0029 §E's activation regress stays intact
# --------------------------------------------------------------------------------------------------


class TestXasset0029NoRegressIntact:
    def test_filing_adds_zero_activation_authorizations(self, decision: str) -> None:
        body = _norm(_section(decision, "D"))
        assert "adds **zero** activation authorizations" in body
        assert "generates **no** attestation and authorizes none" in body

    def test_merging_does_not_arm_stage_1(self, decision: str) -> None:
        body = _norm(_section(decision, "D"))
        assert (
            "**merging this decision authorizes a future read-only verification only — it does not make Stage 1 armed or executable.**"
            in body
        )

    def test_final_activation_stays_the_runtime_operator_act(self, decision: str) -> None:
        body = _norm(_section(decision, "D"))
        assert (
            "the external one-shot runtime attestation and the operator's act — not a merged activation PR"
            in body
        )

    def test_executable_flag_stays_false(self, decision: str) -> None:
        body = _norm(_section(decision, "D"))
        assert "`stage_1_executability.executable` permanently `false`" in body
        block = yaml.safe_load(PREREG.read_text(encoding="utf-8"))["stage_1_executability"]
        assert block["executable"] is False
        assert block["executable_is_never_the_authorization_source"] is True

    def test_no_committed_value_authorizes_execution(self, decision: str) -> None:
        body = _norm(_section(decision, "D"))
        assert "**No committed value in this repository authorizes Stage-1 execution**" in body


# --------------------------------------------------------------------------------------------------
# 10. XASSET-0027 §P.1 remains reserved and unspent
# --------------------------------------------------------------------------------------------------


class TestP1ResultsPRRemainsSeparate:
    def test_p1_is_not_consumed(self, decision: str) -> None:
        body = _norm(_section(decision, "C"))
        assert "**not consumed, replaced, amended, or counted against**" in body
        assert "**one, unspent.**" in body

    def test_the_three_distinguishing_grounds_are_stated(self, decision: str) -> None:
        body = _norm(_section(decision, "C"))
        assert "delivers a **results document**" in body
        assert "sits **after arming**" in body
        assert "**no repository change at all**" in body


# --------------------------------------------------------------------------------------------------
# 11. This filing mutates nothing load-bearing — proven against live state, not asserted
# --------------------------------------------------------------------------------------------------


class TestThisFilingMutatesNothingLoadBearing:
    def test_load_bearing_set_is_exactly_the_ten_xasset_0037_bound(self) -> None:
        assert set(A.LOAD_BEARING_RELPATHS) == set(EXPECTED_LOAD_BEARING)
        # EXTENDED BY XASSET-0044, 10 -> 14, by direct membership; nothing removed.
        # EXTENDED AGAIN BY XASSET-0047, 14 -> 16, likewise by direct membership and likewise
        # removing nothing. The exact set equality above is the load-bearing check and is
        # unchanged in kind; this count is bound at BOTH ends so neither a silent shrink back to
        # the previous size nor an unexplained further growth passes.
        # EXTENDED AGAIN BY XASSET-0049, 16 -> 18, additively and by direct membership. Bound
        # at BOTH ends so neither a silent shrink back nor an unexplained further growth passes.
        assert len(A.LOAD_BEARING_RELPATHS) == 18
        assert len(A.LOAD_BEARING_RELPATHS) != 16
        assert len(A.LOAD_BEARING_RELPATHS) != 14

    @pytest.mark.parametrize("relative", EXPECTED_LOAD_BEARING)
    def test_each_load_bearing_path_still_exists(self, relative: str) -> None:
        assert (ROOT / relative).is_file()

    def test_canonical_bytes_match_the_effective_v7_pins(self) -> None:
        assert hashlib.sha256(PROTOCOL.read_bytes()).hexdigest() == CURRENT_PROTOCOL_SHA256
        assert hashlib.sha256(PREREG.read_bytes()).hexdigest() == CURRENT_PREREG_SHA256
        # RE-POINTED BY XASSET-0044: the module's EFFECTIVE pins describe the live files, which
        # the post-correction rebinding lawfully amended in lockstep. XASSET-0037's superseded
        # pins are retained on the module and asserted here as history, so nothing is lost.
        assert A.CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH] == CURRENT_PROTOCOL_SHA256
        assert A.CANONICAL_PINS[A.CANONICAL_PREREGISTRATION_RELPATH] == CURRENT_PREREG_SHA256
        assert A.XASSET_0037_CANONICAL_PINS[A.CANONICAL_PROTOCOL_RELPATH] == PROTOCOL_SHA256
        assert A.XASSET_0037_CANONICAL_PINS[A.CANONICAL_PREREGISTRATION_RELPATH] == PREREG_SHA256

    def test_construction_universe_module_identity_unchanged(self) -> None:
        module_path = ROOT / "level1_construction_universe_closure_validator.py"
        digest = hashlib.sha256(module_path.read_bytes()).hexdigest()
        assert digest == CONSTRUCTION_UNIVERSE_MODULE_SHA256

    def test_frozen_universe_is_unchanged(self) -> None:
        data = yaml.safe_load(PREREG.read_text(encoding="utf-8"))
        closure = data["construction_universe_closure"]
        assert closure["registered_construction_count"] == 680
        assert closure["construction_universe_sha256"] == FROZEN_UNIVERSE_SHA256
        assert data["trial_inventory"]["derived_cells"] == 48

    def test_frozen_universe_traversal_still_yields_680_and_48(self) -> None:
        """Read-only structural traversal under XASSET-0036 §F.1(a); no gate is evaluated."""
        universe = CU.frozen_construction_universe()
        assert len(universe) == 680
        assert CU.universe_aggregate_sha256() == FROZEN_UNIVERSE_SHA256
        per_cell = CU.per_cell_cardinality()
        assert len(per_cell) == 48
        assert sum(per_cell.values()) == 680

    def test_lane_state_absent_and_execution_unauthorized(self) -> None:
        paths = A.LanePaths(A.AUTHORIZATION_PATH, A.CLAIM_PATH, A.COMPLETION_PATH, A.LEDGER_PATH)
        state, _reason = A.lane_state_at(paths)
        assert state == A.LANE_ABSENT
        assert not A.AUTHORIZATION_ROOT.exists()
        assert not A.AUTHORIZATION_PATH.exists()
        assert not A.CLAIM_PATH.exists()
        assert not A.COMPLETION_PATH.exists()
        assert not A.LEDGER_PATH.exists()
        authorized, _ = A.new_execution_is_authorized()
        assert authorized is False

    def test_no_real_stage1_results_document_exists(self) -> None:
        assert not (ROOT / "stage1_results.yaml").exists()
        assert not (ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()

    def test_decision_declares_it_mutates_nothing_load_bearing(self, decision: str) -> None:
        body = _norm(_section(decision, "L"))
        assert "changes no `LOAD_BEARING_RELPATHS`, no canonical file, and no hash pin" in body
        assert (
            "creates no `stage1_results.yaml` and no runner, result validator, or other outcome-producing code"
            in body
        )

    def test_decision_declares_stage_1_still_unarmed(self, norm: str) -> None:
        assert "Stage 1 remains UNARMED and NOT EXECUTABLE" in norm
        assert "`ATTEMPT_1` is intact, unclaimed, and unconsumed" in norm


# --------------------------------------------------------------------------------------------------
# 12. Catalog and register synchronisation are factual
# --------------------------------------------------------------------------------------------------


class TestCatalogAndRegisterSynchronisation:
    def test_catalog_entry_is_present_and_points_at_the_real_file(self) -> None:
        entries = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["decisions"]
        matches = [e for e in entries if e["decision_id"] == "XASSET-0038"]
        assert len(matches) == 1
        entry = matches[0]
        assert entry["status"] == "Proposed"
        assert entry["category"] == "cross_asset_allocation_architecture"
        assert entry["supporting_artifact"] == Path(__file__).name
        assert (ROOT / entry["file"]).is_file()
        assert entry["file"] == str(D0038.relative_to(ROOT))

    def test_catalog_entry_relates_to_its_immediate_predecessor(self) -> None:
        entries = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["decisions"]
        entry = next(e for e in entries if e["decision_id"] == "XASSET-0038")
        for required in ("XASSET-0030", "XASSET-0036", "XASSET-0037", "OPS-0007", "OPS-0009"):
            assert required in entry["related_decisions"]

    def test_pr337_post_merge_gate_records_the_verified_identities(self) -> None:
        gate = _ws0014_gate("xasset0037-post-merge-verification")
        assert gate["status"] == "complete"
        assert gate["pr"] == 337
        for identity in (MERGE_SHA, ACCEPTED_HEAD, MERGE_BASE, MERGE_TREE, "32198881652"):
            assert identity in gate["description"], f"missing identity in gate: {identity}"

    def test_prior_rebinding_gate_is_marked_complete_without_losing_its_history(self) -> None:
        gate = _ws0014_gate("xasset0037-successor-operational-rebinding")
        assert gate["status"] == "complete"
        assert gate["pr"] == 337
        assert "STEP 8" in gate["description"]

    def test_step9_gate_states_the_non_authorization_boundary(self) -> None:
        gate = _ws0014_gate("xasset0038-step9-readiness-verification-authorization")
        body = gate["description"]
        assert "PERFORMS NO PART OF STEP 9" in body
        assert "NO PART OF STEP 10 OR STEP 11" in body
        assert "DOES NOT MAKE STAGE 1 ARMED" in body

    def test_workstream_live_fields_reflect_this_session(self) -> None:
        data = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
        workstream = next(w for w in data["workstreams"] if w.get("id") == "WS-0014")
        # AMENDED BY XASSET-0039, ADVANCED AGAIN BY XASSET-0040. This originally pinned the PR #337
        # merge -- live `main` while THIS filing was drafted -- then the PR #338 merge. PR #339 has
        # since merged, so the register's live self-reference lawfully advanced again. The anchor
        # this decision authorizes against is unchanged and is still `MERGE_SHA`, and its own merge
        # is still `SUCCESSOR_MERGE_SHA`; only the register's "where main is now" field moved.
        # ADVANCED BY XASSET-0049: this is the register's SHARED live field, so it names the
        # currently-live unit. Bound at BOTH ends -- every prior generation's value is a negative
        # pin, so a silent revert to finished work still fails here.
        assert workstream["last_verified_main_sha"] == XASSET0057_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0056_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0055_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0053_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0052_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0051_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0050_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0049_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0048_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0047_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0046_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0045_MAIN_SHA
        assert MERGE_SHA != CURRENT_MAIN_SHA
        assert SUCCESSOR_MERGE_SHA != CURRENT_MAIN_SHA
        # ADVANCED BY XASSET-0051, with the shared fields above. Bound at BOTH ends.
        # ADVANCED BY XASSET-0053, with the shared fields above: PR #353 merged and the
        # register's shared live self-reference moved onto this successor unit. Every
        # prior generation is retained as a NEGATIVE pin, so the field stays bound at
        # BOTH ends and a silent revert to finished work still fails.
        assert str(workstream["last_verified_date"]).startswith("2026-08-26")
        assert not str(workstream["last_verified_date"]).startswith("2026-08-24")
        assert not str(workstream["last_verified_date"]).startswith("2026-08-23")
        assert not str(workstream["last_verified_date"]).startswith("2026-08-22")
        # ADVANCED AGAIN BY XASSET-0042: PR #341 has merged, so WS-0014's single shared
        # `active_pr` now points at THIS correction unit's own pull request. Pinned to a
        # module constant, set from the real number GitHub issued rather than guessed.
        assert workstream["active_pr"] == XASSET0057_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0056_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0055_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0053_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0052_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0051_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0050_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0049_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0048_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0047_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0046_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0045_ACTIVE_PR


# --------------------------------------------------------------------------------------------------
# Suite hygiene — guards that make the assertions above non-vacuous
# --------------------------------------------------------------------------------------------------


class TestSuiteHygiene:
    def test_no_assertion_uses_an_or_fallback(self) -> None:
        """An ``assert a or b`` survives mutation of ``a`` and silently stops testing it.

        This suite carries **zero**. Every needle is matched against the whitespace-and-blockquote
        normalised text, so no wrap-tolerance fallback is needed — and an earlier draft that used
        such pairs had thirteen dead branches whose newline-bearing needle could never match a
        normalised body, which is precisely how a weakened clause hides.
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

        A substring scan would match the guard's own pattern list, so this walks the AST for actual
        mutating calls instead — also the stronger check, since it cannot be evaded by aliasing the
        call through a differently-spelled name.
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
            "rename",
            "replace",
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

    def test_suite_evaluates_no_gate_for_any_construction(self) -> None:
        """Structural traversal is authorized; gate evaluation is not, and never appears here."""
        forbidden_calls = {
            "evaluate_gate",
            "evaluate_gates",
            "derive_disposition",
            "derive_cell_outcome",
            "run_stage1",
            "execute_stage1",
            "write_results",
        }
        offenders = [
            (node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id)
            for node in ast.walk(_suite_ast_excluding_hygiene())
            if isinstance(node, ast.Call)
            and (
                (isinstance(node.func, ast.Attribute) and node.func.attr in forbidden_calls)
                or (isinstance(node.func, ast.Name) and node.func.id in forbidden_calls)
            )
        ]
        assert not offenders, f"suite must evaluate no gate; found calls: {offenders}"

    def test_section_extractor_is_not_vacuous(self, decision: str) -> None:
        """If ``_section`` ever silently returned a fragment, every ``in`` assertion would pass."""
        for letter in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"):
            body = _section(decision, letter)
            assert len(body) > 200
            assert body.lstrip().startswith(f"### {letter}.")

    def test_norm_helper_actually_collapses_wraps(self) -> None:
        """If ``_norm`` were a no-op, every wrapped-phrase assertion above would be vacuous."""
        assert _norm("a\n   b") == "a b"
        assert _norm("> quoted\n> text") == " quoted text"

    def test_decision_file_declares_this_module_as_its_supporting_artifact(
        self, decision: str
    ) -> None:
        assert f"supporting_artifact: {Path(__file__).name}" in decision
