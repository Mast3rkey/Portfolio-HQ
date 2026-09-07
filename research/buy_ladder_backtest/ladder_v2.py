"""Deterministic, network-free runner for the one LADDER V2 registered run.

``validate`` binds and checks every frozen input without calculating any holdout
result. ``execute`` requires that exact receipt and writes the complete registered
result atomically. This module is advisory research only and has no account,
brokerage, order, margin, or Stage-1 integration.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import random
import shutil
import statistics
import subprocess
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping

import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import risk_level1_core
STUDY = ROOT / "research/buy_ladder_backtest"
CONFIG = STUDY / "implementation_config.yaml"
DISPOSITION = STUDY / "inputs/input_disposition.json"
ACTIONS = STUDY / "inputs/corporate_actions.json"
ANOMALIES = STUDY / "inputs/price_anomaly_overrides.json"
PROTOCOL = STUDY / "PROTOCOL_V2.md"
AMENDMENT = STUDY / "PROTOCOL_V2_FOREIGN_DIVIDEND_AMENDMENT.md"
RECEIPT = STUDY / "validation/validation_receipt.json"
OUTPUT = STUDY / "execution"
BUILDER = STUDY / "build_input_disposition.py"
CORRECTIVE_DECISION = ROOT / "governance/decisions/LADDER-0004-invalid-initial-execution-and-corrective-reexecution-authorization.md"

ARMS = ("A_ATR", "B_FIXED", "C_IMMEDIATE")
SCOPES = ("whole", "equity", "broad_funds", "gold")
SEGMENT = {"SPY": "broad_funds", "VEA": "broad_funds", "VWO": "broad_funds", "GLD": "gold"}
EXPECTED = (
    "NVDA", "TSM", "ASML", "AVGO", "KLAC", "MSFT", "GOOGL", "AMZN", "META",
    "PANW", "LLY", "ISRG", "TMO", "V", "COST", "CEG", "ETN", "GEV", "GNRC",
    "PWR", "RTX", "SPY", "VEA", "VWO", "GLD",
)
WINDOWS = {"context": ("2021-06-01", "2023-12-29"), "holdout": ("2024-04-02", "2026-07-31"), "regime_2022": ("2022-01-01", "2022-12-31")}


class StudyError(RuntimeError):
    pass


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    def reject(token: str) -> None:
        raise StudyError(f"non-finite JSON token {token}")
    obj = json.loads(path.read_text(), parse_constant=reject)
    if type(obj) is not dict:
        raise StudyError(f"{path}: mapping required")
    return obj


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def code_commit() -> str:
    value = os.environ.get("LADDER_V2_CODE_COMMIT")
    if not value:
        value = subprocess.run(
            [
                "git", "log", "-1", "--format=%H", "--",
                str(Path(__file__).relative_to(ROOT)),
                str(CONFIG.relative_to(ROOT)),
                "test_buy_ladder_v2.py",
            ],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()
    if len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
        raise StudyError("code commit must be a lowercase 40-character SHA")
    return value


def config() -> dict[str, Any]:
    cfg = yaml.safe_load(CONFIG.read_text())
    registered = {
        "schema_version": "2.0",
        "study_id": "LADDER-V2-0001",
        "window": {
            "simulation_start": date(2021, 6, 1), "context_end": date(2023, 12, 29),
            "holdout_start": date(2024, 4, 2), "end": date(2026, 7, 31),
        },
        "friction_bps": [0, 10, 25], "decision_friction_bps": 10,
        "monthly_contribution": 2000.0, "protected_weight": 0.165,
        "minimum_lot": 25.0, "dividend_tax_rate": 0.168,
        "cash_tax_rate": 0.24, "cash_drag_bps": 25,
        "bootstrap": {"seed": 20260907, "resamples": 2000, "mean_block_sessions": 21},
    }
    drift = [key for key, value in registered.items() if cfg.get(key) != value]
    if drift:
        raise StudyError("registered parameter drift: " + ", ".join(drift))
    if cfg.get("status") != "FROZEN_BEFORE_REGISTERED_EXECUTION" or cfg.get("advisory_only") is not True:
        raise StudyError("implementation status or advisory boundary drift")
    if cfg.get("stage1") != "UNARMED_AND_NOT_EXECUTABLE":
        raise StudyError("Stage 1 boundary drift")
    if cfg.get("authority") != ["LADDER-0001", "LADDER-0002", "LADDER-0003", "LADDER-0004"]:
        raise StudyError("corrective authority drift")
    if cfg.get("holdout_previously_exposed") is not True:
        raise StudyError("corrective holdout disclosure missing")
    pins = {
        PROTOCOL: cfg["protocol_sha256"],
        AMENDMENT: cfg["amendment_sha256"],
        DISPOSITION: cfg["input_disposition_sha256"],
        ACTIONS: cfg["corporate_actions_sha256"],
        BUILDER: cfg["builder_sha256"],
        CORRECTIVE_DECISION: cfg["corrective_decision_sha256"],
    }
    for rel, digest in cfg["configuration_hashes"].items():
        pins[ROOT / rel] = digest
    for rel, digest in cfg["support_hashes"].items():
        pins[ROOT / rel] = digest
    bad = [f"{p.relative_to(ROOT)} expected {want} got {sha(p)}" for p, want in pins.items() if sha(p) != want]
    if bad:
        raise StudyError("frozen input drift: " + "; ".join(bad))
    return cfg


def load_inputs() -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]], list[str], dict[str, list[dict[str, Any]]]]:
    cfg = config()
    disp = read_json(DISPOSITION)
    rows = disp.get("price_files", [])
    if ([r.get("ticker") for r in rows] != list(EXPECTED)
            or disp.get("status") != "ACCEPTED_FOR_LADDER_IMPLEMENTATION_AFTER_MERGE"
            or disp.get("result_blind") is not True):
        raise StudyError("input disposition roster/status drift")
    prices: dict[str, list[dict[str, Any]]] = {}
    manifest = []
    anomaly_meta = disp.get("price_anomaly_corrections", {})
    if (anomaly_meta.get("path") != str(ANOMALIES.relative_to(ROOT))
            or anomaly_meta.get("sha256") != sha(ANOMALIES)):
        raise StudyError("price-anomaly disposition drift")
    overrides = read_json(ANOMALIES)
    if overrides.get("schema_version") != "1.0" or type(overrides.get("corrections")) is not list:
        raise StudyError("invalid price-anomaly override document")
    override_map = {}
    for correction in overrides["corrections"]:
        key = (correction.get("ticker"), correction.get("date"))
        if (key in override_map or key[0] not in EXPECTED
                or correction.get("field") not in {"open", "high", "low", "close"}
                or type(correction.get("evidence_receipt_ids")) is not list
                or len(correction["evidence_receipt_ids"]) < 2):
            raise StudyError("invalid/duplicate price-anomaly override")
        accepted = float(correction.get("accepted_value", float("nan")))
        observed = float(correction.get("observed_value", float("nan")))
        if not all(math.isfinite(value) and value > 0 for value in (accepted, observed)):
            raise StudyError("nonpositive/nonfinite price-anomaly override")
        override_map[key] = (correction["field"], accepted, observed)
    for item in rows:
        path = ROOT / item["path"]
        if sha(path) != item["sha256"]:
            raise StudyError(f"{item['ticker']}: selected price hash drift")
        doc = read_json(path)
        if doc.get("instrument") != item["ticker"] or doc.get("adjustment") != "SPLIT_ADJUSTED_NON_TOTAL_RETURN":
            raise StudyError(f"{item['ticker']}: identity/adjustment drift")
        bars = []
        prior = ""
        for raw in doc["rows"]:
            day = raw["date"]
            if day <= prior or day > "2026-07-31":
                raise StudyError(f"{item['ticker']}: invalid date sequence/end")
            row = dict(raw)
            if (item["ticker"], day) in override_map:
                field_name, accepted, observed = override_map[(item["ticker"], day)]
                if abs(float(row[field_name]) - observed) > 1e-12:
                    raise StudyError(f"{item['ticker']}: anomaly source value drift on {day}")
                row[field_name] = accepted
            vals = [float(row[k]) for k in ("open", "high", "low", "close")]
            if not all(math.isfinite(x) and x > 0 for x in vals) or row["low"] > min(row["open"], row["close"], row["high"]) or row["high"] < max(row["open"], row["close"], row["low"]):
                raise StudyError(f"{item['ticker']}: invalid OHLC on {day}")
            bars.append(row); prior = day
        if len(bars) != item["total_row_count"] or bars[-1]["date"] != "2026-07-31":
            raise StudyError(f"{item['ticker']}: row count/end drift")
        prices[item["ticker"]] = bars
        manifest.append({k: item[k] for k in ("ticker", "path", "sha256", "provider", "adjustment", "first_observation", "last_observation", "total_row_count")})
    sessions_doc = read_json(ROOT / "research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json")
    sessions = [x["session"] for x in sessions_doc["sessions"] if "2021-06-01" <= x["session"] <= "2026-07-31"]
    actions_doc = read_json(ACTIONS)
    if actions_doc.get("decision_id") != "LADDER-0003" or actions_doc.get("tax_semantics") != "PROTOCOL_V2_FOREIGN_DIVIDEND_AMENDMENT":
        raise StudyError("corporate-action authority drift")
    actions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen = set()
    for event in actions_doc["events"]:
        key = (event["symbol"], event["action_type"], event["ex_date"], event["id"])
        if key in seen or event["symbol"] not in EXPECTED or not ("2021-06-01" <= event["ex_date"] <= "2026-07-31"):
            raise StudyError("invalid/duplicate corporate action")
        if event["action_type"] == "cash_dividend":
            required = ("payable_date", "gross_rate_usd", "source_net_rate_usd", "source_withholding_usd", "rate_evidence", "same_day_split_basis")
            if any(event.get(k) in (None, "") for k in required):
                raise StudyError(f"{event['id']}: incomplete dividend fact")
            gross = float(event["gross_rate_usd"]); net = float(event["source_net_rate_usd"]); withheld = float(event["source_withholding_usd"])
            if not all(math.isfinite(x) for x in (gross, net, withheld)) or gross <= 0 or net <= 0 or withheld < 0 or net > gross + 1e-10 or abs(gross-net-withheld) > 1e-6:
                raise StudyError(f"{event['id']}: invalid dividend rates")
            if event["payable_date"] < event["ex_date"]:
                raise StudyError(f"{event['id']}: payable date precedes ex-date")
        elif event["action_type"] == "split":
            old = float(event.get("old_rate", 0)); new = float(event.get("new_rate", 0))
            if not math.isfinite(old) or not math.isfinite(new) or old <= 0 or new <= 0:
                raise StudyError(f"{event['id']}: invalid split rates")
        else:
            raise StudyError(f"{event['id']}: unsupported action type")
        seen.add(key); actions[event["symbol"]].append(event)
    return cfg, prices, sessions, actions


def indicators(bars: list[dict[str, Any]], end_index: int) -> tuple[float, float, float, float]:
    history = bars[:end_index + 1]
    closes = [float(x["close"]) for x in history]
    if len(closes) < 210:
        raise StudyError("indicator called before 210 rows")
    sma50 = sum(closes[-50:]) / 50
    sma200 = sum(closes[-200:]) / 200
    gains: list[float] = []; losses: list[float] = []; trs: list[float] = []
    for i in range(1, len(history)):
        delta = closes[i] - closes[i - 1]
        gains.append(max(delta, 0)); losses.append(max(-delta, 0))
        r = history[i]
        trs.append(max(float(r["high"]) - float(r["low"]), abs(float(r["high"]) - closes[i - 1]), abs(float(r["low"]) - closes[i - 1])))
    ag, al, atr = gains[0], losses[0], trs[0]
    alpha = 1 / 14
    for g, l, tr in zip(gains[1:], losses[1:], trs[1:]):
        ag = alpha * g + (1-alpha) * ag; al = alpha * l + (1-alpha) * al; atr = alpha * tr + (1-alpha) * atr
    rsi = 100.0 if al == 0 else 100 - 100 / (1 + ag/al)
    return sma50, sma200, atr, rsi


@dataclass
class Account:
    cash: float = 0.0
    shares: dict[str, float] = field(default_factory=lambda: defaultdict(float))
    receivables: list[dict[str, Any]] = field(default_factory=list)
    excluded_dividend_cash: float = 0.0
    contributions: list[dict[str, Any]] = field(default_factory=list)
    fills: list[dict[str, Any]] = field(default_factory=list)
    dividend_events: list[dict[str, Any]] = field(default_factory=list)
    settlement_events: list[dict[str, Any]] = field(default_factory=list)
    prior_shares: dict[str, float] = field(default_factory=dict)

    def nav(self, close: Mapping[str, float]) -> float:
        return self.cash + sum(self.shares[t] * close[t] for t in self.shares) + sum(x["net"] for x in self.receivables)

    def price_only_nav(self, close: Mapping[str, float]) -> float:
        return self.nav(close) - self.excluded_dividend_cash - sum(x["net"] for x in self.receivables)


def segment(ticker: str) -> str:
    return SEGMENT.get(ticker, "equity")


def first_eligible_decision_dates(
    prices: Mapping[str, list[dict[str, Any]]], cfg: Mapping[str, Any],
) -> dict[str, str]:
    simulation_start = cfg["window"]["simulation_start"].isoformat()
    return {
        ticker: max(simulation_start, rows[209]["date"])
        for ticker, rows in prices.items() if len(rows) >= 210
    }


def cell_key(arm: str, bps: int, scope: str = "whole") -> tuple[str, int, str]:
    return arm, bps, scope


def transaction(budget: float, bps: int) -> tuple[float, float]:
    if not math.isfinite(budget) or budget <= 0 or bps < 0:
        raise StudyError("invalid transaction budget or friction")
    rate = bps / 10000
    notional = budget / (1 + rate)
    cost = notional * rate
    if abs(notional + cost - budget) > 1e-8:
        raise StudyError("transaction identity failed")
    return notional, cost


def post_contribution(account: Account, day: str, amount: float) -> None:
    if not math.isfinite(amount) or amount < 0:
        raise StudyError("invalid contribution")
    account.cash += amount
    if amount:
        account.contributions.append({"date": day, "amount": amount})


def settle_and_accrue(account: Account, prior_day: str, day: str, cash_daily: Mapping[str, float]) -> None:
    cursor = date.fromisoformat(prior_day) + timedelta(days=1)
    stop = date.fromisoformat(day)
    while cursor <= stop:
        current = cursor.isoformat()
        keep = []
        for rec in account.receivables:
            if rec["payable_date"] == current:
                account.cash += rec["net"]
                account.excluded_dividend_cash += rec["net"]
                account.settlement_events.append({**rec, "date": current})
            else:
                keep.append(rec)
        account.receivables = keep
        factor = cash_daily[current]
        account.cash *= factor
        account.excluded_dividend_cash *= factor
        cursor += timedelta(days=1)


def recognize_dividend(account: Account, event: Mapping[str, Any], day: str, tax_mode: str, tax_rate: float = 0.168) -> None:
    quantity = account.prior_shares.get(str(event["symbol"]), 0.0)
    gross = quantity * float(event["anchor_gross"])
    if not gross:
        return
    source = quantity * float(event["anchor_withholding"])
    if tax_mode == "etn_no_exemption" and event["symbol"] == "ETN":
        source = gross * 0.25
    tentative = gross * tax_rate
    credit = 0.0 if tax_mode == "no_credit" else min(source, tentative)
    residual = tentative - credit
    total_tax = source + residual
    net = gross - total_tax
    if min(gross, source, tentative, credit, residual, total_tax, net) < -1e-10:
        raise StudyError("negative dividend component")
    row = {
        "ticker": event["symbol"], "ex_date": day,
        "payable_date": event["payable_date"], "gross": gross,
        "source_withholding": source, "tentative_us_tax": tentative,
        "foreign_tax_credit": credit, "residual_us_tax": residual,
        "total_tax": total_tax, "net": net,
    }
    account.receivables.append(dict(row))
    account.dividend_events.append(dict(row))


def dff_rates(sessions: list[str], cfg: Mapping[str, Any]) -> tuple[dict[str, float], dict[str, float]]:
    doc = read_json(ROOT / "research/level1_sleeve_robustness/data/transformed/selected/DFF.json")
    rates = {x["date"]: float(x["rate_pct"]) for x in doc["rows"]}
    start = (date.fromisoformat(sessions[0]) - timedelta(days=10)).isoformat()
    end = (date.fromisoformat(sessions[-1]) + timedelta(days=2)).isoformat()
    business = risk_level1_core.federal_business_days(start, end)
    missing = [day for day in business if day <= sessions[-1] and day not in rates]
    if missing:
        raise StudyError(f"DFF missing {len(missing)} federal-business-day observations")
    lawful = []
    for i in range(len(business)-1):
        lawful.append((date.fromisoformat(business[i+1]) + timedelta(days=1), rates[business[i]]))
    cash_daily: dict[str, float] = {}; rf_daily: dict[str, float] = {}
    pointer = 0; current = None; day = date.fromisoformat(sessions[0])
    last = date.fromisoformat(sessions[-1])
    while day <= last:
        while pointer < len(lawful) and lawful[pointer][0] <= day:
            current = lawful[pointer][1]; pointer += 1
        if current is None: raise StudyError(f"no lawful DFF for {day}")
        cash_daily[day.isoformat()] = 1 + ((current/100 - cfg["cash_drag_bps"]/10000) * (1-cfg["cash_tax_rate"])) / 360
        rf_daily[day.isoformat()] = 1 + (current/100) / 360
        day += timedelta(days=1)
    return cash_daily, rf_daily


def exposure_rooms(values: Mapping[str, float], nav: float, targets: Mapping[str, float], caps: list[dict[str, Any]], look: Mapping[str, Any]) -> tuple[dict[str, float], float, dict[str, float]]:
    cluster_vals = {c["name"]: sum(values.get(t, 0) for t in c["tickers"]) for c in caps}
    issuer = defaultdict(float)
    for row in look["issuers"]:
        ticker = row["ticker"]
        issuer[ticker] += values.get(ticker, 0)
        for f in row.get("funds", []): issuer[ticker] += values.get(f["fund"], 0) * float(f["fund_holding_weight"])
    common = sum(issuer.values())
    return cluster_vals, common, dict(issuer)


def _invalid_pr384_simulate(cfg: Mapping[str, Any], prices: Mapping[str, list[dict[str, Any]]], sessions: list[str], actions: Mapping[str, list[dict[str, Any]]], tax_mode: str = "baseline") -> dict[str, Any]:
    targets_doc = yaml.safe_load((ROOT / "targets.yaml").read_text())
    targets = {r["ticker"]: float(r["target_pct"])/100 for r in targets_doc["destination"] if r["ticker"] in EXPECTED}
    order = {r["ticker"]: i for i, r in enumerate(targets_doc["destination"])}
    caps = targets_doc["caps"]["clusters"]
    look = yaml.safe_load((ROOT / "issuer_lookthrough.yaml").read_text())
    by_day = {t: {r["date"]: (i, r) for i, r in enumerate(rows)} for t, rows in prices.items()}
    first_eligible = {}
    for t, rows in prices.items():
        if len(rows) >= 210: first_eligible[t] = rows[209]["date"]
    accounts = {(a, b): Account() for a in ARMS for b in cfg["friction_bps"]}
    shadow = Account()
    paths = {(a, b): [] for a in ARMS for b in cfg["friction_bps"]}
    pending: list[dict[str, Any]] = []
    all_orders: list[dict[str, Any]] = []
    cycles: list[dict[str, Any]] = []
    cash_daily, rf_daily = dff_rates(sessions, cfg)
    action_day = defaultdict(list)
    for ticker, events in actions.items():
        splits = [e for e in events if e["action_type"] == "split"]
        for e in events:
            if e["action_type"] != "cash_dividend": continue
            divisor = 1.0
            for sp in splits:
                if sp["ex_date"] > e["ex_date"] or (sp["ex_date"] == e["ex_date"] and e["same_day_split_basis"] == "PRE_SPLIT"):
                    divisor *= float(sp["new_rate"])/float(sp["old_rate"])
            event = dict(e); event["anchor_gross"] = float(e["gross_rate_usd"])/divisor; event["anchor_withholding"] = float(e["source_withholding_usd"])/divisor
            action_day[e["ex_date"]].append(event)
    prior_close = None
    for si, day in enumerate(sessions):
        close = {}
        for t in EXPECTED:
            if day in by_day[t]: close[t] = float(by_day[t][day][1]["close"])
            elif day >= first_eligible[t]: raise StudyError(f"{t}: missing required XNYS row {day}")
        if si:
            # Split every close-to-close interval at 00:00 payable timestamps.
            # This prevents a weekend/holiday receivable from earning cash return
            # before it actually settles.
            for acct in [shadow, *accounts.values()]:
                cursor = date.fromisoformat(sessions[si-1]) + timedelta(days=1)
                while cursor <= date.fromisoformat(day):
                    cursor_s = cursor.isoformat(); keep = []
                    for rec in acct.receivables:
                        if rec["payable_date"] == cursor_s:
                            acct.cash += rec["net"]; acct.dividends["settlements"] += rec["net"]
                        else: keep.append(rec)
                    acct.receivables = keep
                    acct.cash *= cash_daily[cursor_s]
                    cursor += timedelta(days=1)
            # Open fills before ex-date entitlement.
            still = []
            for o in pending:
                if day < o["active"] or day > o["expiry"]: continue
                if day not in by_day[o["ticker"]]: still.append(o); continue
                row = by_day[o["ticker"]][day][1]
                fill = o["arm"] == "C_IMMEDIATE" or float(row["low"]) <= o["limit"]
                if not fill: still.append(o); continue
                price = float(row["open"]) if o["arm"] == "C_IMMEDIATE" else min(float(row["open"]), o["limit"])
                acct = accounts[(o["arm"], o["bps"])]
                budget = o["budget"]; cost = budget * (o["bps"]/10000)/(1+o["bps"]/10000); notional = budget-cost
                if acct.cash + 1e-8 < budget: raise StudyError("negative cash required for fill")
                acct.cash -= budget; acct.shares[o["ticker"]] += notional/price; acct.costs += cost; acct.deployed += notional; acct.tx += 1
                o["filled"] = day; o["fill_price"] = price
                acct.fills.append({"ticker":o["ticker"],"selection":o["selection"],"date":day,"budget":budget,"notional":notional,"cost":cost,"segment":o["segment"]})
            pending = still
            # Shadow next-open fills are separately recorded as C/0 orders.
            for cyc in cycles:
                if cyc["active"] == day and not cyc.get("shadow_filled"):
                    for alloc in cyc["allocations"]:
                        row = by_day[alloc["ticker"]][day][1]
                        shadow.cash -= alloc["budget"]; shadow.shares[alloc["ticker"]] += alloc["budget"]/float(row["open"])
                    cyc["shadow_filled"] = True
        # Dividend belongs only to shares held at preceding close; open fills above
        # are removed from entitlement by snapshotting quantities before fills would
        # be ideal. We use prior-close quantities retained on each account.
        for e in action_day.get(day, []):
            t = e["symbol"]
            for acct in [shadow, *accounts.values()]:
                qty = acct.prior_shares.get(t, 0.0)
                gross = qty * e["anchor_gross"]
                source = qty * e["anchor_withholding"]
                if tax_mode == "etn_no_exemption" and t == "ETN": source = gross * .25
                us = gross * cfg["dividend_tax_rate"]
                credit = 0 if tax_mode == "no_credit" else min(source, us)
                residual = us-credit; tax = source+residual; net = gross-tax
                if net < -1e-10: raise StudyError("negative dividend receivable")
                if gross:
                    acct.receivables.append({"ticker": t, "ex_date": day, "payable_date": e["payable_date"], "net": net})
                    for k,v in (("gross",gross),("source_withholding",source),("tentative_us_tax",us),("foreign_tax_credit",credit),("residual_us_tax",residual),("total_tax",tax),("net",net)): acct.dividends[k]+=v
        preflow_nav = {key: acct.nav(close) for key, acct in accounts.items()}
        # Store the cash-flow-adjusted close path before adding the external flow.
        for key, acct in accounts.items():
            prior = paths[key][-1] if paths[key] else None
            if prior is None and preflow_nav[key] == 0: ret = 0.0; idx = 1.0
            elif prior is None: ret = 0.0; idx = 1.0
            else:
                ret = preflow_nav[key]/prior["postflow_nav"]-1; idx = prior["index"]*(1+ret)
            rf = 1.0
            if si:
                cursor = date.fromisoformat(sessions[si-1]) + timedelta(days=1)
                while cursor <= date.fromisoformat(day): rf *= rf_daily[cursor.isoformat()]; cursor += timedelta(days=1)
            paths[key].append({"date":day,"preflow_nav":preflow_nav[key],"postflow_nav":preflow_nav[key],"cash":acct.cash,"return":ret,"index":idx,"risk_free_return":rf-1})
        first_of_month = si == 0 or sessions[si-1][:7] != day[:7]
        if first_of_month:
            shadow.cash += cfg["monthly_contribution"]
            for key, acct in accounts.items():
                acct.cash += cfg["monthly_contribution"]; paths[key][-1]["postflow_nav"] += cfg["monthly_contribution"]; paths[key][-1]["cash"] = acct.cash
            shadow_nav = shadow.nav(close)
            surplus = [max(0.0, shadow.cash-cfg["protected_weight"]*shadow_nav)]
            surplus += [max(0.0, a.cash-cfg["protected_weight"]*a.nav(close)) for a in accounts.values()]
            remaining = min(cfg["monthly_contribution"], min(surplus))
            values = {t: shadow.shares[t]*close[t] for t in close}
            gaps = []
            for t in EXPECTED:
                if t not in close or day < first_eligible[t]: continue
                sma50,sma200,atr,rsi = indicators(prices[t],by_day[t][day][0])
                if close[t] < sma200 and rsi >= 30: continue
                gap = targets[t]*shadow_nav-values.get(t,0)
                if gap > 0: gaps.append((t,gap,(sma50,sma200,atr,rsi)))
            gaps.sort(key=lambda x:(-x[1],order[x[0]]))
            cluster_vals, common, issuer = exposure_rooms(values,shadow_nav,targets,caps,look)
            allocations=[]; clip_counts=defaultdict(int)
            for t,gap,ind in gaps:
                if remaining < cfg["minimum_lot"]: break
                want=min(gap,remaining)
                for c in caps:
                    if t in c["tickers"]:
                        room=shadow_nav*float(c["pct"])/100-cluster_vals[c["name"]]
                        if room < want: clip_counts["cluster"]+=1
                        want=min(want,max(0,room))
                direct={x["ticker"]:x for x in look["issuers"]}
                if t in direct:
                    room=shadow_nav*float(look["issuer_ceiling_pct"])/100-issuer.get(t,0)
                    if room < want: clip_counts["issuer"]+=1
                    want=min(want,max(0,room))
                elif t in {f["fund"] for x in look["issuers"] for f in x.get("funds",[])}:
                    for x in look["issuers"]:
                        for f in x.get("funds",[]):
                            if f["fund"]==t:
                                room=(shadow_nav*float(look["issuer_ceiling_pct"])/100-issuer.get(x["ticker"],0))/float(f["fund_holding_weight"])
                                want=min(want,max(0,room))
                marginal=1.0 if t in direct else sum(float(f["fund_holding_weight"]) for x in look["issuers"] for f in x.get("funds",[]) if f["fund"]==t)
                if marginal:
                    room=(shadow_nav*float(look["common_driver_ceiling_pct"])/100-common)/marginal
                    if room < want: clip_counts["common_driver"]+=1
                    want=min(want,max(0,room))
                if want < cfg["minimum_lot"]: continue
                allocations.append({"ticker":t,"budget":want,"indicators":{"sma50":ind[0],"sma200":ind[1],"atr14":ind[2],"rsi14":ind[3]},"segment":SEGMENT.get(t,"equity")})
                remaining-=want; values[t]=values.get(t,0)+want
                for c in caps:
                    if t in c["tickers"]: cluster_vals[c["name"]]+=want
                if t in direct: issuer[t]=issuer.get(t,0)+want; common+=want
                else:
                    for x in look["issuers"]:
                        for f in x.get("funds",[]):
                            if f["fund"]==t: issuer[x["ticker"]]=issuer.get(x["ticker"],0)+want*float(f["fund_holding_weight"]); common+=want*float(f["fund_holding_weight"])
            active=sessions[si+1] if si+1<len(sessions) else None
            next_month=next((x for x in sessions[si+1:] if x[:7]!=day[:7]),None)
            expiry=sessions[sessions.index(next_month)-1] if next_month else sessions[-1]
            cycle={"selection_date":day,"active":active,"expiry":expiry,"allocations":allocations,"unassigned":remaining,"clip_counts":dict(clip_counts)}; cycles.append(cycle)
            if active:
                for alloc in allocations:
                    t=alloc["ticker"]; sma50=alloc["indicators"]["sma50"]
                    levels={"A_ATR":[sma50-alloc["indicators"]["atr14"],sma50-2*alloc["indicators"]["atr14"],max(sma50-3*alloc["indicators"]["atr14"],alloc["indicators"]["sma200"])],"B_FIXED":[sma50*.95,sma50*.90,sma50*.85]}
                    for bps in cfg["friction_bps"]:
                        immediate={"arm":"C_IMMEDIATE","bps":bps,"ticker":t,"budget":alloc["budget"],"limit":math.inf,"active":active,"expiry":active,"selection":day,"segment":alloc["segment"]}
                        pending.append(immediate); all_orders.append(immediate)
                        for arm in ("A_ATR","B_FIXED"):
                            for level in levels[arm]:
                                order_row={"arm":arm,"bps":bps,"ticker":t,"budget":alloc["budget"]/3,"limit":level,"active":active,"expiry":expiry,"selection":day,"segment":alloc["segment"]}
                                pending.append(order_row); all_orders.append(order_row)
        for acct in [shadow,*accounts.values()]: acct.prior_shares = dict(acct.shares)
    return {"paths":paths,"accounts":accounts,"cycles":cycles,"first_eligible":first_eligible,"pending":pending,"orders":all_orders,"tax_mode":tax_mode}


def _invalid_pr384_metrics(result: Mapping[str, Any], cfg: Mapping[str, Any]) -> dict[str, Any]:
    out={}
    for (arm,bps),path in result["paths"].items():
        acct=result["accounts"][(arm,bps)]
        for win,(start,end) in WINDOWS.items():
            rows=[x for x in path if start<=x["date"]<=end]
            if len(rows)<2: raise StudyError("insufficient window observations")
            base=rows[0]["index"]; idx=[x["index"]/base for x in rows]; rets=[x["return"] for x in rows[1:]]; rf=[x["risk_free_return"] for x in rows[1:]]
            cum=idx[-1]-1; days=(date.fromisoformat(rows[-1]["date"])-date.fromisoformat(rows[0]["date"])).days
            cagr=(1+cum)**(365.2425/days)-1 if days else 0
            peak=idx[0]; maxdd=0.0
            for x in idx: peak=max(peak,x); maxdd=min(maxdd,x/peak-1)
            vol=statistics.stdev(rets)*math.sqrt(252) if len(rets)>1 else None
            excess=[a-b for a,b in zip(rets,rf)]; sharpe=statistics.mean(excess)/statistics.stdev(excess)*math.sqrt(252) if len(excess)>1 and statistics.stdev(excess)>0 else None
            out[f"{arm}|{bps}|{win}"]={"arm":arm,"cost_bps":bps,"window":win,"observations":len(rows),"cumulative_twr":cum,"annualized_twr":cagr,"max_drawdown":maxdd,"annualized_volatility":vol,"sharpe":sharpe,"ending_value":rows[-1]["preflow_nav"],"time_weighted_cash_pct":statistics.mean(x["cash"]/x["postflow_nav"] if x["postflow_nav"] else 1 for x in rows),"transaction_count":acct.tx,"deployed_dollars":acct.deployed,"transaction_cost":acct.costs,"dividends":dict(acct.dividends)}
    for bps in cfg["friction_bps"]:
        c=out[f"C_IMMEDIATE|{bps}|holdout"]["cumulative_twr"]
        for arm in ARMS: out[f"{arm}|{bps}|holdout"]["cash_drag"] = c-out[f"{arm}|{bps}|holdout"]["cumulative_twr"]
    return out


def _invalid_pr384_bootstrap(paths: Mapping[tuple[str,int],list[dict[str,Any]]], cfg: Mapping[str,Any]) -> list[dict[str,Any]]:
    answer=[]; nres=cfg["bootstrap"]["resamples"]; mean=cfg["bootstrap"]["mean_block_sessions"]
    for bps in cfg["friction_bps"]:
        window={a:[x["return"] for x in paths[(a,bps)] if "2024-04-02"<=x["date"]<="2026-07-31"] for a in ARMS}
        n=len(next(iter(window.values())))
        for challenger in ARMS:
            for baseline in ARMS:
                if challenger==baseline: continue
                seed=int.from_bytes(hashlib.sha256(f"20260907|{challenger}|{baseline}".encode()).digest()[:8],"big"); rng=random.Random(seed); wins=0
                for _ in range(nres):
                    indexes=[]; cur=rng.randrange(n)
                    for i in range(n):
                        if i and rng.random()<1/mean: cur=rng.randrange(n)
                        elif i: cur=(cur+1)%n
                        indexes.append(cur)
                    ca=ba=1.0
                    for i in indexes: ca*=1+window[challenger][i]; ba*=1+window[baseline][i]
                    wins+=ca>ba
                answer.append({"challenger":challenger,"baseline":baseline,"cost_bps":bps,"probability_challenger_exceeds":wins/nres,"resamples":nres,"mean_block_sessions":mean,"seed":seed})
    return answer


def _invalid_pr384_disposition(metric: Mapping[str,Any], boot: list[dict[str,Any]], sensitivities: Mapping[str,Mapping[str,Any]], cfg: Mapping[str,Any]) -> dict[str,Any]:
    gates=[]; winners=[]
    probs={(x["challenger"],x["baseline"],x["cost_bps"]):x["probability_challenger_exceeds"] for x in boot}
    for ch in ARMS:
        all_pass=True
        for base in ARMS:
            if ch==base: continue
            cells=[]
            for bps in cfg["friction_bps"]:
                a=metric[f"{ch}|{bps}|holdout"]; b=metric[f"{base}|{bps}|holdout"]
                passed=a["annualized_twr"]-b["annualized_twr"]>.01 and a["max_drawdown"]-b["max_drawdown"]>=-.01
                cells.append({"cost_bps":bps,"annualized_twr_delta":a["annualized_twr"]-b["annualized_twr"],"max_drawdown_delta":a["max_drawdown"]-b["max_drawdown"],"bootstrap_probability":probs[(ch,base,bps)],"passed":passed})
            pair_pass=all(x["passed"] for x in cells) and probs[(ch,base,cfg["decision_friction_bps"])]>=.90
            gates.append({"challenger":ch,"baseline":base,"cells":cells,"passed":pair_pass}); all_pass &= pair_pass
        if all_pass:winners.append(ch)
    status="RETAIN_BASELINE" if not winners else ("STRONGER_EVIDENCE_FOR_A" if winners==["A_ATR"] else f"RECOMMEND_{winners[0]}_FOR_SEPARATE_GOVERNANCE")
    baseline_rank=max(ARMS,key=lambda a:metric[f"{a}|10|holdout"]["annualized_twr"])
    for mode,sm in sensitivities.items():
        if max(ARMS,key=lambda a:sm[f"{a}|10|holdout"]["annualized_twr"])!=baseline_rank: status="INSUFFICIENT_EVIDENCE"
    return {"status":status,"winning_arms":winners,"apparent_decision_cell_leader":baseline_rank,"pairwise_gates":gates,"production_change_authorized":False,"stage1":"UNARMED_AND_NOT_EXECUTABLE"}


def _invalid_pr384_bundle(cfg: Mapping[str,Any], include_holdout: bool) -> dict[str,Any]:
    disp=read_json(DISPOSITION)
    paths=[CONFIG,PROTOCOL,AMENDMENT,DISPOSITION,ACTIONS,Path(__file__),ROOT/"targets.yaml",ROOT/"gates.yaml",ROOT/"issuer_lookthrough.yaml"]+[ROOT/x["path"] for x in disp["price_files"]]
    return {"schema_version":"2.0","study_id":cfg["study_id"],"code_commit":code_commit(),"runtime":{"python":sys.version.split()[0],"packages":{"PyYAML":importlib.metadata.version("PyYAML")}},"files":{str(p.relative_to(ROOT)):sha(p) for p in paths},"holdout_results_emitted":include_holdout,"seed":cfg["bootstrap"]["seed"],"advisory_only":True,"stage1":"UNARMED_AND_NOT_EXECUTABLE"}


def _invalid_pr384_validate() -> dict[str,Any]:
    cfg,prices,sessions,actions=load_inputs()
    # Non-holdout-only indicator and availability validation; simulate is
    # deliberately not called, so no holdout metric can be produced here.
    for t,rows in prices.items():
        candidates=[i for i,r in enumerate(rows) if r["date"]<="2023-12-29" and i>=209]
        if not candidates and t not in ("CEG","GEV"): raise StudyError(f"{t}: no context indicator window")
        for i in candidates[::max(1,len(candidates)//5)]:
            if not all(math.isfinite(x) for x in indicators(rows,i)): raise StudyError(f"{t}: nonfinite context indicator")
    receipt=bundle(cfg,False); receipt["validation_scope"]="INPUTS_AND_NON_HOLDOUT_ONLY"; receipt["validated_tickers"]=list(EXPECTED); receipt["session_count"]=len(sessions); receipt["action_count"]=sum(map(len,actions.values()))
    RECEIPT.parent.mkdir(exist_ok=True); RECEIPT.write_bytes(canonical(receipt)); return receipt


def _invalid_pr384_execute() -> dict[str,Any]:
    cfg,prices,sessions,actions=load_inputs(); expected=bundle(cfg,False)
    if not RECEIPT.is_file(): raise StudyError("validation receipt missing")
    receipt=read_json(RECEIPT)
    for k in ("code_commit","runtime","files","seed","advisory_only","stage1"):
        if receipt.get(k)!=expected.get(k): raise StudyError(f"validation receipt drift: {k}")
    if receipt.get("holdout_results_emitted") is not False: raise StudyError("invalid validation receipt")
    main=simulate(cfg,prices,sessions,actions); met=metrics(main,cfg); boot=bootstrap(main["paths"],cfg)
    sens={}
    for mode in ("no_credit","etn_no_exemption"):
        sim=simulate(cfg,prices,sessions,actions,mode); sens[mode]=metrics(sim,cfg)
    decision=disposition(met,boot,sens,cfg)
    manifest=bundle(cfg,True)
    docs={"metrics.json":met,"bootstrap.json":boot,"sensitivities.json":sens,"cycles.json":main["cycles"],"portfolio_paths.json":{f"{a}|{b}":v for (a,b),v in main["paths"].items()},"disposition.json":decision,"input_manifest.json":manifest}
    manifest["outputs"]={name:hashlib.sha256(canonical(value)).hexdigest() for name,value in docs.items() if name!="input_manifest.json"}
    docs["input_manifest.json"]=manifest
    OUTPUT.parent.mkdir(exist_ok=True)
    tmp=Path(tempfile.mkdtemp(prefix="ladder-v2-",dir=STUDY))
    try:
        for name,value in docs.items():(tmp/name).write_bytes(canonical(value))
        if OUTPUT.exists(): raise StudyError("registered output already exists; rerun prohibited")
        tmp.replace(OUTPUT)
    except Exception:
        if tmp.exists():
            for p in tmp.iterdir():p.unlink()
            tmp.rmdir()
        raise
    return decision


# Corrective implementation. The prefixed functions above preserve the invalid
# PR #384 attempt for audit comparison; no entry point calls them.
def exposure_rooms_v2(values: Mapping[str, float], caps: list[dict[str, Any]], look: Mapping[str, Any]) -> tuple[dict[str, float], float, dict[str, float]]:
    clusters = {c["name"]: sum(values.get(t, 0.0) for t in c["tickers"]) for c in caps}
    issuer: dict[str, float] = {}
    for row in look["issuers"]:
        value = values.get(row["ticker"], 0.0)
        value += sum(values.get(f["fund"], 0.0) * float(f["fund_holding_weight"]) for f in row.get("funds", []))
        issuer[row["ticker"]] = value
    return clusters, sum(issuer.values()), issuer


def select_allocations(
    shadow: Account,
    whole_accounts: Iterable[Account],
    close: Mapping[str, float],
    targets: Mapping[str, float],
    destination_order: Mapping[str, int],
    indicator_values: Mapping[str, tuple[float, float, float, float]],
    caps: list[dict[str, Any]],
    look: Mapping[str, Any],
    contribution: float,
    protected_weight: float,
    minimum_lot: float,
) -> tuple[list[dict[str, Any]], float, list[dict[str, Any]]]:
    """Run the frozen production-greedy mechanics on the shared shadow state."""
    shadow_nav = shadow.nav(close)
    surpluses = [max(0.0, shadow.cash - protected_weight * shadow_nav)]
    surpluses.extend(max(0.0, account.cash - protected_weight * account.nav(close)) for account in whole_accounts)
    remaining = min(contribution, *surpluses)
    values = {ticker: shadow.shares[ticker] * close[ticker] for ticker in close}
    candidates = []
    for ticker in EXPECTED:
        if ticker not in indicator_values or ticker not in close:
            continue
        sma50, sma200, atr14, rsi14 = indicator_values[ticker]
        if close[ticker] < sma200 and rsi14 >= 30:
            continue
        gap = targets[ticker] * shadow_nav - values.get(ticker, 0.0)
        if gap > 0:
            candidates.append((ticker, gap, (sma50, sma200, atr14, rsi14)))
    candidates.sort(key=lambda row: (-row[1], destination_order[row[0]]))
    cluster_values, common_value, issuer_values = exposure_rooms_v2(values, caps, look)
    direct = {row["ticker"]: row for row in look["issuers"]}
    fund_rows: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for row in look["issuers"]:
        for fund in row.get("funds", []):
            fund_rows[fund["fund"]].append((row["ticker"], float(fund["fund_holding_weight"])))
    allocations: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    for ticker, gap, ind in candidates:
        if remaining < minimum_lot:
            break
        initial = min(gap, remaining)
        want = initial
        constraints: list[tuple[str, str, float]] = []
        for cluster in caps:
            if ticker in cluster["tickers"]:
                room = shadow_nav * float(cluster["pct"]) / 100 - cluster_values[cluster["name"]]
                constraints.append(("cluster", cluster["name"], max(0.0, room)))
        if ticker in direct:
            room = shadow_nav * float(look["issuer_ceiling_pct"]) / 100 - issuer_values.get(ticker, 0.0)
            constraints.append(("effective_issuer", ticker, max(0.0, room)))
        for issuer_ticker, holding_weight in fund_rows[ticker]:
            room = (shadow_nav * float(look["issuer_ceiling_pct"]) / 100 - issuer_values.get(issuer_ticker, 0.0)) / holding_weight
            constraints.append(("effective_issuer", issuer_ticker, max(0.0, room)))
        marginal = 1.0 if ticker in direct else sum(weight for _, weight in fund_rows[ticker])
        if marginal:
            room = (shadow_nav * float(look["common_driver_ceiling_pct"]) / 100 - common_value) / marginal
            constraints.append(("common_driver", "AI_PLATFORM", max(0.0, room)))
        want = min([want, *(room for _kind, _subject, room in constraints)])
        binding = [
            (kind, subject) for kind, subject, room in constraints
            if room + 1e-9 < initial and abs(room - want) <= 1e-9
        ]
        if want < minimum_lot:
            for kind, subject in binding:
                events.append({"ticker": ticker, "segment": segment(ticker), "constraint": kind, "subject": subject, "outcome": "block", "requested": initial, "admitted": 0.0})
            continue
        for kind, subject in binding:
            events.append({"ticker": ticker, "segment": segment(ticker), "constraint": kind, "subject": subject, "outcome": "clip", "requested": initial, "admitted": want})
        allocations.append({
            "ticker": ticker, "budget": want, "segment": segment(ticker),
            "indicators": {"sma50": ind[0], "sma200": ind[1], "atr14": ind[2], "rsi14": ind[3]},
        })
        remaining -= want
        values[ticker] = values.get(ticker, 0.0) + want
        for cluster in caps:
            if ticker in cluster["tickers"]:
                cluster_values[cluster["name"]] += want
        if ticker in direct:
            issuer_values[ticker] = issuer_values.get(ticker, 0.0) + want
            common_value += want
        else:
            for issuer_ticker, holding_weight in fund_rows[ticker]:
                delta = want * holding_weight
                issuer_values[issuer_ticker] = issuer_values.get(issuer_ticker, 0.0) + delta
                common_value += delta
    return allocations, remaining, events


def _append_path_v2(path: list[dict[str, Any]], account: Account, day: str, close: Mapping[str, float], rf_return: float) -> None:
    pre = account.nav(close)
    price_pre = account.price_only_nav(close)
    prior = path[-1] if path else None
    total_ret = 0.0 if prior is None or prior["postflow_nav"] == 0 else pre / prior["postflow_nav"] - 1
    price_ret = 0.0 if prior is None or prior["price_only_postflow_nav"] == 0 else price_pre / prior["price_only_postflow_nav"] - 1
    positions = {ticker: account.shares[ticker] * close[ticker] for ticker in account.shares if ticker in close and account.shares[ticker]}
    path.append({
        "date": day, "preflow_nav": pre, "postflow_nav": pre,
        "price_only_preflow_nav": price_pre, "price_only_postflow_nav": price_pre,
        "external_flow": 0.0, "cash": account.cash,
        "receivables": sum(row["net"] for row in account.receivables),
        "receivables_by_ticker": {
            ticker: sum(row["net"] for row in account.receivables if row["ticker"] == ticker)
            for ticker in sorted({row["ticker"] for row in account.receivables})
        },
        "return": total_ret, "index": (prior["index"] if prior else 1.0) * (1 + total_ret),
        "price_only_return": price_ret,
        "price_only_index": (prior["price_only_index"] if prior else 1.0) * (1 + price_ret),
        "risk_free_return": rf_return, "position_values": positions,
    })


def _apply_flow_v2(path: list[dict[str, Any]], account: Account, day: str, amount: float) -> None:
    post_contribution(account, day, amount)
    row = path[-1]
    row["external_flow"] += amount
    row["postflow_nav"] += amount
    row["price_only_postflow_nav"] += amount
    row["cash"] = account.cash


def _fill_v2(
    account: Account, order: dict[str, Any], fill_day: str, price: float,
    *, segment_mirror: bool = False,
) -> None:
    requested_budget = float(order["budget"])
    # Segment paths are attribution mirrors, not separately funded accounts.
    # Their allocated cash can decline slightly between selection and activation
    # when the registered net cash rate is negative. Mirror the executable whole
    # account's fill with the cash actually available instead of manufacturing a
    # tiny segment-level loan or failing an otherwise funded whole-account order.
    budget = min(requested_budget, max(0.0, account.cash)) if segment_mirror else requested_budget
    if budget <= 0:
        raise StudyError("nonpositive cash available for fill")
    notional, cost = transaction(budget, int(order["bps"]))
    if account.cash + 1e-8 < budget:
        raise StudyError("negative cash required for fill")
    account.cash -= budget
    account.shares[order["ticker"]] += notional / price
    account.fills.append({
        "ticker": order["ticker"], "selection_date": order["selection_date"],
        "date": fill_day, "budget": budget, "requested_budget": requested_budget,
        "segment_mirror": segment_mirror, "notional": notional,
        "cost": cost, "fill_price": price, "segment": order["segment"],
    })


def anchor_dividend(source: Mapping[str, Any], splits: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Convert a source-date dividend to the frozen 2026-07-31 share basis."""
    divisor = 1.0
    for split in splits:
        same_day = split["ex_date"] == source["ex_date"]
        if same_day and source["same_day_split_basis"] not in {"PRE_SPLIT", "POST_SPLIT"}:
            raise StudyError(f"{source['id']}: ambiguous same-day split basis")
        if split["ex_date"] > source["ex_date"] or (same_day and source["same_day_split_basis"] == "PRE_SPLIT"):
            divisor *= float(split["new_rate"]) / float(split["old_rate"])
    event = dict(source)
    event["anchor_gross"] = float(source["gross_rate_usd"]) / divisor
    event["anchor_withholding"] = float(source["source_withholding_usd"]) / divisor
    return event


