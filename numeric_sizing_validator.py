"""Read-only XASSET-0016 Level-1 numeric-sizing validator."""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
import re
import yaml

from level1_sleeve_synthesis_validator import SLEEVE_IDS, canonical_record_hash

SCHEMA_VERSION = "1.0"
READY = {"sizing_conditionally_ready", "sizing_ready"}
BASELINE = Decimal("16.67")
INCREMENT = Decimal("2.00")
NUMERIC_DIR = "intelligence/level1_sleeve_synthesis/numeric_sizing"
POLICY_DIR = "intelligence/level1_sleeve_synthesis/policy_adoption"
REL_DIR = "intelligence/level1_sleeve_synthesis/relationships"
STATUS_ASSIGNED = "provisional_target_assigned"
STATUS_BLOCKED = "no_provisional_target_pending_axis_c"
BOUNDARY = "Provisional Level 1 sleeve sizing only; no Level 2 instrument selection or sizing, no adopted policy, and no allocation check is authorized by this record."
REVIEW = "Revisit upon the first governed sizing-challenge risk analysis or targeted backtest, a material sealed-population or relationship-accounting change, or a separately authorized study of the baseline or increment."
UNSIZED_DISCLOSURE = "This residual is capital not yet assigned to any sleeve pending resolution of a blocked sleeve status or additional evidence; it is not the cash_reserve sleeve, not an automatically deployable cash allocation, and is never redistributed without a future governance act."

RECORD_KEYS = {"schema_version","sleeve_id","policy_adoption_reference","numeric_target_status","provisional_target_pct","starting_baseline_pct","applied_adjustments","governing_rule_ids","target_classification","review_condition","uncertainty_disclosure","comparative_consistency_note","blocking_rationale","sizing_boundary_note","record_status","sealed_at","governing_decisions","drafting_session_or_shard_id","content_sha256","cohort_manifest_entry"}
REF_KEYS = {"record_path", "referenced_content_sha256"}
ADJ_KEYS = {"governing_rule_id", "direction", "magnitude_pct", "evidence_ref"}
MANIFEST_KEYS = {"schema_version","governing_decision","cohort","portfolio_reconciliation"}
ROW_KEYS = {"sleeve_id","record_path","content_sha256","schema_version","governing_decision","shard_id","sealed_at"}
REC_KEYS = {"sum_of_assigned_targets_pct","unsized_reserved_capital_pct","reconciliation_identity_holds","unsized_capital_disclosure"}
FORBIDDEN_KEYS = re.compile(r"(?:score|rank|priority_index|target_pct|max_position_size|ticker|instrument_weight|coin_weight|fund_weight)", re.I)
FORBIDDEN_TEXT = re.compile(r"\b(?:buy|sell|trade|chart|technical\s+analysis)\b", re.I)

def _load(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)

def _two(value) -> Decimal:
    if isinstance(value, float):
        raise ValueError("numeric values must be YAML strings preserving two-decimal precision")
    s = str(value)
    if not re.fullmatch(r"\d+\.\d{2}", s):
        raise ValueError(f"expected two-decimal value, got {value!r}")
    return Decimal(s)

def _closed(obj, keys, where, errors):
    if not isinstance(obj, dict):
        errors.append(f"{where} must be a mapping"); return
    missing, extra = keys-set(obj), set(obj)-keys
    if missing: errors.append(f"{where} missing keys: {sorted(missing)}")
    if extra: errors.append(f"{where} extra keys: {sorted(extra)}")

def _walk_forbidden(obj, where, errors):
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k not in RECORD_KEYS and k not in MANIFEST_KEYS and k not in ROW_KEYS and k not in REC_KEYS and k not in ADJ_KEYS and k not in REF_KEYS and FORBIDDEN_KEYS.search(str(k)): errors.append(f"{where}: forbidden Level-2/score key {k!r}")
            _walk_forbidden(v, where, errors)
    elif isinstance(obj, list):
        for v in obj: _walk_forbidden(v, where, errors)
    elif isinstance(obj, str) and FORBIDDEN_TEXT.search(obj):
        errors.append(f"{where}: forbidden directive/chart language")

