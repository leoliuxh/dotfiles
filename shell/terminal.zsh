# Source this file from ~/.zshrc. Keep private settings in ~/.zshrc.local.
typeset -U path
path=("$HOME/.local/bin" $path)

if (( $+commands[eza] )); then
  alias ls='eza --icons=auto --group-directories-first'
  alias ll='eza --long --all --icons=auto --git --group-directories-first'
  alias lt='eza --tree --level=2 --icons=auto --group-directories-first'
fi

# Optional decoration; skip SSH sessions and noninteractive output.
if [[ -o interactive && -t 1 && ${DOTFILES_WELCOME:-1} != 0 && -z ${SSH_CONNECTION}${SSH_CLIENT}${SSH_TTY} ]]; then
  if (( $+commands[fastfetch] )); then
    if (( $+commands[python3] )) && [[ -x "$HOME/.local/bin/pokemon-welcome" ]]; then
      "$HOME/.local/bin/pokemon-welcome"
    else
      fastfetch
    fi
  fi
fi

if (( $+commands[starship] )); then
  eval "$(starship init zsh)"
fi
