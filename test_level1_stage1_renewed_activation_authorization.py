"""Adversarial tests pinning the ``XASSET-0052`` renewed link-5 / step-11 activation authorization.

``XASSET-0041`` §I set out a five-link remediation sequence. Links 1--4 are discharged: the
correction (``XASSET-0042``), the step-8-equivalent rebinding (``XASSET-0049``), the renewed
readiness verification (``STEP_9_READINESS_VERIFICATION_PASS``), and the renewed fail-closed drift
check (``STEP_10_NO_DRIFT``). **Link 5 is next, and it had no authority.**

``XASSET-0040`` supplied that authority once. Its single unit ran and reached a terminal
``STOPPED_BEFORE_ATTESTATION``, so that grant is **spent**, and **ten** later filings each named
step 11 / link 5 and each withheld it -- ``XASSET-0041``, ``XASSET-0043``, ``XASSET-0044``,
``XASSET-0045``, ``XASSET-0046``, ``XASSET-0047``, ``XASSET-0048``, ``XASSET-0049``,
``XASSET-0050``, ``XASSET-0051``. ``XASSET-0052`` closes that gap for link 5 and nothing else.

The whole risk of an authorization filing is that it grants more than it says, or that a future
session reads more out of it than it contains. Every test below therefore pins **an authorized
boundary and its nearest plausible overreach** -- the stronger permission a successor might infer
from the same text, which the decision must refuse.

The overreaches that matter most each have a dedicated guard:

1. **Link 5 performed now, or treated as authorized on filing.**
   ``TestLink5IsNotPerformedHere`` and ``TestEffectivityRequiresCompleteLifecycleClosure`` fail if
   the filing attests, arms, claims, executes, or lets any single lifecycle step stand in for
   complete closure.
2. **``XASSET-0040`` treated as revivable.** ``TestXasset0040IsSpentAsAStop`` fails if the filing
   revives, amends, extends, or re-opens it, or if its dead anchors are not pinned NEGATIVELY.
3. **The authority/performance distinction collapsed.**
   ``TestTheAuthorityPerformanceDistinction`` fails if link 5 is placed inside a "not authorized"
   list, or if §A.1's canonical sentence is absent or weakened.
4. **More than one unit granted.** ``TestExactlyOneFutureUnit``.
5. **The attestation rebound to this decision.**
   ``TestTheAttestationMechanismIsClosedAndUnchanged`` fails if any module constant moves, if
   ``XASSET-0052`` is inserted into the payload, or if the eighteen bound paths change.
6. **The intervening-commit rule softened to ancestry.** ``TestTheInterveningCommitRule`` fails if
   descendant ancestry is treated as sufficient, if a merge SHA is predicted, or if an unexpected
   commit is anything other than a stop.
7. **The lane order relaxed.** ``TestTheRequiredLaneTransitionOrder``.
8. **A stop turned into a retry.** ``TestNoRetryNoRecovery`` and ``TestTerminalOutcomes``.
9. **The reserved results PR consumed.** ``TestP1ResultsPRRemainsSeparate``.
10. **A protected or load-bearing path slipping into the diff.** ``TestNoProtectedPathIsTouched``
    compares every one of them, byte for byte, against the bound merge.
11. **A vacuous prohibition assertion.** ``TestProhibitionsAreBoundToTheirGoverningClause``
    extracts each withheld bullet from its governing "must not:" clause and binds whole lines, so
    prefixing a permissive qualifier fails rather than survives.

They also pin the negative space that makes the filing honest: this authorization PR changes no
canonical file, no validator, no authorization module, no runner, no result validator, and no
load-bearing byte; all eighteen load-bearing paths, both canonical pins, the frozen universe, and
the construction-universe module identity are untouched; ``REQUIRED_LIFECYCLE_GATES`` is still the
six-element tuple; and Stage 1 is still ``UNARMED`` with lane state ``ABSENT`` and ``ATTEMPT_1``
unclaimed.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No results document, lane directory, attestation, claim, completion, or ledger
entry is created or read for authorization purposes. No ``risk_lane_boundary`` protected result
path is read, listed, opened, or referenced.
"""

from __future__ import annotations

import ast
import hashlib
import inspect
import os
import re
import subprocess
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

DECISION_ID = "XASSET-0052"
DECISION = (
    GOV
    / "XASSET-0052-endpoint-0001-stage-1-renewed-step-11-activation-and-execution-authorization.md"
)

D0027 = GOV / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
D0029 = GOV / "XASSET-0029-endpoint-0001-stage-1-operational-authorization.md"
D0030 = GOV / "XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md"
D0040 = (
    GOV / "XASSET-0040-endpoint-0001-stage-1-step-11-activation-and-execution-authorization.md"
)
D0041 = (
    GOV
    / "XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md"
)
D0043 = GOV / "XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md"
D0044 = GOV / "XASSET-0044-endpoint-0001-stage-1-post-correction-operational-rebinding.md"
D0045 = GOV / "XASSET-0045-endpoint-0001-stage-1-post-merge-ci-recovery-authorization.md"
D0046 = GOV / "XASSET-0046-endpoint-0001-stage-1-post-merge-ci-recovery-reauthorization.md"
D0047 = GOV / "XASSET-0047-endpoint-0001-stage-1-post-merge-ci-recovery-reconciliation.md"
D0048 = GOV / "XASSET-0048-endpoint-0001-stage-1-step-8-equivalent-rebinding-authorization.md"
D0049 = (
    GOV
    / "XASSET-0049-endpoint-0001-stage-1-step-8-equivalent-successor-operational-rebinding.md"
)
D0050 = (
    GOV
    / "XASSET-0050-endpoint-0001-stage-1-renewed-readiness-verification-authorization.md"
)
D0051 = (
    GOV
    / "XASSET-0051-endpoint-0001-stage-1-renewed-drift-check-fail-closed-authorization.md"
)

# ---------------------------------------------------------------------------------------------
# The effective XASSET-0049 bound merge. Verified live in preflight against the object store.
# ---------------------------------------------------------------------------------------------

BOUND_MERGE_SHA = "a941455491cc5e4d3d868775fb6b4b88f0fe2ce3"
BOUND_MERGE_PARENT_1 = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"
BOUND_MERGE_PARENT_2 = "b2059e80101fc6457f4004939d7d12886e6feedf"
BOUND_MERGE_TREE = "b7015b271362ae0c2fe663e8bfda9c6d10de5e7e"

# ---------------------------------------------------------------------------------------------
# The two completed renewed determinations, and the base this filing is anchored to.
# ---------------------------------------------------------------------------------------------

#: Link 3 -- the valid FIRST and only exercise of XASSET-0050's one-shot authority.
LINK3_PASS_COMMENT = "5384453102"
LINK3_PASS_DETERMINATION = "STEP_9_READINESS_VERIFICATION_PASS"

#: A LATER, separate concurrent session's correct fail-closed stop. Carries NO PASS, is NOT an
#: anchor, and does not invalidate the determination above. Pinned so it can never be promoted.
LINK3_DUPLICATE_STOP_COMMENT = "5384471997"

#: Link 4 -- the ONE XASSET-0051-authorized drift check. Its grant is now spent.
LINK4_DETERMINATION_COMMENT = "5387645607"
LINK4_DETERMINATION = "STEP_10_NO_DRIFT"

#: The exact `main` at which the link-4 determination was recorded. This filing's base, and the
#: FIRST parent the future unit's acting merge must have (§G.1).
LINK4_OBSERVATION_HEAD = "8def8bd096b4edecbf10fc20870a6d03b6cb56fe"

#: XASSET-0051's own lifecycle closure, and the accepted head it closed at.
XASSET0051_CLOSURE_COMMENT = "5386974704"
XASSET0051_ACCEPTED_HEAD = "753524a96526d2e6ccbcffb065baf3a2e1dfaf7e"
XASSET0051_BASE = "ea9e74a1f4224a78df2416db9c872b0c5812894b"

# ---------------------------------------------------------------------------------------------
# NEGATIVE pins. XASSET-0040's grant is SPENT and its anchors are DEAD; a silent reversion to any
# of them must FAIL rather than pass unnoticed.
# ---------------------------------------------------------------------------------------------

SPENT_STEP11_EVIDENCE_COMMENT = "5343692162"
SPENT_STEP11_DETERMINATION = "STOPPED_BEFORE_ATTESTATION"

DEAD_MERGE_SHA = "637eaa30302f5a71f84ab1d215ecbd32c01399b5"
DEAD_STEP9_EVIDENCE_COMMENT = "5336643459"
DEAD_STEP10_EVIDENCE_COMMENT = "5341448714"
DEAD_LOAD_BEARING_COUNT = 10
DEAD_AUTHORIZING_DECISION = "XASSET-0037"
DEAD_AUTHORIZING_PULL_REQUEST = 337

# ---------------------------------------------------------------------------------------------
# The pins the binding conditions bind.
# ---------------------------------------------------------------------------------------------

EXPECTED_LOAD_BEARING_COUNT = 18


# ── RE-ANCHORED BY XASSET-0060 ──────────────────────────────────────────────────────────────
#
# XASSET-0060 is the ONE post-parser-correction rebinding XASSET-0057 SS-E authorizes. Under
# XASSET-0057 SS-F.7 it extends LOAD_BEARING_RELPATHS ADDITIVELY, 18 -> 25, adding the six
# decisions that authorized and defined the formal-disposition parser plus its own decision file.
#
# This suite's claims are about the merge THIS unit bound, which is IMMUTABLE. A later unit
# lawfully adding paths does not falsify any of them -- but comparing the LIVE tuple against that
# historical merge silently turned "my paths are unchanged" into "no successor may ever add one",
# which is a claim this suite never had the authority to make and which the anchoring-to-a-moving-
# reference defect (the one that stopped PRs #344 and #345) is exactly about.
#
# The re-anchor is STRICTLY STRENGTHENING, never a relaxation:
#   * the historical membership is DERIVED BY AST from the bound merge, not restated;
#   * its COUNT is still pinned at exactly EXPECTED_LOAD_BEARING_COUNT;
#   * the live tuple must contain the historical set as an ORDERED PREFIX -- so nothing may be
#     removed, reordered, swapped or traded away, which the old equality could not distinguish
#     from a wholesale replacement of equal length;
#   * the live count is pinned EXACTLY at SUCCESSOR_LOAD_BEARING_COUNT, so a further silent
#     addition still fails here.
SUCCESSOR_LOAD_BEARING_COUNT = 25
SUCCESSOR_DECISION_ID = "XASSET-0060"
SUCCESSOR_REVIEWED_BASE_SHA = "301e79334876a4bda6e7b89a6156b34e8d38a605"


def _load_bearing_declared_at_bound_merge() -> tuple[str, ...]:
    """The exact tuple the production module DECLARED at ``BOUND_MERGE_SHA``.

    Parsed with ``ast`` and never imported or executed, so a historical module's code cannot run.
    Module-level string aliases and implicit concatenation are resolved from the SAME historical
    source, never from the live module.
    """
    source = subprocess.run(
        ["git", "show", f"{BOUND_MERGE_SHA}:level1_stage1_execution_authorization.py"],
        cwd=ROOT, capture_output=True, check=True, text=True,
    ).stdout
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
    raise AssertionError("LOAD_BEARING_RELPATHS is not declared at the bound merge")


HISTORICAL_LOAD_BEARING = _load_bearing_declared_at_bound_merge()


def _assert_boundary_is_the_bound_set_plus_authorized_additions() -> None:
    """Shared by every re-anchored claim in this suite, so one weakening cannot slip into one."""
    live = tuple(A.LOAD_BEARING_RELPATHS)
    assert len(HISTORICAL_LOAD_BEARING) == EXPECTED_LOAD_BEARING_COUNT
    assert len(set(HISTORICAL_LOAD_BEARING)) == EXPECTED_LOAD_BEARING_COUNT
    # ORDERED PREFIX: nothing removed, reordered, swapped or traded away.
    assert live[:EXPECTED_LOAD_BEARING_COUNT] == HISTORICAL_LOAD_BEARING
    assert set(HISTORICAL_LOAD_BEARING) <= set(live)
    # The successor's own count, pinned exactly -- a further silent addition still fails.
    assert len(live) == SUCCESSOR_LOAD_BEARING_COUNT
    assert len(set(live)) == SUCCESSOR_LOAD_BEARING_COUNT

#: The five outcome-capable modules §G item 3 names individually, recorded as the filing-time
#: WITNESS. The value DERIVED from the bound merge tree is operative; this table exists so a drift
#: between the two fails in CI instead of waiting to be noticed at verification time.
OUTCOME_CAPABLE_MODULE_WITNESS = {
    "level1_stage1_runner.py":
        "4a88cf6d0271da0dc3a6ca175fadb0223bf7ff8843479733cbcf0effd47ba5d9",
    "level1_stage1_result_validator.py":
        "b4773eb767158434136b72316e9802308b9e6fb47b6e45f8f10445c02cee3b7a",
    "level1_endpoint_evidence_preregistration_validator.py":
        "b3a87e4f8b828d420795348642c977a9f0585eafa9262a4be48df406f770233d",
    "level1_construction_universe_closure_validator.py":
        "1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5",
    "level1_stage1_execution_authorization.py":
        "4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541",
}

