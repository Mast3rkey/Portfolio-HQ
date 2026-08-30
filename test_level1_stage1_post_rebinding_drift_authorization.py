"""Adversarial tests pinning the ``XASSET-0039`` §G.B step-10 drift-fail-closed authorization.

``XASSET-0038``'s complete seven-condition lifecycle closed, the single read-only unit it authorized
then ran, and it returned ``STEP_9_READINESS_VERIFICATION_PASS``. ``XASSET-0030`` §G.B **step 9** is
therefore done. Step 10 is next, and it had **no authority**: ``XASSET-0030`` §G.B authorizes none of
itself and states that steps 4, 5, 8 and 10 describe what a *successor* must do; ``XASSET-0037`` §I
withholds "steps 9, 10, or 11" **by name**; and ``XASSET-0038`` both bars its own unit from
performing or authorizing step 10 and forecloses the nearest inference -- that its fail-closed stop
rule might amount to a grant. ``XASSET-0039`` closes that gap for step 10 and nothing else.

Step 10 is the last gate before the irreversible one. ``ATTEMPT_1`` cannot be re-run after claim, so
the overreaches that matter here are sharper than at any prior link, and each has a dedicated guard:

1. **Step 10 performed now, or treated as authorized on filing.**
   ``TestStep10NotPerformedHere`` and ``TestEffectivityRequiresCompleteLifecycleClosure`` fail if the
   filing runs the comparison, issues a determination, or lets any single lifecycle step stand in for
   complete closure.
2. **The completed step 9 re-performed or reopened.** ``TestStep9PassRecordedNotRePerformed`` fails
   if the filing re-runs C1-C11, re-derives the ten identities, or reopens a step-9 finding -- and
   equally if it stops recording the ``PASS`` at all.
3. **One anchor treated as sufficient.** ``TestBothComparisonAnchorsRequired`` fails if either the
   bound merge or the step-9 evidence stops being required, or if a single-anchor comparison is
   allowed to count as a partial success.
4. **The detector drifting into a remediator.** ``TestNoRepairNoRebinding`` fails if the unit may
   repair, revert, re-pin, rebind, or re-run readiness to clear what it found, or if the three
   separately authorized remedies collapse into fewer.
5. **A clean result read as permission.** ``TestNoDriftAuthorizesNothingFurther`` fails if a no-drift
   determination is made to reach attestation, ``READY``, claim, execution, or step 11.
6. **Step 11 read as included.** ``TestStep11RemainsSeparateAndUnauthorized``.
7. **Arming by implication.** ``TestXasset0029NoRegressIntact`` fails if the filing presents itself as
   an activation PR, adds an activation authorization, or lets merge imply an armed Stage 1.
8. **Silent consumption of the reserved results PR.** ``TestP1ResultsPRRemainsSeparate``.

They also pin the negative space that makes the filing honest: this authorization PR changes no
canonical file, no validator, no authorization module, no runner, no result validator, and no
load-bearing byte; all ten load-bearing paths, both V7 pins, the frozen universe, and the
construction-universe module identity are untouched; and Stage 1 is still ``UNARMED`` with lane state
``ABSENT`` and ``ATTEMPT_1`` unclaimed.

Nothing here arms, claims, completes, or executes Stage 1. **No gate is evaluated for any
construction.** No results document, lane directory, attestation, claim, completion, or ledger entry
is created or read for authorization purposes. No ``risk_lane_boundary`` protected result path is
read, listed, opened, or referenced.
"""

from __future__ import annotations

import ast
import hashlib
import re
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

D0027 = GOV / "XASSET-0027-level1-endpoint-authority-and-all-four-sleeve-evidence-program-charter.md"
D0029 = GOV / "XASSET-0029-endpoint-0001-stage-1-operational-authorization.md"
D0030 = GOV / "XASSET-0030-endpoint-0001-stage-1-gate-evaluation-method-determination.md"
D0036 = GOV / "XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md"
D0037 = GOV / "XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md"
D0038 = (
    GOV
    / "XASSET-0038-endpoint-0001-stage-1-runner-execution-readiness-verification-authorization.md"
)
D0039 = (
    GOV
    / "XASSET-0039-endpoint-0001-stage-1-post-rebinding-drift-fail-closed-authorization.md"
)

#: The effective PR #337 bound merge -- the exact bytes §G.B step 8 bound, and anchor 1 of §H.
BOUND_MERGE_SHA = "637eaa30302f5a71f84ab1d215ecbd32c01399b5"

#: The PR #338 merge that carried XASSET-0038 onto `main` and made it effective.
XASSET0038_MERGE_SHA = "b0361ce74dea357715b2ec2b4ce36b47c4f3cffc"

#: The completed step-9 evidence -- anchor 2 of §H -- and its formal determination.
STEP9_EVIDENCE_COMMENT = "5336643459"
STEP9_DETERMINATION = "STEP_9_READINESS_VERIFICATION_PASS"

#: XASSET-0038's own lifecycle closure, which made the step-9 unit authorized.
XASSET0038_CLOSURE_COMMENT = "5336559614"

#: The PR #339 merge that carried XASSET-0039 onto `main` and made it effective, and the completed
#: step-10 evidence the single unit it authorized then produced. Added by the XASSET-0040 filing so
#: this suite's own now-merged lifecycle is asserted against merged truth rather than a stale value.
XASSET0039_MERGE_SHA = "6960ce5ddbfa8cff1ef591c58682341c4d4407c7"
#: PR #340's merge -- live `main` as XASSET-0041 was drafted.
#: ADVANCED BY XASSET-0043: PR #341 (`9c8647f9`) and then PR #342 have both merged, so
#: WS-0014's single shared `last_verified_main_sha` advances with them, exactly.
XASSET0043_MAIN_SHA = "5fbfc94d7333e552bd2654261e0c57134a172e31"
#: ADVANCED BY XASSET-0044: PR #343 merged at `0709d2f0`, so the register's shared live
#: "where main is now" field lawfully advanced again. The anchor each decision authorizes
#: against is unchanged; only the shared self-reference moved.
XASSET0044_MAIN_SHA = "0709d2f05ab031ecb6f69c40465ed4a227983aed"
#: ADVANCED BY XASSET-0045: PR #344 merged at `f5dedce1`, so the register's shared live
#: "where main is now" field lawfully advanced again under OPS-0001's Active-GitHub-fields
#: rule. The anchor each decision authorizes against is unchanged; only the shared
#: self-reference moved. The assertion stays EXACT.
XASSET0045_MAIN_SHA = "f5dedce1d1d3116ed8a6845c4447388c85a5414c"
#: ADVANCED BY XASSET-0046: PR #345 merged at `2f8cdebe`, so the register's shared live
#: "where main is now" field lawfully advanced again under OPS-0001's Active-GitHub-fields
#: rule. The anchor each decision authorizes against is unchanged; only the shared
#: self-reference moved. The assertion stays EXACT, and gains a negative pin so the field is
#: bound at BOTH ends rather than only at one.
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
#: WS-0014's shared `active_pr` while THIS rebinding-authorization unit is the live work.
#: Set to the real GitHub number issued when the pull request was opened, verified
#: against live GitHub afterwards, never left as a guess.
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
#: ADVANCED BY XASSET-0053. PR #353 merged at `cc1d1b62...`, so WS-0014's shared live
#: "where main is now" / "which pull request is live" fields lawfully advanced again under
#: OPS-0001's Active-GitHub-fields rule. XASSET-0053 is a DESIGN-ONLY authorization: it changes
#: no module constant, so `REVIEWED_BASE_SHA` stays XASSET-0049's lawful rebinding base and only
#: the register's shared self-reference moved. Each prior generation's value is retained beside
#: the current one as a NEGATIVE pin rather than deleted, so a silent revert to any finished
#: unit's state still fails. The assertion stays EXACT and is bound at BOTH ends.
XASSET0053_MAIN_SHA = "cc1d1b62b8b48c7123b73e05e7ea04af89c89cd6"
#: Committed as an impossible sentinel first (-53), then replaced by the number GitHub actually
#: issued in a fast-forward follow-up commit. Never predicted. Distinct from every prior sentinel.
XASSET0053_ACTIVE_PR = 354
#: ADVANCED BY XASSET-0055. PR #354 merged at `683c3246...`, so WS-0014's shared live
#: "where main is now" / "which pull request is live" fields lawfully advanced again under
#: OPS-0001's Active-GitHub-fields rule. XASSET-0055 is a GOVERNANCE-ONLY authorization: it
#: changes no module constant and touches no production authorization code, so
#: `REVIEWED_BASE_SHA` stays XASSET-0049's lawful rebinding base and only the register's
#: shared self-reference moved. There is deliberately NO XASSET0054 generation: XASSET-0054's
#: pull request #355 was CLOSED UNMERGED after independent DELTA review 5010334966, so it
#: never became `main` state and has no merge SHA to pin. Each prior generation's value is
#: retained beside the current one as a NEGATIVE pin rather than deleted, so a silent revert
#: to any finished unit's state still fails. The assertion stays EXACT and is bound at BOTH
#: ends.
XASSET0055_MAIN_SHA = "683c324629544a84d2cf75ebca37325e3375c479"
#: Committed as an impossible sentinel first (-55), then replaced by the number GitHub actually
#: issued in a fast-forward follow-up commit. Never predicted. Distinct from every prior sentinel.
XASSET0055_ACTIVE_PR = 356

