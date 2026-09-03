import csv
from datetime import datetime, timezone

import pytest

import allocate
from measurement_ledger import (
    MeasurementError,
    exact_twr,
    read_cashflows,
    record_cashflow,
    record_interest,
    record_margin_sync,
)


T0 = datetime(2026, 9, 3, 12, 0, tzinfo=timezone.utc)
T1 = datetime(2026, 9, 3, 13, 0, tzinfo=timezone.utc)
T2 = datetime(2026, 9, 3, 14, 0, tzinfo=timezone.utc)


def _rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_cashflow_requires_exact_bracketing_identity(tmp_path):
    path = tmp_path / "cashflow.csv"
    with pytest.raises(MeasurementError, match="book_after must equal"):
        record_cashflow(
            path,
            direction="deposit",
            amount=50,
            book_before=100,
            book_after=149,
            occurred_at=T1,
        )
    assert not path.exists()


def test_cashflow_is_append_only_and_strictly_ordered(tmp_path):
    path = tmp_path / "cashflow.csv"
    record_cashflow(
        path, direction="deposit", amount=50, book_before=100,
        book_after=150, occurred_at=T1,
    )
    record_cashflow(
        path, direction="withdrawal", amount=20, book_before=160,
        book_after=140, occurred_at=T2,
    )
    with pytest.raises(MeasurementError, match="strictly increasing"):
        record_cashflow(
            path, direction="deposit", amount=1, book_before=140,
            book_after=141, occurred_at=T1,
        )
    rows = read_cashflows(path)
    assert [row["direction"] for row in rows] == ["deposit", "withdrawal"]
    assert b"\r" not in path.read_bytes()


@pytest.mark.parametrize(
    "bad_row",
    [
        "2026-09-03T13:00:00Z,deposit,1,1,2,statement,note,extra\n",
        "2026-09-03T13:00:00Z,deposit,1,1,2,statement\n",
        '2026-09-03T13:00:00Z,deposit,1,1,2,statement,"unterminated\n',
    ],
)
def test_existing_malformed_rows_block_reads_and_appends(tmp_path, bad_row):
    path = tmp_path / "cashflow.csv"
    path.write_text(
        ",".join((
            "occurred_at", "direction", "amount", "book_before", "book_after",
            "source", "note",
        )) + "\n" + bad_row,
        encoding="utf-8",
    )
    original = path.read_bytes()
    with pytest.raises(MeasurementError, match="schema|malformed CSV"):
        read_cashflows(path)
    with pytest.raises(MeasurementError, match="schema|malformed CSV"):
        record_cashflow(
            path, direction="deposit", amount=1, book_before=2,
            book_after=3, occurred_at=T2,
        )
    assert path.read_bytes() == original


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -1, True])
def test_measurement_numbers_fail_closed(tmp_path, bad):
    path = tmp_path / "cashflow.csv"
    with pytest.raises(MeasurementError):
        record_cashflow(
            path, direction="deposit", amount=bad,
            book_before=100, book_after=100, occurred_at=T1,
        )
    assert not path.exists()


def test_exact_twr_links_around_external_flow():
    performance = [
        {"observed_at": T0.isoformat(), "book": "100.00"},
        {"observed_at": T2.isoformat(), "book": "176.00"},
    ]
    flows = [{
        "occurred_at": T1.isoformat(),
        "direction": "deposit",
        "amount": "50.00",
        "book_before": "110.00",
        "book_after": "160.00",
    }]
    result = exact_twr(performance, flows)
    assert result.return_pct == pytest.approx(21.0)
    assert result.valuation_count == 2
    assert result.cashflow_count == 1


def test_exact_twr_ignores_legacy_rows_but_never_backfills_them():
    performance = [
        {"date": "2026-07-13", "observed_at": "", "book": ""},
        {"observed_at": T0.isoformat(), "book": "100.00"},
        {"observed_at": T1.isoformat(), "book": "110.00"},
    ]
    result = exact_twr(performance, [])
    assert result.return_pct == pytest.approx(10.0)
    assert result.valuation_count == 2


