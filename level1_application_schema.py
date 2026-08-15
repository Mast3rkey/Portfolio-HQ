"""XASSET-0022 -- Level-1 application artifact schema and canonical serialization.

Purely mechanical. This module defines the exact artifact identity, the one
canonical serialization, the complete closed field set, the closed state
vocabularies, the deterministic-trace contract, and the reopen-trigger
contract for a future Level-1 application artifact.

It defines NO economic rule, evidence conclusion, sleeve allocation, endpoint,
or portfolio policy, and it authorizes NO application. Every economic
consequence remains exactly as XASSET-0020 and XASSET-0021 left it.

Application authority is WITHHELD: `APPLICATION_AUTHORIZATION_REGISTRY` is
empty, so no artifact can validate until a separate governance decision grants
application authority and is recorded here.

Zero import coupling with `allocate.py` / `margin_state.py` in either
direction, and this module never reads current holdings, targets, gates,
weights, margin state, or market data.
"""

from __future__ import annotations

import json
from hashlib import sha256

# ---------------------------------------------------------------------------
# 1. Exact artifact identity (XASSET-0022 §C; XASSET-0021 §L item 1)
# ---------------------------------------------------------------------------

SCHEMA_NAME = "level1_application"
SCHEMA_VERSION = "1.0"
CANONICAL_ARTIFACT_PATH = "intelligence/level1_application/level1_application.json"
FILE_FORMAT = "json"
ENCODING = "utf-8"
NEWLINE = "\n"

SCHEMA_IDENTITY = {
    "schema_name": SCHEMA_NAME,
    "schema_version": SCHEMA_VERSION,
    "canonical_path": CANONICAL_ARTIFACT_PATH,
    "file_format": FILE_FORMAT,
    "encoding": ENCODING,
    "newline": "lf",
}

# ---------------------------------------------------------------------------
# 2. Canonical serialization (XASSET-0021 §L item 2)
#
# Reuses this repository's already-accepted canonical convention -- compact
# separators, sorted keys, UTF-8, non-ASCII preserved -- identical to every
# sibling `canonical_record_hash()` and to the retained RISK result artifacts.
# No second serialization convention is introduced.
#
# Key order is DERIVED (sort_keys=True), never author-chosen. Exactly one
# trailing LF. No BOM. `allow_nan=False` bars NaN/Infinity tokens, which are
# not valid JSON.
# ---------------------------------------------------------------------------


def canonical_text(document: object) -> str:
    """The one lawful canonical text form of an artifact document."""
    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ) + NEWLINE


def canonical_bytes(document: object) -> bytes:
    """The one lawful canonical byte form of an artifact document."""
    return canonical_text(document).encode(ENCODING)


def canonical_sha256(document: object) -> str:
    """SHA-256 over the canonical bytes."""
    return sha256(canonical_bytes(document)).hexdigest()


def contains_float(value: object) -> bool:
    """True if any float appears anywhere in the document tree.

    Floats are barred from canonical bytes entirely: their textual form is
    representation-dependent, and XASSET-0021 §G requires exact arithmetic
    with no rounding that could change an outcome. Any future lawful exact
    numeric value must be an exact-precision string carrying NUM-0001
    provenance, never a binary float.
    """
    if isinstance(value, float):
        return True
    if isinstance(value, dict):
        return any(contains_float(v) for v in value.values())
    if isinstance(value, list):
        return any(contains_float(v) for v in value)
    return False


# ---------------------------------------------------------------------------
# 3. Canonical orders (XASSET-0021 §A, §D; XASSET-0020 §H)
# ---------------------------------------------------------------------------

CANONICAL_SLEEVE_ORDER = (
    "equity",
    "fund_broad_market",
    "fund_gld_defensive",
    "crypto",
)

# Exactly six unordered pairs. Each pair's members are emitted in canonical
# sleeve order, so a reversed pair is not expressible.
CANONICAL_PAIR_ORDER = tuple(
    f"{CANONICAL_SLEEVE_ORDER[i]}__{CANONICAL_SLEEVE_ORDER[j]}"
    for i in range(len(CANONICAL_SLEEVE_ORDER))
    for j in range(i + 1, len(CANONICAL_SLEEVE_ORDER))
)