def simulate(cfg: Mapping[str, Any], prices: Mapping[str, list[dict[str, Any]]], sessions: list[str], actions: Mapping[str, list[dict[str, Any]]], tax_mode: str = "baseline") -> dict[str, Any]:
    if tax_mode not in {"baseline", "no_credit", "etn_no_exemption"}:
        raise StudyError("unknown tax mode")
    targets_doc = yaml.safe_load((ROOT / "targets.yaml").read_text())
    targets = {row["ticker"]: float(row["target_pct"]) / 100 for row in targets_doc["destination"] if row["ticker"] in EXPECTED}
    if list(targets) != list(EXPECTED) or abs(sum(targets.values()) - 0.835) > 1e-12:
        raise StudyError("target roster or residual cash drift")
    destination_order = {row["ticker"]: i for i, row in enumerate(targets_doc["destination"])}
    caps = targets_doc["caps"]["clusters"]
    look = yaml.safe_load((ROOT / "issuer_lookthrough.yaml").read_text())
    by_day = {ticker: {row["date"]: (i, row) for i, row in enumerate(rows)} for ticker, rows in prices.items()}
    first_eligible = first_eligible_decision_dates(prices, cfg)
    accounts = {cell_key(arm, bps, scope): Account() for arm in ARMS for bps in cfg["friction_bps"] for scope in SCOPES}
    whole_keys = [cell_key(arm, bps) for arm in ARMS for bps in cfg["friction_bps"]]
    shadow = Account()
    paths = {key: [] for key in accounts}
    pending: list[dict[str, Any]] = []
    orders: list[dict[str, Any]] = []
    cycles: list[dict[str, Any]] = []
    constraint_events: list[dict[str, Any]] = []
    cash_daily, rf_daily = dff_rates(sessions, cfg)
    action_day: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ticker, events in actions.items():
        splits = [event for event in events if event["action_type"] == "split"]
        for source in events:
            if source["action_type"] != "cash_dividend":
                continue
            action_day[source["ex_date"]].append(anchor_dividend(source, splits))
    for session_index, day in enumerate(sessions):
        close: dict[str, float] = {}
        for ticker in EXPECTED:
            if day in by_day[ticker]:
                close[ticker] = float(by_day[ticker][day][1]["close"])
            elif day >= first_eligible[ticker]:
                raise StudyError(f"{ticker}: missing required XNYS row {day}")
        if session_index:
            prior_day = sessions[session_index - 1]
            for account in [shadow, *accounts.values()]:
                settle_and_accrue(account, prior_day, day, cash_daily)
            still_pending = []
            for order in pending:
                if day < order["active"]:
                    still_pending.append(order); continue
                if day > order["expiry"]:
                    raise StudyError("order crossed expiry unresolved")
                price_row = by_day[order["ticker"]].get(day)
                if price_row is None:
                    raise StudyError(f"{order['ticker']}: missing order-session OHLC")
                bar = price_row[1]
                fillable = order["arm"] == "C_IMMEDIATE" or float(bar["low"]) <= float(order["limit"])
                if fillable:
                    fill_price = float(bar["open"]) if order["arm"] == "C_IMMEDIATE" else min(float(bar["open"]), float(order["limit"]))
                    _fill_v2(accounts[cell_key(order["arm"], order["bps"])], order, day, fill_price)
                    _fill_v2(
                        accounts[cell_key(order["arm"], order["bps"], order["segment"])],
                        order, day, fill_price, segment_mirror=True,
                    )
                    order["status"] = "filled"; order["resolution_date"] = day; order["fill_price"] = fill_price
                elif day == order["expiry"]:
                    order["status"] = "expired"; order["resolution_date"] = day
                else:
                    still_pending.append(order)
            pending = still_pending
            for cycle in cycles:
                if cycle["active"] == day and not cycle["shadow_filled"]:
                    for allocation in cycle["allocations"]:
                        price = float(by_day[allocation["ticker"]][day][1]["open"])
                        shadow.cash -= allocation["budget"]
                        shadow.shares[allocation["ticker"]] += allocation["budget"] / price
                    cycle["shadow_filled"] = True
        for event in action_day.get(day, []):
            for account in [shadow, *accounts.values()]:
                recognize_dividend(account, event, day, tax_mode, float(cfg["dividend_tax_rate"]))
        rf_factor = 1.0
        if session_index:
            cursor = date.fromisoformat(sessions[session_index - 1]) + timedelta(days=1)
            while cursor <= date.fromisoformat(day):
                rf_factor *= rf_daily[cursor.isoformat()]
                cursor += timedelta(days=1)
        for key, account in accounts.items():
            _append_path_v2(paths[key], account, day, close, rf_factor - 1)
        if session_index == 0 or sessions[session_index - 1][:7] != day[:7]:
            post_contribution(shadow, day, cfg["monthly_contribution"])
            for key in whole_keys:
                _apply_flow_v2(paths[key], accounts[key], day, cfg["monthly_contribution"])
            indicator_values = {}
            for ticker in EXPECTED:
                located = by_day[ticker].get(day)
                if located is not None and located[0] >= 209:
                    indicator_values[ticker] = indicators(prices[ticker], located[0])
            allocations, unassigned, events = select_allocations(
                shadow, (accounts[key] for key in whole_keys), close, targets,
                destination_order, indicator_values, caps, look,
                cfg["monthly_contribution"], cfg["protected_weight"], cfg["minimum_lot"],
            )
            constraint_events.extend({"selection_date": day, **event} for event in events)
            active = sessions[session_index + 1] if session_index + 1 < len(sessions) else None
            next_month = next((candidate for candidate in sessions[session_index + 1:] if candidate[:7] != day[:7]), None)
            expiry = sessions[sessions.index(next_month) - 1] if next_month else sessions[-1]
            alloc_digest = hashlib.sha256(canonical([{"ticker": row["ticker"], "budget": row["budget"]} for row in allocations])).hexdigest()
            identities = {f"{arm}|{bps}": alloc_digest for arm in ARMS for bps in cfg["friction_bps"]}
            if len(set(identities.values())) != 1:
                raise StudyError("selector allocation identity failed")
            cycles.append({
                "selection_date": day, "active": active, "expiry": expiry,
                "allocations": allocations, "unassigned": unassigned,
                "allocation_sha256_by_cell": identities, "shadow_filled": False,
            })
            for arm in ARMS:
                for bps in cfg["friction_bps"]:
                    allocated = defaultdict(float)
                    for allocation in allocations:
                        allocated[allocation["segment"]] += allocation["budget"]
                    for scope, amount in allocated.items():
                        key = cell_key(arm, bps, scope)
                        _apply_flow_v2(paths[key], accounts[key], day, amount)
            if active:
                for allocation in allocations:
                    ticker = allocation["ticker"]
                    sma50 = allocation["indicators"]["sma50"]
                    levels = {
                        "A_ATR": [sma50 - allocation["indicators"]["atr14"], sma50 - 2 * allocation["indicators"]["atr14"], max(sma50 - 3 * allocation["indicators"]["atr14"], allocation["indicators"]["sma200"])],
                        "B_FIXED": [sma50 * .95, sma50 * .90, sma50 * .85],
                    }
                    for bps in cfg["friction_bps"]:
                        immediate = {"arm": "C_IMMEDIATE", "bps": bps, "ticker": ticker, "budget": allocation["budget"], "limit": None, "active": active, "expiry": active, "selection_date": day, "segment": allocation["segment"], "status": "pending"}
                        pending.append(immediate); orders.append(immediate)
                        for arm in ("A_ATR", "B_FIXED"):
                            for rung, level in enumerate(levels[arm], 1):
                                order = {"arm": arm, "bps": bps, "ticker": ticker, "rung": rung, "budget": allocation["budget"] / 3, "limit": level, "active": active, "expiry": expiry, "selection_date": day, "segment": allocation["segment"], "status": "pending"}
                                pending.append(order); orders.append(order)
        whole_navs = {(arm, bps): accounts[cell_key(arm, bps)].nav(close) for arm in ARMS for bps in cfg["friction_bps"]}
        for (arm, bps, scope), account in accounts.items():
            row = paths[cell_key(arm, bps, scope)][-1]
            row["cash"] = account.cash
            row["postflow_nav"] = account.nav(close)
            row["price_only_postflow_nav"] = account.price_only_nav(close)
            row["whole_nav"] = whole_navs[(arm, bps)]
        for account in [shadow, *accounts.values()]:
            account.prior_shares = dict(account.shares)
    if pending:
        raise StudyError("orders unresolved at simulation end")
    return {"paths": paths, "accounts": accounts, "cycles": cycles, "first_eligible": first_eligible, "orders": orders, "constraint_events": constraint_events, "tax_mode": tax_mode}


