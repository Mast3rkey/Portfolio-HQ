"""Regression coverage for performance_log.csv's line-ending defect.

csv.DictWriter defaults to the "excel" dialect's CRLF line terminator
regardless of platform, and log_performance() opens the file with
newline="" (required so the csv module controls line endings at all) —
which lets that literal \\r\\n through unmodified. Every other tracked
file in this repo is LF-only, and CI's git-diff-check step flags a
rewritten CRLF row as trailing whitespace (reproduced against PR #127's
32a2d05 and PR #130). log_performance() must always emit LF only, both
when appending a brand-new row and when rewriting an existing same-day
row (the idempotent re-log path that actually triggered both failures).
"""

import csv
import datetime

import pytest
import yaml

import allocate


class _FakeClient:
    def get_bars(self, *a, **k):
        return [{"c": 100.0}]


@pytest.fixture(autouse=True)
def current_state(tmp_path, monkeypatch):
    """A holdings.yaml with a CURRENT cash and margin observation.

    Added under PHQ-2026-07 item 8: log_performance() now refuses to write a row
    at all when margin state is stale, unknown or out of domain, because
    ``net_equity = gross - margin_debt`` would otherwise record an unverified
    debt as today's. These tests are about LINE ENDINGS, so they need a row to
    actually be written -- this supplies the current state that produces one.
    Nothing about the line-ending assertions is relaxed; a separate suite
    (test_protected_capital_accounting.py) pins the refusal itself.
    """
    today = datetime.date.today().isoformat()
    f = tmp_path / "holdings.yaml"
    f.write_text(yaml.safe_dump({
        "shares": {"AAA": 10.0},
        "cash": {"balance": 500.0, "synced_at": today},
        "margin": {"debt": 0.0, "buffer_pct": 60.0, "synced_at": today},
    }))
    monkeypatch.setattr(allocate, "HOLDINGS_FILE", f)
    return f


def test_appended_row_has_no_carriage_return(tmp_path, monkeypatch):
    perf_log = tmp_path / "performance_log.csv"
    monkeypatch.setattr(allocate, "PERF_LOG_FILE", perf_log)

    allocate.log_performance(client=_FakeClient(), quiet=True,
                             resolved_holdings={"AAA": 1000.0})

    raw = perf_log.read_bytes()
    assert b"\r" not in raw


def test_rewritten_existing_row_has_no_carriage_return(tmp_path, monkeypatch):
    # The exact path that broke CI twice: log_performance() is idempotent
    # per day (_read_perf_log() drops any existing row for today before
    # appending the fresh one), so a second same-day call rewrites the row
    # rather than appending a new one.
    perf_log = tmp_path / "performance_log.csv"
    monkeypatch.setattr(allocate, "PERF_LOG_FILE", perf_log)

    allocate.log_performance(client=_FakeClient(), quiet=True,
                             resolved_holdings={"AAA": 1000.0})
    allocate.log_performance(client=_FakeClient(), quiet=True,
                             resolved_holdings={"AAA": 1200.0})

    raw = perf_log.read_bytes()
    assert b"\r" not in raw
    assert raw.count(b"\n") == 2, "one header line + one data line, LF-terminated"


def test_rewrite_preserves_data_and_ordering_only_line_endings_differ(tmp_path, monkeypatch):
    perf_log = tmp_path / "performance_log.csv"
    monkeypatch.setattr(allocate, "PERF_LOG_FILE", perf_log)

    # Seed a CRLF-formatted prior log, matching what's actually committed
    # today -- confirms the fix normalizes on the very next write without
    # dropping or reordering any existing row.
    seeded_rows = [
        {"date": "2026-07-16", "net_equity": "100.0", "gross": "100.0",
         "margin_debt": "0.0", "qqq_price": "700.0", "voo_price": "690.0", "note": ""},
        {"date": "2026-07-17", "net_equity": "110.0", "gross": "110.0",
         "margin_debt": "0.0", "qqq_price": "701.0", "voo_price": "691.0", "note": ""},
    ]
    with open(perf_log, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=allocate.PERF_FIELDS, lineterminator="\r\n")
        w.writeheader()
        w.writerows(seeded_rows)
    assert b"\r\n" in perf_log.read_bytes()   # sanity: seed really is CRLF

    allocate.log_performance(client=_FakeClient(), quiet=True,
                             resolved_holdings={"AAA": 1000.0})

    raw = perf_log.read_bytes()
    assert b"\r" not in raw

    with open(perf_log, newline="") as f:
        result_rows = list(csv.DictReader(f))

    assert [r["date"] for r in result_rows] == ["2026-07-16", "2026-07-17", allocate.date.today().isoformat()]
    assert result_rows[0]["net_equity"] == "100.0"
    assert result_rows[0]["gross"] == "100.0"
    assert result_rows[1]["net_equity"] == "110.0"
    assert result_rows[1]["gross"] == "110.0"


