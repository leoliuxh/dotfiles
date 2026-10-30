#!/usr/bin/env python3
"""Install copies of these configs, backing up replaced files."""
import argparse
import datetime
import os
import shutil
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--desktop', action='store_true', help='Also install Ghostty and Fastfetch settings')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[1]
home = Path.home()
config = Path(os.environ.get('XDG_CONFIG_HOME', str(home / '.config')))
stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
backup = home / '.local/state/dotfiles/backups' / stamp

def install(source, target):
    data = source.read_bytes()
    if target.is_file() and target.read_bytes() == data:
        return
    if target.exists() or target.is_symlink():
        try:
            relative = target.relative_to(home)
        except ValueError:
            relative = Path('external') / str(target).lstrip('/')
        saved = backup / relative
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, saved)
        print(f'Backup: {saved}')
        target.unlink()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    print(f'Installed: {target}')

install(repo / 'config/starship.toml', config / 'starship.toml')
install(repo / 'shell/terminal.zsh', config / 'dotfiles/terminal.zsh')
if args.desktop:
    install(repo / 'config/fastfetch/config.jsonc', config / 'fastfetch/config.jsonc')
    install(repo / 'bin/pokemon-welcome', home / '.local/bin/pokemon-welcome')
    ghostty = config / 'ghostty/config.ghostty'
    if os.uname().sysname == 'Darwin':
        ghostty = home / 'Library/Application Support/com.mitchellh.ghostty/config.ghostty'
    install(repo / 'config/ghostty/config.ghostty', ghostty)

rc = home / '.zshrc'
line = 'source "${XDG_CONFIG_HOME:-$HOME/.config}/dotfiles/terminal.zsh"'
text = rc.read_text() if rc.exists() else ''
if line not in text:
    if rc.exists():
        backup.mkdir(parents=True, exist_ok=True)
        shutil.copy2(rc, backup / '.zshrc')
    with rc.open('a') as f:
        f.write('\n# Portable terminal customization\n' + line + '\n')
    print(f'Added source line to {rc}')
print('Open a new terminal. Re-run this installer after updating the repository.')