CANONICAL_PINS = {
    "research/level1_endpoint_evidence/PROTOCOL_V1.md":
        "1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84",
    "research/level1_endpoint_evidence/pre_registration.yaml":
        "898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f",
}

CONSTRUCTION_COUNT = 680
CELL_COUNT = 48
UNIVERSE_SHA = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"

#: XASSET-0049's lawful rebinding, which this filing must not touch. REVIEWED_BASE_SHA is that
#: rebinding base -- NOT a "current main" field that advances with every merge.
BOUND_AUTHORIZING_DECISION = "XASSET-0049"
BOUND_AUTHORIZING_PULL_REQUEST = 349
BOUND_REVIEWED_BASE_SHA = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"

EXPECTED_LIFECYCLE_GATES = (
    "INDEPENDENT_FULL_EXACT_HEAD_REVIEW",
    "PRINCIPAL_EXACT_HEAD_ACCEPTANCE",
    "MERGE",
    "POST_MERGE_VERIFICATION",
    "MERGE_COMMIT_CI_SUCCESS",
    "MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION",
)

ATTEMPT_ID = "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

PORTFOLIO_RELPATHS = (
    "allocate.py",
    "margin_state.py",
    "levels.py",
    "targets.yaml",
    "holdings.yaml",
    "gates.yaml",
    "issuer_lookthrough.yaml",
)

#: An impossible sentinel, distinct from every sentinel used before (-1, -2, -50, -51). Committed
#: first, then replaced by the number GitHub actually issued in a fast-forward follow-up commit.
#: RETAINED as a negative pin so a revert to the unbound state still fails.
PR_SENTINEL = -52
PRIOR_SENTINELS = (-1, -2, -50, -51)

#: The number GitHub ISSUED for this unit, read back from the live API after the draft was opened.
#: Never predicted, never guessed.
THIS_PULL_REQUEST = 353

THIS_GATE = "xasset0052-renewed-step11-activation-authorization"
PRIOR_UNIT_GATE = "xasset0051-renewed-drift-check-authorization"
PRIOR_CLOSURE_GATE = "xasset0051-post-merge-verification"

#: Every filing that named step 11 / link 5 and DECLINED to grant it, with the verbatim clause the
#: claim rests on. Machine-verified against the live predecessor file, so a paraphrase drifting
#: from source -- or a later source edit invalidating a citation -- FAILS rather than survives.
WITHHOLDING_QUOTES = {
    "XASSET-0041": (
        D0041,
        "5. new step-11 authorization   (separately authorized; XASSET-0040 is spent as a stop)",
    ),
    "XASSET-0043": (D0043, "`XASSET-0030` §G.B steps 9, 10, or 11, in whole or in part;"),
    "XASSET-0044": (D0044, "`XASSET-0030` §G.B steps 9, 10, or 11, in whole or in part;"),
    "XASSET-0045": (D0045, "- perform or authorize **Step 11**;"),
    "XASSET-0046": (D0046, "- perform or authorize **Step 11**;"),
    "XASSET-0047": (D0047, "- perform or authorize **Step 11**;"),
    "XASSET-0048": (
        D0048,
        "- **Step 11** in any part (§G.B step 11 / link 5) — `XASSET-0040` stays spent as a stop;",
    ),
    "XASSET-0049": (
        D0049,
        "- **Step 11** in any part (`§G.B` step 11 / link 5) — `XASSET-0040` stays spent as a "
        "stop;",
    ),
    "XASSET-0050": (
        D0050,
        "**perform or authorize `XASSET-0041` §I link 4 or link 5 — `XASSET-0030` §G.B step 10 "
        "or step 11.**",
    ),
    "XASSET-0051": (
        D0051,
        "**perform or authorize `XASSET-0041` §I link 5 — `XASSET-0030` §G.B step 11 — in any "
        "part.**",
    ),
}


# ---------------------------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------------------------


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=True, text=True
    ).stdout.strip()


# ``git commit-tree`` refuses to run without a committer identity, and a bare CI checkout has
# none configured (``actions/checkout`` sets no ``user.email``/``user.name``). Supplying one
# through the environment keeps the synthetic-merge probe below hermetic: it depends on no
# ambient git configuration, and — unlike ``git config`` — it mutates nothing, so the checkout
# is left exactly as found. Caught by CI on run 32667212952 attempt 3, where the ambient
# identity this development environment happens to carry was simply absent.
_SYNTHETIC_COMMIT_IDENTITY = {
    "GIT_AUTHOR_NAME": "xasset-0052-test",
    "GIT_AUTHOR_EMAIL": "xasset-0052-test@invalid",
    "GIT_COMMITTER_NAME": "xasset-0052-test",
    "GIT_COMMITTER_EMAIL": "xasset-0052-test@invalid",
}


def _git_with_identity(*args: str) -> str:
    """``_git``, but with an explicit committer identity supplied via the environment."""
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
        env={**os.environ, **_SYNTHETIC_COMMIT_IDENTITY},
    ).stdout.strip()


def _blob_sha256_at(relpath: str, rev: str = BOUND_MERGE_SHA) -> str:
    """SHA-256 of ``relpath`` as it exists in the git tree at ``rev``.

    Reading from an immutable commit rather than the worktree is what keeps these assertions
    anchored: a claim measured against a moving ref is the defect that stopped PRs #344 and #345.
    """
    blob = subprocess.run(
        ["git", "show", f"{rev}:{relpath}"], cwd=ROOT, capture_output=True, check=True
    ).stdout
    return hashlib.sha256(blob).hexdigest()


@pytest.fixture(scope="module")
def decision_text() -> str:
    return DECISION.read_text()


@pytest.fixture(scope="module")
def ws0014() -> dict:
    data = yaml.safe_load(WORKSTREAMS.read_text())
    return next(w for w in data["workstreams"] if w["id"] == "WS-0014")


@pytest.fixture(scope="module")
def withheld(decision_text) -> list[str]:
    """Whole withheld bullets, extracted from §H's own governing prohibitive clause."""
    return _bullets_under(_raw_section(decision_text, "H."), "The link-5 unit **must not**:")


@pytest.fixture(scope="module")
def catalog() -> list:
    data = yaml.safe_load(CATALOG.read_text())
    return data["decisions"] if isinstance(data, dict) else data


def _flat(text: str) -> str:
    """Collapse runs of whitespace.

    The decision file is hard-wrapped at ~100 columns, so a multi-word phrase can fall across a
    line break. Normalizing means a phrase assertion tests the PROSE rather than where the
    wrapper happened to break it; `|` and other structural characters survive intact.
    """
    return " ".join(text.split())


def _flat_prose(text: str) -> str:
    """``_flat`` with markdown blockquote markers removed first.

    §A.1 states the canonical distinction as a blockquote so it can be lifted verbatim into a
    summary. Collapsing whitespace alone leaves the ``>`` markers embedded mid-sentence, which
    would make a prose assertion fail for a purely typographic reason.
    """
    stripped = "\n".join(re.sub(r"^\s*>\s?", "", line) for line in text.split("\n"))
    return _flat(stripped)


def _demphasize(text: str) -> str:
    """Strip markdown emphasis markers so a prose assertion tests words, not typography.

    Single-asterisk italics are stripped too: §G.1 emphasises *between* and *after* mid-
    sentence, and a guard that only knew about ``**`` failed on correct text.
    """
    return text.replace("*", "").replace("`", "")


def _section(text: str, heading: str) -> str:
    """The whitespace-normalized body of one ``### X.`` section.

    Scoping to one section is what stops a claim being satisfied by identical words elsewhere in
    the document.
    """
    pattern = rf"^### {re.escape(heading)}.*?(?=^### |^## |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    assert match, f"section {heading!r} not found"
    return _flat(match.group(0))


def _subsection(text: str, heading: str) -> str:
    """The whitespace-normalized body of one ``#### X`` subsection.

    ``_section`` matches ``### `` only; a subsection assertion scoped with it silently matches
    nothing and raises, which is how ``G.1`` was found to need its own accessor.
    """
    pattern = rf"^#### {re.escape(heading)}.*?(?=^#### |^### |^## |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    assert match, f"subsection {heading!r} not found"
    return _flat(match.group(0))


def _raw_subsection(text: str, heading: str) -> str:
    """The RAW (unflattened) body of one ``#### X`` subsection.

    ``_subsection`` flattens, which embeds markdown blockquote markers mid-line and makes
    ``_flat_prose``'s per-line strip a no-op. §A.1 states its canonical sentence as a
    blockquote, so it needs the raw text.
    """
    pattern = rf"^#### {re.escape(heading)}.*?(?=^#### |^### |^## |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    assert match, f"subsection {heading!r} not found"
    return match.group(0)


def _raw_section(text: str, heading: str) -> str:
    """The RAW (unflattened) body of one ``### X.`` section, for line-level extraction."""
    pattern = rf"^### {re.escape(heading)}.*?(?=^### |^## |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    assert match, f"section {heading!r} not found"
    return match.group(0)


def _bullets_under(raw: str, governing: str) -> list[str]:
    """Whole bullet lines following ``governing``, joined across hard wraps.

    XASSET-0051's own P9 probe found that asserting a prohibition's WORDS are present is vacuous:
    prefixing "it may " to a bullet leaves every substring intact while inverting the meaning.
    Extracting from the governing clause and binding WHOLE LINES is the repair, carried forward.
    """
    idx = raw.find(governing)
    assert idx != -1, f"governing clause {governing!r} not found"
    body = raw[idx + len(governing):]
    # stop at the first subsection or section boundary
    stop = re.search(r"^(####|###|##) ", body, re.M)
    if stop:
        body = body[: stop.start()]
    bullets: list[str] = []
    current: list[str] = []
    for line in body.split("\n"):
        if line.startswith("- "):
            if current:
                bullets.append(_flat(" ".join(current)))
            current = [line[2:]]
        elif current and line.startswith("  ") and line.strip():
            current.append(line.strip())
        elif current and not line.strip():
            bullets.append(_flat(" ".join(current)))
            current = []
        elif current:
            bullets.append(_flat(" ".join(current)))
            current = []
    if current:
        bullets.append(_flat(" ".join(current)))
    return [b for b in bullets if b]


# ---------------------------------------------------------------------------------------------


class TestTheFilingExistsAndIsWellFormed:
    def test_decision_file_exists_with_correct_frontmatter(self, decision_text):
        assert decision_text.startswith("---\n")
        front = yaml.safe_load(decision_text.split("---")[1])
        assert front["decision_id"] == DECISION_ID
        assert front["status"] == "Proposed"
        assert front["supporting_artifact"] == Path(__file__).name
        assert front["category"] == "cross_asset_allocation_architecture"

    def test_the_decision_is_not_marked_accepted_by_its_own_filing(self, decision_text):
        """A filing may never certify its own acceptance; §N's seven conditions do that."""
        front = yaml.safe_load(decision_text.split("---")[1])
        assert front["status"] != "Accepted"

    def test_the_related_decisions_name_the_whole_remediation_chain(self, decision_text):
        front = yaml.safe_load(decision_text.split("---")[1])
        related = set(front["related_decisions"])
        for required in (
            "XASSET-0027", "XASSET-0029", "XASSET-0030", "XASSET-0040", "XASSET-0041",
            "XASSET-0042", "XASSET-0043", "XASSET-0044", "XASSET-0048", "XASSET-0049",
            "XASSET-0050", "XASSET-0051",
        ):
            assert required in related, required

    def test_every_lettered_section_the_body_relies_on_exists(self, decision_text):
        for heading in "ABCDEFGHIJKLMNO":
            assert re.search(rf"^### {heading}\. ", decision_text, re.M), heading
        for sub in ("A.1", "E.1", "G.1", "H.1", "I.1", "J.1"):
            assert re.search(rf"^#### {re.escape(sub)} ", decision_text, re.M), sub


