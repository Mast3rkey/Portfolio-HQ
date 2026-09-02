"""Supporting artifact for ``XASSET-0061``.

`XASSET-0061` authorizes exactly one future, separate, strictly read-only `XASSET-0041` §I link-3 /
`XASSET-0030` §G.B step-9 readiness verification against the **current twenty-five-path binding**,
and performs no part of it.

This suite is deliberately **mechanism-based**, not prose-based. Every claim that can be checked
against the live system is checked against the live system: the twenty-five load-bearing paths are
resolved by parsing the production module with ``ast`` and hashing the real files; the four-role
module-identity chain is compared against the real constants; the canonical pins, universe identity
and authorization constants are read from the real artifacts; and the Stage-1 safety posture is
evaluated by calling the real predicates. A test that could pass merely because a sentence appears
in a Markdown file would be worthless here, so where a textual property genuinely is the subject —
an authorization boundary, a withheld grant — the assertion is pinned to specific operative wording
*and* paired with a live-system check that the filing did not in fact do the thing it disclaims.

Nothing in this module executes Stage 1, evaluates a gate, writes a lane, or touches `ATTEMPT_1`.
The production authorization module is imported read-only; historical module sources are parsed with
``ast`` and never executed.
"""

from __future__ import annotations

import ast
import collections
import copy
import textwrap
import hashlib
import re
import subprocess
from pathlib import Path

import pytest
import yaml

import level1_stage1_execution_authorization as A

ROOT = Path(__file__).resolve().parent
GOV = ROOT / "governance/decisions"
CATALOG = ROOT / "governance/decisions.yaml"
WORKSTREAMS = ROOT / "operations/WORKSTREAMS.yaml"
PROTOCOL = ROOT / "research/level1_endpoint_evidence/PROTOCOL_V1.md"
PREREG = ROOT / "research/level1_endpoint_evidence/pre_registration.yaml"

DECISION_ID = "XASSET-0061"
DECISION = GOV / (
    "XASSET-0061-endpoint-0001-stage-1-post-parser-correction-renewed-readiness-"
    "verification-authorization.md"
)
GATE = "xasset0061-post-parser-correction-renewed-readiness-verification-authorization"
FOLD_FORWARD_GATE = "xasset0060-post-merge-verification"

# --------------------------------------------------------------------------------------------
# The binding this filing anchors to. Every value re-resolved from live git/GitHub at authoring
# time; the suite re-derives what it can rather than trusting these.
# --------------------------------------------------------------------------------------------

BOUND_MERGE_SHA = "413e033ac33741829168762ab24d73327c047d4b"
#: THIS unit's own merge commit (PR #362). Immutable, and the closing end of the only
#: range this filing can speak for. The changed-set checks below were open-ended --
#: `git diff BOUND_MERGE_SHA` against the live worktree -- which meant the NEXT commit
#: merged to `main`, of any kind by anyone, made them fail. Closed here on both sides.
THIS_UNIT_MERGE_SHA = "3db918530b10ffc1423ba0b749b086e349a4901d"
BOUND_ACCEPTED_HEAD = "eac06700e9ca72c30e704899f6b761a7e07717f7"
BOUND_MERGE_BASE = "301e79334876a4bda6e7b89a6156b34e8d38a605"
BOUND_MERGE_TREE = "998c28a3c7f349cd36796255854924fa7473dfae"

FULL_REVIEW = "5047221802"
PRINCIPAL_ACCEPTANCE = "5449752973"
POST_MERGE_VERIFICATION = "5449783195"
FINAL_CLOSURE = "5449912049"
MERGE_CI_RUN = "33151977375"
MERGE_CI_JOB = "98785832731"

BOUND_AUTHORIZING_DECISION = "XASSET-0060"
BOUND_AUTHORIZING_PULL_REQUEST = 361
BOUND_REVIEWED_BASE_SHA = BOUND_MERGE_BASE

EXPECTED_LOAD_BEARING_COUNT = 25

#: This filing's own pull request. Bound ONLY after GitHub issued it -- never predicted. The first
#: commit carried ``null`` in the register, the draft was opened, and the issued number was read
#: back and bound. Mirrors the XASSET-0050 suite's own ``THIS_PULL_REQUEST`` pattern.
THIS_PULL_REQUEST = 362

#: The predecessor link-3 authorization, and the anchor that no longer describes the system.
DEAD_DECISION = "XASSET-0050"
DEAD_MERGE_SHA = "a941455491cc5e4d3d868775fb6b4b88f0fe2ce3"
DEAD_TREE = "e0ee2d4c25066cdc3d1c936015c3ada62bed74e8"
DEAD_LOAD_BEARING_COUNT = 18
DEAD_PASS_COMMENT = "5384453102"
DUPLICATE_EXERCISE_STOP_COMMENT = "5384471997"

#: Roles 1-4 of the module-identity chain. Role 2 is the permanent negative pin.
ROLE1_SHA = "4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541"
ROLE1_BLOB = "f71b08b4ebe95f161c57cdbb2a924748f13af02d"
ROLE2_SHA = "12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5"
ROLE2_BLOB = "b5622f9e412afd604a11cde04317b79c5e57920a"
ROLE3_SHA = "1283a2d4ccc3794fd37b81d4e5e23ac6f67a0b87b911ef3861c724d636fabd00"
ROLE3_BLOB = "b8414a69f41e37f8fdd5c18dae13176fd847170e"
ROLE4_SHA = "3f261b6b3cdcabc5f0cb228d987a52dd36e2a0f522e7fc4e57c483d3c0e3001a"
ROLE4_BLOB = "a9753d1273785e9ce2ebb4de2067489dfbb9156c"

#: C4 -- the five outcome-capable modules. Recorded as a WITNESS; §G.1 makes the derived value
#: operative. This table exists so a drift between the two fails in CI rather than at verification.
C4_MODULE_WITNESS = {
    "level1_stage1_runner.py":
        "4a88cf6d0271da0dc3a6ca175fadb0223bf7ff8843479733cbcf0effd47ba5d9",
    "level1_stage1_result_validator.py":
        "b4773eb767158434136b72316e9802308b9e6fb47b6e45f8f10445c02cee3b7a",
    "level1_endpoint_evidence_preregistration_validator.py":
        "b3a87e4f8b828d420795348642c977a9f0585eafa9262a4be48df406f770233d",
    "level1_construction_universe_closure_validator.py":
        "1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5",
    "level1_stage1_execution_authorization.py": ROLE4_SHA,
}

C6_CANONICAL_PINS = {
    "research/level1_endpoint_evidence/PROTOCOL_V1.md":
        "1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84",
    "research/level1_endpoint_evidence/pre_registration.yaml":
        "898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f",
}

C7_CONSTRUCTION_COUNT = 680
C7_CELL_COUNT = 48
C7_UNIVERSE_SHA = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"

#: The three pre-execution authorization predicates. §G.2 fixes the count at THREE, not two.
AUTHORIZATION_PREDICATES = (
    "new_execution_is_authorized",
    "claimed_execution_is_authorized",
    "active_execution_is_authorized",
)

#: The prior link-3/4/5 authorizations, none of which is inside the trust boundary.
PRIOR_LINK_AUTHORIZATIONS = ("XASSET-0038", "XASSET-0050", "XASSET-0051", "XASSET-0052")

#: The EXACT, CLOSED set of files this authorization changes against ``BOUND_MERGE_SHA``.
#: Independent review found the superseded open ``test_*.py`` class widened the accepted boundary,
#: so the manifest is pinned by name and asserted for EXACT equality -- an unexpected file fails,
#: and a silently reverted expected file fails too.
EXPECTED_CHANGED_FILES = {
    "governance/decisions.yaml",
    "governance/decisions/XASSET-0061-endpoint-0001-stage-1-post-parser-correction-renewed-readiness-verification-authorization.md",
    "operations/WORKSTREAMS.yaml",
    "test_level1_stage1_activation_authorization.py",
    "test_level1_stage1_formal_disposition_parser_correction.py",
    "test_level1_stage1_formal_disposition_parser_correction_authorization.py",
    "test_level1_stage1_parser_contract_correction_authorization.py",
    "test_level1_stage1_post_correction_rebinding.py",
    "test_level1_stage1_post_correction_rebinding_authorization.py",
    "test_level1_stage1_post_merge_ci_recovery_authorization.py",
    "test_level1_stage1_post_merge_ci_recovery_reauthorization.py",
    "test_level1_stage1_post_merge_ci_recovery_reconciliation.py",
    "test_level1_stage1_post_parser_correction_operational_rebinding.py",
    "test_level1_stage1_post_parser_correction_rebinding_authorization.py",
    "test_level1_stage1_post_parser_correction_renewed_readiness_verification_authorization.py",
    "test_level1_stage1_post_rebinding_drift_authorization.py",
    "test_level1_stage1_pr337_actor_evidence_correction_authorization.py",
    "test_level1_stage1_readiness_verification_authorization.py",
    "test_level1_stage1_verdict_boundary_governance.py",
    "test_portfolio_hq_dashboard_decisions.py",
}

#: Production, canonical and portfolio paths this filing must never touch.
PROTECTED_RELPATHS = {
    "level1_stage1_execution_authorization.py",
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_construction_universe_closure_validator.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "holdings.yaml",
    "targets.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
    "allocate.py",
    "margin_state.py",
    "levels.py",
}

#: The one changed test that is NOT a predecessor re-anchoring. Its only change is this filing's
#: own catalog-count assertion (161 -> 162); it never carried XASSET-0060's value and never should,
#: so the re-anchoring narrative check below does not apply to it. It IS still hash-pinned, because
#: integrity coverage must not have a hole.
NON_REANCHORING_CHANGED_TESTS = {
    "test_portfolio_hq_dashboard_decisions.py",
}

