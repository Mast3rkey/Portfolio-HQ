"""Adversarial tests pinning the ``XASSET-0044`` post-correction operational rebinding.

``XASSET-0043`` §F authorized **exactly one** future rebinding unit and performed no part of it.
This is that unit, and this suite exists to make the ways it could go wrong fail loudly rather
than quietly:

1. **Step 8 claimed a second time**, or ``XASSET-0037`` treated as invalidated.
   ``TestStep8IsNotReconsumed`` -- the single most easily-flattered claim here.
2. **An identity family overloaded** rather than kept separate, so a rebinding starts binding the
   wrong tree. ``TestFiveDistinctIdentities``.
3. **The trust boundary shrunk, or grown by an asserted equivalence rather than direct
   membership.** ``TestTrustBoundaryGrowsByDirectMembership``.
4. **The appended transition loosening the first link** instead of adding a second.
   ``TestTheChainIsAppendedNotReplaced``.
5. **The canonical amendment widening past authorization language**, or the universe moving.
   ``TestCanonicalAmendmentIsAuthorizationLanguageOnly`` and ``TestOutcomeSurfaceIsUnchanged``.
6. **A guard weakened rather than re-anchored** while resolving the ``XASSET-0042`` hand-off.
   ``TestXasset0042HandoffIsResolvedNotWeakened``.
7. **Merging read as arming**, ``ATTEMPT_1`` reached, or a downstream link made reachable.
   ``TestNotAnActivation`` and ``TestNothingDownstreamIsAuthorized``.
8. **Pins recomputed early**, or a successor pin equal to a predecessor's.
   ``TestPinsAreCurrentAndSuccessionIsRefused``.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No attestation, claim, completion, lane directory, or ledger entry is created or
read for authorization purposes. No ``risk_lane_boundary`` protected result path is read, listed,
opened, or referenced. ``write_authorization`` is never called.
"""

from __future__ import annotations

import ast
import hashlib
import re
import subprocess
from pathlib import Path

import pytest
import yaml

import level1_stage1_execution_authorization as A
import level1_endpoint_evidence_preregistration_validator as PREREG
# The accepted production harness -- injectable git/GitHub stand-ins -- so the bounded
# correction below exercises validate_authorization_document itself, not a private helper.
import test_level1_stage1_execution_authorization as H

ROOT = Path(__file__).resolve().parent

DECISION_ID = "XASSET-0044"
DECISION_RELPATH = (
    "governance/decisions/"
    "XASSET-0044-endpoint-0001-stage-1-post-correction-operational-rebinding.md"
)
DECISION_PATH = ROOT / DECISION_RELPATH
CATALOG_PATH = ROOT / "governance/decisions.yaml"
REGISTER_PATH = ROOT / "operations/WORKSTREAMS.yaml"

AUTH_MODULE_RELPATH = "level1_stage1_execution_authorization.py"
DERIVATION_RELPATH = "level1_endpoint_evidence_preregistration_validator.py"
PROTOCOL_RELPATH = "research/level1_endpoint_evidence/PROTOCOL_V1.md"
PREREG_RELPATH = "research/level1_endpoint_evidence/pre_registration.yaml"

#: The ten paths XASSET-0037 bound. Written literally, never imported, so this file independently
#: pins BOTH the predecessor membership and the count of ten.
XASSET_0037_LOAD_BEARING = (
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
)

#: The four this rebinding adds, by DIRECT MEMBERSHIP.
BOUNDARY_ADDITIONS = (
    "governance/decisions/"
    "XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md",
    "governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md",
    "governance/decisions/"
    "XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md",
    DECISION_RELPATH,
)

#: ADDED BY XASSET-0047. Its own two additions to the trust boundary, named explicitly so that
#: THIS decision's four can still be asserted EXACTLY -- as a set difference -- rather than
#: relaxed into a subset test that any future growth would satisfy.
XASSET_0047_DECISION_RELPATH = (
    "governance/decisions/"
    "XASSET-0047-endpoint-0001-stage-1-post-merge-ci-recovery-reconciliation.md"
)
XASSET_0047_BOUNDARY_ADDITIONS = (
    "governance/decisions/"
    "XASSET-0046-endpoint-0001-stage-1-post-merge-ci-recovery-reauthorization.md",
    XASSET_0047_DECISION_RELPATH,
)

#: ADDED BY XASSET-0049, for exactly the reason XASSET-0047's own block gives: its two additions
#: are named explicitly so THIS decision's four can still be asserted EXACTLY as a set difference,
#: rather than relaxed into a subset test that any future growth would satisfy.
XASSET_0049_DECISION_RELPATH = (
    "governance/decisions/"
    "XASSET-0049-endpoint-0001-stage-1-step-8-equivalent-successor-operational-rebinding.md"
)
XASSET_0049_BOUNDARY_ADDITIONS = (
    "governance/decisions/"
    "XASSET-0048-endpoint-0001-stage-1-step-8-equivalent-rebinding-authorization.md",
    XASSET_0049_DECISION_RELPATH,
)
#: The authorization module's exact bytes at XASSET-0047's own merge -- the identity THAT unit
#: recorded, immutable, and therefore still true after a lawful successor rebinding.
XASSET_0047_FINAL_MODULE_SHA256 = (
    "e5b509ca74734bffea788d4e7499699356395216285e941164ccf21b6159c924"
)

#: The bytes this rebinding is measured against. Its own base is the XASSET-0043 merge.
PR_BASE_SHA = "0709d2f05ab031ecb6f69c40465ed4a227983aed"
#: ADDED BY XASSET-0045: the register's shared live "where main is now" field after
#: THIS decision's own pull request merged. Distinct from PR_BASE_SHA above, which
#: remains this decision's own unchanged closed anchor.
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
#: ADVANCED BY XASSET-0049: PR #348 merged at `f052efad`, so the register's shared "where main is
#: now" field lawfully advanced again under OPS-0001's Active-GitHub-fields rule. Each prior value
#: is retained beside it as a negative pin rather than deleted.
XASSET0049_MAIN_SHA = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"
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
#: An IMPOSSIBLE sentinel until GitHub issues the real number, which is then bound in a
#: fast-forward follow-up commit. Never predicted.
XASSET0056_ACTIVE_PR = -56


#: A real, immutable historical commit pair across which a protected path GENUINELY changed --
#: PR #342's base and merge -- so the base->head comparison can never pass vacuously.
PROTECTED_CHANGE_CONTROL_BEFORE = "9c8647f9dddacdf63825f569097214ba65299fe8"
PROTECTED_CHANGE_CONTROL_AFTER = "5fbfc94d7333e552bd2654261e0c57134a172e31"
PROTECTED_CHANGE_CONTROL_PATH = AUTH_MODULE_RELPATH

#: Portfolio and allocator bytes a Level-1 rebinding must never touch.
PORTFOLIO_RELPATHS = (
    "allocate.py",
    "margin_state.py",
    "levels.py",
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
)

#: Identities, each independently recomputable and each distinct from every other.
BOUND_MODULE_SHA256 = "8186a50f71d05bbb7189183bacad6aa0752147e9c7f4e1f5b3bacabad91f2fc8"
INTERMEDIATE_MODULE_SHA256 = (
    "03d842126913bf2d62aa5d7c070ecca236926ec847102da82414ee51e7422734"
)
XASSET_0042_FINAL_MODULE_SHA256 = (
    "749597ee9085a189e187e23ccffb7718d98860847dfe514c173e7437b50f24c7"
)

#: The accepted successor blob -- link 1's endpoint and link 2's starting bytes.
SUCCESSOR_DERIVATION_SHA256 = (
    "2b8ead2b0d661ddd14fa6019ee1802fe49900a214ec443228636701edeb3d356"
)
UNIVERSE_HASH = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"

XASSET_0037_PROTOCOL_PIN = (
    "367583b616e1c6ab614bcf67d451fe27ce40507d073374190c57291e761d8971"
)
XASSET_0037_PREREG_PIN = (
    "768b013c0129f02577fea3c2a1a3100b4340b9a42f48ee0d0dbd6e671894bce1"
)

GATE_SELF = "xasset0044-post-correction-operational-rebinding"
GATE_PRIOR = "xasset0043-post-correction-rebinding-authorization"


# ======================================================================================
# Helpers and fixtures
# ======================================================================================


def _git(*args: str) -> str:
    out = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if out.returncode != 0:
        pytest.skip(f"git {' '.join(args)} unavailable in this checkout")
    return out.stdout


def _blob_at(commit: str, relpath: str) -> bytes:
    out = subprocess.run(
        ["git", "cat-file", "blob", f"{commit}:{relpath}"],
        cwd=ROOT, capture_output=True, check=False,
    )
    if out.returncode != 0:
        pytest.skip(f"{relpath} unavailable at {commit} in this checkout")
    return out.stdout


