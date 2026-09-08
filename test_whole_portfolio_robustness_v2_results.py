from copy import deepcopy
from whole_portfolio_robustness_v2_result_validator import *

def document():
    rows=[{'cash':'100000','positions':[],'receivables':[],'nav':'100000'}, {'cash':'100000','positions':[],'receivables':[],'nav':'100000','events':[],'interest_credited':'0'}]
    gates={c:{a:False for a in ALTS} for c in CASES}
    cells=[f"COST_{c}_TAX_{t}_CADENCE_{q}" for c in ('0','10','25') for t in ('TAX_DEFERRED','TAXABLE_MID','TAXABLE_HIGH') for q in ('QUARTERLY','ANNUAL')]
    bad={'net_cagr_delta_pp':0.,'sharpe_delta':0.,'sortino_delta':0.,'max_drawdown_delta_pp':0.,'daily_cvar_95_delta_pp':0.}
    details={c:{a:{'cells':[dict(bad,cell_id=x) for x in cells],'primary':{'correction_replication':bad,'context':bad},'bootstrap':{'SHARPE_DELTA':0.,'MAX_DRAWDOWN_DELTA':0.,'DAILY_CVAR_95_DELTA':0.},'regime_pass':True,'concentration_pass':True,'final':False} for a in ALTS} for c in CASES}
    return {'initial_nav':'100000','ledger':rows,'summary':{'cumulative_twr':0.,'max_drawdown':0.},'decision_evidence':{'cell_ids':cells,'cases':details},'foreign_case_gate_booleans':gates,'disposition':{'disposition':'RETAIN_BASELINE','passing_set':[]}}

def test_independent_ledger_and_disposition_recompute(): assert validate_result(document())==[]
def test_tampered_nav_and_summary_detected():
    x=document();x['ledger'][1]['nav']='111000';x['summary']['cumulative_twr']=.11
    e=validate_result(x);assert any('NAV' in z for z in e) and any('cumulative' in z for z in e)
def test_negative_cash_and_external_flow_detected():
    x=document();x['ledger'][1].update(cash='-1',nav='-1',external_flow='1')
    e=validate_result(x);assert any('negative' in z for z in e) and any('external' in z for z in e)
def test_missing_extra_duplicate_like_gate_evidence_fails_closed():
    x=document();del x['foreign_case_gate_booleans'][CASES[-1]]
    assert recompute_disposition(x['foreign_case_gate_booleans'])['disposition']=='UNABLE_TO_DETERMINE'
def test_foreign_boolean_change_overrides_claim():
    x=document();x['foreign_case_gate_booleans'][CASES[1]][ALTS[0]]=True
    assert 'disposition not independently reproducible' in validate_result(x)

def test_unexplained_cash_doubling_and_missing_decision_evidence_rejected():
    x=document();x['ledger'][1].update(cash='200000',nav='200000');x['summary']['cumulative_twr']=1
    assert any('unexplained cash' in e for e in validate_result(x))
    x=document();del x['decision_evidence'];assert any('comparison evidence' in e for e in validate_result(x))
