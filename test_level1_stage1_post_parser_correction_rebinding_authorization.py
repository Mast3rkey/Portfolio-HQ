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
        f = _flat(_section(decision_text, "F"))
        assert "The operative rule is equality, not descent" in f
        assert "must **equal** the exact normal-merge commit" in f

    def test_ancestry_is_stated_necessary_but_explicitly_insufficient(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "necessary history and explicitly insufficient authority" in f
        assert "descent alone never qualifies a base" in f

    def test_any_intervening_main_commit_is_drift_and_a_stop(self, decision_text):
        f = _flat(_section(decision_text, "F"))
        assert "Any intervening `main` commit is drift, and drift is a stop" in f
        assert "may not proceed on the strength of this authorization" in f
        assert "never absorbed merely because the base descends" in f

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
_ADVERSE_TAIL = "SITION: CHANGES REQUIRED"


def _adverse_then_approval(prefix_body: str) -> str:
    return prefix_body + "\n" + _APPROVAL + "\n"


class TestTheDisclosedFindingIsReproducedAndBounded:
    """``SS-M`` claims the bot finding reproduces and is bounded. Both halves are executed here."""

    @pytest.mark.parametrize(
        "homoglyph",
        [
            "Ο",  # GREEK CAPITAL LETTER OMICRON — the reported case
            "А",  # CYRILLIC CAPITAL LETTER A
            "İ",  # LATIN CAPITAL LETTER I WITH DOT ABOVE
        ],
    )
    def test_the_reported_skip_family_reproduces(self, homoglyph):
        """A prefix-interior homoglyph makes the adverse line skip and a later approval win."""
        body = _adverse_then_approval("FORMAL DISP" + homoglyph + _ADVERSE_TAIL[1:])
        assert AUTH.parse_formal_disposition(body) == (
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        )

    def test_the_canonical_adverse_line_still_wins(self):
        """The control: an untampered adverse first line is not skipped."""
        body = _adverse_then_approval("FORMAL DISPOSITION: CHANGES REQUIRED")
        assert AUTH.parse_formal_disposition(body) == "CHANGES REQUIRED"

    def test_a_tampered_prefix_alone_never_authenticates(self):
        """The bound: the finding is a skip, never a direct authentication."""
        tampered = "FORMAL DISPΟSITION: APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE\n"
        assert AUTH.parse_formal_disposition(tampered) != (
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        )

    def test_a_homoglyph_in_the_verdict_does_not_bypass(self):
        """The bound: only the prefix is affected."""
        body = _adverse_then_approval("FORMAL DISPOSITION: CHANGЕS REQUIRED")
        assert body and AUTH.parse_formal_disposition(body) != (
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        )

    def test_a_plain_approval_still_authenticates(self):
        assert AUTH.parse_formal_disposition(_APPROVAL + "\n") == (
            "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"
        )

    def test_the_disclosure_records_the_bot_review_and_its_timing(self, decision_flat):
        assert POST_MERGE_BOT_REVIEW in decision_flat
        assert "chatgpt-codex-connector[bot]" in decision_flat
        assert "not** part of the accepted `XASSET-0056` lifecycle" in decision_flat

    def test_the_disclosure_states_all_three_consequences(self, decision_text):
        m = _flat(_section(decision_text, "M"))
        assert "does not repair it, and is not authorized to" in m
        assert "does not make Stage 1 executable" in m
        assert "bears directly on" in m and "drift rule applies" in m

    def test_the_disclosure_does_not_rule_on_the_fix(self, decision_text):
        m = _flat(_section(decision_text, "M"))
        assert "open, unresolved, and outside this grant" in m


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