def _paths_changed_between(before: str, after: str, relpaths) -> list[str]:
    """Which of ``relpaths`` differ between two commits, read only from the object store."""
    for commit in (before, after):
        probe = subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=ROOT, capture_output=True, check=False,
        )
        if probe.returncode != 0:
            pytest.skip(f"commit {commit} unavailable in this checkout")
    changed: list[str] = []
    for relative in relpaths:
        out = subprocess.run(
            ["git", "diff", "--name-only", before, after, "--", relative],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        assert out.returncode == 0, f"git diff failed for {relative}"
        if out.stdout.strip():
            changed.append(relative)
    return changed


def _flat(text: str) -> str:
    """Collapse markdown wrapping and blockquote markers: test content, not typography."""
    unquoted = re.sub(r"(?m)^\s*>\s?", "", text)
    return re.sub(r"\s+", " ", unquoted)


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def sections(decision_text: str) -> dict[str, str]:
    """The decision's lettered sections, split on their own headings."""
    found: dict[str, str] = {}
    pattern = re.compile(r"(?m)^### ([A-Z])\. ")
    marks = list(pattern.finditer(decision_text))
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(decision_text)
        found[mark.group(1)] = decision_text[mark.start(): end]
    return found


@pytest.fixture(scope="module")
def flat_sections(sections: dict[str, str]) -> dict[str, str]:
    return {key: _flat(value) for key, value in sections.items()}


@pytest.fixture(scope="module")
def prereg() -> dict:
    return yaml.safe_load((ROOT / PREREG_RELPATH).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ws0014() -> dict:
    data = yaml.safe_load(REGISTER_PATH.read_text(encoding="utf-8"))
    return next(w for w in data["workstreams"] if w.get("id") == "WS-0014")


# ======================================================================================
# 1 -- Step 8 is not re-consumed, and XASSET-0037 is not invalidated
# ======================================================================================


class TestStep8IsNotReconsumed:
    def test_the_decision_states_step_8_was_spent_by_xasset_0037(self, flat_sections):
        text = flat_sections["C"]
        assert "Step 8 authorized **one** rebinding" in text
        assert "`XASSET-0037` performed it" in text
        assert "That budget stays spent" in text

    def test_the_authority_is_section_d_plus_link_2_plus_xasset_0043(self, flat_sections):
        text = flat_sections["C"]
        assert "reconciliation lifecycle" in text
        assert "***equivalent***" in text
        assert "`XASSET-0043` §F" in text

    def test_the_predecessor_is_preserved_not_invalidated(self, flat_sections):
        assert "preserved, not invalidated" in flat_sections["C"]

    def test_the_module_says_the_same_thing_in_its_own_words(self):
        source = " ".join(
            (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8").replace("#:", " ").split()
        )
        assert "SS-G.B STEP 8 IS NOT RE-CONSUMED" in source
        assert "that budget stays spent" in source

    def test_the_canonical_record_does_not_claim_step_8_again(self, prereg):
        rebinding = prereg["stage_1_operational_authorization"]["successor_operational_rebinding"]
        assert rebinding["rebinding_authority"] != "XASSET-0030_SS_G_B_STEP_8"
        assert rebinding["predecessor_rebinding_authority_xasset_0037"] == (
            "XASSET-0030_SS_G_B_STEP_8"
        )
        assert rebinding["rebinding_decision"] == DECISION_ID
        assert rebinding["predecessor_rebinding_decision_xasset_0037"] == "XASSET-0037"


# ======================================================================================
# 2 -- Five structurally distinct identities, never overloaded
# ======================================================================================


class TestFiveDistinctIdentities:
    def test_the_five_decision_identities_are_pairwise_distinct(self):
        identities = {
            A.PREDECESSOR_DECISION,
            A.HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION,
            A.PACKAGE_AUTHORIZING_DECISION,
            A.PRIOR_SUCCESSOR_REBINDING_DECISION,
            A.AUTHORIZING_DECISION,
        }
        assert len(identities) == 5

    def test_the_structural_closure_predecessor_is_untouched(self):
        """Repointing PREDECESSOR_* at anything else is the overloading this forbids."""
        assert A.PREDECESSOR_DECISION == "XASSET-0028"
        assert A.PREDECESSOR_MERGE_SHA == "c51e94609eff7ede2bdfa084844d59b8347561e5"
        assert A.PREDECESSOR_ACCEPTED_HEAD == "036606401ea569b0a03f2d716d87a057d07d71dc"
        assert A.PREDECESSOR_MERGE_BASE == "e4b6f0b810884fcb73d1b8ee053d8005db532f3e"

    def test_the_prior_rebinding_carries_xasset_0037s_own_identity(self):
        assert A.PRIOR_SUCCESSOR_REBINDING_DECISION == "XASSET-0037"
        assert A.PRIOR_SUCCESSOR_REBINDING_PULL_REQUEST == 337
        assert A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA == (
            "637eaa30302f5a71f84ab1d215ecbd32c01399b5"
        )
        assert A.PRIOR_SUCCESSOR_REBINDING_ACCEPTED_HEAD == (
            "f40c816223c78f1d1e436b718455df5fb3d77fa7"
        )
        # ... and it really was branched from the package it bound.
        assert A.PRIOR_SUCCESSOR_REBINDING_MERGE_BASE == A.EXECUTABLE_PACKAGE_MERGE_SHA

    def test_the_correction_authority_is_not_the_correction(self):
        """XASSET-0041 authorized; XASSET-0042 is the merged tree. Different things."""
        assert A.CORRECTION_AUTHORIZING_DECISION == "XASSET-0041"
        assert A.CORRECTED_MODULE_DECISION == "XASSET-0042"
        assert A.CORRECTION_AUTHORIZING_PULL_REQUEST != A.CORRECTED_MODULE_PULL_REQUEST
        assert A.CORRECTION_AUTHORIZING_MERGE_SHA != A.CORRECTED_MODULE_MERGE_SHA
        # The correction's own base is its authority's merge.
        assert A.CORRECTED_MODULE_MERGE_BASE == A.CORRECTION_AUTHORIZING_MERGE_SHA

    def test_the_rebinding_authority_is_this_units_own_base(self):
        """ADVANCED BY XASSET-0047, unchanged in KIND.

        The property is "the live reviewed base is the merge of the decision that authorized the
        LIVE unit", asserted mechanically so a unit branched from anywhere else fails here. The
        live unit is no longer XASSET-0044, so the equality now names XASSET-0046's merge.
        XASSET-0043's own identity is asserted unchanged, and this decision's own closed anchor
        ``PR_BASE_SHA`` is retained and re-asserted on the constants that now carry it, so nothing
        was dropped -- only re-pointed at the relationship each constant actually names.
        """
        assert A.REBINDING_AUTHORIZING_DECISION == "XASSET-0043"
        assert A.REBINDING_AUTHORIZING_PULL_REQUEST == 343
        # ADVANCED AGAIN BY XASSET-0049, unchanged in KIND for the third time. The live unit is
        # the XASSET-0048-authorized step-8-EQUIVALENT rebinding, so the equality names
        # XASSET-0048's merge. XASSET-0047's own accepted equality is retained immediately below
        # on the constants that now carry it, so nothing is dropped.
        assert A.REVIEWED_BASE_SHA == A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA
        assert A.REVIEWED_BASE_SHA != PR_BASE_SHA
        assert A.PRIOR_RECONCILIATION_MERGE_BASE == A.RECOVERY_AUTHORIZING_MERGE_SHA
        # THIS decision's own closed anchor, retained: PR #344 really did branch from PR #343's
        # merge, and that fact is immutable and still asserted exactly.
        assert A.STOPPED_REBINDING_MERGE_BASE == A.REBINDING_AUTHORIZING_MERGE_SHA
        assert A.STOPPED_REBINDING_MERGE_BASE == PR_BASE_SHA
        # ... and that authority branched from the correction it followed.
        assert A.REBINDING_AUTHORIZING_MERGE_BASE == A.CORRECTED_MODULE_MERGE_SHA

    @pytest.mark.parametrize(
        "merge,base,head",
        [
            (
                "637eaa30302f5a71f84ab1d215ecbd32c01399b5",
                "3e5de8f85c69c2e5dc2b75421446b5db996d7cf1",
                "f40c816223c78f1d1e436b718455df5fb3d77fa7",
            ),
            (
                "5fbfc94d7333e552bd2654261e0c57134a172e31",
                "9c8647f9dddacdf63825f569097214ba65299fe8",
                "4d5d99d67364d3c940aad74c3093bd2afbc3481d",
            ),
            (
                "0709d2f05ab031ecb6f69c40465ed4a227983aed",
                "5fbfc94d7333e552bd2654261e0c57134a172e31",
                "8e9d65ffa40991fade92b60f72f833501ce799d9",
            ),
        ],
    )
    def test_every_inherited_merge_is_real_ordered_and_undrifted(self, merge, base, head):
        """Re-derived from the object store, never taken from the decision's prose."""
        parents = _git("log", "-1", "--pretty=%P", merge).split()
        assert parents == [base, head], f"{merge} parents are {parents!r}"
        merge_tree = _git("rev-parse", f"{merge}^{{tree}}").strip()
        head_tree = _git("rev-parse", f"{head}^{{tree}}").strip()
        assert merge_tree == head_tree, f"{merge} carries drift its review never saw"

    @pytest.mark.parametrize(
        "merge",
        [
            "637eaa30302f5a71f84ab1d215ecbd32c01399b5",
            "9c8647f9dddacdf63825f569097214ba65299fe8",
            "5fbfc94d7333e552bd2654261e0c57134a172e31",
            "0709d2f05ab031ecb6f69c40465ed4a227983aed",
        ],
    )
    def test_every_inherited_merge_is_an_ancestor_of_this_work(self, merge):
        head = _git("rev-parse", "HEAD").strip()
        assert _git("merge-base", merge, head).strip() == merge

    def test_the_attempt_identity_is_not_reminted(self):
        """A successor authorization does not mint a second attempt."""
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"


# ======================================================================================
# 3 -- The trust boundary grows by DIRECT MEMBERSHIP; nothing is removed
# ======================================================================================


class TestTrustBoundaryGrowsByDirectMembership:
    def test_the_set_grew_from_ten_to_fourteen(self):
        """ADVANCED BY XASSET-0047: 14 -> 16, additively and by direct membership.

        This decision's own growth -- ten to fourteen -- is immutable history and is asserted
        exactly, arithmetically, below. The LIVE size is a live fact and is asserted exactly at
        its current value and bound at both ends, so neither a silent shrink back nor an
        unexplained further growth passes.
        """
        # ADVANCED AGAIN BY XASSET-0049: 16 -> 18, additively and by direct membership.
        assert len(XASSET_0037_LOAD_BEARING) == 10
        assert len(A.LOAD_BEARING_RELPATHS) == 18
        assert len(set(A.LOAD_BEARING_RELPATHS)) == 18
        assert len(A.LOAD_BEARING_RELPATHS) != 16
        assert len(A.LOAD_BEARING_RELPATHS) != 14
        # THIS decision's own four additions are still present, all four, individually.
        assert set(BOUNDARY_ADDITIONS) <= set(A.LOAD_BEARING_RELPATHS)
        assert len(set(XASSET_0037_LOAD_BEARING) | set(BOUNDARY_ADDITIONS)) == 14

    def test_every_predecessor_path_is_retained(self):
        """Growth is additive. A path traded away is the defect this catches."""
        assert set(XASSET_0037_LOAD_BEARING) <= set(A.LOAD_BEARING_RELPATHS)

    def test_the_additions_are_exactly_the_four_authority_chain_files(self):
        """ADVANCED BY XASSET-0047, which added two more under its own separate authority.

        This decision's four additions are still asserted EXACTLY, by subtracting the successor's
        own two by name. Nothing is relaxed into a subset test that any future growth would
        satisfy: a THIRD unexplained addition still fails here.
        """
        # ADVANCED AGAIN BY XASSET-0049, which added two more under its own separate authority.
        # THIS decision's four additions are still asserted EXACTLY, by subtracting each later
        # unit's own additions BY NAME. Nothing is relaxed into a subset test any future growth
        # would satisfy: a further unexplained addition still fails here.
        additions = set(A.LOAD_BEARING_RELPATHS) - set(XASSET_0037_LOAD_BEARING)
        assert additions == (
            set(BOUNDARY_ADDITIONS)
            | set(XASSET_0047_BOUNDARY_ADDITIONS)
            | set(XASSET_0049_BOUNDARY_ADDITIONS)
        )
        assert (
            additions
            - set(XASSET_0047_BOUNDARY_ADDITIONS)
            - set(XASSET_0049_BOUNDARY_ADDITIONS)
        ) == set(BOUNDARY_ADDITIONS)
        assert set(BOUNDARY_ADDITIONS).isdisjoint(XASSET_0047_BOUNDARY_ADDITIONS)
        assert set(BOUNDARY_ADDITIONS).isdisjoint(XASSET_0049_BOUNDARY_ADDITIONS)
        assert set(XASSET_0047_BOUNDARY_ADDITIONS).isdisjoint(XASSET_0049_BOUNDARY_ADDITIONS)

    @pytest.mark.parametrize("relpath", BOUNDARY_ADDITIONS)
    def test_each_addition_is_a_real_file_bound_by_membership_not_citation(self, relpath):
        """A decision that merely CITES predecessor text does not byte-bind it."""
        assert (ROOT / relpath).is_file(), relpath
        assert relpath in A.LOAD_BEARING_RELPATHS

    def test_every_load_bearing_path_exists(self):
        for relative in A.LOAD_BEARING_RELPATHS:
            assert (ROOT / relative).exists(), relative

    def test_no_results_artifact_is_load_bearing(self):
        assert "stage1_results" not in " ".join(A.LOAD_BEARING_RELPATHS).lower()

    def test_expected_identity_is_still_derived_from_the_merged_tree(self):
        """A hard-coded expected digest would be edited in the same commit it claims to verify."""
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert "expected values come from the MERGED TREE, not a constant" in source

    def test_the_decision_forbids_an_asserted_equivalent(self, flat_sections):
        text = flat_sections["E"]
        assert "Direct membership, not an equivalent" in text
        assert "would **not** be a binding of those files" in text


# ======================================================================================
# 4 -- The derivation chain is APPENDED, never replaced or loosened
# ======================================================================================


class TestTheChainIsAppendedNotReplaced:
    def test_link_one_is_preserved_verbatim(self):
        assert len(A.OUTCOME_PRODUCING_TRANSITION) == 17
        assert A.OUTCOME_PRODUCING_SUCCESSOR_SHA256 == SUCCESSOR_DERIVATION_SHA256

    def test_link_two_exists_and_starts_where_link_one_ends(self):
        assert len(A.OUTCOME_PRODUCING_REBOUND_TRANSITION) == 23
        assert A.OUTCOME_PRODUCING_REBOUND_SHA256 != A.OUTCOME_PRODUCING_SUCCESSOR_SHA256
        assert A.OUTCOME_PRODUCING_REBOUND_SHA256 != A.OUTCOME_PRODUCING_PACKAGE_SHA256

    def test_the_pinned_identities_match_the_real_blobs(self):
        package = _blob_at(A.EXECUTABLE_PACKAGE_MERGE_SHA, DERIVATION_RELPATH)
        successor = _blob_at(A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA, DERIVATION_RELPATH)
        rebound = (ROOT / DERIVATION_RELPATH).read_bytes()
        assert hashlib.sha256(package).hexdigest() == A.OUTCOME_PRODUCING_PACKAGE_SHA256
        assert hashlib.sha256(successor).hexdigest() == A.OUTCOME_PRODUCING_SUCCESSOR_SHA256
        assert hashlib.sha256(rebound).hexdigest() == A.OUTCOME_PRODUCING_REBOUND_SHA256
        assert len(package) == A.OUTCOME_PRODUCING_PACKAGE_LENGTH
        assert len(successor) == A.OUTCOME_PRODUCING_SUCCESSOR_LENGTH
        assert len(rebound) == A.OUTCOME_PRODUCING_REBOUND_LENGTH

    def test_both_links_verify_against_the_real_bytes(self):
        package = _blob_at(A.EXECUTABLE_PACKAGE_MERGE_SHA, DERIVATION_RELPATH)
        successor = _blob_at(A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA, DERIVATION_RELPATH)
        rebound = (ROOT / DERIVATION_RELPATH).read_bytes()
        A.verify_exact_transition(package, successor)
        A.verify_exact_rebound_transition(successor, rebound)

    def test_the_successor_anchors_really_agree_with_each_other(self):
        """Both XASSET-0037 anchors must carry identical bytes, or the link's start is ambiguous."""
        at_head = _blob_at(A.PRIOR_SUCCESSOR_REBINDING_ACCEPTED_HEAD, DERIVATION_RELPATH)
        at_merge = _blob_at(A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA, DERIVATION_RELPATH)
        assert at_head == at_merge

    def test_link_two_is_closed_and_consumes_both_blobs(self):
        """Independently re-derived here rather than trusting the module's own verifier."""
        successor = _blob_at(A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA, DERIVATION_RELPATH)
        rebound = (ROOT / DERIVATION_RELPATH).read_bytes()
        s_cursor = r_cursor = 0
        for index, region in enumerate(A.OUTCOME_PRODUCING_REBOUND_TRANSITION):
            s_at, s_len, s_want, r_at, r_len, r_want = region
            assert s_at >= s_cursor and r_at >= r_cursor, f"region {index} overlaps"
            assert successor[s_cursor:s_at] == rebound[r_cursor:r_at], (
                f"the span before region {index} is not byte-identical"
            )
            assert hashlib.sha256(successor[s_at:s_at + s_len]).hexdigest() == s_want
            assert hashlib.sha256(rebound[r_at:r_at + r_len]).hexdigest() == r_want
            s_cursor, r_cursor = s_at + s_len, r_at + r_len
        assert successor[s_cursor:] == rebound[r_cursor:], "trailing spans differ"

    def test_no_region_declares_no_change_on_either_side(self):
        for index, region in enumerate(A.OUTCOME_PRODUCING_REBOUND_TRANSITION):
            assert region[1] or region[4], f"region {index} declares no change"

    @pytest.mark.parametrize("at", [0, 1, 500])
    def test_a_flipped_byte_outside_a_region_is_refused(self, at):
        successor = _blob_at(A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA, DERIVATION_RELPATH)
        rebound = bytearray((ROOT / DERIVATION_RELPATH).read_bytes())
        rebound[at] ^= 0x01
        with pytest.raises(A.TransitionError):
            A.verify_exact_rebound_transition(successor, bytes(rebound))

    def test_a_flipped_byte_inside_a_region_is_refused(self):
        successor = _blob_at(A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA, DERIVATION_RELPATH)
        rebound = bytearray((ROOT / DERIVATION_RELPATH).read_bytes())
        first = A.OUTCOME_PRODUCING_REBOUND_TRANSITION[0]
        assert first[4] > 0
        rebound[first[3]] ^= 0x01
        with pytest.raises(A.TransitionError):
            A.verify_exact_rebound_transition(successor, bytes(rebound))

    def test_dropping_a_region_is_refused(self):
        successor = _blob_at(A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA, DERIVATION_RELPATH)
        rebound = (ROOT / DERIVATION_RELPATH).read_bytes()
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(
                successor, rebound, A.OUTCOME_PRODUCING_REBOUND_TRANSITION[1:],
                package_length=A.OUTCOME_PRODUCING_SUCCESSOR_LENGTH,
                package_sha256=A.OUTCOME_PRODUCING_SUCCESSOR_SHA256,
                successor_length=A.OUTCOME_PRODUCING_REBOUND_LENGTH,
                successor_sha256=A.OUTCOME_PRODUCING_REBOUND_SHA256,
            )

    def test_an_empty_manifest_is_refused(self):
        successor = _blob_at(A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA, DERIVATION_RELPATH)
        rebound = (ROOT / DERIVATION_RELPATH).read_bytes()
        with pytest.raises(A.TransitionError):
            A.verify_exact_transition(
                successor, rebound, (),
                package_length=A.OUTCOME_PRODUCING_SUCCESSOR_LENGTH,
                package_sha256=A.OUTCOME_PRODUCING_SUCCESSOR_SHA256,
                successor_length=A.OUTCOME_PRODUCING_REBOUND_LENGTH,
                successor_sha256=A.OUTCOME_PRODUCING_REBOUND_SHA256,
            )

    def test_the_two_links_are_not_swappable(self):
        """Link 2's manifest must not verify link 1's blobs, or the chain is not really a chain."""
        package = _blob_at(A.EXECUTABLE_PACKAGE_MERGE_SHA, DERIVATION_RELPATH)
        successor = _blob_at(A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA, DERIVATION_RELPATH)
        with pytest.raises(A.TransitionError):
            A.verify_exact_rebound_transition(package, successor)

    def test_link_one_defaults_are_untouched_by_the_generalisation(self):
        """Adding keyword-only expectations must not change link 1's behaviour."""
        import inspect

        signature = inspect.signature(A.verify_exact_transition)
        assert signature.parameters["package_length"].default == (
            A.OUTCOME_PRODUCING_PACKAGE_LENGTH
        )
        assert signature.parameters["package_sha256"].default == (
            A.OUTCOME_PRODUCING_PACKAGE_SHA256
        )
        assert signature.parameters["successor_length"].default == (
            A.OUTCOME_PRODUCING_SUCCESSOR_LENGTH
        )
        assert signature.parameters["successor_sha256"].default == (
            A.OUTCOME_PRODUCING_SUCCESSOR_SHA256
        )
        for name in (
            "package_length", "package_sha256", "successor_length", "successor_sha256",
        ):
            assert signature.parameters[name].kind is inspect.Parameter.KEYWORD_ONLY

    def test_the_authorization_boundary_is_still_bytes_only(self):
        """No AST, import, exec, eval, or diff library may participate in the authorization."""
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        tree = ast.parse(source)
        target = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "verify_exact_transition":
                target = node
        assert target is not None
        called = {
            n.func.id for n in ast.walk(target)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        }
        for forbidden in ("eval", "exec", "compile", "__import__"):
            assert forbidden not in called
        # `difflib` is named in the module's PROHIBITION prose, so a bare substring scan would
        # flag the sentence that forbids it. Ask whether it is actually imported.
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    assert name.name != "difflib"
            if isinstance(node, ast.ImportFrom):
                assert node.module != "difflib"


# ======================================================================================
# 5 -- The outcome-producing surface and the universe are unchanged
# ======================================================================================


class TestOutcomeSurfaceIsUnchanged:
    @pytest.mark.parametrize(
        "relpath",
        [
            "level1_stage1_runner.py",
            "level1_stage1_result_validator.py",
            "level1_construction_universe_closure_validator.py",
        ],
    )
    def test_outcome_producing_modules_are_byte_identical_to_the_package(self, relpath):
        """No transition, no exception: these must be the accepted package's exact bytes."""
        package = _blob_at(A.EXECUTABLE_PACKAGE_ACCEPTED_HEAD, relpath)
        merge = _blob_at(A.EXECUTABLE_PACKAGE_MERGE_SHA, relpath)
        working = (ROOT / relpath).read_bytes()
        assert package == merge == working

    def test_the_universe_regenerates_unchanged(self):
        import level1_construction_universe_closure_validator as CU

        assert CU.universe_aggregate_sha256() == UNIVERSE_HASH
        assert A.CONSTRUCTION_UNIVERSE_SHA256 == UNIVERSE_HASH
        assert len(CU.frozen_construction_universe()) == 680
        assert A.CONSTRUCTION_COUNT == 680
        assert A.CONSTRUCTION_CELL_COUNT == 48

    def test_the_gate_and_disposition_surfaces_are_untouched(self, prereg):
        gates = prereg["gate_sequence"]["gates"]
        assert len(gates) == 12
        assert [g["gate_index"] for g in gates] == list(range(1, 13))
        inventory = prereg["pair_consumption_rule"]["structural_inventory"]
        assert inventory["consuming_total"] == 480
        assert inventory["non_consuming_total"] == 200
        assert inventory["universe_total"] == 680
        assert prereg["g12_modal_register"]["scope"] == "G12_ONLY"
        assert prereg["reserved_gate_recording_posture"]["recorded_value"] == "UNABLE_TO_DETERMINE"

    def test_every_consumer_reachable_symbol_survives_the_rebound_transition(self):
        """§G.4a point 6, derived from the CONSUMERS' own source rather than asserted.

        Every symbol the runner and the result validator import from the derivation module must
        still be defined in the rebound blob, and must be structurally identical to its definition
        in the accepted successor blob.
        """
        imported: set[str] = set()
        for consumer in ("level1_stage1_runner.py", "level1_stage1_result_validator.py"):
            tree = ast.parse((ROOT / consumer).read_text(encoding="utf-8"))
            alias = None
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        if name.name == DERIVATION_RELPATH[:-3]:
                            alias = name.asname or name.name
                if isinstance(node, ast.ImportFrom) and node.module == DERIVATION_RELPATH[:-3]:
                    imported.update(n.name for n in node.names)
            if alias:
                for node in ast.walk(tree):
                    if (
                        isinstance(node, ast.Attribute)
                        and isinstance(node.value, ast.Name)
                        and node.value.id == alias
                    ):
                        imported.add(node.attr)
        assert imported, "no consumer-reachable symbols were discovered; the premise is broken"

        def _definitions(source: str) -> dict[str, str]:
            tree = ast.parse(source)
            out: dict[str, str] = {}
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    out[node.name] = ast.dump(node, annotate_fields=True)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            out[target.id] = ast.dump(node.value, annotate_fields=True)
            return out

        successor = _definitions(
            _blob_at(A.PRIOR_SUCCESSOR_REBINDING_MERGE_SHA, DERIVATION_RELPATH).decode("utf-8")
        )
        rebound = _definitions((ROOT / DERIVATION_RELPATH).read_text(encoding="utf-8"))
        checked = 0
        for symbol in sorted(imported):
            if symbol not in successor:
                continue
            assert symbol in rebound, f"{symbol} disappeared from the rebound blob"
            assert successor[symbol] == rebound[symbol], (
                f"{symbol} is consumer-reachable and its definition changed"
            )
            checked += 1
        assert checked >= 10, f"only {checked} consumer-reachable definitions were compared"


# ======================================================================================
# 6 -- The canonical amendment is authorization language only
# ======================================================================================


class TestCanonicalAmendmentIsAuthorizationLanguageOnly:
    def test_the_operative_lifecycle_names_this_decision(self, prereg):
        effectivity = prereg["lifecycle_effectivity"]
        assert effectivity["stage_1_execution_may_begin_only_after"].startswith("XASSET_0044_")
        assert effectivity["stage_1_execution_precondition_amended_by"] == DECISION_ID
        assert prereg["stages"]["stage_1"]["executable_only_after"].startswith("XASSET_0044_")
        assert prereg["stage_1_executability"]["blocking_prerequisite"].startswith("XASSET_0044_")

    def test_every_superseded_generation_is_retained(self, prereg):
        effectivity = prereg["lifecycle_effectivity"]
        for generation in ("0037", "0029", "0028"):
            key = f"predecessor_stage_1_execution_may_begin_only_after_xasset_{generation}"
            assert key in effectivity, key

    def test_the_mechanisms_establisher_is_not_rewritten(self, prereg):
        """Historical truth is never rewritten by a successor."""
        block = prereg["stage_1_operational_authorization"]
        assert block["established_by"] == "XASSET-0029"
        assert block["rebound_by"] == DECISION_ID
        assert block["effective_structural_authorization_source"] == DECISION_ID
        assert block["predecessor_rebound_by_xasset_0037"] == "XASSET-0037"

    def test_executability_stays_permanently_false(self, prereg):
        block = prereg["stage_1_executability"]
        assert block["executable"] is False
        assert block["executable_is_never_the_authorization_source"] is True
        for generation in ("0027", "0028", "0029", "0036", "0037", "0044"):
            assert block[f"authorized_by_xasset_{generation}"] is False

    def test_the_protocol_mirror_moves_in_lockstep(self):
        protocol = (ROOT / PROTOCOL_RELPATH).read_text(encoding="utf-8")
        assert f"stage_1_effective_structural_authorization_source: {DECISION_ID}" in protocol
        assert f"stage_1_authorization_rebound_by: {DECISION_ID}" in protocol
        assert PREREG.validate_protocol_mirror(protocol).ok

    def test_the_whole_canonical_surface_validates(self):
        assert PREREG.validate_file().ok

    def test_the_predecessor_amendment_section_is_not_deleted(self):
        protocol = (ROOT / PROTOCOL_RELPATH).read_text(encoding="utf-8")
        assert "## Amendment — `XASSET-0037` Stage-1 successor operational rebinding" in protocol
        assert "## Amendment — `XASSET-0044` Stage-1 post-correction operational rebinding" in (
            protocol
        )


# ======================================================================================
# 7 -- Pins are current, and pin succession is refused
# ======================================================================================


class TestPinsAreCurrentAndSuccessionIsRefused:
    def test_the_effective_pins_are_the_live_bytes(self):
        for relative in (PROTOCOL_RELPATH, PREREG_RELPATH):
            actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            assert A.CANONICAL_PINS[relative] == actual

    def test_the_predecessor_pins_are_retained_and_distinct(self):
        assert A.XASSET_0037_CANONICAL_PINS[PROTOCOL_RELPATH] == XASSET_0037_PROTOCOL_PIN
        assert A.XASSET_0037_CANONICAL_PINS[PREREG_RELPATH] == XASSET_0037_PREREG_PIN
        for relative in (PROTOCOL_RELPATH, PREREG_RELPATH):
            assert A.CANONICAL_PINS[relative] != A.XASSET_0037_CANONICAL_PINS[relative]

    def test_a_successor_pin_equal_to_any_predecessor_is_refused(self):
        """The refusal is EXTENDED to XASSET-0037's generation, never relaxed."""
        assert "XASSET-0037" in [
            label for label, _ in [
                ("XASSET-0037", PREREG.XASSET_0037_PINS),
            ]
        ]
        source = (ROOT / DERIVATION_RELPATH).read_text(encoding="utf-8")
        assert '("XASSET-0037", XASSET_0037_PINS)' in source

    def test_the_decision_declares_exactly_one_current_module_identity(self, decision_text):
        """ADVANCED BY XASSET-0047: the CURRENT identity is declared by the CURRENT decision.

        The property is unchanged -- exactly one line, exactly one 64-hex token, and that token
        must equal the module's real bytes -- and it is now checked on BOTH decisions rather than
        one. XASSET-0044's own declaration is accepted merged history, byte-identical to what it
        always was, and must therefore NO LONGER match a module its successor lawfully changed;
        asserting that inequality is what proves the successor really rebound rather than leaving
        a stale pin agreeing by accident.
        """

        def _sole_token(text: str) -> str:
            declared = [
                ln for ln in text.split("\n")
                if ln.strip().startswith("CURRENT_MODULE_SHA256:")
            ]
            assert len(declared) == 1, declared
            tokens = [
                token for token in declared[0].replace("`", " ").split()
                if len(token) == 64 and all(c in "0123456789abcdef" for c in token)
            ]
            assert len(tokens) == 1, tokens
            return tokens[0]

        # ADVANCED AGAIN BY XASSET-0049, unchanged in KIND. Every generation's declaration is
        # accepted merged history describing the module AS THAT UNIT LEFT IT, and each remains
        # exactly one line with exactly one token. Which declaration matches the LIVE module is a
        # live fact belonging to the CURRENT unit; XASSET-0047's now describes its own merge, and
        # asserting that it no longer matches the live module is precisely what proves the newest
        # successor really rebound rather than leaving a stale pin agreeing by accident.
        live = hashlib.sha256((ROOT / AUTH_MODULE_RELPATH).read_bytes()).hexdigest()
        successor = (ROOT / XASSET_0047_DECISION_RELPATH).read_text(encoding="utf-8")
        assert _sole_token(successor) == XASSET_0047_FINAL_MODULE_SHA256
        assert _sole_token(successor) != live
        # ADVANCED AGAIN BY XASSET-0056, on exactly the terms this test already applies to
        # every earlier generation: a declaration is accepted merged history describing the
        # module AS THAT UNIT LEFT IT. The single replacement parser-correction implementation
        # XASSET-0055 §H authorized lawfully changed that byte, so XASSET-0049's declaration
        # must now ALSO no longer match the live module -- and asserting that inequality is
        # precisely what proves the correction really landed rather than a stale pin agreeing
        # by accident. The declaration is NOT re-pinned here: this filing performs no
        # rebinding, and the value it still declares is asserted EXACTLY, not merely as
        # "different", so nothing is relaxed.
        latest = (ROOT / XASSET_0049_DECISION_RELPATH).read_text(encoding="utf-8")
        assert _sole_token(latest) == "4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541"
        assert _sole_token(latest) != live
        # THIS decision's own declaration is unchanged history and no longer describes the module.
        assert _sole_token(decision_text) != live
        # Every generation's declaration is distinct: none was copied forward.
        assert len({
            _sole_token(decision_text), _sole_token(successor), _sole_token(latest)
        }) == 3

    def test_all_four_module_identities_are_retained_and_mutually_distinct(self, decision_text):
        current = hashlib.sha256((ROOT / AUTH_MODULE_RELPATH).read_bytes()).hexdigest()
        for historical in (
            BOUND_MODULE_SHA256, INTERMEDIATE_MODULE_SHA256, XASSET_0042_FINAL_MODULE_SHA256,
        ):
            assert historical in decision_text, historical
        assert len({
            current,
            BOUND_MODULE_SHA256,
            INTERMEDIATE_MODULE_SHA256,
            XASSET_0042_FINAL_MODULE_SHA256,
        }) == 4

    def test_the_hash_pin_block_is_present_and_live_verified(self, decision_text):
        assert "<!-- XASSET-0044-HASH-PINS-V1" in decision_text
        assert PREREG.validate_xasset_0044_successor_hash_pins(decision_text).ok

    def test_a_forged_pin_block_fails_closed(self, decision_text):
        forged = decision_text.replace(A.CANONICAL_PINS[PROTOCOL_RELPATH], "0" * 64)
        assert forged != decision_text
        assert not PREREG.validate_xasset_0044_successor_hash_pins(forged).ok

    def test_a_rewritten_predecessor_pin_fails_closed(self, decision_text):
        """A successor may not rewrite the history it claims to succeed."""
        forged = decision_text.replace(XASSET_0037_PROTOCOL_PIN, "1" * 64)
        assert forged != decision_text
        assert not PREREG.validate_xasset_0044_successor_hash_pins(forged).ok


# ======================================================================================
# 8 -- The XASSET-0042 hand-off is RESOLVED, and no guard is weakened
# ======================================================================================


class TestXasset0042HandoffIsResolvedNotWeakened:
    GUARD_SUITE = ROOT / "test_level1_stage1_pr337_lifecycle_actor_evidence_correction.py"
    GUARD_CLASS = "TestDeclaredCorrectedIdentityMatchesTheModule"
    XASSET_0042_DECISION = ROOT / (
        "governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md"
    )

    def test_the_choice_is_argued_not_assumed(self, flat_sections):
        text = flat_sections["H"]
        assert "This unit takes (b), retirement." in text
        assert "would make `XASSET-0042` claim to have produced bytes it never produced" in text

    def test_xasset_0042s_declaration_line_is_byte_unchanged(self):
        """Retirement moves the ROLE, not the value."""
        live = [
            ln for ln in self.XASSET_0042_DECISION.read_text(encoding="utf-8").split("\n")
            if ln.strip().startswith("FINAL_CORRECTED_MODULE_SHA256:")
        ]
        at_merge = [
            ln for ln in _blob_at(
                A.CORRECTED_MODULE_MERGE_SHA,
                "governance/decisions/"
                "XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md",
            ).decode("utf-8").split("\n")
            if ln.strip().startswith("FINAL_CORRECTED_MODULE_SHA256:")
        ]
        assert len(live) == 1 and len(at_merge) == 1
        assert live[0] == at_merge[0]
        assert XASSET_0042_FINAL_MODULE_SHA256 in live[0]

    def test_the_guard_class_only_ever_grew(self):
        """SS-I.4 permits re-anchoring and forbids deletion. Proven, not asserted."""

        def _names(source: str) -> list[str]:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == self.GUARD_CLASS:
                    return [
                        n.name for n in node.body
                        if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
                    ]
            pytest.fail(f"{self.GUARD_CLASS} not found")
            raise AssertionError  # pragma: no cover - unreachable

        at_merge = _names(
            _blob_at(
                A.CORRECTED_MODULE_MERGE_SHA,
                "test_level1_stage1_pr337_lifecycle_actor_evidence_correction.py",
            ).decode("utf-8")
        )
        live = _names(self.GUARD_SUITE.read_text(encoding="utf-8"))
        assert set(at_merge) <= set(live), "a guard test was removed or renamed"
        assert len(live) > len(at_merge), "re-anchoring should have added mutation pins"

    def test_no_guard_was_skipped_or_xfailed(self):
        source = self.GUARD_SUITE.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == self.GUARD_CLASS:
                for decorator in (
                    d for n in node.body
                    if isinstance(n, ast.FunctionDef) for d in n.decorator_list
                ):
                    rendered = ast.dump(decorator)
                    assert "xfail" not in rendered
                    assert "skipif" not in rendered

    def test_the_actor_evidence_correction_is_preserved_byte_for_byte(self):
        """§G.3: the corrected mechanism is the reason this rebinding exists."""
        assert A.PRINCIPAL_ACCOUNT_LOGIN == "Mast3rkey"
        assert A.LIFECYCLE_OPERATOR_LOGIN == "Mast3rkey"
        assert A.RATIFIED_HISTORICAL_ACTOR == "claude[bot]"
        assert A.RATIFIED_PULL_REQUEST == 337
        assert A.RATIFIED_HEAD_SHA == "f40c816223c78f1d1e436b718455df5fb3d77fa7"
        assert A.RATIFIED_REVIEW_ID == "4966846374"
        assert A.RATIFIED_ACCEPTANCE_COMMENT_ID == "5335697214"
        assert A.RATIFIED_MERGE_SHA == "637eaa30302f5a71f84ab1d215ecbd32c01399b5"
        assert A.RATIFIED_POST_MERGE_VERIFICATION_COMMENT_ID == "5335849767"
        assert A.RATIFICATION_AUTHORIZING_DECISION == "XASSET-0041"
        assert A._RATIFICATION_MUST_POSTDATE_RATIFIED_MERGE is True

    def test_the_four_ratification_fingerprints_are_unchanged(self):
        assert A.RATIFICATION_REVIEW_FINGERPRINT == (
            "904f4cb4642f0f7b8bcd6bb33be92d72678270b122402e5d423789960aa33067"
        )
        assert A.RATIFICATION_COMMENT_FINGERPRINT == (
            "acbd2bb2a9ccb9c71475dab83d2ab62cfc1b9110ed5a597e232cd6aaa620b0c6"
        )
        assert A.RATIFICATION_VERIFICATION_FINGERPRINT == (
            "763e4e2fbd2559bb4e4e6e04dd782e4f1d1840e750e23ab776cb44de74d9ed0d"
        )
        assert A.RATIFICATION_CLOSURE_FINGERPRINT == (
            "4e39a8b16248ebe616f5262b6c476f3b6780eedfaf9df2e85d7113272a26f568"
        )

    def test_claude_bot_gains_no_general_standing(self):
        """The exception is a conjunction of exact pins, never an accepted-actor list."""
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        flat = " ".join(source.replace("#", " ").split())
        assert "It is NOT an accepted-actor list" in flat
        assert "gains no standing on any other pull request" in flat

    def test_the_correction_section_is_byte_identical_to_its_accepted_form(self):
        """The whole XASSET-0042 section, compared span-for-span against its own merge."""
        marker = "# XASSET-0042 — the PR #337 lifecycle actor-evidence correction"
        live = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        accepted = _blob_at(A.CORRECTED_MODULE_MERGE_SHA, AUTH_MODULE_RELPATH).decode("utf-8")
        assert marker in live and marker in accepted

        def _section(text: str) -> str:
            start = text.index(marker)
            end = text.index("def _canonical_record_fingerprint", start)
            return text[start:end]

        assert _section(live) == _section(accepted), (
            "the actor-evidence correction section changed; §G.3 requires it byte-for-byte"
        )


# ======================================================================================
# 9 -- Not an activation; ATTEMPT_1 intact; §P.1 reserved
# ======================================================================================


class TestNotAnActivation:
    def test_no_execution_is_authorized(self):
        """ADVANCED BY XASSET-0047. Unchanged in kind: nothing is authorized, and the reason
        names the lifecycle that must close in full. That lifecycle is now the successor's,
        because THIS decision's own can never close -- its merge-commit CI failed permanently.
        Bound at both ends so a silent revert to naming the stopped lifecycle fails here.
        """
        authorized, reason = A.new_execution_is_authorized()
        assert authorized is False
        assert A.AUTHORIZING_DECISION in reason
        # RE-ANCHORED BY XASSET-0049, unchanged in KIND. The property this protects is that the
        # anchor names a lifecycle that CAN close and never this stopped one -- not that it names
        # any one particular successor forever. Both ends stay bound: the anchor is a real
        # successor, and it is not this decision nor any permanently ineffective one.
        assert A.AUTHORIZING_DECISION == "XASSET-0049"
        assert A.AUTHORIZING_DECISION not in A.PERMANENTLY_INEFFECTIVE_DECISIONS
        assert A.AUTHORIZING_DECISION != DECISION_ID
        # The superseded anchor is PRESERVED as history rather than erased.
        assert A.PRIOR_RECONCILIATION_DECISION == "XASSET-0047"
        assert DECISION_ID not in reason
        assert DECISION_ID in A.PERMANENTLY_INEFFECTIVE_DECISIONS

    def test_the_lane_is_absent(self):
        assert not A.AUTHORIZATION_ROOT.exists()
        for path in (A.AUTHORIZATION_PATH, A.CLAIM_PATH, A.COMPLETION_PATH, A.LEDGER_PATH):
            assert not path.exists()

    def test_no_results_document_exists(self):
        assert not (ROOT / "stage1_results.yaml").exists()

    def test_zero_activation_authorizations_are_added(self, flat_sections):
        text = flat_sections["J"]
        assert "ZERO activation" in text
        assert "No committed value in this repository authorizes Stage-1 execution" in text

    def test_the_regress_terminator_is_unchanged(self, flat_sections):
        assert "changes no repository state" in flat_sections["J"]

    def test_p1_remains_reserved_and_unspent(self, flat_sections):
        assert "stays **one, unspent**" in flat_sections["I"]

    def test_xasset_0040_is_not_revived(self, flat_sections):
        assert "remains spent as `STOPPED_BEFORE_ATTESTATION`" in flat_sections["I"]

    def test_this_suite_never_calls_write_authorization(self):
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                assert node.attr != "write_authorization"
            if isinstance(node, ast.Name):
                assert node.id != "write_authorization"


# ======================================================================================
# 10 -- Nothing downstream is authorized
# ======================================================================================


class TestNothingDownstreamIsAuthorized:
    @pytest.mark.parametrize(
        "clause",
        [
            "§G.B steps 9, 10, or 11, in whole or in part",
            "any renewed readiness verification or renewed post-rebinding drift check",
            "generating any external attestation",
            "arming, claiming, completing, executing, or recovering any Stage-1 execution",
            "consuming any part of `ATTEMPT_1`",
            "evaluating any gate for any registered construction",
            "authorizing any successor unit of any kind",
            "rewriting any accepted history",
        ],
    )
    def test_section_i_withholds_it_by_name(self, flat_sections, clause):
        assert clause in flat_sections["I"]

    def test_completing_this_authorizes_no_next_link(self, flat_sections):
        assert (
            "Completing this rebinding authorizes the next link no more than a clean step-10 "
            "result authorized step 11"
        ) in flat_sections["I"]

    def test_no_protected_risk_path_is_referenced(self):
        """No protected ``RISK`` result path is read, listed, opened, or referenced.

        A bare substring scan cannot express this: the token necessarily appears in this suite's
        own prohibition prose, and a test that forbade the word would forbid the sentence saying
        it is never used. The precise properties are that no RISK module is imported, and that the
        token never appears as an identifier or attribute -- only ever inside prose.
        """
        source = Path(__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    assert not name.name.startswith("risk"), name.name
            if isinstance(node, ast.ImportFrom):
                assert not (node.module or "").startswith("risk"), node.module
            if isinstance(node, ast.Name):
                assert "risk_lane_boundary" not in node.id
            if isinstance(node, ast.Attribute):
                assert "risk_lane_boundary" not in node.attr
        # ... and nothing in this suite ever opens a path built from that token.
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                rendered = ast.dump(node)
                if "risk_lane_boundary" in rendered:
                    pytest.fail(f"a call references a protected RISK path: {rendered[:200]}")

    def test_this_suite_imports_no_outcome_producing_module(self):
        forbidden = {
            "level1_stage1_runner",
            "level1_stage1_result_validator",
        }
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    assert name.name not in forbidden
            if isinstance(node, ast.ImportFrom):
                assert node.module not in forbidden


# ======================================================================================
# 11 -- No protected byte was touched
# ======================================================================================


class TestNoProtectedByteWasTouched:
    @pytest.mark.parametrize("relpath", PORTFOLIO_RELPATHS)
    def test_portfolio_path_is_unchanged_from_the_pr_base_to_head(self, relpath):
        assert (ROOT / relpath).exists(), f"{relpath} must still exist"
        changed = _paths_changed_between(PR_BASE_SHA, "HEAD", (relpath,))
        assert changed == [], (
            f"{relpath} changed between the PR base and HEAD; a Level-1 rebinding must never "
            "touch portfolio or allocator bytes"
        )

    @pytest.mark.parametrize("relpath", PORTFOLIO_RELPATHS)
    def test_portfolio_path_is_unchanged_against_head(self, relpath):
        """Worktree cleanliness -- a separate failure mode the base->head check cannot see."""
        blob = _git("rev-parse", f"HEAD:{relpath}").strip()
        committed = subprocess.run(
            ["git", "cat-file", "blob", blob], cwd=ROOT, capture_output=True, check=False
        )
        assert committed.returncode == 0
        assert hashlib.sha256(committed.stdout).hexdigest() == hashlib.sha256(
            (ROOT / relpath).read_bytes()
        ).hexdigest()

    def test_the_comparison_detects_a_real_protected_change(self):
        """MUTATION PIN: the check must not be able to pass vacuously."""
        changed = _paths_changed_between(
            PROTECTED_CHANGE_CONTROL_BEFORE,
            PROTECTED_CHANGE_CONTROL_AFTER,
            (PROTECTED_CHANGE_CONTROL_PATH,),
        )
        assert changed == [PROTECTED_CHANGE_CONTROL_PATH], (
            "the base->head comparison failed to detect a known real change"
        )

    def test_the_pr_base_pin_is_a_real_distinct_ancestor(self):
        assert len(PR_BASE_SHA) == 40
        assert all(c in "0123456789abcdef" for c in PR_BASE_SHA)
        head = _git("rev-parse", "HEAD").strip()
        assert PR_BASE_SHA != head
        assert _git("merge-base", PR_BASE_SHA, head).strip() == PR_BASE_SHA


# ======================================================================================
# 12 -- Catalog and register synchronisation
# ======================================================================================


class TestCatalogAndRegisterSynchronisation:
    def test_the_catalog_carries_exactly_one_entry_for_this_decision(self):
        catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
        entries = [d for d in catalog["decisions"] if d["decision_id"] == DECISION_ID]
        assert len(entries) == 1
        entry = entries[0]
        assert entry["status"] == "Proposed"
        assert entry["file"] == DECISION_RELPATH
        assert entry["supporting_artifact"] == Path(__file__).name

    def test_the_register_records_this_units_gate(self, ws0014):
        gates = {g["gate"]: g for g in ws0014["milestones"]}
        assert GATE_SELF in gates
        assert gates[GATE_SELF]["status"] == "in_progress", (
            "a filing may not mark its own unmerged work complete"
        )
        assert gates[GATE_SELF]["pr"] == 344, (
            "the gate records its own real pull-request number while in progress"
        )

    def test_the_prior_gates_own_text_is_not_rewritten(self, ws0014):
        """Additive synchronisation: the predecessor's narrative survives byte-for-byte."""
        live = {g["gate"]: g for g in ws0014["milestones"]}
        assert GATE_PRIOR in live
        at_merge = yaml.safe_load(
            _blob_at(A.REBINDING_AUTHORIZING_MERGE_SHA, "operations/WORKSTREAMS.yaml")
            .decode("utf-8")
        )
        prior_ws = next(w for w in at_merge["workstreams"] if w.get("id") == "WS-0014")
        prior = {g["gate"]: g for g in prior_ws["milestones"]}
        assert live[GATE_PRIOR]["description"] == prior[GATE_PRIOR]["description"]

    def test_the_register_records_the_current_module_identity(self, ws0014):
        """Unchanged property, and it still holds: the register carries the LIVE module identity.

        XASSET-0047 recomputed it once, after every permitted byte stabilised, and recorded it in
        its own gate. This decision's own recorded identity is retained beside it as history
        rather than overwritten, and that retention is asserted here too.
        """
        # RE-ANCHORED BY XASSET-0049. Each unit's gate records the module identity THAT unit
        # produced, and every one of them is retained rather than overwritten. The live identity
        # is recorded by the LIVE unit's own gate, which is that unit's own suite's subject.
        register = REGISTER_PATH.read_text(encoding="utf-8")
        flat = register.replace("\n", "").replace(" ", "")
        current = hashlib.sha256((ROOT / AUTH_MODULE_RELPATH).read_bytes()).hexdigest()
        assert current in flat
        assert XASSET_0042_FINAL_MODULE_SHA256 in flat
        assert XASSET_0047_FINAL_MODULE_SHA256 in flat

    def test_the_workstream_posture_is_unchanged(self, ws0014):
        # ADVANCED BY XASSET-0045: `last_verified_main_sha` is WS-0014's SINGLE SHARED live
        # self-reference field, not this decision's anchor. PR #344 merged at `f5dedce1`, so
        # under OPS-0001's Active-GitHub-fields rule it lawfully advances to the unit that is
        # now live. `PR_BASE_SHA` -- the anchor THIS decision authorizes against -- is
        # unchanged, and is asserted here to be exactly what it must no longer be showing, so
        # the field is still pinned to an exact value at both ends rather than relaxed.
        assert ws0014["status"] == "proposed"
        assert ws0014["priority"] == "secondary"
        assert ws0014["last_verified_main_sha"] != PR_BASE_SHA
        # ADVANCED BY XASSET-0049. This is WS-0014's SINGLE SHARED live self-reference and moves
        # with every unit; each generation's own value is retained as a NEGATIVE pin so a silent
        # revert to any finished unit's state still fails here.
        assert ws0014["last_verified_main_sha"] == XASSET0056_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0055_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0053_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0052_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0051_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0050_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0049_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0048_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0047_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0046_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0045_MAIN_SHA


# ======================================================================================
# 13 -- No section is vacuous
# ======================================================================================


# =============================================================================================
# Bounded correction after independent FULL review 4986931575.
#
# Three findings, each reproduced through its REAL public mechanism before being corrected, and
# each pinned here by the negative cases the review named. These use the accepted production
# harness (``test_level1_stage1_execution_authorization``'s injectable truth sources) so they
# exercise ``validate_authorization_document`` itself rather than a private helper.
# =============================================================================================


def _valid_document():
    """A document that validates cleanly, assembled by the module's own public builder."""
    doc = H.AUTH.build_authorization_payload(
        authorization_head=H.HEAD,
        lifecycle_evidence=H.lifecycle(),
        author_identity=H.AUTHOR_LOGIN,
        generated_at_utc="2026-08-16T00:00:00Z",
        merge_sha=H.MERGE,
    )
    doc["load_bearing_identity"] = {
        rel: A.sha256_file(ROOT / rel) for rel in sorted(A.LOAD_BEARING_RELPATHS)
    }
    return doc


def _refused(doc, fragment, *, git=None, governance=None):
    result = A.validate_authorization_document(
        doc, H.sources(git=git, governance=governance)
    )
    assert not result.valid, f"expected refusal for {fragment!r}; document validated"
    assert any(fragment in e for e in result.errors), (
        f"expected an error containing {fragment!r}, got {result.errors}"
    )


class TestLifecycleClosureIsAuthenticated:
    """BLOCKING 1 -- SS-L condition 7 is a gate, not a claim.

    SS-L makes seven conditions conjunctively necessary. Before this correction the runtime
    authenticated six and stopped, so a document naming NO closure at all validated -- meaning an
    attestation could be assembled the moment merge-commit CI went green, strictly earlier than
    this decision's own stated effectivity. Reproduced through the public path before correcting.
    """

    def test_the_baseline_document_still_validates(self):
        # The gate must refuse the bad cases WITHOUT refusing the good one.
        result = A.validate_authorization_document(_valid_document(), H.sources())
        assert result.valid, result.errors

    def test_closure_evidence_is_structurally_required(self):
        assert "lifecycle_closure" in A.REQUIRED_LIFECYCLE_EVIDENCE_KEYS

    def test_missing_closure_is_refused(self):
        doc = _valid_document()
        del doc["lifecycle_evidence"]["lifecycle_closure"]
        _refused(doc, "lifecycle_closure")

    def test_a_nonexistent_closure_comment_is_refused(self):
        doc = _valid_document()
        doc["lifecycle_evidence"]["lifecycle_closure"]["comment_id"] = "9999999999"
        _refused(doc, "does not exist")

    def test_wrong_actor_is_refused(self):
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.comments[H.CLOSURE_ID] = dict(gov.comments[H.CLOSURE_ID], user={"login": "claude[bot]"})
        _refused(_valid_document(), "not the lifecycle operator", governance=gov)

    def test_the_pr337_bot_ratification_does_not_reach_this_gate(self):
        """XASSET-0042's exception is pinned to two PR #337 comment ids on two pre-existing
        gates. It must never become forward permission for a bot-authored closure."""
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.comments[H.CLOSURE_ID] = dict(gov.comments[H.CLOSURE_ID], user={"login": "claude[bot]"})
        _refused(_valid_document(), "not the lifecycle operator", governance=gov)

    def test_wrong_pull_request_is_refused(self):
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.comments[H.CLOSURE_ID] = dict(
            gov.comments[H.CLOSURE_ID],
            issue_url="https://api.github.com/repos/Mast3rkey/Portfolio-HQ/issues/999",
        )
        _refused(_valid_document(), "does not belong to pull request", governance=gov)

    def test_wrong_merge_sha_is_refused(self):
        doc = _valid_document()
        doc["lifecycle_evidence"]["lifecycle_closure"]["closed_merge_sha"] = "9" * 40
        _refused(doc, "closed_merge_sha")

    def test_wrong_run_id_is_refused(self):
        doc = _valid_document()
        doc["lifecycle_evidence"]["lifecycle_closure"]["closed_run_id"] = "1234567890"
        _refused(doc, "closed_run_id")

    def test_wrong_job_id_is_refused(self):
        doc = _valid_document()
        doc["lifecycle_evidence"]["lifecycle_closure"]["closed_job_id"] = "1234567890"
        _refused(doc, "closed_job_id")

    def test_a_closure_body_not_naming_the_merge_is_refused(self):
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.comments[H.CLOSURE_ID] = dict(
            gov.comments[H.CLOSURE_ID], body=f"Closed. Run {H.RUN_ID}."
        )
        _refused(_valid_document(), "does not name the merge SHA", governance=gov)

    def test_a_closure_body_not_naming_the_ci_run_is_refused(self):
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.comments[H.CLOSURE_ID] = dict(
            gov.comments[H.CLOSURE_ID], body=f"Closed for merge `{H.MERGE}`."
        )
        _refused(_valid_document(), "does not name the merge-commit CI run", governance=gov)

    def test_closure_before_post_merge_verification_is_refused(self):
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.comments[H.CLOSURE_ID] = dict(
            gov.comments[H.CLOSURE_ID], created_at="2026-08-16T12:30:00Z"
        )
        _refused(_valid_document(), "does not follow post-merge verification", governance=gov)

    def test_closure_simultaneous_with_verification_is_refused(self):
        """Strictly after, not merely not-before: an identical instant proves no ordering."""
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.comments[H.CLOSURE_ID] = dict(
            gov.comments[H.CLOSURE_ID], created_at=gov.comments[H.VERIFY_ID]["created_at"]
        )
        _refused(_valid_document(), "does not follow post-merge verification", governance=gov)

    def test_closure_before_ci_completion_is_refused(self):
        """PREMATURE CLOSURE -- the exact hole the review named: after verification, but before
        the merge-commit CI job it claims to close actually finished."""
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.comments[H.CLOSURE_ID] = dict(
            gov.comments[H.CLOSURE_ID], created_at="2026-08-16T13:10:00Z"
        )
        gov.jobs = dict(gov.jobs)
        gov.jobs[H.JOB_ID] = dict(gov.jobs[H.JOB_ID], completed_at="2026-08-16T13:30:00Z")
        gov.runs = dict(gov.runs)
        gov.runs[H.RUN_ID] = dict(gov.runs[H.RUN_ID], updated_at="2026-08-16T13:30:00Z")
        # Message wording corrected by delta review 4987958687 MAJOR 1 part 2, when the
        # comparison became strict. The assertion is unchanged in force: still a refusal.
        _refused(_valid_document(), "does not strictly follow", governance=gov)

    def test_an_unresolvable_ci_completion_time_fails_closed(self):
        gov = H.FakeGovernance()
        gov.jobs = {H.JOB_ID: {"run_id": H.RUN_ID, "conclusion": "success", "head_sha": H.MERGE}}
        gov.runs = {
            H.RUN_ID: {"status": "completed", "conclusion": "success", "head_sha": H.MERGE}
        }
        _refused(_valid_document(), "completion time could not be resolved", governance=gov)

    def test_an_unknown_closure_key_is_refused(self):
        doc = _valid_document()
        doc["lifecycle_evidence"]["lifecycle_closure"]["approved"] = True
        _refused(doc, "the schema is closed")

    def test_the_closure_schema_is_closed_and_exact(self):
        assert A.LIFECYCLE_CLOSURE_KEYS == (
            "comment_id", "closed_merge_sha", "closed_run_id", "closed_job_id",
        )

    def test_the_six_gate_tuple_and_canonical_strings_are_untouched(self):
        """The correction is bounded: the seventh condition gets its own gate WITHOUT rewriting
        the six-gate list that the canonical ``..._ALL_SIX_GATES_...`` strings name verbatim."""
        assert len(A.REQUIRED_LIFECYCLE_GATES) == 6
        assert "LIFECYCLE_CLOSURE" not in " ".join(A.REQUIRED_LIFECYCLE_GATES)
        assert "ALL_SIX_GATES" in PREREG.STAGE_1_EXECUTION_PRECONDITION


class TestCorrectionAuthorizationMergeIsFullyVerified:
    """MAJOR 1 -- PR #341's inherited merge was only half-checked.

    Its base and accepted head were ``None``, and the verification loop skips BOTH the
    exact-parent and the merge-tree check whenever either is absent. Reproduced through
    ``validate_authorization_document`` before correcting: a PR #341 merge rewritten to a single
    WRONG parent with a DRIFTED tree still validated.
    """

    def test_the_identities_are_bound(self):
        assert A.CORRECTION_AUTHORIZING_MERGE_BASE == "f212cce50e28ae887dc8c594bf8ae491a3ef85af"
        assert A.CORRECTION_AUTHORIZING_ACCEPTED_HEAD == "0449d08217b5c0e422721ff3ef76b4241fb8a95a"

    def test_the_bound_identities_match_the_real_object_store(self):
        """Independently re-derived, not taken from the review on faith."""
        out = subprocess.run(
            ["git", "rev-parse", f"{A.CORRECTION_AUTHORIZING_MERGE_SHA}^@"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
        assert out == [
            A.CORRECTION_AUTHORIZING_MERGE_BASE,
            A.CORRECTION_AUTHORIZING_ACCEPTED_HEAD,
        ]

    def test_the_real_merge_carries_zero_drift(self):
        def tree(rev):
            return subprocess.run(
                ["git", "rev-parse", f"{rev}^{{tree}}"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout.strip()
        assert tree(A.CORRECTION_AUTHORIZING_MERGE_SHA) == tree(
            A.CORRECTION_AUTHORIZING_ACCEPTED_HEAD
        )

    def test_the_identities_are_in_the_closed_payload(self):
        block = _valid_document()["correction_identity"]
        assert block["authorizing_merge_base"] == A.CORRECTION_AUTHORIZING_MERGE_BASE
        assert block["authorizing_accepted_head"] == A.CORRECTION_AUTHORIZING_ACCEPTED_HEAD

    def test_wrong_parent_count_is_refused(self):
        git = H.FakeGit()
        git.parents = dict(git.parents)
        git.parents[A.CORRECTION_AUTHORIZING_MERGE_SHA] = (A.CORRECTION_AUTHORIZING_MERGE_BASE,)
        _refused(_valid_document(), "merge parents", git=git)

    def test_wrong_parent_order_is_refused(self):
        """Order is the whole point: base then accepted head, never the reverse."""
        git = H.FakeGit()
        git.parents = dict(git.parents)
        git.parents[A.CORRECTION_AUTHORIZING_MERGE_SHA] = (
            A.CORRECTION_AUTHORIZING_ACCEPTED_HEAD,
            A.CORRECTION_AUTHORIZING_MERGE_BASE,
        )
        _refused(_valid_document(), "are not exactly", git=git)

    def test_merge_tree_drift_is_refused(self):
        git = H.FakeGit()
        git.trees = dict(git.trees)
        git.trees[A.CORRECTION_AUTHORIZING_MERGE_SHA] = "0" * 40
        _refused(_valid_document(), "carries drift the review never saw", git=git)

    def test_an_unresolvable_tree_fails_closed(self):
        git = H.FakeGit()
        git.trees = dict(git.trees)
        del git.trees[A.CORRECTION_AUTHORIZING_ACCEPTED_HEAD]
        _refused(_valid_document(), "zero merge drift cannot be proven", git=git)

    def test_no_inherited_merge_is_bound_without_complete_identity(self):
        """The hole was OMISSION, so omission itself must now fail rather than skip."""
        source = (ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        assert "is bound without a complete " in source
        assert "elif inherited_base is not None and" not in source
        assert "if inherited_head is not None:" not in source


class TestGate8BodyIdentityAndStrictPostCiOrder:
    """Delta review 4987958687 MAJOR 1 -- two conjuncts Gate 8 declared but did not enforce.

    Both were reproduced through the public ``verify_lifecycle_against_truth`` path before being
    corrected: a closure body naming the merge and run while OMITTING the job returned no errors,
    and so did one carrying a SUBSTITUTED job; and a closure whose timestamp EQUALLED the CI job's
    ``completed_at`` passed the chronology branch, against both the job's own time and the
    run-time fallback.
    """

    def test_the_baseline_document_still_validates(self):
        result = A.validate_authorization_document(_valid_document(), H.sources())
        assert result.valid, result.errors

    # --- part 1: the durable body must name the exact job ---------------------------------

    def test_a_body_omitting_the_job_id_is_refused(self):
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.comments[H.CLOSURE_ID] = dict(
            gov.comments[H.CLOSURE_ID],
            body=f"Lifecycle closure for merge `{H.MERGE}`, run {H.RUN_ID}.",
        )
        _refused(_valid_document(), "does not name the merge-commit CI job", governance=gov)

    def test_a_body_naming_a_substituted_job_id_is_refused(self):
        """A run can carry more than one job, so naming the run does not identify the job whose
        completion the closure claims to follow."""
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.comments[H.CLOSURE_ID] = dict(
            gov.comments[H.CLOSURE_ID],
            body=f"Lifecycle closure for merge `{H.MERGE}`, run {H.RUN_ID}, job 9999999999.",
        )
        _refused(_valid_document(), "does not name the merge-commit CI job", governance=gov)

    def test_the_three_body_identities_are_independently_required(self):
        """Merge, run, and job each on their own -- dropping any one is refused."""
        for missing, fragment in (
            ("merge", "does not name the merge SHA"),
            ("run", "does not name the merge-commit CI run"),
            ("job", "does not name the merge-commit CI job"),
        ):
            parts = {
                "merge": f"merge `{H.MERGE}`",
                "run": f"run {H.RUN_ID}",
                "job": f"job {H.JOB_ID}",
            }
            del parts[missing]
            gov = H.FakeGovernance()
            gov.comments = dict(gov.comments)
            gov.comments[H.CLOSURE_ID] = dict(
                gov.comments[H.CLOSURE_ID],
                body="Lifecycle closure for " + ", ".join(parts.values()) + ".",
            )
            _refused(_valid_document(), fragment, governance=gov)

    # --- part 2: strictly after, on the CI conjunct too ------------------------------------

    def test_closure_equal_to_job_completion_is_refused(self):
        """Second-resolution equality cannot distinguish "closed after CI finished" from "closed
        in the same second, order unknown". An unprovable ordering is not a proven one."""
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.jobs = dict(gov.jobs)
        gov.jobs[H.JOB_ID] = dict(gov.jobs[H.JOB_ID], completed_at="2026-08-16T13:30:00Z")
        gov.comments[H.CLOSURE_ID] = dict(
            gov.comments[H.CLOSURE_ID], created_at="2026-08-16T13:30:00Z"
        )
        _refused(_valid_document(), "does not strictly follow", governance=gov)

    def test_closure_equal_to_the_run_time_fallback_is_refused(self):
        """The same rule on the fallback path, where the job carries no completion time."""
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.jobs = {
            H.JOB_ID: {"run_id": H.RUN_ID, "conclusion": "success", "head_sha": H.MERGE}
        }
        gov.runs = dict(gov.runs)
        gov.runs[H.RUN_ID] = dict(gov.runs[H.RUN_ID], updated_at="2026-08-16T13:30:00Z")
        gov.comments[H.CLOSURE_ID] = dict(
            gov.comments[H.CLOSURE_ID], created_at="2026-08-16T13:30:00Z"
        )
        _refused(_valid_document(), "does not strictly follow", governance=gov)

    def test_closure_one_second_after_job_completion_is_accepted(self):
        """Strictly after is satisfiable: the rule refuses equality, not the ordering itself."""
        gov = H.FakeGovernance()
        gov.comments = dict(gov.comments)
        gov.jobs = dict(gov.jobs)
        gov.jobs[H.JOB_ID] = dict(gov.jobs[H.JOB_ID], completed_at="2026-08-16T13:30:00Z")
        gov.comments[H.CLOSURE_ID] = dict(
            gov.comments[H.CLOSURE_ID], created_at="2026-08-16T13:30:01Z"
        )
        result = A.validate_authorization_document(
            _valid_document(), H.sources(governance=gov)
        )
        assert result.valid, result.errors

    def test_the_ci_chronology_branch_uses_strict_comparison(self):
        source = (ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        assert "elif closed_at <= finished_at:" in source
        assert "elif closed_at < finished_at:" not in source

    def test_the_verification_chronology_branch_is_still_strict(self):
        """The correction must not have loosened the conjunct that was already correct."""
        source = (ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        assert "elif closed_at <= verified_at:" in source


class TestOperatorStatusReasonNamesTheSeventhCondition:
    """Delta review 4987958687 MINOR 1 -- the public status reason understated the requirement.

    With no attestation the reason printed only ``REQUIRED_LIFECYCLE_GATES``, the intentionally
    preserved six-item predecessor tuple, so an operator reading it would not learn that final
    post-CI lifecycle closure is now additionally mandatory.
    """

    def test_the_requirement_string_exists_and_is_specific(self):
        text = A.LIFECYCLE_CLOSURE_STATUS_REQUIREMENT
        assert "FINAL POST-CI LIFECYCLE CLOSURE is additionally mandatory" in text
        for phrase in (
            "lifecycle operator",
            "merge SHA",
            "run and job",
            "strictly after",
            "post-merge verification",
        ):
            assert phrase in text, phrase

    def test_the_no_attestation_reason_states_it(self):
        authorized, reason = A.new_execution_is_authorized()
        assert authorized is False
        assert A.LIFECYCLE_CLOSURE_STATUS_REQUIREMENT in reason

    def test_the_reason_still_prints_all_six_accepted_gates_verbatim(self):
        """Corrected SEPARATELY, exactly as the review required: the accepted tuple is added to,
        never rewritten."""
        _, reason = A.new_execution_is_authorized()
        for gate in A.REQUIRED_LIFECYCLE_GATES:
            assert gate in reason, gate

    def test_the_six_gate_tuple_and_canonical_strings_remain_byte_identical(self):
        assert A.REQUIRED_LIFECYCLE_GATES == (
            "INDEPENDENT_FULL_EXACT_HEAD_REVIEW",
            "PRINCIPAL_EXACT_HEAD_ACCEPTANCE",
            "MERGE",
            "POST_MERGE_VERIFICATION",
            "MERGE_COMMIT_CI_SUCCESS",
            "MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION",
        )
        assert "ALL_SIX_GATES" in PREREG.STAGE_1_EXECUTION_PRECONDITION
        # MINOR 1 (delta review 4988858926): this line previously read
        #     assert "ALL_SIX_GATES" in PREREG.STAGE_1_BLOCKING_PREREQUISITE or True
        # which can never fail. The blocking prerequisite does NOT contain "ALL_SIX_GATES" -- the
        # left operand is false -- so the fallback masked a false premise while the test's own name
        # claimed byte identity. Replaced with the exact value, which is what the test meant to
        # preserve, rather than merely deleting the clause and losing the coverage it claimed.
        assert PREREG.STAGE_1_BLOCKING_PREREQUISITE == (
            "XASSET_0044_LIFECYCLE_CLOSURE_THEN_EXTERNAL_ONE_SHOT_PREEXECUTION_ATTESTATION"
        )
        # every predecessor-named canonical string keeps its own generation
        assert "XASSET_0037" in PREREG.PREDECESSOR_STAGE_1_EXECUTION_PRECONDITION_XASSET_0037

    def test_the_status_reason_still_reports_unauthorized(self):
        """The correction changes the EXPLANATION, never the verdict."""
        authorized, _ = A.new_execution_is_authorized()
        assert authorized is False

    def test_the_requirement_is_not_smuggled_into_the_gate_tuple(self):
        assert A.LIFECYCLE_CLOSURE_STATUS_REQUIREMENT not in A.REQUIRED_LIFECYCLE_GATES
        assert len(A.REQUIRED_LIFECYCLE_GATES) == 6


def _closure_body(body: str):
    """A governance stand-in whose lifecycle-closure record carries exactly ``body``."""
    gov = H.FakeGovernance()
    gov.comments = dict(gov.comments)
    gov.comments[H.CLOSURE_ID] = dict(gov.comments[H.CLOSURE_ID], body=body)
    return gov


class TestClosureBodyIdentitiesAreCompleteTokens:
    """MAJOR 1 (delta review 4988858926) -- substring containment is not identity.

    Reproduced through the public ``verify_lifecycle_against_truth`` path before correcting: a
    closure body whose only mentions were ``<merge>0``, ``<run>0`` and ``<job>0`` returned no
    errors, because each real sequence sits inside a different, longer identifier. A job id that
    merely CONTAINS the real job id is a different job, so such a body does not identify the job
    whose completion the closure claims to follow.

    All three identities now go through one shared boundary-aware mechanism, so they cannot drift
    apart into three separately-worded checks again.
    """

    NOT_A_TOKEN = "as a complete token"

    # --- the genuine body must still be accepted -------------------------------------------

    def test_the_canonical_body_is_accepted(self):
        result = A.validate_authorization_document(_valid_document(), H.sources())
        assert result.valid, result.errors

    @pytest.mark.parametrize("body_template", [
        "Lifecycle closure for merge `{m}`, run {r}, job {j}.",
        "Closure: merge {m} run {r} job {j}",
        "Closure (merge {m}) [run {r}] {{job {j}}}",
        "merge {m}\nrun {r}\njob {j}",
        "merge={m}; run={r}; job={j}",
    ])
    def test_ordinary_punctuation_and_whitespace_are_boundaries(self, body_template):
        """The mechanism must not reject genuine bodies to achieve strictness."""
        gov = _closure_body(body_template.format(m=H.MERGE, r=H.RUN_ID, j=H.JOB_ID))
        result = A.validate_authorization_document(
            _valid_document(), H.sources(governance=gov)
        )
        assert result.valid, result.errors

    # --- the exact case the review reproduced ----------------------------------------------

    def test_the_reviews_superset_body_is_refused(self):
        """All three identities present ONLY inside a longer token, exactly as reported."""
        gov = _closure_body(
            f"Lifecycle closure for merge `{H.MERGE}0`, run {H.RUN_ID}0, job {H.JOB_ID}0."
        )
        _refused(_valid_document(), self.NOT_A_TOKEN, governance=gov)

    # --- one extra character before and after EACH identity ---------------------------------

    @pytest.mark.parametrize("extra", ["a", "f", "0", "9"])
    def test_a_hex_character_before_the_merge_sha_is_refused(self, extra):
        gov = _closure_body(f"merge `{extra}{H.MERGE}`, run {H.RUN_ID}, job {H.JOB_ID}")
        _refused(_valid_document(), "merge SHA", governance=gov)

    @pytest.mark.parametrize("extra", ["a", "f", "0", "9"])
    def test_a_hex_character_after_the_merge_sha_is_refused(self, extra):
        gov = _closure_body(f"merge `{H.MERGE}{extra}`, run {H.RUN_ID}, job {H.JOB_ID}")
        _refused(_valid_document(), "merge SHA", governance=gov)

    @pytest.mark.parametrize("extra", ["0", "1", "7", "9"])
    def test_a_digit_before_the_run_id_is_refused(self, extra):
        gov = _closure_body(f"merge `{H.MERGE}`, run {extra}{H.RUN_ID}, job {H.JOB_ID}")
        _refused(_valid_document(), "merge-commit CI run", governance=gov)

    @pytest.mark.parametrize("extra", ["0", "1", "7", "9"])
    def test_a_digit_after_the_run_id_is_refused(self, extra):
        gov = _closure_body(f"merge `{H.MERGE}`, run {H.RUN_ID}{extra}, job {H.JOB_ID}")
        _refused(_valid_document(), "merge-commit CI run", governance=gov)

    @pytest.mark.parametrize("extra", ["0", "1", "7", "9"])
    def test_a_digit_before_the_job_id_is_refused(self, extra):
        gov = _closure_body(f"merge `{H.MERGE}`, run {H.RUN_ID}, job {extra}{H.JOB_ID}")
        _refused(_valid_document(), "merge-commit CI job", governance=gov)

    @pytest.mark.parametrize("extra", ["0", "1", "7", "9"])
    def test_a_digit_after_the_job_id_is_refused(self, extra):
        gov = _closure_body(f"merge `{H.MERGE}`, run {H.RUN_ID}, job {H.JOB_ID}{extra}")
        _refused(_valid_document(), "merge-commit CI job", governance=gov)

    # --- embedded inside larger tokens, and concatenated ------------------------------------

    def test_identities_embedded_in_larger_alphanumeric_tokens_are_refused(self):
        gov = _closure_body(f"X{H.MERGE}X Y{H.RUN_ID}Y Z{H.JOB_ID}Z")
        _refused(_valid_document(), self.NOT_A_TOKEN, governance=gov)

    def test_identities_concatenated_together_are_refused(self):
        """Each identity is adjacent to the next, so none of the three is a complete token."""
        gov = _closure_body(f"{H.MERGE}{H.RUN_ID}{H.JOB_ID}")
        _refused(_valid_document(), self.NOT_A_TOKEN, governance=gov)

    def test_an_underscore_joined_suffix_is_refused(self):
        gov = _closure_body(f"merge `{H.MERGE}`, run {H.RUN_ID}_2, job {H.JOB_ID}")
        _refused(_valid_document(), "merge-commit CI run", governance=gov)

    # --- omission and unrelated substitution, preserved from the prior round -----------------

    @pytest.mark.parametrize("drop,fragment", [
        ("merge", "merge SHA"),
        ("run", "merge-commit CI run"),
        ("job", "merge-commit CI job"),
    ])
    def test_omitting_each_identity_is_refused(self, drop, fragment):
        parts = {
            "merge": f"merge `{H.MERGE}`",
            "run": f"run {H.RUN_ID}",
            "job": f"job {H.JOB_ID}",
        }
        del parts[drop]
        _refused(
            _valid_document(), fragment,
            governance=_closure_body("Closure for " + ", ".join(parts.values()) + "."),
        )

    @pytest.mark.parametrize("swap,replacement,fragment", [
        ("merge", "c" * 40, "merge SHA"),
        ("run", "1234567890", "merge-commit CI run"),
        ("job", "1234567890", "merge-commit CI job"),
    ])
    def test_an_unrelated_substituted_identity_is_refused(self, swap, replacement, fragment):
        parts = {
            "merge": f"merge `{H.MERGE}`",
            "run": f"run {H.RUN_ID}",
            "job": f"job {H.JOB_ID}",
        }
        parts[swap] = {
            "merge": f"merge `{replacement}`",
            "run": f"run {replacement}",
            "job": f"job {replacement}",
        }[swap]
        _refused(
            _valid_document(), fragment,
            governance=_closure_body("Closure for " + ", ".join(parts.values()) + "."),
        )

    # --- the mechanism itself, directly ------------------------------------------------------

    def test_the_mechanism_is_shared_by_all_three_identities(self):
        """One mechanism, so the three checks cannot drift apart again."""
        source = (ROOT / "level1_stage1_execution_authorization.py").read_text(encoding="utf-8")
        assert source.count("body_names_identity(body, identity)") == 1
        assert "not in body" not in source

    @pytest.mark.parametrize("body,identity,expected", [
        ("abc 1234 def", "1234", True),
        ("abc `1234` def", "1234", True),
        ("abc 1234, def", "1234", True),
        ("abc\n1234\ndef", "1234", True),
        ("abc 12345 def", "1234", False),
        ("abc 01234 def", "1234", False),
        ("abc x1234 def", "1234", False),
        ("abc 1234x def", "1234", False),
        ("abc 1234_ def", "1234", False),
        ("abc _1234 def", "1234", False),
        ("abc def", "1234", False),
        ("abc 1234 def", "", False),
        ("abc 1234 def", None, False),
        (None, "1234", False),
    ])
    def test_body_names_identity_boundary_behaviour(self, body, identity, expected):
        assert A.body_names_identity(body, identity) is expected

    def test_the_mechanism_treats_regex_metacharacters_literally(self):
        """An identity is a literal token, never a pattern: a body must not match by wildcard."""
        assert A.body_names_identity("run a.c", "a.c") is True
        assert A.body_names_identity("run abc", "a.c") is False


def _unconditional_or_fallbacks(source: str) -> list[str]:
    """Assertions made unfalsifiable by a constant-truthy disjunct: ``assert X or True``.

    THE detection mechanism -- module level, and used by BOTH the live-corpus guard below and the
    falsifiability proofs beside it. An earlier draft re-implemented this logic inside the proof,
    so disabling the real check changed nothing and two mutation probes went MISSED: the guard was
    decoration. Sharing one function is what makes those probes bite.
    """
    offenders = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Assert):
            continue
        test = node.test
        if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.Or):
            for value in test.values:
                if isinstance(value, ast.Constant) and bool(value.value):
                    offenders.append(
                        f"line {node.lineno}: `or {value.value!r}` makes the assertion vacuous"
                    )
    return offenders


def _bare_truthy_assertions(source: str) -> list[str]:
    """``assert True`` / ``assert 1`` / ``assert "text"`` -- assert nothing about the system.

    Shared for the same reason as above.
    """
    return [
        f"line {n.lineno}: bare truthy constant {n.test.value!r}"
        for n in ast.walk(ast.parse(source))
        if isinstance(n, ast.Assert)
        and isinstance(n.test, ast.Constant)
        and bool(n.test.value)
    ]


class TestSuiteHygieneNoUnconditionalFallbacks:
    """MINOR 1 (delta review 4988858926) -- an assertion that cannot fail is not coverage.

    A vacuous ``or True`` reached this suite and survived a full review round while its own test
    name claimed byte identity. Deleting the clause alone would have removed the false premise but
    also the coverage it claimed, so the assertion was replaced with the exact value AND this guard
    was added so the shape cannot recur silently.

    Implemented over the parsed AST, not a substring scan: a text search would flag this very
    docstring and every explanatory comment about the defect, which is how such a guard becomes
    unusable and then gets deleted.
    """

    SUITE = Path(__file__)

    def _source(self) -> str:
        return self.SUITE.read_text(encoding="utf-8")

    def test_no_assertion_is_unconditionally_true(self):
        offenders = _unconditional_or_fallbacks(self._source())
        assert offenders == [], "unconditionally-true assertions found:\n" + "\n".join(offenders)

    def test_no_assertion_is_a_bare_truthy_constant(self):
        offenders = _bare_truthy_assertions(self._source())
        assert offenders == [], "vacuous constant assertions found:\n" + "\n".join(offenders)

    def test_the_or_fallback_detector_is_falsifiable(self):
        """A hygiene guard that cannot detect its own target is decoration. Exercises the REAL
        detector against synthetic source, so disabling it fails here."""
        assert len(_unconditional_or_fallbacks('assert "X" in y or True\n')) == 1
        assert len(_unconditional_or_fallbacks("assert True or check()\n")) == 1
        assert len(_unconditional_or_fallbacks("assert value or 1\n")) == 1
        assert len(_unconditional_or_fallbacks('assert value or "text"\n')) == 1
        # genuine disjunctions of real expressions are untouched
        assert _unconditional_or_fallbacks("assert a or b\n") == []
        assert _unconditional_or_fallbacks("assert a == 1 or a == 2\n") == []
        # a falsey constant disjunct narrows nothing but also hides nothing
        assert _unconditional_or_fallbacks("assert check() or False\n") == []
        # and the guard must not fire on non-assert code
        assert _unconditional_or_fallbacks("x = y or True\n") == []

    def test_the_bare_constant_detector_is_falsifiable(self):
        """Likewise for the second detector, exercising the real function."""
        assert len(_bare_truthy_assertions("assert True\n")) == 1
        assert len(_bare_truthy_assertions("assert 1\n")) == 1
        assert len(_bare_truthy_assertions('assert "text"\n')) == 1
        assert _bare_truthy_assertions("assert False\n") == []
        assert _bare_truthy_assertions("assert 0\n") == []
        assert _bare_truthy_assertions("assert check()\n") == []
        assert _bare_truthy_assertions("x = True\n") == []

    def test_the_detectors_see_this_suites_real_source(self):
        """Not vacuous by reading an empty or wrong file: the real source must parse to a large
        number of real assertions, so a clean result means CHECKED-and-clean."""
        statements = [
            n for n in ast.walk(ast.parse(self._source())) if isinstance(n, ast.Assert)
        ]
        assert len(statements) > 200, len(statements)

    def test_the_blocking_prerequisite_assertion_is_now_falsifiable(self):
        """The specific line MINOR 1 named: it must compare against a real, wrong-able value."""
        real = PREREG.STAGE_1_BLOCKING_PREREQUISITE
        assert real == (
            "XASSET_0044_LIFECYCLE_CLOSURE_THEN_EXTERNAL_ONE_SHOT_PREEXECUTION_ATTESTATION"
        )
        # and the premise the vacuous clause masked is recorded as the falsehood it was
        assert "ALL_SIX_GATES" not in real


class TestNoSectionIsVacuous:
    @pytest.mark.parametrize("letter", list("ABCDEFGHIJKL"))
    def test_each_section_exists_and_says_something(self, sections, letter):
        assert letter in sections, f"§{letter} is missing"
        body = sections[letter]
        assert len(body.strip()) > 400, f"§{letter} is too thin to constrain anything"

    def test_the_effectivity_section_requires_all_seven_conditions(self, flat_sections):
        text = flat_sections["L"]
        for condition in (
            "independent **FULL** exact-head review",
            "bounded correction and exact-head re-review",
            "principal exact-head acceptance",
            "normal merge",
            "immediate post-merge verification",
            "merge-commit CI whose `head_sha` is the exact merge SHA",
            "final post-CI verification and lifecycle closure",
        ):
            assert condition in text, condition
        assert "None is individually sufficient" in text