class TestTheAuthorityPerformanceDistinction:
    """§A / §A.1 -- the one thing this decision grants must never appear as withheld."""

    def test_the_determination_string_is_exact(self, decision_text):
        assert "`RENEWED_STEP_11_ACTIVATION_AND_EXECUTION_AUTHORIZED`" in decision_text

    def test_section_a_conditionally_grants_link_5_and_says_it_performs_none_of_it(
        self, decision_text
    ):
        a = _demphasize(_section(decision_text, "A."))
        assert "Exactly one future, separate, bounded" in a
        assert "link 5" in a and "step-11" in a
        assert "conditionally authorized" in a
        assert "This filing performs none of those acts." in a
        assert "Merging it arms nothing" in a

    def test_a1_states_the_canonical_distinction_verbatim(self, decision_text):
        """CORRECTED after review 5003284327 MAJOR 2.

        The reviewed head required the sentence "neither performed nor authorized by this filing
        itself" -- which denies authorization of exactly the acts §A grants, and so demanded the
        defect rather than detecting it. The canonical sentence now states CONDITIONAL
        AUTHORIZATION, NON-PERFORMANCE, and NON-EXERCISABILITY as three separate claims.
        """
        quote = _demphasize(_flat_prose(_raw_subsection(decision_text, "A.1")))
        assert (
            "XASSET-0052 conditionally authorizes exactly one future, separate link-5 "
            "activation-and-execution unit, but this filing performs none of those acts, and "
            "none is exercisable unless and until §N closes and every §G and §G.1 condition "
            "holds." in quote
        )

    def test_a1_forbids_placing_the_link_5_acts_inside_a_not_authorized_list(self, decision_text):
        a1 = _demphasize(_subsection(decision_text, "A.1"))
        assert (
            'Link 5 — and each of its constituent acts — never belongs inside a "not authorized" '
            "list." in a1
        )
        assert "exactly what this decision is the authority for" in a1
        assert "conditionally-authorized-but-unperformed" in a1
        assert "unsafe acceptance evidence" in a1

    def test_a1_prohibits_the_three_contradictory_claims(self, decision_text):
        """ADDED after review 5003284327 MAJOR 2 — the prohibitions must be stated, not implied."""
        a1 = _demphasize(_subsection(decision_text, "A.1"))
        assert '"not authorized by this filing itself" — this filing *is*' in a1 or (
            '"not authorized by this filing itself"' in a1 and "conditional authority source" in a1
        )
        assert '"zero activation authority" or "zero activation authorizations"' in a1
        assert "zero committed activation factors" in a1
        assert "performed, armed, claimed, executed, or produced anything" in a1

    def test_a1_separates_conditional_authority_from_the_act_and_from_exercisability(
        self, decision_text
    ):
        a1 = _demphasize(_subsection(decision_text, "A.1"))
        assert (
            "The grant is of conditional authority, never of the act, and never of present "
            "exercisability." in a1
        )
        assert "may lawfully end without arming anything" in a1

    def test_the_decision_never_denies_authority_for_the_link_5_acts(self, decision_text):
        """The exact MAJOR-2 defect, encoded so it cannot recur anywhere in the governed text."""
        flat = _demphasize(_flat_prose(decision_text)).lower()
        forbidden = "neither performed nor authorized by this filing itself"
        # It may appear ONLY inside §A.1's own prohibition list, never as an operative claim.
        a1 = _demphasize(_flat_prose(_raw_subsection(decision_text, "A.1"))).lower()
        outside = flat.replace(a1, "")
        assert forbidden not in outside, "the denial survives outside §A.1's prohibition list"

    def test_the_decision_never_claims_zero_activation_authority(self, decision_text):
        flat = _demphasize(_flat_prose(decision_text)).lower()
        a1 = _demphasize(_flat_prose(_raw_subsection(decision_text, "A.1"))).lower()
        e = _demphasize(_flat_prose(_raw_section(decision_text, "E."))).lower()
        outside = flat.replace(a1, "").replace(e, "")
        for banned in ("zero activation authority", "zero activation authorizations"):
            assert banned not in outside, banned

    def test_the_decision_states_the_conditional_grant_at_the_point_of_grant(self, decision_text):
        a = _demphasize(_section(decision_text, "A."))
        assert "is **conditionally authorized**" in _section(decision_text, "A.")
        assert "This decision is the authority source for each of those acts." in a
        assert "The authorization is conditional, and nothing in it is exercisable yet." in a
        assert "zero committed activation factors" in a

    def test_the_decision_never_claims_to_have_performed_anything(self, decision_text):
        flat = _demphasize(_flat_prose(decision_text)).lower()
        for banned in (
            "this filing armed", "this filing claimed", "this filing executed",
            "this decision armed", "this decision claimed", "this decision executed",
            "this filing produced the canonical", "this filing attested",
        ):
            assert banned not in flat, banned

    def test_no_governed_section_places_link_5_on_the_withheld_side(self, decision_text):
        """The exact defect XASSET-0051 §A.1 named: a record that both grants and denies link 5.

        §H and §O enumerate what the future UNIT and this FILING may not do. Neither may say that
        link 5 -- or any of its constituent acts -- is unauthorized, because §A conditionally
        grants all of them. STRENGTHENED after review 5003284327 MAJOR 2 to cover the constituent
        acts by name, not just the phrase "link 5".
        """
        for heading in ("H.", "O."):
            body = _demphasize(_section(decision_text, heading)).lower()
            for banned in (
                "link 5 is not authorized",
                "link 5 remains unauthorized",
                "link 5 is neither performed nor authorized",
                "does not authorize link 5",
                "authorizes no part of link 5",
                "the attestation is not authorized",
                "arming is not authorized",
                "the claim of attempt_1 is not authorized",
                "the 680-construction run is not authorized",
                "neither performed nor authorized by this filing itself",
                "zero activation authority",
                "zero activation authorizations",
            ):
                assert banned not in body, (heading, banned)

    def test_section_o_declares_itself_a_non_performance_section(self, decision_text):
        """ADDED after review 5003284327 MAJOR 2 — §O must say what it is, so a reader cannot
        read its list as a denial of the §A grant."""
        o = _demphasize(_section(decision_text, "O."))
        assert "about what this filing does not *do*" in o or (
            "what this filing does not" in o and "never a denial of the one thing" in o
        )
        assert "conditionally authorizes" in o.lower()
        assert "merely unperformed and not yet exercisable" in o


class TestExactlyOneFutureUnit:
    def test_exactly_one_unit_is_granted_in_both_a_and_the_consequences(self, decision_text):
        a = _demphasize(_section(decision_text, "A."))
        assert "Exactly one future, separate, bounded" in a
        cons = _demphasize(_flat(decision_text.split("## Consequences")[1]))
        assert "exactly one future, separate" in cons

    def test_no_successor_authorization_is_created(self, decision_text):
        cons = _demphasize(_flat(decision_text.split("## Consequences")[1]))
        assert "authorizes no successor authorization" in cons
        assert (
            "no outcome of link 5 — including the cleanest possible one — authorizes any "
            "successor unit" in cons
        )

    def test_section_e_shows_the_regress_terminates(self, decision_text):
        e = _demphasize(_section(decision_text, "E."))
        assert "eleven steps and no twelfth" in e
        assert "five links and no sixth" in e
        assert "authorizes no successor authorization of any kind" in e


class TestXasset0040IsSpentAsAStop:
    def test_section_b_names_the_stop_and_its_evidence(self, decision_text):
        b = _demphasize(_section(decision_text, "B."))
        assert SPENT_STEP11_DETERMINATION in b
        assert SPENT_STEP11_EVIDENCE_COMMENT in b

    def test_section_b_records_the_grant_as_consumed_and_not_revived(self, decision_text):
        b = _demphasize(_section(decision_text, "B."))
        assert "Its single grant is therefore consumed by that exercise" in b
        assert "it is not revived here" in b
        assert (
            "This decision does not revive, reinterpret, extend, or re-open XASSET-0040." in b
        )

    def test_section_b_leaves_xasset_0040s_own_record_intact(self, decision_text):
        b = _demphasize(_section(decision_text, "B."))
        assert "XASSET-0040's file is not edited" in b
        assert "its status is not changed" in b

    def test_xasset_0040s_file_is_byte_identical_to_the_bound_merge(self):
        rel = (
            "governance/decisions/"
            "XASSET-0040-endpoint-0001-stage-1-step-11-activation-and-execution-authorization.md"
        )
        assert _blob_sha256_at(rel) == hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()

    @pytest.mark.parametrize("decision_id", sorted(WITHHOLDING_QUOTES))
    def test_each_withholding_quote_is_verbatim_in_the_live_predecessor(self, decision_id):
        path, quote = WITHHOLDING_QUOTES[decision_id]
        assert _flat(quote) in _flat(path.read_text()), decision_id

    def test_the_filing_counts_ten_withholding_filings(self, decision_text):
        e = _demphasize(_section(decision_text, "E."))
        assert "Ten decisions accepted" in e
        assert len(WITHHOLDING_QUOTES) == 10

    def test_the_dead_anchors_are_pinned_negatively(self, decision_text):
        """A silent reversion to XASSET-0040's own dead binding must FAIL, not pass unnoticed."""
        flat = _flat(decision_text)
        # The dead PR #337 bound merge and the dead ten-path boundary may be MENTIONED as history
        # in the Rationale, but must never appear as a binding condition in §G.
        g = _flat(_raw_section(decision_text, "G."))
        assert DEAD_MERGE_SHA not in g
        assert BOUND_MERGE_SHA in g
        assert f"{DEAD_LOAD_BEARING_COUNT} `LOAD_BEARING_RELPATHS`" not in g
        assert f"{EXPECTED_LOAD_BEARING_COUNT} `LOAD_BEARING_RELPATHS`" in g
        assert DEAD_STEP9_EVIDENCE_COMMENT not in flat
        assert DEAD_STEP10_EVIDENCE_COMMENT not in flat

    def test_the_dead_attestation_binding_is_not_reintroduced(self, decision_text):
        e1 = _flat(_subsection(decision_text, "E.1"))
        assert BOUND_AUTHORIZING_DECISION in e1
        assert str(BOUND_AUTHORIZING_PULL_REQUEST) in e1
        assert DEAD_AUTHORIZING_DECISION not in e1
        assert f"PR #{DEAD_AUTHORIZING_PULL_REQUEST}" not in e1


class TestTheCorrectionChainIsRecorded:
    def test_section_c_names_the_actual_defect_not_a_vague_one(self, decision_text):
        c = _demphasize(_section(decision_text, "C."))
        assert "governance-evidence gap on PR #337" in c
        assert "claude[bot]" in c
        assert "Mast3rkey" in c
        assert "PRINCIPAL_EXACT_HEAD_ACCEPTANCE" in c
        assert "POST_MERGE_VERIFICATION" in c

    def test_section_c_records_all_four_completed_links(self, decision_text):
        c = _demphasize(_section(decision_text, "C."))
        for token in (
            "XASSET-0042", "XASSET-0049", "XASSET-0050", "XASSET-0051",
            LINK3_PASS_DETERMINATION, LINK4_DETERMINATION,
        ):
            assert token in c, token

    def test_section_c_records_that_step_8_was_not_re_consumed(self, decision_text):
        c = _demphasize(_section(decision_text, "C."))
        assert "Step 8 was not re-consumed." in c
        assert "equivalent" in c

    def test_section_c_records_the_intervening_recovery_filings(self, decision_text):
        c = _demphasize(_section(decision_text, "C."))
        for token in ("XASSET-0045", "XASSET-0046", "XASSET-0047"):
            assert token in c, token
        assert "Neither performed, authorized, or advanced any part of links 3, 4, or 5" in c

    def test_section_c_does_not_rest_on_a_predecessors_summary_alone(self, decision_text):
        c = _demphasize(_section(decision_text, "C."))
        assert "is not asserted here on the strength of any prior filing's summary" in c


class TestTheLink4DeterminationIsIdentifiedAndConsumed:
    def test_the_link_4_comment_and_determination_are_named_exactly(self, decision_text):
        d = _demphasize(_section(decision_text, "D."))
        assert LINK4_DETERMINATION_COMMENT in d
        assert LINK4_DETERMINATION in d

    def test_the_link_4_evidence_is_pinned_by_author_date_and_edit_state(self, decision_text):
        d = _demphasize(_section(decision_text, "D."))
        assert "2026-08-23T18:09:48Z" in d
        assert "Mast3rkey" in d
        assert "never edited" in d
        assert "created_at == updated_at" in d
        assert "PR #352" in d

    def test_the_link_4_body_hash_is_pinned_with_its_normalization(self, decision_text):
        d = _flat(_raw_section(decision_text, "D."))
        assert (
            "898d82c75d27d9da81e7d41b1e4429101a6490bfaa8aabbc01db030d0ef57646" in d
        ), "the link-4 body hash must be pinned"
        assert "HTML-unescaped" in d, (
            "a hash without its normalization is unverifiable; the raw API body hashes "
            "differently"
        )

    def test_the_link_4_grant_is_recorded_as_spent(self, decision_text):
        d = _demphasize(_section(decision_text, "D."))
        assert "complete and consumed" in d
        assert "spent" in d

    def test_the_link_4_result_authorizes_nothing_further(self, decision_text):
        d = _demphasize(_flat_prose(_raw_section(decision_text, "D.")))
        assert "This result authorizes nothing further." in d
        assert "not permission to produce an attestation" in d
        assert "or to perform any part of link 5" in d

    def test_the_authority_comes_from_this_decisions_own_lifecycle(self, decision_text):
        d = _demphasize(_section(decision_text, "D."))
        assert (
            "the authority for link 5 comes from this decision's own lifecycle (§N) and from "
            "nowhere else" in d
        )

    def test_link_3_ordering_is_preserved_and_the_duplicate_stop_is_never_promoted(
        self, decision_text
    ):
        d = _demphasize(_section(decision_text, "D."))
        assert LINK3_PASS_COMMENT in d
        assert LINK3_DUPLICATE_STOP_COMMENT in d
        assert "NO PASS ISSUED" in d
        assert "is not an anchor" in d
        assert "does not invalidate, supersede, contradict, or weaken" in d
        # The valid PASS must be introduced BEFORE the duplicate stop, so a reader cannot take
        # the later comment as the operative determination.
        assert d.index(LINK3_PASS_COMMENT) < d.index(LINK3_DUPLICATE_STOP_COMMENT)

    def test_neither_link_3_nor_link_4_may_be_rerun_or_readjudicated(self, decision_text):
        d = _demphasize(_section(decision_text, "D."))
        assert "link 3 must not be rerun or re-adjudicated" in d
        assert "re-performs no part of either" in d
        assert "neither may be rerun without new authority" in d