#: RE-ANCHORED BY XASSET-0056, the single replacement parser-correction implementation
#: XASSET-0055 §H authorized. `active_branch`, `active_pr` and `last_verified_main_sha` are
#: WS-0014's SINGLE SHARED live self-reference fields under OPS-0001's Active-GitHub-fields
#: rule, so they lawfully advance to whichever unit is live. The XASSET-0055 generation is
#: RETAINED below as a negative pin rather than deleted, so every field stays bound at BOTH
#: ends and a silent revert to ANY finished unit's state still fails here.
XASSET0056_MAIN_SHA = "29e4969885970d942a5acecc1424fb2e2b080d60"

#: ADVANCED BY XASSET-0057. WS-0014's SINGLE SHARED live self-reference field advances
#: with every generation; XASSET-0056's own value is retained above as a NEGATIVE pin, so
#: a silent revert to that finished unit's state still fails here.
XASSET0057_MAIN_SHA = "583022a5f2106d61f82d270edadd3520d8b0c55d"
#: RETAINED above as a negative pin rather than deleted, so every field stays bound at BOTH
#: ends and a silent revert to ANY finished unit's state still fails here.
#: ADVANCED BY XASSET-0058. WS-0014's SINGLE SHARED live self-reference field advances with
#: every generation; XASSET-0057's own value is retained above as a NEGATIVE pin, so a silent
#: revert to that finished unit's state still fails here.
XASSET0058_MAIN_SHA = "556a43cf91679d3e8ca95703c8d49e672b662b73"
#: ADVANCED BY XASSET-0059 -- the Lifecycle B parser correction XASSET-0058 SS-F authorized.
#: WS-0014's live self-reference fields are SHARED under OPS-0001's Active-GitHub-fields
#: rule, so they name whichever unit is live. The superseded value is retained BESIDE the
#: new one as a NEGATIVE pin -- bound at both ends, so a silent revert to finished work
#: still fails -- and nothing is deleted, skipped or relaxed.
XASSET0059_MAIN_SHA = "34c45900ce23742d04d80cf12471c34aabe9682d"
#: ADVANCED BY XASSET-0060, the post-parser-correction rebinding. This is the register's SHARED
#: live self-reference, so it names the currently-live unit; every prior generation stays a
#: NEGATIVE pin below, so a silent revert to finished work still fails here.
XASSET0060_MAIN_SHA = "301e79334876a4bda6e7b89a6156b34e8d38a605"
#: ADVANCED BY XASSET-0061. The shared live field moved onto the successor; the prior
#: generation's value joins the NEGATIVE PINS rather than being deleted, so the field
#: stays bound at BOTH ends and a silent revert to finished work still fails.
XASSET0061_MAIN_SHA = "413e033ac33741829168762ab24d73327c047d4b"
#: ADVANCED BY XASSET-0062, the PR #362 lifecycle provenance correction. WS-0014's
#: `last_verified_main_sha` is a SINGLE SHARED live field naming whichever unit is live,
#: not any one filing's own. PR #362 merged at the value below, so the field lawfully
#: advances. The predecessor value is retained immediately above as a NEGATIVE pin, so the
#: field stays bound at BOTH ends and a silent revert still fails here.
XASSET0062_MAIN_SHA = "3db918530b10ffc1423ba0b749b086e349a4901d"
#: Read back from the live pull request AFTER GitHub issued it, never predicted. The
#: branch's first commit carried the impossible sentinel -56 (negative, so structurally
#: cannot be a real pull-request number); this value replaced it in a fast-forward
#: follow-up commit, with no amend and no force-push.
XASSET0056_ACTIVE_PR = 357
XASSET0057_ACTIVE_PR = 358
#: ADVANCED BY XASSET-0058. WS-0014's single shared `active_pr`. It carries the IMPOSSIBLE
#: SENTINEL -58 (negative, so structurally cannot be a real pull-request number) until GitHub
#: issued this filing's number. GitHub issued 359, and it replaced the sentinel in a
#: fast-forward follow-up commit -- read back from the live API, never predicted, with no
#: amend and no force-push.
XASSET0058_ACTIVE_PR = 359
#: ADVANCED BY XASSET-0059 -- the Lifecycle B parser correction XASSET-0058 SS-F authorized.
#: WS-0014's live self-reference fields are SHARED under OPS-0001's Active-GitHub-fields
#: rule, so they name whichever unit is live. Every superseded value is retained BESIDE the
#: new one as a NEGATIVE pin, so the field stays bound at BOTH ends and a silent revert to
#: finished work still fails. The active_pr carries the IMPOSSIBLE SENTINEL until GitHub
#: issues this unit's real number, which is bound in one fast-forward follow-up commit.
XASSET0059_ACTIVE_PR = 360
#: ADVANCED BY XASSET-0060: WS-0014's SHARED live active_pr names the currently-live unit, and
#: XASSET-0059's own number is retained below as a NEGATIVE pin rather than deleted.
XASSET0060_ACTIVE_PR = 361
XASSET0061_ACTIVE_PR = 362
#: ADVANCED BY XASSET-0062. `active_pr` is WS-0014's SINGLE SHARED live field, naming
#: whichever unit is live: `None` before GitHub issues the successor's number and exactly
#: that number afterwards. It is BOUND, never predicted -- set from GitHub's own response.
#: XASSET-0061's own number is retained below as a NEGATIVE pin.
XASSET0062_ACTIVE_PR: int | None = None

XASSET0043_ACTIVE_PR = 343
#: ADVANCED BY XASSET-0044. WS-0014's single shared `active_pr`, set from the real number
#: GitHub issued and verified against the live pull request after opening, never guessed.
XASSET0044_ACTIVE_PR = 344
#: ADVANCED BY XASSET-0045. WS-0014's single shared `active_pr`, set from the real number
#: GitHub issued and verified against the live pull request after opening, never guessed.
XASSET0045_ACTIVE_PR = 345
#: ADVANCED BY XASSET-0046. WS-0014's single shared `active_pr`, set from the real number
#: GitHub issued for this reauthorization unit and verified against the live pull request
#: after opening, never guessed.
XASSET0046_ACTIVE_PR = 346
#: ADVANCED BY XASSET-0047. WS-0014's single shared `active_pr`, set from the real number
#: GitHub issued for this recovery unit -- never guessed: the branch's first commit carried
#: the impossible sentinel 0, the draft was opened, and the issued number was read back from
#: live GitHub before being bound here.
XASSET0047_ACTIVE_PR = 347
#: ADVANCED BY XASSET-0048. WS-0014's single shared `active_pr`, carrying the impossible
#: sentinel ``None`` until GitHub issues this unit's number, which is then read back from
#: live GitHub and bound -- never guessed.
XASSET0048_ACTIVE_PR = 348
STEP10_EVIDENCE_COMMENT = "5341448714"
STEP10_DETERMINATION = "STEP_10_NO_DRIFT"

