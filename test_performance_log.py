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

import allocate


class _FakeClient:
    def get_bars(self, *a, **k):
        return [{"c": 100.0}]


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
