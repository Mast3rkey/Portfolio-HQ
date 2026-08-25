"""ENDPOINT-0001 Stage-1 operational execution authorization — XASSET-0047 (post-merge-CI recovery).

WHAT THIS MODULE IS
===================

XASSET-0028 closed the concrete construction universe STRUCTURALLY (680 registered
constructions across 48 cells). Structural closure is not operational authorization. This
module supplies the missing half: the mechanism by which exactly one Stage-1 execution
attempt may become operationally authorized, and the fail-closed machinery that decides
both "may a NEW execution start?" and "did THIS result come from the one lawful execution?"

WHY THE COMMITTED BOOLEAN IS NOT THE MECHANISM
==============================================

Flipping ``stage_1_executability.executable`` to true is wrong on three independent
grounds, the third dispositive: (1) a committed flag is effective the instant its PR
merges, before post-merge verification and before CI concludes; (2) a flag ASSERTS
authorization without demonstrating any gate closed; (3) it is already a validation error
-- ``_validate_stage_1_executability`` enforces ``_false(executable)``, so the canonical
file is INVALID in exactly the state that would authorize execution. XASSET-0029 preserves
that lock. ``executable`` stays false FOREVER: *no committed value in this repository
authorizes Stage-1 execution.*

CORRECTED AFTER INDEPENDENT FULL REVIEW 4946327932 (2 BLOCKING / 2 MAJOR)
========================================================================

BLOCKING 1 -- the previous form accepted the entire lifecycle from caller strings and
checked only internal consistency, so an entirely fictional review/acceptance/merge/CI
chain validated. Reproduced before correcting. Lifecycle facts are now DERIVED AND
RE-VERIFIED from two durable truth sources on every validation:

  * LOCAL GIT OBJECT STORE (``GitTruthSource``) -- merge SHA, both parents, ancestry, and
    the byte identity of load-bearing files AS THEY EXIST IN THE MERGED TREE. Content
    addressed and cryptographically durable; forging it means forging SHA-1/SHA-256
    preimages, not editing a JSON file.
  * GITHUB GOVERNANCE METADATA (``GovernanceTruthSource``) -- the review, its exact
    reviewed commit, its formal disposition, the reviewer's login, the principal
    acceptance comment, the post-merge verification comment, and the merge-commit CI
    run/job. This is GOVERNANCE metadata only. It is NOT market, price, fundamental, or
    any other economic data, and this module acquires none.

A recorded value is never accepted because its text is well-formed. Every recorded value
is compared against the independently fetched fact, and an unreachable source FAILS CLOSED.

BLOCKING 2 -- consuming the authorization made the public result validator reject the very
execution that consumed it, while deferring consumption until after the work left a replay
and concurrency window. Reproduced before correcting. The lane is now an explicit state
machine:

    ABSENT -> READY -> CLAIMED -> COMPLETED

and the two questions are separated, because they are genuinely different questions:

  * ``new_execution_is_authorized()``  -- may a NEW execution start?  READY only.
  * ``claimed_execution_is_authorized()`` -- did THIS result come from the one lawful
    claim? CLAIMED or COMPLETED, bound to the exact attestation hash and attempt id.

``validate_stage1_results()`` asks the SECOND question, so the lawfully claimed execution
can publish a valid result while a second execution remains impossible.

DURABILITY BOUNDARY -- STATED, NOT OVERCLAIMED
==============================================

``O_EXCL`` prevents a second creation only while the path exists, so "can never be
replayed" would be an overclaim. What is actually enforced:

  * The claim is recorded in TWO places -- ``claim.json`` and an append-only
    ``lane_ledger.jsonl``. Losing either one alone does NOT reopen the lane, because both
    are consulted and either is sufficient to establish CLAIMED.
  * Destroying the whole authorization directory destroys the attestation too, so the lane
    becomes ABSENT, which is NOT READY. Re-arming then requires passing the full
    authenticated lifecycle verification again from scratch.
  * A crash after CLAIM leaves the lane CLAIMED. It never returns to READY on its own.
    Recovery is a governed act, not an automatic transition.

A privileged operator who deletes the entire directory is outside any filesystem-based
enforcement boundary; that is disclosed here rather than papered over.

SUCCESSOR OPERATIONAL REBINDING — XASSET-0037 (XASSET-0030 §G.B step 8)
=======================================================================

XASSET-0036 authorized the §G.B steps-2–7 executable package, and PR #336 delivered it: the
deterministic runner, the result validator, the corrected §C enforcement branch, the reconciled
canonical bytes, and an extension of the trust boundary from six paths to nine. XASSET-0030 §D
recorded up front that doing so *deliberately creates enforcement drift*, because the structural
authorization source was still bound to the XASSET-0029 merged tree (PR #328, ``3cc15d58…``), in
which three of those nine paths do not exist and four others carry different bytes.

**That fail-closed condition was reproduced before it was corrected.** Against the XASSET-0029
merged tree, the nine load-bearing paths resolve to three ``git truth: … is absent from the
authorized merged tree`` errors (the runner, the result validator, and the XASSET-0036 decision)
and four ``enforcement drift: …`` errors (this module, the preregistration validator, and both
canonical files). No attestation could be written and no lane could reach READY. **The obsolete
XASSET-0029 lifecycle cannot authorize the current package, and that is the correct behaviour.**

XASSET-0037 performs the one successor operational-authorization / load-bearing rebinding
lifecycle XASSET-0030 §G.B step 8 requires, against the exact merged bytes of PR #336. It binds
**four structurally distinct identities**, deliberately kept in separate constants and separate
attestation blocks so no single "predecessor" field carries inconsistent meanings:

  * ``PREDECESSOR_*`` — XASSET-0028, the construction-universe **structural closure** predecessor.
    Unchanged in name, meaning, and value; this rebinding does not touch it.
  * ``HISTORICAL_OPERATIONAL_AUTHORIZATION_*`` — XASSET-0029, the **historical** operational
    authorization (PR #328). Preserved as predecessor authority and still verified against git;
    it is no longer the effective structural authorization source.
  * ``PACKAGE_AUTHORIZING_*`` — XASSET-0036, the decision that **authorized** the executable
    package (PR #335). Authority over the package, not over this rebinding.
  * ``EXECUTABLE_PACKAGE_*`` — PR #336 itself, the exact **completed package identity** being
    rebound: its merge, accepted head, base, and zero merge drift.

``AUTHORIZING_DECISION`` / ``AUTHORIZING_PULL_REQUEST`` / ``REVIEWED_BASE_SHA`` now name
XASSET-0037. Nothing is removed from ``LOAD_BEARING_RELPATHS`` and no exact-byte check is
weakened: the set grows 9 → 10 with the XASSET-0037 decision itself, on the same footing
XASSET-0029 and XASSET-0036 already occupy for their own authorizations.

Rebinding is **not** arming. It changes repository state, so XASSET-0029 §E's no-infinite-regress
rule — whose stated terminating condition is a final step that *changes no repository state* — is
untouched: this adds zero activation authorizations, and final activation remains the external
one-shot runtime attestation and the operator's act.

POST-CORRECTION OPERATIONAL REBINDING — XASSET-0044 (XASSET-0030 §D, authorized by XASSET-0043)
================================================================================================

XASSET-0041 authorized one bounded correction of the PR #337 lifecycle actor evidence, and
XASSET-0042 (PR #342) performed it — lawfully changing this module. XASSET-0030 §D recorded in
advance that any such lawful correction *deliberately creates enforcement drift*, and it did:
against the bound XASSET-0037 merged tree, exactly one of the ten load-bearing paths drifted, and
it is precisely the one XASSET-0042 was authorized to correct. An obsolete authorization that
cannot authorize a corrected module is the mechanism working, not a defect.

**§G.B step 8 is NOT consumed a second time.** Step 8 authorized ONE rebinding against the
executable package's exact merged bytes, and XASSET-0037 performed it; that budget stays spent and
the package it bound stays bound. This rebinding's authority is §D's "successor
operational-authorization **or reconciliation lifecycle**" clause plus XASSET-0041 §I link 2's own
word, *equivalent* — the same kind and rigour, separately authorized by XASSET-0043, not a second
draw on step 8. XASSET-0037 is preserved exactly as it preserved XASSET-0029.

This rebinding binds a **fifth** structurally distinct relationship — the corrected module and the
merge that delivered it — in its own constants, for the same anti-overloading reason XASSET-0037 §C
gave for its four: ``PRIOR_SUCCESSOR_REBINDING_*`` (XASSET-0037 / PR #337),
``CORRECTION_AUTHORIZING_*`` (XASSET-0041 / PR #341), ``CORRECTED_MODULE_*`` (XASSET-0042 / PR #342,
the completed correction being bound), and ``REBINDING_AUTHORIZING_*`` (XASSET-0043 / PR #343, whose
closed lifecycle is also this rebinding's own reviewed base).

``LOAD_BEARING_RELPATHS`` grows 10 → 14 by **direct membership**: after this rebinding, four
decisions jointly make the corrected bytes lawful, and any left outside the boundary would stay
editable after attestation. Nothing is removed, no identity is altered, and the pin-succession
refusal is extended to XASSET-0037's own accepted pins rather than relaxed. The derivation surface
gains a **second** exact closed transition, appended — ``package → successor → rebound`` — with the
first link preserved verbatim as accepted history.

Rebinding is **not** arming. XASSET-0029 §E's no-infinite-regress rule is untouched: this adds zero
activation authorizations, ``stage_1_executability.executable`` stays ``false`` permanently, and
final activation remains the external one-shot runtime attestation and the operator's act.

POST-MERGE-CI RECOVERY — XASSET-0047 (XASSET-0046 SS-G.6, authorized by XASSET-0046 SS-F)
=========================================================================================

XASSET-0044 bound this module's lifecycle anchor to itself and PR #344. That lifecycle STOPPED: its
own merge-commit CI at merge ``f5dedce1...`` FAILED (run 32439614683 / job 96647501864), so its
seventh condition never closed and XASSET-0044 is NOT EFFECTIVE. XASSET-0045 authorized a recovery
and stopped identically at merge ``2f8cdebe...`` (run 32490789238 / job 96797667282), so its own
grant NEVER VESTED. XASSET-0046 then closed all seven of its conditions and authorized EXACTLY ONE
recovery/reconciliation unit. This module is rebound by that unit.

WHY AN ANCHOR HAD TO MOVE AT ALL. The anchor is not decoration: ``verify_lifecycle_against_truth``
authenticates the AUTHORIZING pull request's own six-plus-one lifecycle from durable truth, and
XASSET-0044's sixth gate is a merge-commit CI success at a commit whose CI is recorded as failed and
is immutable. A green run at any other commit is excluded by that condition's own words. The old
anchor is therefore not merely stale -- it is PERMANENTLY UNSATISFIABLE, and an attestation could
never be authenticated against it again.

WHAT MOVED, AND WHAT DELIBERATELY DID NOT. Only the lifecycle anchor:
``AUTHORIZING_DECISION`` / ``AUTHORIZING_PULL_REQUEST`` / ``REVIEWED_BASE_SHA``, one new identity
family for the recovery AUTHORITY, one new family recording the two STOPPED lifecycles as adverse
history, and ``LOAD_BEARING_RELPATHS`` 14 -> 16 so the two decisions that jointly make these bytes
lawful sit inside the identity they authorize. XASSET-0046 SS-G.9 freezes the canonical inputs, so
``PROTOCOL_V1.md``, ``pre_registration.yaml``, the derivation module, the runner, the result
validator, the universe, and every outcome-producing semantic are UNCHANGED -- and
:func:`_verify_recovery_lifecycle_anchor` refuses the attestation if a canonical pin ever moves
without the succession machinery moving with it.

NOTHING IS REMOVED AND NOTHING IS RELAXED. Every predecessor identity, every inherited merge, every
exact-byte check, and the pin-succession refusal all survive verbatim; three inherited merges are
ADDED to the verification table, and four new refusals are added on top. Recovering is not arming:
this adds zero activation authorizations, ``stage_1_executability.executable`` stays ``false``
permanently, and final activation remains the external one-shot runtime attestation and the
operator's act.

NOT A RISK MODULE. No RISK-0001 scenario, threshold, magnitude, window, parameter, attempt
identity, result value, or family conclusion is read, imported, or reused. Only neutral
engineering patterns are shared: canonical JSON hashing, duplicate-key rejection, immutable
preexecution metadata, exact-identity verification, O_EXCL one-shot creation, consuming
authorization at the first eligible work item, and fail-closed validation.
"""

from __future__ import annotations

import builtins
import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence

ROOT = Path(__file__).resolve().parent

# ======================================================================================
# Bound identity
# ======================================================================================

REPOSITORY_IDENTITY = "Mast3rkey/Portfolio-HQ"
STUDY_ID = "ENDPOINT-0001"
#: EFFECTIVE structural authorization source, REBOUND AGAIN under XASSET-0046 SS-G.6, which requires
#: this recovery unit to establish a successor lifecycle anchor against ITS OWN decision, pull
#: request, accepted head, merge, successful exact-merge CI, and final closure.
#:
#: WHY THE PREVIOUS ANCHOR IS PERMANENTLY UNUSABLE, stated exactly rather than softened. XASSET-0044
#: named itself here, and its own effectivity condition required successful merge-commit CI at the
#: exact merge SHA ``f5dedce1...``. Run 32439614683 / job 96647501864 is that run, and it FAILED.
#: XASSET-0045 then authorized a recovery, reached six of its own seven conditions, and failed the
#: same sixth at ``2f8cdebe...`` (run 32490789238 / job 96797667282). Both failures are immutable
#: adverse history: neither may be re-run in place, relabelled, waived, or represented as
#: successful, and neither lifecycle closure may be posted retrospectively. Consequently NEITHER
#: XASSET-0044 NOR XASSET-0045 IS EFFECTIVE, and an anchor naming an ineffective decision cannot
#: authorize anything. See PERMANENTLY_INEFFECTIVE_DECISIONS below, which refuses that shape
#: mechanically rather than by comment.
#:
#: SS-G.B STEP 8 IS NOT RE-CONSUMED, and this rebinding does not draw on it either. Step 8
#: authorized ONE rebinding against the executable package's exact merged bytes and XASSET-0037
#: performed it; that budget stays spent and the package it bound stays bound. The authority for
#: THIS rebinding is XASSET-0046 SS-F, which authorizes exactly one recovery/reconciliation unit and
#: bounds it by SS-G.
#:
#: SCOPE, per XASSET-0046 SS-G.7 and SS-G.9. Only the LIFECYCLE ANCHOR moves. The canonical inputs
#: are frozen by SS-G.9 and are NOT amended here, so ``rebound_by`` and
#: ``effective_structural_authorization_source`` in the canonical charter still name XASSET-0044 --
#: which remains literally true, because XASSET-0044 is still the last decision that amended those
#: canonical BYTES and this unit amends none of them. The two are different relationships: which
#: decision last rebound the canonical bytes, and which decision's lifecycle the mechanism
#: authenticates against. Overloading them is the failure mode XASSET-0037 SS-C named, so they are
#: deliberately left distinct.
#: EFFECTIVE structural authorization source, REBOUND AGAIN by XASSET-0049 under XASSET-0048 SS-E,
#: which authorizes exactly one XASSET-0030 SS-G.B STEP-8-EQUIVALENT successor
#: operational-authorization / load-bearing rebinding against the exact merged bytes as they stand
#: at XASSET-0048's own lifecycle-closing merge.
#:
#: EXACT CLOSED TRANSITION, per XASSET-0048 SS-F.3. Old value ``"XASSET-0047"``; new value
#: ``"XASSET-0049"``. The old value is PRESERVED rather than overwritten -- see
#: :data:`PRIOR_RECONCILIATION_DECISION` and the whole ``PRIOR_RECONCILIATION_*`` family below,
#: which keeps XASSET-0047's own merge, accepted head, and base verifiable from git after the
#: anchor moves off it. A value that moves without both ends bound is drift wearing a rebinding's
#: label, and before this rebinding XASSET-0047's identity was reachable ONLY through the moving
#: anchor: reproduced against the live module, neither ``bb95ed26...`` nor ``8ae0988d...`` appeared
#: under any constant, so overwriting the anchor alone would have destroyed that identity outright.
#:
#: SS-G.B STEP 8 IS NOT RE-CONSUMED, and this rebinding does not draw on it. Step 8 authorized ONE
#: rebinding against the executable package's exact merged bytes and XASSET-0037 performed it;
#: that budget stays spent and the package it bound stays bound. XASSET-0043 SS-C and XASSET-0044
#: SS-C both record it. The authority for THIS rebinding is XASSET-0048 SS-E, which is
#: XASSET-0041 SS-I link 2 -- the step-8 EQUIVALENT: a lifecycle of the same kind and rigour,
#: separately authorized, and never a second draw on step 8's own spent budget.
#:
#: SCOPE, per XASSET-0048 SS-F.7's "only to the extent the rebinding requires". The canonical
#: artifacts are NOT amended by this unit, so ``rebound_by`` and
#: ``effective_structural_authorization_source`` in the canonical charter still name XASSET-0044 --
#: which remains literally true, because XASSET-0044 is still the last decision that amended those
#: canonical BYTES and this unit amends none of them. XASSET-0047 drew that distinction and it is
#: preserved unchanged here: which decision last rebound the canonical bytes, and which decision's
#: lifecycle the mechanism authenticates against, are DIFFERENT relationships. Overloading them is
#: the failure mode XASSET-0037 SS-C named.
AUTHORIZING_DECISION = "XASSET-0049"

#: XASSET-0028, the construction-universe STRUCTURAL CLOSURE predecessor. Deliberately UNCHANGED in
#: name, meaning, and value: repointing it at XASSET-0029 would overload one field with two
#: different relationships, which is exactly what this rebinding must not do.
PREDECESSOR_DECISION = "XASSET-0028"

#: The XASSET-0049 pull request. Bound so an attestation cannot silently reference another.
#:
#: EXACT CLOSED TRANSITION, per XASSET-0048 SS-F.3. Old value ``347`` (XASSET-0047's own pull
#: request); new value this unit's own GitHub-issued number. The old value is PRESERVED rather
#: than overwritten -- see :data:`PRIOR_RECONCILIATION_PULL_REQUEST`.
#:
#: PROVENANCE, stated exactly rather than flatteringly: this number was NOT written in advance as
#: the next sequential guess. The first commit on this branch carried the sentinel ``-2`` -- a
#: NEGATIVE, structurally impossible pull-request number that can never validate by accident, and
#: deliberately distinct from XASSET-0047's own ``0`` and XASSET-0048's own ``-1`` so this unit's
#: sentinel can never be mistaken for a predecessor's. The draft pull request was then opened,
#: GitHub issued its own number, that number was read back from live GitHub, and only then was it
#: bound here and re-verified against the live pull request's own head, base, and state. A wrong
#: number still fails closed at ``verify_lifecycle_against_truth``, which fetches this exact pull
#: request from durable governance metadata; the point of the sentinel is that the failure can
#: never be a SILENT one.
AUTHORIZING_PULL_REQUEST = 349

#: The single Stage-1 execution lane XASSET-0027 SS-P.1 permits. Derived from repository
#: truth, not invented: no Stage-1 attempt has ever been executed or authorized. UNCHANGED by the
#: rebinding -- a successor authorization does not mint a second attempt.
EXECUTION_ATTEMPT_ID = "ENDPOINT-0001::STAGE_1::ATTEMPT_1"

#: MAJOR 2 (review 4946397399), rebound by XASSET-0037, again by XASSET-0044, again by
#: XASSET-0047, and again here: the exact base THIS rebinding lifecycle was reviewed against --
#: the XASSET-0048 merge, which is the single event that made this unit authorized to begin at
#: all. The real merge's FIRST parent must equal this. If main advances before merge, the
#: lifecycle cannot arm from the old review -- it requires a fresh exact-head/base review.
#:
#: EXACT CLOSED TRANSITION, per XASSET-0048 SS-F.3. Old value
#: ``"0b76c09f8d1aba01780b4f06fdd692f7393fbfd3"`` (the XASSET-0046 merge, XASSET-0047's own
#: authority); new value ``"f052efad38e3d57e3e5615799ac3bcbebe83ff5f"`` (the XASSET-0048 merge).
#: The old value is PRESERVED rather than overwritten -- it remains bound, unchanged, as
#: :data:`RECOVERY_AUTHORIZING_MERGE_SHA` and as :data:`PRIOR_RECONCILIATION_MERGE_BASE`.
#:
#: EQUALITY, NOT DESCENT -- XASSET-0048 SS-F.2, made operative rather than described. The base is
#: required to EQUAL the exact normal-merge commit closing XASSET-0048's own SS-J lifecycle, and
#: :func:`_verify_step8_equivalent_base_equality` decides that as a pure proposition rather than
#: leaving it to prose. Descent stays NECESSARY HISTORY and is explicitly INSUFFICIENT AUTHORITY:
#: under a descent-only rule any later commit on main would qualify while carrying bytes no review
#: of the grant ever saw. Reproduced through the real mechanism before this rebinding was written.
REVIEWED_BASE_SHA = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"

#: XASSET-0028's exact historical identity. MAJOR 1: the canonical contract promises this
#: is bound, so it is now actually verified against the local git object store.
PREDECESSOR_MERGE_SHA = "c51e94609eff7ede2bdfa084844d59b8347561e5"
PREDECESSOR_ACCEPTED_HEAD = "036606401ea569b0a03f2d716d87a057d07d71dc"
PREDECESSOR_MERGE_BASE = "e4b6f0b810884fcb73d1b8ee053d8005db532f3e"

# --------------------------------------------------------------------------------------
# XASSET-0037 / SS-G.B step 8 — three further identities, each structurally distinct
# --------------------------------------------------------------------------------------
#
# These are NOT interchangeable with PREDECESSOR_* above, and NOT with each other. Overloading one
# "predecessor" notion across four different relationships is precisely how a rebinding silently
# starts binding the wrong tree, so each relationship gets its own constants and its own
# independently verified attestation block.

#: XASSET-0029, the HISTORICAL operational authorization (PR #328). Its lifecycle really closed and
#: is not invalidated; it simply stopped being the EFFECTIVE structural authorization source once
#: the XASSET-0036 executable package changed the bytes it bound. Still verified against git, so
#: the successor cannot quietly disown a predecessor it claims to inherit from.
HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION = "XASSET-0029"
HISTORICAL_OPERATIONAL_AUTHORIZATION_PULL_REQUEST = 328
HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA = "3cc15d58a42e6d56fbe702ccf4f377b60fbb8b0c"
HISTORICAL_OPERATIONAL_AUTHORIZATION_ACCEPTED_HEAD = "49609c3ff9befe1ba8d0b296da421337b5a425a0"
HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_BASE = "c51e94609eff7ede2bdfa084844d59b8347561e5"

#: XASSET-0036 (PR #335), which AUTHORIZED the executable package. Authority over the package's
#: creation -- not over this rebinding, and not itself the package.
PACKAGE_AUTHORIZING_DECISION = "XASSET-0036"
PACKAGE_AUTHORIZING_PULL_REQUEST = 335
PACKAGE_AUTHORIZING_MERGE_SHA = "be90aeef5c48e84849a007b31abbb1166857785d"

#: PR #336 itself -- the exact COMPLETED EXECUTABLE PACKAGE this rebinding binds. Distinct from the
#: decision that authorized it: the authority is a governance record, this is a merged tree.
EXECUTABLE_PACKAGE_PULL_REQUEST = 336
EXECUTABLE_PACKAGE_MERGE_SHA = "3e5de8f85c69c2e5dc2b75421446b5db996d7cf1"
EXECUTABLE_PACKAGE_ACCEPTED_HEAD = "07519f864c869d98aaf4a65cea53e85086a99fec"
EXECUTABLE_PACKAGE_MERGE_BASE = "be90aeef5c48e84849a007b31abbb1166857785d"

# --------------------------------------------------------------------------------------
# XASSET-0044 / XASSET-0030 SS-D — the FIFTH relationship, and its three further identities
# --------------------------------------------------------------------------------------
#
# XASSET-0037 SS-C identified the largest failure mode available to a rebinding: overloading one
# identity across relationships that are not the same relationship. It answered that with four
# separately named identity families. This rebinding adds a FIFTH -- the CORRECTED MODULE and the
# merge that delivered it -- and the same anti-overloading rule is what keeps it from being smuggled
# into ``EXECUTABLE_PACKAGE_*`` or ``HISTORICAL_OPERATIONAL_AUTHORIZATION_*``. None of the constants
# below is interchangeable with any above, or with each other.

#: XASSET-0037, the PRIOR successor operational rebinding (PR #337). Its own six-gate lifecycle
#: really closed and is NOT invalidated; it simply stopped being the EFFECTIVE structural
#: authorization source once XASSET-0042 lawfully corrected one of the ten paths it bound. Still
#: verified against git, so this successor cannot quietly disown the predecessor it inherits from.
PRIOR_SUCCESSOR_REBINDING_DECISION = "XASSET-0037"
PRIOR_SUCCESSOR_REBINDING_PULL_REQUEST = 337
PRIOR_SUCCESSOR_REBINDING_MERGE_SHA = "637eaa30302f5a71f84ab1d215ecbd32c01399b5"
PRIOR_SUCCESSOR_REBINDING_ACCEPTED_HEAD = "f40c816223c78f1d1e436b718455df5fb3d77fa7"
PRIOR_SUCCESSOR_REBINDING_MERGE_BASE = "3e5de8f85c69c2e5dc2b75421446b5db996d7cf1"

#: XASSET-0041 (PR #341), which AUTHORIZED the actor-evidence correction. Authority over the
#: correction's creation -- not the correction itself, and not this rebinding.
CORRECTION_AUTHORIZING_DECISION = "XASSET-0041"
CORRECTION_AUTHORIZING_PULL_REQUEST = 341
CORRECTION_AUTHORIZING_MERGE_SHA = "9c8647f9dddacdf63825f569097214ba65299fe8"
#: MAJOR 1 (review 4986931575). These two were absent, and their absence silently DISABLED the
#: exact-parent and merge-tree checks for this one inherited merge: the verification loop skips
#: both whenever a base or accepted head is ``None``. Reproduced through the public path before
#: this correction -- a PR #341 merge rewritten to a single WRONG parent with a DRIFTED tree still
#: validated. Re-derived independently from the local object store and cross-checked against
#: GitHub's own record of PR #341, which agree exactly.
CORRECTION_AUTHORIZING_ACCEPTED_HEAD = "0449d08217b5c0e422721ff3ef76b4241fb8a95a"
CORRECTION_AUTHORIZING_MERGE_BASE = "f212cce50e28ae887dc8c594bf8ae491a3ef85af"

#: PR #342 itself -- the exact COMPLETED CORRECTION this rebinding binds, and the reason it exists.
#: Distinct from the decision that authorized it: the authority is a governance record, this is a
#: merged tree carrying the corrected module's actual bytes.
CORRECTED_MODULE_DECISION = "XASSET-0042"
CORRECTED_MODULE_PULL_REQUEST = 342
CORRECTED_MODULE_MERGE_SHA = "5fbfc94d7333e552bd2654261e0c57134a172e31"
CORRECTED_MODULE_ACCEPTED_HEAD = "4d5d99d67364d3c940aad74c3093bd2afbc3481d"
CORRECTED_MODULE_MERGE_BASE = "9c8647f9dddacdf63825f569097214ba65299fe8"

#: XASSET-0043 (PR #343), which AUTHORIZED this rebinding. Its complete seven-condition SS-N
#: lifecycle closing is the single event that made this unit authorized to begin, which is why its
#: merge is also this rebinding's own reviewed base.
REBINDING_AUTHORIZING_DECISION = "XASSET-0043"
REBINDING_AUTHORIZING_PULL_REQUEST = 343
REBINDING_AUTHORIZING_MERGE_SHA = "0709d2f05ab031ecb6f69c40465ed4a227983aed"
REBINDING_AUTHORIZING_ACCEPTED_HEAD = "8e9d65ffa40991fade92b60f72f833501ce799d9"
REBINDING_AUTHORIZING_MERGE_BASE = "5fbfc94d7333e552bd2654261e0c57134a172e31"

# --------------------------------------------------------------------------------------
# XASSET-0047 / XASSET-0046 SS-G.6 — the SIXTH relationship, and the two STOPPED lifecycles
# --------------------------------------------------------------------------------------
#
# XASSET-0037 SS-C identified the largest failure mode available to a rebinding: overloading one
# identity across relationships that are not the same relationship. XASSET-0044 added a fifth family
# for exactly that reason. This recovery adds a SIXTH -- the RECOVERY AUTHORIZATION -- and, for the
# first time in this chain, a family whose members are NOT authorities at all: two merged,
# reviewed, accepted, drift-free lifecycles that STOPPED, and which therefore may never be cited as
# authority by anything. Keeping them under their own explicitly-named constants is what stops a
# future reader from mistaking a preserved predecessor for an effective one.