CANONICAL_PAIR_MEMBERS = {
    f"{CANONICAL_SLEEVE_ORDER[i]}__{CANONICAL_SLEEVE_ORDER[j]}": (
        CANONICAL_SLEEVE_ORDER[i],
        CANONICAL_SLEEVE_ORDER[j],
    )
    for i in range(len(CANONICAL_SLEEVE_ORDER))
    for j in range(i + 1, len(CANONICAL_SLEEVE_ORDER))
}

# All six driver classes apply to every pair. `not_applicable` is deliberately
# absent from DRIVER_DIRECTION: XASSET-0021 §D bars marking a driver class
# inapplicable merely because evidence is missing.
CANONICAL_DRIVER_CLASS_ORDER = (
    "portfolio_function",
    "valuation_opportunity_cost",
    "downside_path_risk",
    "recovery",
    "diversification_cobehavior",
    "sleeve_deployability",
)

# One trace structure, fully populated, in exactly this order, for every sleeve.
CANONICAL_TRACE_STEP_ORDER = (
    "frozen_input_identity_verified",
    "evidence_admission_evaluated",
    "evidence_classification_applied",
    "source_owned_freshness_recorded",
    "driver_ledger_populated",
    "missingness_and_conflict_propagated",
    "representation_sensitivity_evaluated",
    "endpoint_authority_evaluated",
    "constraint_effects_applied",
    "sleeve_outcome_determined",
    "unassigned_capital_reconciled",
)

# Exactly one lawful `output_recorded` per trace step under the frozen
# snapshot. This leaves the trace fully derived rather than author-described.
# A future snapshot that admitted a non-abstaining result would require its own
# governed schema version, which is itself a rejected drift condition here.
TRACE_STEP_REQUIRED_OUTPUT = {
    "frozen_input_identity_verified": "verified",
    "evidence_admission_evaluated": "admitted_set_frozen",
    "evidence_classification_applied": "classification_applied",
    "source_owned_freshness_recorded": "freshness_recorded",
    "driver_ledger_populated": "unable_to_determine",
    "missingness_and_conflict_propagated": "unable_to_determine",
    "representation_sensitivity_evaluated": "unable_to_determine",
    "endpoint_authority_evaluated": "no_positive_endpoint_authority",
    "constraint_effects_applied": "not_binding",
    "sleeve_outcome_determined": "abstain",
    "unassigned_capital_reconciled": "unassigned_retained",
}

TRACE_OUTPUT_VOCAB = frozenset(TRACE_STEP_REQUIRED_OUTPUT.values())

# Exactly the XASSET-0021 §Q triggers, in this order. Not author-selected.
CANONICAL_REOPEN_TRIGGER_ORDER = (
    "methodology_effective_identity_changed",
    "frozen_evidence_path_or_hash_changed",
    "new_evidence_class_pair_representation_endpoint_or_freshness_rule_proposed",
    "liquidity_or_level2_boundary_changed",
    "accepted_risk_identity_or_disposition_changed",
    "validator_revealed_incomplete_closure_or_nondeterminism",
    "application_would_require_unrepresented_judgment",
)

# ---------------------------------------------------------------------------
# 4. Closed vocabularies (XASSET-0021 §L item 4)
# No free-text synonym may control any outcome.
# ---------------------------------------------------------------------------

EVIDENCE_CLASSIFICATION = frozenset({"DRIVER", "CONSTRAINT", "DISCLOSURE"})

EVIDENCE_ADMISSION = frozenset({
    "admitted",
    "excluded_hash_mismatch",
    "excluded_missing_path",
    "excluded_authority_failure",
    "excluded_validator_failure",
})

FRESHNESS_STATE = frozenset({
    "source_owned_current",
    "source_owned_stale",
    "no_governed_currentness_rule",
    "historical_fixed",
})

MISSINGNESS_STATE = frozenset({
    "present",
    "missing_no_accepted_record",
    "unavailable_censored",
    "not_computable_interface_only",
})

CONFLICT_STATE = frozenset({
    "no_conflict",
    "same_authority_contrary_directions",
    "determinate_plus_indeterminate",
    "higher_authority_conflict",
})

REPRESENTATION_STATE = frozenset({
    "all_required_admitted_and_agreeing",
    "required_representation_missing",
    "required_representation_unavailable",
    "required_representation_conflicted",
    "required_representation_directionally_disagreeing",
})

DRIVER_DIRECTION = frozenset({
    "favors_self",
    "favors_counterpart",
    "unable_to_determine",
})

CONSTRAINT_STATE = frozenset({"not_binding", "binding_clips_to_unassigned"})