def _sum_fields(rows: Iterable[Mapping[str, Any]], fields: Iterable[str]) -> dict[str, float]:
    return {field_name: sum(float(row.get(field_name, 0.0)) for row in rows) for field_name in fields}


def _metric_row(
    result: Mapping[str, Any], cfg: Mapping[str, Any], arm: str, bps: int,
    scope: str, window_name: str, start: str, end: str,
) -> dict[str, Any]:
    key = cell_key(arm, bps, scope)
    path = result["paths"][key]
    rows = [row for row in path if start <= row["date"] <= end]
    if len(rows) < 2:
        raise StudyError(f"insufficient {scope} observations in {window_name}")
    index = [row["index"] / rows[0]["index"] for row in rows]
    price_index = [row["price_only_index"] / rows[0]["price_only_index"] for row in rows]
    returns = [row["return"] for row in rows[1:]]
    risk_free = [row["risk_free_return"] for row in rows[1:]]
    cumulative = index[-1] - 1
    price_only = price_index[-1] - 1
    elapsed = (date.fromisoformat(rows[-1]["date"]) - date.fromisoformat(rows[0]["date"])).days
    annualized = (1 + cumulative) ** (365.2425 / elapsed) - 1 if elapsed and 1 + cumulative > 0 else None
    peak = index[0]
    max_drawdown = 0.0
    for value in index:
        peak = max(peak, value)
        max_drawdown = min(max_drawdown, value / peak - 1)
    volatility = statistics.stdev(returns) * math.sqrt(252) if len(returns) > 1 else None
    excess = [value - rf for value, rf in zip(returns, risk_free)]
    excess_std = statistics.stdev(excess) if len(excess) > 1 else 0.0
    sharpe = statistics.mean(excess) / excess_std * math.sqrt(252) if excess_std else None
    account: Account = result["accounts"][key]
    fills = [row for row in account.fills if start <= row["date"] <= end]
    dividends = [row for row in account.dividend_events if start <= row["ex_date"] <= end]
    settlements = [row for row in account.settlement_events if start <= row["date"] <= end]
    applicable_orders = [
        order for order in result["orders"]
        if order["arm"] == arm and order["bps"] == bps
        and (scope == "whole" or order["segment"] == scope)
        and start <= order["resolution_date"] <= end
    ]
    expired = [order for order in applicable_orders if order["status"] == "expired"]
    deployment_days = [
        (date.fromisoformat(row["date"]) - date.fromisoformat(row["selection_date"])).days
        for row in fills
    ]
    capital_days = sum(
        float(order["budget"]) * ((date.fromisoformat(order["resolution_date"]) - date.fromisoformat(order["active"])).days + 1)
        for order in applicable_orders
    )
    events = [
        event for event in result["constraint_events"]
        if start <= event["selection_date"] <= end
        and (scope == "whole" or event["segment"] == scope)
    ]
    constraints = {
        kind: {
            outcome: sum(1 for event in events if event["constraint"] == kind and event["outcome"] == outcome)
            for outcome in ("clip", "block")
        }
        for kind in ("cluster", "effective_issuer", "common_driver")
    }
    target_doc = yaml.safe_load((ROOT / "targets.yaml").read_text())
    targets = {row["ticker"]: float(row["target_pct"]) / 100 for row in target_doc["destination"] if row["ticker"] in EXPECTED}
    max_weight = 0.0
    max_deviation = 0.0
    scope_tickers = [ticker for ticker in EXPECTED if scope == "whole" or segment(ticker) == scope]
    for row in rows:
        denominator = row["whole_nav"]
        if denominator <= 0:
            continue
        for ticker in scope_tickers:
            value = row["position_values"].get(ticker, 0.0)
            weight = value / denominator
            max_weight = max(max_weight, weight)
            max_deviation = max(max_deviation, abs(weight - targets[ticker]))
    cycles = [
        cycle for cycle in result["cycles"] if start <= cycle["selection_date"] <= end
        and any(scope == "whole" or allocation["segment"] == scope for allocation in cycle["allocations"])
    ]
    dividend_totals = _sum_fields(
        dividends,
        ("gross", "source_withholding", "tentative_us_tax", "foreign_tax_credit", "residual_us_tax", "total_tax", "net"),
    )
    return {
        "arm": arm, "cost_bps": bps, "scope": scope, "window": window_name,
        "observations": len(rows), "attributed_cycles": len(cycles),
        "segment_veto_eligible": scope == "whole" or len(cycles) >= 12,
        "cumulative_twr": cumulative, "annualized_twr": annualized,
        "max_drawdown": max_drawdown, "annualized_volatility": volatility,
        "sharpe": sharpe, "ending_value": rows[-1]["preflow_nav"],
        "cumulative_contributions": sum(row["amount"] for row in account.contributions if start <= row["date"] <= end),
        "time_weighted_cash_pct": statistics.mean(row["cash"] / row["postflow_nav"] if row["postflow_nav"] else 1.0 for row in rows),
        "cash_drag": None, "transaction_count": len(fills),
        "deployed_dollars": sum(row["notional"] for row in fills),
        "transaction_cost": sum(row["cost"] for row in fills),
        "median_deployment_days": statistics.median(deployment_days) if deployment_days else None,
        "unfilled_dollars": sum(float(order["budget"]) for order in expired),
        "unfilled_capital_days": capital_days,
        "dividends": dividend_totals,
        "settlements": {**_sum_fields(settlements, ("net",)), "event_count": len(settlements)},
        "ending_receivables": rows[-1]["receivables"],
        "ending_receivables_by_ticker": rows[-1]["receivables_by_ticker"],
        "price_only_cumulative_twr": price_only,
        "max_single_name_weight": max_weight,
        "max_target_deviation": max_deviation,
        "constraint_counts": constraints,
    }


