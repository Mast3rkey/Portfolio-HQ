"""Adversarial tests pinning the ``XASSET-0043`` post-correction rebinding authorization.

``XASSET-0041`` §I enumerates five links after the ``XASSET-0040`` step-11 stop, each requiring its
own separate governance authority and its own complete lifecycle. Link 1 -- the correction -- is
merged and effective as ``XASSET-0042``, which lawfully changed ``level1_stage1_execution_authorization.py``
and thereby created the enforcement drift ``XASSET-0030`` §D recorded in advance. ``XASSET-0043``
supplies the authority for link 2, the rebinding, and for nothing else.

The danger here is not the rebinding -- it is the *reach* a session might read into a filing that
sits one merged correction away from an armable Stage 1. Every guard below exists to make a broader
reading impossible to take from the text:

1. **The filing performs the rebinding, or is treated as having performed it.**
   ``TestFilingIsGovernanceOnly`` and ``TestNoProtectedByteWasTouched``.
2. **The drift reproduction inflated into the authorized step-9 or step-10 unit.**
   ``TestDriftReproducedReadOnlyOnly`` -- the reproduction is git-object-level and touches no lane.
3. **`§G.B` step 8 claimed a second time, or `XASSET-0037` treated as invalidated.**
   ``TestStep8NotReconsumed`` -- the single most easily-flattered claim in this filing.
4. **More than one unit authorized, or links 3-5 pre-authorized.**
   ``TestExactlyOneFutureRebindingAuthorized`` and ``TestDownstreamLinksNotAuthorized``.
5. **A required property softened into advice.** ``TestTenRequiredProperties``.
6. **A load-bearing path dropped, or an exact-byte check weakened, to make a rebinding easier.**
   ``TestLoadBearingPreservationAndGrowth``.
7. **The `XASSET-0042` current-identity guard left to be discovered and deleted.**
   ``TestXasset0042EvidenceMustBeResolved``.
8. **A canonical amendment widened past authorization language, or the universe touched.**
   ``TestCanonicalAmendmentIsAuthorizationLanguageOnly``.
9. **Merging read as arming, `ATTEMPT_1` reached, or `XASSET-0040` revived.**
   ``TestNotAnActivationAndAttemptIntact`` and ``TestP1ResultsPRRemainsSeparate``.
10. **A lifecycle step allowed to stand in for complete closure, or a vacuous section.**
    ``TestEffectivityRequiresCompleteLifecycleClosure`` and ``TestNoSectionIsVacuous``.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No attestation, claim, completion, lane directory, or ledger entry is created or read
for authorization purposes. No ``risk_lane_boundary`` protected result path is read, listed, opened,
or referenced. ``write_authorization`` is never called, and no module capable of producing a Stage-1
outcome is imported.
"""

from __future__ import annotations

import ast
import hashlib
import re
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent

DECISION_ID = "XASSET-0043"
DECISION_PATH = ROOT / (
    "governance/decisions/"
    "XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md"
)
CATALOG_PATH = ROOT / "governance/decisions.yaml"
REGISTER_PATH = ROOT / "operations/WORKSTREAMS.yaml"
SUITE_PATH = Path(__file__).resolve()

AUTH_MODULE_RELPATH = "level1_stage1_execution_authorization.py"

