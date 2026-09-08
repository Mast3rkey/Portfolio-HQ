#!/usr/bin/env python3
"""Independent, result-free V2 input admission checks."""
from __future__ import annotations
import hashlib, json, math
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from whole_portfolio_robustness_v2_preregistration_validator import EXPECTED_PINS, validate as validate_contract

ROOT=Path(__file__).resolve().parent
REQUIRED_CRYPTO=("BTC","ETH","SOL")

def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path:Path)->Any:
    def pairs(items):
        out={}
        for k,v in items:
            if k in out: raise ValueError(f"duplicate JSON key: {k}")
            out[k]=v
        return out
    return json.loads(path.read_bytes(),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(f"nonfinite JSON: {x}")))

def validate_receipt(receipt:dict, raw:Path, *, provider:str, pair:str)->list[str]:
    e=[]
    status=receipt.get("response_status",receipt.get("status"))
    endpoint=receipt.get("endpoint_locator",receipt.get("request_url",""))
    if status != 200: e.append("acquisition status is not 200")
    if not endpoint.startswith("https://data.alpaca.markets/"): e.append("unsupported or malformed provider endpoint")
    if receipt.get("provider") != provider or provider!="ALPACA_CRYPTO": e.append("provider identity mismatch")
    if pair.replace("USD","%2FUSD") not in endpoint and pair.replace("USD","/USD") not in endpoint:e.append("pair/quote identity mismatch")
    if receipt.get("dataset_id") != f"crypto:{pair[:-3]}:alpaca":e.append("dataset identity mismatch")
    if not raw.is_file(): e.append("transformed bytes missing")
    return e

def validate_crypto(raw_rows:list[dict], symbol:str, start:date, end:date)->list[str]:
    e=[]; seen={}
    for i,row in enumerate(raw_rows):
        try:
            if row.get("symbol")!=symbol or row.get("pair")!=symbol+"USD": raise ValueError("identity")
            close=datetime.fromisoformat(row["close_at"].replace("Z","+00:00"))
            if close.tzinfo is None or close.astimezone(timezone.utc).time().isoformat()!="00:00:00": raise ValueError("close timestamp")
            label=date.fromisoformat(row["date"])
            if close.date()!=label+timedelta(days=1): raise ValueError("bar close/date convention")
            if label in seen: raise ValueError("duplicate date")
            value=row["close"]
            if isinstance(value,bool) or not isinstance(value,(str,int,float)) or not math.isfinite(float(value)) or float(value)<=0: raise ValueError("close")
            seen[label]=row
        except Exception as ex: e.append(f"row {i}: {ex}")
    required={start-timedelta(days=1)}; d=start
    while d<=end: required.add(d); d+=timedelta(days=1)
    missing=sorted(required-set(seen))
    if missing: e.append(f"incomplete calendar coverage: {len(missing)} missing; first={missing[0]}")
    return e

def validate_manifest(path:Path, root:Path=ROOT)->list[str]:
    try: m=load(path)
    except Exception as ex:return [f"cannot load manifest: {ex}"]
    e=[]
    if m.get("study_id")!="PORTFOLIO-ROBUSTNESS-V2-0001" or m.get("result_free") is not True:e.append("wrong study/result-free declaration")
    if m.get("dff_availability",{}).get("status") != "AUTHENTICATED":
        e.append("DFF: actual publication-time/vintage evidence unresolved")
    entries=m.get("crypto",[])
    if [x.get("symbol") for x in entries]!=list(REQUIRED_CRYPTO):e.append("crypto registry must be exactly BTC, ETH, SOL")
    for x in entries:
        raw=root/x.get("raw_path",""); rec=root/x.get("receipt_path","")
        if not rec.is_file():e.append(f"{x.get('symbol')}: missing receipt");continue
        receipt=load(rec); e += [f"{x['symbol']}: {z}" for z in validate_receipt(receipt,raw,provider=x.get("provider"),pair=x.get("symbol","")+"USD")]
        if raw.is_file() and x.get("transform_sha256")!=sha(raw):e.append(f"{x['symbol']}: transform hash mismatch")
        if raw.is_file():
            transformed=load(raw)
            if not isinstance(transformed,dict) or transformed.get("instrument")!=x["symbol"] or transformed.get("provider")!="ALPACA_CRYPTO" or not isinstance(transformed.get("rows"),list):
                e.append(f"{x['symbol']}: malformed transform identity")
            else:
                rows=[{"symbol":x["symbol"],"pair":x["symbol"]+"USD","date":r.get("date"),"close_at":(date.fromisoformat(r["date"])+timedelta(days=1)).isoformat()+"T00:00:00Z","close":r.get("close")} for r in transformed["rows"]]
                e += [f"{x['symbol']}: {z}" for z in validate_crypto(rows,x["symbol"],date(2021,6,1),date(2026,7,31))]
                raw_source=root/receipt.get("raw_path","")
                if not raw_source.is_file() or sha(raw_source)!=receipt.get("raw_sha256"):e.append(f"{x['symbol']}: retained raw/receipt chain mismatch")
    return e

def historical_admission(root:Path=ROOT)->dict:
    errors=validate_contract(root)
    for rel,digest in EXPECTED_PINS.items():
        p=root/rel
        if not p.is_file() or sha(p)!=digest: errors.append(f"pinned predecessor byte mismatch: {rel}")
    manifest=root/"research/whole_portfolio_robustness_v2/inputs/input_freeze.json"
    errors.extend(validate_manifest(manifest,root))
    # The accepted LADDER disposition is a manifest, not an opaque blessing.
    try:
        disposition=load(root/"research/buy_ladder_backtest/inputs/input_disposition.json")
        refs=[]
        def walk(x):
            if isinstance(x,dict):
                if "raw_path" in x and "raw_sha256" in x: refs.append((x["raw_path"],x["raw_sha256"]))
                if "receipt_path" in x and "receipt_sha256" in x: refs.append((x["receipt_path"],x["receipt_sha256"]))
                for v in x.values():walk(v)
            elif isinstance(x,list):
                for v in x:walk(v)
        walk(disposition)
        if not refs: errors.append("LADDER disposition contains no reconstructible provenance")
        for rel,digest in refs:
            p=root/rel
            if not p.is_file() or sha(p)!=digest:errors.append(f"LADDER provenance mismatch: {rel}")
    except Exception as ex:errors.append(f"cannot reconstruct LADDER evidence: {ex}")
    return {"study_id":"PORTFOLIO-ROBUSTNESS-V2-0001","result_free":True,"admitted":not errors,
            "disposition":"ADMITTED" if not errors else "INPUT_ADMISSION_FAILED","errors":errors,
            "historical_results_executed":False,"stage1":"UNARMED_AND_NOT_EXECUTABLE"}

if __name__=="__main__":
    result=historical_admission();print(json.dumps(result,sort_keys=True,indent=2));raise SystemExit(0 if result["admitted"] else 2)
