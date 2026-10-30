# Terminal dotfiles

Tokyo Night Starship prompt, icon-based file listings, translucent Ghostty, and an optional Pokemon welcome panel. Works with zsh on macOS and Linux; available tools and fonts determine which features appear.

## Install

Clone this repository on the target machine, then run commands from its directory.

Install dependencies using your system package manager. On macOS:

```sh
brew install starship eza fastfetch python
```

Select **JetBrainsMono Nerd Font Mono** in the terminal's font settings. The font belongs on the computer displaying the terminal; SSH servers do not need it.

For the prompt and file-listing aliases only (recommended on servers):

```sh
python3 scripts/install.py
```

For Ghostty, Fastfetch, and the welcome panel too:

```sh
python3 scripts/install.py --desktop
python3 scripts/setup-pokemon.py  # optional; downloads sprites and metadata
```

Open a new terminal. Installers copy files rather than symlinking them. Re-run the installer after pulling updates. Existing replaced files are backed up under `~/.local/state/dotfiles/backups/`.

**Existing customizations:** the installer appends one source line to `.zshrc`; it does not remove previous prompt initializers, aliases, or welcome commands. Remove old duplicate terminal-customization blocks before enabling this setup on an already customized account. In particular, the original Mac used to prepare this repo already has these blocks; there is no need to install it there immediately.

## What appears

- Prompt: path, Git branch/status, and matching Node/Bun/Rust/Go/PHP projects; no clock.
- SSH: `user@host` before the path. Starship and this config must be installed on the remote host.
- `ls`: icons; `ll`: detailed files with Git status; `lt`: two-level tree.
- Desktop welcome: aligned system information and Pokemon details on the left, random compact sprite on the right.
- OS icon and system details are detected locally; Pokemon name, number and types match the random sprite.
- Without Pokemon assets the welcome falls back to Fastfetch's detected system logo.
- Welcome art is skipped in SSH sessions. Set `DOTFILES_WELCOME=0` before the source line to disable it locally.

Manual preview:

```sh
pokemon-welcome
```

The scripts honor `XDG_CONFIG_HOME` and `XDG_DATA_HOME`. Keep machine-specific Java settings, credentials, SSH configuration, and other private setup outside this repository. No dependencies are installed automatically by these scripts.

## Files

- `config/starship.toml`: prompt colors, modules, SSH detection, and OS symbols.
- `config/ghostty/config.ghostty`: 85% opacity and background blur.
- `config/fastfetch/config.jsonc`: fallback startup information.
- `shell/terminal.zsh`: guarded tool setup and aliases.
- `bin/pokemon-welcome`: offline startup panel once assets are downloaded.
- `scripts/setup-pokemon.py`: optional asset download and half-size conversion.

## Credits

Prompt adapted from Starship's [Tokyo Night preset](https://starship.rs/presets/tokyo-night), part of the [ISC-licensed Starship project](https://github.com/starship/starship).
Sprite files are downloaded from [pokemon-colorscripts-mac](https://github.com/nuke-dash/pokemon-colorscripts-mac), pinned to commit `6aa0cd93b255bee35c5716652b8b7dfecb5fcfa2`; its license is saved with the downloaded assets. Metadata comes from [PokeAPI](https://github.com/PokeAPI/pokeapi). Pokemon names and designs belong to their respective owners. Assets are not committed to this repository.
