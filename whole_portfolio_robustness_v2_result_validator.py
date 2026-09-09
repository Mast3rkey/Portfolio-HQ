#!/usr/bin/env python3
"""Independent recomputation of V2 synthetic result ledgers.

No simulation helper is imported: primitive cash, positions, receivables, trades and NAV
records are recomputed directly. Historical validation additionally requires admission.
"""
from __future__ import annotations
import json, math, random
import yaml
import numpy as np
from decimal import Decimal as D, localcontext
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ALTS=("BROAD_PLUS_5","DEFENSIVE_PLUS_5","CRYPTO_HALF","GOLD_PLUS_2","DIVERSIFIED_BALANCE")
CASES=("STANDARD_AVAILABLE_CREDIT","ZERO_FOREIGN_TAX_CREDIT","ETN_25_PERCENT_IRISH_WITHHOLDING","JOINT_ZERO_CREDIT_AND_ETN_25_PERCENT_IRISH_WITHHOLDING")
ROOT=Path(__file__).resolve().parent
_XNYS=json.loads((ROOT/"research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json").read_text())["sessions"]
_LOOK=yaml.safe_load((ROOT/"issuer_lookthrough.yaml").read_text())
_WINDOW_BOUNDS={"full":("2021-06-01","2026-07-31"),"context":("2021-06-01","2023-12-29"),"correction_replication":("2024-04-02","2026-07-31")}
_BOOTSTRAP_INDEX_CACHE: dict[int,np.ndarray]={}
_SUMMARY_FIELDS=("cumulative_twr","net_twr_cagr","sharpe","sortino","max_drawdown","daily_cvar_95","annualized_volatility","downside_deviation","calmar","worst_month","worst_quarter","worst_year","recovery_days","one_way_turnover","rebalance_count","taxable_realized_gain","cost_drag","tax_drag","cash_drag")

def _derived_windows(replay_path:list[dict], initial_nav:str="100000")->dict[str,list[dict]]:
    """Derive every registered window and its true predecessor NAV anchor."""
    expected=[x["session"] for x in _XNYS if _WINDOW_BOUNDS["full"][0]<=x["session"]<=_WINDOW_BOUNDS["full"][1]]
    if [x.get("date") for x in replay_path]!=expected:raise ValueError("replayed full path does not match frozen XNYS calendar")
    result={}
    for name,(start,end) in _WINDOW_BOUNDS.items():
        indices=[i for i,x in enumerate(replay_path) if start<=x["date"]<=end]
        if not indices:raise ValueError(f"{name} replay window is empty")
        rows=[dict(replay_path[i]) for i in indices]
        rows[0]["anchor_nav"]=initial_nav if indices[0]==0 else replay_path[indices[0]-1]["nav"]
        rows[0]["anchor_date"]=replay_path[0]["anchor_date"] if indices[0]==0 else replay_path[indices[0]-1]["date"]
        rows[0]["anchor_operations"]={k:"0" for k in rows[0]["operations"]} if indices[0]==0 else replay_path[indices[0]-1]["operations"]
        result[name]=rows
    return result

def _path_identity(rows:list[dict])->list[tuple]:
    return rows

def _concentration(nav:D,shares:dict[str,D],prices:dict[str,D])->dict[str,float]:
    values={t:float(u*prices[t]/nav) for t,u in shares.items() if u}
    non_issuers={"SPY","VEA","VWO","GLD","BTC","ETH","SOL"}
    direct=[v for t,v in values.items() if t not in non_issuers];effective={t:v for t,v in values.items() if t not in non_issuers}
    for item in _LOOK["issuers"]:effective[item["ticker"]]=effective.get(item["ticker"],0)+sum(values.get(x["fund"],0)*float(x["fund_holding_weight"]) for x in item["funds"])
    names=("NVDA","MSFT","AMZN","GOOGL","AVGO","META","LLY","TSLA","AAPL","TSM","ASML")
    return {"direct_hhi":sum(x*x for x in direct),"max_direct_name":max(direct,default=0),"effective_issuer_max":max(effective.values(),default=0),"ai_platform_common_driver":sum(effective.get(x,0) for x in names),"semis_cluster":sum(effective.get(x,0) for x in ("ASML","TSM","NVDA","AVGO","KLAC")),"power_infra_cluster":sum(effective.get(x,0) for x in ("ETN","GEV","PWR"))}

