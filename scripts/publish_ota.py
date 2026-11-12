import argparse,hashlib,json,re,zipfile
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];P=R/'public'
a=argparse.ArgumentParser();a.add_argument('--web-dir',required=True);a.add_argument('--version',required=True);a.add_argument('--min-native-version',required=True);v=a.parse_args()
for x in (v.version,v.min_native_version):
 if not re.fullmatch(r'\d+\.\d+\.\d+',x):a.error('Versões devem ser N.N.N')
w=Path(v.web_dir).resolve()
if not (w/'index.html').is_file() or not (w/'ota-updater.bundle.js').is_file():a.error('www precisa de index.html e ota-updater.bundle.js')
files=[f for f in w.rglob('*') if f.is_file()]
if any(f.is_symlink() for f in w.rglob('*')):a.error('Links simbólicos não permitidos')
out=P/'versions'/v.version/'web.zip'
if out.exists():a.error('Versão já publicada')
out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(files):z.write(f,f.relative_to(w).as_posix())
m={'appId':'com.check.app','available':True,'version':v.version,'packageUrl':f'https://chiildish.github.io/check-updates/versions/{v.version}/web.zip','sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'minimumNativeVersion':v.min_native_version,'publishedAt':datetime.now(timezone.utc).isoformat()}
(P/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('Publicado localmente:',out,'\nSHA-256:',m['sha256'])
