import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import ts from 'typescript';
async function load(file){const js=ts.transpileModule(readFileSync(file,'utf8'),{compilerOptions:{module:ts.ModuleKind.ESNext,target:ts.ScriptTarget.ES2022}}).outputText;return import('data:text/javascript;base64,'+Buffer.from(js).toString('base64'))}
const {readOnlyQuery,resultValue}=await load('lib/atlas/query.ts');
const {filterRulers}=await load('lib/atlas/explorer.ts');
const atlas=JSON.parse(readFileSync('lib/atlas/data.json'));
const defaults={q:'',realm:'all',status:'all',min:'',max:'',sort:'chronology',ascending:true};
const rows=f=>filterRulers(atlas.rulers,{...defaults,...f});
assert.equal(rows({}).length,129);
assert.equal(rows({status:'eligible'}).length,121);
assert.equal(rows({realm:'stewards'}).length,26);
assert.equal(rows({q:'  EARNUr '})[0].person_id,'gondor-earnur');
assert.equal(rows({q:'aragorn ii'}).length,2);
assert.equal(rows({min:'500'}).length,0);
assert.equal(rows({min:'80',max:'20'}).length,0);
assert.equal(rows({status:'usurper'}).length,3);
assert.equal(rows({sort:'duration',ascending:false})[0].reign_years,410);
for(const realm of atlas.realms){const eligible=rows({realm:realm.realm_id,status:'eligible'});const summary=atlas.summaries.find(s=>s.realm_id===realm.realm_id);assert.equal(eligible.length,summary.n)}
for(const sql of ['SELECT 1;','-- comment\n SELECT 1; -- end',"SELECT 'DROP; TABLE' AS text;",'WITH x AS (SELECT 1) SELECT * FROM x','/* outer /* inner */ */ SELECT 1','SELECT 1 -- trailing comment',"SELECT 'it''s fine' AS value"]){assert.ok(readOnlyQuery(sql))}
for(const sql of ['', 'DROP TABLE persons','SELECT 1; SELECT 2','SELECT 1; DELETE FROM persons',"SELECT 'open",'SELECT 1 /* open','WITH x AS (DELETE FROM persons RETURNING *) SELECT * FROM x'])assert.throws(()=>readOnlyQuery(sql));
assert.equal(readOnlyQuery('SELECT 1; -- end'),'SELECT 1');
assert.deepEqual(resultValue({a:1n,b:[2n],c:null}),{a:'1',b:['2'],c:null});
console.log('PASS: filters, accent-insensitive search, sorting, institution summaries, SQL validation and nested result serialization.');