def _align_crypto_primitives(bars:list[dict],sessions:list[str],closes:dict[str,str],start:date,end:date)->dict[str,D]:
    """Independently authenticate and align one complete UTC daily spot series."""
    expected=[];day=start
    while day<=end:expected.append(datetime.combine(day,datetime.min.time(),timezone.utc));day+=timedelta(days=1)
    parsed=[]
    for row in bars:
        if not isinstance(row,dict) or set(row)!={"close_at","close"} or isinstance(row["close"],bool):raise ValueError("malformed crypto bar")
        instant=datetime.fromisoformat(str(row["close_at"]).replace("Z","+00:00"));value=D(str(row["close"]))
        if instant.tzinfo is None or instant.utcoffset()!=timedelta(0) or not value.is_finite() or value<=0:raise ValueError("invalid crypto bar")
        parsed.append((instant.astimezone(timezone.utc),value))
    if [x[0] for x in parsed]!=expected or len({x[0] for x in parsed})!=len(parsed):raise ValueError("crypto daily coverage/order mismatch")
    result={};index=-1
    for session in sessions:
        cutoff=datetime.fromisoformat(closes[session].replace("Z","+00:00"))
        if cutoff.tzinfo is None:raise ValueError("invalid XNYS cutoff")
        while index+1<len(parsed) and parsed[index+1][0]<=cutoff.astimezone(timezone.utc):index+=1
        if index<0:raise ValueError("missing predecessor crypto close")
        result[session]=parsed[index][1]
    return result

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
    if not rows or "anchor_nav" not in rows[0]:raise ValueError("path boundary anchor missing")
    nav=[float(rows[0]["anchor_nav"])]+[float(x["nav"]) for x in rows];ret=[nav[i]/nav[i-1]-1 for i in range(1,len(nav))];rf=[float(x["risk_free_return"]) for x in rows]
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
    br=[float(x["nav"])/(float(x["anchor_nav"]) if i==0 else float(base[i-1]["nav"]))-1 for i,x in enumerate(base)]
    ar=[float(x["nav"])/(float(x["anchor_nav"]) if i==0 else float(alt[i-1]["nav"]))-1 for i,x in enumerate(alt)];rf=[float(x["risk_free_return"]) for x in base]
    n=len(br);indices=_BOOTSTRAP_INDEX_CACHE.get(n)
    if indices is None:
        rng=random.Random(20260907);indices=np.empty((2000,n),dtype=np.int32)
        for draw in range(2000):
            j=rng.randrange(n)
            for i in range(n):indices[draw,i]=j;j=(j+1)%n if rng.random()>1/21 else rng.randrange(n)
        indices.setflags(write=False);_BOOTSTRAP_INDEX_CACHE[n]=indices
    def stat(ret):
        sample=np.asarray(ret)[indices];risk=np.asarray(rf)[indices];ex=sample-risk;std=ex.std(axis=1,ddof=1)
        if np.any(std==0) or not np.all(np.isfinite(std)):raise ValueError("undefined bootstrap")
        wealth=np.cumprod(1+sample,axis=1);peaks=np.maximum.accumulate(np.concatenate((np.ones((2000,1)),wealth),axis=1),axis=1)[:,1:];tail=np.sort(sample,axis=1)[:,:max(1,math.ceil(.05*n))].mean(axis=1)
        return np.prod(1+sample,axis=1)**(252/n)-1,ex.mean(axis=1)/std*math.sqrt(252),np.min(wealth/peaks-1,axis=1),tail
    b=stat(br);a=stat(ar);names=("NET_TWR_CAGR_DELTA","SHARPE_DELTA","MAX_DRAWDOWN_DELTA","DAILY_CVAR_95_DELTA")
    return {name:float(np.mean(a[i]-b[i]>0)) for i,name in enumerate(names)}

