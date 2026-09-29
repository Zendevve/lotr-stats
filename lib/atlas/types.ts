import data from './data.json';
export type Ruler = typeof data.rulers[number];
export type Realm = typeof data.realms[number];
export const atlas = data;
export function median(values:number[]){const a=[...values].sort((a,b)=>a-b);return a.length ? (a[Math.floor((a.length-1)/2)]+a[Math.floor(a.length/2)])/2 : 0}
export function date(age:string,year:number){return `${age} ${year.toLocaleString()}`}
export function csv(rows:Record<string,unknown>[],name:string){if(!rows.length)return;const keys=Object.keys(rows[0]);const cell=(v:unknown)=>`"${(typeof v==='object'&&v!==null?JSON.stringify(v):String(v??'')).replaceAll('"','""')}"`;const blob=new Blob([[keys.join(','),...rows.map(r=>keys.map(k=>cell(r[k])).join(','))].join('\n')],{type:'text/csv;charset=utf-8;'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
