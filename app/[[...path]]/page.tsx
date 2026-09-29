import Atlas from '@/components/atlas';
import {notFound} from 'next/navigation';
import data from '@/lib/atlas/data.json';
const routes=new Set(['','timeline','rulers','analysis','compare','lineage','sql','methodology']);
export default async function Page({params}:{params:Promise<{path?:string[]}>}){
 const {path=[]}=await params;
 if(!(path.length<=1&&routes.has(path[0]??''))&&!(path.length===2&&path[0]==='rulers'&&data.persons.some(p=>p.slug===path[1])))notFound();
 return <Atlas/>;
}