DISCLOSURE_STATE = frozenset({"recorded_non_directional"})

PAIR_CONCLUSION = frozenset({
    "unable_to_determine",
    "favors_self",
    "favors_counterpart",
})

SLEEVE_OUTCOME_TYPE = frozenset({"abstain", "point", "range"})

UNCERTAINTY_STATE = frozenset({"determinate", "unable_to_determine"})

SLEEVE_VS_UNASSIGNED = frozenset({
    "no_positive_endpoint_authority",
    "positive_endpoint_authority_established",
})

RECONCILIATION_STATE = frozenset({
    "exact_symbolic_identity_holds",
    "invalid_requires_plug",
    "invalid_negative_complement",
})

LIQUIDITY_STATUS = frozenset({
    "unresolved_not_entered_into_application_ledger",
    "resolved_entered_into_application_ledger",
})

UNASSIGNED_DEPLOYMENT_STATUS = frozenset({"prohibited_without_future_governance"})

PROVISIONAL_ADOPTION_STATE = frozenset({"provisional_not_adopted"})

AUTHORIZATION_STATUS = frozenset({"withheld", "granted"})

# ---------------------------------------------------------------------------
# 5. Fixed upstream identities (XASSET-0021 §A)
# Mechanically fixed constants -- never author-chosen, never wall-clock.
# ---------------------------------------------------------------------------

METHODOLOGY_IDENTITY = {
    "decision_id": "XASSET-0020",
    "accepted_head": "d2c0ce84f1922bc606c3de6983eb47266dbe4d72",
    "decision_file_sha256":
        "f04ee116b7ed93165f621f65d91594557c5e4e3d0744d5f87ddfea5ccba999d2",
    "independent_review_id": "4943427551",
    "principal_acceptance_id": "5301699393",
    "merge_commit": "e7d66d93b5f7ab2ecd985a7a4bf680a118df6b0e",
    "post_merge_verification_id": "5301728726",
    "merge_ci_run_id": "31878188273",
}

CLOSURE_IDENTITY = {
    "decision_id": "XASSET-0021",
    "accepted_head": "afc3eef410dd3748c209053bdb8de7dd09c273bf",
    "independent_review_id": "4943931318",
    "principal_acceptance_id": "5302485718",
    "merge_commit": "5f94634bdfd0ff8ab603b8dd6ece2921033191df",
    "post_merge_verification_id": "5302525526",
    "merge_ci_run_id": "31887814190",
}

# The tree the evidence snapshot was frozen at. This is a DIFFERENT commit from
# any future artifact's own containing commit, so recording it is not
# self-referential (XASSET-0021 §L item 8).
SOURCE_TREE_IDENTITY = "e7d66d93b5f7ab2ecd985a7a4bf680a118df6b0e"

SNAPSHOT_ID = "XASSET-0021-FROZEN-SNAPSHOT-V1"

# ---------------------------------------------------------------------------
# 6. Frozen evidence manifest -- exactly the 35 XASSET-0021 §C identities
# (21 non-RISK + 14 RISK). Mechanical transcription of accepted governance
# text; every entry is independently re-verifiable against the repository tree.
# ---------------------------------------------------------------------------