def derive(repo_root: Path):
    policies = {}
    for sid in SLEEVE_IDS:
        p = repo_root/POLICY_DIR/f"{sid}.yaml"; d = _load(p)
        policies[sid] = (p,d)
    eligible = sorted(s for s,(_,d) in policies.items() if d["sizing_readiness_status"] in READY)
    deferred = {s: sum(x["coverage_state"] == "deferred_disclosed" for x in policies[s][1]["relationship_coverage_ledger"]) for s in eligible}
    breadth = {s:set() for s in eligible}; rel_refs = {s:[] for s in eligible}
    for p in sorted((repo_root/REL_DIR).glob("*.yaml")):
        if p.name == "COHORT_MANIFEST.yaml": continue
        d=_load(p); pair=d["sleeve_pair"]
        for s in (pair["sleeve_a"],pair["sleeve_b"]):
            if s in breadth:
                breadth[s].update(d["secondary_conditions"])
                rel_refs[s].append({"record_path":str(p.relative_to(repo_root)),"referenced_content_sha256":canonical_record_hash(d)})
    states={s:{} for s in eligible}
    for rule, values in (("R2",deferred),("R3",{s:len(v) for s,v in breadth.items()})):
        lo,hi=min(values.values()),max(values.values())
        for s,v in values.items():
            states[s][rule] = "up" if v==lo and list(values.values()).count(lo)==1 else "down" if v==hi and list(values.values()).count(hi)==1 else None
    out={}
    for s in eligible:
        adjustments=[]
        for rule in ("R2","R3"):
            direction=states[s][rule]
            if direction:
                refs = [{"record_path":str(policies[s][0].relative_to(repo_root)),"referenced_content_sha256":canonical_record_hash(policies[s][1])}] if rule=="R2" else rel_refs[s]
                adjustments.append({"governing_rule_id":rule,"direction":direction,"magnitude_pct":"2.00","evidence_ref":refs})
        net=sum((INCREMENT if a["direction"]=="up" else -INCREMENT) for a in adjustments)
        out[s]={"baseline":"16.67","adjustments":adjustments,"rules":[a["governing_rule_id"] for a in adjustments],"target":str((BASELINE+net).quantize(Decimal("0.01"),rounding=ROUND_HALF_EVEN)),"state":states[s]}
    return policies,eligible,out

