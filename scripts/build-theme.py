#!/usr/bin/env python3
"""Write the theme config files from config/palette.json.

Each color is defined once in config/palette.json. The files
config/*.in hold the real configuration with {{name}} markers in place
of the colors. This script fills the markers in and writes the result
next to the template, without the .in suffix.

Markers:
    {{green}}            #a7c080              the value as written
    {{green:upper}}      #A7C080              uppercase hex, for dconf
    {{green:rgb}}        38;2;167;192;128     ANSI escape, for fastfetch logos
    {{opacity:percent}}  5                    (1 - value) as a percent, for dconf

Run it after every change to the palette, then commit both the palette
and the generated files.
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PALETTE = REPO / 'config/palette.json'
MARKER = re.compile(r'\{\{(\w+)(?::(\w+))?\}\}')


def load_palette():
    """Return the color names, without the _comment entry."""
    data = json.loads(PALETTE.read_text(encoding='utf-8'))
    return {k: v for k, v in data.items() if not k.startswith('_')}


def channels(hex_color):
    """'#a7c080' -> (167, 192, 128)."""
    return tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))


def render(text, palette, source):
    """Replace every marker in text. Raises on an unknown name or form."""
    def one(match):
        name, form = match.group(1), match.group(2)
        if name not in palette:
            raise SystemExit(f'{source}: nothing named {name!r} in {PALETTE.name}')
        value = palette[name]

        if form is None:
            return str(value)
        if form == 'percent':
            return str(round((1 - value) * 100))
        if form not in ('upper', 'rgb'):
            raise SystemExit(f'{source}: unknown marker form {form!r}')

        if not isinstance(value, str):
            raise SystemExit(f'{source}: {name!r} is not a color, so :{form} does not apply')
        if form == 'upper':
            return value.upper()
        return '38;2;%d;%d;%d' % channels(value)

    return MARKER.sub(one, text)


def main():
    palette = load_palette()
    templates = sorted(REPO.glob('config/**/*.in'))
    if not templates:
        raise SystemExit('no templates found under config/')

    check = '--check' in sys.argv
    stale = []
    for template in templates:
        out = template.with_suffix('')
        new = render(template.read_text(encoding='utf-8'), palette, template.name)
        old = out.read_text(encoding='utf-8') if out.exists() else None
        if new == old:
            continue
        if check:
            stale.append(out.relative_to(REPO))
        else:
            out.write_text(new, encoding='utf-8')
            print(f'Wrote: {out.relative_to(REPO)}')

    if check and stale:
        names = ', '.join(str(p) for p in stale)
        raise SystemExit(f'Out of date with the palette: {names}')
    if check:
        print('All theme files match the palette.')


if __name__ == '__main__':
    main()
