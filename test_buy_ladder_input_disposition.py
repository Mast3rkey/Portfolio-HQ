"""Fail-closed checks for LADDER-0003's result-blind input freeze."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
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
    AMENDMENT: "6f9e335caa5f0733c57932637cca1563a9daeb94a4dcdb81fe51587920f7c60f",
    BUILDER: "0d6f2311d0e3cbc01f16d729ca8ca0e68f769c855364559218590ea077e90cdd",
    DISPOSITION: "bc59b76c63387b8f8049128a8fcb16b0cfff776f4930dd6f20c8b9a2ee9dba96",
    ACTIONS: "79be46b9e64191d4897c5b9ada2c7ba7cfb8c4f86eca4e9ec6943c5895a6d2f1",
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


def _aggregate(root: Path, files: list[Path]) -> tuple[str, int]:
    ordered = sorted(files, key=lambda path: path.relative_to(root).as_posix())
    rows = "".join(f"{_sha(path)}  {path.relative_to(root).as_posix()}\n" for path in ordered)
    return hashlib.sha256(rows.encode("utf-8")).hexdigest(), len(ordered)


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


def test_selected_transforms_reconstruct_from_pinned_raw_bytes_and_receipts() -> None:
    disposition = _json(DISPOSITION)
    frozen = disposition["frozen_source_evidence"]
    data = ROOT / "research/level1_sleeve_robustness/data"
    inventory = data / "acquisition_receipt_inventory.json"
    raw_files = [path for path in (data / "raw").rglob("*") if path.is_file()]
    receipt_files = [path for path in (data / "receipts").rglob("*") if path.is_file()]

    assert _sha(inventory) == frozen["receipt_inventory_sha256"] == (
        "260095460e120a1ab222d48846f45fd1b246a634c04d900d966db64662d31a95"
    )
    assert _aggregate(ROOT, raw_files) == (
        frozen["raw_aggregate_sha256"], frozen["raw_file_count"]
    ) == ("76b9a429d15280b9b16624e66cc80129d2a7359cb12bcc948ed126ad2c19bfb7", 66)
    assert _aggregate(ROOT, receipt_files) == (
        frozen["receipt_aggregate_sha256"], frozen["receipt_file_count"]
    ) == ("abf6f603d71f388288a4c3e691e810f683f36fbec2c5d696ef9448551a677ce7", 963)
    assert frozen["transform_reconstruction"] == "EXACT_BYTE_IDENTITY_VERIFIED"

    provenance = disposition["upstream_action_registry"]["raw_provenance"]
    assert disposition["upstream_action_registry"]["reconstructed_from_raw"] is True
    assert len(provenance) == 28
    assert len({row["raw_path"] for row in provenance}) == 28
    assert len({row["receipt_path"] for row in provenance}) == 28
    for row in provenance + [entry["raw_provenance"] for entry in disposition["price_files"]]:
        assert _sha(ROOT / row["raw_path"]) == row["raw_sha256"]
        assert _sha(ROOT / row["receipt_path"]) == row["receipt_sha256"]

    # Re-run the actual reconstruction gate; it compares the reconstructed
    # canonical bytes with every retained transformed file before emitting.
    _load_builder().main()


def test_builder_checks_survive_optimized_python() -> None:
    source = BUILDER.read_text(encoding="utf-8")
    assert "assert " not in source
    before = _sha(DISPOSITION)
    completed = subprocess.run(
        [sys.executable, "-O", str(BUILDER)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert _sha(DISPOSITION) == before

    probe = subprocess.run(
        [
            sys.executable,
            "-O",
            "-c",
            (
                "import runpy; "
                f"m=runpy.run_path({str(BUILDER)!r}); "
                "m['require'](False, 'OPTIMIZED_SENTINEL')"
            ),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert probe.returncode != 0
    assert "InputIntegrityError: OPTIMIZED_SENTINEL" in probe.stderr


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
        ("COST", "2026-07-24", "2026-08-07"),
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
    cost = lookup[("COST", "2026-07-24")]
    assert cost["gross_rate_usd"] == 1.47
    assert cost["ex_date_evidence"] == (
        "RULE_BASED_INFERENCE_RECORD_DATE_EQUALS_REGULAR_EX_DATE_UNDER_NASDAQ_T1"
    )
    assert any("nasdaqtrader.com" in source for source in cost["source_lineage"])
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

    etn = [event for event in dividends if event["symbol"] == "ETN"]
    assert etn
    assert {event["withholding_convention"] for event in etn} == {
        "US_BROKER_DOCUMENTED_EXEMPTION_RESEARCH_ASSUMPTION"
    }
    assert {event["source_withholding_usd"] for event in etn} == {0.0}
    assert {event["withholding_sensitivity"]["case"] for event in etn} == {
        "NO_EXEMPTION_25_PERCENT_IRISH_DWT"
    }

    module = _load_builder()
    gross_quote = module.etn_dividend_terms(1.0, "GROSS")
    net_quote = module.etn_dividend_terms(0.75, "SOURCE_NET_AT_25_PERCENT")
    for key in ("gross_rate_usd", "source_net_rate_usd", "source_withholding_usd"):
        assert gross_quote[key] == net_quote[key]
    assert gross_quote["withholding_sensitivity"] == net_quote["withholding_sensitivity"]

    text = AMENDMENT.read_text(encoding="utf-8")
    for token in (
        "foreign_tax_credit      = min(source_withholding, tentative_us_tax)",
        "foreign-tax-credit sensitivity that sets the credit to zero",
        "mandatory no-exemption sensitivity with 25% Irish DWT",
        "INSUFFICIENT_EVIDENCE",
        "UNARMED AND NOT EXECUTABLE",
    ):
        assert token in text


def test_entitlement_filter_does_not_repeat_process_date_cutoff_defect() -> None:
    module = _load_builder()
    included = {
        "ex_date": "2026-07-24",
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
