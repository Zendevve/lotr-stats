/** Validate a single read-only statement while respecting SQL strings and comments. */
export function readOnlyQuery(input:string){
 let code='',quote='',depth=0,line=false;
 for(let i=0;i<input.length;i++){
  const c=input[i],n=input[i+1];
  if(line){if(c==='\n'){line=false;code+='\n'}else code+=' ';continue}
  if(depth){if(c==='/'&&n==='*'){depth++;i++;code+='  '}else if(c==='*'&&n==='/'){depth--;i++;code+='  '}else code+=' ';continue}
  if(quote){if(c===quote){if(n===quote){i++;code+='  ';continue}quote=''}code+=' ';continue}
  if(c==='-'&&n==='-'){line=true;i++;code+='  ';continue}
  if(c==='/'&&n==='*'){depth=1;i++;code+='  ';continue}
  if(c==="'"||c==='"'){quote=c;code+=' ';continue}
  code+=c;
 }
 if(quote||depth)throw new Error('Close the SQL string or comment before running.');
 const trimmed=code.trim();
 if(!/^(SELECT|WITH)\b/i.test(trimmed)||/\b(INSERT|UPDATE|DELETE|DROP|CREATE|COPY|ATTACH|DETACH|INSTALL|LOAD|PRAGMA|CALL|SET|RESET|EXPORT|IMPORT|ALTER|TRUNCATE|MERGE)\b/i.test(code))throw new Error('Use one SELECT or WITH query. This lab is read-only.');
 const semicolons=[...code.matchAll(/;/g)];
 if(semicolons.length>1||(semicolons.length===1&&code.slice(semicolons[0].index!+1).trim()))throw new Error('Run one SQL statement at a time.');
 const end=semicolons[0]?.index;
 return (end===undefined?input:input.slice(0,end)).trim();
}
export function resultValue(value:unknown):unknown{
 if(typeof value==='bigint')return value.toString();
 if(value instanceof Date)return value.toISOString();
 if(Array.isArray(value))return value.map(resultValue);
 if(value&&typeof value==='object')return Object.fromEntries(Object.entries(value).map(([k,v])=>[k,resultValue(v)]));
 return value;
}
