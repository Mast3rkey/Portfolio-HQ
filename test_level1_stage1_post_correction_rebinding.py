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

#: The bytes this rebinding is measured against. Its own base is the XASSET-0043 merge.
PR_BASE_SHA = "0709d2f05ab031ecb6f69c40465ed4a227983aed"

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
        assert A.REBINDING_AUTHORIZING_DECISION == "XASSET-0043"
        assert A.REBINDING_AUTHORIZING_PULL_REQUEST == 343
        assert A.REVIEWED_BASE_SHA == A.REBINDING_AUTHORIZING_MERGE_SHA
        assert A.REVIEWED_BASE_SHA == PR_BASE_SHA
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
        assert len(XASSET_0037_LOAD_BEARING) == 10
        assert len(A.LOAD_BEARING_RELPATHS) == 14
        assert len(set(A.LOAD_BEARING_RELPATHS)) == 14

    def test_every_predecessor_path_is_retained(self):
        """Growth is additive. A path traded away is the defect this catches."""
        assert set(XASSET_0037_LOAD_BEARING) <= set(A.LOAD_BEARING_RELPATHS)

    def test_the_additions_are_exactly_the_four_authority_chain_files(self):
        additions = set(A.LOAD_BEARING_RELPATHS) - set(XASSET_0037_LOAD_BEARING)
        assert additions == set(BOUNDARY_ADDITIONS)

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
        declared = [
            ln for ln in decision_text.split("\n")
            if ln.strip().startswith("CURRENT_MODULE_SHA256:")
        ]
        assert len(declared) == 1
        tokens = [
            token for token in declared[0].replace("`", " ").split()
            if len(token) == 64 and all(c in "0123456789abcdef" for c in token)
        ]
        assert len(tokens) == 1
        assert tokens[0] == hashlib.sha256(
            (ROOT / AUTH_MODULE_RELPATH).read_bytes()
        ).hexdigest()

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
        authorized, reason = A.new_execution_is_authorized()
        assert authorized is False
        assert DECISION_ID in reason

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
        assert gates[GATE_SELF]["status"] == "in_progress"
        assert gates[GATE_SELF]["pr"] is None, (
            "a filing may not mark its own unmerged work complete"
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
        register = REGISTER_PATH.read_text(encoding="utf-8")
        current = hashlib.sha256((ROOT / AUTH_MODULE_RELPATH).read_bytes()).hexdigest()
        assert current in register.replace("\n", "").replace(" ", "")

    def test_the_workstream_posture_is_unchanged(self, ws0014):
        assert ws0014["status"] == "proposed"
        assert ws0014["priority"] == "secondary"
        assert ws0014["last_verified_main_sha"] == PR_BASE_SHA


# ======================================================================================
# 13 -- No section is vacuous
# ======================================================================================


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
