"""Adversarial tests pinning the ``XASSET-0060`` post-parser-correction operational rebinding.

``XASSET-0057`` authorized **exactly one** future pull request to reconcile the load-bearing
register with the merged parser-corrected bytes, and then refused to do it itself -- because the
bytes it would have bound carried a **live** parser defect. That refusal shaped everything about
this unit: ``§F.0`` made a separately authorized, independently reviewed, merged, CI-green and
closed parser correction a **conjunctive prerequisite**, recorded the vulnerable identity
``12eab05e…604a5`` as a **permanent negative pin**, and ``§F.2`` withdrew the base rule every
predecessor rebinding had used.

The danger this suite exists to prevent is not the rebinding. It is the set of ways a rebinding of
exactly this shape can look correct while being wrong:

1. **Binding the vulnerable module.** ``TestTheVulnerableIdentityCanNeverBeBound`` -- the negative
   pin driven as a refusal against the merged tree, not read as prose. A rebinding that bound role
   2 *consistently* would satisfy every agreement check the module already had.
2. **A base that is anything but the Lifecycle B merge.** ``TestBaseEqualityIsOperative`` -- the
   new rule extracted as a pure function and driven against a REAL later descendant, against the
   superseded base, and against the authorizing merge, each of which a looser rule would accept.
3. **A prerequisite lifecycle that merged but never became effective.**
   ``TestBothPrerequisiteLifecyclesReallyClosed`` -- ``XASSET-0044`` and ``XASSET-0045`` each
   merged and neither became effective, which is exactly why ``§F.0.3`` requires more than merge.
4. **A moved value with one end unbound.** ``TestExactClosedTransitions``.
5. **A predecessor identity destroyed by the move.** ``TestPredecessorIdentitiesArePreserved`` --
   reproduced against the base, where ``XASSET-0049``'s identity was reachable ONLY through the
   three values this unit moves.
6. **The boundary shrunk, swapped, reordered or traded rather than extended.**
   ``TestTrustBoundaryGrewAdditively`` -- including ``XASSET-0054``'s exclusion, which ``§F.7``
   permits to be lifted only on independent evidence that it is operative.
7. **Meaning moved under cover of a byte-binding.** ``TestTheOutcomeSurfaceIsUnchanged`` and
   ``TestCanonicalArtifactsAreUnamended``.
8. **The authority mistaken for the unit, or a prerequisite claimed as this unit's own work.**
   ``TestTheNewRefusalsAreIndependentlyRequired``.
9. **Something armed, claimed, or executed.** ``TestNothingIsArmed``.
10. **A proof that passes because it asserts nothing.** ``TestNonVacuityAgainstTheBase`` -- every
    re-anchored claim shown FAILING at this unit's own base.

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

import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
SUITE_PATH = Path(__file__).resolve()

DECISION_ID = "XASSET-0060"
DECISION_RELPATH = (
    "governance/decisions/"
    "XASSET-0060-endpoint-0001-stage-1-post-parser-correction-operational-rebinding.md"
)
DECISION_PATH = ROOT / DECISION_RELPATH
AUTHORITY_RELPATH = (
    "governance/decisions/"
    "XASSET-0057-endpoint-0001-stage-1-post-parser-correction-rebinding-authorization.md"
)
CATALOG_RELPATH = "governance/decisions.yaml"
REGISTER_RELPATH = "operations/WORKSTREAMS.yaml"
AUTH_MODULE_RELPATH = "level1_stage1_execution_authorization.py"
REGISTER_GATE = "xasset0060-post-parser-correction-operational-rebinding"
PRIOR_UNIT_GATE = "xasset0059-post-merge-verification"

# ── The impossible sentinel, and the number GitHub actually issued ──────────────────────────
#
# A pull-request number cannot be negative, so the sentinel can never be mistaken for a real one
# and can never accidentally validate. ``-3`` is deliberately distinct from XASSET-0047's ``0``,
# XASSET-0048's ``-1`` and XASSET-0049's ``-2``.
PULL_REQUEST_SENTINEL = -3
#: Read back from live GitHub AFTER the draft was opened. Never predicted.
THIS_PULL_REQUEST = 361

#: ADVANCED BY XASSET-0061. Every decision appended to the catalog AFTER this one,
#: named EXACTLY, so "last" stays an exact index rather than being relaxed to "present".
SUCCESSORS_APPENDED_SINCE = ("XASSET-0061",)
#: Gates this unit's successors added to WS-0014 after this unit's own two.
SUCCESSOR_GATES_ADDED_SINCE = 2
#: The shared live fields lawfully moved onto the successor; this unit's own values
#: are retained as NEGATIVE pins so a silent revert to finished work still fails.
SUCCESSOR_BRANCH_NAME = "claude/xasset-0061-authorization-jux8p9"
SUCCESSOR_ACTIVE_PR = 362
SUCCESSOR_MAIN_SHA_VALUE = "413e033ac33741829168762ab24d73327c047d4b"

# ── XASSET-0057 / PR #358 — this unit's AUTHORITY (not its base) ────────────────────────────
PR358_BASE_SHA = "583022a5f2106d61f82d270edadd3520d8b0c55d"
PR358_ACCEPTED_HEAD = "53d2d3d770f379393a1a3fde4408915c9fcf81f0"
PR358_MERGE_SHA = "556a43cf91679d3e8ca95703c8d49e672b662b73"
PR358_MERGE_TREE = "0c7b738c22c2a0f3bbdfa9cbcea3971a7029307f"
PR358_CLEAN_REVIEW = "5030740306"
PR358_PRINCIPAL_ACCEPTANCE = "5425835377"
PR358_POST_MERGE_VERIFICATION = "5425857818"
PR358_FINAL_CLOSURE = "5426014312"
PR358_MERGE_CI_RUN = "32973075626"

# ── XASSET-0058 / PR #359 — Lifecycle A (§F.0.3) ────────────────────────────────────────────
PR359_BASE_SHA = "556a43cf91679d3e8ca95703c8d49e672b662b73"
PR359_ACCEPTED_HEAD = "e8d53c184a7612ab6e38ba8d7ae1e348f7046de2"
PR359_MERGE_SHA = "34c45900ce23742d04d80cf12471c34aabe9682d"
PR359_MERGE_TREE = "76e1021499464f4c2152d9e55c0d03b5ea14708c"
PR359_FULL_REVIEW = "5034171910"
PR359_CLEAN_DELTA_REVIEW = "5035960873"
PR359_PRINCIPAL_ACCEPTANCE = "5432460504"
PR359_POST_MERGE_VERIFICATION = "5432479068"
PR359_FINAL_CLOSURE = "5432562310"
PR359_MERGE_CI_RUN = "33024792395"

# ── XASSET-0059 / PR #360 — Lifecycle B, whose B5 merge IS this unit's base ─────────────────
PR360_BASE_SHA = "34c45900ce23742d04d80cf12471c34aabe9682d"
PR360_FIRST_REVIEWED_HEAD = "ebec2f1626e59db587903bcb684fbe4fd600a922"
PR360_REJECTED_DELTA_HEAD = "0082fae3f1ea591594e720f6177295e5ddceb91b"
PR360_ACCEPTED_HEAD = "90b829863875223d56b8da2c62ba0bfc06fbcd7e"
PR360_MERGE_SHA = "301e79334876a4bda6e7b89a6156b34e8d38a605"
PR360_MERGE_TREE = "3bf579d64fd86680668d628f557b86e66ab7e76a"
PR360_FULL_REVIEW = "5037196415"
PR360_ADVERSE_DELTA_REVIEW = "5041611657"
PR360_CLEAN_DELTA_REVIEW = "5044822360"
PR360_PRINCIPAL_ACCEPTANCE = "5444698584"
PR360_POST_MERGE_VERIFICATION = "5444767925"
PR360_MERGE_CI_RUN = "33112432925"
PR360_MERGE_CI_JOB = "98658423867"
PR360_FINAL_CLOSURE = "5444905083"

#: This unit's own base. XASSET-0057 §F.2 permits exactly one value: the Lifecycle B B5 merge.
THIS_UNIT_BASE_SHA = PR360_MERGE_SHA

# ── XASSET-0049 / PR #349 — the PRIOR anchor this unit supersedes ───────────────────────────
PR349_ACCEPTED_HEAD = "b2059e80101fc6457f4004939d7d12886e6feedf"
PR349_MERGE_SHA = "a941455491cc5e4d3d868775fb6b4b88f0fe2ce3"
PR349_MERGE_BASE = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"

# ── The four-role module identity chain (XASSET-0057 §F.3) ──────────────────────────────────
ROLE1_SHA256 = "4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541"
ROLE1_BLOB = "f71b08b4ebe95f161c57cdbb2a924748f13af02d"
ROLE1_COMMIT = "8ab773866c5959cd61a73dd48af197339c48754a"

ROLE2_SHA256 = "12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5"
ROLE2_BLOB = "b5622f9e412afd604a11cde04317b79c5e57920a"
ROLE2_COMMIT = "f1bf3fd0f1f878ccf9db88f15c48059e5e4637e2"

ROLE3_SHA256 = "1283a2d4ccc3794fd37b81d4e5e23ac6f67a0b87b911ef3861c724d636fabd00"
ROLE3_BLOB = "b8414a69f41e37f8fdd5c18dae13176fd847170e"
ROLE3_COMMIT = PR360_ACCEPTED_HEAD

#: Role 4 -- DERIVED after every authorized byte stabilized, recorded once and last. It is
#: deliberately NOT a module constant: a file cannot carry its own post-edit digest.
ROLE4_SHA256 = "3f261b6b3cdcabc5f0cb228d987a52dd36e2a0f522e7fc4e57c483d3c0e3001a"
ROLE4_BLOB = "a9753d1273785e9ce2ebb4de2067489dfbb9156c"

#: The exact membership the register bound at this unit's base, and the seven additions.
LOAD_BEARING_COUNT_AT_BASE = 18
LOAD_BEARING_COUNT_NOW = 25
ADDED_DECISION_IDS = (
    "XASSET-0053", "XASSET-0055", "XASSET-0056",
    "XASSET-0057", "XASSET-0058", "XASSET-0059", "XASSET-0060",
)


# ======================================================================================
# Helpers -- immutable git facts only
# ======================================================================================


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _commit_exists(sha: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=ROOT, capture_output=True, text=True,
    ).returncode == 0


def _object_exists(sha: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", sha], cwd=ROOT, capture_output=True, text=True,
    ).returncode == 0


def _range_is_present(*shas: str) -> bool:
    """Whether ANY of the named anchors is in this checkout.

    Deliberately ``any``, not ``all``. A checkout holding none of them is genuinely truncated and
    is an environment precondition; a checkout holding some but not all is a REFUSAL inside the
    proof, never a skip, so one unresolvable object cannot silence the whole thing.
    """
    return any(_commit_exists(sha) for sha in shas)


def _blob_at(commit: str, relpath: str) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", f"{commit}:{relpath}"],
        cwd=ROOT, capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _sha256_at(commit: str, relpath: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relpath}"],
        cwd=ROOT, capture_output=True,
    )
    if result.returncode != 0:
        return None
    import hashlib
    return hashlib.sha256(result.stdout).hexdigest()


def _flat(text: str) -> str:
    """Collapse whitespace runs and drop blockquote markers, so an exact phrase match is
    insensitive to where hard-wrapped prose happens to break. Not a weakening: the full phrase
    must still be present, contiguously."""
    return re.sub(r"\s+", " ", text.replace("\n>", "\n")).strip()


def _load_bearing_declared_at(commit: str) -> tuple[str, ...]:
    """The exact ``LOAD_BEARING_RELPATHS`` the production module DECLARED at a given commit.

    Parsed with ``ast`` and never imported or executed, so a historical module's code cannot run.
    Implicit string concatenation and module-level aliases are resolved from the SAME historical
    source, never from the live module.
    """
    source = subprocess.run(
        ["git", "show", f"{commit}:{AUTH_MODULE_RELPATH}"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    tree = ast.parse(source)

    def _module_string(name: str) -> str:
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets
            ):
                value = ast.literal_eval(node.value)
                assert isinstance(value, str), name
                return value
        raise AssertionError(f"{name} is not a module-level string assignment")

    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "LOAD_BEARING_RELPATHS" for t in node.targets
        ):
            assert isinstance(node.value, ast.Tuple)
            values: list[str] = []
            for element in node.value.elts:
                if isinstance(element, ast.Constant) and isinstance(element.value, str):
                    values.append(element.value)
                elif isinstance(element, ast.Name):
                    values.append(_module_string(element.id))
                else:  # pragma: no cover - defensive
                    raise AssertionError(f"unexpected element {ast.dump(element)}")
            return tuple(values)
    raise AssertionError("LOAD_BEARING_RELPATHS is not declared at that commit")


def _module_constant_at(commit: str, name: str):
    """A module-level constant's literal value at a historical commit, via ``ast`` only."""
    source = subprocess.run(
        ["git", "show", f"{commit}:{AUTH_MODULE_RELPATH}"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            return ast.literal_eval(node.value)
    raise AssertionError(f"{name} is not declared at {commit}")


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_flat(decision_text: str) -> str:
    return _flat(decision_text)


@pytest.fixture(scope="module")
def catalog() -> dict:
    return yaml.safe_load((ROOT / CATALOG_RELPATH).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ws0014() -> dict:
    register = yaml.safe_load((ROOT / REGISTER_RELPATH).read_text(encoding="utf-8"))
    return next(w for w in register["workstreams"] if w["id"] == "WS-0014")


# ======================================================================================
# 1 -- The permanent negative pin: role 2 may NEVER be a bound end
# ======================================================================================


class TestTheVulnerableIdentityCanNeverBeBound:
    """``XASSET-0057`` §F.0's negative pin, driven as a refusal rather than read as prose.

    This is the finding that shaped the whole grant. §F.0 refuses the vulnerable bytes "at any
    time, under any reading, however unchanged ``main`` may be", and §F.3 says a rebinding whose
    bound module identity equals role 2 "fails outright". A rebinding that bound role 2
    *consistently* -- recorded, merged and working tree all agreeing on it -- would satisfy every
    agreement check the module already had, so a separate refusal is genuinely required.
    """

    def test_the_refused_identity_is_bound_as_a_constant(self):
        assert A.VULNERABLE_MODULE_SHA256 == ROLE2_SHA256
        assert A.VULNERABLE_MODULE_BLOB == ROLE2_BLOB
        assert ROLE2_SHA256 in A.NEVER_BINDABLE_MODULE_SHA256

    def test_the_rule_refuses_the_vulnerable_identity(self):
        errors = A._verify_module_identity_is_not_the_vulnerable_intermediate(ROLE2_SHA256)
        assert errors, "role 2 must be refused"
        assert any("PERMANENTLY REFUSED" in e for e in errors), errors

    def test_the_rule_admits_every_other_role_in_the_chain(self):
        for identity in (ROLE1_SHA256, ROLE3_SHA256):
            assert A._verify_module_identity_is_not_the_vulnerable_intermediate(identity) == []

    def test_an_absent_identity_is_not_silently_admitted_as_refused(self):
        """``None`` means the caller could not resolve the blob at all. That is the SURROUNDING
        verifier's error to raise -- it already does -- and must not be converted into a negative
        pin hit, which would misattribute the failure."""
        assert A._verify_module_identity_is_not_the_vulnerable_intermediate(None) == []

    def test_the_refusal_set_is_driveable_and_not_read_from_a_global(self):
        """MUTATION PIN. A rule that read the module global directly could not be driven against
        a known-bad input at all, so the negative test above would be unwritable."""
        assert A._verify_module_identity_is_not_the_vulnerable_intermediate(
            "x" * 64, frozenset({"x" * 64})
        )
        assert A._verify_module_identity_is_not_the_vulnerable_intermediate(
            ROLE2_SHA256, frozenset()
        ) == []

    def test_the_rule_reads_no_external_source(self):
        """Pure and offline: it must not be silenceable by an unavailable git, GitHub or clock.
        Proven structurally from the function's own AST, not from its docstring."""
        tree = ast.parse((ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8"))
        fn = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef)
            and n.name == "_verify_module_identity_is_not_the_vulnerable_intermediate"
        )
        called = {
            node.func.attr for node in ast.walk(fn)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        for forbidden in ("run", "is_ancestor", "commit_parents", "blob_sha256_at", "now",
                          "utcnow", "read_text", "read_bytes"):
            assert forbidden not in called, forbidden

    def test_the_refusal_is_actually_wired_into_the_identity_verifier(self):
        """A refusal nothing calls refuses nothing. Proved from the caller's own AST."""
        tree = ast.parse((ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8"))
        caller = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "_verify_git_anchored_identity"
        )
        called = {
            node.func.id for node in ast.walk(caller)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        assert "_verify_module_identity_is_not_the_vulnerable_intermediate" in called

    def test_the_bound_identity_is_not_role_two_anywhere(self):
        """The live end-to-end fact, not the rule in isolation: whatever the merged tree carries
        for this module, it is not the refused identity."""
        assert A.sha256_file(ROOT / AUTH_MODULE_RELPATH) != ROLE2_SHA256
        if _commit_exists(THIS_UNIT_BASE_SHA):
            assert _sha256_at(THIS_UNIT_BASE_SHA, AUTH_MODULE_RELPATH) != ROLE2_SHA256

    def test_the_module_relpath_constant_names_the_right_file(self):
        assert A.AUTHORIZATION_MODULE_RELPATH == AUTH_MODULE_RELPATH
        assert A.AUTHORIZATION_MODULE_RELPATH == A.LOAD_BEARING_RELPATHS[0]


# ======================================================================================
# 2 -- The four-role identity chain, every adjacent transition proved
# ======================================================================================


class TestTheModuleIdentityChain:
    """``XASSET-0057`` §F.3: four roles, one ordered chain, only the last ever bound.

    §F.3 withdrew the "two ends, already known" formulation as self-contradictory -- it named the
    vulnerable identity as the transition's NEW end while §F.0 forbids binding it. These tests
    derive every role from the object store and prove each adjacent transition separately.
    """

    def test_role_one_is_the_identity_the_register_bound_at_the_base(self):
        assert A.PREVIOUSLY_BOUND_MODULE_SHA256 == ROLE1_SHA256
        assert A.PREVIOUSLY_BOUND_MODULE_BLOB == ROLE1_BLOB
        if not _object_exists(ROLE1_BLOB):
            pytest.skip("role 1's blob is not present in this checkout")
        import hashlib
        raw = subprocess.run(
            ["git", "cat-file", "-p", ROLE1_BLOB], cwd=ROOT, capture_output=True, check=True,
        ).stdout
        assert hashlib.sha256(raw).hexdigest() == ROLE1_SHA256

    def test_role_two_is_derived_and_is_adverse_history_only(self):
        if not _object_exists(ROLE2_BLOB):
            pytest.skip("role 2's blob is not present in this checkout")
        import hashlib
        raw = subprocess.run(
            ["git", "cat-file", "-p", ROLE2_BLOB], cwd=ROOT, capture_output=True, check=True,
        ).stdout
        assert hashlib.sha256(raw).hexdigest() == ROLE2_SHA256
        # It is recorded, and it is refused. Both facts, together.
        assert A.VULNERABLE_MODULE_SHA256 == ROLE2_SHA256
        assert A._verify_module_identity_is_not_the_vulnerable_intermediate(ROLE2_SHA256)

    def test_role_three_is_derived_from_the_lifecycle_b_merge_not_predicted(self):
        """§F.0.4: role 3's value is DERIVED at the parser correction's own merge."""
        assert A.PARSER_CORRECTED_MODULE_SHA256 == ROLE3_SHA256
        assert A.PARSER_CORRECTED_MODULE_BLOB == ROLE3_BLOB
        if not _commit_exists(PR360_MERGE_SHA):
            pytest.skip("the Lifecycle B merge is not present in this checkout")
        assert _sha256_at(PR360_MERGE_SHA, AUTH_MODULE_RELPATH) == ROLE3_SHA256
        assert _blob_at(PR360_MERGE_SHA, AUTH_MODULE_RELPATH) == ROLE3_BLOB

    def test_the_four_roles_are_four_distinct_identities(self):
        identities = [ROLE1_SHA256, ROLE2_SHA256, ROLE3_SHA256, ROLE4_SHA256]
        assert len(set(identities)) == 4, identities

    def test_transition_one_to_two_is_proved_as_history_not_adoption(self):
        if not _range_is_present(ROLE1_COMMIT, ROLE2_COMMIT):
            pytest.skip("the role 1 -> role 2 range is not present in this checkout")
        assert _commit_exists(ROLE1_COMMIT) and _commit_exists(ROLE2_COMMIT)
        assert _sha256_at(ROLE1_COMMIT, AUTH_MODULE_RELPATH) == ROLE1_SHA256
        assert _sha256_at(ROLE2_COMMIT, AUTH_MODULE_RELPATH) == ROLE2_SHA256
        assert _git("merge-base", "--is-ancestor", ROLE1_COMMIT, ROLE2_COMMIT) == ""
        # HISTORY, NOT ADOPTION: role 2 is refused, and the register never moved to it.
        assert A._verify_module_identity_is_not_the_vulnerable_intermediate(ROLE2_SHA256)

    def test_transition_two_to_three_is_proved(self):
        if not _range_is_present(ROLE2_COMMIT, ROLE3_COMMIT):
            pytest.skip("the role 2 -> role 3 range is not present in this checkout")
        assert _commit_exists(ROLE2_COMMIT) and _commit_exists(ROLE3_COMMIT)
        assert _sha256_at(ROLE3_COMMIT, AUTH_MODULE_RELPATH) == ROLE3_SHA256
        assert _git("merge-base", "--is-ancestor", ROLE2_COMMIT, ROLE3_COMMIT) == ""

    def test_transition_three_to_four_is_proved_and_is_the_only_binding_one(self):
        """Role 3 reaches the register ONLY through role 4's own derivation."""
        live = A.sha256_file(ROOT / AUTH_MODULE_RELPATH)
        assert live == ROLE4_SHA256, (
            "role 4 must equal this unit's own stabilized module bytes; recompute it LAST"
        )
        assert live != ROLE3_SHA256, "this unit edited the module, so role 4 cannot equal role 3"
        if _commit_exists(THIS_UNIT_BASE_SHA):
            assert _sha256_at(THIS_UNIT_BASE_SHA, AUTH_MODULE_RELPATH) == ROLE3_SHA256

    def test_role_four_is_not_a_module_constant(self):
        """A file cannot carry its own post-edit digest. §F.3 records role 4 in the DECISION."""
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert ROLE4_SHA256 not in source
        assert ROLE4_SHA256 in DECISION_PATH.read_text(encoding="utf-8")

    def test_the_register_transition_performed_is_role_one_to_role_four(self):
        """Not role 1 -> role 3, and never anything -> role 2."""
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        declared_before = _load_bearing_declared_at(THIS_UNIT_BASE_SHA)
        assert AUTH_MODULE_RELPATH in declared_before
        assert AUTH_MODULE_RELPATH in A.LOAD_BEARING_RELPATHS
        assert A.sha256_file(ROOT / AUTH_MODULE_RELPATH) == ROLE4_SHA256
        assert A.PREVIOUSLY_BOUND_MODULE_SHA256 == ROLE1_SHA256


# ======================================================================================
# 3 -- The base rule XASSET-0057 §F.2 replaced
# ======================================================================================


class TestBaseEqualityIsOperative:
    """``XASSET-0057`` §F.2, converted from prose into a decidable proposition.

    §F.2 did something no predecessor did: it **withdrew** the rule every earlier rebinding used.
    "Equal your own authorization's merge" and "a parser correction must intervene" cannot both
    hold, so the replacement names one commit -- the Lifecycle B **B5 merge** -- and removes every
    admission path for an intervening commit. These tests drive the new rule, including against a
    real later descendant and against the base a looser reading would have accepted.
    """

    def test_the_module_binds_this_units_base_by_equality(self):
        assert A.REVIEWED_BASE_SHA == THIS_UNIT_BASE_SHA
        assert A.REVIEWED_BASE_SHA == A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA
        assert A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA == PR360_MERGE_SHA

    def test_the_base_is_NOT_this_units_own_authorizing_merge(self):
        """The single most important difference from every predecessor rebinding.

        `XASSET-0049` bound its base to `XASSET-0048`'s merge because that decision was both its
        authority and, under the rule then in force, the commit its base had to equal. §F.2 split
        those apart. A unit that bound `XASSET-0057`'s merge here would be applying the withdrawn
        rule -- and would be binding the state in which the §M parser defect is still live, which
        §F.2 names in terms as the case the earlier formulation wrongly permitted.
        """
        assert A.REVIEWED_BASE_SHA != A.POST_PARSER_CORRECTION_AUTHORIZING_MERGE_SHA
        assert A.POST_PARSER_CORRECTION_AUTHORIZING_MERGE_SHA == PR358_MERGE_SHA
        assert A._verify_post_parser_correction_base_equality(
            PR358_MERGE_SHA, A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA, True
        ), "the authorizing merge must be refused as a base"

    def test_the_lifecycle_b_merge_really_has_the_derived_identity(self):
        """§F.2 forbids ASSERTING this merge and requires DERIVING it. Derived here from the
        object store: ordered parents, and a merge tree byte-identical to the accepted head's."""
        if not _range_is_present(PR360_MERGE_SHA, PR360_ACCEPTED_HEAD, PR360_BASE_SHA):
            pytest.skip("PR #360's closed range is not present in this checkout")
        assert _commit_exists(PR360_MERGE_SHA)
        parents = _git("log", "-1", "--pretty=%P", PR360_MERGE_SHA).split()
        assert parents == [PR360_BASE_SHA, PR360_ACCEPTED_HEAD]
        assert _git("rev-parse", f"{PR360_MERGE_SHA}^{{tree}}") == PR360_MERGE_TREE
        assert _git("rev-parse", f"{PR360_ACCEPTED_HEAD}^{{tree}}") == PR360_MERGE_TREE

    def test_no_commit_intervened_between_the_b5_merge_and_this_units_base(self):
        """§F.2 removed EVERY admission path: "there is no clause by which such a commit may be
        admitted, absorbed, or cured inside XASSET-0057". Equality decides it, so this is a
        direct check that the equality was not merely asserted into existence."""
        assert A.REVIEWED_BASE_SHA == PR360_MERGE_SHA
        if not _commit_exists(PR360_MERGE_SHA):
            pytest.skip("the B5 merge is not present in this checkout")
        # Nothing on the first-parent path between them, because they are the same commit.
        assert _git("rev-list", "--count", f"{PR360_MERGE_SHA}..{A.REVIEWED_BASE_SHA}") == "0"

    def test_the_rule_accepts_the_bound_pair(self):
        assert A._verify_post_parser_correction_base_equality(
            A.REVIEWED_BASE_SHA, A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA, True
        ) == []

    def test_the_rule_refuses_a_real_later_descendant_even_with_ancestry_granted(self):
        """Reproduced against a REAL commit rather than a placeholder. Ancestry was never the
        wrong answer -- it was the wrong test, and equality survives ancestry being granted."""
        if not _commit_exists(PR360_MERGE_SHA):
            pytest.skip("the B5 merge is not present in this checkout")
        head = _git("rev-parse", "HEAD")
        if head == PR360_MERGE_SHA:
            pytest.skip("HEAD is the B5 merge itself; no later descendant exists here")
        assert _git("merge-base", "--is-ancestor", PR360_MERGE_SHA, head) == ""
        errors = A._verify_post_parser_correction_base_equality(
            head, A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA, True
        )
        assert errors, "a later descendant must be refused"
        assert any("EQUALITY" in e for e in errors), errors
        assert any("descent alone never qualifies" in e for e in errors), errors
        assert any("no admission path exists" in e for e in errors), errors

    def test_the_superseded_descent_only_rule_accepts_what_the_corrected_rule_refuses(self):
        """Retained beside the corrected rule and shown FAILING, so the correction is proved a
        real change in behaviour rather than a change in wording."""
        if not _commit_exists(PR360_MERGE_SHA):
            pytest.skip("the B5 merge is not present in this checkout")
        head = _git("rev-parse", "HEAD")
        if head == PR360_MERGE_SHA:
            pytest.skip("HEAD is the B5 merge itself")

        def superseded_descent_only_rule(base, merge, descends):
            return [] if descends else ["base does not descend"]

        assert superseded_descent_only_rule(head, PR360_MERGE_SHA, True) == []
        assert A._verify_post_parser_correction_base_equality(
            head, A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA, True
        ) != []

    def test_the_rule_refuses_the_superseded_base(self):
        """The value the anchor moved OFF must not validate under the rule it moved ON to."""
        errors = A._verify_post_parser_correction_base_equality(
            A.PRIOR_STEP8_EQUIVALENT_MERGE_BASE,
            A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA,
            True,
        )
        assert any("EQUALITY" in e for e in errors), errors

    @pytest.mark.parametrize("bad", [None, "", "not-a-sha", "abc", 42, "0" * 39, "z" * 40])
    def test_the_rule_refuses_a_malformed_identity_at_either_end(self, bad):
        assert A._verify_post_parser_correction_base_equality(
            bad, A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA, True
        )
        assert A._verify_post_parser_correction_base_equality(A.REVIEWED_BASE_SHA, bad, True)

    def test_ancestry_remains_necessary(self):
        errors = A._verify_post_parser_correction_base_equality(
            A.REVIEWED_BASE_SHA, A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA, False
        )
        assert any("ancestry remains NECESSARY" in e for e in errors), errors

    def test_an_unresolvable_ancestry_answer_is_not_itself_a_failure(self):
        assert A._verify_post_parser_correction_base_equality(
            A.REVIEWED_BASE_SHA, A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA, None
        ) == []

    def test_the_rule_reads_no_external_source(self):
        tree = ast.parse((ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8"))
        fn = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef)
            and n.name == "_verify_post_parser_correction_base_equality"
        )
        called = {
            node.func.attr for node in ast.walk(fn)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        for forbidden in ("run", "is_ancestor", "commit_parents", "now", "utcnow", "get"):
            assert forbidden not in called, forbidden

    def test_the_rule_takes_its_inputs_as_parameters_not_module_globals(self):
        """MUTATION PIN. A rule reading the globals directly could not be driven against a
        known-bad input at all, so every negative test above would be unwritable."""
        tree = ast.parse((ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8"))
        fn = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef)
            and n.name == "_verify_post_parser_correction_base_equality"
        )
        names = [a.arg for a in fn.args.args]
        assert names == [
            "reviewed_base", "implementation_merge", "descends_from_implementation_merge"
        ], names
        loaded = {
            n.id for n in ast.walk(fn) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
        }
        assert "REVIEWED_BASE_SHA" not in loaded
        assert "PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA" not in loaded

    def test_the_predecessor_rule_is_retained_unchanged_and_still_exercised(self):
        """§F.2's replacement must not silently delete the rule it replaced: `XASSET-0048`'s own
        proposition is still decided, still by its own function, for its own commits."""
        assert A._verify_step8_equivalent_base_equality(
            A.PRIOR_STEP8_EQUIVALENT_MERGE_BASE,
            A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA,
            True,
        ) == []
        # And it is a genuinely DIFFERENT function, not an alias.
        assert (
            A._verify_step8_equivalent_base_equality
            is not A._verify_post_parser_correction_base_equality
        )

    def test_the_new_rule_is_the_one_the_verifier_actually_calls(self):
        """A replacement nothing calls replaces nothing. Proved from the caller's own AST."""
        tree = ast.parse((ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8"))
        caller = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "_verify_successor_rebinding_identity"
        )
        called = {
            node.func.id for node in ast.walk(caller)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        assert "_verify_post_parser_correction_base_equality" in called
        assert "_verify_step8_equivalent_base_equality" not in called


# ======================================================================================
# 4 -- Both prerequisite lifecycles really closed
# ======================================================================================


class TestBothPrerequisiteLifecyclesReallyClosed:
    """``XASSET-0057`` §F.0.3: **merged is not effective**, and TWO lifecycles must close.

    That section is not abstract caution. ``XASSET-0044`` and ``XASSET-0045`` each merged and
    neither became effective, because merge-commit CI failed at the exact merge SHA their own
    effectivity conditions named. §F.0.3 therefore lists the failure modes explicitly, and each
    is checked here against the object store rather than against a summary.
    """

    @pytest.mark.parametrize(
        "label,merge,base,head,tree",
        [
            ("XASSET-0057 / PR #358", PR358_MERGE_SHA, PR358_BASE_SHA,
             PR358_ACCEPTED_HEAD, PR358_MERGE_TREE),
            ("XASSET-0058 / PR #359 (Lifecycle A)", PR359_MERGE_SHA, PR359_BASE_SHA,
             PR359_ACCEPTED_HEAD, PR359_MERGE_TREE),
            ("XASSET-0059 / PR #360 (Lifecycle B)", PR360_MERGE_SHA, PR360_BASE_SHA,
             PR360_ACCEPTED_HEAD, PR360_MERGE_TREE),
        ],
    )
    def test_each_prerequisite_merge_has_ordered_parents_and_zero_drift(
        self, label, merge, base, head, tree
    ):
        if not _range_is_present(merge, base, head):
            pytest.skip(f"{label}'s closed range is not present in this checkout")
        assert _commit_exists(merge), label
        assert _git("log", "-1", "--pretty=%P", merge).split() == [base, head], label
        assert _git("rev-parse", f"{merge}^{{tree}}") == tree, label
        assert _git("rev-parse", f"{head}^{{tree}}") == tree, label

    def test_the_chain_is_ordered_and_unbroken(self):
        """§F.2 fixes the ordering exactly: this decision's merge -> Lifecycle A -> Lifecycle B
        -> this unit's base. Each link proved by ancestry, not asserted."""
        chain = [PR358_MERGE_SHA, PR359_MERGE_SHA, PR360_MERGE_SHA]
        if not _range_is_present(*chain):
            pytest.skip("the prerequisite chain is not present in this checkout")
        for earlier, later in zip(chain, chain[1:]):
            assert _git("merge-base", "--is-ancestor", earlier, later) == ""
        # And each merge's own base is the previous merge -- a chain, not merely a partial order.
        assert PR359_BASE_SHA == PR358_MERGE_SHA
        assert PR360_BASE_SHA == PR359_MERGE_SHA
        assert THIS_UNIT_BASE_SHA == PR360_MERGE_SHA

    def test_the_module_binds_all_three_prerequisite_identities(self):
        assert A.POST_PARSER_CORRECTION_AUTHORIZING_DECISION == "XASSET-0057"
        assert A.POST_PARSER_CORRECTION_AUTHORIZING_PULL_REQUEST == 358
        assert A.PARSER_CORRECTION_AUTHORIZING_DECISION == "XASSET-0058"
        assert A.PARSER_CORRECTION_AUTHORIZING_PULL_REQUEST == 359
        assert A.PARSER_CORRECTION_IMPLEMENTATION_DECISION == "XASSET-0059"
        assert A.PARSER_CORRECTION_IMPLEMENTATION_PULL_REQUEST == 360

    def test_the_three_prerequisite_families_are_structurally_distinct(self):
        """§C's failure mode: overloading one identity across relationships that are not the same
        relationship. Authority over a unit and the unit's own merged tree differ."""
        merges = {
            A.POST_PARSER_CORRECTION_AUTHORIZING_MERGE_SHA,
            A.PARSER_CORRECTION_AUTHORIZING_MERGE_SHA,
            A.PARSER_CORRECTION_IMPLEMENTATION_MERGE_SHA,
            A.PRIOR_STEP8_EQUIVALENT_MERGE_SHA,
            A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA,
        }
        assert len(merges) == 5, merges

    def test_the_decision_records_the_b7_ci_evidence_naming_the_exact_merge_sha(
        self, decision_flat
    ):
        """§F.2 requires the base, the SHA tested by B7, and the SHA named by B8 to be the SAME
        commit, and requires THIS unit to prove it."""
        assert PR360_MERGE_CI_RUN in decision_flat
        assert PR360_MERGE_CI_JOB in decision_flat
        assert PR360_FINAL_CLOSURE in decision_flat
        assert PR360_MERGE_SHA in decision_flat
        assert A.REVIEWED_BASE_SHA == PR360_MERGE_SHA

    def test_the_two_permanently_ineffective_decisions_are_still_refused(self):
        """§F.10, and the reason §F.0.3 exists at all."""
        assert "XASSET-0044" in A.PERMANENTLY_INEFFECTIVE_DECISIONS
        assert "XASSET-0045" in A.PERMANENTLY_INEFFECTIVE_DECISIONS
        assert A.AUTHORIZING_DECISION not in A.PERMANENTLY_INEFFECTIVE_DECISIONS
        assert A.PARSER_CORRECTION_IMPLEMENTATION_DECISION not in (
            A.PERMANENTLY_INEFFECTIVE_DECISIONS
        )


# ======================================================================================
# 5 -- Exact closed transitions, bound at BOTH ends
# ======================================================================================


class TestExactClosedTransitions:
    """``XASSET-0057`` §F.3: old value and new value, both explicit, the old one PRESERVED.

    "A value that moves without both ends bound is drift wearing a rebinding's label."
    """

    def test_the_anchor_decision_moved_and_both_ends_are_bound(self):
        assert A.AUTHORIZING_DECISION == DECISION_ID
        assert A.AUTHORIZING_DECISION != "XASSET-0049"
        assert A.PRIOR_STEP8_EQUIVALENT_DECISION == "XASSET-0049"

    def test_the_anchor_pull_request_moved_and_both_ends_are_bound(self):
        assert A.AUTHORIZING_PULL_REQUEST == THIS_PULL_REQUEST
        assert A.AUTHORIZING_PULL_REQUEST != 349
        assert A.PRIOR_STEP8_EQUIVALENT_PULL_REQUEST == 349

    def test_the_reviewed_base_moved_and_both_ends_are_bound(self):
        assert A.REVIEWED_BASE_SHA == THIS_UNIT_BASE_SHA
        assert A.REVIEWED_BASE_SHA != PR349_MERGE_BASE
        # PRESERVED TWICE, deliberately: the old value remains reachable from two constants.
        assert A.PRIOR_STEP8_EQUIVALENT_MERGE_BASE == PR349_MERGE_BASE
        assert A.STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA == PR349_MERGE_BASE

    def test_the_prior_anchor_family_is_complete_and_derived(self):
        """§F.3 requires the OLD value preserved, not merely referenced. Reproduced against this
        unit's base, exactly as `XASSET-0049` reproduced it for `XASSET-0047`: `XASSET-0049`'s own
        merge and accepted head appeared under NO constant, so moving the three fields without
        this family would have DESTROYED that identity rather than weakened it."""
        assert A.PRIOR_STEP8_EQUIVALENT_MERGE_SHA == PR349_MERGE_SHA
        assert A.PRIOR_STEP8_EQUIVALENT_ACCEPTED_HEAD == PR349_ACCEPTED_HEAD
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        source = _git("show", f"{THIS_UNIT_BASE_SHA}:{AUTH_MODULE_RELPATH}")
        assert PR349_MERGE_SHA not in source, (
            "if it were already reachable at the base, this family would be decorative"
        )
        assert PR349_ACCEPTED_HEAD not in source
        # ... and it is reachable NOW.
        live = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert PR349_MERGE_SHA in live
        assert PR349_ACCEPTED_HEAD in live

    def test_no_moved_value_lost_its_old_end(self):
        """The single invariant §F.3 reduces to, asserted directly over all three."""
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        for name in ("AUTHORIZING_DECISION", "AUTHORIZING_PULL_REQUEST", "REVIEWED_BASE_SHA"):
            old = _module_constant_at(THIS_UNIT_BASE_SHA, name)
            new = getattr(A, name)
            assert old != new, f"{name} did not move"
            assert str(old) in (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8"), (
                f"{name}'s old value {old!r} is no longer reachable from the module"
            )


# ======================================================================================
# 6 -- The trust boundary grew additively, 18 -> 25
# ======================================================================================


class TestTrustBoundaryGrewAdditively:
    """``XASSET-0057`` §F.7: extension only, count DERIVED rather than guessed."""

    def test_the_set_grew_from_eighteen_to_twenty_five(self):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        at_base = _load_bearing_declared_at(THIS_UNIT_BASE_SHA)
        assert len(at_base) == LOAD_BEARING_COUNT_AT_BASE
        assert len(A.LOAD_BEARING_RELPATHS) == LOAD_BEARING_COUNT_NOW
        assert len(set(A.LOAD_BEARING_RELPATHS)) == LOAD_BEARING_COUNT_NOW
        assert len(A.LOAD_BEARING_RELPATHS) != LOAD_BEARING_COUNT_AT_BASE

    def test_the_count_is_derived_from_the_actual_chain_not_stated_in_the_grant(
        self, decision_flat
    ):
        """§F.7 "deliberately states NO predicted final membership figure". A unit that read a
        number out of its own authority would be inventing it."""
        authority = _flat((ROOT / AUTHORITY_RELPATH).read_text(encoding="utf-8"))
        assert "The final count is derived, never guessed." in authority
        assert "predicted final membership figure" in authority
        assert "derive the exact final count" in authority
        # This unit states a figure, because this unit DERIVED one.
        assert "eighteen to twenty-five" in decision_flat.lower()
        assert str(LOAD_BEARING_COUNT_NOW) in decision_flat

    def test_nothing_was_removed_reordered_or_traded_away(self):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        at_base = _load_bearing_declared_at(THIS_UNIT_BASE_SHA)
        live = tuple(A.LOAD_BEARING_RELPATHS)
        # ORDERED PREFIX -- strictly stronger than a subset test, which a reorder would satisfy.
        assert live[:len(at_base)] == at_base
        assert set(at_base) <= set(live)

    def test_the_additions_are_exactly_the_seven_governing_decisions(self):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        at_base = _load_bearing_declared_at(THIS_UNIT_BASE_SHA)
        additions = set(A.LOAD_BEARING_RELPATHS) - set(at_base)
        assert len(additions) == 7
        for decision_id in ADDED_DECISION_IDS:
            matching = [p for p in additions if decision_id in p]
            assert len(matching) == 1, decision_id

    def test_every_addition_is_a_real_file_bound_by_membership_not_citation(self):
        """§F.7: "Citation is not membership." Only a path in the tuple is inside the boundary."""
        for decision_id in ADDED_DECISION_IDS:
            path = next(p for p in A.LOAD_BEARING_RELPATHS if decision_id in p)
            assert (ROOT / path).is_file(), path

    def test_the_gap_this_extension_closes_was_real_at_the_base(self):
        """Non-vacuity: §F.7 reproduced these as ABSENT, and so does this."""
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        at_base = _load_bearing_declared_at(THIS_UNIT_BASE_SHA)
        for decision_id in ADDED_DECISION_IDS:
            assert not [p for p in at_base if decision_id in p], decision_id

    def test_xasset_0054_remains_excluded_on_evidence_not_on_narrative(self):
        """§F.7 permits admission ONLY on independent evidence that it is operative, "never on
        the strength of appearing in a narrative, a related-decisions list, or this enumeration".
        The evidence is checked here rather than the exclusion being asserted."""
        assert not [p for p in A.LOAD_BEARING_RELPATHS if "XASSET-0054" in p]
        # No decision file exists for it anywhere on the merged tree.
        matches = list((ROOT / "governance" / "decisions").glob("XASSET-0054-*.md"))
        assert matches == [], matches
        if _commit_exists(THIS_UNIT_BASE_SHA):
            listing = subprocess.run(
                ["git", "ls-tree", "--name-only", f"{THIS_UNIT_BASE_SHA}:governance/decisions"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout
            assert "XASSET-0054" not in listing
        # And it is not in the catalog either.
        catalog = yaml.safe_load((ROOT / CATALOG_RELPATH).read_text(encoding="utf-8"))
        assert "XASSET-0054" not in {d["decision_id"] for d in catalog["decisions"]}

    def test_xasset_0045_remains_excluded_because_it_authorizes_nothing(self):
        assert not [p for p in A.LOAD_BEARING_RELPATHS if "XASSET-0045" in p]

    def test_every_bound_path_exists_and_the_tuple_is_unique(self):
        assert len(set(A.LOAD_BEARING_RELPATHS)) == len(A.LOAD_BEARING_RELPATHS)
        for relpath in A.LOAD_BEARING_RELPATHS:
            assert (ROOT / relpath).exists(), relpath


# ======================================================================================
# 7 -- Meaning did not move under cover of a byte-binding
# ======================================================================================


class TestTheOutcomeSurfaceIsUnchanged:
    """``XASSET-0057`` §F.5: "The rebinding binds bytes; it does not get to move meaning." """

    OUTCOME_SURFACE = (
        "level1_stage1_runner.py",
        "level1_stage1_result_validator.py",
        "level1_construction_universe_closure_validator.py",
        "level1_endpoint_evidence_preregistration_validator.py",
    )
    PROTECTED = (
        "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
        "allocate.py", "margin_state.py", "levels.py",
    )

    @pytest.mark.parametrize("relpath", OUTCOME_SURFACE + PROTECTED)
    def test_no_outcome_or_protected_path_changed_against_the_base(self, relpath):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        at_base = _blob_at(THIS_UNIT_BASE_SHA, relpath)
        assert at_base is not None, relpath
        assert _git("hash-object", relpath) == at_base, relpath

    def test_the_only_load_bearing_path_this_unit_changed_is_the_module_itself(self):
        """Every load-bearing path except the module and this unit's own seven additions must be
        byte-identical to the base. The additions are new FILES, not edits, proved separately."""
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        at_base = set(_load_bearing_declared_at(THIS_UNIT_BASE_SHA))
        changed = []
        for relative in A.LOAD_BEARING_RELPATHS:
            if relative == AUTH_MODULE_RELPATH or relative not in at_base:
                continue
            base_blob = _blob_at(THIS_UNIT_BASE_SHA, relative)
            assert base_blob is not None, relative
            if _git("hash-object", relative) != base_blob:
                changed.append(relative)
        assert changed == [], changed

    def test_the_six_predecessor_decision_files_this_unit_bound_are_unedited(self):
        """Binding a decision must not become licence to edit it. Six of the seven additions
        already existed at the base and must be byte-identical to it."""
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        for decision_id in ADDED_DECISION_IDS:
            if decision_id == DECISION_ID:
                continue  # this unit's own file did not exist at the base
            path = next(p for p in A.LOAD_BEARING_RELPATHS if decision_id in p)
            base_blob = _blob_at(THIS_UNIT_BASE_SHA, path)
            assert base_blob is not None, path
            assert _git("hash-object", path) == base_blob, path

    def test_this_units_own_decision_file_did_not_exist_at_the_base(self):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        assert _blob_at(THIS_UNIT_BASE_SHA, DECISION_RELPATH) is None

    def test_the_universe_and_its_cardinalities_are_unchanged(self):
        assert A.CONSTRUCTION_UNIVERSE_SHA256 == (
            _module_constant_at(THIS_UNIT_BASE_SHA, "CONSTRUCTION_UNIVERSE_SHA256")
            if _commit_exists(THIS_UNIT_BASE_SHA)
            else A.CONSTRUCTION_UNIVERSE_SHA256
        )
        pre = yaml.safe_load(
            (ROOT / A.CANONICAL_PREREGISTRATION_RELPATH).read_text(encoding="utf-8")
        )
        assert pre["stage_1_executability"]["executable"] is False

    def test_the_required_lifecycle_gates_are_the_committed_six(self):
        assert len(A.REQUIRED_LIFECYCLE_GATES) == 6
        assert A.REQUIRED_LIFECYCLE_GATES == (
            "INDEPENDENT_FULL_EXACT_HEAD_REVIEW",
            "PRINCIPAL_EXACT_HEAD_ACCEPTANCE",
            "MERGE",
            "POST_MERGE_VERIFICATION",
            "MERGE_COMMIT_CI_SUCCESS",
            "MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION",
        )


class TestCanonicalArtifactsAreUnamended:
    """``XASSET-0057`` §F.8 permits amendment "only to the extent the rebinding requires", and
    §F.4 requires the SMALLEST strictly necessary rebinding. This unit determined expressly that
    it requires none -- the same determination `XASSET-0047` and `XASSET-0049` each reached."""

    @pytest.mark.parametrize(
        "relpath",
        ["research/level1_endpoint_evidence/PROTOCOL_V1.md",
         "research/level1_endpoint_evidence/pre_registration.yaml"],
    )
    def test_the_canonical_artifact_is_byte_identical_to_the_base(self, relpath):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        assert _git("hash-object", relpath) == _blob_at(THIS_UNIT_BASE_SHA, relpath), relpath

    def test_the_canonical_artifacts_carry_none_of_the_moved_values(self):
        """The determination is not merely asserted: the reason it is lawful is that nothing in
        them names any of the three constants this unit moved."""
        for relpath in ("research/level1_endpoint_evidence/PROTOCOL_V1.md",
                        "research/level1_endpoint_evidence/pre_registration.yaml"):
            text = (ROOT / relpath).read_text(encoding="utf-8")
            assert "XASSET-0049" not in text, relpath
            assert PR349_MERGE_BASE not in text, relpath
            assert DECISION_ID not in text, relpath

    def test_rebound_by_still_names_xasset_0044_and_that_is_still_true(self):
        """`XASSET-0044` remains the last decision that amended the canonical BYTES, and this
        unit amends none of them, so the field is literally correct rather than stale."""
        pre = yaml.safe_load(
            (ROOT / A.CANONICAL_PREREGISTRATION_RELPATH).read_text(encoding="utf-8")
        )
        block = pre["load_bearing_identity"] if "load_bearing_identity" in pre else pre
        text = (ROOT / A.CANONICAL_PREREGISTRATION_RELPATH).read_text(encoding="utf-8")
        assert "rebound_by: XASSET-0044" in text
        assert "effective_structural_authorization_source: XASSET-0044" in text
        assert isinstance(block, dict)

    def test_the_decision_makes_this_an_express_determination(self, decision_flat):
        assert "canonical artifacts are not amended by this unit" in decision_flat.lower()
        assert "remains literally true" in decision_flat.lower()


# ======================================================================================
# 8 -- The new refusals are independently required
# ======================================================================================


class TestTheNewRefusalsAreIndependentlyRequired:
    """Each closes a class the anchor move newly opens, and each is a REFUSAL, not a comment."""

    def test_the_superseded_anchor_may_not_silently_remain_the_anchor(self):
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert "if AUTHORIZING_DECISION == PRIOR_STEP8_EQUIVALENT_DECISION:" in source
        assert "if AUTHORIZING_PULL_REQUEST == PRIOR_STEP8_EQUIVALENT_PULL_REQUEST:" in source
        # ... and the live anchor genuinely is not the predecessor.
        assert A.AUTHORIZING_DECISION != A.PRIOR_STEP8_EQUIVALENT_DECISION
        assert A.AUTHORIZING_PULL_REQUEST != A.PRIOR_STEP8_EQUIVALENT_PULL_REQUEST

    def test_the_authority_may_not_be_mistaken_for_the_unit(self):
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert (
            "if AUTHORIZING_DECISION == POST_PARSER_CORRECTION_AUTHORIZING_DECISION:" in source
        )
        assert (
            "if AUTHORIZING_PULL_REQUEST == POST_PARSER_CORRECTION_AUTHORIZING_PULL_REQUEST:"
            in source
        )
        assert A.AUTHORIZING_DECISION != A.POST_PARSER_CORRECTION_AUTHORIZING_DECISION
        assert A.AUTHORIZING_PULL_REQUEST != A.POST_PARSER_CORRECTION_AUTHORIZING_PULL_REQUEST

    def test_neither_prerequisite_lifecycle_may_be_mistaken_for_this_unit(self):
        """§G forbids this unit from correcting the parser; an anchor naming either lifecycle
        would claim `XASSET-0058`/`XASSET-0059`'s work as this rebinding's own."""
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert "PARSER_CORRECTION_AUTHORIZING_DECISION," in source
        assert "PARSER_CORRECTION_IMPLEMENTATION_DECISION," in source
        assert A.AUTHORIZING_DECISION != A.PARSER_CORRECTION_AUTHORIZING_DECISION
        assert A.AUTHORIZING_DECISION != A.PARSER_CORRECTION_IMPLEMENTATION_DECISION
        assert A.AUTHORIZING_PULL_REQUEST != A.PARSER_CORRECTION_AUTHORIZING_PULL_REQUEST
        assert A.AUTHORIZING_PULL_REQUEST != A.PARSER_CORRECTION_IMPLEMENTATION_PULL_REQUEST

    def test_the_predecessor_refusals_are_retained_not_replaced(self):
        """Refusals 5 and 6 still name `XASSET-0047` and `XASSET-0048`. They are not weakened;
        they simply no longer describe the live pair, which is why 7-9 were added beside them."""
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert "if AUTHORIZING_DECISION == PRIOR_RECONCILIATION_DECISION:" in source
        assert "if AUTHORIZING_DECISION == STEP8_EQUIVALENT_AUTHORIZING_DECISION:" in source

    def test_the_module_never_names_this_decision_as_a_predecessor_constant(self):
        """This unit is the ANCHOR, never a preserved predecessor of itself."""
        assert A.PRIOR_STEP8_EQUIVALENT_DECISION != DECISION_ID
        assert A.PRIOR_RECONCILIATION_DECISION != DECISION_ID
        assert A.POST_PARSER_CORRECTION_AUTHORIZING_DECISION != DECISION_ID
        assert A.PARSER_CORRECTION_AUTHORIZING_DECISION != DECISION_ID
        assert A.PARSER_CORRECTION_IMPLEMENTATION_DECISION != DECISION_ID


# ======================================================================================
# 9 -- Nothing is armed, claimed, or executed
# ======================================================================================


class TestNothingIsArmed:
    """``XASSET-0057`` §G and §L, and ``XASSET-0060`` §K and §N.

    Reconciling the register removes a STALE-DIGEST refusal. It must not remove any other, and it
    must not create authority. Every predicate is still false on its own terms.
    """

    def test_all_three_authorization_predicates_are_false(self):
        for fn in (
            A.new_execution_is_authorized,
            A.active_execution_is_authorized,
            A.claimed_execution_is_authorized,
        ):
            authorized, reason = fn()
            assert authorized is False, fn.__name__
            assert isinstance(reason, str) and reason.strip(), fn.__name__

    def test_the_lane_is_absent_and_no_authorization_root_exists(self):
        assert not A.AUTHORIZATION_ROOT.exists()
        assert not A.AUTHORIZATION_PATH.exists()

    def test_attempt_one_is_intact_unclaimed_and_unconsumed(self):
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"
        assert not A.AUTHORIZATION_ROOT.exists()

    def test_no_results_artifact_exists_anywhere(self):
        assert not (ROOT / "stage1_results.yaml").exists()
        assert list(ROOT.glob("**/stage1_results.yaml")) == []

    def test_stage_1_executability_is_still_false(self):
        pre = yaml.safe_load(
            (ROOT / A.CANONICAL_PREREGISTRATION_RELPATH).read_text(encoding="utf-8")
        )
        assert pre["stage_1_executability"]["executable"] is False

    def test_this_suite_imports_no_outcome_producing_module(self):
        """A suite that imported the runner could produce an outcome by accident."""
        source = SUITE_PATH.read_text(encoding="utf-8")
        for forbidden in ("level1_stage1_runner", "level1_stage1_result_validator",
                          "level1_construction_universe_closure_validator"):
            assert f"import {forbidden}" not in source, forbidden

    def test_this_suite_reads_no_protected_risk_result(self):
        """The operative property, stated so a self-referential string search cannot fake it.

        Naming the boundary in prose is exactly what §L requires a filing to do; READING a
        protected result is what it forbids. A plain substring scan cannot tell those apart --
        it matches its own needle list -- so the scan is done over the suite's PARSED string
        constants with THIS function's own subtree excluded. What remains is every literal the
        suite could actually use as a path, and none of them points into a protected area.
        """
        source = SUITE_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        this_fn = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef)
            and n.name == "test_this_suite_reads_no_protected_risk_result"
        )
        own = {id(n) for n in ast.walk(this_fn)}
        # DOCSTRINGS are prose, and §L positively REQUIRES a filing to name the boundary in
        # prose. Excluding them is what makes this a check about PATHS rather than about words.
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                body = getattr(node, "body", None)
                if (
                    body
                    and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)
                ):
                    docstrings.add(id(body[0].value))
        literals = [
            n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant)
            and isinstance(n.value, str)
            and id(n) not in own
            and id(n) not in docstrings
        ]
        assert literals, "the exclusion must not empty the scanned set"
        forbidden = ("untouched_sealed", "risk_lane_boundary", "margin_target_study",
                     "RISK-0001")
        for literal in literals:
            for needle in forbidden:
                assert needle not in literal, (needle, literal[:80])
        # ... and nothing capable of producing or reading an outcome is imported.
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.add((node.module or "").split(".")[0])
        assert imported <= {
            "__future__", "ast", "re", "subprocess", "pathlib", "pytest", "yaml", "hashlib",
            "level1_stage1_execution_authorization",
        }, imported

    def test_the_decision_withholds_every_downstream_link(self, decision_flat):
        for phrase in (
            "renewed readiness verification",
            "renewed drift verification",
            "attestation",
            "claim",
            "Stage 1 remains UNARMED and NOT EXECUTABLE",
        ):
            assert phrase.lower() in decision_flat.lower(), phrase

    def test_the_decision_does_not_consume_the_reserved_results_pull_request(self, decision_flat):
        assert "not consumed, replaced, or counted against" in decision_flat
        assert "reserved and unspent" in decision_flat


# ======================================================================================
# 10 -- Catalog, register, and the pull-request number
# ======================================================================================


class TestCatalogAndRegisterSynchronisation:
    def test_the_catalog_lists_this_decision_once_last_and_completely(self, catalog):
        ids = [d["decision_id"] for d in catalog["decisions"]]
        assert ids.count(DECISION_ID) == 1
        assert len(ids) == len(set(ids))
        assert ids[len(ids) - 1 - len(SUCCESSORS_APPENDED_SINCE)] == DECISION_ID
        assert list(ids[len(ids) - len(SUCCESSORS_APPENDED_SINCE):]) == list(
            SUCCESSORS_APPENDED_SINCE
        )
        entry = next(d for d in catalog["decisions"] if d["decision_id"] == DECISION_ID)
        assert entry["file"] == DECISION_RELPATH
        assert (ROOT / entry["file"]).exists()
        assert entry["status"] == "Proposed"
        assert entry["supporting_artifact"] == SUITE_PATH.name

    def test_the_catalog_gained_exactly_one_entry(self, catalog):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        before = yaml.safe_load(
            _git("show", f"{THIS_UNIT_BASE_SHA}:{CATALOG_RELPATH}")
        )["decisions"]
        assert len(catalog["decisions"]) == len(before) + 1 + len(SUCCESSORS_APPENDED_SINCE)
        assert DECISION_ID not in {d["decision_id"] for d in before}

    def test_the_register_gained_exactly_two_gates_and_rewrote_none(self, ws0014):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        before = yaml.safe_load(
            _git("show", f"{THIS_UNIT_BASE_SHA}:{REGISTER_RELPATH}")
        )
        before_ws = next(w for w in before["workstreams"] if w["id"] == "WS-0014")
        assert ws0014["milestones"][: len(before_ws["milestones"])] == before_ws["milestones"]
        assert (
            len(ws0014["milestones"])
            == len(before_ws["milestones"]) + 2 + SUCCESSOR_GATES_ADDED_SINCE
        )

    def test_this_units_gate_is_in_progress_not_complete(self, ws0014):
        """A unit does not mark its own unmerged work complete."""
        gate = next(g for g in ws0014["milestones"] if g["gate"] == REGISTER_GATE)
        assert gate["status"] == "in_progress"

    def test_the_prior_units_post_merge_gate_records_the_confirmed_facts(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == PRIOR_UNIT_GATE)
        assert gate["status"] == "complete"
        assert gate["pr"] == 360
        for token in (PR360_MERGE_SHA, PR360_MERGE_CI_RUN, PR360_MERGE_CI_JOB,
                      PR360_ACCEPTED_HEAD, PR360_FINAL_CLOSURE):
            assert token in gate["description"], token

    def test_the_shared_live_fields_name_this_unit(self, ws0014):
        # ADVANCED BY XASSET-0061: the shared live field moved onto the successor; this
        # unit's own branch is retained as a NEGATIVE pin. Its durable anchor is its GATE.
        assert ws0014["active_branch"] == SUCCESSOR_BRANCH_NAME
        assert ws0014["active_branch"] != "claude/xasset-0057-rebinding-gqtg9o"
        # ADVANCED BY XASSET-0061: WS-0014's single shared live field lawfully moved onto
        # the successor. This unit's own base is RETAINED as a NEGATIVE pin -- never
        # deleted -- so the field stays bound at BOTH ends.
        assert ws0014["last_verified_main_sha"] == SUCCESSOR_MAIN_SHA_VALUE
        assert ws0014["last_verified_main_sha"] != THIS_UNIT_BASE_SHA
        # Every prior generation stays a NEGATIVE pin.
        assert ws0014["last_verified_main_sha"] != PR359_MERGE_SHA
        assert ws0014["last_verified_main_sha"] != PR358_MERGE_SHA
        assert ws0014["active_branch"] != "claude/xasset-0058-parser-correction-a2kteq"

    def test_the_workstream_posture_is_unchanged(self, ws0014):
        assert ws0014["status"] == "proposed"
        assert ws0014["priority"] == "secondary"

    def test_exactly_zero_primary_workstreams(self):
        register = yaml.safe_load((ROOT / REGISTER_RELPATH).read_text(encoding="utf-8"))
        assert [w["id"] for w in register["workstreams"] if w.get("priority") == "primary"] == []


class TestTheBoundPullRequestNumber:
    """``XASSET-0057`` §E.2 / §F.1: the number is READ BACK from GitHub, never predicted."""

    def test_the_module_binds_the_number_github_actually_issued(self, ws0014):
        assert A.AUTHORIZING_PULL_REQUEST == THIS_PULL_REQUEST
        assert A.AUTHORIZING_PULL_REQUEST > 0
        gate = next(g for g in ws0014["milestones"] if g["gate"] == REGISTER_GATE)
        assert gate["pr"] == THIS_PULL_REQUEST
        # ADVANCED BY XASSET-0061. What this protects -- that THIS unit bound the number
        # GitHub really issued -- is immutable history and is asserted against this unit's
        # OWN gate, which does not move.
        assert ws0014["active_pr"] == SUCCESSOR_ACTIVE_PR
        assert ws0014["active_pr"] != THIS_PULL_REQUEST
        assert any(
            g.get("pr") == THIS_PULL_REQUEST for g in ws0014["milestones"]
        ), "this unit's own gate must still carry its real number"

    def test_the_sentinel_was_replaced_and_is_structurally_impossible(self):
        assert PULL_REQUEST_SENTINEL < 0
        assert A.AUTHORIZING_PULL_REQUEST != PULL_REQUEST_SENTINEL
        source = (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")
        assert f"AUTHORIZING_PULL_REQUEST = {PULL_REQUEST_SENTINEL}" not in source

    def test_the_sentinel_is_distinct_from_every_predecessors(self):
        assert PULL_REQUEST_SENTINEL not in (0, -1, -2)

    def test_it_is_a_later_pull_request_than_every_predecessor_in_the_chain(self):
        for predecessor in (349, 358, 359, 360):
            assert A.AUTHORIZING_PULL_REQUEST > predecessor, predecessor


# ======================================================================================
# 11 -- Non-vacuity: every re-anchored claim FAILED at this unit's own base
# ======================================================================================


class TestNonVacuityAgainstTheBase:
    """A guard against a suite that would pass identically before this filing existed."""

    def test_the_decision_file_did_not_exist_at_the_base(self):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        assert _blob_at(THIS_UNIT_BASE_SHA, DECISION_RELPATH) is None
        assert _blob_at(THIS_UNIT_BASE_SHA, SUITE_PATH.name) is None

    def test_the_decision_id_appears_nowhere_at_the_base(self):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        result = subprocess.run(
            ["git", "grep", "-l", DECISION_ID, THIS_UNIT_BASE_SHA],
            cwd=ROOT, capture_output=True, text=True,
        )
        assert result.returncode != 0, result.stdout

    def test_every_moved_constant_held_a_different_value_at_the_base(self):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        assert _module_constant_at(THIS_UNIT_BASE_SHA, "AUTHORIZING_DECISION") == "XASSET-0049"
        assert _module_constant_at(THIS_UNIT_BASE_SHA, "AUTHORIZING_PULL_REQUEST") == 349
        assert _module_constant_at(THIS_UNIT_BASE_SHA, "REVIEWED_BASE_SHA") == PR349_MERGE_BASE

    def test_the_new_verifiers_did_not_exist_at_the_base(self):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        source = _git("show", f"{THIS_UNIT_BASE_SHA}:{AUTH_MODULE_RELPATH}")
        assert "_verify_post_parser_correction_base_equality" not in source
        assert "_verify_module_identity_is_not_the_vulnerable_intermediate" not in source
        assert "NEVER_BINDABLE_MODULE_SHA256" not in source

    def test_the_negative_pin_would_not_have_fired_at_the_base(self):
        """The refusal is new. Before it, binding the vulnerable module was structurally
        possible -- which is precisely what §F.0 refused and what this unit implements."""
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        source = _git("show", f"{THIS_UNIT_BASE_SHA}:{AUTH_MODULE_RELPATH}")
        assert ROLE2_SHA256 not in source
        assert ROLE2_SHA256 in (ROOT / AUTH_MODULE_RELPATH).read_text(encoding="utf-8")

    def test_the_seven_additions_were_absent_from_the_boundary_at_the_base(self):
        if not _commit_exists(THIS_UNIT_BASE_SHA):
            pytest.skip("this unit's base is not present in this checkout")
        at_base = _load_bearing_declared_at(THIS_UNIT_BASE_SHA)
        assert len(at_base) == LOAD_BEARING_COUNT_AT_BASE
        for decision_id in ADDED_DECISION_IDS:
            assert not [p for p in at_base if decision_id in p], decision_id


# ======================================================================================
# 12 -- The decision record says what the module does
# ======================================================================================


class TestTheDecisionAndTheModuleAgree:
    def test_the_decision_names_its_own_authority_and_not_another(self, decision_flat):
        assert "XASSET-0057" in decision_flat
        assert A.POST_PARSER_CORRECTION_AUTHORIZING_DECISION == "XASSET-0057"

    def test_the_decision_records_the_four_role_chain_with_every_derived_value(
        self, decision_text
    ):
        for value in (ROLE1_SHA256, ROLE1_BLOB, ROLE2_SHA256, ROLE2_BLOB,
                      ROLE3_SHA256, ROLE3_BLOB, ROLE4_SHA256, ROLE4_BLOB):
            assert value in decision_text, value

    def test_the_decision_records_the_exact_closed_transitions(self, decision_text):
        for value in ("XASSET-0049", "349", PR349_MERGE_BASE,
                      DECISION_ID, THIS_UNIT_BASE_SHA, str(THIS_PULL_REQUEST)):
            assert value in decision_text, value

    def test_the_decision_records_both_prerequisite_lifecycles_in_full(self, decision_flat):
        for token in (
            PR358_FINAL_CLOSURE, PR358_MERGE_CI_RUN,
            PR359_FINAL_CLOSURE, PR359_MERGE_CI_RUN,
            PR360_FINAL_CLOSURE, PR360_MERGE_CI_RUN, PR360_MERGE_CI_JOB,
        ):
            assert token in decision_flat, token

    def test_the_decision_states_the_seven_condition_effectivity_in_full(self, decision_flat):
        for phrase in (
            "independent",
            "principal exact-head acceptance",
            "normal merge",
            "immediate post-merge verification",
            "successful merge-commit CI whose",
            "final post-CI verification and lifecycle closure",
            "None is individually sufficient",
        ):
            assert phrase.lower() in decision_flat.lower(), phrase

    def test_the_decision_is_marked_proposed_not_accepted(self, decision_text):
        front = decision_text.split("---")[1]
        meta = yaml.safe_load(front)
        assert meta["decision_id"] == DECISION_ID
        assert meta["status"] == "Proposed"
        assert meta["supporting_artifact"] == SUITE_PATH.name
