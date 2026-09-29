"""Reviewed lifespan and ancestral-branch curation. Idempotent after seed.py."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'data/raw'
def curate():
 t={p.stem:json.loads(p.read_text()) for p in ROOT.glob('*.json')}
 ps={p['person_id']:p for p in t['persons'] if not p['person_id'].startswith('family-')}
 ruler_ids=set(ps)
 sources={s['source_id']:s for s in t['sources']}
 def source(key,page,reference='The Lord of the Rings, Appendix A; The Peoples of Middle-earth, The Heirs of Elendil'):
  sources[key]=dict(source_id=key,title='Tolkien Gateway: '+page.replace('_',' '),url='https://tolkiengateway.net/wiki/'+page,reference=reference,accessed='2026-09-29',status='Secondary genealogy and date reference reviewed; primary citation supplied')
 for key,page in [('family-numenor','House_of_Elros'),('family-north','House_of_Isildur'),('family-gondor','House_of_Anárion'),('family-stewards','House_of_Húrin'),('elros-life','Elros'),('aragorn-life','Aragorn'),('minardil-life','Minardil'),('pharazon-fate','Ar-Pharazôn'),('earnur-fate','Eärnur'),('gilraen-life','Gilraen'),('herucalmo-family','Herucalmo')]:source(key,page)
 sources['family-numenor']['reference']='Unfinished Tales, The Line of Elros; The Silmarillion, Akallabêth'
 sources['herucalmo-family']['reference']='Unfinished Tales, The Line of Elros'
 sources['elros-life']['reference']='The War of the Jewels, The Tale of Years; Unfinished Tales, The Line of Elros'
 sources['pharazon-fate']['reference']='The Silmarillion, Akallabêth; Unfinished Tales, The Line of Elros'
 def group(g):return [p for p in ps if p.startswith(g+'-')]
 def dates(g,pairs):
  ids=group(g); pairs=pairs.split(); assert len(ids)==len(pairs),(g,len(ids),len(pairs))
  for pid,pair in zip(ids,pairs):
   b,d=map(int,pair.split(':')); p=ps[pid];p.update(birth_age='TA',birth_year=b,death_age='TA' if d else None,death_year=d or None)
 dates('arnor','3119:3441 3209:2 3430:249 87:339 185:435 280:515 372:602 462:652 552:777 640:861')
 dates('arthedain','726:946 812:1029 895:1110 979:1191 1062:1272 1144:1349 1226:1356 1309:1409 1391:1589 1473:1670 1553:1743 1633:1813 1711:1891 1789:1964 1864:1975')
 dates('chieftains','1938:2106 2012:2177 2084:2247 2156:2319 2227:2327 2296:2455 2365:2523 2431:2588 2497:2654 2563:2719 2628:2784 2693:2848 2757:2912 2820:2930 2873:2933 2931:120')
 dates('gondor','3219:3440 3318:158 3399:238 48:324 136:411 222:492 310:541 397:667 480:748 570:830 654:913 736:936 820:1015 899:1149 977:1226 1049:1294 1058:1304 1126:1366 1194:1432 1255:1490 1259:1447 1330:1540 1391:1621 1454:1634 1516:1636 1577:1798 1632:1850 1684:1856 1736:1936 1787:1944 1883:2043 1928:0')
 dates('stewards','1960:2080 1999:2116 2037:2148 2074:2204 2124:2244 2165:2278 2245:2395 2290:2412 2328:2435 2375:2477 2410:2489 2449:2567 2480:2605 2515:2628 2545:2655 2576:2685 2600:2698 2626:2743 2655:2763 2700:2811 2752:2872 2782:2882 2815:2914 2855:2953 2886:2984 2930:3019')
 for pid in ['arnor-elendil','arnor-isildur','arnor-valandil','gondor-anarion','gondor-meneldil','gondor-cemendur']:ps[pid]['birth_age']='SA'
 for pid in ['arnor-elendil','gondor-anarion']:ps[pid]['death_age']='SA'
 ps['chieftains-aragorn-ii']['death_age']='FA'
 ps['numenor-elros-tar-minyatur'].update(birth_age='First Age',birth_year=532,death_age='SA',death_year=442)
 ps['numenor-ar-pharazon'].update(birth_age='SA',birth_year=3118,death_age=None,death_year=None)
 def family(key,name,house,sex='M',birth=None,death=None,age='TA'):
  pid='family-'+key;ps[pid]=dict(person_id=pid,canonical_name=name,slug=pid,house_id=house,birth_age=age if birth else None,birth_year=birth,death_age=age if death else None,death_year=death,sex=sex);return pid
 for args in [('isilmo','Isilmo','Elros'),('gimilkhad','Gimilkhâd','Elros','M',3044,3243,'SA'),('miriel','Tar-Míriel','Elros','F',3117,3319,'SA'),('inzilbeth','Inzilbêth','Elros','F'),('silmarien','Silmariën','Elros','F',521,None,'SA'),('elatan','Elatan','Elros'),('valandil-andunie','Valandil of Andúnië','Elros','M',630,None,'SA'),('numendil','Númendil','Elros'),('amandil','Amandil of Andúnië','Elros'),('earendil-halfelven','Eärendil the Half-elven','Elros'),('elwing','Elwing','Elros','F'),('almarian','Almarian','Elros','F'),('erendis','Erendis','Elros','F',771,985,'SA'),('hallacar','Hallacar','Elros','M',852,1211,'SA'),('tarciryan','Tarciryan','Anárion'),('calimehtar-prince','Calimehtar, son of Calmacil','Anárion'),('vidumavi','Vidumavi','Anárion','F',None,1332),('minastan','Minastan','Anárion'),('arciryas','Arciryas','Anárion'),('calimmacil','Calimmacil','Anárion'),('siriondil-prince','Siriondil, father of Eärnil II','Anárion'),('firiel','Fíriel','Anárion','F',1896),('gilraen','Gilraen','Isildur','F',2907,3007),('rian','Rían, daughter of Barahir','Húrin','F'),('morwen','Morwen, daughter of Belecthor I','Húrin','F'),('vorondil','Vorondil','Húrin','M',1919,2029),('pelendur','Pelendur','Húrin','M',1879,1998),('hurin-emyn-arnen','Húrin of Emyn Arnen','Húrin')]:family(*args)
 edges=[]
 def edge(a,b,src,kind='parent',generations=1):
  assert a in ps and b in ps,(a,b)
  edges.append(dict(source_person_id=a,target_person_id=b,relationship_type=kind,source_id=src,generations=generations))
 def chain(ids,src):
  for a,b in zip(ids,ids[1:]):edge(a,b,src)
 n=group('numenor'); north=group('arnor')+group('arthedain')+group('chieftains');g=group('gondor');s=group('stewards')
 chain(n[:10],'family-numenor');chain([n[8],'family-isilmo']+n[10:16],'family-numenor');chain(n[17:25],'family-numenor')
 for a,b in [(n[15],n[17]),(n[16],n[17]),(n[23],'family-gimilkhad'),('family-gimilkhad',n[25]),(n[24],'family-miriel'),('family-inzilbeth',n[23+1]),('family-inzilbeth','family-gimilkhad'),(n[3],'family-silmarien'),('family-silmarien','family-valandil-andunie'),('family-elatan','family-valandil-andunie'),('family-numendil','family-amandil'),('family-amandil',north[0]),('family-earendil-halfelven',n[0]),('family-elwing',n[0]),('family-almarian',n[5]),('family-erendis',n[6]),('family-hallacar',n[7])]:edge(a,b,'family-numenor')
 edge(n[12],n[16],'herucalmo-family','ancestor',3);edge('family-valandil-andunie','family-numendil','family-numenor','ancestor',None)
 chain(north,'family-north');edge('family-gilraen',north[-1],'gilraen-life');edge('family-firiel','chieftains-aranarth','family-north')
 chain([north[0]]+g[:11],'family-gondor');chain([g[9],'family-tarciryan']+g[11:16],'family-gondor');chain([g[14]]+g[16:20],'family-gondor');chain([g[19]]+g[21:25],'family-gondor');chain([g[23],'family-minastan']+g[25:30],'family-gondor');chain([g[26],'family-arciryas','family-calimmacil','family-siriondil-prince']+g[30:],'family-gondor')
 edge(g[16],'family-calimehtar-prince','family-gondor');edge('family-calimehtar-prince',g[20],'family-gondor','ancestor',2);edge('family-vidumavi',g[19],'family-gondor');edge(g[29],'family-firiel','family-gondor')
 chain(['family-pelendur','family-vorondil']+s[:9],'family-stewards');chain([s[7],'family-rian']+s[9:17],'family-stewards');edge(s[14],'family-morwen','family-stewards');edge('family-morwen',s[17],'family-stewards','ancestor',2);chain(s[17:],'family-stewards');edge('family-hurin-emyn-arnen','family-pelendur','family-stewards','ancestor',None)
 # Only documented descent is modeled; unknown intervening generations stay explicit.
 provenance=[f for f in t['field_sources'] if f['entity_type']!='persons' and f['field_name']!='succession_type']
 def psource(pid):
  if pid=='numenor-elros-tar-minyatur':return 'elros-life'
  if pid=='chieftains-aragorn-ii':return 'aragorn-life'
  if pid=='gondor-minardil':return 'minardil-life'
  if pid=='numenor-ar-pharazon':return 'pharazon-fate'
  if pid=='gondor-earnur':return 'earnur-fate'
  return 'family-'+('numenor' if ps[pid]['house_id']=='Elros' else 'gondor' if ps[pid]['house_id']=='Anárion' else 'stewards' if ps[pid]['house_id']=='Húrin' else 'north')
 for pid,p in ps.items():
  p.update(is_ruler=pid in ruler_ids,review_status='reviewed',reported_lifespan=500 if pid==n[0] else 210 if pid==north[-1] else None,life_note='',last_known_age=None,last_known_year=None,life_source_id=psource(pid))
  if pid==n[0]:p['life_note']='Reported lifespan 500; First Age birth is retained without an invented cross-Age ordinal.'
  if pid==north[-1]:p['life_note']='Reported age 210 takes precedence over simplified cross-Age year-label subtraction.'
  if pid==n[-1]:p.update(life_note='Fate uncertain: said to lie in the Caves of the Forgotten. Downfall is not treated as an ordinary death.',last_known_age='SA',last_known_year=3319)
  if pid==g[-1]:p.update(life_note='Disappeared after accepting the challenge at Minas Morgul in TA 2050; death date unknown.',last_known_age='TA',last_known_year=2050)
  if not p['death_year'] and not p['life_note']:p['life_note']='Death date not supplied by the cited genealogy; supporting relative, excluded from ruler coverage counts.'
  for field in ['birth_age','birth_year','death_age','death_year','reported_lifespan','life_note','last_known_age','last_known_year','review_status']:
   provenance.append(dict(entity_type='persons',entity_id=pid,field_name=field,source_id=p['life_source_id']))
 parents=lambda pid:{e['source_person_id'] for e in edges if e['target_person_id']==pid and e['relationship_type']=='parent'}
 previous={}
 for r in t['reigns']:
  pid=r['person_id']; prior=previous.get(r['office_id']);typ='foundation / new office'
  if r['status']=='usurper':typ='usurpation'
  elif prior:
   if prior in parents(pid):typ='parent-child'
   elif parents(pid)&parents(prior):typ='sibling'
   elif any(parents(x)&parents(prior) for x in parents(pid)):typ='nephew / niece'
   else:typ='collateral dynastic succession'
  if pid=='gondor-eldacar' and r['start_year']==1447:typ='restoration'
  r['succession_type']=typ;previous[r['office_id']]=pid
  provenance.append(dict(entity_type='reigns',entity_id=r['reign_id'],field_name='succession_type',source_id=r['source_id']))
 t.update(persons=list(ps.values()),relationships=edges,sources=list(sources.values()),field_sources=provenance)
 for name,rows in t.items():(ROOT/(name+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':curate()