#: XASSET-0046 (PR #346), which AUTHORIZED this recovery. Its complete seven-condition SS-M
#: lifecycle closing is the single event that made this unit authorized to begin, which is why its
#: merge is also this recovery's own reviewed base. Distinct from every constant above: this is the
#: authority for THIS unit, not a package, not a correction, not a prior rebinding.
RECOVERY_AUTHORIZING_DECISION = "XASSET-0046"
RECOVERY_AUTHORIZING_PULL_REQUEST = 346
RECOVERY_AUTHORIZING_MERGE_SHA = "0b76c09f8d1aba01780b4f06fdd692f7393fbfd3"
RECOVERY_AUTHORIZING_ACCEPTED_HEAD = "0964dc2bd6ab3be8282193f76fa04c764198db0f"
RECOVERY_AUTHORIZING_MERGE_BASE = "2f8cdebe14925021171b9779453946be1f69b506"

#: XASSET-0044 (PR #344) -- the STOPPED post-correction rebinding this recovery supersedes as the
#: lifecycle anchor. It merged with zero drift after a clean review chain, and then its own
#: merge-commit CI FAILED at its exact merge SHA. Its identity is preserved and verified from git
#: exactly as every closed predecessor's is, but it is NOT a closed predecessor and must never be
#: described as one: its lifecycle never closed, so it is not effective and authorizes nothing.
STOPPED_REBINDING_DECISION = "XASSET-0044"
STOPPED_REBINDING_PULL_REQUEST = 344
STOPPED_REBINDING_MERGE_SHA = "f5dedce1d1d3116ed8a6845c4447388c85a5414c"
STOPPED_REBINDING_ACCEPTED_HEAD = "9c2821ab9e0e0dff09f5a03da5a6034775b00750"
STOPPED_REBINDING_MERGE_BASE = "0709d2f05ab031ecb6f69c40465ed4a227983aed"
#: The exact failed merge-commit CI at STOPPED_REBINDING_MERGE_SHA. Immutable adverse history.
STOPPED_REBINDING_FAILED_CI_RUN = "32439614683"
STOPPED_REBINDING_FAILED_CI_JOB = "96647501864"

#: XASSET-0045 (PR #345) -- the STOPPED recovery authorization for XASSET-0044's stopped lifecycle.
#: Its SS-F grant was conditioned on its own complete lifecycle closure, which did not occur, so
#: that grant NEVER VESTED. That is a different failure from XASSET-0043's, whose single grant was
#: SPENT BY USE; both roads end with no available authority, and the distinction is recorded so a
#: future reader cannot reach for an unspent grant by analogy to a spent one.
STOPPED_RECOVERY_AUTHORIZATION_DECISION = "XASSET-0045"
STOPPED_RECOVERY_AUTHORIZATION_PULL_REQUEST = 345
STOPPED_RECOVERY_AUTHORIZATION_MERGE_SHA = "2f8cdebe14925021171b9779453946be1f69b506"
STOPPED_RECOVERY_AUTHORIZATION_ACCEPTED_HEAD = "61e629f0f655ce8ca4ccd7eaa370d132d593515c"
STOPPED_RECOVERY_AUTHORIZATION_MERGE_BASE = "f5dedce1d1d3116ed8a6845c4447388c85a5414c"
#: The exact failed merge-commit CI at STOPPED_RECOVERY_AUTHORIZATION_MERGE_SHA. Immutable adverse
#: history, on precisely the footing PR #344's own failed run occupies.
STOPPED_RECOVERY_AUTHORIZATION_FAILED_CI_RUN = "32490789238"
STOPPED_RECOVERY_AUTHORIZATION_FAILED_CI_JOB = "96797667282"

# --------------------------------------------------------------------------------------
# XASSET-0049 / XASSET-0048 SS-E — the SEVENTH relationship, and the PRIOR ANCHOR it supersedes
# --------------------------------------------------------------------------------------
#
# XASSET-0037 SS-C identified the largest failure mode available to a rebinding: overloading one
# identity across relationships that are not the same relationship. XASSET-0044 added a fifth
# family for exactly that reason and XASSET-0047 a sixth. This rebinding adds a SEVENTH -- the
# STEP-8-EQUIVALENT AUTHORIZATION -- together with the PRIOR ANCHOR whose place it takes.
#
# WHY THE PRIOR-ANCHOR FAMILY IS MANDATORY RATHER THAN DECORATIVE. Reproduced against the live
# module BEFORE this rebinding was written: XASSET-0047's own merge ``bb95ed26...`` and accepted
# head ``8ae0988d...`` appeared under NO constant anywhere. They were reachable only through
# AUTHORIZING_DECISION / AUTHORIZING_PULL_REQUEST / REVIEWED_BASE_SHA -- the three values this
# rebinding moves. Moving them without this family would therefore not have weakened XASSET-0047's
# identity; it would have DESTROYED it, and XASSET-0048 SS-F.9 requires every preserved
# predecessor identity family to be carried forward intact.

#: XASSET-0048 (PR #348), which AUTHORIZED this step-8-equivalent rebinding. Its complete
#: seven-condition SS-J lifecycle closing is the single event that made this unit authorized to
#: begin, which is why its merge is also this rebinding's own reviewed base. Distinct from every
#: constant above: this is the authority for THIS unit -- not a package, not a correction, not a
#: prior rebinding, and not a recovery.
#:
#: XASSET-0048 SS-F.2 makes the relationship between this merge and :data:`REVIEWED_BASE_SHA` an
#: EQUALITY rather than a descent, and :func:`_verify_step8_equivalent_base_equality` decides it.
STEP8_EQUIVALENT_AUTHORIZING_DECISION = "XASSET-0048"
STEP8_EQUIVALENT_AUTHORIZING_PULL_REQUEST = 348
STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA = "f052efad38e3d57e3e5615799ac3bcbebe83ff5f"
STEP8_EQUIVALENT_AUTHORIZING_ACCEPTED_HEAD = "42e3a8aec1b36c4e5f22e4cdf4210a61ed781156"
STEP8_EQUIVALENT_AUTHORIZING_MERGE_BASE = "bb95ed26964b1bc7a2e230c76060fec82752efa1"

#: XASSET-0047 (PR #347) -- the PRIOR lifecycle anchor this rebinding supersedes. Its own complete
#: seven-condition lifecycle really closed and is NOT invalidated: it is a CLOSED PREDECESSOR, on
#: exactly the footing XASSET-0029 and XASSET-0037 occupy, and emphatically NOT on the footing of
#: the two STOPPED lifecycles below. It stopped being the EFFECTIVE structural authorization
#: source only because XASSET-0048 authorized a successor and this unit is that successor.
#:
#: DELIBERATELY ITS OWN FAMILY, not folded into ``RECOVERY_AUTHORIZING_*``. Those constants name
#: XASSET-0046, the decision that AUTHORIZED the reconciliation; these name XASSET-0047, the
#: reconciliation ITSELF. Authority over a unit and the unit's own merged tree are different
#: relationships, and the module already keeps that distinction for XASSET-0036/PR #336 and for
#: XASSET-0041/XASSET-0042.
PRIOR_RECONCILIATION_DECISION = "XASSET-0047"
PRIOR_RECONCILIATION_PULL_REQUEST = 347
PRIOR_RECONCILIATION_MERGE_SHA = "bb95ed26964b1bc7a2e230c76060fec82752efa1"
PRIOR_RECONCILIATION_ACCEPTED_HEAD = "8ae0988d4c1ffc551e7fa0a1d1ee1edfa7a49a9e"
PRIOR_RECONCILIATION_MERGE_BASE = "0b76c09f8d1aba01780b4f06fdd692f7393fbfd3"

#: Decisions whose own effectivity condition named an exact merge SHA whose merge-commit CI failed.
#: For each, that condition is PERMANENTLY unsatisfiable -- a green run at any other commit is
#: excluded by the condition's own words, not merely unpersuasive -- so none of them is effective
#: and none may ever supply authority. Enforced, not merely documented: see
#: :func:`_verify_recovery_lifecycle_anchor`.
PERMANENTLY_INEFFECTIVE_DECISIONS = frozenset(
    {STOPPED_REBINDING_DECISION, STOPPED_RECOVERY_AUTHORIZATION_DECISION}
)
#: The pull requests those stopped lifecycles ran in. An attestation naming either as its own
#: authorizing pull request is refused for the same reason.
PERMANENTLY_INEFFECTIVE_PULL_REQUESTS = frozenset(
    {STOPPED_REBINDING_PULL_REQUEST, STOPPED_RECOVERY_AUTHORIZATION_PULL_REQUEST}
)
#: Every failed merge-commit CI run in this chain, by exact ``(run, job, merge_sha)`` identity.
#: Retained so the record cannot be lost by omission, and so no future edit can quietly drop one
#: while leaving the prose that describes it. NOTHING here is ever consulted as evidence of
#: SUCCESS -- these are refusals, and :func:`_verify_recovery_lifecycle_anchor` uses them only to
#: reject a merge SHA that is already known to have failed its own merge-commit CI.
FAILED_MERGE_COMMIT_CI_RUNS = (
    (
        STOPPED_REBINDING_FAILED_CI_RUN,
        STOPPED_REBINDING_FAILED_CI_JOB,
        STOPPED_REBINDING_MERGE_SHA,
    ),
    (
        STOPPED_RECOVERY_AUTHORIZATION_FAILED_CI_RUN,
        STOPPED_RECOVERY_AUTHORIZATION_FAILED_CI_JOB,
        STOPPED_RECOVERY_AUTHORIZATION_MERGE_SHA,
    ),
)

#: The outcome-producing bytes PR #336 delivered. XASSET-0030 SS-G.B's invariant is that no
#: outcome-producing executable code may be created, changed, or left outside the bound execution
#: identity after the final rebinding -- so the rebinding proves these are BYTE-IDENTICAL across
#: the package's reviewed head, the package's merge, the successor's reviewed head, the successor's
#: merge, and the working tree. A silent runner edit smuggled into the rebinding fails closed.
#:
#: MAJOR 1 (FULL review 4965914272). ``level1_construction_universe_closure_validator.py`` was
#: missing from this tuple while being a DIRECT outcome-producing dependency: the runner imports it
#: as ``CU`` and calls ``generate_construction_universe``, ``frozen_construction_universe`` and
#: ``universe_aggregate_sha256`` to establish the actual 680-cell traversal, its exact order, the
#: frozen mapping, the per-construction identities, and the aggregate hash; the result validator
#: consumes the same module. It was already in :data:`LOAD_BEARING_RELPATHS`, but that boundary
#: compares only the successor's reviewed head, the successor's merge, and the working tree -- NOT
#: the two EXECUTABLE-PACKAGE anchors. Reproduced through the real mechanism before correcting:
#: withholding its blob at both package anchors, with every other input valid,
#: ``_verify_successor_rebinding_identity`` returned ``[]``. A coherent successor change to universe
#: traversal, ordering, the frozen mapping, or the aggregate hash -- accompanied by matching
#: successor load-bearing hashes -- would therefore not have violated the package binding. Its bytes
#: are in fact unchanged from the package through this head (SHA-256
#: ``1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5``); the defect was that the
#: invariant was not mechanically PROVEN. Listing it here corrects that at its source.
EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS = (
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    "level1_construction_universe_closure_validator.py",
)

# --------------------------------------------------------------------------------------
# The TRANSITIVE outcome-producing surface -- an EXACT CLOSED TRANSITION
# --------------------------------------------------------------------------------------
#
# The two paths above are not the whole outcome-producing surface. Both modules
# ``import level1_endpoint_evidence_preregistration_validator as PV`` and call its
# ``generate_cell_universe``, ``derive_candidate_disposition``, ``derive_cell_outcome``,
# ``derive_roll_up_outcome``, ``required_g2_gate_result`` and ``is_reading_dependent``, plus the
# gate/disposition/reading vocabularies those decisions are made against. That module therefore sits
# squarely on the path SS-G.B defines as outcome-producing: it DECIDES and ORDERS the 680 outcomes.
#
# WHY NOT WHOLE-FILE EQUALITY AGAINST THE PACKAGE. That module also carries authorization-only code
# -- the canonical lifecycle constants, the pin-succession checks, the rebinding block validator --
# which THIS rebinding must lawfully change. Requiring whole-file equality with the package would
# make a lawful rebinding impossible.
#
# WHY NOT A SEMANTIC PROJECTION. Review 4963386313 established that the predecessor mechanism -- a
# deterministic AST projection of the outcome-determining symbols plus their ambient bindings -- was
# NONCONVERGENT. To decide "did the outcome surface change" from source text alone, it had to decide
# arbitrary Python runtime behaviour statically: reachability through aliases, containers, call
# results and higher-order builtins; callback invocation; attributed local-class members;
# descriptors; decorators; class construction AND class-creation hooks; namespace effects; and
# deferred execution. Four independent reviews closed sixteen distinct bypass forms and each one
# produced new ones, because the underlying question is undecidable, not merely unimplemented.
# Correction-by-example cannot terminate against an adversary who may write any Python.
#
# WHAT IS ENFORCED INSTEAD. A FINITE proposition, decided by byte identity alone:
#
#     these exact accepted package bytes became these exact successor bytes
#     through only this exact reviewed transition.
#
# Both complete blobs are pinned. Between them sits a CLOSED, ORDERED manifest of the reviewed
# replacement regions, each recording exact byte offsets, exact lengths, and the cryptographic
# identity of the package bytes it replaces and the successor bytes it installs. Every span outside
# a declared region must be byte-identical, both files must be consumed completely, and no gap,
# overlap, duplicate, reordering, resizing, addition, or removal is tolerated. Any other byte change
# anywhere -- including a change INSIDE a declared region that is not exactly the authorized
# successor bytes -- fails closed.
#
# The authorization boundary is bytes: no AST interpretation, no import or execution of the audited
# module, no ``eval``, no ``difflib``, and no version-dependent diff algorithm participates. The
# manifest is a frozen constant, and this module verifies it by comparison only.
#
# HONEST SCOPE. This does NOT prove Python semantic equivalence, and does not claim to. It proves
# exact reviewed byte identity plus an exact closed transition -- which is a stronger and, unlike
# the projection, a DECIDABLE claim. What the reviewed transition means was settled by review, not
# by a parser.

#: The module carrying the imported derivation surface.
OUTCOME_PRODUCING_DERIVATION_RELPATH = "level1_endpoint_evidence_preregistration_validator.py"

#: The COMPLETE accepted executable-package blob (PR #336 accepted head and merge) and the COMPLETE
#: successor blob this rebinding reviews. Independently recomputed from the git objects at both
#: package anchors and at the successor head.
OUTCOME_PRODUCING_PACKAGE_SHA256 = (
    "840b558b9923b9a6fa480146a192ce0cb92b81de71448bf2c9896ee9225883b7"
)
OUTCOME_PRODUCING_PACKAGE_LENGTH = 147967
OUTCOME_PRODUCING_SUCCESSOR_SHA256 = (
    "2b8ead2b0d661ddd14fa6019ee1802fe49900a214ec443228636701edeb3d356"
)
OUTCOME_PRODUCING_SUCCESSOR_LENGTH = 161232

#: The CLOSED, ORDERED transition. Seventeen replacement regions, each
#: ``(package_offset, package_length, package_sha256, successor_offset, successor_length,
#: successor_sha256)``, ordered by package offset. Everything not named here must be byte-identical
#: in both files. Together with the two whole-blob pins above, this is the entire authorization
#: boundary for the derivation module.
#:
#: Every region is confined to XASSET-0037 lifecycle constants, pin succession, canonical
#: validation, or successor-rebinding validation. No region alters an outcome-consumed symbol: all
#: twenty-six symbols the runner and result validator import are structurally identical across the
#: two blobs, verified independently in the test module rather than asserted here.
OUTCOME_PRODUCING_TRANSITION: tuple[tuple[int, int, str, int, int, str], ...] = (
    (2447, 76, "f5d2f6298222b03724d8bd17fb7f24413fc91a714f0abddd14af170edfece78c",
     2447, 222, "95fdb59a97f56a58acfa3db5f3c59953c05c8e8fb66bc5801e7772ba70082f2f"),
    (2665, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     2811, 224, "3d59d54b4f302ba6a00a30bf945fc55a0a94d90c6b10c135e25625e9cdc99ba8"),
    (2692, 94, "7d485b65b4acd0d318bec20d45774709e9b177bf2bba4918cdfa8c1b81d11a4b",
     3062, 94, "1e6dad91b2540a29ec753f75eec6f501f92e75aa0b4f55a644983c1bcdfa7b2f"),
    (11018, 339, "1ed43083907435324367a13c828e8cee71f6bceffc839bf3335b4f136d8808c1",
     11388, 544, "f52f965396ce53a8894027b645de48d1294b5393cb3ad4fd91fc28c04b567290"),
    (11392, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     11967, 250, "09f5cc8bce2a442c721e1b507473555f22e14635b10f76f3ea4f37db501540e1"),
    (11697, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     12522, 145, "c91695cda27443df537e78c6e1c36b9bfc275d7612c9478c018c49c374a97347"),
    (12046, 142, "0d04bc11ff13276ef533d05c831afa4e8268bc3388ca5348a7471fbd4cb0e9ca",
     13016, 2196, "bba4460251e0ed7a13b898d7864b62fa4dd949d0256baec9cf17f898f52bfe8f"),
    (13736, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     16760, 471, "c850053a7f943ca1865c21d1bc19df9ae20d6756ab8d8b02731dd4ce7d29a5c3"),
    (35126, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     38621, 189, "1435764c91084d59d88f0200258151c3b66956c80cd0cad35ec4395f7c0b8546"),
    (35175, 23, "347dd3a6b3cbdb7729e12f6c473af8fbed54c09a05cf17cfa451378c7ff3db56",
     38859, 56, "327c635dfef43343e8d540cb27c2111e336dea977b405068af04c3d5f1ab7962"),
    (35280, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     38997, 470, "d5b7deb28ad2059e08922b6d5725f2a7a391461775bb3fd6a7b6d363786e054e"),
    (37561, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     41748, 4437, "83f3aa63bd96c0b8660ed4aa05c99713c04aa8eba298d8b4f5ca6fb6f7df4843"),
    (131872, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     140496, 620, "06237b012cd85eee1d475a339daadb0e581a54f2c64cbc381ead1b9d649f180e"),
    (135627, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     144871, 489, "be02a42aa485b8d2c5b863109c602b4242db80d1639c726d8ad6e09864b0b055"),
    (137239, 507, "a0a4197a9ab965984e1b82b3313b78d7b09286a6e805bb709575f7172d6b51f7",
     146972, 919, "122525fda0e596593f4c497b1871415cdb81587734d9b684b2ef05f90e35edf3"),
    (144723, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     154868, 2574, "a0375e1c5edc67b5b475f3c6ae96e4601707dd2c97ff135bca8102942cc7df76"),
    (147193, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     159912, 546, "9275d8b0d7ae70be0cbd59f1d476c53159bc9c0f50ca9e85a59885e2e75a5054"),
)


# --------------------------------------------------------------------------------------
# XASSET-0044 / XASSET-0043 SS-G.4a — a SECOND exact closed transition, APPENDED
# --------------------------------------------------------------------------------------
#
# XASSET-0043 SS-G.4a states why this is required rather than optional. Whole-file equality is the
# wrong instrument for this ONE file, and XASSET-0037 SS-D.1 said so before XASSET-0043 existed: the
# same module also carries the canonical lifecycle constants and the pin-succession and
# rebinding-block validators -- authorization-only code a lawful rebinding MUST change. Freezing it
# whole-file and permitting the SS-J canonical amendment are not jointly satisfiable, and that was
# reproduced rather than argued: with the frozen module in place, advancing only
# ``rebound_by``, ``effective_structural_authorization_source`` and
# ``stage_1_executability.blocking_prerequisite`` produced exactly those three validation errors,
# because the module hard-codes XASSET-0037 in precisely the fields the successor must advance.
#
# THE FIRST LINK IS PRESERVED, NOT REPLACED. ``OUTCOME_PRODUCING_PACKAGE_SHA256``,
# ``OUTCOME_PRODUCING_SUCCESSOR_SHA256``, both lengths, and the seventeen-region
# ``OUTCOME_PRODUCING_TRANSITION`` above are untouched and still verified at the XASSET-0036 package
# anchors and at XASSET-0037's own anchors. The chain is now
#
#     package -> successor -> rebound
#
# with each link a separate frozen manifest. The new link never subsumes the first, and every
# constraint that governs link 1 governs link 2 identically: exact source and target offsets, exact
# lengths, the SHA-256 of the bytes replaced and the bytes installed, byte-identity everywhere
# outside a declared region, complete consumption of both blobs, and no gap, overlap, duplicate,
# reordering, resizing, addition, or removal.
#
# EVERY DECLARED REGION LIES INSIDE THE AUTHORIZATION-ONLY SURFACE: successor-lifecycle constants,
# canonical validation of those constants, pin succession, and rebinding-block validation. The
# consumer-reachable and outcome-producing definitions -- every symbol the runner and the result
# validator import, and everything those symbols reach -- are re-proved unchanged semantically and
# byte-identically in the supporting test module, derived from the consumers' own source rather
# than asserted here, exactly as XASSET-0037 SS-D.1's evidence check already does.

#: The COMPLETE accepted successor blob (the transition's starting bytes for link 2) and the
#: COMPLETE rebound blob this rebinding reviews. Independently recomputed from the git objects at
#: BOTH XASSET-0037 anchors, which were required to agree, and from the working tree.
OUTCOME_PRODUCING_REBOUND_SHA256 = (
    "b3a87e4f8b828d420795348642c977a9f0585eafa9262a4be48df406f770233d"
)
OUTCOME_PRODUCING_REBOUND_LENGTH = 169058

#: The CLOSED, ORDERED transition for link 2. Twenty-three replacement regions, each
#: ``(successor_offset, successor_length, successor_sha256, rebound_offset, rebound_length,
#: rebound_sha256)``, ordered by successor offset. Everything not named here is byte-identical in
#: both blobs.
OUTCOME_PRODUCING_REBOUND_TRANSITION: tuple[tuple[int, int, str, int, int, str], ...] = (
    (2811, 76, "d6f3da6fd8ff4d67e8769a9cad19874b27853a2f151fd629e2d5a76bde9289f1",
     2811, 269, "8a460e6c432b04a0cb36aadd5194f96da6c54d3e5a513fd0d624e2ea75d6206d"),
    (3032, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     3225, 439, "cba8198832f7d801d4e0a44afdcd6422ecf344e941fe09145fa2df43c68bf328"),
    (11967, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     12599, 250, "33265ab88f716f50b2837ee17f7e811ec9b6f71c9987262fb126a6f4a52b3cb5"),
    (12522, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     13404, 145, "08204ebe1ff2722e90a12465204b4b29ad39e4db77cce3e3c95c4b39a4efb6b9"),
    (13324, 115, "ebadfa6f4b706ec1078d843a3192dcb4344c4af3fb8b47933128ecdf36c3fd17",
     14351, 438, "3765a94aedcdaca872acf5c0845ca0aec917d4adad94a4b625f7f13ac5163f0c"),
    (14019, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     15369, 494, "7a311577e33cb5cb0aaaebaca5ddedd2e96a15aef7a6108276a284e82963db41"),
    (36755, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     38599, 702, "6e118e3cf051994f4d8291fa1e8c8687a9e32f6262058b16d226f9b47074c2f2"),
    (42998, 102, "8e9ec242b4254d53a30eabfa5a4c75112c2e2d31a671ff99d4c3bf97b6137714",
     45544, 299, "ecb4ca979c184c6ab4a2a9f0b7ca4714a5eb80338a940b20916b1391c00a41a6"),
    (43158, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     45901, 412, "66b64ce0a98b16ae859731bff9b967bb9bf87b45e158f4478fd5050442c86f69"),
    (43195, 40, "f9ad71ac448db8218e9f545dd6b4aadad7664d7c3599dfe29692deec6cbfdbb6",
     46350, 547, "a702abbfd56552609acbff117f8e84c365547d80f10791821ca8f9d8f7cd4762"),
    (145360, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     149022, 455, "b436d4c3369a9a57ce831dc69677098487f89bc387d655d035ea2da39ff81f4a"),
    (147318, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     151435, 47, "78a06a4104a008e29fc36f40d42ceed49a1f2213a4f58ec1c75aa997547ca688"),
    (155142, 95, "4373effa1f067adebca7ebe56f799d0922beda4d07e9812db71d326886490eae",
     159306, 59, "c42f0efe96f6333042d682be654751ae4f0ba068f9214410e6cce1e022a19bb2"),
    (155238, 271, "d5ea2aa04efc45f1077c0ce5e7bad603372e2515bcb40035d5c72d4eebeac75b",
     159366, 652, "728141246a7de0ada8ebe44cb3631faa36dce78c2be61b53ed3f465efc536d99"),
    (155677, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     160186, 177, "957c431159a44752a0415981ed06857ef910f42bf9552c5656837a23af6aff47"),
    (155685, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     160371, 91, "98367e5568157baaf3450ee64ff03a3b9fcbc8c5ee9e261f3d51636ecf58074a"),
    (156234, 123, "5c5f0167d99ef99f899fd46064e6d265ee9102e768fa94e5f18862d60df212b3",
     161011, 62, "5fd358f2ac3ea4dd050c8ad4b5593d5e2ae160769d78b76e096471a9083a6c1f"),
    (156388, 35, "2d807aa4c340379425c0b09a246f68a923621cb2a28ab8af19a83fd45bdd0ccc",
     161104, 37, "fa81ae5b00c8e1c3db65ead89b37fa8e0bd85b1951bd1fe5b9292c0a81fd8cdd"),
    (156515, 31, "5cc0bc72c5cbda1af1335ed3c347201f16293045c09151f943812c251e261050",
     161233, 29, "a34a79fefeb4461716cbb9c7e2a655153980eff9a426b72d1f699cabb264149c"),
    (156573, 91, "03482067141b9633c438a691f4bb4a14ab243ce126a46f704ef8d4f02eaea479",
     161289, 172, "1d076b31df19b529a23135aa9869ecbea4ec0fe9dd0687f98725680e1526b6ce"),
    (157371, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     162168, 2521, "0aea9d5ea95f0f1d5461a2cfbc12ce05928733387cd8b39ead737f752ae7aa7d"),
    (159912, 223, "7801a40ff321326c9593b59cd7583b546068027ef8c0ab7b0917bcbc08620512",
     167230, 185, "1a05cccd9b122ff6172b001544ae0c5bfacf3ad275803188df2b03ba5a8c4c1b"),
    (160457, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     167737, 546, "d730d582616cba5be0845b102acca0b46c92f581c1dfaee7fcbcfa371ffec073"),
)


CONSTRUCTION_UNIVERSE_SHA256 = (
    "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
)
CONSTRUCTION_COUNT = 680
CONSTRUCTION_CELL_COUNT = 48

CANONICAL_PROTOCOL_RELPATH = "research/level1_endpoint_evidence/PROTOCOL_V1.md"
CANONICAL_PREREGISTRATION_RELPATH = "research/level1_endpoint_evidence/pre_registration.yaml"

PROTOCOL_PATH = ROOT / CANONICAL_PROTOCOL_RELPATH
PREREGISTRATION_PATH = ROOT / CANONICAL_PREREGISTRATION_RELPATH

#: EFFECTIVE pins for the canonical bytes, recomputed ONCE under XASSET-0044 after every permitted
#: canonical and enforcement byte stabilized -- never mid-correction, and never carried forward from
#: a superseded head. That ordering is XASSET-0043 SS-G.6, and it is the exact failure XASSET-0042's
#: second bounded correction had to repair. Separate files from this module, so there is no
#: self-hashing circularity.
CANONICAL_PINS: dict[str, str] = {
    CANONICAL_PROTOCOL_RELPATH: (
        "1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84"
    ),
    CANONICAL_PREREGISTRATION_RELPATH: (
        "898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f"
    ),
}

#: XASSET-0044's pins, retained as historical identity by XASSET-0047, written as INDEPENDENT
#: LITERALS -- exactly like every predecessor mapping below, and deliberately NOT derived from
#: :data:`CANONICAL_PINS`.
#:
#: MAJOR 1 (review 4997532748): this was ``dict(CANONICAL_PINS)``, which made the succession
#: refusal source-vacuous. Reproduced before correcting: a SOURCE-LEVEL edit to one current pin
#: literal was rebuilt into this mapping during import, the two stayed equal, and the refusal
#: returned clean -- so the check detected only a post-import monkeypatch of one name, never the
#: edit it claims to prevent. A historical identity copied from the thing it is supposed to
#: outlive cannot prove succession, because it has no independent existence to compare against.
#:
#: The VALUES are currently identical to :data:`CANONICAL_PINS`, and that remains a FACT rather
#: than an oversight: XASSET-0046 SS-G.9 freezes the canonical inputs, this recovery amends none
#: of them, and XASSET-0044 is still the last decision that changed those bytes. Being equal in
#: value is not the defect; being equal BY CONSTRUCTION was. Written out here, the equality is a
#: verifiable claim that a future canonical amendment must break loudly -- which is precisely what
#: forces that amendment to extend the succession machinery instead of copying a pin forward.
XASSET_0044_CANONICAL_PINS = {
    CANONICAL_PROTOCOL_RELPATH: (
        "1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84"
    ),
    CANONICAL_PREREGISTRATION_RELPATH: (
        "898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f"
    ),
}

