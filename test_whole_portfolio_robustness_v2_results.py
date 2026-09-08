from copy import deepcopy
from whole_portfolio_robustness_v2_result_validator import *

def document():
    rows=[{'date':'2025-01-02','cash':'100000','positions':[],'receivables':[],'nav':'100000','events':[]}, {'date':'2025-01-03','cash':'100000','positions':[],'receivables':[],'nav':'100000','events':[],'interest_credited':'0'}]
    gates={c:{a:False for a in ALTS} for c in CASES}
    cells=[f"COST_{c}_TAX_{t}_CADENCE_{q}" for c in ('0','10','25') for t in ('TAX_DEFERRED','TAXABLE_MID','TAXABLE_HIGH') for q in ('QUARTERLY','ANNUAL')]
    bad={'net_cagr_delta_pp':0.,'sharpe_delta':0.,'sortino_delta':0.,'max_drawdown_delta_pp':0.,'daily_cvar_95_delta_pp':0.}
    named={'support_15_of_18':False,'primary':False,'context_direction':True,'bootstrap_sharpe':False,'regimes':True,'concentration':True,'linked_tail':False,'final':False}
    details={c:{a:{'cells':[dict(bad,cell_id=x,window='correction_replication') for x in cells],'primary':{'correction_replication':bad,'context':bad},'bootstrap':{'SHARPE_DELTA':0.,'MAX_DRAWDOWN_DELTA':0.,'DAILY_CVAR_95_DELTA':0.},'regime_pass':True,'concentration_pass':True,'gates':named,'final':False} for a in ALTS} for c in CASES}
    calendar=[{'date':'2025-01-02','opening_eligible_cash':'100000','dff_percent':'.25','interest_credited':'0','settled_cash':'100000','events':[]},{'date':'2025-01-03','opening_eligible_cash':'100000','dff_percent':'.25','interest_credited':'0','settled_cash':'100000','events':[]}]
    return {'initial_nav':'100000','cell':{'cost_bps':'0','profile':{'ordinary_income_rate':'0'}},'calendar_ledger':calendar,'ledger':rows,'summary':{'cumulative_twr':0.,'max_drawdown':0.},'decision_evidence':{'cell_ids':cells,'cases':details},'foreign_case_gate_booleans':gates,'disposition':{'disposition':'RETAIN_BASELINE','passing_set':[]}}

def test_invented_dictionary_without_paired_paths_is_rejected(): assert any('portfolio paths' in e for e in validate_result(document()))
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
    assert any('cash' in e for e in validate_result(x))
    x=document();del x['decision_evidence'];assert any('comparison evidence' in e for e in validate_result(x))

def test_complete_synthetic_driver_result_replays_and_path_mutation_fails():
    from test_whole_portfolio_robustness_v2_engine import synthetic_study_paths,REGIMES
    from whole_portfolio_robustness_v2_engine import evaluate_study
    generated=evaluate_study(synthetic_study_paths(),REGIMES);doc=document();doc.update(generated)
    assert validate_result(doc)==[]
    case=CASES[0];cell=doc['decision_evidence']['cell_ids'][0]
    doc['portfolio_paths'][case][cell]['BASELINE']['context'][0]['risk_free_return']='NaN'
    assert validate_result(doc)
