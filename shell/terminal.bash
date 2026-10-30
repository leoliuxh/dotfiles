# Source this file from ~/.bashrc. Keep private settings in ~/.bashrc.local.
case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *) export PATH="$HOME/.local/bin:$PATH" ;;
esac

if command -v eza >/dev/null 2>&1; then
  alias ls='eza --icons=auto --group-directories-first'
  alias ll='eza --long --all --icons=auto --git --group-directories-first'
  alias lt='eza --tree --level=2 --icons=auto --group-directories-first'
fi

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=aliases.sh
source "$HERE/aliases.sh"
alias reload='source ~/.bashrc'

# Optional decoration; skip SSH sessions and noninteractive output.
# Default comes from `welcome-toggle` (saved in $dotfiles_welcome_state); DOTFILES_WELCOME overrides it for one session.
dotfiles_welcome_state="${XDG_STATE_HOME:-$HOME/.local/state}/dotfiles/welcome"
dotfiles_welcome_default=1
[ -r "$dotfiles_welcome_state" ] && dotfiles_welcome_default=$(cat "$dotfiles_welcome_state")
if [ -t 1 ] && [ "${DOTFILES_WELCOME:-$dotfiles_welcome_default}" != 0 ] && [ -z "${SSH_CONNECTION}${SSH_CLIENT}${SSH_TTY}" ]; then
  if command -v fastfetch >/dev/null 2>&1; then
    if command -v python3 >/dev/null 2>&1 && [ -x "$HOME/.local/bin/pokemon-welcome" ]; then
      "$HOME/.local/bin/pokemon-welcome"
    else
      fastfetch
    fi
  fi
fi
unset dotfiles_welcome_state dotfiles_welcome_default

if command -v starship >/dev/null 2>&1; then
  eval "$(starship init bash)"
fi
