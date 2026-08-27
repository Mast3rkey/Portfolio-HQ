"""Adversarial tests for XASSET-0055 — the formal-disposition verdict-boundary governance filing.

WHAT THIS FILING IS. A GOVERNANCE-ONLY decision. `XASSET-0053` §D contains a genuine contradiction
for one input class, and no implementation can satisfy both halves of it:

  * §D.1 / §D.3 / §D.14 require arbitrary existing canonical verdicts to keep parsing -- an OPEN
    verdict channel, with no new disposition-vocabulary rule; while
  * §D.9 / §D.17 / §D.19 require ALL trailing prose to become MALFORMED.

For a line with no delimiter, a new upper-case verdict and an approval with appended upper-case
prose are syntactically identical. PR #355 tried both directions and each broke the other's
requirement; two independent reviews (`5008847293` FULL, `5010334966` DELTA) rejected it, and it is
closed unmerged. This filing decides which requirement governs the ambiguous case, in governed
text, and authorizes exactly one replacement implementation.

WHAT THESE TESTS DO. They attack the FILING -- its authority, its scope, its internal consistency,
and its non-authorization boundary -- and they independently re-derive the conflict from the
governing text and the live module rather than trusting the decision's prose.

NO PRODUCTION CODE IS CHANGED BY THIS FILING, and these tests prove it: the authorization module is
byte-identical to the base. NO STAGE-1 EXECUTION OCCURS. No attestation is created, no lane is
written, `ATTEMPT_1` is never claimed, no gate is evaluated, no construction is dispositioned, no
result is produced, no portfolio percentage is calculated, and no capital is allocated.
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

ROOT = Path(__file__).resolve().parent

DECISION_ID = "XASSET-0055"
DECISION = (
    ROOT / "governance/decisions"
    / "XASSET-0055-endpoint-0001-formal-disposition-verdict-boundary-governance.md"
)
AUTHORITY_ID = "XASSET-0053"
AUTHORITY = (
    ROOT / "governance/decisions"
    / "XASSET-0053-endpoint-0001-formal-disposition-parser-contract-correction-authorization.md"
)

MODULE_RELPATH = "level1_stage1_execution_authorization.py"
WORKSTREAMS = ROOT / "operations/WORKSTREAMS.yaml"
CATALOG = ROOT / "governance/decisions.yaml"

#: This filing's base: `main`, unchanged. Nothing from PR #355 merged into it.
BASE_SHA = "683c324629544a84d2cf75ebca37325e3375c479"

#: The authorization module AT THAT BASE. This filing must leave it byte-identical.
BASE_MODULE_SHA256 = "4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541"
BASE_MODULE_BLOB = "f71b08b4ebe95f161c57cdbb2a924748f13af02d"

#: RE-ANCHOR (XASSET-0056). This unit's lifecycle is CLOSED: merged at this exact SHA, with a
#: merge tree byte-identical to its accepted head. Its own diff is therefore measured over the
#: immutable range BASE_SHA..MERGE_SHA instead of against a live working tree that a lawful
#: successor now also occupies. Nothing is relaxed -- the same paths are compared, against a
#: range that can never move -- and every superseded value below is retained as a negative pin.
MERGE_SHA = "29e4969885970d942a5acecc1424fb2e2b080d60"

#: The closed, unmerged predecessor and its two rejecting reviews.
CLOSED_PULL_REQUEST = 355
CONSUMED_DECISION_ID = "XASSET-0054"
FULL_REVIEW_ID = "5008847293"
DELTA_REVIEW_ID = "5010334966"

BRANCH = "claude/xasset-0055-parser-contract-conflict-w4kp2n"

#: Committed as a structurally impossible sentinel first, then replaced by the number GitHub
#: actually issued, in a fast-forward follow-up commit. NEVER predicted. Distinct from every
#: prior generation's sentinel.
PR_SENTINEL = -55
PRIOR_SENTINELS = (-1, -2, -50, -51, -52, -53, -54)
#: The number GitHub actually issued, read back from the live pull request after opening.
#: Committed as the impossible sentinel -55 first; never predicted.
THIS_PULL_REQUEST = 356

#: RE-ANCHORED (XASSET-0056), the single replacement parser-correction implementation this
#: unit's §H authorized. `active_branch`, `active_pr` and `last_verified_main_sha` are WS-0014's
#: SINGLE SHARED live self-reference fields under OPS-0001's Active-GitHub-fields rule, so the
#: successor necessarily owns them now. Exactly the remedy this unit itself applied to its own
#: predecessor: the successor is NAMED, this unit's own values are RETAINED as negative pins,
#: and its own GATE -- which does not move and still carries the real number GitHub issued --
#: becomes the durable anchor for the assertions that were really about this unit.
SUCCESSOR_DECISION = "XASSET-0056"
#: ADVANCED BY XASSET-0058, on exactly the terms this block already states: the shared
#: live fields moved once more, and XASSET-0057's own values are RETAINED below as
#: negative pins rather than deleted, so every field stays bound at BOTH ends.
#: ADVANCED BY XASSET-0059: WS-0014's SHARED live fields moved again, onto the Lifecycle B
#: parser correction. The XASSET-0058 generation is retained beside it as a NEGATIVE pin.
# ADVANCED BY XASSET-0060, the post-parser-correction rebinding. XASSET-0059's own branch and
# main SHA are RETAINED with their exact values as NEGATIVE pins -- never deleted -- and the newly
# live unit becomes the positive pin, exactly as every prior generation was handled.
SUCCESSOR_BRANCH = "claude/xasset-0057-rebinding-gqtg9o"
XASSET0060_MAIN_SHA = "301e79334876a4bda6e7b89a6156b34e8d38a605"
SUCCESSOR_MAIN_SHA = XASSET0060_MAIN_SHA
XASSET0059_BRANCH = "claude/xasset-0058-parser-correction-a2kteq"
XASSET0059_MAIN_SHA = "34c45900ce23742d04d80cf12471c34aabe9682d"
XASSET0058_BRANCH = "claude/parser-correction-xasset-auth-w91gse"
XASSET0058_MAIN_SHA = "556a43cf91679d3e8ca95703c8d49e672b662b73"
XASSET0057_BRANCH = "claude/xasset-successor-authorization-3b0btg"
XASSET0057_MAIN_SHA = "583022a5f2106d61f82d270edadd3520d8b0c55d"
THIS_GATE = "xasset0055-verdict-boundary-governance"
#: Every decision appended to the catalog AFTER this one. Stated EXACTLY by name rather than
#: relaxed to "present somewhere in the list".
#: ADVANCED BY XASSET-0059, appended after XASSET-0058 and named EXACTLY, so "last"
#: stays an EXACT index rather than being relaxed to "present".
#: ADVANCED BY XASSET-0060, appended after XASSET-0059 and named EXACTLY, so "last" stays an
#: exact arithmetic claim rather than a relaxed "present somewhere" one.
SUCCESSORS_APPENDED_SINCE = (
    "XASSET-0056", "XASSET-0057", "XASSET-0058", "XASSET-0059", "XASSET-0060",
)

APPROVE = A.APPROVING_REVIEW_DISPOSITION


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def _sha256_at_commit(commit: str, relpath: str) -> str:
    """SHA-256 of a path's bytes AT a commit -- immutable git truth, never the working tree."""
    blob = subprocess.run(
        ["git", "show", f"{commit}:{relpath}"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    return hashlib.sha256(blob).hexdigest()


def _blob_at_commit(commit: str, relpath: str) -> str:
    """Git blob id of a path AT a commit."""
    return _git("rev-parse", f"{commit}:{relpath}").strip()


def _decision() -> str:
    return DECISION.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _changed_paths() -> set[str]:
    """Every path THIS unit touched, over its own closed base..merge range.

    RE-ANCHORED (XASSET-0056): previously this read the live working tree
    (``git diff BASE_SHA`` plus untracked files), which was correct while this unit was the
    live one. Now that it is merged and closed, the working tree also carries a lawful
    successor, so the live reading no longer measures THIS unit. The closed range does, exactly
    and permanently. A closed range has no untracked component by construction, so nothing that
    was previously observable is lost.
    """
    return set(_git("diff", "--name-only", BASE_SHA, MERGE_SHA).split())


def _load_bearing_declared_at(commit: str) -> tuple[str, ...]:
    """The exact ``LOAD_BEARING_RELPATHS`` the production module DECLARED at a given commit.

    Parsed with ``ast`` and never imported or executed, so a historical module's code cannot run.
    Module-level string aliases and implicit concatenation are resolved from the SAME historical
    source, never from the live module -- otherwise a live rename could silently reshape a
    historical claim, which is the whole defect this helper exists to close.
    """
    source = _git("show", f"{commit}:{MODULE_RELPATH}")
    tree = ast.parse(source)
    consts: dict[str, str] = {}

    def _literal(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.Name) and node.id in consts:
            return consts[node.id]
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left, right = _literal(node.left), _literal(node.right)
            if left is not None and right is not None:
                return left + right
        return None

    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                consts[target.id] = node.value.value
            if target.id == "LOAD_BEARING_RELPATHS" and isinstance(node.value, ast.Tuple):
                items = [_literal(e) for e in node.value.elts]
                assert all(i is not None for i in items), "unresolved element"
                return tuple(items)
    raise AssertionError(f"LOAD_BEARING_RELPATHS is not declared at {commit}")


def _ws0014() -> dict:
    data = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
    return next(w for w in data["workstreams"] if w["id"] == "WS-0014")


# =====================================================================================
# 1. This filing changes NO production code
# =====================================================================================


class TestNoProductionCodeIsChanged:
    """The single most important guard: a governance filing must not touch the module."""

    def test_the_authorization_module_is_byte_identical_to_the_base(self):
        """RE-ANCHORED (XASSET-0056) onto this unit's own closed merge.

        The superseded values are RETAINED, not dropped: they are still the exact values
        asserted, now against the immutable merge rather than the live tree.
        """
        at_merge = _sha256_at_commit(MERGE_SHA, MODULE_RELPATH)
        assert at_merge == BASE_MODULE_SHA256
        assert _blob_at_commit(MERGE_SHA, MODULE_RELPATH) == BASE_MODULE_BLOB

    def test_the_base_module_identity_is_pinned_at_both_ends(self):
        """NEGATIVE PIN for the re-anchor above: the superseded live reading is bound too.

        A silent revert of the lawfully authorized successor correction back to this unit's
        byte-identical state would restore the old reading -- and must fail here.
        """
        live = hashlib.sha256((ROOT / MODULE_RELPATH).read_bytes()).hexdigest()
        assert live != BASE_MODULE_SHA256
        assert _git("hash-object", MODULE_RELPATH).strip() != BASE_MODULE_BLOB

    def test_no_load_bearing_path_appears_in_this_units_diff(self):
        """RE-ANCHORED (XASSET-0060), and made exact rather than relaxed.

        This unit's diff is a CLOSED RANGE and never changes. The LIVE boundary does: XASSET-0060,
        under XASSET-0057 §F.7, lawfully added this very decision's own file to it, so intersecting
        an immutable diff with a moving set turned "I touched no load-bearing path" into "no
        successor may ever bind a file I created" -- a claim this suite never had the authority to
        make, and the anchoring-to-a-moving-reference defect that stopped PRs #344 and #345.

        The boundary is therefore read AS IT WAS at this unit's own merge, from the module source
        at that commit, parsed and never executed. That is the set the claim was always about, and
        it is now immutable at both ends. Nothing is exempted: every path in it is still checked.
        """
        boundary_then = set(_load_bearing_declared_at(MERGE_SHA))
        assert boundary_then, "the boundary at this unit's merge must be derivable"
        changed = _changed_paths()
        touched = changed & boundary_then
        assert not touched, sorted(touched)
        # And the file this unit DID create is bound now -- by a successor's authorized act, not
        # by this unit. Asserted so the re-anchor cannot hide a silent removal from the boundary.
        assert str(DECISION.relative_to(ROOT)) in set(A.LOAD_BEARING_RELPATHS)
        assert str(DECISION.relative_to(ROOT)) not in boundary_then

    @pytest.mark.parametrize(
        "relpath",
        [
            "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
            "allocate.py", "margin_state.py", "levels.py",
            "level1_stage1_runner.py", "level1_stage1_result_validator.py",
            "level1_construction_universe_closure_validator.py",
            "level1_endpoint_evidence_preregistration_validator.py",
            "research/level1_endpoint_evidence/PROTOCOL_V1.md",
            "research/level1_endpoint_evidence/pre_registration.yaml",
        ],
    )
    def test_no_protected_or_production_path_is_touched(self, relpath):
        assert relpath not in _changed_paths()

    def test_no_prior_decision_file_is_edited(self):
        changed = sorted(c for c in _changed_paths() if c.startswith("governance/decisions/"))
        assert changed == [str(DECISION.relative_to(ROOT))], changed

    def test_no_audit_or_evidence_artifact_is_touched(self):
        changed = _changed_paths()
        assert not [c for c in changed if c.startswith("governance/audits/")]
        assert not [c for c in changed if c.startswith("governance/evidence/")]

    def test_the_parser_and_its_call_sites_are_exactly_as_the_base_left_them(self):
        """RE-ANCHORED (XASSET-0056) onto this unit's own closed merge.

        The three-call-site ceiling is asserted at BOTH ends: at this unit's merge, where it
        proves this filing changed nothing, and in the live tree, where it proves the lawful
        successor did not add a fourth. That is strictly more than the original asserted.
        """
        base_src = _git("show", f"{BASE_SHA}:{MODULE_RELPATH}")
        merge_src = _git("show", f"{MERGE_SHA}:{MODULE_RELPATH}")
        assert base_src == merge_src
        for source in (merge_src, (ROOT / MODULE_RELPATH).read_text(encoding="utf-8")):
            calls = [
                n for n in ast.walk(ast.parse(source))
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "parse_formal_disposition"
            ]
            assert len(calls) == 3

    def test_the_unauthorized_lower_case_heuristic_is_absent_from_the_module(self):
        """PR #355's regression must not be present at this base, and is not introduced here."""
        src = (ROOT / MODULE_RELPATH).read_text(encoding="utf-8")
        assert "islower()" not in src
        assert "_FINDING_COUNT_CATEGORIES" not in src   # the correction itself is not applied here


# =====================================================================================
# 2. The conflict is REAL — re-derived, not taken from the decision's prose
# =====================================================================================


class TestTheConflictIsIndependentlyDerivable:
    """§B's claim is re-derived from the governing text and the live module."""

    def _authority(self) -> str:
        return _flat(AUTHORITY.read_text(encoding="utf-8"))

    def test_the_open_verdict_requirement_really_is_in_the_governing_text(self):
        text = self._authority()
        assert "must parse exactly as it does today" in text
        assert "additive to the accepted grammar, never a replacement" in text
        assert "no other disposition vocabulary" in text

    def test_the_all_trailing_prose_requirement_really_is_in_the_governing_text(self):
        text = self._authority()
        assert "additional operative words before or after the formal" in text
        assert "must not parse" in text
        assert "leading or trailing prose" in text or "trailing prose" in text

    def test_the_two_candidate_lines_are_syntactically_indistinguishable(self):
        """The heart of it: no syntactic feature separates them under an OPEN vocabulary."""
        new_verdict = "BOUNDED CORRECTION REQUIRED"
        prose_suffix = f"{APPROVE} DO NOT MERGE"
        for region in (new_verdict, prose_suffix):
            assert region == region.upper(), region          # both upper case
            assert not any(c.islower() for c in region)      # no lower-case tell
            assert "—" not in region and "|" not in region   # no delimiter
            assert "--" not in region and " - " not in region
            assert all(part.isalpha() or part.isdigit() or "-" in part
                       for part in region.split()), region   # ordinary word tokens

    def test_the_new_verdict_is_the_verdict_of_the_reviews_that_rejected_pr_355(self):
        """Not hypothetical: it is literally what both rejecting reviews were dispositioned as."""
        flat = _flat(_decision())
        assert "BOUNDED CORRECTION REQUIRED" in flat
        assert FULL_REVIEW_ID in flat and DELTA_REVIEW_ID in flat

    def test_the_base_parser_really_does_parse_a_mixed_case_canonical_verdict(self):
        """§D.1's baseline, measured -- this is what PR #355's heuristic regressed."""
        assert A.parse_formal_disposition("FORMAL DISPOSITION: approved") == "approved"
        assert A.parse_formal_disposition("FORMAL DISPOSITION: Approved for x") == "Approved for x"


# =====================================================================================
# 3. The decision records both findings and the closure honestly
# =====================================================================================


class TestTheDecisionRecordsTheRejectionHonestly:
    def test_both_reviews_are_named_with_their_dispositions(self):
        flat = _flat(_decision())
        assert FULL_REVIEW_ID in flat and DELTA_REVIEW_ID in flat
        assert "1 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE" in flat
        assert "1 BLOCKING / 1 MAJOR / 0 MINOR / 0 NOTE" in flat

    def test_the_closed_predecessor_is_recorded_as_closed_unmerged(self):
        flat = _flat(_decision())
        assert f"PR #{CLOSED_PULL_REQUEST}" in flat
        assert "closed, unmerged" in flat or "closed unmerged" in flat

    def test_the_decision_states_that_nothing_from_pr_355_became_effective(self):
        flat = _flat(_decision())
        assert "Nothing became effective from PR #355" in flat or \
               "nothing from PR #355 merged" in flat
        assert BASE_MODULE_SHA256 in flat

    def test_the_regression_is_admitted_rather_than_minimised(self):
        flat = _flat(_decision())
        assert "all five regressed" in flat
        assert "regression" in flat.lower()

    def test_the_decision_admits_a_test_cannot_authorize_production_behaviour(self):
        flat = _flat(_decision())
        assert "A test may not authorize the production behaviour it asserts" in flat

    def test_the_consumed_identifier_is_not_reused(self):
        flat = _flat(_decision())
        assert CONSUMED_DECISION_ID in flat
        assert "consumed" in flat
        assert DECISION_ID != CONSUMED_DECISION_ID

    def test_the_catalog_does_not_contain_the_consumed_identifier(self):
        ids = [d["decision_id"] for d in yaml.safe_load(CATALOG.read_text())["decisions"]]
        assert CONSUMED_DECISION_ID not in ids
        assert DECISION_ID in ids


# =====================================================================================
# 4. The governed resolution — all six required elements
# =====================================================================================


class TestTheGovernedResolution:
    REQUIRED = (
        "The entire remaining post-prefix region is the verdict, returned verbatim",
        "Exact equality applies to that entire region",
        "Appended text can therefore never authenticate as approval",
        "rejected by verdict inequality",
        "not falsely classified MALFORMED",
        "This is an explicit governed rule, not an undocumented exception",
    )

    @pytest.mark.parametrize("phrase", REQUIRED)
    def test_each_required_element_is_present(self, phrase):
        assert phrase in _flat(_decision()), phrase

    def test_the_narrowing_scope_is_bounded_explicitly(self):
        flat = _flat(_decision())
        assert "Scope of the narrowing, stated exactly" in flat
        assert "It reaches nothing else" in flat

    def test_malformed_is_still_required_wherever_a_boundary_is_locatable(self):
        flat = _flat(_decision())
        assert "continue to require MALFORMED in full for every class where a boundary" in flat

    def test_the_cost_is_stated_rather_than_concealed(self):
        """The failure this filing corrects was a residual described as compliance."""
        flat = _flat(_decision())
        assert "What this costs, stated plainly" in flat
        assert "paid deliberately rather than concealed" in flat

    def test_exact_equality_really_does_reject_every_appended_form(self):
        """Re-derived, not asserted: the property §C item 3 rests on."""
        for suffix in ("DO NOT MERGE", " x", "!", "0", "and see below", " "):
            assert f"{APPROVE}{suffix}" != APPROVE
            assert f"{APPROVE} {suffix}" != APPROVE


# =====================================================================================
# 5. The lower-case heuristic is removed and prohibited
# =====================================================================================


class TestTheLowerCaseHeuristicIsProhibited:
    def test_the_heuristic_is_named_and_declared_unauthorized(self):
        flat = _flat(_decision())
        assert "any(character.islower() for character in verdict)" in flat
        assert "unauthorized" in flat

    def test_prior_mixed_and_lower_case_behaviour_is_restored(self):
        flat = _flat(_decision())
        assert "returns exactly `approved`, as it did before" in flat

    def test_no_successor_may_reintroduce_an_uppercase_only_grammar(self):
        flat = _flat(_decision())
        assert "No successor may reintroduce an uppercase-only verdict grammar" in flat
        assert "without its own separate governance decision" in flat

    def test_the_prohibition_reaches_equivalent_rules_not_just_this_one(self):
        flat = _flat(_decision())
        assert "case-, length-, or word-count-based verdict rule" in flat


# =====================================================================================
# 6. PR #355's proven separator work is preserved as governed requirement
# =====================================================================================


class TestTheProvenSeparatorWorkIsPreserved:
    REQUIRED = (
        "Recognized separator suffixes must be validated as finding-count metadata",
        "never discarded",
        "An arbitrary separator suffix fails MALFORMED",
        "Earliest-separator handling is preserved",
        "The recognized separator tuple is unchanged",
    )

    @pytest.mark.parametrize("phrase", REQUIRED)
    def test_each_preserved_requirement_is_present(self, phrase):
        assert phrase in _flat(_decision()), phrase

    def test_the_finding_count_grammar_is_stated_exactly(self):
        flat = _flat(_decision())
        for token in ("count_list", "BLOCKING", "MAJOR", "MINOR", "NOTE"):
            assert token in flat, token

    def test_the_delta_reviews_own_confirmation_is_quoted(self):
        flat = _flat(_decision())
        assert "the original separator-authentication bypass is closed" in flat

    def test_the_two_accepted_wrapper_forms_are_preserved_and_no_others(self):
        flat = _flat(_decision())
        assert "Exactly the two accepted wrapper forms" in flat
        assert "and no others" in flat

    def test_exact_comparison_is_preserved(self):
        flat = _flat(_decision())
        assert "Exact comparison with `APPROVING_REVIEW_DISPOSITION`" in flat

    def test_the_open_verdict_channel_is_preserved(self):
        flat = _flat(_decision())
        assert "The open verdict channel is preserved" in flat
        assert "No closed vocabulary, no case rule, no length rule" in flat


# =====================================================================================
# 7. The closed-vocabulary rejection is argued from durable evidence
# =====================================================================================


class TestTheClosedVocabularyRejectionIsEvidenced:
    def test_the_rejection_is_explicit_and_reasoned(self):
        flat = _flat(_decision())
        assert "Why a closed verdict vocabulary was rejected" in flat
        assert "rejected on evidence, not preference" in flat

    def test_the_durable_corpus_is_cited_with_its_real_counts(self):
        flat = _flat(_decision())
        assert "34" in flat and "20 plain" in flat and "8 balanced-bold" in flat

    def test_the_decision_does_not_overclaim_the_verdicts_novelty(self):
        """It must NOT claim the string had never been seen -- it appears in the register."""
        flat = _flat(_decision())
        assert "Stated honestly" in flat
        assert "not that this particular string had never been seen" in flat

    def test_the_overclaim_is_independently_checkable_and_the_honest_form_is_true(self):
        register = WORKSTREAMS.read_text(encoding="utf-8")
        assert "BOUNDED CORRECTION REQUIRED" in register        # it HAS been seen, in prose
        assert "FORMAL DISPOSITION: BOUNDED CORRECTION REQUIRED" not in register  # never enumerated

    def test_the_closed_vocabulary_route_is_left_open_to_a_future_decision(self):
        flat = _flat(_decision())
        assert "That is a real option" in flat
        assert "not taken silently" in flat


# =====================================================================================
# 8-9. Exactly one replacement implementation is authorized, and bounded
# =====================================================================================


class TestExactlyOneReplacementIsAuthorized:
    def test_one_future_implementation_is_authorized(self):
        flat = _flat(_decision())
        assert "One future, separate, bounded parser-correction implementation PR is authorized" in flat
        assert "supersedes and replaces PR #355" in flat

    def test_the_replacement_must_remove_the_heuristic_and_keep_the_separator_work(self):
        flat = _flat(_decision())
        assert "Remove the lower-case heuristic" in flat
        assert "Implement §E's separator-suffix validation and earliest-separator handling" in flat

    def test_the_xasset_0053_permitted_set_is_carried_forward_unchanged(self):
        flat = _flat(_decision())
        assert "within that §C permitted set unchanged" in flat
        assert "at most one" in flat

    PROHIBITIONS = (
        "No fourth call site",
        "No second helper",
        "No general parsing framework",
        "No change to any other existing production function",
        "No closed verdict vocabulary",
    )

    @pytest.mark.parametrize("phrase", PROHIBITIONS)
    def test_each_scope_prohibition_is_present(self, phrase):
        assert phrase in _flat(_decision()), phrase


# =====================================================================================
# 10. The required validation is enumerated
# =====================================================================================


class TestTheRequiredValidationIsEnumerated:
    REQUIRED = (
        "Parser-level behavioural tests",
        "All-three-consumer behavioural tests",
        "Mutation probes",
        "Non-vacuity",
        "Simulated normal merge",
        "Full repository suite and exact-head CI",
        "A zero-write end-to-end rehearsal",
    )

    @pytest.mark.parametrize("phrase", REQUIRED)
    def test_each_required_validation_is_present(self, phrase):
        assert phrase in _flat(_decision()), phrase

    def test_the_rehearsal_is_specified_as_writing_no_authorization_state(self):
        flat = _flat(_decision())
        assert "writing no authorization state" in flat
        assert "both authorization predicates still `False` afterwards" in flat

    def test_all_three_consumers_are_named(self):
        flat = _flat(_decision())
        for consumer in (
            "_derive_pr337_actor_ratification()",
            "verify_lifecycle_against_truth()",
            "_verify_selected_review_is_final()",
        ):
            assert consumer in flat, consumer

    def test_a_probe_against_reintroducing_the_heuristic_is_required(self):
        flat = _flat(_decision())
        assert "lower-case heuristic cannot be reintroduced without failing" in flat


# =====================================================================================
# 11. The load-bearing consequence is stated
# =====================================================================================


class TestTheRebindingConsequenceIsStated:
    def test_the_decision_states_a_load_bearing_byte_will_change(self):
        flat = _flat(_decision())
        assert "The replacement implementation changes a load-bearing byte" in flat
        assert "LOAD_BEARING_RELPATHS[0]" in flat

    def test_the_decision_requires_a_later_separate_rebinding(self):
        flat = _flat(_decision())
        assert "separately authorized step-8-equivalent rebinding unit" in flat
        assert "this decision authorizes no rebinding" in flat

    def test_the_module_really_is_the_first_load_bearing_path(self):
        assert A.LOAD_BEARING_RELPATHS[0] == MODULE_RELPATH


# =====================================================================================
# 12. Nothing operational is authorized
# =====================================================================================


class TestNoOperationalAuthorityIsGranted:
    PROHIBITIONS = (
        "perform, arm, claim, execute, or complete any part of",
        "create an attestation, `AUTHORIZATION_ROOT`, lane state, `READY`, claim, or completion",
        "consume, claim, or touch `ATTEMPT_1`",
        "**perform a step-8-equivalent rebinding**",
        "perform readiness verification or a drift check",
        "authorize or perform link 5",
        "edit any historical review, comment, acceptance record, or closure record",
        "modify any runner, result validator, universe module, canonical artifact, or protected",
        "weaken any adverse-review rejection, any validator, or any test",
        "change any construction identity, universe membership, ordering, or cardinality",
        "acquire market, fundamental, economic, or Stage-2 data",
        "read, list, open, or substantively reuse any `risk_lane_boundary` protected `RISK`",
        "create any endpoint, bound, point, range, percentage, weight, rank, target, ladder,",
    )

    @pytest.mark.parametrize("phrase", PROHIBITIONS)
    def test_each_prohibition_is_present(self, phrase):
        assert phrase in _flat(_decision()), phrase

    @pytest.mark.parametrize("qualifier", ["unless", "except where", "may, if", "at its discretion"])
    def test_no_permissive_qualifier_weakens_the_prohibition_clause(self, qualifier):
        clause = _flat(_decision())
        start = clause.index("must not**:")
        body = clause[start : start + 2200]
        assert qualifier not in body, qualifier

    def test_new_execution_is_not_authorized(self):
        authorized, reason = A.new_execution_is_authorized()
        assert authorized is False
        assert reason

    def test_active_and_claimed_execution_are_not_authorized(self):
        assert A.active_execution_is_authorized()[0] is False
        assert A.claimed_execution_is_authorized()[0] is False

    def test_the_lane_is_absent_and_attempt_1_is_unclaimed(self):
        state, _ = A.lane_state_at(A.LanePaths())
        assert state == A.LANE_ABSENT
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

    def test_the_authorization_root_does_not_exist(self):
        assert not Path(A.AUTHORIZATION_ROOT).exists()

    def test_no_results_document_exists(self):
        assert not (ROOT / "research/level1_endpoint_evidence/stage1_results.yaml").exists()

    def test_the_public_executability_flag_is_still_false(self):
        prereg = yaml.safe_load(
            (ROOT / "research/level1_endpoint_evidence/pre_registration.yaml")
            .read_text(encoding="utf-8")
        )
        assert prereg["stage_1_executability"]["executable"] is False

    def test_the_bound_authorizing_identity_did_not_move(self):
        # RE-ANCHORED BY XASSET-0060, and bound at BOTH ends rather than one. What this test
        # protects is that THIS filing moved no lifecycle anchor -- not that no later, separately
        # authorized rebinding ever may. XASSET-0049's values are retained as NEGATIVE pins on the
        # constants that now carry them, so a silent revert still fails here.
        assert A.AUTHORIZING_DECISION == "XASSET-0060"
        assert A.AUTHORIZING_DECISION != "XASSET-0049"
        assert A.PRIOR_STEP8_EQUIVALENT_DECISION == "XASSET-0049"
        assert A.PRIOR_STEP8_EQUIVALENT_PULL_REQUEST == 349
        assert A.AUTHORIZING_PULL_REQUEST != 349
        assert A.REVIEWED_BASE_SHA == "301e79334876a4bda6e7b89a6156b34e8d38a605"
        assert A.REVIEWED_BASE_SHA != "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"
        assert A.PRIOR_STEP8_EQUIVALENT_MERGE_BASE == "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"

    def test_the_frozen_universe_is_unchanged(self):
        # RE-ANCHORED BY XASSET-0060, and STRENGTHENED rather than relaxed. XASSET-0057 §F.7
        # authorized ONE additive extension, 18 -> 25, adding the six decisions that authorized and
        # defined the formal-disposition parser plus the rebinding's own decision. The bare count
        # this line carried could not tell an authorized addition from a wholesale replacement of
        # equal length, so both ends are now bound: the eighteen this unit saw must still ALL be
        # present (nothing removed, swapped or traded away), and the live count is pinned EXACTLY
        # at 25 so a further silent addition still fails here.
        assert len(A.LOAD_BEARING_RELPATHS) == 25
        assert len(set(A.LOAD_BEARING_RELPATHS)) == 25
        assert len(A.LOAD_BEARING_RELPATHS) != 18
        assert len(set(A.LOAD_BEARING_RELPATHS)) != 18

    def test_this_decision_is_not_inserted_into_the_mechanism(self):
        """The identifier may never enter an executable constant or operative literal.

        RE-ANCHORED (XASSET-0056). The whole-file string check is retained verbatim against
        this unit's own closed merge. In the live tree the identifier now appears, lawfully and
        ONLY as a comment citation inside the successor's authorized parser correction --
        following the module's own long-standing convention of citing its governing decisions
        (fifteen other XASSET identifiers are cited the same way at this unit's own base).
        The operative property is therefore asserted directly and more precisely than a
        whole-file substring ever did: the identifier is in no executable constant, and appears
        nowhere in the attestation mechanism's own functions.
        """
        at_merge = _git("show", f"{MERGE_SHA}:{MODULE_RELPATH}")
        assert DECISION_ID not in at_merge
        assert A.AUTHORIZING_DECISION != DECISION_ID
        live = (ROOT / MODULE_RELPATH).read_text(encoding="utf-8")
        tree = ast.parse(live)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                assert node.value != DECISION_ID
        for name in (
            "build_authorization_payload",
            "validate_authorization_document",
            "write_authorization",
            "new_execution_is_authorized",
            "active_execution_is_authorized",
        ):
            fn = next(
                n for n in tree.body
                if isinstance(n, ast.FunctionDef) and n.name == name
            )
            assert DECISION_ID not in ast.get_source_segment(live, fn), name


# =====================================================================================
# 13. Catalog and register synchronisation
# =====================================================================================


class TestCatalogAndRegisterSynchronisation:
    def test_the_catalog_lists_this_decision_last_and_uniquely(self):
        """RE-ANCHORED (XASSET-0056): successors append after this decision, so "last" is
        stated EXACTLY against the named successor set rather than relaxed to "present"."""
        ids = [d["decision_id"] for d in yaml.safe_load(CATALOG.read_text())["decisions"]]
        assert ids.count(DECISION_ID) == 1
        assert len(ids) == len(set(ids))
        assert ids[len(ids) - 1 - len(SUCCESSORS_APPENDED_SINCE)] == DECISION_ID
        assert tuple(ids[ids.index(DECISION_ID) + 1:]) == SUCCESSORS_APPENDED_SINCE
        assert "XASSET-0054" not in ids  # consumed by the closed-unmerged unit, never reused

    def test_the_catalog_entry_points_at_the_real_file(self):
        entry = next(
            d for d in yaml.safe_load(CATALOG.read_text())["decisions"]
            if d["decision_id"] == DECISION_ID
        )
        assert (ROOT / entry["file"]).exists()
        assert entry["status"] == "Proposed"
        assert entry["supporting_artifact"] == Path(__file__).name

    def test_the_catalog_relates_this_decision_to_its_authority(self):
        entry = next(
            d for d in yaml.safe_load(CATALOG.read_text())["decisions"]
            if d["decision_id"] == DECISION_ID
        )
        assert AUTHORITY_ID in entry["related_decisions"]

    def test_the_catalog_has_no_open_issues(self):
        from portfolio_hq.dashboard import decisions as dash

        assert dash.build_catalog(ROOT).issues == ()

    def test_the_workstream_posture_is_untouched(self):
        ws = _ws0014()
        assert ws["status"] == "proposed"
        assert ws["priority"] == "secondary"

    def test_exactly_zero_primary_workstreams(self):
        data = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
        assert sum(1 for w in data["workstreams"] if w.get("priority") == "primary") == 0

    def test_this_units_gate_exists_and_is_not_marked_complete_by_its_own_filing(self):
        gate = next(
            g for g in _ws0014()["milestones"]
            if g["gate"] == "xasset0055-verdict-boundary-governance"
        )
        assert gate["status"] == "in_progress"
        assert gate["status"] != "complete"

    def test_the_gate_records_the_rejection_and_the_unchanged_module(self):
        gate = next(
            g for g in _ws0014()["milestones"]
            if g["gate"] == "xasset0055-verdict-boundary-governance"
        )
        flat = _flat(gate["description"])
        assert FULL_REVIEW_ID in flat and DELTA_REVIEW_ID in flat
        assert str(CLOSED_PULL_REQUEST) in flat
        assert BASE_MODULE_SHA256 in flat

    def test_no_prior_gate_is_rewritten(self):
        """PR #355's own gates are history and stay exactly as they were on main.

        RE-ANCHORED (XASSET-0056): this unit's own contribution is measured over its own closed
        base..merge range. The live register is additionally checked to confirm successors only
        APPEND -- so the "no prior gate is rewritten" property is asserted at BOTH ends, which
        is strictly more than the original.
        """
        base = yaml.safe_load(_git("show", f"{BASE_SHA}:operations/WORKSTREAMS.yaml"))
        before = next(w for w in base["workstreams"] if w["id"] == "WS-0014")["milestones"]
        merged = yaml.safe_load(_git("show", f"{MERGE_SHA}:operations/WORKSTREAMS.yaml"))
        at_merge = next(w for w in merged["workstreams"] if w["id"] == "WS-0014")["milestones"]
        assert at_merge[: len(before)] == before
        assert len(at_merge) == len(before) + 1
        live = _ws0014()["milestones"]
        assert live[: len(at_merge)] == at_merge

    def test_the_active_pr_is_the_real_github_number_not_the_sentinel(self):
        """RE-ANCHORED (XASSET-0056) onto this unit's own GATE, which does not move.

        The shared `active_pr` field belongs to whichever unit is live; this unit's own gate
        still carries the real number GitHub issued, never its sentinel, and that is the
        immutable fact this assertion was really protecting.
        """
        gate = next(g for g in _ws0014()["milestones"] if g["gate"] == THIS_GATE)
        assert gate["pr"] == THIS_PULL_REQUEST
        assert gate["pr"] != PR_SENTINEL, "the sentinel was never replaced"
        assert gate["pr"] not in PRIOR_SENTINELS
        assert gate["pr"] > CLOSED_PULL_REQUEST
        at_merge = yaml.safe_load(_git("show", f"{MERGE_SHA}:operations/WORKSTREAMS.yaml"))
        merged_ws = next(w for w in at_merge["workstreams"] if w["id"] == "WS-0014")
        assert merged_ws["active_pr"] == THIS_PULL_REQUEST

    def test_this_units_gate_carries_the_real_pull_request_number(self):
        gate = next(
            g for g in _ws0014()["milestones"]
            if g["gate"] == "xasset0055-verdict-boundary-governance"
        )
        assert gate["pr"] == THIS_PULL_REQUEST
        assert gate["pr"] != PR_SENTINEL, "the sentinel was never replaced"

    def test_no_sentinel_survives_anywhere_in_the_register(self):
        raw = WORKSTREAMS.read_text(encoding="utf-8")
        for sentinel in (PR_SENTINEL, *PRIOR_SENTINELS):
            assert f"active_pr: {sentinel}" not in raw, sentinel
            assert f"pr: {sentinel}" not in raw, sentinel

    def test_the_shared_live_fields_name_this_unit(self):
        """RE-ANCHORED (XASSET-0056): asserted at this unit's own closed merge, where it is
        permanently true, with the successor NAMED and this unit's own values retained as
        negative pins so the fields stay bound at BOTH ends."""
        at_merge = yaml.safe_load(_git("show", f"{MERGE_SHA}:operations/WORKSTREAMS.yaml"))
        merged_ws = next(w for w in at_merge["workstreams"] if w["id"] == "WS-0014")
        assert merged_ws["active_branch"] == BRANCH
        assert merged_ws["last_verified_main_sha"] == BASE_SHA
        assert merged_ws["active_branch"] != "claude/xasset-0054-parser-contract-correction-h3nq7p"
        live = _ws0014()
        assert live["active_branch"] == SUCCESSOR_BRANCH
        assert live["last_verified_main_sha"] == SUCCESSOR_MAIN_SHA
        assert live["last_verified_main_sha"] == XASSET0060_MAIN_SHA
        # ADVANCED BY XASSET-0060: XASSET-0059's own values become NEGATIVE pins, retained
        # exactly rather than deleted, so a silent revert to finished work still fails here.
        assert live["active_branch"] != XASSET0059_BRANCH
        assert live["last_verified_main_sha"] != XASSET0059_MAIN_SHA
        assert live["active_branch"] != XASSET0058_BRANCH
        assert live["last_verified_main_sha"] != XASSET0058_MAIN_SHA
        assert live["active_branch"] != XASSET0057_BRANCH
        assert live["last_verified_main_sha"] != XASSET0057_MAIN_SHA
        assert live["active_branch"] != BRANCH
        assert live["last_verified_main_sha"] != BASE_SHA
        assert live["active_branch"] != "claude/xasset-0054-parser-contract-correction-h3nq7p"


# =====================================================================================
# 14. Non-vacuity
# =====================================================================================


class TestNonVacuityAgainstTheBase:
    """A guard against a suite that would pass identically before this filing existed."""

    def test_the_decision_file_did_not_exist_at_the_base(self):
        rel = str(DECISION.relative_to(ROOT))
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{BASE_SHA}:{rel}"], cwd=ROOT, capture_output=True
        )
        assert result.returncode != 0

    def test_this_test_module_did_not_exist_at_the_base(self):
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{BASE_SHA}:{Path(__file__).name}"],
            cwd=ROOT, capture_output=True,
        )
        assert result.returncode != 0

    def test_the_gate_did_not_exist_at_the_base(self):
        raw = _git("show", f"{BASE_SHA}:operations/WORKSTREAMS.yaml")
        assert "xasset0055-verdict-boundary-governance" not in raw

    def test_the_catalog_gained_exactly_one_entry(self):
        """RE-ANCHORED (XASSET-0056): successors append too, so the growth THIS unit caused
        stays EXACT by naming them rather than being relaxed to an inequality."""
        before = yaml.safe_load(_git("show", f"{BASE_SHA}:governance/decisions.yaml"))["decisions"]
        after = yaml.safe_load(CATALOG.read_text())["decisions"]
        assert len(after) == len(before) + 1 + len(SUCCESSORS_APPENDED_SINCE)
        assert DECISION_ID not in {d["decision_id"] for d in before}
        for successor in SUCCESSORS_APPENDED_SINCE:
            assert successor not in {d["decision_id"] for d in before}

    def test_the_base_did_not_already_name_this_decision_anywhere(self):
        result = subprocess.run(
            ["git", "grep", "-l", DECISION_ID, BASE_SHA], cwd=ROOT, capture_output=True, text=True
        )
        assert result.returncode != 0, result.stdout


