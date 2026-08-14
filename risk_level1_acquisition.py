"""Receipt-first bounded acquisition for the RISK-0001 study.

This module performs data acquisition and normalization only.  It never imports
the result evaluator, computes a registered metric, or executes a registered
cell.  Yahoo and Coinbase bytes are written only to the ignored quarantine
tree.  Every HTTP attempt emits a redacted receipt, including failures.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

import certifi
import exchange_calendars as xcals
import yaml


ROOT = Path(__file__).resolve().parent
STUDY = ROOT / "research/level1_sleeve_robustness"
CONFIG_PATH = STUDY / "implementation_config.yaml"
PREREG_PATH = STUDY / "pre_registration.yaml"
DATA = STUDY / "data"
RAW = DATA / "raw"
TRANSFORMED = DATA / "transformed"
QUARANTINE = DATA / "quarantine"
RECEIPTS = DATA / "receipts"
START = "2004-11-18"
END = "2026-07-31"
USER_AGENT = "Portfolio-HQ-RISK-0001/1.0 research-acquisition"
RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


class AcquisitionError(RuntimeError):
    pass


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(value))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise AcquisitionError(f"{path}: expected mapping")
    return value


def representations(prereg: dict[str, Any]) -> tuple[list[str], list[str]]:
    equity = list(prereg["representations"]["EQUITY"]["ids"])
    broad = list(prereg["representations"]["FUND_BROAD_MARKET"]["ids"])
    gold = list(prereg["representations"]["FUND_GLD_DEFENSIVE"]["core_ids"])
    gold += list(prereg["representations"]["FUND_GLD_DEFENSIVE"]["conditional_ids"])
    crypto = list(prereg["representations"]["CRYPTO"]["ids"])
    return equity + broad + gold, crypto


def load_credentials(env_file: Path | None) -> dict[str, str]:
    values = dict(os.environ)
    if env_file is not None:
        if not env_file.is_file():
            raise AcquisitionError(f"credential file missing: {env_file}")
        for raw in env_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values.setdefault(key.strip(), value.strip().strip("'\""))
    key = values.get("ALPACA_API_KEY") or values.get("APCA_API_KEY_ID")
    secret = values.get("ALPACA_API_SECRET") or values.get("APCA_API_SECRET_KEY")
    if not key or not secret:
        raise AcquisitionError("missing Alpaca credentials")
    return {"APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": secret}


def _receipt_name(dataset_id: str, page: int, attempt: int) -> str:
    safe = dataset_id.replace("/", "_").replace(":", "_")
    return f"{safe}.run-{RUN_ID}.page-{page:04d}.attempt-{attempt}.json"


def fetch_bytes(
    *,
    dataset_id: str,
    provider: str,
    url: str,
    headers: dict[str, str] | None,
    raw_path: Path,
    page: int,
    cursor_in: str | None,
    retries: int = 3,
) -> tuple[bytes, dict[str, Any]]:
    """Fetch bytes and retain a receipt for every attempt.

    Header values are never serialized. URLs contain no credentials.
    """
    last: Exception | None = None
    context = __import__("ssl").create_default_context(cafile=certifi.where())
    for attempt in range(1, retries + 1):
        acquired_at = utc_now()
        status: int | None = None
        payload = b""
        error: str | None = None
        try:
            request_headers = {"User-Agent": USER_AGENT, **(headers or {})}
            request = urllib.request.Request(url, headers=request_headers)
            with urllib.request.urlopen(request, timeout=90, context=context) as response:
                status = int(response.status)
                payload = response.read()
            if status != 200:
                raise AcquisitionError(f"HTTP {status}")
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_bytes(payload)
            receipt = {
                "schema_version": "1.0",
                "study_id": "RISK-0001",
                "dataset_id": dataset_id,
                "provider": provider,
                "endpoint_locator": url,
                "request_headers": sorted((headers or {}).keys()),
                "request_timestamp_utc": acquired_at,
                "response_status": status,
                "page_index": page,
                "cursor_in": cursor_in,
                "raw_path": str(raw_path.relative_to(ROOT)) if raw_path.is_relative_to(ROOT) else str(raw_path),
                "raw_byte_count": len(payload),
                "raw_sha256": sha256_bytes(payload),
                "error": None,
            }
            write_json(RECEIPTS / _receipt_name(dataset_id, page, attempt), receipt)
            return payload, receipt
        except Exception as exc:  # network boundary; every attempt is retained
            last = exc
            if isinstance(exc, urllib.error.HTTPError):
                status = exc.code
            error = f"{type(exc).__name__}: {exc}"
            receipt = {
                "schema_version": "1.0",
                "study_id": "RISK-0001",
                "dataset_id": dataset_id,
                "provider": provider,
                "endpoint_locator": url,
                "request_headers": sorted((headers or {}).keys()),
                "request_timestamp_utc": acquired_at,
                "response_status": status,
                "page_index": page,
                "cursor_in": cursor_in,
                "raw_path": None,
                "raw_byte_count": 0,
                "raw_sha256": None,
                "error": error,
            }
            write_json(RECEIPTS / _receipt_name(dataset_id, page, attempt), receipt)
            if attempt < retries:
                time.sleep(float(attempt))
    raise AcquisitionError(f"{dataset_id}: request failed after {retries} logged attempts: {last}")


def alpaca_stock(symbol: str, headers: dict[str, str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    bars: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    token: str | None = None
    page = 0
    while True:
        params = {
            "timeframe": "1Day", "adjustment": "split", "feed": "sip",
            "limit": "10000", "start": START, "end": f"{END}T23:59:59Z",
        }
        if token:
            params["page_token"] = token
        url = f"https://data.alpaca.markets/v2/stocks/{urllib.parse.quote(symbol, safe='')}/bars?{urllib.parse.urlencode(params)}"
        payload, receipt = fetch_bytes(
            dataset_id=f"stock:{symbol}:alpaca", provider="ALPACA_MARKET_DATA", url=url,
            headers=headers, raw_path=RAW / "alpaca/stocks" / symbol / f"page-{page:04d}.json",
            page=page, cursor_in=token,
        )
        parsed = json.loads(payload)
        page_bars = parsed.get("bars") or []
        bars.extend(page_bars)
        token = parsed.get("next_page_token")
        receipt["next_page_or_terminal_marker"] = token if token else "TERMINAL"
        write_json(RECEIPTS / f"stock_{symbol}_alpaca.page-{page:04d}.final.json", receipt)
        receipts.append(receipt)
        page += 1
        if not token:
            break
    return bars, receipts


def alpaca_actions(symbols: Iterable[str], headers: dict[str, str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, str]]:
    all_rows: list[dict[str, Any]] = []
    all_receipts: list[dict[str, Any]] = []
    failures: dict[str, str] = {}
    symbols = list(symbols)
    # Alpaca's request vocabulary is singular while response buckets are plural.
    # Split and merger directions are separate endpoint values even though the
    # registered study treats each direction as one governed action category.
    for action_type in ("cash_dividend", "stock_dividend", "forward_split", "reverse_split",
                        "spin_off", "cash_merger", "stock_merger"):
        for batch_index in range(0, len(symbols), 10):
            batch = symbols[batch_index:batch_index + 10]
            token: str | None = None
            page = 0
            while True:
                params = {"symbols": ",".join(batch), "types": action_type,
                          "start": START, "end": END, "limit": "1000"}
                if token:
                    params["page_token"] = token
                url = "https://data.alpaca.markets/v1/corporate-actions?" + urllib.parse.urlencode(params, safe=",")
                dataset = f"actions:{action_type}:batch-{batch_index // 10:02d}:alpaca"
                try:
                    payload, receipt = fetch_bytes(
                        dataset_id=dataset, provider="ALPACA_CORPORATE_ACTIONS", url=url, headers=headers,
                        raw_path=RAW / "alpaca/actions" / action_type / f"batch-{batch_index // 10:02d}-page-{page:04d}.json",
                        page=page, cursor_in=token,
                    )
                except AcquisitionError as exc:
                    failures[action_type] = str(exc)
                    break
                parsed = json.loads(payload)
                grouped = parsed.get("corporate_actions") or {}
                for kind, rows in grouped.items():
                    for row in rows or []:
                        all_rows.append({"action_type": kind, **row})
                token = parsed.get("next_page_token")
                receipt["next_page_or_terminal_marker"] = token if token else "TERMINAL"
                write_json(RECEIPTS / f"actions_{action_type}_batch-{batch_index // 10:02d}.page-{page:04d}.final.json", receipt)
                all_receipts.append(receipt)
                page += 1
                if not token:
                    break
    return all_rows, all_receipts, failures


def yahoo_chart(symbol: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    start_epoch = int(datetime.fromisoformat(START).replace(tzinfo=timezone.utc).timestamp())
    end_epoch = int((datetime.fromisoformat(END).replace(tzinfo=timezone.utc) + timedelta(days=1)).timestamp())
    params = {
        "period1": str(start_epoch), "period2": str(end_epoch), "interval": "1d",
        "events": "div,splits,capitalGains", "includeAdjustedClose": "true",
    }
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol, safe='')}?{urllib.parse.urlencode(params)}"
    payload, receipt = fetch_bytes(
        dataset_id=f"stock:{symbol}:yahoo-reconciliation", provider="YAHOO_FINANCE_CHART", url=url,
        headers=None, raw_path=QUARANTINE / "yahoo" / f"{symbol}.json", page=0, cursor_in=None,
    )
    receipt["next_page_or_terminal_marker"] = "TERMINAL"
    write_json(RECEIPTS / f"stock_{symbol}_yahoo-reconciliation.page-0000.final.json", receipt)
    return json.loads(payload), [receipt]


def alpaca_crypto(symbol: str, headers: dict[str, str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    pair = f"{symbol}/USD"
    bars: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    token: str | None = None
    page = 0
    while True:
        params = {
            "symbols": pair, "timeframe": "1Day", "limit": "10000",
            "start": START, "end": f"{END}T23:59:59Z",
        }
        if token:
            params["page_token"] = token
        url = "https://data.alpaca.markets/v1beta3/crypto/us/bars?" + urllib.parse.urlencode(params)
        payload, receipt = fetch_bytes(
            dataset_id=f"crypto:{symbol}:alpaca", provider="ALPACA_CRYPTO", url=url,
            headers=headers, raw_path=RAW / "alpaca/crypto" / symbol / f"page-{page:04d}.json",
            page=page, cursor_in=token,
        )
        parsed = json.loads(payload)
        bars.extend((parsed.get("bars") or {}).get(pair) or [])
        token = parsed.get("next_page_token")
        receipt["next_page_or_terminal_marker"] = token if token else "TERMINAL"
        write_json(RECEIPTS / f"crypto_{symbol}_alpaca.page-{page:04d}.final.json", receipt)
        receipts.append(receipt)
        page += 1
        if not token:
            break
    return bars, receipts


def coinbase_crypto(symbol: str) -> tuple[list[list[Any]], list[dict[str, Any]]]:
    rows: list[list[Any]] = []
    receipts: list[dict[str, Any]] = []
    cursor = date.fromisoformat(START)
    finish = date.fromisoformat(END)
    page = 0
    while cursor <= finish:
        chunk_end = min(cursor + timedelta(days=249), finish)
        params = {
            "granularity": "86400",
            "start": datetime.combine(cursor, datetime.min.time(), tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
            "end": datetime.combine(chunk_end + timedelta(days=1), datetime.min.time(), tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        url = f"https://api.exchange.coinbase.com/products/{symbol}-USD/candles?{urllib.parse.urlencode(params)}"
        payload, receipt = fetch_bytes(
            dataset_id=f"crypto:{symbol}:coinbase", provider="COINBASE_EXCHANGE", url=url,
            headers=None, raw_path=QUARANTINE / "coinbase" / symbol / f"page-{page:04d}.json",
            page=page, cursor_in=cursor.isoformat(),
        )
        parsed = json.loads(payload)
        if type(parsed) is not list:
            raise AcquisitionError(f"Coinbase {symbol} page {page}: list required")
        rows.extend(parsed)
        receipt["next_page_or_terminal_marker"] = "TERMINAL" if chunk_end == finish else (chunk_end + timedelta(days=1)).isoformat()
        write_json(RECEIPTS / f"crypto_{symbol}_coinbase.page-{page:04d}.final.json", receipt)
        receipts.append(receipt)
        page += 1
        cursor = chunk_end + timedelta(days=1)
        time.sleep(0.05)
    return rows, receipts


def acquire_fred() -> tuple[bytes, list[dict[str, Any]]]:
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DFF"
    payload, receipt = fetch_bytes(
        dataset_id="comparator:DFF:FRED", provider="FRED", url=url, headers=None,
        raw_path=RAW / "fred" / "DFF.csv", page=0, cursor_in=None,
    )
    receipt["next_page_or_terminal_marker"] = "TERMINAL"
    write_json(RECEIPTS / "comparator_DFF_FRED.page-0000.final.json", receipt)
    return payload, [receipt]


def acquire_identity_pages() -> list[dict[str, Any]]:
    lineage = load_yaml(DATA / "identity_lineage.yaml")
    receipts: list[dict[str, Any]] = []
    for record in lineage["records"]:
        for index, url in enumerate(record["primary_evidence"]):
            instrument = record["instrument"]
            try:
                _, receipt = fetch_bytes(
                    dataset_id=f"identity:{instrument}:primary-{index}", provider="SEC_EDGAR_OR_PRIMARY_ISSUER",
                    url=url, headers=None,
                    raw_path=QUARANTINE / "identity" / instrument / f"primary-{index}.html",
                    page=index, cursor_in=None, retries=2,
                )
                receipt["next_page_or_terminal_marker"] = "TERMINAL"
                write_json(RECEIPTS / f"identity_{instrument}_primary-{index}.final.json", receipt)
                receipts.append(receipt)
            except AcquisitionError:
                # Failure receipts already exist. Classification occurs at the data gate.
                continue
    return receipts


def _finite_number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def normalize_alpaca_bars(symbol: str, bars: list[dict[str, Any]], provider: str) -> dict[str, Any]:
    rows = []
    for bar in bars:
        row = {
            "date": str(bar["t"])[:10],
            "open": _finite_number(bar.get("o")), "high": _finite_number(bar.get("h")),
            "low": _finite_number(bar.get("l")), "close": _finite_number(bar.get("c")),
            "volume": _finite_number(bar.get("v")),
        }
        rows.append(row)
    rows.sort(key=lambda item: item["date"])
    return {"schema_version": "1.0", "instrument": symbol, "provider": provider,
            "adjustment": "SPLIT_ADJUSTED_NON_TOTAL_RETURN", "rows": rows, "events": []}


def normalize_yahoo(symbol: str, payload: dict[str, Any]) -> dict[str, Any]:
    result = ((payload.get("chart") or {}).get("result") or [None])[0]
    if type(result) is not dict:
        raise AcquisitionError(f"Yahoo {symbol}: chart result missing")
    timestamps = result.get("timestamp") or []
    quote = (((result.get("indicators") or {}).get("quote") or [{}])[0])
    rows = []
    for index, stamp in enumerate(timestamps):
        values = {key: (quote.get(key) or [None] * len(timestamps))[index] for key in ("open", "high", "low", "close", "volume")}
        if values["close"] is None:
            continue
        rows.append({"date": datetime.fromtimestamp(int(stamp), tz=timezone.utc).date().isoformat(),
                     **{key: _finite_number(value) for key, value in values.items()}})
    events: list[dict[str, Any]] = []
    raw_events = result.get("events") or {}
    for event_type, group in raw_events.items():
        for event in (group or {}).values():
            event_date = datetime.fromtimestamp(int(event["date"]), tz=timezone.utc).date().isoformat()
            if event_type == "dividends":
                events.append({"action_type": "cash_dividend", "symbol": symbol,
                               "ex_date": event_date, "rate": _finite_number(event.get("amount")),
                               "source": "YAHOO_FINANCE_CHART_FALLBACK"})
            elif event_type == "splits":
                numerator = event.get("numerator")
                denominator = event.get("denominator")
                events.append({"action_type": "split", "symbol": symbol, "ex_date": event_date,
                               "new_rate": _finite_number(numerator), "old_rate": _finite_number(denominator),
                               "source": "YAHOO_FINANCE_CHART_FALLBACK"})
    rows.sort(key=lambda item: item["date"])
    events.sort(key=lambda item: (item["ex_date"], item["action_type"]))
    return {"schema_version": "1.0", "instrument": symbol, "provider": "YAHOO_FINANCE_CHART",
            "adjustment": "SPLIT_ADJUSTED_NON_TOTAL_RETURN_CLOSE_PLUS_EXPLICIT_EVENTS",
            "rows": rows, "events": events}


def normalize_coinbase(symbol: str, rows: list[list[Any]]) -> dict[str, Any]:
    normalized = []
    for row in rows:
        if type(row) is not list or len(row) != 6:
            raise AcquisitionError(f"Coinbase {symbol}: six-field candle required")
        stamp, low, high, open_, close, volume = row
        date = datetime.fromtimestamp(int(stamp), tz=timezone.utc).date().isoformat()
        if START <= date <= END:
            normalized.append({"date": date, "open": _finite_number(open_),
                               "high": _finite_number(high), "low": _finite_number(low),
                               "close": _finite_number(close), "volume": _finite_number(volume)})
    unique = {row["date"]: row for row in normalized}
    return {"schema_version": "1.0", "instrument": symbol, "provider": "COINBASE_EXCHANGE",
            "adjustment": "SPOT", "rows": [unique[key] for key in sorted(unique)], "events": []}


def normalize_actions(rows: list[dict[str, Any]]) -> dict[str, Any]:
    normalized = []
    category = {
        "cash_dividends": "cash_dividend",
        "stock_dividends": "stock_dividend",
        "forward_splits": "split",
        "reverse_splits": "split",
        "spin_offs": "spin_off",
        "cash_mergers": "cash_merger",
        "stock_mergers": "stock_merger",
    }
    for row in rows:
        record = dict(row)
        record["provider_action_type"] = record.get("action_type")
        record["action_type"] = category.get(str(record.get("action_type")), record.get("action_type"))
        for key in ("rate", "new_rate", "old_rate", "cash", "quantity"):
            if key in record:
                record[key] = _finite_number(record[key])
        normalized.append(record)
    normalized.sort(key=lambda item: (str(item.get("symbol", "")), str(item.get("ex_date", item.get("process_date", ""))), str(item.get("action_type", "")), str(item.get("id", ""))))
    return {"schema_version": "1.0", "provider": "ALPACA_CORPORATE_ACTIONS", "rows": normalized}


def normalize_dff(payload: bytes) -> dict[str, Any]:
    reader = csv.DictReader(io.StringIO(payload.decode("utf-8-sig")))
    rows = []
    for row in reader:
        raw_date = row.get("DATE") or row.get("observation_date")
        raw_rate = row.get("DFF")
        if not raw_date or raw_rate in (None, "", "."):
            continue
        parsed_date = date.fromisoformat(raw_date).isoformat()
        if parsed_date <= END:
            rows.append({"date": parsed_date, "rate_pct": str(raw_rate)})
    rows.sort(key=lambda item: item["date"])
    return {"schema_version": "1.0", "series": "DFF", "provider": "FRED", "rows": rows}


def session_dates(start: str = START, end: str = END) -> list[str]:
    calendar = xcals.get_calendar("XNYS", start=START, end=END)
    return [stamp.date().isoformat() for stamp in calendar.sessions_in_range(start, end)]


def gap_inventory(rows: list[dict[str, Any]], expected: list[str]) -> list[dict[str, Any]]:
    observed = {row["date"] for row in rows}
    missing = [value for value in expected if value not in observed]
    blocks: list[dict[str, Any]] = []
    if not missing:
        return blocks
    block_start = previous = missing[0]
    count = 1
    for value in missing[1:]:
        if date.fromisoformat(value) == date.fromisoformat(previous) + timedelta(days=1):
            previous = value
            count += 1
            continue
        blocks.append({"start": block_start, "end": previous, "count": count})
        block_start = previous = value
        count = 1
    blocks.append({"start": block_start, "end": previous, "count": count})
    return blocks


def bar_quality(document: dict[str, Any], *, crypto: bool, lawful_inception: str | None = None) -> dict[str, Any]:
    rows = document["rows"]
    dates = [row["date"] for row in rows]
    duplicates = len(dates) - len(set(dates))
    invalid = 0
    for row in rows:
        o, h, l, c = (row[key] for key in ("open", "high", "low", "close"))
        if any(value is None or value <= 0 for value in (o, h, l, c)) or l > min(o, c) or h < max(o, c) or h < l:
            invalid += 1
    first = dates[0] if dates else None
    last = dates[-1] if dates else None
    start = max(filter(None, [first, lawful_inception])) if first else lawful_inception
    if not start or not last:
        expected: list[str] = []
    elif crypto:
        expected = [(date.fromisoformat(start) + timedelta(days=i)).isoformat()
                    for i in range((date.fromisoformat(last) - date.fromisoformat(start)).days + 1)]
    else:
        expected = [value for value in session_dates(start, last)]
    gaps = gap_inventory(rows, expected)
    return {"first_observation": first, "last_observation": last, "row_count": len(rows),
            "expected_row_count": len(expected), "duplicates": duplicates, "invalid_ohlc": invalid,
            "gap_blocks": gaps, "missing_count": sum(block["count"] for block in gaps)}


def actions_for_symbol(actions: dict[str, Any], symbol: str) -> list[dict[str, Any]]:
    return [row for row in actions["rows"] if row.get("symbol") == symbol]


def action_signature(events: list[dict[str, Any]]) -> set[tuple[str, str]]:
    return {(str(event.get("action_type")), str(event.get("ex_date"))) for event in events
            if event.get("action_type") in ("cash_dividend", "split") and event.get("ex_date")}


def acquisition_main(env_file: Path) -> None:
    config = load_yaml(CONFIG_PATH)
    prereg = load_yaml(PREREG_PATH)
    if config["study_id"] != prereg["study_id"]:
        raise AcquisitionError("implementation/preregistration study identity mismatch")
    headers = load_credentials(env_file)
    stock_symbols, crypto_symbols = representations(prereg)
    for directory in (RAW, TRANSFORMED, QUARANTINE, RECEIPTS):
        directory.mkdir(parents=True, exist_ok=True)

    try:
        action_rows, action_receipts, action_failures = alpaca_actions(stock_symbols, headers)
        action_doc = normalize_actions(action_rows)
        write_json(TRANSFORMED / "actions/alpaca_actions.json", action_doc)
        critical_action_failures = {key: value for key, value in action_failures.items()
                                    if key in ("cash_dividend", "forward_split", "reverse_split")}
        action_failure = None if not critical_action_failures else json.dumps(critical_action_failures, sort_keys=True)
    except AcquisitionError as exc:
        action_receipts = []
        action_failures = {"GLOBAL": str(exc)}
        action_doc = {"schema_version": "1.0", "provider": "ALPACA_CORPORATE_ACTIONS", "rows": []}
        action_failure = str(exc)

    stock_inventory = []
    boundaries = config["identity_boundaries"]
    for symbol in stock_symbols:
        primary_error = None
        fallback_error = None
        primary_doc = None
        fallback_doc = None
        primary_receipts: list[dict[str, Any]] = []
        fallback_receipts: list[dict[str, Any]] = []
        try:
            bars, primary_receipts = alpaca_stock(symbol, headers)
            primary_doc = normalize_alpaca_bars(symbol, bars, "ALPACA_MARKET_DATA")
            primary_doc["events"] = actions_for_symbol(action_doc, symbol)
            write_json(TRANSFORMED / "candidates/alpaca" / f"{symbol}.json", primary_doc)
        except AcquisitionError as exc:
            primary_error = str(exc)
        try:
            yahoo_payload, fallback_receipts = yahoo_chart(symbol)
            fallback_doc = normalize_yahoo(symbol, yahoo_payload)
            write_json(QUARANTINE / "transformed/yahoo" / f"{symbol}.json", fallback_doc)
        except AcquisitionError as exc:
            fallback_error = str(exc)

        inception = (boundaries.get(symbol) or {}).get("lawful_inception")
        primary_quality = bar_quality(primary_doc, crypto=False, lawful_inception=inception) if primary_doc else None
        fallback_quality = bar_quality(fallback_doc, crypto=False, lawful_inception=inception) if fallback_doc else None
        lawful_inception = inception or ((fallback_quality or primary_quality or {}).get("first_observation"))
        primary_complete = bool(primary_quality and not primary_quality["duplicates"]
                                and not primary_quality["invalid_ohlc"]
                                and not primary_quality["missing_count"]
                                and primary_quality["first_observation"] <= lawful_inception)
        # Known gaps are a Stage-B cell limitation, not a reason to discard an
        # otherwise lawful whole-path fallback and erase unaffected windows.
        fallback_usable = bool(fallback_quality and not fallback_quality["duplicates"]
                               and not fallback_quality["invalid_ohlc"])
        action_mismatch = True
        if primary_doc and fallback_doc and action_failure is None:
            action_mismatch = action_signature(primary_doc["events"]) != action_signature(fallback_doc["events"])
        if primary_complete and not action_mismatch:
            selected_provider = "ALPACA_MARKET_DATA"
            selected_doc = primary_doc
            selected_path = TRANSFORMED / "selected" / f"{symbol}.json"
            disposition = "COMMITTED"
        elif fallback_usable:
            selected_provider = "YAHOO_FINANCE_CHART"
            selected_doc = fallback_doc
            selected_path = QUARANTINE / "selected" / f"{symbol}.json"
            disposition = "QUARANTINED_HASH_PINNED"
        else:
            selected_provider = None
            selected_doc = fallback_doc or primary_doc
            selected_path = None
            disposition = "UNAVAILABLE"
        if selected_path and selected_doc:
            write_json(selected_path, selected_doc)
        stock_inventory.append({
            "instrument": symbol, "study_role": "EQUITY_OR_ETF_TOTAL_RETURN_INPUT",
            "primary_provider": "ALPACA_MARKET_DATA", "fallback_provider": "YAHOO_FINANCE_CHART",
            "selected_provider": selected_provider, "whole_path_only": True,
            "lawful_inception": lawful_inception,
            "primary_error": primary_error, "fallback_error": fallback_error,
            "action_acquisition_error": action_failure, "action_reconciliation_mismatch": action_mismatch,
            "primary_quality": primary_quality, "fallback_quality": fallback_quality,
            "selected_path": str(selected_path.relative_to(ROOT)) if selected_path else None,
            "selected_transformed_sha256": sha256_file(selected_path) if selected_path else None,
            "commit_or_quarantine_disposition": disposition,
            "receipt_count": len(primary_receipts) + len(fallback_receipts),
        })

    crypto_inventory = []
    for symbol in crypto_symbols:
        primary_error = None
        fallback_error = None
        primary_doc = None
        fallback_doc = None
        primary_receipts: list[dict[str, Any]] = []
        fallback_receipts: list[dict[str, Any]] = []
        try:
            bars, primary_receipts = alpaca_crypto(symbol, headers)
            primary_doc = normalize_alpaca_bars(symbol, bars, "ALPACA_CRYPTO")
            primary_doc["adjustment"] = "SPOT"
            write_json(TRANSFORMED / "candidates/alpaca_crypto" / f"{symbol}.json", primary_doc)
        except AcquisitionError as exc:
            primary_error = str(exc)
        primary_quality = bar_quality(primary_doc, crypto=True) if primary_doc else None
        primary_complete = bool(primary_quality and not primary_quality["duplicates"] and not primary_quality["invalid_ohlc"] and not primary_quality["missing_count"])
        if not primary_complete:
            try:
                rows, fallback_receipts = coinbase_crypto(symbol)
                fallback_doc = normalize_coinbase(symbol, rows)
                write_json(QUARANTINE / "transformed/coinbase" / f"{symbol}.json", fallback_doc)
            except AcquisitionError as exc:
                fallback_error = str(exc)
        fallback_quality = bar_quality(fallback_doc, crypto=True) if fallback_doc else None
        fallback_complete = bool(fallback_quality and not fallback_quality["duplicates"] and not fallback_quality["invalid_ohlc"] and not fallback_quality["missing_count"])
        if primary_complete:
            selected_provider = "ALPACA_CRYPTO"
            selected_doc = primary_doc
            selected_path = TRANSFORMED / "selected" / f"{symbol}.json"
            disposition = "COMMITTED"
        elif fallback_complete:
            selected_provider = "COINBASE_EXCHANGE"
            selected_doc = fallback_doc
            selected_path = QUARANTINE / "selected" / f"{symbol}.json"
            disposition = "QUARANTINED_HASH_PINNED"
        else:
            selected_provider = None
            selected_doc = fallback_doc or primary_doc
            selected_path = None
            disposition = "UNAVAILABLE"
        if selected_path and selected_doc:
            write_json(selected_path, selected_doc)
        crypto_inventory.append({
            "instrument": symbol, "study_role": "CRYPTO_SPOT_RETURN_INPUT",
            "primary_provider": "ALPACA_CRYPTO", "fallback_provider": "COINBASE_EXCHANGE",
            "selected_provider": selected_provider, "whole_path_only": True,
            "lawful_inception": min(filter(None, [
                (primary_quality or {}).get("first_observation"),
                (fallback_quality or {}).get("first_observation"),
            ]), default=None),
            "primary_error": primary_error, "fallback_error": fallback_error,
            "primary_quality": primary_quality, "fallback_quality": fallback_quality,
            "selected_path": str(selected_path.relative_to(ROOT)) if selected_path else None,
            "selected_transformed_sha256": sha256_file(selected_path) if selected_path else None,
            "commit_or_quarantine_disposition": disposition,
            "receipt_count": len(primary_receipts) + len(fallback_receipts),
        })

    dff_error = None
    try:
        dff_payload, dff_receipts = acquire_fred()
        dff_doc = normalize_dff(dff_payload)
        dff_path = TRANSFORMED / "selected/DFF.json"
        write_json(dff_path, dff_doc)
        dff_record = {"instrument": "DFF", "study_role": "ANALYTICAL_OPPORTUNITY_COST_ONLY",
                      "selected_provider": "FRED", "selected_path": str(dff_path.relative_to(ROOT)),
                      "selected_transformed_sha256": sha256_file(dff_path), "row_count": len(dff_doc["rows"]),
                      "first_observation": dff_doc["rows"][0]["date"], "last_observation": dff_doc["rows"][-1]["date"],
                      "receipt_count": len(dff_receipts), "commit_or_quarantine_disposition": "COMMITTED_PUBLIC_DOMAIN"}
    except AcquisitionError as exc:
        dff_error = str(exc)
        dff_record = {"instrument": "DFF", "study_role": "ANALYTICAL_OPPORTUNITY_COST_ONLY",
                      "selected_provider": None, "selected_path": None, "selected_transformed_sha256": None,
                      "row_count": 0, "first_observation": None, "last_observation": None,
                      "receipt_count": 0, "commit_or_quarantine_disposition": "UNAVAILABLE", "error": dff_error}

    identity_receipts = acquire_identity_pages()
    source_inventory = {
        "schema_version": "1.0", "study_id": "RISK-0001", "acquisition_completed_at_utc": utc_now(),
        "implementation_config_sha256": sha256_file(CONFIG_PATH),
        "protocol_sha256": config["authority"]["protocol_sha256"],
        "preregistration_sha256": config["authority"]["preregistration_sha256"],
        "stock_and_etf_datasets": stock_inventory, "crypto_datasets": crypto_inventory,
        "comparator_dataset": dff_record,
        "corporate_actions": {"selected_provider": None if action_failure else "ALPACA_CORPORATE_ACTIONS",
                              "error": action_failure, "type_failures": action_failures, "row_count": len(action_doc["rows"]),
                              "receipt_count": len(action_receipts),
                              "transformed_path": "research/level1_sleeve_robustness/data/transformed/actions/alpaca_actions.json" if not action_failure else None,
                              "transformed_sha256": sha256_file(TRANSFORMED / "actions/alpaca_actions.json") if not action_failure else None},
        "identity_evidence": {"receipt_count": len(identity_receipts), "registry_path": "research/level1_sleeve_robustness/data/identity_lineage.yaml",
                              "registry_sha256": sha256_file(DATA / "identity_lineage.yaml")},
        "no_registered_results_executed": True,
    }
    write_json(DATA / "source_inventory.json", source_inventory)
    print(f"RISK-0001 acquisition complete: stocks_etfs={len(stock_inventory)} crypto={len(crypto_inventory)} DFF={'ok' if not dff_error else 'unavailable'}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path, required=True)
    args = parser.parse_args()
    acquisition_main(args.env_file.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