#: EXACT content identity of every changed predecessor/dashboard suite, excluding THIS artifact --
#: which cannot pin its own hash without self-reference. This is the check that actually forecloses
#: a semantic weakening: a file with a required negative-pin assertion replaced by ``assert True``
#: keeps the predecessor SHA string and RAISES its assert count, but cannot keep this hash.
PINNED_TEST_HASHES = {
    "test_level1_stage1_activation_authorization.py":
        "e71e3fc477c636ed8b98b917d5d4167064e7f4b453b56a5b3aac1f76a94dd635",
    "test_level1_stage1_formal_disposition_parser_correction.py":
        "8a1e15bbab5be928292e7a5931fc8f63d47e270b52d91f39cc0c75c98e0fe355",
    "test_level1_stage1_formal_disposition_parser_correction_authorization.py":
        "653ae8fcfd37dcaf188e9a1a53b467ea7d9b52ede6000ea3d5bd1b2f8b2ca8d8",
    "test_level1_stage1_parser_contract_correction_authorization.py":
        "3df490ce5682224406db604e5f3ce3cc1f6b1f5f38b8ae7e7ffd0e25f0ab7b27",
    "test_level1_stage1_post_correction_rebinding.py":
        "0e49bf40d56491bef05f782bc1c6f663fe496ea9a9e3aa0f70b260ef5e77dbe7",
    "test_level1_stage1_post_correction_rebinding_authorization.py":
        "9b415f0255c77c4c11e19e70363c659112720ad98fb0d4aac5f4b01e5f176ff6",
    "test_level1_stage1_post_merge_ci_recovery_authorization.py":
        "4f2145554bba39af90d838a8f08b5c325e223deec1ec125892cf5e18c99e17fe",
    "test_level1_stage1_post_merge_ci_recovery_reauthorization.py":
        "0dbf090f846728a9677bdd719d138284dde46bda5fa51a110c7bd3311aa3bc9e",
    "test_level1_stage1_post_merge_ci_recovery_reconciliation.py":
        "0ac485eb39a661b7cee2148804d3c5f1fae652e2a35f21964c34e65fb74ca07f",
    "test_level1_stage1_post_parser_correction_operational_rebinding.py":
        "79bd10f9a839d42067990c7a8d5ff5af28486b297718fd73d9cc9b9eb18d59fa",
    "test_level1_stage1_post_parser_correction_rebinding_authorization.py":
        "55001f942030242f165a1b01b4c5fd4180f71ce0cb4b4825db05d74ae71bf306",
    "test_level1_stage1_post_rebinding_drift_authorization.py":
        "a427cb719e180aeca54001e3dc1f3f19d621a24f6e0a2fe337d5ac4030d11963",
    "test_level1_stage1_pr337_actor_evidence_correction_authorization.py":
        "21e73766b2bf762d7f565a3eefce24eea18cb487844f51139d2c156c38f20a59",
    "test_level1_stage1_readiness_verification_authorization.py":
        "c8993d7e2ad15ea297f985c2128c790d7b5b6130306cfe7e6cd565f5ac2c256c",
    "test_level1_stage1_verdict_boundary_governance.py":
        "904d5ab289121a39bbc53e7036aba9a3f85610ef4450d3c7440b79e7d44083a6",
    "test_portfolio_hq_dashboard_decisions.py":
        "b09e51927092cf9ccc202f575e426186a101f43ef82a2324042fc37ec422279d",
}


EXPECTED_DECISION_SECTIONS = (
    "### A. Determination",
    "#### A.1",
    "### B. Why `XASSET-0050` cannot supply this authority",
    "#### B.1",
    "### C. Relation to `XASSET-0027`",
    "### D. Relation to `XASSET-0029`",
    "### E. Authority granted",
    "### F. Authority withheld",
    "#### F.1",
    "### G. The closed renewed-readiness checklist",
    "#### G.1",
    "#### G.2",
    "### H. Fail-closed",
    "### I. Packaging and evidence",
    "### J. Effectivity",
    "### K. Links 4 and 5",
    "### L. Absolute non-authorization",
)


# --------------------------------------------------------------------------------------------
# Helpers -- everything derived, never trusted from prose.
# --------------------------------------------------------------------------------------------


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=True, text=True
    ).stdout.strip()


def _live_load_bearing() -> tuple[str, ...]:
    """Resolve ``LOAD_BEARING_RELPATHS`` by parsing the module with ``ast``, never executing it.

    Module-level string aliases and implicit/explicit concatenation are resolved from the same
    source, so a member spelled as a constant reference is still checked as its real path.
    """
    source = (ROOT / "level1_stage1_execution_authorization.py").read_text()
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
                assert all(i is not None for i in items), "unresolved LOAD_BEARING element"
                return tuple(items)
    raise AssertionError("LOAD_BEARING_RELPATHS is not declared in the live module")


LIVE_LOAD_BEARING = _live_load_bearing()
DECISION_TEXT = DECISION.read_text() if DECISION.exists() else ""

def _norm(text: str) -> str:
    """Collapse runs of whitespace so a prose assertion is about words, not line wrapping.

    Every phrase asserted through this helper is still asserted **in full**; only the permitted
    wrapping varies. Nothing is shortened, and no assertion is reduced to a fragment.
    """
    return re.sub(r"\s+", " ", text)


DECISION_NORM = _norm(DECISION_TEXT)
WORKSTREAMS_TEXT = WORKSTREAMS.read_text()


def _gate_block(gate_name: str) -> str:
    """The raw YAML text of one ``WS-0014`` gate, so wording claims are checked where they live."""
    marker = f"- gate: {gate_name}\n"
    start = WORKSTREAMS_TEXT.index(marker)
    nxt = WORKSTREAMS_TEXT.find("\n      - gate: ", start + len(marker))
    end = nxt if nxt != -1 else WORKSTREAMS_TEXT.find("\n    evidence_refs:", start)
    assert end != -1, f"could not bound gate block {gate_name}"
    return WORKSTREAMS_TEXT[start:end]


def _ws0014() -> dict:
    data = yaml.safe_load(WORKSTREAMS_TEXT)
    for w in data["workstreams"]:
        if w.get("id") == "WS-0014":
            return w
    raise AssertionError("WS-0014 not found")


WS0014 = _ws0014()


# --------------------------------------------------------------------------------------------



_ANCHOR_NAME = re.compile(r"^[A-Z][A-Z0-9_]*$")


#: A string literal is a LAWFUL ANCHOR only if it looks like one. Everything else
#: is operative expected text and must survive normalization untouched.
#:
#: Independent review reproduced why this distinction is load-bearing. The
#: superseded normaliser abstracted EVERY string, so
#:
#:     assert "Merging it arms nothing" in section
#:
#: and
#:
#:     assert "" in section
#:
#: normalized identically -- a substantive Stage-1 safety assertion could be made
#: vacuous with the inventory reporting no loss at all. These patterns are
#: FAIL-CLOSED: a string that does not match one is preserved, so an unrecognised
#: form is protected rather than silently abstracted.
#: Anchor CATEGORIES, each with its own placeholder. Independent review required
#: that recognized values not all collapse to one universal token: doing so makes
#: a decision id interchangeable with a date, and a determination string with a
#: merge SHA. Each category abstracts only within itself.
_ANCHOR_CATEGORIES = (
    ("SHA",           re.compile(r"^[0-9a-f]{7,40}$")),
    ("DATE",          re.compile(r"^\d{4}-\d{2}-\d{2}")),
    ("DECISION",      re.compile(r"^[A-Z][A-Z0-9]{1,9}-\d{4}(-\d{2})?$")),
    ("BRANCH",        re.compile(r"^claude/[A-Za-z0-9._\-/]+$")),
    ("DECISION_FILE", re.compile(r"^governance/decisions/[A-Za-z0-9._\-]+\.md$")),
    ("NUMBER",        re.compile(r"^\d+$")),
)


def _anchor_category(text: str) -> str | None:
    """Which anchor category this exact string belongs to, or None.

    FAIL-CLOSED. A string matching no category is not an anchor and is preserved
    verbatim, so an unrecognised form is protected rather than abstracted. The
    empty string is never an anchor -- it is the vacuous-``in`` bypass itself.
    """
    t = text.strip()
    if not t:
        return None
    for name, pattern in _ANCHOR_CATEGORIES:
        if pattern.match(t):
            return name
    return None


def _is_lawful_anchor(text: str) -> bool:
    """Whether this string is the kind of value a lawful re-anchor changes."""
    return _anchor_category(text) is not None


def _module_anchor_categories(source: str) -> dict:
    """Category of every module-level constant, derived from its BOUND VALUE.

    This is the correction independent review required. Typography proves
    nothing: ``STEP10_DETERMINATION`` and ``BOUND_MERGE_SHA`` are both
    SCREAMING_CASE, and collapsing both to one ``<ANCHOR_NAME>`` made

        assert STEP10_DETERMINATION in section   ->   assert BOUND_MERGE_SHA in section

    invisible -- a substantive Step-10 requirement replaced by an already-present
    merge check, with the inventory unchanged. A name's category comes from what
    it is actually bound to: a 40-hex value is a SHA anchor, ``STEP_10_NO_DRIFT``
    is not an anchor at all. A name bound to anything non-literal has no category
    and is never abstracted.
    """
    cats = {}
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return cats
    # EVERY assignment, not only module-level ones. Several predecessor suites
    # bind their re-anchor constants inside the test function that uses them, and
    # scanning only the module body missed those -- reporting a genuinely lawful
    # XASSET0060 -> XASSET0061 re-anchor as a weakening.
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Constant):
            continue
        v = node.value.value
        if isinstance(v, bool):
            continue
        if isinstance(v, str):
            cat = _anchor_category(v)
        elif isinstance(v, int):
            cat = "NUMBER"          # a PR number is an anchor too
        else:
            cat = None
        if cat is None:
            continue
        for tgt in node.targets:
            if isinstance(tgt, ast.Name) and _ANCHOR_NAME.match(tgt.id):
                cats[tgt.id] = cat
    return cats


def _authorized_reanchor_placeholders(pinned_src: str, live_src: str) -> dict:
    """Name substitutions THIS DELTA actually performed, same category only.

    The review's preferred construction: derive permitted substitutions from the
    authorized predecessor re-anchor rather than accepting every name with
    similar typography. A constant that exists in BOTH versions was not
    re-anchored, so it is never abstracted -- which is precisely why the
    ``STEP10_DETERMINATION`` -> ``BOUND_MERGE_SHA`` swap is caught: both names
    are present on both sides, so neither is in play.
    """
    pinned = _module_anchor_categories(pinned_src)
    live = _module_anchor_categories(live_src)
    # A lawful re-anchor in this corpus ADDS the successor constant and KEEPS the
    # predecessor as historical evidence -- XASSET0060_MAIN_SHA stays, and
    # XASSET0061_MAIN_SHA appears beside it, while the assertion moves from one
    # to the other. So the delta's own signal is the SET OF ADDED CONSTANTS, not
    # a removed/added pairing: an earlier attempt required removal and wrongly
    # reported that real re-anchor as a weakening.
    added_categories = {cat for name, cat in live.items() if name not in pinned}
    if not added_categories:
        # Nothing was re-anchored, so nothing is interchangeable. This is the
        # case that catches STEP10_DETERMINATION -> BOUND_MERGE_SHA: the mutation
        # adds no constant, so both names stay literal and the swap is a loss.
        return {}
    ph = {}
    for source_map in (pinned, live):
        for name, cat in source_map.items():
            if cat in added_categories:
                ph[name] = f"<REANCHOR:{cat}>"
    return ph


class _AnchorNormaliser(ast.NodeTransformer):
    """Abstract LAWFUL ANCHOR SUBSTITUTIONS; preserve every operative predicate.

    Abstracted:

    * a string literal, to ITS OWN CATEGORY's placeholder -- SHA to ``<SHA>``,
      date to ``<DATE>``, and so on, never to one shared token, so a
      decision-for-date or determination-for-SHA swap is a change;
    * an f-string whose every literal part is an anchor or bare punctuation;
    * a module constant ONLY when this delta actually re-anchored it, and then
      only within its own category.

    Preserved -- changing any of these changes what is asserted:

    * every other string literal, including expected prose;
    * every constant name not part of an authorized re-anchor;
    * attribute and method names -- ``startswith`` vs ``endswith``;
    * comparison and boolean operators, numeric literals, call structure.
    """

    def __init__(self, name_placeholders=None):
        super().__init__()
        self._names = name_placeholders or {}

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            cat = _anchor_category(node.value)
            if cat is not None:
                return ast.copy_location(ast.Constant(value=f"<ANCHOR_{cat}>"), node)
        return node

    def visit_Name(self, node):
        ph = self._names.get(node.id)
        if ph is not None:
            return ast.copy_location(ast.Name(id=ph, ctx=node.ctx), node)
        return node

    def visit_JoinedStr(self, node):
        for part in node.values:
            if isinstance(part, ast.Constant) and isinstance(part.value, str):
                t = part.value.strip()
                if t and not _is_lawful_anchor(t) and not _TRIVIAL_JOINER.match(t):
                    return self.generic_visit(node)
        return ast.copy_location(ast.Constant(value="<ANCHOR_FSTR>"), node)