class TestTheAttestationMechanismIsClosedAndUnchanged:
    def test_module_constants_are_exactly_the_bound_generation(self):
        """RE-ANCHORED BY XASSET-0060, and bound at BOTH ends rather than one.

        The lifecycle anchor lawfully moved onto the post-parser-correction rebinding. The values
        THIS unit bound are retained as NEGATIVE PINS -- still named, still asserted, now asserted
        as the values the anchor moved OFF -- and the successor's own values are pinned positively.
        Nothing is dropped: an unauthorized move to any third value fails both halves.
        """
        assert A.AUTHORIZING_DECISION == SUCCESSOR_DECISION_ID
        assert A.AUTHORIZING_DECISION != BOUND_AUTHORIZING_DECISION
        assert A.PRIOR_STEP8_EQUIVALENT_DECISION == BOUND_AUTHORIZING_DECISION
        assert A.AUTHORIZING_PULL_REQUEST != BOUND_AUTHORIZING_PULL_REQUEST
        assert A.PRIOR_STEP8_EQUIVALENT_PULL_REQUEST == BOUND_AUTHORIZING_PULL_REQUEST
        assert A.REVIEWED_BASE_SHA == SUCCESSOR_REVIEWED_BASE_SHA
        assert A.REVIEWED_BASE_SHA != BOUND_REVIEWED_BASE_SHA
        assert A.PRIOR_STEP8_EQUIVALENT_MERGE_BASE == BOUND_REVIEWED_BASE_SHA
        assert A.EXECUTION_ATTEMPT_ID == ATTEMPT_ID
        assert A.REQUIRED_LIFECYCLE_GATES == EXPECTED_LIFECYCLE_GATES
        assert len(A.REQUIRED_LIFECYCLE_GATES) == 6

    def test_the_decision_never_names_itself_as_an_authorizing_constant(self):
        source = (ROOT / "level1_stage1_execution_authorization.py").read_text()
        assert DECISION_ID not in source
        assert str(PR_SENTINEL) not in source

    def test_e1_forbids_inserting_this_decision_into_the_mechanism(self, decision_text):
        e1 = _demphasize(_subsection(decision_text, "E.1"))
        assert "XASSET-0052 must not be inserted into that mechanism." in e1
        assert "closed" in e1
        assert "load-bearing path #1" in e1
        assert "require its own separate correction" in e1
        assert "rebinding, and renewed readiness and drift lifecycle" in e1

    def test_e1_records_reviewed_base_sha_as_a_rebinding_base_not_a_moving_field(
        self, decision_text
    ):
        e1 = _demphasize(_subsection(decision_text, "E.1"))
        assert "is the lawful rebinding base" in e1
        assert 'not a "current main" field that advances with every merge' in e1
        assert "it does not move because this decision merges" in e1

    def test_load_bearing_relpaths_are_eighteen_unique_and_unchanged(self):
        """RE-ANCHORED BY XASSET-0060. The eighteen this unit bound are still all eighteen, in
        order, unique, and none traded away -- now proved against the AST-derived historical set
        rather than against a live count a later authorized addition would move."""
        _assert_boundary_is_the_bound_set_plus_authorized_additions()

    def test_the_relpath_tuple_is_derivable_from_the_bound_merge_by_ast(self):
        """The list must be DERIVED from the bound tree, not read from a restated constant."""
        source = subprocess.run(
            ["git", "show", f"{BOUND_MERGE_SHA}:level1_stage1_execution_authorization.py"],
            cwd=ROOT, capture_output=True, check=True, text=True,
        ).stdout
        tree = ast.parse(source)
        consts: dict[str, str] = {}
        derived: tuple[str, ...] | None = None

        def _literal(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                return node.value
            if isinstance(node, ast.Name) and node.id in consts:
                return consts[node.id]
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                left, right = _literal(node.left), _literal(node.right)
                if left is not None and right is not None:
                    return left + right
            if isinstance(node, ast.JoinedStr):
                return None
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
                    derived = tuple(items)

        assert derived is not None, "LOAD_BEARING_RELPATHS not derivable by AST"
        assert len(derived) == EXPECTED_LOAD_BEARING_COUNT
        # RE-ANCHORED BY XASSET-0060: the derived historical tuple must still be exactly what the
        # live tuple STARTS with. Equality against the live tuple would have forbidden any future
        # authorized addition; the prefix form forbids removal, reordering and substitution, which
        # is what this test was actually protecting.
        assert derived == HISTORICAL_LOAD_BEARING
        assert tuple(A.LOAD_BEARING_RELPATHS)[:EXPECTED_LOAD_BEARING_COUNT] == derived
        _assert_boundary_is_the_bound_set_plus_authorized_additions()

    @pytest.mark.parametrize("relpath", sorted(OUTCOME_CAPABLE_MODULE_WITNESS))
    def test_each_outcome_capable_module_matches_its_derived_bound_identity(self, relpath):
        derived = _blob_sha256_at(relpath)
        assert derived == OUTCOME_CAPABLE_MODULE_WITNESS[relpath], relpath
        # RE-ANCHORED BY XASSET-0056, the single replacement parser-correction implementation
        # XASSET-0055 §H authorized. That correction lawfully changes exactly ONE load-bearing
        # path -- the authorization module itself, LOAD_BEARING_RELPATHS[0] -- so its bound
        # digest is stale BY DESIGN: it is the fail-closed hand-off to a later, separately
        # authorized step-8-equivalent rebinding unit. This is NOT a blanket exemption, which
        # would hide any future unauthorized edit to the most sensitive path; the module is
        # pinned to be DIFFERENT, which is strictly binding. Every OTHER path must still match
        # the bound merge exactly, and does.
        live = hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest()
        if relpath == "level1_stage1_execution_authorization.py":
            assert live != derived, relpath
        else:
            assert live == derived, relpath

    def test_the_five_outcome_capable_modules_are_named_in_the_binding_section(
        self, decision_text
    ):
        g = _flat(_raw_section(decision_text, "G."))
        for relpath in OUTCOME_CAPABLE_MODULE_WITNESS:
            assert relpath in g, relpath


class TestNoProtectedPathIsTouched:
    @pytest.mark.parametrize("relpath", list(HISTORICAL_LOAD_BEARING))
    def test_each_load_bearing_path_is_byte_identical_to_the_bound_merge(self, relpath):
        # RE-ANCHORED BY XASSET-0056, the single replacement parser-correction implementation
        # XASSET-0055 §H authorized. That correction lawfully changes exactly ONE load-bearing
        # path -- the authorization module itself, LOAD_BEARING_RELPATHS[0] -- so its bound
        # digest is stale BY DESIGN: it is the fail-closed hand-off to a later, separately
        # authorized step-8-equivalent rebinding unit. This is NOT a blanket exemption, which
        # would hide any future unauthorized edit to the most sensitive path; the module is
        # pinned to be DIFFERENT, which is strictly binding. Every OTHER path must still match
        # the bound merge exactly, and does.
        #
        # RE-ANCHORED AGAIN BY XASSET-0060. The parametrisation now runs over the HISTORICAL set
        # this unit actually bound, derived by AST from the immutable bound merge, rather than over
        # the live tuple. The seven paths XASSET-0060 lawfully ADDED did not exist in this merge at
        # all, so asking whether they are "byte-identical to the bound merge" was not a weaker
        # question -- it was an unanswerable one, and it failed for a reason that had nothing to do
        # with drift. Their identity is bound by XASSET-0060's own suite. Coverage of the eighteen
        # is unchanged, and the module is still pinned to be DIFFERENT rather than exempted.
        live = hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest()
        bound = _blob_sha256_at(relpath)
        if relpath == "level1_stage1_execution_authorization.py":
            assert live != bound, relpath
        else:
            assert live == bound, relpath

    @pytest.mark.parametrize("relpath", PORTFOLIO_RELPATHS)
    def test_each_portfolio_path_is_byte_identical_to_the_bound_merge(self, relpath):
        assert (
            hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest()
            == _blob_sha256_at(relpath)
        ), relpath

    def test_the_protected_comparison_is_not_vacuous(self):
        """A positive control: a commit pair across which a protected path GENUINELY changed.

        Without it, the byte-identity assertions above could pass because the comparison itself
        is broken rather than because nothing moved.
        """
        before = "9c8647f9dddacdf63825f569097214ba65299fe8"
        after = "5fbfc94d7333e552bd2654261e0c57134a172e31"
        rel = "level1_stage1_execution_authorization.py"
        assert _blob_sha256_at(rel, before) != _blob_sha256_at(rel, after)

    @pytest.mark.parametrize("relpath,expected", sorted(CANONICAL_PINS.items()))
    def test_each_canonical_pin_matches_its_file_and_the_module(self, relpath, expected):
        assert hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest() == expected
        assert A.CANONICAL_PINS[relpath] == expected

    def test_the_frozen_universe_is_unchanged(self):
        assert A.CONSTRUCTION_UNIVERSE_SHA256 == UNIVERSE_SHA
        universe = CU.frozen_construction_universe()
        assert len(universe) == CONSTRUCTION_COUNT
        assert len({row["cell_id"] for row in universe.values()}) == CELL_COUNT
        assert CU.universe_aggregate_sha256() == UNIVERSE_SHA


class TestExactBindingConditionsAreConjunctive:
    def test_section_g_requires_live_re_resolution_over_any_summary(self, decision_text):
        g = _demphasize(_section(decision_text, "G."))
        assert "immediately before it acts" in g
        assert "never against a summary carried forward from an earlier moment" in g
        assert "the derived value governs" in g
        assert "the disagreement is itself a stop" in g

    def test_section_g_is_explicitly_conjunctive(self, decision_text):
        g = _demphasize(_section(decision_text, "G."))
        assert "These are conjunctive" in g
        assert "failure or uncertainty on any one is a stop" in g

    def test_section_g_binds_all_nine_conditions(self, decision_text):
        g = _flat(_raw_section(decision_text, "G."))
        for n in range(1, 10):
            assert f"{n}. **" in g or f"{n}. " in g, n
        for token in (
            BOUND_MERGE_SHA, BOUND_MERGE_PARENT_1, BOUND_MERGE_PARENT_2, BOUND_MERGE_TREE,
            LINK3_PASS_COMMENT, LINK4_DETERMINATION_COMMENT, UNIVERSE_SHA,
            str(CONSTRUCTION_COUNT), str(CELL_COUNT),
        ):
            assert token in g, token
        for relpath, pin in CANONICAL_PINS.items():
            assert pin in g, relpath

    def test_section_g_forbids_a_third_parent_on_the_bound_merge(self, decision_text):
        g = _demphasize(_section(decision_text, "G."))
        assert "no third parent" in g.lower()

    def test_section_g_requires_the_path_list_to_be_derived_not_restated(self, decision_text):
        g = _demphasize(_section(decision_text, "G."))
        assert "must be derived from the module as it exists in the bound merge tree" in g
        assert "never read from a constant restated in a decision record" in g

    def test_section_g_requires_both_determinations_read_from_the_live_comment(
        self, decision_text
    ):
        g = _demphasize(_section(decision_text, "G."))
        assert "read independently from the live comment" in g
        assert "This decision is context, not evidence." in g

    def test_section_g_requires_the_mechanism_on_top_not_instead(self, decision_text):
        g = _demphasize(_section(decision_text, "G."))
        assert (
            "the unit's own pre-attestation verification is required on top of it, not instead "
            "of it" in g
        )


class TestTheInterveningCommitRule:
    def test_g1_names_the_link_4_observation_head_as_the_first_parent(self, decision_text):
        g1 = _demphasize(_subsection(decision_text, "G.1"))
        assert LINK4_OBSERVATION_HEAD in g1
        assert "exactly two ordered parents" in g1
        assert "No third parent." in g1

    def test_g1_forbids_predicting_the_merge_identity(self, decision_text):
        g1 = _demphasize(_subsection(decision_text, "G.1"))
        assert "must be derived after the normal merge, never predicted in this filing" in g1
        assert "No merge SHA for this decision appears anywhere in this text" in g1
        assert "none may be invented, pre-computed, or asserted before GitHub records it" in g1

    def test_no_merge_sha_for_this_decision_is_actually_present(self, decision_text):
        """The rule is only worth anything if the filing itself obeys it.

        Every 40-hex token in the file must be one of the identities preflight verified live.
        A new, unexplained commit-shaped token would be exactly the predicted merge SHA §G.1
        forbids.
        """
        known = {
            BOUND_MERGE_SHA, BOUND_MERGE_PARENT_1, BOUND_MERGE_PARENT_2, BOUND_MERGE_TREE,
            LINK4_OBSERVATION_HEAD, XASSET0051_ACCEPTED_HEAD, XASSET0051_BASE,
            DEAD_MERGE_SHA, UNIVERSE_SHA,
            *CANONICAL_PINS.values(),
            *OUTCOME_CAPABLE_MODULE_WITNESS.values(),
            "e0ee2d4c25066cdc3d1c936015c3ada62bed74e8",
            "898d82c75d27d9da81e7d41b1e4429101a6490bfaa8aabbc01db030d0ef57646",
        }
        found = set(re.findall(r"\b[0-9a-f]{40}\b", decision_text))
        found |= set(re.findall(r"\b[0-9a-f]{64}\b", decision_text))
        unexpected = found - known
        assert not unexpected, f"unexplained commit-shaped identities: {sorted(unexpected)}"

    def test_g1_refuses_descendant_ancestry_as_sufficient(self, decision_text):
        g1 = _demphasize(_subsection(decision_text, "G.1"))
        assert "not a descendant of it" in g1
        assert "Descendant ancestry is not sufficient" in g1
        assert (
            'may not treat "the merge is an ancestor" as satisfying this condition' in g1
        )

    def test_g1_requires_the_merge_tree_to_equal_the_accepted_head_tree(self, decision_text):
        g1 = _demphasize(_subsection(decision_text, "G.1"))
        assert "The merge tree equals the accepted head's own tree" in g1
        assert "zero drift at merge" in g1

    def test_g1_requires_no_load_bearing_or_protected_byte_changed(self, decision_text):
        g1 = _demphasize(_subsection(decision_text, "G.1"))
        assert "No load-bearing or protected production byte changed" in g1
        assert str(EXPECTED_LOAD_BEARING_COUNT) in g1
        for relpath in PORTFOLIO_RELPATHS:
            assert relpath in g1, relpath

    def test_g1_makes_any_extra_member_of_the_exact_range_a_stop(self, decision_text):
        """CORRECTED after review 5003284327 MAJOR 1 — the quantifier is the RANGE, not reachability."""
        g1 = _demphasize(_subsection(decision_text, "G.1"))
        assert (
            "Any commit inside the exact range above that is not one of its two admitted classes "
            "is a stop." in g1
        )
        assert "fail closed and stop" in g1
        for member in (
            "an additional feature commit",
            "an unexpected first-parent",
            "a third parent on the merge",
            "any commit after the merge",
            "any other extra member of the exact post-checkpoint range",
        ):
            assert member in g1, member

    def test_g1_excludes_pre_checkpoint_ancestors_from_the_governed_set(self, decision_text):
        """The heart of MAJOR 1: history below the checkpoint must NOT be an intervening commit."""
        g1 = _demphasize(_subsection(decision_text, "G.1"))
        assert (
            "Historical ancestors already reachable from the observation checkpoint are not "
            "intervening commits and must not be treated as such." in g1
        )
        assert "a merge reaches its entire ancestry" in g1
        assert "unsatisfiable" in g1

    def test_g1_states_the_range_equality_explicitly(self, decision_text):
        g1 = _subsection(decision_text, "G.1")
        assert "commits(observation_head..acting_head)" in g1
        assert "commits(observation_head..accepted_head)" in g1
        assert "the one exact lifecycle-closing merge" in g1
        assert "with **no additional member**" in g1

    def test_g1_forbids_a_later_commit_after_the_merge(self, decision_text):
        g1 = _demphasize(_subsection(decision_text, "G.1"))
        assert "No later commit follows the merge." in g1

    def test_g1_no_longer_quantifies_over_global_reachability(self, decision_text):
        """The reviewed-head defect, encoded so it cannot return."""
        g1 = _demphasize(_subsection(decision_text, "G.1")).lower()
        assert "any commit reachable from the acting head" not in g1

    def test_g1_admits_an_exception_only_when_separately_authorized_and_admitted(
        self, decision_text
    ):
        g1 = _demphasize(_subsection(decision_text, "G.1"))
        assert "separately authorized by its own accepted governance decision" in g1
        assert "expressly admitted by governed text" in g1
        assert "Discovery of such a commit is not admission of it" in g1
        assert "may not admit one on its own judgment" in g1

    def test_g1_explains_why_exact_identity_rather_than_ancestry(self, decision_text):
        g1 = _demphasize(_subsection(decision_text, "G.1"))
        assert "verified-clean checkpoint at one exact commit" in g1
        assert "unreviewed history" in g1


class TestTheCommitRangeRuleIsSemanticallyCorrect:
    """ADDED after review 5003284327 MAJOR 1 — a SET MODEL, not another substring assertion.

    The reviewed head said "any commit **reachable** from the acting head" other than three named
    identities is a stop. A merge reaches its entire ancestry, so a perfectly formed merge produced
    211 "stop" commits against this repository's own history and the authorized unit was
    UNSATISFIABLE. Substring guards could not see that, because the words were all present and
    correct-sounding.

    These tests therefore model the commit sets directly. ``_range`` is a deliberately tiny,
    self-contained reimplementation of ``git rev-list A..B`` over a synthetic parent map, so the
    model exercises the RULE rather than git. ``_reviewed_head_rule`` reimplements the DEFECT, and
    a test proves it fails on the clean graph -- if a future edit reintroduced global reachability,
    that test would start passing and the correct-rule tests would start failing.
    """

    #: A synthetic graph shaped exactly like the real one: a long pre-checkpoint history, an
    #: observation checkpoint, this PR's own commits, and one lifecycle-closing merge.
    OLD = ["h0", "h1", "h2", "h3"]          # historical ancestors BELOW the checkpoint
    OBS = "obs"                             # the observation checkpoint (8def8bd0... in reality)
    PR = ["c1", "c2"]                       # commits introduced by the accepted head
    ACC = "c2"                              # the final accepted head
    MERGE = "m"                             # the lifecycle-closing merge

    @classmethod
    def _clean_parents(cls) -> dict[str, list[str]]:
        parents: dict[str, list[str]] = {"h0": []}
        for prev, cur in zip(cls.OLD, cls.OLD[1:]):
            parents[cur] = [prev]
        parents[cls.OBS] = [cls.OLD[-1]]
        parents["c1"] = [cls.OBS]
        parents["c2"] = ["c1"]
        parents[cls.MERGE] = [cls.OBS, cls.ACC]   # first parent obs, second parent accepted head
        return parents

    @staticmethod
    def _reachable(parents: dict[str, list[str]], tip: str) -> set[str]:
        seen, stack = set(), [tip]
        while stack:
            c = stack.pop()
            if c in seen:
                continue
            seen.add(c)
            stack.extend(parents.get(c, []))
        return seen

    @classmethod
    def _range(cls, parents: dict[str, list[str]], excl: str, incl: str) -> set[str]:
        """``git rev-list excl..incl`` — reachable from ``incl`` but not from ``excl``."""
        return cls._reachable(parents, incl) - cls._reachable(parents, excl)

    # ---- the two rules, side by side ---------------------------------------------------------

    @classmethod
    def _corrected_rule(cls, parents, acting, accepted, obs, merge) -> bool:
        """The §G.1 rule as corrected. True == the unit may proceed."""
        # 1. acting head IS the merge (never merely a descendant)
        if acting != merge:
            return False
        # 2. exactly two ordered parents, first obs, second accepted, no third
        if parents.get(merge) != [obs, accepted]:
            return False
        # 5. the exact post-checkpoint range equality
        expected = cls._range(parents, obs, accepted) | {merge}
        if cls._range(parents, obs, acting) != expected:
            return False
        # 6. no later commit follows the merge
        later = {c for c, ps in parents.items() if merge in ps}
        return not later

    @classmethod
    def _reviewed_head_rule(cls, parents, acting, accepted, obs, merge) -> bool:
        """The DEFECT: quantify over everything reachable from the acting head."""
        allowed = {obs, accepted, merge}
        return not (cls._reachable(parents, acting) - allowed)

    # ---- what the corrected rule must permit --------------------------------------------------

    def test_historical_ancestors_below_the_checkpoint_are_permitted(self):
        parents = self._clean_parents()
        assert self._corrected_rule(parents, self.MERGE, self.ACC, self.OBS, self.MERGE)
        # and they really are present, so this is not vacuous
        assert set(self.OLD) <= self._reachable(parents, self.MERGE)
        assert not (set(self.OLD) & self._range(parents, self.OBS, self.MERGE))

    def test_the_accepted_head_commits_plus_the_exact_merge_are_permitted(self):
        parents = self._clean_parents()
        governed = self._range(parents, self.OBS, self.MERGE)
        assert governed == {"c1", "c2", self.MERGE}
        assert self._corrected_rule(parents, self.MERGE, self.ACC, self.OBS, self.MERGE)

    # ---- what it must refuse -------------------------------------------------------------------

    @classmethod
    def _range_check_only(cls, parents, acting, accepted, obs, merge) -> bool:
        """Condition 5 alone, with the parent checks removed.

        Stated honestly: for a two-parent merge whose parents are exactly ``[obs, accepted]``, the
        range equality is IMPLIED by conditions 1 and 2 — it is defence in depth there, not an
        independent constraint. It becomes independent exactly where those conditions are the ones
        under attack: an unexpected first parent, an extra parent, or an acting head that is not
        the merge. This helper isolates it so those cases prove the range rule catches them on its
        own, rather than riding on a check that a future edit might weaken.
        """
        expected = cls._range(parents, obs, accepted) | {merge}
        return cls._range(parents, obs, acting) == expected

    def test_one_unexpected_commit_between_observation_and_merge_is_refused(self):
        """`main` advanced by one commit after the checkpoint, and the merge took it in.

        Both the first-parent check and the range check must refuse this, and the range check must
        refuse it *independently* — that is what makes it a real second line of defence.
        """
        parents = self._clean_parents()
        parents["rogue"] = [self.OBS]                    # an unexpected main commit
        parents[self.MERGE] = ["rogue", self.ACC]        # the merge takes it as first parent
        governed = self._range(parents, self.OBS, self.MERGE)
        assert "rogue" in governed, "the model must actually contain the extra commit"
        assert governed != self._range(parents, self.OBS, self.ACC) | {self.MERGE}
        assert not self._corrected_rule(parents, self.MERGE, self.ACC, self.OBS, self.MERGE)
        assert not self._range_check_only(parents, self.MERGE, self.ACC, self.OBS, self.MERGE)

    def test_the_range_check_refuses_a_later_descendant_on_its_own(self):
        """The range check, isolated, also catches an acting head that is not the merge."""
        parents = self._clean_parents()
        parents["later"] = [self.MERGE]
        assert not self._range_check_only(parents, "later", self.ACC, self.OBS, self.MERGE)

    def test_the_range_check_is_defence_in_depth_for_a_well_formed_two_parent_merge(self):
        """Disclosed rather than overclaimed: on the clean graph the range equality follows from
        conditions 1 and 2, so it adds nothing there. It is retained because it is exactly what
        catches the malformed cases above, and because it is the wording that replaced the
        unsatisfiable global-reachability quantifier."""
        parents = self._clean_parents()
        assert self._range_check_only(parents, self.MERGE, self.ACC, self.OBS, self.MERGE)
        assert self._corrected_rule(parents, self.MERGE, self.ACC, self.OBS, self.MERGE)

    def test_one_later_descendant_after_the_merge_is_refused(self):
        parents = self._clean_parents()
        parents["later"] = [self.MERGE]
        assert not self._corrected_rule(parents, "later", self.ACC, self.OBS, self.MERGE)
        # and even acting AT the merge is refused once a later commit exists
        assert not self._corrected_rule(parents, self.MERGE, self.ACC, self.OBS, self.MERGE)

    def test_a_third_parent_is_refused(self):
        parents = self._clean_parents()
        parents["extra"] = [self.OBS]
        parents[self.MERGE] = [self.OBS, self.ACC, "extra"]
        assert not self._corrected_rule(parents, self.MERGE, self.ACC, self.OBS, self.MERGE)

    def test_an_unexpected_first_parent_is_refused(self):
        parents = self._clean_parents()
        parents[self.MERGE] = [self.OLD[-1], self.ACC]   # first parent is NOT the checkpoint
        assert not self._corrected_rule(parents, self.MERGE, self.ACC, self.OBS, self.MERGE)

    def test_mere_ancestry_is_refused(self):
        parents = self._clean_parents()
        parents["tip"] = [self.MERGE]
        assert self.MERGE in self._reachable(parents, "tip")   # the merge IS an ancestor
        assert not self._corrected_rule(parents, "tip", self.ACC, self.OBS, self.MERGE)

    # ---- the defect itself -----------------------------------------------------------------------

    def test_the_reviewed_head_global_reachability_rule_fails_the_clean_model(self):
        """The MAJOR-1 defect, reproduced in the model: the clean case is refused."""
        parents = self._clean_parents()
        assert self._corrected_rule(parents, self.MERGE, self.ACC, self.OBS, self.MERGE)
        assert not self._reviewed_head_rule(parents, self.MERGE, self.ACC, self.OBS, self.MERGE)
        offenders = self._reachable(parents, self.MERGE) - {self.OBS, self.ACC, self.MERGE}
        assert offenders, "the model must actually contain pre-checkpoint history"
        assert set(self.OLD) <= offenders

    def test_the_model_matches_this_repositorys_real_shape(self):
        """Non-vacuity: the synthetic graph must mirror the real defect, not a toy that cannot.

        Built against the REAL object store with ``commit-tree``, which updates no ref. This is
        read-only with respect to every branch, tag and tracked file.
        """
        obs = LINK4_OBSERVATION_HEAD
        acc = _git("rev-parse", "HEAD")
        merge = _git_with_identity(
            "commit-tree", _git("rev-parse", f"{acc}^{{tree}}"),
            "-p", obs, "-p", acc, "-m", "test-only synthetic merge; no ref updated",
        )
        reachable = set(_git("rev-list", merge).split())
        governed = set(_git("rev-list", f"{obs}..{merge}").split())
        expected = set(_git("rev-list", f"{obs}..{acc}").split()) | {merge}
        # the corrected rule is satisfied ...
        assert governed == expected
        # ... while the reviewed-head rule would call hundreds of real commits a stop
        assert len(reachable - {obs, acc, merge}) > 100

    def test_the_real_shape_probe_does_not_depend_on_ambient_git_identity(self):
        """REGRESSION for CI run 32667212952 attempt 3.

        The probe above first shipped calling plain ``_git("commit-tree", ...)``. It passed here,
        where this development environment happens to carry a configured ``user.email``, and failed
        in CI with exit 128 -- ``actions/checkout`` configures no committer identity, and
        ``commit-tree`` refuses to run without one. A test whose result depends on ambient git
        configuration is not a test of this repository, so the call is pinned to the explicit-identity
        helper by AST rather than by hope.
        """
        tree = ast.parse(Path(__file__).read_text())
        fn = next(
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef)
            and n.name == "test_the_model_matches_this_repositorys_real_shape"
        )
        callees = {
            c.func.id for c in ast.walk(fn)
            if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
        }
        assert "_git_with_identity" in callees
        # and the bare helper must not be the one carrying commit-tree
        commit_tree_calls = [
            c for c in ast.walk(fn)
            if isinstance(c, ast.Call)
            and any(
                isinstance(a, ast.Constant) and a.value == "commit-tree" for a in c.args
            )
        ]
        assert commit_tree_calls, "the probe must still exercise commit-tree against the real store"
        for call in commit_tree_calls:
            assert isinstance(call.func, ast.Name)
            assert call.func.id == "_git_with_identity"

    def test_the_supplied_identity_covers_both_author_and_committer(self):
        """``commit-tree`` needs BOTH identities; supplying only one still exits 128."""
        assert set(_SYNTHETIC_COMMIT_IDENTITY) == {
            "GIT_AUTHOR_NAME",
            "GIT_AUTHOR_EMAIL",
            "GIT_COMMITTER_NAME",
            "GIT_COMMITTER_EMAIL",
        }
        assert all(v for v in _SYNTHETIC_COMMIT_IDENTITY.values())

    def test_the_identity_is_supplied_by_environment_and_mutates_no_git_config(self):
        """The helper must not reach for ``git config``, which would edit the checkout."""
        source = inspect.getsource(_git_with_identity)
        assert "env=" in source
        assert "config" not in source


