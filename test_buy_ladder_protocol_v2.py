"""Integrity checks for the LADDER-0002 frozen execution protocol."""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
PROTOCOL = ROOT / "research/buy_ladder_backtest/PROTOCOL_V2.md"
DECISION = (
    ROOT
    / "governance/decisions/LADDER-0002-canonical-buy-ladder-execution-amendment.md"
)
PROTOCOL_SHA256 = "fce77edb5a214186c7f14e08cccb728f6d3e8f191d427e541c81bcfe2b6fab7f"
CONFIG_HASHES = {
    "targets.yaml": "69cda30c3f2f7bff00ef4cd3f8f59cda83ece999145e82646ff0987041da874d",
    "gates.yaml": "e9a0bcd98a45f75b77e5f60076be34c4eda890255bb9aa0cf1a14868418f2d86",
    "issuer_lookthrough.yaml": "6cf4e417e747d9a1ae9621e57d238c685ab593fb65539d561a5d136c7027b0b9",
    "research/level1_sleeve_robustness/data/raw/fred/DFF.csv": (
        "a052a99256ac7fdf075911b03496ab14acbcfd76f428137966bc0fd8781c4849"
    ),
}
ELIGIBLE = {
    "NVDA", "TSM", "ASML", "AVGO", "KLAC", "MSFT", "GOOGL", "AMZN",
    "META", "PANW", "LLY", "ISRG", "TMO", "V", "COST", "CEG", "ETN",
    "GEV", "GNRC", "PWR", "RTX", "SPY", "VEA", "VWO", "GLD",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    return yaml.safe_load(text.split("---\n", 2)[1])


def test_protocol_and_configuration_are_exactly_pinned() -> None:
    assert _sha256(PROTOCOL) == PROTOCOL_SHA256
    for relpath, expected in CONFIG_HASHES.items():
        assert _sha256(ROOT / relpath) == expected


def test_decision_and_catalog_bind_the_same_protocol() -> None:
    front = _front_matter(DECISION)
    rows = yaml.safe_load((ROOT / "governance/decisions.yaml").read_text())["decisions"]
    matches = [row for row in rows if row["decision_id"] == "LADDER-0002"]
    assert len(matches) == 1
    row = matches[0]
    assert front["status"] == row["status"] == "Accepted"
    assert front["supporting_artifact"] == row["supporting_artifact"]
    assert row["supporting_artifact"] == "research/buy_ladder_backtest/PROTOCOL_V2.md"
    assert PROTOCOL_SHA256 in DECISION.read_text(encoding="utf-8")


def test_protocol_freezes_identifiable_held_out_comparison() -> None:
    text = PROTOCOL.read_text(encoding="utf-8")
    for token in (
        "2021-06-01 through 2023-12-29",
        "2024-04-02 through 2026-07-31",
        "shared shadow allocator",
        "byte-identical across",
        "0 bp and 25 bp",
        "2,000 resamples",
        "mean block length 21",
        "historical earnings calendar",
        "UNARMED AND NOT EXECUTABLE",
    ):
        assert token in text
    assert "network,\naccount, credential, holdings, order, and brokerage access are prohibited" in text


def test_frozen_roster_has_data_and_excludes_protected_names() -> None:
    data_dir = (
        ROOT
        / "research/level1_sleeve_robustness/data/transformed/candidates/alpaca"
    )
    assert len(ELIGIBLE) == 25
    assert all((data_dir / f"{ticker}.json").is_file() for ticker in ELIGIBLE)
    text = PROTOCOL.read_text(encoding="utf-8")
    assert "SNPS, ICE, SPGI, WM, RKLB, and TSLA are gated and excluded" in text
    assert "BTC, ETH, SOL, CASH, and RESERVE are outside" in text