# ── PHQ-2026-07 correction round 3 — independent DELTA review 5085019004 ───────
# MAJOR 2 (reproduced two ways):
#
#   (a) log_performance() applied the finite-value boundary only when the caller
#       SUPPLIED resolved_holdings. Called without it -- the ordinary production
#       path -- it resolved holdings internally and summed them unchecked, so a
#       manual or orphan entry carrying NaN wrote gross, net_equity and book as
#       the literal string ``nan``.
#
#   (b) Benchmark closes were read straight out of the bars. A NaN QQQ or VOO
#       close serialized as ``nan`` in the ledger -- recorded as though it were
#       today's observed price.
#
# The correction applies ONE boundary to whichever mapping is about to be summed,
# regardless of how it was obtained, and treats an invalid optional benchmark
# observation the same way an absent fetch is treated: blank, never a current NaN.

import math

NON_FINITE = [
    pytest.param(float("nan"), id="nan"),
    pytest.param(float("inf"), id="posinf"),
    pytest.param(float("-inf"), id="neginf"),
]

#: Every spelling csv/str() can produce for a non-finite float, upper and lower.
NON_FINITE_SPELLINGS = ("nan", "inf", "infinity", "-inf", "-infinity",
                        "NAN", "INF", "INFINITY", "-INF", "-INFINITY")


def _assert_ledger_has_no_non_finite_spelling(perf_log):
    if not perf_log.exists():
        return
    text = perf_log.read_text()
    for token in NON_FINITE_SPELLINGS:
        assert token not in text, f"ledger contains {token!r}:\n{text}"


class _NonFiniteBenchClient:
    """Returns bars whose most recent close is not a finite number."""

    def __init__(self, value):
        self._v = value

    def get_bars(self, *a, **k):
        return [{"c": 100.0}, {"c": self._v}]


@pytest.mark.parametrize("bad", NON_FINITE)
def test_internally_resolved_non_finite_holding_writes_no_row(
        bad, tmp_path, monkeypatch, current_state):
    """(a) The production path: no caller-supplied set, one poisoned value.

    resolve_holdings() merges manual and orphan entries that never pass through
    the live-pricing path, so this is reachable without any API involvement.
    """
    perf_log = tmp_path / "performance_log.csv"
    monkeypatch.setattr(allocate, "PERF_LOG_FILE", perf_log)
    monkeypatch.setattr(allocate, "resolve_holdings",
                        lambda cfg: {"AAA": 1000.0, "MAN": bad})

    allocate.log_performance(client=_FakeClient(), quiet=True)

    assert not perf_log.exists(), (
        "a poisoned internally-resolved value must not produce a row at all")
    _assert_ledger_has_no_non_finite_spelling(perf_log)


@pytest.mark.parametrize("bad", NON_FINITE)
def test_caller_supplied_non_finite_holding_writes_no_row(
        bad, tmp_path, monkeypatch, current_state):
    """The same boundary on the other resolution path -- one rule, not two."""
    perf_log = tmp_path / "performance_log.csv"
    monkeypatch.setattr(allocate, "PERF_LOG_FILE", perf_log)

    allocate.log_performance(client=_FakeClient(), quiet=True,
                             resolved_holdings={"AAA": 1000.0, "MAN": bad})

    assert not perf_log.exists()
    _assert_ledger_has_no_non_finite_spelling(perf_log)


