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
import datetime
import textwrap
import hashlib
import re
import subprocess
import sys
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

#: The one shared live WS-0014 binding is intentionally separate from this
#: historical filing's immutable identities above. Only this current-binding
#: control changes when legitimate live GitHub state advances again.
CURRENT_WS0014_BINDING = {
    "active_branch": "claude/protected-capital-accounting",
    "active_pr": 364,
    "last_verified_main_sha": "3db918530b10ffc1423ba0b749b086e349a4901d",
    "last_verified_date": "2026-09-02",
}
WS0014_REGISTER_FIELDS = frozenset(CURRENT_WS0014_BINDING)
EXPECTED_RETAINED_REGISTER_NEGATIVES = 316

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


#: A string value is an ANCHOR CANDIDATE only if it has one of these complete,
#: domain-valid forms. Shape categorizes a registry endpoint; it never authorizes
#: substitution. Every value remains exact unless its own assertion occurrence is
#: explicitly registered below.
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
#: FAIL-CLOSED: a string that does not match one cannot be a registry endpoint.
#: Categories also prevent cross-domain endpoint pairings: a decision id cannot
#: pair with a date, nor a determination string with a merge SHA.
_ANCHOR_CATEGORIES = (
    # NUMBER FIRST, deliberately. A digits-only token is an IDENTIFIER -- a PR,
    # run, job, review or comment number -- not a commit SHA. Independent review
    # 5092359752 demonstrated the opposite ordering classifying the review id
    # `4976985695` as a SHA, which made it interchangeable with a real 40-hex
    # merge SHA and let a cross-domain weakening pass unseen.
    ("NUMBER",        re.compile(r"^\d+$")),
    ("SHA",           re.compile(r"^[0-9a-f]{7,40}$")),
    # A COMPLETE date or timestamp, anchored at BOTH ends AND validated component
    # by component. Two reviews shaped this. 5093063766 showed the prefix form
    # treating operative prose as an anchor ("2026-08-27 Merging it arms nothing"
    # classified as DATE). 5093500583 then showed that anchoring the shape is not
    # enough either: only `text[:10]` was validated, so "2026-08-27T99:99:99Z"
    # was still a DATE. Digit SHAPE is not a domain -- every component is now
    # range-checked by `_is_valid_date_or_timestamp()`.
    ("DATE",          re.compile(
        r"^\d{4}-\d{2}-\d{2}"
        r"(?:[T ]\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)?$")),
    ("DECISION",      re.compile(r"^[A-Z][A-Z0-9]{1,9}-\d{4}(-\d{2})?$")),
    ("BRANCH",        re.compile(r"^claude/[A-Za-z0-9._\-/]+$")),
    ("DECISION_FILE", re.compile(r"^governance/decisions/[A-Za-z0-9._\-]+\.md$")),
)


#: A complete date, or a complete timestamp, decomposed into its components so
#: each one can be RANGE-CHECKED. The pattern alone constrains only digit count.
_DATETIME_SHAPE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})"
    r"(?:[T ](?P<hh>\d{2}):(?P<mm>\d{2})(?::(?P<ss>\d{2}))?(?P<frac>\.\d+)?"
    r"(?P<off>Z|[+-]\d{2}:?\d{2})?)?$")


def _is_valid_date_or_timestamp(text: str) -> bool:
    """Whether every supplied component is a real value in its own domain.

    SHAPE IS NOT A DOMAIN. Independent review 5093500583 demonstrated the gap
    directly: the previous check validated only ``text[:10]``, so
    ``2026-08-27T99:99:99Z`` -- a well-shaped string whose hour, minute and
    second are all impossible -- was accepted as a DATE anchor candidate. Each
    component is now checked against its own range:

    * the calendar date must be real (``2026-02-30`` is not);
    * hour 0-23, minute 0-59, second 0-59;
    * a UTC offset's own hour 0-23 and minute 0-59.

    Anything else cannot be a registered endpoint and is compared VERBATIM.
    """
    m = _DATETIME_SHAPE.match(text)
    if m is None:
        return False
    try:
        datetime.date.fromisoformat(m.group("date"))
    except ValueError:
        return False
    hh, mm, ss = m.group("hh"), m.group("mm"), m.group("ss")
    if hh is not None:
        if not (0 <= int(hh) <= 23 and 0 <= int(mm) <= 59):
            return False
        # A leap second is not representable here, and accepting 60 would let an
        # impossible value through; 0-59 is the domain this corpus asserts on.
        if ss is not None and not 0 <= int(ss) <= 59:
            return False
    off = m.group("off")
    if off is not None and off != "Z":
        digits = off[1:].replace(":", "")
        if len(digits) != 4:
            return False
        if not (0 <= int(digits[:2]) <= 23 and 0 <= int(digits[2:]) <= 59):
            return False
    return True


def _anchor_category(text: str) -> str | None:
    """Which anchor category this exact string belongs to, or None.

    FAIL-CLOSED. A string matching no category cannot be a registry endpoint and
    is preserved verbatim. A matching category is candidate evidence only; file
    and assertion identity still decide authorization. The empty string is never
    an anchor -- it is the vacuous-``in`` bypass itself.
    """
    t = text.strip()
    if not t:
        return None
    for name, pattern in _ANCHOR_CATEGORIES:
        if not pattern.match(t):
            continue
        if name == "DATE" and not _is_valid_date_or_timestamp(t):
            # A well-shaped string that is not a real date is not an anchor.
            # Fail closed: it stays verbatim and cannot be a registry endpoint.
            return None
        return name
    return None


#: THE COMPLETE, ENUMERATED SET of lawful bare-literal re-anchors, identified by
#: OCCURRENCE rather than by value.
#:
#: Independent review 5093500583 showed why the value pair alone is not an
#: identity. Enumerating ``("2026-08-27", "2026-08-28", "DATE")`` authorized EVERY
#: structurally matching occurrence of that pair, so one lawful WS-0014 transition
#: still laundered an unrelated `freeze["cutoff"] == "2026-08-27"` assertion in the
#: same delta. Narrower than the category-wide defect before it, but the same G5
#: assurance class.
#:
#: An entry is therefore ``(relpath, pinned_fingerprint_sha256, predecessor,
#: successor, category)``. The identity is the exact FILE plus the exact PINNED
#: ASSERTION -- its exact AST fingerprint, digested -- so a second
#: assertion in the same file using the same values has a different fingerprint,
#: matches no entry, and stays verbatim. Each entry is consumed AT MOST ONCE.
#:
#: These six are DERIVED FROM THE CORPUS, not invented: running the inventory with
#: literal substitution disabled entirely across every pinned predecessor suite
#: reports exactly these six assertions, and nothing else. (Every other reported
#: loss falls in a suite covered by ``PROTECTED_PREDICATES``, whose assertions this
#: filing lawfully REWROTE under its own already-reviewed G4 correction and which
#: the inventory therefore does not govern.) The five date sites and the one branch
#: site are listed individually, never collapsed into value-pair licences.
#:
#: Two sites share a fingerprint digest because their assertions are genuinely
#: identical in shape; they remain SEPARATE entries because their relpaths differ,
#: and each is consumed only against its own file.
BARE_LITERAL_REANCHORS = (
    # WS-0014 last_verified_date, asserted via startswith(...)
    ("test_level1_stage1_activation_authorization.py",
     "9a8aa1ddce1eba7caf2e9087127624569232d881a4e93ddb6abd8126a37d4424",
     "2026-08-27", "2026-08-28", "DATE"),
    # WS-0014 last_verified_date, asserted via str(...) == ...
    ("test_level1_stage1_post_merge_ci_recovery_authorization.py",
     "fb39f66109d21ec62b88c14deca754ea25217c404c60ed1a7637a99fa874dae3",
     "2026-08-27", "2026-08-28", "DATE"),
    # WS-0014 last_verified_date, asserted via startswith(...)
    ("test_level1_stage1_post_rebinding_drift_authorization.py",
     "9a8aa1ddce1eba7caf2e9087127624569232d881a4e93ddb6abd8126a37d4424",
     "2026-08-27", "2026-08-28", "DATE"),
    # WS-0014 active_branch, predecessor retained beside it as a negative pin
    ("test_level1_stage1_pr337_actor_evidence_correction_authorization.py",
     "ec18917190cc524eca9548bad3155e74f6f085f4b780b0c95c020037c73a8ce9",
     "claude/xasset-0057-rebinding-gqtg9o", "claude/xasset-0061-authorization-jux8p9", "BRANCH"),
    # WS-0014 last_verified_date, asserted via str(...) == ...
    ("test_level1_stage1_pr337_actor_evidence_correction_authorization.py",
     "fb39f66109d21ec62b88c14deca754ea25217c404c60ed1a7637a99fa874dae3",
     "2026-08-27", "2026-08-28", "DATE"),
    # WS-0014 last_verified_date, asserted via startswith(...)
    ("test_level1_stage1_readiness_verification_authorization.py",
     "9a8aa1ddce1eba7caf2e9087127624569232d881a4e93ddb6abd8126a37d4424",
     "2026-08-27", "2026-08-28", "DATE"),
)


#: THE COMPLETE, ENUMERATED SET of lawful NAMED-anchor re-anchors, identified by
#: assertion occurrence rather than by a shared name role or raw value.
#:
#: Review 5094619011 demonstrated that ``(role, category)`` is only a candidate
#: relationship, never an occurrence identity. Globally normalising every name in
#: that slot let one legitimate current-anchor move hide a distinct historical
#: negative-pin rewrite. Globally normalising the values bound to those names also
#: let the same move hide an unrelated raw-literal rewrite.
#:
#: An entry is ``(relpath, pinned_fingerprint_sha256, predecessor_name,
#: predecessor_value, successor_name, successor_value, category)``. It is honoured
#: only when each endpoint name has exactly one binding occurrence in its source,
#: that unique occurrence is the exact registered literal declaration, the exact
#: pinned assertion has the registered fingerprint, and replacing the predecessor
#: NAME in that assertion produces an exact live assertion. Each entry is consumed
#: at most once. Raw literal values are never substituted.
#:
#: These eleven entries are derived from the pinned corpus with all name and value
#: normalisation disabled: eight MAIN_SHA sites and three ACTIVE_PR sites. No other
#: unprotected predecessor assertion requires a named transition.
NAMED_ANCHOR_REANCHORS = (
    ("test_level1_stage1_activation_authorization.py",
     "f6a3da01089237bfcb3a2c9f8f2a53e91004e350f004488fac0f14f9e3c08fc6",
     "XASSET0060_MAIN_SHA", "301e79334876a4bda6e7b89a6156b34e8d38a605",
     "XASSET0061_MAIN_SHA", "413e033ac33741829168762ab24d73327c047d4b", "SHA"),
    ("test_level1_stage1_activation_authorization.py",
     "754cc03b460b6177bab460349422c46f2d153b056601840d18add8c5ff428031",
     "XASSET0060_ACTIVE_PR", 361, "XASSET0061_ACTIVE_PR", 362, "NUMBER"),
    ("test_level1_stage1_post_correction_rebinding.py",
     "9091c5fc8b7b1669c3179422d3718997a125cda242bfd06f5b7b21338802203b",
     "XASSET0060_MAIN_SHA", "301e79334876a4bda6e7b89a6156b34e8d38a605",
     "XASSET0061_MAIN_SHA", "413e033ac33741829168762ab24d73327c047d4b", "SHA"),
    ("test_level1_stage1_post_correction_rebinding_authorization.py",
     "9091c5fc8b7b1669c3179422d3718997a125cda242bfd06f5b7b21338802203b",
     "XASSET0060_MAIN_SHA", "301e79334876a4bda6e7b89a6156b34e8d38a605",
     "XASSET0061_MAIN_SHA", "413e033ac33741829168762ab24d73327c047d4b", "SHA"),
    ("test_level1_stage1_post_merge_ci_recovery_authorization.py",
     "9091c5fc8b7b1669c3179422d3718997a125cda242bfd06f5b7b21338802203b",
     "XASSET0060_MAIN_SHA", "301e79334876a4bda6e7b89a6156b34e8d38a605",
     "XASSET0061_MAIN_SHA", "413e033ac33741829168762ab24d73327c047d4b", "SHA"),
    ("test_level1_stage1_post_merge_ci_recovery_reauthorization.py",
     "9091c5fc8b7b1669c3179422d3718997a125cda242bfd06f5b7b21338802203b",
     "XASSET0060_MAIN_SHA", "301e79334876a4bda6e7b89a6156b34e8d38a605",
     "XASSET0061_MAIN_SHA", "413e033ac33741829168762ab24d73327c047d4b", "SHA"),
    ("test_level1_stage1_post_rebinding_drift_authorization.py",
     "f6a3da01089237bfcb3a2c9f8f2a53e91004e350f004488fac0f14f9e3c08fc6",
     "XASSET0060_MAIN_SHA", "301e79334876a4bda6e7b89a6156b34e8d38a605",
     "XASSET0061_MAIN_SHA", "413e033ac33741829168762ab24d73327c047d4b", "SHA"),
    ("test_level1_stage1_post_rebinding_drift_authorization.py",
     "754cc03b460b6177bab460349422c46f2d153b056601840d18add8c5ff428031",
     "XASSET0060_ACTIVE_PR", 361, "XASSET0061_ACTIVE_PR", 362, "NUMBER"),
    ("test_level1_stage1_pr337_actor_evidence_correction_authorization.py",
     "9091c5fc8b7b1669c3179422d3718997a125cda242bfd06f5b7b21338802203b",
     "XASSET0060_MAIN_SHA", "301e79334876a4bda6e7b89a6156b34e8d38a605",
     "XASSET0061_MAIN_SHA", "413e033ac33741829168762ab24d73327c047d4b", "SHA"),
    ("test_level1_stage1_readiness_verification_authorization.py",
     "f6a3da01089237bfcb3a2c9f8f2a53e91004e350f004488fac0f14f9e3c08fc6",
     "XASSET0060_MAIN_SHA", "301e79334876a4bda6e7b89a6156b34e8d38a605",
     "XASSET0061_MAIN_SHA", "413e033ac33741829168762ab24d73327c047d4b", "SHA"),
    ("test_level1_stage1_readiness_verification_authorization.py",
     "754cc03b460b6177bab460349422c46f2d153b056601840d18add8c5ff428031",
     "XASSET0060_ACTIVE_PR", 361, "XASSET0061_ACTIVE_PR", 362, "NUMBER"),
)

