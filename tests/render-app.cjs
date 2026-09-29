// Server-render every app surface without a browser; navigation hooks are isolated.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const Module=require('node:module');
const ts=require('typescript');
const React=require('react');
const {renderToStaticMarkup}=require('react-dom/server');
const root=process.cwd();let pathname='/';const errors=[];console.error=(...args)=>errors.push(args.join(' '));
const original=Module._resolveFilename;
Module._resolveFilename=function(name,parent,...rest){if(name.startsWith('@/'))name=path.join(root,name.slice(2));return original.call(this,name,parent,...rest)};
const originalLoad=Module._load;
Module._load=function(name,parent,...rest){
 if(name==='next/navigation')return {usePathname:()=>pathname,notFound:()=>{throw new Error('NOT_FOUND')}};
 if(name==='next/link')return {__esModule:true,default:({children,prefetch,replace,scroll,...props})=>React.createElement('a',props,children)};
 return originalLoad.call(this,name,parent,...rest);
};
for(const ext of ['.tsx','.ts'])require.extensions[ext]=(module,file)=>module._compile(ts.transpileModule(fs.readFileSync(file,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,jsx:ts.JsxEmit.ReactJSX,esModuleInterop:true}}).outputText,file);
const Atlas=require('../components/atlas.tsx').default;
const SQL=require('../components/atlas-sql.tsx').default;
const Page=require('../app/[[...path]]/page.tsx').default;
const data=require('../lib/atlas/data.json');
async function main(){
 const routes=['/','/timeline','/rulers','/analysis','/compare','/lineage','/sql','/methodology',...data.persons.map(p=>'/rulers/'+p.slug)];
 const links=new Set();
 for(const route of routes){pathname=route;await Page({params:Promise.resolve({path:route.slice(1).split('/').filter(Boolean)})});const html=renderToStaticMarkup(React.createElement(Atlas));assert.match(html,/<main/);assert.doesNotMatch(html,/Page not found|This ruler is not in/);for(const match of html.matchAll(/href="(\/[^"?#]*)(?:[?#][^"]*)?"/g))links.add(match[1]);}
 const sql=renderToStaticMarkup(React.createElement(SQL));assert.match(sql,/Run query/);assert.match(sql,/SQL query/);
 for(const invalid of [['no-page'],['rulers','missing'],['rulers',data.persons[0].slug,'extra']])await assert.rejects(Page({params:Promise.resolve({path:invalid})}),/NOT_FOUND/);
 for(const link of links){if(link.startsWith('/data/'))assert.ok(fs.existsSync(path.join(root,'public',link)),link);else assert.ok(routes.includes(link),'Broken internal link: '+link)}
 assert.deepEqual(errors,[],'React render warnings');
 console.log(`PASS: ${routes.length} server-rendered routes, SQL editor, invalid-route rejection, ${links.size} internal links and download targets.`);
}
main().catch(e=>{process.stderr.write(String(e)+'\n');process.exitCode=1});
