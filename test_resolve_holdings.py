"""Tests for resolve_holdings() — the live qty x price valuation path added
July 2026 to replace static dollar snapshots. Covers the fallback behavior for
tickers with no live price (SKHY's permanent zero-coverage gap) and no share
count (crypto), since a bug here silently misvalues the whole book.
"""

import yaml

import allocate
from allocate import resolve_holdings


class _FakeClient:
    """get_bars() should never be called when metrics already has the price —
    raising makes that assertion enforceable."""
    def get_bars(self, *a, **k):
        raise AssertionError("should not fetch bars when metrics already has the price")


def _write_holdings(path, holdings=None, shares=None, margin=None):
    data = {"holdings": holdings or {}, "shares": shares or {},
           "margin": margin or {"debt": 0.0, "buffer_pct": 50.0, "synced_at": "2026-07-13"}}
    with open(path, "w") as f:
        yaml.safe_dump(data, f)


def test_share_tracked_ticker_uses_qty_times_metrics_price(tmp_path, monkeypatch):
    hfile = tmp_path / "holdings.yaml"
    _write_holdings(hfile, holdings={}, shares={"AAPL": 2.0})
    monkeypatch.setattr(allocate, "HOLDINGS_FILE", hfile)

    result = resolve_holdings(_FakeClient(), metrics={"AAPL": {"price": 150.0}})
    assert result == {"AAPL": 300.0}


def test_no_live_price_falls_back_to_manual_holdings_value(tmp_path, monkeypatch):
    # SKHY-shaped case: no metrics price available at all, and no share count —
    # the manual dollar value in 'holdings' is used as-is.
    hfile = tmp_path / "holdings.yaml"
    _write_holdings(hfile, holdings={"SKHY": 24.45}, shares={})
    monkeypatch.setattr(allocate, "HOLDINGS_FILE", hfile)

    result = resolve_holdings(_FakeClient(), metrics={"SKHY": {"price": None}})
    assert result == {"SKHY": 24.45}


def test_share_tracked_ticker_with_missing_price_keeps_prior_manual_value(tmp_path, monkeypatch):
    # A share-tracked ticker whose price fetch comes back empty shouldn't be
    # silently zeroed or dropped — keep whatever was last known.
    hfile = tmp_path / "holdings.yaml"
    _write_holdings(hfile, holdings={"AAPL": 290.0}, shares={"AAPL": 2.0})
    monkeypatch.setattr(allocate, "HOLDINGS_FILE", hfile)

    class _NoBarsClient:
        def get_bars(self, *a, **k):
            return []

    result = resolve_holdings(_NoBarsClient(), metrics={"AAPL": {}})
    assert result == {"AAPL": 290.0}


def test_manual_only_entries_untouched_when_not_in_shares(tmp_path, monkeypatch):
    # Crypto-shaped case: value comes straight from 'holdings', 'shares' is empty.
    hfile = tmp_path / "holdings.yaml"
    _write_holdings(hfile, holdings={"ETH": 369.97, "SOL": 323.63}, shares={})
    monkeypatch.setattr(allocate, "HOLDINGS_FILE", hfile)

    result = resolve_holdings(_FakeClient(), metrics={})
    assert result == {"ETH": 369.97, "SOL": 323.63}


def test_shares_value_overrides_stale_manual_entry_for_same_ticker(tmp_path, monkeypatch):
    # If a ticker exists in both blocks (e.g. a stray old paste), the live
    # share-based value wins — 'shares' is the source of truth.
    hfile = tmp_path / "holdings.yaml"
    _write_holdings(hfile, holdings={"AAPL": 999.0}, shares={"AAPL": 2.0})
    monkeypatch.setattr(allocate, "HOLDINGS_FILE", hfile)

    result = resolve_holdings(_FakeClient(), metrics={"AAPL": {"price": 150.0}})
    assert result == {"AAPL": 300.0}


def test_zero_value_positions_dropped(tmp_path, monkeypatch):
    hfile = tmp_path / "holdings.yaml"
    _write_holdings(hfile, holdings={"BTC": 0.0}, shares={"AAPL": 0.0})
    monkeypatch.setattr(allocate, "HOLDINGS_FILE", hfile)

    result = resolve_holdings(_FakeClient(), metrics={"AAPL": {"price": 150.0}})
    assert result == {}
