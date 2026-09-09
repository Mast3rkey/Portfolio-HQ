#!/usr/bin/env python3
"""Result-blind primitives for PORTFOLIO-ROBUSTNESS-V2-0001.

This module deliberately has no historical entry point.  It operates on caller supplied
records (the tests use synthetic records); historical admission is a separate gate.
"""
from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, localcontext
from typing import Any, Iterable, Mapping, Sequence
from pathlib import Path
import yaml
import numpy as np

D = Decimal
ALTERNATIVES = ("BROAD_PLUS_5", "DEFENSIVE_PLUS_5", "CRYPTO_HALF", "GOLD_PLUS_2", "DIVERSIFIED_BALANCE")
FOREIGN_CASES = ("STANDARD_AVAILABLE_CREDIT", "ZERO_FOREIGN_TAX_CREDIT", "ETN_25_PERCENT_IRISH_WITHHOLDING", "JOINT_ZERO_CREDIT_AND_ETN_25_PERCENT_IRISH_WITHHOLDING")
_BOOTSTRAP_INDEX_CACHE: dict[tuple[int,int,int,int],np.ndarray] = {}

def cash_delta(cash: D, dff_percent: D, ordinary_rate: D) -> D:
    with localcontext() as ctx:
        ctx.prec=60
        r = dff_percent / D(100)
        return cash * (r - max(r, D(0)) * ordinary_rate - D("0.0025")) / D(360)

@dataclass
class Lot:
    units: D
    basis_per_unit: D
    acquired: date

def hifo_sell(lots: list[Lot], units: D, price: D, when: date, short_rate: D, long_rate: D,
              *, gold_rate: D | None = None) -> tuple[D, D, list[dict]]:
    if units < 0 or sum((x.units for x in lots), D(0)) < units:
        raise ValueError("insufficient units")
    tax = D(0); gain_total = D(0); records = []
    for lot in sorted(lots, key=lambda x: (x.basis_per_unit, x.acquired), reverse=True):
        take = min(lot.units, units)
        if not take: continue
        gain = take * (price - lot.basis_per_unit)
        # Frozen rule: losses generate no credit.
        rate = gold_rate if gold_rate is not None else (long_rate if (when-lot.acquired).days > 365 else short_rate)
        due = max(gain, D(0)) * rate
        lot.units -= take; units -= take; tax += due; gain_total += max(gain, D(0))
        records.append({"units": str(take), "basis": str(lot.basis_per_unit), "acquired":lot.acquired.isoformat(),"rate":str(rate), "gain": str(gain), "tax": str(due)})
    lots[:] = [x for x in lots if x.units]
    return gain_total, tax, records

def funded_purchase(cash: D, desired_notional: D, price: D, cost_bps: D) -> tuple[D, D, D]:
    """Return units, cost and cash remainder; never borrow."""
    rate = cost_bps / D(10000)
    spend = min(desired_notional, cash / (D(1) + rate))
    cost = spend * rate
    remainder = cash - spend - cost
    if abs(remainder) < D("1e-25"): remainder=D(0)
    if remainder < 0: raise ArithmeticError("negative cash")
    return spend / price, cost, remainder

def dividend_net(shares: D, gross_per_share: D, withholding_rate: D, qualified_fraction: D,
                 qualified_rate: D, ordinary_rate: D, credit_allowed: bool = True) -> dict[str, D]:
    gross = shares * gross_per_share
    withholding = gross * withholding_rate
    tentative = gross * (qualified_fraction * qualified_rate + (D(1)-qualified_fraction)*ordinary_rate)
    credit = min(withholding, tentative) if credit_allowed else D(0)
    us_tax = tentative - credit
    return {"gross": gross, "withholding": withholding, "foreign_tax_credit": credit,
            "us_tax": us_tax, "net_receivable": gross-withholding-us_tax}

def run_cash_clock(start: date, end: date, cash: D, settlements: Mapping[date, D],
                   rates: Mapping[date, D], ordinary_rate: D, sessions: set[date]) -> list[dict]:
    """Calendar clock. Rates are keyed by lawful start-of-day availability date."""
    rows=[]; opening=D(0); pending=D(0); day=start
    while day <= end:
        cash += pending
        credited = pending
        opening = cash
        settled = settlements.get(day, D(0)); cash += settled
        if day not in rates: raise ValueError(f"missing lawful DFF for {day}")
        pending = cash_delta(opening, rates[day], ordinary_rate)
        rows.append({"date":day.isoformat(),"xnys_session":day in sessions,"opening_eligible_cash":str(opening),
                     "interest_credited":str(credited),"settlement":str(settled),"settled_cash":str(cash),
                     "unposted_interest":str(pending),"nav":str(cash)})
        day += timedelta(days=1)
    return rows

def lawful_dff(records:Sequence[Mapping], days:Sequence[date], fed_business_days:set[date])->dict[date,D]:
    """Resolve rates from explicit publication instants; labels alone are never availability."""
    parsed=[]
    for r in records:
        observed=date.fromisoformat(r["observation_date"]); published=datetime.fromisoformat(r["published_at"].replace("Z","+00:00"))
        if published.tzinfo is None or isinstance(r.get("value"),bool) or not D(str(r["value"])).is_finite():raise ValueError("invalid DFF evidence")
        later=sorted(x for x in fed_business_days if x>observed)
        if not later or published.date()<later[0]:raise ValueError("DFF violates frozen one-business-day lag")
        parsed.append((published.astimezone(timezone.utc),D(str(r["value"]))))
    result={}
    for day in days:
        cutoff=datetime.combine(day,datetime.min.time(),timezone.utc)
        eligible=[x for x in parsed if x[0]<=cutoff]
        if not eligible:raise ValueError(f"no lawfully available DFF at {day}")
        result[day]=max(eligible,key=lambda x:x[0])[1]
    return result

