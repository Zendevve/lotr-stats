import unittest,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import ordinal,build
class DataTests(unittest.TestCase):
 def test_age_boundary(self):
  self.assertEqual(ordinal('TA',1)-ordinal('SA',3441),1)
  self.assertEqual(ordinal('FA',120)-ordinal('TA',3019),122)
  with self.assertRaises(ValueError):ordinal('TA',0)
 def test_exceptional_tenures(self):
  t=build();r=t['mart_ruler_reigns']
  self.assertEqual(len([x for x in r if x['person_id']=='gondor-eldacar']),2)
  self.assertEqual(sum(x['reign_years'] for x in r if x['person_id']=='gondor-eldacar'),48)
  self.assertFalse(next(x for x in r if x['person_id']=='chieftains-aranarth')['eligible'])
  self.assertEqual(len([x for x in r if x['office_id']=='stewards']),26)
 def test_genealogy_acyclic(self):
  edges=json.loads((Path(__file__).resolve().parents[2]/'data/raw/relationships.json').read_text())
  def visit(node,path):
   self.assertNotIn(node,path)
   for e in edges:
    if e['source_person_id']==node:visit(e['target_person_id'],path|{node})
  for e in edges:visit(e['source_person_id'],set())
if __name__=='__main__':unittest.main()

class CoverageTests(unittest.TestCase):
 def test_completed_curation_and_provenance(self):
  t=build();ps={p['person_id']:p for p in t['persons']};rulers={r['person_id']:r for r in t['mart_ruler_reigns']}
  self.assertEqual(len(rulers),125)
  self.assertEqual(sum(r['lifespan'] is not None for r in rulers.values()),123)
  self.assertEqual({pid for pid,r in rulers.items() if r['lifespan'] is None},{'gondor-earnur','numenor-ar-pharazon'})
  self.assertEqual(rulers['numenor-elros-tar-minyatur']['lifespan'],500)
  self.assertEqual(rulers['chieftains-aragorn-ii']['lifespan'],210)
  self.assertEqual(ps['gondor-minardil']['birth_year'],1454)
  self.assertEqual(ps['gondor-earnil-i']['death_year'],936)
  sources={s['source_id'] for s in t['sources']}
  for pid in rulers:
   self.assertEqual(ps[pid]['review_status'],'reviewed')
   self.assertIsNotNone(ps[pid]['birth_year'])
   self.assertTrue(any(e['target_person_id']==pid for e in t['relationships']))
   for field in ['birth_year','death_year','reported_lifespan']:
    self.assertTrue(any(f['entity_id']==pid and f['field_name']==field and f['source_id'] in sources for f in t['field_sources']))
  for e in t['relationships']:
   self.assertIn(e['source_id'],sources)
   if e['relationship_type']=='parent':
    a,b=ps[e['source_person_id']],ps[e['target_person_id']]
    if a['birth_year'] and b['birth_year'] and a['birth_age']==b['birth_age']:self.assertLess(a['birth_year'],b['birth_year'])
 def test_collateral_branches(self):
  t=build();edges=t['relationships']
  self.assertFalse(any(e['source_person_id']=='numenor-tar-telperien' and e['target_person_id']=='numenor-tar-minastir' for e in edges))
  self.assertTrue(any(e['source_person_id']=='family-morwen' and e['target_person_id']=='stewards-egalmoth' and e['relationship_type']=='ancestor' and e['generations']==2 for e in edges))
  ancestors=set()
  def trace(pid):
   for e in edges:
    if e['target_person_id']==pid and e['source_person_id'] not in ancestors:
     ancestors.add(e['source_person_id']);trace(e['source_person_id'])
  trace('chieftains-aragorn-ii')
  self.assertTrue({'gondor-ondoher','family-firiel','gondor-anarion','arnor-isildur','numenor-tar-elendil'}<=ancestors)
