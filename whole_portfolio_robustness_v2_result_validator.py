#!/usr/bin/env python3
"""Independent recomputation of V2 synthetic result ledgers.

No simulation helper is imported: primitive cash, positions, receivables, trades and NAV
records are recomputed directly. Historical validation additionally requires admission.
"""
from __future__ import annotations
import json, math, random
from decimal import Decimal as D, localcontext
from pathlib import Path
from typing import Any

ALTS=("BROAD_PLUS_5","DEFENSIVE_PLUS_5","CRYPTO_HALF","GOLD_PLUS_2","DIVERSIFIED_BALANCE")
CASES=("STANDARD_AVAILABLE_CREDIT","ZERO_FOREIGN_TAX_CREDIT","ETN_25_PERCENT_IRISH_WITHHOLDING","JOINT_ZERO_CREDIT_AND_ETN_25_PERCENT_IRISH_WITHHOLDING")

def _finite(x:Any)->bool:
    return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)

def recompute_metrics(rows:list[dict])->dict[str,float]:
    nav=[100000.0]+[float(x["nav"]) for x in rows]
    if len(nav)<2 or any(not math.isfinite(x) or x<=0 for x in nav): raise ValueError("invalid NAV path")
    returns=[nav[i]/nav[i-1]-1 for i in range(1,len(nav))]
    cumulative=nav[-1]/nav[0]-1; peak=nav[0]; mdd=0
    for x in nav: peak=max(peak,x);mdd=min(mdd,x/peak-1)
    return {"cumulative_twr":cumulative,"max_drawdown":mdd,"returns":returns}

def _path_stats(rows:list[dict])->dict[str,float]:
    nav=[100000.]+[float(x["nav"]) for x in rows];ret=[nav[i]/nav[i-1]-1 for i in range(1,len(nav))];rf=[float(x["risk_free_return"]) for x in rows]
    excess=[x-y for x,y in zip(ret,rf)];mean=sum(excess)/len(excess);var=sum((x-mean)**2 for x in excess)/(len(excess)-1);down=(sum(min(x,0)**2 for x in excess)/len(excess))**.5
    if var<=0 or down<=0:raise ValueError("undefined path risk metric")
    peak=nav[0];mdd=0
    for x in nav:peak=max(peak,x);mdd=min(mdd,x/peak-1)
    tail=sorted(ret)[:max(1,math.ceil(.05*len(ret)))]
    return {"net_twr_cagr":(nav[-1]/nav[0])**(252/len(ret))-1,"sharpe":mean/math.sqrt(var)*math.sqrt(252),"sortino":mean/down*math.sqrt(252),"max_drawdown":mdd,"daily_cvar_95":sum(tail)/len(tail)}

def _paired_delta(base:list[dict],alt:list[dict])->dict[str,float]:
    if [x["date"] for x in base]!=[x["date"] for x in alt]:raise ValueError("unpaired paths")
    b=_path_stats(base);a=_path_stats(alt)
    return {"net_cagr_delta_pp":100*(a["net_twr_cagr"]-b["net_twr_cagr"]),"sharpe_delta":a["sharpe"]-b["sharpe"],"sortino_delta":a["sortino"]-b["sortino"],"max_drawdown_delta_pp":100*(a["max_drawdown"]-b["max_drawdown"]),"daily_cvar_95_delta_pp":100*(a["daily_cvar_95"]-b["daily_cvar_95"])}