#: One-time conversion of predecessor suites from mutable-current positive pins
#: into immutable-generation negative pins. Each row is the exact file and exact
#: source fingerprint at XASSET-0061's accepted merge plus the exact live target
#: fingerprint. Every target is a literal-bound negative predicate, so arbitrary
#: runtime mutation of a Python anchor name cannot change what it excludes. This
#: registry is finite:
#: future WS-0014 advances update only CURRENT_WS0014_BINDING and the YAML,
#: never these predecessor files or this occurrence set.
HISTORICALIZED_REGISTER_ASSERTIONS = (
    ("test_level1_stage1_activation_authorization.py",
     "2ccd878bd135b5e668d581e98c9e97efe386cc17ccfc1825775106f42f3def0b",
     "708f32b54d0372e5da3505592aa656bb35f1e3d0af2122d03ced1fc2f07282dd"),
    ("test_level1_stage1_activation_authorization.py",
     "d1b184ce6e0b62da91fb06850d4b3c022ba6c8c48da74d995492b5fc269ae9fb",
     "48e9d6da92c7bc43cb956ed424c7675f46b59115d0ece9bc89bef71abbe7acb4"),
    ("test_level1_stage1_activation_authorization.py",
     "2cef5c73b2b89234dc504e858fec797e0b96ec6c0fb8367520761dc124ad5afc",
     "21c05d602a20acdb4be2289de17b3c2d50a0fdedd377ac3ac79582b97a28af29"),
    ("test_level1_stage1_post_correction_rebinding.py",
     "dbafa124103b3c171ddc6560dfc24715ddc88bfca7a533838ebe2d275c672df1",
     "8b868fa9f788c9074bc6a2ed0052e7cc4e01422158b3d871ba3b4c1424e23ba2"),
    ("test_level1_stage1_post_correction_rebinding_authorization.py",
     "dbafa124103b3c171ddc6560dfc24715ddc88bfca7a533838ebe2d275c672df1",
     "8b868fa9f788c9074bc6a2ed0052e7cc4e01422158b3d871ba3b4c1424e23ba2"),
    ("test_level1_stage1_post_merge_ci_recovery_authorization.py",
     "dbafa124103b3c171ddc6560dfc24715ddc88bfca7a533838ebe2d275c672df1",
     "8b868fa9f788c9074bc6a2ed0052e7cc4e01422158b3d871ba3b4c1424e23ba2"),
    ("test_level1_stage1_post_merge_ci_recovery_authorization.py",
     "d5bb6540e5d94bcbf801b781c9cbf540f9ef73f1f313f4854fe200c9079579ec",
     "b7ec8413608ef8d1fab1560954eae1031e5a3d220cf0d108e3e760493b928444"),
    ("test_level1_stage1_post_merge_ci_recovery_reauthorization.py",
     "dbafa124103b3c171ddc6560dfc24715ddc88bfca7a533838ebe2d275c672df1",
     "8b868fa9f788c9074bc6a2ed0052e7cc4e01422158b3d871ba3b4c1424e23ba2"),
    ("test_level1_stage1_post_parser_correction_rebinding_authorization.py",
     "19a8f8c58b491b2e2b76c7190f0461ad9ac338418c58abda445523bb8a448c97",
     "064ccbfdbaa39b8f4a2771aad0709e6d2317a72b4536e16bb4e37332b950182f"),
    ("test_level1_stage1_post_parser_correction_rebinding_authorization.py",
     "ac5229c6d8ba43b0522d8cc62b65a831226189257198ad0264245c82ca72afde",
     "5d06702073811275dc9e070e5c4bad7fc8c5963181830d71140b446e577270d0"),
    ("test_level1_stage1_post_rebinding_drift_authorization.py",
     "2ccd878bd135b5e668d581e98c9e97efe386cc17ccfc1825775106f42f3def0b",
     "708f32b54d0372e5da3505592aa656bb35f1e3d0af2122d03ced1fc2f07282dd"),
    ("test_level1_stage1_post_rebinding_drift_authorization.py",
     "d1b184ce6e0b62da91fb06850d4b3c022ba6c8c48da74d995492b5fc269ae9fb",
     "48e9d6da92c7bc43cb956ed424c7675f46b59115d0ece9bc89bef71abbe7acb4"),
    ("test_level1_stage1_post_rebinding_drift_authorization.py",
     "2cef5c73b2b89234dc504e858fec797e0b96ec6c0fb8367520761dc124ad5afc",
     "21c05d602a20acdb4be2289de17b3c2d50a0fdedd377ac3ac79582b97a28af29"),
    ("test_level1_stage1_pr337_actor_evidence_correction_authorization.py",
     "f5ce46c934051b62f3df6ae4dfd1f6fa9a03f79838059f6a894976e2d0ed9362",
     "58ee1e0dadbb15ed0b670eccf7a3e24abd04a3896ee86152e6a97642412cb4d0"),
    ("test_level1_stage1_pr337_actor_evidence_correction_authorization.py",
     "dbafa124103b3c171ddc6560dfc24715ddc88bfca7a533838ebe2d275c672df1",
     "8b868fa9f788c9074bc6a2ed0052e7cc4e01422158b3d871ba3b4c1424e23ba2"),
    ("test_level1_stage1_pr337_actor_evidence_correction_authorization.py",
     "d5bb6540e5d94bcbf801b781c9cbf540f9ef73f1f313f4854fe200c9079579ec",
     "b7ec8413608ef8d1fab1560954eae1031e5a3d220cf0d108e3e760493b928444"),
    ("test_level1_stage1_readiness_verification_authorization.py",
     "2ccd878bd135b5e668d581e98c9e97efe386cc17ccfc1825775106f42f3def0b",
     "708f32b54d0372e5da3505592aa656bb35f1e3d0af2122d03ced1fc2f07282dd"),
    ("test_level1_stage1_readiness_verification_authorization.py",
     "d1b184ce6e0b62da91fb06850d4b3c022ba6c8c48da74d995492b5fc269ae9fb",
     "48e9d6da92c7bc43cb956ed424c7675f46b59115d0ece9bc89bef71abbe7acb4"),
    ("test_level1_stage1_readiness_verification_authorization.py",
     "2cef5c73b2b89234dc504e858fec797e0b96ec6c0fb8367520761dc124ad5afc",
     "21c05d602a20acdb4be2289de17b3c2d50a0fdedd377ac3ac79582b97a28af29"),

    # The five suites routed through PROTECTED_PREDICATES need the same exact
    # occurrence protection for their newly historical register predicates.
    ("test_level1_stage1_formal_disposition_parser_correction_authorization.py",
     "19a8f8c58b491b2e2b76c7190f0461ad9ac338418c58abda445523bb8a448c97",
     "064ccbfdbaa39b8f4a2771aad0709e6d2317a72b4536e16bb4e37332b950182f"),
    ("test_level1_stage1_formal_disposition_parser_correction_authorization.py",
     "ac5229c6d8ba43b0522d8cc62b65a831226189257198ad0264245c82ca72afde",
     "5d06702073811275dc9e070e5c4bad7fc8c5963181830d71140b446e577270d0"),
    ("test_level1_stage1_parser_contract_correction_authorization.py",
     "e44d97a2654922db1d77ccdc014e490118777039e671de7a8907e79db560e9be",
     "58ee1e0dadbb15ed0b670eccf7a3e24abd04a3896ee86152e6a97642412cb4d0"),
    ("test_level1_stage1_parser_contract_correction_authorization.py",
     "e4f4231a90d6bab860535b4798918114f8eca81beea106326899fc99545d369f",
     "8b868fa9f788c9074bc6a2ed0052e7cc4e01422158b3d871ba3b4c1424e23ba2"),
    ("test_level1_stage1_post_merge_ci_recovery_reconciliation.py",
     "6531fc8ab57ca19e7edfbed9dee040bcc8fd95823173e7b8abbd6c2f1a117560",
     "c864fa0567da6bb474892c2e2735277fbef880454c6b3b317e3af1f7f3e9909e"),
    ("test_level1_stage1_post_merge_ci_recovery_reconciliation.py",
     "abf86d25e136723d2376c98dcec9f39644ccb4d6b15c8fed014f22c71bbb3084",
     "7dad9b98303769ae9c6e0dce0ab891e597b131bd4018f2e73f8bf30d7ac5a2f7"),
    ("test_level1_stage1_post_merge_ci_recovery_reconciliation.py",
     "abf86d25e136723d2376c98dcec9f39644ccb4d6b15c8fed014f22c71bbb3084",
     "7dad9b98303769ae9c6e0dce0ab891e597b131bd4018f2e73f8bf30d7ac5a2f7"),
    ("test_level1_stage1_post_parser_correction_operational_rebinding.py",
     "98832ed7c8ea617746dab05af3a976436b6b4f0564624162acf865402bdb3ce3",
     "58ee1e0dadbb15ed0b670eccf7a3e24abd04a3896ee86152e6a97642412cb4d0"),
    ("test_level1_stage1_post_parser_correction_operational_rebinding.py",
     "c3d19fec7a3c6520ddb615e7dcda1ecc2dd793de8769009c57c05c00a2244fff",
     "8b868fa9f788c9074bc6a2ed0052e7cc4e01422158b3d871ba3b4c1424e23ba2"),
    ("test_level1_stage1_post_parser_correction_operational_rebinding.py",
     "c5a9a677842c286ee149fe058fe9f00a5d9062638b5f9b7a96a02ceb914fdeb8",
     "800a2a0eb3d5b305b1415770aad86aa66b19d79d3dc01e95aa8bb5fba210c3ce"),
    ("test_level1_stage1_verdict_boundary_governance.py",
     "a7ff7d9401d1ca98525e7030552ded339e4e96d3fb84c9a4fe2dfc8949e8d79b",
     "bdecd00f37afa0aec457cc30ac1a7f1df4a7b4a1bddf4a67545ed81b2973b11c"),
    ("test_level1_stage1_verdict_boundary_governance.py",
     "00b5457cef4520b209327edb7a92a86bd9143b1eb619764c0f409a0f05ff3368",
     "d082f7c9b01f2ed796461100dd3d1114ae907b0be733b0d1cc946826ee77aa43"),
    ("test_level1_stage1_verdict_boundary_governance.py",
     "7d5311f304ec46ba1ac6a8d1200f0e4942ca4c2c66ecc9dd5066272b84bcc5c8",
     "d082f7c9b01f2ed796461100dd3d1114ae907b0be733b0d1cc946826ee77aa43"),
    ("test_level1_stage1_verdict_boundary_governance.py",
     "00b5457cef4520b209327edb7a92a86bd9143b1eb619764c0f409a0f05ff3368",
     "d082f7c9b01f2ed796461100dd3d1114ae907b0be733b0d1cc946826ee77aa43"),
)


#: The instance-distinguishing token a constant name carries -- ``XASSET0061_``,
#: ``OLD_``, ``B_``. Stripping it leaves the SEMANTIC ROLE: the slot the value
#: occupies, independent of which decision instance owns it.
_INSTANCE_PREFIX = re.compile(
    r"^(?:[A-Z][A-Z0-9]*\d+|OLD|NEW|PREV|PREVIOUS|CURRENT|PRIOR|[AB])_")


def _anchor_role(name: str) -> str:
    """The semantic slot a constant name occupies.

    ``XASSET0060_MAIN_SHA`` and ``XASSET0061_MAIN_SHA`` are the SAME role
    (``MAIN_SHA``) in two decision instances -- that pairing is what makes a
    re-anchor lawful. ``BOUND_MERGE_SHA`` is a different role entirely, so it is
    never interchangeable with either, however similar its typography or its
    category.
    """
    return _INSTANCE_PREFIX.sub("", name, count=1)