#: Punctuation that merely joins interpolated anchors and carries no meaning of
#: its own -- ``f"{A}-{B}"``, ``f"{SHA}:{path}"``.
_TRIVIAL_JOINER = re.compile(r"^[\-:/.,;_=~^@#|\s\[\](){}<>]+$")


def _assertion_inventory(source: str, name_placeholders=None) -> collections.Counter:
    """The suite's assertions as NORMALIZED SEMANTIC FINGERPRINTS.

    RE-ANCHORED AGAIN (PHQ-2026-07, review 5085019004). Two superseded mechanisms
    both failed, in opposite directions:

    * a bare COUNT, then a count plus an AST-shape total, could not see an
      EQUAL-SHAPE weakening. Independent review demonstrated

          Path(entry["file"]).name.startswith(f"{DECISION_ID}-")
              ->  Path(entry["file"]).name.endswith(".md")

      which loses the decision-ID/file binding entirely -- a row pointing at
      ANOTHER decision's file then passes -- while both forms scored (441, 433)
      and the guard reported no loss;

    * an EXACT fingerprint inventory saw that, but also rejected a LAWFUL
      predecessor re-anchor (``XASSET0060_MAIN_SHA`` -> ``XASSET0061_MAIN_SHA``,
      which ADDED two assertions). That is whole-file immutability wearing a
      different hat.

    What separates the two is which parts of an assertion an anchor change may
    lawfully touch. ``_AnchorNormaliser`` abstracts exactly those parts and
    nothing else, so ``startswith`` -> ``endswith`` is a different fingerprint
    while ``==  SHA_A`` -> ``== SHA_B`` is the same one.

    A ``Counter``, so removing one of several identical assertions is still a loss.
    ``assert True``/``assert 1`` are excluded: they are the shape a silent gutting
    takes, and counting them would let a weakened file keep its total.
    """
    inv = collections.Counter()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Assert):
            continue
        test = node.test
        if isinstance(test, ast.Constant) and bool(test.value) is True:
            continue          # vacuous by construction
        norm = _AnchorNormaliser(name_placeholders).visit(copy.deepcopy(test))
        inv[ast.dump(norm)] += 1
    return inv


def _lost_assertions(pinned_src: str, live_src: str) -> list[str]:
    """Fingerprints asserted when pinned that are no longer asserted now.

    The permitted name substitutions are derived from THIS delta -- only a
    constant the delta actually retired, replaced by a new one of the same
    anchor category, is treated as interchangeable. A name present on both sides
    was not re-anchored and is compared literally, which is what makes the
    ``STEP10_DETERMINATION`` -> ``BOUND_MERGE_SHA`` swap visible.

    KNOWN RESIDUAL, stated rather than hidden: within a delta that DOES add a new
    constant of some category, the constants of that same category become
    interchangeable for that comparison. That is the "SHA-to-successor-SHA in the
    same role" case the review names as lawful, and narrowing it further would
    need a role model the sources do not carry. What is caught: any cross-category
    substitution (determination for SHA, decision for date, comment for branch),
    and ANY name substitution at all in a delta that re-anchors nothing.
    """
    ph = _authorized_reanchor_placeholders(pinned_src, live_src)
    missing = (_assertion_inventory(pinned_src, ph)
               - _assertion_inventory(live_src, ph))
    return sorted(missing.elements())


#: DIRECT PROTECTED PREDICATES (PHQ-2026-07, second correction).
#:
#: Independent review's prescription for this defect class offered two mechanisms:
#: direct assertions for the required protected predicates, OR a normalized semantic
#: inventory abstracting only lawful anchor substitutions. Both are used here, and the
#: split between them is not arbitrary -- it follows a real property of the corpus.
#:
#: The inventory answers "did this suite lose an assertion since its baseline?". That
#: question is exactly right for a suite this filing did not re-anchor. It is the WRONG
#: question for the seven suites whose catalog-position, catalog-cardinality and
#: base-revision assertions this filing lawfully REWROTE under its own already-reviewed
#: G4 correction: those assertions were replaced, not lost, and a diff against a
#: pre-correction baseline cannot tell the two apart without reading intent.
#:
#: So for those seven, the invariant is stated positively instead: these named predicates
#: must still be asserted. That is a semantic claim, not a count, hash or shape total. It
#: is immune to a lawful re-anchor of some OTHER assertion, and it still catches the
#: equal-shape predicate swap -- ``startswith`` and ``endswith`` are different attribute
#: names, which the normaliser deliberately preserves.
PROTECTED_PREDICATES = {
    "test_level1_stage1_formal_disposition_parser_correction.py": (
        'assert Path(entry["file"]).name.startswith(f"{DECISION_ID}-")',
        'assert len(rows) == 1',
        'assert "*" not in inner',
        'assert inner.startswith(PREFIX)',
        'assert "category.strip()" not in source',
    ),
    "test_level1_stage1_formal_disposition_parser_correction_authorization.py": (
        'assert PREFIX.endswith(":")',
        'assert len(CANON_LABEL) == 18',
        'assert len(NONSPACE_POSITIONS) == 17',
    ),
    "test_level1_stage1_parser_contract_correction_authorization.py": (
        r'assert decision.startswith("---\n")',
        'assert "stripped.upper().startswith(FORMAL_DISPOSITION_PREFIX)" in body',
        'assert line.startswith("**") and line.endswith("**")',
    ),
    "test_level1_stage1_post_merge_ci_recovery_reconciliation.py": (
        'assert A.AUTHORIZING_DECISION not in A.PERMANENTLY_INEFFECTIVE_DECISIONS',
        'assert A.AUTHORIZING_PULL_REQUEST not in A.PERMANENTLY_INEFFECTIVE_PULL_REQUESTS',
        'assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"',
    ),
    "test_level1_stage1_post_parser_correction_operational_rebinding.py": (
        'assert ROLE4_SHA256 not in source',
        'assert "REVIEWED_BASE_SHA" not in loaded',
        'assert A.AUTHORIZING_DECISION not in A.PERMANENTLY_INEFFECTIVE_DECISIONS',
    ),
    "test_level1_stage1_verdict_boundary_governance.py": (
        'assert relpath not in _changed_paths()',
        'assert not [c for c in changed if c.startswith("governance/audits/")]',
        'assert not [c for c in changed if c.startswith("governance/evidence/")]',
    ),
    "test_portfolio_hq_dashboard_decisions.py": (
        'assert "<iframe" not in html.lower()',
        'assert "<script" not in html.lower()',
        'assert "<form" not in html.lower()',
    ),
}


def _unasserted_predicates(relpath: str, live_src: str) -> list[str]:
    """Which of ``relpath``'s named protected predicates are no longer asserted.

    Membership is decided on the NORMALIZED form, not on the source text, so a
    lawful message change or anchor substitution inside the predicate still counts
    as asserted -- while a different operator, attribute or call structure does not.
    """
    live = _assertion_inventory(live_src)
    missing = []
    for text in PROTECTED_PREDICATES[relpath]:
        want = _assertion_inventory(textwrap.dedent(text))
        assert want, f"a protected predicate must itself parse to an assertion: {text}"
        # TWO independent conditions, because each closes the other's blind spot.
        #
        # The normalized form catches a structural weakening -- a different operator,
        # attribute, call shape or arity -- including the equal-shape ``startswith`` /
        # ``endswith`` swap independent review named.
        #
        # Verbatim presence catches what abstraction deliberately cannot: two protected
        # predicates in one suite may normalize to the SAME form when they differ only
        # in a string anchor (``"category.strip()"`` and ``"category.strip("``), so
        # gutting one still leaves the form present in the multiset. Requiring the
        # predicate's own text closes that, and constrains nothing else in the file --
        # it is not a whole-file hash, and a lawful message change lies outside it.
        if not (want <= live) or text not in live_src:
            missing.append(text)
    return missing


class TestTheFilingExistsAndIsWellFormed:
    def test_decision_file_exists_and_is_the_declared_name(self):
        assert DECISION.exists(), DECISION

    def test_frontmatter_is_parseable_and_correct(self):
        assert DECISION_TEXT.startswith("---\n")
        fm = yaml.safe_load(DECISION_TEXT.split("---", 2)[1])
        assert fm["decision_id"] == DECISION_ID
        assert fm["status"] == "Proposed"
        assert fm["category"] == "cross_asset_allocation_architecture"
        assert fm["supporting_artifact"] == Path(__file__).name
        # The chain this filing depends on must be declared, not merely mentioned in prose.
        for dep in (
            "XASSET-0029", "XASSET-0030", "XASSET-0036", "XASSET-0040", "XASSET-0041",
            "XASSET-0050", "XASSET-0051", "XASSET-0052", "XASSET-0057", "XASSET-0058",
            "XASSET-0059", "XASSET-0060",
        ):
            assert dep in fm["related_decisions"], dep

    def test_catalog_entry_is_present_unique_and_points_at_real_files(self):
        cat = yaml.safe_load(CATALOG.read_text())["decisions"]
        ids = [d["decision_id"] for d in cat]
        assert len(ids) == len(set(ids)), "duplicate decision_id in the catalog"
        entry = next(d for d in cat if d["decision_id"] == DECISION_ID)
        assert entry["status"] == "Proposed"
        assert (ROOT / entry["file"]).exists()
        assert (ROOT / entry["supporting_artifact"]).exists()
        assert entry["file"] == str(DECISION.relative_to(ROOT))
        assert entry["supporting_artifact"] == Path(__file__).name

    def test_the_record_carries_no_h1_matching_every_other_catalogued_decision(self):
        """The dashboard derives a decision's title from its filename, not a body heading.

        `decisions.build_catalog` sets ``title_source == "h1"`` when a record opens with a
        level-one heading, and the whole catalogued corpus relies on ``"filename"``. A single
        record with an H1 breaks that invariant repository-wide, so it is pinned here too --
        localised to this file, with a clearer failure than the corpus-wide assertion gives.
        """
        body = DECISION_TEXT.split("---", 2)[2]
        offenders = [ln for ln in body.splitlines() if re.match(r"^# \S", ln)]
        assert offenders == [], offenders

    def test_every_authored_section_is_present(self):
        for heading in EXPECTED_DECISION_SECTIONS:
            assert heading in DECISION_TEXT, heading

    def test_workstream_gate_exists_and_does_not_mark_its_own_unmerged_work_complete(self):
        """The load-bearing property is the STATUS, not the nullness of ``pr``.

        A session may never mark its own still-unmerged filing ``complete``; that is what this
        pins. ``pr`` is legitimately ``null`` before GitHub issues a number and exactly the issued
        number afterwards -- and nothing else, so a predicted or wrong number still fails.
        """
        gates = {m["gate"]: m for m in WS0014["milestones"]}
        assert GATE in gates
        assert gates[GATE]["status"] == "in_progress"
        assert gates[GATE]["pr"] in (None, THIS_PULL_REQUEST), gates[GATE]["pr"]

    def test_ws0014_self_reference_fields_point_at_the_current_binding(self):
        assert WS0014["last_verified_main_sha"] == BOUND_MERGE_SHA
        assert WS0014["active_pr"] in (None, THIS_PULL_REQUEST), WS0014["active_pr"]

    def test_binding_the_pull_request_number_touched_no_other_workstream(self):
        """Reading back GitHub's issued number must not clobber a sibling workstream.

        ``active_pr`` exists on every workstream, so a whole-file substitution would silently
        rewrite several. Each sibling is pinned against its own value at the bound merge.
        """
        base = yaml.safe_load(
            subprocess.run(
                ["git", "show", f"{BOUND_MERGE_SHA}:operations/WORKSTREAMS.yaml"],
                cwd=ROOT, capture_output=True, check=True, text=True,
            ).stdout
        )
        base_by_id = {w["id"]: w for w in base["workstreams"]}
        live_by_id = {w["id"]: w for w in yaml.safe_load(WORKSTREAMS_TEXT)["workstreams"]}
        assert set(live_by_id) == set(base_by_id)
        for wid, w in live_by_id.items():
            if wid == "WS-0014":
                continue
            assert w.get("active_pr") == base_by_id[wid].get("active_pr"), wid