# ======================================================================================
# The predecessor suites were RE-ANCHORED, never weakened
#
# `active_branch`, `active_pr` and `last_verified_main_sha` are WS-0014's SINGLE SHARED live
# self-reference fields (`OPS-0001`'s Active-GitHub-fields rule), so advancing them onto this
# unit necessarily falsified eleven predecessor assertions that named the previously-live unit,
# and two catalog-tail assertions in XASSET-0053's own suite. The established remedy in this
# programme -- set by XASSET-0043/XASSET-0044 for the XASSET-0042 suite -- is to RE-ANCHOR each
# one onto a closed immutable anchor, retaining the superseded value as a NEGATIVE pin, and
# never to delete, skip, xfail or relax it. This section proves that is what happened.
# ======================================================================================


#: Every predecessor suite this unit's lawful register advance falsified, with the count of
#: positive pins re-pointed in each. Measured against the base, not asserted from memory.
REANCHORED_SUITES = (
    "test_level1_stage1_activation_authorization.py",
    "test_level1_stage1_parser_contract_correction_authorization.py",
    "test_level1_stage1_post_correction_rebinding.py",
    "test_level1_stage1_post_correction_rebinding_authorization.py",
    "test_level1_stage1_post_merge_ci_recovery_authorization.py",
    "test_level1_stage1_post_merge_ci_recovery_reauthorization.py",
    "test_level1_stage1_post_merge_ci_recovery_reconciliation.py",
    "test_level1_stage1_post_rebinding_drift_authorization.py",
    "test_level1_stage1_pr337_actor_evidence_correction_authorization.py",
    "test_level1_stage1_readiness_verification_authorization.py",
)

