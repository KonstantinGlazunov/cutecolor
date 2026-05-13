#!/usr/bin/env python3
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_DIR = os.path.join(ROOT, 'content', 'original')
OUT_DIR = os.path.join(ROOT, 'public', 'archive', 'pages')

os.makedirs(OUT_DIR, exist_ok=True)

def rewrite(html: str) -> str:
    html = html.replace('https://static.tildacdn.info/', '/assets/tilda/static.tildacdn.info/')
    html = html.replace('https://static.tildacdn.com/', '/assets/tilda/static.tildacdn.com/')
    html = html.replace('https://neo.tildacdn.com/', '/assets/tilda/neo.tildacdn.com/')
    html = re.sub(r'https?://cutecolors\\.tilda\\.ws/(lisichka|kit)\\b', r'/archive/pages/\\1.html', html)
    html = re.sub(r'https?://cutecolors\\.tilda\\.ws/?\\b', r'/archive/pages/index.html', html)
    html = html.replace('http://cutecolors.tilda.ws', 'https://cutecolors.tilda.ws')
    return html

for name in ('index','lisichka','kit'):
    in_path = os.path.join(IN_DIR, f'{name}.html')
    out_path = os.path.join(OUT_DIR, f'{name}.html')
    with open(in_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(rewrite(html))
    print('wrote', os.path.relpath(out_path, ROOT))