def metrics(result: Mapping[str, Any], cfg: Mapping[str, Any]) -> dict[str, Any]:
    output = {}
    for arm in ARMS:
        for bps in cfg["friction_bps"]:
            for scope in SCOPES:
                for window_name, (start, end) in WINDOWS.items():
                    key = f"{arm}|{bps}|{scope}|{window_name}"
                    output[key] = _metric_row(result, cfg, arm, bps, scope, window_name, start, end)
    for bps in cfg["friction_bps"]:
        for scope in SCOPES:
            for window_name in WINDOWS:
                immediate = output[f"C_IMMEDIATE|{bps}|{scope}|{window_name}"]["cumulative_twr"]
                for arm in ARMS:
                    output[f"{arm}|{bps}|{scope}|{window_name}"]["cash_drag"] = immediate - output[f"{arm}|{bps}|{scope}|{window_name}"]["cumulative_twr"]
    return output


def bootstrap(paths: Mapping[tuple[str, int, str], list[dict[str, Any]]], cfg: Mapping[str, Any]) -> list[dict[str, Any]]:
    output = []
    count = int(cfg["bootstrap"]["resamples"])
    mean_block = int(cfg["bootstrap"]["mean_block_sessions"])
    for bps in cfg["friction_bps"]:
        window = {
            arm: [row["return"] for row in paths[cell_key(arm, bps)] if "2024-04-02" <= row["date"] <= "2026-07-31"][1:]
            for arm in ARMS
        }
        lengths = {len(values) for values in window.values()}
        if len(lengths) != 1 or not next(iter(lengths)):
            raise StudyError("bootstrap path alignment failed")
        n = next(iter(lengths))
        for challenger in ARMS:
            for baseline in ARMS:
                if challenger == baseline:
                    continue
                seed = int.from_bytes(hashlib.sha256(f"20260907|{challenger}|{baseline}".encode()).digest()[:8], "big")
                rng = random.Random(seed)
                wins = 0
                for _ in range(count):
                    cursor = rng.randrange(n)
                    challenger_value = baseline_value = 1.0
                    for draw in range(n):
                        if draw:
                            cursor = rng.randrange(n) if rng.random() < 1 / mean_block else (cursor + 1) % n
                        challenger_value *= 1 + window[challenger][cursor]
                        baseline_value *= 1 + window[baseline][cursor]
                    wins += challenger_value > baseline_value
                output.append({
                    "challenger": challenger, "baseline": baseline, "cost_bps": bps,
                    "probability_challenger_exceeds": wins / count, "resamples": count,
                    "mean_block_sessions": mean_block, "seed": seed,
                })
    return output


