import type {Ruler} from './types';
export function normalizeSearch(value:string){return value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim()}
export function filterRulers(rows:Ruler[],filters:{q:string,realm:string,status:string,min:string,max:string,sort:string,ascending:boolean}){
 const {q,realm,status,min,max,sort,ascending}=filters;
 const needle=normalizeSearch(q);
 return rows.filter(r=>(realm==='all'||r.office_id===realm)&&normalizeSearch(`${r.ruler_name} ${r.aliases}`).includes(needle)&&(status==='all'||status==='eligible'&&r.eligible||r.status===status)&&(!min||r.reign_years>=Number(min))&&(!max||r.reign_years<=Number(max))).sort((a,b)=>(sort==='name'?a.ruler_name.localeCompare(b.ruler_name):sort==='duration'?a.reign_years-b.reign_years:a.start_sort-b.start_sort)*(ascending?1:-1));
}