FROZEN_EVIDENCE = (
    ("PROFILE_EQUITY", "intelligence/level1_sleeve_synthesis/profiles/equity.yaml", "edf3cce04b2f63bed97975ba8dd04313d5bd0a6e4c06b165987580e3f47f4796", "1f44f44369a4c1fe9ea824d99e82539d96f9ccf6407a740ef93d182a8b64bedc"),
    ("PROFILE_FUND_BROAD_MARKET", "intelligence/level1_sleeve_synthesis/profiles/fund_broad_market.yaml", "a2657187141f4dbeaa9f1a583192c74071eb530985a194fedb9c69a72d10f194", "2ed99d67847a9aea644be6867c53cac15b5870eff84ea759ab87a7a3a2d49de1"),
    ("PROFILE_FUND_GLD_DEFENSIVE", "intelligence/level1_sleeve_synthesis/profiles/fund_gld_defensive.yaml", "f7474115e8e9303fa07c2b7b0db589a855c4a386c50bf4a06dec8e57b3aada01", "255c74fc9b3d901de1aa1418765aabcac6f995e62270cdc306dd1c07373a23e1"),
    ("PROFILE_CRYPTO", "intelligence/level1_sleeve_synthesis/profiles/crypto.yaml", "3677dacfc0956450cd83da8537d85cc3e03c0860156c59b557d0bbbe10dad4a1", "3c0cfcd1e7fd61357e5507e23b460a3d63137b6b678815f194982588df683e31"),
    ("REL_EQUITY_FUND_BROAD_MARKET", "intelligence/level1_sleeve_synthesis/relationships/equity_fund_broad_market.yaml", "c54b24f4f8cf793043df0b76628a55905a2e63949f70a02578573183b3ba331c", "8667974b8e08926173ffb9819e4418a06fe2731b0983883fab062e8a272ed0f8"),
    ("REL_EQUITY_FUND_GLD_DEFENSIVE", "intelligence/level1_sleeve_synthesis/relationships/equity_fund_gld_defensive.yaml", "7af1e3f98d81cf86e70fbd175df615f700a019fa3f27fd70c969d417e0abf390", "5f5daa85f6aea16354fb8a6202df23747c39b57147a201debffdc37b67dbabed"),
    ("REL_CRYPTO_EQUITY", "intelligence/level1_sleeve_synthesis/relationships/crypto_equity.yaml", "673d45e6c60ee1f133a8c006975be62ce8f5a73d9d241be9391c2c6f4332c70e", "54fa83d59e761536fa332ef3eb23f8a995a5f2ce3a99acb2034fb90042aa7e9e"),
    ("REL_CRYPTO_FUND_GLD_DEFENSIVE", "intelligence/level1_sleeve_synthesis/relationships/crypto_fund_gld_defensive.yaml", "bbe09701f46211007d5574efc93fb70a8c7d0f83bd6c29cecc51d4721d0f447b", "d939157d59d4d59fdab81d3d1a51900551dd6a69588c7198864c7608c33b8312"),
    ("ETF_ECON_SPY", "intelligence/instrument_economic_assessment/SPY.yaml", "b5ce51c220d6b16d67efa6253dbd2d53108f9c522899ef63316a93388b4a5221", "3bd02ff4028830439573a78f2b2cbe6d92070615ca1907f5530de72dfec57cda"),
    ("ETF_ECON_VEA", "intelligence/instrument_economic_assessment/VEA.yaml", "d4f9bb5a1b103c51b3ddda2e533c0ea3e4d16e1e5c83a075894b9e19e9750da1", "b8c90454d98bbc445360f92562ff01bfee40e25e7c5f6bb004b5c95d259cc42c"),
    ("ETF_ECON_VWO", "intelligence/instrument_economic_assessment/VWO.yaml", "470234f9a0e68c59cb873ad87ada902763f3460663853559a1bb1edd5fd4fb03", "4f9986fb7eae9758b558d5f9d76325eb6469e82912ed0c2457d6c491ca10ac00"),
    ("CRYPTO_ECON_BTC", "intelligence/instrument_economic_assessment/BTC.yaml", "617924326be8c1f5459174fd2b81ce2eff89d45d87e7315ce2651f9c9a42ca0b", "99a2e2dabc40aa6cf8004b17807495390e1d65523efa9bd4d48fe9329f72d3c0"),
    ("CRYPTO_ECON_ETH", "intelligence/instrument_economic_assessment/ETH.yaml", "2261fb6c0c8684226950d0b13c152373068c326434050f06963e4736765fe0d2", "830953dc1da2f74f30f77fc7ab6e518e59c77cc6612454554ba133010c6ba4b4"),
    ("CRYPTO_ECON_SOL", "intelligence/instrument_economic_assessment/SOL.yaml", "74d423e3e3626f80fd2c8a5684fb6836ec610967251854eb9040b8f36d51c309", "b94b5785a661479ba6a9a8539dded3c180cf36703797263785e878e49f089734"),
    ("GLD_FUNCTION", "intelligence/functional_doctrine/GLD_DEFENSIVE_ROLE.yaml", "cf391b226c8d08bca55216bdb094bcf99d57f8ad6b8f4b4d55e3c7797f2f483d", "52dd76614fab7e3a6ac33b9da6486ea2d485b935a8ab633cef88ba323c9a9b5e"),
    ("GLD_ECON", "intelligence/economic_assessment/GLD.yaml", "e75577cd546bb906cddf49a24d80c2e48637ab6939c86a2002c95f1931121991", "055d3e9abd270122c7120bbfd474b61a2282d7c0fd7803b82fe8ec1edfce5406"),
    ("OVERLAP_ETF_DIRECT", "intelligence/overlap_model/etf_direct_equity_duplication.yaml", "79de4b36224301befe86a24664604ed72f9a11e810714e6e06faffb099b13a9f", "aae8dcc80b9a55741910abacad90dbbb6c7e27f0cacbd339d17b49d7c34c7b77"),
    ("OVERLAP_ISSUER_LOOKTHROUGH", "intelligence/overlap_model/issuer_overlap_etf_lookthrough.yaml", "e0255956d0bdb4e4704a8c007d2435a08bd4f093ecf95a8fec17f485afdcd1fc", "246bc77aaf831db1478884eb3eea831d3a1731ecf281b0ca20e0616643f81c12"),
    ("OVERLAP_CRYPTO_INTERFACE", "intelligence/overlap_model/crypto_correlation_interface.yaml", "d55527be57f7d8ba4641d578aeecb69b383219171e7199e01b33c635f8535591", "90553348b0f23f2f20caab718e10db5da979b2e86b36a144a666ca6831646108"),
    ("OVERLAP_DEFENSIVE_INTERFACE", "intelligence/overlap_model/defensive_offset_interface.yaml", "55992b329ef5617be374ccf873c85f2338ce9355b249b26a3a1522a65c1e0ad4", "cf9cd500f2710c7280effde328a5b414e3620c7dcb213049b5ebd0c99a5b2316"),
    ("EQUITY_VALUATION_MANIFEST", "intelligence/valuation_results/COHORT_MANIFEST.yaml", "2f402e3c20b4ecc83d30cae2eb389c82ccba4c2a5ebf1a0d00e8cb15cf8be85f", "5956a37d0de87def2e94a62a80c87956bb0fc7e6bcc674812a556d0eabc89d11"),
    ("RISK_PROTOCOL_V1_MD", "research/level1_sleeve_robustness/PROTOCOL_V1.md", "90277ad4767e4766d7a38c1199affde66f44e55ff16fd7f73e0894380cf8a425", None),
    ("RISK_PRE_REGISTRATION_YAML", "research/level1_sleeve_robustness/pre_registration.yaml", "8da1697456e8a8f4a168c99ae8387c77cd023e0e615cf51c78110165223d3c5a", None),
    ("RISK_IMPLEMENTATION_CONFIG_YAML", "research/level1_sleeve_robustness/implementation_config.yaml", "9f97162260ca97ef340b56811d8d91009235922cddf478ff39be7270614301de", None),
    ("RISK_ELIGIBILITY_MATRIX_JSON", "research/level1_sleeve_robustness/eligibility_matrix.json", "3854e9203c6b282e3d7c398b19a8f35de6cdad1c291b06456af19fa4d47ed680", None),
    ("RISK_TRIAL_REGISTRY_JSON", "research/level1_sleeve_robustness/trial_registry.json", "8942227dfba3a4fff6b1b94067ad252f0890cfa0959e2939e25ef98036904f51", None),
    ("RISK_INDEPENDENT_PREEXECUTION_REVIEW_JSON", "research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/independent_preexecution_review.json", "ec9dd6aeb4b8f5751ea8679c700723203b20777e89623b52882508a0a144b2cd", None),
    ("RISK_EXECUTION_RECEIPT_JSON", "research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/execution_receipt.json", "9d72f2b461e7834d24b3cadac0ebd5572e10c89519ae863b4ec7cc241158ac24", None),
    ("RISK_RAW_EVIDENCE_JSON", "research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/raw_evidence.json", "eae2f5e54950efbe5fe97016d688b09529507c915658fed020e94568171c1cbc", None),
    ("RISK_CELL_RESULTS_JSON", "research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/cell_results.json", "c5f6d8b0f24dee69ca0c398a42071ddbec04eddb0baeef014f6fb89932111b61", None),
    ("RISK_DISPOSITION_JSON", "research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/disposition.json", "364a324c6dad68d84ee5126600e2caef6ac6d3253c739e6ed55773325107e5d5", None),
    ("RISK_DIAGNOSTICS_JSON", "research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/diagnostics.json", "f1c5d08fdebb368472c5e07a4c485d3c8356ed3c7116737dc6ba348d17ce5b04", None),
    ("RISK_RESULTS_MD", "research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/RESULTS.md", "2a6b814e8df578bbc30c4bf2c40e05815df48cf0d1c2308630b7f7042ff207bc", None),
    ("RISK_LIMITATIONS_AND_SURVIVORSHIP_MD", "research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/LIMITATIONS_AND_SURVIVORSHIP.md", "28eb4796d371ffb527845b8539b5cbb14493a191452b2f37bca4956a21971deb", None),
    ("RISK_RESULTS_DISCLOSURE_SUPPLEMENT_MD", "research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/RESULTS_DISCLOSURE_SUPPLEMENT.md", "8013f376a0ad08bbbdffe7e6481d8d3e40b993b98515f6f3a9b7c445d49ded45", None),
)

