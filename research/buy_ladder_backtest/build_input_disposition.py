#!/usr/bin/env python3
"""Build LADDER-0003's deterministic, result-blind input disposition.

This program reads only retained market/action evidence.  It never evaluates a
ladder arm or a holdout return.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research/buy_ladder_backtest/inputs"
ALPACA = ROOT / "research/level1_sleeve_robustness/data/transformed/candidates/alpaca"
ACTIONS = ROOT / "research/level1_sleeve_robustness/data/transformed/actions/alpaca_actions.json"
DATA = ROOT / "research/level1_sleeve_robustness/data"
RAW = DATA / "raw"
RECEIPTS = DATA / "receipts"
RECEIPT_INVENTORY = DATA / "acquisition_receipt_inventory.json"
YAHOO = OUT / "yahoo_action_crosscheck.json"
AMENDMENT = ROOT / "research/buy_ladder_backtest/PROTOCOL_V2_FOREIGN_DIVIDEND_AMENDMENT.md"

EXPECTED_ACTIONS_SHA256 = "a75341f1279665423722074fbc3c89eed2a0c4708e8aefcd658220c3e7bc83b2"
EXPECTED_YAHOO_SHA256 = "3a2a7b7604a43bd97a485065b0e59af11e8fd65c3c487a012c0c1ad0f6496544"
EXPECTED_RECEIPT_INVENTORY_SHA256 = "260095460e120a1ab222d48846f45fd1b246a634c04d900d966db64662d31a95"
EXPECTED_RAW_AGGREGATE_SHA256 = "76b9a429d15280b9b16624e66cc80129d2a7359cb12bcc948ed126ad2c19bfb7"
EXPECTED_RECEIPT_AGGREGATE_SHA256 = "abf6f603d71f388288a4c3e691e810f683f36fbec2c5d696ef9448551a677ce7"
STUDY_START = "2021-06-01"
STUDY_END = "2026-07-31"
ACTION_AS_OF = "2026-09-07"

ROSTER = (
    "NVDA TSM ASML AVGO KLAC MSFT GOOGL AMZN META PANW LLY ISRG TMO V COST "
    "CEG ETN GEV GNRC PWR RTX SPY VEA VWO GLD"
).split()
EXPECTED_OHLC_SHA256 = {
    "NVDA": "a5d08f4d9ca7670661812d6d30507306515f36bc1f527ff87423bf2cf16cb432",
    "TSM": "4db41b4d3ab1e6cc297fbf0f8e2d04b9ec9277dccaf55177db61fe12161f4a58",
    "ASML": "40416552a8ef86bd856e78099be48bf1131d736031eeaa94615a08380577b99d",
    "AVGO": "cd2f1adffe2f2077e228532a59d1b404bd3088718c761e37dbd7b711b217fe7c",
    "KLAC": "607220358dfdeb084bf4d7e6d5efc52a6c119f74ffcb20493863641b6a7827ed",
    "MSFT": "65c30aace8c0489c3d1451f16b0cbcd5d84478a110b1733df8805901f078ab65",
    "GOOGL": "5bb60ceffc47d237a2250ea9066d049026db5e6a036129f32f7fe3a8ec3e6317",
    "AMZN": "0af12da74b84266363f1d1d3b233ef52f06765e23fca090050d63a4370f89275",
    "META": "bf71fc188ad525f06e4d4a24b161ebb028e8950fa14e5b4d20fe7170ceadf875",
    "PANW": "6b06c810bcd807a91b88e856d969f5874cc7c0af0bb2b4c701a08650d8703c2d",
    "LLY": "8e2cd1302efa2eab908f3bd87d215ddb25c6f5c89a73fb2bf3354a4b00b8d37f",
    "ISRG": "fbf51a447454e133a169617f2ee32b6b0485cbba3e63739c87ea5a06e572d1ea",
    "TMO": "7bd4d5ada8356b03fb2fb1dd37eb657a9b00c0446120edd72803f3e51cbcae22",
    "V": "35ecb25501b86e481831bba7e5994c25dcd4aeb4651be02e7f1b49d3f6fceba7",
    "COST": "107c7fe11b5c8d9da1e5b00bddb6f1bd0ecb5ca0bec430c88f07ad718f694ecb",
    "CEG": "923df00f4dcf7b45a792227dd1a680c976e8c353dcdfe8b4d4eb5a2ef29b396c",
    "ETN": "a2a03178d13f875bbb094ee20b0631ad0d64099db48d60a621ce3e791737e784",
    "GEV": "6ad467d7d54a31cdab6401976020ee7ef65ac228fe9c9a23125199347ab450db",
    "GNRC": "cf7946500528f50db12c5de38280beb4b632c09a69e97b31732aeddfa9785836",
    "PWR": "c72bf303a6ebab6cb598f29b827e9e85c129f4b6eda122a6a5d5f012fa104f48",
    "RTX": "53559234774f2902bd9753567fa7be60293417dc8e0e3ee144d3493324cf9828",
    "SPY": "f8127149dce69ba42740bebe3fc8377d916782447fde6e15ede74ec64d786edc",
    "VEA": "f138b33dc1789f3870cab7b8d74be2f601b1271b8a5416d1b53bd51bcac87b06",
    "VWO": "857a958ef7fd68b3dbaf88c0317a3b64f37ae9b9dcda9e08ba4c2a2506982c25",
    "GLD": "c7b7c33e87c655f8f53c3cb19d697692bf5a9ce2195347343c7e177122d1d56f",
}

# Exact issuer-published ADR gross and source-net amounts, 4Q20 through 4Q25.
TSM = [
    ("2021-06-17", .4456010, .3520250, "4q20"), ("2021-09-16", .491246, .388084, "1q21"),
    ("2021-12-16", .496981, .392615, "2q21"), ("2022-03-16", .475613, .375734, "3q21"),
    ("2022-06-16", .461579, .364647, "4q21"), ("2022-09-15", .434892, .343565, "1q22"),
    ("2022-12-15", .447299, .353366, "2q22"), ("2023-03-16", .451071, .356346, "3q22"),
    ("2023-06-15", .438987, .346800, "4q22"), ("2023-09-14", .465116, .367441, "1q23"),
    ("2023-12-14", .483247, .381765, "2q23"), ("2024-03-18", .545597, .431022, "3q23"),
    ("2024-06-13", .539924, .426540, "4q23"), ("2024-09-12", .624826, .493613, "1q24"),
    ("2024-12-12", .608106, .480404, "2q24"), ("2025-03-18", .6776930, .5353770, "3q24"),
    ("2025-06-12", .7803050, .6164410, "4q24"), ("2025-09-16", .8219650, .6493520, "1q25"),
    ("2025-12-11", .7954200, .6283820, "2q25"), ("2026-03-17", .9389720, .7417880, "3q25"),
    ("2026-06-11", .9393250, .7420670, "4q25"),
]
TSM_BY_DATE = {d: (g, n, q) for d, g, n, q in TSM}

ACTION_TYPES = (
    "cash_dividend", "stock_dividend", "forward_split", "reverse_split",
    "spin_off", "cash_merger", "stock_merger",
)
ACTION_CATEGORY = {
    "cash_dividends": "cash_dividend",
    "stock_dividends": "stock_dividend",
    "forward_splits": "split",
    "reverse_splits": "split",
    "spin_offs": "spin_off",
    "cash_mergers": "cash_merger",
    "stock_mergers": "stock_merger",
}


class InputIntegrityError(RuntimeError):
    """Raised when any frozen evidence or deterministic transform drifts."""


def require(condition: bool, message: str) -> None:
    """Enforce an invariant under normal and optimized Python interpreters."""
    if not condition:
        raise InputIntegrityError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def aggregate(root: Path, files: Iterable[Path]) -> tuple[str, int]:
    ordered = sorted(files, key=lambda path: path.relative_to(root).as_posix())
    rows = "".join(
        f"{sha(path)}  {path.relative_to(root).as_posix()}\n"
        for path in ordered
    )
    return hashlib.sha256(rows.encode("utf-8")).hexdigest(), len(ordered)


def encoded(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def finite_number(value: object) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def verify_receipt(
    receipt_path: Path,
    *,
    expected_dataset: str,
    inventory: dict[str, dict[str, object]],
) -> Path:
    relative_receipt = receipt_path.relative_to(ROOT).as_posix()
    require(relative_receipt in inventory, f"receipt absent from frozen inventory: {relative_receipt}")
    inventory_row = inventory[relative_receipt]
    require(sha(receipt_path) == inventory_row["receipt_sha256"], f"receipt hash drift: {relative_receipt}")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    require(receipt.get("dataset_id") == expected_dataset, f"receipt dataset drift: {relative_receipt}")
    require(receipt.get("response_status") == 200 and receipt.get("error") is None, f"receipt unsuccessful: {relative_receipt}")
    require(receipt.get("next_page_or_terminal_marker") == "TERMINAL", f"receipt pagination incomplete: {relative_receipt}")
    raw_relative = receipt.get("raw_path")
    require(isinstance(raw_relative, str) and raw_relative, f"receipt raw path missing: {relative_receipt}")
    raw_path = ROOT / raw_relative
    require(raw_path.is_file(), f"raw evidence missing: {raw_relative}")
    require(sha(raw_path) == receipt.get("raw_sha256"), f"raw evidence hash drift: {raw_relative}")
    require(raw_path.stat().st_size == receipt.get("raw_byte_count"), f"raw evidence size drift: {raw_relative}")
    return raw_path


def reconstruct_actions(inventory: dict[str, dict[str, object]]) -> tuple[dict[str, object], list[dict[str, str]]]:
    source_rows: list[dict[str, object]] = []
    provenance: list[dict[str, str]] = []
    for action_type in ACTION_TYPES:
        for batch in range(4):
            receipt_path = RECEIPTS / f"actions_{action_type}_batch-{batch:02d}.page-0000.final.json"
            raw_path = verify_receipt(
                receipt_path,
                expected_dataset=f"actions:{action_type}:batch-{batch:02d}:alpaca",
                inventory=inventory,
            )
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            require(raw.get("next_page_token") in (None, ""), f"raw action page is not terminal: {raw_path}")
            grouped = raw.get("corporate_actions") or {}
            require(isinstance(grouped, dict), f"raw action buckets malformed: {raw_path}")
            for kind, rows in grouped.items():
                require(kind in ACTION_CATEGORY, f"unknown action bucket {kind}: {raw_path}")
                require(isinstance(rows, list), f"action bucket is not a list: {raw_path}")
                source_rows.extend({"action_type": kind, **row} for row in rows)
            provenance.append({
                "raw_path": raw_path.relative_to(ROOT).as_posix(),
                "raw_sha256": sha(raw_path),
                "receipt_path": receipt_path.relative_to(ROOT).as_posix(),
                "receipt_sha256": sha(receipt_path),
            })

    normalized = []
    for source in source_rows:
        record = dict(source)
        record["provider_action_type"] = record.get("action_type")
        record["action_type"] = ACTION_CATEGORY.get(str(record.get("action_type")), record.get("action_type"))
        for key in ("rate", "new_rate", "old_rate", "cash", "quantity"):
            if key in record:
                record[key] = finite_number(record[key])
        normalized.append(record)
    normalized.sort(key=lambda item: (
        str(item.get("symbol", "")),
        str(item.get("ex_date", item.get("process_date", ""))),
        str(item.get("action_type", "")),
        str(item.get("id", "")),
    ))
    document: dict[str, object] = {
        "schema_version": "1.0",
        "provider": "ALPACA_CORPORATE_ACTIONS",
        "rows": normalized,
    }
    require(encoded(document) == ACTIONS.read_bytes(), "action transform does not reconstruct from frozen raw evidence")
    return document, provenance


def reconstruct_price(
    ticker: str,
    action_rows: list[dict[str, object]],
    inventory: dict[str, dict[str, object]],
) -> tuple[dict[str, object], dict[str, str]]:
    receipt_path = RECEIPTS / f"stock_{ticker}_alpaca.page-0000.final.json"
    raw_path = verify_receipt(
        receipt_path,
        expected_dataset=f"stock:{ticker}:alpaca",
        inventory=inventory,
    )
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    require(raw.get("symbol") == ticker, f"raw price symbol drift: {raw_path}")
    require(raw.get("next_page_token") in (None, ""), f"raw price page is not terminal: {raw_path}")
    bars = raw.get("bars")
    require(isinstance(bars, list) and bars, f"raw price bars missing: {raw_path}")
    rows = [{
        "date": str(bar["t"])[:10],
        "open": finite_number(bar.get("o")),
        "high": finite_number(bar.get("h")),
        "low": finite_number(bar.get("l")),
        "close": finite_number(bar.get("c")),
        "volume": finite_number(bar.get("v")),
    } for bar in bars]
    rows.sort(key=lambda item: item["date"])
    document: dict[str, object] = {
        "schema_version": "1.0",
        "instrument": ticker,
        "provider": "ALPACA_MARKET_DATA",
        "adjustment": "SPLIT_ADJUSTED_NON_TOTAL_RETURN",
        "rows": rows,
        "events": [row for row in action_rows if row.get("symbol") == ticker],
    }
    transformed = ALPACA / f"{ticker}.json"
    require(encoded(document) == transformed.read_bytes(), f"{ticker} transform does not reconstruct from frozen raw evidence")
    return document, {
        "raw_path": raw_path.relative_to(ROOT).as_posix(),
        "raw_sha256": sha(raw_path),
        "receipt_path": receipt_path.relative_to(ROOT).as_posix(),
        "receipt_sha256": sha(receipt_path),
    }


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")


def is_in_entitlement_window(event: dict[str, object]) -> bool:
    """Select actions by ex-date entitlement, never provider process date."""
    ex_date = str(event.get("ex_date") or "")
    return STUDY_START <= ex_date <= STUDY_END


def etn_dividend_terms(provider_rate: float, provider_amount_basis: str) -> dict[str, object]:
    """Normalize ETN quotes, then apply one study-wide withholding convention."""
    require(provider_rate > 0, "ETN provider rate must be positive")
    require(
        provider_amount_basis in {"GROSS", "SOURCE_NET_AT_25_PERCENT"},
        "unsupported ETN provider amount basis",
    )
    gross = provider_rate if provider_amount_basis == "GROSS" else provider_rate / 0.75
    return {
        "provider_reported_rate_usd": round(provider_rate, 9),
        "provider_amount_basis": provider_amount_basis,
        "gross_rate_usd": round(gross, 9),
        "source_net_rate_usd": round(gross, 9),
        "source_withholding_usd": 0.0,
        "withholding_convention": "US_BROKER_DOCUMENTED_EXEMPTION_RESEARCH_ASSUMPTION",
        "withholding_sensitivity": {
            "case": "NO_EXEMPTION_25_PERCENT_IRISH_DWT",
            "source_net_rate_usd": round(gross * 0.75, 9),
            "source_withholding_usd": round(gross * 0.25, 9),
        },
    }


def main() -> None:
    require(sha(ACTIONS) == EXPECTED_ACTIONS_SHA256, "upstream action transform hash drift")
    require(sha(YAHOO) == EXPECTED_YAHOO_SHA256, "Yahoo cross-check hash drift")
    require(
        sha(RECEIPT_INVENTORY) == EXPECTED_RECEIPT_INVENTORY_SHA256,
        "acquisition receipt inventory hash drift",
    )
    raw_aggregate, raw_count = aggregate(ROOT, (path for path in RAW.rglob("*") if path.is_file()))
    receipt_aggregate, receipt_count = aggregate(
        ROOT,
        (path for path in RECEIPTS.rglob("*") if path.is_file()),
    )
    require(
        (raw_count, raw_aggregate) == (66, EXPECTED_RAW_AGGREGATE_SHA256),
        "frozen raw-evidence aggregate drift",
    )
    require(
        (receipt_count, receipt_aggregate) == (963, EXPECTED_RECEIPT_AGGREGATE_SHA256),
        "frozen acquisition-receipt aggregate drift",
    )
    receipt_inventory_payload = json.loads(RECEIPT_INVENTORY.read_text(encoding="utf-8"))
    receipt_records = receipt_inventory_payload.get("records")
    require(isinstance(receipt_records, list), "acquisition receipt inventory records malformed")
    receipt_inventory = {
        str(record["receipt_path"]): record for record in receipt_records
        if isinstance(record, dict) and isinstance(record.get("receipt_path"), str)
    }
    require(
        len(receipt_inventory) == receipt_inventory_payload.get("receipt_count") == 963,
        "acquisition receipt inventory count or uniqueness drift",
    )
    reconstructed_actions, action_raw_provenance = reconstruct_actions(receipt_inventory)
    action_rows = reconstructed_actions["rows"]
    require(isinstance(action_rows, list), "reconstructed action rows malformed")

    price_files = []
    for ticker in ROSTER:
        path = ALPACA / f"{ticker}.json"
        require(sha(path) == EXPECTED_OHLC_SHA256[ticker], f"{ticker} transformed OHLC hash drift")
        payload, provenance = reconstruct_price(ticker, action_rows, receipt_inventory)
        rows = payload["rows"]
        price_files.append({
            "ticker": ticker,
            "path": str(path.relative_to(ROOT)),
            "sha256": EXPECTED_OHLC_SHA256[ticker],
            "provider": "ALPACA_MARKET_DATA_SIP",
            "adjustment": "split",
            "total_row_count": len(rows),
            "first_observation": rows[0]["date"],
            "last_observation": rows[-1]["date"],
            "admitted_start": max(STUDY_START, rows[0]["date"]),
            "identity_floor": "2020-04-03" if ticker == "RTX" else None,
            "raw_provenance": provenance,
        })

    raw = action_rows
    events = []
    quarantined = []
    for source in raw:
        if source.get("symbol") not in ROSTER or not is_in_entitlement_window(source):
            continue
        if source["symbol"] == "ASML" and source.get("cusip") == "G3730V147":
            quarantined.append({
                "source_id": source["id"], "symbol_label": "ASML", "cusip": "G3730V147",
                "disposition": "EXCLUDE_CROSS_SECURITY_CONTAMINATION",
                "identified_security": "FTAI Aviation Series D preferred",
                "issuer_source": "https://ir.ftaiaviation.com/news-releases/news-release-details/ftai-aviation-ltd-reports-third-quarter-2024-results-declares",
                "identity_source": "https://www.sec.gov/Archives/edgar/data/1058022/000105802224000005/xslForm13F_X02/shikiar3q13f2024.xml",
            })
            continue
        event = dict(source)
        event["source_lineage"] = ["retained_alpaca_action_registry"]
        if event["action_type"] == "cash_dividend":
            paid = float(event.pop("rate"))
            gross = paid
            if event["symbol"] == "TSM":
                gross, official_paid, quarter = TSM_BY_DATE[event["ex_date"]]
                require(abs(paid - official_paid) < 1e-12, f"TSM source-net rate drift: {event['ex_date']}")
                event["source_lineage"].append(f"https://investor.tsmc.com/english/dividends/{quarter}")
                event["rate_evidence"] = "ISSUER_EXACT_GROSS_AND_SOURCE_NET"
            elif event["symbol"] == "ASML":
                gross = paid / 0.85
                event["gross_rate_derivation"] = "source_net_rate / 0.85 Dutch statutory withholding assumption"
                event["rate_evidence"] = "PROVIDER_SOURCE_NET_PLUS_WITHHOLDING_ASSUMPTION"
            elif event["symbol"] == "ETN":
                provider_basis = (
                    "SOURCE_NET_AT_25_PERCENT" if event["ex_date"] >= "2023-05-05" else "GROSS"
                )
                terms = etn_dividend_terms(paid, provider_basis)
                gross = float(terms["gross_rate_usd"])
                event.update(terms)
                event["gross_rate_derivation"] = (
                    "provider gross quote" if provider_basis == "GROSS"
                    else "provider source-net quote / 0.75 observed reporting basis"
                )
                event["rate_evidence"] = "PROVIDER_BASIS_NORMALIZED_PLUS_CONSTANT_MODEL_CONVENTION"
                event["source_lineage"].append(
                    "https://www.eaton.com/us/en-us/company/investor-relations/Irish-Dividend-Withholding-Tax.html"
                )
                if event["ex_date"] == "2025-11-06":
                    event["source_lineage"].append(
                        "https://www.eaton.com/us/en-us/company/news-insights/news-releases/2025/"
                        "eaton-declares-quarterly-dividend-payable-november-21--2025.html"
                    )
            else:
                event["rate_evidence"] = "RETAINED_PROVIDER_RATE_TREATED_AS_GROSS"
            if event["symbol"] != "ETN":
                event.update({
                    "gross_rate_usd": round(gross, 9),
                    "source_net_rate_usd": round(paid, 9),
                    "source_withholding_usd": round(gross - paid, 9),
                })
            event["same_day_split_basis"] = "NOT_APPLICABLE"
        else:
            event["same_day_dividend_basis"] = "NOT_APPLICABLE"
        events.append(event)

    # Two provider omissions confirmed by issuer primary sources.  Both payable
    # dates fall after the market-data end and therefore remain receivables.
    events.extend([
        {
            "action_type": "cash_dividend", "symbol": "COST", "cusip": "22160K105",
            "ex_date": "2026-07-24", "record_date": "2026-07-24", "payable_date": "2026-08-07",
            "gross_rate_usd": 1.47, "source_net_rate_usd": 1.47, "source_withholding_usd": 0.0,
            "same_day_split_basis": "NOT_APPLICABLE", "id": "ladder-0003-cost-2026-07-24",
            "rate_evidence": "ISSUER_EXACT_GROSS_PLUS_NASDAQ_T1_EX_DATE_INFERENCE",
            "ex_date_evidence": "RULE_BASED_INFERENCE_RECORD_DATE_EQUALS_REGULAR_EX_DATE_UNDER_NASDAQ_T1",
            "source_lineage": [
                "https://investor.costco.com/news/news-details/2026/Costco-Wholesale-Corporation-Reports-June-Sales-Results-and-Announces-Quarterly-Cash-Dividend/default.aspx",
                "https://www.nasdaqtrader.com/TraderNews.aspx?id=ETA2024-29",
                "https://listingcenter.nasdaq.com/assets/RuleBook/Nasdaq/rules/Issuer_Alert_2024-001.pdf",
            ],
        },
        {
            "action_type": "cash_dividend", "symbol": "ASML", "cusip": "N07059210",
            "ex_date": "2026-07-28", "record_date": "2026-07-28", "payable_date": "2026-08-05",
            "gross_rate_usd": 2.137748, "source_net_rate_usd": 1.8170858,
            "source_withholding_usd": 0.3206622, "same_day_split_basis": "NOT_APPLICABLE",
            "id": "ladder-0003-asml-2026-07-28",
            "rate_evidence": "ISSUER_EXACT_GROSS_PLUS_WITHHOLDING_ASSUMPTION",
            "gross_rate_derivation": "EUR 1.88 * issuer-fixed EUR/USD 1.1371; source net assumes 15% Dutch withholding",
            "source_lineage": ["https://www.asml.com/en/investors/why-invest-in-asml/capital-return-and-financing"],
        },
    ])
    events.sort(key=lambda x: (x["ex_date"], x["symbol"], x["action_type"], x["id"]))
    require(len(events) == 381, "selected action count drift")
    require(len(quarantined) == 1, "quarantined action count drift")
    require(
        len({(x["symbol"], x["action_type"], x["ex_date"]) for x in events}) == len(events),
        "selected action identities are not unique",
    )

    action_payload = {
        "schema_version": "1.0", "decision_id": "LADDER-0003",
        "window": {"start": STUDY_START, "end": STUDY_END},
        "action_as_of": ACTION_AS_OF,
        "selection_basis": "ex_date entitlement within window; process/payable dates may follow window end",
        "tax_semantics": "PROTOCOL_V2_FOREIGN_DIVIDEND_AMENDMENT",
        "events": events, "quarantined_events": quarantined,
    }
    action_path = OUT / "corporate_actions.json"
    dump(action_path, action_payload)

    yahoo = json.loads(YAHOO.read_text())
    require(set(yahoo["symbols"]) == set(ROSTER), "Yahoo cross-check roster drift")
    crosscheck = {
        "snapshot_path": str(YAHOO.relative_to(ROOT)), "snapshot_sha256": sha(YAHOO),
        "scope": "secondary completeness cross-check only; not a canonical rate source",
        "result": "22 symbols have identical type/ex-date signatures; three require primary-source disposition",
        "exceptions": [
            {"symbol": "ASML", "issue": "Yahoo adds 2026-07-28; Alpaca adds false 2024-12-02", "resolution": "add issuer event; quarantine CUSIP G3730V147"},
            {"symbol": "COST", "issue": "Yahoo date 2026-07-24; Alpaca omits event", "resolution": "issuer record 2026-07-24 plus Nasdaq T+1 regular-distribution rule support same-day ex-date"},
            {"symbol": "ETN", "issue": "Yahoo says 2025-11-05; Alpaca says 2025-11-06", "resolution": "issuer record date and exchange corroboration support 2025-11-06"},
        ],
    }
    disposition = {
        "schema_version": "1.0", "decision_id": "LADDER-0003",
        "status": "ACCEPTED_FOR_LADDER_IMPLEMENTATION_AFTER_MERGE",
        "result_blind": True, "ladder_result_inspected": False,
        "study_window": {"start": STUDY_START, "end": STUDY_END},
        "action_as_of": ACTION_AS_OF,
        "action_coverage_rule": (
            "Select by in-window ex-date through 2026-07-31 from an event-completeness "
            "cross-check captured 2026-09-07; preserve later payable dates as receivables."
        ),
        "tax_amendment": {
            "path": str(AMENDMENT.relative_to(ROOT)),
            "sha256": sha(AMENDMENT),
        },
        "price_selection_rule": "uniform retained Alpaca SIP split-adjusted non-total-return OHLC; selected before any ladder result",
        "price_files": price_files,
        "corporate_actions": {"path": str(action_path.relative_to(ROOT)), "sha256": sha(action_path), "event_count": len(events)},
        "upstream_action_registry": {
            "path": str(ACTIONS.relative_to(ROOT)),
            "sha256": EXPECTED_ACTIONS_SHA256,
            "reconstructed_from_raw": True,
            "raw_provenance": action_raw_provenance,
        },
        "frozen_source_evidence": {
            "receipt_inventory_path": str(RECEIPT_INVENTORY.relative_to(ROOT)),
            "receipt_inventory_sha256": EXPECTED_RECEIPT_INVENTORY_SHA256,
            "raw_file_count": raw_count,
            "raw_aggregate_sha256": raw_aggregate,
            "receipt_file_count": receipt_count,
            "receipt_aggregate_sha256": receipt_aggregate,
            "transform_reconstruction": "EXACT_BYTE_IDENTITY_VERIFIED",
        },
        "action_crosscheck": crosscheck,
        "rtx_identity": {"lawful_start": "2020-04-03", "admitted_study_start": "2021-06-01", "predecessor_stitching": "PROHIBITED"},
        "sol_disposition": {
            "ladder_scope": "EXCLUDED_BY_LADDER-0002",
            "prior_robustness_status": "EVIDENCE_LIMITED_NOT_DECISION_GRADE",
            "successor_rule": "No pre-2021-06-17 SOLUSD history may be inferred or stitched; a successor must use a separately accepted exact source or abstain.",
        },
        "old_robustness_artifacts": "PRESERVED_UNCHANGED_AND_PROHIBITED_AS_DECISION_GRADE_EVIDENCE",
    }
    dump(OUT / "input_disposition.json", disposition)


if __name__ == "__main__":
    main()