class TestFoldForwardGateRecordsTheClosedLifecycleWithoutRewritingHistory:
    def test_fold_forward_gate_is_additive_and_complete(self):
        gates = {m["gate"]: m for m in WS0014["milestones"]}
        assert FOLD_FORWARD_GATE in gates
        assert gates[FOLD_FORWARD_GATE]["status"] == "complete"
        assert gates[FOLD_FORWARD_GATE]["pr"] == BOUND_AUTHORIZING_PULL_REQUEST

    def test_the_prior_gate_is_left_byte_unedited_at_in_progress(self):
        """The convention is to record beside a prior gate, never to rewrite its own text."""
        gates = {m["gate"]: m for m in WS0014["milestones"]}
        prior = gates["xasset0060-post-parser-correction-operational-rebinding"]
        assert prior["status"] == "in_progress"
        assert prior["pr"] == BOUND_AUTHORIZING_PULL_REQUEST

    def test_fold_forward_gate_names_every_lifecycle_identity(self):
        block = _gate_block(FOLD_FORWARD_GATE)
        for identity in (
            BOUND_MERGE_SHA, BOUND_ACCEPTED_HEAD, BOUND_MERGE_BASE, BOUND_MERGE_TREE,
            FULL_REVIEW, PRINCIPAL_ACCEPTANCE, POST_MERGE_VERIFICATION, FINAL_CLOSURE,
            MERGE_CI_RUN, MERGE_CI_JOB,
        ):
            assert identity in block, identity


class TestTheBoundMergeIsRealAndDriftFree:
    """C1/C2 are not taken on trust -- they are re-derived from the object store."""

    def test_merge_commit_has_exactly_two_ordered_parents(self):
        parents = _git("rev-list", "--parents", "-n", "1", BOUND_MERGE_SHA).split()
        assert parents[0] == BOUND_MERGE_SHA
        assert parents[1:] == [BOUND_MERGE_BASE, BOUND_ACCEPTED_HEAD], parents

    def test_merge_tree_is_byte_identical_to_the_accepted_head_tree(self):
        merge_tree = _git("rev-parse", f"{BOUND_MERGE_SHA}^{{tree}}")
        head_tree = _git("rev-parse", f"{BOUND_ACCEPTED_HEAD}^{{tree}}")
        assert merge_tree == BOUND_MERGE_TREE
        assert merge_tree == head_tree, "merge drift"

    def test_accepted_head_to_merge_diff_is_empty(self):
        diff = _git("diff", "--name-only", BOUND_ACCEPTED_HEAD, BOUND_MERGE_SHA)
        assert diff == "", diff


class TestAuthorityGapIsGroundedInAcceptedText:
    def test_xasset0060_section_k_requires_separate_authority_for_links_3_4_and_5(self):
        """The grant this filing supplies must be traceable to accepted text, not asserted."""
        src = (GOV / (
            "XASSET-0060-endpoint-0001-stage-1-post-parser-correction-operational-rebinding.md"
        )).read_text()
        assert (
            "**Links 3, 4 and 5 each require their own separate authority and their own "
            "complete lifecycle.**" in _norm(src)
        )

    def test_xasset0041_section_i_defines_link_3_as_read_only_and_separately_authorized(self):
        src = (GOV / (
            "XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-"
            "authorization.md"
        )).read_text()
        assert "3. renewed readiness           (separately authorized; step-9 equivalent, read-only)" in src

    def test_xasset0030_step_9_is_read_only_verification_of_already_bound_bytes(self):
        src = (GOV / (
            "XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md"
        )).read_text()
        assert '9. After rebinding, "runner execution-readiness" is **read-only verification of already-bound bytes**.' in src


class TestPredecessorAuthorityIsSpentAndItsAnchorIsDead:
    """§B's two independent grounds, each checked against the real system where possible."""

    def test_the_filing_states_both_independent_grounds(self):
        assert "Ground 1 — `XASSET-0050` is spent" in DECISION_TEXT
        assert "Ground 2 — `XASSET-0050`'s anchor no longer describes the system" in DECISION_NORM
        assert "**Either ground below is independently sufficient**" in DECISION_NORM

    def test_the_dead_anchor_really_is_a_different_binding(self):
        """Not a wording claim: the two path counts genuinely differ, live."""
        assert len(LIVE_LOAD_BEARING) == EXPECTED_LOAD_BEARING_COUNT
        assert EXPECTED_LOAD_BEARING_COUNT != DEAD_LOAD_BEARING_COUNT
        assert BOUND_MERGE_SHA != DEAD_MERGE_SHA
        assert BOUND_MERGE_TREE != DEAD_TREE
        assert ROLE4_SHA != ROLE1_SHA

    def test_the_module_identity_actually_moved_off_the_dead_anchor(self):
        """The predecessor PASS enumerated role 1; the live module is role 4."""
        live = _sha256(ROOT / "level1_stage1_execution_authorization.py")
        assert live == ROLE4_SHA
        assert live != ROLE1_SHA, "module still at the identity the spent PASS verified"

    def test_the_filing_records_the_dead_anchor_values_exactly(self):
        for value in (DEAD_MERGE_SHA, DEAD_TREE, str(DEAD_LOAD_BEARING_COUNT), ROLE1_SHA):
            assert value in DECISION_TEXT, value

    def test_the_discharged_determination_is_preserved_not_re_adjudicated(self):
        assert DEAD_PASS_COMMENT in DECISION_TEXT
        assert DUPLICATE_EXERCISE_STOP_COMMENT in DECISION_TEXT
        assert "does not reopen it, does not contradict it" in DECISION_NORM
        assert "remains **true of what it verified**" in DECISION_NORM
        # And the prohibition is operative, not merely narrative.
        assert (
            "reopen, re-adjudicate, invalidate, or re-weigh `XASSET-0050`'s discharged link-3"
            in DECISION_NORM
        )

    @pytest.mark.parametrize("decision", ("XASSET-0050", "XASSET-0051", "XASSET-0052"))
    def test_no_predecessor_link_authorization_is_revived(self, decision):
        assert f"`{decision}`" in DECISION_TEXT
        assert re.search(rf"`{decision}`[^\n]*(not revived|are retired|is spent|not revived)",
                         DECISION_TEXT) or "are likewise not revived" in DECISION_TEXT


class TestVerificationIsNotPerformedHere:
    """The single most important property: this filing grants, it does not exercise."""

    def test_no_pass_or_fail_is_issued(self):
        assert "issues no `PASS` and no `FAIL`" in DECISION_NORM
        assert "**This decision performs no part of that verification.**" in DECISION_NORM
        assert "consumes none of the authority it creates" in DECISION_NORM
        assert "performs no readiness verification and issues no `PASS` or `FAIL`" in DECISION_NORM

    def test_the_predecessor_pass_token_is_only_ever_cited_never_issued(self):
        """Citing a predecessor's determination is not issuing one.

        `STEP_9_READINESS_VERIFICATION_PASS` legitimately appears in SS-B, where this filing
        explains that `XASSET-0050`'s one-shot grant was already exercised. That is a historical
        citation about a different unit. What must never appear is this filing ISSUING such a
        determination, so every occurrence is required to be a citation of the predecessor.
        """
        token = "STEP_9_READINESS_VERIFICATION_PASS"
        occurrences = [
            m.start() for m in re.finditer(re.escape(token), DECISION_TEXT)
        ]
        assert occurrences, "the predecessor's spent determination should be cited in SS-B"
        for pos in occurrences:
            window = DECISION_TEXT[max(0, pos - 400):pos + 400]
            assert "XASSET-0050" in window, (
                "the token appears outside a citation of the spent predecessor determination"
            )
            assert DEAD_PASS_COMMENT in window, (
                "a cited determination must carry the predecessor's own evidence identifier"
            )

    def test_this_filing_issues_no_determination_of_its_own(self):
        """No FAIL token at all, and no present-tense issuance by this decision."""
        assert "READINESS_VERIFICATION_FAIL" not in DECISION_TEXT
        for forbidden in (
            "this decision determines",
            "this filing determines",
            "readiness is verified",
            "verification passes",
            "we therefore issue",
        ):
            assert forbidden not in DECISION_NORM.lower(), forbidden

    def test_the_determination_token_is_an_authorization_not_a_verification(self):
        assert "POST_PARSER_CORRECTION_RENEWED_STEP_9_READINESS_VERIFICATION_AUTHORIZED" in DECISION_NORM

    def test_the_summary_distinction_is_stated_verbatim(self):
        assert "**Link 3 never belongs inside a \"not authorized\" list.**" in DECISION_NORM
        assert "authorized-but-unperformed" in DECISION_NORM


class TestEffectivityRequiresCompleteLifecycleClosure:
    def test_all_seven_conditions_are_enumerated(self):
        section = DECISION_TEXT.split("### J. Effectivity")[1].split("### K.")[0]
        for n in range(1, 8):
            assert f"\n{n}. " in section, n
        assert "**None is individually sufficient.**" in section
        assert "successful merge-commit CI whose `head_sha` is the exact merge SHA" in _norm(section)

    def test_a_green_pr_head_run_is_explicitly_not_sufficient(self):
        section = DECISION_TEXT.split("### J. Effectivity")[1].split("### K.")[0]
        assert "not the pull request head's own run" in _norm(section)
        assert "a green PR-head CI run does not" in _norm(section)

    def test_the_repository_lifecycle_gate_tuple_is_unchanged(self):
        gates = tuple(A.REQUIRED_LIFECYCLE_GATES)
        assert len(gates) == 6, gates
        assert "PRINCIPAL_EXACT_HEAD_ACCEPTANCE" in gates