FROZEN_EVIDENCE_COUNT = len(FROZEN_EVIDENCE)

FROZEN_EVIDENCE_BY_ID = {row[0]: row for row in FROZEN_EVIDENCE}


def evidence_manifest_sha256() -> str:
    """Mechanically derived identity of the frozen evidence manifest.

    Derived from the frozen list itself -- no wall clock, no author input.
    """
    manifest = [
        {"evidence_id": eid, "path": path, "sha256": sha,
         "source_content_sha256": content}
        for eid, path, sha, content in sorted(FROZEN_EVIDENCE)
    ]
    return sha256(canonical_bytes(manifest)).hexdigest()


EVIDENCE_MANIFEST_SHA256 = evidence_manifest_sha256()

# ---------------------------------------------------------------------------
# 7. Application authorization registry -- THE HARD GATE
#
# XASSET-0021 §O installs a double gate: this schema unit becoming effective
# does NOT authorize an application. A lawful artifact must name an
# application-authorization decision that appears here. The set is EMPTY, so no
# artifact can validate today. Adding an entry requires its own separate,
# independently reviewed, principal-accepted governance decision.
# ---------------------------------------------------------------------------

APPLICATION_AUTHORIZATION_REGISTRY: frozenset[str] = frozenset()

# ---------------------------------------------------------------------------
# 8. Complete closed field sets (XASSET-0021 §L item 3)
# Every mapping level is closed: extra keys and missing keys both fail.
# ---------------------------------------------------------------------------