#: The values accepted authority already fixes as exact constants, and the only ones XASSET-0039
#: restates. Everything else in its comparison derives from the bound merge tree and the step-9
#: evidence at verification time.
PROTOCOL_SHA256 = "367583b616e1c6ab614bcf67d451fe27ce40507d073374190c57291e761d8971"
PREREG_SHA256 = "768b013c0129f02577fea3c2a1a3100b4340b9a42f48ee0d0dbd6e671894bce1"

#: ADDED BY XASSET-0044. The two constants above are what XASSET-0039's own ACCEPTED,
#: MERGED decision text restates, and that text is history: it is not edited, so they are
#: not either. XASSET-0044's post-correction rebinding lawfully amended the canonical
#: authorization language in lockstep (V7 -> V8) under XASSET-0030 SS-D, so the pins that
#: describe the LIVE files are these. The two roles were conflated in a single pair of
#: constants until the amendment forced them apart; keeping both is what lets the
#: decision-text checks and the live-byte checks each stay at full strength.
CURRENT_PROTOCOL_SHA256 = "1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84"
CURRENT_PREREG_SHA256 = "898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f"
FROZEN_UNIVERSE_SHA256 = "73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224"
CONSTRUCTION_UNIVERSE_MODULE_SHA256 = (
    "1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5"
)

#: The ten paths XASSET-0037 bound. XASSET-0039 must change none of them.
#: EXTENDED BY XASSET-0044, 10 -> 14. The four additions are the decision files that jointly make
#: the corrected bytes lawful, bound by DIRECT MEMBERSHIP so none can be edited after an
#: attestation authenticates. Nothing is removed: the original ten are all still here, and the
#: sorted comparison below is unchanged in kind and still exact.
EXPECTED_LOAD_BEARING = tuple(sorted((
    "governance/decisions/XASSET-0029-endpoint-0001-stage-1-operational-authorization.md",
    "governance/decisions/XASSET-0036-endpoint-0001-stage-1-gb-executable-package-authorization.md",
    "governance/decisions/XASSET-0037-endpoint-0001-stage-1-successor-operational-rebinding.md",
    "level1_construction_universe_closure_validator.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_stage1_execution_authorization.py",
    "level1_stage1_result_validator.py",
    "level1_stage1_runner.py",
    "research/level1_endpoint_evidence/PROTOCOL_V1.md",
    "research/level1_endpoint_evidence/pre_registration.yaml",
    "governance/decisions/"
    "XASSET-0041-endpoint-0001-pr337-lifecycle-actor-evidence-correction-authorization.md",
    "governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md",
    "governance/decisions/"
    "XASSET-0043-endpoint-0001-stage-1-post-correction-rebinding-authorization.md",
    "governance/decisions/"
    "XASSET-0044-endpoint-0001-stage-1-post-correction-operational-rebinding.md",
    # EXTENDED AGAIN BY XASSET-0047, 14 -> 16, under XASSET-0046 SS-G.6. The two additions are the
    # authority for the post-merge-CI recovery and the recovery's own decision, bound by DIRECT
    # MEMBERSHIP on the footing XASSET-0043 and XASSET-0044 already occupy. Nothing is removed:
    # the original ten and XASSET-0044's own four are all still here, and the sorted comparison
    # below is unchanged in kind and still EXACT.
    "governance/decisions/"
    "XASSET-0046-endpoint-0001-stage-1-post-merge-ci-recovery-reauthorization.md",
    "governance/decisions/"
    "XASSET-0047-endpoint-0001-stage-1-post-merge-ci-recovery-reconciliation.md",
    # EXTENDED AGAIN BY XASSET-0049 / XASSET-0048 SS-E, 16 -> 18: the step-8-EQUIVALENT successor
    # rebinding's own authority and the rebinding itself, both by DIRECT MEMBERSHIP. Nothing was
    # removed and no existing member changed, so the sorted EXACT comparison still catches a
    # removal, a swap, or a trade.
    "governance/decisions/"
    "XASSET-0048-endpoint-0001-stage-1-step-8-equivalent-rebinding-authorization.md",
    "governance/decisions/"
    "XASSET-0049-endpoint-0001-stage-1-step-8-equivalent-successor-operational-rebinding.md",
    # EXTENDED AGAIN BY XASSET-0060, 18 -> 25, under XASSET-0057 SS-F.7. The seven additions are
    # the six decisions that authorized and defined the formal-disposition parser -- XASSET-0053,
    # XASSET-0055, XASSET-0056, XASSET-0057, XASSET-0058, XASSET-0059 -- plus the rebinding's own
    # decision, all by DIRECT MEMBERSHIP on the footing every predecessor already occupies. SS-F.7
    # is BROADER than the SS-E principle the earlier extensions applied: it reaches every decision
    # that makes the newly bound BYTES lawful, because binding the parser-corrected implementation
    # while leaving the decisions that define what the parser must do outside the boundary would
    # protect the code and not the authority over it. Nothing is removed: all eighteen prior paths
    # are still here, and the comparison below is unchanged in kind and still EXACT.
    # XASSET-0054 stays EXCLUDED -- identifier consumed, pull request closed unmerged, no decision
    # file on main -- and XASSET-0045 stays excluded because it authorizes nothing.
    "governance/decisions/"
    "XASSET-0053-endpoint-0001-formal-disposition-parser-contract-correction-authorization.md",
    "governance/decisions/"
    "XASSET-0055-endpoint-0001-formal-disposition-verdict-boundary-governance.md",
    "governance/decisions/XASSET-0056-endpoint-0001-formal-disposition-parser-correction.md",
    "governance/decisions/"
    "XASSET-0057-endpoint-0001-stage-1-post-parser-correction-rebinding-authorization.md",
    "governance/decisions/"
    "XASSET-0058-endpoint-0001-formal-disposition-parser-correction-authorization.md",
    "governance/decisions/XASSET-0059-endpoint-0001-formal-disposition-parser-correction.md",
    "governance/decisions/"
    "XASSET-0060-endpoint-0001-stage-1-post-parser-correction-operational-rebinding.md",
)))

#: The five Python modules inside those ten paths, each independently able to affect the 680
#: outcomes. Step 10's whole subject is drift in the runner / result-production members of this set.
OUTCOME_CAPABLE_MODULES = (
    "level1_construction_universe_closure_validator.py",
    "level1_endpoint_evidence_preregistration_validator.py",
    "level1_stage1_execution_authorization.py",
    "level1_stage1_result_validator.py",
    "level1_stage1_runner.py",
)


def _norm(text: str) -> str:
    """Collapse whitespace and blockquote markers so a phrase match survives hard wrapping.

    These decisions are hard-wrapped at ~100 columns and state operative rules inside Markdown
    blockquotes and tables, so an exact quoted phrase is routinely split across a newline with a
    ``>`` continuation marker landing mid-phrase. Both are normalised away, so each assertion below
    is a genuine requirement that the phrase be *present* rather than a hostage to the wrap column.
    """
    without_quote_markers = re.sub(r"^\s*>\s?", " ", text, flags=re.MULTILINE)
    return re.sub(r"\s+", " ", without_quote_markers)


