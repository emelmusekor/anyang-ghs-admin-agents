from pathlib import Path
import csv, json
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'source'/'data'
def registrations():
    rows=list(csv.DictReader((DATA/'registrations.csv').open(encoding='utf-8')))
    latest={}
    for r in rows:
        rid=r['request_id']
        if rid not in latest or r['updated_at']>latest[rid]['updated_at']: latest[rid]=r
    active=[r for r in latest.values() if r['status']=='active' and r['name'] and r['email']]
    cancelled=[r for r in latest.values() if r['status']=='cancelled']
    errors=[r for r in latest.values() if not r['name'] or not r['email']]
    emails={}
    for r in active: emails.setdefault(r['email'],[]).append(r)
    review=[rs for rs in emails.values() if len(rs)>1]
    return {'active':len(active),'cancelled':len(cancelled),'review':len(review),'error':len(errors)}
def budget():
    rows=list(csv.DictReader((DATA/'budget.csv').open(encoding='utf-8')))
    mismatch=[]; total=0
    for r in rows:
        calc=int(r['qty'])*int(r['unit_price']); total+=calc
        if calc!=int(r['stated_amount']): mismatch.append(r['item'])
    return {'calculated_total':total,'mismatch_items':mismatch}
if __name__=='__main__': print(json.dumps({'registration':registrations(),'budget':budget()},ensure_ascii=False,indent=2))