class TestTheCanonicalRunnerArtifactException:
    """ADDED after review 5003284327 MAJOR 3.

    §H's opening bullet said the unit must not "edit any repository byte", with no qualifier. §I.7
    and §M REQUIRE the accepted runner to create
    ``research/level1_endpoint_evidence/stage1_results.yaml``. An executor applying the strictest
    applicable rule had to refuse, making terminal outcome §K.4 ``COMPLETED`` structurally
    unreachable. §H.1 now carries one exact-identity exception, and these tests pin both halves.
    """

    ARTIFACT = "research/level1_endpoint_evidence/stage1_results.yaml"

    def test_the_absolute_edit_any_repository_byte_wording_is_gone(self, decision_text):
        """The reviewed-head defect, encoded so it cannot return."""
        h = _demphasize(_section(decision_text, "H.")).lower()
        assert "edit any repository byte" not in h

    def test_the_prohibition_is_narrowed_to_pre_existing_tracked_bytes(self, withheld):
        joined = " ".join(_demphasize(b) for b in withheld)
        assert "modify any pre-existing tracked repository byte" in joined
        assert "make any committed repository mutation" in joined

    def test_creating_the_exact_canonical_artifact_is_permitted(self, decision_text):
        h1 = _demphasize(_subsection(decision_text, "H.1"))
        assert self.ARTIFACT in h1
        assert "may create exactly one file" in h1
        assert "isolated operational working tree" in h1
        assert "canonical output of the single authorized run" in h1

    def test_creating_it_before_the_claim_is_forbidden(self, decision_text):
        h1 = _demphasize(_subsection(decision_text, "H.1"))
        assert "Creation only after the lawful claim." in h1
        assert "may not exist, and may not be written, before" in h1
        assert "Creating it before the claim is a stop" in h1

    def test_editing_or_replacing_it_after_creation_is_forbidden(self, decision_text):
        h1 = _demphasize(_subsection(decision_text, "H.1"))
        assert "After creation it is immutable to this unit." in h1
        for banned in ("edited", "rewritten", "replaced", "regenerated", "interpreted"):
            assert banned in h1, banned

    def test_committing_or_delivering_it_is_forbidden(self, decision_text, withheld):
        h1 = _demphasize(_subsection(decision_text, "H.1"))
        assert "It stays uncommitted and undelivered." in h1
        joined = " ".join(_demphasize(b) for b in withheld)
        assert "edit, rewrite, replace, interpret, commit, or deliver" in joined
        assert "P.1's" in joined or "§P.1" in _section(decision_text, "H.")

    def test_creating_any_other_file_is_forbidden(self, decision_text, withheld):
        h1 = _demphasize(_subsection(decision_text, "H.1"))
        assert "No other file creation or mutation of any kind is permitted" in h1
        assert "extends to exactly one path and no other" in h1
        joined = " ".join(_demphasize(b) for b in withheld)
        assert "create any repository file other than" in joined

    def test_the_exception_is_bound_at_completion(self, decision_text):
        h1 = _demphasize(_subsection(decision_text, "H.1"))
        assert "Its exact identity is bound during completion" in h1

    def test_the_exception_is_the_only_working_tree_write(self, decision_text):
        h1 = _demphasize(_subsection(decision_text, "H.1"))
        assert (
            "This exception is the only respect in which the unit may write inside a repository "
            "working tree." in h1
        )

    def test_i7_m_and_k4_name_the_exception_so_they_cannot_drift_apart(self, decision_text):
        i = _demphasize(_section(decision_text, "I."))
        m = _demphasize(_section(decision_text, "M."))
        k = _demphasize(_section(decision_text, "K."))
        assert self.ARTIFACT in i and "§H.1" in _section(decision_text, "I.")
        assert self.ARTIFACT in m and "§H.1" in _section(decision_text, "M.")
        assert "created under §H.1" in _section(decision_text, "K.")
        assert "only after the lawful claim" in i

    def test_no_artifact_exists_in_this_repository_now(self):
        """This filing creates nothing: the exception is text, not an act."""
        assert not (ROOT / self.ARTIFACT).exists()
        assert [] == [p for p in ROOT.rglob("stage1_results*") if ".git" not in p.parts]


