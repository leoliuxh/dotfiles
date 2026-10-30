#!/usr/bin/env python3
"""Install copies of these configs, backing up replaced files."""
import argparse
import datetime
import os
import shutil
import subprocess
from pathlib import Path

default_shell = 'bash' if os.environ.get('SHELL', '').endswith('bash') else 'zsh'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--desktop', action='store_true', help='Also install Fastfetch (and, on Linux, the GNOME Terminal look); Ghostty settings on macOS')
parser.add_argument('--shell', choices=['zsh', 'bash'], default=default_shell, help=f'Shell to wire up (default: {default_shell}, from $SHELL)')
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

def load_dconf(path, source):
    """Load a dconf dump, after saving the current state for rollback."""
    before = subprocess.run(['dconf', 'dump', path], capture_output=True, text=True, check=True).stdout
    backup.mkdir(parents=True, exist_ok=True)
    saved = backup / ('dconf' + path.rstrip('/').replace('/', '_') + '.dconf')
    saved.write_text(before)
    print(f'Backup: {saved}')
    subprocess.run(['dconf', 'load', path], input=source.read_text(), text=True, check=True)
    print(f'Loaded: {path} from {source}')

install(repo / 'config/starship.toml', config / 'starship.toml')
install(repo / 'shell/aliases.sh', config / 'dotfiles/aliases.sh')
terminal_script = f'terminal.{args.shell}'
install(repo / 'shell' / terminal_script, config / 'dotfiles' / terminal_script)
if args.desktop:
    install(repo / 'config/fastfetch/config.jsonc', config / 'fastfetch/config.jsonc')
    install(repo / 'bin/pokemon-welcome', home / '.local/bin/pokemon-welcome')
    install(repo / 'bin/welcome-toggle', home / '.local/bin/welcome-toggle')
    system = os.uname().sysname
    if system == 'Darwin':
        ghostty = home / 'Library/Application Support/com.mitchellh.ghostty/config.ghostty'
        install(repo / 'config/ghostty/config.ghostty', ghostty)
    elif system == 'Linux' and shutil.which('dconf'):
        load_dconf('/org/gnome/terminal/legacy/profiles:/', repo / 'config/linux/gnome-terminal.dconf')
        load_dconf('/org/gnome/shell/extensions/blur-my-shell/', repo / 'config/linux/blur-my-shell.dconf')
        print('GNOME-only: enable the "Blur my Shell" extension yourself (not installed by this script).')

rc = home / f'.{args.shell}rc'
line = f'source "${{XDG_CONFIG_HOME:-$HOME/.config}}/dotfiles/{terminal_script}"'
text = rc.read_text() if rc.exists() else ''
if line not in text:
    if rc.exists():
        backup.mkdir(parents=True, exist_ok=True)
        shutil.copy2(rc, backup / rc.name)
    with rc.open('a') as f:
        f.write('\n# Portable terminal customization\n' + line + '\n')
    print(f'Added source line to {rc}')
print('Open a new terminal. Re-run this installer after updating the repository.')