def test_internally_resolved_finite_holdings_do_write_a_row(
        tmp_path, monkeypatch, current_state):
    """Positive control for the path above: the guard is fail-closed, not fail-shut."""
    perf_log = tmp_path / "performance_log.csv"
    monkeypatch.setattr(allocate, "PERF_LOG_FILE", perf_log)
    monkeypatch.setattr(allocate, "resolve_holdings",
                        lambda cfg: {"AAA": 1000.0, "MAN": 25.0})

    allocate.log_performance(client=_FakeClient(), quiet=True)

    rows = list(csv.DictReader(perf_log.read_text().splitlines()))
    assert len(rows) == 1, rows
    assert float(rows[0]["gross"]) == pytest.approx(1025.0)
    _assert_ledger_has_no_non_finite_spelling(perf_log)


@pytest.mark.parametrize("bad", NON_FINITE)
def test_non_finite_benchmark_close_is_blank_not_a_current_value(
        bad, tmp_path, monkeypatch, current_state):
    """(b) An unusable optional observation is recorded as unavailable.

    The portfolio figures are independently valid here and must survive -- the
    correction withholds the benchmark reading, it does not discard a good row.
    """
    perf_log = tmp_path / "performance_log.csv"
    monkeypatch.setattr(allocate, "PERF_LOG_FILE", perf_log)

    allocate.log_performance(client=_NonFiniteBenchClient(bad), quiet=True,
                             resolved_holdings={"AAA": 1000.0})

    rows = list(csv.DictReader(perf_log.read_text().splitlines()))
    assert len(rows) == 1, rows
    assert rows[0]["qqq_price"] == "", rows[0]
    assert rows[0]["voo_price"] == "", rows[0]
    # ...while the real portfolio figures are untouched.
    assert float(rows[0]["gross"]) == pytest.approx(1000.0)
    _assert_ledger_has_no_non_finite_spelling(perf_log)


def test_a_finite_benchmark_close_is_still_recorded(
        tmp_path, monkeypatch, current_state):
    """Positive control: the benchmark boundary blanks only what is unusable."""
    perf_log = tmp_path / "performance_log.csv"
    monkeypatch.setattr(allocate, "PERF_LOG_FILE", perf_log)

    allocate.log_performance(client=_NonFiniteBenchClient(432.25), quiet=True,
                             resolved_holdings={"AAA": 1000.0})

    rows = list(csv.DictReader(perf_log.read_text().splitlines()))
    assert float(rows[0]["qqq_price"]) == pytest.approx(432.25)
    assert float(rows[0]["voo_price"]) == pytest.approx(432.25)
    _assert_ledger_has_no_non_finite_spelling(perf_log)


def test_a_valid_partial_caller_supplied_set_still_writes(
        tmp_path, monkeypatch, current_state):
    """The behaviour the correction was explicitly required to preserve.

    A caller-supplied set that does not cover every tracked name is legitimate --
    it is a snapshot of what the caller actually resolved. Only NON-FINITE values
    block a row; incompleteness alone does not.
    """
    perf_log = tmp_path / "performance_log.csv"
    monkeypatch.setattr(allocate, "PERF_LOG_FILE", perf_log)

    allocate.log_performance(client=_FakeClient(), quiet=True,
                             resolved_holdings={"AAA": 250.0})

    rows = list(csv.DictReader(perf_log.read_text().splitlines()))
    assert len(rows) == 1, rows
    assert float(rows[0]["gross"]) == pytest.approx(250.0)
    _assert_ledger_has_no_non_finite_spelling(perf_log)


@pytest.mark.parametrize("bad", NON_FINITE)
def test_no_ledger_field_ever_carries_a_non_finite_spelling(
        bad, tmp_path, monkeypatch, current_state):
    """The output-boundary claim, stated once over every path that can write.

    Whatever combination of poisoned holding and poisoned benchmark is supplied,
    and by whichever resolution route, the resulting file must contain no
    spelling of a non-finite float anywhere.
    """
    perf_log = tmp_path / "performance_log.csv"
    monkeypatch.setattr(allocate, "PERF_LOG_FILE", perf_log)

    for supplied in ({"AAA": 1000.0, "MAN": bad}, {"AAA": 1000.0}, None):
        if supplied is None:
            monkeypatch.setattr(allocate, "resolve_holdings",
                                lambda cfg: {"AAA": 1000.0, "MAN": bad})
            allocate.log_performance(client=_NonFiniteBenchClient(bad), quiet=True)
        else:
            allocate.log_performance(client=_NonFiniteBenchClient(bad), quiet=True,
                                     resolved_holdings=supplied)
        _assert_ledger_has_no_non_finite_spelling(perf_log)
