'use client';
import {useState,useRef,useEffect} from 'react';
import {Play,RotateCcw,Download,Database} from 'lucide-react';
import {Table,TableHeader,TableHead,TableBody,TableRow,TableCell} from '@/components/ui/table';
import {Select,SelectContent,SelectItem,SelectTrigger,SelectValue} from '@/components/ui/select';
import {readOnlyQuery,resultValue} from '@/lib/atlas/query';
import {csv} from '@/lib/atlas/types';
import type {AsyncDuckDB,AsyncDuckDBConnection} from '@duckdb/duckdb-wasm';
const examples=[{name:'Reign lengths by institution',sql:`SELECT realm_name, COUNT(*) AS tenures,\n       ROUND(AVG(reign_years), 1) AS mean_years,\n       MEDIAN(reign_years) AS median_years\nFROM ruler_reigns\nWHERE eligible = true\nGROUP BY realm_name\nORDER BY median_years DESC;`},{name:'Three longest reigns per realm',sql:`WITH ranked AS (\n  SELECT ruler_name, realm_name, reign_years,\n    DENSE_RANK() OVER (PARTITION BY realm_name\n      ORDER BY reign_years DESC) AS rank\n  FROM ruler_reigns WHERE eligible = true\n)\nSELECT * FROM ranked WHERE rank <= 3;`},{name:'Missing lifespan coverage',sql:`SELECT realm_name, COUNT(*) AS tenures,\n  COUNT(lifespan) AS known_lifespans\nFROM ruler_reigns GROUP BY realm_name;`},{name:'Recorded succession types',sql:`SELECT realm_name, succession_type, COUNT(*) AS transitions\nFROM mart_succession\nGROUP BY realm_name, succession_type\nORDER BY realm_name, transitions DESC;`}];
const tables=['persons','reigns','realms','offices','aliases','relationships','sources','field_sources','events','houses','mart_ruler_reigns','mart_realm_summary','mart_succession'];
export default function SQLLab(){
 const [query,setQuery]=useState(examples[0].sql),[results,setResults]=useState<Record<string,unknown>[]>([]),[busy,setBusy]=useState(false),[error,setError]=useState(''),[elapsed,setElapsed]=useState<number|null>(null),[ready,setReady]=useState(false);
 const db=useRef<AsyncDuckDB|null>(null),conn=useRef<AsyncDuckDBConnection|null>(null),worker=useRef<Worker|null>(null),timer=useRef<ReturnType<typeof setTimeout>|null>(null),generation=useRef(0),running=useRef(false);
 function release(){worker.current?.terminate();worker.current=null;db.current=null;conn.current=null;}
 useEffect(()=>{try{const q=localStorage.getItem('atlas-query');if(q)setQuery(q)}catch{/* Storage is optional. */}return()=>{generation.current++;release();if(timer.current)clearTimeout(timer.current)}},[]);
 async function init(token:number){
  if(conn.current)return conn.current;
  const check=()=>{if(token!==generation.current)throw new Error('Query cancelled.')};
  const duck=await import('@duckdb/duckdb-wasm');check();
  const w=new Worker('/duckdb/duckdb-browser-mvp.worker.js');worker.current=w;
  const engine=new duck.AsyncDuckDB(new duck.ConsoleLogger(duck.LogLevel.WARNING),w);db.current=engine;
  const compressed=await fetch('/duckdb/duckdb-mvp.wasm.gz');check();
  if(!compressed.ok||!compressed.body)throw new Error('Unable to load the SQL engine. Run again to retry.');
  if(typeof DecompressionStream==='undefined')throw new Error('This browser cannot load the SQL engine. Use a current browser or download the data from Methodology.');
  const wasm=await new Response(compressed.body.pipeThrough(new DecompressionStream('gzip'))).arrayBuffer();check();
  const wasmURL=URL.createObjectURL(new Blob([wasm],{type:'application/wasm'}));
  try{await engine.instantiate(wasmURL)}finally{URL.revokeObjectURL(wasmURL)}check();
  const c=await engine.connect();
  for(const name of tables){const response=await fetch(`/data/${name}.parquet`);check();if(!response.ok)throw new Error(`Unable to load ${name}. Run again to retry.`);const buffer=new Uint8Array(await response.arrayBuffer());check();await engine.registerFileBuffer(`${name}.parquet`,buffer);await c.query(`CREATE TABLE ${name} AS SELECT * FROM read_parquet('${name}.parquet')`);check()}
  await c.query('CREATE VIEW ruler_reigns AS SELECT * FROM mart_ruler_reigns');
  await c.query('CREATE VIEW rulers AS SELECT * FROM persons WHERE is_ruler=true');
  await c.query('SET enable_external_access=false');check();conn.current=c;setReady(true);return c;
 }
 function cancel(){generation.current++;running.current=false;if(timer.current)clearTimeout(timer.current);release();setReady(false);setBusy(false);setError('Query cancelled. The engine will reload on the next run.');}
 async function run(){
  if(running.current)return;
  let clean:string;try{clean=readOnlyQuery(query)}catch(e){setResults([]);setElapsed(null);setError(e instanceof Error?e.message:String(e));return}
  running.current=true;const token=++generation.current;setBusy(true);setError('');setResults([]);setElapsed(null);const start=performance.now();
  timer.current=setTimeout(()=>{if(token!==generation.current)return;generation.current++;running.current=false;release();setReady(false);setBusy(false);setError('The query exceeded its time limit. The engine was reset; simplify the query and run again.')},ready?20000:60000);
  try{const c=await init(token);const res=await c.query(`SELECT * FROM (${clean}\n) AS result LIMIT 1000`);if(token!==generation.current)return;setResults(res.toArray().map(row=>resultValue(row.toJSON()) as Record<string,unknown>));setElapsed(Math.round(performance.now()-start));try{localStorage.setItem('atlas-query',query)}catch{/* Successful queries do not depend on storage. */}}
  catch(e){if(token===generation.current){if(!conn.current){release();setReady(false)}setError(e instanceof Error?e.message:String(e))}}
  finally{if(token===generation.current){if(timer.current)clearTimeout(timer.current);running.current=false;setBusy(false)}}
 }
 const keys=results.length?Object.keys(results[0]):[];
 return <div className="sql-layout"><aside className="schema-panel"><div className="eyebrow"><Database size={14}/> DATASET SCHEMA</div>{tables.map(t=><button key={t} onClick={()=>setQuery(`SELECT * FROM ${t} LIMIT 25;`)}>{t}</button>)}<p>Local Parquet tables. Queries run in your browser. No remote database. The rulers view includes only the 125 officeholders; persons also includes connecting relatives.</p></aside><div><div className="panel sql-editor"><div className="panel-heading"><Select onValueChange={v=>setQuery(examples[Number(v)].sql)} defaultValue="0"><SelectTrigger aria-label="Example query"><SelectValue/></SelectTrigger><SelectContent>{examples.map((e,i)=><SelectItem key={e.name} value={String(i)}>{e.name}</SelectItem>)}</SelectContent></Select><span className="mono">DuckDB · {ready?'ready':'loads on first run'}</span></div><textarea aria-label="SQL query" spellCheck={false} value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();if(!busy)void run()}}}/><div className="sql-actions"><button className="primary-button" disabled={busy} onClick={()=>void run()}><Play size={15}/>{busy?'Running…':'Run query'}</button><span className="muted">Ctrl / ⌘ + Enter</span>{busy&&<button className="outline-button" onClick={cancel}>Cancel</button>}<button className="text-button" disabled={busy} onClick={()=>{try{localStorage.removeItem('atlas-query')}catch{}setQuery(examples[0].sql);setResults([]);setError('');setElapsed(null)}}><RotateCcw size={14}/> Reset</button></div></div>{error&&<div className="error-box" role="alert">{error}</div>}<div className="panel results"><div className="panel-heading"><h3>Query results</h3><span className="mono">{elapsed===null?'':`${results.length} rows · ${elapsed} ms`}</span><button className="text-button" disabled={!results.length} onClick={()=>csv(results,'query-results.csv')}><Download size={14}/> CSV</button></div>{results.length?<Table><TableHeader><TableRow>{keys.map(k=><TableHead key={k}>{k}</TableHead>)}</TableRow></TableHeader><TableBody>{results.map((r,i)=><TableRow key={i}>{keys.map(k=><TableCell key={k}>{r[k]===null?'NULL':typeof r[k]==='object'?JSON.stringify(r[k]):String(r[k])}</TableCell>)}</TableRow>)}</TableBody></Table>:<div className="empty-state">{elapsed===null?'Run a query to explore the dataset.':'The query returned no rows.'}</div>}</div><p className="footnote">Results are capped at 1,000 rows. A 20-second limit resets expensive queries (60 seconds on the first run). Only SELECT and WITH queries are accepted; external access is disabled after loading.</p></div></div>
}