TOP_LEVEL_KEYS = frozenset({
    "schema_identity",
    "methodology_identity",
    "prerequisite_identity",
    "application_authorization",
    "evidence_snapshot_identity",
    "normalized_asset_state",
    "evidence_snapshot",
    "sleeves",
    "pairs",
    "portfolio_reconciliation",
    "reopen_triggers",
    "authority_boundary",
})

SCHEMA_IDENTITY_KEYS = frozenset(SCHEMA_IDENTITY)

METHODOLOGY_IDENTITY_KEYS = frozenset(METHODOLOGY_IDENTITY)

PREREQUISITE_IDENTITY_KEYS = frozenset({
    "closure_decision_id",
    "closure_accepted_head",
    "closure_merge_commit",
    "schema_decision_id",
    "schema_accepted_head",
})

APPLICATION_AUTHORIZATION_KEYS = frozenset({
    "decision_id",
    "authorization_status",
})

EVIDENCE_SNAPSHOT_IDENTITY_KEYS = frozenset({
    "snapshot_id",
    "source_count",
    "source_tree_identity",
    "evidence_manifest_sha256",
})

NORMALIZED_ASSET_STATE_KEYS = frozenset({
    "denominator_identity",
    "separately_governed_liquidity_state",
    "debt_excluded",
})

LIQUIDITY_STATE_KEYS = frozenset({"status", "numeric_value"})

EVIDENCE_ENTRY_KEYS = frozenset({
    "evidence_id",
    "path",
    "sha256",
    "source_content_sha256",
    "governing_authority",
    "authority_lifecycle",
    "permitted_question",
    "classification",
    "admission",
    "freshness_state",
    "representation_scope",
    "forbidden_implications",
})

SLEEVE_KEYS = frozenset({
    "sleeve_id",
    "admitted_drivers",
    "applicable_constraints",
    "disclosures",
    "representation_sensitivity",
    "uncertainty_state",
    "sleeve_vs_unassigned",
    "conflict_missingness_state",
    "outcome_type",
    "point_or_range_or_null",
    "deterministic_derivation_trace",
})

TRACE_STEP_KEYS = frozenset({
    "step_id",
    "step_index",
    "inputs_referenced",
    "output_recorded",
})