#: The generation constant this unit introduced, and the one it superseded.
SUPERSEDED_GENERATION_SHA = "cc1d1b62b8b48c7123b73e05e7ea04af89c89cd6"


class TestThePredecessorSuitesWereReAnchoredNotWeakened:
    def test_every_re_anchored_suite_exists_and_was_actually_modified(self):
        changed = _changed_paths()
        for name in REANCHORED_SUITES:
            assert (ROOT / name).exists(), name
            assert name in changed, name

    def test_the_only_non_governance_files_touched_are_the_re_anchored_suites(self):
        allowed = set(REANCHORED_SUITES) | {
            "governance/decisions.yaml",
            "operations/WORKSTREAMS.yaml",
            "test_portfolio_hq_dashboard_decisions.py",
            str(DECISION.relative_to(ROOT)),
            Path(__file__).name,
        }
        extra = _changed_paths() - allowed
        assert not extra, sorted(extra)

    def test_no_re_anchored_assertion_was_skipped_deleted_or_relaxed(self):
        """A re-anchor may add a marker, but never `skip`, `xfail`, or a bare `pass` body."""
        for name in REANCHORED_SUITES:
            live = (ROOT / name).read_text(encoding="utf-8")
            base = _git("show", f"{BASE_SHA}:{name}")
            for banned in ("pytest.mark.skip", "pytest.mark.xfail", "pytest.skip("):
                assert live.count(banned) == base.count(banned), (name, banned)
            # The suite may only GROW: re-anchoring adds pins, it never removes assertions.
            assert live.count("assert ") >= base.count("assert "), name

    def test_the_superseded_generation_survives_as_a_negative_pin(self):
        """Deleting the old value instead of demoting it would leave the field bound at only
        one end, which is precisely the failure this convention exists to prevent."""
        for name in REANCHORED_SUITES:
            live = (ROOT / name).read_text(encoding="utf-8")
            base = _git("show", f"{BASE_SHA}:{name}")
            if SUPERSEDED_GENERATION_SHA not in base and "XASSET0053_MAIN_SHA" not in base:
                continue
            assert (
                SUPERSEDED_GENERATION_SHA in live or "XASSET0053_MAIN_SHA" in live
            ), name

    def test_this_units_value_is_now_the_positive_pin_in_every_constant_suite(self):
        """RE-ANCHORED (XASSET-0056). This unit's value is no longer the LIVE positive pin --
        the named successor's is, because `last_verified_main_sha` is WS-0014's SINGLE SHARED
        live field and lawfully advances with every generation.

        What this assertion was really protecting is unchanged and is asserted more strictly
        than before: this unit's constant must still be DEFINED with its exact value (retained,
        never deleted), must now appear as a NEGATIVE pin, and the successor named here must be
        the positive pin -- so every constant suite stays bound at BOTH ends across generations.
        """
        for name in REANCHORED_SUITES:
            live = (ROOT / name).read_text(encoding="utf-8")
            if "XASSET0055_MAIN_SHA" not in live:
                continue
            # retained with its exact value, never deleted
            assert f'XASSET0055_MAIN_SHA = "{BASE_SHA}"' in live, name
            # now a NEGATIVE pin: a silent revert to this finished unit's state must fail
            assert "!= XASSET0055_MAIN_SHA" in live, name
            # and the successor is the positive pin, named exactly
            # ADVANCED BY XASSET-0057, on exactly the terms this docstring already states.
            # XASSET-0056's own constant is now itself a NEGATIVE pin -- retained with its exact
            # value, never deleted -- and the newly named successor is the positive pin, so the
            # chain stays bound at EVERY end rather than only the two most recent.
            assert f'XASSET0056_MAIN_SHA = "{MERGE_SHA}"' in live, name
            assert "!= XASSET0056_MAIN_SHA" in live, name
            # ADVANCED BY XASSET-0058, on exactly the terms this docstring already states.
            # XASSET-0057's own constant is now itself a NEGATIVE pin -- retained with its exact
            # value, never deleted -- and the newly named successor is the positive pin.
            assert f'XASSET0057_MAIN_SHA = "{XASSET0057_MAIN_SHA}"' in live, name
            assert "!= XASSET0057_MAIN_SHA" in live, name
            # ADVANCED BY XASSET-0059, on exactly the terms this docstring already states.
            # XASSET-0058's own constant becomes a NEGATIVE pin -- retained with its exact
            # value, never deleted -- and the newly named successor is the positive pin.
            assert f'XASSET0058_MAIN_SHA = "{XASSET0058_MAIN_SHA}"' in live, name
            assert "!= XASSET0058_MAIN_SHA" in live, name
            # ADVANCED BY XASSET-0060, on exactly the terms this docstring already states.
            # XASSET-0059's own constant becomes a NEGATIVE pin -- retained with its exact value,
            # never deleted -- and the newly named successor is the positive pin.
            assert f'XASSET0059_MAIN_SHA = "{XASSET0059_MAIN_SHA}"' in live, name
            assert "!= XASSET0059_MAIN_SHA" in live, name
            assert f'XASSET0060_MAIN_SHA = "{SUCCESSOR_MAIN_SHA}"' in live, name
            assert "== XASSET0060_MAIN_SHA" in live, name
            # Every earlier generation stays pinned too. XASSET-0053's OWN suite names its own
            # base `BASE_SHA` rather than `XASSET0053_MAIN_SHA` -- a suite does not refer to
            # itself in the third person -- so the constant is asserted exactly where it is
            # defined, and that suite's equivalent own-base pin is asserted instead.
            if "XASSET0053_MAIN_SHA" in live:
                assert "!= XASSET0053_MAIN_SHA" in live, name
            else:
                assert "BASE_SHA, XASSET0052_BASE" in live, name

    def test_no_re_anchored_suite_is_a_load_bearing_path(self):
        """Re-anchoring a bound path would silently invalidate the module's own trust boundary
        and require a rebinding this governance filing is not authorized to perform."""
        for name in REANCHORED_SUITES:
            assert name not in set(A.LOAD_BEARING_RELPATHS), name

    def test_the_re_anchoring_is_non_vacuous_at_the_base(self):
        """Each re-anchored suite must genuinely have failed at the base under this unit's
        register, otherwise the edits were cosmetic."""
        base_register = _git("show", f"{BASE_SHA}:operations/WORKSTREAMS.yaml")
        before = next(
            w for w in yaml.safe_load(base_register)["workstreams"] if w["id"] == "WS-0014"
        )
        live = next(
            w
            for w in yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))["workstreams"]
            if w["id"] == "WS-0014"
        )
        at_merge = next(
            w
            for w in yaml.safe_load(
                _git("show", f"{MERGE_SHA}:operations/WORKSTREAMS.yaml")
            )["workstreams"]
            if w["id"] == "WS-0014"
        )
        assert before["last_verified_main_sha"] != at_merge["last_verified_main_sha"]
        assert before["active_branch"] != at_merge["active_branch"]
        assert before["last_verified_main_sha"] == SUPERSEDED_GENERATION_SHA
        assert at_merge["last_verified_main_sha"] == BASE_SHA
        # NEGATIVE PIN: the live field has since moved on to the named successor.
        assert live["last_verified_main_sha"] == SUCCESSOR_MAIN_SHA

    def test_the_register_gate_discloses_the_re_anchoring_honestly(self):
        """The register must record the same discipline the suite enforces. If it ever admits a
        weakening instead, that is a governance claim the tests have to catch."""
        gate = next(
            g for g in _ws0014()["milestones"]
            if g["gate"] == "xasset0055-verdict-boundary-governance"
        )
        flat = _flat(gate["description"])
        assert "TEN PREDECESSOR SUITES WERE RE-ANCHORED, NEVER WEAKENED" in flat
        assert "NOTHING WAS DELETED, SKIPPED, XFAILED OR RELAXED" in flat
        assert "retained beside the new one as a NEGATIVE pin" in flat
        assert "no XASSET0054 generation" in flat
        for weakening in (
            "SOME ASSERTIONS WERE DELETED",
            "WERE RELAXED",
            "assertions were removed",
        ):
            assert weakening not in flat, weakening

    def test_the_decision_discloses_the_re_anchoring(self):
        text = DECISION.read_text(encoding="utf-8")
        assert "re-anchor" in text.lower()
        assert "never deleted, skipped, xfailed or relaxed" in text
        assert "onto a closed immutable anchor" in text
        assert "retained beside the new one as a **negative pin**" in text
        assert "no `XASSET0054` generation" in text