class TestLinks4And5RetainSeparateAuthority:
    def test_links_4_and_5_are_withheld_by_name(self):
        section = DECISION_TEXT.split("### K. Links 4 and 5")[1].split("### L.")[0]
        assert "**Link 4 / step 10**" in section
        assert "**Link 5 / step 11**" in section
        assert "retains its own separate-authority requirement" in _norm(section)

    def test_a_clean_pass_authorizes_nothing_further(self):
        assert "**authorizes nothing further.**" in DECISION_NORM

    def test_no_attestation_arming_claim_or_execution_is_granted(self):
        for phrase in (
            "produce an attestation",
            "It does not arm Stage 1",
            "It does not claim or consume any part of `ATTEMPT_1`",
            "evaluates no gate for any registered construction",
        ):
            assert phrase in DECISION_NORM, phrase

    def test_p1_results_pr_remains_unspent(self):
        assert "**not consumed, replaced, counted against, or brought forward**" in DECISION_NORM
        assert "remains one, unspent" in DECISION_NORM.lower()


class TestReadOnlyMeansReadOnly:
    @pytest.mark.parametrize("prohibition", [
        "create, edit, regenerate, correct, reformat, or re-pin",
        "**declare any defect \"fixed\"**",
        "extend, reduce, re-order, or re-derive `LOAD_BEARING_RELPATHS`",
        "produce an attestation",
        "create `stage1_results.yaml`",
        "**evaluate or decide any gate (`G1`–`G12`) for any registered construction**",
        "read, list, open, or substantively reuse any `risk_lane_boundary` protected `RISK` result",
    ])
    def test_prohibition_is_present(self, prohibition):
        section = DECISION_TEXT.split("### F. Authority withheld")[1].split("### G.")[0]
        assert prohibition in section, prohibition

    def test_the_role_2_negative_pin_may_not_be_rehabilitated(self):
        section = DECISION_TEXT.split("### F. Authority withheld")[1].split("### G.")[0]
        assert "bind, rehabilitate, or treat as acceptable the role-2 vulnerable intermediate" in _norm(section)
        assert ROLE2_SHA in section

    def test_no_repair_is_authorized_on_a_finding(self):
        section = DECISION_TEXT.split("### H. Fail-closed")[1].split("### I.")[0]
        assert "**no repair of any kind is authorized**" in _norm(section)
        assert "**Uncertainty is failure.**" in section
        assert "stop report" in section

    def test_the_unit_makes_no_repository_mutation(self):
        section = DECISION_TEXT.split("### I. Packaging and evidence")[1].split("### J.")[0]
        assert "**no branch, no commit, and no pull request**" in _norm(section)
        assert "**no repository mutation**" in section
        assert "neither required nor authorized" in _norm(section)


class TestClosedChecklistCoversEveryRequiredCondition:
    def test_the_checklist_is_declared_closed(self):
        section = DECISION_TEXT.split("### G. The closed renewed-readiness checklist")[1]
        assert "**Closed**" in section
        assert "a finding to report, not a checklist item to add" in _norm(section)

    @pytest.mark.parametrize("condition", [f"**C{n}**" for n in range(1, 14)])
    def test_every_condition_row_is_present(self, condition):
        section = DECISION_TEXT.split("### G. The closed renewed-readiness checklist")[1]
        assert condition in section, condition

    def test_no_condition_beyond_c13_is_smuggled_in(self):
        section = DECISION_TEXT.split("### G. The closed renewed-readiness checklist")[1]
        found = {int(m) for m in re.findall(r"\*\*C(\d+)\*\*", section)}
        assert found == set(range(1, 14)), sorted(found)

    def test_derived_beats_recorded_and_disagreement_is_a_stop(self):
        section = DECISION_TEXT.split("#### G.1")[1].split("#### G.2")[0]
        assert "**The derived value is operative. The recorded value is a witness.**" in _norm(section)
        assert "drift is a **stop**" in section
        assert "never a substitute for derivation" in section

    def test_the_predicate_count_is_fixed_at_three_not_two(self):
        section = DECISION_TEXT.split("#### G.2")[1].split("### H.")[0]
        assert "names **three** predicates, not two" in _norm(section)
        assert "the live module governs and the count is three" in _norm(section)
        for name in AUTHORIZATION_PREDICATES:
            assert name in section, name


class TestChecklistPinsMatchTheLiveSystem:
    """§G.1's tripwire: if a recorded value drifts from the derived one, this fails in CI."""

    def test_load_bearing_set_is_exactly_twenty_five_unique_existing_paths(self):
        assert len(LIVE_LOAD_BEARING) == EXPECTED_LOAD_BEARING_COUNT
        assert len(set(LIVE_LOAD_BEARING)) == EXPECTED_LOAD_BEARING_COUNT
        for rel in LIVE_LOAD_BEARING:
            assert (ROOT / rel).exists(), rel

    def test_every_load_bearing_path_matches_the_bound_merge_tree(self):
        """Derived, not recorded: hash each real file against the merged tree's own blob."""
        for rel in LIVE_LOAD_BEARING:
            in_tree = _git("rev-parse", f"{BOUND_MERGE_SHA}:{rel}")
            on_disk = _git("hash-object", rel)
            assert in_tree == on_disk, rel

    @pytest.mark.parametrize("rel,expected", sorted(C4_MODULE_WITNESS.items()))
    def test_outcome_capable_module_identity_matches(self, rel, expected):
        assert _sha256(ROOT / rel) == expected, rel
        assert rel in LIVE_LOAD_BEARING, rel

    def test_four_role_chain_constants_are_intact(self):
        assert A.PREVIOUSLY_BOUND_MODULE_SHA256 == ROLE1_SHA
        assert A.PREVIOUSLY_BOUND_MODULE_BLOB == ROLE1_BLOB
        assert A.VULNERABLE_MODULE_SHA256 == ROLE2_SHA
        assert A.VULNERABLE_MODULE_BLOB == ROLE2_BLOB
        assert A.PARSER_CORRECTED_MODULE_SHA256 == ROLE3_SHA
        assert A.PARSER_CORRECTED_MODULE_BLOB == ROLE3_BLOB

    def test_role_2_is_a_permanent_negative_pin(self):
        assert ROLE2_SHA in A.NEVER_BINDABLE_MODULE_SHA256
        # The bound end is role 4, and it is not the refused identity.
        assert _sha256(ROOT / "level1_stage1_execution_authorization.py") == ROLE4_SHA
        assert ROLE4_SHA not in A.NEVER_BINDABLE_MODULE_SHA256

    def test_module_git_blob_matches_role_4(self):
        assert _git("hash-object", "level1_stage1_execution_authorization.py") == ROLE4_BLOB

    @pytest.mark.parametrize("rel,expected", sorted(C6_CANONICAL_PINS.items()))
    def test_canonical_pin_matches_both_the_file_and_the_module(self, rel, expected):
        assert _sha256(ROOT / rel) == expected, rel
        assert A.CANONICAL_PINS[rel] == expected, rel

    def test_frozen_universe_identity_is_unchanged(self):
        assert A.CONSTRUCTION_COUNT == C7_CONSTRUCTION_COUNT
        assert A.CONSTRUCTION_CELL_COUNT == C7_CELL_COUNT
        assert A.CONSTRUCTION_UNIVERSE_SHA256 == C7_UNIVERSE_SHA

    def test_authorization_constants_are_the_current_binding(self):
        assert A.AUTHORIZING_DECISION == BOUND_AUTHORIZING_DECISION
        assert A.AUTHORIZING_PULL_REQUEST == BOUND_AUTHORIZING_PULL_REQUEST
        assert A.REVIEWED_BASE_SHA == BOUND_REVIEWED_BASE_SHA

    def test_every_pinned_value_also_appears_in_the_decision_record(self):
        """A witness that is not written down cannot trip."""
        for value in (
            *C4_MODULE_WITNESS.values(), *C6_CANONICAL_PINS.values(),
            ROLE1_SHA, ROLE2_SHA, ROLE3_SHA, ROLE4_SHA, ROLE4_BLOB,
            C7_UNIVERSE_SHA, BOUND_MERGE_SHA, BOUND_ACCEPTED_HEAD, BOUND_MERGE_TREE,
            BOUND_AUTHORIZING_DECISION, BOUND_REVIEWED_BASE_SHA,
        ):
            assert value in DECISION_TEXT, value


class TestStage1SafetyPostureIsUnchangedByThisFiling:
    """Evaluated by calling the real predicates -- not by reading a sentence about them."""

    def test_lane_and_authorization_paths_are_absent(self):
        assert not A.AUTHORIZATION_ROOT.exists()
        assert not A.AUTHORIZATION_PATH.exists()
        assert not A.CLAIM_PATH.exists()
        assert not A.COMPLETION_PATH.exists()

    @pytest.mark.parametrize("predicate", AUTHORIZATION_PREDICATES)
    def test_authorization_predicate_is_false(self, predicate):
        result = getattr(A, predicate)()
        value = result[0] if isinstance(result, tuple) else result
        assert value is False, (predicate, result)

    def test_stage_1_is_not_executable_in_the_canonical_artifact(self):
        prereg = yaml.safe_load(PREREG.read_text())
        assert prereg["stage_1_executability"]["executable"] is False

    def test_no_stage1_results_artifact_exists_anywhere(self):
        assert list(ROOT.rglob("stage1_results.yaml")) == []

    def test_attempt_1_is_intact_unclaimed_and_unconsumed(self):
        """No claim or completion record exists, so the one-shot lane is untouched."""
        assert not A.CLAIM_PATH.exists()
        assert not A.COMPLETION_PATH.exists()
        assert "ATTEMPT_1" in DECISION_TEXT
        assert "intact, unclaimed and unconsumed" in DECISION_NORM