def _fixed_evaluations(rows:list[dict], regimes:list[dict])->dict:
    def complete(selected):
        base=_path_stats(selected);nav=[float(selected[0]["anchor_nav"])]+[float(x["nav"]) for x in selected];returns=[nav[i]/nav[i-1]-1 for i in range(1,len(nav))]
        if "anchor_date" not in selected[0]:raise ValueError("path boundary date missing")
        mean=sum(returns)/len(returns);dates=[date.fromisoformat(selected[0]["anchor_date"])]+[date.fromisoformat(x["date"]) for x in selected]
        def worst(group):
            buckets={}
            for i,r in enumerate(returns,1):buckets[group(dates[i])]=buckets.get(group(dates[i]),1)*(1+r)
            return min(x-1 for x in buckets.values())
        peak=nav[0];peak_i=0;deepest=0.;deep_peak=0;trough=0
        for i,value in enumerate(nav[1:],1):
            if value>=peak:peak=value;peak_i=i
            elif value/peak-1<deepest:deepest=value/peak-1;deep_peak=peak_i;trough=i
        if deepest==0:recovery=0
        else:
            recovered=next((i for i in range(trough+1,len(nav)) if nav[i]>=nav[deep_peak]),None)
            recovery=None if recovered is None else (dates[recovered]-dates[deep_peak]).days
        result={"cumulative_twr":nav[-1]/nav[0]-1,**base,"annualized_volatility":(sum((x-mean)**2 for x in returns)/(len(returns)-1))**.5*math.sqrt(252),"downside_deviation":(sum(min(x,0)**2 for x in returns)/len(returns))**.5*math.sqrt(252)}
        result["calmar"]=result["net_twr_cagr"]/abs(result["max_drawdown"]) if result["max_drawdown"]<0 else math.nan
        end=selected[-1]["operations"];start=selected[0]["anchor_operations"];ops={k:float(end[k])-float(start[k]) for k in end}
        result.update(worst_month=worst(lambda d:(d.year,d.month)),worst_quarter=worst(lambda d:(d.year,(d.month-1)//3)),worst_year=worst(lambda d:d.year),recovery_days=recovery,one_way_turnover=ops["turnover_notional"]/nav[0],rebalance_count=int(ops["rebalance_count"]),taxable_realized_gain=ops["taxable_realized_gain"],cost_drag=ops["cost_drag"],tax_drag=ops["tax_drag"],cash_drag=ops["cash_drag"])
        return result
    out={}
    for regime in regimes:
        selected=[dict(x) for x in rows if regime["start"]<=x["date"]<=regime["end"]]
        if len(selected)<2:raise ValueError("missing fixed regime path")
        index=next(i for i,x in enumerate(rows) if x["date"]==selected[0]["date"])
        selected[0]["anchor_nav"]=rows[index-1]["nav"] if index else rows[0]["anchor_nav"]
        selected[0]["anchor_date"]=rows[index-1]["date"] if index else rows[0]["anchor_date"]
        selected[0]["anchor_operations"]=rows[index-1]["operations"] if index else rows[0]["anchor_operations"]
        out[regime["id"]]=complete(selected)
    years=sorted({date.fromisoformat(x["date"]).year for x in rows});walk={}
    for year in years:
        selected=[dict(x) for x in rows if date.fromisoformat(x["date"]).year<=year]
        if len(selected)>=2:walk[str(year)]=complete(selected)
    out["walk_forward"]=walk
    return out

def _compare_metric_tree(actual:Any, claimed:Any, path="evaluations")->list[str]:
    errors=[]
    if isinstance(actual,dict):
        if not isinstance(claimed,dict) or set(actual)!=set(claimed):return [f"{path}: registry mismatch"]
        for key,value in actual.items():errors.extend(_compare_metric_tree(value,claimed[key],f"{path}/{key}"))
    elif isinstance(actual,list):
        if not isinstance(claimed,list) or len(actual)!=len(claimed):return [f"{path}: registry mismatch"]
        for index,value in enumerate(actual):errors.extend(_compare_metric_tree(value,claimed[index],f"{path}/{index}"))
    elif isinstance(actual,(int,float)):
        if not _finite(claimed) or abs(actual-claimed)>1e-10:errors.append(f"{path}: numeric mismatch")
    elif actual!=claimed:errors.append(f"{path}: value mismatch")
    return errors

_BOOTSTRAP_FIELDS={"NET_TWR_CAGR_DELTA","SHARPE_DELTA","MAX_DRAWDOWN_DELTA","DAILY_CVAR_95_DELTA"}

def _compare_probability_claim(actual:Any,claimed:Any,path:str)->list[str]:
    """Strictly bind the complete probability vector; bool is never numeric."""
    if not isinstance(actual,dict) or set(actual)!=_BOOTSTRAP_FIELDS:return [f"{path}: computed probability registry mismatch"]
    if not isinstance(claimed,dict) or set(claimed)!=_BOOTSTRAP_FIELDS:return [f"{path}: probability registry mismatch"]
    for key in sorted(_BOOTSTRAP_FIELDS):
        value=claimed[key]
        if not _finite(value) or not 0<=value<=1:return [f"{path}/{key}: invalid probability"]
        if value!=actual[key]:return [f"{path}/{key}: probability mismatch"]
    return []

def validate_ledger(doc:dict)->list[str]:
    e=[]; rows=doc.get("ledger"); primitive_rows=[]
    if not isinstance(rows,list):return ["ledger missing"]
    last=None; last_cash=D("100000"); last_shares={}; calendar=doc.get("calendar_ledger")
    if str(doc.get("initial_nav"))!="100000":e.append("initial NAV must be 100000")
    for i,r in enumerate(rows):
        try:
            cash=D(str(r["cash"])); recv=sum((D(str(x["net"])) for x in r.get("receivables",[])),D(0))
            has_holdings="positions" in r
            positions=sum((D(str(x["shares"]))*D(str(x["price"])) for x in r.get("positions",[])),D(0))
            nav=cash+recv+positions if has_holdings else D(str(r["nav"]))
            primitive_rows.append({"nav":str(nav)})
            if has_holdings and nav!=D(str(r["nav"])):e.append(f"row {i}: NAV does not reconcile")
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
    if not isinstance(calendar,list) or not calendar:e.append("complete calendar ledger missing")
    else:
        dates=[date.fromisoformat(x["date"]) for x in calendar]
        if dates!=[dates[0]+timedelta(days=i) for i in range((dates[-1]-dates[0]).days+1)]:e.append("calendar ledger is truncated or duplicated")
        cash=D("100000");pending=D(0);shares={};receivables=[];sessions={r["date"]:r for r in rows};profile=doc.get("cell",{}).get("profile",{});cost_bps=D(str(doc.get("cell",{}).get("cost_bps","NaN")))
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
                        gains=sum((max(D(str(x["gain"])),D(0)) for x in event.get("lots",[])),D(0))
                        price=D(str(event["price"]));lot_errors=any(D(str(x["gain"]))!=D(str(x["units"]))*(price-D(str(x["basis"]))) or D(str(x["tax"]))!=max(D(str(x["gain"])),D(0))*D(str(x["rate"])) for x in event.get("lots",[]))
                        if abs(proceeds-units*price)>D("1e-18") or lot_errors or abs(gains-D(str(event.get("realized_gain"))))>D("1e-18") or abs(D(str(event["cost"]))-proceeds*cost_bps/D(10000))>D("1e-18") or abs(D(str(event["tax"]))-sum((D(str(x["tax"])) for x in event.get("lots",[])),D(0)))>D("1e-18"):e.append(f"calendar row {i}: sell economics mismatch")
                        cash+=proceeds-D(str(event["cost"]))-D(str(event["tax"]));shares[event["ticker"]]-=units
                    elif kind=="receivable_settlement":
                        match=next((x for x in receivables if x["ticker"]==event["ticker"] and x["payable_date"]==row["date"] and x["net"]==D(str(event["net"]))),None)
                        if match is None:e.append(f"calendar row {i}: settlement without receivable")
                        else:receivables.remove(match)
                        cash+=D(str(event["net"]))
                    elif kind=="split":
                        if event.get("unit_basis")!="SPLIT_NORMALIZED_NO_POSITION_MUTATION" or D(str(event["factor"]))<=0:e.append(f"calendar row {i}: invalid split normalization")
                    elif kind=="dividend_recognition":
                        gross=D(str(event["gross"]));withholding=D(str(event["withholding"]));us_tax=D(str(event["us_tax"]));credit=D(str(event["foreign_tax_credit"]));net=D(str(event["net"]))
                        if net!=gross-withholding-us_tax or credit<0 or credit>withholding:e.append(f"calendar row {i}: dividend economics mismatch")
                        receivables.append({"ticker":event["ticker"],"payable_date":event["payable_date"],"net":net})
                    elif kind=="rebalance":pass
                    else:e.append(f"calendar row {i}: unknown event")
                if abs(cash-D(str(row["settled_cash"])))>D("1e-18"):e.append(f"calendar row {i}: unexplained cash transition")
                reported=[{"ticker":x["ticker"],"payable_date":x["payable_date"],"net":D(str(x["net"]))} for x in row.get("receivables",[])]
                if reported!=receivables:e.append(f"calendar row {i}: receivable replay mismatch")
                if row["date"] in sessions:
                    if abs(D(str(sessions[row["date"]]["cash"]))-cash)>D("1e-18"):e.append(f"calendar row {i}: valuation cash mismatch")
                    actual={x["ticker"]:D(str(x["shares"])) for x in sessions[row["date"]].get("positions",[])}
                    if actual and (set(shares)!=set(actual) or any(abs(shares[x]-actual[x])>D("1e-18") for x in shares)):e.append(f"calendar row {i}: position replay mismatch")
                    fixture=doc.get("primitive_fixture")
                    if fixture:
                        securities=sum((units*D(str(fixture["prices"][ticker][row["date"]])) for ticker,units in shares.items()),D(0))
                        expected_nav=cash+securities+sum((x["net"] for x in receivables),D(0))
                        if abs(expected_nav-D(str(sessions[row["date"]]["nav"])))>D("1e-18"):e.append(f"calendar row {i}: valuation NAV mismatch")
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

def _weights(variant:str)->dict[str,D]:
    """Independently reconstruct the frozen constructions."""
    targets=yaml.safe_load((ROOT/"targets.yaml").read_text())["destination"]
    gated={x["ticker"] for x in yaml.safe_load((ROOT/"gates.yaml").read_text())["gates"]}
    weights={x["ticker"]:D(str(x["target_pct"]))/100 for x in targets if x["asset_class"] not in {"cash","reserve"} and x["ticker"] not in gated}
    sleeves={"equity":[x["ticker"] for x in targets if x["asset_class"]=="equity" and x["ticker"] not in gated],"fund":[x["ticker"] for x in targets if x["asset_class"]=="fund" and x["ticker"]!="GLD"],"gold":["GLD"],"crypto":["BTC","ETH","SOL"]}
    transforms={"BROAD_PLUS_5":[("equity","fund",D(".05"))],"DEFENSIVE_PLUS_5":[("equity",None,D(".05"))],"CRYPTO_HALF":[("crypto",None,D(".02"))],"GOLD_PLUS_2":[("equity","gold",D(".02"))],"DIVERSIFIED_BALANCE":[("equity","fund",D(".03")),("equity","gold",D(".01")),("equity",None,D(".01")),("crypto",None,D(".02"))]}
    for source,destination,amount in transforms.get(variant,[]):
        total=sum(weights[t] for t in sleeves[source])
        for ticker in sleeves[source]:weights[ticker]-=amount*weights[ticker]/total
        if destination:
            total=sum(weights[t] for t in sleeves[destination])
            for ticker in sleeves[destination]:weights[ticker]+=amount*weights[ticker]/total
    weights["CASH"]=D(1)-sum(weights.values())
    return weights

def _replay_simulation(fixture:dict, case:str, cell_id:str, variant:str)->dict:
    """Independently stream a simulation from dated source primitives."""
    if fixture.get("input_kind")!="SYNTHETIC_TEST_ONLY":raise ValueError("unadmitted primitive fixture")
    retained=[x for x in _XNYS if fixture.get("start")<=x["session"]<=fixture.get("end")];sessions=[x["session"] for x in retained]
    if fixture.get("sessions")!=sessions or fixture.get("session_closes")!={x["session"]:x["close_utc"] for x in retained}:raise ValueError("pinned XNYS clock mismatch")
    cost_name=cell_id.split("_")[1];tax_name=cell_id.split("_TAX_")[1].split("_CADENCE_")[0];cadence=cell_id.split("_CADENCE_")[1]
    prereg=yaml.safe_load((ROOT/"research/whole_portfolio_robustness_v2/pre_registration.yaml").read_text());registered={x["cell_id"]:x for x in prereg["frictions"]["cell_registry"]}
    if cell_id not in registered or registered[cell_id]!={"cell_id":cell_id,"one_way_cost_bps":cost_name,"tax_profile":tax_name,"rebalance_cadence":cadence}:raise ValueError("cell identity mismatch")
    profile={k:D(str(v)) for k,v in prereg["frictions"]["tax_profile_parameters"][tax_name].items()};cost=D(cost_name);weights=_weights(variant)
    available={k:date.fromisoformat(v) for k,v in fixture.get("available",{}).items()};prices={t:{d:D(str(v)) for d,v in series.items()} for t,series in fixture.get("prices",{}).items()}
    bars=fixture.get("crypto_bars")
    if not isinstance(bars,dict) or set(bars)!={"BTC","ETH","SOL"}:raise ValueError("complete underlying crypto bars missing")
    for ticker in ("BTC","ETH","SOL"):
        aligned=_align_crypto_primitives(bars[ticker],sessions,fixture["session_closes"],date.fromisoformat(fixture["start"]),date.fromisoformat(fixture["end"]))
        if prices.get(ticker)!=aligned:raise ValueError(f"{ticker} aligned prices detached from bars")
        prices[ticker]=aligned
    for series in prices.values():
        if any(isinstance(v,bool) or not v.is_finite() or v<=0 for v in series.values()):raise ValueError("invalid price primitive")
    start=date.fromisoformat(fixture["start"]);end=date.fromisoformat(fixture["end"]);session_set=set(sessions);session_dates=[date.fromisoformat(x) for x in sessions]
    fed={date.fromisoformat(x) for x in fixture.get("fed_business_days",[])};records=[]
    for record in fixture.get("dff_records",[]):
        value=record.get("value");published=datetime.fromisoformat(record["published_at"].replace("Z","+00:00"));observed=date.fromisoformat(record["observation_date"]);later=sorted(x for x in fed if x>observed)
        if isinstance(value,bool) or not D(str(value)).is_finite() or published.tzinfo is None or not later or published.date()<later[0]:raise ValueError("invalid DFF primitive")
        records.append((published.astimezone(timezone.utc),D(str(value))))
    cash=D("100000");pending=D(0);pending_rf=D(0);rf_index=D(1);prior_rf=D(1);lots={};receivables=[];prior_shares={};calendar=[];ledger=[];day=start
    op_keys=("turnover_notional","rebalance_count","taxable_realized_gain","cost_drag","tax_drag","cash_drag");operations={k:D(0) for k in op_keys}
    while day<=end:
        cutoff=datetime.combine(day,datetime.min.time(),timezone.utc);eligible=[x for x in records if x[0]<=cutoff]
        if not eligible:raise ValueError("missing lawful DFF")
        rate=max(eligible,key=lambda x:x[0])[1];credited=pending;cash+=credited;rf_index*=1+pending_rf;opening=cash;gross_rate=rate/100
        with localcontext() as ctx:ctx.prec=60;pending=opening*(gross_rate-max(gross_rate,D(0))*profile["ordinary_income_rate"]-D(".0025"))/360
        pending_rf=gross_rate/360;events=[]
        for split in fixture.get("splits",[]):
            if split["date"]==day.isoformat():
                factor=D(str(split["factor"]));
                if factor<=0:raise ValueError("invalid split")
                events.append({"type":"split","ticker":split["ticker"],"factor":str(factor),"unit_basis":"SPLIT_NORMALIZED_NO_POSITION_MUTATION"})
        for div in fixture.get("dividends",[]):
            if div["ex_date"]==day.isoformat():
                ticker=div["ticker"];gross=prior_shares.get(ticker,D(0))*D(str(div["gross_per_share"]));wh_rate=D(".25") if "ETN_25" in case and ticker=="ETN" else D(str(div.get("withholding_rate",0)));withholding=gross*wh_rate
                tentative=gross*(profile["qualified_dividend_fraction"]*profile["qualified_dividend_rate"]+(1-profile["qualified_dividend_fraction"])*profile["ordinary_income_rate"]);credit=D(0) if "ZERO" in case else min(withholding,tentative);us_tax=tentative-credit;net=gross-withholding-us_tax
                rec={"ticker":ticker,"payable_date":div["payable_date"],"net":net};receivables.append(rec);events.append({"type":"dividend_recognition","gross":str(gross),"withholding":str(withholding),"foreign_tax_credit":str(credit),"us_tax":str(us_tax),"net_receivable":str(net),**rec})
        for rec in list(receivables):
            if rec["payable_date"]==day.isoformat():cash+=rec["net"];receivables.remove(rec);events.append({"type":"receivable_settlement",**rec})
        if day.isoformat() in session_set:
            previous=[x for x in session_dates if x<day];rebalance=not previous or (day.year!=previous[-1].year if cadence=="ANNUAL" else (day.year,(day.month-1)//3)!=(previous[-1].year,(previous[-1].month-1)//3))
            if rebalance:
                nav=cash+sum(sum(x["units"] for x in ls)*prices[t][day.isoformat()] for t,ls in lots.items())+sum(x["net"] for x in receivables);targets={t:(w*nav if available.get(t,start)<=day else D(0)) for t,w in weights.items() if t!="CASH"};events.append({"type":"rebalance","cadence":cadence})
                for ticker,ls in list(lots.items()):
                    price=prices[ticker][day.isoformat()];delta=sum(x["units"] for x in ls)*price-targets.get(ticker,D(0))
                    if delta>0:
                        left=delta/price;details=[];tax=D(0);gain_total=D(0)
                        for lot in sorted(ls,key=lambda x:(x["basis"],x["acquired"]),reverse=True):
                            take=min(lot["units"],left)
                            if not take:continue
                            gain=take*(price-lot["basis"]);rate_tax=profile["gold_gain_rate"] if ticker=="GLD" else (profile["long_gain_rate"] if (day-lot["acquired"]).days>365 else profile["short_gain_rate"]);due=max(gain,D(0))*rate_tax
                            lot["units"]-=take;left-=take;tax+=due;gain_total+=max(gain,D(0));details.append({"units":str(take),"basis":str(lot["basis"]),"acquired":lot["acquired"].isoformat(),"rate":str(rate_tax),"gain":str(gain),"tax":str(due)})
                        lots[ticker]=[x for x in ls if x["units"]];fee=delta*cost/D(10000);cash+=delta-fee-tax;events.append({"type":"sell","ticker":ticker,"price":str(price),"units":str(delta/price),"proceeds":str(delta),"realized_gain":str(gain_total),"cost":str(fee),"tax":str(tax),"lots":details})
                for ticker,target in targets.items():
                    held=sum((x["units"] for x in lots.get(ticker,[])),D(0));current=held*prices[ticker][day.isoformat()] if held else D(0);need=max(target-current,D(0))
                    if need:
                        fee_rate=cost/D(10000);spend=min(need,cash/(1+fee_rate));fee=spend*fee_rate;price=prices[ticker][day.isoformat()];units=spend/price;cash=cash-spend-fee;lots.setdefault(ticker,[]).append({"units":units,"basis":price+fee/units,"acquired":day});events.append({"type":"buy","ticker":ticker,"units":str(units),"notional":str(units*price),"cost":str(fee)})
            prior_shares={t:sum((x["units"] for x in ls),D(0)) for t,ls in lots.items()};positions=[{"ticker":t,"shares":str(sum(x["units"] for x in ls)),"price":str(prices[t][day.isoformat()]),"lots":[{"units":str(x["units"]),"basis":str(x["basis"]),"acquired":x["acquired"].isoformat()} for x in ls]} for t,ls in lots.items()]
            securities=sum((sum(x["units"] for x in lots[t])*prices[t][day.isoformat()] for t in lots),D(0));nav=cash+securities+sum(x["net"] for x in receivables);interval_rf=rf_index/prior_rf-1;prior_rf=rf_index
            row={"date":day.isoformat(),"nav":str(nav),"cash":str(cash),"risk_free_return":str(interval_rf),"_interest_credited":str(credited),"_positions":positions}
            if not ledger:row["anchor_date"]=fixture["anchor_date"]
            if events:row.update(events=events,positions=positions,receivables=[{**x,"net":str(x["net"])} for x in receivables])
            ledger.append(row)
        operations["cash_drag"]+=credited
        for event in events:
            kind=event.get("type")
            if kind in {"buy","sell"}:operations["turnover_notional"]+=D(str(event.get("notional",event.get("proceeds",0))))
            if kind=="rebalance":operations["rebalance_count"]+=1
            if kind=="sell":operations["taxable_realized_gain"]+=D(str(event.get("realized_gain",0)))
            operations["cost_drag"]+=D(str(event.get("cost",0)))
            operations["tax_drag"]+=D(str(event.get("tax",0)))+D(str(event.get("withholding",0)))+D(str(event.get("us_tax",0)))
        if day.isoformat() in session_set:
            ledger[-1]["operations"]={k:str(v) for k,v in operations.items()}
            if len(ledger)==1:ledger[-1]["anchor_operations"]={k:"0" for k in operations}
        if events:calendar.append({"date":day.isoformat(),"opening_eligible_cash":str(opening),"dff_percent":str(rate),"interest_credited":str(credited),"settled_cash":str(cash),"events":events,"receivables":[{**x,"net":str(x["net"])} for x in receivables]})
        day+=timedelta(days=1)
    return {"calendar_ledger":calendar,"calendar_day_count":(end-start).days+1,"ledger":ledger}

def validate_result(doc:dict, *, decision_only:bool=False)->list[str]:
    errors=[] if decision_only else validate_ledger(doc)
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
                        expected=[x["session"] for x in _XNYS if start<=x["session"]<=end]
                        concentration_keys={"direct_hhi","max_direct_name","effective_issuer_max","ai_platform_common_driver","semis_cluster","power_infra_cluster"};operation_keys={"turnover_notional","rebalance_count","taxable_realized_gain","cost_drag","tax_drag","cash_drag"}
                        malformed=any(isinstance(x.get("risk_free_return"),bool) or not _finite(float(x.get("risk_free_return",float("nan")))) or set(x.get("concentration",{}))!=concentration_keys or any(not _finite(v) for v in x.get("concentration",{}).values()) or set(x.get("operations",{}))!=operation_keys or any(isinstance(v,bool) or not D(str(v)).is_finite() for v in x.get("operations",{}).values()) for x in windows[window])
                        if dates!=expected or malformed or "anchor_nav" not in windows[window][0] or "anchor_operations" not in windows[window][0]:errors.append(f"{case}/{cell}/{variant}/{window}: invalid dated primitives")
        if errors:return errors
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
                        actual_primary=_paired_delta(paths[case][primary_id]["BASELINE"]["correction_replication"],paths[case][primary_id][alt]["correction_replication"])
                        if any(abs(actual_primary[k]-primary[k])>1e-10 for k in actual_primary):raise ValueError("primary metric/path mismatch")
                        actual_context=_paired_delta(paths[case][primary_id]["BASELINE"]["context"],paths[case][primary_id][alt]["context"])
                        if any(abs(actual_context[k]-context[k])>1e-10 for k in actual_context):raise ValueError("context metric/path mismatch")
                        if not all(finite(x.get(k)) for x in (primary,context) for k in ("net_cagr_delta_pp","sharpe_delta","sortino_delta","max_drawdown_delta_pp","daily_cvar_95_delta_pp")):raise ValueError("nonfinite primary/context evidence")
                        actual_boot=_bootstrap(paths[case][primary_id]["BASELINE"]["correction_replication"],paths[case][primary_id][alt]["correction_replication"])
                        mismatch=_compare_probability_claim(actual_boot,boot,"bootstrap")
                        if mismatch:raise ValueError(mismatch[0])
                        actual_context_boot=_bootstrap(paths[case][primary_id]["BASELINE"]["context"],paths[case][primary_id][alt]["context"])
                        mismatch=_compare_probability_claim(actual_context_boot,detail.get("context_bootstrap"),"context_bootstrap")
                        if mismatch:raise ValueError(mismatch[0])
                        concentrations=[x["concentration"] for x in paths[case][primary_id][alt]["correction_replication"]]
                        if detail.get("concentration_path")!=concentrations:raise ValueError("concentration/path mismatch")
                        base_concentrations=[x["concentration"] for x in paths[case][primary_id]["BASELINE"]["correction_replication"]]
                        concentration_pass=all(a["direct_hhi"]<=b["direct_hhi"] and a["max_direct_name"]<=b["max_direct_name"] and a["effective_issuer_max"]-b["effective_issuer_max"]<=.0025 and a["ai_platform_common_driver"]-b["ai_platform_common_driver"]<=.0025 and a["semis_cluster"]<=.25 and a["power_infra_cluster"]<=.20 for a,b in zip(concentrations,base_concentrations))
                        regimes=[{"id":"RATE_INFLATION_2022","start":"2022-01-03","end":"2022-12-30"},{"id":"CALENDAR_2023","start":"2023-01-03","end":"2023-12-29"},{"id":"CALENDAR_2024","start":"2024-01-02","end":"2024-12-31"},{"id":"CALENDAR_2025","start":"2025-01-02","end":"2025-12-31"},{"id":"CALENDAR_2026_PARTIAL","start":"2026-01-02","end":"2026-07-31"}]
                        evaluations={"baseline":_fixed_evaluations(paths[case][primary_id]["BASELINE"]["full"],regimes),"alternative":_fixed_evaluations(paths[case][primary_id][alt]["full"],regimes)}
                        mismatch=_compare_metric_tree(evaluations,detail.get("evaluations"),f"{case}/{alt}/evaluations")
                        if mismatch:raise ValueError(mismatch[0])
                        regime_pass=all(evaluations["alternative"][r["id"]]["max_drawdown"]-evaluations["baseline"][r["id"]]["max_drawdown"]>=-.01 for r in regimes)
                        if detail.get("regime_pass") is not regime_pass or detail.get("concentration_pass") is not concentration_pass:raise ValueError("derived regime/concentration gate mismatch")
                        linked=(primary["max_drawdown_delta_pp"]>=2 and context["max_drawdown_delta_pp"]>=0 and boot["MAX_DRAWDOWN_DELTA"]>=.75) or (primary["daily_cvar_95_delta_pp"]>=.1 and context["daily_cvar_95_delta_pp"]>=0 and boot["DAILY_CVAR_95_DELTA"]>=.75)
                        passed=sum(support(x) for x in cells)>=15 and support(primary) and all(context[k]>=0 for k in ("net_cagr_delta_pp","sharpe_delta","sortino_delta")) and boot["SHARPE_DELTA"]>=.75 and linked and regime_pass and concentration_pass
                        named={"support_15_of_18":sum(support(x) for x in cells)>=15,"primary":support(primary),"context_direction":all(context[k]>=0 for k in ("net_cagr_delta_pp","sharpe_delta","sortino_delta")),"bootstrap_sharpe":boot["SHARPE_DELTA"]>=.75,"regimes":regime_pass,"concentration":concentration_pass,"linked_tail":linked,"final":passed}
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
    """Independently replay every registered simulation before accepting a bundle."""
    simulations=bundle.get("simulations");fixture=bundle.get("primitive_fixture")
    if bundle.get("study_id")!="PORTFOLIO-ROBUSTNESS-V2-0001" or bundle.get("synthetic") is not True:return ["invalid study identity"]
    if not isinstance(simulations,dict) or tuple(simulations)!=CASES:return ["complete simulation registry missing"]
    combined={"portfolio_paths":bundle.get("portfolio_paths"),"decision_evidence":bundle.get("decision_evidence"),"foreign_case_gate_booleans":bundle.get("foreign_case_gate_booleans"),"disposition":bundle.get("disposition")}
    errors=validate_result(combined,decision_only=True)
    if errors:return errors
    cell_ids=tuple(bundle["decision_evidence"]["cell_ids"])
    for case,cells in simulations.items():
        if tuple(cells)!=cell_ids:return [f"{case}: simulation cell registry mismatch"]
        for cell,variants in cells.items():
            if tuple(variants)!=("BASELINE",*ALTS):return [f"{case}/{cell}: simulation variant registry mismatch"]
            for variant,actual in variants.items():
                try:
                    expected=_replay_simulation(fixture,case,cell,variant);identity=actual.get("cell",{});tax=cell.split("_TAX_")[1].split("_CADENCE_")[0]
                    if actual.get("variant")!=variant or actual.get("initial_nav")!="100000" or identity.get("cost_bps")!=cell.split("_")[1] or identity.get("tax_profile")!=tax or identity.get("cadence")!=cell.split("_CADENCE_")[1] or identity.get("foreign_case")!=case:raise ValueError("simulation identity mismatch")
                    if actual.get("calendar_day_count")!=expected["calendar_day_count"] or actual.get("calendar_ledger")!=expected["calendar_ledger"]:raise ValueError("calendar/economic replay mismatch")
                    projection=lambda rows:[{k:v for k,v in x.items() if not k.startswith("_")} for x in rows]
                    if actual.get("ledger")!=projection(expected["ledger"]):raise ValueError("session cash/NAV/event/lot replay mismatch")
                    replay_full=[]
                    for i,row in enumerate(expected["ledger"]):
                        item={"date":row["date"],"nav":row["nav"],"risk_free_return":row["risk_free_return"],"operations":row["operations"]};shares={x["ticker"]:D(x["shares"]) for x in row["_positions"]};prices={x["ticker"]:D(x["price"]) for x in row["_positions"]};item["concentration"]=_concentration(D(row["nav"]),shares,prices)
                        if i==0:item.update(anchor_nav="100000",anchor_date=row["anchor_date"],anchor_operations=row["anchor_operations"])
                        replay_full.append(item)
                    expected_windows=_derived_windows(replay_full,"100000");stored=bundle["portfolio_paths"][case][cell][variant]
                    if set(stored)!=set(expected_windows):raise ValueError("registered window inventory mismatch")
                    for window,rows in expected_windows.items():
                        if _path_identity(stored[window])!=_path_identity(rows):raise ValueError(f"{window} path detached from primitive replay")
                    summary=_fixed_evaluations(replay_full,[{"id":"FULL","start":replay_full[0]["date"],"end":replay_full[-1]["date"]}])["FULL"];claimed=actual.get("summary",{})
                    if set(claimed)!=set(_SUMMARY_FIELDS):raise ValueError("summary field inventory mismatch")
                    mismatch=_compare_metric_tree({k:summary[k] for k in _SUMMARY_FIELDS},claimed,"summary")
                    if mismatch:raise ValueError(mismatch[0])
                except Exception as ex:return [f"{case}/{cell}/{variant}: {ex}"]
    return []

def validate_decision_variant(bundle:dict,case:str,alt:str)->list[str]:
    """Focused independent replay used for mutation diagnostics without replaying 432 simulations."""
    errors=[];primary="COST_10_TAX_TAXABLE_MID_CADENCE_QUARTERLY";detail=bundle["decision_evidence"]["cases"][case][alt];paths=bundle["portfolio_paths"][case][primary]
    try:
        actual=_paired_delta(paths["BASELINE"]["correction_replication"],paths[alt]["correction_replication"])
        if any(abs(actual[k]-detail["primary"]["correction_replication"][k])>1e-10 for k in actual):errors.append("primary metric/path mismatch")
        concentrations=[x["concentration"] for x in paths[alt]["correction_replication"]]
        if concentrations!=detail["concentration_path"]:errors.append("concentration/path mismatch")
        actual_boot=_bootstrap(paths["BASELINE"]["correction_replication"],paths[alt]["correction_replication"])
        errors.extend(_compare_probability_claim(actual_boot,detail.get("bootstrap"),"bootstrap"))
    except Exception as ex:errors.append(f"malformed decision evidence: {ex}")
    return errors
