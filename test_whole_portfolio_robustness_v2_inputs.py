import hashlib,json
from datetime import date,timedelta
from decimal import Decimal as D
from pathlib import Path
from whole_portfolio_robustness_v2_engine import cash_delta, run_cash_clock
from whole_portfolio_robustness_v2_input_validator import *

def fixture(tmp_path, *, pair='SOLUSD', missing=False, status=200):
    rows=[];d=date(2021,5,31)
    while d<=date(2026,7,31):
        if not(missing and d==date(2021,6,2)): rows.append({'symbol':'SOL','pair':pair,'date':d.isoformat(),'close_at':(d+timedelta(days=1)).isoformat()+'T00:00:00Z','close':'1'})
        d+=timedelta(days=1)
    raw=tmp_path/'raw.json';raw.write_text(json.dumps(rows))
    receipt={'response_status':status,'provider':'ALPACA_CRYPTO','dataset_id':'crypto:SOL:alpaca','endpoint_locator':'https://data.alpaca.markets/v1beta3/crypto/us/bars?symbols=SOL%2FUSD'}
    rec=tmp_path/'receipt.json';rec.write_text(json.dumps(receipt));return rows,raw,receipt

def test_complete_crypto_and_predecessor_close(tmp_path):
    rows,_,_=fixture(tmp_path);assert validate_crypto(rows,'SOL',date(2021,6,1),date(2026,7,31))==[]

def test_missing_coverage_pair_and_predecessor_fail(tmp_path):
    rows,_,_=fixture(tmp_path,missing=True);assert 'incomplete calendar coverage' in validate_crypto(rows,'SOL',date(2021,6,1),date(2026,7,31))[-1]
    rows[0]['pair']='SOLUSDT';assert any('identity' in x for x in validate_crypto(rows,'SOL',date(2021,6,1),date(2026,7,31)))

def test_malformed_receipt_hash_status_transport(tmp_path):
    _,raw,receipt=fixture(tmp_path,status=404);receipt['endpoint_locator']='not-a-url';receipt['provider']='UNVERIFIED'
    e=validate_receipt(receipt,raw,provider='P',pair='SOLUSD');assert len(e)>=3

def test_nonfinite_and_boolean_crypto_close_rejected(tmp_path):
    rows,_,_=fixture(tmp_path)
    for invalid in ('NaN','Infinity',True):
        altered=[dict(x) for x in rows];altered[0]['close']=invalid
        assert any('close' in x for x in validate_crypto(altered,'SOL',date(2021,6,1),date(2026,7,31)))

def test_rate_shock_not_available_at_midnight():
    # Input mapping must be keyed by actual availability; no engine inference from observation labels.
    prior=D('1'); shock=D('9')
    rows=run_cash_clock(date(2025,1,2),date(2025,1,3),D(100),{}, {date(2025,1,2):prior,date(2025,1,3):shock},D(0),set())
    assert D(rows[0]['unposted_interest'])==cash_delta(D(100),prior,D(0))

def test_historical_admission_is_result_free_and_fails_precisely():
    r=historical_admission();assert not r['admitted'] and not r['historical_results_executed']
    assert any('SOL' in e for e in r['errors'])