def _section(text: str, letter: str) -> str:
    """Return one top-level ``### <letter>.`` section body, normalised.

    Anchored at line start with exactly three hashes: a naive ``split("### G.")`` also matches
    inside a ``#### G.1`` sub-heading and would silently return a near-empty fragment, making any
    ``in`` assertion over it vacuous. The length floor makes that failure loud instead.
    """
    match = re.search(
        rf"^### {re.escape(letter)}\..*?(?=^### [A-Z]\.|^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match is not None, f"XASSET-0039 section {letter} not found"
    body = match.group(0)
    assert len(body) > 200, f"section {letter} extracted suspiciously short ({len(body)} chars)"
    return _norm(body)


def _suite_ast_excluding_hygiene() -> ast.Module:
    """This module's AST with ``TestSuiteHygiene`` removed.

    The hygiene class is the guard; it must scan everything *else*. Without this exclusion the
    guards below would trip on their own forbidden-pattern literals -- a self-reference, not a
    genuine finding. Removal is asserted rather than assumed so the exclusion can never silently
    become a no-op that scans nothing.
    """
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    before = len(tree.body)
    tree.body = [
        node
        for node in tree.body
        if not (isinstance(node, ast.ClassDef) and node.name == "TestSuiteHygiene")
    ]
    assert len(tree.body) == before - 1, "TestSuiteHygiene not found; the guard exclusion is stale"
    assert tree.body, "excluding the hygiene class emptied the module; the scan would be vacuous"
    return tree


def _ws0014_gate(gate_id: str) -> dict:
    data = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
    for workstream in data["workstreams"]:
        if workstream.get("id") == "WS-0014":
            for gate in workstream["milestones"]:
                if gate["gate"] == gate_id:
                    return gate
    raise AssertionError(f"WS-0014 gate {gate_id!r} not found")


@pytest.fixture(scope="module")
def decision() -> str:
    return D0039.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def norm(decision: str) -> str:
    return _norm(decision)


# --------------------------------------------------------------------------------------------------
# 1. The authority gap is real, and rests on accepted text rather than convenience
# --------------------------------------------------------------------------------------------------


class TestAuthorityGapIsGroundedInAcceptedText:
    def test_predecessors_actually_withhold_step_10(self) -> None:
        """The gap must be verifiable in the predecessors themselves, not merely asserted."""
        norm_0030 = _norm(D0030.read_text(encoding="utf-8"))
        assert "This decision authorizes none of G.A or G.B" in norm_0030
        assert (
            "Steps 4, 5, 8 and 10 describe what a successor must do; performing any of them here "
            "is prohibited (§H)." in norm_0030
        )
        norm_0037 = _norm(D0037.read_text(encoding="utf-8"))
        assert "`XASSET-0030` §G.B steps 9, 10, or 11" in norm_0037
        assert "each requires its own separate authority" in norm_0037
        norm_0038 = _norm(D0038.read_text(encoding="utf-8"))
        assert "perform or authorize `XASSET-0030` §G.B step 10 or step 11." in norm_0038
        assert "retains its own separate-authority requirement" in norm_0038

    def test_xasset_0038_forecloses_the_nearest_inference(self) -> None:
        """The strongest overreach is that 0038's own stop rule already granted step 10."""
        assert (
            "§H's stop-and-report rule is what the step-9 unit does *for itself*; it is not a "
            "grant of step 10." in _norm(D0038.read_text(encoding="utf-8"))
        )

    @pytest.mark.parametrize(
        ("source", "phrase"),
        [
            (D0030, "This decision authorizes none of G.A or G.B"),
            (
                D0030,
                "Steps 4, 5, 8 and 10 describe what a successor must do; performing any of them "
                "here is prohibited (§H).",
            ),
            (
                D0030,
                "Any post-rebinding drift in runner / result-production bytes must fail closed "
                "before `READY` or claim",
            ),
            (
                D0030,
                "the same fail-closed property §D already records for the current six load-bearing "
                "paths",
            ),
            (
                D0030,
                "Only then may the external one-shot attestation be produced and Stage 1 armed — "
                "arm, claim, and the 680-construction run",
            ),
            (D0037, "`XASSET-0030` §G.B steps 9, 10, or 11"),
            (D0037, "steps 9, 10, and 11 remain unperformed and unauthorized"),
            (D0037, "each requires its own separate authority"),
            (D0038, "perform or authorize `XASSET-0030` §G.B step 10 or step 11."),
            (D0038, "retains its own separate-authority requirement"),
            (
                D0038,
                "§H's stop-and-report rule is what the step-9 unit does *for itself*; it is not a "
                "grant of step 10.",
            ),
            (D0038, "authorizes nothing further"),
            (D0038, "would let one review cover both the check and the response to its failure"),
        ],
    )
    def test_every_quoted_predecessor_phrase_is_verbatim_in_its_source(
        self, source: Path, phrase: str, norm: str
    ) -> None:
        """A paraphrase drifting from source, or a source edit invalidating a citation, must fail.

        Both directions are required: the phrase must be present in the live predecessor AND in
        this decision. Checking only the source would let the decision quietly stop citing it.
        """
        assert phrase in _norm(source.read_text(encoding="utf-8")), f"not verbatim in {source.name}"
        assert phrase in norm, f"XASSET-0039 stopped citing: {phrase[:60]}"

    def test_decision_names_the_four_filings_that_declined_to_grant_step_10(
        self, decision: str
    ) -> None:
        section = _section(decision, "B")
        for predecessor in ("XASSET-0030", "XASSET-0037", "XASSET-0038"):
            assert predecessor in section
        assert "Four filings named step 10 and four declined to grant it" in section

    def test_decision_does_not_claim_step_10_is_self_authorizing(self, norm: str) -> None:
        """The honest ground is the express withholding, not a Class 0 self-authorization claim."""
        assert "the express withholding governs" in norm
        assert (
            "rests on closing it rather than on the weaker claim that step 10 might be "
            "self-authorizing" in norm
        )


# --------------------------------------------------------------------------------------------------
# 2. Step 10 is not performed here
# --------------------------------------------------------------------------------------------------


class TestStep10NotPerformedHere:
    def test_decision_states_it_performs_no_part_of_step_10(self, norm: str) -> None:
        assert "**This filing performs no part of step 10.**" in norm
        assert "performs no part of §G.B step 10 and no part of step 11" in norm

    def test_determination_is_an_authorization_not_a_drift_result(self, norm: str) -> None:
        assert "STEP_10_DRIFT_FAIL_CLOSED_AUTHORIZED" in norm
        assert "It runs no comparison, detects no drift, and issues no step-10 determination." in norm

    def test_decision_issues_no_drift_verdict(self, decision: str) -> None:
        """A drift verdict token in an authorization record would mean step 10 was performed."""
        for forbidden in ("STEP_10_NO_DRIFT", "STEP_10_DRIFT_DETECTED", "STEP_10_PASS"):
            assert forbidden not in decision

    def test_no_step_10_evidence_artifact_was_committed(self) -> None:
        """§M requires external evidence; a committed step-10 result would mean the unit ran."""
        for pattern in ("step10_result*", "*step_10_evidence*", "stage1_results.yaml"):
            assert list(ROOT.rglob(pattern)) == []


# --------------------------------------------------------------------------------------------------
# 3. The completed step-9 PASS is recorded, and not re-performed
# --------------------------------------------------------------------------------------------------


class TestStep9PassRecordedNotRePerformed:
    def test_the_completed_pass_is_recorded_with_its_determination_and_evidence(
        self, norm: str, decision: str
    ) -> None:
        """Scoped to the sections that must carry it, not merely to the document.

        A document-wide check passes while the determination survives anywhere -- including only
        in the preflight table -- so dropping it from §C, whose entire job is to record it, would
        go unnoticed. Mutation M18 demonstrated exactly that, so each operative section is pinned.
        """
        assert STEP9_DETERMINATION in norm
        assert STEP9_EVIDENCE_COMMENT in norm
        assert "conditions **C1–C11 all `PASS`**" in norm
        # §C records it; §H consumes it as anchor 2. Both must name it explicitly.
        assert STEP9_DETERMINATION in _section(decision, "C")
        assert STEP9_EVIDENCE_COMMENT in _section(decision, "C")
        assert STEP9_DETERMINATION in _section(decision, "H")

    def test_the_filing_does_not_re_perform_step_9(self, decision: str) -> None:
        section = _section(decision, "C")
        assert "re-performs no part of it" in section
        assert "does not re-run the C1–C11 checklist" in section
        assert "does not re-derive the ten identities" in section

    def test_step_9_findings_are_not_reopened(self, decision: str) -> None:
        section = _section(decision, "C")
        assert (
            "does not revisit, reopen, extend, reduce, or re-adjudicate any step-9 condition or "
            "finding" in section
        )
        assert "reopen, re-adjudicate, or overturn the completed step-9 `PASS`" in _section(
            decision, "G"
        )

    def test_the_pass_is_an_input_not_the_authority_for_step_10(self, decision: str) -> None:
        """Authority comes from this decision's own lifecycle -- 0038 §K forbids anything else."""
        section = _section(decision, "C")
        assert "it authorizes nothing further" in section
        assert (
            "the authority for step 10 comes from **this decision's own lifecycle** (§N) and from "
            "nowhere else" in section
        )


# --------------------------------------------------------------------------------------------------
# 4. Effectivity -- no single lifecycle step is sufficient
# --------------------------------------------------------------------------------------------------


class TestEffectivityRequiresCompleteLifecycleClosure:
    def test_all_seven_conditions_are_stated(self, decision: str) -> None:
        section = _section(decision, "N")
        for condition in (
            "independent **FULL** exact-head review",
            "bounded correction and exact-head re-review",
            "principal exact-head acceptance",
            "normal merge",
            "immediate post-merge verification",
            "successful merge-commit CI whose `head_sha` is the exact merge SHA",
            "final post-CI verification and lifecycle closure",
        ):
            assert condition in section

    def test_no_single_condition_is_sufficient(self, decision: str) -> None:
        section = _section(decision, "N")
        assert "**None is individually sufficient.**" in section
        assert "Opening this PR authorizes nothing" in section
        assert "a green PR-head CI run does not" in section
        assert "**Only complete closure of all seven does**" in section

    def test_effectivity_matches_the_repositorys_own_lifecycle_gate_count(self) -> None:
        """Six enforced gates plus OPS-0009's exact-head re-review condition."""
        assert len(A.REQUIRED_LIFECYCLE_GATES) == 6

    def test_even_full_closure_yields_only_a_fail_closed_check(self, decision: str) -> None:
        assert (
            "what becomes authorized is a **fail-closed drift check**, never arming and never "
            "execution" in _section(decision, "N")
        )

    def test_register_gate_records_the_completed_lifecycle_without_losing_its_history(self) -> None:
        # This assertion pinned `in_progress` / `pr: null` while PR #339 was open, which was
        # accurate then and is factually false now that PR #339 is merged. It is STRENGTHENED
        # rather than relaxed: the merged values are checked exactly, and the drafting session's
        # own narrative -- including its statement that it performed no part of step 10 -- must
        # still be present byte-for-byte in the same gate.
        gate = _ws0014_gate("xasset0039-step10-drift-fail-closed-authorization")
        assert gate["status"] == "complete"
        assert gate["pr"] == 339
        assert "THIS FILING PERFORMS NO PART OF STEP 10" in gate["description"]
        assert "IT PERFORMS AND AUTHORIZES NO PART OF STEP 11" in gate["description"]

    def test_additive_post_merge_gate_records_the_step_10_determination(self) -> None:
        # The completed lifecycle is recorded by a NEW additive gate, never by rewriting the
        # gate above -- the established convention this repository has followed since
        # xasset0037-post-merge-verification.
        gate = _ws0014_gate("xasset0039-post-merge-verification")
        assert gate["status"] == "complete"
        assert gate["pr"] == 339
        assert XASSET0039_MERGE_SHA in gate["description"]
        assert STEP10_EVIDENCE_COMMENT in gate["description"]
        assert STEP10_DETERMINATION in gate["description"]
        assert "STEP 10 IS THEREFORE COMPLETE" in gate["description"]
        # Step 11 must still be recorded as unauthorized by that lifecycle.
        assert "STEP 11 remains unperformed and unauthorized" in gate["description"]


# --------------------------------------------------------------------------------------------------
# 5. Both comparison anchors are required
# --------------------------------------------------------------------------------------------------


class TestBothComparisonAnchorsRequired:
    def test_anchor_one_is_the_effective_bound_merge(self, decision: str) -> None:
        section = _section(decision, "H")
        assert BOUND_MERGE_SHA in section
        assert "the exact bytes the single `XASSET-0030` §G.B step-8 rebinding actually bound" in section

    def test_anchor_two_is_the_successful_step_9_evidence(self, decision: str) -> None:
        section = _section(decision, "H")
        assert STEP9_EVIDENCE_COMMENT in section
        assert STEP9_DETERMINATION in section

    def test_both_are_required_and_one_alone_is_a_failure(self, decision: str) -> None:
        section = _section(decision, "H")
        assert "must compare against **both** of the following" in section
        assert (
            "a comparison against only one is a failure of the step, not a partial success"
            in section
        )

    def test_the_two_anchors_are_stated_to_be_non_redundant(self, decision: str) -> None:
        """If they were redundant, dropping one later would look harmless. They are not."""
        section = _section(decision, "H")
        assert "The two anchors are not redundant." in section
        assert "catches a change that slipped past step 9" in section
        assert "catches a change made *since* step 9 returned `PASS`" in section

    def test_drift_against_either_anchor_counts(self, decision: str) -> None:
        assert "**Drift against either anchor is drift.**" in _section(decision, "H")

    def test_expected_identity_derives_from_sources_not_from_this_record(
        self, decision: str
    ) -> None:
        section = _section(decision, "F")
        assert (
            "derived from the effective bound merge tree and the step-9 evidence at verification "
            "time" in section
        )
        assert "never from a constant restated in a decision record" in section

    def test_only_the_already_fixed_constants_are_restated(self, decision: str) -> None:
        """Restating a derived hash would replace live derivation with a copied constant."""
        hashes = set(re.findall(r"\b[0-9a-f]{64}\b", decision))
        assert hashes == {
            PROTOCOL_SHA256,
            PREREG_SHA256,
            FROZEN_UNIVERSE_SHA256,
            CONSTRUCTION_UNIVERSE_MODULE_SHA256,
        }


# --------------------------------------------------------------------------------------------------
# 6. Fail-closed
# --------------------------------------------------------------------------------------------------


class TestFailClosed:
    @pytest.mark.parametrize(
        "trigger",
        [
            "drift",
            "missing identity",
            "validation failure",
            "unexpected lane state",
            "state the unit cannot determine with certainty",
        ],
    )
    def test_every_trigger_class_stops_the_unit(self, trigger: str, decision: str) -> None:
        section = _section(decision, "I")
        assert trigger in section
        assert "**stops the step-10 unit**" in section

    def test_the_four_required_responses_are_stated(self, decision: str) -> None:
        section = _section(decision, "I")
        assert "**stop**" in section
        assert "**report** the exact condition" in section
        assert "**change nothing**" in section
        assert "**not** issue a step-10 no-drift determination" in section

    def test_a_stop_also_forbids_ready_and_claim(self, decision: str) -> None:
        """Step 10 exists to gate READY/claim; stopping must block them, not merely the verdict."""
        assert "and **not** permit `READY` or claim" in _section(decision, "I")

    def test_uncertainty_is_failure(self, decision: str) -> None:
        section = _section(decision, "I")
        assert "**Uncertainty is failure.**" in section
        assert "may not resolve an ambiguous state in favour of no-drift" in section
        assert (
            "may not treat an identity it could not derive as though it had matched" in section
        )

    def test_prohibition_is_not_relaxed_by_finding_a_defect(self, decision: str) -> None:
        assert (
            "the prohibition in §G is not relaxed by the discovery of a defect"
            in _section(decision, "I")
        )


# --------------------------------------------------------------------------------------------------
# 7. No repair, no rebinding
# --------------------------------------------------------------------------------------------------


class TestNoRepairNoRebinding:
    def test_the_unit_is_a_detector_and_a_refusal(self, decision: str) -> None:
        assert "**detector and a refusal**, never a remediator" in _section(decision, "J")

    @pytest.mark.parametrize(
        "forbidden",
        [
            "correct, revert, regenerate, or re-pin the drifted byte",
            "rebind the drifted path, or perform any part of a rebinding",
            're-run readiness verification to "clear" what it found',
        ],
    )
    def test_each_repair_route_is_barred(self, forbidden: str, decision: str) -> None:
        assert forbidden in _section(decision, "J")

    def test_three_separately_authorized_remedies_are_required(self, decision: str) -> None:
        section = _section(decision, "J")
        assert "**three separately authorized things**" in section
        assert "a **separately authorized correction**" in section
        assert "a **separately authorized rebinding**" in section
        assert "any **renewed readiness verification**" in section

    def test_the_rebinding_requirement_states_why(self, decision: str) -> None:
        """Corrected bytes are no longer the bound bytes -- the §G.B step-5 trust gap, reopened."""
        assert (
            "corrected bytes are no longer the bytes the single step-8 rebinding bound"
            in _section(decision, "J")
        )

    def test_a_prior_pass_does_not_survive_a_change_to_certified_bytes(
        self, decision: str
    ) -> None:
        assert (
            "a prior step-9 `PASS` does not survive a change to the bytes it certified"
            in _section(decision, "J")
        )

    def test_finding_the_work_is_not_authority_to_do_it(self, decision: str) -> None:
        section = _section(decision, "J")
        assert "None of those three is authorized by this decision" in section
        assert "**Finding the work is not authority to do the work.**" in section

    def test_rebinding_is_barred_in_the_withheld_authority_section_too(
        self, decision: str
    ) -> None:
        """§J alone could be read as advice; §G must bar it as authority."""
        section = _section(decision, "G")
        assert "**rebind anything**" in section
        assert "or perform any part of a successor operational-authorization rebinding" in section


# --------------------------------------------------------------------------------------------------
# 8. A no-drift result authorizes nothing further
# --------------------------------------------------------------------------------------------------


class TestNoDriftAuthorizesNothingFurther:
    def test_the_rule_is_stated_operatively(self, decision: str) -> None:
        assert (
            "**A step-10 no-drift determination, however clean, authorizes nothing further.**"
            in _section(decision, "K")
        )

    @pytest.mark.parametrize(
        "not_permitted",
        [
            "permission to produce an attestation",
            "permission to arm Stage 1, to reach `READY`, or to claim `ATTEMPT_1`",
            "permission to execute the 680-construction run",
            "permission to perform `XASSET-0030` §G.B step 11, or any part of it",
            "a substitute for step 11's own separate authority",
        ],
    )
    def test_each_thing_it_is_not_is_enumerated(self, not_permitted: str, decision: str) -> None:
        assert not_permitted in _section(decision, "K")

    def test_a_clean_result_does_not_weaken_the_no_regress_rule(self, decision: str) -> None:
        section = _section(decision, "K")
        assert "`XASSET-0029` §E is not weakened by a clean step-10 result" in section
        assert "`executable` stays permanently `false`" in section

    def test_the_consequences_repeat_the_rule(self, norm: str) -> None:
        """A boundary stated once in the body and dropped from Consequences invites drift."""
        assert "A step-10 no-drift determination **authorizes nothing further**." in norm


# --------------------------------------------------------------------------------------------------
# 9. Step 11 remains separate and unauthorized
# --------------------------------------------------------------------------------------------------


class TestStep11RemainsSeparateAndUnauthorized:
    def test_step_11_is_quoted_and_withheld(self, decision: str) -> None:
        section = _section(decision, "L")
        assert (
            "Only then may the external one-shot attestation be produced and Stage 1 armed — arm, "
            "claim, and the 680-construction run" in section
        )
        assert (
            "**retains its own separate-authority requirement and is entirely outside this "
            "filing.**" in section
        )

    def test_step_11_is_not_reachable_by_a_clean_result_or_by_merge(self, decision: str) -> None:
        section = _section(decision, "L")
        assert "is not made reachable by a clean step-10 result" in section
        assert "is not made reachable by this decision's own merge" in section

    def test_neither_stop_rule_nor_no_repair_rule_grants_step_11(self, decision: str) -> None:
        assert (
            "neither is a grant of step 11" in _section(decision, "L")
        )

    def test_withheld_authority_bars_performing_or_authorizing_step_11(
        self, decision: str
    ) -> None:
        assert (
            "**perform or authorize `XASSET-0030` §G.B step 11.**" in _section(decision, "G")
        )

    def test_consequences_repeat_that_step_11_is_unauthorized(self, norm: str) -> None:
        assert (
            "**`XASSET-0030` §G.B step 11 remains unperformed and unauthorized**" in norm
        )


# --------------------------------------------------------------------------------------------------
# 10. The absolute bars
# --------------------------------------------------------------------------------------------------


class TestAbsoluteBarsPreserved:
    @pytest.mark.parametrize(
        "barred",
        [
            "produce an attestation",
            "an `AUTHORIZATION_ROOT`",
            "lane state",
            "a `READY` state",
            "a claim",
            "a ledger entry",
            "a completion record",
            "a recovery",
            "an execution",
            "create `stage1_results.yaml`",
            "**evaluate or decide any gate (`G1`–`G12`) for any registered construction**",
            "consume any part of `ATTEMPT_1`",
            "`risk_lane_boundary` protected `RISK` result",
        ],
    )
    def test_every_absolute_bar_is_named_in_withheld_authority(
        self, barred: str, decision: str
    ) -> None:
        assert barred in _section(decision, "G")

    def test_every_mutation_class_is_barred(self, decision: str) -> None:
        section = _section(decision, "G")
        assert (
            "create, edit, regenerate, correct, reformat, repair, or re-pin **any** canonical, "
            "validator, authorization, runner, result-production, universe, governance, or "
            "protected portfolio byte" in section
        )
        assert "extend, reduce, or re-derive `LOAD_BEARING_RELPATHS`, re-pin any canonical hash" in section

    def test_declaring_a_defect_fixed_is_barred(self, decision: str) -> None:
        section = _section(decision, "G")
        assert '**declare any defect "fixed"**' in section
        assert "never work to perform" in section

    def test_read_only_boundary_is_reused_not_widened(self, decision: str) -> None:
        assert "That line is adopted here unchanged." in _norm(decision)
        assert "not widened by one step" in _norm(decision)

    def test_real_680_run_remains_absolutely_prohibited(self, decision: str) -> None:
        assert (
            "**An actual Stage-1 run over the real 680 remains absolutely prohibited**"
            in _norm(decision)
        )

    def test_non_authorization_section_repeats_the_bars(self, decision: str) -> None:
        section = _section(decision, "O")
        for barred in (
            "generates no attestation",
            "performs no part of §G.B step 10 and no part of step 11",
            "re-performs no part of the completed step 9",
            "consumes nothing of `ATTEMPT_1`",
            "creates no `stage1_results.yaml`",
            "modifies no research, intelligence, or protected portfolio path",
        ):
            assert barred in section

    def test_no_production_or_outcome_producing_code_is_created(self, decision: str) -> None:
        assert (
            "creates no production or outcome-producing code" in _norm(decision)
        )


# --------------------------------------------------------------------------------------------------
# 11. XASSET-0029 §E and XASSET-0027 §P.1 remain intact
# --------------------------------------------------------------------------------------------------


class TestXasset0029NoRegressIntact:
    def test_filing_adds_zero_activation_authorizations(self, decision: str) -> None:
        section = _section(decision, "E")
        assert "adds **zero** activation authorizations" in section
        assert "generates no attestation and arms nothing" in section

    def test_merging_does_not_arm_stage_1(self, decision: str) -> None:
        assert (
            "**Merging this decision authorizes a future fail-closed drift check only. It does "
            "not make Stage 1 armed or executable.**" in _section(decision, "E")
        )

    def test_final_activation_stays_the_runtime_operator_act(self, decision: str) -> None:
        assert (
            "Final activation remains the external, authenticated, one-shot runtime attestation "
            "and the operator's act." in _section(decision, "E")
        )

    def test_no_committed_value_authorizes_execution(self, decision: str) -> None:
        assert (
            "**no committed value in this repository authorizing Stage-1 execution**"
            in _section(decision, "E")
        )

    def test_executable_flag_stays_false(self) -> None:
        """Enforced in the canonical file itself, not merely asserted in prose."""
        data = yaml.safe_load(PREREG.read_text(encoding="utf-8"))
        assert data["stage_1_executability"]["executable"] is False


class TestP1ResultsPRRemainsSeparate:
    def test_p1_is_not_consumed(self, decision: str) -> None:
        section = _section(decision, "D")
        assert "remains **one, unspent**" in section
        assert "This filing does not consume it" in section

    def test_the_step_10_unit_also_does_not_consume_it(self, decision: str) -> None:
        assert "and neither does the step-10 unit it authorizes" in _section(decision, "D")
        assert "consume `XASSET-0027` §P.1's reserved results PR" in _section(decision, "G")

    def test_the_three_distinguishing_grounds_are_stated(self, decision: str) -> None:
        section = _section(decision, "D")
        assert "three independent grounds" in section
        assert "may make no production configuration change" in section
        assert "sits on the far side of arming" in section


# --------------------------------------------------------------------------------------------------
# 12. This filing mutates nothing load-bearing, and live state is unchanged
# --------------------------------------------------------------------------------------------------


class TestThisFilingMutatesNothingLoadBearing:
    def test_load_bearing_set_is_exactly_the_ten_xasset_0037_bound(self) -> None:
        assert tuple(sorted(A.LOAD_BEARING_RELPATHS)) == EXPECTED_LOAD_BEARING

    @pytest.mark.parametrize("relative", EXPECTED_LOAD_BEARING)
    def test_each_load_bearing_path_still_exists(self, relative: str) -> None:
        assert (ROOT / relative).is_file()

    @pytest.mark.parametrize("module", OUTCOME_CAPABLE_MODULES)
    def test_each_outcome_capable_module_still_exists(self, module: str) -> None:
        assert (ROOT / module).is_file()

    def test_canonical_bytes_match_the_effective_v7_pins(self) -> None:
        assert hashlib.sha256(PROTOCOL.read_bytes()).hexdigest() == CURRENT_PROTOCOL_SHA256
        assert hashlib.sha256(PREREG.read_bytes()).hexdigest() == CURRENT_PREREG_SHA256

    def test_construction_universe_module_identity_unchanged(self) -> None:
        module = ROOT / "level1_construction_universe_closure_validator.py"
        assert (
            hashlib.sha256(module.read_bytes()).hexdigest()
            == CONSTRUCTION_UNIVERSE_MODULE_SHA256
        )

    def test_frozen_universe_is_unchanged(self) -> None:
        assert CU.universe_aggregate_sha256() == FROZEN_UNIVERSE_SHA256

    def test_frozen_universe_traversal_still_yields_680_and_48(self) -> None:
        """Read-only structural traversal under XASSET-0036 §F.1(a). No gate is evaluated."""
        universe = CU.generate_construction_universe()
        assert len(universe) == 680
        assert len(CU.per_cell_cardinality()) == 48

    def test_lane_state_absent_and_execution_unauthorized(self) -> None:
        paths = A.LanePaths()
        assert not paths.authorization.exists()
        assert not paths.claim.exists()
        assert not paths.completion.exists()
        assert not paths.ledger.exists()
        state, _ = A.lane_state_at(paths)
        assert state == A.LANE_ABSENT
        authorized, _ = A.new_execution_is_authorized()
        assert authorized is False

    def test_attempt_1_is_the_single_lane_and_is_unclaimed(self) -> None:
        assert A.EXECUTION_ATTEMPT_ID == "ENDPOINT-0001::STAGE_1::ATTEMPT_1"
        assert not A.AUTHORIZATION_ROOT.exists()

    def test_no_real_stage1_results_document_exists(self) -> None:
        assert list(ROOT.rglob("stage1_results.yaml")) == []

    def test_decision_declares_it_mutates_nothing_load_bearing(self, norm: str) -> None:
        assert (
            "changes no `LOAD_BEARING_RELPATHS`, no canonical file, and no hash pin" in norm
        )

    def test_decision_declares_stage_1_still_unarmed(self, norm: str) -> None:
        assert "**Stage 1 remains UNARMED and NOT EXECUTABLE." in norm
        assert "`ATTEMPT_1` is intact, unclaimed, and unconsumed.**" in norm


# --------------------------------------------------------------------------------------------------
# 13. Catalog and register synchronisation
# --------------------------------------------------------------------------------------------------


class TestCatalogAndRegisterSynchronisation:
    def test_catalog_entry_is_present_and_points_at_the_real_file(self) -> None:
        # Anchored to XASSET-0039's own identity rather than to the tail position it happened to
        # occupy while PR #339 was open. STRENGTHENED, not relaxed: the entry must exist, carry
        # its own status, point at a real file, and name THIS suite as its supporting artifact.
        entries = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["decisions"]
        entry = next(e for e in entries if e["decision_id"] == "XASSET-0039")
        assert entry["status"] == "Proposed"
        assert (ROOT / entry["file"]).is_file()
        assert entry["supporting_artifact"] == Path(__file__).name

    def test_catalog_entry_relates_to_its_immediate_predecessor(self) -> None:
        entries = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["decisions"]
        entry = next(e for e in entries if e["decision_id"] == "XASSET-0039")
        assert "XASSET-0038" in entry["related_decisions"]

    def test_prior_step9_gate_is_marked_complete_without_losing_its_history(self) -> None:
        gate = _ws0014_gate("xasset0038-step9-readiness-verification-authorization")
        assert gate["status"] == "complete"
        assert gate["pr"] == 338
        # The drafting session's own narrative is retained verbatim, not rewritten.
        assert "THIS FILING PERFORMS NO PART OF STEP 9" in gate["description"]
        assert "eleven conditions C1-C11" in gate["description"]

    def test_post_merge_gate_records_the_verified_identities_and_the_step_9_pass(self) -> None:
        gate = _ws0014_gate("xasset0038-post-merge-verification")
        assert gate["status"] == "complete"
        assert gate["pr"] == 338
        assert XASSET0038_MERGE_SHA in gate["description"]
        assert XASSET0038_CLOSURE_COMMENT in gate["description"]
        assert STEP9_EVIDENCE_COMMENT in gate["description"]
        assert STEP9_DETERMINATION in gate["description"]
        assert "STEP 9 IS THEREFORE COMPLETE" in gate["description"]

    def test_step10_gate_states_the_non_authorization_boundary(self) -> None:
        description = _ws0014_gate("xasset0039-step10-drift-fail-closed-authorization")["description"]
        assert "THIS FILING PERFORMS NO PART OF STEP 10" in description
        assert "IT PERFORMS AND AUTHORIZES NO PART OF STEP 11" in description
        assert "RE-PERFORMS NO PART OF THE COMPLETED STEP 9" in description
        assert "AUTHORIZES NOTHING FURTHER" in description
        assert "NEVER A REMEDIATOR" in description
        assert BOUND_MERGE_SHA in description
        assert STEP9_EVIDENCE_COMMENT in description

    def test_workstream_live_fields_reflect_this_session(self) -> None:
        data = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
        workstream = next(w for w in data["workstreams"] if w.get("id") == "WS-0014")
        # This pinned the PR #338 merge while PR #339 was open. STRENGTHENED to the merged
        # PR #339 value, which is the SHA the successor filing independently re-verified.
        # ADVANCED AGAIN BY XASSET-0041 for the same reason: PR #340 merged at `f212cce5`.
        # ADVANCED BY XASSET-0049: this is the register's SHARED live field, so it names the
        # currently-live unit. Bound at BOTH ends -- every prior generation's value is a negative
        # pin, so a silent revert to finished work still fails here.
        assert workstream["last_verified_main_sha"] == XASSET0062_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0061_MAIN_SHA
        # XASSET-0061 advanced the shared live field; XASSET-0060's value is now a
        # NEGATIVE PIN, so a silent revert to that finished generation still fails.
        assert workstream["last_verified_main_sha"] != XASSET0060_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0059_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0058_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0057_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0056_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0055_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0053_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0052_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0051_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0050_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0049_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0048_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0047_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0046_MAIN_SHA
        assert workstream["last_verified_main_sha"] != XASSET0045_MAIN_SHA
        # ADVANCED BY XASSET-0051, with the shared fields above. Bound at BOTH ends.
        # ADVANCED BY XASSET-0053, with the shared fields above: PR #353 merged and the
        # register's shared live self-reference moved onto this successor unit. Every
        # prior generation is retained as a NEGATIVE pin, so the field stays bound at
        # BOTH ends and a silent revert to finished work still fails.
        # ADVANCED BY XASSET-0059, with the shared fields above: the register's single
        # shared verification date moved to this unit's own live preflight date. Every
        # prior generation stays a NEGATIVE pin, so the field is bound at BOTH ends.
        # ADVANCED BY XASSET-0062, with the shared fields above: the register's single
        # shared verification date moved to this unit's own live preflight date. The
        # predecessor date joins the NEGATIVE pins, so the field stays bound at BOTH ends.
        assert str(workstream["last_verified_date"]).startswith("2026-08-30")
        assert not str(workstream["last_verified_date"]).startswith("2026-08-28")
        assert not str(workstream["last_verified_date"]).startswith("2026-08-26")
        assert not str(workstream["last_verified_date"]).startswith("2026-08-24")
        assert not str(workstream["last_verified_date"]).startswith("2026-08-23")
        assert not str(workstream["last_verified_date"]).startswith("2026-08-22")
        # ADVANCED AGAIN BY XASSET-0042: PR #341 has merged, so WS-0014's single shared
        # `active_pr` now points at THIS correction unit's own pull request. Pinned to a
        # module constant, set from the real number GitHub issued rather than guessed.
        assert workstream["active_pr"] in (None, XASSET0062_ACTIVE_PR)
        assert workstream["active_pr"] != XASSET0061_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0060_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0059_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0058_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0057_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0056_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0055_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0053_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0052_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0051_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0050_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0049_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0048_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0047_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0046_ACTIVE_PR
        assert workstream["active_pr"] != XASSET0045_ACTIVE_PR

    def test_workstream_stays_secondary_and_no_primary_is_introduced(self) -> None:
        data = yaml.safe_load(WORKSTREAMS.read_text(encoding="utf-8"))
        workstream = next(w for w in data["workstreams"] if w.get("id") == "WS-0014")
        assert workstream["priority"] == "secondary"
        primary = [w["id"] for w in data["workstreams"] if w.get("priority") == "primary"]
        assert primary == []


# --------------------------------------------------------------------------------------------------
# 14. Evidence is external, and the unit mutates nothing to record it
# --------------------------------------------------------------------------------------------------


class TestEvidenceIsExternalAndNonMutating:
    """§M was reachable by no assertion in an earlier draft of this suite.

    Its clauses are substantive: they are what keeps the step-10 unit from contending for the
    ``OPS-0014`` §D single mutation lane, and what stops "record the result" from becoming a
    licence to write to the repository. An unpinned section can be weakened later with nothing
    failing, so each operative clause is pinned here.
    """

    def test_unit_creates_no_branch_commit_or_pr(self, decision: str) -> None:
        assert "**no branch, no commit, and no pull request**" in _section(decision, "M")

    def test_unit_makes_no_repository_mutation(self, decision: str) -> None:
        assert "**no repository mutation**" in _section(decision, "M")

    def test_unit_does_not_contend_for_the_single_mutation_lane(self, decision: str) -> None:
        assert (
            "it does not contend for the `OPS-0014` §D single mutation lane"
            in _section(decision, "M")
        )

    def test_evidence_is_durable_and_externally_posted(self, decision: str) -> None:
        section = _section(decision, "M")
        assert "**durable, externally posted evidence**" in section
        assert "the outcome against each of the two §H anchors" in section

    def test_a_mutation_to_record_the_result_is_not_authorized(self, decision: str) -> None:
        """The nearest overreach: "we need a commit to record this" becoming self-granted scope."""
        section = _section(decision, "M")
        assert (
            "**A repository mutation to record the result is neither required nor authorized**"
            in section
        )
        assert "that is a finding to report under §I, not scope to assume" in section


# --------------------------------------------------------------------------------------------------
# Suite hygiene -- guards that make the assertions above non-vacuous
# --------------------------------------------------------------------------------------------------


class TestSuiteHygiene:
    def test_no_assertion_uses_an_or_fallback(self) -> None:
        """An ``assert a or b`` passes when either half is dead, hiding a stale needle."""
        offenders = [
            node.lineno
            for node in ast.walk(_suite_ast_excluding_hygiene())
            if isinstance(node, ast.Assert)
            and isinstance(node.test, ast.BoolOp)
            and isinstance(node.test.op, ast.Or)
        ]
        assert offenders == []

    def test_suite_performs_no_filesystem_write(self) -> None:
        """Detects real write *calls*, not source substrings.

        A substring scan would match this guard's own pattern list -- a self-reference, not a
        finding. Walking the AST for actual mutating calls is also the stronger check, since it
        cannot be evaded by spelling the call differently in prose.
        """
        forbidden_attrs = {
            "write_text",
            "write_bytes",
            "mkdir",
            "unlink",
            "touch",
            "rmtree",
            "remove",
            "makedirs",
            "rename",
            "replace",
            "rmdir",
        }
        offenders = [
            f"{node.func.attr}:{node.lineno}"
            for node in ast.walk(_suite_ast_excluding_hygiene())
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in forbidden_attrs
        ]
        assert offenders == [], f"suite must not mutate the filesystem; found: {offenders}"

    def test_suite_never_references_the_protected_risk_result_path(self) -> None:
        """Scans string *constants*, excluding this guard class's own needle."""
        needle = "phq-risk0001-results"
        offenders = [
            node.value
            for node in ast.walk(_suite_ast_excluding_hygiene())
            if isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and needle in node.value
        ]
        assert offenders == [], f"suite must not reference the protected RISK result path: {offenders}"

    def test_suite_evaluates_no_gate_for_any_construction(self) -> None:
        """The one-shot lane's hardest guard: traversal is permitted, gate evaluation is not."""
        forbidden = {
            "evaluate_gate",
            "evaluate_gates",
            "gate_disposition",
            "derive_disposition",
            "run_stage1",
            "execute_stage1",
            "claim_execution",
            "record_completion",
        }
        offenders = [
            f"{name}:{node.lineno}"
            for node in ast.walk(_suite_ast_excluding_hygiene())
            if isinstance(node, ast.Call)
            for name in (
                [node.func.attr]
                if isinstance(node.func, ast.Attribute)
                else [node.func.id] if isinstance(node.func, ast.Name) else []
            )
            if name in forbidden
        ]
        assert offenders == []

    def test_section_extractor_is_not_vacuous(self, decision: str) -> None:
        """Every section this suite reads must exist and be substantial."""
        for letter in "ABCDEFGHIJKLMNO":
            assert len(_section(decision, letter)) > 200

    def test_section_extractor_rejects_a_missing_section(self, decision: str) -> None:
        with pytest.raises(AssertionError):
            _section(decision, "Z")

    def test_norm_helper_actually_collapses_wraps(self) -> None:
        assert _norm("a\n>  b   c") == "a b c"

    def test_decision_file_declares_this_module_as_its_supporting_artifact(
        self, decision: str
    ) -> None:
        assert f"supporting_artifact: {Path(__file__).name}" in decision

    def test_decision_frontmatter_is_proposed_not_accepted(self, decision: str) -> None:
        """A filing may never mark itself Accepted in its own authoring session."""
        assert "status: Proposed" in decision.split("---")[1]
