"""Manually transcribed facts; no scraped prose. Regenerate raw normalized tables."""
import json, unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def slug(s): return ''.join(c for c in unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace(' ','-') if c.isalnum() or c=='-')
persons={}; reigns=[]; relationships=[]; sources=[]; field_sources=[]; aliases=[]
groups=[('numenor','Númenor','Monarch','Elros','#a27c38','King_of_Númenor'),('arnor','Arnor','King','Isildur','#56817d','King_of_Arnor'),('arthedain','Arthedain','King','Isildur','#87976d','King_of_Arthedain'),('chieftains','Chieftains','Chieftain','Isildur','#748799','Chieftain_of_the_Dúnedain'),('gondor','Gondor','King','Anárion','#556579','King_of_Gondor'),('stewards','Ruling Stewards','Ruling Steward','Húrin','#967c7a','Stewards'),('reunited','Reunited Kingdom','High King','Telcontar','#9b884d','Aragorn')]
for gid,name,office,house,color,page in groups:
 sources.append(dict(source_id=gid,title='Tolkien Gateway: '+page.replace('_',' '),url='https://tolkiengateway.net/wiki/'+page,reference='Unfinished Tales, The Line of Elros' if gid=='numenor' else 'The Lord of the Rings, Appendices A and B',accessed='2026-09-28',status='Secondary reference checked; primary citation supplied for review'))
sources.append(dict(source_id='lifespans',title='Zarkanya: recorded Númenórean lifespans, Appendix 1',url='https://www.zarkanya.net/Tolkien/Decline%20of%20the%20Numenoreans.htm',reference='Unfinished Tales, The Line of Elros',accessed='2026-09-28',status='Recorded dates only; speculative estimates excluded'))
def add(g,name,start,end,age='TA',endage=None,status='recorded',note='',succ='unclassified',person=None):
 pid=person or g+'-'+slug(name); rid=g+'-'+pid+'-'+str(start)
 if pid not in persons: persons[pid]=dict(person_id=pid,canonical_name=name,slug=pid,house_id=next(x[3] for x in groups if x[0]==g),birth_age=None,birth_year=None,death_age=None,death_year=None,sex='F' if name in ['Tar-Ancalimë','Tar-Telperiën','Tar-Vanimeldë'] else 'M')
 reigns.append(dict(reign_id=rid,person_id=pid,office_id=g,start_age=age,start_year=start,end_age=endage or age,end_year=end,status=status,note=note,succession_type=succ,source_id=g))
 for field in ['start_age','start_year','end_age','end_year','status']:
  field_sources.append(dict(entity_type='reigns',entity_id=rid,field_name=field,source_id=g))
 return pid
num='''Elros Tar-Minyatur|32|442
Vardamir Nólimon|442|443
Tar-Amandil|443|590
Tar-Elendil|590|740
Tar-Meneldur|740|883
Tar-Aldarion|883|1075
Tar-Ancalimë|1075|1280
Tar-Anárion|1280|1394
Tar-Súrion|1394|1556
Tar-Telperiën|1556|1731
Tar-Minastir|1731|1869
Tar-Ciryatan|1869|2029
Tar-Atanamir|2029|2221
Tar-Ancalimon|2221|2386
Tar-Telemmaitë|2386|2526
Tar-Vanimeldë|2526|2637
Tar-Anducal|2637|2657
Tar-Alcarin|2657|2737
Tar-Calmacil|2737|2825
Tar-Ardamin|2825|2899
Ar-Adûnakhôr|2899|2962
Ar-Zimrathôn|2962|3033
Ar-Sakalthôr|3033|3102
Ar-Gimilzôr|3102|3177
Tar-Palantir|3177|3255
Ar-Pharazôn|3255|3319'''
for i,line in enumerate(num.splitlines()):
 n,s,e=line.split('|'); stat='titular' if i==1 else 'usurper' if i in [16,25] else 'recorded'
 note={1:'Nominal one-year convention. Vardamir immediately yielded power; effective rule by Tar-Amandil began in SA 442.',2:'Formal regnal convention starts in SA 443; effective rule began in SA 442.',10:'Accession chronology and the fleet sent in SA 1700 are not fully aligned across accounts.',17:'Effective reign from SA 2657; legal claim dates from SA 2637.',25:'End of rule is the Downfall; fate is not treated as an ordinary death.'}.get(i,'')
 add('numenor',n,int(s),int(e),'SA',status=stat,note=note,succ='usurpation' if stat=='usurper' else 'unclassified')
