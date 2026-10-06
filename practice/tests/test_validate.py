from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import validate
def test_registration_counts():
    r=validate.registrations()
    assert r['cancelled']==1
    assert r['error']==1
def test_budget_mismatch():
    assert '간식' in validate.budget()['mismatch_items']
