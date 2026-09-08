#!/usr/bin/env python3
"""Independent recomputation of V2 synthetic result ledgers.

No simulation helper is imported: primitive cash, positions, receivables, trades and NAV
records are recomputed directly. Historical validation additionally requires admission.
"""
from __future__ import annotations
import json, math
from decimal import Decimal as D
from pathlib import Path
from typing import Any

ALTS=("BROAD_PLUS_5","DEFENSIVE_PLUS_5","CRYPTO_HALF","GOLD_PLUS_2","DIVERSIFIED_BALANCE")
CASES=("STANDARD_AVAILABLE_CREDIT","ZERO_FOREIGN_TAX_CREDIT","ETN_25_PERCENT_IRISH_WITHHOLDING","JOINT_ZERO_CREDIT_AND_ETN_25_PERCENT_IRISH_WITHHOLDING")

def _finite(x:Any)->bool:
    return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)

def recompute_metrics(rows:list[dict])->dict[str,float]:
    nav=[float(x["nav"]) for x in rows]
    if len(nav)<2 or any(not math.isfinite(x) or x<=0 for x in nav): raise ValueError("invalid NAV path")
    returns=[nav[i]/nav[i-1]-1 for i in range(1,len(nav))]
    cumulative=nav[-1]/nav[0]-1; peak=nav[0]; mdd=0
    for x in nav: peak=max(peak,x);mdd=min(mdd,x/peak-1)
    return {"cumulative_twr":cumulative,"max_drawdown":mdd,"returns":returns}

def validate_ledger(doc:dict)->list[str]:
    e=[]; rows=doc.get("ledger"); primitive_rows=[]
    if not isinstance(rows,list):return ["ledger missing"]
    last=None; last_cash=D("100000"); last_shares={}
    if str(doc.get("initial_nav"))!="100000":e.append("initial NAV must be 100000")
    for i,r in enumerate(rows):
        try:
            cash=D(str(r["cash"])); recv=sum((D(str(x["net"])) for x in r.get("receivables",[])),D(0))
            positions=sum((D(str(x["shares"]))*D(str(x["price"])) for x in r.get("positions",[])),D(0))
            nav=cash+recv+positions
            primitive_rows.append({"nav":str(nav)})
            if nav!=D(str(r["nav"])):e.append(f"row {i}: NAV does not reconcile")
            if cash<0:e.append(f"row {i}: borrowing/negative cash")
            if last_cash is not None:
                external=D(str(r.get("external_flow","0")))
                if external:e.append(f"row {i}: external flow prohibited")
                expected=last_cash+D(str(r.get("interest_credited","0")))
                shares=dict(last_shares)
                for event in r.get("events",[]):
                    kind=event.get("type")
                    if kind=="buy":expected-=D(str(event["notional"]))+D(str(event["cost"]));shares[event["ticker"]]=shares.get(event["ticker"],D(0))+D(str(event["units"]))
                    elif kind=="sell":expected+=D(str(event["proceeds"]))-D(str(event["cost"]))-D(str(event["tax"]));shares[event["ticker"]]=shares.get(event["ticker"],D(0))-D(str(event["units"]))
                    elif kind=="receivable_settlement":expected+=D(str(event["net"]))
                    elif kind in {"split","dividend_recognition"}: pass
                    else:e.append(f"row {i}: unknown event")
                if expected!=cash:e.append(f"row {i}: unexplained cash transition")
                actual={x["ticker"]:D(str(x["shares"])) for x in r.get("positions",[])}
                if shares!=actual:e.append(f"row {i}: unexplained position transition")
            last=nav
            last_cash=cash;last_shares={x["ticker"]:D(str(x["shares"])) for x in r.get("positions",[])}
        except Exception as ex:e.append(f"row {i}: malformed primitive: {ex}")
    try:
        calc=recompute_metrics(primitive_rows); claimed=doc["summary"]
        for k in ("cumulative_twr","max_drawdown"):
            if not _finite(claimed.get(k)) or abs(calc[k]-claimed[k])>1e-12:e.append(f"summary {k} mismatch")
    except Exception as ex:e.append(f"metric recomputation failed: {ex}")
    return e

