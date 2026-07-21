"""Direct, network-free unit tests for earnings.py's public contract.

Every test here replaces yfinance.Ticker with a mock object — no real
HTTP/network call is made anywhere in this file. This is the dedicated
counterpart to test_plan_gates.py's earnings-blackout tests (which cover
plan()'s gate logic against a monkeypatched allocate.days_until_earnings
and never touch earnings.py itself).
"""

from datetime import date, datetime, timedelta, timezone

import pytest
import yfinance

import earnings


@pytest.fixture(autouse=True)
def _clear_earnings_cache():
    """earnings._CACHE is module-level and persists across calls by design
    (see test_repeated_lookup_uses_cache_and_skips_provider below) — clear
    it before and after every test so tests can't see each other's cached
    results."""
    earnings._CACHE.clear()
    yield
    earnings._CACHE.clear()


class _FakeEarningsDates:
    """Stands in for the DataFrame get_earnings_dates() normally returns —
    earnings.py only ever touches .index and len(), both reproduced here."""

    def __init__(self, dates):
        self.index = list(dates)

    def __len__(self):
        return len(self.index)


class _FakeTicker:
    """Records every symbol/session it was constructed with, and serves
    canned get_earnings_dates()/calendar responses (or raises, if asked)."""

    calls: list[tuple[str, object]] = []

    def __init__(self, symbol, session=None, *, dates=None, dates_exc=None,
                calendar=None, calendar_exc=None):
        type(self).calls.append((symbol, session))
        self._dates = dates
        self._dates_exc = dates_exc
        self._calendar = calendar
        self._calendar_exc = calendar_exc

    def get_earnings_dates(self, limit=12):
        if self._dates_exc is not None:
            raise self._dates_exc
        if self._dates is None:
            return None
        return _FakeEarningsDates(self._dates)

    @property
    def calendar(self):
        if self._calendar_exc is not None:
            raise self._calendar_exc
        return self._calendar


def _install_fake_ticker(monkeypatch, **kwargs):
    """Patch yfinance.Ticker with a factory that always returns a
    _FakeTicker configured with the given canned responses, and reset the
    call-recording list so each test starts clean."""
    _FakeTicker.calls = []

    def factory(symbol, session=None):
        return _FakeTicker(symbol, session=session, **kwargs)

    monkeypatch.setattr(yfinance, "Ticker", factory)
    return _FakeTicker


def _today():
    return datetime.now(timezone.utc).date()


def test_upcoming_earnings_date_returned_correctly(monkeypatch):
    future = _today() + timedelta(days=10)
    _install_fake_ticker(monkeypatch, dates=[future])

    assert earnings.next_earnings_date("XYZ") == future
    assert earnings.days_until_earnings("XYZ") == 10


def test_past_date_is_ignored(monkeypatch):
    past = _today() - timedelta(days=5)
    # No calendar fallback data either, so a past-only table must resolve
    # to None rather than incorrectly surfacing the past date.
    _install_fake_ticker(monkeypatch, dates=[past], calendar=None)

    assert earnings.next_earnings_date("XYZ") is None
    assert earnings.days_until_earnings("XYZ") is None


def test_calendar_fallback_used_when_dates_table_has_no_upcoming_date(monkeypatch):
    future = _today() + timedelta(days=4)
    # get_earnings_dates() yields nothing usable (None result); the
    # secondary "calendar" source must be consulted and used instead.
    _install_fake_ticker(monkeypatch, dates=None,
                         calendar={"Earnings Date": [future]})

    assert earnings.next_earnings_date("XYZ") == future
    assert earnings.days_until_earnings("XYZ") == 4


def test_provider_failure_degrades_to_none(monkeypatch):
    _install_fake_ticker(monkeypatch,
                         dates_exc=RuntimeError("provider unavailable"),
                         calendar_exc=RuntimeError("provider unavailable"))

    assert earnings.next_earnings_date("XYZ") is None
    assert earnings.days_until_earnings("XYZ") is None


def test_repeated_lookup_uses_cache_and_skips_provider(monkeypatch):
    future = _today() + timedelta(days=7)
    fake_cls = _install_fake_ticker(monkeypatch, dates=[future])

    first = earnings.next_earnings_date("XYZ")
    second = earnings.next_earnings_date("XYZ")

    assert first == future
    assert second == future
    assert len(fake_cls.calls) == 1   # provider constructed exactly once


def test_brk_b_maps_to_yahoo_brk_dash_b_symbol(monkeypatch):
    fake_cls = _install_fake_ticker(monkeypatch, dates=None, calendar=None)

    earnings.next_earnings_date("BRK.B")

    assert len(fake_cls.calls) == 1
    symbol_used, _session = fake_cls.calls[0]
    assert symbol_used == "BRK-B"
