import {createRequire} from 'node:module';
import {readFileSync} from 'node:fs';
import {gunzipSync} from 'node:zlib';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
const duck=require('@duckdb/duckdb-wasm/blocking');
const db=await duck.createDuckDB({mvp:{mainModule:resolve('node_modules/@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm')}},new duck.ConsoleLogger(duck.LogLevel.WARNING),duck.NODE_RUNTIME);
await db.instantiate();
const c=db.connect();
for(const name of ['persons','reigns','realms','offices','aliases','relationships','sources','field_sources','events','houses','mart_ruler_reigns','mart_realm_summary','mart_succession']){
 db.registerFileBuffer(name+'.parquet',new Uint8Array(readFileSync('public/data/'+name+'.parquet')));
 c.query(`CREATE TABLE ${name} AS SELECT * FROM read_parquet('${name}.parquet')`);
}
c.query('CREATE VIEW ruler_reigns AS SELECT * FROM mart_ruler_reigns');
c.query('CREATE VIEW rulers AS SELECT * FROM persons WHERE is_ruler=true');
c.query('SET enable_external_access=false');
const result=c.query('SELECT realm_name, COUNT(*) AS tenures, ROUND(AVG(reign_years),1) AS mean_years, MEDIAN(reign_years) AS median_years FROM ruler_reigns WHERE eligible=true GROUP BY realm_name ORDER BY median_years DESC');
assert.equal(result.numRows,7);
assert.equal(Number(c.query('SELECT COUNT(*) AS n FROM persons WHERE is_ruler=true').toArray()[0].n),125);
assert.equal(Number(c.query("SELECT SUM(reign_years) AS n FROM ruler_reigns WHERE person_id='gondor-eldacar'").toArray()[0].n),48);
assert.throws(()=>c.query("SELECT * FROM read_parquet('https://example.com/no.parquet')"));
assert.equal(Number(c.query('SELECT COUNT(*) n FROM rulers').toArray()[0].n),125);
assert.equal(Number(c.query('SELECT COUNT(*) n FROM persons').toArray()[0].n),153);
for(const match of readFileSync('components/atlas-sql.tsx','utf8').matchAll(/sql:`([^`]+)`/g)){
 const clean=match[1].replaceAll('\\n','\n').replace(/;\s*$/,'');
 assert.ok(c.query(`SELECT * FROM (${clean}\n) AS result LIMIT 1000`).numRows>0);
}
assert.equal(c.query('SELECT * FROM persons WHERE false').numRows,0);
assert.throws(()=>c.query('SELECT nonexistent_column FROM persons'));
assert.equal(c.query('SELECT 1 AS recovered').numRows,1);
assert.equal(c.query('SELECT * FROM (SELECT * FROM range(10000)) AS result LIMIT 1000').numRows,1000);
assert.throws(()=>c.query("SELECT * FROM read_csv('/etc/passwd')"));
const hash=x=>createHash('sha256').update(x).digest('hex');
assert.equal(hash(gunzipSync(readFileSync('public/duckdb/duckdb-mvp.wasm.gz'))),hash(readFileSync('node_modules/@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm')));
assert.equal(hash(readFileSync('public/duckdb/duckdb-browser-mvp.worker.js')),hash(readFileSync('node_modules/@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js')));
console.log('PASS: real WASM SQL, all 13 Parquet tables, all example queries, aliases, empty/error recovery, row cap, external-access restrictions and shipped engine assets.');
c.close();
