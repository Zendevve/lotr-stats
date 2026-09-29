"""Deterministic normalized JSON -> validated marts, CSV and Parquet."""
import csv,json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def ordinal(age,year):
 if age not in ('SA','TA','FA') or not isinstance(year,int) or year<1: raise ValueError('Invalid Arda date')
 if age=='SA' and year>3441 or age=='TA' and year>3021: raise ValueError('Year exceeds era')
 return {'SA':0,'TA':3441,'FA':6462}[age]+year

def build():
 tables={p.stem:json.loads(p.read_text()) for p in (ROOT/'data/raw').glob('*.json')}
 ps={p['person_id']:p for p in tables['persons']}; offices={o['office_id']:o for o in tables['offices']}; realms={r['realm_id']:r for r in tables['realms']}; src={s['source_id'] for s in tables['sources']}
 assert len(ps)==len(tables['persons'])
 ids=[r['reign_id'] for r in tables['reigns']]; assert len(set(ids))==len(ids)
 for r in tables['relationships']:assert r['source_person_id'] in ps and r['target_person_id'] in ps and r['source_person_id']!=r['target_person_id']
 # Validate every normalized foreign key before labeling a bundle as validated.
 house_ids={h['house_id'] for h in tables['houses']}
 for p in ps.values():assert p['house_id'] in house_ids and p['life_source_id'] in src
 for a in tables['aliases']:assert a['person_id'] in ps and a['source_id'] in src
 for e in tables['events']:assert e['realm_id'] in realms and e['source_id'] in src
 for e in tables['relationships']:assert e['source_id'] in src and e['relationship_type'] in ('parent','ancestor')
 for f in tables['field_sources']:
  assert f['source_id'] in src
  assert f['entity_id'] in (ps if f['entity_type']=='persons' else ids)
 def visit(pid,path):
  assert pid not in path, 'Cyclic genealogy'
  for e in tables['relationships']:
   if e['source_person_id']==pid:visit(e['target_person_id'],path|{pid})
 for pid in ps:visit(pid,set())
 marts=[]
 for r in tables['reigns']:
  assert r['person_id'] in ps and r['office_id'] in offices and r['source_id'] in src
  p=ps[r['person_id']]; office=offices[r['office_id']]; realm=realms[office['realm_id']]
  start=ordinal(r['start_age'],r['start_year']); end=ordinal(r['end_age'],r['end_year']); assert end>=start
  life=p.get('reported_lifespan') or (None if p['birth_year'] is None or p['death_year'] is None else ordinal(p['death_age'],p['death_year'])-ordinal(p['birth_age'],p['birth_year']))
  assert life is None or life>0
  if p['birth_year'] is not None and p['birth_age']!='First Age':assert ordinal(p['birth_age'],p['birth_year'])<=start
  assert all(any(f['entity_id']==r['reign_id'] and f['field_name']==field for f in tables['field_sources']) for field in ['start_year','end_year'])
  events=[e for e in tables['events'] if e['realm_id']==r['office_id'] and start<=ordinal(e['age'],e['year'])<=end]
  marts.append(dict(p | r,ruler_name=p['canonical_name'],realm_name=realm['name'],color=realm['color'],office_name=office['name'],start_sort=start,end_sort=end,reign_years=end-start,lifespan=life,accession_age=None if p['birth_year'] is None or p['birth_age']=='First Age' else start-ordinal(p['birth_age'],p['birth_year']),eligible=r['status']=='recorded',event_count=len(events),event_density=len(events)/(end-start) if end>start else None,aliases='; '.join(a['name'] for a in tables['aliases'] if a['person_id']==p['person_id'])))
 summaries=[]
 for rid,realm in realms.items():
  rows=[r for r in marts if r['office_id']==rid and r['eligible']]; values=[r['reign_years'] for r in rows]
  summaries.append(dict(realm_id=rid,realm_name=realm['name'],n=len(values),mean=round(statistics.mean(values),2),median=statistics.median(values),minimum=min(values),maximum=max(values),variance=round(statistics.pvariance(values),2),lifespan_known=sum(r['lifespan'] is not None for r in rows)))
 tables.update(mart_ruler_reigns=marts,mart_realm_summary=summaries,mart_succession=[dict(reign_id=r['reign_id'],realm_name=r['realm_name'],succession_type=r['succession_type']) for r in marts])
 output=ROOT/'public/data'; output.mkdir(exist_ok=True)
 import pyarrow as pa,pyarrow.parquet as pq
 for name,rows in tables.items():
  (output/f'{name}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
  if rows:
   pq.write_table(pa.Table.from_pylist(rows),output/f'{name}.parquet')
   with (output/f'{name}.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 bundle=dict(persons=tables['persons'],rulers=marts,summaries=summaries,realms=tables['realms'],sources=tables['sources'],relationships=tables['relationships'],events=tables['events'],quality=dict(people=len(ps),tenures=len(marts),eligible=sum(r['eligible'] for r in marts),ruler_count=sum(p['is_ruler'] for p in ps.values()),reviewed_rulers=sum(p['is_ruler'] and p['review_status']=='reviewed' for p in ps.values()),missing_lifespan=sum(p['is_ruler'] and p['death_year'] is None for p in ps.values()),known_ruler_lifespans=len({r['person_id'] for r in marts if r['lifespan'] is not None}),warnings=sum(r['status']!='recorded' for r in marts),validated=True))
 (ROOT/'lib/atlas/data.json').write_text(json.dumps(bundle,ensure_ascii=False)+'\n')
 (output/'atlas.json').write_text(json.dumps(bundle,ensure_ascii=False)+'\n')
 print(json.dumps(bundle['quality']))
 return tables
if __name__=='__main__':build()