class TestTheGrantedSequenceEndsAtItemSeven:
    def test_section_i_lists_nine_numbered_permissions(self, decision_text):
        i = _flat(_raw_section(decision_text, "I."))
        for n in range(1, 10):
            assert f"{n}. **" in i, n

    def test_the_authority_ends_at_item_7(self, decision_text):
        i = _demphasize(_section(decision_text, "I."))
        assert "that authority ends at item 7" in i
        assert "no further attestation" in i
        assert "no further claim" in i
        assert "no further lane transition" in i

    def test_items_8_and_9_are_duties_that_do_not_extend_the_sequence(self, decision_text):
        i = _demphasize(_section(decision_text, "I."))
        assert "Items 8 and 9 are duties, not further steps." in i
        assert "do not extend the execution sequence" in i
        assert "do not move the lane" in i
        assert "authorize no successor work of any kind" in i
        assert "Discharging them is how the unit ends, never how it continues." in i

    def test_the_unit_runs_the_frozen_universe_exactly_once(self, decision_text):
        i = _demphasize(_section(decision_text, "I."))
        assert "Execute exactly the frozen 680-construction universe, once" in i

    def test_the_claim_is_atomic_and_immediately_before_the_first_gate_evaluation(
        self, decision_text
    ):
        i = _demphasize(_section(decision_text, "I."))
        assert "atomically and immediately before the first real gate evaluation" in i


class TestTheRequiredLaneTransitionOrder:
    def test_i1_states_the_exact_order(self, decision_text):
        i1 = _subsection(decision_text, "I.1")
        assert "ABSENT ──▶ READY ──▶ CLAIMED ──▶ COMPLETED" in i1

    def test_i1_forbids_skipping_reordering_repeating_or_re_entering(self, decision_text):
        i1 = _demphasize(_subsection(decision_text, "I.1"))
        assert (
            "No step may be skipped, reordered, repeated, or entered from any other state." in i1
        )
        assert "only forwards" in i1

    def test_i1_derives_completion_rather_than_assuming_it(self, decision_text):
        i1 = _demphasize(_subsection(decision_text, "I.1"))
        assert "is derived, not assumed" in i1
        assert "governed recovery" in i1
        assert "not an extension of it" in i1

    def test_the_four_lane_states_appear_in_order_in_the_prose(self, decision_text):
        i1 = _subsection(decision_text, "I.1")
        idx = [i1.index(s) for s in ("`ABSENT`", "`READY`", "`CLAIMED`", "`COMPLETED`")]
        assert idx == sorted(idx)


class TestFailClosedNoRepairNoRebindingNoRetry:
    def test_section_j_enumerates_the_stop_triggers(self, decision_text):
        j = _demphasize(_section(decision_text, "J."))
        for trigger in (
            "drift", "missing evidence", "unexpected state", "authentication failure",
            "stale identity", "ambiguous actor evidence", "continuity gap", "lane mismatch",
            "validation failure",
        ):
            assert trigger in j, trigger

    def test_section_j_requires_stop_report_change_nothing(self, decision_text):
        j = _demphasize(_section(decision_text, "J."))
        assert "stop" in j and "report" in j
        assert "change nothing further" in j
        assert "§H is not relaxed by the discovery of a defect" in j

    def test_uncertainty_is_failure(self, decision_text):
        j = _demphasize(_section(decision_text, "J."))
        assert "Uncertainty is failure." in j
        assert "may not resolve an ambiguous state in favour of proceeding" in j

    def test_the_unit_is_an_executor_never_a_remediator(self, decision_text):
        j = _demphasize(_section(decision_text, "J."))
        assert "executor under exact conditions, never a remediator" in j
        assert "Finding the work is not authority to do the work." in j

    def test_remediation_requires_separately_authorized_things(self, decision_text):
        j = _demphasize(_section(decision_text, "J."))
        for token in ("correction", "rebinding", "renewed readiness", "governed recovery"):
            assert token in j, token
        assert "None of those is authorized by this decision" in j

    def test_j1_closes_both_gaps(self, decision_text):
        j1 = _demphasize(_subsection(decision_text, "J.1"))
        assert "No unverified interval may separate the attestation from the claim." in j1
        assert "must close in full before the unit may begin" in j1
        assert "immediately before it acts" in j1


class TestTerminalOutcomes:
    @pytest.mark.parametrize(
        "outcome",
        [
            "STOPPED_BEFORE_ATTESTATION",
            "STOPPED_AFTER_ATTESTATION_BEFORE_CLAIM",
            "STOPPED_AFTER_CLAIM",
            "COMPLETED",
        ],
    )
    def test_each_terminal_outcome_is_named_exactly(self, decision_text, outcome):
        k = _section(decision_text, "K.")
        assert f"`{outcome}`" in k, outcome

    def test_the_four_outcomes_are_exhaustive_and_terminal(self, decision_text):
        k = _demphasize(_section(decision_text, "K."))
        assert "in exactly these four ways" in k
        assert "Each is terminal; none is a pause." in k

    def test_every_stop_forbids_retry_and_recovery(self, decision_text):
        k = _demphasize(_section(decision_text, "K."))
        assert "no retry" in k
        assert "no replacement attestation" in k
        assert "no second claim" in k
        for token in ("no reset", "no deletion", "no recovery", "no repair", "no rebinding",
                      "no continuation"):
            assert token in k, token
        assert "any recovery requires new authority" in k
        assert "Durable evidence must be posted" in k

    def test_a_post_claim_stop_records_the_attempt_as_consumed(self, decision_text):
        k = _demphasize(_section(decision_text, "K."))
        assert "ATTEMPT_1 is consumed" in k

    def test_no_outcome_authorizes_a_successor(self, decision_text):
        k = _demphasize(_section(decision_text, "K."))
        assert "the unit's next act is to report and stop" in k
        assert "authorizes any successor unit" in k


class TestNoRetryNoRecovery:
    def test_section_l_binds_the_one_shot_attempt_identity(self, decision_text):
        ell = _demphasize(_section(decision_text, "L."))
        assert ATTEMPT_ID in ell
        assert "spent by the first lawful claim" in ell
        assert "does not authorize a second attempt" in ell
        assert "not a retry" in ell

    def test_section_l_preserves_the_disclosed_durability_boundary(self, decision_text):
        ell = _demphasize(_section(decision_text, "L."))
        assert "outside any filesystem-based enforcement boundary" in ell
        assert "Reconstructing a lane that was destroyed is not authorized here." in ell

    def test_the_attempt_identity_matches_the_live_module(self):
        assert A.EXECUTION_ATTEMPT_ID == ATTEMPT_ID


