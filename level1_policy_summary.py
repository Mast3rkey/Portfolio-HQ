"""Deterministic, recommendation-only Level-1 view of canonical targets.

This module does not propose or change portfolio policy. It aggregates the
currently accepted per-instrument destination weights in ``targets.yaml`` into
the economic sleeves a person needs for a whole-portfolio review. It has no
brokerage, pricing, holdings, allocator, margin, or Stage-1 dependency.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

import yaml


POLICY_BASIS = ("PHQ-2026-01", "PHQ-2026-02", "PHQ-2026-04")
CANONICAL_TOTAL = Decimal("100.00")
BROAD_MARKET_TICKERS = frozenset({"SPY", "VEA", "VWO"})
GOLD_TICKERS = frozenset({"GLD"})


class PolicySummaryError(ValueError):
    """Raised when canonical targets cannot be mapped without judgment."""


def _decimal(value: Any, *, ticker: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except Exception as exc:  # pragma: no cover - Decimal exposes several subclasses
        raise PolicySummaryError(f"{ticker}: target_pct is not numeric") from exc
    if not result.is_finite() or result < 0:
        raise PolicySummaryError(f"{ticker}: target_pct must be finite and non-negative")
    return result


def _sleeve_for(row: Mapping[str, Any]) -> str:
    ticker = str(row.get("ticker", "")).strip().upper()
    asset_class = str(row.get("asset_class", "")).strip()
    if not ticker:
        raise PolicySummaryError("destination row has no ticker")
    if asset_class == "equity":
        return "direct_equity"
    if asset_class == "crypto":
        return "crypto"
    if asset_class in {"cash", "reserve"}:
        return "cash_and_reserve"
    if asset_class == "fund" and ticker in BROAD_MARKET_TICKERS:
        return "broad_market_funds"
    if asset_class == "fund" and ticker in GOLD_TICKERS:
        return "gold_defensive"
    raise PolicySummaryError(
        f"{ticker}: no deterministic Level-1 mapping for asset_class={asset_class!r}"
    )


def build_policy_summary(targets: Mapping[str, Any]) -> dict[str, Any]:
    """Return an exact sleeve aggregation of an already-adopted target policy."""

    destination = targets.get("destination")
    if not isinstance(destination, list) or not destination:
        raise PolicySummaryError("targets.destination must be a non-empty list")

    totals = {
        "direct_equity": Decimal("0"),
        "broad_market_funds": Decimal("0"),
        "gold_defensive": Decimal("0"),
        "crypto": Decimal("0"),
        "cash_and_reserve": Decimal("0"),
    }
    members: dict[str, list[str]] = {name: [] for name in totals}
    seen: set[str] = set()
    for row in destination:
        if not isinstance(row, Mapping):
            raise PolicySummaryError("every destination row must be a mapping")
        ticker = str(row.get("ticker", "")).strip().upper()
        if ticker in seen:
            raise PolicySummaryError(f"duplicate destination ticker: {ticker}")
        seen.add(ticker)
        sleeve = _sleeve_for(row)
        totals[sleeve] += _decimal(row.get("target_pct"), ticker=ticker)
        members[sleeve].append(ticker)

    assigned = sum(totals.values(), Decimal("0"))
    if assigned > CANONICAL_TOTAL:
        raise PolicySummaryError(f"assigned targets exceed 100%: {assigned}")
    unallocated = CANONICAL_TOTAL - assigned
    equities = totals["direct_equity"] + totals["broad_market_funds"]

    display_totals = {key: f"{value:.2f}" for key, value in totals.items()}
    display_totals["broad_market_and_equities"] = f"{equities:.2f}"
    display_totals["unallocated"] = f"{unallocated:.2f}"
    return {
        "status": "CURRENT_ACCEPTED_POLICY_SNAPSHOT",
        "policy_source": "targets.yaml",
        "policy_basis": list(POLICY_BASIS),
        "units": "percent_of_book",
        "sleeves_pct": display_totals,
        "members": members,
        "reconciliation": {
            "assigned_pct": f"{assigned:.2f}",
            "unallocated_pct": f"{unallocated:.2f}",
            "total_pct": f"{assigned + unallocated:.2f}",
        },
        "safety": {
            "changes_policy": False,
            "uses_live_data": False,
            "uses_holdings": False,
            "places_orders": False,
            "arms_or_executes_stage1": False,
        },
    }


def load_policy_summary(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, Mapping):
        raise PolicySummaryError("targets document must be a mapping")
    return build_policy_summary(data)


def _render_text(summary: Mapping[str, Any]) -> str:
    sleeves = summary["sleeves_pct"]
    rows = (
        ("Direct equities", sleeves["direct_equity"]),
        ("Broad-market funds", sleeves["broad_market_funds"]),
        ("Broad-market + equities", sleeves["broad_market_and_equities"]),
        ("Gold", sleeves["gold_defensive"]),
        ("Crypto", sleeves["crypto"]),
        ("Cash + reserve", sleeves["cash_and_reserve"]),
        ("Unallocated", sleeves["unallocated"]),
    )
    lines = ["CURRENT ACCEPTED LEVEL-1 POLICY", ""]
    lines.extend(f"{label:<27} {value:>6}%" for label, value in rows)
    lines.extend(
        (
            "",
            f"Reconciled total             {summary['reconciliation']['total_pct']:>6}%",
            "Recommendation-only snapshot; no policy, holding, or execution state changed.",
        )
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Show the accepted target policy as deterministic Level-1 sleeves."
    )
    parser.add_argument("--targets", type=Path, default=Path("targets.yaml"))
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)
    summary = load_policy_summary(args.targets)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(_render_text(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
