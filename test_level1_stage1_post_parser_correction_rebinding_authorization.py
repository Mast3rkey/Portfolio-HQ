"""Supporting artifact for ``XASSET-0057``.

``XASSET-0057`` is a **design-only Lane G governance authorization**. It grants authority for
exactly one future, separate step-8-equivalent rebinding unit and **performs no rebinding**.

This module proves that claim mechanically rather than by assertion. Every historical fact is
proved over an **immutable commit range** — this unit's own base and its ancestors — so the suite
does not depend on any moving ref, and it keeps passing at a merged-``main`` state where ``HEAD``
equals ``origin/main``.

The suite deliberately proves four different kinds of thing:

* that the authority this filing rests on is **real and closed** (the ``XASSET-0056`` lifecycle);
* that the grant is **bounded** — one unit, conditions unwaivable, withholdings enumerated;
* that this filing **changes no production byte** and leaves Stage 1 fail-closed; and
* that the ``SS-M`` disclosure is **true of the merged bytes**, executed rather than believed.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

import pytest
import yaml

import level1_stage1_execution_authorization as AUTH

#: The three REAL consumer seams, reused from the XASSET-0056 suite that already drives them
#: against the live module rather than re-implementing a second, divergent harness here. These are
#: the actual production call sites of ``parse_formal_disposition``:
#:   1. ``_derive_pr337_actor_ratification``
#:   2. ``verify_lifecycle_against_truth``
#:   3. ``_verify_selected_review_is_final``
import test_level1_stage1_formal_disposition_parser_correction as _SEAMS_MODULE


class _SEAMS:
    """Thin, explicit binding to the real seam runners. No behaviour of its own."""

    run_consumer_one = staticmethod(_SEAMS_MODULE._run_consumer_one)
    run_consumer_two = staticmethod(_SEAMS_MODULE._run_consumer_two)
    run_consumer_three = staticmethod(_SEAMS_MODULE._run_consumer_three)

ROOT = Path(__file__).resolve().parent

# =====================================================================================
# Immutable identities — every one independently verified from live git/GitHub before use
# =====================================================================================

#: This unit's own base: the normal-merge commit that closed the ``XASSET-0056`` lifecycle.
THIS_UNIT_BASE_SHA = "583022a5f2106d61f82d270edadd3520d8b0c55d"

#: ``XASSET-0056``'s independently reviewed and principal-accepted head.
XASSET_0056_ACCEPTED_HEAD = "f1bf3fd0f1f878ccf9db88f15c48059e5e4637e2"

#: The merge's first parent — the prior ``main`` tip.
XASSET_0056_MERGE_PARENT_1 = "29e4969885970d942a5acecc1424fb2e2b080d60"

#: Byte-identical between the accepted head and the merge: zero drift at merge.
SHARED_TREE = "8df4624eac7477a7b898e92178bc46be3ff1056b"

#: The load-bearing module's **retained** (old) identity — still bound, deliberately stale.
BOUND_MODULE_SHA256 = "4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541"
BOUND_MODULE_BLOB = "f71b08b4ebe95f161c57cdbb2a924748f13af02d"

#: The load-bearing module's **current merged** identity — the new end of the future transition.
MERGED_MODULE_SHA256 = "12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5"
MERGED_MODULE_BLOB = "b5622f9e412afd604a11cde04317b79c5e57920a"

#: The structural bindings this filing leaves entirely unmoved.
AUTHORIZING_DECISION = "XASSET-0049"
AUTHORIZING_PULL_REQUEST = 349
REVIEWED_BASE_SHA = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"
LOAD_BEARING_COUNT = 18

#: The outcome surface this grant preserves unchanged.
CONSTRUCTION_COUNT = 680
CONSTRUCTION_CELL_COUNT = 48
CONSTRUCTION_UNIVERSE_SHA256 = (
    "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
)

#: ``XASSET-0056`` lifecycle evidence.
CLEAN_REVIEW = "5024576065"
PRINCIPAL_ACCEPTANCE = "5417902549"
POST_MERGE_VERIFICATION = "5417925363"
FINAL_CLOSURE = "5418040301"
MERGE_COMMIT_CI_RUN = "32907801650"
MERGE_COMMIT_CI_JOB = "97995562890"
CLOSED_PULL_REQUEST = 357

#: The post-merge bot review disclosed in ``SS-M``.
POST_MERGE_BOT_REVIEW = "5025021718"

#: This unit's own identity.
DECISION_ID = "XASSET-0057"
DECISION_RELPATH = (
    "governance/decisions/"
    "XASSET-0057-endpoint-0001-stage-1-post-parser-correction-rebinding-authorization.md"
)
BRANCH = "claude/xasset-successor-authorization-3b0btg"
THIS_GATE = "xasset0057-post-parser-correction-rebinding-authorization"
PR_SENTINEL = -57
PRIOR_SENTINELS = (-1, -2, -50, -51, -52, -53, -54, -55, -56)

MODULE_RELPATH = "level1_stage1_execution_authorization.py"
WORKSTREAMS = ROOT / "operations" / "WORKSTREAMS.yaml"
DECISION_PATH = ROOT / DECISION_RELPATH


# =====================================================================================
# Helpers
# =====================================================================================


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def _commit_exists(sha: str) -> bool:
    return (
        subprocess.run(
            ["git", "-C", str(ROOT), "cat-file", "-e", f"{sha}^{{commit}}"],
            capture_output=True,
        ).returncode
        == 0
    )


def _blob_at(commit: str, relpath: str) -> str | None:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", f"{commit}:{relpath}"],
        capture_output=True,
        text=True,
    )
    return out.stdout.strip() if out.returncode == 0 else None


def _content_at(commit: str, relpath: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{commit}:{relpath}"],
        capture_output=True,
        check=True,
    ).stdout


def _flat(text: str) -> str:
    """Collapse whitespace so prose assertions survive line wrapping."""
    return re.sub(r"\s+", " ", text)


def _section(text: str, letter: str) -> str:
    """Return the body of ``### <letter>.`` up to the next ``###``/``##`` heading."""
    m = re.search(rf"^### {re.escape(letter)}\. .*?$", text, re.M)
    assert m, f"section {letter} not found"
    rest = text[m.end() :]
    nxt = re.search(r"^#{2,3} ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_flat(decision_text: str) -> str:
    return _flat(decision_text)


@pytest.fixture(scope="module")
def register() -> dict:
    doc = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
    return next(w for w in doc["workstreams"] if w["id"] == "WS-0014")


# =====================================================================================
# 1. The authority this filing rests on is real, and it is closed
# =====================================================================================


class TestTheAuthorityIsRealAndClosed:
    def test_this_units_base_is_the_xasset_0056_merge(self):
        assert _commit_exists(THIS_UNIT_BASE_SHA)
        parents = _git("rev-list", "--parents", "-n", "1", THIS_UNIT_BASE_SHA).split()
        assert parents[0] == THIS_UNIT_BASE_SHA
        assert len(parents) == 3, "a normal merge has exactly two parents"

    def test_the_merge_parents_are_exact_and_ordered(self):
        parents = _git("rev-list", "--parents", "-n", "1", THIS_UNIT_BASE_SHA).split()[1:]
        assert parents == [XASSET_0056_MERGE_PARENT_1, XASSET_0056_ACCEPTED_HEAD]

    def test_the_authority_merged_with_zero_drift(self):
        """The merge tree is byte-identical to the accepted head's own tree."""
        assert _git("rev-parse", f"{THIS_UNIT_BASE_SHA}^{{tree}}") == SHARED_TREE
        assert _git("rev-parse", f"{XASSET_0056_ACCEPTED_HEAD}^{{tree}}") == SHARED_TREE

    def test_the_accepted_head_descends_from_the_prior_main_tip(self):
        assert (
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(ROOT),
                    "merge-base",
                    "--is-ancestor",
                    XASSET_0056_MERGE_PARENT_1,
                    XASSET_0056_ACCEPTED_HEAD,
                ],
                capture_output=True,
            ).returncode
            == 0
        )

    @pytest.mark.parametrize(
        "token",
        [
            CLEAN_REVIEW,
            PRINCIPAL_ACCEPTANCE,
            POST_MERGE_VERIFICATION,
            FINAL_CLOSURE,
            MERGE_COMMIT_CI_RUN,
            MERGE_COMMIT_CI_JOB,
        ],
    )
    def test_the_decision_records_each_lifecycle_identity(self, decision_flat, token):
        assert token in decision_flat


# =====================================================================================
# 2. The authority gap is reproduced from accepted text, not asserted
# =====================================================================================


class TestTheAuthorityGapIsReproducedFromAcceptedText:
    def test_the_predecessors_own_withholding_is_quoted(self, decision_flat):
        assert "is **not applied by anything here**" in decision_flat
        assert "or any successor unit of any kind" in decision_flat

    def test_the_predecessor_really_does_withhold_it(self):
        """Not merely quoted here: the merged XASSET-0056 file actually says it."""
        body = _content_at(
            THIS_UNIT_BASE_SHA,
            "governance/decisions/XASSET-0056-endpoint-0001-formal-disposition-parser-correction.md",
        ).decode("utf-8")
        flat = _flat(body)
        assert "is not applied by anything here" in flat
        assert "perform a step-8-equivalent rebinding" in flat
        assert "or any successor unit of any kind" in flat

    def test_the_prior_grant_is_recorded_spent(self, decision_flat):
        assert "XASSET-0048" in decision_flat
        assert "spent" in decision_flat
        assert "XASSET-0049 consumed it" in decision_flat or "XASSET-0049` consumed it" in decision_flat

    def test_the_conclusion_is_that_no_live_authority_existed(self, decision_flat):
        assert "no live authority existed" in decision_flat

    def test_the_filing_refuses_the_implicit_grant_reading(self, decision_flat):
        assert "refused here in terms" in decision_flat


# =====================================================================================
# 3. The grant is bounded
# =====================================================================================


class TestTheGrantIsBounded:
    def test_the_determination_is_the_expected_one(self, decision_flat):
        assert "STEP_8_EQUIVALENT_REBINDING_AUTHORIZED" in decision_flat

    def test_the_determination_says_design_only_and_arms_nothing(self, decision_flat):
        assert "design-only" in decision_flat
        assert "arms nothing" in decision_flat

    def test_the_grant_names_exactly_one_unit(self, decision_text):
        e = _flat(_section(decision_text, "E"))
        assert "exactly** one" in e or "**exactly one**" in e

    def test_the_successor_identifier_is_never_predicted(self, decision_text):
        e = _flat(_section(decision_text, "E"))
        assert "verified unused against live repository state" in e
        assert "never predicted, reserved, or named here" in e

    def test_no_successor_identifier_is_named_anywhere(self, decision_text):
        """The filing must not pre-name the unit it authorizes."""
        found = set(re.findall(r"XASSET-(\d{4})", decision_text))
        assert "0058" not in found
        assert "0059" not in found
        assert max(found) == "0057", f"an identifier beyond this one is named: {sorted(found)}"

    def test_this_filing_performs_no_rebinding(self, decision_flat):
        assert "**It performs no rebinding.**" in decision_flat
        assert "Merging this decision performs no rebinding" in decision_flat


