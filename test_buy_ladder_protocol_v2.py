"""Integrity checks for the LADDER-0002 frozen execution protocol."""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
PROTOCOL = ROOT / "research/buy_ladder_backtest/PROTOCOL_V2.md"
DECISION = (
    ROOT
    / "governance/decisions/LADDER-0002-canonical-buy-ladder-execution-amendment.md"
)
PROTOCOL_SHA256 = "0529d0d64b213ad876173ba16f555b6c27b7812f483a4839bdffd9f47d609fe4"
CONFIG_HASHES = {
    "targets.yaml": "69cda30c3f2f7bff00ef4cd3f8f59cda83ece999145e82646ff0987041da874d",
    "gates.yaml": "e9a0bcd98a45f75b77e5f60076be34c4eda890255bb9aa0cf1a14868418f2d86",
    "issuer_lookthrough.yaml": "6cf4e417e747d9a1ae9621e57d238c685ab593fb65539d561a5d136c7027b0b9",
    "research/level1_sleeve_robustness/data/raw/fred/DFF.csv": (
        "a052a99256ac7fdf075911b03496ab14acbcfd76f428137966bc0fd8781c4849"
    ),
    "research/level1_sleeve_robustness/data/transformed/selected/DFF.json": (
        "a4610d02a33fc4e72eff5c54ba8499b7d0f85e5d828dd054e4158f967b530b5b"
    ),
    "research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json": (
        "365c740ed489a2804189dee439a8cfe4fd926db1f92957988e51ad91db12fabe"
    ),
    "research/level1_sleeve_robustness/data/source_inventory.json": (
        "9b604871e9180e9aa7a7ae298a749050a267ea81a7e402e099d9519a1d979f71"
    ),
    "research/level1_sleeve_robustness/data/transformed/actions/alpaca_actions.json": (
        "a75341f1279665423722074fbc3c89eed2a0c4708e8aefcd658220c3e7bc83b2"
    ),
}
ELIGIBLE = {
    "NVDA", "TSM", "ASML", "AVGO", "KLAC", "MSFT", "GOOGL", "AMZN",
    "META", "PANW", "LLY", "ISRG", "TMO", "V", "COST", "CEG", "ETN",
    "GEV", "GNRC", "PWR", "RTX", "SPY", "VEA", "VWO", "GLD",
}
ACTION_PATH = (
    ROOT
    / "research/level1_sleeve_robustness/data/transformed/actions/alpaca_actions.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    return yaml.safe_load(text.split("---\n", 2)[1])


def _anchor_basis_rate(
    raw_rate: Decimal,
    dividend_day: str,
    splits: list[dict],
    *,
    same_day_basis: str | None = None,
) -> Decimal:
    """Compact oracle for the frozen dividend-unit contract."""
    factor = Decimal("1")
    for split in splits:
        split_day = str(split["ex_date"])
        if split_day > dividend_day or (
            split_day == dividend_day and same_day_basis == "PRE_SPLIT"
        ):
            factor *= Decimal(str(split["new_rate"])) / Decimal(str(split["old_rate"]))
    return raw_rate / factor


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
        "seed **20260907**",
        "stable `targets.yaml` destination order as the deterministic tie-break",
        "minimum of those surpluses",
        "challenger annualized TWR - baseline annualized TWR > 0.0100",
        "challenger MaxDD - baseline MaxDD >= -0.0100",
        "365.2425-day year",
        "Sharpe use 252 trading sessions",
        "Actual/360 cash factor",
        "sole master trading calendar",
        "A blocked or sub-$25 candidate does not stop later candidates",
        "against both\nother arms",
        "accepted evidence-disposition decision",
        "effective 16.8% tax rate",
        "2026-07-31 adjustment anchor",
        "An ex-date open fill is\n  not eligible",
        "receivable payable after 2026-07-31 remains in final NAV",
        "price-only diagnostic",
        "after-tax total-return whole-portfolio voting holdout",
        "SOL's provider first observation",
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


def test_dividend_unit_entitlement_and_settlement_counterexamples() -> None:
    rows = json.loads(ACTION_PATH.read_text(encoding="utf-8"))["rows"]
    dividends = [
        row for row in rows
        if row.get("action_type") == "cash_dividend"
        and row.get("symbol") in ELIGIBLE
        and "2021-06-01" <= str(row.get("ex_date", "")) <= "2026-07-31"
    ]
    assert len(dividends) == 371
    assert all(row.get("payable_date") for row in dividends)

    splits = [row for row in rows if row.get("action_type") == "split"]
    nvda = next(
        row for row in dividends
        if row["symbol"] == "NVDA" and row["ex_date"] == "2024-03-05"
    )
    avgo = next(
        row for row in dividends
        if row["symbol"] == "AVGO" and row["ex_date"] == "2024-06-24"
    )
    nvda_splits = [row for row in splits if row.get("symbol") == "NVDA"]
    avgo_splits = [row for row in splits if row.get("symbol") == "AVGO"]
    assert _anchor_basis_rate(Decimal(str(nvda["rate"])), nvda["ex_date"], nvda_splits) == Decimal("0.004")
    assert _anchor_basis_rate(Decimal(str(avgo["rate"])), avgo["ex_date"], avgo_splits) == Decimal("0.525")

    same_day_split = [{"ex_date": "2024-01-02", "new_rate": 10, "old_rate": 1}]
    assert _anchor_basis_rate(
        Decimal("1"), "2024-01-02", same_day_split, same_day_basis="PRE_SPLIT"
    ) == Decimal("0.1")
    assert _anchor_basis_rate(
        Decimal("1"), "2024-01-02", same_day_split, same_day_basis="POST_SPLIT"
    ) == Decimal("1")

    preceding_close_quantity = Decimal("10")
    ex_date_open_fill = Decimal("5")
    gross_receivable = preceding_close_quantity * Decimal("0.004")
    assert gross_receivable == Decimal("0.040")
    assert gross_receivable != (
        preceding_close_quantity + ex_date_open_fill
    ) * Decimal("0.004")
    tax = gross_receivable * Decimal("0.168")
    net_receivable = gross_receivable - tax
    assert tax == Decimal("0.006720")
    assert net_receivable == Decimal("0.033280")

    cash_before, receivable_before = Decimal("0"), net_receivable
    nav_before = cash_before + receivable_before
    cash_after, receivable_after = cash_before + receivable_before, Decimal("0")
    assert cash_after + receivable_after == nav_before

    spy = next(
        row for row in dividends
        if row["symbol"] == "SPY" and row["ex_date"] == "2024-03-15"
    )
    assert spy["payable_date"] == "2024-04-30"
    assert spy["ex_date"] < "2024-04-02" < spy["payable_date"]