def test_exact_twr_refuses_insufficient_evidence():
    with pytest.raises(MeasurementError, match="at least two"):
        exact_twr([{"observed_at": T0.isoformat(), "book": 100}], [])


def test_exact_twr_refuses_ambiguous_timestamp_collision():
    performance = [
        {"observed_at": T0.isoformat(), "book": 100},
        {"observed_at": T2.isoformat(), "book": 110},
    ]
    flows = [{
        "occurred_at": T2.isoformat(), "direction": "deposit", "amount": 10,
        "book_before": 100, "book_after": 110,
    }]
    with pytest.raises(MeasurementError, match="collides"):
        exact_twr(performance, flows)


def test_margin_events_infer_draw_paydown_and_resync(tmp_path):
    path = tmp_path / "margin.csv"
    record_margin_sync(
        path, prior_debt=None, resulting_debt=100,
        resulting_buffer_pct=60, observed_at=T0,
    )
    record_margin_sync(
        path, prior_debt=100, resulting_debt=125,
        resulting_buffer_pct=55, observed_at=T1,
    )
    record_margin_sync(
        path, prior_debt=125, resulting_debt=75,
        resulting_buffer_pct=65, observed_at=T2,
    )
    record_margin_sync(
        path, prior_debt=75, resulting_debt=75,
        resulting_buffer_pct=64, observed_at="2026-09-03T15:00:00Z",
    )
    rows = _rows(path)
    assert [row["event_type"] for row in rows] == [
        "initial_sync", "draw", "paydown", "resync"
    ]
    assert [row["amount"] for row in rows] == ["0.00", "25.00", "50.00", "0.00"]


def test_interest_accepts_actual_charge_and_valid_period(tmp_path):
    path = tmp_path / "interest.csv"
    record_interest(
        path,
        amount_charged=12.34,
        statement_period_start="2026-08-01",
        statement_period_end="2026-08-31",
        charged_at=T2,
    )
    assert _rows(path)[0]["amount_charged"] == "12.34"


def test_interest_rejects_reversed_period(tmp_path):
    with pytest.raises(MeasurementError, match="must not precede"):
        record_interest(
            tmp_path / "interest.csv",
            amount_charged=1,
            statement_period_start="2026-09-01",
            statement_period_end="2026-08-31",
            charged_at=T2,
        )


def test_update_margin_preserves_state_and_adds_audit_event(tmp_path, monkeypatch):
    holdings = tmp_path / "holdings.yaml"
    holdings.write_text(
        "margin:\n  debt: 100.0\n  buffer_pct: 60.0\n  synced_at: 2026-09-03\n"
        "holdings: {}\nshares: {}\ncrypto_shares: {}\n",
        encoding="utf-8",
    )
    margin_log = tmp_path / "margin_log.csv"
    monkeypatch.setattr(allocate, "HOLDINGS_FILE", holdings)
    monkeypatch.setattr(allocate, "MARGIN_LOG_FILE", margin_log)
    monkeypatch.setattr(allocate, "log_performance", lambda *args, **kwargs: None)

    allocate.update_margin(80, 65, "manual verification")

    row = _rows(margin_log)[0]
    assert row["event_type"] == "paydown"
    assert row["amount"] == "20.00"
    assert row["note"] == "manual verification"
    assert "debt: 80.0" in holdings.read_text(encoding="utf-8")


def test_render_performance_labels_exact_twr_unavailable_for_legacy_log(
        tmp_path, monkeypatch):
    perf = tmp_path / "performance_log.csv"
    perf.write_text(
        "date,net_equity,gross,margin_debt,qqq_price,voo_price,note\n"
        "2026-07-13,100,100,0,100,100,\n"
        "2026-07-14,110,110,0,101,101,\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(allocate, "PERF_LOG_FILE", perf)
    monkeypatch.setattr(allocate, "CASHFLOW_LOG_FILE", tmp_path / "cashflows.csv")
    out = allocate.render_performance()
    assert "Exact cash-flow-adjusted TWR: **unavailable**" in out
    assert "at least two timestamped whole-book snapshots" in out