# =====================================================================================
# 4. The required properties are conditions, and they are the right ones
# =====================================================================================


class TestTheRequiredPropertiesAreConditions:
    def test_they_are_conditions_and_unwaivable(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "None is satisfied by this filing" in f
        assert "none may be waived by the unit that performs it" in f

    def test_the_base_rule_is_equality_not_descent(self, decision_text):
        """RE-ANCHORED (DELTA 5027180757 MAJOR 2): the base rule now names the qualifying
        commit EXACTLY -- the Lifecycle B implementation's B5 normal-merge commit -- rather
        than referring to the withdrawn, ambiguous "the required parser-correction lifecycle
        (SS F.0 conditions 1-8)". Strictly stronger: the superseded OPERATIVE form is pinned
        absent, the withdrawal is pinned present, and the new exact naming is pinned present."""
        f = _flat(_section(decision_text, "F"))
        assert "Equality, not descent" in f

        # (a) the superseded OPERATIVE formulation is gone as a rule.
        assert "must EQUAL the exact normal-merge commit" not in f
        # ... and the earlier absolute-plus-exception formulation stays gone.
        assert "at *this* authorization's own merge" not in f

        # (b) its withdrawal is stated, not silently dropped.
        assert "That reference is **withdrawn and replaced**" in f
        assert "There are no longer generic \u00a7F.0 conditions 1\u20138" in _flat(
            _section(decision_text, "F")
        ).replace("\u201c", "").replace("\u201d", "").replace('"', "")

        # (c) the replacement names the commit exactly, at BOTH statements of it.
        assert (
            "must EQUAL the Lifecycle B implementation's normal-merge commit at B5"
            in f
        )
        assert "the base must **equal the B5 normal-merge commit** of the Lifecycle B" in f

        # (d) B5 is tied to the SHA B7 tests and B8 names -- the three are one commit.
        assert "exact B5 merge SHA is the SHA tested by B7" in f
        assert "named by B8" in f

        # (e) singularity is unchanged.
        assert "single, unambiguous" in f

    def test_ancestry_is_stated_necessary_but_explicitly_insufficient(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "necessary history and explicitly insufficient authority" in f
        assert "descent alone never qualifies a base" in f

    def test_any_intervening_main_commit_is_drift_and_a_stop(self, decision_text):
        """RE-ANCHORED (DELTA 5026362328 BLOCKING 1): drift is now measured from the
        PARSER-CORRECTION merge, which is the only lawful base."""
        f = _flat(_section(decision_text, "F"))
        # RE-ANCHORED (DELTA 5026856868 BLOCKING 1A): the admission path was REMOVED, so the
        # rule is now absolute rather than "unadmitted drift is a stop".
        assert "Any later `main` commit invalidates this grant for that base" in f
        assert "may not proceed on the strength of this\nauthorization**, full stop" in _section(
            decision_text, "F"
        ) or "full stop" in f
        # RE-ANCHORED (DELTA 5027180757 MAJOR 2): drift is measured from the exactly-named
        # B5 implementation merge, not from an ambiguous "parser-correction merge".
        assert (
            "between the **B5 implementation merge** and the authorized unit's base" in f
        )
        assert "between the parser-correction merge and the authorized" not in f

    def test_the_base_must_be_derived_not_predicted(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "must never be predicted" in f
        assert "prove the equality from the git object store" in f

    def test_exact_closed_transitions_are_required_at_both_ends(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "exact closed transition" in f
        assert "both explicit, both independently proven" in f
        assert "preserved rather than overwritten" in f

    def test_the_module_transition_names_both_ends_explicitly(self, decision_flat):
        assert BOUND_MODULE_SHA256 in decision_flat
        assert MERGED_MODULE_SHA256 in decision_flat
        assert BOUND_MODULE_BLOB in decision_flat
        assert MERGED_MODULE_BLOB in decision_flat

    def test_the_lifecycle_anchor_transition_names_all_three_old_values(self, decision_flat):
        assert AUTHORIZING_DECISION in decision_flat
        assert str(AUTHORIZING_PULL_REQUEST) in decision_flat
        assert REVIEWED_BASE_SHA in decision_flat

    def test_minimality_is_an_operative_condition(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "smallest strictly necessary rebinding" in f
        assert "stops and discloses" in f

    def test_the_boundary_may_only_grow(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "may only be extended" in f
        assert "No existing member may be removed" in f

    def test_pins_are_recomputed_once_and_last(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "recomputed exactly once" in f
        assert "after every authorized byte has stabilized" in f

    @pytest.mark.parametrize(
        "requirement",
        [
            "adversarial mutation proofs",
            "exact-head CI",
            "simulated normal-merge verification",
            "working-tree residue check",
            "zero-write rehearsal",
        ],
    )
    def test_the_validation_requirements_are_enumerated(self, decision_text, requirement):
        f = _flat(_section(decision_text, "F"))
        assert requirement in f


# =====================================================================================
# 5. The outcome surface and the universe are preserved
# =====================================================================================


class TestTheOutcomeSurfaceIsPreserved:
    @pytest.mark.parametrize(
        "preserved",
        [
            "deterministic runner",
            "result validator",
            "universe closure validator",
            "deterministic derivation surface",
            "canonical construction inputs",
            "frozen construction identities",
            "ordering",
            "risk_lane_boundary",
        ],
    )
    def test_each_preserved_surface_is_named(self, decision_text, preserved):
        f = _flat(_section(decision_text, "F"))
        assert preserved in f

    def test_the_universe_values_are_pinned_in_the_decision(self, decision_flat):
        assert "680 / 48" in decision_flat
        assert "73c0965e" in decision_flat

    def test_the_universe_values_are_the_live_ones(self):
        assert AUTH.CONSTRUCTION_COUNT == CONSTRUCTION_COUNT
        assert AUTH.CONSTRUCTION_CELL_COUNT == CONSTRUCTION_CELL_COUNT
        assert AUTH.CONSTRUCTION_UNIVERSE_SHA256 == CONSTRUCTION_UNIVERSE_SHA256

    def test_the_rebinding_binds_bytes_not_meaning(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "it does not get to move meaning" in f


# =====================================================================================
# 6. Authority withheld
# =====================================================================================


class TestAuthorityWithheld:
    @pytest.mark.parametrize(
        "withheld",
        [
            "readiness verification",
            "drift verification",
            "attestation",
            "arming",
            "claiming",
            "evaluating any gate",
            "stage1_results.yaml",
            "percentage",
            "risk_lane_boundary",
            "the parser",
        ],
    )
    def test_each_withheld_act_appears(self, decision_text, withheld):
        combined = _flat(_section(decision_text, "G")) + " " + _flat(_section(decision_text, "L"))
        assert withheld.lower() in combined.lower()

    def test_completing_the_rebinding_authorizes_no_next_link(self, decision_text):
        g = _flat(_section(decision_text, "G"))
        assert "each require their own separate authority" in g
        assert "Completing the rebinding authorizes the next link no more than" in g

    def test_the_reserved_results_pr_stays_unconsumed(self, decision_text):
        c = _flat(_section(decision_text, "C"))
        assert "not consumed, replaced, or counted against" in c
        assert "reserved and unspent" in c

    def test_no_activation_authorization_is_added(self, decision_text):
        d = _flat(_section(decision_text, "D"))
        assert "zero** activation authorizations" in d or "**zero** activation authorizations" in d
        assert "never** another merged authorization PR" in d


# =====================================================================================
# 7. This filing changes no production byte
# =====================================================================================


class TestThisFilingChangesNoProductionByte:
    def test_the_load_bearing_module_is_byte_identical_to_its_base(self):
        assert _blob_at(THIS_UNIT_BASE_SHA, MODULE_RELPATH) == MERGED_MODULE_BLOB
        live = hashlib.sha256((ROOT / MODULE_RELPATH).read_bytes()).hexdigest()
        assert live == MERGED_MODULE_SHA256

    def test_the_structural_bindings_are_unmoved(self):
        assert AUTH.AUTHORIZING_DECISION == AUTHORIZING_DECISION
        assert AUTH.AUTHORIZING_PULL_REQUEST == AUTHORIZING_PULL_REQUEST
        assert AUTH.REVIEWED_BASE_SHA == REVIEWED_BASE_SHA

    def test_the_trust_boundary_is_unchanged_at_eighteen(self):
        assert len(AUTH.LOAD_BEARING_RELPATHS) == LOAD_BEARING_COUNT

    def test_the_bound_digest_is_still_the_stale_one(self):
        """The whole safety property: bound != merged, deliberately.

        Both ends of the future closed transition are proved from the git object store rather
        than read from any prose: the OLD end is the module as it stood at the pre-correction
        commit the register still binds, and the NEW end is the merged state.
        """
        assert BOUND_MODULE_SHA256 != MERGED_MODULE_SHA256
        assert MERGED_MODULE_BLOB != BOUND_MODULE_BLOB

        old_blob = _blob_at(XASSET_0056_MERGE_PARENT_1, MODULE_RELPATH)
        old_sha = hashlib.sha256(
            _content_at(XASSET_0056_MERGE_PARENT_1, MODULE_RELPATH)
        ).hexdigest()
        assert old_blob == BOUND_MODULE_BLOB
        assert old_sha == BOUND_MODULE_SHA256

        new_blob = _blob_at(THIS_UNIT_BASE_SHA, MODULE_RELPATH)
        new_sha = hashlib.sha256(_content_at(THIS_UNIT_BASE_SHA, MODULE_RELPATH)).hexdigest()
        assert new_blob == MERGED_MODULE_BLOB
        assert new_sha == MERGED_MODULE_SHA256

    def test_the_enforcement_surface_itself_is_unchanged(self):
        """`_verify_git_anchored_identity` is byte-identical across the correction."""
        import ast

        def _defn(commit: str) -> str:
            src = _content_at(commit, MODULE_RELPATH).decode("utf-8")
            tree = ast.parse(src)
            node = next(
                n
                for n in tree.body
                if isinstance(n, ast.FunctionDef) and n.name == "_verify_git_anchored_identity"
            )
            return ast.dump(node)

        assert _defn(XASSET_0056_MERGE_PARENT_1) == _defn(THIS_UNIT_BASE_SHA)

    def test_this_filing_touches_no_load_bearing_path(self):
        """Every load-bearing path is byte-identical between the base and the working tree."""
        for relpath in AUTH.LOAD_BEARING_RELPATHS:
            p = ROOT / relpath
            if not p.exists():
                continue
            base_blob = _blob_at(THIS_UNIT_BASE_SHA, relpath)
            live_blob = _git("hash-object", str(p))
            assert base_blob == live_blob, f"load-bearing path changed: {relpath}"


# =====================================================================================
# 8. Stage 1 remains fail-closed
# =====================================================================================


class TestStage1RemainsFailClosed:
    def test_both_authorization_predicates_are_false(self):
        for fn in ("new_execution_is_authorized", "active_execution_is_authorized"):
            result = getattr(AUTH, fn)()
            authorized = result[0] if isinstance(result, tuple) else result
            assert authorized is False, fn

    def test_the_lane_and_authorization_root_are_absent(self):
        assert not Path(str(AUTH.AUTHORIZATION_ROOT)).exists()

    def test_attempt_one_is_intact_and_unconsumed(self):
        assert AUTH.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

    def test_no_results_artifact_exists(self):
        assert not (ROOT / "stage1_results.yaml").exists()
        assert list(ROOT.rglob("stage1_results*")) == []

    def test_stage_1_executability_stays_false(self):
        doc = yaml.safe_load(
            (ROOT / "research" / "level1_endpoint_evidence" / "pre_registration.yaml").read_text(
                encoding="utf-8"
            )
        )
        assert doc["stage_1_executability"]["executable"] is False

    def test_the_decision_states_the_posture(self, decision_flat):
        assert "Stage 1 remains UNARMED and NOT EXECUTABLE" in decision_flat
        assert "`ATTEMPT_1` is intact, unclaimed" in decision_flat


# =====================================================================================
# 9. The SS-M disclosure is true of the merged bytes — executed, not believed
# =====================================================================================

_APPROVAL = "FORMAL DISPOSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"

#: The canonical adverse first line, untampered. Every attack below is this exact string with
#: EXACTLY ONE ASCII character replaced in place by a visual lookalike -- never an insertion, never
#: a deletion, and never a character replaced at some other character's position.
_CANONICAL_ADVERSE = "FORMAL DISPOSITION: CHANGES REQUIRED"


def _replace_at(text: str, index: int, replacement: str) -> str:
    """Replace exactly one code point at ``index``. Length in code points is preserved."""
    return text[:index] + replacement + text[index + 1 :]


#: Each entry is (label, ascii_char, index, homoglyph). ``index`` is the position of a REAL
#: occurrence of ``ascii_char`` inside ``_CANONICAL_ADVERSE``, so each lookalike genuinely
#: substitutes for the character it resembles:
#:
#:   * U+039F GREEK CAPITAL OMICRON replaces the ASCII ``O`` of DISP-O-SITION (index 11)
#:   * U+0410 CYRILLIC CAPITAL A    replaces the ASCII ``A`` of FORM-A-L      (index 4)
#:   * U+0130 LATIN CAPITAL I WITH DOT ABOVE replaces the ASCII ``I`` of D-I-SPOSITION (index 8)
#:
#: DELTA review 5026362328 MINOR 1: the superseded construction was
#: ``"FORMAL DISP" + homoglyph + _ADVERSE_TAIL[1:]`` with ``_ADVERSE_TAIL = "SITION: ..."``. The
#: ``[1:]`` slice DROPPED the ``S``, so the Omicron case built ``FORMAL DISPΟITION:`` rather than
#: the reported ``FORMAL DISPΟSITION:``, and all three code points were inserted at the ``O``
#: position instead of replacing their own ASCII counterparts. The finding was real; the artifact
#: did not pin the exact forms it claimed. These are the position-correct forms.
_HOMOGLYPH_ATTACKS = (
    ("U+039F GREEK CAPITAL OMICRON for ASCII O", "O", 11, "\u039f"),
    ("U+0410 CYRILLIC CAPITAL A for ASCII A", "A", 4, "\u0410"),
    ("U+0130 LATIN CAPITAL I WITH DOT for ASCII I", "I", 8, "\u0130"),
)


def _attack_first_line(ascii_char: str, index: int, homoglyph: str) -> str:
    """Build one position-correct tampered adverse first line, asserting its own correctness."""
    assert _CANONICAL_ADVERSE[index] == ascii_char, (index, _CANONICAL_ADVERSE[index], ascii_char)
    line = _replace_at(_CANONICAL_ADVERSE, index, homoglyph)
    # Non-vacuity: the intended code point really is at the intended position, exactly one
    # character differs, and the length is unchanged.
    assert line[index] == homoglyph
    assert len(line) == len(_CANONICAL_ADVERSE)
    assert sum(1 for a, b in zip(line, _CANONICAL_ADVERSE) if a != b) == 1
    return line


def _adverse_then_approval(prefix_body: str) -> str:
    return prefix_body + "\n" + _APPROVAL + "\n"


class TestTheDisclosedFindingIsReproducedAndBounded:
    """``SS-M`` claims the bot finding reproduces and is bounded. Both halves are executed here,
    against position-correct attack bodies driven through the parser and all three real consumer
    seams."""

    # ---- structural non-vacuity: the bodies really are what they claim to be ----

    @pytest.mark.parametrize("label,ascii_char,index,homoglyph", _HOMOGLYPH_ATTACKS)
    def test_each_attack_replaces_its_own_ascii_character_in_place(
        self, label, ascii_char, index, homoglyph
    ):
        line = _attack_first_line(ascii_char, index, homoglyph)
        assert _CANONICAL_ADVERSE[index] == ascii_char, "the index must name a REAL occurrence"
        assert line[index] == homoglyph, "the lookalike must sit at that exact position"
        assert line[index] != ascii_char
        assert ord(homoglyph) > 127, "the replacement must be non-ASCII"
        # DELTA review 5026856868 MINOR 1: the superseded assertion here was
        # `homoglyph.upper() == homoglyph or homoglyph.upper() != homoglyph`, an exhaustive
        # `x == y or x != y` that is true of EVERY comparable value and proved nothing. The
        # documented mechanism is that UPPERCASING the lookalike does not turn it into the ASCII
        # character it resembles -- which is exactly why the wide resemblance view deletes it
        # rather than recognising it. That is the property now asserted.
        upper = homoglyph.upper()
        assert all(ord(c) > 127 for c in upper), (
            f"{homoglyph!r}.upper() = {upper!r} must stay non-ASCII"
        )
        assert upper != ascii_char, f"{homoglyph!r}.upper() must not become {ascii_char!r}"
        assert upper.upper() == upper, "uppercasing must be idempotent"
        # nothing else moved
        assert line[:index] == _CANONICAL_ADVERSE[:index]
        assert line[index + 1 :] == _CANONICAL_ADVERSE[index + 1 :]

    def test_the_superseded_construction_is_gone(self):
        """The `[1:]`-slice construction that dropped the S must not survive in what EXECUTES.

        Asserted on the parsed AST rather than on the file text, because the comment above
        necessarily NAMES the superseded construction in order to explain what was removed. A
        substring scan would false-positive on that prose; a structural scan cannot.
        """
        import ast

        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        names = {
            n.id for n in ast.walk(tree) if isinstance(n, ast.Name)
        } | {
            t.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Assign)
            for t in node.targets
            if isinstance(t, ast.Name)
        }
        assert "_ADVERSE_TAIL" not in names, "the superseded constant is still live code"

        # And no surviving slice-of-a-tail construction anywhere in the module.
        for node in ast.walk(tree):
            if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name):
                assert not node.value.id.endswith("_TAIL"), ast.dump(node)

    def test_the_omicron_body_is_exactly_the_reported_string(self):
        """The exact form the external finding named, character for character."""
        line = _attack_first_line("O", 11, "\u039f")
        assert line == "FORMAL DISP\u039fSITION: CHANGES REQUIRED"
        assert "SITION" in line, "the S must NOT be dropped"
        assert line.count("S") == _CANONICAL_ADVERSE.count("S")

    @pytest.mark.parametrize("label,ascii_char,index,homoglyph", _HOMOGLYPH_ATTACKS)
    def test_the_body_is_adverse_first_then_approving(self, label, ascii_char, index, homoglyph):
        body = _adverse_then_approval(_attack_first_line(ascii_char, index, homoglyph))
        lines = [ln for ln in body.split("\n") if ln.strip()]
        assert len(lines) == 2, lines
        assert "CHANGES REQUIRED" in lines[0], "line 1 must be the ADVERSE record"
        assert lines[1] == _APPROVAL, "line 2 must be the canonical approval"

    # ---- the parser itself ----

    @pytest.mark.parametrize("label,ascii_char,index,homoglyph", _HOMOGLYPH_ATTACKS)
    def test_the_reported_skip_family_reproduces_in_the_parser(
        self, label, ascii_char, index, homoglyph
    ):
        """A prefix-interior homoglyph makes the adverse line skip and a later approval win."""
        body = _adverse_then_approval(_attack_first_line(ascii_char, index, homoglyph))
        assert AUTH.parse_formal_disposition(body) == (
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        ), label

    def test_the_canonical_adverse_line_still_wins(self):
        """The control: an untampered adverse first line is not skipped."""
        assert AUTH.parse_formal_disposition(
            _adverse_then_approval(_CANONICAL_ADVERSE)
        ) == "CHANGES REQUIRED"

    def test_a_tampered_prefix_alone_never_authenticates(self):
        """The bound: the finding is a skip, never a direct authentication."""
        tampered = _replace_at(_APPROVAL, 11, "\u039f") + "\n"
        assert tampered[11] == "\u039f"
        assert AUTH.parse_formal_disposition(tampered) != (
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        )

    def test_a_homoglyph_in_the_verdict_does_not_bypass(self):
        """The bound: only the PREFIX is affected. U+0415 replaces the E of CHANGES."""
        e_index = _CANONICAL_ADVERSE.index("CHANGES") + 5
        assert _CANONICAL_ADVERSE[e_index] == "E"
        line = _replace_at(_CANONICAL_ADVERSE, e_index, "\u0415")
        assert AUTH.parse_formal_disposition(_adverse_then_approval(line)) != (
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        )

    def test_a_plain_approval_still_authenticates(self):
        assert AUTH.parse_formal_disposition(_APPROVAL + "\n") == (
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        )

    # ---- every real consumer seam ----

    @pytest.mark.parametrize("label,ascii_char,index,homoglyph", _HOMOGLYPH_ATTACKS)
    def test_the_bypass_reaches_consumer_one(self, label, ascii_char, index, homoglyph, monkeypatch):
        """Seam 1 -- `_derive_pr337_actor_ratification`: the tampered body passes the parser gate
        exactly as a clean approval does, so execution proceeds past it."""
        body = _adverse_then_approval(_attack_first_line(ascii_char, index, homoglyph))
        recorder = _SEAMS.run_consumer_one(body, monkeypatch)
        assert any(c.startswith("reviews:") for c in recorder.calls), (label, recorder.calls)

    def test_consumer_one_stops_on_the_untampered_adverse_body(self, monkeypatch):
        """Seam 1 control: the canonical adverse first line does NOT pass the gate."""
        body = _adverse_then_approval(_CANONICAL_ADVERSE)
        recorder = _SEAMS.run_consumer_one(body, monkeypatch)
        assert not any(c.startswith("reviews:") for c in recorder.calls), recorder.calls

    @pytest.mark.parametrize("label,ascii_char,index,homoglyph", _HOMOGLYPH_ATTACKS)
    def test_the_bypass_reaches_consumer_two(self, label, ascii_char, index, homoglyph):
        """Seam 2 -- `verify_lifecycle_against_truth`: the tampered body is treated as approving,
        so it raises none of the adverse/malformed/absent disposition errors."""
        body = _adverse_then_approval(_attack_first_line(ascii_char, index, homoglyph))
        errors = _SEAMS.run_consumer_two(body)
        joined = " ".join(errors)
        assert "carries no parseable" not in joined, (label, errors)
        assert "CHANGES REQUIRED" not in joined, (label, errors)

    def test_consumer_two_reports_the_untampered_adverse_body(self):
        """Seam 2 control: the canonical adverse line is still seen as adverse."""
        errors = _SEAMS.run_consumer_two(_adverse_then_approval(_CANONICAL_ADVERSE))
        assert any("CHANGES REQUIRED" in e for e in errors), errors

    @pytest.mark.parametrize("label,ascii_char,index,homoglyph", _HOMOGLYPH_ATTACKS)
    def test_the_bypass_reaches_consumer_three(self, label, ascii_char, index, homoglyph):
        """Seam 3 -- `_verify_selected_review_is_final`: a later tampered record is not treated as
        an adverse successor, so it does not unseat the selected review."""
        body = _adverse_then_approval(_attack_first_line(ascii_char, index, homoglyph))
        errors = _SEAMS.run_consumer_three(body, "COMMENTED")
        assert not any("CHANGES REQUIRED" in e for e in errors), (label, errors)

    def test_consumer_three_reports_the_untampered_adverse_body(self):
        """Seam 3 control: the canonical adverse successor IS caught."""
        errors = _SEAMS.run_consumer_three(_adverse_then_approval(_CANONICAL_ADVERSE), "COMMENTED")
        assert any("CHANGES REQUIRED" in e for e in errors), errors

    # ---- the decision's own SS-M text ----

    def test_the_disclosure_records_the_bot_review_and_its_timing(self, decision_flat):
        assert POST_MERGE_BOT_REVIEW in decision_flat
        assert "chatgpt-codex-connector[bot]" in decision_flat
        assert "not** part of the accepted `XASSET-0056` lifecycle" in decision_flat

    def test_the_disclosure_states_all_three_consequences(self, decision_text):
        m = _flat(_section(decision_text, "M"))
        assert "does not repair it, and is not authorized to" in m
        assert "does not make Stage 1 executable" in m
        assert "disclosure is not a safety precondition" in m.lower()

    def test_the_disclosure_does_not_rule_on_the_fix(self, decision_text):
        m = _flat(_section(decision_text, "M"))
        assert "open, unresolved, and outside this grant" in m


# =====================================================================================
# 9b. BLOCKING 1 — the parser correction is a conjunctive PREREQUISITE, not a contingency
# =====================================================================================


class TestTheParserCorrectionIsAConjunctivePrerequisite:
    """DELTA review 5026362328 BLOCKING 1.

    The superseded text let the rebinding proceed against the known-defective bytes whenever no
    parser fix happened to land first: no intervening commit meant no drift, so nothing fired.
    These assertions pin the corrected posture at its mechanism, not at its prose.
    """

    def test_section_f0_exists_and_is_conjunctive(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "F.0 —" in f
        assert "conjunctive with every other condition" in f
        assert "not an alternative to any of them" in f
        assert "not satisfied by disclosure" in f

    def test_the_defective_identity_is_a_permanent_negative_pin(self, decision_flat):
        assert "The current vulnerable module may never be rebound" in decision_flat
        assert MERGED_MODULE_SHA256 in decision_flat
        assert "permanent negative pin" in decision_flat

    def test_the_defective_identity_pinned_is_the_one_that_is_actually_defective(self):
        """Non-vacuity: the digest named as the negative pin is the live, reproducing module."""
        live = hashlib.sha256((ROOT / MODULE_RELPATH).read_bytes()).hexdigest()
        assert live == MERGED_MODULE_SHA256
        body = _adverse_then_approval(_attack_first_line("O", 11, "\u039f"))
        assert AUTH.parse_formal_disposition(body) == (
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        ), "the pinned identity must be the one that actually fails open"

    def test_all_eight_prerequisite_conditions_are_enumerated(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        # RE-ANCHORED (DELTA 5026856868 MAJOR 1): the single eight-step list is superseded by
        # TWO lifecycles -- A1-A7 for the AUTHORIZATION, B1-B8 for the IMPLEMENTATION.
        for required in (
            "independent **FULL** exact-head review",
            "principal exact-head acceptance",
            "normal merge",
            "immediate post-merge verification",
            "successful merge-commit CI",
            "final post-CI verification and lifecycle closure",
            "the implementation itself, correcting the defect family",
        ):
            assert required in f, required
        assert "None of A1–A7 or B1–B8 is individually sufficient" in f
        assert "only complete closure of both lifecycles is" in f

    def test_the_corrected_identity_is_derived_never_predicted(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        # RE-ANCHORED (DELTA 5026856868 BLOCKING 1B): F.0 no longer carries its own table; the
        # derived identities live in F.3's single four-role chain.
        assert "single ordered identity chain in §F.3 as role 3" in f
        assert "**no** competing transition table of its own" in f
        assert "never\npredicted" in _section(decision_text, "F")

    def test_a_rebinding_of_the_old_end_fails_outright(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        # RE-ANCHORED (DELTA 5026856868 BLOCKING 1B): "the old end" is now role 2 by name.
        assert "equals role 2 — the vulnerable intermediate —" in f
        assert "fails this condition outright" in f

    def test_the_grant_itself_is_gated_on_the_prerequisite(self, decision_text):
        e = _flat(_section(decision_text, "E"))
        assert "conjunctive parser-correction prerequisite in §F.0" in e
        assert "both, not either" in e

    def test_the_determination_records_the_grant_as_conditional(self, decision_text):
        a = _flat(_section(decision_text, "A"))
        assert "conditional, not standing" in a

    def test_this_filing_still_performs_no_parser_correction(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "does not perform, design, schedule or authorize that parser correction" in f

    def test_the_module_is_untouched_by_this_correction(self):
        """Structural: the absolute boundary held through the correction too."""
        assert _blob_at(THIS_UNIT_BASE_SHA, MODULE_RELPATH) == MERGED_MODULE_BLOB
        live = _git("hash-object", str(ROOT / MODULE_RELPATH))
        assert live == MERGED_MODULE_BLOB

    def test_the_single_base_rule_has_no_competing_absolute(self, decision_text):
        """The reviewer's specific objection: no absolute rule followed by a generic exception."""
        f = _flat(_section(decision_text, "F"))
        assert "the earlier formulation" in f and "withdrawn and replaced" in f
        assert "there is no other, and no exception clause qualifies it" in f
        # the superseded absolute must not survive anywhere in the document
        assert "at *this* authorization's own merge" not in _flat(decision_text)

    def test_the_ordering_is_stated_explicitly(self, decision_text):
        # RE-ANCHORED (DELTA 5027180757 MAJOR 2): the ordering now routes through BOTH named
        # lifecycles and terminates on the exactly-named B5 merge. Strictly stronger: the
        # superseded two-step chain is pinned absent and every new hop is pinned present.
        f = _flat(_section(decision_text, "F"))
        assert "this decision's merge \u2192 the parser correction's" not in f
        assert "this decision's merge \u2192 Lifecycle A's complete closure (A1\u2013A7)" in f
        assert "\u2192 Lifecycle B's complete closure (B1\u2013B8)" in f
        assert "whose **B5 merge** is the sole qualifying commit" in f
        assert (
            "\u2192 the authorized rebinding's base, which **equals that B5 merge**" in f
        )
        assert "A rebinding based on this decision's own merge" in f
        assert "fails this condition" in f


# =====================================================================================
# 9c. MAJOR 1 — the load-bearing decision boundary is closed
# =====================================================================================


class TestTheLoadBearingDecisionBoundaryIsClosed:
    """DELTA review 5026362328 MAJOR 1."""

    #: Every decision that governs the parser bytes and must gain DIRECT membership.
    REQUIRED = ("XASSET-0053", "XASSET-0055", "XASSET-0056", "XASSET-0057")

    def test_the_gap_this_correction_closes_is_real(self):
        """Non-vacuity: these decisions really are absent from the live boundary today."""
        for d in self.REQUIRED:
            assert not [p for p in AUTH.LOAD_BEARING_RELPATHS if d in p], d
        assert len(AUTH.LOAD_BEARING_RELPATHS) == LOAD_BEARING_COUNT

    @pytest.mark.parametrize("decision", REQUIRED)
    def test_each_governing_decision_is_required_by_name(self, decision_text, decision):
        """Each name must appear as a REQUIRED-MEMBERSHIP path bullet, not merely be mentioned.

        Mutation probe "F.7 drops XASSET-0053" MISSED an earlier form of this assertion: it only
        checked that the name occurred somewhere in SS-F, and SS-F.7's own prose already names
        every one of them when reporting that they are currently ABSENT. Deleting the membership
        bullet therefore left the assertion satisfied. It now pins the bullet itself.
        """
        f = _flat(_section(decision_text, "F"))
        bullet = f"`governance/decisions/{decision}-…`"
        assert bullet in f, f"{decision} is not required as a direct-membership path"
        # and it must sit inside the required-membership list, not the absent-today report
        required_list = f[f.index("**Direct membership is therefore required**") :]
        required_list = required_list[: required_list.index("`XASSET-0054` remains excluded")]
        assert bullet in required_list, f"{decision} is named but not REQUIRED"

    def test_the_future_rebinding_decision_and_the_chain_are_required(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "the future **rebinding** decision's own file" in f
        assert "every** future accepted decision that authorizes or implements" in f

    def test_direct_membership_is_required_not_citation(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "Citation is not membership" in f
        for substitute in ("related_decisions", "quoting it", "equivalence", "inheriting"):
            assert substitute in f, substitute
        assert "Only a path present in that tuple is" in f

    def test_xasset_0054_stays_excluded_absent_independent_evidence(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "`XASSET-0054` remains excluded" in f
        assert "independent evidence that it is operative" in f

    def test_xasset_0054_really_is_absent_from_main(self):
        """Non-vacuity for the exclusion: no XASSET-0054 decision file exists at this base."""
        listing = _git("ls-tree", "--name-only", f"{THIS_UNIT_BASE_SHA}", "governance/decisions/")
        assert not [p for p in listing.split("\n") if "XASSET-0054" in p]
        assert not [p for p in AUTH.LOAD_BEARING_RELPATHS if "XASSET-0054" in p]

    def test_the_final_count_is_derived_never_guessed(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "The final count is derived, never guessed" in f
        assert "derive the exact final count and the exact" in f
        assert "closed membership transition from the actual completed chain" in f

    def test_no_predicted_final_count_is_stated(self, decision_text):
        """Structural: the decision must not name a guessed post-expansion membership figure."""
        f = _section(decision_text, "F")
        for guessed in ("**22**", "**23**", "**24**", "**25**", "22 paths", "23 paths"):
            assert guessed not in f, guessed
        assert "no** predicted final membership figure" in _flat(f)

    def test_the_precedent_is_cited_accurately(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "XASSET-0041`→`XASSET-0044" in f

    def test_that_precedent_really_bound_its_own_chain(self):
        """Non-vacuity: the cited precedent genuinely has all four decisions bound today."""
        for d in ("XASSET-0041", "XASSET-0042", "XASSET-0043", "XASSET-0044"):
            assert [p for p in AUTH.LOAD_BEARING_RELPATHS if d in p], d

    def test_the_grant_item_four_was_widened(self, decision_text):
        e = _flat(_section(decision_text, "E"))
        assert "every** decision file that makes the newly" in e
        assert "parser-governing chain §F.7 enumerates" in e


# =====================================================================================
# 9d. DELTA 5026856868 — singular base rule, four-role chain, two lifecycles, no tautology
# =====================================================================================


class TestTheBaseRuleIsGenuinelySingular:
    """BLOCKING 1A: the `unless` admission path must be REMOVED, not narrowed."""

    def test_no_operative_admission_path_survives(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        # the superseded clause, in the exact shape the reviewer quoted
        assert "admitted into the rebinding through" not in f
        assert "It must stop and obtain new authority, unless" not in f

    def test_the_only_remaining_unless_is_self_describing_prose(self, decision_text):
        """Non-vacuity: `unless` may survive ONLY inside the sentence explaining its removal."""
        f = _section(decision_text, "F")
        for m in re.finditer(r"\bunless\b", f):
            window = _flat(f[max(0, m.start() - 160) : m.start() + 160])
            assert "would reinstate" in window or "admission path" in window, window

    def test_the_replacement_rule_is_absolute(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "with no admission path" in f
        assert "There is **no** clause by which" in f
        assert "new, superseding rebinding authorization" in f
        assert "It is therefore **removed**, not narrowed" in f

    def test_the_equality_rule_still_stands_alone(self, decision_text):
        # RE-ANCHORED (DELTA 5027180757 MAJOR 2): singularity is unchanged; only the naming
        # of the qualifying commit moved. Superseded operative form pinned absent.
        f = _flat(_section(decision_text, "F"))
        assert "must EQUAL the exact normal-merge commit" not in f
        assert (
            "must EQUAL the Lifecycle B implementation's normal-merge commit at B5" in f
        )
        assert "\u2014 and nothing else" in f
        assert "there is no other, and no exception clause qualifies it" in f


class TestTheModuleIdentityChainIsOrderedAndClosed:
    """BLOCKING 1B: one four-role chain, replacing the contradictory two-end tables."""

    def test_the_competing_tables_are_gone(self, decision_flat):
        assert "New — the merged `XASSET-0056` bytes" not in decision_flat
        assert "two ends are already known" not in decision_flat

    @pytest.mark.parametrize(
        "role", ["Previously bound", "Vulnerable intermediate", "Parser-corrected",
                 "Final stabilized post-rebinding"]
    )
    def test_each_of_the_four_roles_is_present(self, decision_flat, role):
        assert role in decision_flat

    def test_the_roles_appear_in_order(self, decision_text):
        f = _section(decision_text, "F")
        idx = [f.index(r) for r in ("Previously bound", "Vulnerable intermediate",
                                    "Parser-corrected", "Final stabilized post-rebinding")]
        assert idx == sorted(idx), idx

    def test_role_two_is_never_a_bound_end(self, decision_flat):
        assert "NEVER a new bound end" in decision_flat
        assert "The final bound identity can never be `12eab05e…604a5`" in decision_flat

    def test_role_two_is_the_actually_defective_identity(self):
        """Non-vacuity: role 2's digest is the live module that really fails open."""
        assert hashlib.sha256((ROOT / MODULE_RELPATH).read_bytes()).hexdigest() == (
            MERGED_MODULE_SHA256
        )
        body = _adverse_then_approval(_attack_first_line("O", 11, "\u039f"))
        assert AUTH.parse_formal_disposition(body) == (
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        )

    def test_roles_three_and_four_are_derived_never_predicted(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "**Derived** at the parser correction's own merge" in f
        assert "**Derived** after every authorized edit of the rebinding has stabilized" in f
        assert f.count("Never predicted here") >= 2

    def test_no_digest_is_invented_for_roles_three_or_four(self, decision_text):
        """Structural: only the two REAL digests may appear as 64-hex literals."""
        found = set(re.findall(r"\b[0-9a-f]{64}\b", decision_text))
        assert found <= {BOUND_MODULE_SHA256, MERGED_MODULE_SHA256, CONSTRUCTION_UNIVERSE_SHA256}, (
            found - {BOUND_MODULE_SHA256, MERGED_MODULE_SHA256, CONSTRUCTION_UNIVERSE_SHA256}
        )

    def test_every_adjacent_transition_must_be_proved(self, decision_flat):
        assert "Every adjacent transition must be proved" in decision_flat
        for pair in ("**1 → 2**", "**2 → 3**", "**3 → 4**"):
            assert pair in decision_flat, pair

    def test_the_final_register_transition_is_named(self, decision_flat):
        assert "The final register transition that the rebinding actually performs is" in decision_flat
        assert "preserved rather than overwritten" in decision_flat


class TestBothLifecyclesMustClose:
    """MAJOR 1: merged is not effective. Two lifecycles, A then B."""

    def test_the_authorization_lifecycle_is_its_own(self, decision_flat):
        assert "Lifecycle A — the parser-correction AUTHORIZATION decision must itself become" in decision_flat
        assert "Lifecycle B — the parser-correction IMPLEMENTATION" in decision_flat
        assert "may not begin until Lifecycle A has" in decision_flat

    def test_the_superseded_merely_merged_wording_is_gone(self, decision_flat):
        assert "its own accepted governance authorization, filed and merged" not in decision_flat

    #: Each authorization step must be present AND carry its own defining content. Probe
    #: "authorization lifecycle collapses back to merged" MISSED an earlier form of this test
    #: that asserted only `f"* {step}." in decision_flat`, so gutting A6 to "a merge of some
    #: kind" still passed. Content is now pinned per step.
    AUTH_STEPS = [
        ("A1", "independent **FULL** exact-head review"),
        ("A2", "exact-head re-review"),
        ("A3", "principal exact-head acceptance"),
        ("A4", "normal merge"),
        ("A5", "post-merge verification"),
        ("A6", "successful merge-commit CI whose `head_sha` is that authorization's exact merge SHA"),
        ("A7", "final post-CI verification and lifecycle closure"),
    ]

    @pytest.mark.parametrize("step,content", AUTH_STEPS)
    def test_every_authorization_step_is_enumerated_with_its_content(
        self, decision_text, step, content
    ):
        f = _section(decision_text, "F")
        assert f"* {step}." in f, step
        body = f[f.index(f"* {step}.") : ]
        body = body[: body.index("\n*")] if "\n*" in body else body
        assert _flat(content) in _flat(body), (step, _flat(body)[:200])

    def test_the_stale_head_bar_is_operative_not_decorative(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "a review anchored to a superseded head does **not** satisfy A1" in f

    @pytest.mark.parametrize("step", ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"])
    def test_every_implementation_step_is_enumerated(self, decision_flat, step):
        assert f"* {step}." in decision_flat, step

    @pytest.mark.parametrize(
        "negative",
        [
            "merged with **failed** merge-commit CI",
            "merged with **no recorded closure**",
            "review anchors to a **stale head**",
            "lifecycle is otherwise **incomplete**",
            "implementation begun **before** Lifecycle A closed",
        ],
    )
    def test_each_disqualifying_case_is_named(self, decision_text, negative):
        assert _flat(negative) in _flat(_section(decision_text, "F")), negative

    def test_the_adverse_precedent_is_cited(self, decision_flat):
        assert "each merged and neither" in decision_flat
        assert "XASSET-0044" in decision_flat and "XASSET-0045" in decision_flat

    def test_the_precedent_is_real_in_this_document(self, decision_flat):
        """Non-vacuity: the decision itself already records both as not effective."""
        assert "remain **not effective**" in decision_flat

    def test_neither_lifecycle_is_individually_sufficient(self, decision_flat):
        assert "only complete closure of both lifecycles is" in decision_flat


class TestTheDefectIsTreatedAsAFamily:
    """Proactive audit: three homoglyphs are examples, not the definition."""

    def test_the_family_subsection_exists(self, decision_flat):
        assert "F.0.1 — The defect is a FAMILY, not three code points" in decision_flat

    #: (matrix row label, measured result). Probe "family matrix drops transposition" MISSED an
    #: earlier form that only looked for the family NAME anywhere in SS-F -- and SS-F.0.2 item 2
    #: names every family in prose, so deleting a matrix row left it satisfied. The MEASURED
    #: ROW is now pinned, not the word.
    FAMILY_ROWS = [
        ("Single-character **deletion**", "**17 / 17**"),
        ("ASCII **substitution**", "**17 / 17**"),
        ("ASCII **insertion**", "**16 / 17**"),
        ("**Adjacent transposition**", "**17 / 17**"),
        ("**Unicode / confusable substitution**", "**17 / 17**"),
    ]

    @pytest.mark.parametrize("row,result", FAMILY_ROWS)
    def test_each_mutation_family_row_is_present_with_its_result(self, decision_text, row, result):
        f = _section(decision_text, "F")
        assert f"| {row} |" in f, row
        line = next(l for l in f.split("\n") if l.startswith(f"| {row} |"))
        assert result in line, (row, line)

    @pytest.mark.parametrize(
        "family",
        ["deletion", "substitution", "insertion", "transposition", "confusable"],
    )
    def test_each_mutation_family_is_also_dispositioned_in_prose(self, decision_text, family):
        """The SS-F.0.2 item-2 requirement, separate from the matrix row above."""
        f = _flat(_section(decision_text, "F"))
        req = f[f.index("**explicitly disposition**") :][:400]
        assert family in req.lower(), family

    def test_patching_three_code_points_is_explicitly_insufficient(self, decision_flat):
        assert "merely patches the three" in decision_flat
        assert "does NOT satisfy §F.0" in decision_flat

    @pytest.mark.parametrize(
        "requirement",
        [
            "total, mechanically testable boundary",
            "explicitly disposition",
            "cannot be skipped",
            "ordinary prose as ABSENT",
            "all three consumer seams",
            "native-`APPROVED` rescue",
            "family-by-position adversarial matrix",
            "exact positive controls",
        ],
    )
    def test_each_future_requirement_is_stated(self, decision_text, requirement):
        assert _flat(requirement) in _flat(_section(decision_text, "F")), requirement

    def test_the_boundary_is_reserved_not_decided_here(self, decision_flat):
        assert "This filing does not decide that recognition boundary" in decision_flat
        assert "reserved" in decision_flat
        assert "unavailable until that decision's complete lifecycle closes" in decision_flat

    # ---- the family is REAL: executed against the unchanged parser ----

    @staticmethod
    def _bypasses(first_line: str) -> bool:
        return AUTH.parse_formal_disposition(
            _adverse_then_approval(first_line)
        ) == "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"

    #: The 17 non-space positions of the `FORMAL DISPOSITION` prefix.
    PREFIX_POSITIONS = tuple(
        i for i, c in enumerate("FORMAL DISPOSITION") if c != " "
    )

    def test_the_prefix_has_seventeen_non_space_positions(self):
        assert len(self.PREFIX_POSITIONS) == 17

    def test_single_character_deletion_bypasses_at_every_position(self):
        hits = [
            i for i in self.PREFIX_POSITIONS
            if self._bypasses(_CANONICAL_ADVERSE[:i] + _CANONICAL_ADVERSE[i + 1 :])
        ]
        assert len(hits) == 17, hits

    def test_ascii_substitution_bypasses_at_every_position(self):
        hits = []
        for i in self.PREFIX_POSITIONS:
            r = "X" if _CANONICAL_ADVERSE[i] != "X" else "Y"
            if self._bypasses(_replace_at(_CANONICAL_ADVERSE, i, r)):
                hits.append(i)
        assert len(hits) == 17, hits

    def test_ascii_insertion_bypasses_at_sixteen_of_seventeen(self):
        """Position 0 is the measured exception: inserting before the `F` leaves the canonical
        prefix intact as a substring, so the line is correctly read as adverse, not skipped."""
        hits = [
            i for i in self.PREFIX_POSITIONS
            if self._bypasses(_CANONICAL_ADVERSE[:i] + "X" + _CANONICAL_ADVERSE[i:])
        ]
        assert len(hits) == 16, hits
        assert 0 not in hits
        assert AUTH.parse_formal_disposition(
            _adverse_then_approval("X" + _CANONICAL_ADVERSE)
        ) is AUTH.MALFORMED_FORMAL_DISPOSITION

    def test_adjacent_transposition_bypasses_at_every_distinct_pair(self):
        prefix = "FORMAL DISPOSITION"
        pairs = [i for i in range(len(prefix) - 1) if prefix[i] != prefix[i + 1]]
        hits = [
            i for i in pairs
            if self._bypasses(
                _CANONICAL_ADVERSE[:i]
                + _CANONICAL_ADVERSE[i + 1]
                + _CANONICAL_ADVERSE[i]
                + _CANONICAL_ADVERSE[i + 2 :]
            )
        ]
        assert len(pairs) == 17 and len(hits) == 17, (pairs, hits)

    def test_confusable_substitution_bypasses_at_every_position(self):
        confusables = {
            "F": "\uff26", "O": "\u039f", "R": "\u0280", "M": "\u039c", "A": "\u0410",
            "L": "\u029f", "D": "\u13a0", "I": "\u0130", "S": "\u0405", "P": "\u0420",
            "T": "\u0422", "N": "\u0274",
        }
        covered = [i for i in self.PREFIX_POSITIONS if _CANONICAL_ADVERSE[i] in confusables]
        hits = [
            i for i in covered
            if self._bypasses(
                _replace_at(_CANONICAL_ADVERSE, i, confusables[_CANONICAL_ADVERSE[i]])
            )
        ]
        assert len(covered) == 17 and len(hits) == 17, (covered, hits)

    def test_ordinary_prose_is_not_treated_as_a_formal_record(self):
        """The boundary's other side: prose must not become a formal candidate."""
        assert AUTH.parse_formal_disposition("just some ordinary prose\n") is None


class TestNoTautologicalAssertionsSurvive:
    """MINOR 1: the `x == y or x != y` shape must be gone AND barred from returning."""

    def test_the_real_property_is_asserted(self):
        source = Path(__file__).read_text(encoding="utf-8")
        assert "must stay non-ASCII" in source
        assert "must not become" in source

    @pytest.mark.parametrize(
        "homoglyph,ascii_char", [("\u039f", "O"), ("\u0410", "A"), ("\u0130", "I")]
    )
    def test_the_property_holds_for_each_real_lookalike(self, homoglyph, ascii_char):
        upper = homoglyph.upper()
        assert all(ord(c) > 127 for c in upper)
        assert upper != ascii_char

    @pytest.mark.parametrize("known_bad", ["o", "a", "i", "O", "A", "I"])
    def test_the_property_REJECTS_a_plain_ascii_lookalike(self, known_bad):
        """Known-bad control: an ASCII character must fail the property the assertion pins.

        This is what makes the assertion falsifiable -- the superseded tautology accepted these.
        """
        upper = known_bad.upper()
        assert not all(ord(c) > 127 for c in upper), known_bad

    def test_no_exhaustive_comparison_tautology_exists_anywhere(self):
        """AST/hygiene guard: reject `x == y or x != y` over the same operands, in any order.

        Asserted structurally rather than by substring, because the explanatory comment above
        necessarily quotes the superseded expression.
        """
        import ast

        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not (isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or)):
                continue
            cmps = [v for v in node.values if isinstance(v, ast.Compare) and len(v.ops) == 1]
            for i, a in enumerate(cmps):
                for b in cmps[i + 1 :]:
                    ops = {type(a.ops[0]).__name__, type(b.ops[0]).__name__}
                    if ops != {"Eq", "NotEq"}:
                        continue
                    same = (
                        ast.dump(a.left) == ast.dump(b.left)
                        and ast.dump(a.comparators[0]) == ast.dump(b.comparators[0])
                    )
                    assert not same, f"exhaustive tautology at line {node.lineno}"

    def test_no_assertion_is_neutered_by_a_constant_disjunct(self):
        """AST guard: reject `assert <constant-truthy> or ...`, which short-circuits the real check.

        Probe "non-ASCII property dropped" MISSED an earlier state of this suite by rewriting a
        real assertion to `assert True or all(...)`. That is vacuous in exactly the way an
        exhaustive tautology is, so it is barred by the same class of guard.
        """
        import ast

        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assert):
                continue
            test = node.test
            if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.Or):
                for v in test.values:
                    const = isinstance(v, ast.Constant) and bool(v.value)
                    assert not const, (
                        f"assertion neutered by a constant-truthy disjunct at line {node.lineno}"
                    )
            assert not (
                isinstance(test, ast.Constant) and bool(test.value)
            ), f"constant-truthy assertion at line {node.lineno}"

    def test_the_constant_disjunct_guard_actually_catches_one(self):
        """Non-vacuity for the guard above."""
        import ast

        tree = ast.parse("assert True or all(ord(c) > 127 for c in upper)\n")
        hit = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert) and isinstance(node.test, ast.BoolOp):
                for v in node.test.values:
                    if isinstance(v, ast.Constant) and bool(v.value):
                        hit = True
        assert hit, "the guard's own detector failed to fire"

    def test_the_tautology_guard_actually_catches_one(self):
        """Non-vacuity for the guard above: it must reject a real tautology."""
        import ast

        tree = ast.parse("assert x.upper() == x or x.upper() != x\n")
        found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
                cmps = [v for v in node.values if isinstance(v, ast.Compare)]
                ops = {type(c.ops[0]).__name__ for c in cmps}
                if ops == {"Eq", "NotEq"} and ast.dump(cmps[0].left) == ast.dump(cmps[1].left):
                    found = True
        assert found, "the guard's own detector failed to fire on a known tautology"


# =====================================================================================
# 9e. DELTA 5027180757 MAJOR 1 — a MECHANICAL two-lifecycle qualification model
# =====================================================================================
#
# The prior suite only searched for A/B labels and phrases. DELTA review 5027180757 MAJOR 1
# proved the consequence concretely: gutting B7 to "a CI run of some kind" left every committed
# test passing, because only the label `* B7.` was checked. What follows is a TEST-ONLY pure
# condition model that actually EVALUATES a candidate lifecycle pair conjunctively.
#
# It adds NO production authorization behaviour. `level1_stage1_execution_authorization.py` is
# untouched by this filing and is asserted byte-identical to base elsewhere in this module.


#: The decision's own enumerated steps, bound MECHANICALLY to the record rather than restated.
#: Each entry is (step_id, substantive content that must appear inside that step's own bullet).
#: If the decision renames, reorders, drops or guts a step, `test_the_model_binds_to_the_decision`
#: fails -- so the model cannot silently diverge from the authority it models.
LIFECYCLE_A_STEPS = (
    ("A1", "independent **FULL** exact-head review"),
    ("A2", "exact-head re-review"),
    ("A3", "principal exact-head acceptance"),
    ("A4", "normal merge"),
    ("A5", "post-merge verification"),
    ("A6", "successful merge-commit CI whose `head_sha` is that authorization's exact merge SHA"),
    ("A7", "final post-CI verification and lifecycle closure"),
)

LIFECYCLE_B_STEPS = (
    ("B1", "the implementation itself, correcting the defect family"),
    ("B2", "independent **FULL** exact-head review"),
    ("B3", "exact-head re-review"),
    ("B4", "principal exact-head acceptance"),
    ("B5", "normal merge"),
    ("B6", "immediate post-merge verification"),
    ("B7", "successful merge-commit CI whose `head_sha` is that implementation's exact merge SHA"),
    ("B8", "final post-CI verification and lifecycle closure"),
)


class LifecycleRecord(dict):
    """A candidate lifecycle, as a plain mapping. Test-only; no production coupling."""


def _complete_authorization_record() -> LifecycleRecord:
    """One complete, correctly ordered, exact-head / exact-merge Lifecycle A."""
    return LifecycleRecord(
        accepted_head="a" * 40,
        A1_review_present=True,
        A1_reviewed_head="a" * 40,          # anchored to the FINAL accepted head
        A2_recorrection_reviewed_head="a" * 40,
        A3_acceptance_present=True,
        A3_accepted_head="a" * 40,
        A4_merge_sha="m" * 40,
        A4_merge_parents=("p" * 40, "a" * 40),   # second parent is the accepted head
        A5_verification_present=True,
        A6_ci_present=True,
        A6_ci_conclusion="success",
        A6_ci_head_sha="m" * 40,            # equals the merge SHA
        A7_closure_present=True,
        A7_closure_names_merge_sha="m" * 40,
    )


def _complete_implementation_record() -> LifecycleRecord:
    """One complete, correctly ordered Lifecycle B, begun after A closed."""
    return LifecycleRecord(
        accepted_head="b" * 40,
        B1_implementation_present=True,
        B1_started_after_a_closure=True,
        B2_review_present=True,
        B2_reviewed_head="b" * 40,
        B3_recorrection_reviewed_head="b" * 40,
        B4_acceptance_present=True,
        B4_accepted_head="b" * 40,
        B5_merge_sha="n" * 40,
        B5_merge_parents=("q" * 40, "b" * 40),
        B6_verification_present=True,
        B7_ci_present=True,
        B7_ci_conclusion="success",
        B7_ci_head_sha="n" * 40,            # equals the B5 merge SHA
        B8_closure_present=True,
        B8_closure_names_merge_sha="n" * 40,
    )


def evaluate_lifecycle_a(rec) -> tuple[bool, tuple[str, ...]]:
    """Evaluate A1-A7 CONJUNCTIVELY. Returns (qualifies, refusal reasons)."""
    bad = []
    if not rec.get("A1_review_present"):
        bad.append("A1: no independent FULL exact-head review")
    if rec.get("A1_reviewed_head") != rec.get("accepted_head"):
        bad.append("A1: review anchored to a stale or wrong head")
    if rec.get("A2_recorrection_reviewed_head") != rec.get("accepted_head"):
        bad.append("A2: re-review does not hold at the final accepted head")
    if not rec.get("A3_acceptance_present"):
        bad.append("A3: no principal exact-head acceptance")
    if rec.get("A3_accepted_head") != rec.get("accepted_head"):
        bad.append("A3: acceptance at a different head")
    parents = rec.get("A4_merge_parents") or ()
    if not rec.get("A4_merge_sha"):
        bad.append("A4: no normal merge")
    elif len(parents) != 2 or parents[1] != rec.get("accepted_head"):
        bad.append("A4: merge is not a normal two-parent merge of the accepted head")
    if not rec.get("A5_verification_present"):
        bad.append("A5: no post-merge verification")
    if not rec.get("A6_ci_present"):
        bad.append("A6: no merge-commit CI")
    elif rec.get("A6_ci_conclusion") != "success":
        bad.append("A6: merge-commit CI did not succeed")
    elif rec.get("A6_ci_head_sha") != rec.get("A4_merge_sha"):
        bad.append("A6: CI ran against a commit other than the exact merge SHA")
    if not rec.get("A7_closure_present"):
        bad.append("A7: no final post-CI closure")
    elif rec.get("A7_closure_names_merge_sha") != rec.get("A4_merge_sha"):
        bad.append("A7: closure names a different merge SHA")
    return (not bad), tuple(bad)


def evaluate_lifecycle_b(rec, a_qualifies: bool) -> tuple[bool, tuple[str, ...]]:
    """Evaluate B1-B8 CONJUNCTIVELY, and refuse if Lifecycle A has not closed."""
    bad = []
    if not a_qualifies:
        bad.append("B: Lifecycle A has not closed; implementation may not begin")
    if not rec.get("B1_implementation_present"):
        bad.append("B1: no implementation")
    if not rec.get("B1_started_after_a_closure"):
        bad.append("B1: implementation began before Lifecycle A closed")
    if not rec.get("B2_review_present"):
        bad.append("B2: no independent FULL exact-head review")
    if rec.get("B2_reviewed_head") != rec.get("accepted_head"):
        bad.append("B2: review anchored to a stale or wrong head")
    if rec.get("B3_recorrection_reviewed_head") != rec.get("accepted_head"):
        bad.append("B3: re-review does not hold at the final accepted head")
    if not rec.get("B4_acceptance_present"):
        bad.append("B4: no principal exact-head acceptance")
    if rec.get("B4_accepted_head") != rec.get("accepted_head"):
        bad.append("B4: acceptance at a different head")
    parents = rec.get("B5_merge_parents") or ()
    if not rec.get("B5_merge_sha"):
        bad.append("B5: no normal merge")
    elif len(parents) != 2 or parents[1] != rec.get("accepted_head"):
        bad.append("B5: merge is not a normal two-parent merge of the accepted head")
    if not rec.get("B6_verification_present"):
        bad.append("B6: no immediate post-merge verification")
    if not rec.get("B7_ci_present"):
        bad.append("B7: no merge-commit CI")
    elif rec.get("B7_ci_conclusion") != "success":
        bad.append("B7: merge-commit CI did not succeed")
    elif rec.get("B7_ci_head_sha") != rec.get("B5_merge_sha"):
        bad.append("B7: CI ran against a commit other than the exact B5 merge SHA")
    if not rec.get("B8_closure_present"):
        bad.append("B8: no final post-CI closure")
    elif rec.get("B8_closure_names_merge_sha") != rec.get("B5_merge_sha"):
        bad.append("B8: closure names a different merge SHA")
    return (not bad), tuple(bad)


def qualifying_rebinding_base(a_rec, b_rec):
    """The §F.2 rule, mechanically: the base is the B5 merge, or nothing qualifies."""
    a_ok, _ = evaluate_lifecycle_a(a_rec)
    b_ok, _ = evaluate_lifecycle_b(b_rec, a_ok)
    if not (a_ok and b_ok):
        return None
    if not (b_rec["B5_merge_sha"] == b_rec["B7_ci_head_sha"] == b_rec["B8_closure_names_merge_sha"]):
        return None
    return b_rec["B5_merge_sha"]


#: Every A-condition, and the mutation that must drive it false.
A_MUTATIONS = (
    ("A1 absent", {"A1_review_present": False}),
    ("A1 stale reviewed head", {"A1_reviewed_head": "z" * 40}),
    ("A2 re-review at wrong head", {"A2_recorrection_reviewed_head": "z" * 40}),
    ("A3 absent", {"A3_acceptance_present": False}),
    ("A3 at wrong head", {"A3_accepted_head": "z" * 40}),
    ("A4 no merge", {"A4_merge_sha": None}),
    ("A4 not a two-parent merge", {"A4_merge_parents": ("p" * 40,)}),
    ("A4 merge of a different head", {"A4_merge_parents": ("p" * 40, "z" * 40)}),
    ("A5 no verification", {"A5_verification_present": False}),
    ("A6 CI missing", {"A6_ci_present": False}),
    ("A6 CI failed", {"A6_ci_conclusion": "failure"}),
    ("A6 CI on the wrong SHA", {"A6_ci_head_sha": "z" * 40}),
    ("A7 no closure", {"A7_closure_present": False}),
    ("A7 closure names wrong SHA", {"A7_closure_names_merge_sha": "z" * 40}),
)

#: Every B-condition, and the mutation that must drive it false.
B_MUTATIONS = (
    ("B1 absent", {"B1_implementation_present": False}),
    ("B1 began before A closed", {"B1_started_after_a_closure": False}),
    ("B2 absent", {"B2_review_present": False}),
    ("B2 stale reviewed head", {"B2_reviewed_head": "z" * 40}),
    ("B3 re-review at wrong head", {"B3_recorrection_reviewed_head": "z" * 40}),
    ("B4 absent", {"B4_acceptance_present": False}),
    ("B4 at wrong head", {"B4_accepted_head": "z" * 40}),
    ("B5 no merge", {"B5_merge_sha": None}),
    ("B5 not a two-parent merge", {"B5_merge_parents": ("q" * 40,)}),
    ("B5 merge of a different head", {"B5_merge_parents": ("q" * 40, "z" * 40)}),
    ("B6 no verification", {"B6_verification_present": False}),
    ("B7 CI missing", {"B7_ci_present": False}),
    ("B7 CI failed", {"B7_ci_conclusion": "failure"}),
    ("B7 CI on the wrong SHA", {"B7_ci_head_sha": "z" * 40}),
    ("B8 no closure", {"B8_closure_present": False}),
    ("B8 closure names wrong SHA", {"B8_closure_names_merge_sha": "z" * 40}),
)


class TestTheTwoLifecycleQualificationModel:
    """MAJOR 1: a model that EVALUATES, not a search for labels."""

    # ---- the model is bound to the decision, not restated beside it ----

    @pytest.mark.parametrize("step,content", LIFECYCLE_A_STEPS + LIFECYCLE_B_STEPS)
    def test_the_model_binds_to_the_decisions_exact_steps(self, decision_text, step, content):
        """Each modelled step must exist in the decision AND carry its substantive content.

        This is what closes MAJOR 1's B-step gap: gutting B7 while leaving `* B7.` in place now
        fails here, because the CI/exact-merge-SHA content is pinned inside B7's own bullet.
        """
        f = _section(decision_text, "F")
        marker = f"* {step}."
        assert marker in f, step
        body = f[f.index(marker) :]
        body = body[: body.index("\n*")] if "\n*" in body else body
        assert _flat(content) in _flat(body), (step, _flat(body)[:200])

    def test_the_model_covers_every_step_the_decision_enumerates(self, decision_text):
        """Non-vacuity: the model must not silently omit a step the decision defines."""
        f = _section(decision_text, "F")
        declared = set(re.findall(r"^\* (A\d|B\d)\.", f, re.M))
        modelled = {s for s, _ in LIFECYCLE_A_STEPS + LIFECYCLE_B_STEPS}
        assert declared == modelled, (declared ^ modelled)
        assert len(modelled) == 15, len(modelled)

    # ---- the all-true control qualifies ----

    def test_a_complete_correctly_ordered_pair_qualifies(self):
        a, b = _complete_authorization_record(), _complete_implementation_record()
        a_ok, a_bad = evaluate_lifecycle_a(a)
        b_ok, b_bad = evaluate_lifecycle_b(b, a_ok)
        assert a_ok, a_bad
        assert b_ok, b_bad
        assert qualifying_rebinding_base(a, b) == "n" * 40

    # ---- every condition, independently driven false, must refuse ----

    @pytest.mark.parametrize("label,mutation", A_MUTATIONS)
    def test_every_authorization_condition_is_load_bearing(self, label, mutation):
        a = _complete_authorization_record()
        a.update(mutation)
        ok, reasons = evaluate_lifecycle_a(a)
        assert not ok, f"{label} still qualified"
        assert reasons, label
        # and B must refuse too, because A did not close
        b_ok, b_reasons = evaluate_lifecycle_b(_complete_implementation_record(), ok)
        assert not b_ok and any("Lifecycle A has not closed" in r for r in b_reasons), label
        assert qualifying_rebinding_base(a, _complete_implementation_record()) is None, label

    @pytest.mark.parametrize("label,mutation", B_MUTATIONS)
    def test_every_implementation_condition_is_load_bearing(self, label, mutation):
        a = _complete_authorization_record()
        b = _complete_implementation_record()
        b.update(mutation)
        a_ok, _ = evaluate_lifecycle_a(a)
        assert a_ok
        ok, reasons = evaluate_lifecycle_b(b, a_ok)
        assert not ok, f"{label} still qualified"
        assert reasons, label
        assert qualifying_rebinding_base(a, b) is None, label

    # ---- the named disqualifying cases, driven through the model ----

    def test_a_stale_reviewed_head_is_refused(self):
        a = _complete_authorization_record(); a["A1_reviewed_head"] = "z" * 40
        ok, reasons = evaluate_lifecycle_a(a)
        assert not ok and any("stale or wrong head" in r for r in reasons), reasons

    def test_a_wrong_merge_sha_is_refused(self):
        b = _complete_implementation_record(); b["B7_ci_head_sha"] = "z" * 40
        ok, reasons = evaluate_lifecycle_b(b, True)
        assert not ok and any("exact B5 merge SHA" in r for r in reasons), reasons

    def test_missing_or_failed_exact_merge_ci_is_refused(self):
        for mut, frag in (
            ({"A6_ci_present": False}, "no merge-commit CI"),
            ({"A6_ci_conclusion": "failure"}, "did not succeed"),
        ):
            a = _complete_authorization_record(); a.update(mut)
            ok, reasons = evaluate_lifecycle_a(a)
            assert not ok and any(frag in r for r in reasons), (mut, reasons)

    def test_missing_verification_or_closure_is_refused(self):
        for mut, frag in (
            ({"A5_verification_present": False}, "no post-merge verification"),
            ({"A7_closure_present": False}, "no final post-CI closure"),
        ):
            a = _complete_authorization_record(); a.update(mut)
            ok, reasons = evaluate_lifecycle_a(a)
            assert not ok and any(frag in r for r in reasons), (mut, reasons)

    def test_implementation_beginning_before_a_closes_is_refused(self):
        b = _complete_implementation_record(); b["B1_started_after_a_closure"] = False
        ok, reasons = evaluate_lifecycle_b(b, True)
        assert not ok and any("began before Lifecycle A closed" in r for r in reasons), reasons

    def test_a_merged_but_ineffective_authorization_cannot_qualify(self):
        """The exact XASSET-0045 shape: merged, but merge-CI failed and closure never recorded."""
        a = _complete_authorization_record()
        a.update({"A6_ci_conclusion": "failure", "A7_closure_present": False})
        assert a["A4_merge_sha"], "the authorization DID merge -- that is the point"
        ok, reasons = evaluate_lifecycle_a(a)
        assert not ok
        assert any("did not succeed" in r for r in reasons)
        assert any("no final post-CI closure" in r for r in reasons)
        assert qualifying_rebinding_base(a, _complete_implementation_record()) is None

    # ---- the §F.2 base rule, mechanically ----

    def test_only_the_b5_merge_qualifies_as_the_base(self):
        a, b = _complete_authorization_record(), _complete_implementation_record()
        base = qualifying_rebinding_base(a, b)
        assert base == b["B5_merge_sha"]
        assert base != a["A4_merge_sha"], "the Lifecycle A authorization merge must NOT qualify"

    @pytest.mark.parametrize(
        "candidate,why",
        [
            ("m" * 40, "the Lifecycle A authorization merge"),
            ("p" * 40, "a pre-implementation commit"),
            ("d" * 40, "a later descendant"),
            ("u" * 40, "an unrelated or intervening main commit"),
        ],
    )
    def test_no_other_commit_can_serve_as_the_base(self, candidate, why):
        a, b = _complete_authorization_record(), _complete_implementation_record()
        assert qualifying_rebinding_base(a, b) != candidate, why

    def test_b5_b7_and_b8_must_name_the_same_commit(self):
        for field in ("B7_ci_head_sha", "B8_closure_names_merge_sha"):
            b = _complete_implementation_record(); b[field] = "z" * 40
            assert qualifying_rebinding_base(_complete_authorization_record(), b) is None, field

    # ---- falsifiability of the model itself ----

    def test_the_model_is_conjunctive_not_disjunctive(self):
        """Two independent failures must both be reported, not short-circuited to one."""
        a = _complete_authorization_record()
        a.update({"A5_verification_present": False, "A7_closure_present": False})
        ok, reasons = evaluate_lifecycle_a(a)
        assert not ok and len(reasons) >= 2, reasons

    def test_the_model_adds_no_production_behaviour(self):
        """Test-only: the model must not be imported from, or exist in, the production module."""
        for name in ("evaluate_lifecycle_a", "evaluate_lifecycle_b", "qualifying_rebinding_base"):
            assert not hasattr(AUTH, name), name

    def test_the_mutation_tables_cover_every_modelled_step(self):
        """Non-vacuity: no modelled step may be left without a refusal mutation."""
        covered = {lbl.split()[0] for lbl, _ in A_MUTATIONS + B_MUTATIONS}
        modelled = {s for s, _ in LIFECYCLE_A_STEPS + LIFECYCLE_B_STEPS}
        assert modelled <= covered, modelled - covered


# =====================================================================================
# 10. The register is synchronized, additively
# =====================================================================================


class TestTheRegisterIsSynchronized:
    def test_this_units_gate_exists(self, register):
        gates = [g["gate"] for g in register["milestones"]]
        assert THIS_GATE in gates

    def test_the_predecessor_gate_text_is_untouched(self):
        """XASSET-0056's own gate is recorded additively, never rewritten."""
        base_doc = yaml.safe_load(
            _content_at(THIS_UNIT_BASE_SHA, "operations/WORKSTREAMS.yaml").decode("utf-8")
        )
        base_ws = next(w for w in base_doc["workstreams"] if w["id"] == "WS-0014")
        base_gate = next(
            g
            for g in base_ws["milestones"]
            if g["gate"] == "xasset0056-formal-disposition-parser-correction"
        )
        live_doc = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
        live_ws = next(w for w in live_doc["workstreams"] if w["id"] == "WS-0014")
        live_gate = next(
            g
            for g in live_ws["milestones"]
            if g["gate"] == "xasset0056-formal-disposition-parser-correction"
        )
        assert live_gate == base_gate, "a predecessor gate was rewritten instead of appended to"

    def test_gates_are_only_appended(self, register):
        base_doc = yaml.safe_load(
            _content_at(THIS_UNIT_BASE_SHA, "operations/WORKSTREAMS.yaml").decode("utf-8")
        )
        base_ws = next(w for w in base_doc["workstreams"] if w["id"] == "WS-0014")
        before = base_ws["milestones"]
        live = register["milestones"]
        assert live[: len(before)] == before, "existing gates were modified, not appended to"
        assert len(live) > len(before)

    def test_no_sentinel_survives_anywhere_in_the_register(self):
        raw = WORKSTREAMS.read_text(encoding="utf-8")
        for sentinel in (PR_SENTINEL, *PRIOR_SENTINELS):
            assert f"active_pr: {sentinel}" not in raw, sentinel
            assert f"pr: {sentinel}" not in raw, sentinel

    def test_the_shared_live_fields_name_this_unit(self, register):
        assert register["active_branch"] == BRANCH
        assert register["last_verified_main_sha"] == THIS_UNIT_BASE_SHA
        assert register["active_branch"] != "claude/xasset-0055-parser-correction-c3ro29"
        assert register["last_verified_main_sha"] != XASSET_0056_MERGE_PARENT_1

    def test_this_units_gate_carries_a_real_or_pending_number(self, register):
        gate = next(g for g in register["milestones"] if g["gate"] == THIS_GATE)
        pr = gate["pr"]
        assert pr is None or pr > CLOSED_PULL_REQUEST
        assert pr not in PRIOR_SENTINELS and pr != PR_SENTINEL

    def test_the_workstream_priority_is_unchanged(self, register):
        assert register["status"] == "proposed"
        assert register["priority"] == "secondary"


# =====================================================================================
# 11. Non-vacuity — these assertions can fail
# =====================================================================================


class TestNonVacuity:
    def test_the_decision_file_is_substantial(self, decision_text):
        assert len(decision_text) > 20_000
        assert decision_text.count("###") >= 13

    def test_every_asserted_section_exists(self, decision_text):
        for letter in "ABCDEFGHIJKLM":
            assert _section(decision_text, letter).strip(), letter

    def test_the_helpers_would_catch_a_wrong_identity(self):
        assert _blob_at(THIS_UNIT_BASE_SHA, "does/not/exist.py") is None
        assert not _commit_exists("0" * 40)

    def test_the_section_helper_rejects_a_missing_section(self, decision_text):
        with pytest.raises(AssertionError):
            _section(decision_text, "Z")

    def test_the_flat_helper_really_collapses(self):
        assert _flat("a\n  b\tc") == "a b c"

    def test_the_parser_probes_are_not_trivially_equal(self):
        """The reproduced and control bodies must genuinely differ."""
        tampered = _adverse_then_approval("FORMAL DISPΟSITION: CHANGES REQUIRED")
        clean = _adverse_then_approval("FORMAL DISPOSITION: CHANGES REQUIRED")
        assert tampered != clean
        assert AUTH.parse_formal_disposition(tampered) != AUTH.parse_formal_disposition(clean)


# =====================================================================================
# 14. DELTA 5027180757 MINOR 1 — the position-zero mechanism is pinned to the REAL parser
# =====================================================================================


class TestThePositionZeroInsertionFailsClosedAsMalformed:
    """DELTA review 5027180757 MINOR 1.

    §F.0.1 previously said the single non-bypassing insertion (position 0) "is read as a
    genuine adverse record". That is inaccurate. This class pins the CORRECTED claim to the
    REAL parser rather than to prose alone -- deliberately, because the review's own MAJOR 1
    was that a prose-only statement with no mechanical counterpart cannot be falsified.
    """

    #: The one insertion index that leaves the canonical prefix intact as a substring.
    POSITION_ZERO_LINE = "X" + _CANONICAL_ADVERSE

    def test_the_canonical_prefix_survives_intact_at_position_zero(self):
        """Non-vacuity: this really is the case where the prefix is NOT broken."""
        assert _CANONICAL_ADVERSE in self.POSITION_ZERO_LINE
        assert not self.POSITION_ZERO_LINE.startswith(_CANONICAL_ADVERSE)
        assert len(self.POSITION_ZERO_LINE) == len(_CANONICAL_ADVERSE) + 1

    def test_the_real_parser_returns_malformed_not_the_adverse_verdict(self):
        """The load-bearing correction: MALFORMED, not 'CHANGES REQUIRED'."""
        body = _adverse_then_approval(self.POSITION_ZERO_LINE)
        verdict = AUTH.parse_formal_disposition(body)
        # pinned by IDENTITY against the module's own sentinel, not by a string that a
        # future refactor could reproduce accidentally.
        assert verdict is AUTH.MALFORMED_FORMAL_DISPOSITION, repr(verdict)
        assert type(verdict).__name__ == "_MalformedFormalDisposition"
        # the superseded claim -- that it is read as a genuine adverse record -- is FALSE.
        assert verdict != "CHANGES REQUIRED"
        assert not isinstance(verdict, str)

    def test_it_still_does_not_bypass(self):
        """The SECURITY conclusion is unchanged: the later approval must not win."""
        body = _adverse_then_approval(self.POSITION_ZERO_LINE)
        assert AUTH.parse_formal_disposition(body) != (
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        )

    def test_it_differs_from_every_bypassing_attack(self):
        """Position zero is genuinely a different outcome class from the skip family."""
        zero = AUTH.parse_formal_disposition(
            _adverse_then_approval(self.POSITION_ZERO_LINE)
        )
        for label, ascii_char, index, homoglyph in _HOMOGLYPH_ATTACKS:
            bypassing = AUTH.parse_formal_disposition(
                _adverse_then_approval(_attack_first_line(ascii_char, index, homoglyph))
            )
            assert bypassing == "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE", label
            assert zero != bypassing, label

    def test_a_nonzero_insertion_does_break_the_prefix_and_bypasses(self):
        """Control: insertion anywhere INSIDE the prefix behaves differently."""
        broken = _CANONICAL_ADVERSE[:5] + "X" + _CANONICAL_ADVERSE[5:]
        assert _CANONICAL_ADVERSE not in broken
        assert AUTH.parse_formal_disposition(_adverse_then_approval(broken)) == (
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        )

    # ---- and the decision must STATE the corrected mechanism, not the superseded one ----

    def test_the_decision_states_the_corrected_mechanism(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert (
            "**recognized as formal-looking and fails closed as `MALFORMED`**" in f
        ), "the corrected mechanism must be stated"
        assert "`MALFORMED_FORMAL_DISPOSITION` **sentinel object**" in f
        assert "not the adverse verdict, and not a string" in f
        assert "pins it by **identity** against that sentinel" in f
        assert "the canonical prefix **survives intact as a substring**" in f

    def test_the_decision_withdraws_the_inaccurate_wording(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "withdrawn as inaccurate" in f
        # the superseded claim may appear ONLY inside its own withdrawal sentence.
        assert f.count("read as a genuine adverse record") == 1
        idx = f.index("read as a genuine adverse record")
        assert "withdrawn as inaccurate" in f[idx : idx + 400]

    def test_the_superseded_claim_is_not_stated_as_operative(self, decision_text):
        """Falsifiability guard: reverting the prose must FAIL this class."""
        f = _flat(_section(decision_text, "F"))
        assert "is **read as a genuine adverse record**" not in f
        assert "line is therefore read as a genuine adverse record" not in f