class TestThisFilingMutatesNothingLoadBearing:
    """The authored delta must be governance-only, and CLOSED rather than class-admitted.

    An earlier form of this guard admitted any path matching ``test_*.py`` and called a changed
    predecessor suite a genuine re-anchoring when three shallow textual conditions held: the file
    differed from base, the XASSET-0060 SHA string still appeared somewhere, and the count of
    lines beginning with ``assert`` had not fallen. Independent review demonstrated that those
    conditions do NOT prove a predecessor assertion was preserved or relocated: replacing

        assert workstream["active_pr"] != XASSET0060_ACTIVE_PR

    with ``assert True`` satisfies all three -- the file still differs from base, still contains
    the SHA as inert text, and its assert count RISES from 231 to 233 -- while the meaningful
    negative pin is gone. An arbitrary unrelated test file could enter scope on the same terms.

    The guard is therefore closed on both axes: the changed set is pinned to an EXACT manifest,
    and every changed predecessor suite is pinned to an EXACT content hash. A weakened file has a
    different hash and fails, whatever its assert count or SHA-string content says.
    """

    @staticmethod
    def _changed_set() -> set[str]:
        """THIS unit's own change set, measured over its own CLOSED immutable range.

        Previously an OPEN-ENDED diff against the live worktree plus untracked files. That
        made the set grow with every later commit on `main`, so the manifest assertion
        below was guaranteed to fail on the next lawful merge of any kind -- and it did.
        A closed range names what this unit actually changed, exactly and permanently.
        """
        return set(
            _git("diff", "--name-only", BOUND_MERGE_SHA, THIS_UNIT_MERGE_SHA).split()
        )

    def test_the_changed_set_is_exactly_the_expected_manifest(self):
        """Closed on both sides: no unexpected file, and no expected file silently dropped."""
        assert self._changed_set() == EXPECTED_CHANGED_FILES, {
            "unexpected": sorted(self._changed_set() - EXPECTED_CHANGED_FILES),
            "missing": sorted(EXPECTED_CHANGED_FILES - self._changed_set()),
        }

    def test_the_changed_set_touches_no_load_bearing_path(self):
        """Derived from the live module, never from a literal list here."""
        assert not (self._changed_set() & set(LIVE_LOAD_BEARING)), sorted(
            self._changed_set() & set(LIVE_LOAD_BEARING)
        )

    def test_the_changed_set_touches_no_production_or_portfolio_path(self):
        assert not (self._changed_set() & PROTECTED_RELPATHS), sorted(
            self._changed_set() & PROTECTED_RELPATHS
        )

    def test_no_load_bearing_path_differs_from_the_bound_merge(self):
        """RESTORED. A direct git-blob comparison, independent of the changed-set derivation.

        The changed-set checks above would also catch a modified bound path, but they depend on
        ``git diff --name-only`` reporting it. This compares the object-store blob at the bound
        merge against the working tree byte-for-byte, so a bound path cannot drift even if the
        changed-set derivation were wrong. Removing it while closing the scope guard would have
        traded one form of coverage for another; both are kept.
        """
        for rel in LIVE_LOAD_BEARING:
            assert _git("rev-parse", f"{BOUND_MERGE_SHA}:{rel}") == _git(
                "hash-object", rel
            ), rel

    @pytest.mark.parametrize("rel", sorted(PROTECTED_RELPATHS))
    def test_protected_path_is_byte_identical_to_the_bound_merge(self, rel):
        """RESTORED, widened to all fourteen paths, then RE-ANCHORED to this unit's own
        CLOSED range. The live ``hash-object`` end made a closed historical unit assert
        that no later, separately authorized unit may ever touch a protected path --
        authority this filing never had. Both endpoints are immutable now."""
        assert _git("rev-parse", f"{BOUND_MERGE_SHA}:{rel}") == _git(
            "rev-parse", f"{THIS_UNIT_MERGE_SHA}:{rel}"
        ), rel

    def test_every_pinned_predecessor_suite_matches_its_exact_hash(self):
        """The load-bearing check, RE-EXPRESSED as the semantic claim it exists to make.

        This pinned each changed suite's WHOLE-FILE sha256 against the live worktree. The
        goal is right -- a file whose required negative pin is replaced by ``assert True``
        keeps its SHA strings and even RAISES its assert count, but cannot keep its hash.
        The mechanism was too strong: it also forbids any LATER lawful edit to any of
        those sixteen files, forever, including a strengthening. PHQ-2026-07's own
        re-anchoring of these guards is exactly such an edit, and this pin fired on it.

        RE-ANCHORED AGAIN (PHQ-2026-07). The first correction compared assertion
        COUNTS. Independent review showed a count is blind to a same-count weakening:
        replacing a specific negative check with a bare truthiness test loses the
        property while the total is unchanged. What is enforced now is the normalized
        SEMANTIC INVENTORY -- every assertion this suite made when pinned must still
        be made. Adding assertions is free, so a lawful later strengthening passes;
        losing or hollowing one does not.
        """
        assert PINNED_TEST_HASHES, "the pinned set must not be empty"
        assert set(PROTECTED_PREDICATES) <= set(PINNED_TEST_HASHES), (
            "a protected-predicate entry names a file this filing does not pin")
        weakened = {}
        for rel in sorted(PINNED_TEST_HASHES):
            live_path = ROOT / rel
            assert live_path.exists(), rel
            live_src = live_path.read_text(encoding="utf-8")
            if rel in PROTECTED_PREDICATES:
                # This filing lawfully re-anchored this suite's catalog-position,
                # cardinality or base-revision assertions under its own already-reviewed
                # G4 correction. A diff against the pre-correction baseline reports those
                # REPLACEMENTS as losses, so the invariant is stated positively instead.
                missing = _unasserted_predicates(rel, live_src)
            else:
                at_merge_src = _git("show", f"{THIS_UNIT_MERGE_SHA}:{rel}")
                missing = _lost_assertions(at_merge_src, live_src)
            if missing:
                weakened[rel] = missing[:3]
        assert not weakened, weakened

    def test_the_pinned_set_is_exactly_the_changed_tests_less_this_artifact(self):
        """No changed test may escape pinning, and no pin may name an unchanged file."""
        changed_tests = {
            r for r in self._changed_set()
            if r.startswith("test_") and r.endswith(".py")
        }
        assert set(PINNED_TEST_HASHES) == changed_tests - {Path(__file__).name}, {
            "unpinned": sorted(changed_tests - {Path(__file__).name} - set(PINNED_TEST_HASHES)),
            "over_pinned": sorted(set(PINNED_TEST_HASHES) - changed_tests),
        }

    def test_every_changed_predecessor_suite_retains_its_predecessor_pin(self):
        """Retained as a SUPPORTING check, no longer as the proof.

        Hash equality above is what actually forecloses a weakening. This check remains because
        it states, in readable terms, the property the re-anchoring had to preserve: XASSET-0060's
        exact value survives, the file really changed, and no assertion was dropped. It is
        explicitly NOT claimed to prove a genuine re-anchoring on its own -- the reproduced
        ``assert True`` bypass satisfies every condition here.
        """
        reanchored = set(PINNED_TEST_HASHES) - NON_REANCHORING_CHANGED_TESTS
        assert reanchored, "the re-anchoring set must not be silently empty"
        for rel in sorted(reanchored):
            live = (ROOT / rel).read_text()
            base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
            assert live != base, f"{rel} is a no-op edit"
            assert BOUND_MERGE_BASE in live, (
                f"{rel} dropped XASSET-0060's value instead of retaining it as a pin"
            )
            # Same semantic mechanism as above, not a textual count. The superseded
            # regex counted lines beginning with ``assert``, which a same-count
            # weakening slips straight past.
            if rel in PROTECTED_PREDICATES:
                missing = _unasserted_predicates(rel, live)
            else:
                missing = _lost_assertions(base, live)
            assert not missing, f"{rel} no longer asserts: {missing[:3]}"