def evaluate_gates(metric: Mapping[str, Any], bootstrap_rows: list[dict[str, Any]], cfg: Mapping[str, Any]) -> dict[str, Any]:
    probabilities = {(row["challenger"], row["baseline"], row["cost_bps"]): row["probability_challenger_exceeds"] for row in bootstrap_rows}
    pairwise = []
    winners = []
    for challenger in ARMS:
        challenger_pass = True
        for baseline in ARMS:
            if challenger == baseline:
                continue
            cells = []
            for bps in cfg["friction_bps"]:
                left = metric[f"{challenger}|{bps}|whole|holdout"]
                right = metric[f"{baseline}|{bps}|whole|holdout"]
                twr_delta = left["annualized_twr"] - right["annualized_twr"]
                drawdown_delta = left["max_drawdown"] - right["max_drawdown"]
                cells.append({"cost_bps": bps, "annualized_twr_delta": twr_delta, "max_drawdown_delta": drawdown_delta, "passed": twr_delta > .01 and drawdown_delta >= -.01})
            probability = probabilities[(challenger, baseline, cfg["decision_friction_bps"])]
            passed = all(cell["passed"] for cell in cells) and probability >= .90
            pairwise.append({"challenger": challenger, "baseline": baseline, "cells": cells, "bootstrap_probability": probability, "passed": passed})
            challenger_pass &= passed
        if challenger_pass:
            winners.append(challenger)
    leader = max(ARMS, key=lambda arm: metric[f"{arm}|{cfg['decision_friction_bps']}|whole|holdout"]["annualized_twr"])
    return {"winners": winners, "apparent_decision_cell_leader": leader, "pairwise_gates": pairwise}


