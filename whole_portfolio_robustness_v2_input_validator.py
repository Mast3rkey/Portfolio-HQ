#!/usr/bin/env python3
"""Independent, result-free V2 input admission checks."""
from __future__ import annotations
import hashlib, json, math, shutil, subprocess, sys, tempfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from whole_portfolio_robustness_v2_preregistration_validator import EXPECTED_PINS, validate as validate_contract

ROOT=Path(__file__).resolve().parent
REQUIRED_CRYPTO=("BTC","ETH","SOL")
ACCEPTED_CRYPTO = {'BTC': {'transform': '2060887fe9921ac9c5a8e5db57011cb0a03bdcfd9077e0875be36d2a82fc9fb9', 'raw': 'c0259e8d47bbb8706ec3946deae4c6e8b7a5954232896f9ab5b30dc2b937e51e', 'receipt': '4322a2deb2a6d50a036b755753ce9993ed4bea0251310960e95f048b423f50a8'}, 'ETH': {'transform': 'f2f2ff4c998575a7a1172649aba4e6078e2534848f272c4fb43e4ea15363b186', 'raw': '026074c64d23c40b860368b05076388d9dead4d0235d522a14bff2b2b1bd9dc0', 'receipt': '7a596181f1a24a32528bea2439c9036e453a73e89c3f4aace7aebcd7e49a1540'}}


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
    dff=m.get("dff_availability",{})
    dff_receipt=root/dff.get("publication_receipt_path","")
    if dff.get("status") != "AUTHENTICATED" or dff.get("source")!="FRED_DFF" or not dff_receipt.is_file() or sha(dff_receipt)!=dff.get("publication_receipt_sha256"):
        e.append("DFF: actual publication-time/vintage evidence unresolved")
    entries=m.get("crypto",[])
    if [x.get("symbol") for x in entries]!=list(REQUIRED_CRYPTO):e.append("crypto registry must be exactly BTC, ETH, SOL")
    for x in entries:
        if x.get("symbol")=="SOL" and "SOL" not in ACCEPTED_CRYPTO:e.append("SOL: no independently accepted successor source anchor")
        raw=root/x.get("raw_path",""); rec=root/x.get("receipt_path","")
        if not rec.is_file():e.append(f"{x.get('symbol')}: missing receipt");continue
        receipt=load(rec); e += [f"{x['symbol']}: {z}" for z in validate_receipt(receipt,raw,provider=x.get("provider"),pair=x.get("symbol","")+"USD")]
        if raw.is_file() and x.get("transform_sha256")!=sha(raw):e.append(f"{x['symbol']}: transform hash mismatch")
        anchor=ACCEPTED_CRYPTO.get(x["symbol"])
        if anchor and (sha(raw) if raw.is_file() else None)!=anchor["transform"]:e.append(f"{x['symbol']}: transform differs from independently accepted bytes")
        if anchor and (sha(rec) if rec.is_file() else None)!=anchor["receipt"]:e.append(f"{x['symbol']}: receipt differs from independently accepted bytes")
        if raw.is_file():
            transformed=load(raw)
            if not isinstance(transformed,dict) or transformed.get("instrument")!=x["symbol"] or transformed.get("provider")!="ALPACA_CRYPTO" or not isinstance(transformed.get("rows"),list):
                e.append(f"{x['symbol']}: malformed transform identity")
            else:
                rows=[{"symbol":x["symbol"],"pair":x["symbol"]+"USD","date":r.get("date"),"close_at":(date.fromisoformat(r["date"])+timedelta(days=1)).isoformat()+"T00:00:00Z","close":r.get("close")} for r in transformed["rows"]]
                e += [f"{x['symbol']}: {z}" for z in validate_crypto(rows,x["symbol"],date(2021,6,1),date(2026,7,31))]
                raw_source=root/receipt.get("raw_path","")
                if not raw_source.is_file() or sha(raw_source)!=receipt.get("raw_sha256"):e.append(f"{x['symbol']}: retained raw/receipt chain mismatch")
                elif anchor and sha(raw_source)!=anchor["raw"]:e.append(f"{x['symbol']}: raw page differs from independently accepted bytes")
                else:
                    payload=load(raw_source); provider_rows=payload.get("bars",{}).get(x["symbol"]+"/USD") if isinstance(payload,dict) else None
                    if not isinstance(provider_rows,list) or payload.get("next_page_token") is not None:e.append(f"{x['symbol']}: malformed provider candle payload")
                    else:
                        derived=[{"date":r["t"][:10],"open":r["o"],"high":r["h"],"low":r["l"],"close":r["c"],"volume":r["v"]} for r in provider_rows]
                        actual=[{k:r[k] for k in ("date","open","high","low","close","volume")} for r in transformed["rows"]]
                        if derived!=actual:e.append(f"{x['symbol']}: raw-to-transform reconstruction mismatch")
    return e

def historical_admission(root:Path=ROOT)->dict:
    errors=validate_contract(root)
    for rel,digest in EXPECTED_PINS.items():
        p=root/rel
        if not p.is_file() or sha(p)!=digest: errors.append(f"pinned predecessor byte mismatch: {rel}")
    manifest=root/"research/whole_portfolio_robustness_v2/inputs/input_freeze.json"
    errors.extend(validate_manifest(manifest,root))
    # Rebuild only result-blind LADDER inputs in an isolated destination.
    try:
        study=root/"research/buy_ladder_backtest"; data=root/"research/level1_sleeve_robustness/data"
        builder=study/"build_input_disposition.py"
        if sha(builder)!="01a664c1c5bc623b5026cb3137a6694f0a55c3ee730eaad39dc7b82f7508bd7f":raise ValueError("builder identity mismatch")
        with tempfile.TemporaryDirectory(prefix="v2-ladder-reconstruct-") as tmp:
            isolated=Path(tmp);shutil.copytree(study,isolated/"research/buy_ladder_backtest",ignore=shutil.ignore_patterns("execution","validation","__pycache__"));shutil.copytree(data,isolated/"research/level1_sleeve_robustness/data")
            run=subprocess.run([sys.executable,str(isolated/"research/buy_ladder_backtest/build_input_disposition.py")],cwd=isolated,capture_output=True,text=True)
            if run.returncode:raise ValueError(run.stderr.strip())
            expected={"input_disposition.json":"05a86b0f42df6b055532076d2e84e7ac7a460799012402904afe1fcb1e72ab2e","corporate_actions.json":"79be46b9e64191d4897c5b9ada2c7ba7cfb8c4f86eca4e9ec6943c5895a6d2f1","yahoo_action_crosscheck.json":"0c154aa9e88d495f23b4d08e82e079b8054524bed5e3921cbaf1bf56f199deb4"}
            for name,digest in expected.items():
                rebuilt=isolated/"research/buy_ladder_backtest/inputs"/name
                if sha(rebuilt)!=digest or rebuilt.read_bytes()!=(study/"inputs"/name).read_bytes():raise ValueError(f"isolated reconstruction mismatch: {name}")
    except Exception as ex:errors.append(f"cannot reconstruct LADDER evidence: {ex}")
    return {"study_id":"PORTFOLIO-ROBUSTNESS-V2-0001","result_free":True,"admitted":not errors,
            "disposition":"ADMITTED" if not errors else "INPUT_ADMISSION_FAILED","errors":errors,
            "historical_results_executed":False,"stage1":"UNARMED_AND_NOT_EXECUTABLE"}

if __name__=="__main__":
    result=historical_admission();print(json.dumps(result,sort_keys=True,indent=2));raise SystemExit(0 if result["admitted"] else 2)