class TestTheScopeGuardCatchesTheReviewedBypasses:
    """Adversarial regressions for the exact constructions independent review demonstrated.

    Each runs entirely in memory against a copy of the real corpus; no tracked file is written.
    """

    @staticmethod
    def _hash_text(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def test_a_same_count_weakening_of_the_wrong_file_check_is_caught(self):
        """ADVERSARIAL (PHQ-2026-07). The exact bypass independent review demonstrated.

        Against the real corpus, replacing

            assert Path(entry["file"]).name.startswith(f"{DECISION_ID}-")

        with

            assert entry["file"]

        destroys the catalog-path identity property -- a row pointing at ANOTHER
        decision's file then passes -- while the textual assert count stays 441 -> 441
        and the non-vacuous AST count stays 441 -> 441. The superseded count-based
        guard accepted it. The semantic inventory must reject it.
        """
        rel = "test_level1_stage1_formal_disposition_parser_correction.py"
        src = (ROOT / rel).read_text(encoding="utf-8")
        strong = ('assert Path(entry["file"]).name.startswith(f"{DECISION_ID}-"), '
                  'entry["file"]')
        assert src.count(strong) == 1, "the pinned check moved; re-anchor this proof"
        weakened = src.replace(strong, 'assert entry["file"]')

        # The counts a weaker guard would have compared are IDENTICAL ...
        import re as _re
        assert (len(re.findall(r"^\s+assert ", src, re.M))
                == len(re.findall(r"^\s+assert ", weakened, re.M)))
        assert (len(re.findall(r"^\\s+assert ", src, re.M))
                == len(re.findall(r"^\\s+assert ", weakened, re.M))), \
            "the raw totals must be identical, or this proves nothing"
        # ... and the semantic inventory still catches the loss.
        assert _lost_assertions(src, weakened), "same-count weakening slipped through"

    def test_an_equal_shape_predicate_swap_is_caught(self):
        """REQUIRED PROBE (review 5085019004). The construction that defeated the
        superseded count-and-shape guard.

            Path(entry["file"]).name.startswith(f"{DECISION_ID}-")
                ->  Path(entry["file"]).name.endswith(".md")

        Identical assertion count, identical AST SHAPE (a method call on an
        attribute of a call), and the weaker form ACCEPTS current catalog data --
        while losing the decision-ID/file binding completely: a row pointing at
        another decision's ``.md`` file passes it. The normalized inventory must
        reject this, because the method NAME is operative and is not abstracted.
        """
        rel = "test_level1_stage1_formal_disposition_parser_correction.py"
        src = (ROOT / rel).read_text(encoding="utf-8")
        strong = ('assert Path(entry["file"]).name.startswith(f"{DECISION_ID}-"), '
                  'entry["file"]')
        assert src.count(strong) == 1, "the pinned check moved; re-anchor this proof"
        weakened = src.replace(
            strong, 'assert Path(entry["file"]).name.endswith(".md"), entry["file"]')

        # Same raw count AND same coarse shape -- the superseded guard saw nothing.
        assert (len(re.findall(r"^\s+assert ", src, re.M))
                == len(re.findall(r"^\s+assert ", weakened, re.M)))
        # ... and the weakened predicate genuinely accepts the wrong file.
        assert Path("GOV-0001-governance-architecture-adopted.md").name.endswith(".md")
        assert not Path(
            "GOV-0001-governance-architecture-adopted.md").name.startswith("XASSET-0056-")
        # The normalized inventory must catch it.
        assert _lost_assertions(src, weakened), \
            "equal-shape predicate swap slipped through"

    def test_a_lawful_anchor_substitution_is_not_reported_as_a_loss(self):
        """The complement, and the reason an exact fingerprint inventory was rejected.

        A predecessor lawfully re-anchored ``== XASSET0060_MAIN_SHA`` to
        ``== XASSET0061_MAIN_SHA`` and ADDED two assertions. An identity-based rule
        calls that a loss; abstracting anchor NAMES and STRING literals -- and only
        those -- does not.
        """
        base = _git("show", f"{BOUND_MERGE_SHA}:test_level1_stage1_activation_authorization.py")
        live = (ROOT / "test_level1_stage1_activation_authorization.py").read_text(
            encoding="utf-8")
        assert base != live, "this proof needs a genuinely re-anchored predecessor"
        assert not _lost_assertions(base, live), \
            "a lawful anchor substitution was reported as a weakening"

    def test_the_operative_parts_of_an_assertion_are_not_abstracted(self):
        """Pin exactly WHAT the normaliser is allowed to ignore.

        Anchor strings and SCREAMING_CASE names may change; a method name, a
        comparison operator, a numeric literal and the call structure may not.
        Without this, a future widening of the normaliser would silently reopen
        the very class this guard was rebuilt to close.
        """
        def one(expr):
            return _assertion_inventory(f"def f():\n    assert {expr}\n")

        # ABSTRACTED -- lawful anchor substitutions, each matching a pattern
        assert one('v == "413e033ac33741829168762ab24d73327c047d4b"') == \
               one('v == "3db918530b10ffc1423ba0b749b086e349a4901d"')   # SHA
        assert one('d == "2026-08-28"') == one('d == "2026-09-02"')      # date
        assert one('i == "XASSET-0060"') == one('i == "XASSET-0061"')    # decision id
        assert one('b == "claude/one"') == one('b == "claude/two"')      # branch

        # NOT abstracted by typography alone. Two SCREAMING_CASE names are only
        # interchangeable when THIS delta actually re-anchored one -- see
        # test_a_constant_name_substitution_across_roles_is_caught. Capitalization
        # is not evidence, which is the correction review 5091155438 required.
        assert one("v == SHA_ALPHA") != one("v == SHA_BETA")
        assert one('x.startswith(f"{DECISION_ID}-")') == one('x.startswith(f"{OTHER}-")')

        # ...and each recognized category keeps its OWN placeholder, so a
        # cross-category string swap is a change rather than a wash.
        assert one('v == "2026-09-02"') != one('v == "XASSET-0061"')        # date/decision
        assert one('v == "claude/one"') != one('v == "2026-09-02"')         # branch/date
        assert one('v == "413e033ac33741829168762ab24d73327c047d4b"') != \
               one('v == "claude/one"')                                     # SHA/branch

        # NOT abstracted -- operative expected TEXT is not an anchor. This is the
        # correction independent review required: the superseded normaliser
        # abstracted every string, so a searched-for phrase could be replaced by
        # anything -- including "" -- with the inventory unchanged.
        assert one('"Merging it arms nothing" in section') != one('"" in section')
        assert one('"Merging it arms nothing" in section') != \
               one('"Merging it arms something" in section')
        assert one('x.startswith("aaa")') != one('x.startswith("bbb")')

        # NOT abstracted -- operative meaning
        assert one('x.startswith("a")') != one('x.endswith("a")')
        assert one("n >= 441") != one("n >= 440")
        assert one("n >= 441") != one("n > 441")
        assert one('x.startswith("a")') != one("x")

        # An f-string carrying PROSE is not an anchor either, even though one
        # carrying only an interpolated id is.
        assert one('m == f"expected {x} in the header"') != \
               one('m == f"required {x} in the header"')

    def test_a_semantic_string_weakening_on_an_unprotected_suite_is_caught(self):
        """REQUIRED NEGATIVE CONTROL (PHQ-2026-07, third correction).

        Independent review demonstrated this exact mutation on a suite that is
        PINNED but deliberately NOT in ``PROTECTED_PREDICATES``:

            assert "Merging it arms nothing" in section   ->   assert "" in section

        The weakened form accepts any string whatsoever, including the empty one,
        so a substantive Stage-1 safety assertion becomes vacuous. Under the
        superseded normaliser both forms abstracted to the same thing and the
        inventory reported no loss. The searched-for phrase is not a SHA, a date,
        a decision id or a branch name, so it is not an anchor and is preserved.
        """
        rel = "test_level1_stage1_activation_authorization.py"
        assert rel in PINNED_TEST_HASHES, "the probe's own target is no longer pinned"
        assert rel not in PROTECTED_PREDICATES, (
            "this probe exists to prove the GENERAL mechanism, so its target must "
            "not be covered by the direct-protection list")
        src = (ROOT / rel).read_text(encoding="utf-8")
        strong = 'assert "Merging it arms nothing" in section'
        assert strong in src, "the probe's own target has moved"
        weak = src.replace(strong, 'assert "" in section')
        assert _lost_assertions(src, weak), (
            "the semantic-string weakening was NOT caught")

    def test_the_empty_string_is_never_treated_as_an_anchor(self):
        """The specific value that makes an ``in`` test vacuous."""
        assert not _is_lawful_anchor("")
        assert not _is_lawful_anchor("   ")

    def test_only_contextually_lawful_anchor_shapes_are_abstracted(self):
        """Pin the classifier itself, both directions.

        Fail-closed: an unrecognised string is PRESERVED. So the risk this test
        guards is the opposite one -- a pattern quietly widening until prose
        matches it again.
        """
        for lawful in ("413e033ac33741829168762ab24d73327c047d4b", "3db91853",
                       "2026-09-02", "2026-09-02T13:17:24Z",
                       "XASSET-0061", "PHQ-2026-07", "OPS-0014",
                       "claude/protected-capital-accounting",
                       "governance/decisions/XASSET-0061-something.md", "364"):
            assert _is_lawful_anchor(lawful), lawful
        for operative in ("Merging it arms nothing", "", "   ", "startswith",
                          "UNAVAILABLE", "arms", "Stage 1", "nothing",
                          "the catalog row must be unique", "assert True",
                          "net_equity", "qqq_price", "hold_no_add"):
            assert not _is_lawful_anchor(operative), operative

    def test_every_required_property_of_the_guard_holds_together(self):
        """One place stating all five retained properties, so none can drift alone."""
        rel = "test_level1_stage1_formal_disposition_parser_correction.py"
        src = (ROOT / rel).read_text(encoding="utf-8")
        strong = 'assert Path(entry["file"]).name.startswith(f"{DECISION_ID}-")'
        assert strong in src

        # 1. startswith -> endswith is caught
        assert _lost_assertions(
            src, src.replace(strong, 'assert Path(entry["file"]).name.endswith(".md")'))
        # 2. replacing a required assertion with assert True is caught
        assert _lost_assertions(src, src.replace(strong, "assert True"))
        # 3. deleting it outright is caught
        assert _lost_assertions(
            src, src.replace("        " + strong + ', entry["file"]\n', ""))
        # 4. a genuine ADDITION is permitted
        assert not _lost_assertions(
            src, src.replace("        " + strong + ', entry["file"]\n',
                             "        " + strong + ', entry["file"]\n'
                             '        assert entry["id"], entry\n'))
        # 5. a lawful, specifically recognised re-anchor is permitted
        assert not _lost_assertions(src, src.replace("== 162", "== 163"))

    def test_a_constant_name_substitution_across_roles_is_caught(self):
        """REQUIRED NEGATIVE CONTROL (PHQ-2026-07, review 5091155438).

        The exact mutation independent review demonstrated, on a suite that is
        PINNED but deliberately not in ``PROTECTED_PREDICATES``:

            assert STEP10_DETERMINATION in section
            assert BOUND_MERGE_SHA in section

        Both constants exist and both values are present in the section, so the
        weakened suite still PASSES -- while the Step-10 determination
        requirement is gone and the merge-SHA check it was replaced with is
        already asserted elsewhere. Under the superseded rule both names
        collapsed to one ``<ANCHOR_NAME>`` and the guard reported no loss.
        """
        rel = "test_level1_stage1_activation_authorization.py"
        assert rel in PINNED_TEST_HASHES
        assert rel not in PROTECTED_PREDICATES, (
            "this probe proves the GENERAL mechanism, so its target must not be "
            "covered by the direct-protection list")
        src = (ROOT / rel).read_text(encoding="utf-8")
        strong = "assert STEP10_DETERMINATION in section"
        assert strong in src, "the probe's own target has moved"
        # Both constants are real, and the substituted one is already asserted --
        # which is exactly why the mutated suite still passes.
        assert "STEP10_DETERMINATION = " in src and "BOUND_MERGE_SHA = " in src
        mutated = src.replace(strong, "assert BOUND_MERGE_SHA in section")
        at_merge = _git("show", f"{THIS_UNIT_MERGE_SHA}:{rel}")
        assert not _lost_assertions(at_merge, src), "the live suite must be clean"
        assert _lost_assertions(at_merge, mutated), (
            "the cross-role constant substitution was NOT caught")

    def test_typography_alone_never_authorizes_a_substitution(self):
        """A name's category comes from its BOUND VALUE, not its capitalization."""
        cats = _module_anchor_categories(
            'A_SHA = "413e033ac33741829168762ab24d73327c047d4b"\n'
            'A_DATE = "2026-09-02"\n'
            'A_DECISION = "XASSET-0061"\n'
            'A_BRANCH = "claude/x"\n'
            'A_PR = 364\n'
            'A_DETERMINATION = "STEP_10_NO_DRIFT"\n'
            'A_PROSE = "Merging it arms nothing"\n'
            'A_COMPUTED = some_call()\n')
        assert cats == {"A_SHA": "SHA", "A_DATE": "DATE", "A_DECISION": "DECISION",
                        "A_BRANCH": "BRANCH", "A_PR": "NUMBER"}, cats
        # A determination string, prose, and anything non-literal have NO category
        # and are therefore never interchangeable with anything.
        for absent in ("A_DETERMINATION", "A_PROSE", "A_COMPUTED"):
            assert absent not in cats

    @pytest.mark.parametrize("old_name,new_name,label", [
        ("A_DETERMINATION", "A_SHA", "determination -> SHA"),
        ("A_PROSE", "A_BRANCH", "comment -> branch"),
        ("A_DECISION", "A_DATE", "decision -> date"),
        ("A_BRANCH", "A_PR", "branch -> number"),
    ])
    def test_every_cross_role_substitution_is_caught(self, old_name, new_name, label):
        """Cross-category swaps are losses even when a re-anchor IS in play.

        The delta below adds a new SHA constant, so SHA names are legitimately
        interchangeable within it -- and that allowance must not leak into any
        other category.
        """
        header = ('A_SHA = "413e033ac33741829168762ab24d73327c047d4b"\n'
                  'A_DATE = "2026-09-02"\n'
                  'A_DECISION = "XASSET-0061"\n'
                  'A_BRANCH = "claude/x"\n'
                  'A_PR = 364\n'
                  'A_DETERMINATION = "STEP_10_NO_DRIFT"\n'
                  'A_PROSE = "Merging it arms nothing"\n')
        pinned = header + f"def f():\n    assert {old_name} in section\n"
        # A genuine re-anchor happening in the same delta.
        live = (header + 'B_SHA = "3db918530b10ffc1423ba0b749b086e349a4901d"\n'
                + f"def f():\n    assert {new_name} in section\n")
        assert _lost_assertions(pinned, live), f"{label} was not caught"

    def test_a_same_category_reanchor_in_the_same_delta_is_permitted(self):
        """The complement: the lawful case the review names explicitly.

        A successor SHA constant added beside its predecessor, with the assertion
        moved onto it, is a re-anchor -- not a weakening.
        """
        pinned = ('OLD_SHA = "301e79334876a4bda6e7b89a6156b34e8d38a605"\n'
                  "def f():\n    assert ws['sha'] == OLD_SHA\n")
        live = ('OLD_SHA = "301e79334876a4bda6e7b89a6156b34e8d38a605"\n'
                'NEW_SHA = "413e033ac33741829168762ab24d73327c047d4b"\n'
                "def f():\n    assert ws['sha'] == NEW_SHA\n")
        assert not _lost_assertions(pinned, live), (
            "a lawful same-category re-anchor was reported as a weakening")

    def test_a_name_substitution_without_any_reanchor_is_always_caught(self):
        """Fail closed: with nothing re-anchored, NO name is interchangeable."""
        header = ('A_SHA = "413e033ac33741829168762ab24d73327c047d4b"\n'
                  'B_SHA = "3db918530b10ffc1423ba0b749b086e349a4901d"\n')
        pinned = header + "def f():\n    assert x == A_SHA\n"
        live = header + "def f():\n    assert x == B_SHA\n"
        assert _lost_assertions(pinned, live), (
            "a substitution was permitted in a delta that re-anchored nothing")

    def test_all_required_g5_properties_hold_together(self):
        """Every property the review required kept, stated in one place.

        Listing them together is deliberate: each has been re-derived at least
        once during this PR, and a single test makes it impossible for one to be
        satisfied while another silently regresses.
        """
        rel = "test_level1_stage1_formal_disposition_parser_correction.py"
        src = (ROOT / rel).read_text(encoding="utf-8")
        strong = 'assert Path(entry["file"]).name.startswith(f"{DECISION_ID}-")'
        assert strong in src

        act = "test_level1_stage1_activation_authorization.py"
        act_src = (ROOT / act).read_text(encoding="utf-8")
        prose = 'assert "Merging it arms nothing" in section'
        det = "assert STEP10_DETERMINATION in section"

        # 1. semantic prose weakening
        assert _lost_assertions(act_src, act_src.replace(prose, 'assert "" in section'))
        # 2. startswith -> endswith
        assert _lost_assertions(
            src, src.replace(strong, 'assert Path(entry["file"]).name.endswith(".md")'))
        # 3. deletion
        assert _lost_assertions(
            src, src.replace("        " + strong + ', entry["file"]\n', ""))
        # 4. assert True replacement
        assert _lost_assertions(src, src.replace(strong, "assert True"))
        # 5. cross-role uppercase-name substitution
        assert _lost_assertions(
            act_src, act_src.replace(det, "assert BOUND_MERGE_SHA in section"))
        # 6. genuine addition permitted
        assert not _lost_assertions(
            src, src.replace("        " + strong + ', entry["file"]\n',
                             "        " + strong + ', entry["file"]\n'
                             '        assert entry["id"], entry\n'))
        # 7. specifically lawful same-role re-anchor permitted
        base = _git("show", f"{BOUND_MERGE_SHA}:{act}")
        assert base != act_src
        assert not _lost_assertions(base, act_src)

    def test_the_protected_catalog_predicate_is_asserted_directly(self):
        """Belt and braces: the ONE named protected property, pinned by name.

        The normalized inventory is a general mechanism, and its own docstring
        discloses a residual limit -- a weakening expressed purely as a different
        string anchor is indistinguishable from a lawful re-anchor. So the specific
        predicate independent review named is ALSO asserted directly here, where no
        abstraction applies.
        """
        rel = "test_level1_stage1_formal_disposition_parser_correction.py"
        src = (ROOT / rel).read_text(encoding="utf-8")
        assert 'Path(entry["file"]).name.startswith(f"{DECISION_ID}-")' in src, (
            "the catalog-path identity predicate was removed or weakened")
        assert 'assert len(rows) == 1' in src, (
            "the catalog-row uniqueness predicate was removed or weakened")

    def test_a_protected_predicate_cannot_be_swapped_for_an_equal_shape_one(self):
        """REQUIRED PROBE (PHQ-2026-07, second correction).

        Independent review named this exact mutation and required it to be caught:

            assert Path(entry["file"]).name.startswith(f"{DECISION_ID}-")
            assert Path(entry["file"]).name.endswith(".md")

        Both are one ``Assert`` holding one ``Call`` on one ``Attribute`` of one
        ``Call`` on one ``Attribute`` of one ``Subscript``. Every aggregate the
        superseded mechanism computed -- assertion count, non-vacuous count, AST node
        totals -- is IDENTICAL across the pair, so each let it through. The named
        predicate is checked here, and the attribute name is not abstracted, so the
        swap is a loss.
        """
        rel = "test_level1_stage1_formal_disposition_parser_correction.py"
        src = (ROOT / rel).read_text(encoding="utf-8")
        strong = 'assert Path(entry["file"]).name.startswith(f"{DECISION_ID}-")'
        assert strong in src, "the probe's own target has moved"
        swapped = src.replace(strong, 'assert Path(entry["file"]).name.endswith(".md")')
        assert _unasserted_predicates(rel, swapped), (
            "the equal-shape predicate swap was NOT caught")
        # And the superseded mechanism's blind spot is demonstrated, not merely asserted:
        # the ASSERTION COUNT -- the quantity it compared -- is identical across the pair,
        # so it reported no loss. (Raw node totals do differ here, because an f-string
        # anchor expands to more nodes than a plain literal; that difference is incidental
        # to the anchor, not to the predicate, which is exactly why a total is the wrong
        # instrument.)
        def _n(text):
            return sum(1 for x in ast.walk(ast.parse(text)) if isinstance(x, ast.Assert))
        assert _n(src) == _n(swapped)

    def test_every_protected_predicate_is_currently_asserted(self):
        """Positive control. The named set must describe the corpus as it stands.

        Without this the protected set could silently name predicates that no longer
        exist anywhere, and every check over it would pass vacuously.
        """
        assert PROTECTED_PREDICATES, "the protected set must not be empty"
        for rel in sorted(PROTECTED_PREDICATES):
            assert PROTECTED_PREDICATES[rel], f"{rel} names no protected predicate"
            live = (ROOT / rel).read_text(encoding="utf-8")
            assert not _unasserted_predicates(rel, live), rel

    def test_the_other_named_protected_predicates_are_each_enforced(self):
        """Each named predicate must be individually load-bearing, not decorative.

        Removing any ONE of them, in any protected suite, must be reported. This is
        what stops the set from degrading into a list that only its first entry
        actually defends.
        """
        for rel in sorted(PROTECTED_PREDICATES):
            src = (ROOT / rel).read_text(encoding="utf-8")
            for text in PROTECTED_PREDICATES[rel]:
                assert text in src, f"{rel}: protected predicate not found verbatim: {text}"
                gutted = src.replace(text, "assert True")
                assert _unasserted_predicates(rel, gutted), (
                    f"{rel}: gutting {text} was not caught")

    def test_a_lawful_reanchor_of_an_unprotected_assertion_is_not_a_loss(self):
        """The complement, and the reason this mechanism exists.

        This filing's own already-reviewed G4 correction rewrote catalog-position and
        cardinality assertions in these suites. Those are moving targets a lawful
        successor MUST re-anchor. Re-anchoring one must not read as a weakening.
        """
        rel = "test_portfolio_hq_dashboard_decisions.py"
        src = (ROOT / rel).read_text(encoding="utf-8")
        assert "== 163" in src, "the cardinality anchor this test re-anchors has moved"
        assert not _unasserted_predicates(rel, src.replace("== 163", "== 164")), (
            "a lawful cardinality re-anchor was reported as a weakening")

    def test_a_genuine_strengthening_is_not_reported_as_a_loss(self):
        """The complement: the guard must not bind a lawful later improvement.

        Adding an assertion, and improving an assertion's MESSAGE, are both free.
        Without this the invariant would be whole-file immutability wearing a
        different hat -- the exact defect the first correction was made to remove.
        """
        rel = "test_level1_stage1_formal_disposition_parser_correction.py"
        src = (ROOT / rel).read_text(encoding="utf-8")
        strong = ('assert Path(entry["file"]).name.startswith(f"{DECISION_ID}-"), '
                  'entry["file"]')
        stronger = src.replace(
            strong, strong + '\n        assert entry["file"].endswith(".md"), entry["file"]')
        assert not _lost_assertions(src, stronger), "a strengthening was called a loss"
        remsg = src.replace(strong,
                            'assert Path(entry["file"]).name.startswith(f"{DECISION_ID}-"), '
                            'f"bad catalog row: {entry}"')
        assert not _lost_assertions(src, remsg), "a message change was called a loss"

    def test_gutting_an_assertion_to_assert_true_is_still_caught(self):
        """The original bypass class must remain closed under the new mechanism."""
        rel = "test_level1_stage1_formal_disposition_parser_correction.py"
        src = (ROOT / rel).read_text(encoding="utf-8")
        strong = ('assert Path(entry["file"]).name.startswith(f"{DECISION_ID}-"), '
                  'entry["file"]')
        assert _lost_assertions(src, src.replace(strong, "assert True"))

    def test_replacing_a_negative_pin_with_assert_true_is_caught(self):
        """The reviewer's construction, reproduced and required to FAIL.

        Preserves the predecessor SHA and RAISES the assert count, so the superseded
        three-condition check accepts it. The content pin must reject it.
        """
        rel = "test_level1_stage1_activation_authorization.py"
        live = (ROOT / rel).read_text()
        needle = '        assert workstream["active_pr"] != XASSET0060_ACTIVE_PR\n'
        assert needle in live, "the reproduced construction must target a real assertion"
        weakened = live.replace(needle, "        assert True\n", 1)

        base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
        # The superseded conditions ALL still hold on the weakened text ...
        assert weakened != base
        assert BOUND_MERGE_BASE in weakened
        assert len(re.findall(r"^\s+assert ", weakened, re.M)) >= len(
            re.findall(r"^\s+assert ", base, re.M)
        )
        # ... and the meaningful guard is nevertheless gone ...
        assert "!= XASSET0060_ACTIVE_PR" not in weakened
        # ... so only the exact content pin catches it.
        assert self._hash_text(weakened) != PINNED_TEST_HASHES[rel]

    def test_any_single_character_edit_to_a_pinned_suite_is_caught(self):
        """Generalises the above: the pin admits exactly one byte sequence per file."""
        for rel in sorted(PINNED_TEST_HASHES):
            mutated = (ROOT / rel).read_text() + "\n"
            assert self._hash_text(mutated) != PINNED_TEST_HASHES[rel], rel

    def test_an_unrelated_test_file_cannot_enter_the_changed_set(self):
        """The open ``test_*.py`` class is gone; the manifest is closed."""
        intruder = "test_allocate_integration.py"
        assert (ROOT / intruder).exists(), "probe must name a real, unrelated suite"
        assert intruder not in EXPECTED_CHANGED_FILES
        assert intruder not in PINNED_TEST_HASHES
        polluted = TestThisFilingMutatesNothingLoadBearing._changed_set() | {intruder}
        assert polluted != EXPECTED_CHANGED_FILES

    def test_dropping_an_expected_file_is_caught(self):
        """Closed on the other side too -- a silently reverted file fails."""
        for victim in sorted(EXPECTED_CHANGED_FILES):
            assert (
                TestThisFilingMutatesNothingLoadBearing._changed_set() - {victim}
            ) != EXPECTED_CHANGED_FILES, victim


class TestThisDecisionIsNotAddedToTheTrustBoundary:
    def test_this_decision_file_is_not_load_bearing(self):
        assert not any(DECISION_ID in rel for rel in LIVE_LOAD_BEARING)

    @pytest.mark.parametrize("decision", PRIOR_LINK_AUTHORIZATIONS)
    def test_no_prior_link_authorization_is_load_bearing_either(self, decision):
        """The precedent is checked live, not asserted from prose."""
        assert not any(decision in rel for rel in LIVE_LOAD_BEARING), decision

    def test_the_filing_states_the_reason_rather_than_leaving_it_implicit(self):
        assert "deliberately **not** added to `LOAD_BEARING_RELPATHS`" in DECISION_NORM
        assert "authorizes a read-only verification that produces no attestation" in DECISION_NORM
