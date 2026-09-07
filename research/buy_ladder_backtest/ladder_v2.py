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
import statistics
import subprocess
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Mapping

import yaml
import risk_level1_core


ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "research/buy_ladder_backtest"
CONFIG = STUDY / "implementation_config.yaml"
DISPOSITION = STUDY / "inputs/input_disposition.json"
ACTIONS = STUDY / "inputs/corporate_actions.json"
PROTOCOL = STUDY / "PROTOCOL_V2.md"
AMENDMENT = STUDY / "PROTOCOL_V2_FOREIGN_DIVIDEND_AMENDMENT.md"
RECEIPT = STUDY / "validation/validation_receipt.json"
OUTPUT = STUDY / "execution"

ARMS = ("A_ATR", "B_FIXED", "C_IMMEDIATE")
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
        value = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    if len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
        raise StudyError("code commit must be a lowercase 40-character SHA")
    return value


def config() -> dict[str, Any]:
    cfg = yaml.safe_load(CONFIG.read_text())
    if cfg.get("status") != "FROZEN_BEFORE_REGISTERED_EXECUTION" or cfg.get("advisory_only") is not True:
        raise StudyError("implementation status or advisory boundary drift")
    if cfg.get("stage1") != "UNARMED_AND_NOT_EXECUTABLE":
        raise StudyError("Stage 1 boundary drift")
    pins = {PROTOCOL: cfg["protocol_sha256"], AMENDMENT: cfg["amendment_sha256"], DISPOSITION: cfg["input_disposition_sha256"], ACTIONS: cfg["corporate_actions_sha256"]}
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
    overrides = read_json(STUDY / "inputs/price_anomaly_overrides.json")
    override_map = {(x["ticker"], x["date"]): (x["field"], x["accepted_value"])
                    for x in overrides["corrections"]}
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
                field_name, accepted = override_map[(item["ticker"], day)]
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
    actions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen = set()
    for event in actions_doc["events"]:
        key = (event["symbol"], event["action_type"], event["ex_date"], event["id"])
        if key in seen or event["symbol"] not in EXPECTED or not ("2021-06-01" <= event["ex_date"] <= "2026-07-31"):
            raise StudyError("invalid/duplicate corporate action")
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
    costs: float = 0.0
    deployed: float = 0.0
    tx: int = 0
    dividends: dict[str, float] = field(default_factory=lambda: defaultdict(float))
    prior_shares: dict[str, float] = field(default_factory=dict)
    fills: list[dict[str, Any]] = field(default_factory=list)

    def nav(self, close: Mapping[str, float]) -> float:
        return self.cash + sum(self.shares[t] * close[t] for t in self.shares) + sum(x["net"] for x in self.receivables)


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


def simulate(cfg: Mapping[str, Any], prices: Mapping[str, list[dict[str, Any]]], sessions: list[str], actions: Mapping[str, list[dict[str, Any]]], tax_mode: str = "baseline") -> dict[str, Any]:
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


def metrics(result: Mapping[str, Any], cfg: Mapping[str, Any]) -> dict[str, Any]:
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


def bootstrap(paths: Mapping[tuple[str,int],list[dict[str,Any]]], cfg: Mapping[str,Any]) -> list[dict[str,Any]]:
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


def disposition(metric: Mapping[str,Any], boot: list[dict[str,Any]], sensitivities: Mapping[str,Mapping[str,Any]], cfg: Mapping[str,Any]) -> dict[str,Any]:
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


def bundle(cfg: Mapping[str,Any], include_holdout: bool) -> dict[str,Any]:
    disp=read_json(DISPOSITION)
    paths=[CONFIG,PROTOCOL,AMENDMENT,DISPOSITION,ACTIONS,Path(__file__),ROOT/"targets.yaml",ROOT/"gates.yaml",ROOT/"issuer_lookthrough.yaml"]+[ROOT/x["path"] for x in disp["price_files"]]
    return {"schema_version":"2.0","study_id":cfg["study_id"],"code_commit":code_commit(),"runtime":{"python":sys.version.split()[0],"packages":{"PyYAML":importlib.metadata.version("PyYAML")}},"files":{str(p.relative_to(ROOT)):sha(p) for p in paths},"holdout_results_emitted":include_holdout,"seed":cfg["bootstrap"]["seed"],"advisory_only":True,"stage1":"UNARMED_AND_NOT_EXECUTABLE"}


def validate() -> dict[str,Any]:
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


def execute() -> dict[str,Any]:
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


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("command",choices=("validate","execute")); args=parser.parse_args()
    result=validate() if args.command=="validate" else execute(); print(json.dumps(result,indent=2,sort_keys=True)); return 0


if __name__=="__main__": raise SystemExit(main())
