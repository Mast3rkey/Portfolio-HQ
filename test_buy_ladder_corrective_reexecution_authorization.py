from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
DECISION = ROOT / "governance/decisions/LADDER-0004-invalid-initial-execution-and-corrective-reexecution-authorization.md"
CATALOG = ROOT / "governance/decisions.yaml"
PROTOCOL = ROOT / "research/buy_ladder_backtest/PROTOCOL_V2.md"


def test_invalid_attempt_is_explicitly_non_decision_grade():
    text = DECISION.read_text(encoding="utf-8")
    assert "c435243376b1ed761ac4c0f5e69281fcbbce4d45" in text
    assert "https://github.com/Mast3rkey/Portfolio-HQ/pull/384" in text
    assert "INVALID AND NON-DECISION-GRADE" in text
    assert "portfolio_paths.json` has no retained blob" in text
    assert "does not close LADDER V2" in text


def test_corrective_execution_is_one_shot_and_result_blind_until_reviewed():
    text = " ".join(DECISION.read_text(encoding="utf-8").split())
    required = (
        "exactly one corrective execution",
        "Result-free implementation phase",
        "that contains no holdout metric or disposition",
        "isolated temporary reconstruction workspace",
        "Freeze the candidate code SHA",
        "Without changing reviewed code",
        "including daily paths",
        "holdout was previously exposed",
        "another execution would require a new decision",
    )
    for phrase in required:
        assert phrase in text


def test_frozen_protocol_and_advisory_boundaries_are_preserved():
    decision = " ".join(DECISION.read_text(encoding="utf-8").split())
    protocol = PROTOCOL.read_text(encoding="utf-8")
    for phrase in (
        "may not change or reinterpret the roster",
        "may not acquire later data",
        "No implementation choice may be selected because it improves or harms a particular arm",
        "changes no production target",
        "UNARMED AND NOT EXECUTABLE",
    ):
        assert phrase in decision
    assert "After one valid registered run, the study closes." in protocol


def test_decision_catalog_exactly_registers_ladder_0004():
    rows = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["decisions"]
    matches = [row for row in rows if row.get("decision_id") == "LADDER-0004"]
    assert matches == [{
        "decision_id": "LADDER-0004",
        "date": __import__("datetime").date(2026, 9, 7),
        "status": "Accepted",
        "category": "research_integrity_correction",
        "related_decisions": [
            "GOV-0001", "GOV-0002", "OPS-0009", "NUM-0001",
            "LADDER-0001", "LADDER-0002", "LADDER-0003",
        ],
        "supporting_artifact": None,
        "file": "governance/decisions/LADDER-0004-invalid-initial-execution-and-corrective-reexecution-authorization.md",
    }]