#: XASSET-0037's pins, retained as predecessor identity now that XASSET-0044 amends the canonical
#: authorization language under successor authority. They no longer describe the current files and
#: must NOT be rewritten to pretend otherwise -- the same treatment XASSET-0037 gave XASSET-0036's,
#: XASSET-0036 gave XASSET-0029's, XASSET-0029 gave XASSET-0028's, and XASSET-0028 gave
#: XASSET-0027's.
XASSET_0037_CANONICAL_PINS = {
    CANONICAL_PROTOCOL_RELPATH: (
        "367583b616e1c6ab614bcf67d451fe27ce40507d073374190c57291e761d8971"
    ),
    CANONICAL_PREREGISTRATION_RELPATH: (
        "768b013c0129f02577fea3c2a1a3100b4340b9a42f48ee0d0dbd6e671894bce1"
    ),
}

#: The XASSET-0036 executable package's V6 pins, retained as predecessor identity now that
#: XASSET-0037 amends the canonical authorization language under successor authority. They no
#: longer describe the current files and must NOT be rewritten to pretend otherwise -- the same
#: treatment XASSET-0036 gave XASSET-0029's, XASSET-0029 gave XASSET-0028's, and XASSET-0028 gave
#: XASSET-0027's.
XASSET_0036_PACKAGE_CANONICAL_PINS = {
    CANONICAL_PROTOCOL_RELPATH: (
        "86b2a5e8674247698ac592ce4734744f940b4a119ffda5fd702bc3cbf3e40c13"
    ),
    CANONICAL_PREREGISTRATION_RELPATH: (
        "e993df9f41d2f5352e51c9921dd006d50ab69518a730d37def106696b3f149d4"
    ),
}

#: XASSET-0029's pins, retained as predecessor identity now that XASSET-0036's executable package
#: amends the canonical bytes under successor authority. History is never invalidated.
XASSET_0029_CANONICAL_PINS = {
    CANONICAL_PROTOCOL_RELPATH: (
        "6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb"
    ),
    CANONICAL_PREREGISTRATION_RELPATH: (
        "6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c"
    ),
}

#: XASSET-0028's pins, retained as predecessor identity. History is never invalidated.
PREDECESSOR_CANONICAL_PINS = {
    CANONICAL_PROTOCOL_RELPATH: (
        "c02b4d519267b96ddb12500e6d1d55a47aeafd9437de8e41014c8871f631618c"
    ),
    CANONICAL_PREREGISTRATION_RELPATH: (
        "ffde86c1585050b2bf89e58033f37777a903ace86e97be46b6440a217c78ec4a"
    ),
}

#: MAJOR 1: load-bearing enforcement code. Expected identity is DERIVED FROM THE MERGED GIT
#: TREE at validation time, never from a hard-coded constant here -- a literal would have to
#: be edited in the same commit that changes the bytes it claims to verify, which is not a
#: check. Drift in any of these between the accepted/merged tree and the working tree is
#: refused.
#
# EXTENDED BY XASSET-0036 SS-E.6 / XASSET-0030 SS-G.B step 5. The prior set contained exactly six
# paths and NO outcome-producing code, because none existed when XASSET-0029 was accepted. An
# attestation could therefore have been perfectly authenticated while the code generating every one
# of the 680 dispositions was unbound, and ATTEMPT_1 is non-rerunnable after claim.
#
# The three added paths are exactly those whose bytes can materially decide, order, map, derive,
# serialize, write, or validate a Stage-1 outcome:
#   * the runner -- decides ordering, applies B1/B2/B3, composes dispositions, serializes, writes;
#   * the result validator -- decides whether a candidate result document may be published;
#   * XASSET-0036 itself -- the decision authorizing the package, on the same footing XASSET-0029
#     already occupies for its own authorization.
#
# The EXISTING exact-byte mechanism is reused unchanged (XASSET-0036 SS-E.6 states a preference for
# it, and no concrete technical reason to depart was found): expected identity is still DERIVED
# FROM THE MERGED GIT TREE at validation time, never from a hard-coded constant here.
#
# EXTENDED AGAIN BY XASSET-0037 / SS-G.B step 8, 9 -> 10. NOTHING IS REMOVED and no exact-byte check
# is weakened. The single addition is the XASSET-0037 decision itself, on exactly the footing
# XASSET-0029 and XASSET-0036 already occupy for their own authorizations: the decision that
# supplies the effective structural authorization must be inside the identity it authorizes, or an
# attestation could authenticate perfectly while its own governing text had been edited afterwards.
#
# What that rebinding changed was not this tuple's mechanism but the TREE it is proven against: the
# ten paths were verified in the XASSET-0037 merged tree and its independently reviewed head,
# rather than the obsolete XASSET-0029 tree in which three of them do not exist at all. XASSET-0044
# has since moved that tree again -- see the next block -- without changing the mechanism either.
#
# EXTENDED AGAIN BY XASSET-0044 / XASSET-0030 SS-D, 10 -> 14. NOTHING IS REMOVED, no existing
# identity is altered, and no exact-byte check is weakened -- the pin-succession refusal is
# EXTENDED to XASSET-0037's own accepted pins rather than relaxed.
#
# XASSET-0037 SS-E's principle is that the decision supplying the effective structural authorization
# must sit inside the identity it authorizes, or an attestation could authenticate perfectly while
# its own governing text had been edited afterwards. Applied honestly, that principle reaches FOUR
# files here rather than one, because after this rebinding four decisions JOINTLY make the corrected
# bytes lawful, and any of them left outside the boundary stays editable after attestation:
#
#   * XASSET-0041 -- authorized the actor-evidence correction;
#   * XASSET-0042 -- implemented it, and records the corrected module's identity being rebound;
#   * XASSET-0043 -- the authority for this rebinding itself;
#   * XASSET-0044 -- this decision, the effective structural authorization source after it.
#
# DIRECT MEMBERSHIP, NOT AN EQUIVALENT. Each of the four joins this tuple and is verified by the
# existing exact-byte mechanism, whose expected identity is derived from the merged git tree at
# validation time. A decision that merely DESCRIBES or CITES predecessor text does not byte-bind it,
# and citing XASSET-0041 or XASSET-0042 inside this decision would NOT be a binding of those files.
# XASSET-0036 SS-E.6's stated preference for the existing mechanism holds, and no concrete technical
# reason to depart from it was found.
LOAD_BEARING_RELPATHS = (
    "level1_stage1_execution_authorization.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_construction_universe_closure_validator.py",
    "level1_stage1_runner.py",
    "level1_stage1_result_validator.py",
    CANONICAL_PROTOCOL_RELPATH,
    CANONICAL_PREREGISTRATION_RELPATH,
    "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
    "governance/decisions/XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
    "governance/decisions/XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md",
    "governance/decisions/"
    "XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md",
    "governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md",
    "governance/decisions/"
    "XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md",
    "governance/decisions/"
    "XASSET-0044-endpoint-0001-stage-1-post-correction-operational-rebinding.md",
    # EXTENDED AGAIN BY XASSET-0047 / XASSET-0046 SS-G.6, 14 -> 16. NOTHING IS REMOVED, no existing
    # identity is altered, and no exact-byte check is weakened. XASSET-0037 SS-E's principle -- the
    # decision supplying the effective structural authorization must sit INSIDE the identity it
    # authorizes, or an attestation could authenticate perfectly while its own governing text had
    # been edited afterwards -- reaches exactly two further files once the anchor moves:
    #
    #   * XASSET-0046 -- the authority for this recovery, on precisely the footing XASSET-0043
    #     already occupies for the rebinding it authorized;
    #   * XASSET-0047 -- this decision, the effective structural authorization source after it.
    #
    # XASSET-0044's own decision file STAYS, exactly where XASSET-0044 put it. A stopped lifecycle
    # is not an invalidated one, and a path traded away is the defect this boundary exists to catch.
    # XASSET-0045's decision file is deliberately NOT added: it authorizes nothing, so binding it
    # would assert an authority relationship that does not exist.
    "governance/decisions/"
    "XASSET-0046-endpoint-0001-stage-1-post-merge-ci-recovery-reauthorization.md",
    "governance/decisions/"
    "XASSET-0047-endpoint-0001-stage-1-post-merge-ci-recovery-reconciliation.md",
    # EXTENDED AGAIN BY XASSET-0049 / XASSET-0048 SS-E.4 and SS-F.6, 16 -> 18. ADDITIVE ONLY:
    # NOTHING IS REMOVED, no existing member is altered or reordered, no path is swapped or traded
    # away, and no exact-byte check is weakened. XASSET-0037 SS-E's principle -- the decision
    # supplying the effective structural authorization must sit INSIDE the identity it authorizes,
    # or an attestation could authenticate perfectly while its own governing text had been edited
    # afterwards -- reaches exactly two further files once the anchor moves:
    #
    #   * XASSET-0048 -- the authority for this step-8-equivalent rebinding, on precisely the
    #     footing XASSET-0043 occupies for the rebinding it authorized and XASSET-0046 for the
    #     recovery it authorized;
    #   * XASSET-0049 -- this decision, the effective structural authorization source after it.
    #
    # Reproduced before extending: neither file appeared anywhere in this tuple, so both sat
    # OUTSIDE the identity they make lawful and were editable after attestation.
    #
    # XASSET-0044's own decision file STAYS, exactly where XASSET-0044 put it, and so does
    # XASSET-0047's. A stopped lifecycle is not an invalidated one, and a superseded anchor is not
    # a retired one; a path traded away is the defect this boundary exists to catch. XASSET-0045's
    # decision file remains deliberately ABSENT for the reason XASSET-0047 gave: it authorizes
    # nothing, so binding it would assert an authority relationship that does not exist.
    "governance/decisions/"
    "XASSET-0048-endpoint-0001-stage-1-step-8-equivalent-rebinding-authorization.md",
    "governance/decisions/"
    "XASSET-0049-endpoint-0001-stage-1-step-8-equivalent-successor-operational-rebinding.md",
)

# ======================================================================================
# Lane storage — deliberately OUTSIDE the repository
# ======================================================================================

#: Outside the repository so no lane record can be committed, reviewed into existence, or
#: forged into a pull request. Deliberately NOT the RISK-0001 results location, which this
#: module never reads or references.
AUTHORIZATION_ROOT = Path("/var/tmp/phq-endpoint0001-stage1-authorization")
AUTHORIZATION_PATH = AUTHORIZATION_ROOT / "authorization.json"
CLAIM_PATH = AUTHORIZATION_ROOT / "claim.json"
COMPLETION_PATH = AUTHORIZATION_ROOT / "completion.json"
LEDGER_PATH = AUTHORIZATION_ROOT / "lane_ledger.jsonl"

# ======================================================================================
# Vocabulary
# ======================================================================================

REQUIRED_LIFECYCLE_GATES = (
    "INDEPENDENT_FULL_EXACT_HEAD_REVIEW",
    "PRINCIPAL_EXACT_HEAD_ACCEPTANCE",
    "MERGE",
    "POST_MERGE_VERIFICATION",
    "MERGE_COMMIT_CI_SUCCESS",
    "MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION",
)

AUTHORIZATION_MECHANISM = "EXTERNAL_ONE_SHOT_PREEXECUTION_ATTESTATION"
APPROVING_REVIEW_DISPOSITION = "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"

#: BLOCKING 2 (review 4946464366): the GitHub account that performs principal acceptance and
#: post-merge verification in this repository. Previously the acceptance and post-merge gates
#: checked only comment location and body text, so ANY account able to comment on the pull
#: request could impersonate them. This repository's principal, merge, and lifecycle-operator
#: account is the same login throughout its recorded history -- stated here honestly rather than
#: implying separate accounts exist.
PRINCIPAL_ACCOUNT_LOGIN = "Mast3rkey"
LIFECYCLE_OPERATOR_LOGIN = "Mast3rkey"

#: MAJOR 1: the repository's review grammar. The formal disposition is the FIRST formal line and
#: must match EXACTLY -- a substring test let an adverse review pass merely by containing the
#: approval phrase in later explanatory text.
FORMAL_DISPOSITION_PREFIX = "FORMAL DISPOSITION:"

#: GitHub's own review states. The NATIVE state is durable truth and is evaluated independently of
#: the repository's body grammar, so a later CHANGES_REQUESTED is adverse even with no formal line.
NATIVE_ADVERSE_REVIEW_STATES = frozenset({"CHANGES_REQUESTED"})

#: States that mechanically prove a later review is NOT an adverse finding. Anything outside both
#: sets, with no parseable formal disposition, is unclassifiable and fails closed.
NATIVE_NON_ADVERSE_REVIEW_STATES = frozenset({"APPROVED"})
SCHEMA_VERSION = 2

LANE_ABSENT = "ABSENT"
LANE_READY = "READY"
LANE_CLAIMED = "CLAIMED"
LANE_COMPLETED = "COMPLETED"

# Not a lane state: the marker :func:`_read_ledger` substitutes for any line it cannot read as
# exactly one mapping. Named because three separate sites must agree on it, and a divergence
# between them is precisely how MINOR 1 (review 4946706062) went unnoticed.
LEDGER_CORRUPT = "CORRUPT"

REQUIRED_TOP_KEYS = (
    "schema_version",
    "mechanism",
    "repository",
    "study_id",
    "authorizing_decision",
    "authorizing_pull_request",
    "predecessor_decision",
    "execution_attempt_id",
    "authorization_head",
    "predecessor_identity",
    # XASSET-0037. Three SEPARATE blocks, deliberately not folded into ``predecessor_identity``:
    # that field means XASSET-0028's structural closure and nothing else.
    "historical_operational_authorization",
    "package_authorization",
    "executable_package_identity",
    # XASSET-0044. THREE further separate blocks, on exactly the same footing and for exactly the
    # same reason: the prior rebinding, the authority that authorized the correction, the corrected
    # module itself, and the authority that authorized THIS rebinding are four different
    # relationships, and folding any of them together is how a rebinding starts binding the wrong
    # tree. ``correction_identity`` carries both the correction's authority and its merged tree,
    # which are distinguished by their own field names within the block.
    "prior_successor_rebinding",
    "correction_identity",
    "rebinding_authorization_identity",
    # XASSET-0047. TWO further separate blocks, for the same anti-overloading reason and one new
    # one. ``recovery_authorization_identity`` is the authority for THIS unit and is a different
    # relationship from every authority above it. ``stopped_lifecycle_identity`` is not an
    # authority at all: it records, by exact identity, the two merged lifecycles that STOPPED at
    # their own merge-commit CI, so an attestation cannot be assembled that quietly omits them,
    # renames them, or describes either failed run as anything other than failed.
    "recovery_authorization_identity",
    "stopped_lifecycle_identity",
    # XASSET-0049. TWO further separate blocks, for the same anti-overloading reason.
    # ``step8_equivalent_authorization_identity`` is the authority for THIS unit and is a different
    # relationship from every authority above it. ``prior_reconciliation_identity`` is the CLOSED
    # predecessor anchor this unit supersedes -- a real, completed lifecycle, and emphatically NOT
    # one of the stopped ones -- carried so an attestation cannot be assembled that quietly omits
    # the anchor it replaced.
    "step8_equivalent_authorization_identity",
    "prior_reconciliation_identity",
    "canonical_pins",
    "construction_universe",
    "lifecycle_evidence",
    "load_bearing_identity",
    "author_identity",
    "generated_at_utc",
)

REQUIRED_LIFECYCLE_EVIDENCE_KEYS = (
    "independent_review",
    "principal_acceptance",
    "merge",
    "post_merge_verification",
    "merge_commit_ci",
    # BLOCKING 1 (review 4986931575). XASSET-0044 SS-L makes SEVEN conditions conjunctively
    # necessary, and its seventh is "final post-CI verification and lifecycle closure". The five
    # keys above carry conditions 1-6; the seventh had NO evidence key and NO gate, so a document
    # naming no closure at all validated -- allowing an attestation to be written after CI but
    # before the decision it cites is effective. Reproduced through the public path before this
    # correction: build_authorization_payload + validate_authorization_document returned valid
    # with zero closure evidence.
    #
    # Deliberately NOT added to REQUIRED_LIFECYCLE_GATES. That tuple is a differently-scoped list
    # -- six gates that are not in 1:1 correspondence with SS-L's seven conditions (SS-L 1 and 2
    # both close the single review gate, and MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION
    # answers to no SS-L condition at all) -- and it is named verbatim by the canonical
    # ``..._LIFECYCLE_CLOSURE_ALL_SIX_GATES_...`` strings and by every predecessor-named history
    # field beside them. Renaming those to "SEVEN" would rewrite accepted predecessor semantics to
    # fix a hole that is closed here exactly, so the six-gate list and the canonical strings are
    # left byte-identical and the seventh condition is authenticated on its own footing.
    "lifecycle_closure",
)

#: MINOR 1 (delta review 4987958687): the operator-facing statement of XASSET-0044 SS-L's SEVENTH
#: condition. It lives beside the schema it describes, and is spliced into the CURRENT no-attestation
#: status reason so that reason states what Gate 8 actually enforces. It is deliberately NOT added to
#: ``REQUIRED_LIFECYCLE_GATES`` and does not alter any canonical ``..._ALL_SIX_GATES_...`` string:
#: those name an accepted, differently-scoped, historically-referenced list and stay byte-identical.
LIFECYCLE_CLOSURE_STATUS_REQUIREMENT = (
    "FINAL POST-CI LIFECYCLE CLOSURE is additionally mandatory -- a durable closure record on the "
    "authorizing pull request, authored by the lifecycle operator, naming the exact merge SHA and "
    "the exact merge-commit CI run and job, recorded strictly after both the post-merge "
    "verification and the completion of that CI job"
)

#: The keys a ``lifecycle_closure`` record may carry. Closed: an unknown key is refused rather
#: than ignored, so a closure record cannot smuggle an unverified field past the gate.
LIFECYCLE_CLOSURE_KEYS = (
    "comment_id",
    "closed_merge_sha",
    "closed_run_id",
    "closed_job_id",
)


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()


# ======================================================================================
# Primitives
# ======================================================================================


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def stage1_result_identity(results: Any) -> str:
    """THE deterministic Stage-1 result SEMANTIC identity. One mechanism, every consumer.

    MAJOR 3 (review 4946464366): the canonical contract previously called this
    ``EXACT_RESULT_ARTIFACT_SHA256``, which was not truthful -- this is NOT the SHA-256 of the
    ``stage1_results.yaml`` file bytes. It is the SHA-256 of the canonical JSON serialization of
    the parsed result mapping, deliberately chosen so that key ordering and insignificant
    whitespace do not change identity while any content change does. Canonical wording is
    renamed to EXACT_STAGE1_RESULT_SEMANTIC_IDENTITY_SHA256 to match what the code computes.

    BLOCKING 2 (review 4946397399): completion recorded a result hash that nothing ever
    checked, so completing result A did not prevent publishing result B. This function is the
    single identity used by the future Stage-1 result writer, by ``complete_execution``, and by
    the PUBLIC ``validate_stage1_results`` gate, so "the exact completed artifact" is a
    mechanically decidable question rather than a promise.

    It hashes the canonical JSON serialization, so key order and insignificant whitespace do not
    change identity while any content change does. It invents no economic content.
    """
    return sha256_bytes(canonical_json(results).encode("utf-8"))


class TransitionError(ValueError):
    """The exact package-to-successor transition could not be proven.

    Raised only by :func:`verify_exact_transition`. Every path is fail-closed: an unreadable blob,
    a wrong length, a wrong whole-blob digest, a malformed manifest, a region that does not carry
    its declared bytes, a span outside the declared regions that is not byte-identical, or bytes
    left unconsumed at either end all raise rather than returning a verdict.
    """


def verify_exact_transition(
    package: bytes,
    successor: bytes,
    transition: Sequence[tuple[int, int, str, int, int, str]] = OUTCOME_PRODUCING_TRANSITION,
    *,
    package_length: int = OUTCOME_PRODUCING_PACKAGE_LENGTH,
    package_sha256: str = OUTCOME_PRODUCING_PACKAGE_SHA256,
    successor_length: int = OUTCOME_PRODUCING_SUCCESSOR_LENGTH,
    successor_sha256: str = OUTCOME_PRODUCING_SUCCESSOR_SHA256,
) -> None:
    """Prove ``package`` became ``successor`` through EXACTLY ``transition``, or raise.

    Byte identity is the whole instrument. No parsing, importing, executing, ``eval``, ``difflib``,
    or version-dependent diff algorithm participates, so the answer does not vary with interpreter
    version, library version, or anyone's ability to model Python's runtime.

    Enforced, in order:

    1. both blobs carry their pinned lengths and pinned whole-blob digests;
    2. the manifest is well-formed -- ordered, non-overlapping in BOTH files, no region empty on
       both sides, and offsets/lengths inside their file;
    3. every span BETWEEN declared regions is byte-identical in both files, and so is the span
       before the first region and after the last;
    4. every declared region carries exactly its declared package bytes and exactly its declared
       successor bytes, by digest;
    5. both files are consumed completely -- no undeclared trailing bytes on either side.

    Adding, removing, reordering, resizing, duplicating, overlapping, or gapping a region breaks
    (2) or (3). Editing bytes inside a region breaks (4). Editing bytes anywhere else breaks (1)
    and (3). Appending or truncating breaks (1) and (5).
    """
    if len(package) != package_length:
        raise TransitionError(
            f"package blob is {len(package)} bytes, expected {package_length}"
        )
    if len(successor) != successor_length:
        raise TransitionError(
            f"successor blob is {len(successor)} bytes, expected "
            f"{successor_length}"
        )
    package_digest = sha256_bytes(package)
    if package_digest != package_sha256:
        raise TransitionError(
            f"package blob digest is {package_digest}, expected "
            f"{package_sha256}"
        )
    successor_digest = sha256_bytes(successor)
    if successor_digest != successor_sha256:
        raise TransitionError(
            f"successor blob digest is {successor_digest}, expected "
            f"{successor_sha256}"
        )
    if not transition:
        raise TransitionError("the transition manifest is empty; a closed transition must be declared")

    package_cursor = 0
    successor_cursor = 0
    for index, region in enumerate(transition):
        if len(region) != 6:
            raise TransitionError(f"region {index}: expected six fields, got {len(region)}")
        p_at, p_len, p_want, s_at, s_len, s_want = region
        if not all(isinstance(v, int) for v in (p_at, p_len, s_at, s_len)):
            raise TransitionError(f"region {index}: offsets and lengths must be integers")
        if p_len < 0 or s_len < 0 or p_at < 0 or s_at < 0:
            raise TransitionError(f"region {index}: offsets and lengths must not be negative")
        if p_len == 0 and s_len == 0:
            raise TransitionError(f"region {index}: declares no change on either side")
        if p_at < package_cursor or s_at < successor_cursor:
            raise TransitionError(
                f"region {index}: starts at package {p_at}/successor {s_at}, which overlaps or "
                f"precedes the previous region ending at {package_cursor}/{successor_cursor}"
            )
        if p_at + p_len > len(package) or s_at + s_len > len(successor):
            raise TransitionError(f"region {index}: extends past the end of its file")

        gap_package = package[package_cursor:p_at]
        gap_successor = successor[successor_cursor:s_at]
        if gap_package != gap_successor:
            raise TransitionError(
                f"the span before region {index} (package {package_cursor}:{p_at}, successor "
                f"{successor_cursor}:{s_at}) is not byte-identical; only declared regions may differ"
            )

        got_package = sha256_bytes(package[p_at:p_at + p_len])
        if got_package != p_want:
            raise TransitionError(
                f"region {index}: package bytes {p_at}:{p_at + p_len} hash {got_package}, expected "
                f"{p_want}"
            )
        got_successor = sha256_bytes(successor[s_at:s_at + s_len])
        if got_successor != s_want:
            raise TransitionError(
                f"region {index}: successor bytes {s_at}:{s_at + s_len} hash {got_successor}, "
                f"expected {s_want}"
            )
        package_cursor = p_at + p_len
        successor_cursor = s_at + s_len

    if package[package_cursor:] != successor[successor_cursor:]:
        raise TransitionError(
            "the span after the last declared region is not byte-identical; only declared regions "
            "may differ"
        )
    if package_cursor + len(package[package_cursor:]) != len(package):  # pragma: no cover
        raise TransitionError("package blob was not consumed completely")
    if successor_cursor + len(successor[successor_cursor:]) != len(successor):  # pragma: no cover
        raise TransitionError("successor blob was not consumed completely")


def _reject_duplicate_keys(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    """A duplicate key silently discards the earlier value in ordinary ``json.loads``."""
    seen: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key {key!r} in authorization document")
        seen[key] = value
    return seen


def _is_commit_sha(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value)
    )


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _mapping(value: Any, where: str, errors: list[str]) -> Mapping[str, Any] | None:
    if not isinstance(value, Mapping):
        errors.append(f"{where}: expected a mapping")
        return None
    return value


def _exact(value: Any, expected: Any, where: str, errors: list[str]) -> None:
    if value != expected:
        errors.append(f"{where}: expected {expected!r}, found {value!r}")


def pins_are_placeholders() -> bool:
    return any(not _is_sha256(value) for value in CANONICAL_PINS.values())


# ======================================================================================
# Truth sources — injectable so tests never touch live GitHub
# ======================================================================================


class GitTruthSource(Protocol):
    """The local git object store. Content-addressed, durable, offline."""

    def commit_parents(self, sha: str) -> tuple[str, ...] | None: ...
    def commit_tree(self, sha: str) -> str | None: ...
    def is_ancestor(self, ancestor: str, descendant: str) -> bool: ...
    def blob_sha256_at(self, commit: str, relpath: str) -> str | None: ...
    #: MAJOR 1 (review 4955010993): a digest alone cannot answer "is the outcome-producing SURFACE
    #: the same", only "are the whole bytes the same" -- and whole-byte equality is the wrong
    #: question for a file this rebinding must lawfully change. Source text is required.
    def blob_text_at(self, commit: str, relpath: str) -> str | None: ...
    def head(self) -> str | None: ...


class GovernanceTruthSource(Protocol):
    """GitHub GOVERNANCE metadata only. Never market, price, or fundamental data."""

    def pull_request(self, number: int) -> Mapping[str, Any] | None: ...
    def review(self, number: int, review_id: str) -> Mapping[str, Any] | None: ...
    def reviews(self, number: int) -> Sequence[Mapping[str, Any]] | None: ...
    def issue_comment(self, comment_id: str) -> Mapping[str, Any] | None: ...
    def workflow_run(self, run_id: str) -> Mapping[str, Any] | None: ...
    def workflow_job(self, job_id: str) -> Mapping[str, Any] | None: ...


class LiveGitTruthSource:
    """Reads the real local git object store via plumbing commands."""

    def __init__(self, root: Path = ROOT) -> None:
        self._root = root

    def _run(self, *args: str) -> str | None:
        try:
            proc = subprocess.run(
                ["git", *args],
                cwd=self._root,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):  # pragma: no cover - defensive
            return None
        if proc.returncode != 0:
            return None
        return proc.stdout.strip()

    def commit_parents(self, sha: str) -> tuple[str, ...] | None:
        out = self._run("rev-list", "--parents", "-n", "1", sha)
        if not out:
            return None
        parts = out.split()
        return tuple(parts[1:]) if len(parts) > 1 else ()

    def commit_tree(self, sha: str) -> str | None:
        """The commit's tree SHA. Equal trees prove byte-identical content."""
        return self._run("rev-parse", f"{sha}^{{tree}}")

    def is_ancestor(self, ancestor: str, descendant: str) -> bool:
        try:
            proc = subprocess.run(
                ["git", "merge-base", "--is-ancestor", ancestor, descendant],
                cwd=self._root,
                capture_output=True,
                timeout=30,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):  # pragma: no cover - defensive
            return False
        return proc.returncode == 0

    def _blob_bytes(self, commit: str, relpath: str) -> bytes | None:
        try:
            proc = subprocess.run(
                ["git", "cat-file", "blob", f"{commit}:{relpath}"],
                cwd=self._root,
                capture_output=True,
                timeout=30,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):  # pragma: no cover - defensive
            return None
        if proc.returncode != 0:
            return None
        return proc.stdout

    def blob_sha256_at(self, commit: str, relpath: str) -> str | None:
        raw = self._blob_bytes(commit, relpath)
        return None if raw is None else sha256_bytes(raw)

    def blob_text_at(self, commit: str, relpath: str) -> str | None:
        """Decoded source at a commit. Undecodable content fails closed as absent."""
        raw = self._blob_bytes(commit, relpath)
        if raw is None:
            return None
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:  # pragma: no cover - defensive
            return None

    def head(self) -> str | None:
        return self._run("rev-parse", "HEAD")


