#!/usr/bin/env python3
"""Download optional Pokemon sprites and metadata, then make compact ANSI art."""
import csv
import io
import os
import re
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path

commit = '6aa0cd93b255bee35c5716652b8b7dfecb5fcfa2'
root = Path(os.environ.get('XDG_DATA_HOME', str(Path.home() / '.local/share'))) / 'pokemon-colorscripts'
root.mkdir(parents=True, exist_ok=True)

def download(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'terminal-dotfiles'})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()

print('Downloading Pokemon sprite collection...')
archive = download(f'https://codeload.github.com/nuke-dash/pokemon-colorscripts-mac/zip/{commit}')
with zipfile.ZipFile(io.BytesIO(archive)) as z:
    for member in z.namelist():
        parts = member.split('/')
        if len(parts) == 3 and parts[1] == 'colorscripts' and parts[2].endswith('.txt'):
            target = root / 'colorscripts' / Path(parts[2]).name
            target.parent.mkdir(exist_ok=True)
            target.write_bytes(z.read(member))
        elif len(parts) == 2 and parts[1] == 'LICENSE.txt':
            (root / 'LICENSE.txt').write_bytes(z.read(member))

print('Downloading PokeAPI metadata...')
data = root / 'data'
data.mkdir(exist_ok=True)
for remote, local in [('pokemon_species.csv', 'species.csv'), ('pokemon_types.csv', 'pokemon_types.csv'), ('types.csv', 'types.csv')]:
    content = download('https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/' + remote)
    if not list(csv.DictReader(io.StringIO(content.decode()))):
        raise SystemExit('Invalid metadata: ' + remote)
    (data / local).write_bytes(content)

out = root / 'colorscripts-small'
out.mkdir(exist_ok=True)
ansi = re.compile(r'\x1b\[([0-9;]*)m|([^\x1b])')
def color_code(color, background=False):
    return '\x1b[' + ('48' if background else '38') + ';2;' + ';'.join(map(str, color)) + 'm'
for p in (root / 'colorscripts').glob('*.txt'):
    rows = []
    color = (0, 0, 0)
    for line in p.read_text().splitlines():
        row = []
        for m in ansi.finditer(line):
            if m.group(1) is not None:
                v = m.group(1).split(';')
                if v[:2] == ['38', '2'] and len(v) == 5:
                    color = tuple(map(int, v[2:]))
            else:
                row.append(color if m.group(2) == '█' else None)
        if row:
            rows.append(row[::2])
    width = max(map(len, rows), default=0)
    rows = [r + [None] * (width - len(r)) for r in rows]
    if len(rows) % 2:
        rows.append([None] * width)
    lines = []
    for a, b in zip(rows[::2], rows[1::2]):
        line = ''
        for top, bottom in zip(a, b):
            line += '\x1b[0m'
            if top is None and bottom is None:
                line += ' '
            elif top is None:
                line += color_code(bottom) + '▄'
            elif bottom is None:
                line += color_code(top) + '▀'
            else:
                line += color_code(top) + color_code(bottom, True) + '▀'
        lines.append(line + '\x1b[0m')
    (out / p.name).write_text('\n'.join(lines) + '\n')
print(f'Ready: {len(list(out.glob("*.txt")))} compact sprites in {out}')