class TestP1ResultsPRRemainsSeparate:
    def test_section_f_quotes_p1_verbatim_from_the_live_charter(self, decision_text):
        f = _flat(_raw_section(decision_text, "F."))
        quote = (
            "That PR may make no production configuration change, must pass "
            "`validate_stage1_results()` against the closed universe, and its own result "
            "lifecycle requires independent exact-head review and principal acceptance."
        )
        assert _flat(quote) in f
        assert _flat(quote) in _flat(D0027.read_text())

    def test_step_11_ends_at_the_run_not_at_delivery(self, decision_text):
        f = _demphasize(_section(decision_text, "F."))
        assert "ends at the run" in f
        assert "It does not extend to delivering results into the repository." in f

    def test_p1_stays_one_unspent(self, decision_text):
        f = _demphasize(_section(decision_text, "F."))
        assert "neither consumes nor pre-authorizes §P.1's PR, and does not open it" in f
        assert "one, unspent" in f
        cons = _demphasize(_flat(decision_text.split("## Consequences")[1]))
        assert "XASSET-0027 §P.1 remains one, unspent" in cons

    def test_the_two_authorities_are_independent(self, decision_text):
        f = _demphasize(_section(decision_text, "F."))
        assert "The two are independent." in f

    def test_producing_results_is_not_applying_them(self, decision_text):
        """§H.2 after the review-5003284327 MAJOR-3 correction inserted the exception as §H.1."""
        h2 = _demphasize(_subsection(decision_text, "H.2"))
        assert "A completed run is a result, not a conclusion." in h2
        for token in ("percentages", "target weights", "Stage 2"):
            assert token in h2, token


class TestProhibitionsAreBoundToTheirGoverningClause:
    """Whole-line binding, extracted from the governing clause.

    XASSET-0051's P9 probe proved that asserting a prohibition's WORDS are present is vacuous:
    prefixing "it may " leaves every substring intact while inverting the meaning. These tests
    bind each bullet as a complete line under its own "must not:" clause.
    """

    def test_the_governing_clause_is_prohibitive(self, decision_text):
        h = _flat(_raw_section(decision_text, "H."))
        assert "The link-5 unit **must not**:" in h

    def test_there_are_many_withheld_bullets(self, withheld):
        assert len(withheld) >= 14, len(withheld)

    @pytest.mark.parametrize(
        "fragment",
        [
            "modify any pre-existing tracked repository byte",
            "make any committed repository mutation",
            "create any repository file other than",
            "rebind or repair anything",
            "correct, revert, regenerate, or re-pin",
            "rerun or re-adjudicate link 3 or link 4",
            "retry, re-attest, re-claim, recover, reset, or delete the lane",
            "execute before a lawful claim",
            "open a branch, a commit, or a pull request",
            "edit, rewrite, replace, interpret, commit, or deliver",
            "risk_lane_boundary",
            "acquire market, fundamental, economic, or Stage-2 data",
            "change any construction identity",
            "interpret, aggregate, rank, or act on the results",
            "authorize any successor unit of any kind",
        ],
    )
    def test_each_prohibition_appears_as_a_whole_bullet(self, withheld, fragment):
        matches = [b for b in withheld if fragment in _demphasize(b)]
        assert matches, fragment

    def test_no_withheld_bullet_carries_a_permissive_qualifier(self, withheld):
        """A bullet beginning "it may", "may", or "except" would invert the whole list."""
        for bullet in withheld:
            lowered = _demphasize(bullet).lower().lstrip()
            for permissive in ("it may ", "may ", "except ", "unless ", "is permitted"):
                assert not lowered.startswith(permissive), bullet

    def test_the_protected_portfolio_paths_are_each_withheld_by_name(self, withheld):
        joined = " ".join(_demphasize(b) for b in withheld)
        for relpath in PORTFOLIO_RELPATHS:
            assert relpath in joined, relpath


class TestEffectivityRequiresCompleteLifecycleClosure:
    def test_section_n_lists_all_seven_conditions(self, decision_text):
        n = _flat(_raw_section(decision_text, "N."))
        for i in range(1, 8):
            assert f"{i}. " in n, i
        for token in (
            "independent **FULL** exact-head review",
            "bounded correction and exact-head re-review",
            "principal exact-head acceptance",
            "normal merge",
            "immediate post-merge verification",
            "successful merge-commit CI whose `head_sha` is the exact merge SHA",
            "final post-CI verification and lifecycle closure",
        ):
            assert token in n, token

    def test_no_single_condition_is_sufficient(self, decision_text):
        n = _demphasize(_section(decision_text, "N."))
        assert "None is individually sufficient." in n
        assert "Opening this PR authorizes nothing" in n
        assert "a green PR-head CI run does not" in n
        assert "principal acceptance does not" in n
        assert "merge does not" in n
        assert "Only complete closure of all seven does" in n

    def test_ci_must_be_the_merge_commit_run_not_the_pr_head_run(self, decision_text):
        n = _demphasize(_section(decision_text, "N."))
        assert "not the PR head's own CI run" in n
        assert "not a run against any other commit" in n

    def test_effectivity_still_leaves_the_unit_conditional(self, decision_text):
        n = _demphasize(_section(decision_text, "N."))
        assert "must still satisfy every §G and §G.1 condition at the moment it acts" in n
        assert "may lawfully end without arming anything" in n

    def test_merging_arms_nothing(self, decision_text):
        n = _demphasize(_section(decision_text, "N."))
        assert "Merging this decision does not arm Stage 1" in n
        assert "new_execution_is_authorized() still returns False" in n
        assert "active_execution_is_authorized() still returns False" in n
        assert "the lane is still ABSENT" in n

    def test_the_seven_conditions_cover_the_six_required_gates(self, decision_text):
        n = _demphasize(_section(decision_text, "N."))
        assert "REQUIRED_LIFECYCLE_GATES" in n
        assert len(EXPECTED_LIFECYCLE_GATES) == 6


class TestLink5IsNotPerformedHere:
    def test_the_filing_performs_no_part_of_link_5(self, decision_text):
        a = _demphasize(_section(decision_text, "A."))
        for token in (
            "generates no attestation", "creates no AUTHORIZATION_ROOT", "arms nothing",
            "reaches no READY", "claims nothing", "evaluates no gate", "executes nothing",
            "produces no result", "persists nothing",
        ):
            assert token in a, token

    def test_section_o_is_an_exhaustive_non_authorization(self, decision_text):
        o = _demphasize(_section(decision_text, "O."))
        for token in (
            "generates no attestation",
            "creates no AUTHORIZATION_ROOT",
            "revives no spent authority, XASSET-0040 included",
            "evaluates no gate for any registered construction",
            "creates no stage1_results.yaml",
            "consumes nothing of ATTEMPT_1",
            "consumes no XASSET-0027 §P.1 results PR",
            "rewrites no accepted history",
        ):
            assert token in o, token

    def test_section_o_names_the_three_module_constants_as_unchanged(self, decision_text):
        o = _demphasize(_section(decision_text, "O."))
        for token in (
            "AUTHORIZING_DECISION", "AUTHORIZING_PULL_REQUEST", "REVIEWED_BASE_SHA",
            "LOAD_BEARING_RELPATHS",
        ):
            assert token in o, token

    def test_no_determination_string_for_link_5_execution_is_issued(self, decision_text):
        """The filing must not itself post a terminal outcome; only the future unit may."""
        flat = _flat(decision_text)
        assert "FORMAL DETERMINATION" not in flat.upper()


class TestStage1RemainsUnarmedAndNotExecutable:
    def test_the_lane_is_absent_and_every_lane_path_is_missing(self):
        assert not A.AUTHORIZATION_ROOT.exists()
        for path in (A.AUTHORIZATION_PATH, A.CLAIM_PATH, A.COMPLETION_PATH, A.LEDGER_PATH):
            assert not path.exists(), path

    def test_new_execution_is_not_authorized(self):
        authorized, reason = A.new_execution_is_authorized()
        assert authorized is False
        assert reason

    def test_active_execution_is_not_authorized(self):
        authorized, reason = A.active_execution_is_authorized()
        assert authorized is False
        assert "ABSENT" in reason

    def test_stage_1_executability_is_permanently_false(self):
        prereg = yaml.safe_load(PREREG.read_text())
        block = prereg["stage_1_executability"]
        assert block["executable"] is False
        assert block["executable_is_never_the_authorization_source"] is True

    def test_no_results_artifact_exists_anywhere(self):
        matches = [
            p for p in ROOT.rglob("stage1_results*")
            if ".git" not in p.parts
        ]
        assert matches == [], matches

    def test_the_decision_records_the_unarmed_posture(self, decision_text):
        cons = _demphasize(_flat(decision_text.split("## Consequences")[1]))
        assert "Stage 1 remains UNARMED and NOT EXECUTABLE" in cons
        assert "Lane state remains ABSENT" in cons
        assert "ATTEMPT_1 is intact, unclaimed, and unconsumed" in cons

    def test_zero_committed_activation_factors_are_added(self, decision_text):
        """CORRECTED after review 5003284327 MAJOR 2.

        "Zero activation factors" was imprecise: this filing adds exactly one CONDITIONAL
        governance authorization, which is its entire purpose. What it adds zero of is COMMITTED
        activation factors, and what it performs zero of is activation ACTS.
        """
        e = _demphasize(_section(decision_text, "E."))
        # ``_demphasize`` strips single-asterisk italics, so the emphasis on "committed" is gone here.
        assert "It adds zero committed activation factors." in e
        assert "stage_1_executability.executable stays permanently false" in e
        assert (
            "no committed value in this repository — this decision included — authorizes "
            "Stage-1 execution" in e
        )
        assert "exactly one **conditional governance authorization**" in _section(
            decision_text, "E."
        )
        assert 'Saying this decision adds "zero activation authority" would be false' in e

    def test_this_filing_is_not_an_activation_event(self, decision_text):
        e = _demphasize(_section(decision_text, "E."))
        assert "This filing is not an arming step and not an activation event." in e
        assert "Merging this decision arms nothing." in e

    def test_xasset_0029_e_is_quoted_verbatim(self, decision_text):
        e = _flat(_raw_section(decision_text, "E."))
        quote = (
            "Arming is a **runtime operator act**, not a further merged governance PR. "
            "`XASSET-0029` is the final governance decision required for Stage 1; the generator "
            "is then run once, and no additional authorization PR is ever required. The regress "
            "terminates because the final step changes no repository state."
        )
        assert _flat(quote) in e
        assert _flat(quote) in _flat(D0029.read_text())


class TestPackagingAndEvidence:
    def test_the_unit_creates_no_branch_commit_or_pull_request(self, decision_text):
        m = _demphasize(_section(decision_text, "M."))
        assert "no branch, no commit, and no pull request" in m
        assert "does not contend for the OPS-0014 §D single mutation lane" in m

    def test_the_evidence_is_external_and_names_its_terminal_outcome(self, decision_text):
        m = _demphasize(_section(decision_text, "M."))
        assert "durable, externally posted evidence" in m
        assert "its terminal outcome from §K by name" in m
        assert "what remains unauthorized" in m

    def test_a_repository_mutation_to_record_the_outcome_is_not_authorized(self, decision_text):
        m = _demphasize(_section(decision_text, "M."))
        assert (
            "A repository mutation to record the outcome is neither required nor authorized" in m
        )
        assert "not scope to assume" in m

    def test_the_unit_acts_at_the_exact_head_g1_requires(self, decision_text):
        m = _demphasize(_section(decision_text, "M."))
        assert "at the exact acting head §G.1 requires" in m