def _anchor_name_bindings(source: str) -> dict:
    """``name -> [binding, ...]`` for every name binding occurrence in ``source``.

    A binding is ``(category, literal_value)`` only for a direct, anchor-shaped
    literal assignment. Every other binding form is represented by ``None``. The
    list retains multiplicity across every lexical scope: a nested assignment is
    still a second occurrence and makes the name ambiguous for registry purposes.

    Counting *bindings*, rather than only recognised anchor assignments, is the
    fail-closed detail. Otherwise a non-literal or differently-shaped shadow could
    be ignored while an unrelated decoy supplies the registry's approved value.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}

    direct_literals = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, (ast.AnnAssign, ast.NamedExpr)):
            targets, value = (node.target,), node.value
        else:
            continue
        if not isinstance(value, ast.Constant) or isinstance(value.value, bool):
            continue
        literal = value.value
        if isinstance(literal, str):
            category = _anchor_category(literal)
        elif isinstance(literal, int):
            category = "NUMBER"
        else:
            category = None
        if category is None:
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                direct_literals[id(target)] = (category, literal)

    out = collections.defaultdict(list)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            out[node.id].append(direct_literals.get(id(node)))
        elif isinstance(node, ast.arg):
            out[node.arg].append(None)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out[node.name].append(None)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                out[alias.asname or alias.name.split(".", 1)[0]].append(None)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            out[node.name].append(None)
        elif isinstance(node, (ast.MatchAs, ast.MatchStar)) and node.name:
            out[node.name].append(None)
        elif isinstance(node, ast.MatchMapping) and node.rest:
            out[node.rest].append(None)
    return dict(out)


def _module_anchor_constants(source: str) -> dict:
    """``name -> (category, value)`` for unambiguous anchor declarations.

    Category comes from the BOUND VALUE, never from typography:
    ``STEP10_DETERMINATION = "STEP_10_NO_DRIFT"`` is not an anchor at all, while
    ``BOUND_MERGE_SHA = "413e033a..."`` is a SHA. A name bound to anything
    non-literal has no category and cannot be a registered endpoint.

    Every lexical scope is scanned because several predecessor suites bind their
    re-anchor constants inside the test function that uses them. A name is
    returned only when it has EXACTLY ONE binding occurrence anywhere and that
    occurrence is a direct anchor-shaped literal assignment. A second binding is
    ambiguity even when it repeats the same value: uniqueness is occurrence
    evidence, and an unrelated nested decoy must never certify a module binding.
    """
    return {
        name: bindings[0]
        for name, bindings in _anchor_name_bindings(source).items()
        if (_ANCHOR_NAME.match(name)
            and len(bindings) == 1
            and bindings[0] is not None)
    }


def _module_anchor_categories(source: str) -> dict:
    """``name -> category`` view of :func:`_module_anchor_constants`."""
    return {n: cat for n, (cat, _v) in _module_anchor_constants(source).items()}


def _anchor_value_category(value) -> str | None:
    """The anchor category of an exact constant value, with bool excluded."""
    if isinstance(value, bool):
        return None
    if isinstance(value, str):
        return _anchor_category(value)
    if isinstance(value, int):
        return "NUMBER"
    return None


def _is_lawful_anchor(text: str) -> bool:
    """Whether this string has the SHAPE of a value a re-anchor may change.

    Shape alone no longer authorizes anything -- the occurrence registries require
    exact file, fingerprint and endpoint evidence. This predicate states only
    which forms are anchor-shaped at all; empty strings and operative prose are
    not among them.
    """
    return _anchor_category(text) is not None


def _assertion_inventory(source: str) -> collections.Counter:
    """The suite's assertions as exact semantic fingerprints.

    A ``Counter``, so removing one of several identical assertions is still a loss.
    ``assert True``/``assert 1`` are excluded: they are the shape a silent gutting
    takes, and counting them would let a weakened file keep its total.

    No name or literal is normalized here. Lawful moving anchors are handled only
    by the occurrence registries in :func:`_lost_assertions`; keeping the general
    inventory exact prevents a registry from becoming a global substitution map.
    """
    return collections.Counter(_assertion_fingerprints(source))


def _assertion_fingerprints(source: str) -> list[str]:
    """Exact AST fingerprints for every non-vacuous assertion in ``source``."""
    out = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Assert):
            continue
        test = node.test
        if isinstance(test, ast.Constant) and bool(test.value) is True:
            continue          # vacuous by construction
        out.append(ast.dump(test))
    return out


def _register_negative_inventory(source: str) -> collections.Counter:
    """Exact negative assertions about WS-0014's four moving fields."""
    out = collections.Counter()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Assert):
            continue
        strings = {
            child.value for child in ast.walk(node.test)
            if isinstance(child, ast.Constant) and isinstance(child.value, str)
        }
        if not strings.intersection(WS0014_REGISTER_FIELDS):
            continue
        negative = any(
            isinstance(child, (ast.NotEq, ast.NotIn))
            or (isinstance(child, ast.UnaryOp) and isinstance(child.op, ast.Not))
            for child in ast.walk(node.test)
        )
        if negative:
            out[ast.dump(node.test)] += 1
    return out


def _ws0014_binding_errors(workstream: dict) -> set[str]:
    """Return every live self-reference field that is not the exact binding."""
    actual = dict(workstream)
    actual["last_verified_date"] = str(actual.get("last_verified_date"))
    return {
        field for field, expected in CURRENT_WS0014_BINDING.items()
        if actual.get(field) != expected
    }


def _fingerprint_digest(fingerprint: str) -> str:
    """The stable identity of one exact assertion shape."""
    return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()


def _registered_occurrences(relpath):
    """The lawful bare-literal transitions for THIS FILE, each usable once.

    Returns ``{pinned_fingerprint_digest: [(predecessor, successor, category), ...]}``.
    With no relpath -- a synthetic comparison, or a caller that did not say which
    file it is comparing -- NOTHING is registered. That is the fail-closed
    default: an unidentified comparison authorizes no literal substitution at all.
    """
    out = {}
    if not relpath:
        return out
    for rel, digest, old, new, cat in BARE_LITERAL_REANCHORS:
        if rel == relpath:
            out.setdefault(digest, []).append((old, new, cat))
    return out


def _historicalized_occurrences(relpath):
    """Exact source occurrence -> exact literal-bound historical targets."""
    if not relpath:
        return {}
    out = {}
    for rel, source_digest, target_digest in HISTORICALIZED_REGISTER_ASSERTIONS:
        if rel == relpath:
            out.setdefault(source_digest, []).append(target_digest)
    return out


def _historicalized_registration_losses(pinned_src: str, live_src: str, relpath):
    """Missing registered sources or literal targets, including multiplicity."""
    rows = [
        (source, target)
        for rel, source, target in HISTORICALIZED_REGISTER_ASSERTIONS
        if rel == relpath
    ]
    if not rows:
        return []
    pinned = collections.Counter(
        _fingerprint_digest(fp) for fp in _assertion_fingerprints(pinned_src))
    live = collections.Counter(
        _fingerprint_digest(fp) for fp in _assertion_fingerprints(live_src))
    required_sources = collections.Counter(source for source, _target in rows)
    required_targets = collections.Counter(target for _source, target in rows)
    losses = []
    for digest, count in required_sources.items():
        if pinned[digest] < count:
            losses.append(f"missing registered source {digest}: {pinned[digest]} < {count}")
    for digest, count in required_targets.items():
        if live[digest] < count:
            losses.append(f"missing literal target {digest}: {live[digest]} < {count}")
    return losses


def _registered_named_occurrences(relpath, pinned_src: str, live_src: str):
    """The lawful named transitions for this exact file and exact delta.

    A registry row is inert unless both endpoint declarations and their values
    match exactly, the successor is genuinely new, the predecessor is retained,
    and the two names have the same candidate role and category. Those checks
    validate the row; only its file plus pinned-assertion digest authorizes use.
    """
    out = {}
    if not relpath:
        return out
    pinned = _module_anchor_constants(pinned_src)
    live = _module_anchor_constants(live_src)
    for (rel, digest, old_name, old_value, new_name, new_value,
         category) in NAMED_ANCHOR_REANCHORS:
        if rel != relpath:
            continue
        if old_name == new_name or _anchor_role(old_name) != _anchor_role(new_name):
            continue
        if (_anchor_value_category(old_value) != category
                or _anchor_value_category(new_value) != category):
            continue
        if pinned.get(old_name) != (category, old_value):
            continue
        if new_name in pinned:                 # the successor must be introduced
            continue
        if live.get(old_name) != (category, old_value):
            continue                           # historical predecessor retained
        if live.get(new_name) != (category, new_value):
            continue
        out.setdefault(digest, []).append(
            (old_name, old_value, new_name, new_value, category))
    return out


def _rename_in_fingerprint(fingerprint: str, old_name: str, new_name: str) -> str:
    """Rename exactly one identifier spelling inside an assertion fingerprint."""
    old = f"Name(id={old_name!r}, ctx=Load())"
    new = f"Name(id={new_name!r}, ctx=Load())"
    return fingerprint.replace(old, new)


def _lost_assertions(pinned_src: str, live_src: str, relpath=None) -> list[str]:
    """Fingerprints asserted when pinned that are no longer asserted now.

    FOUR STAGES, in this order:

    1. **Verbatim.** An assertion still present unchanged is preserved. Nothing
       about it is abstracted, so a negative pin that legitimately kept its own
       literal matches its own twin and never reaches a later stage.
    2. **Registered named-anchor OCCURRENCE.** A still-unmatched assertion is
       looked up by ``(relpath, its own fingerprint digest)``. Its exact declared
       predecessor name/value may become only the registered successor name/value.
    3. **Registered literal OCCURRENCE.** A still-unmatched pinned assertion is
       looked up by ``(relpath, its own fingerprint digest)``. Only if THIS EXACT
       ASSERTION is registered may its predecessor literal be rewritten to the
       registered successor -- and then the result must appear verbatim among the
       live assertions. Each registration is consumed AT MOST ONCE.
    4. **Registered historicalization.** Only a specifically registered current
       positive occurrence may become one exact literal-bound negative target.
       The live predicate never executes through a mutable Python name. This is a
       finite, one-time conversion; it does not create a moving value map.

    Stages 2 and 3 answer reviews 5094619011 and 5093500583 respectively. The
    former global named-slot mechanism normalized every same-role name and every
    raw literal equal to one of their values. One lawful move could therefore
    hide a distinct negative-pin or literal rewrite. Named anchors now use the
    same file/assertion identity and single-use rule as bare literals, while raw
    literal values never enter a substitution map at all.

    The former literal mechanism mapped registered VALUES through a substitution map,
    which rewrote every assertion containing them: one lawful WS-0014 date
    transition therefore laundered an unrelated ``freeze["cutoff"]`` assertion
    using the same pair. A value is not an identity. An assertion is -- so the
    unrelated occurrence now has a different fingerprint, matches no
    registration, stays verbatim, and is reported.
    """
    pinned_fingerprints = _assertion_fingerprints(pinned_src)
    live_fingerprints = collections.Counter(_assertion_fingerprints(live_src))
    named_registered = _registered_named_occurrences(relpath, pinned_src, live_src)
    bare_registered = _registered_occurrences(relpath)
    historical_remaining = _historicalized_occurrences(relpath)
    # Each registration is spent once. Copying the lists makes that explicit and
    # keeps the module-level registry immutable.
    named_remaining = {d: list(v) for d, v in named_registered.items()}
    bare_remaining = {d: list(v) for d, v in bare_registered.items()}

    def consume_historical(candidate: str) -> bool:
        digest = _fingerprint_digest(candidate)
        targets = historical_remaining.get(digest) or []
        # A historicalized positive is closed, not optional. Keeping the exact
        # literal-bound negative while restoring the former positive would make
        # both predicates part of the live suite and could let a runtime name
        # rewrite choose which value the positive actually enforces.
        if live_fingerprints.get(candidate, 0) > 0:
            return False
        for i, target_digest in enumerate(targets):
            for live in live_fingerprints:
                if (_fingerprint_digest(live) == target_digest
                        and live_fingerprints[live] > 0):
                    targets.pop(i)
                    live_fingerprints[live] -= 1
                    return True
        return False

    # STAGE 1 -- exact match, and it is deliberately FIRST. An assertion that is
    # present unchanged is explained by itself, never by a re-anchor or a
    # registration, so nothing downstream can be spent on it.
    #
    lost, deferred = [], []
    for strict in pinned_fingerprints:
        # A registered one-time historicalization closes the old positive
        # endpoint. Its verbatim return is not preservation; only the exact
        # literal-bound negative target is now lawful.
        if _fingerprint_digest(strict) in historical_remaining:
            if not consume_historical(strict):
                deferred.append(strict)
        elif live_fingerprints[strict] > 0:
            live_fingerprints[strict] -= 1
        else:
            deferred.append(strict)

    # STAGE 2 -- exact registered named occurrence. A role can validate endpoint
    # compatibility, but it never supplies identity and never creates a map.
    still = []
    for strict in deferred:
        entries = named_remaining.get(_fingerprint_digest(strict)) or []
        matched = False
        for i, (old_name, _old_value, new_name, _new_value, _cat) in enumerate(entries):
            expected = _rename_in_fingerprint(strict, old_name, new_name)
            if expected == strict:
                continue
            if consume_historical(expected):
                entries.pop(i)
                matched = True
                break
            # Once an occurrence has a registered literal-bound historical
            # target, restoring its named positive form is a weakening, never a
            # second lawful endpoint.
            if (_fingerprint_digest(expected) not in historical_remaining
                    and live_fingerprints.get(expected, 0) > 0):
                live_fingerprints[expected] -= 1
                entries.pop(i)
                matched = True
                break
        if not matched:
            still.append(strict)

    # STAGE 3 -- exact registered bare-literal occurrence.
    for strict in still:
        entries = bare_remaining.get(_fingerprint_digest(strict)) or []
        matched = False
        for i, (old, new, cat) in enumerate(entries):
            # The registry's own claim about these values must still hold, so a
            # stale entry cannot outlive a change in what they are.
            if _anchor_category(old) != cat or _anchor_category(new) != cat:
                continue
            expected = strict.replace(f"Constant(value={old!r})",
                                      f"Constant(value={new!r})")
            if expected == strict:
                # Defensive only, and UNREACHABLE by construction: the digest is
                # the fingerprint of this exact assertion, so an entry keyed on it
                # necessarily carries `old`. Kept because the invariant is a
                # property of the identity scheme, not of this loop, and a future
                # change to the identity scheme would make it load-bearing again.
                continue
            if consume_historical(expected):
                entries.pop(i)
                matched = True
                break
            if (_fingerprint_digest(expected) not in historical_remaining
                    and live_fingerprints.get(expected, 0) > 0):
                live_fingerprints[expected] -= 1
                entries.pop(i)             # CONSUMED -- one registration, one use
                matched = True
                break
        if not matched and consume_historical(strict):
            matched = True
        if not matched:
            lost.append(strict)
    return sorted(lost)


