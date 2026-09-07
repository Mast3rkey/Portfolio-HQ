"""Regression checks for the post-execution whole-portfolio evidence disposition."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

import risk_level1_acquisition as acquisition


ROOT = Path(__file__).resolve().parent
DISPOSITION_PATH = (
    ROOT / "research/whole_portfolio_robustness/evidence_disposition.json"
)
SOURCE_INVENTORY_PATH = (
    ROOT / "research/level1_sleeve_robustness/data/source_inventory.json"
)
INPUT_FREEZE_PATH = (
    ROOT / "research/whole_portfolio_robustness/execution/input_freeze.json"
)
ACTION_PATH = (
    ROOT
    / "research/level1_sleeve_robustness/data/transformed/actions/alpaca_actions.json"
)


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_disposition_preserves_every_original_authority_and_result_byte() -> None:
    disposition = _json(DISPOSITION_PATH)
    assert disposition["current_evidence_status"] == "EVIDENCE_LIMITED_NOT_DECISION_GRADE"
    assert disposition["original_artifacts"]["disposition_text"] == "RETAIN_BASELINE"
    assert (
        disposition["original_artifacts"]["claim_limit"]
        == "ORIGINAL_DISPOSITION_MAY_NOT_BE_CITED_AS_EMPIRICAL_VALIDATION_OF_THE_BASELINE"
    )
    for relpath, expected in disposition["original_artifacts"]["sha256"].items():
        assert _sha256(ROOT / relpath) == expected


def test_consumed_alpaca_transforms_reconstruct_from_retained_raw_bytes() -> None:
    data_root = ROOT / "research/level1_sleeve_robustness/data"
    candidates = data_root / "transformed/candidates/alpaca"
    for candidate_path in sorted(candidates.glob("*.json")):
        symbol = candidate_path.stem
        bars = []
        for raw_path in sorted(
            (data_root / "raw/alpaca/stocks" / symbol).glob("page-*.json")
        ):
            bars.extend(_json(raw_path).get("bars") or [])
        reconstructed = acquisition.normalize_alpaca_bars(
            symbol, bars, "ALPACA_MARKET_DATA"
        )
        retained = _json(candidate_path)
        reconstructed["events"] = retained["events"]
        assert reconstructed == retained

    action_rows = []
    for raw_path in sorted((data_root / "raw/alpaca/actions").glob("*/*.json")):
        payload = _json(raw_path)
        for action_type, rows in (payload.get("corporate_actions") or {}).items():
            action_rows.extend(
                {"action_type": action_type, **row} for row in (rows or [])
            )
    assert acquisition.normalize_actions(action_rows) == _json(ACTION_PATH)


def test_consumed_source_and_action_conflicts_are_complete_and_reproducible() -> None:
    disposition = _json(DISPOSITION_PATH)
    frozen = _json(INPUT_FREEZE_PATH)["datasets"]
    inventory_doc = _json(SOURCE_INVENTORY_PATH)
    inventory = {
        row["instrument"]: row
        for row in (
            inventory_doc["stock_and_etf_datasets"]
            + inventory_doc["crypto_datasets"]
        )
    }

    source_mismatches = [
        ticker
        for ticker, consumed in frozen.items()
        if consumed["sha256"] != inventory[ticker]["selected_transformed_sha256"]
    ]
    action_mismatches = [
        ticker
        for ticker in source_mismatches
        if inventory[ticker].get("action_reconciliation_mismatch") is True
    ]
    source_finding = disposition["findings"]["consumed_source_selection_conflict"]
    action_finding = disposition["findings"]["corporate_action_reconciliation_conflict"]

    assert len(frozen) == source_finding["consumed_dataset_count"] == 28
    assert source_mismatches == source_finding["mismatch_tickers"]
    assert len(source_mismatches) == source_finding["mismatch_count"] == 23
    assert action_mismatches == action_finding["mismatch_tickers"]
    assert len(action_mismatches) == action_finding["mismatch_count"] == 17
    assert all(inventory[ticker]["selected_provider"] == "YAHOO_FINANCE_CHART" for ticker in source_mismatches)
    assert all(frozen[ticker]["provider"] == "ALPACA_MARKET_DATA" for ticker in source_mismatches)


def test_sol_gap_and_rtx_identity_boundary_are_not_masked() -> None:
    disposition = _json(DISPOSITION_PATH)
    inventory = {
        row["instrument"]: row
        for row in _json(SOURCE_INVENTORY_PATH)["crypto_datasets"]
    }
    sol = inventory["SOL"]
    sol_finding = disposition["findings"]["sol_coverage_gap"]
    sessions = _json(
        ROOT
        / "research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json"
    )["sessions"]
    affected_sessions = [
        row["session"]
        for row in sessions
        if "2021-01-04" <= row["session"] <= "2021-06-17"
    ]
    assert sol["lawful_inception"] == sol_finding["registered_lawful_inception"]
    assert sol["fallback_quality"]["first_observation"] == sol_finding["first_consumed_observation"]
    assert len(affected_sessions) == sol_finding["affected_confirmation_sessions"] == 115
    assert affected_sessions[0] == sol_finding["first_affected_session"]
    assert affected_sessions[-1] == sol_finding["last_affected_session"]

    lineage = yaml.safe_load(
        (
            ROOT
            / "research/level1_sleeve_robustness/data/identity_lineage.yaml"
        ).read_text(encoding="utf-8")
    )
    rtx_identity = next(row for row in lineage["records"] if row["instrument"] == "RTX")
    rtx_rows = {
        row["date"]: row
        for row in _json(
            ROOT
            / "research/level1_sleeve_robustness/data/transformed/candidates/alpaca/RTX.json"
        )["rows"]
    }
    rtx_finding = disposition["findings"]["rtx_identity_boundary"]
    assert rtx_identity["lawful_inception"] == rtx_finding["registered_lawful_inception"]
    assert rtx_identity["predecessor_stitching"] == "PROHIBITED"
    assert rtx_rows["2020-04-02"]["close"] == rtx_finding["close_2020_04_02"]
    assert rtx_rows["2020-04-03"]["close"] == rtx_finding["close_2020_04_03"]
    observed_return = (
        rtx_rows["2020-04-03"]["close"] / rtx_rows["2020-04-02"]["close"] - 1
    )
    assert abs(observed_return - rtx_finding["one_session_return"]) < 1e-15


def test_confirmed_asml_omission_and_downstream_halts_are_explicit() -> None:
    disposition = _json(DISPOSITION_PATH)
    finding = disposition["findings"]["known_action_omission"]
    actions = _json(ACTION_PATH)["rows"]
    retained = [
        row
        for row in actions
        if row.get("symbol") == "ASML"
        and row.get("action_type") == "cash_dividend"
        and row.get("ex_date") == "2026-07-28"
    ]
    assert retained == []
    assert finding["retained_action_present"] is False
    assert finding["declared_gross_per_share"] == "1.88"
    assert finding["gross_usd_before_withholding_and_fees"] == "2.137748"
    assert finding["source"].startswith("https://www.asml.com/")
    assert disposition["downstream_gates"] == {
        "ladder_validation": "HALT_PENDING_ACCEPTED_EXACT_INPUT_DISPOSITION",
        "ladder_execution": "HALT_PENDING_ACCEPTED_EXACT_INPUT_DISPOSITION",
        "margin_input_reuse": "PROHIBITED_WITHOUT_SEPARATE_REVALIDATION",
        "stage1": "UNARMED_AND_NOT_EXECUTABLE",
    }


def test_decision_catalog_and_prominent_readme_status_agree() -> None:
    disposition = _json(DISPOSITION_PATH)
    decision_path = (
        ROOT
        / "governance/decisions/RISK-0005-whole-portfolio-evidence-disposition.md"
    )
    front = yaml.safe_load(decision_path.read_text(encoding="utf-8").split("---\n", 2)[1])
    catalog = yaml.safe_load((ROOT / "governance/decisions.yaml").read_text(encoding="utf-8"))
    catalog_row = next(
        row for row in catalog["decisions"] if row["decision_id"] == "RISK-0005"
    )
    assert front["status"] == catalog_row["status"] == "Accepted"
    assert front["supporting_artifact"] == catalog_row["supporting_artifact"]
    assert front["decision_id"] == disposition["decision_id"]
    readme_prefix = " ".join((
        ROOT / "research/whole_portfolio_robustness/README.md"
    ).read_text(encoding="utf-8").splitlines()[:12])
    assert "EVIDENCE LIMITED" in readme_prefix
    assert "not" in readme_prefix.lower() and "validation" in readme_prefix.lower()