births=[None,61,192,350,543,700,873,1003,1174,1320,1474,1634,1800,1986,2136,2277,2286,2406,2516,2618,2709,2798,2876,2960,3035,3118]
deaths=[None,471,603,751,942,1098,1285,1404,1574,1731,1873,2035,2221,2386,2526,2637,2657,2737,2825,2899,2962,3033,3102,3177,3255,None]
for p,b,d in zip(list(persons.values()),births,deaths):
 p.update(birth_age='SA' if b else None,birth_year=b,death_age='SA' if d else None,death_year=d)
 for f in ['birth_year','death_year']:
  if p[f]!=None: field_sources.append(dict(entity_type='persons',entity_id=p['person_id'],field_name=f,source_id='lifespans'))
elendil=add('arnor','Elendil',3320,3441,'SA',succ='foundation')
isildur=add('arnor','Isildur',3441,2,'SA','TA',succ='parent-child')
def chain(g,text,start,firstsucc='unclassified'):
 prev=None
 for i,line in enumerate(text.splitlines()):
  n,e=line.split('|'); e=int(e); pid=add(g,n,start,e,succ=firstsucc if i==0 else 'parent-child' if g in ['arnor','arthedain','chieftains'] else 'unclassified')
  if prev and g in ['arnor','arthedain','chieftains']: relationships.append(dict(source_person_id=prev,target_person_id=pid,relationship_type='parent',source_id=g))
  prev=pid; start=e
chain('arnor','''Valandil|249
Eldacar|339
Arantar|435
Tarcil|515
Tarondor|602
Valandur|652
Elendur|777
Eärendur|861''',2,'parent-child')
chain('arthedain','''Amlaith|946
Beleg|1029
Mallor|1110
Celepharn|1191
Celebrindor|1272
Malvegil|1349
Argeleb I|1356
Arveleg I|1409
Araphor|1589
Argeleb II|1670
Arvegil|1743
Arveleg II|1813
Araval|1891
Araphant|1964
Arvedui|1974''',861,'institutional transition')
chain('chieftains','''Aranarth|2106
Arahael|2177
Aranuir|2247
Aravir|2319
Aragorn I|2327
Araglas|2455
Arahad I|2523
Aragost|2588
Aravorn|2654
Arahad II|2719
Arassuil|2784
Arathorn I|2848
Argonui|2912
Arador|2930
Arathorn II|2933
Aragorn II|3019''',1976,'institutional transition')
for r in reigns:
 if r['person_id']=='chieftains-aranarth': r.update(status='uncertain',note='Institution established TA 1976 in Appendix B; regnal lists also use TA 1975. This dataset uses 1976 and excludes the tenure from default statistics.')
 if r['person_id']=='arthedain-arvedui': r['note']='Kingdom fell TA 1974; Arvedui died TA 1975. Office end and death are distinct.'
add('gondor','Elendil',3320,3441,'SA',person=elendil,status='overlord',note='High kingship overlaps the local co-rulers. Excluded from default duration comparisons.')
add('gondor','Anárion',3320,3440,'SA',status='co-ruler')
add('gondor','Isildur',3320,2,'SA','TA',person=isildur,status='co-ruler')
chain('gondor','''Meneldil|158
Cemendur|238
Eärendil|324
Anardil|411
Ostoher|492
Rómendacil I|541
Turambar|667
Atanatar I|748
Siriondil|830
Tarannon Falastur|913
Eärnil I|936
Ciryandil|1015
Hyarmendacil I|1149
Atanatar II Alcarin|1226
Narmacil I|1294
Calmacil|1304
Rómendacil II|1366
Valacar|1432
Eldacar|1437
Castamir|1447''',2)
add('gondor','Eldacar',1447,1490,person='gondor-eldacar',succ='restoration',note='Second tenure; the ten-year exile is excluded.')
chain('gondor','''Aldamir|1540
Hyarmendacil II|1621
Minardil|1634
Telemnar|1636
Tarondor|1798
Telumehtar Umbardacil|1850
Narmacil II|1856
Calimehtar|1936
Ondoher|1944''',1490)
add('gondor','Eärnil II',1945,2043,succ='other relative',note='TA 1944–1945 interregnum is not assigned to a king.')
add('gondor','Eärnur',2043,2050,succ='parent-child',note='Disappeared TA 2050; this is an office end, not a verified death date.')
for r in reigns:
 if r['person_id']=='gondor-castamir':r.update(status='usurper',succession_type='usurpation')
 if r['person_id']=='gondor-calmacil':r['succession_type']='sibling'
 if r['person_id'] in ['gondor-earnil-i','gondor-tarondor']:r['succession_type']='other relative'
