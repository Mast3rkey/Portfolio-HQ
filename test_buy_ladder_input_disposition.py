"""Fail-closed checks for LADDER-0003's result-blind input freeze."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from decimal import Decimal
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
STUDY = ROOT / "research/buy_ladder_backtest"
INPUTS = STUDY / "inputs"
DISPOSITION = INPUTS / "input_disposition.json"
ACTIONS = INPUTS / "corporate_actions.json"
YAHOO = INPUTS / "yahoo_action_crosscheck.json"
AMENDMENT = STUDY / "PROTOCOL_V2_FOREIGN_DIVIDEND_AMENDMENT.md"
BUILDER = STUDY / "build_input_disposition.py"
DECISION = ROOT / "governance/decisions/LADDER-0003-ladder-input-evidence-disposition.md"

PINS = {
    AMENDMENT: "c6e44d91aaa022f7159cd40f4df0c3cfc2b8fabfbed50044b83299f229647e81",
    BUILDER: "7536af8b8b7e8595beb99f8a2ad0a33d65861663bcbaf6d8850adf2f32e34d8b",
    DISPOSITION: "a045d88e23c49210e933787b9e151c6f2ce5cdfb5e3b970ebf072691276af210",
    ACTIONS: "4cd066e9ef72041941ab59a283bc5b2aa61351979f47356c27a9ec4c06c9b828",
    YAHOO: "3a2a7b7604a43bd97a485065b0e59af11e8fd65c3c487a012c0c1ad0f6496544",
}
ROSTER = (
    "NVDA TSM ASML AVGO KLAC MSFT GOOGL AMZN META PANW LLY ISRG TMO V COST "
    "CEG ETN GEV GNRC PWR RTX SPY VEA VWO GLD"
).split()


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_builder():
    spec = importlib.util.spec_from_file_location("ladder_input_disposition", BUILDER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_artifacts_and_catalog_entry_are_pinned() -> None:
    for path, expected in PINS.items():
        assert _sha(path) == expected

    front = yaml.safe_load(DECISION.read_text(encoding="utf-8").split("---\n", 2)[1])
    rows = yaml.safe_load((ROOT / "governance/decisions.yaml").read_text())["decisions"]
    matches = [row for row in rows if row["decision_id"] == "LADDER-0003"]
    assert len(matches) == 1
    assert front["status"] == matches[0]["status"] == "Accepted"
    assert front["supporting_artifact"] == matches[0]["supporting_artifact"]
    assert all(value in DECISION.read_text(encoding="utf-8") for value in PINS.values())


def test_price_roster_paths_and_hashes_fail_closed() -> None:
    disposition = _json(DISPOSITION)
    price_files = disposition["price_files"]
    assert [row["ticker"] for row in price_files] == ROSTER
    assert len({row["path"] for row in price_files}) == len(ROSTER) == 25

    for row in price_files:
        path = ROOT / row["path"]
        payload = _json(path)
        observations = payload["rows"]
        assert _sha(path) == row["sha256"]
        assert row["provider"] == "ALPACA_MARKET_DATA_SIP"
        assert row["adjustment"] == "split"
        assert row["total_row_count"] == len(observations)
        assert row["first_observation"] == observations[0]["date"]
        assert row["last_observation"] == observations[-1]["date"] == "2026-07-31"
        assert row["admitted_start"] == max("2021-06-01", observations[0]["date"])

    by_ticker = {row["ticker"]: row for row in price_files}
    assert by_ticker["CEG"]["admitted_start"] == "2022-02-02"
    assert by_ticker["GEV"]["admitted_start"] == "2024-04-02"
    assert by_ticker["RTX"]["identity_floor"] == "2020-04-03"


def test_action_ledger_is_unique_complete_and_preserves_receivables() -> None:
    disposition = _json(DISPOSITION)
    payload = _json(ACTIONS)
    events = payload["events"]
    assert payload["action_as_of"] == disposition["action_as_of"] == "2026-09-07"
    assert payload["selection_basis"].startswith("ex_date entitlement")
    assert disposition["corporate_actions"] == {
        "event_count": 381,
        "path": "research/buy_ladder_backtest/inputs/corporate_actions.json",
        "sha256": PINS[ACTIONS],
    }
    assert len(events) == 381
    keys = {(event["symbol"], event["action_type"], event["ex_date"]) for event in events}
    assert len(keys) == len(events)
    assert all(event["symbol"] in ROSTER for event in events)
    assert all("2021-06-01" <= event["ex_date"] <= "2026-07-31" for event in events)

    late = [(event["symbol"], event["ex_date"], event["payable_date"])
            for event in events if event.get("payable_date", "") > "2026-07-31"]
    assert late == [
        ("COST", "2026-07-23", "2026-08-07"),
        ("ASML", "2026-07-28", "2026-08-05"),
    ]


def test_cross_security_contamination_and_date_conflicts_are_closed() -> None:
    payload = _json(ACTIONS)
    events = payload["events"]
    quarantined = payload["quarantined_events"]
    assert len(quarantined) == 1
    assert quarantined[0]["source_id"] == "43368afb-52dd-4894-bcd5-27bc10ec73b6"
    assert quarantined[0]["cusip"] == "G3730V147"
    assert quarantined[0]["identified_security"] == "FTAI Aviation Series D preferred"
    assert not any(event.get("cusip") == "G3730V147" for event in events)

    lookup = {(event["symbol"], event["ex_date"]): event for event in events}
    assert lookup[("COST", "2026-07-23")]["gross_rate_usd"] == 1.47
    assert lookup[("ASML", "2026-07-28")]["gross_rate_usd"] == 2.137748
    assert ("ETN", "2025-11-06") in lookup
    assert ("ETN", "2025-11-05") not in lookup
    assert any("eaton.com" in source for source in lookup[("ETN", "2025-11-06")]["source_lineage"])

    crosscheck = _json(DISPOSITION)["action_crosscheck"]
    assert crosscheck["snapshot_sha256"] == PINS[YAHOO]
    assert crosscheck["scope"].startswith("secondary completeness cross-check only")
    assert [row["symbol"] for row in crosscheck["exceptions"]] == ["ASML", "COST", "ETN"]


def test_foreign_dividend_facts_inferences_and_tax_math_are_explicit() -> None:
    events = _json(ACTIONS)["events"]
    dividends = [event for event in events if event["action_type"] == "cash_dividend"]
    assert all(event["rate_evidence"] for event in dividends)
    tsm = [event for event in dividends if event["symbol"] == "TSM"]
    assert len(tsm) == 21
    assert all(event["rate_evidence"] == "ISSUER_EXACT_GROSS_AND_SOURCE_NET" for event in tsm)
    assert all(any("investor.tsmc.com" in source for source in event["source_lineage"])
               for event in tsm)

    event = next(row for row in tsm if row["ex_date"] == "2026-06-11")
    gross = Decimal(str(event["gross_rate_usd"]))
    source_withholding = Decimal(str(event["source_withholding_usd"]))
    tentative_us_tax = Decimal("0.168") * gross
    foreign_tax_credit = min(source_withholding, tentative_us_tax)
    residual_us_tax = tentative_us_tax - foreign_tax_credit
    total_tax = source_withholding + residual_us_tax
    assert source_withholding == gross - Decimal(str(event["source_net_rate_usd"]))
    assert total_tax == max(source_withholding, tentative_us_tax)

    text = AMENDMENT.read_text(encoding="utf-8")
    for token in (
        "foreign_tax_credit      = min(source_withholding, tentative_us_tax)",
        "foreign-tax-credit sensitivity that sets the credit to zero",
        "INSUFFICIENT_EVIDENCE",
        "UNARMED AND NOT EXECUTABLE",
    ):
        assert token in text


def test_entitlement_filter_does_not_repeat_process_date_cutoff_defect() -> None:
    module = _load_builder()
    included = {
        "ex_date": "2026-07-23",
        "process_date": "2026-08-07",
        "payable_date": "2026-08-07",
    }
    excluded = {
        "ex_date": "2026-08-03",
        "process_date": "2026-07-30",
        "payable_date": "2026-08-20",
    }
    assert module.is_in_entitlement_window(included)
    assert not module.is_in_entitlement_window(excluded)


def test_sol_gap_is_not_silently_stitched_or_rehabilitated() -> None:
    disposition = _json(DISPOSITION)
    sol = disposition["sol_disposition"]
    assert sol["ladder_scope"] == "EXCLUDED_BY_LADDER-0002"
    assert sol["prior_robustness_status"] == "EVIDENCE_LIMITED_NOT_DECISION_GRADE"
    assert "may be inferred or stitched" in sol["successor_rule"]
    assert disposition["old_robustness_artifacts"].endswith(
        "PROHIBITED_AS_DECISION_GRADE_EVIDENCE"
    )
