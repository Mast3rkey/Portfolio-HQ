"""Adversarial tests for the ENDPOINT-0001 Stage-1 operational authorization mechanism (XASSET-0029).

Every test here attacks the gate. The mechanism is only worth having if a forged, stale, drifted,
replayed, self-authored, or misdirected attestation is refused, so each scenario constructs the
attack and asserts refusal rather than asserting the happy path.

NO STAGE-1 EXECUTION OCCURS IN THIS FILE. No gate is evaluated, no construction is dispositioned,
no results document is produced, and no data is acquired. Fixtures are synthetic and are written to
pytest ``tmp_path``, never to the real authorization location.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

import level1_construction_universe_closure_validator as CU
import level1_endpoint_evidence_preregistration_validator as PREREG
import level1_stage1_execution_authorization as AUTH

REPO_ROOT = Path(__file__).resolve().parent

XASSET_0029_HEAD = "1111111111111111111111111111111111111111"
XASSET_0029_MERGE = "2222222222222222222222222222222222222222"
XASSET_0029_BASE = "3333333333333333333333333333333333333333"


def _lifecycle_evidence(head: str = XASSET_0029_HEAD, merge: str = XASSET_0029_MERGE) -> dict:
    """A structurally complete, internally consistent evidence block. Values are synthetic."""
    return {
        "gates_closed": list(AUTH.REQUIRED_LIFECYCLE_GATES),
        "independent_review": {
            "review_id": "9999999999",
            "formal_disposition": AUTH.APPROVING_REVIEW_DISPOSITION,
            "blocking_count": 0,
            "major_count": 0,
            "reviewed_sha": head,
            "reviewer_identity": "SYNTHETIC_INDEPENDENT_REVIEWER",
        },
        "principal_acceptance": {"comment_id": "8888888888", "accepted_head": head},
        "merge": {"merge_sha": merge, "parents": [XASSET_0029_BASE, head]},
        "post_merge_verification": {
            "comment_id": "7777777777",
            "verified_merge_sha": merge,
        },
        "merge_commit_ci": {
            "run_id": "6666666666",
            "job_id": "5555555555",
            "status": "completed",
            "conclusion": "success",
            "head_sha": merge,
        },
    }


@pytest.fixture
def payload() -> dict:
    return AUTH.build_authorization_payload(
        authorization_head=XASSET_0029_HEAD,
        lifecycle_evidence=_lifecycle_evidence(),
        author_identity="SYNTHETIC_AUTHOR",
        generated_at_utc="2026-08-16T00:00:00Z",
    )


def _assert_rejected(doc, fragment: str) -> None:
    result = AUTH.validate_authorization_document(doc)
    assert not result.valid, f"expected refusal for {fragment!r}"
    assert any(fragment in error for error in result.errors), (
        f"expected an error containing {fragment!r}, got {result.errors}"
    )


def _install(tmp_path: Path, doc) -> tuple[Path, Path]:
    path = tmp_path / "authorization.json"
    path.write_text(AUTH.canonical_json(doc) + "\n", encoding="utf-8")
    return path, tmp_path / "consumed.json"


# =============================================================================================
# 1-2 — the merged state is not executable, and the universe is still readable at 680
# =============================================================================================


class TestCurrentStateIsNotExecutable:
    def test_01_current_merged_state_is_not_operationally_authorized(self):
        authorized, reason = AUTH.authorization_is_effective()
        assert authorized is False
        assert "no Stage-1 preexecution authorization attestation exists" in reason

    def test_01b_preregistration_gate_agrees_stage_1_is_not_authorized(self):
        authorized, reason = PREREG.stage_1_operational_authorization_is_effective()
        assert authorized is False
        assert "XASSET-0029" in reason and "attestation" in reason

    def test_01c_public_results_validation_refuses_before_any_structural_check(self):
        result = PREREG.validate_stage1_results({"candidate_results": []})
        assert not result.ok
        assert any("not operationally authorized" in error for error in result.errors)

    def test_02_structural_universe_remains_readable_at_exactly_680(self):
        universe = CU.frozen_construction_universe()
        assert len(universe) == 680
        assert CU.derived_cardinality() == 680
        assert len(CU.per_cell_cardinality()) == 48
        assert CU.universe_aggregate_sha256() == AUTH.CONSTRUCTION_UNIVERSE_SHA256


# =============================================================================================
# 3-7 — bound identity: hashes, repository, study
# =============================================================================================


class TestBoundIdentity:
    def test_03_wrong_universe_hash_rejected(self, payload):
        payload["construction_universe"]["sha256"] = "0" * 64
        _assert_rejected(payload, "construction_universe.sha256")

    def test_03b_wrong_construction_count_rejected(self, payload):
        payload["construction_universe"]["count"] = 679
        _assert_rejected(payload, "construction_universe.count")

    def test_03c_wrong_cell_count_rejected(self, payload):
        payload["construction_universe"]["cell_count"] = 47
        _assert_rejected(payload, "construction_universe.cell_count")

    def test_04_wrong_canonical_protocol_hash_rejected(self, payload):
        key = "research/level1_endpoint_evidence/PROTOCOL_V1.md"
        payload["canonical_pins"][key] = "0" * 64
        _assert_rejected(payload, "canonical_pins")

    def test_05_wrong_preregistration_hash_rejected(self, payload):
        key = "research/level1_endpoint_evidence/pre_registration.yaml"
        payload["canonical_pins"][key] = "0" * 64
        _assert_rejected(payload, "canonical_pins")

    def test_05b_unknown_canonical_file_rejected(self, payload):
        payload["canonical_pins"]["research/level1_endpoint_evidence/OTHER.md"] = "0" * 64
        _assert_rejected(payload, "unknown canonical file")

    def test_06_wrong_repository_rejected(self, payload):
        payload["repository"] = "SomeoneElse/Portfolio-HQ"
        _assert_rejected(payload, "authorization.repository")

    def test_07_wrong_study_id_rejected(self, payload):
        payload["study_id"] = "RISK-0001"
        _assert_rejected(payload, "authorization.study_id")

    def test_07b_wrong_authorizing_decision_rejected(self, payload):
        payload["authorizing_decision"] = "XASSET-0028"
        _assert_rejected(payload, "authorization.authorizing_decision")

    def test_07c_bound_pins_match_the_live_canonical_bytes(self):
        assert AUTH.pins_are_placeholders() is False
        assert AUTH.live_canonical_hashes() == AUTH.CANONICAL_PINS


# =============================================================================================
# 8-18 — lifecycle evidence and drift
# =============================================================================================


class TestLifecycleEvidence:
    def test_08_stale_authorization_head_rejected(self, payload):
        payload["authorization_head"] = "4" * 40
        _assert_rejected(payload, "does not equal authorization_head")

    def test_09_missing_independent_review_rejected(self, payload):
        del payload["lifecycle_evidence"]["independent_review"]
        _assert_rejected(payload, "independent_review: required gate evidence is absent")

    def test_10_adverse_review_rejected(self, payload):
        payload["lifecycle_evidence"]["independent_review"]["formal_disposition"] = (
            "CHANGES REQUIRED"
        )
        _assert_rejected(payload, "formal_disposition")

    def test_10b_unresolved_blocking_finding_rejected(self, payload):
        payload["lifecycle_evidence"]["independent_review"]["blocking_count"] = 1
        _assert_rejected(payload, "blocking_count")

    def test_10c_unresolved_major_finding_rejected(self, payload):
        payload["lifecycle_evidence"]["independent_review"]["major_count"] = 2
        _assert_rejected(payload, "major_count")

    def test_11_review_of_the_wrong_commit_rejected(self, payload):
        payload["lifecycle_evidence"]["independent_review"]["reviewed_sha"] = "5" * 40
        _assert_rejected(payload, "independent_review.reviewed_sha")

    def test_12_missing_principal_acceptance_rejected(self, payload):
        del payload["lifecycle_evidence"]["principal_acceptance"]
        _assert_rejected(payload, "principal_acceptance: required gate evidence is absent")

    def test_13_acceptance_for_the_wrong_head_rejected(self, payload):
        payload["lifecycle_evidence"]["principal_acceptance"]["accepted_head"] = "6" * 40
        _assert_rejected(payload, "principal_acceptance.accepted_head")

    def test_14_missing_merge_rejected(self, payload):
        del payload["lifecycle_evidence"]["merge"]
        _assert_rejected(payload, "merge: required gate evidence is absent")

    def test_15_wrong_merge_parents_rejected(self, payload):
        payload["lifecycle_evidence"]["merge"]["parents"] = [XASSET_0029_BASE, "7" * 40]
        _assert_rejected(payload, "merge.parents[1]")

    def test_15b_squash_or_rebase_single_parent_rejected(self, payload):
        payload["lifecycle_evidence"]["merge"]["parents"] = [XASSET_0029_BASE]
        _assert_rejected(payload, "expected exactly two parents")

    def test_16_missing_post_merge_verification_rejected(self, payload):
        del payload["lifecycle_evidence"]["post_merge_verification"]
        _assert_rejected(payload, "post_merge_verification: required gate evidence is absent")

    def test_16b_merge_alone_does_not_authorize(self, payload):
        payload["lifecycle_evidence"]["post_merge_verification"]["comment_id"] = ""
        _assert_rejected(payload, "merge alone")

    def test_17_missing_merge_commit_ci_rejected(self, payload):
        del payload["lifecycle_evidence"]["merge_commit_ci"]
        _assert_rejected(payload, "merge_commit_ci: required gate evidence is absent")

    @pytest.mark.parametrize("conclusion", ["failure", "cancelled", "timed_out", None])
    def test_17b_unsuccessful_merge_commit_ci_rejected(self, payload, conclusion):
        payload["lifecycle_evidence"]["merge_commit_ci"]["conclusion"] = conclusion
        _assert_rejected(payload, "merge_commit_ci.conclusion")

    def test_17c_still_running_merge_commit_ci_rejected(self, payload):
        payload["lifecycle_evidence"]["merge_commit_ci"]["status"] = "in_progress"
        _assert_rejected(payload, "merge_commit_ci.status")

    def test_17d_ci_for_another_commit_rejected(self, payload):
        payload["lifecycle_evidence"]["merge_commit_ci"]["head_sha"] = "8" * 40
        _assert_rejected(payload, "merge_commit_ci.head_sha")

    def test_18_post_acceptance_drift_rejected(self, payload):
        """The merge no longer carries the accepted head: the merged bytes are not the accepted ones."""
        payload["lifecycle_evidence"]["merge"]["parents"] = [XASSET_0029_BASE, "9" * 40]
        payload["lifecycle_evidence"]["post_merge_verification"]["verified_merge_sha"] = "9" * 40
        result = AUTH.validate_authorization_document(payload)
        assert not result.valid

    def test_18b_dropping_a_declared_gate_rejected(self, payload):
        payload["lifecycle_evidence"]["gates_closed"] = ["MERGE"]
        _assert_rejected(payload, "gates_closed: must include")

    def test_18c_self_authored_review_rejected(self, payload):
        payload["lifecycle_evidence"]["independent_review"]["reviewer_identity"] = payload[
            "author_identity"
        ]
        _assert_rejected(payload, "is the authoring session")


# =============================================================================================
# 19-23 — self-authorization, bypass, malformation, replay, attempt identity
# =============================================================================================


class TestNoSelfAuthorization:
    def test_19_results_document_cannot_self_authorize(self):
        """A results document carrying its own authorization claim is refused."""
        forged = {
            "candidate_results": [],
            "stage_1_executability": {"executable": True},
            "authorization": {"authorized": True},
            "operationally_authorized": True,
        }
        result = PREREG.validate_stage1_results(forged)
        assert not result.ok
        assert any("not operationally authorized" in error for error in result.errors)

    def test_20_public_validator_accepts_no_universe_or_authorization_parameter(self):
        """There is no call form that supplies a universe or an authorization path."""
        with pytest.raises(TypeError):
            PREREG.validate_stage1_results({"candidate_results": []}, {})  # type: ignore[call-arg]
        with pytest.raises(TypeError):
            AUTH.authorization_is_effective(Path("/nonexistent"))  # type: ignore[call-arg]

    def test_20b_private_structural_seam_confers_no_authorization(self):
        """Calling the private seam validates structure and authorizes nothing."""
        PREREG._validate_stage1_results_against_universe(
            {"candidate_results": []}, CU.frozen_construction_universe()
        )
        assert AUTH.authorization_is_effective()[0] is False
        assert PREREG.stage_1_operational_authorization_is_effective()[0] is False

    def test_21_malformed_attestation_rejected(self, tmp_path):
        path = tmp_path / "authorization.json"
        path.write_text("{ not json", encoding="utf-8")
        effective, reason = AUTH._authorization_is_effective_at(path, tmp_path / "consumed.json")
        assert effective is False
        assert "malformed" in reason

    def test_21b_duplicate_keyed_attestation_rejected(self, tmp_path):
        path = tmp_path / "authorization.json"
        path.write_text('{"study_id": "ENDPOINT-0001", "study_id": "OTHER"}', encoding="utf-8")
        effective, reason = AUTH._authorization_is_effective_at(path, tmp_path / "consumed.json")
        assert effective is False
        assert "duplicate key" in reason

    def test_21c_unknown_key_rejected(self, payload):
        payload["extra_authorization_override"] = True
        _assert_rejected(payload, "the schema is closed")

    def test_21d_non_mapping_rejected(self):
        _assert_rejected(["not", "a", "mapping"], "expected a mapping")

    def test_22_replay_after_consumption_rejected(self, tmp_path, payload):
        path, receipt = _install(tmp_path, payload)
        receipt.write_text("{}", encoding="utf-8")
        effective, reason = AUTH._authorization_is_effective_at(path, receipt)
        assert effective is False
        assert "already been consumed" in reason

    def test_22b_attestation_cannot_be_regenerated(self, tmp_path, payload):
        path = tmp_path / "authorization.json"
        AUTH.write_authorization(payload, path)
        with pytest.raises(FileExistsError):
            AUTH.write_authorization(payload, path)

    def test_22c_invalid_payload_never_reaches_disk(self, tmp_path, payload):
        payload["study_id"] = "WRONG"
        path = tmp_path / "authorization.json"
        with pytest.raises(ValueError):
            AUTH.write_authorization(payload, path)
        assert not path.exists(), "an invalid attestation must not occupy the one-shot slot"

    def test_23_authorization_for_another_attempt_rejected(self, payload):
        payload["execution_attempt_id"] = "ENDPOINT-0001::STAGE_1::ATTEMPT_2"
        _assert_rejected(payload, "authorization.execution_attempt_id")

    def test_23b_consumption_receipt_is_bound_to_the_single_attempt(self, tmp_path, payload):
        path, receipt = _install(tmp_path, payload)
        AUTH.consume_authorization(
            consumed_at_utc="2026-08-16T00:00:00Z",
            authorization_path=path,
            receipt_path=receipt,
        )
        recorded = json.loads(receipt.read_text(encoding="utf-8"))
        assert recorded["execution_attempt_id"] == AUTH.EXECUTION_ATTEMPT_ID
        assert AUTH._authorization_is_effective_at(path, receipt)[0] is False


# =============================================================================================
# 24-27 — nothing was executed, nothing was produced, no RISK reuse
# =============================================================================================


class TestNothingWasExecuted:
    def test_24_stage_1_remains_unauthorized_throughout_this_pr_lifecycle(self):
        assert AUTH.authorization_is_effective()[0] is False
        assert PREREG.stage_1_operational_authorization_is_effective()[0] is False
        assert not AUTH.AUTHORIZATION_PATH.exists()
        assert not AUTH.CONSUMPTION_RECEIPT_PATH.exists()

    def test_25_no_stage_1_result_artifact_exists_anywhere(self):
        assert list(REPO_ROOT.rglob("stage1_results.yaml")) == []
        assert not (REPO_ROOT / "intelligence/level1_application").exists()

    def test_25b_authorization_marker_is_outside_the_repository(self):
        assert not str(AUTH.AUTHORIZATION_PATH).startswith(str(REPO_ROOT))
        assert not str(AUTH.CONSUMPTION_RECEIPT_PATH).startswith(str(REPO_ROOT))

    def test_26_module_performs_no_network_or_data_acquisition(self):
        source = (REPO_ROOT / "level1_stage1_execution_authorization.py").read_text(
            encoding="utf-8"
        )
        for banned in ("requests", "urllib", "http", "socket", "yfinance", "alpaca"):
            assert f"import {banned}" not in source

    def test_27_no_risk_study_substance_is_reused(self):
        """Neutral engineering patterns are shared; RISK substance is not."""
        source = (REPO_ROOT / "level1_stage1_execution_authorization.py").read_text(
            encoding="utf-8"
        )
        assert "phq-risk0001-results" not in source
        assert "import risk_level1" not in source
        assert "RISK_0001_ATTEMPT" not in source
        # The RISK results location is never referenced by the authorization path.
        assert "/private/tmp" not in source

    def test_27b_zero_import_coupling_with_allocator_and_margin(self):
        source = (REPO_ROOT / "level1_stage1_execution_authorization.py").read_text(
            encoding="utf-8"
        )
        for banned in ("allocate", "margin_state", "levels"):
            assert f"import {banned}" not in source


# =============================================================================================
# 28-30 — preserved postures
# =============================================================================================


@pytest.fixture
def prereg() -> dict:
    """A fresh parse per test: several tests below mutate it to prove weakening is refused."""
    return yaml.safe_load(
        (REPO_ROOT / "research/level1_endpoint_evidence/pre_registration.yaml").read_text(
            encoding="utf-8"
        )
    )


class TestPreservedPostures:
    def test_28_k1_remains_unresolved(self, prereg):
        blob = yaml.safe_dump(prereg)
        assert "RESOLVED" not in blob.replace("UNRESOLVED", "").replace(
            "RESOLVED_BY_XASSET_0025_OUTCOME_C_OVER_THE_XASSET_0021_FROZEN_SNAPSHOT", ""
        )

    def test_29_j12_remains_deferred(self, prereg):
        assert PREREG.validate(prereg).ok

    def test_30_stage_2_and_application_authority_remain_withheld(self, prereg):
        stage_2 = prereg["stages"]["stage_2"]
        assert stage_2["authorized_by_xasset_0027"] is False
        block = prereg["stage_1_executability"]
        assert block["executable"] is False
        assert block["authorized_by_xasset_0029"] is False

    def test_30b_mechanism_block_never_claims_effectivity(self, prereg):
        mechanism = prereg["stage_1_operational_authorization"]
        assert mechanism["currently_effective"] is False
        assert mechanism["authorization_is_committed_state"] is False
        assert mechanism["authorization_is_external_runtime_evidence"] is True
        assert mechanism["one_shot"] is True
        assert mechanism["no_merge_to_execution_gap"] is True
        assert mechanism["no_infinite_authorization_regress"] is True

    def test_30c_dropping_a_fail_closed_condition_is_rejected(self, prereg):
        prereg["stage_1_operational_authorization"]["must_fail_closed_on"] = ["NO_ATTESTATION_PRESENT"]
        result = PREREG.validate(prereg)
        assert not result.ok
        assert any("must_fail_closed_on" in error for error in result.errors)

    def test_30d_weakening_the_mechanism_is_rejected(self, prereg):
        prereg["stage_1_operational_authorization"]["authorization_is_committed_state"] = True
        result = PREREG.validate(prereg)
        assert not result.ok

    def test_30e_removing_the_mechanism_block_is_rejected(self, prereg):
        del prereg["stage_1_operational_authorization"]
        result = PREREG.validate(prereg)
        assert not result.ok
        assert any("stage_1_operational_authorization" in error for error in result.errors)


# =============================================================================================
# The happy path exists, and it is the ONLY path
# =============================================================================================


class TestCompleteAttestationIsAccepted:
    def test_a_fully_evidenced_attestation_validates(self, payload):
        """Proves the gate is passable in principle -- otherwise the tests above prove nothing."""
        result = AUTH.validate_authorization_document(payload)
        assert result.valid, result.errors

    def test_and_becomes_effective_only_through_the_marker(self, tmp_path, payload):
        path, receipt = _install(tmp_path, payload)
        assert AUTH._authorization_is_effective_at(path, receipt)[0] is True
        # ...while the REAL location is still empty, so nothing is authorized in this repository.
        assert AUTH.authorization_is_effective()[0] is False