def align_crypto(bars: Sequence[Mapping], sessions: Sequence[date], session_closes: Mapping[date, datetime] | None = None) -> dict[str, D]:
    """Map UTC bar closes to the first XNYS close at/after actual availability."""
    parsed=[]
    for row in bars:
        close_at=datetime.fromisoformat(str(row["close_at"]).replace("Z","+00:00"))
        if close_at.tzinfo is None: raise ValueError("crypto close_at must be timezone aware")
        parsed.append((close_at.astimezone(timezone.utc), D(str(row["close"]))))
    if len({x[0] for x in parsed}) != len(parsed): raise ValueError("duplicate crypto close")
    parsed.sort(); out={}; i=-1
    for session in sorted(sessions):
        if session_closes is None or session not in session_closes:
            raise ValueError(f"missing authenticated XNYS close for {session}")
        cutoff=session_closes[session]
        if cutoff.tzinfo is None: raise ValueError("XNYS close must be timezone aware")
        while i+1 < len(parsed) and parsed[i+1][0] <= cutoff: i += 1
        if i < 0: raise ValueError("missing predecessor crypto close")
        out[session.isoformat()] = parsed[i][1]
    return out

def metrics(returns: Sequence[float], risk_free: Sequence[float] | None = None) -> dict[str,float]:
    if not returns or any(not math.isfinite(x) or x <= -1 for x in returns): raise ValueError("invalid returns")
    rf=list(risk_free or [0.0]*len(returns))
    if len(rf)!=len(returns) or any(not math.isfinite(x) for x in rf): raise ValueError("invalid risk-free series")
    nav=1.; peak=1.; mdd=0.; excess=[]; downside=[]
    for r,f in zip(returns,rf):
        nav*=1+r; peak=max(peak,nav); mdd=min(mdd,nav/peak-1); excess.append(r-f); downside.append(min(r-f,0.)**2)
    n=len(returns); mean=sum(excess)/n
    var=sum((x-mean)**2 for x in excess)/(n-1) if n>1 else 0
    down=(sum(downside)/n)**.5
    sharpe=mean/(var**.5)*math.sqrt(252) if var>0 else math.nan
    sortino=mean/down*math.sqrt(252) if down>0 else math.nan
    tail=sorted(returns)[:max(1,math.ceil(.05*n))]
    return {"cumulative_twr":nav-1,"net_twr_cagr":nav**(252/n)-1,"sharpe":sharpe,"sortino":sortino,
            "max_drawdown":mdd,"daily_cvar_95":sum(tail)/len(tail)}