PAIR_KEYS = frozenset({
    "canonical_pair_id",
    "self_sleeve",
    "counterpart_sleeve",
    "direct_evidence",
    "driver_ledger",
    "missing_conflicting_stale_evidence",
    "constraint_effects",
    "conclusion",
})

DRIVER_LEDGER_ENTRY_KEYS = frozenset({
    "driver_class",
    "direction",
    "missingness",
    "conflict_state",
    "evidence_refs",
})

CONSTRAINT_EFFECT_KEYS = frozenset({"constraint_id", "state", "evidence_refs"})

PORTFOLIO_RECONCILIATION_KEYS = frozenset({
    "exact_feasible_set_or_point",
    "unsized_unassigned_capital",
    "constraint_clipping_to_unassigned",
    "reconciliation_identity",
    "reconciliation_state",
})

UNSIZED_UNASSIGNED_CAPITAL_KEYS = frozenset({"symbol", "deployment_status"})

AUTHORITY_BOUNDARY_KEYS = frozenset({
    "provisional_not_adopted",
    "no_policy_effect",
    "no_level2_effect",
    "no_liquidity_or_debt_effect",
})

# ---------------------------------------------------------------------------
# 9. Governed identifier set.
#
# Every value that this schema itself defines as a closed identifier. A string
# that is EXACTLY one of these is a validated closed-vocabulary value, not free
# text, so the validator's free-text token scans do not apply to it. This keeps
# governed identifiers such as `diversification_cobehavior` (which contains the
# substring "rsi") and `liquidity_or_level2_boundary_changed` (which contains
# "level2") from tripping scans aimed at genuinely free-text fields.
#
# Membership here is not a licence: every one of these values is separately
# checked against its own closed vocabulary at its own position in the schema.
# ---------------------------------------------------------------------------


def _governed_identifiers() -> frozenset[str]:
    values: set[str] = set()
    for vocabulary in (
        EVIDENCE_CLASSIFICATION, EVIDENCE_ADMISSION, FRESHNESS_STATE,
        MISSINGNESS_STATE, CONFLICT_STATE, REPRESENTATION_STATE, DRIVER_DIRECTION,
        CONSTRAINT_STATE, DISCLOSURE_STATE, PAIR_CONCLUSION, SLEEVE_OUTCOME_TYPE,
        UNCERTAINTY_STATE, SLEEVE_VS_UNASSIGNED, RECONCILIATION_STATE,
        LIQUIDITY_STATUS, UNASSIGNED_DEPLOYMENT_STATUS, PROVISIONAL_ADOPTION_STATE,
        AUTHORIZATION_STATUS, TRACE_OUTPUT_VOCAB,
    ):
        values |= set(vocabulary)
    values |= set(CANONICAL_SLEEVE_ORDER)
    values |= set(CANONICAL_PAIR_ORDER)
    values |= set(CANONICAL_DRIVER_CLASS_ORDER)
    values |= set(CANONICAL_TRACE_STEP_ORDER)
    values |= set(CANONICAL_REOPEN_TRIGGER_ORDER)
    values |= set(SCHEMA_IDENTITY.values())
    values |= {row[0] for row in FROZEN_EVIDENCE}
    values |= {row[1] for row in FROZEN_EVIDENCE}
    values |= {row[2] for row in FROZEN_EVIDENCE}
    values |= {row[3] for row in FROZEN_EVIDENCE if row[3]}
    values |= set(METHODOLOGY_IDENTITY.values())
    values |= set(CLOSURE_IDENTITY.values())
    values |= {SOURCE_TREE_IDENTITY, SNAPSHOT_ID, EVIDENCE_MANIFEST_SHA256}
    return frozenset(values)


# Fixed exact values that carry no author discretion.
RECONCILIATION_IDENTITY_TEXT = (
    "NORMALIZED_ASSET_UNIT = SUM(ADMITTED_SLEEVE_ASSIGNMENTS)"
    " + UNSIZED_UNASSIGNED_CAPITAL"
)
UNSIZED_UNASSIGNED_CAPITAL_SYMBOL = "UNSIZED_UNASSIGNED_CAPITAL"
DENOMINATOR_IDENTITY = "XASSET-0020_NORMALIZED_UNLEVERED_ASSET_UNIT"

GOVERNED_IDENTIFIERS = _governed_identifiers() | {
    RECONCILIATION_IDENTITY_TEXT,
    UNSIZED_UNASSIGNED_CAPITAL_SYMBOL,
    DENOMINATOR_IDENTITY,
}
