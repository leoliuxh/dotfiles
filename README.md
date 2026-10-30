# Terminal dotfiles

Everforest Starship prompt, icon-based file listings, translucent terminal background, and an optional Pokemon welcome panel. Works with zsh or bash, on macOS and Linux; available tools and fonts determine which features appear.

## Install

Clone this repository on the target machine, then run commands from its directory.

Install dependencies using your system package manager. On macOS:

```sh
brew install starship eza fastfetch python
```

On Linux, install each tool the same way with your package manager, or as a plain user-space binary from the project's own release page (no root needed; put it on `PATH`, for example in `~/.local/bin`): [starship](https://starship.rs), [eza](https://github.com/eza-community/eza), [bat](https://github.com/sharkdp/bat), [fastfetch](https://github.com/fastfetch-cli/fastfetch).

Select **JetBrainsMono Nerd Font Mono** in the terminal's font settings. The font belongs on the computer displaying the terminal; SSH servers do not need it. `config/linux/gnome-terminal.dconf` sets this font for GNOME Terminal directly, so install the font (same release page below) before running `--desktop` on Linux, or the profile will fall back to whatever the terminal already has.

On Linux, a Nerd-Font-patched font can double the width of every character in VTE-based terminals (GNOME Terminal and others). If spacing looks too wide, keep a normal font and add only the [Nerd Fonts "Symbols Only" package](https://github.com/ryanoasis/nerd-fonts/releases) plus its fontconfig rule (`10-nerd-font-symbols.conf`, included in that package) instead of a fully patched font, and list that symbols font as a second, comma-separated family in the terminal's font setting (for example `DejaVu Sans Mono,Symbols Nerd Font Mono 12`) so letters keep normal spacing. A global fontconfig alias alone is not always enough: GNOME Terminal did not honor it for one Powerline glyph in testing, and needed the fallback font named directly in its own font string. Even then, Powerline separators (the glyphs that must fill a cell exactly, like the half-circle divider) can end up a size that does not quite match the surrounding color blocks, since they come from a different font file with different metrics than the letters; a fully-patched font avoids this because the separator and the letters share one file and one set of metrics.

The installer picks zsh or bash from `$SHELL`; pass `--shell zsh` or `--shell bash` to choose directly.

For the prompt and file-listing aliases only (recommended on servers):

```sh
python3 scripts/install.py
```

For Fastfetch, the welcome panel, and (on Linux) the GNOME Terminal look too:

```sh
python3 scripts/install.py --desktop
python3 scripts/setup-pokemon.py  # optional; downloads sprites and metadata
```

On Linux, `--desktop` also loads the saved GNOME Terminal colors, transparency, and font settings, plus the "Blur my Shell" extension's blur settings, from `config/linux/`. This needs GNOME Terminal and the `dconf` command (both ship with GNOME by default). It also needs the "Blur my Shell" GNOME Shell extension; the installer does not install or enable that extension itself. On macOS, `--desktop` instead installs Ghostty's config.

Open a new terminal. Installers copy files rather than symlinking them. Re-run the installer after pulling updates. Existing replaced files are backed up under `~/.local/state/dotfiles/backups/` (GNOME Terminal and Blur my Shell settings are saved there too, as `dconf dump` output, before being overwritten).

**Existing customizations:** the installer appends one source line to `.zshrc` or `.bashrc`; it does not remove previous prompt initializers, aliases, or welcome commands. Remove old duplicate terminal-customization blocks before enabling this setup on an already customized account. In particular, the original Mac used to prepare this repo already has these blocks; there is no need to install it there immediately.

## What appears

- Prompt: path, Git branch/status, and matching Node/Bun/Rust/Go/PHP projects; no clock.
- SSH: `user@host` before the path. Starship and this config must be installed on the remote host.
- `ls`: icons; `ll`: detailed files with Git status; `lt`: two-level tree.
- Desktop welcome: aligned system information and Pokemon details on the left, random compact sprite on the right.
- OS icon and system details are detected locally; Pokemon name, number and types match the random sprite.
- Without Pokemon assets the welcome falls back to Fastfetch's detected system logo.
- Welcome art is skipped in SSH sessions, always, regardless of the toggle below.

Turn the welcome panel on or off for local sessions, saved across terminals:

```sh
welcome-toggle        # flips it
welcome-toggle on
welcome-toggle off
welcome-toggle status
```

`DOTFILES_WELCOME=0` (or `=1`) before the source line overrides the saved setting for one session only.

To keep the system-info panel but drop the Pokemon sprite, use `pokemon-toggle` instead (same `on`/`off`/`status`/no-argument-flips usage, `DOTFILES_POKEMON` for a one-session override). With the sprite off, startup falls back to plain fastfetch.

Manual preview, regardless of the toggle or SSH:

```sh
pokemon-welcome
```

The scripts honor `XDG_CONFIG_HOME` and `XDG_DATA_HOME`. Keep machine-specific Java settings, credentials, SSH configuration, and other private setup outside this repository. No dependencies are installed automatically by these scripts.

## Files

- `config/palette.json`: every color used by this repository, defined once.
- `config/*.in`: templates with `{{color}}` markers; `scripts/build-theme.py` turns them into the files below.
- `config/starship.toml`: prompt colors, modules, SSH detection, and OS symbols. Generated.
- `config/ghostty/config.ghostty`: matching colors, opacity, and background blur (macOS). Generated.
- `config/linux/gnome-terminal.dconf`: matching colors, 5% transparency, and font for GNOME Terminal (Linux). Generated.
- `config/linux/blur-my-shell.dconf`: matching blur strength and tint for the "Blur my Shell" extension (Linux).
- `config/fastfetch/config.jsonc`: fallback startup information. Generated.
- `shell/terminal.zsh`, `shell/terminal.bash`: guarded tool setup, per shell.
- `shell/aliases.sh`: shell-agnostic aliases (navigation, safety, git, GPU, misc), used by both of the above.
- `bin/pokemon-welcome`: offline startup panel once assets are downloaded.
- `bin/welcome-toggle`: on/off switch for the startup panel, saved in `$XDG_STATE_HOME/dotfiles/welcome`.
- `bin/pokemon-toggle`: on/off switch for just the Pokemon sprite (falls back to fastfetch), saved in `$XDG_STATE_HOME/dotfiles/pokemon`.
- `scripts/setup-pokemon.py`: optional asset download and half-size conversion.
- `scripts/build-theme.py`: writes the generated files above from the palette.

## Colors

Every color lives once, in `config/palette.json`, and so does the window opacity. The theme files for both platforms are generated from the `config/*.in` templates, so do not edit them directly; the generator overwrites them.

```sh
# edit config/palette.json, then:
python3 scripts/build-theme.py
python3 scripts/install.py --desktop   # apply the result
```

Commit the palette and the generated files together. `python3 scripts/build-theme.py --check` fails if they disagree.

A marker takes an optional form: `{{green}}` gives `#a7c080`, `{{green:upper}}` gives `#A7C080` for the dconf file, `{{green:rgb}}` gives the ANSI escape `38;2;167;192;128` that fastfetch needs for logo colors, and `{{opacity:percent}}` turns the opacity `0.95` into the `5` that GNOME Terminal wants as a transparency percentage.

The blur settings in `config/linux/blur-my-shell.dconf` are not generated. Its white tint and blur radius appear in that one file only, so they are already a single decision.

## Credits

Prompt structure adapted from Starship's [Tokyo Night preset](https://starship.rs/presets/tokyo-night), part of the [ISC-licensed Starship project](https://github.com/starship/starship). Colors are the [Everforest](https://github.com/sainnhe/everforest) Dark Hard palette (MIT license).
Sprite files are downloaded from [pokemon-colorscripts-mac](https://github.com/nuke-dash/pokemon-colorscripts-mac), pinned to commit `6aa0cd93b255bee35c5716652b8b7dfecb5fcfa2`; its license is saved with the downloaded assets. Metadata comes from [PokeAPI](https://github.com/PokeAPI/pokeapi). Pokemon names and designs belong to their respective owners. Assets are not committed to this repository.
