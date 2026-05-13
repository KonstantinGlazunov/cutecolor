#!/usr/bin/env python3
import glob
import os
import re
import sys
import urllib.parse
import subprocess

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, 'content', 'original')
OUT_DIR = os.path.join(ROOT, 'public', 'assets', 'tilda')

os.makedirs(OUT_DIR, exist_ok=True)

def normalize(u: str) -> set[str]:
    u = u.strip().rstrip("'\">)\]}")
    if not u.startswith('https://'):
        return set()
    if not any(h in u for h in ('static.tildacdn.','neo.tildacdn.com')):
        return set()
    u = u.split('?', 1)[0]
    res = {u}
    if '/-/resize/' in u:
        parts = u.split('/-/resize/', 1)
        if len(parts) == 2:
            after = parts[1]
            after = re.sub(r'^[0-9]+x[0-9]*/', '', after)
            res.add(parts[0] + '/' + after)
    if '/-/empty/' in u:
        parts = u.split('/-/empty/', 1)
        if len(parts) == 2:
            res.add(parts[0] + '/' + parts[1])
    return res

urls: set[str] = set()
for f in glob.glob(os.path.join(CONTENT_DIR, '*.html')):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        html = fp.read()
    for m in re.finditer(r'https?://[^"\s>\)]+', html):
        for u in normalize(m.group(0)):
            if any(u.lower().endswith(ext) for ext in ('.jpg','.jpeg','.png','.webp','.gif','.svg','.ico','.css','.js')):
                urls.add(u)

urls = {u for u in urls if 'tildafavicon.ico' not in u}

print(f'Found {len(urls)} asset URLs')

failures = 0
for u in sorted(urls):
    parsed = urllib.parse.urlparse(u)
    host = parsed.netloc
    path = parsed.path.lstrip('/')
    out_path = os.path.join(OUT_DIR, host, path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        continue

    cmd = [
        'curl','-LsS',
        '-A', UA,
        '-o', out_path,
        u,
    ]
    try:
        subprocess.check_call(cmd)
        if os.path.getsize(out_path) == 0:
            raise RuntimeError('empty file')
    except Exception as e:
        failures += 1
        print(f'FAIL {u}: {e}', file=sys.stderr)

if failures:
    print(f'Completed with {failures} failures', file=sys.stderr)
    sys.exit(1)
print('Done')