chain('stewards','''Mardil Voronwë|2080
Eradan|2116
Herion|2148
Belegorn|2204
Húrin I|2244
Túrin I|2278
Hador|2395
Barahir|2412
Dior|2435
Denethor I|2477
Boromir|2489
Cirion|2567
Hallas|2605
Húrin II|2628
Belecthor I|2655
Orodreth|2685
Ecthelion I|2698
Egalmoth|2743
Beren|2763
Beregond|2811
Belecthor II|2872
Thorondir|2882
Túrin II|2914
Turgon|2953
Ecthelion II|2984
Denethor II|3019''',2050,'institutional transition')
add('reunited','Aragorn II',3019,120,'TA','FA',person='chieftains-aragorn-ii',succ='restoration',note='Year-level convention uses SA 3441 and TA 3021 as era lengths; exact month/day durations are not claimed.')
for a,b,src in [('arnor-elendil','arnor-isildur','arnor'),('arnor-isildur','arnor-valandil','arnor'),('arnor-earendur','arthedain-amlaith','arthedain'),('arthedain-arvedui','chieftains-aranarth','chieftains'),('arnor-elendil','gondor-anarion','gondor'),('gondor-anarion','gondor-meneldil','gondor')]: relationships.append(dict(source_person_id=a,target_person_id=b,relationship_type='parent',source_id=src))
for pid,names in {'chieftains-aragorn-ii':['Elessar','Strider','Estel','Telcontar'],'numenor-tar-calmacil':['Ar-Belzagar'],'numenor-tar-ardamin':['Ar-Abattârik'],'numenor-tar-palantir':['Ar-Inziladûn'],'numenor-tar-anducal':['Herucalmo'],'gondor-eldacar':['Vinitharya'],'gondor-romendacil-ii':['Minalcar']}.items():
 for n in names:aliases.append(dict(person_id=pid,name=n,source_id='numenor' if pid.startswith('numenor') else 'gondor'))
events=[]
for name,age,year,g in [('Downfall of Númenor','SA',3319,'numenor'),('Realms in Exile founded','SA',3320,'arnor'),('End of the Last Alliance','SA',3441,'gondor'),('Division of Arnor','TA',861,'arnor'),('Kin-strife: usurpation','TA',1437,'gondor'),('Eldacar restored','TA',1447,'gondor'),('Great Plague','TA',1636,'gondor'),('Fall of Arthedain','TA',1974,'arthedain'),('Disappearance of Eärnur','TA',2050,'gondor'),('Restoration of kingship','TA',3019,'reunited')]:events.append(dict(event_id=slug(name),name=name,age=age,year=year,realm_id=g,source_id=g))
realms=[dict(realm_id=g,name=n,color=c) for g,n,o,h,c,p in groups]
offices=[dict(office_id=g,realm_id=g,name=o,house_id=h) for g,n,o,h,c,p in groups]
tables=dict(persons=list(persons.values()),reigns=reigns,realms=realms,offices=offices,relationships=relationships,sources=sources,field_sources=field_sources,aliases=aliases,events=events,houses=[dict(house_id=h,name='House of '+h) for h in dict.fromkeys(x[3] for x in groups)])
persons['arnor-elendil']['house_id']='Elendil'
tables['houses'].append(dict(house_id='Elendil',name='House of Elendil'))
for table,rows in tables.items(): (ROOT/'data/raw'/f'{table}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(f'{len(persons)} people; {len(reigns)} tenures')

# Apply the reviewed genealogy and lifespan extension on every regeneration.
from curate import curate
curate()
