from copy import deepcopy
from pathlib import Path
import shutil
import yaml
import pytest

from numeric_sizing_validator import derive, validate, NUMERIC_DIR, POLICY_DIR, REL_DIR

ROOT=Path(__file__).resolve().parent

def load(p):
    with p.open() as f: return yaml.safe_load(f)

def write(p,d):
    p.write_text(yaml.safe_dump(d,sort_keys=False),encoding="utf-8")

@pytest.fixture
def repo(tmp_path):
    for rel in (NUMERIC_DIR,POLICY_DIR,REL_DIR):
        dst=tmp_path/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copytree(ROOT/rel,dst)
    return tmp_path

def record(repo,sid): return repo/NUMERIC_DIR/f"{sid}.yaml"
def manifest(repo): return repo/NUMERIC_DIR/"COHORT_MANIFEST.yaml"
def mutate(path,fn):
    d=load(path); fn(d); write(path,d)

def assert_bad(repo,needle=None):
    e=validate(repo); assert e
    if needle: assert any(needle in x for x in e),e

def test_live_candidate_valid(): assert validate(ROOT)==[]

@pytest.mark.parametrize("counts,expected",[
    ({"a":1,"b":1,"c":2},{"a":None,"b":None,"c":"down"}),
    ({"a":1,"b":2,"c":2},{"a":"up","b":None,"c":None}),
])
def test_relative_extreme_tie_rule(counts,expected):
    def states(v):
        lo,hi=min(v.values()),max(v.values())
        return {s:("up" if n==lo and list(v.values()).count(lo)==1 else "down" if n==hi and list(v.values()).count(hi)==1 else None) for s,n in v.items()}
    assert states(counts)==expected

@pytest.mark.parametrize("r2,r3,target",[("up","up","20.67"),("down","down","12.67"),("up","down","16.67"),("up",None,"18.67"),(None,"down","14.67")])
def test_adjustment_matrix(r2,r3,target):
    from decimal import Decimal
    net=sum(Decimal("2.00") if x=="up" else Decimal("-2.00") if x=="down" else Decimal("0") for x in (r2,r3))
    assert str(Decimal("16.67")+net)==target

def test_wrong_baseline(repo): mutate(record(repo,"equity"),lambda d:d.update(starting_baseline_pct="16.66")); assert_bad(repo,"wrong baseline")
def test_wrong_magnitude(repo): mutate(record(repo,"equity"),lambda d:d["applied_adjustments"][0].update(magnitude_pct="1.00")); assert_bad(repo,"adjustments do not match")
def test_wrong_direction(repo): mutate(record(repo,"equity"),lambda d:d["applied_adjustments"][0].update(direction="down")); assert_bad(repo,"adjustments do not match")
def test_stale_declared_trigger(repo): mutate(record(repo,"crypto"),lambda d:d.update(applied_adjustments=[{"governing_rule_id":"R2","direction":"up","magnitude_pct":"2.00","evidence_ref":[]}],governing_rule_ids=["R2"])); assert_bad(repo,"adjustments do not match")
def test_wrong_target_inside_bounds(repo): mutate(record(repo,"crypto"),lambda d:d.update(provisional_target_pct="18.67")); assert_bad(repo,"target does not match")
def test_negative_residual(repo): mutate(manifest(repo),lambda d:d["portfolio_reconciliation"].update(unsized_reserved_capital_pct="-0.01")); assert_bad(repo)
def test_exact_100_arithmetic_is_accepted_by_primitive(): assert 100+0==100
def test_sum_overshoot(repo): mutate(manifest(repo),lambda d:d["portfolio_reconciliation"].update(sum_of_assigned_targets_pct="100.01",unsized_reserved_capital_pct="0.00")); assert_bad(repo,"overshoot")
def test_excess_precision(repo): mutate(record(repo,"equity"),lambda d:d.update(provisional_target_pct="18.670")); assert_bad(repo,"two-decimal")
def test_rounding_drift(repo): mutate(manifest(repo),lambda d:d["portfolio_reconciliation"].update(sum_of_assigned_targets_pct="66.67",unsized_reserved_capital_pct="33.33")); assert_bad(repo,"assigned sum")
@pytest.mark.parametrize("value",["0.00","1.00"])
def test_blocked_numeric_rejected(repo,value): mutate(record(repo,"cash_reserve"),lambda d:d.update(provisional_target_pct=value)); assert_bad(repo,"blocked field")
def test_cash_reserve_not_residual(repo): mutate(manifest(repo),lambda d:d["portfolio_reconciliation"].update(unsized_capital_disclosure="This is the cash_reserve allocation.")); assert_bad(repo,"unsized disclosure")
def test_stronger_evidence_maturity_non_influence(repo):
    before=derive(repo)[2]
    for p in (repo/REL_DIR).glob("*.yaml"):
        if p.name=="COHORT_MANIFEST.yaml": continue
        d=load(p)
        if d.get("favored_sleeve_id") is not None: d["favored_sleeve_id"]="masked_counterfactual"
        write(p,d)
    assert derive(repo)[2]==before
def test_targets_yaml_cannot_anchor_derivation(repo):
    (repo/"targets.yaml").write_text("destinations: [{target_pct: 99.99}]\n")
    assert derive(repo)[2]==derive(ROOT)[2]
def test_order_independence(repo):
    d=load(manifest(repo)); d["cohort"].reverse(); write(manifest(repo),d); assert validate(repo)==[]
def test_stale_hash(repo): mutate(record(repo,"equity"),lambda d:d["policy_adoption_reference"].update(referenced_content_sha256="0"*64)); assert_bad(repo,"stale policy")
def test_manifest_missing_record(repo): mutate(manifest(repo),lambda d:d.update(cohort=d["cohort"][:-1])); assert_bad(repo,"manifest population")
def test_manifest_orphan(repo): shutil.copy(record(repo,"equity"),repo/NUMERIC_DIR/"orphan.yaml"); assert_bad(repo,"population mismatch")
def test_extra_key(repo): mutate(record(repo,"equity"),lambda d:d.update(extra="x")); assert_bad(repo,"extra keys")
@pytest.mark.parametrize("key",["ticker_weight","instrument_weight","rank","composite_score"])
def test_level2_or_hidden_score_key(repo,key): mutate(record(repo,"equity"),lambda d:d["policy_adoption_reference"].update({key:"x"})); assert_bad(repo,"forbidden Level-2/score")
def test_retired_r1(repo): mutate(record(repo,"equity"),lambda d:d["applied_adjustments"][0].update(governing_rule_id="R1")); assert_bad(repo,"adjustments do not match")
def test_comparative_consistency_live():
    _,_,d=derive(ROOT)
    assert d["crypto"]["state"]==d["fund_gld_defensive"]["state"]
    assert d["crypto"]["target"]==d["fund_gld_defensive"]["target"]
def test_determinism(): assert derive(ROOT)[2]==derive(ROOT)[2]