class LiveGovernanceTruthSource:
    """Reads GitHub governance metadata over HTTPS.

    GOVERNANCE ONLY. This fetches reviews, comments, pull-request state, and CI run/job
    status. It never fetches market, price, fundamental, or any other economic data, and it
    is not, and must not become, a Stage-1 data-acquisition path.
    """

    API = "https://api.github.com"
    REVIEW_PAGE_SIZE = 100
    #: A ceiling only, so a pathological listing cannot loop forever. Exceeding it returns None
    #: (fail closed), never a silently truncated list.
    MAX_REVIEW_PAGES = 50

    def __init__(self, repository: str = REPOSITORY_IDENTITY) -> None:
        self._repository = repository

    def _get(self, path: str) -> Mapping[str, Any] | None:
        import urllib.error
        import urllib.request

        request = urllib.request.Request(
            f"{self.API}{path}",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "phq-xasset-0029"},
        )
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception:  # pragma: no cover - network/permission failure fails closed
            return None
        return payload if isinstance(payload, Mapping) else None

    def _get_list(self, path: str) -> list[Mapping[str, Any]] | None:
        import urllib.request

        request = urllib.request.Request(
            f"{self.API}{path}",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "phq-xasset-0029"},
        )
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception:  # pragma: no cover - network/permission failure fails closed
            return None
        return payload if isinstance(payload, list) else None

    def pull_request(self, number: int) -> Mapping[str, Any] | None:
        return self._get(f"/repos/{self._repository}/pulls/{number}")

    def review(self, number: int, review_id: str) -> Mapping[str, Any] | None:
        return self._get(f"/repos/{self._repository}/pulls/{number}/reviews/{review_id}")

    def reviews(self, number: int) -> Sequence[Mapping[str, Any]] | None:
        """EVERY review on the pull request, for finality checking.

        MAJOR 1 (review 4946540894): this previously issued ONE request for the first 100
        reviews and returned it as though it were the whole list, so with enough history a later
        adverse exact-head review could sit on page 2 and never be seen. Pagination now continues
        until a short page proves exhaustion, and ANY page that fails to retrieve or decode
        returns ``None`` so the caller fails closed rather than reasoning over a partial list.
        """
        collected: list[Mapping[str, Any]] = []
        page = 1
        while page <= self.MAX_REVIEW_PAGES:
            payload = self._get_list(
                f"/repos/{self._repository}/pulls/{number}/reviews"
                f"?per_page={self.REVIEW_PAGE_SIZE}&page={page}"
            )
            if payload is None:
                return None  # a failed page means the list is NOT proven complete
            collected.extend(payload)
            if len(payload) < self.REVIEW_PAGE_SIZE:
                return collected  # a short page proves exhaustion
            page += 1
        # Ran past the page ceiling without proving exhaustion: refuse to assert completeness.
        return None

    def issue_comment(self, comment_id: str) -> Mapping[str, Any] | None:
        return self._get(f"/repos/{self._repository}/issues/comments/{comment_id}")

    def workflow_run(self, run_id: str) -> Mapping[str, Any] | None:
        return self._get(f"/repos/{self._repository}/actions/runs/{run_id}")

    def workflow_job(self, job_id: str) -> Mapping[str, Any] | None:
        return self._get(f"/repos/{self._repository}/actions/jobs/{job_id}")


@dataclass(frozen=True)
class TruthSources:
    git: GitTruthSource = field(default_factory=LiveGitTruthSource)
    governance: GovernanceTruthSource = field(default_factory=LiveGovernanceTruthSource)


# ======================================================================================
# Live repository facts
# ======================================================================================


def live_canonical_hashes() -> dict[str, str]:
    return {relative: sha256_file(ROOT / relative) for relative in sorted(CANONICAL_PINS)}


def live_construction_universe_facts() -> dict[str, Any]:
    import level1_construction_universe_closure_validator as closure

    return {
        "sha256": closure.universe_aggregate_sha256(),
        "count": closure.derived_cardinality(),
        "cell_count": len(closure.per_cell_cardinality()),
    }


def live_load_bearing_hashes() -> dict[str, str]:
    return {relative: sha256_file(ROOT / relative) for relative in sorted(LOAD_BEARING_RELPATHS)}


# ======================================================================================
# Authenticated lifecycle verification — BLOCKING 1
# ======================================================================================


#: XASSET-0055 §C / XASSET-0053 §C item 2 -- THE minimal result representation, and the only one.
#: ``parse_formal_disposition`` must separate two outcomes the previous ``str | None`` channel
#: collapsed into a single ``None``:
#:
#:   * **ABSENT** -- the body carries no formal-looking disposition at all. Still ``None``, so every
#:     consumer's existing ABSENT policy is preserved literally rather than re-derived.
#:   * **MALFORMED / UNSUPPORTED** -- the body carries a formal-looking disposition line that is not
#:     in one of the two accepted wrapper forms. This value, and never ``None``.
#:
#: One sentinel is the smallest of the three routes §C item 2 permits (one added value, one small
#: typed result, or one sentinel), so no helper is introduced and none is needed. This is a
#: sentinel, not a parsing framework: it carries no behaviour and parses nothing.
class _MalformedFormalDisposition:
    """The single MALFORMED / UNSUPPORTED sentinel type."""

    __slots__ = ()

    def __repr__(self) -> str:  # pragma: no cover - trivial, but keeps error text readable
        return "MALFORMED_FORMAL_DISPOSITION"


MALFORMED_FORMAL_DISPOSITION = _MalformedFormalDisposition()


def parse_formal_disposition(body: str) -> "str | None | _MalformedFormalDisposition":
    """Return the review's FORMAL DISPOSITION verdict, parsed exactly from the first formal line.

    MAJOR 1 (review 4946464366): the previous check was ``APPROVING_REVIEW_DISPOSITION in body``,
    so a review whose formal line read ``CHANGES REQUIRED`` still passed if any later explanatory
    sentence quoted the approval phrase. Reproduced before correcting.

    Only the FIRST formal-looking line counts (XASSET-0053 §D.4). It is never skipped: a
    formal-looking line that is not in an accepted form STOPS the parse and yields no verdict
    (§D.17), so a later, better-formed line can never win past it.

    Exactly two wrapper forms are accepted, and no others (§D.2, §D.16): the plain canonical line,
    and a precisely balanced WHOLE-LINE Markdown-bold pair whose enclosed text is itself a plain
    canonical line and carries no further ``*``. Headings, blockquotes, bullets, code fences,
    leading or trailing prose, and unbalanced, partial, nested or repeated emphasis are all
    MALFORMED.

    Returns:
        * ``str`` -- the verdict, verbatim. Never normalized, truncated, case-folded,
          fuzzy-matched, canonicalized or coerced (§D.3), and never restricted to a closed
          vocabulary. A mixed-case or lower-case canonical verdict returns exactly as written;
          XASSET-0055 §D removes and PROHIBITS the lower-case heuristic that regressed this, and
          forbids any equivalent case-, length- or word-count-based verdict rule.
        * ``None`` -- ABSENT.
        * ``MALFORMED_FORMAL_DISPOSITION`` -- MALFORMED / UNSUPPORTED.

    XASSET-0055 §C -- the verdict boundary. After any recognized separator suffix has been
    VALIDATED as finding-count metadata (§E.1), the ENTIRE remaining post-prefix region is the
    verdict. Exact equality applies to that whole region, so appended text can never authenticate
    as approval -- a property of exact equality, not of a heuristic. Where no delimiter marks a
    boundary the parser does not pretend it can find one: it returns the region verbatim and lets
    inequality reject it, rather than falsely classifying it MALFORMED (§C.4).
    """
    if not isinstance(body, str):
        return None
    inside_code_fence = False
    for line in body.splitlines():
        stripped = line.strip()
        # §D.17 names code-fenced lines among the shapes that must fail closed. A fence is the
        # one unsupported shape not visible in the line itself, so it needs this single boolean
        # of context and nothing more. An unclosed fence leaves the flag set, which fails closed.
        if stripped.startswith("```") or stripped.startswith("~~~"):
            inside_code_fence = not inside_code_fence
            continue
        if FORMAL_DISPOSITION_PREFIX not in stripped.upper():
            continue  # not formal-looking: still ABSENT so far, keep scanning
        if inside_code_fence:
            return MALFORMED_FORMAL_DISPOSITION

        # --- the two accepted wrapper forms, and nothing else (§D.2, §D.16) ---------------
        revealed = stripped
        if not revealed.upper().startswith(FORMAL_DISPOSITION_PREFIX):
            if not (
                len(revealed) >= 4
                and revealed.startswith("**")
                and revealed.endswith("**")
            ):
                return MALFORMED_FORMAL_DISPOSITION
            inner = revealed[2:-2]
            # A further ``*`` means nested, doubled, partial or ambiguous emphasis (§D.10); and
            # the enclosed text must itself be a plain canonical line, never prose (§D.9).
            if "*" in inner or not inner.upper().startswith(FORMAL_DISPOSITION_PREFIX):
                return MALFORMED_FORMAL_DISPOSITION
            revealed = inner

        region = revealed[len(FORMAL_DISPOSITION_PREFIX):].strip()

        # --- §E.3: the EARLIEST recognized separator governs, never tuple order ------------
        # Splitting on each separator in tuple order let ``<approval> | <adverse> — 0 BLOCKING``
        # authenticate: the em dash is split first and erases the adverse ``|`` text.
        earliest: tuple[int, str] | None = None
        for separator in ("—", "--", " - ", "|"):
            index = region.find(separator)
            if index != -1 and (earliest is None or index < earliest[0]):
                earliest = (index, separator)
        if earliest is None:
            return region  # §C.1: the ENTIRE region is the verdict, verbatim

        verdict = region[: earliest[0]].strip()
        suffix = region[earliest[0] + len(earliest[1]):].strip(" ")
        # §E.1/§E.2: a recognized separator suffix is finding-count metadata and is VALIDATED,
        # never discarded unread. Grammar: count ( "/" count )*, count := digits SPACE CATEGORY.
        #
        # Every clause below is strict on purpose. ``.strip(" ")`` trims ORDINARY SPACES ONLY --
        # bare ``.strip()`` would silently swallow a tab around a count and accept it. The
        # category is compared UNSTRIPPED, so ``0<space><space>BLOCKING`` fails on the leading
        # space that ``partition`` leaves attached rather than being quietly normalized away.
        # ``isascii() and isdigit()`` together reject a signed or decimal count and every
        # non-ASCII digit form. An empty element -- from a leading, doubled or trailing "/" --
        # has no space and fails too.
        for element in suffix.split("/"):
            digits, spacer, category = element.strip(" ").partition(" ")
            if (
                not spacer
                or not digits.isascii()
                or not digits.isdigit()
                or category not in ("BLOCKING", "MAJOR", "MINOR", "NOTE")
            ):
                return MALFORMED_FORMAL_DISPOSITION
        return verdict
    return None


def _actor_login(record: Mapping[str, Any]) -> str | None:
    user = record.get("user")
    if isinstance(user, Mapping):
        login = user.get("login")
        return login if isinstance(login, str) and login.strip() else None
    return None


def _belongs_to_pull_request(record: Mapping[str, Any], number: Any) -> bool:
    """Does this durable record actually belong to the authorizing pull request?

    MAJOR 1: acceptance and post-merge verification were fetched as repository-wide comment
    ids and only their body text was inspected, so a comment from any other pull request or
    issue satisfied the gate. GitHub records carry their own owning URL; a record without one
    cannot prove ownership and is refused.
    """
    if not isinstance(number, int):
        return False
    marker = f"/{number}"
    for key in ("issue_url", "pull_request_url", "html_url", "_links"):
        value = record.get(key)
        if isinstance(value, str) and (value.endswith(marker) or f"{marker}#" in value):
            return True
    return False


# ======================================================================================
# XASSET-0042 — the PR #337 lifecycle actor-evidence correction
# ======================================================================================
#
# WHAT THIS IS, EXACTLY
# ---------------------
# Two comments in PR #337's completed lifecycle -- the principal acceptance ``5335697214``
# and the post-merge verification ``5335849767`` -- were posted through an App-token write
# path GitHub attributes to ``claude[bot]``. BLOCKING 2's actor requirement (above) is
# therefore unmet for those two exact records, and the step-11 unit correctly stopped
# rather than arming. XASSET-0041 authorizes ONE bounded correction, subject to ten
# conjunctive properties, and its own principal acceptance carries the ratification.
#
# WHAT THIS IS NOT
# ----------------
# It is NOT an accepted-actor list. ``PRINCIPAL_ACCOUNT_LOGIN`` and
# ``LIFECYCLE_OPERATOR_LOGIN`` remain ``Mast3rkey`` and are not consulted differently
# anywhere. ``claude[bot]`` is never classified as principal or lifecycle operator, gains
# no standing on any other pull request, comment, actor, head, review, merge, or future
# lifecycle, and is named below ONLY as the actor of two exactly pinned historical records
# the principal has durably ratified.
#
# It is NOT identity inference from comment text. Author identity is still derived
# exclusively from durable ``user.login`` via :func:`_actor_login`, for the ratified
# records and for the ratification itself. The body checks below verify that the
# RATIFICATION RECORD names the identities XASSET-0041 SS-G.3/SS-G.4 require it to name;
# they never establish who wrote anything.
#
# It is NOT a fictional pre-merge acceptance. The ratification is required to POSTDATE the
# PR #337 merge (:data:`_RATIFICATION_MUST_POSTDATE_RATIFIED_MERGE`). It ratifies the two
# historical acts as they stand; it rewrites no timestamp and relaxes no chronology rule.
# Every ordinary chronology check still runs unchanged, for PR #337 and everything else.
#
# FAIL-CLOSED
# -----------
# The exception is a conjunction. Any missing, unreachable, malformed, ambiguous,
# substituted, altered, wrong-actor, wrong-PR, wrong-head, wrong-review, wrong-comment,
# wrong-merge, wrong-CI, or incomplete-lifecycle evidence yields the all-false result, and
# the ordinary actor error fires with its wording unchanged.

#: The decision that authorizes this exception, and whose own completed lifecycle unlocks it.
RATIFICATION_AUTHORIZING_DECISION = "XASSET-0041"

#: XASSET-0041 SS-F.5 -- the five exact PR #337 identities. ALL five must match the document
#: under validation AND live truth. These are the entire scope of the exception.
RATIFIED_PULL_REQUEST = 337
RATIFIED_HEAD_SHA = "f40c816223c78f1d1e436b718455df5fb3d77fa7"
RATIFIED_REVIEW_ID = "4966846374"
RATIFIED_ACCEPTANCE_COMMENT_ID = "5335697214"
RATIFIED_MERGE_SHA = "637eaa30302f5a71f84ab1d215ecbd32c01399b5"
RATIFIED_POST_MERGE_VERIFICATION_COMMENT_ID = "5335849767"

#: The actor of the two ratified historical records. NOT an accepted principal or lifecycle
#: operator anywhere: this login authenticates nothing on its own and unlocks nothing except
#: in conjunction with every other pin in this section.
RATIFIED_HISTORICAL_ACTOR = "claude[bot]"

#: XASSET-0041's own complete lifecycle (PR #341), every element pinned exactly. Anything
#: short of all of it -- including a merged-but-CI-less or closure-less lifecycle -- leaves
#: the exception locked.
RATIFICATION_PULL_REQUEST = 341
RATIFICATION_HEAD_SHA = "0449d08217b5c0e422721ff3ef76b4241fb8a95a"
RATIFICATION_BASE_SHA = "f212cce50e28ae887dc8c594bf8ae491a3ef85af"
RATIFICATION_REVIEW_ID = "4974291044"
RATIFICATION_COMMENT_ID = "5345229177"
RATIFICATION_MERGE_SHA = "9c8647f9dddacdf63825f569097214ba65299fe8"
RATIFICATION_POST_MERGE_VERIFICATION_COMMENT_ID = "5345270602"
RATIFICATION_FINAL_CLOSURE_COMMENT_ID = "5345376547"
RATIFICATION_CI_RUN_ID = "32278094960"
RATIFICATION_CI_JOB_ID = "96150134005"

#: XASSET-0041 SS-G.4's required statement. The ratification must say what it is doing, not
#: merely exist. An edited body that drops this stops unlocking the exception.
RATIFICATION_REQUIRED_PHRASE = "authorized acts performed for"

#: XASSET-0041 SS-F.8 / SS-F.1, made mechanical: a ratification is retrospective, so it must
#: come STRICTLY AFTER the merge whose lifecycle records it ratifies. Equality fails: a
#: ratification simultaneous with the act is not a retrospective ratification of it.
_RATIFICATION_MUST_POSTDATE_RATIFIED_MERGE = True

# --------------------------------------------------------------------------------------
# MAJOR 1 (review 4975556072) -- bind the EXACT accepted records, not a bag of substrings
# --------------------------------------------------------------------------------------
#
# Token presence proves names are PRESENT. It does not prove the record affirmatively
# ratifies, verifies, or closes anything. Reproduced through the public validator: a
# ratification edited to read "VOID. I do NOT ratify anything." while still quoting every
# required identity still unlocked both gates; so did a post-merge comment reading "this does
# NOT verify" and a closure reading "NO closure occurred". That is not hypothetical record
# shape -- PR #341 comment 5345204885 was itself retracted by editing its body into a VOID
# notice while retaining its historical text, and XASSET-0041 SS-F.7 expressly requires an
# ALTERED record to be rejected.
#
# The fix is to authenticate the exact accepted records. Each pinned record is reduced to a
# deterministic fingerprint over EXPLICITLY SELECTED identity-bearing and semantic fields,
# with the body represented by its own SHA-256. Any body edit -- negation, VOID notice,
# retraction, or a single changed character -- changes the fingerprint and relocks both
# gates. So does a changed actor, state, reviewed commit, or timestamp.
#
# This is deliberately NOT a natural-language parser. Nothing here looks for the words
# "VOID" or "not"; a permissive reader of prose is exactly the class of mechanism that
# failed. The question asked is only "is this byte-for-byte the record that was accepted?"
#
# The fingerprints below were re-derived from the live records this session, not copied.

#: Selected fields, canonically serialized, for the approving PR #341 review.
RATIFICATION_REVIEW_FINGERPRINT = (
    "904f4cb4642f0f7b8bcd6bb33be92d72678270b122402e5d423789960aa33067"
)
#: ... the principal acceptance carrying the SS-G ratification.
RATIFICATION_COMMENT_FINGERPRINT = (
    "acbd2bb2a9ccb9c71475dab83d2ab62cfc1b9110ed5a597e232cd6aaa620b0c6"
)
#: ... the immediate post-merge verification.
RATIFICATION_VERIFICATION_FINGERPRINT = (
    "763e4e2fbd2559bb4e4e6e04dd782e4f1d1840e750e23ab776cb44de74d9ed0d"
)
#: ... the final post-CI verification and lifecycle closure.
RATIFICATION_CLOSURE_FINGERPRINT = (
    "4e39a8b16248ebe616f5262b6c476f3b6780eedfaf9df2e85d7113272a26f568"
)