#: The ten load-bearing paths as of this filing. Written literally, never imported, so this
#: file independently pins BOTH the membership and the count of ten.
LOAD_BEARING_RELPATHS_AT_FILING = (
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

#: The four decision files the FUTURE boundary must add (review 4976985695 MAJOR 1). The first
#: three exist now and are checked on disk; the fourth is the future rebinding decision, which by
#: construction cannot be named here -- naming it would reserve an identifier §F forbids reserving.
FUTURE_BOUNDARY_ADDITIONS = (
    "governance/decisions/"
    "XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md",
    "governance/decisions/"
    "XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md",
    "governance/decisions/"
    "XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md",
)

#: The exact base this pull request is measured against. Fixed for the life of the PR: unlike
#: ``HEAD`` it does not move when a correction commit lands, which is precisely why the
#: base->head protected-path proof uses it (review 4976985695 MINOR 1).
PR_BASE_SHA = "5fbfc94d7333e552bd2654261e0c57134a172e31"

#: RE-ANCHORED BY XASSET-0044. This suite's governance-only claims are about PR #343's OWN diff,
#: and that pull request is now merged and closed, so the range it spans is CLOSED: base -> its own
#: merge. Measuring to a moving ``HEAD`` instead silently re-scoped every one of those claims to
#: "and nothing since", which is a different and much larger proposition -- one that any later,
#: separately authorized unit lawfully touching a protected path would falsify, reporting a defect
#: in PR #343 that PR #343 did not commit. This is exactly the moving-anchor defect XASSET-0043
#: SS-I.4 names, applied here to XASSET-0043's own suite. Immutable, so it cannot be satisfied by
#: editing anything today.
PR_MERGE_SHA = "0709d2f05ab031ecb6f69c40465ed4a227983aed"
#: ADDED BY XASSET-0045: PR #344 has since merged, so WS-0014's single shared
#: `last_verified_main_sha` advances to ITS merge. `PR_MERGE_SHA` above is retained
#: unchanged as the closed predecessor anchor this decision authorizes against.
XASSET0044_MERGE_SHA = "f5dedce1d1d3116ed8a6845c4447388c85a5414c"
#: ADVANCED BY XASSET-0046: PR #345 merged at `2f8cdebe`. WS-0014's single shared
#: "where main is now" field advances again under OPS-0001's Active-GitHub-fields rule; the
#: anchor this decision authorizes against is unchanged.
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

#: A real, immutable, historical commit pair in which a protected path GENUINELY changed --
#: PR #342's base and its merge, across which the authorization module was lawfully corrected.
#: Used as a positive control so the base->head comparison can never pass vacuously.
PROTECTED_CHANGE_CONTROL_BEFORE = "9c8647f9dddacdf63825f569097214ba65299fe8"
PROTECTED_CHANGE_CONTROL_AFTER = "5fbfc94d7333e552bd2654261e0c57134a172e31"
PROTECTED_CHANGE_CONTROL_PATH = "level1_stage1_execution_authorization.py"

#: Portfolio and allocator bytes a governance-only filing must never touch.
PORTFOLIO_RELPATHS = (
    "allocate.py",
    "margin_state.py",
    "levels.py",
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
)

PROTECTED_RELPATHS = LOAD_BEARING_RELPATHS_AT_FILING + PORTFOLIO_RELPATHS

#: The bound XASSET-0037 merged tree -- PR #337's merge -- and the three module identities.
BOUND_MERGE_SHA = "637eaa30302f5a71f84ab1d215ecbd32c01399b5"
BOUND_MODULE_SHA256 = "8186a50f71d05bbb7189183bacad6aa0752147e9c7f4e1f5b3bacabad91f2fc8"
INTERMEDIATE_MODULE_SHA256 = (
    "03d842126913bf2d62aa5d7c070ecca236926ec847102da82414ee51e7422734"
)
CURRENT_MODULE_SHA256 = "749597ee9085a189e187e23ccffb7718d98860847dfe514c173e7437b50f24c7"
CURRENT_MODULE_BLOB = "d55b9e1882368a5e8ed888a336a5d00e49b2b05e"

#: PR #342's verified anchors.
CORRECTION_MERGE_SHA = "5fbfc94d7333e552bd2654261e0c57134a172e31"
CORRECTION_ACCEPTED_HEAD = "4d5d99d67364d3c940aad74c3093bd2afbc3481d"
CORRECTION_MERGE_BASE = "9c8647f9dddacdf63825f569097214ba65299fe8"
CORRECTION_MERGE_TREE = "96215644985ae322d78915850bec21b7b247c12d"
CORRECTION_FULL_REVIEW = "4975556072"
CORRECTION_DELTA_REVIEW = "4976030124"
CORRECTION_FINAL_REVIEW = "4976294690"
CORRECTION_ACCEPTANCE = "5347516573"
CORRECTION_VERIFICATION = "5347527432"
CORRECTION_CLOSURE = "5347619800"
CORRECTION_CI_RUN = "32297842564"
CORRECTION_CI_JOB = "96213267167"

#: The preserved outcome-producing and universe identities.
DERIVATION_SUCCESSOR_SHA256 = (
    "2b8ead2b0d661ddd14fa6019ee1802fe49900a214ec443228636701edeb3d356"
)
UNIVERSE_HASH = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"

#: WS-0014's shared `active_pr` while THIS filing is the live work. Set to the real GitHub
#: number issued when the pull request was opened, verified afterwards, never left as a guess.
XASSET0043_ACTIVE_PR = 343
ACTIVE_BRANCH = "claude/xasset-0043-rebinding-auth-1qrj1i"

GATE_SELF = "xasset0043-post-correction-rebinding-authorization"
GATE_PRIOR = "xasset0042-pr337-lifecycle-actor-evidence-correction"

#: SHA-256 of the XASSET-0042 gate narrative as it stood BEFORE this filing, with the folded
#: scalar's own trailing newline stripped. This filing only APPENDS to that description, so the
#: prior narrative must survive as an exact prefix; a rewrite of any earlier sentence fails here.
PRIOR_GATE_NARRATIVE_SHA256 = (
    "1ae9b598007ddead1a91f4d0b8deb3a588fe26978e28bd7231530c66cf581c8a"
)


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


def _paths_changed_between(before: str, after: str, relpaths) -> list[str]:
    """Which of ``relpaths`` differ between two commits, read only from the object store.

    Deliberately compares COMMITS, not the working tree: a protected file edited *and committed*
    is invisible to a ``HEAD``-versus-worktree comparison, which is the defect review 4976985695
    MINOR 1 identified. Skips rather than silently passing when a commit is unavailable.
    """
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


def _blob_at_pr_merge(relpath: str) -> bytes:
    """The bytes of ``relpath`` AT PR #343's OWN MERGE, from the git object store.

    ADDED BY XASSET-0044's re-anchoring. Every guard below asks what PR #343 left behind, which
    was the same as the working tree only while PR #343 was the most recent unit to touch these
    files. Reading the closed anchor is immutable and cannot be satisfied by editing anything now.
    """
    out = subprocess.run(
        ["git", "cat-file", "blob", f"{PR_MERGE_SHA}:{relpath}"],
        cwd=ROOT, capture_output=True, check=False,
    )
    if out.returncode != 0:
        pytest.skip(f"{relpath} is unavailable at {PR_MERGE_SHA} in this checkout")
    return out.stdout


def _flat(text: str) -> str:
    """Collapse markdown line wrapping and blockquote markers.

    A phrase assertion should test content, not typography: neither where a line happens to
    wrap nor whether the sentence sits inside a ``>`` quote may change whether it matches.
    """
    unquoted = re.sub(r"(?m)^\s*>\s?", "", text)
    return re.sub(r"\s+", " ", unquoted)


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_body(decision_text: str) -> str:
    """The decision without front matter, so front matter cannot satisfy a body assertion."""
    parts = decision_text.split("---\n", 2)
    assert len(parts) == 3, "decision must carry exactly one YAML front-matter block"
    return parts[2]


@pytest.fixture(scope="module")
def flat_body(decision_body: str) -> str:
    return _flat(decision_body)


@pytest.fixture(scope="module")
def sections(decision_body: str) -> dict[str, str]:
    """Map ``A``..``N`` to that section's own text, so an assertion cannot be satisfied elsewhere."""
    found: dict[str, str] = {}
    pattern = re.compile(r"^### ([A-N])\. ", re.MULTILINE)
    marks = list(pattern.finditer(decision_body))
    assert marks, "no lettered sections found"
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(decision_body)
        found[mark.group(1)] = decision_body[mark.start():end]
    return found


@pytest.fixture(scope="module")
def flat_sections(sections: dict[str, str]) -> dict[str, str]:
    return {letter: _flat(text) for letter, text in sections.items()}


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
# 1 -- The filing is governance-only and performs no part of the rebinding
# ======================================================================================


class TestFilingIsGovernanceOnly:
    def test_determination_is_the_authorization_not_the_rebinding(self, flat_sections):
        assert "`POST_CORRECTION_REBINDING_AUTHORIZED`" in flat_sections["A"]
        assert "This filing performs no part of that rebinding." in flat_sections["A"]

    def test_section_a_enumerates_what_it_does_not_do(self, flat_sections):
        text = flat_sections["A"]
        for phrase in (
            "edits no load-bearing byte",
            "rebinds nothing",
            "amends no canonical artifact",
            "runs no readiness verification and no drift check",
            "retries no part of step 11",
            "generates no attestation",
            "creates no result",
        ):
            assert phrase in text, f"§A must state: {phrase}"

    def test_it_authorizes_and_defines_rather_than_binding(self, flat_sections):
        assert "It authorizes and defines; a later unit binds." in flat_sections["A"]

    def test_the_nearest_overreach_is_refused(self, flat_body):
        """The overreach: a filing that both authorizes and performs, in one motion."""
        assert (
            "A filing that authorized and performed the rebinding in one motion would be "
            "exercising authority it created for itself in the same document"
        ) in flat_body

    def test_the_authorizing_module_is_byte_identical_to_head(self):
        at_merge = hashlib.sha256(_blob_at_pr_merge(AUTH_MODULE_RELPATH)).hexdigest()
        assert at_merge == CURRENT_MODULE_SHA256
        blob = _git("rev-parse", f"{PR_MERGE_SHA}:{AUTH_MODULE_RELPATH}").strip()
        assert blob == CURRENT_MODULE_BLOB


# ======================================================================================
# 2 -- The drift reproduction is read-only and is not the step-9 or step-10 unit
# ======================================================================================


class TestDriftReproducedReadOnlyOnly:
    def test_exactly_one_load_bearing_path_drifts_from_the_bound_tree(self):
        """Recomputed here from the git object store, never taken from the decision's prose."""
        drifted: list[str] = []
        for relative in LOAD_BEARING_RELPATHS_AT_FILING:
            out = subprocess.run(
                ["git", "cat-file", "blob", f"{BOUND_MERGE_SHA}:{relative}"],
                cwd=ROOT, capture_output=True, check=False,
            )
            if out.returncode != 0:
                pytest.skip("the bound merge is unavailable in this checkout")
            bound = hashlib.sha256(out.stdout).hexdigest()
            at_merge = hashlib.sha256(_blob_at_pr_merge(relative)).hexdigest()
            if bound != at_merge:
                drifted.append(relative)
        assert drifted == [AUTH_MODULE_RELPATH], (
            f"expected exactly one drifted load-bearing path, found {drifted!r}"
        )

    def test_the_bound_module_identity_is_the_one_the_decision_states(self):
        out = subprocess.run(
            ["git", "cat-file", "blob", f"{BOUND_MERGE_SHA}:{AUTH_MODULE_RELPATH}"],
            cwd=ROOT, capture_output=True, check=False,
        )
        if out.returncode != 0:
            pytest.skip("the bound merge is unavailable in this checkout")
        assert hashlib.sha256(out.stdout).hexdigest() == BOUND_MODULE_SHA256

    def test_section_b_records_the_reproduction_as_git_object_level_only(self, flat_sections):
        text = flat_sections["B"]
        assert "at the git-object level only" in text
        assert "`write_authorization` was never called" in text

    def test_section_b_disclaims_the_step_9_and_step_10_units(self, flat_sections):
        """The nearest overreach: a read-only comparison rebranded as the authorized checks."""
        text = flat_sections["B"]
        assert (
            "no part of the authorized step-9 readiness verification or step-10 drift check was "
            "performed"
        ) in text
        assert "this filing does not claim their authority" in text

    def test_section_b_records_no_lane_was_touched(self, flat_sections):
        text = flat_sections["B"]
        assert "No lane was created, inspected, or touched" in text
        assert "`AUTHORIZATION_ROOT` was not created" in text

    def test_the_drift_is_framed_as_the_mechanism_working(self, flat_sections):
        assert (
            "An obsolete authorization that cannot authorize a corrected module is the mechanism "
            "working."
        ) in flat_sections["B"]


# ======================================================================================
# 3 -- Step 8 is not re-consumed, and XASSET-0037 is not invalidated
# ======================================================================================


class TestStep8NotReconsumed:
    def test_step_8_is_recorded_as_spent_by_xasset_0037(self, flat_sections):
        text = flat_sections["C"]
        assert (
            "`XASSET-0037` performed that one, and this decision does not reopen, re-consume, or "
            "re-issue it."
        ) in text
        assert "Step 8's own single rebinding remains spent" in text

    def test_the_separate_authority_is_named_and_is_not_step_8(self, flat_sections):
        text = flat_sections["C"]
        assert "or reconciliation lifecycle" in text
        assert "step-8 **equivalent**" in text
        assert "*Equivalent*, not *identical*" in text
        assert "not a second draw on step 8's own budget" in text

    def test_predecessor_authorizations_are_preserved_not_invalidated(self, flat_sections):
        text = flat_sections["C"]
        assert "`XASSET-0037` is preserved, not invalidated" in text
        assert "remains valid accepted history" in text

    def test_what_changes_is_only_which_tree_identity_is_proven_against(self, flat_sections):
        assert (
            "which merged tree the mechanism proves load-bearing identity against"
        ) in flat_sections["C"]

    def test_the_nearest_overreach_is_refused_in_alternatives(self, flat_body):
        """The overreach: inheriting step 8's authority wholesale by calling this 'step 8'."""
        assert (
            "**Treat this as a second draw on `XASSET-0030` §G.B step 8.** Rejected as inaccurate."
        ) in flat_body
        assert "would either double-count a spent budget" in flat_body

    def test_amending_xasset_0037_in_place_was_considered_and_rejected(self, flat_body):
        assert "**Amend `XASSET-0037` in place to cover the corrected bytes.** Rejected." in flat_body


# ======================================================================================
# 4 -- Exactly one future unit; downstream links stay unauthorized
# ======================================================================================


class TestExactlyOneFutureRebindingAuthorized:
    def test_section_a_grants_exactly_one_unit(self, flat_sections):
        assert "**Exactly one** future, separate, bounded successor" in flat_sections["A"]

    def test_section_f_grants_exactly_one_pull_request(self, flat_sections):
        text = flat_sections["F"]
        assert "**exactly one** future, separate, bounded pull request may" in text
        assert "**One unit, one pull request.**" in text

    def test_the_future_identifier_is_verified_live_never_predicted_here(self, flat_sections):
        assert (
            "verified unused against live repository state at the time it is filed"
        ) in flat_sections["F"]
        assert "never predicted or reserved here" in flat_sections["F"]

    def test_repackaging_requires_a_stop_and_disclose(self, flat_sections):
        """The overreach: silently splitting or merging units to suit convenience."""
        assert (
            "must **stop and disclose**, not decide it silently"
        ) in flat_sections["F"]

    def test_the_decision_does_not_name_a_reserved_successor_identifier(self, decision_body):
        """No XASSET-0044+ identifier may be reserved, named, or implied by this filing."""
        for forbidden in ("XASSET-0044", "XASSET-0045", "XASSET-0046"):
            assert forbidden not in decision_body, (
                f"{forbidden} must not be reserved or named by this filing"
            )


class TestDownstreamLinksNotAuthorized:
    def test_section_a_withholds_links_3_4_and_5(self, flat_sections):
        assert (
            "**Links 3, 4, and 5 are not authorized, here or by implication (§K).**"
        ) in flat_sections["A"]

    def test_section_k_withholds_steps_9_10_and_11_by_name(self, flat_sections):
        text = flat_sections["K"]
        assert "`XASSET-0030` §G.B steps 9, 10, or 11, in whole or in part" in text
        assert "any renewed readiness verification or renewed post-rebinding drift check" in text

    def test_completing_the_rebinding_authorizes_nothing_further(self, flat_sections):
        assert (
            "Completing it authorizes the next link no more than a clean step-10 result "
            "authorized step 11"
        ) in flat_sections["G"]

    def test_xasset_0040_is_not_revived(self, flat_sections):
        assert (
            "reviving `XASSET-0040`, which remains spent as `STOPPED_BEFORE_ATTESTATION`"
        ) in flat_sections["K"]

    def test_authorizing_a_further_successor_is_withheld(self, flat_sections):
        assert (
            "authorizing any successor beyond the **one** future rebinding unit defined in §F"
        ) in flat_sections["K"]

    def test_pre_authorizing_the_whole_chain_was_considered_and_rejected(self, flat_body):
        assert (
            "**Authorize links 2 through 5 together, since the chain is known.** Rejected"
        ) in flat_body
        assert "One link, one authorization, one lifecycle." in flat_body


# ======================================================================================
# 5 -- The ten required properties are present, specific, and conjunctive
# ======================================================================================


class TestTenRequiredProperties:
    @pytest.mark.parametrize("index", list(range(1, 11)))
    def test_each_property_is_present_and_substantive(self, sections, index):
        text = sections["G"]
        marker = f"**G.{index} —"
        assert marker in text, f"§G.{index} is missing"
        start = text.index(marker)
        nxt = text.find(f"**G.{index + 1} —", start)
        body = text[start: nxt if nxt != -1 else len(text)]
        assert len(body.strip()) > 250, f"§G.{index} is vacuous"

    def test_properties_are_conditions_not_advice(self, flat_sections):
        text = flat_sections["G"]
        assert "Each is a condition on the authorized unit." in text
        assert "none may be waived by the unit that performs it" in text

    def test_g1_binds_reviewed_stabilized_exact_bytes(self, flat_sections):
        text = flat_sections["G"]
        assert "never a value asserted in prose" in text
        assert "never a working-tree value that no independent review saw" in text

    def test_g2_preserves_every_path_and_forbids_weakening(self, flat_sections):
        text = flat_sections["G"]
        assert (
            "Every one of the ten paths in §B is retained, with its existing identity and its "
            "existing comparison"
        ) in text
        assert "No path is removed, exempted, made conditional, or excluded" in text
        assert (
            "may be deleted, `skip`ped, `xfail`ed, narrowed to a subset of paths, or rewritten to "
            "assert less than it asserts today"
        ) in text

    def test_g2_retains_the_pin_succession_refusal(self, flat_sections):
        assert (
            "a successor pin equal to **any** predecessor generation's accepted pin is refused — "
            "is retained and may be strengthened, never relaxed"
        ) in flat_sections["G"]

    def test_g3_preserves_the_correction_and_argues_any_exception(self, flat_sections):
        text = flat_sections["G"]
        for element in (
            "both actor-error messages, byte-unchanged",
            "`PRINCIPAL_ACCOUNT_LOGIN` and `LIFECYCLE_OPERATOR_LOGIN`",
            "the four canonical-JSON record fingerprints",
            "the absence of any general standing for `claude[bot]`",
        ):
            assert element in text, f"§G.3 must preserve: {element}"
        assert "**argued as strictly necessary, not assumed**" in text

    def test_g4_preserves_the_outcome_producing_surface_and_universe(self, flat_sections):
        text = flat_sections["G"]
        assert DERIVATION_SUCCESSOR_SHA256[:8] in text
        assert "17-region" in text
        assert UNIVERSE_HASH in text
        assert "unchanged at **680** / **48**" in text

    def test_g4_keeps_the_two_outcome_producing_modules_whole_file_identical(self, flat_sections):
        """The runner and result validator get NO transition -- that freeze is not loosened."""
        text = flat_sections["G"]
        assert (
            "`level1_stage1_runner.py` and `level1_stage1_result_validator.py` stay "
            "**byte-identical** across every anchor the mechanism already compares — no transition, "
            "no exception."
        ) in text

    def test_g4_no_longer_freezes_the_derivation_module_whole_file(self, flat_sections):
        """CORRECTED after review 4976985695 MAJOR 2.

        Whole-file freezing that module and permitting §J's canonical amendment were not jointly
        satisfiable. The stale requirement must be gone, not merely contradicted elsewhere.
        """
        text = flat_sections["G"]
        assert "stays at the accepted successor blob" not in text
        assert "transition manifest remains\nsatisfied and unweakened" not in text
        assert "remains satisfied and unweakened" not in text

    def test_g5_requires_exact_identities_and_fail_closed(self, flat_sections):
        text = flat_sections["G"]
        assert "exactly two parents **in order**, base then accepted head" in text
        assert "byte-identical to its accepted head's tree" in text
        assert "the merged tree never becomes its own source of truth" in text
        assert "**fails closed** rather than being treated as agreement" in text

    def test_g6_recomputes_identities_only_once_after_stabilization(self, flat_sections):
        text = flat_sections["G"]
        assert "computed **once**, after every permitted canonical" in text
        assert "never carried forward from a superseded head" in text
        assert "repeating it is a foreseeable defect, not an accident" in text

    def test_g9_authorizes_nothing_downstream(self, flat_sections):
        assert (
            "performs and authorizes no readiness verification, no drift verification, no part of "
            "step 11, no attestation, no arming, no claim, no execution, no recovery, and no "
            "results work"
        ) in flat_sections["G"]

    def test_g10_requires_its_own_complete_lifecycle(self, flat_sections):
        text = flat_sections["G"]
        assert "Independent **FULL** exact-head review under `OPS-0007` §1" in text
        assert "successful merge-commit CI whose `head_sha` is the exact merge SHA" in text
        assert "**None is individually sufficient.**" in text


# ======================================================================================
# 5a -- §G.4a: the derivation surface moves by an appended exact closed transition only
# ======================================================================================


class TestDerivationSurfaceTransitionIsAppendedNotLoosened:
    """Review 4976985695 MAJOR 2.

    §G.4 froze ``level1_endpoint_evidence_preregistration_validator.py`` whole-file while §J
    permitted -- and §F.2 requires -- advancing canonical successor-lifecycle language that the
    frozen module validates against hard-coded ``XASSET-0037`` expectations. The two were not
    jointly satisfiable. §G.4a resolves it by APPENDING a second exact closed transition, and these
    guard both halves: that the mechanism is real, and that it is not a loosening.
    """

    DERIVATION_RELPATH = "level1_endpoint_evidence_preregistration_validator.py"

    def test_the_contradiction_is_real_and_still_reproducible(self):
        """Derived live from the real public validation surface, never taken from the record.

        Parsed from source with ``ast`` -- the module is not imported, so nothing it defines is
        executed here. If a future change made the successor-lifecycle expectations non-literal,
        this fails rather than silently vouching for a premise that no longer holds.
        """
        # RE-ANCHORED BY XASSET-0044. The contradiction §G.4a records was real AT PR #343's
        # MERGE, which is when it was reproduced and when it justified authorizing the appended
        # transition. XASSET-0044 has since RESOLVED it by performing that authorized amendment,
        # so reading the live file would now (correctly) show XASSET-0044 in these fields and
        # would turn a true historical premise into a false present-tense one.
        source = _blob_at_pr_merge(self.DERIVATION_RELPATH).decode("utf-8")
        tree = ast.parse(source)
        frozen: dict[str, str] = {}
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    frozen[target.id] = node.value.value
        assert frozen.get("STAGE_1_AUTHORIZATION_REBOUND_BY") == "XASSET-0037"
        assert frozen.get("STAGE_1_EFFECTIVE_STRUCTURAL_AUTHORIZATION_SOURCE") == "XASSET-0037"
        # ... and the authorized resolution really was applied, so this premise is not merely
        # preserved as folklore. The live module must NO LONGER carry the frozen XASSET-0037
        # expectations, which is exactly what §G.4a's appended transition was authorized to change.
        live = ast.parse((ROOT / self.DERIVATION_RELPATH).read_text(encoding="utf-8"))
        live_frozen: dict[str, str] = {}
        for node in ast.walk(live):
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if isinstance(target, ast.Name) and isinstance(node.value, ast.Constant):
                    if isinstance(node.value.value, str):
                        live_frozen[target.id] = node.value.value
        assert live_frozen.get("STAGE_1_AUTHORIZATION_REBOUND_BY") != "XASSET-0037"
        assert (
            live_frozen.get("STAGE_1_EFFECTIVE_STRUCTURAL_AUTHORIZATION_SOURCE") != "XASSET-0037"
        )

    def test_g4a_exists_and_is_substantive(self, sections):
        text = sections["G"]
        assert "**G.4a —" in text
        start = text.index("**G.4a —")
        end = text.find("**G.5 —", start)
        body = text[start: end if end != -1 else len(text)]
        assert len(body.strip()) > 1200, "§G.4a is too thin to constrain anything"

    def test_g4a_preserves_the_accepted_blob_and_the_first_transition(self, flat_sections):
        text = flat_sections["G"]
        assert DERIVATION_SUCCESSOR_SHA256 in text, "the accepted blob must be named in full"
        assert "is preserved as a historical anchor" in text
        assert (
            "existing exact closed 17-region package-to-successor transition manifest is preserved "
            "as accepted history"
        ) in text
        assert "Neither is deleted, edited, re-derived, or weakened" in text

    def test_g4a_appends_rather_than_replaces(self, flat_sections):
        text = flat_sections["G"]
        assert "**A new, second exact closed transition is appended**" in text
        assert "package → successor → rebound" in text
        assert "**never replaces or subsumes** the first" in text

    def test_g4a_requires_stabilization_first(self, flat_sections):
        assert "only after the future bytes have stabilized (§G.6)" in flat_sections["G"]

    def test_g4a_enumerates_and_authenticates_every_region(self, flat_sections):
        text = flat_sections["G"]
        assert "**Every permitted changed region is enumerated and authenticated**" in text
        assert "exact source and target byte offsets, exact lengths, and the SHA-256" in text

    def test_g4a_requires_every_byte_outside_a_region_identical(self, flat_sections):
        text = flat_sections["G"]
        assert "**Every byte outside a declared region must be byte-identical**" in text
        assert "no gap, overlap, duplicate, reordering, resizing, addition, or removal is" in text
        assert "fails closed just as a change outside one does" in text

    def test_g4a_confines_regions_to_the_authorization_only_surface(self, flat_sections):
        text = flat_sections["G"]
        assert "**Every declared region must lie inside the authorization-only surface**" in text
        assert (
            "successor-lifecycle constants, canonical validation of those constants, pin "
            "succession, and rebinding-block validation"
        ) in text
        assert "A region touching anything else is a stop (§L), not a widening." in text

    def test_g4a_requires_reproving_the_consumer_reachable_surface(self, flat_sections):
        text = flat_sections["G"]
        assert (
            "**The consumer-reachable and outcome-producing definitions must be re-proved "
            "unchanged**"
        ) in text
        assert "**semantically and byte-identically**" in text
        assert "derived from the consumers' own source" in text

    def test_g4a_forbids_any_behavioural_change(self, flat_sections):
        text = flat_sections["G"]
        assert (
            "**No runner, result-validator, universe, construction, gate, disposition, scoring, "
            "portfolio, or protected-`RISK` behaviour may change**"
        ) in text
        assert "for nothing else" in text

    def test_g4a_keeps_the_authorization_boundary_at_bytes(self, flat_sections):
        text = flat_sections["G"]
        assert "**The authorization boundary remains bytes.**" in text
        assert "no version-dependent diff algorithm participates in the authorization" in text
        assert "loosens nothing about how the link is proved" in text

    def test_section_j_no_longer_contradicts_g4(self, flat_sections):
        """The stale absolute is the contradiction itself; it must be gone, not merely qualified."""
        text = flat_sections["J"]
        assert "Everything §G.4 enumerates is **unchanged**" not in text
        assert "Every substantive thing §G.4 enumerates is **unchanged**" in text

    def test_section_j_requires_lockstep_and_names_g4a_as_the_only_mechanism(self, flat_sections):
        text = flat_sections["J"]
        assert "**The enforcement side must move in lockstep, and §G.4a is what permits it.**" in text
        assert "frozen expectations that currently name `XASSET-0037`" in text
        assert "The two move together or not at all" in text
        assert (
            "§G.4a's appended exact closed transition is the **only** mechanism by which the "
            "enforcement side may move"
        ) in text
        assert "Anything beyond that surface is out of scope for both §J and §G.4a." in text

    def test_this_correction_unit_did_not_edit_the_derivation_module(self):
        """§G.4a authorizes a FUTURE transition; this unit changes no production byte."""
        changed = _paths_changed_between(PR_BASE_SHA, PR_MERGE_SHA, (self.DERIVATION_RELPATH,))
        assert changed == [], f"{self.DERIVATION_RELPATH} must be untouched by this PR"
        actual = hashlib.sha256(_blob_at_pr_merge(self.DERIVATION_RELPATH)).hexdigest()
        assert actual == DERIVATION_SUCCESSOR_SHA256

    def test_this_correction_unit_did_not_edit_either_canonical_artifact(self):
        changed = _paths_changed_between(PR_BASE_SHA, PR_MERGE_SHA, (
            "research/level1_endpoint_evidence/PROTOCOL_V1.md",
            "research/level1_endpoint_evidence/pre_registration.yaml",
        ))
        assert changed == []


# ======================================================================================
# 6 -- The trust boundary grows; nothing is removed
# ======================================================================================


class TestLoadBearingPreservationAndGrowth:
    def test_the_module_still_declares_exactly_the_ten_paths(self):
        """Parsed from source with ``ast``; the module is never imported or executed here.

        Two members are module-scope name references rather than string literals, so the
        tuple is resolved against the module's own constant assignments. A member that
        resolves to nothing fails here rather than being silently dropped.
        """
        tree = ast.parse(_blob_at_pr_merge(AUTH_MODULE_RELPATH).decode("utf-8"))
        constants: dict[str, str] = {}
        tuple_node: ast.AST | None = None
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                if target.id == "LOAD_BEARING_RELPATHS":
                    tuple_node = node.value
                elif isinstance(node.value, ast.Constant) and isinstance(
                    node.value.value, str
                ):
                    constants[target.id] = node.value.value
        assert isinstance(tuple_node, ast.Tuple), "LOAD_BEARING_RELPATHS is not a tuple literal"
        resolved: list[str] = []
        for element in tuple_node.elts:
            if isinstance(element, ast.Constant) and isinstance(element.value, str):
                resolved.append(element.value)
            elif isinstance(element, ast.Name):
                assert element.id in constants, f"unresolvable member {element.id!r}"
                resolved.append(constants[element.id])
            else:
                pytest.fail(f"unexpected LOAD_BEARING_RELPATHS member: {ast.dump(element)}")
        assert tuple(resolved) == LOAD_BEARING_RELPATHS_AT_FILING
        assert len(resolved) == 10

    def test_authorizing_constants_are_unchanged_by_this_filing(self):
        tree = ast.parse(_blob_at_pr_merge(AUTH_MODULE_RELPATH).decode("utf-8"))
        values: dict[str, object] = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in {
                        "AUTHORIZING_DECISION", "AUTHORIZING_PULL_REQUEST",
                    }:
                        values[target.id] = ast.literal_eval(node.value)
        assert values["AUTHORIZING_DECISION"] == "XASSET-0037"
        assert values["AUTHORIZING_PULL_REQUEST"] == 337

    def test_section_h_grows_the_boundary_to_fourteen(self, flat_sections):
        """CORRECTED after review 4976985695 MAJOR 1: 10 -> 11 bound only the future decision."""
        text = flat_sections["H"]
        assert "`LOAD_BEARING_RELPATHS` **10 → 14**" in text
        assert "using the **existing exact-byte mechanism unchanged**" in text
        assert "The four additions are the `XASSET-0041`, `XASSET-0042`, and `XASSET-0043`" in text

    def test_section_h_no_longer_claims_a_single_addition(self, flat_sections):
        """The nearest regression: quietly reverting to binding only the future decision."""
        text = flat_sections["H"]
        assert "The single addition is the new rebinding decision file itself" not in text
        assert "**10 → 11**" not in text

    def test_section_h_states_why_the_chain_is_four_files_long(self, flat_sections):
        text = flat_sections["H"]
        assert "the corrected bytes were made lawful by four decisions, not by the rebinding alone" in text
        assert "binding fewer would leave the rest editable after attestation" in text

    def test_section_h_marks_the_count_nominal_but_the_guarantee_fixed(self, flat_sections):
        """A proved equivalent may change the number; it may never change the guarantee."""
        text = flat_sections["H"]
        assert "The count **14** is nominal" in text
        assert "What may not change is the guarantee" in text
        assert (
            "every file in the authority chain for the corrected bytes is inside the attested "
            "identity"
        ) in text

    @pytest.mark.parametrize("relpath", FUTURE_BOUNDARY_ADDITIONS)
    def test_each_named_future_addition_exists_and_is_bound_by_g8(self, relpath, flat_sections):
        """The requirement must name real files, not remembered ones."""
        assert (ROOT / relpath).exists(), f"{relpath} does not exist"
        assert relpath in flat_sections["G"], f"§G.8 must bind {relpath}"

    def test_g8_binds_all_four_including_the_future_decision(self, flat_sections):
        text = flat_sections["G"]
        assert "reaches **four** files here, not one" in text
        assert (
            "the future rebinding decision, under its own independently verified unused identifier"
        ) in text

    def test_g8_requires_direct_membership_and_refuses_citation_as_binding(self, flat_sections):
        """The overreach the reviewer named explicitly: relabelling a citation as a binding."""
        text = flat_sections["G"]
        assert "**Direct membership, not an equivalent.**" in text
        assert (
            "a future decision that merely *describes* or *cites* predecessor text does not "
            "byte-bind it"
        ) in text
        assert "is **not** a binding of those files" in text

    def test_g8_requires_any_claimed_equivalence_to_be_proved(self, flat_sections):
        text = flat_sections["G"]
        assert "it must **prove** the equivalence" in text
        assert "never assume it" in text

    def test_section_f_requires_four_additions(self, flat_sections):
        text = flat_sections["F"]
        assert "add **four** decision files to `LOAD_BEARING_RELPATHS`" in text
        assert "taking the boundary from **10 to 14**" in text

    def test_g2_states_growth_is_additive_not_a_trade(self, flat_sections):
        text = flat_sections["G"]
        assert "while §G.8 adds four (10 → 14)" in text
        assert "Growth is additive; nothing is displaced or traded away." in text

    def test_section_h_removes_nothing_and_weakens_nothing(self, flat_sections):
        assert (
            "**No load-bearing path is removed and no exact-byte check is weakened.**"
        ) in flat_sections["H"]

    def test_g8_keeps_historical_authority_inside_the_boundary(self, flat_sections):
        text = flat_sections["G"]
        assert (
            "The `XASSET-0029`, `XASSET-0036`, and `XASSET-0037` decision files are **retained**"
        ) in text
        assert "historical authority is preserved, never displaced" in text

    def test_leaving_the_new_decision_outside_the_boundary_was_rejected(self, flat_body):
        """The overreach: binding corrected bytes while the governing text stays editable."""
        assert (
            "**Bind the corrected module without adding the new decision file to the trust "
            "boundary.** Rejected"
        ) in flat_body


# ======================================================================================
# 7 -- The XASSET-0042 current-identity evidence must be explicitly resolved
# ======================================================================================


class TestXasset0042EvidenceMustBeResolved:
    GUARD_SUITE = ROOT / "test_level1_stage1_pr337_lifecycle_actor_evidence_correction.py"
    GUARD_CLASS = "TestDeclaredCorrectedIdentityMatchesTheModule"

    def test_the_guard_referenced_by_the_decision_actually_exists(self):
        """The requirement must point at a real guard, not a remembered one."""
        assert self.GUARD_SUITE.exists()
        source = self.GUARD_SUITE.read_text(encoding="utf-8")
        assert f"class {self.GUARD_CLASS}" in source
        assert "FINAL_CORRECTED_MODULE_SHA256:" in source

    def test_the_guard_currently_matches_the_real_module_bytes(self):
        """Independently recomputed here, so §I rests on live truth rather than the record."""
        decision = _blob_at_pr_merge(
            "governance/decisions/"
            "XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md"
        ).decode("utf-8")
        declared = [
            ln for ln in decision.split("\n")
            if ln.strip().startswith("FINAL_CORRECTED_MODULE_SHA256:")
        ]
        assert len(declared) == 1
        assert CURRENT_MODULE_SHA256 in declared[0]
        actual = hashlib.sha256(_blob_at_pr_merge(AUTH_MODULE_RELPATH)).hexdigest()
        assert actual == CURRENT_MODULE_SHA256

    def test_section_i_quotes_the_reviewer_handoff(self, flat_sections):
        assert (
            "must explicitly amend/retire the current-identity evidence when it lawfully changes "
            "the module, rather than silently invalidating `XASSET-0042`'s declaration"
        ) in flat_sections["I"]

    def test_i1_requires_exactly_one_true_declaration_checked_against_bytes(self, flat_sections):
        text = flat_sections["I"]
        assert "exactly one true current declaration" in text
        assert "machine-checked against the production module's real bytes" in text
        assert "a declaration matched against a stated constant rather than the file" in text

    def test_i2_permits_either_resolution_but_requires_the_choice_be_argued(self, flat_sections):
        text = flat_sections["I"]
        assert "**amend**" in text and "**retire**" in text
        assert "Silence, or a choice made without stating why, is not acceptable." in text

    def test_i3_retains_every_prior_identity_distinctly(self, flat_sections):
        text = flat_sections["I"]
        for digest in (BOUND_MODULE_SHA256[:8], INTERMEDIATE_MODULE_SHA256[:8],
                       CURRENT_MODULE_SHA256[:8]):
            assert digest in text, f"§I.3 must retain identity {digest}"
        assert "all kept mutually distinct" in text

    def test_i3_forbids_reading_0042s_no_repin_statement_as_a_global_claim(self, flat_sections):
        assert (
            "may not be read as a claim about the repository's state after a later, separately "
            "authorized rebinding"
        ) in flat_sections["I"]

    def test_i4_names_the_three_coupled_assertions_and_forbids_weakening(self, flat_sections):
        text = flat_sections["I"]
        assert "Three of its nine assertions are module-digest-coupled" in text
        assert "compares against a **moving** `HEAD`" in text
        assert (
            "Deleting, `skip`ping, `xfail`ing, or relaxing any of them is prohibited"
        ) in text
        assert "no replacement may assert less than the assertion it replaces" in text

    def test_the_guard_has_exactly_the_nine_assertions_section_i_counts(self):
        """§I says 'nine assertions'; that count is verified, not asserted."""
        def _guard_test_names(source: str) -> list[str]:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == self.GUARD_CLASS:
                    return [
                        n.name for n in node.body
                        if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
                    ]
            pytest.fail(f"{self.GUARD_CLASS} not found")
            raise AssertionError  # pragma: no cover - unreachable

        # RE-ANCHORED BY XASSET-0044: nine is what §I counted AT PR #343's MERGE, and that is
        # where it is verified. XASSET-0044's authorized re-anchoring (§I.4) ADDED guard tests to
        # this class; SS-I.4 forbids deleting, skipping, xfailing or relaxing any, so the live
        # class is required to be a strict SUPERSET, never smaller.
        at_merge = _guard_test_names(
            _blob_at_pr_merge(str(self.GUARD_SUITE.relative_to(ROOT))).decode("utf-8")
        )
        assert len(at_merge) == 9, f"expected nine guard tests, found {len(at_merge)}"
        live = _guard_test_names(self.GUARD_SUITE.read_text(encoding="utf-8"))
        assert set(at_merge) <= set(live), (
            "a guard test present at PR #343's merge has been removed or renamed; SS-I.4 permits "
            "re-anchoring but never deletion"
        )
        assert len(live) >= 9

    def test_deferring_the_guard_to_implementation_was_rejected(self, flat_body):
        assert (
            "**Let the `XASSET-0042` guard fail and repair it during implementation.** Rejected."
        ) in flat_body


# ======================================================================================
# 8 -- Canonical amendment is authorization language only
# ======================================================================================


class TestCanonicalAmendmentIsAuthorizationLanguageOnly:
    def test_section_j_confines_the_amendment(self, flat_sections):
        text = flat_sections["J"]
        assert "**in lockstep**" in text
        assert "**only** in successor-lifecycle authorization language" in text

    def test_historical_truth_is_not_rewritten(self, flat_sections):
        text = flat_sections["J"]
        assert "`established_by: XASSET-0029` stays" in text
        assert "retained in an explicitly predecessor-named field" in text

    def test_the_universe_must_be_regenerated_and_unchanged(self, flat_sections):
        text = flat_sections["J"]
        assert "independently regenerated after the amendment" in text
        assert "unchanged at 680 / 48" in text
        assert "`stage_1_executability.executable` stays `false`" in text

    def test_a_gratuitous_amendment_is_refused(self, flat_sections):
        """The overreach: amending the canonical files merely to look thorough."""
        assert (
            "If no authorization-language change is actually required, none may be made merely to "
            "have amended something."
        ) in flat_sections["J"]

    def test_the_canonical_files_are_unchanged_by_this_filing(self):
        for relative, expected in (
            ("research/level1_endpoint_evidence/PROTOCOL_V1.md",
             "367583b616e1c6ab614bcf67d451fe27ce40507d073374190c57291e761d8971"),
            ("research/level1_endpoint_evidence/pre_registration.yaml",
             "768b013c0129f02577fea3c2a1a3100b4340b9a42f48ee0d0dbd6e671894bce1"),
        ):
            actual = hashlib.sha256(_blob_at_pr_merge(relative)).hexdigest()
            assert actual == expected, f"{relative} changed; this filing must not touch it"


# ======================================================================================
# 9 -- Not an activation; ATTEMPT_1 intact; §P.1 reserved
# ======================================================================================


class TestNotAnActivationAndAttemptIntact:
    def test_section_d_places_a_rebinding_outside_the_terminated_step(self, flat_sections):
        text = flat_sections["D"]
        assert "terminates the activation regress on a step that **changes no repository state**" in text
        assert "categorically outside the step §E terminates" in text

    def test_zero_activation_authorizations_are_added(self, flat_sections):
        text = flat_sections["D"]
        assert "adds one authorized rebinding and ZERO activation authorizations." in text
        assert "`stage_1_executability.executable` stays `false` permanently" in text
        assert "**No committed value in this repository authorizes Stage-1 execution**" in text

    def test_final_activation_remains_external_and_operator_driven(self, flat_sections):
        assert (
            "never another merged pull request"
        ) in flat_sections["D"]

    def test_attempt_1_is_not_reached_or_consumed(self, flat_sections):
        assert "consuming any part of `ATTEMPT_1`" in flat_sections["K"]

    def test_merging_changes_nothing_operational(self, flat_sections):
        text = flat_sections["N"]
        assert "does not arm Stage 1, does not rebind anything" in text
        assert "still returns `False`" in text
        assert "`AUTHORIZING_DECISION` is still `XASSET-0037`" in text
        assert "the enforcement drift in §B is still there" in text

    def test_lane_state_is_absent_on_disk(self):
        """No lane path is created by this filing; verified without importing the module."""
        assert not Path("/var/tmp/phq-endpoint0001-stage1-authorization").exists()
        assert not (ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()


class TestP1ResultsPRRemainsSeparate:
    def test_p1_is_not_consumed_or_counted_against(self, flat_sections):
        text = flat_sections["E"]
        assert "**not consumed, replaced, amended, or counted against**" in text
        assert "**one, unspent.**" in text

    def test_the_three_grounds_are_stated(self, flat_sections):
        text = flat_sections["E"]
        assert "may make no production configuration change" in text
        assert "§P.1's deliverable is a results document" in text
        assert "sit before it" in text

    def test_section_k_withholds_consuming_p1(self, flat_sections):
        assert "consuming `XASSET-0027` §P.1's reserved results PR" in flat_sections["K"]


# ======================================================================================
# 10 -- Fail-closed, effectivity, and protected bytes
# ======================================================================================


class TestFailClosed:
    def test_conditions_are_conjunctive_and_a_failure_stops_the_unit(self, flat_sections):
        text = flat_sections["L"]
        assert "Every condition in §G is conjunctive." in text
        assert "it **stops and discloses**" in text

    def test_no_partial_result_and_no_out_of_scope_repair(self, flat_sections):
        text = flat_sections["L"]
        assert (
            "It does not proceed on a partial result, exclude the failing item, or repair a defect "
            "outside its own authorized scope"
        ) in text

    def test_an_unobtainable_anchor_is_never_agreement(self, flat_sections):
        text = flat_sections["L"]
        assert "An unobtainable anchor is never treated as agreement." in text
        assert "is a stop, not a widening" in text


class TestEffectivityRequiresCompleteLifecycleClosure:
    @pytest.mark.parametrize("condition", [
        "independent **FULL** exact-head review under `OPS-0007` §1",
        "any required bounded correction and exact-head re-review",
        "explicit principal exact-head acceptance at that final head",
        "normal merge",
        "immediate post-merge verification",
        "**successful merge-commit CI whose `head_sha` is the exact merge SHA**",
        "final post-CI verification and lifecycle closure",
    ])
    def test_each_of_the_seven_conditions_is_required(self, flat_sections, condition):
        assert condition in flat_sections["N"]

    def test_no_single_step_suffices(self, flat_sections):
        text = flat_sections["N"]
        assert "**None is individually sufficient.**" in text
        assert "Opening this PR authorizes nothing" in text
        assert "principal acceptance does not; merge does not" in text
        assert "**Only complete closure of all seven does**" in text

    def test_what_becomes_authorized_is_a_future_unit_not_an_armed_stage(self, flat_sections):
        assert (
            "a **future rebinding unit**, not an armed Stage 1"
        ) in flat_sections["N"]

    def test_the_ci_run_must_not_be_the_pr_head_run(self, flat_sections):
        assert (
            "not the PR head's own CI run, and not a run against any other commit"
        ) in flat_sections["N"]


class TestNoProtectedByteWasTouched:
    @pytest.mark.parametrize("relpath", PROTECTED_RELPATHS)
    def test_protected_path_is_unchanged_from_the_pr_base_to_head(self, relpath):
        """PROOF 1 of 2, added after review 4976985695 MINOR 1.

        The governance-only claim is about the PR's own diff, so it must be measured across the
        PR's own diff: exact base -> head, from the object store. A protected file edited *and
        committed* is invisible to a HEAD-versus-worktree comparison, which is what the previous
        single check actually measured.
        """
        assert (ROOT / relpath).exists(), f"{relpath} must still exist"
        changed = _paths_changed_between(PR_BASE_SHA, PR_MERGE_SHA, (relpath,))
        assert changed == [], (
            f"{relpath} changed between the PR base {PR_BASE_SHA} and HEAD; this filing is "
            "governance-only and must not touch it"
        )

    def test_the_base_to_head_comparison_detects_a_real_protected_change(self):
        """MUTATION PIN for proof 1: the check must not be able to pass vacuously.

        Uses a real, immutable historical commit pair -- PR #342's base and its merge -- across
        which the authorization module was lawfully corrected. If the comparison mechanism ever
        stops detecting a genuine committed protected-path change, this fails, even while the
        assertion above still (correctly) reports no change across this PR.
        """
        changed = _paths_changed_between(
            PROTECTED_CHANGE_CONTROL_BEFORE,
            PROTECTED_CHANGE_CONTROL_AFTER,
            (PROTECTED_CHANGE_CONTROL_PATH,),
        )
        assert changed == [PROTECTED_CHANGE_CONTROL_PATH], (
            "the base->head protected-path comparison failed to detect a known real change; it "
            "would pass vacuously"
        )

    @pytest.mark.parametrize("relpath", PROTECTED_RELPATHS)
    def test_protected_path_is_unchanged_against_head(self, relpath):
        """PROOF 2 of 2 -- RETAINED UNWEAKENED.

        Worktree cleanliness at the reviewed head. This never proved the base->head boundary and
        is not asked to; it is kept because an uncommitted protected edit is a real, separate
        failure mode that proof 1 cannot see.
        """
        path = ROOT / relpath
        assert path.exists(), f"{relpath} must still exist"
        blob = _git("rev-parse", f"HEAD:{relpath}").strip()
        committed = subprocess.run(
            ["git", "cat-file", "blob", blob], cwd=ROOT, capture_output=True, check=False
        )
        assert committed.returncode == 0
        assert hashlib.sha256(committed.stdout).hexdigest() == hashlib.sha256(
            path.read_bytes()
        ).hexdigest(), f"{relpath} differs from HEAD; this filing must not touch it"

    def test_the_pr_base_pin_is_a_real_commit_distinct_from_head(self):
        """MUTATION PIN for proof 1's anchor (mutation C3-04).

        Repointing ``PR_BASE_SHA`` at ``HEAD`` -- or at any commit that is not this PR's real
        base -- would make the base->head comparison compare a commit with itself and pass
        vacuously without touching a single assertion. Pinned here so that edit fails.
        """
        assert len(PR_BASE_SHA) == 40
        assert all(c in "0123456789abcdef" for c in PR_BASE_SHA)
        assert len(PR_MERGE_SHA) == 40
        assert all(c in "0123456789abcdef" for c in PR_MERGE_SHA)
        assert PR_BASE_SHA != PR_MERGE_SHA, "the base and merge pins must be distinct commits"
        merge_base = _git("merge-base", PR_BASE_SHA, PR_MERGE_SHA).strip()
        assert merge_base == PR_BASE_SHA, (
            "the base pin must be an ancestor of the merge pin; it is this PR's real base"
        )
        # The closed range must be on the authorized history, not an orphan.
        head = _git("rev-parse", "HEAD").strip()
        assert _git("merge-base", PR_MERGE_SHA, head).strip() == PR_MERGE_SHA, (
            "the merge pin must be an ancestor of HEAD"
        )

    def test_the_positive_control_uses_the_real_constants(self):
        """MUTATION PIN for the positive control itself (mutation C3-03).

        A control can be neutered without looking neutered -- pass an empty path tuple and expect
        an empty result, and it still passes while proving nothing. This reads the control's own
        source and requires it to reference the real path constant on both sides.
        """
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        target = None
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.FunctionDef)
                and node.name == "test_the_base_to_head_comparison_detects_a_real_protected_change"
            ):
                target = node
        assert target is not None, "the positive control is missing"
        names = {n.id for n in ast.walk(target) if isinstance(n, ast.Name)}
        for required in (
            "PROTECTED_CHANGE_CONTROL_BEFORE",
            "PROTECTED_CHANGE_CONTROL_AFTER",
            "PROTECTED_CHANGE_CONTROL_PATH",
        ):
            assert required in names, f"the control must reference {required}"
        # The control must ASSERT a non-empty change, never an empty one.
        asserts = [n for n in ast.walk(target) if isinstance(n, ast.Assert)]
        assert asserts, "the control must assert something"
        source = ast.get_source_segment(SUITE_PATH.read_text(encoding="utf-8"), target)
        assert "changed == [PROTECTED_CHANGE_CONTROL_PATH]" in source, (
            "the control must require the known change to be DETECTED, not require an empty result"
        )

    def test_the_two_protected_proofs_are_distinct_mechanisms(self):
        """Proof 1 compares two COMMITS; proof 2 compares a commit with the WORKING TREE.

        Pinned structurally so a later simplification cannot collapse them into one check and
        silently reintroduce the MINOR 1 blind spot.
        """
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        }
        assert "test_protected_path_is_unchanged_from_the_pr_base_to_head" in names
        assert "test_protected_path_is_unchanged_against_head" in names
        assert "test_the_base_to_head_comparison_detects_a_real_protected_change" in names

    def test_suite_never_calls_an_execution_entry_point(self):
        tree = ast.parse(SUITE_PATH.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
                assert name not in {
                    "write_authorization",
                    "claim_execution",
                    "complete_execution",
                    "new_execution_is_authorized",
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

    def test_suite_runs_no_mutating_git_command(self):
        """Every ``git`` call here must be a read; a write would make the suite a mutation.

        The verbs are assembled at runtime so this scan can never be satisfied -- or
        defeated -- by its own source literals.
        """
        source = SUITE_PATH.read_text(encoding="utf-8")
        verbs = [
            "com" + "mit", "check" + "out", "re" + "set",
            "pu" + "sh", "mer" + "ge", "reb" + "ase", "cle" + "an",
        ]
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            for argument in node.args:
                if isinstance(argument, ast.Constant) and argument.value in verbs:
                    pytest.fail(f"suite must not run a mutating git command: {argument.value}")
                if isinstance(argument, (ast.List, ast.Tuple)):
                    for element in argument.elts:
                        if isinstance(element, ast.Constant) and element.value in verbs:
                            pytest.fail(
                                f"suite must not run a mutating git command: {element.value}"
                            )

    def test_suite_references_no_protected_risk_result_path(self):
        """Naming the boundary in prose is fine; referencing a real RISK results path is not."""
        text = SUITE_PATH.read_text(encoding="utf-8")
        risk = "ri" + "sk"
        for token in (
            f"research/level1_{risk}_evidence",
            f"{risk}_level1_result",
            f"{risk}_results",
            "attempt2_" + "results",
        ):
            assert token not in text

    def test_decision_withholds_reading_the_protected_lane_boundary(self, flat_sections):
        assert (
            "reading, listing, opening, or referencing any `risk_lane_boundary` protected `RISK` "
            "result path"
        ) in flat_sections["K"]

    def test_decision_withholds_every_portfolio_and_allocator_byte(self, flat_sections):
        text = flat_sections["K"]
        for token in ("targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml"):
            assert token in text
        assert "authorizing any chart, ladder, deployment, trade, order, or brokerage action" in text


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
        assert "XASSET-0042" in entry["related_decisions"]
        assert "XASSET-0041" in entry["related_decisions"]

    def test_catalog_file_reference_resolves(self, catalog):
        entry = [d for d in catalog if d.get("decision_id") == DECISION_ID][0]
        assert (ROOT / entry["file"]).exists()

    def test_catalog_ids_are_unique(self, catalog):
        ids = [d.get("decision_id") for d in catalog]
        assert len(ids) == len(set(ids))

    def test_self_gate_is_in_progress_while_its_own_pr_is_unmerged(self, gates):
        """No session may mark its own unmerged work complete."""
        gate = gates[GATE_SELF]
        assert gate["status"] == "in_progress"
        assert gate["pr"] == XASSET0043_ACTIVE_PR

    def test_self_gate_records_the_authorization_and_its_limits(self, gates):
        description = gates[GATE_SELF]["description"]
        for phrase in (
            "GOVERNANCE-ONLY",
            "THIS FILING PERFORMS NO PART OF THE REBINDING",
            "XASSET-0041 SS-I link 2",
            "NO LANE WAS CREATED, INSPECTED OR TOUCHED",
            "ZERO activation authorizations",
        ):
            assert phrase in description, f"the self-gate must record: {phrase}"

    def test_self_gate_states_step_8_is_not_reconsumed(self, gates):
        description = gates[GATE_SELF]["description"]
        assert "CONSUMED by XASSET-0037 and is NOT reopened" in description
        assert "RECONCILIATION lifecycle" in description
        assert "step-8 EQUIVALENT" in description

    def test_self_gate_records_the_corrected_boundary_not_the_stale_one(self, gates):
        """Review 4976985695 MAJOR 1 -- the register must not contradict the corrected decision."""
        description = gates[GATE_SELF]["description"]
        assert "LOAD_BEARING_RELPATHS 10 -> 14" in description
        assert "DIRECT MEMBERSHIP" in description
        for decision in ("XASSET-0041", "XASSET-0042", "XASSET-0043"):
            assert decision in description
        assert "citing or describing predecessor text explicitly NOT a binding of it" in description

    def test_self_gate_operative_requirement_is_not_the_superseded_ten_to_eleven(self, gates):
        """`10 -> 11` may appear only where the correction history DESCRIBES the old defect."""
        description = gates[GATE_SELF]["description"]
        assert "LOAD_BEARING_RELPATHS 10 -> 11" not in description
        if "10 -> 11" in description:
            index = description.index("10 -> 11")
            window = description[max(0, index - 200): index]
            assert "MAJOR 1" in window, (
                "`10 -> 11` may only appear inside the correction history's description of the "
                "superseded requirement"
            )

    def test_self_gate_records_the_appended_derivation_transition(self, gates):
        """Review 4976985695 MAJOR 2."""
        description = gates[GATE_SELF]["description"]
        assert "HISTORICAL ANCHORS" in description
        assert (
            "APPENDING a second exact closed successor-to-rebound transition after the future "
            "bytes stabilize"
        ) in description
        assert "SS-G.4a" in description

    def test_self_gate_records_the_correction_history_with_all_three_findings(self, gates):
        description = gates[GATE_SELF]["description"]
        assert "BOUNDED CORRECTION" in description
        assert "4976985695" in description
        assert "0 BLOCKING / 2 MAJOR /" in description
        assert "REPRODUCED THROUGH THE REAL MECHANISMS before anything" in description
        for finding in ("MAJOR 1:", "MAJOR 2:", "MINOR 1:"):
            assert finding in description, f"the correction history must record {finding}"

    def test_self_gate_records_the_two_protected_proofs(self, gates):
        """Review 4976985695 MINOR 1."""
        description = gates[GATE_SELF]["description"]
        assert "TWO distinct proofs" in description
        assert "RETAINED UNWEAKENED" in description
        assert "mutation-pinned against a real" in description

    def test_self_gate_records_the_reproduced_drift_exactly(self, gates):
        description = gates[GATE_SELF]["description"]
        assert BOUND_MERGE_SHA in description
        assert BOUND_MODULE_SHA256 in description
        assert CURRENT_MODULE_SHA256 in description
        assert "exactly ONE drifts" in description

    def test_prior_gate_is_complete_on_merged_lifecycle_evidence(self, gates):
        gate = gates[GATE_PRIOR]
        assert gate["status"] == "complete"
        assert gate["pr"] == 342
        description = gate["description"]
        for evidence in (
            CORRECTION_MERGE_SHA,
            CORRECTION_ACCEPTED_HEAD,
            CORRECTION_MERGE_BASE,
            CORRECTION_MERGE_TREE,
            CORRECTION_FULL_REVIEW,
            CORRECTION_DELTA_REVIEW,
            CORRECTION_FINAL_REVIEW,
            CORRECTION_ACCEPTANCE,
            CORRECTION_VERIFICATION,
            CORRECTION_CLOSURE,
            CORRECTION_CI_RUN,
            CORRECTION_CI_JOB,
        ):
            assert evidence in description, f"completion is unevidenced: {evidence} missing"

    def test_prior_gate_does_not_misdescribe_the_final_review_as_full(self, gates):
        assert (
            "4976294690 is a DELTA review, not a standalone FULL review"
        ) in gates[GATE_PRIOR]["description"]

    def test_prior_gate_narrative_is_preserved_as_an_exact_prefix(self, gates):
        """This filing APPENDS completion truth; it may not rewrite a single earlier sentence."""
        description = gates[GATE_PRIOR]["description"]
        prefix = description[: len(description)]
        assert len(prefix) > 12681
        narrative = description[:12681]
        digest = hashlib.sha256(narrative.encode("utf-8")).hexdigest()
        assert digest == PRIOR_GATE_NARRATIVE_SHA256, (
            "the XASSET-0042 gate narrative must be preserved byte-identically as a prefix"
        )

    def test_prior_gate_hands_the_drift_to_a_separately_authorized_rebinding(self, gates):
        description = gates[GATE_PRIOR]["description"]
        assert "SEPARATELY AUTHORIZED rebinding" in description
        assert "which XASSET-0042 neither performed nor authorized" in description

    def test_register_live_fields_point_at_the_currently_live_work(self, ws0014):
        """`active_branch`, `active_pr` and `last_verified_main_sha` are WS-0014's SINGLE SHARED
        live self-reference fields. PR #342 has merged at `5fbfc94d`, so under `OPS-0001`'s
        Active-GitHub-fields rule they lawfully advance to the unit that is now live."""
        # ADVANCED AGAIN BY XASSET-0045, on exactly the terms the docstring above already states:
        # these are WS-0014's SINGLE SHARED live fields, PR #344 has since merged at `f5dedce1`,
        # and under OPS-0001's Active-GitHub-fields rule they lawfully advance again to whatever
        # unit is now live. What this test protects -- that they point at the LIVE work rather than
        # at a closed one -- is unchanged, so it is asserted against the closed values it must NOT
        # still be showing, plus the current anchor, which is now EXACT rather than a floor.
        assert ws0014["active_branch"] != ACTIVE_BRANCH
        assert ws0014["active_pr"] != XASSET0043_ACTIVE_PR
        assert ws0014["last_verified_main_sha"] != CORRECTION_MERGE_SHA
        assert ws0014["last_verified_main_sha"] != PR_MERGE_SHA
        # ADVANCED AGAIN BY XASSET-0046, on the same terms: PR #345 has since merged at
        # `2f8cdebe`, so the shared field advances once more. Bound at BOTH ends -- the exact
        # current value, and every closed value it must no longer be showing.
        # ADVANCED BY XASSET-0049: this is the register's SHARED live field, so it names the
        # currently-live unit. Bound at BOTH ends -- every prior generation's value is a negative
        # pin, so a silent revert to finished work still fails here.
        assert ws0014["last_verified_main_sha"] == XASSET0052_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0051_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0050_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0049_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0048_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0047_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0046_MAIN_SHA
        assert ws0014["last_verified_main_sha"] != XASSET0044_MERGE_SHA
        assert str(ws0014["last_verified_date"]) >= "2026-08-21"
        # PR #343's own closed record survives in the register as history, not as live state.
        register = REGISTER_PATH.read_text(encoding="utf-8")
        assert ACTIVE_BRANCH in register
        assert str(XASSET0043_ACTIVE_PR) in register

    def test_register_still_parses_and_ws0014_is_unique(self, ws0014):
        assert ws0014["id"] == "WS-0014"
        assert ws0014["status"] == "proposed"
        assert ws0014["priority"] == "secondary"


# ======================================================================================
# 12 -- No section is vacuous; suite hygiene
# ======================================================================================


class TestNoSectionIsVacuous:
    @pytest.mark.parametrize("letter", list("ABCDEFGHIJKLMN"))
    def test_every_section_has_substantive_content(self, sections, letter):
        assert letter in sections, f"§{letter} is missing"
        body = sections[letter]
        content = body.split("\n", 1)[1] if "\n" in body else ""
        assert len(content.strip()) > 200, f"§{letter} is vacuous"

    def test_decision_has_rationale_alternatives_and_consequences(self, decision_body):
        for heading in ("## Rationale", "## Alternatives Considered", "## Consequences"):
            assert heading in decision_body

    def test_front_matter_declares_the_supporting_artifact(self, decision_text):
        assert f"supporting_artifact: {SUITE_PATH.name}" in decision_text

    def test_front_matter_status_is_proposed(self, decision_text):
        assert "status: Proposed" in decision_text.split("---\n", 2)[1]

    def test_front_matter_relates_the_decision_to_its_two_predecessors(self, decision_text):
        front = decision_text.split("---\n", 2)[1]
        assert "XASSET-0041" in front
        assert "XASSET-0042" in front


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
            "level1_endpoint_evidence_preregistration_validator",
            "level1_construction_universe_closure_validator",
        ):
            assert outcome_module not in imported, (
                f"suite must not import outcome-producing module {outcome_module!r}"
            )