def disposition(metric: Mapping[str, Any], bootstrap_rows: list[dict[str, Any]], sensitivities: Mapping[str, Mapping[str, Any]], cfg: Mapping[str, Any]) -> dict[str, Any]:
    base = evaluate_gates(metric, bootstrap_rows, cfg)
    winners = base["winners"]
    status = "INVALID" if len(winners) > 1 else "RETAIN_BASELINE"
    if winners == ["A_ATR"]:
        status = "STRONGER_EVIDENCE_FOR_A"
    elif winners:
        status = f"RECOMMEND_{winners[0]}_FOR_SEPARATE_GOVERNANCE"
    segment_vetoes = []
    if winners and winners[0] != "A_ATR":
        challenger = winners[0]
        for scope in SCOPES[1:]:
            left = metric[f"{challenger}|10|{scope}|holdout"]
            right = metric[f"A_ATR|10|{scope}|holdout"]
            twr_delta = left["annualized_twr"] - right["annualized_twr"]
            drawdown_delta = left["max_drawdown"] - right["max_drawdown"]
            if left["segment_veto_eligible"] and (twr_delta < -.01 or drawdown_delta < -.01):
                segment_vetoes.append({"scope": scope, "annualized_twr_delta": twr_delta, "max_drawdown_delta": drawdown_delta})
        if segment_vetoes:
            status = "RETAIN_BASELINE"
    sensitivity_checks = {}
    baseline_signature = (base["apparent_decision_cell_leader"], tuple((row["challenger"], row["baseline"], row["passed"]) for row in base["pairwise_gates"]))
    for mode, documents in sensitivities.items():
        check = evaluate_gates(documents["metrics"], documents["bootstrap"], cfg)
        signature = (check["apparent_decision_cell_leader"], tuple((row["challenger"], row["baseline"], row["passed"]) for row in check["pairwise_gates"]))
        sensitivity_checks[mode] = {**check, "changes_winner_or_gate": signature != baseline_signature}
        if signature != baseline_signature:
            status = "INSUFFICIENT_EVIDENCE"
    return {
        "status": status, "winning_arms": winners,
        "apparent_decision_cell_leader": base["apparent_decision_cell_leader"],
        "pairwise_gates": base["pairwise_gates"], "segment_vetoes": segment_vetoes,
        "sensitivity_checks": sensitivity_checks,
        "holdout_previously_exposed": True,
        "invalid_predecessor": {"pull_request": 384, "head": "c435243376b1ed761ac4c0f5e69281fcbbce4d45", "use_as_evidence": False},
        "production_change_authorized": False, "advisory_only": True,
        "stage1": "UNARMED_AND_NOT_EXECUTABLE",
    }