def _canonical_record_fingerprint(fields: Mapping[str, Any]) -> str:
    """SHA-256 over EXPLICITLY SELECTED fields, canonically serialized.

    Sorted keys and fixed separators, so the digest depends only on the selected values --
    never on dictionary ordering or a ``repr``, neither of which is a stable contract.
    """
    encoded = json.dumps(
        dict(fields), sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _review_record_fingerprint(review: Mapping[str, Any]) -> str | None:
    """Fingerprint a pull-request review. ``None`` when a selected field is unusable."""
    body = review.get("body")
    actor = _actor_login(review)
    if not isinstance(body, str) or actor is None:
        return None
    return _canonical_record_fingerprint(
        {
            "kind": "pull_request_review",
            "id": str(review.get("id") or ""),
            "commit_id": str(review.get("commit_id") or ""),
            "state": str(review.get("state") or "").upper(),
            "actor": actor,
            "submitted_at": str(review.get("submitted_at") or ""),
            "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        }
    )


def _comment_record_fingerprint(comment: Mapping[str, Any]) -> str | None:
    """Fingerprint an issue comment. ``None`` when a selected field is unusable."""
    body = comment.get("body")
    actor = _actor_login(comment)
    if not isinstance(body, str) or actor is None:
        return None
    return _canonical_record_fingerprint(
        {
            "kind": "issue_comment",
            "id": str(comment.get("id") or ""),
            "actor": actor,
            "created_at": str(comment.get("created_at") or ""),
            "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        }
    )


def _instant(value: Any) -> str | None:
    """A strictly formatted ``YYYY-MM-DDTHH:MM:SSZ`` instant, or ``None``.

    MAJOR 2: every ordering comparison below needs a value it can trust. A missing,
    differently-shaped, or non-string timestamp yields ``None`` and fails the chain closed
    rather than comparing whatever happens to be there. The fixed shape is what makes plain
    lexicographic comparison exact -- same length, same field widths, same UTC zone.
    """
    if not isinstance(value, str) or len(value) != 20:
        return None
    if (
        value[4] != "-"
        or value[7] != "-"
        or value[10] != "T"
        or value[13] != ":"
        or value[16] != ":"
        or value[19] != "Z"
    ):
        return None
    digits = value[:4] + value[5:7] + value[8:10] + value[11:13] + value[14:16] + value[17:19]
    return value if digits.isdigit() else None


@dataclass(frozen=True)
class _Pr337ActorRatification:
    """Which of the two exactly pinned PR #337 actor gates are ratified.

    Constructed only by :func:`_derive_pr337_actor_ratification`. The default instance --
    the one returned for every document that is not PR #337's, and for every failure of any
    conjunct -- ratifies nothing.
    """

    acceptance: bool = False
    post_merge_verification: bool = False

    def ratifies_acceptance(self, comment_id: Any, actor: Any) -> bool:
        """Independently re-check the record's own identity at the call site."""
        return (
            self.acceptance
            and str(comment_id) == RATIFIED_ACCEPTANCE_COMMENT_ID
            and actor == RATIFIED_HISTORICAL_ACTOR
        )

    def ratifies_post_merge_verification(self, comment_id: Any, actor: Any) -> bool:
        return (
            self.post_merge_verification
            and str(comment_id) == RATIFIED_POST_MERGE_VERIFICATION_COMMENT_ID
            and actor == RATIFIED_HISTORICAL_ACTOR
        )


_NO_PR337_ACTOR_RATIFICATION = _Pr337ActorRatification()


def _names_all(body: Any, required: Sequence[str]) -> bool:
    """Does this record's body name every required identity? Content, never identity."""
    if not isinstance(body, str):
        return False
    return all(token in body for token in required)


def _derive_pr337_actor_ratification(
    document: Mapping[str, Any], sources: TruthSources, pull: Mapping[str, Any] | None
) -> _Pr337ActorRatification:
    """Decide whether the two exactly pinned PR #337 actor gates are ratified.

    A conjunction over four independent evidence families. Every one must hold:

      1. **Scope.** The document under validation IS the PR #337 lifecycle -- all five
         SS-F.5 identities, taken from the document itself, equal their pins exactly.
      2. **Live agreement.** PR #337's own durable metadata still reports that head, that
         merge, merged state, and this repository.
      3. **The ratification.** XASSET-0041's complete lifecycle (PR #341) -- merged at the
         pinned head and merge, an approving non-dismissed exact-head review, a principal
         acceptance durably authored by ``Mast3rkey`` naming all five ratified identities
         and stating SS-G.4's ratification, a post-merge verification and a final closure
         both durably authored by ``Mast3rkey``, and merge-commit CI at the exact merge SHA.
      4. **Git.** The ratification merge really has two parents in order, and zero drift.

    Plus retrospection: the ratification postdates the PR #337 merge.

    Returns the all-false instance on ANY failure, including an unreachable source.
    """
    evidence = document.get("lifecycle_evidence")
    if not isinstance(evidence, Mapping):
        return _NO_PR337_ACTOR_RATIFICATION

    def _sub(key: str, field_name: str) -> str:
        block = evidence.get(key)
        return str(block.get(field_name) or "") if isinstance(block, Mapping) else ""

    # --- 1. Scope: this must BE the PR #337 lifecycle, on every one of the five pins ----
    if document.get("authorizing_pull_request") != RATIFIED_PULL_REQUEST:
        return _NO_PR337_ACTOR_RATIFICATION
    if document.get("authorization_head") != RATIFIED_HEAD_SHA:
        return _NO_PR337_ACTOR_RATIFICATION
    if _sub("independent_review", "review_id") != RATIFIED_REVIEW_ID:
        return _NO_PR337_ACTOR_RATIFICATION
    if _sub("merge", "merge_sha") != RATIFIED_MERGE_SHA:
        return _NO_PR337_ACTOR_RATIFICATION
    if _sub("principal_acceptance", "comment_id") != RATIFIED_ACCEPTANCE_COMMENT_ID:
        return _NO_PR337_ACTOR_RATIFICATION
    if (
        _sub("post_merge_verification", "comment_id")
        != RATIFIED_POST_MERGE_VERIFICATION_COMMENT_ID
    ):
        return _NO_PR337_ACTOR_RATIFICATION

    # --- 2. Live PR #337 must still agree with the pins --------------------------------
    if not isinstance(pull, Mapping):
        return _NO_PR337_ACTOR_RATIFICATION
    if ((pull.get("base") or {}).get("repo") or {}).get("full_name") != REPOSITORY_IDENTITY:
        return _NO_PR337_ACTOR_RATIFICATION
    if pull.get("merged") is not True:
        return _NO_PR337_ACTOR_RATIFICATION
    if (pull.get("head") or {}).get("sha") != RATIFIED_HEAD_SHA:
        return _NO_PR337_ACTOR_RATIFICATION
    if pull.get("merge_commit_sha") != RATIFIED_MERGE_SHA:
        return _NO_PR337_ACTOR_RATIFICATION

    # --- 3. XASSET-0041's own complete lifecycle ---------------------------------------
    rat_pull = sources.governance.pull_request(RATIFICATION_PULL_REQUEST)
    if not isinstance(rat_pull, Mapping):
        return _NO_PR337_ACTOR_RATIFICATION
    if ((rat_pull.get("base") or {}).get("repo") or {}).get("full_name") != REPOSITORY_IDENTITY:
        return _NO_PR337_ACTOR_RATIFICATION
    if rat_pull.get("merged") is not True:
        return _NO_PR337_ACTOR_RATIFICATION
    if (rat_pull.get("head") or {}).get("sha") != RATIFICATION_HEAD_SHA:
        return _NO_PR337_ACTOR_RATIFICATION
    if rat_pull.get("merge_commit_sha") != RATIFICATION_MERGE_SHA:
        return _NO_PR337_ACTOR_RATIFICATION

    rat_review = sources.governance.review(RATIFICATION_PULL_REQUEST, RATIFICATION_REVIEW_ID)
    if not isinstance(rat_review, Mapping):
        return _NO_PR337_ACTOR_RATIFICATION
    if rat_review.get("commit_id") != RATIFICATION_HEAD_SHA:
        return _NO_PR337_ACTOR_RATIFICATION
    if str(rat_review.get("state") or "").upper() == "DISMISSED":
        return _NO_PR337_ACTOR_RATIFICATION
    # MAJOR 2: GitHub's NATIVE state is durable truth and is evaluated INDEPENDENTLY of the
    # repository's body grammar. A CHANGES_REQUESTED review is adverse even when its prose
    # still carries the approving formal line.
    if str(rat_review.get("state") or "").upper() in NATIVE_ADVERSE_REVIEW_STATES:
        return _NO_PR337_ACTOR_RATIFICATION
    # XASSET-0053 §D.19: MALFORMED / UNSUPPORTED is refused explicitly, never merely as an
    # incidental consequence of inequality, and a native APPROVED state never rescues it.
    rat_verdict = parse_formal_disposition(rat_review.get("body") or "")
    if rat_verdict is MALFORMED_FORMAL_DISPOSITION:
        return _NO_PR337_ACTOR_RATIFICATION
    if rat_verdict != APPROVING_REVIEW_DISPOSITION:
        return _NO_PR337_ACTOR_RATIFICATION
    if not _belongs_to_pull_request(rat_review, RATIFICATION_PULL_REQUEST):
        return _NO_PR337_ACTOR_RATIFICATION
    # MAJOR 1: the exact accepted review, byte-for-byte.
    if _review_record_fingerprint(rat_review) != RATIFICATION_REVIEW_FINGERPRINT:
        return _NO_PR337_ACTOR_RATIFICATION
    # MAJOR 2: and it must still be the FINAL clean pre-merge exact-head review. Reuses the
    # existing finality machinery and the paginated review source rather than defining a
    # second, weaker notion of finality -- including its fail-closed behaviour when the
    # review list cannot be retrieved at all.
    if _verify_selected_review_is_final(
        sources,
        RATIFICATION_PULL_REQUEST,
        RATIFICATION_HEAD_SHA,
        RATIFICATION_REVIEW_ID,
        rat_review.get("submitted_at"),
        rat_pull,
    ):
        return _NO_PR337_ACTOR_RATIFICATION

    # The ratification itself. Author identity DERIVED, never read out of the body.
    ratification = sources.governance.issue_comment(RATIFICATION_COMMENT_ID)
    if not isinstance(ratification, Mapping):
        return _NO_PR337_ACTOR_RATIFICATION
    if _actor_login(ratification) != PRINCIPAL_ACCOUNT_LOGIN:
        return _NO_PR337_ACTOR_RATIFICATION
    if not _belongs_to_pull_request(ratification, RATIFICATION_PULL_REQUEST):
        return _NO_PR337_ACTOR_RATIFICATION
    ratification_body = ratification.get("body")
    if not _names_all(
        ratification_body,
        (
            # SS-G.2 -- its own accepted head and the review it relies upon.
            RATIFICATION_HEAD_SHA,
            RATIFICATION_REVIEW_ID,
            # SS-G.3 -- all five ratified identities, explicitly.
            RATIFIED_HEAD_SHA,
            RATIFIED_REVIEW_ID,
            RATIFIED_ACCEPTANCE_COMMENT_ID,
            RATIFIED_MERGE_SHA,
            RATIFIED_POST_MERGE_VERIFICATION_COMMENT_ID,
            # SS-G.4 -- names the actor whose acts it ratifies, and says what it is doing.
            RATIFIED_HISTORICAL_ACTOR,
            RATIFICATION_REQUIRED_PHRASE,
        ),
    ):
        return _NO_PR337_ACTOR_RATIFICATION
    # MAJOR 1: the token list above states SS-G.3/SS-G.4's CONTENT REQUIREMENT and is kept for
    # that reason. It is not, and never was, sufficient on its own -- the fingerprint below is
    # what authenticates that this is the exact accepted record rather than an edited,
    # negated, or retracted one that merely still quotes the same identities.
    if _comment_record_fingerprint(ratification) != RATIFICATION_COMMENT_FINGERPRINT:
        return _NO_PR337_ACTOR_RATIFICATION

    rat_verification = sources.governance.issue_comment(
        RATIFICATION_POST_MERGE_VERIFICATION_COMMENT_ID
    )
    if not isinstance(rat_verification, Mapping):
        return _NO_PR337_ACTOR_RATIFICATION
    if _actor_login(rat_verification) != LIFECYCLE_OPERATOR_LOGIN:
        return _NO_PR337_ACTOR_RATIFICATION
    if not _belongs_to_pull_request(rat_verification, RATIFICATION_PULL_REQUEST):
        return _NO_PR337_ACTOR_RATIFICATION
    if not _names_all(rat_verification.get("body"), (RATIFICATION_MERGE_SHA,)):
        return _NO_PR337_ACTOR_RATIFICATION
    # MAJOR 1: a post-merge comment edited to say it does NOT verify the merge, while still
    # quoting the merge SHA, is not the accepted verification record.
    if _comment_record_fingerprint(rat_verification) != RATIFICATION_VERIFICATION_FINGERPRINT:
        return _NO_PR337_ACTOR_RATIFICATION

    rat_closure = sources.governance.issue_comment(RATIFICATION_FINAL_CLOSURE_COMMENT_ID)
    if not isinstance(rat_closure, Mapping):
        return _NO_PR337_ACTOR_RATIFICATION
    if _actor_login(rat_closure) != LIFECYCLE_OPERATOR_LOGIN:
        return _NO_PR337_ACTOR_RATIFICATION
    if not _belongs_to_pull_request(rat_closure, RATIFICATION_PULL_REQUEST):
        return _NO_PR337_ACTOR_RATIFICATION
    if not _names_all(
        rat_closure.get("body"), (RATIFICATION_MERGE_SHA, RATIFICATION_CI_RUN_ID)
    ):
        return _NO_PR337_ACTOR_RATIFICATION
    # MAJOR 1: likewise for a closure edited to say no closure occurred.
    if _comment_record_fingerprint(rat_closure) != RATIFICATION_CLOSURE_FINGERPRINT:
        return _NO_PR337_ACTOR_RATIFICATION

    rat_run = sources.governance.workflow_run(RATIFICATION_CI_RUN_ID)
    if not isinstance(rat_run, Mapping):
        return _NO_PR337_ACTOR_RATIFICATION
    if rat_run.get("status") != "completed" or rat_run.get("conclusion") != "success":
        return _NO_PR337_ACTOR_RATIFICATION
    if rat_run.get("head_sha") != RATIFICATION_MERGE_SHA:
        return _NO_PR337_ACTOR_RATIFICATION

    rat_job = sources.governance.workflow_job(RATIFICATION_CI_JOB_ID)
    if not isinstance(rat_job, Mapping):
        return _NO_PR337_ACTOR_RATIFICATION
    if str(rat_job.get("run_id")) != RATIFICATION_CI_RUN_ID:
        return _NO_PR337_ACTOR_RATIFICATION
    if rat_job.get("conclusion") != "success":
        return _NO_PR337_ACTOR_RATIFICATION

    # --- 4. Git truth for the ratification merge ---------------------------------------
    rat_parents = sources.git.commit_parents(RATIFICATION_MERGE_SHA)
    if rat_parents is None or len(rat_parents) != 2:
        return _NO_PR337_ACTOR_RATIFICATION
    if rat_parents[0] != RATIFICATION_BASE_SHA or rat_parents[1] != RATIFICATION_HEAD_SHA:
        return _NO_PR337_ACTOR_RATIFICATION
    rat_merge_tree = sources.git.commit_tree(RATIFICATION_MERGE_SHA)
    rat_head_tree = sources.git.commit_tree(RATIFICATION_HEAD_SHA)
    if rat_merge_tree is None or rat_head_tree is None or rat_merge_tree != rat_head_tree:
        return _NO_PR337_ACTOR_RATIFICATION

    # --- 5. MAJOR 2: XASSET-0041's own lifecycle, as an ORDERED CHAIN ------------------
    #
    # Existence, content, actors, structure, and CI were all checked above -- but until now
    # nothing proved they happened in the order SS-J requires. Reproduced through the public
    # validator, every one of these still unlocked both gates: an acceptance dated BEFORE the
    # review it certifies; an acceptance dated AFTER the merge it authorized; a "post-merge"
    # verification dated BEFORE the merge; a closure dated before the merge or before CI
    # finished. A lifecycle whose steps are out of order is not the lifecycle SS-J closed.
    #
    # Every instant must be present and strictly well formed. A missing or malformed
    # timestamp is not treated as "no constraint" -- it fails the chain closed.
    review_at = _instant(rat_review.get("submitted_at"))
    accepted_at = _instant(ratification.get("created_at"))
    rat_merged_at = _instant(rat_pull.get("merged_at"))
    verified_at = _instant(rat_verification.get("created_at"))
    ci_completed_at = _instant(rat_job.get("completed_at"))
    closed_at = _instant(rat_closure.get("created_at"))
    if None in (review_at, accepted_at, rat_merged_at, verified_at, ci_completed_at, closed_at):
        return _NO_PR337_ACTOR_RATIFICATION

    # 5.1 the independent review precedes the acceptance that certifies it.
    if accepted_at < review_at:
        return _NO_PR337_ACTOR_RATIFICATION
    # 5.2 acceptance STRICTLY precedes merge -- a merge cannot carry an acceptance that did
    #     not yet exist, and an acceptance simultaneous with its own merge is not evidence
    #     the merge relied on it.
    if not accepted_at < rat_merged_at:
        return _NO_PR337_ACTOR_RATIFICATION
    # 5.3 post-merge verification never predates the merge it verifies. Equality is allowed:
    #     the repository's convention is "immediately after", and a same-second record is a
    #     real one -- only an EARLIER one is impossible.
    if verified_at < rat_merged_at:
        return _NO_PR337_ACTOR_RATIFICATION
    # 5.4 final closure follows the post-merge verification AND the CI completion it reports.
    if closed_at < verified_at:
        return _NO_PR337_ACTOR_RATIFICATION
    if closed_at < ci_completed_at:
        return _NO_PR337_ACTOR_RATIFICATION

    # --- 6. Retrospection: a ratification comes STRICTLY AFTER what it ratifies ---------
    if _RATIFICATION_MUST_POSTDATE_RATIFIED_MERGE:
        ratified_merge_at = _instant(pull.get("merged_at"))
        if ratified_merge_at is None:
            return _NO_PR337_ACTOR_RATIFICATION
        # STRICT (MAJOR 2): equality fails. A ratification stamped at the very instant of the
        # merge it ratifies is not a retrospective account of it.
        if not accepted_at > ratified_merge_at:
            return _NO_PR337_ACTOR_RATIFICATION

    return _Pr337ActorRatification(acceptance=True, post_merge_verification=True)


def verify_lifecycle_against_truth(
    document: Mapping[str, Any], sources: TruthSources
) -> tuple[str, ...]:
    """Re-derive every lifecycle fact from durable truth and compare.

    Nothing is accepted because a recorded string is well-formed. Every claim is checked
    against an independently fetched fact, and an unreachable source fails closed.
    """
    errors: list[str] = []
    evidence = document.get("lifecycle_evidence")
    if not isinstance(evidence, Mapping):
        return ("lifecycle_evidence: expected a mapping",)

    head = document.get("authorization_head")
    number = document.get("authorizing_pull_request")

    # --- The pull request itself -------------------------------------------------------
    pull = sources.governance.pull_request(number) if isinstance(number, int) else None
    if pull is None:
        errors.append(
            f"governance truth: pull request #{number!r} could not be verified; an "
            "unverifiable lifecycle never authorizes execution"
        )
        return tuple(errors)

    repo_full = ((pull.get("base") or {}).get("repo") or {}).get("full_name")
    if repo_full != REPOSITORY_IDENTITY:
        errors.append(f"governance truth: pull request belongs to {repo_full!r}")
    if pull.get("merged") is not True:
        errors.append("governance truth: pull request is not merged")
    real_head = (pull.get("head") or {}).get("sha")
    if real_head != head:
        errors.append(
            f"governance truth: pull request head is {real_head!r}, not the recorded "
            f"authorization_head {head!r}"
        )
    real_merge = pull.get("merge_commit_sha")

    # XASSET-0042: derived ONCE, from the pins and live truth above, before any gate reads
    # it. Ratifies nothing for any document that is not PR #337's exact lifecycle, and
    # nothing at all unless every conjunct in the section above holds.
    ratification = _derive_pr337_actor_ratification(document, sources, pull)

    # --- Gate 1: the review really exists, on the exact head ---------------------------
    recorded_review = evidence.get("independent_review") or {}
    review_id = str(recorded_review.get("review_id") or "")
    review = sources.governance.review(number, review_id) if review_id else None
    if review is None:
        errors.append(
            f"governance truth: independent review {review_id!r} does not exist on pull "
            f"request #{number}; a well-formed but nonexistent review id never authorizes "
            "execution"
        )
    else:
        if review.get("commit_id") != head:
            errors.append(
                f"governance truth: review {review_id} was submitted against "
                f"{review.get('commit_id')!r}, not the authorization head {head!r}"
            )
        verdict = parse_formal_disposition(review.get("body") or "")
        # XASSET-0053 §D.19: MALFORMED / UNSUPPORTED is reported separately from ABSENT; one
        # value may not stand for both. The ABSENT branch below is preserved verbatim.
        if verdict is MALFORMED_FORMAL_DISPOSITION:
            errors.append(
                f"governance truth: review {review_id} carries a "
                f"'{FORMAL_DISPOSITION_PREFIX}' line that is not in an accepted form, so its "
                "verdict cannot be authenticated; an unsupported formal line fails closed and "
                "is never treated as absent"
            )
        elif verdict is None:
            errors.append(
                f"governance truth: review {review_id} carries no parseable "
                f"'{FORMAL_DISPOSITION_PREFIX}' line, so its verdict cannot be authenticated"
            )
        elif verdict != APPROVING_REVIEW_DISPOSITION:
            errors.append(
                f"governance truth: review {review_id}'s formal disposition is {verdict!r}, not "
                f"{APPROVING_REVIEW_DISPOSITION!r}; an adverse review never authorizes execution "
                "even if its explanatory text quotes the approval phrase"
            )
        # Reviewer identity is DERIVED from durable metadata, never self-declared.
        derived_reviewer = (review.get("user") or {}).get("login")
        if recorded_review.get("reviewer_identity") != derived_reviewer:
            errors.append(
                "governance truth: reviewer_identity is self-declared as "
                f"{recorded_review.get('reviewer_identity')!r} but the durable review "
                f"metadata says {derived_reviewer!r}; reviewer identity may not be asserted"
            )
        # MAJOR 1: a dismissed or adverse review is not a lifecycle gate.
        if str(review.get("state") or "").upper() == "DISMISSED":
            errors.append(
                f"governance truth: review {review_id} has been DISMISSED and cannot certify a "
                "lifecycle gate"
            )
        # The review must belong to THIS pull request, not merely exist somewhere.
        if not _belongs_to_pull_request(review, number):
            errors.append(
                f"governance truth: review {review_id} does not belong to pull request #{number}"
            )

    # --- Gate 1b: the selected review must be the FINAL clean exact-head review ---------
    # MAJOR 2 (review 4946464366): only the certified review id was consulted, so a clean pass
    # followed by a later CHANGES REQUIRED review on the SAME head still armed the lifecycle.
    # Historical adverse reviews BEFORE the final clean pass are legitimate and are preserved.
    errors.extend(
        _verify_selected_review_is_final(
            sources, number, head, review_id, (review or {}).get("submitted_at"), pull
        )
    )

    # --- Gate 2: principal acceptance really exists and names the exact head -----------
    acceptance_id = str((evidence.get("principal_acceptance") or {}).get("comment_id") or "")
    acceptance = sources.governance.issue_comment(acceptance_id) if acceptance_id else None
    if acceptance is None:
        errors.append(
            f"governance truth: principal acceptance comment {acceptance_id!r} does not exist"
        )
    else:
        acceptance_body = acceptance.get("body") or ""
        if isinstance(head, str) and head not in acceptance_body:
            errors.append(
                f"governance truth: acceptance comment {acceptance_id} does not name the exact "
                f"head {head!r}"
            )
        if not _belongs_to_pull_request(acceptance, number):
            errors.append(
                f"governance truth: acceptance comment {acceptance_id} does not belong to pull "
                f"request #{number}"
            )
        # BLOCKING 2: the acceptance must be the PRINCIPAL's, not merely a qualifying comment.
        acceptance_actor = _actor_login(acceptance)
        if acceptance_actor is None:
            errors.append(
                f"governance truth: acceptance comment {acceptance_id} carries no durable author "
                "identity, so the principal gate cannot be authenticated"
            )
        elif acceptance_actor != PRINCIPAL_ACCOUNT_LOGIN and not ratification.ratifies_acceptance(
            acceptance_id, acceptance_actor
        ):
            # XASSET-0042: the ONLY relaxation. It requires this exact comment id, this exact
            # actor, and the whole ratified lifecycle above. Every other acceptance record on
            # every other pull request reaches the unchanged error below.
            errors.append(
                f"governance truth: acceptance comment {acceptance_id} was authored by "
                f"{acceptance_actor!r}, not the principal {PRINCIPAL_ACCOUNT_LOGIN!r}"
            )
        # MAJOR 1 -- PRINCIPAL CERTIFICATION replaces the unobservable independence property.
        # Same-account GitHub means login inequality cannot prove independent session authorship,
        # so the honest, mechanically verifiable substitute is that the principal's own durable
        # acceptance record NAMES the exact independent review pass being relied upon.
        if review_id and review_id not in acceptance_body:
            errors.append(
                f"governance truth: acceptance comment {acceptance_id} does not certify the "
                f"independent review {review_id!r} it relies upon; the principal must durably "
                "identify the exact review pass"
            )
        # Chronology: review, then acceptance, then merge.
        submitted = (review or {}).get("submitted_at")
        accepted = acceptance.get("created_at")
        merged_at = pull.get("merged_at")
        if submitted and accepted and str(accepted) < str(submitted):
            errors.append(
                f"governance truth: acceptance {accepted} precedes review {submitted}; the "
                "principal cannot certify a review that had not yet been submitted"
            )
        if accepted and merged_at and str(merged_at) < str(accepted):
            errors.append(
                f"governance truth: merge {merged_at} precedes acceptance {accepted}"
            )

    # --- Gate 3: the merge, its real SHA, and its real parents -------------------------
    recorded_merge = evidence.get("merge") or {}
    merge_sha = recorded_merge.get("merge_sha")
    if real_merge and merge_sha != real_merge:
        errors.append(
            f"governance truth: recorded merge {merge_sha!r} is not the real merge commit "
            f"{real_merge!r}"
        )
    real_parents = sources.git.commit_parents(merge_sha) if _is_commit_sha(merge_sha) else None
    if real_parents is None:
        errors.append(
            f"git truth: merge commit {merge_sha!r} does not exist in the local object store"
        )
    else:
        if list(recorded_merge.get("parents") or []) != list(real_parents):
            errors.append(
                f"git truth: recorded parents {list(recorded_merge.get('parents') or [])!r} do "
                f"not equal the real parents {list(real_parents)!r}"
            )
        if len(real_parents) != 2:
            errors.append(
                f"git truth: merge {merge_sha} has {len(real_parents)} parent(s); a squash or "
                "rebase does not carry the accepted head as a parent"
            )
        else:
            # MAJOR 2: bind BOTH parents exactly. Binding only the second let the base drift
            # after review, so a different base -- or a merge resolution -- could silently
            # become the authorized implementation.
            if real_parents[0] != REVIEWED_BASE_SHA:
                errors.append(
                    f"git truth: merge first parent {real_parents[0]!r} is not the exact reviewed "
                    f"base {REVIEWED_BASE_SHA!r}; base drift requires a fresh exact-head/base "
                    "review and cannot arm from the old one"
                )
            if real_parents[1] != head:
                errors.append(
                    f"git truth: merge second parent {real_parents[1]!r} is not the accepted head "
                    f"{head!r}; the merged bytes are not the accepted bytes"
                )
            # ZERO MERGE DRIFT: equal trees prove merging changed no reviewed byte.
            merge_tree = sources.git.commit_tree(str(merge_sha))
            head_tree = sources.git.commit_tree(str(head)) if _is_commit_sha(head) else None
            if merge_tree is None or head_tree is None:
                errors.append(
                    "git truth: merge or accepted-head tree could not be resolved, so zero merge "
                    "drift cannot be proven"
                )
            elif merge_tree != head_tree:
                errors.append(
                    f"git truth: merge tree {merge_tree} differs from the accepted head tree "
                    f"{head_tree}; merging changed reviewed bytes, so the merged tree may not "
                    "become its own source of truth"
                )

    # --- Gate 4: the post-merge verification record really exists ----------------------
    verification_id = str(
        (evidence.get("post_merge_verification") or {}).get("comment_id") or ""
    )
    verification = (
        sources.governance.issue_comment(verification_id) if verification_id else None
    )
    if verification is None:
        errors.append(
            f"governance truth: post-merge verification comment {verification_id!r} does not "
            "exist; merge alone never authorizes execution"
        )
    else:
        if isinstance(merge_sha, str) and merge_sha not in (verification.get("body") or ""):
            errors.append(
                f"governance truth: post-merge verification {verification_id} does not name the "
                f"merge SHA {merge_sha!r}"
            )
        if not _belongs_to_pull_request(verification, number):
            errors.append(
                f"governance truth: post-merge verification {verification_id} does not belong to "
                f"pull request #{number}"
            )
        verification_actor = _actor_login(verification)
        if verification_actor is None:
            errors.append(
                f"governance truth: post-merge verification {verification_id} carries no durable "
                "author identity, so the verification gate cannot be authenticated"
            )
        elif (
            verification_actor != LIFECYCLE_OPERATOR_LOGIN
            and not ratification.ratifies_post_merge_verification(
                verification_id, verification_actor
            )
        ):
            # XASSET-0042: the second and last relaxation, on the same conjunction.
            errors.append(
                f"governance truth: post-merge verification {verification_id} was authored by "
                f"{verification_actor!r}, not the lifecycle operator "
                f"{LIFECYCLE_OPERATOR_LOGIN!r}"
            )
        verified_at = verification.get("created_at")
        merged_at = pull.get("merged_at")
        if verified_at and merged_at and str(verified_at) < str(merged_at):
            errors.append(
                f"governance truth: post-merge verification {verified_at} precedes the merge "
                f"{merged_at}; it cannot verify a merge that had not happened"
            )

    # --- Gate 5: the merge-commit CI run AND its job, correctly paired ------------------
    recorded_ci = evidence.get("merge_commit_ci") or {}
    run_id = str(recorded_ci.get("run_id") or "")
    job_id = str(recorded_ci.get("job_id") or "")
    run = sources.governance.workflow_run(run_id) if run_id else None
    if run is None:
        errors.append(f"governance truth: workflow run {run_id!r} does not exist")
    else:
        if run.get("status") != "completed" or run.get("conclusion") != "success":
            errors.append(
                f"governance truth: workflow run {run_id} is "
                f"{run.get('status')!r}/{run.get('conclusion')!r}, not completed/success"
            )
        if run.get("head_sha") != merge_sha:
            errors.append(
                f"governance truth: workflow run {run_id} ran against {run.get('head_sha')!r}, "
                f"not the merge commit {merge_sha!r}"
            )
    job = sources.governance.workflow_job(job_id) if job_id else None
    if job is None:
        errors.append(f"governance truth: workflow job {job_id!r} does not exist")
    else:
        if str(job.get("run_id")) != run_id:
            errors.append(
                f"governance truth: job {job_id} belongs to run {job.get('run_id')!r}, not the "
                f"recorded run {run_id!r}"
            )
        if job.get("conclusion") != "success":
            errors.append(f"governance truth: job {job_id} concluded {job.get('conclusion')!r}")

    # --- Gate 6: ancestry, predecessor identity, load-bearing byte identity -------------
    errors.extend(_verify_git_anchored_identity(document, merge_sha, sources))
    # --- Gate 7 (XASSET-0037): the successor rebinding binds the EXACT merged package ---
    errors.extend(_verify_successor_rebinding_identity(document, merge_sha, sources))
    # --- Gate 8 (XASSET-0044 SS-L condition 7): final post-CI verification and closure ---
    errors.extend(
        _verify_lifecycle_closure(
            evidence,
            number=number,
            merge_sha=merge_sha,
            run_id=run_id,
            job_id=job_id,
            run=run,
            job=job,
            verification=verification,
            sources=sources,
        )
    )
    return tuple(errors)


#: MAJOR 1 (delta review 4988858926): characters which, ADJACENT to an identity, mean the body
#: carries a LARGER token that merely contains it rather than naming the identity itself. Written
#: as an explicit ASCII class rather than ``\w`` so the boundary is deterministic and does not
#: shift with the Unicode database. Merge SHAs are hex and CI run/job ids are decimal, so every
#: superset substitution the review named -- a leading or trailing hex character or digit, and an
#: identity embedded inside a larger alphanumeric token -- is adjacency by one of these.
_IDENTITY_BOUNDARY_CLASS = "[0-9A-Za-z_]"


def body_names_identity(body: Any, identity: Any) -> bool:
    """Does ``body`` name ``identity`` as a COMPLETE, unambiguous token?

    The ONE mechanism all three lifecycle-closure body identities share, so merge SHA, CI run id
    and CI job id cannot drift apart into three separately-worded checks again.

    This replaces raw substring containment, which proved only that a character sequence appears
    SOMEWHERE. Reproduced through the public verifier before this correction: a closure body whose
    only merge/run/job mentions were ``<merge>0``, ``<run>0`` and ``<job>0`` returned no errors,
    because each real sequence sits inside a different, longer identifier. A job id that merely
    contains the real job id is a DIFFERENT job, and a closure naming it does not identify the job
    whose completion it claims to follow.

    Boundary-aware, in both directions: an identity is named only where the characters immediately
    before and after it are not identity characters. Ordinary punctuation and whitespace -- the
    backticks, commas, spaces and full stops a genuine closure body uses -- are boundaries, so the
    canonical body is still accepted.
    """
    if not isinstance(body, str) or not isinstance(identity, str) or not identity:
        return False
    pattern = (
        f"(?<!{_IDENTITY_BOUNDARY_CLASS})"
        + re.escape(identity)
        + f"(?!{_IDENTITY_BOUNDARY_CLASS})"
    )
    return re.search(pattern, body) is not None


def _verify_lifecycle_closure(
    evidence: Mapping[str, Any],
    *,
    number: Any,
    merge_sha: Any,
    run_id: str,
    job_id: str,
    run: Mapping[str, Any] | None,
    job: Mapping[str, Any] | None,
    verification: Mapping[str, Any] | None,
    sources: TruthSources,
) -> list[str]:
    """XASSET-0044 SS-L condition 7, authenticated from durable truth.

    SS-L: "final post-CI verification and lifecycle closure". Before this gate the runtime
    authenticated conditions 1-6 and stopped, so an attestation could be assembled the moment CI
    went green -- strictly earlier than the decision's own stated effectivity.

    Nothing here is accepted because it is well-formed. The closure record must be a real comment,
    on the EXACT authorizing pull request, authored by the lifecycle operator, naming and recording
    the EXACT merge and CI identities Gates 3 and 5 independently derived, and created strictly
    AFTER both the post-merge verification and the completion of that CI job. Every unobtainable
    fact is an error, never silent agreement.

    The XASSET-0042 PR #337 actor ratification is deliberately NOT consulted. That exception is
    pinned to two specific PR #337 comment ids on two specific pre-existing gates; extending it to
    a gate that did not exist when it was granted would turn a closed, retrospective ratification
    into forward permission for bot-authored closure.
    """
    errors: list[str] = []
    recorded = evidence.get("lifecycle_closure")
    if not isinstance(recorded, Mapping):
        return [
            "authorization.lifecycle_evidence.lifecycle_closure: expected a mapping; "
            "XASSET-0044 SS-L condition 7 is not optional"
        ]
    for unknown in sorted(set(recorded) - set(LIFECYCLE_CLOSURE_KEYS)):
        errors.append(
            f"authorization.lifecycle_evidence.lifecycle_closure.{unknown}: unknown key; "
            "the schema is closed"
        )

    closure_id = str(recorded.get("comment_id") or "")
    closure = sources.governance.issue_comment(closure_id) if closure_id else None
    if closure is None:
        errors.append(
            f"governance truth: lifecycle-closure record {closure_id!r} does not exist; "
            "successful CI alone never makes this decision effective"
        )
        return errors

    # --- the exact pull request ---------------------------------------------------------
    if not _belongs_to_pull_request(closure, number):
        errors.append(
            f"governance truth: lifecycle-closure record {closure_id} does not belong to pull "
            f"request #{number}; a closure recorded elsewhere closes nothing here"
        )

    # --- the exact actor, with no ratification relaxation --------------------------------
    closure_actor = _actor_login(closure)
    if closure_actor is None:
        errors.append(
            f"governance truth: lifecycle-closure record {closure_id} carries no durable author "
            "identity, so the closure gate cannot be authenticated"
        )
    elif closure_actor != LIFECYCLE_OPERATOR_LOGIN:
        errors.append(
            f"governance truth: lifecycle-closure record {closure_id} was authored by "
            f"{closure_actor!r}, not the lifecycle operator {LIFECYCLE_OPERATOR_LOGIN!r}"
        )

    # --- the exact merge and CI identities, recorded AND named ---------------------------
    _exact(
        recorded.get("closed_merge_sha"),
        merge_sha,
        "authorization.lifecycle_evidence.lifecycle_closure.closed_merge_sha",
        errors,
    )
    _exact(
        str(recorded.get("closed_run_id") or ""),
        run_id,
        "authorization.lifecycle_evidence.lifecycle_closure.closed_run_id",
        errors,
    )
    _exact(
        str(recorded.get("closed_job_id") or ""),
        job_id,
        "authorization.lifecycle_evidence.lifecycle_closure.closed_job_id",
        errors,
    )
    # MAJOR 1 part 1 (delta review 4987958687): the correction declared that the durable body
    # records AND NAMES the exact merge and CI run/JOB identities, but only the merge and run were
    # required. Reproduced before correcting: a body naming the merge and run while OMITTING the
    # job -- and one carrying a SUBSTITUTED job -- both returned no errors. A run can carry more
    # than one job, so naming the run alone does not identify the job whose completion the closure
    # claims to follow.
    #
    # MAJOR 1 (delta review 4988858926): all three are now authenticated as COMPLETE TOKENS through
    # the single shared ``body_names_identity`` mechanism. Raw substring containment proved only
    # that a sequence appears somewhere, so supersets such as ``<merge>0``, ``<run>0`` and
    # ``<job>0`` -- reproduced through the public verifier -- satisfied every check at once while
    # naming three identifiers that are none of them. Each identity is independently required.
    body = closure.get("body") or ""
    for identity, what in (
        (merge_sha if isinstance(merge_sha, str) else "", "merge SHA"),
        (run_id, "merge-commit CI run"),
        (job_id, "merge-commit CI job"),
    ):
        if identity and not body_names_identity(body, identity):
            errors.append(
                f"governance truth: lifecycle-closure record {closure_id} does not name the "
                f"{what} {identity!r} as a complete token"
            )

    # --- chronology: strictly after BOTH the post-merge verification and CI completion ----
    closed_at = _instant(closure.get("created_at"))
    if closed_at is None:
        errors.append(
            f"governance truth: lifecycle-closure record {closure_id} carries no usable "
            "timestamp, so it cannot be proven to follow post-merge verification and CI"
        )
    else:
        verified_at = _instant((verification or {}).get("created_at"))
        if verified_at is None:
            errors.append(
                "governance truth: the post-merge verification timestamp could not be resolved, "
                "so lifecycle closure cannot be proven to follow it; this fails closed"
            )
        elif closed_at <= verified_at:
            errors.append(
                f"governance truth: lifecycle closure {closed_at} does not follow post-merge "
                f"verification {verified_at}; a closure cannot precede what it closes"
            )
        finished_at = _instant((job or {}).get("completed_at")) or _instant(
            (run or {}).get("updated_at")
        )
        if finished_at is None:
            errors.append(
                "governance truth: the merge-commit CI completion time could not be resolved, so "
                "lifecycle closure cannot be proven to follow it; this fails closed"
            )
        # MAJOR 1 part 2 (delta review 4987958687): STRICTLY after, on this conjunct too. The
        # previous ``<`` implemented "not before", which is a weaker claim than the surrounding
        # comment, than SS-L, and than the correction all state. GitHub timestamps are
        # second-resolution, so an EQUAL instant is exactly the case that cannot distinguish
        # "closed after CI finished" from "closed in the same second, order unknown" -- and an
        # unprovable ordering is not a proven one. Reproduced through the public verifier before
        # correcting, against both the job's own completed_at and the run-time fallback.
        elif closed_at <= finished_at:
            errors.append(
                f"governance truth: lifecycle closure {closed_at} does not strictly follow "
                f"completion of the merge-commit CI job {finished_at}; SS-L condition 7 is FINAL "
                "post-CI closure, and an equal instant cannot prove that ordering"
            )
    return errors


def _verify_step8_equivalent_base_equality(
    reviewed_base: Any,
    authorizing_merge: Any,
    descends_from_authorizing_merge: bool | None,
) -> list[str]:
    """XASSET-0048 SS-F.2: the base must EQUAL the authorizing merge, not merely descend from it.

    XASSET-0048's own independent review found the ancestry-only formulation defective and
    corrected it before that decision was accepted: reproduced in an isolated clone, a synthetic
    LATER DESCENDANT of a stand-in for the authorizing merge SATISFIED a descent-only rule, so a
    successor unit could have absorbed and rebound intervening bytes no review of the grant ever
    saw. Ancestry proves history; it does not prove SCOPE IDENTITY.

    That correction landed in XASSET-0048 as prose. Here it is made OPERATIVE, as a pure decidable
    proposition over three inputs and nothing else:

      1. both identities are well-formed 40-hex commit names -- an unobtainable or malformed
         identity is an ERROR, never silent agreement (XASSET-0048 SS-I);
      2. the reviewed base EQUALS the authorizing merge exactly;
      3. ancestry into this rebinding's own merge is RETAINED as necessary history -- a
         ``False`` here is still a failure, so equality never becomes a licence to drop the
         ancestry requirement the predecessor rule carried.

    ``descends_from_authorizing_merge`` is ``None`` when the rebinding merge is not yet a
    resolvable commit (the pre-merge case), which is not itself a failure of THIS proposition; the
    surrounding verifier checks ancestry independently once a real merge exists.

    Pure and offline by construction: it reads no git, no GitHub, no network, and no clock, so it
    cannot be silenced by an unavailable source, and it takes its inputs as PARAMETERS rather than
    reading module globals -- which is what lets the test module drive it against known-good and
    known-bad values, including a real synthetic later descendant, without monkeypatching anything.
    """
    errors: list[str] = []
    if not _is_commit_sha(reviewed_base):
        errors.append(
            f"authority: the reviewed base {reviewed_base!r} is not a well-formed commit name, so "
            "its equality with the authorizing merge cannot be decided; this fails closed"
        )
    if not _is_commit_sha(authorizing_merge):
        errors.append(
            f"authority: the authorizing merge {authorizing_merge!r} is not a well-formed commit "
            "name, so the base-equality rule cannot be decided; this fails closed"
        )
    if errors:
        return errors
    if str(reviewed_base) != str(authorizing_merge):
        errors.append(
            f"authority: the reviewed base {reviewed_base} is not the step-8-equivalent "
            f"authorization merge {authorizing_merge}; XASSET-0048 SS-F.2 makes EQUALITY "
            "operative, and descent alone never qualifies a base -- a later descendant would "
            "carry bytes no review of that grant ever saw"
        )
    if descends_from_authorizing_merge is False:
        errors.append(
            f"git truth: the rebinding merge does not descend from the authorizing merge "
            f"{authorizing_merge}; ancestry remains NECESSARY history even though it is "
            "insufficient authority"
        )
    return errors


def _verify_recovery_lifecycle_anchor(merge_sha: Any) -> list[str]:
    """XASSET-0046 SS-G.6/SS-G.7/SS-G.9: refuse an anchor that cannot lawfully authorize.

    Four refusals, each independently required and each stated as a REFUSAL rather than as a
    comment, because a prose prohibition is exactly what failed to prevent the defect this unit
    exists to repair:

    1. the authorizing DECISION may not be one whose own effectivity condition is permanently
       unsatisfiable -- an ineffective decision authorizes nothing, so binding one is not a
       weaker authorization, it is none at all;
    2. the authorizing PULL REQUEST may not be one of those stopped lifecycles' pull requests,
       which is the same refusal reached by the other identity a caller could supply;
    3. the authorized MERGE may not be a commit already recorded as having FAILED its own
       merge-commit CI -- a green run at some other commit is excluded by the condition's own
       words, so no later success can convert one of these into the success required;
    4. the canonical inputs must be UNCHANGED from the pins XASSET-0044 left. Originally that
       held because XASSET-0046 SS-G.9 FROZE them. It holds here for a different and independently
       sufficient reason, stated rather than inherited: XASSET-0048 SS-F.7 permits canonical
       amendment "only to the extent the rebinding requires", and THIS rebinding requires none --
       its whole authorization identity is carried by this module's own constants, and no
       canonical byte must move for it to be lawful, coherent, or provable. The alternative was
       weighed and declined; see the XASSET-0049 decision record, which states the determination
       expressly so a reviewer can check it rather than infer it. Consequently the canonical
       ``rebound_by`` / ``effective_structural_authorization_source`` still name XASSET-0044 --
       the last decision that amended those BYTES -- and this refusal stays live, unweakened. If a
       future edit moves a canonical byte without extending the succession machinery, this fires.

       That refusal is only as real as the independence of the identity it compares against.
       :data:`XASSET_0044_CANONICAL_PINS` is therefore bound to XASSET-0044's exact historical
       literals and never derived from :data:`CANONICAL_PINS` -- see MAJOR 1 of review
       4997532748, where the previous ``dict(CANONICAL_PINS)`` form followed a source-level pin
       edit during import and reported clean.

    Pure and offline: it reads constants only, never git, GitHub, the network, or the clock, so it
    cannot be silenced by an unavailable source.
    """
    errors: list[str] = []
    if AUTHORIZING_DECISION in PERMANENTLY_INEFFECTIVE_DECISIONS:
        errors.append(
            f"authority: {AUTHORIZING_DECISION} is permanently ineffective -- its own effectivity "
            "condition named an exact merge SHA whose merge-commit CI failed, and a run against "
            "any other commit is excluded by that condition's own words; it cannot be the "
            "authorizing decision"
        )
    if AUTHORIZING_PULL_REQUEST in PERMANENTLY_INEFFECTIVE_PULL_REQUESTS:
        errors.append(
            f"authority: pull request #{AUTHORIZING_PULL_REQUEST} ran a lifecycle that stopped at "
            "its own merge-commit CI; it cannot be the authorizing pull request"
        )
    for run, job, failed_merge in FAILED_MERGE_COMMIT_CI_RUNS:
        if _is_commit_sha(merge_sha) and str(merge_sha) == failed_merge:
            errors.append(
                f"authority: merge {failed_merge} is the head_sha of FAILED merge-commit CI run "
                f"{run} / job {job}; that failure is immutable adverse history and may never be "
                "re-run in place, relabelled, waived, or represented as successful"
            )
    if CANONICAL_PINS != XASSET_0044_CANONICAL_PINS:
        errors.append(
            "canonical drift: this rebinding amends no canonical byte -- XASSET-0048 SS-F.7 "
            "permits amendment only to the extent the rebinding requires, and it requires none -- "
            "but the effective canonical pins differ from the XASSET-0044 pins they must still "
            "equal; a rebinding that claims no canonical amendment may not move a canonical byte"
        )
    # XASSET-0049. Two further refusals, each stated as a REFUSAL rather than as a comment, and
    # each closing a class the anchor move newly opens.
    #
    # 5. the superseded anchor may not silently REMAIN the anchor. XASSET-0048 SS-F.3 requires
    #    every moved value to be an exact closed transition bound at BOTH ends; an anchor still
    #    naming its own predecessor is a transition with one end missing, which is drift wearing a
    #    rebinding's label.
    if AUTHORIZING_DECISION == PRIOR_RECONCILIATION_DECISION:
        errors.append(
            f"authority: {AUTHORIZING_DECISION} is the PRIOR anchor this rebinding supersedes; a "
            "rebinding whose anchor still names its own predecessor has not rebound anything"
        )
    if AUTHORIZING_PULL_REQUEST == PRIOR_RECONCILIATION_PULL_REQUEST:
        errors.append(
            f"authority: pull request #{AUTHORIZING_PULL_REQUEST} is the PRIOR anchor's own pull "
            "request; the successor must name its own"
        )
    # 6. the AUTHORITY may not be mistaken for the UNIT. XASSET-0048 authorized this rebinding; it
    #    did not perform it, and SS-A says so in terms. An anchor naming the authorizing decision
    #    would collapse authority into the thing authorized -- precisely the overloading
    #    XASSET-0037 SS-C named as the largest failure mode available to a rebinding.
    if AUTHORIZING_DECISION == STEP8_EQUIVALENT_AUTHORIZING_DECISION:
        errors.append(
            f"authority: {AUTHORIZING_DECISION} is the decision that AUTHORIZED this rebinding, "
            "not the rebinding itself; XASSET-0048 SS-A performs no rebinding and cannot be the "
            "effective structural authorization source its own grant produces"
        )
    if AUTHORIZING_PULL_REQUEST == STEP8_EQUIVALENT_AUTHORIZING_PULL_REQUEST:
        errors.append(
            f"authority: pull request #{AUTHORIZING_PULL_REQUEST} is the AUTHORIZING pull request, "
            "not this rebinding's own"
        )
    return errors


def _verify_successor_rebinding_identity(
    document: Mapping[str, Any], merge_sha: Any, sources: TruthSources
) -> list[str]:
    """XASSET-0030 SS-G.B step 8: prove this rebinding binds the exact completed package.

    Three separately named relationships, each verified from git rather than declared:

      * the HISTORICAL operational authorization (XASSET-0029 / PR #328) really has the identity
        the successor claims to inherit from, and is reachable from the successor merge;
      * the PACKAGE AUTHORITY (XASSET-0036 / PR #335) really merged, and is reachable;
      * the EXECUTABLE PACKAGE (PR #336) has exactly the recorded merge, accepted head, and base,
        with ZERO merge drift, and is an ancestor of the successor merge.

    And the invariant SS-G.B exists for: the outcome-producing bytes are byte-identical at the
    package's reviewed head, the package's merge, the successor's reviewed head, the successor's
    merge, and the working tree. A rebinding that silently altered the runner would otherwise bind
    code that independent review of the package never saw, against a non-rerunnable ``ATTEMPT_1``.
    """
    errors: list[str] = []
    git = sources.git

    def _block(key: str, expected: Mapping[str, Any]) -> Mapping[str, Any] | None:
        recorded = document.get(key)
        if not isinstance(recorded, Mapping):
            errors.append(f"{key}: expected a mapping")
            return None
        for field_name, want in sorted(expected.items()):
            _exact(recorded.get(field_name), want, f"{key}.{field_name}", errors)
        for unknown in sorted(set(recorded) - set(expected)):
            errors.append(f"{key}.{unknown}: unknown key; the schema is closed")
        return recorded

    _block(
        "historical_operational_authorization",
        {
            "decision": HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION,
            "pull_request": HISTORICAL_OPERATIONAL_AUTHORIZATION_PULL_REQUEST,
            "merge_sha": HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA,
            "accepted_head": HISTORICAL_OPERATIONAL_AUTHORIZATION_ACCEPTED_HEAD,
            "merge_base": HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_BASE,
        },
    )
    _block(
        "package_authorization",
        {
            "decision": PACKAGE_AUTHORIZING_DECISION,
            "pull_request": PACKAGE_AUTHORIZING_PULL_REQUEST,
            "merge_sha": PACKAGE_AUTHORIZING_MERGE_SHA,
        },
    )
    _block(
        "executable_package_identity",
        {
            "pull_request": EXECUTABLE_PACKAGE_PULL_REQUEST,
            "merge_sha": EXECUTABLE_PACKAGE_MERGE_SHA,
            "accepted_head": EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
            "merge_base": EXECUTABLE_PACKAGE_MERGE_BASE,
        },
    )
    # XASSET-0044's three further relationships, each closed and each re-verified from git below.
    _block(
        "prior_successor_rebinding",
        {
            "decision": PRIOR_SUCCESSOR_REBINDING_DECISION,
            "pull_request": PRIOR_SUCCESSOR_REBINDING_PULL_REQUEST,
            "merge_sha": PRIOR_SUCCESSOR_REBINDING_MERGE_SHA,
            "accepted_head": PRIOR_SUCCESSOR_REBINDING_ACCEPTED_HEAD,
            "merge_base": PRIOR_SUCCESSOR_REBINDING_MERGE_BASE,
        },
    )
    _block(
        "correction_identity",
        {
            "authorizing_decision": CORRECTION_AUTHORIZING_DECISION,
            "authorizing_pull_request": CORRECTION_AUTHORIZING_PULL_REQUEST,
            "authorizing_merge_sha": CORRECTION_AUTHORIZING_MERGE_SHA,
            "authorizing_accepted_head": CORRECTION_AUTHORIZING_ACCEPTED_HEAD,
            "authorizing_merge_base": CORRECTION_AUTHORIZING_MERGE_BASE,
            "decision": CORRECTED_MODULE_DECISION,
            "pull_request": CORRECTED_MODULE_PULL_REQUEST,
            "merge_sha": CORRECTED_MODULE_MERGE_SHA,
            "accepted_head": CORRECTED_MODULE_ACCEPTED_HEAD,
            "merge_base": CORRECTED_MODULE_MERGE_BASE,
        },
    )
    _block(
        "rebinding_authorization_identity",
        {
            "decision": REBINDING_AUTHORIZING_DECISION,
            "pull_request": REBINDING_AUTHORIZING_PULL_REQUEST,
            "merge_sha": REBINDING_AUTHORIZING_MERGE_SHA,
            "accepted_head": REBINDING_AUTHORIZING_ACCEPTED_HEAD,
            "merge_base": REBINDING_AUTHORIZING_MERGE_BASE,
        },
    )
    _block(
        "recovery_authorization_identity",
        {
            "decision": RECOVERY_AUTHORIZING_DECISION,
            "pull_request": RECOVERY_AUTHORIZING_PULL_REQUEST,
            "merge_sha": RECOVERY_AUTHORIZING_MERGE_SHA,
            "accepted_head": RECOVERY_AUTHORIZING_ACCEPTED_HEAD,
            "merge_base": RECOVERY_AUTHORIZING_MERGE_BASE,
        },
    )
    # XASSET-0049's two further relationships, each closed and each re-verified from git below.
    _block(
        "step8_equivalent_authorization_identity",
        {
            "decision": STEP8_EQUIVALENT_AUTHORIZING_DECISION,
            "pull_request": STEP8_EQUIVALENT_AUTHORIZING_PULL_REQUEST,
            "merge_sha": STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA,
            "accepted_head": STEP8_EQUIVALENT_AUTHORIZING_ACCEPTED_HEAD,
            "merge_base": STEP8_EQUIVALENT_AUTHORIZING_MERGE_BASE,
        },
    )
    _block(
        "prior_reconciliation_identity",
        {
            "decision": PRIOR_RECONCILIATION_DECISION,
            "pull_request": PRIOR_RECONCILIATION_PULL_REQUEST,
            "merge_sha": PRIOR_RECONCILIATION_MERGE_SHA,
            "accepted_head": PRIOR_RECONCILIATION_ACCEPTED_HEAD,
            "merge_base": PRIOR_RECONCILIATION_MERGE_BASE,
        },
    )
    # Adverse history, carried in the closed payload so it cannot be lost by omission. Every value
    # here is a REFUSAL record: the two lifecycles are named with their exact merges, exact accepted
    # heads, and the exact failed run and job at each merge, and each is explicitly marked as not
    # effective and not authority.
    _block(
        "stopped_lifecycle_identity",
        {
            "stopped_rebinding_decision": STOPPED_REBINDING_DECISION,
            "stopped_rebinding_pull_request": STOPPED_REBINDING_PULL_REQUEST,
            "stopped_rebinding_merge_sha": STOPPED_REBINDING_MERGE_SHA,
            "stopped_rebinding_accepted_head": STOPPED_REBINDING_ACCEPTED_HEAD,
            "stopped_rebinding_merge_base": STOPPED_REBINDING_MERGE_BASE,
            "stopped_rebinding_failed_ci_run": STOPPED_REBINDING_FAILED_CI_RUN,
            "stopped_rebinding_failed_ci_job": STOPPED_REBINDING_FAILED_CI_JOB,
            "stopped_recovery_authorization_decision": (
                STOPPED_RECOVERY_AUTHORIZATION_DECISION
            ),
            "stopped_recovery_authorization_pull_request": (
                STOPPED_RECOVERY_AUTHORIZATION_PULL_REQUEST
            ),
            "stopped_recovery_authorization_merge_sha": (
                STOPPED_RECOVERY_AUTHORIZATION_MERGE_SHA
            ),
            "stopped_recovery_authorization_accepted_head": (
                STOPPED_RECOVERY_AUTHORIZATION_ACCEPTED_HEAD
            ),
            "stopped_recovery_authorization_merge_base": (
                STOPPED_RECOVERY_AUTHORIZATION_MERGE_BASE
            ),
            "stopped_recovery_authorization_failed_ci_run": (
                STOPPED_RECOVERY_AUTHORIZATION_FAILED_CI_RUN
            ),
            "stopped_recovery_authorization_failed_ci_job": (
                STOPPED_RECOVERY_AUTHORIZATION_FAILED_CI_JOB
            ),
            "neither_is_effective": True,
            "neither_may_be_cited_as_authority": True,
            "neither_failed_run_may_be_represented_as_successful": True,
        },
    )

    # --- The historical operational authorization really is what the successor inherits from ---
    historical_parents = git.commit_parents(HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA)
    if historical_parents is None:
        errors.append(
            f"git truth: the historical operational-authorization merge "
            f"{HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA} is absent from the local object "
            "store, so the successor cannot prove what it is superseding"
        )
    elif list(historical_parents) != [
        HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_BASE,
        HISTORICAL_OPERATIONAL_AUTHORIZATION_ACCEPTED_HEAD,
    ]:
        errors.append(
            f"git truth: historical operational-authorization merge parents "
            f"{list(historical_parents)!r} do not match XASSET-0029's accepted identity"
        )

    # --- The package authority really merged ------------------------------------------------
    if git.commit_parents(PACKAGE_AUTHORIZING_MERGE_SHA) is None:
        errors.append(
            f"git truth: the package-authorizing merge {PACKAGE_AUTHORIZING_MERGE_SHA} "
            f"({PACKAGE_AUTHORIZING_DECISION}) is absent from the local object store"
        )

    # --- The executable package: exact parents, and ZERO merge drift -------------------------
    package_parents = git.commit_parents(EXECUTABLE_PACKAGE_MERGE_SHA)
    if package_parents is None:
        errors.append(
            f"git truth: the executable-package merge {EXECUTABLE_PACKAGE_MERGE_SHA} is absent "
            "from the local object store; the bytes being rebound cannot be identified"
        )
    elif list(package_parents) != [
        EXECUTABLE_PACKAGE_MERGE_BASE,
        EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
    ]:
        errors.append(
            f"git truth: executable-package merge parents {list(package_parents)!r} are not "
            f"[{EXECUTABLE_PACKAGE_MERGE_BASE!r}, {EXECUTABLE_PACKAGE_ACCEPTED_HEAD!r}]; a squash, "
            "rebase, or different base is not the accepted package"
        )
    package_merge_tree = git.commit_tree(EXECUTABLE_PACKAGE_MERGE_SHA)
    package_head_tree = git.commit_tree(EXECUTABLE_PACKAGE_ACCEPTED_HEAD)
    if package_merge_tree is None or package_head_tree is None:
        errors.append(
            "git truth: the executable package's merge or accepted-head tree could not be "
            "resolved, so zero merge drift cannot be proven for the package being rebound"
        )
    elif package_merge_tree != package_head_tree:
        errors.append(
            f"package merge drift: the executable-package merge tree {package_merge_tree} differs "
            f"from its accepted head tree {package_head_tree}; the merged package is not the "
            "package independent review accepted"
        )

    # --- The successor must actually descend from the package it claims to bind --------------
    if _is_commit_sha(merge_sha):
        if not git.is_ancestor(EXECUTABLE_PACKAGE_MERGE_SHA, str(merge_sha)):
            errors.append(
                f"git truth: the executable-package merge {EXECUTABLE_PACKAGE_MERGE_SHA} is not an "
                f"ancestor of the successor merge {merge_sha}; a rebinding cannot bind a package "
                "that is not in its own history"
            )
        if not git.is_ancestor(HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA, str(merge_sha)):
            errors.append(
                f"git truth: the historical operational-authorization merge "
                f"{HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA} is not an ancestor of the "
                f"successor merge {merge_sha}; the successor is not on the authorized history"
            )
        if not git.is_ancestor(PACKAGE_AUTHORIZING_MERGE_SHA, str(merge_sha)):
            errors.append(
                f"git truth: the package-authorizing merge {PACKAGE_AUTHORIZING_MERGE_SHA} is not "
                f"an ancestor of the successor merge {merge_sha}"
            )

    # --- XASSET-0044: the four inherited merges are real, undrifted, and actually inherited -----
    #
    # Each is verified the same way the executable package already is: exact parents in order (base
    # then accepted head), a merge tree byte-identical to the accepted head's tree so zero merge
    # drift is PROVEN rather than asserted, and ancestry into this rebinding's own merge. An
    # unobtainable anchor is never treated as agreement -- every branch below appends an error.
    inherited = (
        (
            "prior successor rebinding (XASSET-0037 / PR #337)",
            PRIOR_SUCCESSOR_REBINDING_MERGE_SHA,
            PRIOR_SUCCESSOR_REBINDING_MERGE_BASE,
            PRIOR_SUCCESSOR_REBINDING_ACCEPTED_HEAD,
        ),
        (
            "correction authorization (XASSET-0041 / PR #341)",
            CORRECTION_AUTHORIZING_MERGE_SHA,
            CORRECTION_AUTHORIZING_MERGE_BASE,
            CORRECTION_AUTHORIZING_ACCEPTED_HEAD,
        ),
        (
            "corrected module (XASSET-0042 / PR #342)",
            CORRECTED_MODULE_MERGE_SHA,
            CORRECTED_MODULE_MERGE_BASE,
            CORRECTED_MODULE_ACCEPTED_HEAD,
        ),
        (
            "rebinding authorization (XASSET-0043 / PR #343)",
            REBINDING_AUTHORIZING_MERGE_SHA,
            REBINDING_AUTHORIZING_MERGE_BASE,
            REBINDING_AUTHORIZING_ACCEPTED_HEAD,
        ),
        # XASSET-0047 appends three more, on exactly the same terms and with exactly the same
        # rigour. The first is this recovery's own AUTHORITY. The other two are the STOPPED
        # lifecycles it supersedes as the anchor: they are verified here as HISTORY -- real,
        # ordered, undrifted, and genuinely inherited -- and nowhere as authority. Verifying a
        # stopped lifecycle is not treating it as effective; refusing to verify it is how a
        # successor quietly disowns the history it actually stands on.
        (
            "recovery authorization (XASSET-0046 / PR #346)",
            RECOVERY_AUTHORIZING_MERGE_SHA,
            RECOVERY_AUTHORIZING_MERGE_BASE,
            RECOVERY_AUTHORIZING_ACCEPTED_HEAD,
        ),
        (
            "STOPPED rebinding (XASSET-0044 / PR #344) -- history, never authority",
            STOPPED_REBINDING_MERGE_SHA,
            STOPPED_REBINDING_MERGE_BASE,
            STOPPED_REBINDING_ACCEPTED_HEAD,
        ),
        (
            "STOPPED recovery authorization (XASSET-0045 / PR #345) -- history, never authority",
            STOPPED_RECOVERY_AUTHORIZATION_MERGE_SHA,
            STOPPED_RECOVERY_AUTHORIZATION_MERGE_BASE,
            STOPPED_RECOVERY_AUTHORIZATION_ACCEPTED_HEAD,
        ),
        # XASSET-0049 appends two more, on exactly the same terms and with exactly the same
        # rigour. The first is the PRIOR ANCHOR this rebinding supersedes -- a CLOSED predecessor
        # whose own lifecycle really completed, verified here as inherited history exactly as
        # XASSET-0037's is, and NOT on the footing of the two stopped lifecycles above it. The
        # second is this rebinding's own AUTHORITY.
        (
            "prior reconciliation anchor (XASSET-0047 / PR #347)",
            PRIOR_RECONCILIATION_MERGE_SHA,
            PRIOR_RECONCILIATION_MERGE_BASE,
            PRIOR_RECONCILIATION_ACCEPTED_HEAD,
        ),
        (
            "step-8-equivalent authorization (XASSET-0048 / PR #348)",
            STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA,
            STEP8_EQUIVALENT_AUTHORIZING_MERGE_BASE,
            STEP8_EQUIVALENT_AUTHORIZING_ACCEPTED_HEAD,
        ),
    )
    for label, inherited_merge, inherited_base, inherited_head in inherited:
        # MAJOR 1 (review 4986931575): an absent anchor is a REFUSAL, never a skip. Previously a
        # ``None`` base or head quietly disabled this entry's parent-order and merge-tree checks,
        # so an unverifiable merge read as a verified one. Every entry above now carries real
        # identities, and this branch exists so no future entry can re-open the hole by omission.
        if inherited_base is None or inherited_head is None:
            errors.append(
                f"authority: the {label} merge {inherited_merge} is bound without a complete "
                "base/accepted-head identity, so its exact parents and zero merge drift cannot be "
                "proven; an unverifiable inherited merge never authorizes execution"
            )
            continue
        parents = git.commit_parents(inherited_merge)
        if parents is None:
            errors.append(
                f"git truth: the {label} merge {inherited_merge} is absent from the local object "
                "store, so this rebinding cannot prove what it inherits from"
            )
        elif list(parents) != [inherited_base, inherited_head]:
            errors.append(
                f"git truth: {label} merge parents {list(parents)!r} are not exactly "
                f"[{inherited_base!r}, {inherited_head!r}]"
            )
        merge_tree = git.commit_tree(inherited_merge)
        head_tree = git.commit_tree(inherited_head)
        if merge_tree is None or head_tree is None:
            errors.append(
                f"git truth: the {label} merge or accepted-head tree could not be resolved, so "
                "zero merge drift cannot be proven; this fails closed"
            )
        elif merge_tree != head_tree:
            errors.append(
                f"git truth: the {label} merge tree {merge_tree} differs from its accepted-head "
                f"tree {head_tree}; the merge carries drift the review never saw"
            )
        if _is_commit_sha(merge_sha) and not git.is_ancestor(inherited_merge, str(merge_sha)):
            errors.append(
                f"git truth: the {label} merge {inherited_merge} is not an ancestor of the "
                f"rebinding merge {merge_sha}; this rebinding is not on the authorized history"
            )

    # The reviewed base of THIS unit is the authorization that made it lawful to begin. Stated as
    # an equality rather than left to coincidence: a unit branched from anywhere else has not
    # actually waited for its authorizing decision's lifecycle to close.
    #
    # RE-ANCHORED BY XASSET-0049, not relaxed. XASSET-0044 compared against XASSET-0043's merge,
    # XASSET-0047 against XASSET-0046's, because each named the decision that authorized it. This
    # unit's authorizing decision is XASSET-0048, so the equality now names XASSET-0048's merge.
    # XASSET-0043's and XASSET-0046's own merges stay fully verified in the inherited-merge table
    # above -- exact parents, zero drift, ancestry -- so nothing about either stopped being
    # checked; only the question "which merge is THIS unit's authority" got its correct current
    # answer.
    #
    # STRENGTHENED, NOT MERELY MOVED. XASSET-0048 SS-F.2 makes EQUALITY the operative rule and
    # descent explicitly insufficient, so the check below delegates to a PURE function that
    # decides the whole proposition -- equality AND retained ancestry AND well-formedness -- and
    # refuses a later descendant even when ancestry is granted unconditionally.
    errors.extend(
        _verify_step8_equivalent_base_equality(
            REVIEWED_BASE_SHA,
            STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA,
            git.is_ancestor(STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA, str(merge_sha))
            if _is_commit_sha(merge_sha)
            else None,
        )
    )
    errors.extend(_verify_recovery_lifecycle_anchor(merge_sha))

    # --- SS-G.B's invariant: outcome-producing bytes are the package's, unchanged --------------
    accepted_head = document.get("authorization_head")
    for relative in EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS:
        if relative not in LOAD_BEARING_RELPATHS:
            errors.append(
                f"trust boundary: {relative} produces Stage-1 outcomes but is not load-bearing; "
                "SS-G.B's invariant forbids outcome-producing code outside the bound identity"
            )
        anchors = {
            "executable-package accepted head": EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
            "executable-package merge": EXECUTABLE_PACKAGE_MERGE_SHA,
        }
        if _is_commit_sha(accepted_head):
            anchors["successor reviewed head"] = str(accepted_head)
        if _is_commit_sha(merge_sha):
            anchors["successor merge"] = str(merge_sha)
        digests: dict[str, str] = {}
        for label, commit in anchors.items():
            digest = git.blob_sha256_at(commit, relative)
            if digest is None:
                errors.append(
                    f"git truth: {relative} is absent from the {label} {commit}; the "
                    "outcome-producing bytes being rebound cannot be identified"
                )
                continue
            digests[label] = digest
        working = sha256_file(ROOT / relative) if (ROOT / relative).exists() else None
        if working is None:
            errors.append(f"{relative}: absent from the working tree")
        else:
            digests["working tree"] = working
        if len(set(digests.values())) > 1:
            errors.append(
                f"outcome-producing drift: {relative} is not byte-identical across the accepted "
                f"executable package and this rebinding ({digests!r}); SS-G.B forbids changing "
                "outcome-producing code inside the rebinding that binds it"
            )

    # --- MAJOR 1: the TRANSITIVE surface, projected rather than byte-compared -----------------
    errors.extend(_verify_outcome_producing_transition(document, merge_sha, sources))
    return errors


def verify_exact_rebound_transition(successor: bytes, rebound: bytes) -> None:
    """Prove ``successor`` became ``rebound`` through EXACTLY the reviewed link-2 manifest, or raise.

    Link 2 of ``package -> successor -> rebound``. It reuses :func:`verify_exact_transition`'s
    mechanism unchanged -- the same five enforced properties, the same byte-only instrument, no
    parsing, importing, executing, ``eval``, or version-dependent diff algorithm -- and supplies
    only its own frozen expected identities. Link 1 is untouched by this and is still verified
    separately.
    """
    verify_exact_transition(
        successor,
        rebound,
        OUTCOME_PRODUCING_REBOUND_TRANSITION,
        package_length=OUTCOME_PRODUCING_SUCCESSOR_LENGTH,
        package_sha256=OUTCOME_PRODUCING_SUCCESSOR_SHA256,
        successor_length=OUTCOME_PRODUCING_REBOUND_LENGTH,
        successor_sha256=OUTCOME_PRODUCING_REBOUND_SHA256,
    )


def _verify_outcome_producing_transition(
    document: Mapping[str, Any], merge_sha: Any, sources: TruthSources
) -> list[str]:
    """Prove the derivation module's EXACT package-to-successor transition across five anchors.

    The runner and result validator import their disposition, cell-outcome, roll-up, ``G2``-reading
    and vocabulary decisions from ``level1_endpoint_evidence_preregistration_validator.py``. Whole-
    file equality with the package is the wrong instrument -- this rebinding must lawfully change
    that file's authorization-only code -- and a semantic projection of it was found nonconvergent
    (review 4963386313). What is enforced instead is finite and decidable:

    * the two PACKAGE anchors must carry the exact accepted package blob;
    * the successor reviewed head, the successor merge, and the working tree must carry the exact
      successor blob;
    * and the package blob must have become the successor blob through EXACTLY the reviewed closed
      transition -- see :func:`verify_exact_transition`.

    Fails closed on any anchor whose blob is missing or undecodable. It never treats an unobtainable
    anchor as agreement.
    """
    errors: list[str] = []
    relative = OUTCOME_PRODUCING_DERIVATION_RELPATH

    if relative not in LOAD_BEARING_RELPATHS:
        errors.append(
            f"trust boundary: {relative} supplies the outcome-producing derivation surface but is "
            "not load-bearing"
        )

    def blob_at(commit: str, label: str) -> bytes | None:
        text = sources.git.blob_text_at(commit, relative)
        if text is None:
            errors.append(
                f"git truth: {relative} could not be read at the {label} {commit}; the exact "
                "package-to-successor transition cannot be proven, so this fails closed"
            )
            return None
        return text.encode("utf-8")

    package_anchors = {
        "executable-package accepted head": EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
        "executable-package merge": EXECUTABLE_PACKAGE_MERGE_SHA,
    }
    # XASSET-0044: the accepted SUCCESSOR blob is now proven at XASSET-0037's OWN anchors, which are
    # immutable history, rather than at this rebinding's anchors -- those now carry the REBOUND
    # blob. Link 1 is therefore still verified end to end; it is not weakened, only re-anchored to
    # the commits that actually carry its bytes.
    successor_anchors: dict[str, str] = {
        "prior-rebinding accepted head": PRIOR_SUCCESSOR_REBINDING_ACCEPTED_HEAD,
        "prior-rebinding merge": PRIOR_SUCCESSOR_REBINDING_MERGE_SHA,
    }
    rebound_anchors: dict[str, str] = {}
    accepted_head = document.get("authorization_head")
    if _is_commit_sha(accepted_head):
        rebound_anchors["rebinding reviewed head"] = str(accepted_head)
    if _is_commit_sha(merge_sha):
        rebound_anchors["rebinding merge"] = str(merge_sha)

    package_bytes: bytes | None = None
    for label, commit in package_anchors.items():
        blob = blob_at(commit, label)
        if blob is None:
            continue
        digest = sha256_bytes(blob)
        if digest != OUTCOME_PRODUCING_PACKAGE_SHA256:
            errors.append(
                f"{relative} at the {label} {commit} hashes {digest}, but the accepted executable "
                f"package is {OUTCOME_PRODUCING_PACKAGE_SHA256}; the transition's starting bytes "
                "are not the reviewed ones"
            )
            continue
        package_bytes = blob

    successor_bytes: bytes | None = None
    for label, commit in successor_anchors.items():
        blob = blob_at(commit, label)
        if blob is None:
            continue
        digest = sha256_bytes(blob)
        if digest != OUTCOME_PRODUCING_SUCCESSOR_SHA256:
            errors.append(
                f"{relative} at the {label} {commit} hashes {digest}, but the reviewed successor "
                f"bytes are {OUTCOME_PRODUCING_SUCCESSOR_SHA256}"
            )
            continue
        successor_bytes = blob

    rebound_bytes: bytes | None = None
    for label, commit in rebound_anchors.items():
        blob = blob_at(commit, label)
        if blob is None:
            continue
        digest = sha256_bytes(blob)
        if digest != OUTCOME_PRODUCING_REBOUND_SHA256:
            errors.append(
                f"{relative} at the {label} {commit} hashes {digest}, but the reviewed rebound "
                f"bytes are {OUTCOME_PRODUCING_REBOUND_SHA256}"
            )
            continue
        rebound_bytes = blob

    working_path = ROOT / relative
    if not working_path.exists():
        errors.append(f"{relative}: absent from the working tree")
    else:
        try:
            working = working_path.read_bytes()
        except OSError as exc:  # pragma: no cover - defensive
            errors.append(f"{relative}: unreadable in the working tree: {exc}")
        else:
            digest = sha256_bytes(working)
            if digest != OUTCOME_PRODUCING_REBOUND_SHA256:
                errors.append(
                    f"{relative} in the working tree hashes {digest}, but the reviewed rebound "
                    f"bytes are {OUTCOME_PRODUCING_REBOUND_SHA256}"
                )
            else:
                rebound_bytes = working

    if package_bytes is None or successor_bytes is None or rebound_bytes is None:
        if not errors:  # pragma: no cover - defensive
            errors.append(
                f"{relative}: the exact package-to-successor-to-rebound transition chain could "
                "not be established"
            )
        return errors

    try:
        verify_exact_transition(package_bytes, successor_bytes)
    except TransitionError as exc:
        errors.append(
            f"{relative}: the accepted package bytes did not become the reviewed successor bytes "
            f"through the reviewed transition ({exc})"
        )
    # XASSET-0044 / XASSET-0043 SS-G.4a link 2. APPENDED, never replacing link 1: both must hold.
    try:
        verify_exact_rebound_transition(successor_bytes, rebound_bytes)
    except TransitionError as exc:
        errors.append(
            f"{relative}: the accepted successor bytes did not become the reviewed rebound bytes "
            f"through the reviewed rebound transition ({exc})"
        )
    return errors


def _verify_selected_review_is_final(
    sources: TruthSources,
    number: Any,
    head: Any,
    selected_review_id: str,
    selected_submitted_at: Any,
    pull: Mapping[str, Any],
) -> list[str]:
    """Reject a later non-dismissed adverse review on the EXACT accepted head.

    Scope, stated precisely:

      * only reviews on the exact accepted head matter -- reviews on older heads are history and
        never invalidate the current head;
      * only reviews submitted AFTER the selected approving review and BEFORE the merge matter;
      * a DISMISSED later review does not count as a live adverse finding;
      * a later APPROVING review is not adverse.
    """
    errors: list[str] = []
    listing = sources.governance.reviews(number) if isinstance(number, int) else None
    if listing is None:
        errors.append(
            "governance truth: the pull request's review list could not be retrieved, so the "
            "selected review's finality cannot be established; this fails closed"
        )
        return errors

    merged_at = str(pull.get("merged_at") or "")
    selected_at = str(selected_submitted_at or "")
    for entry in listing:
        if not isinstance(entry, Mapping):
            continue
        if str(entry.get("id")) == str(selected_review_id):
            continue
        if entry.get("commit_id") != head:
            continue  # a different head: historical, not a live finding on this one
        if str(entry.get("state") or "").upper() == "DISMISSED":
            continue
        submitted = str(entry.get("submitted_at") or "")
        if selected_at and submitted and submitted <= selected_at:
            continue  # precedes the final clean pass: legitimate history
        if merged_at and submitted and submitted > merged_at:
            continue  # after the merge: outside this lifecycle
        state = str(entry.get("state") or "").upper()
        verdict = parse_formal_disposition(entry.get("body") or "")

        # GitHub's NATIVE state is durable truth and must never be weaker than the repository's
        # own body grammar. A later CHANGES_REQUESTED is adverse whether or not it carries a
        # formal line.
        if state in NATIVE_ADVERSE_REVIEW_STATES:
            errors.append(
                f"governance truth: review {entry.get('id')} on the exact accepted head is a "
                f"later non-dismissed {state} review submitted after the certified review "
                f"{selected_review_id}; principal certification of an earlier clean pass does "
                "not erase a later exact-head finding"
            )
            continue
        # XASSET-0053 §D.19 / §D.20.2: an unsupported formal-looking line fails closed HERE,
        # before any native-state branch, so a native APPROVED can never rescue it. The
        # genuinely-ABSENT policy immediately below is deliberately PRESERVED (§D.20.1).
        if verdict is MALFORMED_FORMAL_DISPOSITION:
            errors.append(
                f"governance truth: review {entry.get('id')} on the exact accepted head, "
                f"submitted after the certified review {selected_review_id}, carries a "
                f"'{FORMAL_DISPOSITION_PREFIX}' line that is not in an accepted form; an "
                f"unsupported formal line fails closed and its native state "
                f"({state or 'unset'!r}) never rescues it"
            )
            continue
        if verdict == APPROVING_REVIEW_DISPOSITION:
            continue  # a later approving pass is not adverse
        if verdict is None:
            # Unclassifiable: neither a native adverse state nor a parseable formal disposition.
            # Finality cannot be asserted over a review whose verdict is unknown, so this fails
            # closed rather than being silently ignored.
            if state in NATIVE_NON_ADVERSE_REVIEW_STATES:
                continue
            errors.append(
                f"governance truth: review {entry.get('id')} on the exact accepted head, "
                f"submitted after the certified review {selected_review_id}, carries neither a "
                f"recognised native state ({state or 'unset'!r}) nor a parseable formal "
                "disposition, so it cannot be proven non-adverse; finality fails closed"
            )
            continue
        errors.append(
            f"governance truth: review {entry.get('id')} on the exact accepted head carries "
            f"the later adverse formal disposition {verdict!r}, submitted after the certified "
            f"review {selected_review_id}; principal certification of an earlier clean pass "
            "does not erase a later exact-head finding"
        )
    return errors


def _verify_git_anchored_identity(
    document: Mapping[str, Any], merge_sha: Any, sources: TruthSources
) -> list[str]:
    """MAJOR 1: predecessor identity, current ancestry, and load-bearing byte identity."""
    errors: list[str] = []

    # Predecessor XASSET-0028 identity, verified from git rather than merely declared.
    recorded_predecessor = document.get("predecessor_identity")
    if not isinstance(recorded_predecessor, Mapping):
        errors.append("predecessor_identity: expected a mapping")
    else:
        _exact(
            recorded_predecessor.get("merge_sha"),
            PREDECESSOR_MERGE_SHA,
            "predecessor_identity.merge_sha",
            errors,
        )
        _exact(
            recorded_predecessor.get("accepted_head"),
            PREDECESSOR_ACCEPTED_HEAD,
            "predecessor_identity.accepted_head",
            errors,
        )
        _exact(
            recorded_predecessor.get("merge_base"),
            PREDECESSOR_MERGE_BASE,
            "predecessor_identity.merge_base",
            errors,
        )
    predecessor_parents = sources.git.commit_parents(PREDECESSOR_MERGE_SHA)
    if predecessor_parents is None:
        errors.append(
            f"git truth: predecessor merge {PREDECESSOR_MERGE_SHA} is absent from the local "
            "object store"
        )
    elif list(predecessor_parents) != [PREDECESSOR_MERGE_BASE, PREDECESSOR_ACCEPTED_HEAD]:
        errors.append(
            f"git truth: predecessor merge parents {list(predecessor_parents)!r} do not match "
            f"XASSET-0028's accepted identity"
        )

    # Current ancestry: the authorizing merge must be reachable from the working HEAD.
    head_now = sources.git.head()
    if not head_now:
        errors.append("git truth: current HEAD could not be resolved")
    elif _is_commit_sha(merge_sha) and not sources.git.is_ancestor(merge_sha, head_now):
        errors.append(
            f"git truth: the authorizing merge {merge_sha} is not an ancestor of the current "
            f"HEAD {head_now}; the working tree is not on the authorized history"
        )

    # Load-bearing byte identity: expected values come from the MERGED TREE, not a constant.
    recorded = document.get("load_bearing_identity")
    if not isinstance(recorded, Mapping):
        errors.append("load_bearing_identity: expected a mapping")
        return errors
    if sorted(recorded) != sorted(LOAD_BEARING_RELPATHS):
        errors.append(
            "load_bearing_identity: must cover exactly the load-bearing files "
            f"{sorted(LOAD_BEARING_RELPATHS)!r}"
        )
    accepted_head = document.get("authorization_head")
    for relative in sorted(LOAD_BEARING_RELPATHS):
        if not _is_commit_sha(merge_sha):
            continue
        merged = sources.git.blob_sha256_at(str(merge_sha), relative)
        if merged is None:
            errors.append(
                f"git truth: {relative} is absent from the authorized merged tree {merge_sha}"
            )
            continue
        # MAJOR 2: the merged tree may not become its own source of truth. Every load-bearing
        # blob must ALSO equal the same blob in the independently reviewed head.
        if _is_commit_sha(accepted_head):
            reviewed = sources.git.blob_sha256_at(str(accepted_head), relative)
            if reviewed is None:
                errors.append(
                    f"git truth: {relative} is absent from the reviewed head {accepted_head}"
                )
            elif reviewed != merged:
                errors.append(
                    f"merge drift: {relative} differs between the reviewed head "
                    f"({reviewed}) and the merged tree ({merged}); merging changed a "
                    "load-bearing file that independent review never saw"
                )
        if recorded.get(relative) != merged:
            errors.append(
                f"load_bearing_identity[{relative!r}]: recorded {recorded.get(relative)!r} but "
                f"the authorized merged tree has {merged!r}"
            )
        working = sha256_file(ROOT / relative) if (ROOT / relative).exists() else None
        if working != merged:
            errors.append(
                f"enforcement drift: {relative} in the working tree hashes to {working!r} but "
                f"the authorized merged tree has {merged!r}; load-bearing code has changed "
                "since the authorized merge"
            )
    return errors


# ======================================================================================
# Document validation
# ======================================================================================


def validate_authorization_document(
    document: Any, sources: TruthSources | None = None
) -> ValidationResult:
    """Validate an attestation: closed schema, bound identity, and AUTHENTICATED lifecycle."""
    errors: list[str] = []

    root = _mapping(document, "authorization", errors)
    if root is None:
        return ValidationResult(False, tuple(errors))

    for key in sorted(set(root) - set(REQUIRED_TOP_KEYS)):
        errors.append(f"authorization.{key}: unknown key; the schema is closed")
    for key in REQUIRED_TOP_KEYS:
        if key not in root:
            errors.append(f"authorization.{key}: required key is absent")
    if errors:
        return ValidationResult(False, tuple(errors))

    _exact(root.get("schema_version"), SCHEMA_VERSION, "authorization.schema_version", errors)
    _exact(root.get("mechanism"), AUTHORIZATION_MECHANISM, "authorization.mechanism", errors)
    _exact(root.get("repository"), REPOSITORY_IDENTITY, "authorization.repository", errors)
    _exact(root.get("study_id"), STUDY_ID, "authorization.study_id", errors)
    _exact(
        root.get("authorizing_decision"),
        AUTHORIZING_DECISION,
        "authorization.authorizing_decision",
        errors,
    )
    _exact(
        root.get("authorizing_pull_request"),
        AUTHORIZING_PULL_REQUEST,
        "authorization.authorizing_pull_request",
        errors,
    )
    _exact(
        root.get("predecessor_decision"),
        PREDECESSOR_DECISION,
        "authorization.predecessor_decision",
        errors,
    )
    _exact(
        root.get("execution_attempt_id"),
        EXECUTION_ATTEMPT_ID,
        "authorization.execution_attempt_id",
        errors,
    )
    if not _is_commit_sha(root.get("authorization_head")):
        errors.append("authorization.authorization_head: expected a 40-character commit SHA")

    _validate_canonical_pins(root.get("canonical_pins"), errors)
    _validate_construction_universe(root.get("construction_universe"), errors)
    _validate_lifecycle_shape(root.get("lifecycle_evidence"), errors)

    if not isinstance(root.get("author_identity"), str) or not root["author_identity"].strip():
        errors.append("authorization.author_identity: expected a non-empty string")
    if not isinstance(root.get("generated_at_utc"), str) or not root["generated_at_utc"].strip():
        errors.append("authorization.generated_at_utc: expected a non-empty string")

    # AUTHENTICATION. Structural shape alone never authorizes.
    errors.extend(verify_lifecycle_against_truth(root, sources or TruthSources()))
    return ValidationResult(not errors, tuple(errors))


def _validate_canonical_pins(block: Any, errors: list[str]) -> None:
    pins = _mapping(block, "authorization.canonical_pins", errors)
    if pins is None:
        return
    if pins_are_placeholders():
        errors.append(
            f"authorization.canonical_pins: {AUTHORIZING_DECISION} successor pins have not been "
            "refreshed to real digests, so no attestation can be validated"
        )
        return
    live = live_canonical_hashes()
    for relative, bound in sorted(CANONICAL_PINS.items()):
        if pins.get(relative) != bound:
            errors.append(
                f"authorization.canonical_pins[{relative!r}]: recorded {pins.get(relative)!r} "
                f"but the bound {AUTHORIZING_DECISION} pin is {bound!r}"
            )
        if live.get(relative) != bound:
            errors.append(
                f"canonical drift: {relative} on disk hashes to {live.get(relative)!r} but the "
                f"bound {AUTHORIZING_DECISION} pin is {bound!r}"
            )
        # XASSET-0037: an amendment that left the bytes identical to a predecessor's would mean the
        # successor pin was copied forward rather than recomputed after the bytes stabilized.
        for label, historical in (
            (PACKAGE_AUTHORIZING_DECISION, XASSET_0036_PACKAGE_CANONICAL_PINS),
            (HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION, XASSET_0029_CANONICAL_PINS),
            (PREDECESSOR_DECISION, PREDECESSOR_CANONICAL_PINS),
        ):
            if bound == historical.get(relative):
                errors.append(
                    f"canonical pins: {relative} still carries the {label} pin; the successor "
                    "amendment must change the canonical bytes it re-pins"
                )
    for relative in sorted(set(pins) - set(CANONICAL_PINS)):
        errors.append(
            f"authorization.canonical_pins[{relative!r}]: unknown canonical file; the pin set "
            "is closed"
        )


def _validate_construction_universe(block: Any, errors: list[str]) -> None:
    recorded = _mapping(block, "authorization.construction_universe", errors)
    if recorded is None:
        return
    _exact(
        recorded.get("sha256"),
        CONSTRUCTION_UNIVERSE_SHA256,
        "authorization.construction_universe.sha256",
        errors,
    )
    _exact(
        recorded.get("count"), CONSTRUCTION_COUNT, "authorization.construction_universe.count", errors
    )
    _exact(
        recorded.get("cell_count"),
        CONSTRUCTION_CELL_COUNT,
        "authorization.construction_universe.cell_count",
        errors,
    )
    try:
        live = live_construction_universe_facts()
    except Exception as exc:  # pragma: no cover - defensive
        errors.append(f"construction universe could not be recomputed live: {exc}")
        return
    if live["sha256"] != CONSTRUCTION_UNIVERSE_SHA256:
        errors.append(f"universe drift: live universe hashes to {live['sha256']!r}")
    if live["count"] != CONSTRUCTION_COUNT:
        errors.append(f"universe drift: live universe has {live['count']} constructions")
    if live["cell_count"] != CONSTRUCTION_CELL_COUNT:
        errors.append(f"universe drift: live universe has {live['cell_count']} cells")


def _validate_lifecycle_shape(block: Any, errors: list[str]) -> None:
    """Structural shape only. Authenticity is established by verify_lifecycle_against_truth."""
    evidence = _mapping(block, "authorization.lifecycle_evidence", errors)
    if evidence is None:
        return
    where = "authorization.lifecycle_evidence"
    for key in REQUIRED_LIFECYCLE_EVIDENCE_KEYS:
        if key not in evidence:
            errors.append(f"{where}.{key}: required gate evidence is absent")
    for key in sorted(set(evidence) - set(REQUIRED_LIFECYCLE_EVIDENCE_KEYS) - {"gates_closed"}):
        errors.append(f"{where}.{key}: unknown gate evidence; the schema is closed")
    declared = evidence.get("gates_closed") or ()
    if not isinstance(declared, (list, tuple)):
        errors.append(f"{where}.gates_closed: expected a list")
        declared = ()
    for gate in REQUIRED_LIFECYCLE_GATES:
        if gate not in declared:
            errors.append(f"{where}.gates_closed: must include {gate!r}")
    for gate in declared:
        if gate not in REQUIRED_LIFECYCLE_GATES:
            errors.append(f"{where}.gates_closed: unknown gate {gate!r}")
    review = evidence.get("independent_review")
    if isinstance(review, Mapping):
        for counter in ("blocking_count", "major_count"):
            if review.get(counter) != 0:
                errors.append(
                    f"{where}.independent_review.{counter}: expected 0 unresolved, found "
                    f"{review.get(counter)!r}"
                )


# ======================================================================================
# Lane state machine — BLOCKING 2
# ======================================================================================


@dataclass(frozen=True)
class LanePaths:
    authorization: Path = AUTHORIZATION_PATH
    claim: Path = CLAIM_PATH
    completion: Path = COMPLETION_PATH
    ledger: Path = LEDGER_PATH


def _read_ledger(path: Path) -> list[Mapping[str, Any]]:
    if not path.exists():
        return []
    entries: list[Mapping[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line, object_pairs_hook=_reject_duplicate_keys)
        except (ValueError, json.JSONDecodeError):
            entries.append({"event": LEDGER_CORRUPT})
            continue
        # MINOR 1 (review 4946540894): a syntactically valid line that is not a mapping -- `[]`,
        # `"junk"`, `null`, `42` -- was SILENTLY DROPPED rather than treated as corruption, which
        # is weaker than the canonical promise that malformed entries fail closed. Every
        # non-empty line must decode to exactly one mapping or the ledger is corrupt.
        entries.append(entry if isinstance(entry, Mapping) else {"event": LEDGER_CORRUPT})
    return entries


def _append_ledger(path: Path, entry: Mapping[str, Any]) -> None:
    """Append-only. Losing claim.json alone therefore cannot reopen the lane."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(descriptor, "a", encoding="utf-8") as handle:
        handle.write(canonical_json(entry) + "\n")


def _load_authorization(path: Path) -> tuple[Mapping[str, Any] | None, str]:
    if not path.exists():
        return None, "no attestation present"
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"attestation unreadable: {exc}"
    try:
        document = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
    except (ValueError, json.JSONDecodeError) as exc:
        return None, f"attestation malformed: {exc}"
    if not isinstance(document, Mapping):
        return None, "attestation is not a mapping"
    return document, ""


def lane_state_at(
    paths: LanePaths, sources: TruthSources | None = None
) -> tuple[str, str]:
    """Return the lane state and, when not READY, why a new execution may not start.

    A claim recorded in EITHER ``claim.json`` OR the append-only ledger establishes CLAIMED,
    so losing one record alone does not reopen the lane. No attestation means ABSENT, which
    is not READY -- destroying the directory fails closed rather than resetting.
    """
    ledger = _read_ledger(paths.ledger)
    ledger_events = {str(entry.get("event")) for entry in ledger}

    if paths.completion.exists() or LANE_COMPLETED in ledger_events:
        return LANE_COMPLETED, (
            f"the single authorized attempt ({EXECUTION_ATTEMPT_ID}) has already completed; a "
            "second execution requires new governance authority"
        )
    if paths.claim.exists() or LANE_CLAIMED in ledger_events:
        return LANE_CLAIMED, (
            f"the single authorized attempt ({EXECUTION_ATTEMPT_ID}) is already claimed; a "
            "crash after claiming does not reopen the lane, and recovery is a governed act"
        )

    # MINOR 1 (review 4946706062): a ledger ALREADY KNOWN to be corrupt did not block
    # READY -> CLAIMED. `_read_ledger` marked the bad line and `_ledger_events` rejected it, but
    # that rejection was only ever consulted while RECOVERING claim/completion provenance -- here
    # a lone CORRUPT entry fell straight through to the attestation check. Reproduced before
    # correcting: with a valid attestation plus a pre-seeded `[]` ledger line, this returned
    # READY, `new_execution_is_authorized()` returned true, and `claim_execution()` wrote
    # claim.json and appended CLAIMED onto the corrupt ledger. Only the LATER
    # `claimed_execution_is_authorized()` noticed -- after the one authorized attempt had begun.
    #
    # Deliberately placed AFTER the CLAIMED/COMPLETED determination, not before: an already
    # claimed or completed lane is non-READY either way, and reordering would replace
    # `_authenticated_claim`'s precise corrupt-ledger error with a bare "lane state ABSENT",
    # weakening a message the mirror logic already gets right. The mirror rules, the
    # single-record-loss semantics, and the lane states themselves are untouched -- this only
    # refuses to call a lane READY when its provenance ledger is already unreadable.
    if LEDGER_CORRUPT in ledger_events:
        return LANE_ABSENT, (
            "the append-only ledger contains a corrupt entry, so this lane's provenance is "
            "already unreadable and no new execution may start in it. The single authorized "
            f"attempt ({EXECUTION_ATTEMPT_ID}) must not begin under invalid audit state; "
            "repairing the ledger is a governed act, not an automatic recovery"
        )

    document, problem = _load_authorization(paths.authorization)
    if document is None:
        # MINOR 1 (delta review 4987958687): this reason printed only REQUIRED_LIFECYCLE_GATES,
        # so after Gate 8 it UNDERSTATED what the operator actually has to complete. The six-gate
        # tuple and every canonical predecessor string are deliberately left byte-identical -- they
        # are a differently-scoped, accepted, historically-named list -- so the additional
        # requirement is stated here, in the CURRENT status explanation, rather than by rewriting
        # them. See LIFECYCLE_CLOSURE_STATUS_REQUIREMENT.
        return LANE_ABSENT, (
            f"{problem}. Structural closure of the construction universe is not authorization: "
            f"the {AUTHORIZING_DECISION} lifecycle must close in full "
            f"({', '.join(REQUIRED_LIFECYCLE_GATES)}), {LIFECYCLE_CLOSURE_STATUS_REQUIREMENT}, "
            "and an authenticated one-shot attestation must then be generated. There is no "
            "merge-to-execution gap"
        )
    result = validate_authorization_document(document, sources)
    if not result.valid:
        return LANE_ABSENT, "attestation invalid: " + "; ".join(result.errors)
    return LANE_READY, ""


def new_execution_is_authorized(
    paths: LanePaths | None = None, sources: TruthSources | None = None
) -> tuple[bool, str]:
    """May a NEW Stage-1 execution start? READY only. PUBLIC and fail-closed."""
    state, reason = lane_state_at(paths or LanePaths(), sources)
    return (state == LANE_READY), reason


def _ledger_events(paths: LanePaths, event: str) -> tuple[list[Mapping[str, Any]], str]:
    """Return the ledger's events of one kind, or an error if the ledger is unusable."""
    entries = _read_ledger(paths.ledger)
    if any(e.get("event") == LEDGER_CORRUPT for e in entries):
        return [], "the append-only ledger contains a corrupt entry"
    return [e for e in entries if e.get("event") == event], ""


def _recover_mirrored_record(
    paths: LanePaths, path: Path, event: str
) -> tuple[Mapping[str, Any] | None, str, str]:
    """Recover a lane record from its file and its ledger mirror, requiring them to AGREE.

    BLOCKING 1 (review 4946464366): the file was treated as authoritative whenever present and
    the ledger mirror was never consulted, so rewriting only ``completion.json`` retargeted the
    lawful run from result A to result B while the ledger still bound A. Reproduced before
    correcting. The two copies are a CONSISTENCY CHECK, not interchangeable alternatives:

      * both present  -> they must be the same canonical record, byte for byte;
      * file missing  -> recover only from exactly ONE unique uncorrupted ledger event;
      * ledger event missing but file present -> permitted, and ONLY this case, because it is
        exactly the single-record loss the disclosed durability model already covers;
      * conflicting, duplicated-different, malformed, or corrupt entries -> FAIL CLOSED.

    Returns ``(record, identity_sha256, error)``. The identity hash is the SHA-256 of the exact
    canonical bytes the file holds (or would hold), so it is identical whichever copy survives.
    """
    events, ledger_problem = _ledger_events(paths, event)
    distinct = {canonical_json(e) for e in events}

    file_record: Mapping[str, Any] | None = None
    if path.exists():
        file_record, problem = _load_authorization(path)
        if file_record is None:
            return None, "", f"{event.lower()} record unreadable: {problem}"

    if ledger_problem:
        # A corrupt ledger participates in provenance; it may never be silently ignored.
        return None, "", (
            f"{ledger_problem}; {event.lower()} provenance cannot be established"
        )

    # MINOR 1: canonical V5 says DUPLICATED entries fail closed, so the test is "at most one
    # event", not "one distinct value". Two byte-identical CLAIMED/COMPLETED events are still
    # duplicated provenance history and are refused.
    if len(events) > 1:
        identical = len(distinct) == 1
        shape = "identical duplicate" if identical else "conflicting"
        return None, "", (
            f"the ledger holds {len(events)} {event} events ({shape}); duplicated or conflicting "
            f"{event.lower()} provenance fails closed, and identical duplicates are refused too"
        )

    if file_record is not None and events:
        if len(distinct) != 1:
            return None, "", (
                f"the ledger holds conflicting {event} events; {event.lower()} provenance is "
                "ambiguous and fails closed"
            )
        if canonical_json(file_record) != next(iter(distinct)):
            return None, "", (
                f"the {event.lower()} record and its append-only ledger mirror disagree; the "
                "record has been altered after it was written"
            )
        return file_record, sha256_file(path), ""

    if file_record is not None:
        # Single-record loss: the ledger event is gone but the file survives.
        return file_record, sha256_file(path), ""

    if not events:
        return None, "", f"no {event.lower()} record and no ledger {event} entry exists"
    if len(distinct) != 1:
        return None, "", (
            f"the ledger holds conflicting {event} events; exact {event.lower()} identity cannot "
            "be recovered"
        )
    record = events[-1]
    return record, sha256_bytes((canonical_json(record) + "\n").encode("utf-8")), ""


def _recover_claim_record(paths: LanePaths) -> tuple[Mapping[str, Any] | None, str, str]:
    """Recover the canonical claim record and its exact identity hash, mirror-checked."""
    return _recover_mirrored_record(paths, paths.claim, LANE_CLAIMED)


def _recover_completion_record(paths: LanePaths) -> tuple[Mapping[str, Any] | None, str, str]:
    """Recover the canonical completion record and its exact identity hash, mirror-checked."""
    return _recover_mirrored_record(paths, paths.completion, LANE_COMPLETED)


def _authenticated_claim(
    paths: LanePaths, sources: TruthSources | None
) -> tuple[Mapping[str, Any] | None, str, str]:
    """Prove a CLAIMED/COMPLETED lane is LAWFUL, not merely present.

    BLOCKING 1 (review 4946397399): ``lane_state_at`` recognised claim/ledger state BEFORE
    loading the attestation, and this predicate then accepted any syntactically valid 64-hex
    ``authorization_sha256`` -- skipping the hash comparison entirely when the attestation file
    was absent. A local ``claim.json`` with the registered attempt id was therefore enough to
    make the PUBLIC result gate return authorized with no review, acceptance, merge, or CI ever
    consulted. Reproduced before correcting.

    State detection and authorization validity are different questions. The lane may report
    CLAIMED from a surviving record; lawful provenance additionally requires that the exact
    attestation still exists, still hashes to what the claim bound, and STILL passes full
    durable-truth validation -- so post-claim canonical, load-bearing, ancestry, or governance
    drift fails closed rather than being grandfathered in by an old claim.
    """
    record, claim_sha, problem = _recover_claim_record(paths)
    if record is None:
        return None, "", problem
    if record.get("execution_attempt_id") != EXECUTION_ATTEMPT_ID:
        return None, "", (
            f"claim names attempt {record.get('execution_attempt_id')!r}, not "
            f"{EXECUTION_ATTEMPT_ID!r}"
        )
    bound = record.get("authorization_sha256")
    if not _is_sha256(bound):
        return None, "", "claim does not bind an attestation hash"

    # The attestation must STILL exist. A surviving claim never substitutes for it.
    if not paths.authorization.exists():
        return None, "", (
            "the attestation this claim binds no longer exists; a claim record alone never "
            "establishes lawful authorization, so this fails closed"
        )
    actual = sha256_file(paths.authorization)
    if actual != bound:
        return None, "", (
            "the present attestation is not the one this claim bound; the claimed execution "
            "and the current authorization are not the same"
        )

    # ...and it must STILL authenticate against durable truth.
    document, load_problem = _load_authorization(paths.authorization)
    if document is None:
        return None, "", f"attestation unusable: {load_problem}"
    result = validate_authorization_document(document, sources)
    if not result.valid:
        return None, "", (
            "the attestation this claim binds no longer validates against durable truth: "
            + "; ".join(result.errors)
        )
    return record, claim_sha, ""


def claimed_execution_is_authorized(
    paths: LanePaths | None = None, sources: TruthSources | None = None
) -> tuple[bool, str]:
    """Did THIS execution come from the one LAWFUL, still-authenticated claim?

    A different question from "may a new execution start", and conflating them was the earlier
    BLOCKING 2. CLAIMED and COMPLETED both answer yes here -- but only after the attestation
    behind the claim is re-proved, never from claim-file existence alone.
    """
    paths = paths or LanePaths()
    state, _ = lane_state_at(paths, sources)
    if state not in (LANE_CLAIMED, LANE_COMPLETED):
        return False, (
            f"no lawfully claimed Stage-1 execution exists (lane state {state}); a results "
            "document may only be validated when it originates from the one claimed attempt"
        )
    record, _, problem = _authenticated_claim(paths, sources)
    if record is None:
        return False, problem
    return True, ""


def active_execution_is_authorized(
    paths: LanePaths | None = None, sources: TruthSources | None = None
) -> tuple[bool, str]:
    """May THIS execution do real work RIGHT NOW? Exactly ``LANE_CLAIMED``, and lawfully so.

    BLOCKING 1 (review 4953558775): a THIRD question, narrower than both existing ones.

    * :func:`new_execution_is_authorized` -- may a NEW execution start? ``READY`` only.
    * :func:`claimed_execution_is_authorized` -- did THIS execution come from the one lawful
      claim? ``CLAIMED`` **or** ``COMPLETED``, deliberately, because
      :func:`completed_result_is_authorized` authenticates a result AFTER completion and needs
      exactly that provenance. It is not narrowed here, and must not be.
    * this predicate -- is the one lawful attempt CURRENTLY IN PROGRESS? ``CLAIMED`` alone.

    Exactly three acts may happen only DURING the single attempt, and all three ask this one:

    * outcome composition -- :func:`level1_stage1_runner.run_stage1`;
    * result publication -- :func:`level1_stage1_runner.write_stage1_results`;
    * the one ``CLAIMED`` -> ``COMPLETED`` state transition -- :func:`complete_execution`
      (BLOCKING 1, review 4953842000).

    Authenticating an already-completed result is deliberately NOT on that list: it happens after
    the transition, which is exactly why the broader predicate exists and stays broad.

    Reproduced before correcting, on isolated temporary lane paths: with a valid attestation,
    a real claim, and a real completion, ``lane_state_at`` returned ``COMPLETED`` and said "a
    second execution requires new governance authority", while
    ``claimed_execution_is_authorized`` returned ``(True, "")``. Both production entry points
    gated on that predicate alone, so the terminal state did not terminate either
    outcome-producing capability: real composition could re-enter, and a canonical results
    artifact lost after completion could be recreated by the ordinary writer, with ``O_EXCL``
    no longer protecting a path that no longer exists.

    Recovery after a crash or a lost artifact stays a GOVERNED act. This predicate deliberately
    offers no recovery path: it refuses in ``COMPLETED`` exactly as it refuses in ``READY``, so
    the ordinary writer can never become a recovery bypass.
    """
    paths = paths or LanePaths()
    state, why = lane_state_at(paths, sources)
    if state != LANE_CLAIMED:
        return False, (
            f"the one authorized attempt ({EXECUTION_ATTEMPT_ID}) is not currently in progress "
            f"(lane state {state}); real Stage-1 work may only be performed while the lane is "
            f"exactly {LANE_CLAIMED}. {why or 'A claim must be taken immediately beforehand.'} "
            "Recovering a crashed or lost execution is a governed act requiring new authority, "
            "never an ordinary re-run"
        )
    record, _, problem = _authenticated_claim(paths, sources)
    if record is None:
        return False, problem
    return True, ""


def completed_result_is_authorized(
    results: Any, paths: LanePaths | None = None, sources: TruthSources | None = None
) -> tuple[bool, str]:
    """Is THIS EXACT results artifact the one the lawful execution completed?

    BLOCKING 2 (review 4946397399): completion recorded a result hash that nothing ever read,
    and the public validator never computed any identity for the document handed to it, so
    completing result A did not prevent publishing result B. Reproduced before correcting.

    Final publication therefore requires a COMPLETED record whose bound attempt, attestation,
    claim identity, and RESULT identity all match -- the last computed from the supplied
    artifact with :func:`stage1_result_identity`.
    """
    paths = paths or LanePaths()
    authorized, reason = claimed_execution_is_authorized(paths, sources)
    if not authorized:
        return False, reason

    completion, _, completion_problem = _recover_completion_record(paths)
    if completion is None:
        return False, (
            "the lawful execution has not been completed with a consistent, mirror-verified "
            f"record, so no exact result identity is bound and no result may be published "
            f"({completion_problem})"
        )

    claim, claim_sha, claim_problem = _recover_claim_record(paths)
    if claim is None:
        return False, claim_problem
    if completion.get("execution_attempt_id") != EXECUTION_ATTEMPT_ID:
        return False, (
            f"completion names attempt {completion.get('execution_attempt_id')!r}, not "
            f"{EXECUTION_ATTEMPT_ID!r}"
        )
    if completion.get("authorization_sha256") != claim.get("authorization_sha256"):
        return False, "completion binds a different attestation than the claim"
    if completion.get("claim_sha256") != claim_sha:
        return False, "completion binds a different claim than the one on record"

    expected = completion.get("result_identity_sha256")
    if not _is_sha256(expected):
        return False, "completion does not bind an exact result identity"
    supplied = stage1_result_identity(results)
    if supplied != expected:
        return False, (
            f"the supplied results artifact hashes to {supplied}, but the lawful execution "
            f"completed {expected}; a substituted or modified result may not be published"
        )
    return True, ""


def _write_once(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
    except BaseException:  # pragma: no cover - defensive
        try:
            path.unlink()
        except OSError:
            pass
        raise


def claim_execution(
    *,
    claimed_at_utc: str,
    paths: LanePaths | None = None,
    sources: TruthSources | None = None,
) -> Mapping[str, Any]:
    """Atomically claim the single authorized attempt IMMEDIATELY BEFORE the first real work.

    The claim is written with ``O_EXCL`` and mirrored into the append-only ledger, so a
    second claim always fails and losing one record alone does not reopen the lane. This is
    the neutral structural pattern the RISK runner also uses -- authorization is consumed at
    the first eligible work item, before computation -- with no RISK substance reused.
    """
    paths = paths or LanePaths()
    authorized, reason = new_execution_is_authorized(paths, sources)
    if not authorized:
        raise ValueError(f"refusing to claim a non-READY execution lane: {reason}")

    record = {
        "event": LANE_CLAIMED,
        "execution_attempt_id": EXECUTION_ATTEMPT_ID,
        "authorization_sha256": sha256_file(paths.authorization),
        "claimed_at_utc": claimed_at_utc,
    }
    # O_EXCL first: if a concurrent process already claimed, this raises and no ledger entry
    # is written, so the two records cannot disagree about who holds the lane.
    _write_once(paths.claim, canonical_json(record) + "\n")
    _append_ledger(paths.ledger, record)
    return record


def complete_execution(
    *,
    completed_at_utc: str,
    results: Any,
    paths: LanePaths | None = None,
    sources: TruthSources | None = None,
) -> Mapping[str, Any]:
    """Record completion, bound to the exact claim and the SEMANTIC identity of the real result.

    MAJOR 3 (review 4946464366): this previously accepted a caller-supplied
    ``result_identity_sha256``, so completion could bind any 64-hex digest rather than the
    artifact actually produced. It now takes the RESULT ITSELF and computes the identity
    internally with :func:`stage1_result_identity`, so the bound identity is derived, never
    chosen. There is deliberately no public completion API accepting a precomputed digest.

    BLOCKING 1 (review 4953842000): this gated on the deliberately broader
    ``claimed_execution_is_authorized``, true in ``CLAIMED`` **or** ``COMPLETED``, so the terminal
    state was not terminal for the transition API either. Reproduced on isolated lane paths:
    after the single mirror loss the durability contract expressly permits -- ``completion.json``
    gone, the original ``COMPLETED`` ledger event intact, result A still authorized -- an ordinary
    call with result B found the completion path absent, so its ``O_EXCL`` write SUCCEEDED and it
    appended a SECOND ``COMPLETED`` event. ``_recover_mirrored_record`` then rejected the
    duplicated completion, and provenance authorized NEITHER A nor B: a lawful, recoverable result
    had been made unpublishable through the public API alone, with no file forgery.

    A completion is the one ``CLAIMED`` -> ``COMPLETED`` transition, so it asks
    :func:`active_execution_is_authorized` -- exactly ``LANE_CLAIMED``, still authenticated --
    BEFORE computing any result identity and before either write. Repairing a lost mirror is a
    governed act requiring new authority, never a second ordinary completion.
    """
    paths = paths or LanePaths()
    ok, reason = active_execution_is_authorized(paths, sources)
    if not ok:
        raise ValueError(f"refusing to complete an execution that is not actively claimed: {reason}")
    result_identity_sha256 = stage1_result_identity(results)

    # BLOCKING 2: the previous form read the claim from paths.claim only, so completing after a
    # claim-file loss emitted authorization_sha256=None and claim_sha256=None -- directly
    # violating the canonical completion_binds contract. The exact identities are now recovered
    # (from the ledger when necessary) or the completion fails closed.
    claim, claim_sha, problem = _recover_claim_record(paths)
    if claim is None:
        raise ValueError(
            f"refusing to complete without a consistent, mirror-verified claim identity: {problem}"
        )
    bound_attestation = claim.get("authorization_sha256")
    if not _is_sha256(bound_attestation) or not _is_sha256(claim_sha):
        raise ValueError(
            "refusing to complete with a null or malformed attestation/claim identity"
        )
    record = {
        "event": LANE_COMPLETED,
        "execution_attempt_id": EXECUTION_ATTEMPT_ID,
        "authorization_sha256": bound_attestation,
        "claim_sha256": claim_sha,
        "result_identity_sha256": result_identity_sha256,
        "completed_at_utc": completed_at_utc,
    }
    _write_once(paths.completion, canonical_json(record) + "\n")
    _append_ledger(paths.ledger, record)
    return record


# ======================================================================================
# Arming
# ======================================================================================


def build_authorization_payload(
    *,
    authorization_head: str,
    lifecycle_evidence: Mapping[str, Any],
    author_identity: str,
    generated_at_utc: str,
    merge_sha: str,
) -> dict[str, Any]:
    """Assemble an attestation from live repository facts.

    Canonical pins, universe identity, predecessor identity, and load-bearing byte identity
    are all recomputed here rather than accepted from a caller. The lifecycle block is still
    supplied by the operator, but supplying it proves nothing: every field is re-derived and
    compared against durable truth at validation time.
    """
    universe = live_construction_universe_facts()
    git = LiveGitTruthSource()
    load_bearing = {
        relative: (git.blob_sha256_at(merge_sha, relative) or sha256_file(ROOT / relative))
        for relative in sorted(LOAD_BEARING_RELPATHS)
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "mechanism": AUTHORIZATION_MECHANISM,
        "repository": REPOSITORY_IDENTITY,
        "study_id": STUDY_ID,
        "authorizing_decision": AUTHORIZING_DECISION,
        "authorizing_pull_request": AUTHORIZING_PULL_REQUEST,
        "predecessor_decision": PREDECESSOR_DECISION,
        "execution_attempt_id": EXECUTION_ATTEMPT_ID,
        "authorization_head": authorization_head,
        "predecessor_identity": {
            "merge_sha": PREDECESSOR_MERGE_SHA,
            "accepted_head": PREDECESSOR_ACCEPTED_HEAD,
            "merge_base": PREDECESSOR_MERGE_BASE,
        },
        # XASSET-0037. Three distinct relationships, three distinct blocks. Assembled from the
        # module's bound constants and then RE-VERIFIED against git at validation time, so writing
        # them here proves nothing on its own.
        "historical_operational_authorization": {
            "decision": HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION,
            "pull_request": HISTORICAL_OPERATIONAL_AUTHORIZATION_PULL_REQUEST,
            "merge_sha": HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_SHA,
            "accepted_head": HISTORICAL_OPERATIONAL_AUTHORIZATION_ACCEPTED_HEAD,
            "merge_base": HISTORICAL_OPERATIONAL_AUTHORIZATION_MERGE_BASE,
        },
        "package_authorization": {
            "decision": PACKAGE_AUTHORIZING_DECISION,
            "pull_request": PACKAGE_AUTHORIZING_PULL_REQUEST,
            "merge_sha": PACKAGE_AUTHORIZING_MERGE_SHA,
        },
        "executable_package_identity": {
            "pull_request": EXECUTABLE_PACKAGE_PULL_REQUEST,
            "merge_sha": EXECUTABLE_PACKAGE_MERGE_SHA,
            "accepted_head": EXECUTABLE_PACKAGE_ACCEPTED_HEAD,
            "merge_base": EXECUTABLE_PACKAGE_MERGE_BASE,
        },
        # XASSET-0044. Assembled from bound constants and then RE-VERIFIED against git at
        # validation time, so writing them here proves nothing on its own.
        "prior_successor_rebinding": {
            "decision": PRIOR_SUCCESSOR_REBINDING_DECISION,
            "pull_request": PRIOR_SUCCESSOR_REBINDING_PULL_REQUEST,
            "merge_sha": PRIOR_SUCCESSOR_REBINDING_MERGE_SHA,
            "accepted_head": PRIOR_SUCCESSOR_REBINDING_ACCEPTED_HEAD,
            "merge_base": PRIOR_SUCCESSOR_REBINDING_MERGE_BASE,
        },
        "correction_identity": {
            "authorizing_decision": CORRECTION_AUTHORIZING_DECISION,
            "authorizing_pull_request": CORRECTION_AUTHORIZING_PULL_REQUEST,
            "authorizing_merge_sha": CORRECTION_AUTHORIZING_MERGE_SHA,
            "authorizing_accepted_head": CORRECTION_AUTHORIZING_ACCEPTED_HEAD,
            "authorizing_merge_base": CORRECTION_AUTHORIZING_MERGE_BASE,
            "decision": CORRECTED_MODULE_DECISION,
            "pull_request": CORRECTED_MODULE_PULL_REQUEST,
            "merge_sha": CORRECTED_MODULE_MERGE_SHA,
            "accepted_head": CORRECTED_MODULE_ACCEPTED_HEAD,
            "merge_base": CORRECTED_MODULE_MERGE_BASE,
        },
        "rebinding_authorization_identity": {
            "decision": REBINDING_AUTHORIZING_DECISION,
            "pull_request": REBINDING_AUTHORIZING_PULL_REQUEST,
            "merge_sha": REBINDING_AUTHORIZING_MERGE_SHA,
            "accepted_head": REBINDING_AUTHORIZING_ACCEPTED_HEAD,
            "merge_base": REBINDING_AUTHORIZING_MERGE_BASE,
        },
        "recovery_authorization_identity": {
            "decision": RECOVERY_AUTHORIZING_DECISION,
            "pull_request": RECOVERY_AUTHORIZING_PULL_REQUEST,
            "merge_sha": RECOVERY_AUTHORIZING_MERGE_SHA,
            "accepted_head": RECOVERY_AUTHORIZING_ACCEPTED_HEAD,
            "merge_base": RECOVERY_AUTHORIZING_MERGE_BASE,
        },
        "stopped_lifecycle_identity": {
            "stopped_rebinding_decision": STOPPED_REBINDING_DECISION,
            "stopped_rebinding_pull_request": STOPPED_REBINDING_PULL_REQUEST,
            "stopped_rebinding_merge_sha": STOPPED_REBINDING_MERGE_SHA,
            "stopped_rebinding_accepted_head": STOPPED_REBINDING_ACCEPTED_HEAD,
            "stopped_rebinding_merge_base": STOPPED_REBINDING_MERGE_BASE,
            "stopped_rebinding_failed_ci_run": STOPPED_REBINDING_FAILED_CI_RUN,
            "stopped_rebinding_failed_ci_job": STOPPED_REBINDING_FAILED_CI_JOB,
            "stopped_recovery_authorization_decision": (
                STOPPED_RECOVERY_AUTHORIZATION_DECISION
            ),
            "stopped_recovery_authorization_pull_request": (
                STOPPED_RECOVERY_AUTHORIZATION_PULL_REQUEST
            ),
            "stopped_recovery_authorization_merge_sha": (
                STOPPED_RECOVERY_AUTHORIZATION_MERGE_SHA
            ),
            "stopped_recovery_authorization_accepted_head": (
                STOPPED_RECOVERY_AUTHORIZATION_ACCEPTED_HEAD
            ),
            "stopped_recovery_authorization_merge_base": (
                STOPPED_RECOVERY_AUTHORIZATION_MERGE_BASE
            ),
            "stopped_recovery_authorization_failed_ci_run": (
                STOPPED_RECOVERY_AUTHORIZATION_FAILED_CI_RUN
            ),
            "stopped_recovery_authorization_failed_ci_job": (
                STOPPED_RECOVERY_AUTHORIZATION_FAILED_CI_JOB
            ),
            "neither_is_effective": True,
            "neither_may_be_cited_as_authority": True,
            "neither_failed_run_may_be_represented_as_successful": True,
        },
        # XASSET-0049. Assembled from bound constants and then RE-VERIFIED against git at
        # validation time, so writing them here proves nothing on its own.
        "step8_equivalent_authorization_identity": {
            "decision": STEP8_EQUIVALENT_AUTHORIZING_DECISION,
            "pull_request": STEP8_EQUIVALENT_AUTHORIZING_PULL_REQUEST,
            "merge_sha": STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA,
            "accepted_head": STEP8_EQUIVALENT_AUTHORIZING_ACCEPTED_HEAD,
            "merge_base": STEP8_EQUIVALENT_AUTHORIZING_MERGE_BASE,
        },
        "prior_reconciliation_identity": {
            "decision": PRIOR_RECONCILIATION_DECISION,
            "pull_request": PRIOR_RECONCILIATION_PULL_REQUEST,
            "merge_sha": PRIOR_RECONCILIATION_MERGE_SHA,
            "accepted_head": PRIOR_RECONCILIATION_ACCEPTED_HEAD,
            "merge_base": PRIOR_RECONCILIATION_MERGE_BASE,
        },
        "canonical_pins": live_canonical_hashes(),
        "construction_universe": {
            "sha256": universe["sha256"],
            "count": universe["count"],
            "cell_count": universe["cell_count"],
        },
        "lifecycle_evidence": dict(lifecycle_evidence),
        "load_bearing_identity": load_bearing,
        "author_identity": author_identity,
        "generated_at_utc": generated_at_utc,
    }


def write_authorization(
    payload: Mapping[str, Any],
    authorization_path: Path = AUTHORIZATION_PATH,
    sources: TruthSources | None = None,
) -> None:
    """Validate against durable truth, then persist once. Invalid bytes never reach disk."""
    result = validate_authorization_document(payload, sources)
    if not result.valid:
        raise ValueError(
            "refusing to write an invalid Stage-1 authorization attestation: "
            + "; ".join(result.errors)
        )
    _write_once(authorization_path, canonical_json(payload) + "\n")


def main(argv: Sequence[str] | None = None) -> int:  # pragma: no cover - CLI
    state, reason = lane_state_at(LanePaths())
    print(f"study: {STUDY_ID}")
    print(f"attempt: {EXECUTION_ATTEMPT_ID}")
    print(f"mechanism: {AUTHORIZATION_MECHANISM}")
    print(f"effective structural authorization: {AUTHORIZING_DECISION} (PR #{AUTHORIZING_PULL_REQUEST})")
    print(
        f"historical operational authorization: "
        f"{HISTORICAL_OPERATIONAL_AUTHORIZATION_DECISION} "
        f"(PR #{HISTORICAL_OPERATIONAL_AUTHORIZATION_PULL_REQUEST})"
    )
    print(
        f"package authority: {PACKAGE_AUTHORIZING_DECISION} "
        f"(PR #{PACKAGE_AUTHORIZING_PULL_REQUEST})"
    )
    print(f"executable package bound: PR #{EXECUTABLE_PACKAGE_PULL_REQUEST} "
          f"@ {EXECUTABLE_PACKAGE_MERGE_SHA}")
    print(
        f"recovery authority: {RECOVERY_AUTHORIZING_DECISION} "
        f"(PR #{RECOVERY_AUTHORIZING_PULL_REQUEST}) @ {RECOVERY_AUTHORIZING_MERGE_SHA}"
    )
    for decision, pull, run, job, merge in (
        (
            STOPPED_REBINDING_DECISION,
            STOPPED_REBINDING_PULL_REQUEST,
            STOPPED_REBINDING_FAILED_CI_RUN,
            STOPPED_REBINDING_FAILED_CI_JOB,
            STOPPED_REBINDING_MERGE_SHA,
        ),
        (
            STOPPED_RECOVERY_AUTHORIZATION_DECISION,
            STOPPED_RECOVERY_AUTHORIZATION_PULL_REQUEST,
            STOPPED_RECOVERY_AUTHORIZATION_FAILED_CI_RUN,
            STOPPED_RECOVERY_AUTHORIZATION_FAILED_CI_JOB,
            STOPPED_RECOVERY_AUTHORIZATION_MERGE_SHA,
        ),
    ):
        print(
            f"STOPPED, not effective, never authority: {decision} (PR #{pull}) "
            f"@ {merge} -- merge-commit CI run {run} / job {job} FAILED"
        )
    print(f"load-bearing paths: {len(LOAD_BEARING_RELPATHS)}")
    print(f"lane state: {state}")
    print(f"new execution authorized: {state == LANE_READY}")
    if reason:
        print(f"reason: {reason}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(main())