def complete_metrics(ledger:Sequence[Mapping], risk_free:Sequence[float]|None=None)->dict[str,Any]:
    """All registered path and operational measures, with return fields in decimal units."""
    if len(ledger)<2: raise ValueError("insufficient metric observations")
    if "anchor_nav" not in ledger[0]:raise ValueError("path boundary anchor required")
    anchor=float(ledger[0]["anchor_nav"])
    nav=[anchor]+[float(x["nav"]) for x in ledger]
    returns=[nav[i]/nav[i-1]-1 for i in range(1,len(nav))]
    result=metrics(returns,risk_free); mean=sum(returns)/len(returns)
    result["annualized_volatility"]=(sum((x-mean)**2 for x in returns)/(len(returns)-1))**.5*math.sqrt(252)
    result["downside_deviation"]=(sum(min(x,0)**2 for x in returns)/len(returns))**.5*math.sqrt(252)
    result["calmar"]=result["net_twr_cagr"]/abs(result["max_drawdown"]) if result["max_drawdown"]<0 else math.nan
    if "anchor_date" not in ledger[0]:raise ValueError("path boundary date required")
    dates=[date.fromisoformat(ledger[0]["anchor_date"])]+[date.fromisoformat(x["date"]) for x in ledger]
    if any(a>=b for a,b in zip(dates,dates[1:])):raise ValueError("path dates must strictly follow the boundary anchor")
    def worst(period):
        grouped={}
        for i,r in enumerate(returns,1): grouped[period(dates[i])]=grouped.get(period(dates[i]),1)*(1+r)
        return min(x-1 for x in grouped.values())
    result.update(worst_month=worst(lambda d:(d.year,d.month)),worst_quarter=worst(lambda d:(d.year,(d.month-1)//3)),worst_year=worst(lambda d:d.year))
    peak=nav[0];peak_index=0;deepest=0.;deep_peak=0;trough=0
    for i,value in enumerate(nav[1:],1):
        if value>=peak:peak=value;peak_index=i
        elif value/peak-1<deepest:deepest=value/peak-1;deep_peak=peak_index;trough=i
    if deepest==0:recovery=0
    else:
        recovered=next((i for i in range(trough+1,len(nav)) if nav[i]>=nav[deep_peak]),None)
        recovery=None if recovered is None else (dates[recovered]-dates[deep_peak]).days
    if "operations" in ledger[-1]:
        start=ledger[0].get("anchor_operations",{k:0 for k in ledger[-1]["operations"]});ops={k:float(ledger[-1]["operations"][k])-float(start.get(k,0)) for k in ledger[-1]["operations"]}
        result.update(recovery_days=recovery,one_way_turnover=ops["turnover_notional"]/nav[0],rebalance_count=int(ops["rebalance_count"]),taxable_realized_gain=ops["taxable_realized_gain"],cost_drag=ops["cost_drag"],tax_drag=ops["tax_drag"],cash_drag=ops["cash_drag"])
    else:
        events=[e for row in ledger for e in row.get("events",[])]
        result.update(recovery_days=recovery,one_way_turnover=sum(float(e.get("notional",e.get("proceeds",0))) for e in events if e.get("type") in {"buy","sell"})/nav[0],rebalance_count=sum(any(e.get("type")=="rebalance" for e in row.get("events",[])) for row in ledger),taxable_realized_gain=sum(float(e.get("realized_gain",0)) for e in events if e.get("type")=="sell"),cost_drag=sum(float(e.get("cost",0)) for e in events),tax_drag=sum(float(e.get("tax",0))+float(e.get("withholding",0))+float(e.get("us_tax",0)) for e in events),cash_drag=sum(float(row.get("interest_credited",0)) for row in ledger))
    return result

def _attach_operations(ledger:Sequence[dict],calendar:Sequence[Mapping])->None:
    """Attach cumulative calendar economics once, without duplicating event ledgers."""
    keys=("turnover_notional","rebalance_count","taxable_realized_gain","cost_drag","tax_drag","cash_drag");totals={k:D(0) for k in keys};by_date={}
    for day in calendar:
        totals["cash_drag"]+=D(str(day.get("interest_credited",0)))
        for event in day.get("events",[]):
            kind=event.get("type")
            if kind in {"buy","sell"}:totals["turnover_notional"]+=D(str(event.get("notional",event.get("proceeds",0))))
            if kind=="rebalance":totals["rebalance_count"]+=1
            if kind=="sell":totals["taxable_realized_gain"]+=D(str(event.get("realized_gain",0)))
            totals["cost_drag"]+=D(str(event.get("cost",0)))
            totals["tax_drag"]+=D(str(event.get("tax",0)))+D(str(event.get("withholding",0)))+D(str(event.get("us_tax",0)))
        by_date[day["date"]]={k:str(v) for k,v in totals.items()}
    for row in ledger:row["operations"]=by_date[row["date"]]

def concentration(ledger_row:Mapping, issuer_map:Mapping[str,Any]|None=None)->dict[str,float]:
    if "concentration" in ledger_row:return dict(ledger_row["concentration"])
    nav=D(str(ledger_row["nav"])); values={x["ticker"]:float(D(str(x["shares"]))*D(str(x["price"]))/nav) for x in ledger_row["positions"]}
    direct=[v for t,v in values.items() if t not in {"SPY","VEA","VWO","GLD","BTC","ETH","SOL"}]
    non_issuers={"SPY","VEA","VWO","GLD","BTC","ETH","SOL"}
    effective={t:values.get(t,0) for t in values if t not in non_issuers}
    lookthrough={item["ticker"]:{x["fund"]:float(x["fund_holding_weight"]) for x in item["funds"]} for item in (issuer_map or {}).get("issuers",[])} if issuer_map and "issuers" in issuer_map else (issuer_map or {})
    for issuer,funds in lookthrough.items(): effective[issuer]=effective.get(issuer,0)+sum(values.get(f,0)*w for f,w in funds.items())
    ai=("NVDA","MSFT","AMZN","GOOGL","AVGO","META","LLY","TSLA","AAPL","TSM","ASML")
    return {"direct_hhi":sum(x*x for x in direct),"max_direct_name":max(direct,default=0),"effective_issuer_max":max(effective.values(),default=0),"ai_platform_common_driver":sum(effective.get(t,0) for t in ai),"semis_cluster":sum(effective.get(t,0) for t in ("ASML","TSM","NVDA","AVGO","KLAC")),"power_infra_cluster":sum(effective.get(t,0) for t in ("ETN","GEV","PWR"))}

def fixed_evaluations(ledger:Sequence[Mapping], regimes:Sequence[Mapping])->dict[str,Any]:
    out={}
    for r in regimes:
        rows=[dict(x) for x in ledger if r["start"]<=x["date"]<=r["end"]]
        if rows:
            index=next(i for i,x in enumerate(ledger) if x["date"]==rows[0]["date"]);rows[0]["anchor_nav"]="100000" if index==0 else ledger[index-1]["nav"];rows[0]["anchor_date"]=ledger[0]["anchor_date"] if index==0 else ledger[index-1]["date"];rows[0]["anchor_operations"]={k:"0" for k in rows[0]["operations"]} if index==0 else ledger[index-1]["operations"]
        out[r["id"]]=complete_metrics(rows,[float(x["risk_free_return"]) for x in rows]) if len(rows)>=2 else None
    years=sorted({date.fromisoformat(x["date"]).year for x in ledger})
    out["walk_forward"]={str(y):complete_metrics([x for x in ledger if date.fromisoformat(x["date"]).year<=y],[float(x["risk_free_return"]) for x in ledger if date.fromisoformat(x["date"]).year<=y]) for y in years if len([x for x in ledger if date.fromisoformat(x["date"]).year<=y])>=2}
    return out

def evaluate_study(paths:Mapping[str,Mapping[str,Mapping[str,Mapping[str,Sequence[Mapping]]]]], regimes:Sequence[Mapping], issuer_map:Mapping[str,Any]|None=None)->dict[str,Any]:
    """Derive every cell and gate from paired primitive paths (never caller booleans)."""
    if issuer_map is None: issuer_map=yaml.safe_load(Path("issuer_lookthrough.yaml").read_text())
    if len(issuer_map.get("issuers",[]))!=11:raise ValueError("pinned 11-issuer look-through required")
    expected_regimes=(("RATE_INFLATION_2022","2022-01-03","2022-12-30"),("CALENDAR_2023","2023-01-03","2023-12-29"),("CALENDAR_2024","2024-01-02","2024-12-31"),("CALENDAR_2025","2025-01-02","2025-12-31"),("CALENDAR_2026_PARTIAL","2026-01-02","2026-07-31"))
    if tuple((x.get("id"),x.get("start"),x.get("end")) for x in regimes)!=expected_regimes:raise ValueError("mandatory fixed regime registry mismatch")
    if tuple(paths)!=FOREIGN_CASES: raise ValueError("foreign case registry/order mismatch")
    all_cases={}; gate_booleans={}
    for case,cell_map in paths.items():
        if tuple(cell_map)!=_cell_ids(): raise ValueError("cell registry/order mismatch")
        variants={a:[] for a in ALTERNATIVES}; primary_evidence={}
        for cell_id,variant_map in cell_map.items():
            if set(variant_map)!={"BASELINE",*ALTERNATIVES}:raise ValueError("variant registry mismatch")
            for variant in ALTERNATIVES:
                windows=variant_map[variant]; baseline=variant_map["BASELINE"]
                if set(windows)!={"full","context","correction_replication"} or set(baseline)!=set(windows):raise ValueError("window registry mismatch")
                bounds={"full":("2021-06-01","2026-07-31"),"context":("2021-06-01","2023-12-29"),"correction_replication":("2024-04-02","2026-07-31")}
                retained_sessions=json.loads(Path("research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json").read_text())["sessions"]
                for name,(first,last) in bounds.items():
                    dates=[x.get("date") for x in windows[name]]
                    expected=[x["session"] for x in retained_sessions if first<=x["session"]<=last]
                    if dates!=expected or "anchor_nav" not in windows[name][0]:raise ValueError(f"{name} dated window mismatch")
                computed={}
                for window in windows:
                    rf=[float(x["risk_free_return"]) for x in baseline[window]]
                    if [x["date"] for x in baseline[window]]!=[x["date"] for x in windows[window]]:raise ValueError("unpaired dated observations")
                    bm=complete_metrics(baseline[window],rf);am=complete_metrics(windows[window],rf)
                    delta={"net_cagr_delta_pp":100*(am["net_twr_cagr"]-bm["net_twr_cagr"]),"sharpe_delta":am["sharpe"]-bm["sharpe"],"sortino_delta":am["sortino"]-bm["sortino"],"max_drawdown_delta_pp":100*(am["max_drawdown"]-bm["max_drawdown"]),"daily_cvar_95_delta_pp":100*(am["daily_cvar_95"]-bm["daily_cvar_95"])}
                    if not all(math.isfinite(x) for x in delta.values()):raise ValueError("undefined paired metric")
                    computed[window]=delta
                variants[variant].append(dict(computed["correction_replication"],cell_id=cell_id,window="correction_replication"))
                if cell_id=="COST_10_TAX_TAXABLE_MID_CADENCE_QUARTERLY":primary_evidence[variant]=(computed,baseline,windows)
        case_gates={};case_detail={}
        for variant in ALTERNATIVES:
            computed,base_windows,alt_windows=primary_evidence[variant]
            bw=base_windows["correction_replication"];aw=alt_windows["correction_replication"]
            bret=[float(D(x["nav"])/(D(str(x.get("anchor_nav"))) if i==0 else D(bw[i-1]["nav"]))-1) for i,x in enumerate(bw)]
            aret=[float(D(x["nav"])/(D(str(x.get("anchor_nav"))) if i==0 else D(aw[i-1]["nav"]))-1) for i,x in enumerate(aw)]
            rf=[float(x["risk_free_return"]) for x in bw]
            boot=stationary_bootstrap(bret,aret,rf)
            cbw=base_windows["context"];caw=alt_windows["context"]
            cbret=[float(D(x["nav"])/(D(str(x["anchor_nav"])) if i==0 else D(cbw[i-1]["nav"]))-1) for i,x in enumerate(cbw)]
            caret=[float(D(x["nav"])/(D(str(x["anchor_nav"])) if i==0 else D(caw[i-1]["nav"]))-1) for i,x in enumerate(caw)]
            context_boot=stationary_bootstrap(cbret,caret,[float(x["risk_free_return"]) for x in cbw])
            bc_path=[concentration(x,issuer_map) for x in base_windows["correction_replication"]];ac_path=[concentration(x,issuer_map) for x in alt_windows["correction_replication"]]
            concentration_pass=all(a["direct_hhi"]<=b["direct_hhi"] and a["max_direct_name"]<=b["max_direct_name"] and a["effective_issuer_max"]-b["effective_issuer_max"]<=.0025 and a["ai_platform_common_driver"]-b["ai_platform_common_driver"]<=.0025 and a["semis_cluster"]<=.25 and a["power_infra_cluster"]<=.20 for a,b in zip(ac_path,bc_path))
            evaluations={"baseline":fixed_evaluations(base_windows["full"],regimes),"alternative":fixed_evaluations(alt_windows["full"],regimes)}
            regime_pass=all(evaluations["alternative"][regime["id"]]["max_drawdown"]-evaluations["baseline"][regime["id"]]["max_drawdown"]>=-.01 for regime in regimes)
            passed=decide_variant(variants[variant],computed["correction_replication"],computed["context"],boot,bool(regime_pass),bool(concentration_pass))
            linked=(computed["correction_replication"]["max_drawdown_delta_pp"]>=2 and computed["context"]["max_drawdown_delta_pp"]>=0 and boot["MAX_DRAWDOWN_DELTA"]>=.75) or (computed["correction_replication"]["daily_cvar_95_delta_pp"]>=.1 and computed["context"]["daily_cvar_95_delta_pp"]>=0 and boot["DAILY_CVAR_95_DELTA"]>=.75)
            named={"support_15_of_18":sum(cell_support(x) for x in variants[variant])>=15,"primary":cell_support(computed["correction_replication"]),"context_direction":all(computed["context"][k]>=0 for k in ("net_cagr_delta_pp","sharpe_delta","sortino_delta")),"bootstrap_sharpe":boot["SHARPE_DELTA"]>=.75,"regimes":bool(regime_pass),"concentration":bool(concentration_pass),"linked_tail":linked,"final":passed}
            case_gates[variant]=passed;case_detail[variant]={"cells":variants[variant],"primary":computed,"bootstrap":boot,"context_bootstrap":context_boot,"concentration_path":ac_path,"gates":named,"evaluations":evaluations,"concentration_pass":concentration_pass,"regime_pass":regime_pass,"final":passed}
        gate_booleans[case]=case_gates;all_cases[case]=case_detail
    final=disposition(gate_booleans)
    standard=all_cases[FOREIGN_CASES[0]]
    if any(all_cases[c][a]["gates"]!=standard[a]["gates"] for c in FOREIGN_CASES[1:] for a in ALTERNATIVES):final={"disposition":"UNABLE_TO_DETERMINE","passing_set":[]}
    return {"portfolio_paths":paths,"decision_evidence":{"cell_ids":list(_cell_ids()),"cases":all_cases},"foreign_case_gate_booleans":gate_booleans,"disposition":final}

def stationary_bootstrap(base: Sequence[float], alt: Sequence[float], rf: Sequence[float], draws=2000,
                         mean_block=21, seed=20260907) -> dict[str,float]:
    if not (len(base)==len(alt)==len(rf)) or not base: raise ValueError("paired bootstrap length mismatch")
    n=len(base);cache_key=(n,draws,mean_block,seed);indices=_BOOTSTRAP_INDEX_CACHE.get(cache_key)
    if indices is None:
        rng=random.Random(seed);indices=np.empty((draws,n),dtype=np.int32)
        for draw in range(draws):
            j=rng.randrange(n)
            for i in range(n):
                indices[draw,i]=j;j=(j+1)%n if rng.random()>1/mean_block else rng.randrange(n)
        indices.setflags(write=False);_BOOTSTRAP_INDEX_CACHE[cache_key]=indices
    def stats(values):
        sample=np.asarray(values,dtype=float)[indices];risk=np.asarray(rf,dtype=float)[indices];excess=sample-risk;std=excess.std(axis=1,ddof=1)
        if np.any(std==0) or not np.all(np.isfinite(std)):raise ValueError("undefined required bootstrap statistic")
        wealth=np.cumprod(1+sample,axis=1);peaks=np.maximum.accumulate(np.concatenate((np.ones((draws,1)),wealth),axis=1),axis=1)[:,1:]
        tail=np.sort(sample,axis=1)[:,:max(1,math.ceil(.05*n))].mean(axis=1)
        return np.prod(1+sample,axis=1)**(252/n)-1,excess.mean(axis=1)/std*math.sqrt(252),np.min(wealth/peaks-1,axis=1),tail
    b=stats(base);a=stats(alt);names=("NET_TWR_CAGR_DELTA","SHARPE_DELTA","MAX_DRAWDOWN_DELTA","DAILY_CVAR_95_DELTA")
    return {name:float(np.mean(a[i]-b[i]>0)) for i,name in enumerate(names)}

def cell_support(d: Mapping[str,float]) -> bool:
    vals=(d.get("net_cagr_delta_pp"),d.get("sharpe_delta"),d.get("sortino_delta"),d.get("max_drawdown_delta_pp"),d.get("daily_cvar_95_delta_pp"))
    return all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in vals) and vals[0]>=-.5 and vals[1]>=.05 and vals[2]>=.05 and (vals[3]>=2 or vals[4]>=.1)

def _cell_ids() -> tuple[str,...]:
    return tuple(f"COST_{c}_TAX_{t}_CADENCE_{q}" for c in ("0","10","25") for t in ("TAX_DEFERRED","TAXABLE_MID","TAXABLE_HIGH") for q in ("QUARTERLY","ANNUAL"))

def decide_variant(correction_cells: Sequence[Mapping], primary: Mapping, context: Mapping,
                   bootstrap: Mapping, regimes_pass: bool, concentration_pass: bool, integrity_pass=True) -> bool:
    ids=[x.get("cell_id") for x in correction_cells]
    if tuple(ids)!=_cell_ids() or any(x.get("window")!="correction_replication" for x in correction_cells): raise ValueError("invalid correction cell registry/window")
    keys=("net_cagr_delta_pp","sharpe_delta","sortino_delta","max_drawdown_delta_pp","daily_cvar_95_delta_pp")
    valid=lambda value:isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value)
    if any(not all(valid(x.get(k)) for k in keys) for x in correction_cells) or not all(valid(primary.get(k)) and valid(context.get(k)) for k in keys): raise ValueError("invalid numeric gate evidence")
    if not all(valid(bootstrap.get(k)) and 0<=bootstrap[k]<=1 for k in ("NET_TWR_CAGR_DELTA","SHARPE_DELTA","MAX_DRAWDOWN_DELTA","DAILY_CVAR_95_DELTA")):raise ValueError("invalid bootstrap probability")
    if not all(type(x) is bool for x in (regimes_pass,concentration_pass,integrity_pass)): raise ValueError("gate must be boolean")
    if not integrity_pass or sum(map(cell_support,correction_cells))<15: return False
    if not cell_support(primary) or not regimes_pass or not concentration_pass: return False
    finite=valid
    if not all(finite(context.get(k)) and context[k]>=0 for k in ("net_cagr_delta_pp","sharpe_delta","sortino_delta")): return False
    if bootstrap["SHARPE_DELTA"]<.75: return False
    dd=primary["max_drawdown_delta_pp"]>=2 and context.get("max_drawdown_delta_pp",-math.inf)>=0 and bootstrap.get("MAX_DRAWDOWN_DELTA",-1)>=.75
    cv=primary["daily_cvar_95_delta_pp"]>=.1 and context.get("daily_cvar_95_delta_pp",-math.inf)>=0 and bootstrap.get("DAILY_CVAR_95_DELTA",-1)>=.75
    return dd or cv

def disposition(case_results: Mapping[str,Mapping[str,bool]], integrity=True) -> dict:
    if type(integrity) is not bool or set(case_results)!=set(FOREIGN_CASES) or not integrity: return {"disposition":"UNABLE_TO_DETERMINE","passing_set":[]}
    standard=case_results[FOREIGN_CASES[0]]
    if set(standard)!=set(ALTERNATIVES) or any(type(v) is not bool for case in case_results.values() for v in case.values()) or any(case_results[c]!=standard for c in FOREIGN_CASES[1:]):
        return {"disposition":"UNABLE_TO_DETERMINE","passing_set":[]}
    passing=[v for v in ALTERNATIVES if standard[v]]
    return {"disposition":"RECOMMEND_POLICY_REVIEW" if passing else "RETAIN_BASELINE","passing_set":passing}

def historical_main(*_args, **_kwargs):
    raise RuntimeError("historical V2 execution is fail-closed pending independently accepted input admission and implementation gate")

def derive_weights(root: Path, variant: str) -> dict[str,D]:
    targets=yaml.safe_load((root/"targets.yaml").read_text())["destination"]
    gated={x["ticker"] for x in yaml.safe_load((root/"gates.yaml").read_text())["gates"]}
    if variant not in ("BASELINE",)+ALTERNATIVES: raise ValueError("unknown construction")
    weights={x["ticker"]:D(str(x["target_pct"]))/100 for x in targets if x["asset_class"] not in {"cash","reserve"} and x["ticker"] not in gated}
    cash=D(1)-sum(weights.values())
    sleeves={"eligible_direct_equity":[x["ticker"] for x in targets if x["asset_class"]=="equity" and x["ticker"] not in gated],"broad_market_funds":[x["ticker"] for x in targets if x["asset_class"]=="fund" and x["ticker"]!="GLD"],"gold":["GLD"],"crypto":["BTC","ETH","SOL"]}
    transforms={"BROAD_PLUS_5":[("eligible_direct_equity","broad_market_funds",D('.05'))],"DEFENSIVE_PLUS_5":[("eligible_direct_equity","cash",D('.05'))],"CRYPTO_HALF":[("crypto","cash",D('.02'))],"GOLD_PLUS_2":[("eligible_direct_equity","gold",D('.02'))],"DIVERSIFIED_BALANCE":[("eligible_direct_equity","broad_market_funds",D('.03')),("eligible_direct_equity","gold",D('.01')),("eligible_direct_equity","cash",D('.01')),("crypto","cash",D('.02'))]}
    for src,dst,amount in transforms.get(variant,[]):
        total=sum(weights[t] for t in sleeves[src])
        for t in sleeves[src]: weights[t]-=amount*weights[t]/total
        if dst=="cash": cash+=amount
        else:
            total=sum(weights[t] for t in sleeves[dst])
            for t in sleeves[dst]: weights[t]+=amount*weights[t]/total
    weights["CASH"]=D(1)-sum(weights.values())
    return weights

def _rebalance_day(day:date, cadence:str, sessions:Sequence[date])->bool:
    previous=[x for x in sessions if x<day]
    if not previous:return True
    p=previous[-1]
    return day.year!=p.year if cadence=="ANNUAL" else (day.year,(day.month-1)//3)!=(p.year,(p.month-1)//3)

def _xnys_predecessor(root:Path,start:date)->date:
    retained=json.loads((root/"research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json").read_text())["sessions"]
    dates=[date.fromisoformat(row["session"]) for row in retained]
    if start not in dates:raise ValueError("study start is not a retained XNYS session")
    index=dates.index(start)
    if index==0:raise ValueError("retained XNYS predecessor unavailable")
    return dates[index-1]

def simulate(root:Path, fixture:Mapping[str,Any], variant="BASELINE", cost_bps=D(10), profile:Mapping[str,D]|None=None, cadence="QUARTERLY", foreign_case=FOREIGN_CASES[0])->dict:
    """Integrated deterministic synthetic simulator; all input clocks are explicit primitives."""
    profile=profile or {"ordinary_income_rate":D('.24'),"qualified_dividend_rate":D('.15'),"qualified_dividend_fraction":D('.8'),"short_gain_rate":D('.24'),"long_gain_rate":D('.15'),"gold_gain_rate":D('.28')}
    sessions=[date.fromisoformat(x) for x in fixture["sessions"]]; session_set=set(sessions)
    close_clock={date.fromisoformat(k):datetime.fromisoformat(v.replace("Z","+00:00")) for k,v in fixture.get("session_closes",{}).items()}
    if set(close_clock)!=session_set or any(v.tzinfo is None for v in close_clock.values()):raise ValueError("complete authenticated XNYS close clock required")
    start=date.fromisoformat(fixture["start"]); end=date.fromisoformat(fixture["end"])
    expected_anchor=_xnys_predecessor(root,start)
    if "anchor_date" in fixture and (isinstance(fixture["anchor_date"],bool) or date.fromisoformat(str(fixture["anchor_date"]))!=expected_anchor):raise ValueError("initial anchor is not the retained XNYS predecessor")
    prices={t:{date.fromisoformat(d):D(str(v)) for d,v in rows.items()} for t,rows in fixture["prices"].items()}
    for ticker,bars in fixture.get("crypto_bars",{}).items():prices[ticker]={date.fromisoformat(k):v for k,v in align_crypto(bars,sessions,close_clock).items()}
    available={t:date.fromisoformat(v) for t,v in fixture.get("available",{}).items()}; weights=derive_weights(root,variant)
    days=[];cursor=start
    while cursor<=end:days.append(cursor);cursor+=timedelta(days=1)
    rates=lawful_dff(fixture.get("dff_records",[]),days,{date.fromisoformat(x) for x in fixture.get("fed_business_days",[])})
    cash=D('100000'); lots:dict[str,list[Lot]]={}; receivables=[]; ledger=[]; calendar_ledger=[]; events=[]; pending_interest=D(0); pending_rf=D(0); rf_index=D(1); prior_session_rf=D(1); prior_shares={}; day=start
    dividends=fixture.get("dividends",[]); splits=fixture.get("splits",[])
    while day<=end:
        credited_interest=pending_interest;cash+=credited_interest;rf_index*=D(1)+pending_rf; events_day=[]
        opening=cash
        pending_interest=cash_delta(opening,rates[day],D(str(profile["ordinary_income_rate"])))
        pending_rf=rates[day]/D(100)/D(360)
        for s in splits:
            if s["date"]==day.isoformat():
                factor=D(str(s["factor"])); ticker=s["ticker"]
                if factor<=0:raise ValueError("invalid split factor")
                # Prices, lots and entitlements are expressed in split-normalized units.
                events_day.append({"type":"split","ticker":ticker,"factor":str(factor),"unit_basis":"SPLIT_NORMALIZED_NO_POSITION_MUTATION"})
        for d in dividends:
            if d["ex_date"]==day.isoformat():
                wh=D(str(d.get("withholding_rate",0)))
                if "ETN_25" in foreign_case and d["ticker"]=="ETN":wh=D('.25')
                net=dividend_net(prior_shares.get(d["ticker"],D(0)),D(str(d["gross_per_share"])),wh,D(str(profile["qualified_dividend_fraction"])),D(str(profile["qualified_dividend_rate"])),D(str(profile["ordinary_income_rate"])),"ZERO" not in foreign_case)
                rec={"ticker":d["ticker"],"payable_date":d["payable_date"],"net":net["net_receivable"]};receivables.append(rec);events_day.append({"type":"dividend_recognition",**{k:str(v) for k,v in net.items()},**rec})
        for rec in list(receivables):
            if rec["payable_date"]==day.isoformat(): cash+=rec["net"];receivables.remove(rec);events_day.append({"type":"receivable_settlement",**rec})
        if day in session_set:
            if any(day not in prices.get(t,{}) for t,ls in lots.items() if sum(x.units for x in ls)): raise ValueError("missing held-asset session price")
            if _rebalance_day(day,cadence,sessions):
                nav=cash+sum((sum(l.units for l in ls)*prices[t][day] for t,ls in lots.items()),D(0))+sum((r["net"] for r in receivables),D(0))
                targets={t:(w*nav if available.get(t,start)<=day else D(0)) for t,w in weights.items() if t!="CASH"}
                if any(target and day not in prices.get(t,{}) for t,target in targets.items()):raise ValueError("missing price at first scheduled rebalance after availability")
                events_day.append({"type":"rebalance","cadence":cadence})
                # Sells first; HIFO taxes and sell costs immediately reduce settled cash.
                for t,ls in lots.items():
                    value=sum(x.units for x in ls)*prices[t][day]; delta=value-targets.get(t,D(0))
                    if delta>D(0):
                        units=delta/prices[t][day]; gain,tax,detail=hifo_sell(ls,units,prices[t][day],day,D(str(profile["short_gain_rate"])),D(str(profile["long_gain_rate"])),gold_rate=D(str(profile["gold_gain_rate"])) if t=="GLD" else None);cost=delta*cost_bps/D(10000);cash+=delta-cost-tax;events_day.append({"type":"sell","ticker":t,"price":str(prices[t][day]),"units":str(units),"proceeds":str(delta),"realized_gain":str(gain),"cost":str(cost),"tax":str(tax),"lots":detail})
                for t,target in targets.items():
                    held=sum((x.units for x in lots.get(t,[])),D(0))
                    if not held and not target:continue
                    current=held*prices[t][day]; need=max(target-current,D(0))
                    if need:
                        units,cost,cash=funded_purchase(cash,need,prices[t][day],cost_bps);lots.setdefault(t,[]).append(Lot(units,prices[t][day]+cost/units if units else prices[t][day],day));events_day.append({"type":"buy","ticker":t,"units":str(units),"notional":str(units*prices[t][day]),"cost":str(cost)})
            prior_shares={t:sum((x.units for x in ls),D(0)) for t,ls in lots.items()}
            positions=[{"ticker":t,"shares":str(sum(x.units for x in ls)),"price":str(prices[t][day]),"lots":[{"units":str(x.units),"basis":str(x.basis_per_unit),"acquired":x.acquired.isoformat()} for x in ls]} for t,ls in lots.items()]
            nav=cash+sum(D(x["shares"])*D(x["price"]) for x in positions)+sum(r["net"] for r in receivables)
            events.extend({"date":day.isoformat(),**e} for e in events_day)
            interval_rf=rf_index/prior_session_rf-D(1);prior_session_rf=rf_index
            ledger.append({"date":day.isoformat(),"anchor_nav":"100000" if not ledger else None,"anchor_date":expected_anchor.isoformat() if not ledger else None,"cash":str(cash),"opening_eligible_cash":str(opening),"interest_credited":str(credited_interest),"unposted_interest":str(pending_interest),"risk_free_return":str(interval_rf),"positions":positions,"receivables":[{**r,"net":str(r["net"])} for r in receivables],"events":events_day,"nav":str(nav),"external_flow":"0"})
        calendar_ledger.append({"date":day.isoformat(),"opening_eligible_cash":str(opening),"dff_percent":str(rates[day]),"interest_credited":str(credited_interest),"settled_cash":str(cash),"events":events_day,"receivables":[{**r,"net":str(r["net"])} for r in receivables]})
        events.extend({"date":day.isoformat(),**e} for e in events_day if day not in session_set)
        day+=timedelta(days=1)
    _attach_operations(ledger,calendar_ledger)
    if ledger:ledger[0]["anchor_operations"]={k:"0" for k in ledger[0]["operations"]}
    m=complete_metrics(ledger,[float(D(ledger[i].get("risk_free_return",0))) for i in range(len(ledger))]) if ledger else {}
    return {"schema_version":"2.1","variant":variant,"cell":{"cost_bps":str(cost_bps),"profile":dict((k,str(v)) for k,v in profile.items()),"cadence":cadence,"foreign_case":foreign_case},"initial_nav":"100000","calendar_ledger":calendar_ledger,"ledger":ledger,"events":events,"summary":m,"weights":{k:str(v) for k,v in weights.items()}}

def run_synthetic_study(root:Path, fixture:Mapping[str,Any])->dict[str,Any]:
    """Execute the complete frozen 6x18x4 registry from synthetic authenticated primitives."""
    prereg=yaml.safe_load((root/"research/whole_portfolio_robustness_v2/pre_registration.yaml").read_text())
    retained=json.loads((root/"research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json").read_text())["sessions"]
    required=[x for x in retained if fixture["start"]<=x["session"]<=fixture["end"]]
    expected_closes={x["session"]:x["close_utc"] for x in required}
    predecessor=next((x["session"] for x in reversed(retained) if x["session"]<fixture["start"]),None)
    if fixture.get("input_kind")!="SYNTHETIC_TEST_ONLY" or fixture["sessions"]!=[x["session"] for x in required] or fixture["session_closes"]!=expected_closes or fixture.get("anchor_date")!=predecessor:
        raise ValueError("synthetic study requires the exact pinned XNYS session/close clock")
    profiles={k:{n:D(v) for n,v in values.items()} for k,values in prereg["frictions"]["tax_profile_parameters"].items()}
    issuer=yaml.safe_load((root/"issuer_lookthrough.yaml").read_text())
    paths={};simulations={}
    for case in FOREIGN_CASES:
        paths[case]={};simulations[case]={}
        for cell in prereg["frictions"]["cell_registry"]:
            identity=cell["cell_id"];paths[case][identity]={};simulations[case][identity]={}
            for variant in ("BASELINE",)+ALTERNATIVES:
                result=simulate(root,fixture,variant,D(cell["one_way_cost_bps"]),profiles[cell["tax_profile"]],cell["rebalance_cadence"],case)
                result["cell"]["tax_profile"]=cell["tax_profile"]
                audit_rows=result["ledger"]
                rows=[{**{k:row[k] for k in ("date","nav","risk_free_return","operations")},"concentration":concentration(row,issuer)} for row in audit_rows]
                def window(start,end):
                    selected=[x for x in rows if start<=x["date"]<=end]
                    first=next(i for i,x in enumerate(rows) if x["date"]==start)
                    selected[0]={**selected[0],"anchor_nav":result["initial_nav"] if first==0 else rows[first-1]["nav"],"anchor_date":fixture["anchor_date"] if first==0 else rows[first-1]["date"],"anchor_operations":{k:"0" for k in selected[0]["operations"]} if first==0 else rows[first-1]["operations"]}
                    return selected
                windows={"full":window("2021-06-01","2026-07-31"),"context":window("2021-06-01","2023-12-29"),"correction_replication":window("2024-04-02","2026-07-31")}
                paths[case][identity][variant]=windows
                compact_ledger=[]
                for row in audit_rows:
                    keep={k:row[k] for k in ("date","nav","cash","risk_free_return","operations")}
                    if "anchor_operations" in row:keep["anchor_operations"]=row["anchor_operations"]
                    if row.get("anchor_date") is not None:keep["anchor_date"]=row["anchor_date"]
                    if row.get("events"):keep.update(events=row["events"],positions=row["positions"],receivables=row["receivables"])
                    compact_ledger.append(keep)
                compact_calendar=[row for row in result["calendar_ledger"] if row["events"]]
                simulations[case][identity][variant]={"variant":variant,"cell":result["cell"],"initial_nav":"100000","calendar_ledger":compact_calendar,"calendar_day_count":len(result["calendar_ledger"]),"ledger":compact_ledger,"summary":result["summary"]}
    decision=evaluate_study(paths,prereg["windows"]["fixed_regimes"],issuer)
    return {"study_id":"PORTFOLIO-ROBUSTNESS-V2-0001","synthetic":True,"primitive_fixture":fixture,"simulations":simulations,**decision}