def _bootstrap(base:list[dict],alt:list[dict])->dict[str,float]:
    br=[float(base[i]["nav"])/float(base[i-1]["nav"])-1 for i in range(1,len(base))]
    ar=[float(alt[i]["nav"])/float(alt[i-1]["nav"])-1 for i in range(1,len(alt))];rf=[float(x["risk_free_return"]) for x in base][1:]
    rng=random.Random(20260907);counts={k:0 for k in ("NET_TWR_CAGR_DELTA","SHARPE_DELTA","MAX_DRAWDOWN_DELTA","DAILY_CVAR_95_DELTA")};n=len(br)
    for _ in range(2000):
        idx=[];j=rng.randrange(n)
        while len(idx)<n:idx.append(j);j=(j+1)%n if rng.random()>1/21 else rng.randrange(n)
        def stat(ret):
            ex=[ret[i]-rf[i] for i in idx];mean=sum(ex)/n;var=sum((x-mean)**2 for x in ex)/(n-1);nav=1.;peak=1.;mdd=0;sample=[ret[i] for i in idx]
            for x in sample:nav*=1+x;peak=max(peak,nav);mdd=min(mdd,nav/peak-1)
            return nav**(252/n)-1,mean/math.sqrt(var)*math.sqrt(252),mdd,sum(sorted(sample)[:max(1,math.ceil(.05*n))])/max(1,math.ceil(.05*n))
        b=stat(br);a=stat(ar)
        for k,v in zip(counts,(a[0]-b[0],a[1]-b[1],a[2]-b[2],a[3]-b[3])):counts[k]+=v>0
    return {k:v/2000 for k,v in counts.items()}

