"""Create a reproducible source download, excluding local identity and runtime state."""
from pathlib import Path
import json,zipfile
root=Path(__file__).resolve().parents[1]
excluded={'node_modules','.git','.sites-runtime','dist','.wrangler','.next','__pycache__','.openai'}
with zipfile.ZipFile(root/'public/data/source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(root.rglob('*')):
  rel=p.relative_to(root)
  if not p.is_file() or any(x in excluded for x in rel.parts) or p.name in ['source.zip','.env','.env.local'] or p.suffix in ('.pyc','.tsbuildinfo'):continue
  z.write(p,str(Path('dunedain-data-atlas')/rel))
 z.writestr('dunedain-data-atlas/.openai/hosting.json',json.dumps({'d1':None,'r2':None}))
print('Created public/data/source.zip')