def validate(repo_root: Path) -> list[str]:
    errors=[]; records_dir=repo_root/NUMERIC_DIR
    policies,eligible,expected=derive(repo_root)
    on_disk={p.stem for p in records_dir.glob("*.yaml") if p.name!="COHORT_MANIFEST.yaml"}
    if on_disk != SLEEVE_IDS: errors.append(f"numeric_sizing population mismatch: {sorted(on_disk)}")
    records={}
    for sid in sorted(on_disk):
        p=records_dir/f"{sid}.yaml"; d=_load(p); records[sid]=d
        _closed(d,RECORD_KEYS,sid,errors); _walk_forbidden(d,sid,errors)
        if sid not in SLEEVE_IDS:
            errors.append(f"{sid}: unauthorized/orphan sleeve_id")
            continue
        if set(RECORD_KEYS)-set(d): continue
        if d["schema_version"]!=SCHEMA_VERSION or d["sleeve_id"]!=sid: errors.append(f"{sid}: identity/schema mismatch")
        _closed(d["policy_adoption_reference"],REF_KEYS,f"{sid}.policy_adoption_reference",errors)
        pp,pd=policies[sid]; pref=d["policy_adoption_reference"]
        if pref.get("record_path")!=str(pp.relative_to(repo_root)) or pref.get("referenced_content_sha256")!=canonical_record_hash(pd): errors.append(f"{sid}: stale policy_adoption_reference")
        assigned=sid in eligible
        if d["numeric_target_status"]!=(STATUS_ASSIGNED if assigned else STATUS_BLOCKED): errors.append(f"{sid}: numeric_target_status not live-derived")
        if assigned:
            exp=expected[sid]
            try:
                if _two(d["starting_baseline_pct"])!=BASELINE: errors.append(f"{sid}: wrong baseline")
                if _two(d["provisional_target_pct"])!=Decimal(exp["target"]): errors.append(f"{sid}: target does not match live derivation")
            except ValueError as e: errors.append(f"{sid}: {e}")
            if d["applied_adjustments"]!=exp["adjustments"]: errors.append(f"{sid}: adjustments do not match live R2/R3 derivation")
            if d["governing_rule_ids"]!=exp["rules"]: errors.append(f"{sid}: governing_rule_ids mismatch")
            for i,a in enumerate(d["applied_adjustments"]):
                _closed(a,ADJ_KEYS,f"{sid}.applied_adjustments[{i}]",errors)
                if a.get("governing_rule_id") not in {"R2","R3"}: errors.append(f"{sid}: retired/unknown rule")
                try:
                    if _two(a.get("magnitude_pct"))!=INCREMENT: errors.append(f"{sid}: wrong adjustment magnitude")
                except ValueError as e: errors.append(f"{sid}: {e}")
            if d["target_classification"]!="provisional_governance_guardrail" or not d["review_condition"] or not d["uncertainty_disclosure"] or not d["comparative_consistency_note"]: errors.append(f"{sid}: populated-target provenance fields invalid")
            if d["blocking_rationale"] is not None: errors.append(f"{sid}: blocking_rationale must be null")
        else:
            for k in ("provisional_target_pct","starting_baseline_pct","target_classification","review_condition","uncertainty_disclosure","comparative_consistency_note"):
                if d[k] is not None: errors.append(f"{sid}: blocked field {k} must be null")
            if d["applied_adjustments"] or d["governing_rule_ids"] or not d["blocking_rationale"]: errors.append(f"{sid}: blocked/null semantics invalid")
        if d["sizing_boundary_note"]!=BOUNDARY or d["record_status"]!="sealed" or canonical_record_hash(d)!=d["content_sha256"]: errors.append(f"{sid}: seal/boundary/hash invalid")
    mp=records_dir/"COHORT_MANIFEST.yaml"; m=_load(mp) if mp.is_file() else {}
    _closed(m,MANIFEST_KEYS,"manifest",errors)
    if set(MANIFEST_KEYS)<=set(m):
        seen=[]
        for i,row in enumerate(m["cohort"]):
            _closed(row,ROW_KEYS,f"manifest.cohort[{i}]",errors); sid=row.get("sleeve_id"); seen.append(sid)
            if sid in records and (row.get("record_path")!=f"{NUMERIC_DIR}/{sid}.yaml" or row.get("content_sha256")!=canonical_record_hash(records[sid])): errors.append(f"manifest row {sid}: path/hash mismatch")
        if set(seen)!=SLEEVE_IDS or len(seen)!=len(SLEEVE_IDS): errors.append("manifest population duplicate/missing/orphan")
        r=m["portfolio_reconciliation"]; _closed(r,REC_KEYS,"portfolio_reconciliation",errors)
        live=sum(Decimal(expected[s]["target"]) for s in eligible); residual=(Decimal("100.00")-live).quantize(Decimal("0.01"),rounding=ROUND_HALF_EVEN)
        try:
            stored_sum=_two(r["sum_of_assigned_targets_pct"]); stored_res=_two(r["unsized_reserved_capital_pct"])
            if stored_sum!=live or stored_sum>Decimal("100.00"): errors.append("manifest assigned sum mismatch/overshoot")
            if stored_res<0 or stored_res!=residual: errors.append("manifest residual mismatch/negative")
            if stored_sum+stored_res!=Decimal("100.00") or r["reconciliation_identity_holds"] is not True: errors.append("manifest reconciliation identity fails")
        except ValueError as e: errors.append(f"manifest: {e}")
        if r["unsized_capital_disclosure"]!=UNSIZED_DISCLOSURE: errors.append("manifest unsized disclosure invalid")
    return errors

if __name__ == "__main__":
    root=Path(__file__).resolve().parent; errs=validate(root)
    if errs:
        print("numeric_sizing_validator: FAILED"); [print("  -",e) for e in errs]; raise SystemExit(1)
    print("numeric_sizing_validator: OK (6 record(s), live R2/R3 rederived)")