def validate_ledger(doc:dict)->list[str]:
    e=[]; rows=doc.get("ledger"); primitive_rows=[]
    if not isinstance(rows,list):return ["ledger missing"]
    last=None; last_cash=D("100000"); last_shares={}; calendar=doc.get("calendar_ledger")
    if str(doc.get("initial_nav"))!="100000":e.append("initial NAV must be 100000")
    for i,r in enumerate(rows):
        try:
            cash=D(str(r["cash"])); recv=sum((D(str(x["net"])) for x in r.get("receivables",[])),D(0))
            positions=sum((D(str(x["shares"]))*D(str(x["price"])) for x in r.get("positions",[])),D(0))
            nav=cash+recv+positions
            primitive_rows.append({"nav":str(nav)})
            if nav!=D(str(r["nav"])):e.append(f"row {i}: NAV does not reconcile")
            if cash<0:e.append(f"row {i}: borrowing/negative cash")
            if D(str(r.get("external_flow","0"))):e.append(f"row {i}: external flow prohibited")
            if calendar is None and last_cash is not None:
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
    if not isinstance(calendar,list):e.append("complete calendar ledger missing")
    else:
        cash=D("100000");pending=D(0);shares={};sessions={r["date"]:r for r in rows};profile=doc.get("cell",{}).get("profile",{});cost_bps=D(str(doc.get("cell",{}).get("cost_bps","NaN")))
        ordinary=D(str(profile.get("ordinary_income_rate","NaN")))
        for i,row in enumerate(calendar):
            try:
                credited=D(str(row["interest_credited"]));opening=D(str(row["opening_eligible_cash"]));rate=D(str(row["dff_percent"]));
                if abs(credited-pending)>D("1e-18") or abs(opening-(cash+credited))>D("1e-18"):e.append(f"calendar row {i}: cash clock mismatch")
                cash=opening
                for event in row.get("events",[]):
                    kind=event.get("type")
                    if kind=="buy":
                        units=D(str(event["units"]));notional=D(str(event["notional"]));price=D(str(sessions[row["date"]]["positions"][[x["ticker"] for x in sessions[row["date"]]["positions"]].index(event["ticker"])]["price"]))
                        if abs(notional-units*price)>D("1e-18") or abs(D(str(event["cost"]))-notional*cost_bps/D(10000))>D("1e-18"):e.append(f"calendar row {i}: buy economics mismatch")
                        cash-=notional+D(str(event["cost"]));shares[event["ticker"]]=shares.get(event["ticker"],D(0))+units
                    elif kind=="sell":
                        units=D(str(event["units"]));proceeds=D(str(event["proceeds"]));
                        if abs(D(str(event["cost"]))-proceeds*cost_bps/D(10000))>D("1e-18") or D(str(event["tax"]))<0:e.append(f"calendar row {i}: sell economics mismatch")
                        cash+=proceeds-D(str(event["cost"]))-D(str(event["tax"]));shares[event["ticker"]]-=units
                    elif kind=="receivable_settlement":cash+=D(str(event["net"]))
                    elif kind=="split":
                        if event.get("unit_basis")!="SPLIT_NORMALIZED_NO_POSITION_MUTATION" or D(str(event["factor"]))<=0:e.append(f"calendar row {i}: invalid split normalization")
                    elif kind in {"dividend_recognition","rebalance"}:pass
                    else:e.append(f"calendar row {i}: unknown event")
                if abs(cash-D(str(row["settled_cash"])))>D("1e-18"):e.append(f"calendar row {i}: unexplained cash transition")
                if row["date"] in sessions:
                    if abs(D(str(sessions[row["date"]]["cash"]))-cash)>D("1e-18"):e.append(f"calendar row {i}: valuation cash mismatch")
                    actual={x["ticker"]:D(str(x["shares"])) for x in sessions[row["date"]].get("positions",[])}
                    if set(shares)!=set(actual) or any(abs(shares[x]-actual[x])>D("1e-18") for x in shares):e.append(f"calendar row {i}: position replay mismatch")
                with localcontext() as ctx:
                    ctx.prec=60;gross=rate/D(100);pending=opening*(gross-max(gross,D(0))*ordinary-D(".0025"))/D(360)
            except Exception as ex:e.append(f"calendar row {i}: malformed evidence: {ex}")
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
    paths=doc.get("portfolio_paths")
    if not isinstance(paths,dict) or set(paths)!=set(CASES):errors.append("complete paired primitive portfolio paths missing")
    else:
        expected_cells={f"COST_{c}_TAX_{t}_CADENCE_{q}" for c in ("0","10","25") for t in ("TAX_DEFERRED","TAXABLE_MID","TAXABLE_HIGH") for q in ("QUARTERLY","ANNUAL")}
        for case,cell_map in paths.items():
            if set(cell_map)!=expected_cells:errors.append(f"{case}: primitive cell paths missing");continue
            for cell,variants in cell_map.items():
                if set(variants)!={"BASELINE",*ALTS}:errors.append(f"{case}/{cell}: primitive variant paths missing");continue
                for variant,windows in variants.items():
                    if set(windows)!={"full","context","correction_replication"}:errors.append(f"{case}/{cell}/{variant}: primitive windows missing");continue
                    bounds={"full":("2021-06-01","2026-07-31"),"context":("2021-06-01","2023-12-29"),"correction_replication":("2024-04-02","2026-07-31")}
                    for window,(start,end) in bounds.items():
                        dates=[x.get("date") for x in windows[window]]
                        if not dates or dates[0]!=start or dates[-1]!=end or dates!=sorted(set(dates)) or any(not _finite(float(x.get("risk_free_return",float("nan")))) for x in windows[window]):errors.append(f"{case}/{cell}/{variant}/{window}: invalid dated primitives")
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
                        if any(x.get("window")!="correction_replication" or not all(finite(x.get(k)) for k in ("net_cagr_delta_pp","sharpe_delta","sortino_delta","max_drawdown_delta_pp","daily_cvar_95_delta_pp")) for x in cells):raise ValueError("nonfinite or wrong-window cell evidence")
                        primary=detail["primary"]["correction_replication"];context=detail["primary"]["context"];boot=detail["bootstrap"]
                        by_id={x["cell_id"]:x for x in cells}
                        for identity in evidence["cell_ids"]:
                            actual=_paired_delta(paths[case][identity]["BASELINE"]["correction_replication"],paths[case][identity][alt]["correction_replication"])
                            if any(abs(actual[k]-by_id[identity][k])>1e-10 for k in actual):raise ValueError("cell metric/path mismatch")
                        primary_id="COST_10_TAX_TAXABLE_MID_CADENCE_QUARTERLY"
                        actual_context=_paired_delta(paths[case][primary_id]["BASELINE"]["context"],paths[case][primary_id][alt]["context"])
                        if any(abs(actual_context[k]-context[k])>1e-10 for k in actual_context):raise ValueError("context metric/path mismatch")
                        if not all(finite(x.get(k)) for x in (primary,context) for k in ("net_cagr_delta_pp","sharpe_delta","sortino_delta","max_drawdown_delta_pp","daily_cvar_95_delta_pp")):raise ValueError("nonfinite primary/context evidence")
                        if not all(finite(boot[k]) and 0<=boot[k]<=1 for k in ("SHARPE_DELTA","MAX_DRAWDOWN_DELTA","DAILY_CVAR_95_DELTA")):raise ValueError("bootstrap")
                        actual_boot=_bootstrap(paths[case][primary_id]["BASELINE"]["correction_replication"],paths[case][primary_id][alt]["correction_replication"])
                        if any(actual_boot[k]!=boot[k] for k in actual_boot):raise ValueError("bootstrap/path mismatch")
                        linked=(primary["max_drawdown_delta_pp"]>=2 and context["max_drawdown_delta_pp"]>=0 and boot["MAX_DRAWDOWN_DELTA"]>=.75) or (primary["daily_cvar_95_delta_pp"]>=.1 and context["daily_cvar_95_delta_pp"]>=0 and boot["DAILY_CVAR_95_DELTA"]>=.75)
                        passed=sum(support(x) for x in cells)>=15 and support(primary) and all(context[k]>=0 for k in ("net_cagr_delta_pp","sharpe_delta","sortino_delta")) and boot["SHARPE_DELTA"]>=.75 and linked and detail["regime_pass"] is True and detail["concentration_pass"] is True
                        named={"support_15_of_18":sum(support(x) for x in cells)>=15,"primary":support(primary),"context_direction":all(context[k]>=0 for k in ("net_cagr_delta_pp","sharpe_delta","sortino_delta")),"bootstrap_sharpe":boot["SHARPE_DELTA"]>=.75,"regimes":detail["regime_pass"] is True,"concentration":detail["concentration_pass"] is True,"linked_tail":linked and sum(support(x) for x in cells)>=15 and support(primary) and detail["regime_pass"] is True and detail["concentration_pass"] is True,"final":passed}
                        if detail.get("gates")!=named:errors.append(f"{case}/{alt}: named gate vector mismatch")
                        recomputed[case][alt]=passed
                        if detail.get("final") is not passed:errors.append(f"{case}/{alt}: gate summary mismatch")
                    except Exception as ex:errors.append(f"{case}/{alt}: malformed gate evidence: {ex}")
            if recomputed and doc.get("foreign_case_gate_booleans")!=recomputed:errors.append("foreign-case booleans not independently reproducible")
            standard=cases[CASES[0]]
            foreign_named_veto=any(cases[c][a]["gates"]!=standard[a]["gates"] for c in CASES[1:] for a in ALTS)
    calculated=recompute_disposition(doc.get("foreign_case_gate_booleans",{}))
    if locals().get("foreign_named_veto",False):calculated={"disposition":"UNABLE_TO_DETERMINE","passing_set":[]}
    if doc.get("disposition")!=calculated: errors.append("disposition not independently reproducible")
    return errors