class TestRegisterSynchronisation:
    def test_the_workstream_is_untouched_in_status_and_priority(self, ws0014):
        assert ws0014["status"] == "proposed"
        assert ws0014["priority"] == "secondary"

    def test_exactly_zero_primary_workstreams(self):
        data = yaml.safe_load(WORKSTREAMS.read_text())
        assert sum(1 for w in data["workstreams"] if w.get("priority") == "primary") == 0

    def test_the_active_branch_moved_off_this_finished_unit(self, ws0014):
        """RE-ANCHORED BY XASSET-0053, for the same reason as the shared fields below.

        ``active_branch`` is WS-0014's SINGLE SHARED live self-reference. PR #353 merged, so it
        lawfully advanced onto the successor unit; asserting it at this unit's own branch would
        assert "this finished unit is still live". Every predecessor's value is retained as a
        NEGATIVE pin, so a silent revert to any finished unit's state still fails.
        """
        assert ws0014["active_branch"] != "claude/xasset-0052-step11-authority-6nxaha"
        assert ws0014["active_branch"] != "claude/xasset-0051-link4-auth-bjlfya"
        assert ws0014["active_branch"] != "claude/xasset-0049-rebinding-ll6hzf"

    def test_the_last_verified_main_sha_advanced_and_is_bound_at_both_ends(self, ws0014):
        """RE-ANCHORED BY XASSET-0053.

        ``last_verified_main_sha`` is WS-0014's SINGLE SHARED live self-reference, not this
        filing's own. PR #353 merged at `cc1d1b62...`, so under ``OPS-0001``'s Active-GitHub-fields
        rule it lawfully advanced onto the successor unit. Asserting it at this unit's own
        observation head would assert "this finished unit is still live", which is false. Every
        superseded value is retained as a NEGATIVE pin rather than deleted, so a silent revert to
        any finished unit's state still fails here, and the field stays bound at BOTH ends.
        """
        assert ws0014["last_verified_main_sha"] != LINK4_OBSERVATION_HEAD
        for finished in (BOUND_MERGE_SHA, XASSET0051_BASE, DEAD_MERGE_SHA):
            assert ws0014["last_verified_main_sha"] != finished, finished

    def test_the_shared_active_pr_moved_off_this_finished_unit(self, ws0014):
        """RE-ANCHORED BY XASSET-0053, for the same reason as the field above.

        This was ``test_the_active_pr_is_the_real_github_number_not_the_sentinel``, asserting the
        shared field still equalled THIS unit's number. Never predicted then and not predicted
        now: what remains asserted is that the shared field is no longer this finished unit's,
        that no sentinel survived unclaimed into the merged record, and that it never reverted to
        a predecessor. During a successor's own sentinel window the field is negative, which is a
        real state and is checked for consistency rather than skipped.
        """
        active = ws0014["active_pr"]
        assert active != THIS_PULL_REQUEST
        assert active != BOUND_AUTHORIZING_PULL_REQUEST
        if active is None:
            # EXTENDED BY XASSET-0062: ``None`` is the same UN-BOUND window the sentinel branch
            # below describes, in the spelling this register uses. A successor's number does not
            # exist until GitHub issues it and is never predicted, so the ordering cannot be
            # evaluated. As in that branch, the state is checked for CONSISTENCY rather than
            # skipped: a gate must EXPLICITLY claim the un-bound marker and still be in_progress.
            live = [g for g in ws0014["milestones"] if "pr" in g and g["pr"] is None]
            assert live, "the register carries an unbound active_pr that no gate claims"
            assert all(g.get("status") == "in_progress" for g in live), live
        elif active < 0:
            live = [g for g in ws0014["milestones"] if g.get("pr") == active]
            assert live, "the register carries a sentinel active_pr that no gate claims"
            assert all(g["status"] == "in_progress" for g in live), live
        else:
            assert active > THIS_PULL_REQUEST
            assert active not in PRIOR_SENTINELS
            assert active != PR_SENTINEL

    def test_the_finished_units_gate_is_not_rewritten(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == PRIOR_UNIT_GATE)
        assert gate["status"] == "in_progress" and gate["pr"] == 352

    def test_an_additive_closure_gate_records_the_finished_lifecycle(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == PRIOR_CLOSURE_GATE)
        assert gate["status"] == "complete" and gate["pr"] == 352
        flat = _flat(gate["description"])
        assert LINK4_OBSERVATION_HEAD in flat
        assert LINK4_DETERMINATION in flat
        assert LINK4_DETERMINATION_COMMENT in flat
        assert "LEFT BYTE-UNEDITED" in flat

    def test_this_units_gate_exists_and_is_in_progress(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)
        assert gate["status"] == "in_progress"
        assert gate["pr"] == THIS_PULL_REQUEST
        assert gate["pr"] != PR_SENTINEL, "the sentinel was never replaced"
        assert "PERFORMS NO PART" in gate["description"]

    def test_this_units_gate_is_not_marked_complete_by_its_own_filing(self, ws0014):
        gate = next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)
        assert gate["status"] != "complete"

    def test_the_registers_gate_records_the_authority_performance_distinction(self, ws0014):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert "CONDITIONALLY AUTHORIZES" in gate
        assert "THIS FILING PERFORMS NONE OF THOSE ACTS" in gate
        assert "NONE IS EXERCISABLE UNLESS AND UNTIL" in gate
        assert "XASSET-0040" in gate
        assert SPENT_STEP11_DETERMINATION in gate

    def test_the_registers_gate_never_denies_the_authority_it_records(self, ws0014):
        """ADDED after correction probe M2-g, which this suite MISSED at first.

        The gate is a live operative record. Nothing stopped it from reasserting the exact
        contradiction review 5003284327 MAJOR 2 identified, so the probe went uncaught. It is
        bound here directly: the denial and the two "zero activation authority" formulations may
        appear only inside the gate's own explicit list of PROHIBITED claims, never as an
        operative statement.
        """
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        marker = "THREE CLAIMS ARE PROHIBITED"
        assert marker in gate, "the gate must carry the prohibition list"
        operative, prohibited = gate.split(marker, 1)
        for banned in (
            "NEITHER PERFORMED NOR AUTHORIZED BY",
            "ZERO activation authorizations",
            "ZERO activation authority",
            "zero activation authorizations",
            "zero activation authority",
        ):
            assert banned not in operative, banned
        # non-vacuity: the prohibition list must actually quote what it forbids
        assert "not authorized by this filing itself" in prohibited
        assert "zero activation authority" in prohibited

    def test_the_registers_latest_operative_blocks_never_deny_the_authority(self, ws0014):
        """The same guard for `next_action` and `blocker`'s CURRENT operative blocks.

        Earlier append-only history may keep its own accurate wording; the newest block may not.
        """
        for field in ("next_action", "blocker"):
            text = ws0014[field]
            latest = _flat("UPDATE, 2026-08-23" + text.rsplit("UPDATE, 2026-08-23", 1)[1])
            assert "CONDITIONALLY AUTHORIZES" in latest, field
            assert "ZERO COMMITTED ACTIVATION FACTORS" in latest, field
            assert "NEITHER PERFORMED NOR AUTHORIZED BY" not in latest, field
            # the two banned formulations may appear only where the block names them as false
            for banned in ("ZERO activation authorizations", "ZERO activation authority"):
                if banned in latest:
                    idx = latest.find(banned)
                    window = latest[max(0, idx - 200): idx + 200]
                    assert "would be FALSE" in window or "prohibited" in window, (field, banned)

    def test_the_registers_latest_operative_blocks_carry_the_corrected_range_rule(self, ws0014):
        """MAJOR 1, in the register: the operative blocks must not restate global reachability."""
        for field in ("next_action", "blocker"):
            text = ws0014[field]
            latest = _flat("UPDATE, 2026-08-23" + text.rsplit("UPDATE, 2026-08-23", 1)[1])
            assert "commits(observation_head..acting_head)" in latest, field
            assert "HISTORICAL ANCESTORS" in latest and "NOT INTERVENING COMMITS" in latest, field
            assert "ANY OTHER COMMIT IS A FAIL-CLOSED STOP unless" not in latest, field

    def test_the_registers_latest_operative_blocks_carry_the_artifact_exception(self, ws0014):
        """MAJOR 3, in the register."""
        for field in ("next_action", "blocker"):
            text = ws0014[field]
            latest = _flat("UPDATE, 2026-08-23" + text.rsplit("UPDATE, 2026-08-23", 1)[1])
            assert "REPOSITORY-WRITE EXCEPTION" in latest, field
            assert "research/level1_endpoint_evidence/stage1_results.yaml" in latest, field
            assert "ONLY AFTER THE LAWFUL CLAIM" in latest, field
            assert "UNCOMMITTED AND UNDELIVERED" in latest, field

    def test_the_registers_gate_carries_the_artifact_exception(self, ws0014):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert "ONE EXACT REPOSITORY-WRITE EXCEPTION" in gate
        assert "research/level1_endpoint_evidence/stage1_results.yaml" in gate
        assert "ONLY AFTER THE LAWFUL CLAIM" in gate
        assert "NO OTHER FILE CREATION OR MUTATION OF ANY KIND IS PERMITTED" in gate

    def test_the_registers_gate_carries_the_corrected_range_rule(self, ws0014):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert "commits(observation_head..acting_head)" in gate
        assert "UNSATISFIABLE" in gate
        assert "HISTORICAL ANCESTORS" in gate

    def test_the_registers_gate_records_the_intervening_commit_rule(self, ws0014):
        gate = _flat(next(g for g in ws0014["milestones"] if g["gate"] == THIS_GATE)["description"])
        assert "DESCENDANT ANCESTRY ALONE REMAINS" in gate.upper()
        assert "INSUFFICIENT" in gate.upper()
        assert LINK4_OBSERVATION_HEAD in gate

    def test_no_sentinel_survives_anywhere_in_the_register(self):
        raw = WORKSTREAMS.read_text()
        for sentinel in (PR_SENTINEL, *PRIOR_SENTINELS):
            assert f"active_pr: {sentinel}" not in raw, sentinel
            assert f"pr: {sentinel}" not in raw, sentinel

    def test_no_sentinel_survives_anywhere_in_the_tracked_tree(self):
        tracked = _git("ls-files").splitlines()
        needle = f"active_pr: {PR_SENTINEL}"
        for rel in tracked:
            path = ROOT / rel
            if not path.is_file():
                continue
            try:
                text = path.read_text()
            except (UnicodeDecodeError, OSError):
                continue
            assert needle not in text, rel


class TestCatalogSynchronisation:
    def test_the_catalog_lists_this_decision_uniquely_and_a_successor_is_newest(self, catalog):
        """RE-ANCHORED BY XASSET-0053.

        The catalog is append-only, so "newest row" names whichever filing is most recent -- this
        one when the class was written, a successor now. Asserting it here would assert "no
        successor may ever be filed". What is preserved is the invariant that actually mattered:
        this decision has exactly one row, it is still present, and anything after it is a
        strictly LATER identifier rather than a reordering or a duplicate.
        """
        ids = [d["decision_id"] for d in catalog]
        assert len(ids) == len(set(ids))
        assert ids.count(DECISION_ID) == 1
        idx = ids.index(DECISION_ID)
        for later in ids[idx + 1:]:
            assert later.startswith("XASSET-"), later
            assert int(later.split("-")[1]) > int(DECISION_ID.split("-")[1]), later

    def test_the_catalog_entry_points_at_the_real_file(self, catalog):
        entry = next(d for d in catalog if d["decision_id"] == DECISION_ID)
        assert (ROOT / entry["file"]).exists()
        assert entry["file"] == str(DECISION.relative_to(ROOT))
        assert entry["status"] == "Proposed"
        assert entry["supporting_artifact"] == Path(__file__).name

    def test_the_catalog_entry_relates_to_the_whole_chain(self, catalog):
        entry = next(d for d in catalog if d["decision_id"] == DECISION_ID)
        related = set(entry["related_decisions"])
        for required in ("XASSET-0040", "XASSET-0041", "XASSET-0049", "XASSET-0051"):
            assert required in related, required

    def test_the_catalog_has_no_open_issues(self):
        from portfolio_hq.dashboard import decisions as dash

        catalog = dash.build_catalog(ROOT)
        assert catalog.issues == ()


class TestNonVacuityAgainstTheBaseTree:
    """A guard against a suite that would pass identically before this filing existed.

    A test that holds in both states is a forward guard, not a detector. This class proves that
    the *detectors* genuinely depend on this filing's own bytes.
    """

    def test_the_decision_file_did_not_exist_at_the_base(self):
        rel = str(DECISION.relative_to(ROOT))
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{LINK4_OBSERVATION_HEAD}:{rel}"],
            cwd=ROOT, capture_output=True,
        )
        assert result.returncode != 0, "the decision already existed at the base"

    def test_this_test_module_did_not_exist_at_the_base(self):
        rel = Path(__file__).name
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{LINK4_OBSERVATION_HEAD}:{rel}"],
            cwd=ROOT, capture_output=True,
        )
        assert result.returncode != 0, "the suite already existed at the base"

    def test_the_gate_did_not_exist_at_the_base(self):
        raw = subprocess.run(
            ["git", "show", f"{LINK4_OBSERVATION_HEAD}:operations/WORKSTREAMS.yaml"],
            cwd=ROOT, capture_output=True, check=True, text=True,
        ).stdout
        assert THIS_GATE not in raw
        assert PRIOR_CLOSURE_GATE not in raw

    def test_the_catalog_gained_exactly_one_entry_from_this_unit(self, catalog):
        """RE-ANCHORED BY XASSET-0053.

        This compared the CURRENT catalog length against the base, which only holds while this
        unit is the newest filing. A successor appending its own row makes the difference two,
        which is correct rather than a defect. What is preserved is this unit's OWN contribution:
        the base did not carry this identifier, the live catalog carries it exactly once, and it
        is strictly longer than the base.
        """
        raw = subprocess.run(
            ["git", "show", f"{LINK4_OBSERVATION_HEAD}:governance/decisions.yaml"],
            cwd=ROOT, capture_output=True, check=True, text=True,
        ).stdout
        before = yaml.safe_load(raw)["decisions"]
        assert DECISION_ID not in {d["decision_id"] for d in before}
        assert [d["decision_id"] for d in catalog].count(DECISION_ID) == 1
        assert len(catalog) >= len(before) + 1

    def test_the_base_did_not_already_name_this_decision_anywhere(self):
        result = subprocess.run(
            ["git", "grep", "-l", DECISION_ID, LINK4_OBSERVATION_HEAD],
            cwd=ROOT, capture_output=True, text=True,
        )
        assert result.returncode != 0, result.stdout

    def test_the_shared_register_fields_actually_moved(self):
        raw = subprocess.run(
            ["git", "show", f"{LINK4_OBSERVATION_HEAD}:operations/WORKSTREAMS.yaml"],
            cwd=ROOT, capture_output=True, check=True, text=True,
        ).stdout
        before = next(
            w for w in yaml.safe_load(raw)["workstreams"] if w["id"] == "WS-0014"
        )
        assert before["active_pr"] == 352
        assert before["last_verified_main_sha"] == XASSET0051_BASE
        assert before["active_branch"] == "claude/xasset-0051-link4-auth-bjlfya"