def recompute_disposition(gates:dict[str,dict[str,bool]])->dict:
    if set(gates)!=set(CASES) or any(set(v)!=set(ALTS) or any(type(x) is not bool for x in v.values()) for v in gates.values()):
        return {"disposition":"UNABLE_TO_DETERMINE","passing_set":[]}
    standard=gates[CASES[0]]
    if any(gates[c]!=standard for c in CASES[1:]):return {"disposition":"UNABLE_TO_DETERMINE","passing_set":[]}
    passing=[a for a in ALTS if standard[a]]
    return {"disposition":"RECOMMEND_POLICY_REVIEW" if passing else "RETAIN_BASELINE","passing_set":passing}

def validate_result(doc:dict)->list[str]:
    errors=validate_ledger(doc)
    evidence=doc.get("decision_evidence")
    if not isinstance(evidence,dict) or set(evidence.get("cell_ids",[]))!=set(f"COST_{c}_TAX_{t}_CADENCE_{q}" for c in ("0","10","25") for t in ("TAX_DEFERRED","TAXABLE_MID","TAXABLE_HIGH") for q in ("QUARTERLY","ANNUAL")):
        errors.append("complete registered comparison evidence missing")
    else:
        cases=evidence.get("cases")
        if not isinstance(cases,dict) or set(cases)!=set(CASES):errors.append("complete per-case gate evidence missing")
        else:
            recomputed={}
            for case,variants in cases.items():
                if not isinstance(variants,dict) or set(variants)!=set(ALTS):errors.append(f"{case}: variant evidence missing");continue
                recomputed[case]={}
                for alt,detail in variants.items():
                    try:
                        cells=detail["cells"]
                        if len(cells)!=18 or {x["cell_id"] for x in cells}!=set(evidence["cell_ids"]):raise ValueError("cell evidence")
                        finite=lambda x:isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
                        def support(x):return all(finite(x[k]) for k in ("net_cagr_delta_pp","sharpe_delta","sortino_delta","max_drawdown_delta_pp","daily_cvar_95_delta_pp")) and x["net_cagr_delta_pp"]>=-.5 and x["sharpe_delta"]>=.05 and x["sortino_delta"]>=.05 and (x["max_drawdown_delta_pp"]>=2 or x["daily_cvar_95_delta_pp"]>=.1)
                        primary=detail["primary"]["correction_replication"];context=detail["primary"]["context"];boot=detail["bootstrap"]
                        if not all(finite(boot[k]) and 0<=boot[k]<=1 for k in ("SHARPE_DELTA","MAX_DRAWDOWN_DELTA","DAILY_CVAR_95_DELTA")):raise ValueError("bootstrap")
                        linked=(primary["max_drawdown_delta_pp"]>=2 and context["max_drawdown_delta_pp"]>=0 and boot["MAX_DRAWDOWN_DELTA"]>=.75) or (primary["daily_cvar_95_delta_pp"]>=.1 and context["daily_cvar_95_delta_pp"]>=0 and boot["DAILY_CVAR_95_DELTA"]>=.75)
                        passed=sum(support(x) for x in cells)>=15 and support(primary) and all(context[k]>=0 for k in ("net_cagr_delta_pp","sharpe_delta","sortino_delta")) and boot["SHARPE_DELTA"]>=.75 and linked and detail["regime_pass"] is True and detail["concentration_pass"] is True
                        recomputed[case][alt]=passed
                        if detail.get("final") is not passed:errors.append(f"{case}/{alt}: gate summary mismatch")
                    except Exception as ex:errors.append(f"{case}/{alt}: malformed gate evidence: {ex}")
            if recomputed and doc.get("foreign_case_gate_booleans")!=recomputed:errors.append("foreign-case booleans not independently reproducible")
    calculated=recompute_disposition(doc.get("foreign_case_gate_booleans",{}))
    if doc.get("disposition")!=calculated: errors.append("disposition not independently reproducible")
    return errors

def validate_file(path:Path)->list[str]:
    try:return validate_result(json.loads(path.read_text()))
    except Exception as ex:return [f"cannot load result: {ex}"]