#: DIRECT PROTECTED PREDICATES (PHQ-2026-07, second correction).
#:
#: Independent review's prescription for this defect class offered two mechanisms:
#: direct assertions for the required protected predicates, OR a semantic assertion
#: inventory admitting only occurrence-registered anchor substitutions. Both are used
#: here, and the
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
#: names, which the exact fingerprints deliberately preserve.
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

    Membership requires both the exact semantic fingerprint and the protected
    source text. A different operator, attribute, call structure, name, or literal
    does not count as the required predicate.
    """
    live = _assertion_inventory(live_src)
    missing = []
    for text in PROTECTED_PREDICATES[relpath]:
        want = _assertion_inventory(textwrap.dedent(text))
        assert want, f"a protected predicate must itself parse to an assertion: {text}"
        # TWO independent conditions, because each closes the other's blind spot.
        #
        # The exact semantic form catches a structural weakening -- a different operator,
        # attribute, call shape or arity -- including the equal-shape ``startswith`` /
        # ``endswith`` swap independent review named.
        #
        # Verbatim presence catches what abstraction deliberately cannot: two protected
        # predicates in one suite may have the SAME required structure when they differ only
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
        assert WS0014["active_branch"] == CURRENT_WS0014_BINDING["active_branch"]
        assert WS0014["active_pr"] == CURRENT_WS0014_BINDING["active_pr"]
        assert (WS0014["last_verified_main_sha"]
                == CURRENT_WS0014_BINDING["last_verified_main_sha"])
        assert (str(WS0014["last_verified_date"])
                == CURRENT_WS0014_BINDING["last_verified_date"])
        assert _ws0014_binding_errors(WS0014) == set()
        assert WS0014["active_pr"] != THIS_PULL_REQUEST
        assert WS0014["last_verified_main_sha"] != BOUND_MERGE_SHA

    @pytest.mark.parametrize(
        "field,wrong_value",
        (
            ("active_branch", "claude/xasset-0061-authorization-jux8p9"),
            ("active_pr", THIS_PULL_REQUEST),
            ("last_verified_main_sha", BOUND_MERGE_SHA),
            ("last_verified_date", "2026-08-28"),
        ),
    )
    def test_each_wrong_live_binding_field_fails_closed(self, field, wrong_value):
        """Each stale field is reported even when the other three are exact."""
        mutant = dict(WS0014)
        mutant[field] = wrong_value
        assert _ws0014_binding_errors(mutant) == {field}

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
        property while the total is unchanged. What is enforced now is the exact
        SEMANTIC INVENTORY plus occurrence-specific transition registries -- every
        assertion this suite made when pinned must still
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
            at_merge_src = _git("show", f"{THIS_UNIT_MERGE_SHA}:{rel}")
            if rel in PROTECTED_PREDICATES:
                # This filing lawfully re-anchored this suite's catalog-position,
                # cardinality or base-revision assertions under its own already-reviewed
                # G4 correction. A diff against the pre-correction baseline reports those
                # REPLACEMENTS as losses, so the invariant is stated positively instead.
                missing = _unasserted_predicates(rel, live_src)
            else:
                missing = _lost_assertions(at_merge_src, live_src, rel)
            missing.extend(
                _historicalized_registration_losses(at_merge_src, live_src, rel))
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
                missing = _lost_assertions(base, live, rel)
            at_merge = _git("show", f"{THIS_UNIT_MERGE_SHA}:{rel}")
            missing.extend(
                _historicalized_registration_losses(at_merge, live, rel))
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
        another decision's ``.md`` file passes it. The semantic inventory must
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
        # The semantic inventory must catch it.
        assert _lost_assertions(src, weakened), \
            "equal-shape predicate swap slipped through"

    def test_a_lawful_anchor_substitution_is_not_reported_as_a_loss(self):
        """The complement, and the reason an exact fingerprint inventory was rejected.

        A predecessor lawfully re-anchored ``== XASSET0060_MAIN_SHA`` to
        ``== XASSET0061_MAIN_SHA`` and ADDED two assertions. An identity-based rule
        calls that a loss; its two exact occurrence registrations permit only the
        named current-anchor transitions, while the separate bare registry permits
        only its exact date occurrence.
        """
        rel = "test_level1_stage1_activation_authorization.py"
        base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
        live = (ROOT / rel).read_text(encoding="utf-8")
        assert base != live, "this proof needs a genuinely re-anchored predecessor"
        assert not _lost_assertions(base, live, rel), \
            "a lawful anchor substitution was reported as a weakening"
        # ...and the same comparison with NO file identity authorizes nothing,
        # because a literal re-anchor is registered per OCCURRENCE, not per value.
        assert _lost_assertions(base, live), (
            "an unidentified comparison still authorized a literal substitution")

    def test_the_operative_parts_of_an_assertion_are_not_abstracted(self):
        """Every name, value and operative expression is exact by default.

        Rewritten again for review 5094619011. The general inventory performs no
        normalization at all. Only an explicit file/assertion registry entry may
        explain a moving anchor later in :func:`_lost_assertions`.
        """
        def one(expr):
            return _assertion_inventory(f"def f():\n    assert {expr}\n")

        # NOT abstracted WITHOUT a delta -- not even a perfectly anchor-shaped
        # value. This is the corrected contract, stated first because it is the
        # one the review required.
        assert one('v == "413e033ac33741829168762ab24d73327c047d4b"') != \
               one('v == "3db918530b10ffc1423ba0b749b086e349a4901d"')   # SHA
        assert one('d == "2026-08-28"') != one('d == "2026-09-02"')      # date
        assert one('i == "XASSET-0060"') != one('i == "XASSET-0061"')    # decision id
        assert one('b == "claude/one"') != one('b == "claude/two"')      # branch

        # A DIGITS-ONLY identifier is a NUMBER, never a SHA. Review 5092359752
        # showed the opposite ordering classifying the review id 4976985695 as a
        # SHA, which made it interchangeable with a real merge SHA.
        assert _anchor_category("4976985695") == "NUMBER"
        assert _anchor_category("637eaa30302f5a71f84ab1d215ecbd32c01399b5") == "SHA"
        assert one('"4976985695" in d') != \
               one('"637eaa30302f5a71f84ab1d215ecbd32c01399b5" in d')

        # NOT abstracted by typography, role, or category alone.
        assert one("v == SHA_ALPHA") != one("v == SHA_BETA")
        assert one('x.startswith(f"{DECISION_ID}-")') != one('x.startswith(f"{OTHER}-")')

        # NOT abstracted -- operative expected TEXT is not an anchor.
        assert one('"Merging it arms nothing" in section') != one('"" in section')
        assert one('"Merging it arms nothing" in section') != \
               one('"Merging it arms something" in section')
        assert one('x.startswith("aaa")') != one('x.startswith("bbb")')

        # NOT abstracted -- operative meaning
        assert one('x.startswith("a")') != one('x.endswith("a")')
        assert one("n >= 441") != one("n >= 440")
        assert one("n >= 441") != one("n > 441")
        assert one('x.startswith("a")') != one("x")

        # An f-string is WALKED, not collapsed, so its prose parts stay operative.
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

    def test_only_contextually_lawful_anchor_shapes_are_candidates(self):
        """Pin the endpoint classifier itself, both directions.

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
        assert not _lost_assertions(at_merge, src, rel), "the live suite must be clean"
        assert _lost_assertions(at_merge, mutated, rel), (
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

        The delta below adds a new SHA constant, but no occurrence is registered.
        Candidate-role or category evidence cannot authorize this assertion, and
        cannot leak into any other category.
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

    def test_a_same_category_reanchor_requires_a_registered_occurrence(self):
        """A plausible role/category pair is not authority on its own.

        The synthetic delta has all the old global mechanism's candidate signals,
        but no file/fingerprint registry row. It must therefore fail closed.
        Positive controls for all eleven lawful corpus occurrences appear below.
        """
        pinned = ('OLD_SHA = "301e79334876a4bda6e7b89a6156b34e8d38a605"\n'
                  "def f():\n    assert ws['sha'] == OLD_SHA\n")
        live = ('OLD_SHA = "301e79334876a4bda6e7b89a6156b34e8d38a605"\n'
                'NEW_SHA = "413e033ac33741829168762ab24d73327c047d4b"\n'
                "def f():\n    assert ws['sha'] == NEW_SHA\n")
        assert _lost_assertions(pinned, live), (
            "a same-category pair was accepted without an occurrence registration")

    def test_the_real_corpus_cross_domain_id_for_sha_swap_is_caught(self):
        """REQUIRED NEGATIVE CONTROL (PHQ-2026-07, review 5092359752).

        The exact real-corpus probe independent review demonstrated, on a suite
        that is PINNED but deliberately not in ``PROTECTED_PREDICATES``:

            assert "4976985695" in description
            assert "637eaa30302f5a71f84ab1d215ecbd32c01399b5" in description

        The substituted value is an unrelated merge SHA ALREADY PRESENT in the
        same description, so the mutated assertion evaluates true and the suite
        still passes -- while the required independent-review-id check is gone.

        Two separate defects let this through and both are pinned here:

        * the SHA pattern preceded NUMBER and accepted digits-only strings, so
          the review id ``4976985695`` was categorized as a SHA;
        * every recognized literal was normalized unconditionally, so two values
          the delta never re-anchored were interchangeable anyway.
        """
        rel = "test_level1_stage1_post_correction_rebinding_authorization.py"
        assert rel in PINNED_TEST_HASHES
        assert rel not in PROTECTED_PREDICATES, (
            "this probe proves the GENERAL mechanism, so its target must not be "
            "covered by the direct-protection list")
        src = (ROOT / rel).read_text(encoding="utf-8")
        strong = 'assert "4976985695" in description'
        swapped = 'assert "637eaa30302f5a71f84ab1d215ecbd32c01399b5" in description'
        assert strong in src, "the probe's own target has moved"
        # The mutated assertion PASSES: its value is already in the same text.
        assert "637eaa30302f5a71f84ab1d215ecbd32c01399b5" in src
        # Category separation is the first half of the fix.
        assert _anchor_category("4976985695") == "NUMBER"
        assert _anchor_category("637eaa30302f5a71f84ab1d215ecbd32c01399b5") == "SHA"
        mutated = src.replace(strong, swapped)
        assert mutated != src
        assert not _lost_assertions(src, src), "the live suite must be clean"
        assert _lost_assertions(src, mutated), (
            "the cross-domain id-for-SHA substitution was NOT caught")

    def test_a_literal_already_present_is_never_an_authorized_substitution(self):
        """The general property behind that probe, stated directly.

        A delta may re-anchor onto a value it INTRODUCED. It may never reach for
        a value that was already sitting in the file -- that introduces no
        predecessor->successor evidence at all, and is the shape every reviewed
        literal bypass has taken.
        """
        pinned = ('def f():\n'
                  '    assert "4976985695" in d\n'
                  '    assert "637eaa30302f5a71f84ab1d215ecbd32c01399b5" in d\n')
        # The swap reuses a value already present; nothing new is introduced.
        live = ('def f():\n'
                '    assert "637eaa30302f5a71f84ab1d215ecbd32c01399b5" in d\n'
                '    assert "637eaa30302f5a71f84ab1d215ecbd32c01399b5" in d\n')
        assert _registered_occurrences(None) == {}, (
            "a comparison without file identity unexpectedly had a literal registry")
        assert _lost_assertions(pinned, live), "the reused-value swap was not caught"

    def test_an_in_play_category_still_forbids_reusing_an_existing_value(self):
        """A category is never "in play" at all: only an ENUMERATED PAIR is.

        RE-ANCHORED AGAIN (PHQ-2026-07, review 5093500583). Written first against
        a category-wide rule, then against a value-pair registry. Both are gone:
        a literal substitution now requires a REGISTERED OCCURRENCE -- an exact
        file plus an exact assertion fingerprint -- so literals no longer travel
        through the value maps at all. The assertion below therefore moved off
        `live_values` (which no longer carries literals for anyone, making it a
        vacuous check) and onto the occurrence table, which is what actually
        decides. Strictly stronger: it now proves the synthetic assertion is
        registered NOWHERE, not merely that one map is empty.
        """
        old_v, kept_v, added_v = "a" * 40, "b" * 40, "c" * 40
        for v in (old_v, kept_v, added_v):
            assert _anchor_category(v) == "SHA", v
        pinned = (f'def f():\n    assert "{old_v}" in d\n'
                  f'    assert "{kept_v}" in d\n')
        # A real constant IS introduced, AND the required `old_v` assertion is
        # quietly replaced by a value already present.
        live = (f'NEW_SHA = "{added_v}"\n'
                f'def f():\n    assert "{kept_v}" in d\n'
                f'    assert "{kept_v}" in d\n    assert NEW_SHA in d\n')
        registered_values = {v for _r, _d, o, n, _c in BARE_LITERAL_REANCHORS
                             for v in (o, n)}
        assert added_v not in registered_values, "this probe needs an UNregistered value"
        # No file identity, and no registered occurrence for these assertions
        # under ANY file identity -- so no substitution is authorized.
        assert _registered_occurrences(None) == {}
        for rel in sorted(PINNED_TEST_HASHES):
            for digest in _registered_occurrences(rel):
                for st in _assertion_fingerprints(pinned):
                    assert _fingerprint_digest(st) != digest, (
                        "this probe's own assertions must be UNregistered")
        assert _lost_assertions(pinned, live), (
            "a reused pre-existing value was accepted inside an in-play category")

    def test_a_registered_occurrence_does_not_launder_the_same_pair_elsewhere(self):
        """REQUIRED NEGATIVE CONTROL A (PHQ-2026-07, review 5093500583).

        The defect this correction exists to close. A lawful, REGISTERED WS-0014
        date transition happens in a file, and a SECOND, unrelated assertion in
        the same file uses the very same predecessor/successor pair. Under the
        superseded value-pair registry both were rewritten by one substitution
        map, so the unrelated assertion vanished with `_lost_assertions()`
        reporting nothing.

        The registered occurrence still passes. The unrelated one is reported,
        because a VALUE is not an identity -- an ASSERTION is, and this one is
        registered nowhere.
        """
        rel = "test_level1_stage1_pr337_actor_evidence_correction_authorization.py"
        base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
        live = (ROOT / rel).read_text(encoding="utf-8")
        assert not _lost_assertions(base, live, rel), "the live suite must be clean"
        old, new = "2026-08-27", "2026-08-28"
        # An unrelated assertion using the SAME pair, present in both versions and
        # weakened only on the live side.
        extra_pinned = f'\n\ndef _probe(freeze):\n    assert freeze["cutoff"] == "{old}"\n'
        extra_live = f'\n\ndef _probe(freeze):\n    assert freeze["cutoff"] == "{new}"\n'
        lost = _lost_assertions(base + extra_pinned, live + extra_live, rel)
        assert lost, "an unrelated occurrence of a registered pair was laundered"
        assert any("cutoff" in fp for fp in lost), (
            "the reported loss must be the unrelated assertion itself")
        # ...and exactly one loss: the registered occurrence still passes.
        assert len(lost) == 1, lost

    def test_the_review_construction_authorizes_nothing_unregistered(self):
        """The review's literal reproduction, which registers NO occurrence.

        Neither assertion here is a registered occurrence -- their fingerprints
        appear in no entry -- so both are compared verbatim and both are
        reported. Fail-closed, and the unrelated `cutoff` weakening is among
        them, which is what the finding required.
        """
        old, new = "2026-08-27", "2026-08-28"
        pinned = (f'def f(register, freeze):\n'
                  f'    assert register["last_verified_date"] == "{old}"\n'
                  f'    assert freeze["cutoff"] == "{old}"\n')
        live = (f'def f(register, freeze):\n'
                f'    assert register["last_verified_date"] == "{new}"\n'
                f'    assert freeze["cutoff"] == "{new}"\n')
        for relpath in (None,
                        "test_level1_stage1_pr337_actor_evidence_correction_authorization.py"):
            lost = _lost_assertions(pinned, live, relpath)
            assert lost, f"nothing was reported for relpath={relpath!r}"
            assert any("cutoff" in fp for fp in lost), (
                f"the unrelated weakening was not reported for relpath={relpath!r}")

    # The registered occurrence used by the two probes below is REAL: this exact
    # assertion, at this exact relpath, is entry 0 of the registry, so neither
    # probe can pass vacuously against a fingerprint the corpus does not contain.
    _REG_REL = "test_level1_stage1_activation_authorization.py"
    _REG_LINE = 'assert str(workstream["last_verified_date"]).startswith("{v}")'
    _REG_HIST_LINE = 'assert not str(workstream["last_verified_date"]).startswith("{v}")'

    def test_a_registered_occurrence_cannot_be_spent_by_reusing_a_present_value(self):
        """RETAINED PROPERTY (carried forward from the superseded value-pair guard).

        The superseded mechanism needed an explicit "the successor must be
        INTRODUCED by the delta" condition, because a value-pair licence could
        otherwise be spent by a live side that merely REACHED FOR a successor
        already sitting in the pinned file -- the shape every reviewed literal
        bypass has taken. Occurrence binding must not lose that property.

        Here the successor is already asserted on the PINNED side at an unrelated
        site. The registered occurrence still has to be genuinely realised at its
        own fingerprint; the already-present value buys nothing, and the
        unregistered site that moves is reported.
        """
        rel, digest, old, new, _cat = BARE_LITERAL_REANCHORS[0]
        assert rel == self._REG_REL
        reg_old = "    " + self._REG_LINE.format(v=old) + "\n"
        reg_new = "    " + self._REG_HIST_LINE.format(v=new) + "\n"
        # `new` is ALREADY present on the pinned side, at a DIFFERENT, unregistered site.
        other_old = f'    assert freeze["cutoff"] == "{new}"\n'
        other_moved = f'    assert freeze["cutoff"] == "2026-08-26"\n'
        pinned = "def f():\n" + reg_old + other_old
        live = "def f():\n" + reg_new + other_moved
        lost = _lost_assertions(pinned, live, rel)
        assert lost, "an unregistered site was laundered by a present successor value"
        assert any("cutoff" in fp for fp in lost), (
            "the reported loss must be the unregistered site, not the lawful one")
        assert not any("last_verified_date" in fp for fp in lost), (
            "the genuinely-realised registered occurrence must not be reported")

    def test_the_verbatim_stage_prevents_a_false_loss_on_a_partial_reanchor(self):
        """RETAINED PROPERTY. The verbatim-first stage is load-bearing PERMISSIVELY.

        When a registered predecessor VALUE also appears at an unregistered site
        that does NOT move, that site must match itself verbatim. Without the
        verbatim stage it would compete for the registered occurrence's match and
        be reported as a loss that never happened -- a false alarm, which erodes
        the guard by training its readers to ignore it.
        """
        rel, _digest, old, new, _cat = BARE_LITERAL_REANCHORS[0]
        reg_old = "    " + self._REG_LINE.format(v=old) + "\n"
        reg_new = "    " + self._REG_HIST_LINE.format(v=new) + "\n"
        unmoved = f'    assert freeze["cutoff"] == "{old}"\n'
        pinned = "def f():\n" + reg_old + unmoved
        live = "def f():\n" + reg_new + unmoved
        assert not _lost_assertions(pinned, live, rel), (
            "an unmoved occurrence of a registered predecessor was reported lost")
        # ...and that unmoved site is still governed: moving it anywhere is reported.
        bad = "def f():\n" + reg_new + '    assert freeze["cutoff"] == "2026-08-26"\n'
        lost = _lost_assertions(pinned, bad, rel)
        assert lost and any("cutoff" in fp for fp in lost), (
            "the unregistered site became unguarded once the lawful one moved")

    def test_one_live_assertion_cannot_satisfy_two_pinned_copies(self, monkeypatch):
        """DIRECT GUARD TEST, found by this correction's own mutation proof.

        Two mechanisms enforce single use and they are not redundant. Popping the
        entry stops ONE registration being spent twice. Decrementing the live
        counter stops one LIVE assertion answering for two pinned ones -- which is
        reachable the moment a digest carries more than one registration.

        The registry as committed carries no duplicate digest (pinned separately),
        so the property is exercised here against a deliberately duplicated
        registration. Without the live-side decrement a single live assertion
        satisfies both pinned copies and a genuine loss disappears.
        """
        rel, digest, old, new, cat = BARE_LITERAL_REANCHORS[0]
        monkeypatch.setattr(
            sys.modules[__name__], "BARE_LITERAL_REANCHORS",
            BARE_LITERAL_REANCHORS + ((rel, digest, old, new, cat),), raising=True)
        line_old = "    " + self._REG_LINE.format(v=old) + "\n"
        line_new = "    " + self._REG_HIST_LINE.format(v=new) + "\n"
        # The registered assertion is made TWICE on the pinned side...
        pinned = "def f():\n" + line_old + line_old
        # ...and only ONCE on the live side. One of the two is genuinely gone.
        live = "def f():\n" + line_new
        lost = _lost_assertions(pinned, live, rel)
        assert lost, "one live assertion answered for two pinned copies"
        assert len(lost) == 1, ("exactly one of the two pinned copies is lost", lost)

    def test_a_stale_registration_stops_firing_when_its_category_claim_breaks(
            self, monkeypatch):
        """DIRECT GUARD TEST, found by this correction's own mutation proof.

        Each entry states the category both its values must really be. The
        committed entries all satisfy that (pinned separately), which is exactly
        why removing the RUNTIME check changed nothing observable until now: the
        data invariant was proved, the guard that consumes it was not.

        A registration whose category claim no longer holds is STALE. It must
        stop firing rather than keep substituting on a claim the anchor rules no
        longer support -- the fail-closed direction, and the reason a future
        change to DATE or BRANCH recognition cannot silently widen this registry.
        """
        rel, digest, old, new, _cat = BARE_LITERAL_REANCHORS[0]
        line_old = "    " + self._REG_LINE.format(v=old) + "\n"
        line_new = "    " + self._REG_HIST_LINE.format(v=new) + "\n"
        pinned, live = "def f():\n" + line_old, "def f():\n" + line_new
        # Truthful registration: the lawful transition is explained.
        assert not _lost_assertions(pinned, live, rel)
        # Same occurrence, same values, but the entry now claims a category the
        # values are not. Nothing else changes.
        monkeypatch.setattr(
            sys.modules[__name__], "BARE_LITERAL_REANCHORS",
            ((rel, digest, old, new, "BRANCH"),), raising=True)
        assert _anchor_category(old) != "BRANCH", "this probe needs a FALSE claim"
        assert _lost_assertions(pinned, live, rel), (
            "a registration kept firing on a category claim that no longer holds")

    def test_both_date_layers_reject_trailing_text_independently(self):
        """DIRECT GUARD TEST, found by this correction's own mutation proof.

        Date recognition is deliberately two layers: the category pattern is
        end-anchored, and ``_is_valid_date_or_timestamp()`` re-anchors and then
        range-checks. Either layer alone rejects date-prefixed prose, which is
        why removing one alone changed nothing observable -- defence in depth
        working, but also each layer able to rot unnoticed behind the other.

        Both are pinned here, individually, so neither can be quietly dropped.
        """
        prose = "2026-08-27 Merging it arms nothing"
        # Layer 2, on its own terms.
        assert not _is_valid_date_or_timestamp(prose), (
            "the component validator accepted trailing text")
        assert not _is_valid_date_or_timestamp("2026-08-27T12:30:00Z extra")
        assert _is_valid_date_or_timestamp("2026-08-27")
        # Layer 1, on its own terms.
        date_pattern = dict(_ANCHOR_CATEGORIES)["DATE"]
        assert not date_pattern.match(prose), (
            "the DATE category pattern is no longer anchored at the end")
        assert date_pattern.match("2026-08-27")
        # ...and the composition, which is what callers actually see.
        assert _anchor_category(prose) is None

    def test_the_general_inventory_never_normalizes_names_or_values(self):
        """Only a registry occurrence may explain a changed name or literal.

        This directly pins the premise of the correction: the general assertion
        inventory is exact. Adding a plausible successor declaration cannot make
        either an unregistered named assertion or a raw-literal assertion equal.
        """
        old, new = "a1" * 20, "b2" * 20
        pinned = (f'OLD_MAIN_SHA = "{old}"\n'
                  'def f(current, history):\n'
                  '    assert current == OLD_MAIN_SHA\n'
                  f'    assert history["required"] == "{old}"\n')
        live = (f'OLD_MAIN_SHA = "{old}"\n'
                f'NEW_MAIN_SHA = "{new}"\n'
                'def f(current, history):\n'
                '    assert current == NEW_MAIN_SHA\n'
                f'    assert history["required"] == "{new}"\n')
        assert _assertion_inventory(pinned) != _assertion_inventory(live)
        lost = _lost_assertions(pinned, live)
        assert len(lost) == 2, lost

    def test_date_prefixed_operative_prose_is_not_an_anchor(self):
        """REQUIRED NEGATIVE CONTROL B (PHQ-2026-07, review 5093063766).

        Retained verbatim from the previous correction and re-run against the
        occurrence-bound mechanism. ``DATE`` once matched a PREFIX, so any
        operative expectation that happened to begin with a date was treated as
        an anchor and rewriting its meaning was invisible. A date is now the
        whole string or it is not a date, and prose can never reach the registry.
        """
        p_text = "2026-08-27 Merging it arms nothing"
        l_text = "2026-08-28 Merging it arms Stage 1"
        assert _anchor_category(p_text) is None, "prose is not an anchor"
        assert _anchor_category(l_text) is None, "prose is not an anchor"
        pinned = f'def f():\n    assert "{p_text}" in section\n'
        live = f'def f():\n    assert "{l_text}" in section\n'
        # Reported with AND without a file identity: prose is unreachable either way.
        for relpath in (None,
                        "test_level1_stage1_readiness_verification_authorization.py"):
            assert _lost_assertions(pinned, live, relpath), (
                f"a date-prefixed operative expectation was rewritten unseen "
                f"(relpath={relpath!r})")

    @pytest.mark.parametrize("text,expected", [
        # Complete, real, in-domain forms stay recognised.
        ("2026-08-27", "DATE"),
        ("2026-08-27T12:30:00Z", "DATE"),
        ("2026-08-27 12:30", "DATE"),
        ("2026-08-27T12:30:00+01:00", "DATE"),
        ("2026-08-27T12:30:00-05:00", "DATE"),
        ("2026-08-27T23:59:59.123Z", "DATE"),
        ("2026-08-27T00:00:00+0000", "DATE"),
        # Not a whole string, or not a real calendar date.
        ("2026-08-27 Merging it arms nothing", None),
        ("2026-08-27-extra", None),
        ("2026-13-45", None),
        ("2026-02-30", None),
        ("2026-08-27 the register says otherwise", None),
        # REQUIRED (review 5093500583): the clock and offset DOMAINS, not merely
        # the leading ten characters. Each of these is well-SHAPED and was
        # previously accepted as an anchor because only ``text[:10]`` was checked.
        ("2026-08-27T99:99:99Z", None),
        ("2026-08-27T24:00:00Z", None),
        ("2026-08-27T23:60:00Z", None),
        ("2026-08-27T23:59:60Z", None),
        ("2026-08-27T12:30:00+24:00", None),
        ("2026-08-27T12:30:00+00:60", None),
        ("2026-08-27T12:30:00-99:99", None),
        ("2026-08-27T99:00", None),
        ("2026-08-27 25:00", None),
        ("2026-08-27T12:30:00+1", None),
    ])
    def test_date_recognition_accepts_only_valid_dates_and_timestamps(self, text, expected):
        """Named coverage for the DATE domain, superseding the prefix-only check.

        Strictly stronger than the check it replaces: every case the previous
        parametrisation asserted is retained unchanged, and the hour, minute,
        second, fractional-second and UTC-offset domains -- none of which the
        superseded ``text[:10]`` validation could reach -- are added.
        """
        assert _anchor_category(text) == expected, text

    def test_the_named_registry_identifies_occurrences_not_roles_or_values(self):
        """Eleven corpus transitions are individually file/fingerprint bound."""
        assert len(NAMED_ANCHOR_REANCHORS) == 11
        by_names = collections.Counter(
            (old_name, new_name)
            for _r, _d, old_name, _ov, new_name, _nv, _c
            in NAMED_ANCHOR_REANCHORS)
        assert by_names[("XASSET0060_MAIN_SHA", "XASSET0061_MAIN_SHA")] == 8
        assert by_names[("XASSET0060_ACTIVE_PR", "XASSET0061_ACTIVE_PR")] == 3
        seen = set()
        for (rel, digest, old_name, old_value, new_name, new_value,
             category) in NAMED_ANCHOR_REANCHORS:
            assert rel in PINNED_TEST_HASHES, rel
            assert re.fullmatch(r"[0-9a-f]{64}", digest), digest
            assert _anchor_role(old_name) == _anchor_role(new_name)
            assert _anchor_value_category(old_value) == category
            assert _anchor_value_category(new_value) == category
            assert old_name != new_name and old_value != new_value
            assert (rel, digest) not in seen, f"{rel}/{digest[:12]} registered twice"
            seen.add((rel, digest))

    @pytest.mark.parametrize(
        "rel,digest,old_name,old_value,new_name,new_value,category",
        NAMED_ANCHOR_REANCHORS,
        ids=[f"{r.split('_')[-2]}-{c}"
             for r, _d, _on, _ov, _nn, _nv, c in NAMED_ANCHOR_REANCHORS])
    def test_every_named_occurrence_is_real_and_lawful(
            self, rel, digest, old_name, old_value, new_name, new_value, category):
        """POSITIVE CONTROLS: every explicit lawful named occurrence."""
        base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
        live = (ROOT / rel).read_text(encoding="utf-8")
        pinned_bindings = _anchor_name_bindings(base)
        live_bindings = _anchor_name_bindings(live)
        assert pinned_bindings.get(old_name) == [(category, old_value)]
        assert new_name not in pinned_bindings
        assert live_bindings.get(old_name) == [(category, old_value)]
        assert live_bindings.get(new_name) == [(category, new_value)]
        pinned_constants = _module_anchor_constants(base)
        live_constants = _module_anchor_constants(live)
        assert pinned_constants.get(old_name) == (category, old_value)
        assert new_name not in pinned_constants
        assert live_constants.get(old_name) == (category, old_value)
        assert live_constants.get(new_name) == (category, new_value)
        fingerprints = _assertion_fingerprints(base)
        matched = [fp for fp in fingerprints if _fingerprint_digest(fp) == digest]
        assert len(matched) == 1, (rel, digest, len(matched))
        expected = _rename_in_fingerprint(matched[0], old_name, new_name)
        assert expected != matched[0]
        # A subset of these formerly-current positive assertions has now been
        # converted, once, into an immutable negative pin.  Prove the exact
        # registered two-step chain rather than requiring the obsolete positive
        # endpoint to remain live forever.
        historical = _historicalized_occurrences(rel)
        targets = historical.get(_fingerprint_digest(expected)) or []
        if targets:
            candidates = [
                fp for fp in _assertion_fingerprints(live)
                if _fingerprint_digest(fp) in targets
            ]
            assert len(candidates) == 1, (rel, digest, candidates)
            expected = candidates[0]
        assert expected in _assertion_fingerprints(live)
        registered = _registered_named_occurrences(rel, base, live)
        assert (old_name, old_value, new_name, new_value, category) in registered[digest]
        assert not _lost_assertions(base, live, rel)

    def test_scope_shadow_cannot_supply_a_registered_endpoint_value(
            self, monkeypatch):
        """REQUIRED NEGATIVE (corrective review 5095693529).

        The assertion resolves the module-level successor to an UNAUTHORIZED
        value. An unrelated nested assignment then repeats the same NAME with the
        APPROVED registry value. The superseded flattened collector kept only the
        last value and certified the rewrite even though the executable assertion
        used the other declaration.

        The production collector rejects the ambiguous name. The final block also
        installs the old flattened behaviour as a non-equivalent mutant and proves
        that it restores the exact escape, making the uniqueness condition
        observably load-bearing rather than a documentary precaution.
        """
        old = "a1" * 20
        approved = "b2" * 20
        unauthorized = "c3" * 20
        pinned = (f'OLD_MAIN_SHA = "{old}"\n'
                  'def f(ws):\n'
                  '    assert ws["last_verified_main_sha"] == OLD_MAIN_SHA\n')
        live = (f'OLD_MAIN_SHA = "{old}"\n'
                f'NEW_MAIN_SHA = "{unauthorized}"\n'
                'def f(ws):\n'
                '    assert ws["last_verified_main_sha"] == NEW_MAIN_SHA\n'
                'def decoy():\n'
                f'    NEW_MAIN_SHA = "{approved}"\n')

        namespace = {}
        exec(live, namespace)
        namespace["f"]({"last_verified_main_sha": unauthorized})
        with pytest.raises(AssertionError):
            namespace["f"]({"last_verified_main_sha": approved})

        fingerprint = _assertion_fingerprints(pinned)[0]
        rel = "synthetic_scope_shadow.py"
        entry = ((rel, _fingerprint_digest(fingerprint),
                  "OLD_MAIN_SHA", old,
                  "NEW_MAIN_SHA", approved, "SHA"),)
        monkeypatch.setattr(
            sys.modules[__name__], "NAMED_ANCHOR_REANCHORS", entry)

        assert _anchor_name_bindings(live)["NEW_MAIN_SHA"] == [
            ("SHA", unauthorized), ("SHA", approved)]
        assert "NEW_MAIN_SHA" not in _module_anchor_constants(live)
        assert not _registered_named_occurrences(rel, pinned, live)
        lost = _lost_assertions(pinned, live, rel)
        assert lost == [fingerprint]

        def flattened_mutant(source):
            return {
                name: binding
                for name, bindings in _anchor_name_bindings(source).items()
                for binding in bindings
                if _ANCHOR_NAME.match(name) and binding is not None
            }

        assert flattened_mutant(live)["NEW_MAIN_SHA"] == ("SHA", approved)
        monkeypatch.setattr(
            sys.modules[__name__], "_module_anchor_constants", flattened_mutant)
        assert _registered_named_occurrences(rel, pinned, live)
        assert not _lost_assertions(pinned, live, rel), (
            "the flattened mutant no longer reproduces the reviewed escape")

    def test_repeated_same_value_binding_is_still_ambiguous(self, monkeypatch):
        """Uniqueness is occurrence evidence, not value agreement."""
        old, new = "a1" * 20, "b2" * 20
        pinned = (f'OLD_MAIN_SHA = "{old}"\n'
                  'def f(ws):\n'
                  '    assert ws["last_verified_main_sha"] == OLD_MAIN_SHA\n')
        live = (f'OLD_MAIN_SHA = "{old}"\n'
                f'NEW_MAIN_SHA = "{new}"\n'
                'def f(ws):\n'
                '    assert ws["last_verified_main_sha"] == NEW_MAIN_SHA\n'
                'def decoy():\n'
                f'    NEW_MAIN_SHA = "{new}"\n')
        fingerprint = _assertion_fingerprints(pinned)[0]
        rel = "synthetic_same_value_shadow.py"
        monkeypatch.setattr(
            sys.modules[__name__], "NAMED_ANCHOR_REANCHORS",
            ((rel, _fingerprint_digest(fingerprint),
              "OLD_MAIN_SHA", old, "NEW_MAIN_SHA", new, "SHA"),))
        assert "NEW_MAIN_SHA" not in _module_anchor_constants(live)
        assert _lost_assertions(pinned, live, rel) == [fingerprint]

    def test_every_named_registration_is_exercised_by_the_corpus(self):
        """Removing any named row makes its own pinned assertion a loss."""
        saved = globals()["NAMED_ANCHOR_REANCHORS"]
        try:
            for entry in saved:
                rel, digest = entry[:2]
                base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
                live = (ROOT / rel).read_text(encoding="utf-8")
                globals()["NAMED_ANCHOR_REANCHORS"] = tuple(
                    candidate for candidate in saved if candidate != entry)
                lost = _lost_assertions(base, live, rel)
                assert any(_fingerprint_digest(fp) == digest for fp in lost), (
                    f"the named {rel}/{digest[:12]} registration is never needed")
        finally:
            globals()["NAMED_ANCHOR_REANCHORS"] = saved

    def test_a_named_registration_is_consumed_at_most_once(self):
        """One named registration cannot explain two identical pinned copies."""
        entry = NAMED_ANCHOR_REANCHORS[0]
        rel, _digest, old_name, _ov, new_name, _nv, _cat = entry
        base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
        live = (ROOT / rel).read_text(encoding="utf-8")
        old_line = next(
            line for line in base.splitlines()
            if "assert" in line and old_name in line and "!=" not in line)
        new_line = old_line.replace(old_name, new_name)
        lost = _lost_assertions(
            base + "\n" + old_line.strip() + "\n",
            live + "\n" + new_line.strip() + "\n", rel)
        # The added successor positive is itself forbidden once this occurrence
        # has been historicalized, so neither predecessor copy may be licensed.
        assert len(lost) == 2, lost
        assert all(old_name in fingerprint for fingerprint in lost)

    def test_the_registry_identifies_transitions_by_occurrence_not_by_value(self):
        """The registry's own shape is the guarantee, so it is pinned.

        Each entry names a FILE and an exact PINNED ASSERTION fingerprint digest,
        not merely a value pair. Six lawful corpus transitions are listed
        individually -- five date sites and one branch site -- never collapsed
        into value-pair licences.
        """
        assert BARE_LITERAL_REANCHORS, "the registry must not be empty"
        assert len(BARE_LITERAL_REANCHORS) == 6, (
            "the corpus has exactly six lawful bare-literal transitions")
        by_pair = collections.Counter(
            (old, new) for _r, _d, old, new, _c in BARE_LITERAL_REANCHORS)
        # The proof that identity is not the value pair: one pair legitimately
        # covers FIVE separate registered occurrences.
        assert by_pair[("2026-08-27", "2026-08-28")] == 5
        assert by_pair[("claude/xasset-0057-rebinding-gqtg9o",
                        "claude/xasset-0061-authorization-jux8p9")] == 1
        seen = set()
        for rel, digest, old, new, cat in BARE_LITERAL_REANCHORS:
            assert rel in PINNED_TEST_HASHES, rel
            assert re.fullmatch(r"[0-9a-f]{64}", digest), digest
            assert _anchor_category(old) == cat, (old, cat)
            assert _anchor_category(new) == cat, (new, cat)
            assert old != new
            # OCCURRENCE UNIQUENESS: no (file, assertion) is registered twice, so
            # one assertion can never carry two licences.
            assert (rel, digest) not in seen, f"{rel}/{digest[:12]} registered twice"
            seen.add((rel, digest))

    def test_historicalization_registry_is_finite_exact_and_real(self):
        """The one-time conversion is an occurrence list, not a value licence."""
        assert len(HISTORICALIZED_REGISTER_ASSERTIONS) == 33
        by_file = collections.defaultdict(list)
        for rel, source_digest, target_digest in HISTORICALIZED_REGISTER_ASSERTIONS:
            by_file[rel].append((source_digest, target_digest))
        protected_conversions = {
            "test_level1_stage1_formal_disposition_parser_correction_authorization.py",
            "test_level1_stage1_parser_contract_correction_authorization.py",
            "test_level1_stage1_post_merge_ci_recovery_reconciliation.py",
            "test_level1_stage1_post_parser_correction_operational_rebinding.py",
            "test_level1_stage1_verdict_boundary_governance.py",
        }
        assert set(by_file) & set(PROTECTED_PREDICATES) == protected_conversions
        for rel, rows in by_file.items():
            assert rel in PINNED_TEST_HASHES, rel
            base = _git("show", f"{THIS_UNIT_MERGE_SHA}:{rel}")
            live_src = (ROOT / rel).read_text(encoding="utf-8")
            base_fingerprints = _assertion_fingerprints(base)
            live_fingerprints = _assertion_fingerprints(live_src)
            base_counts = collections.Counter(
                _fingerprint_digest(fp) for fp in base_fingerprints)
            live_counts = collections.Counter(
                _fingerprint_digest(fp) for fp in live_fingerprints)
            required_sources = collections.Counter(source for source, _ in rows)
            required_targets = collections.Counter(target for _, target in rows)
            for digest, count in required_sources.items():
                assert re.fullmatch(r"[0-9a-f]{64}", digest), digest
                assert base_counts[digest] == count, (
                    rel, digest, base_counts[digest], count)
            for target_digest, count in required_targets.items():
                assert re.fullmatch(r"[0-9a-f]{64}", target_digest), target_digest
                assert live_counts[target_digest] == count, (
                    rel, target_digest, live_counts[target_digest], count)
                matching = [
                    fp for fp in live_fingerprints
                    if _fingerprint_digest(fp) == target_digest
                ]
                assert all(
                    "NotEq()" in fp or fp.startswith("UnaryOp(op=Not()")
                    for fp in matching)
                assert all("XASSET0061_" not in fp for fp in matching)
                assert all("SUCCESSOR_" not in fp for fp in matching)
            assert not _historicalized_registration_losses(base, live_src, rel)

    def test_every_historicalization_registration_is_load_bearing(self):
        """Removing any row's target exposes that exact occurrence as lost."""
        for index, (rel, _digest, target_digest) in enumerate(
                HISTORICALIZED_REGISTER_ASSERTIONS):
            base = _git("show", f"{THIS_UNIT_MERGE_SHA}:{rel}")
            live = (ROOT / rel).read_text(encoding="utf-8")
            tree = ast.parse(live)
            node = next(
                assertion for assertion in ast.walk(tree)
                if isinstance(assertion, ast.Assert)
                and _fingerprint_digest(ast.dump(assertion.test)) == target_digest
            )
            lines = live.splitlines(keepends=True)
            del lines[node.lineno - 1:node.end_lineno]
            losses = _historicalized_registration_losses(
                base, "".join(lines), rel)
            assert losses, (
                f"historicalization row {index} for {rel} is never needed")

    def test_removing_a_registered_protected_target_fails_closed(self):
        """Direct control for review 3920157771: protected conversions load-bear."""
        protected_rows = collections.defaultdict(list)
        for rel, _source, target in HISTORICALIZED_REGISTER_ASSERTIONS:
            if rel in PROTECTED_PREDICATES:
                protected_rows[rel].append(target)
        assert len(protected_rows) == 5
        for rel, targets in protected_rows.items():
            base = _git("show", f"{THIS_UNIT_MERGE_SHA}:{rel}")
            live = (ROOT / rel).read_text(encoding="utf-8")
            tree = ast.parse(live)
            target = targets[0]
            node = next(
                assertion for assertion in ast.walk(tree)
                if isinstance(assertion, ast.Assert)
                and _fingerprint_digest(ast.dump(assertion.test)) == target
            )
            lines = live.splitlines(keepends=True)
            del lines[node.lineno - 1:node.end_lineno]
            weakened = "".join(lines)
            losses = _historicalized_registration_losses(base, weakened, rel)
            assert losses, f"removing a protected target escaped in {rel}"

    def test_restoring_a_historical_positive_alongside_its_negative_fails_closed(
            self):
        """Direct control for review 3920270781: a closed positive stays closed."""
        rel = "test_level1_stage1_activation_authorization.py"
        base = _git("show", f"{THIS_UNIT_MERGE_SHA}:{rel}")
        live = (ROOT / rel).read_text(encoding="utf-8")
        source_digest = next(
            source for row_rel, source, _target
            in HISTORICALIZED_REGISTER_ASSERTIONS
            if row_rel == rel
        )
        node = next(
            assertion for assertion in ast.walk(ast.parse(base))
            if isinstance(assertion, ast.Assert)
            and _fingerprint_digest(ast.dump(assertion.test)) == source_digest
        )
        restored = ast.unparse(node)
        attacked = (
            live
            + '\nglobals()["XASSET0061_MAIN_SHA"] = "c3" * 20\n'
            + '\ndef restored_positive(workstream):\n'
            + f"    {restored}\n"
        )
        lost = _lost_assertions(base, attacked, rel)
        assert any(_fingerprint_digest(fp) == source_digest for fp in lost), lost

    def test_one_historicalization_registration_cannot_cover_two_occurrences(
            self, monkeypatch):
        """One registered positive occurrence may become one negative occurrence."""
        rel = "synthetic_historicalization.py"
        positive = 'def f(ws):\n    assert ws["active_pr"] == 362\n'
        negative = 'def f(ws):\n    assert ws["active_pr"] != 362\n'
        fingerprint = _assertion_fingerprints(positive)[0]
        target = _assertion_fingerprints(negative)[0]
        monkeypatch.setattr(
            sys.modules[__name__], "HISTORICALIZED_REGISTER_ASSERTIONS",
            ((rel, _fingerprint_digest(fingerprint),
              _fingerprint_digest(target)),))
        lost = _lost_assertions(positive + positive, negative, rel)
        assert len(lost) == 1, lost

    def test_unregistered_historicalization_fails_closed(self):
        positive = 'def f(ws):\n    assert ws["active_pr"] == 362\n'
        negative = 'def f(ws):\n    assert ws["active_pr"] != 362\n'
        assert _lost_assertions(positive, negative)
        assert _lost_assertions(positive, negative, "unregistered.py")

    @pytest.mark.parametrize(
        "attack",
        (
            'globals()["HISTORICAL_SHA"] = "c3" * 20',
            'namespace = globals()\nnamespace["HISTORICAL_SHA"] = "c3" * 20',
            'import sys\nsetattr(sys.modules[__name__], "HISTORICAL_SHA", "c3" * 20)',
            ('def rewrite(namespace):\n'
             '    namespace["HISTORICAL_SHA"] = "c3" * 20\n'
             'rewrite(globals())'),
            'exec(\'HISTORICAL_SHA = "c3" * 20\')',
        ),
        ids=("globals", "globals-alias", "module-setattr", "helper", "exec"),
    )
    def test_dynamic_name_writes_cannot_change_a_literal_bound_negative(
            self, attack):
        """The review's entire runtime-rebinding class is irrelevant to a literal."""
        import types

        approved = "b2" * 20
        source = (
            f'HISTORICAL_SHA = "{approved}"\n'
            'def check(ws):\n'
            f'    assert ws["last_verified_main_sha"] != "{approved}"\n'
            f'{attack}\n'
        )
        name = f"_g5_dynamic_attack_{abs(hash(attack))}"
        module = types.ModuleType(name)
        sys.modules[name] = module
        try:
            exec(source, module.__dict__)
            assert module.HISTORICAL_SHA == "c3" * 20
            module.check({"last_verified_main_sha": "c3" * 20})
            with pytest.raises(AssertionError):
                module.check({"last_verified_main_sha": approved})
        finally:
            sys.modules.pop(name, None)

    def test_dynamic_write_plus_named_positive_cannot_reenter_the_registry(self):
        """Exact review 5096789214: the former named endpoint is no longer accepted."""
        rel = "test_level1_stage1_activation_authorization.py"
        base = _git("show", f"{THIS_UNIT_MERGE_SHA}:{rel}")
        live = (ROOT / rel).read_text(encoding="utf-8")
        literal = (
            'assert workstream["last_verified_main_sha"] '
            '!= "413e033ac33741829168762ab24d73327c047d4b"'
        )
        named = (
            'assert workstream["last_verified_main_sha"] '
            '== XASSET0061_MAIN_SHA'
        )
        assert live.count(literal) == 1
        attacked = live.replace(literal, named, 1).replace(
            'XASSET0061_MAIN_SHA = "413e033ac33741829168762ab24d73327c047d4b"\n',
            'XASSET0061_MAIN_SHA = "413e033ac33741829168762ab24d73327c047d4b"\n'
            'globals()["XASSET0061_MAIN_SHA"] = "c3" * 20\n',
            1,
        )
        assert _lost_assertions(base, attacked, rel), (
            "a dynamically rebound named positive re-entered the registry")

    def test_a_literal_bound_historical_value_cannot_be_substituted(self):
        rel = "test_level1_stage1_activation_authorization.py"
        base = _git("show", f"{THIS_UNIT_MERGE_SHA}:{rel}")
        live = (ROOT / rel).read_text(encoding="utf-8")
        strong = (
            'assert workstream["last_verified_main_sha"] '
            '!= "413e033ac33741829168762ab24d73327c047d4b"'
        )
        assert live.count(strong) == 1
        weakened = live.replace(
            strong,
            'assert workstream["last_verified_main_sha"] != "' + "c3" * 20 + '"',
            1,
        )
        assert _lost_assertions(base, weakened, rel)

    def test_every_preexisting_register_negative_pin_is_retained_exactly(self):
        """Historical exclusions cannot finance the current live binding."""
        baseline_total = 0
        missing = {}
        for rel in sorted(PINNED_TEST_HASHES):
            baseline = _register_negative_inventory(
                _git("show", f"{THIS_UNIT_MERGE_SHA}:{rel}"))
            live = _register_negative_inventory(
                (ROOT / rel).read_text(encoding="utf-8"))
            baseline_total += baseline.total()
            lost = baseline - live
            if lost:
                missing[rel] = lost
        assert baseline_total == EXPECTED_RETAINED_REGISTER_NEGATIVES
        assert not missing, f"historical WS-0014 negative pins lost: {missing}"

    @pytest.mark.parametrize(
        "rel,digest,old,new,cat", BARE_LITERAL_REANCHORS,
        ids=[f"{r.split('_')[-2]}-{c}" for r, _d, _o, _n, c in BARE_LITERAL_REANCHORS])
    def test_every_registered_occurrence_is_real_and_lawful(
            self, rel, digest, old, new, cat):
        """POSITIVE CONTROLS: each of the six lawful sites, via its OWN identity.

        Narrowing the rule must not break the corpus it was derived from. Each
        entry is checked against its own file's real pinned baseline: the
        predecessor is really asserted there, the successor really replaces it,
        and the registered digest really is that assertion's fingerprint.
        """
        base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
        live = (ROOT / rel).read_text(encoding="utf-8")
        assert base != live, "this proof needs a genuinely re-anchored predecessor"
        assert old in base and new in live, "the entry's own endpoints have moved"
        # The registered digest is a real pinned assertion of this file...
        digests = {_fingerprint_digest(st)
                   for st in _assertion_fingerprints(base)}
        assert digest in digests, f"{rel}: registered digest matches no assertion"
        # ...and the whole file is clean once that occurrence is honoured.
        assert not _lost_assertions(base, live, rel), (
            f"the lawful {old} -> {new} occurrence in {rel} was reported as a loss")

    def test_a_registered_occurrence_is_consumed_at_most_once(self):
        """One registration authorizes exactly one transition, never two.

        Duplicating the registered assertion on both sides gives two identical
        pinned occurrences and one registration. The first is spent; the second
        has nothing left and is reported.
        """
        rel = "test_level1_stage1_readiness_verification_authorization.py"
        base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
        live = (ROOT / rel).read_text(encoding="utf-8")
        assert not _lost_assertions(base, live, rel)
        entry = [e for e in BARE_LITERAL_REANCHORS if e[0] == rel]
        assert len(entry) == 1, "this probe assumes one registration for the file"
        _r, digest, old, new, _c = entry[0]
        # Find the exact registered assertion's source text and duplicate it.
        src_line = next(l for l in base.splitlines() if old in l and "assert" in l)
        live_line = src_line.replace(old, new)
        lost = _lost_assertions(base + "\n" + src_line.strip() + "\n",
                                live + "\n" + live_line.strip() + "\n", rel)
        assert lost, "a single registration authorized two occurrences"

    def test_two_registered_occurrences_sharing_values_cannot_cross(self):
        """Same pair, two files: neither registration may cover the other's site.

        Both entries below use the identical `2026-08-27 -> 2026-08-28` pair, so
        under a value-keyed rule they were one licence. Keyed by occurrence they
        are two, and each is confined to its own file.
        """
        pair = ("2026-08-27", "2026-08-28")
        sites = [(r, d) for r, d, o, n, _c in BARE_LITERAL_REANCHORS
                 if (o, n) == pair]
        assert len(sites) >= 2, "this probe needs two sites sharing one pair"
        (rel_a, dig_a), (rel_b, dig_b) = sites[0], sites[1]
        assert rel_a != rel_b
        # A registration is scoped to its own file: file A's entries never include
        # file B's digest unless file B independently registered it.
        a_digests = set(_registered_occurrences(rel_a))
        b_digests = set(_registered_occurrences(rel_b))
        for rel, digs in ((rel_a, a_digests), (rel_b, b_digests)):
            for d in digs:
                assert any(r == rel and dd == d
                           for r, dd, _o, _n, _c in BARE_LITERAL_REANCHORS), (
                    f"{rel} resolved a digest it never registered")
        # And swapping the relpath does not carry a registration across files:
        # file A's baseline compared under file B's identity is only clean if B
        # independently registered that same assertion shape.
        base_a = _git("show", f"{BOUND_MERGE_SHA}:{rel_a}")
        live_a = (ROOT / rel_a).read_text(encoding="utf-8")
        if dig_a not in b_digests:
            assert _lost_assertions(base_a, live_a, rel_b), (
                "a registration was honoured under another file's identity")

    def test_an_unregistered_occurrence_of_a_registered_pair_stays_verbatim(self):
        """The general property, stated directly on the mechanism.

        A file's registrations are exactly its own entries. An assertion whose
        fingerprint is not among them buys nothing, however familiar its values.
        """
        rel = "test_level1_stage1_activation_authorization.py"
        registered = _registered_occurrences(rel)
        assert registered, "this probe needs a file with a registration"
        pinned = 'def f(freeze):\n    assert freeze["cutoff"] == "2026-08-27"\n'
        live = 'def f(freeze):\n    assert freeze["cutoff"] == "2026-08-28"\n'
        fp = _assertion_fingerprints(pinned)[0]
        assert _fingerprint_digest(fp) not in registered, (
            "this probe's own assertion must be UNregistered")
        assert _lost_assertions(pinned, live, rel), (
            "an unregistered occurrence was rewritten by a registered pair")

    def test_no_registration_fires_without_a_file_identity(self):
        """Fail closed: an unidentified comparison authorizes nothing."""
        assert _registered_occurrences(None) == {}
        assert _registered_occurrences("") == {}
        assert _registered_occurrences("not_a_pinned_suite.py") == {}

    def test_the_registry_is_complete_for_the_whole_pinned_corpus(self):
        """Nothing outside ``PROTECTED_PREDICATES`` needs an unregistered literal.

        This is how the registry was derived, kept executable so it cannot drift.
        It runs through the SAME occurrence-specific mechanism the guard itself
        uses -- it cannot validate itself through a permissive global-value path,
        because no such path exists any more.
        """
        unexplained = []
        for rel in sorted(PINNED_TEST_HASHES):
            if rel in PROTECTED_PREDICATES:
                continue
            live = (ROOT / rel).read_text(encoding="utf-8")
            try:
                base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
            except Exception:
                continue
            if base == live:
                continue
            if _lost_assertions(base, live, rel):
                unexplained.append(rel)
        assert not unexplained, (
            "these suites lose an assertion the registry does not explain: "
            f"{unexplained}")

    def test_every_registration_is_exercised_by_the_corpus(self):
        """No dead entry: each registration is actually needed by its own file.

        A registry that outgrows its corpus is a licence nobody is checking, so
        removing any single entry must make that file's comparison fail.
        """
        for rel, digest, old, new, cat in BARE_LITERAL_REANCHORS:
            base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
            live = (ROOT / rel).read_text(encoding="utf-8")
            reduced = tuple(e for e in BARE_LITERAL_REANCHORS
                            if not (e[0] == rel and e[1] == digest))
            saved = globals()["BARE_LITERAL_REANCHORS"]
            try:
                globals()["BARE_LITERAL_REANCHORS"] = reduced
                assert _lost_assertions(base, live, rel), (
                    f"the {rel} / {digest[:12]} registration is never needed")
            finally:
                globals()["BARE_LITERAL_REANCHORS"] = saved

    def test_a_stale_registry_entry_cannot_outlive_its_category(
            self, monkeypatch):
        """DIRECT GUARD TEST for the category re-check.

        DISCLOSED: with the live registry both entries are correctly categorised,
        so removing this check changes no real result -- this correction's own
        mutation proof showed that too. It guards a future registry whose entry
        has gone stale: if a value stops being the category the entry claims, the
        entry stops firing rather than substituting something it no longer
        understands.
        """
        pinned = 'def f():\n    assert "Merging it arms nothing" in s\n'
        live = 'def f():\n    assert "Merging it arms Stage 1" in s\n'
        fingerprint = _assertion_fingerprints(pinned)[0]
        rel = "synthetic_stale_registry.py"
        # Prose is not an anchor of any category, so this otherwise exact entry
        # must never fire.
        stale = ((rel, _fingerprint_digest(fingerprint),
                  "Merging it arms nothing", "Merging it arms Stage 1", "DATE"),)
        monkeypatch.setattr(sys.modules[__name__], "BARE_LITERAL_REANCHORS", stale)
        assert _lost_assertions(pinned, live, rel), (
            "a stale registry entry laundered an operative-prose rewrite")

    def test_a_registry_entry_whose_predecessor_is_absent_is_inert(self):
        """DISCLOSED EQUIVALENCE, recorded rather than dropped.

        The ``old_value not in p_lits`` guard is not observable: a placeholder
        mapped onto a value that appears nowhere in the pinned source cannot
        change any pinned fingerprint, and the only reachable effect of removing
        it is an EXTRA reported loss -- the safe direction. This correction's
        mutation proof demonstrated that, so the guard is documented as
        defence-in-depth and its inertness is pinned here instead of being
        claimed as a caught mutant.
        """
        pinned = 'def f():\n    assert a == "1999-01-01"\n'
        live = 'def f():\n    assert a == "2026-08-28"\n'
        # The registered predecessor is nowhere in `pinned`, so nothing is
        # replaceable and the unrelated swap is a plain loss.
        assert _lost_assertions(pinned, live)

    def test_registered_current_anchor_does_not_launder_a_historical_negative_pin(
            self, monkeypatch):
        """REQUIRED NEGATIVE 1 (review 5094619011).

        The first assertion is explicitly registered as the next lawful current
        anchor. The distinct XASSET-0060 negative pin is not registered and must
        be reported when it is rewritten to duplicate XASSET-0061.
        """
        a, b, c = "a1" * 20, "b2" * 20, "c3" * 20
        pinned = (f'XASSET0060_MAIN_SHA = "{a}"\n'
                  f'XASSET0061_MAIN_SHA = "{b}"\n'
                  'def f(ws):\n'
                  '    assert ws["last_verified_main_sha"] == XASSET0061_MAIN_SHA\n'
                  '    assert ws["last_verified_main_sha"] != XASSET0060_MAIN_SHA\n')
        live = (f'XASSET0060_MAIN_SHA = "{a}"\n'
                f'XASSET0061_MAIN_SHA = "{b}"\n'
                f'XASSET0062_MAIN_SHA = "{c}"\n'
                'def f(ws):\n'
                '    assert ws["last_verified_main_sha"] == XASSET0062_MAIN_SHA\n'
                '    assert ws["last_verified_main_sha"] != XASSET0061_MAIN_SHA\n')
        current = _assertion_fingerprints(pinned)[0]
        rel = "synthetic_next_current_anchor.py"
        entry = ((rel, _fingerprint_digest(current),
                  "XASSET0061_MAIN_SHA", b,
                  "XASSET0062_MAIN_SHA", c, "SHA"),)
        monkeypatch.setattr(sys.modules[__name__], "NAMED_ANCHOR_REANCHORS", entry)
        registered = _registered_named_occurrences(rel, pinned, live)
        assert list(registered) == [_fingerprint_digest(current)]
        lost = _lost_assertions(pinned, live, rel)
        assert len(lost) == 1, lost
        assert "NotEq()" in lost[0] and "XASSET0060_MAIN_SHA" in lost[0]

    def test_a_named_reanchor_never_normalizes_the_same_raw_values(self):
        """REQUIRED NEGATIVE 2 (review 5094619011).

        A real registered MAIN_SHA occurrence remains lawful, while an unrelated
        raw literal using the identical old/new pair is reported.
        """
        rel = "test_level1_stage1_activation_authorization.py"
        base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
        live = (ROOT / rel).read_text(encoding="utf-8")
        old = "301e79334876a4bda6e7b89a6156b34e8d38a605"
        new = "413e033ac33741829168762ab24d73327c047d4b"
        pinned = base + f'\n\ndef _raw(history):\n    assert history["required"] == "{old}"\n'
        current = live + f'\n\ndef _raw(history):\n    assert history["required"] == "{new}"\n'
        lost = _lost_assertions(pinned, current, rel)
        assert len(lost) == 1, lost
        assert "required" in lost[0] and f"Constant(value={old!r})" in lost[0]

    def test_a_named_registration_cannot_cover_a_second_same_role_occurrence(self):
        """REQUIRED NEGATIVE 3 (review 5094619011).

        The real current-anchor occurrence is registered. A second assertion
        changed with the same names in parallel has a different fingerprint and
        remains protected verbatim.
        """
        rel = "test_level1_stage1_activation_authorization.py"
        base = _git("show", f"{BOUND_MERGE_SHA}:{rel}")
        live = (ROOT / rel).read_text(encoding="utf-8")
        pinned = (base + '\n\ndef _other(history):\n'
                  '    assert history["required"] == XASSET0060_MAIN_SHA\n')
        current = (live + '\n\ndef _other(history):\n'
                   '    assert history["required"] == XASSET0061_MAIN_SHA\n')
        lost = _lost_assertions(pinned, current, rel)
        assert len(lost) == 1, lost
        assert "required" in lost[0] and "XASSET0060_MAIN_SHA" in lost[0]

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
        # 7. specifically lawful same-role re-anchor permitted -- under the file's
        #    own identity, which is what a registered literal occurrence needs
        base = _git("show", f"{BOUND_MERGE_SHA}:{act}")
        assert base != act_src
        assert not _lost_assertions(base, act_src, act)
        #    ...and fail-closed without it: no file identity, no literal licence
        assert _lost_assertions(base, act_src)
        # 8. cross-domain review/run/job/comment ids never collapse into SHAs
        for ident in ("4976985695", "5092359752", "100319912406", "33651659011"):
            assert _anchor_category(ident) == "NUMBER", ident
        assert _anchor_category("637eaa30302f5a71f84ab1d215ecbd32c01399b5") == "SHA"
        rebind = "test_level1_stage1_post_correction_rebinding_authorization.py"
        rb_src = (ROOT / rebind).read_text(encoding="utf-8")
        assert _lost_assertions(
            rb_src,
            rb_src.replace('assert "4976985695" in description',
                           'assert "637eaa30302f5a71f84ab1d215ecbd32c01399b5" '
                           "in description")), \
            "a review id was still interchangeable with a merge SHA"
        # 9. ONE LAWFUL DATE RE-ANCHOR NEVER LAUNDERS AN UNRELATED DATE SWAP
        assert _lost_assertions(
            'def f():\n    assert r.startswith("2026-08-27")\n'
            '    assert c == "2026-08-26"\n',
            'def f():\n    assert r.startswith("2026-08-28")\n'
            '    assert c == "2026-08-28"\n'), \
            "a registered re-anchor laundered an unrelated same-category swap"
        # 10. DATE means a COMPLETE, REAL date -- never date-prefixed prose
        assert _anchor_category("2026-08-27 Merging it arms nothing") is None
        assert _anchor_category("2026-02-30") is None
        assert _anchor_category("2026-08-27") == "DATE"
        assert _lost_assertions(
            'def f():\n    assert "2026-08-27 Merging it arms nothing" in s\n',
            'def f():\n    assert "2026-08-28 Merging it arms Stage 1" in s\n'), \
            "date-prefixed operative prose was rewritten unseen"
        # 11. an unregistered literal buys NOTHING, whatever else the delta adds
        unregistered_pinned = (
            'X = "1111111111111111111111111111111111111111"\n'
            'def f():\n    assert a == "2222222222222222222222222222222222222222"\n')
        unregistered_live = (
            'X = "1111111111111111111111111111111111111111"\n'
            'Y = "3333333333333333333333333333333333333333"\n'
            'def f():\n    assert a == "3333333333333333333333333333333333333333"\n')
        assert _lost_assertions(unregistered_pinned, unregistered_live), (
            "an unregistered literal was granted a substitution licence")
        # 12. A REGISTERED OCCURRENCE NEVER LAUNDERS THE SAME PAIR ELSEWHERE
        p337 = "test_level1_stage1_pr337_actor_evidence_correction_authorization.py"
        p337_base = _git("show", f"{BOUND_MERGE_SHA}:{p337}")
        p337_live = (ROOT / p337).read_text(encoding="utf-8")
        assert not _lost_assertions(p337_base, p337_live, p337)
        assert _lost_assertions(
            p337_base + '\n\ndef _p(f):\n    assert f["cutoff"] == "2026-08-27"\n',
            p337_live + '\n\ndef _p(f):\n    assert f["cutoff"] == "2026-08-28"\n',
            p337), "a registered occurrence laundered an unrelated same-pair swap"
        # 13. EVERY datetime COMPONENT is range-checked, not merely shaped
        for invalid in ("2026-08-27T99:99:99Z", "2026-08-27T24:00:00Z",
                        "2026-08-27T23:60:00Z", "2026-08-27T23:59:60Z",
                        "2026-08-27T12:30:00+24:00", "2026-08-27T12:30:00+00:60",
                        "2026-02-30", "2026-13-45"):
            assert _anchor_category(invalid) is None, invalid
        for valid in ("2026-08-27", "2026-08-27T12:30:00Z", "2026-08-27 12:30",
                      "2026-08-27T12:30:00+01:00", "2026-08-27T23:59:59.123Z"):
            assert _anchor_category(valid) == "DATE", valid
        # 14. an unrelated same-category constant cannot collide merely because
        #     ANOTHER anchor of that category was added by the delta
        header = ('A_SHA = "413e033ac33741829168762ab24d73327c047d4b"\n'
                  'UNRELATED_SHA = "3db918530b10ffc1423ba0b749b086e349a4901d"\n')
        pinned_x = header + "def f():\n    assert x == A_SHA\n"
        live_x = (header + 'B_SHA = "637eaa30302f5a71f84ab1d215ecbd32c01399b5"\n'
                  + "def f():\n    assert x == UNRELATED_SHA\n")
        assert _lost_assertions(pinned_x, live_x), (
            "an unrelated same-category constant collided with a re-anchored one")

    def test_the_protected_catalog_predicate_is_asserted_directly(self):
        """Belt and braces: the ONE named protected property, pinned by name.

        The semantic inventory is the general mechanism. This specific predicate
        is also asserted directly because it belongs to the protected-predicate
        set rather than the occurrence-registered predecessor comparison.
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