def account_events(result: Mapping[str, Any]) -> dict[str, Any]:
    """Retain the event ledgers needed to reproduce every reported metric."""
    output = {}
    for (arm, bps, scope), account in result["accounts"].items():
        output[f"{arm}|{bps}|{scope}"] = {
            "contributions": account.contributions,
            "fills": account.fills,
            "dividend_events": account.dividend_events,
            "settlement_events": account.settlement_events,
        }
    return output


def retained_result(
    paths_doc: Mapping[str, Any], events_doc: Mapping[str, Any],
    cycles: list[dict[str, Any]], orders: list[dict[str, Any]],
    constraints: list[dict[str, Any]],
) -> dict[str, Any]:
    paths = {}
    accounts = {}
    for key, rows in paths_doc.items():
        arm, raw_bps, scope = key.split("|")
        cell = cell_key(arm, int(raw_bps), scope)
        if key not in events_doc:
            raise StudyError(f"missing event ledger: {key}")
        ledger = events_doc[key]
        account = Account()
        for field_name in ("contributions", "fills", "dividend_events", "settlement_events"):
            value = ledger.get(field_name)
            if type(value) is not list:
                raise StudyError(f"invalid event ledger field: {key}/{field_name}")
            setattr(account, field_name, value)
        paths[cell] = rows
        accounts[cell] = account
    expected = {cell_key(arm, bps, scope) for arm in ARMS for bps in (0, 10, 25) for scope in SCOPES}
    if set(paths) != expected or set(accounts) != expected:
        raise StudyError("retained cell matrix is incomplete")
    return {
        "paths": paths, "accounts": accounts, "cycles": cycles,
        "orders": orders, "constraint_events": constraints,
    }


def retained_sensitivity_result(retained: Mapping[str, Any]) -> dict[str, Any]:
    """Rebuild a sensitivity from its own decision and event ledgers."""
    required = {
        "portfolio_paths", "account_events", "cycles", "orders",
        "constraint_events", "metrics", "bootstrap",
    }
    if set(retained) != required:
        raise StudyError("sensitivity retained bundle is incomplete")
    for field_name in ("cycles", "orders", "constraint_events"):
        if type(retained[field_name]) is not list:
            raise StudyError(f"invalid sensitivity ledger: {field_name}")
    return retained_result(
        retained["portfolio_paths"], retained["account_events"],
        retained["cycles"], retained["orders"], retained["constraint_events"],
    )


def isolated_reconstruction() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="ladder-v2-reconstruct-") as temporary:
        isolated_root = Path(temporary)
        destination = isolated_root / "research/buy_ladder_backtest"
        destination.parent.mkdir(parents=True)
        shutil.copytree(STUDY, destination, ignore=shutil.ignore_patterns("execution", "validation", "ladder-v2-*", "__pycache__"))
        shutil.copytree(ROOT / "research/level1_sleeve_robustness/data", isolated_root / "research/level1_sleeve_robustness/data")
        completed = subprocess.run([sys.executable, str(destination / BUILDER.name)], cwd=isolated_root, text=True, capture_output=True)
        if completed.returncode:
            raise StudyError("isolated LADDER-0003 reconstruction failed: " + completed.stderr.strip())
        artifacts = {}
        for name in ("input_disposition.json", "corporate_actions.json", "yahoo_action_crosscheck.json"):
            rebuilt = destination / "inputs" / name
            retained = STUDY / "inputs" / name
            if rebuilt.read_bytes() != retained.read_bytes():
                raise StudyError(f"isolated reconstruction mismatch: {name}")
            artifacts[name] = sha(retained)
        return {"status": "EXACT_BYTE_IDENTITY_VERIFIED", "builder_sha256": sha(BUILDER), "artifacts": artifacts}