def validate_file(path:Path)->list[str]:
    try:return validate_result(json.loads(path.read_text()))
    except Exception as ex:return [f"cannot load result: {ex}"]

def validate_study_bundle(bundle:dict)->list[str]:
    """Replay every simulation and then independently validate the complete decision evidence."""
    errors=[]; simulations=bundle.get("simulations")
    if not isinstance(simulations,dict) or set(simulations)!=set(CASES):return ["complete simulation registry missing"]
    exemplar=None
    for case,cells in simulations.items():
        if set(cells)!=set(bundle.get("decision_evidence",{}).get("cell_ids",[])):errors.append(f"{case}: simulation cell registry mismatch");continue
        for cell,variants in cells.items():
            if set(variants)!={"BASELINE",*ALTS}:errors.append(f"{case}/{cell}: simulation variant registry mismatch");continue
            for variant,simulation in variants.items():
                found=validate_ledger(simulation)
                errors.extend(f"{case}/{cell}/{variant}: {x}" for x in found)
                exemplar=exemplar or simulation
    if exemplar:
        combined={**exemplar,"portfolio_paths":bundle.get("portfolio_paths"),"decision_evidence":bundle.get("decision_evidence"),"foreign_case_gate_booleans":bundle.get("foreign_case_gate_booleans"),"disposition":bundle.get("disposition")}
        errors.extend(validate_result(combined))
    return errors