def bundle(cfg: Mapping[str, Any], include_holdout: bool) -> dict[str, Any]:
    input_disposition = read_json(DISPOSITION)
    paths = [CONFIG, PROTOCOL, AMENDMENT, DISPOSITION, ACTIONS, BUILDER, CORRECTIVE_DECISION, Path(__file__), ROOT / "targets.yaml", ROOT / "gates.yaml", ROOT / "issuer_lookthrough.yaml"]
    paths.extend(ROOT / relative for relative in cfg["configuration_hashes"])
    paths.extend(ROOT / relative for relative in cfg["support_hashes"])
    paths.extend(ROOT / row["path"] for row in input_disposition["price_files"])
    paths = list(dict.fromkeys(paths))
    return {
        "schema_version": "2.1", "study_id": cfg["study_id"],
        "code_commit": code_commit(),
        "runtime": {"python": sys.version.split()[0], "packages": {"PyYAML": importlib.metadata.version("PyYAML")}},
        "files": {str(path.relative_to(ROOT)): sha(path) for path in paths},
        "selected_prices": [{key: row[key] for key in ("ticker", "path", "sha256", "provider", "adjustment", "first_observation", "last_observation", "total_row_count")} for row in input_disposition["price_files"]],
        "holdout_results_emitted": include_holdout, "holdout_previously_exposed": True,
        "corrective_authority": "LADDER-0004", "seed": cfg["bootstrap"]["seed"],
        "advisory_only": True, "stage1": "UNARMED_AND_NOT_EXECUTABLE",
    }


def validate() -> dict[str, Any]:
    cfg, prices, sessions, actions = load_inputs()
    reconstruction = isolated_reconstruction()
    for ticker, rows in prices.items():
        candidates = [i for i, row in enumerate(rows) if row["date"] <= "2023-12-29" and i >= 209]
        if not candidates and ticker not in ("CEG", "GEV"):
            raise StudyError(f"{ticker}: no context indicator window")
        for index in candidates[::max(1, len(candidates) // 5)]:
            if not all(math.isfinite(value) for value in indicators(rows, index)):
                raise StudyError(f"{ticker}: nonfinite context indicator")
    receipt = bundle(cfg, False)
    receipt.update({
        "validation_scope": "INPUT_RECONSTRUCTION_AND_NON_HOLDOUT_INVARIANTS_ONLY",
        "reconstruction": reconstruction, "validated_tickers": list(EXPECTED),
        "first_eligible_decision_dates": first_eligible_decision_dates(prices, cfg),
        "session_count": len(sessions), "action_count": sum(map(len, actions.values())),
        "holdout_metrics": None, "disposition": None,
    })
    RECEIPT.parent.mkdir(exist_ok=True)
    RECEIPT.write_bytes(canonical(receipt))
    return receipt


def _report(decision: Mapping[str, Any], metric: Mapping[str, Any]) -> bytes:
    lines = [
        "# Corrective canonical buy-ladder comparison", "",
        f"Disposition: **{decision['status']}**", "",
        "This is advisory research only. It is not a current buy list, order, trade, target change, or automatic policy adoption.", "",
        "## Voting holdout at 10 bps", "",
        "| Arm | Annualized TWR | Maximum drawdown |", "|---|---:|---:|",
    ]
    for arm in ARMS:
        row = metric[f"{arm}|10|whole|holdout"]
        lines.append(f"| {arm} | {row['annualized_twr']:.2%} | {row['max_drawdown']:.2%} |")
    lines.extend(["", "## Segment divergence", "", "| Segment | 10 bps TWR leader | Veto-eligible cycles |", "|---|---|---:|"])
    for scope in SCOPES[1:]:
        leader = max(ARMS, key=lambda arm: metric[f"{arm}|10|{scope}|holdout"]["annualized_twr"])
        cycles = metric[f"{leader}|10|{scope}|holdout"]["attributed_cycles"]
        lines.append(f"| {scope} | {leader} | {cycles} |")
    lines.extend([
        "", "## Decision controls", "",
        f"Pairwise winner(s): {', '.join(decision['winning_arms']) or 'none'}.",
        f"Apparent 10 bps leader: {decision['apparent_decision_cell_leader']}.",
        f"Eligible segment vetoes: {len(decision['segment_vetoes'])}.",
        f"Tax sensitivities changing a winner or gate: {sum(1 for row in decision['sensitivity_checks'].values() if row['changes_winner_or_gate'])}.", "",
        "The historical earnings blackout is omitted identically because the repository has no complete point-in-time calendar.",
        "The voting holdout was exposed by invalid PR #384; that preliminary result is excluded and cannot confirm or veto this corrected result.",
        "Stage 1 remains **UNARMED AND NOT EXECUTABLE**.", "",
    ])
    return ("\n".join(lines) + "\n").encode()


def validate_documents(documents: Mapping[str, bytes], cfg: Mapping[str, Any]) -> None:
    required = {"metrics.json", "bootstrap.json", "sensitivities.json", "cycles.json", "orders.json", "constraint_events.json", "portfolio_paths.json", "account_events.json", "disposition.json", "input_manifest.json", "REPORT.md"}
    if set(documents) != required:
        raise StudyError("output bundle is incomplete")
    decoded = {name: json.loads(payload) for name, payload in documents.items() if name.endswith(".json")}
    if len(decoded["metrics.json"]) != len(ARMS) * len(cfg["friction_bps"]) * len(SCOPES) * len(WINDOWS):
        raise StudyError("metric matrix is incomplete")
    for cycle in decoded["cycles.json"]:
        if len(set(cycle["allocation_sha256_by_cell"].values())) != 1 or len(cycle["allocation_sha256_by_cell"]) != len(ARMS) * len(cfg["friction_bps"]):
            raise StudyError("retained selector identity failed")
    reconstructed = retained_result(
        decoded["portfolio_paths.json"], decoded["account_events.json"],
        decoded["cycles.json"], decoded["orders.json"], decoded["constraint_events.json"],
    )
    if canonical(metrics(reconstructed, cfg)) != documents["metrics.json"]:
        raise StudyError("retained main metrics do not independently recompute")
    if canonical(bootstrap(reconstructed["paths"], cfg)) != documents["bootstrap.json"]:
        raise StudyError("retained main bootstrap does not independently recompute")
    for mode, retained in decoded["sensitivities.json"].items():
        sensitivity_result = retained_sensitivity_result(retained)
        if metrics(sensitivity_result, cfg) != retained["metrics"]:
            raise StudyError(f"{mode}: retained metrics do not independently recompute")
        if bootstrap(sensitivity_result["paths"], cfg) != retained["bootstrap"]:
            raise StudyError(f"{mode}: retained bootstrap does not independently recompute")
    sensitivity_inputs = {
        mode: {"metrics": retained["metrics"], "bootstrap": retained["bootstrap"]}
        for mode, retained in decoded["sensitivities.json"].items()
    }
    recomputed_decision = disposition(
        decoded["metrics.json"], decoded["bootstrap.json"], sensitivity_inputs, cfg,
    )
    if recomputed_decision != decoded["disposition.json"]:
        raise StudyError("retained disposition does not independently recompute")
    if documents["REPORT.md"] != _report(recomputed_decision, decoded["metrics.json"]):
        raise StudyError("retained narrative does not independently recompute")
    manifest = decoded["input_manifest.json"]
    for name in required - {"input_manifest.json"}:
        if manifest["outputs"].get(name) != hashlib.sha256(documents[name]).hexdigest():
            raise StudyError(f"output hash mismatch: {name}")
    decision = decoded["disposition.json"]
    if decision["production_change_authorized"] is not False or decision["stage1"] != "UNARMED_AND_NOT_EXECUTABLE":
        raise StudyError("advisory boundary failure")


def execute() -> dict[str, Any]:
    cfg, prices, sessions, actions = load_inputs()
    if not RECEIPT.is_file():
        raise StudyError("validation receipt missing")
    receipt = read_json(RECEIPT)
    expected = bundle(cfg, False)
    for key in ("code_commit", "runtime", "files", "seed", "advisory_only", "stage1", "corrective_authority", "holdout_previously_exposed"):
        if receipt.get(key) != expected.get(key):
            raise StudyError(f"validation receipt drift: {key}")
    if receipt.get("holdout_results_emitted") is not False or receipt.get("holdout_metrics") is not None or receipt.get("disposition") is not None:
        raise StudyError("validation receipt leaked holdout output")
    if receipt.get("reconstruction", {}).get("status") != "EXACT_BYTE_IDENTITY_VERIFIED":
        raise StudyError("validation reconstruction proof missing")
    main_result = simulate(cfg, prices, sessions, actions)
    main_metrics = metrics(main_result, cfg)
    main_bootstrap = bootstrap(main_result["paths"], cfg)
    sensitivities = {}
    for mode in ("no_credit", "etn_no_exemption"):
        sensitivity = simulate(cfg, prices, sessions, actions, mode)
        sensitivities[mode] = {
            "metrics": metrics(sensitivity, cfg),
            "bootstrap": bootstrap(sensitivity["paths"], cfg),
            "portfolio_paths": {f"{arm}|{bps}|{scope}": value for (arm, bps, scope), value in sensitivity["paths"].items()},
            "account_events": account_events(sensitivity),
            "cycles": sensitivity["cycles"], "orders": sensitivity["orders"],
            "constraint_events": sensitivity["constraint_events"],
        }
    decision = disposition(main_metrics, main_bootstrap, sensitivities, cfg)
    json_values = {
        "metrics.json": main_metrics, "bootstrap.json": main_bootstrap,
        "sensitivities.json": sensitivities, "cycles.json": main_result["cycles"],
        "orders.json": main_result["orders"], "constraint_events.json": main_result["constraint_events"],
        "portfolio_paths.json": {f"{arm}|{bps}|{scope}": value for (arm, bps, scope), value in main_result["paths"].items()},
        "account_events.json": account_events(main_result),
        "disposition.json": decision,
    }
    documents = {name: canonical(value) for name, value in json_values.items()}
    documents["REPORT.md"] = _report(decision, main_metrics)
    manifest = bundle(cfg, True)
    manifest["first_eligible_decision_dates"] = main_result["first_eligible"]
    manifest["outputs"] = {name: hashlib.sha256(payload).hexdigest() for name, payload in documents.items()}
    documents["input_manifest.json"] = canonical(manifest)
    validate_documents(documents, cfg)
    OUTPUT.parent.mkdir(exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix="ladder-v2-output-", dir=STUDY))
    try:
        for name, payload in documents.items():
            (temporary / name).write_bytes(payload)
        if OUTPUT.exists():
            raise StudyError("registered output already exists; rerun prohibited")
        temporary.replace(OUTPUT)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return decision


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("command",choices=("validate","execute")); args=parser.parse_args()
    result=validate() if args.command=="validate" else execute(); print(json.dumps(result,indent=2,sort_keys=True)); return 0


if __name__=="__main__": raise SystemExit(main())
