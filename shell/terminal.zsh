# Source this file from ~/.zshrc. Keep private settings in ~/.zshrc.local.
typeset -U path
path=("$HOME/.local/bin" $path)

if (( $+commands[eza] )); then
  alias ls='eza --icons=auto --group-directories-first'
  alias ll='eza --long --all --icons=auto --git --group-directories-first'
  alias lt='eza --tree --level=2 --icons=auto --group-directories-first'
fi

source "${0:A:h}/aliases.sh"
alias reload='source ~/.zshrc'

# Optional decoration; skip SSH sessions and noninteractive output.
# Default comes from `welcome-toggle` (saved in $dotfiles_welcome_state); DOTFILES_WELCOME overrides it for one session.
dotfiles_welcome_state="${XDG_STATE_HOME:-$HOME/.local/state}/dotfiles/welcome"
dotfiles_welcome_default=1
[[ -r $dotfiles_welcome_state ]] && dotfiles_welcome_default=$(<$dotfiles_welcome_state)
dotfiles_pokemon_state="${XDG_STATE_HOME:-$HOME/.local/state}/dotfiles/pokemon"
dotfiles_pokemon_default=1
[[ -r $dotfiles_pokemon_state ]] && dotfiles_pokemon_default=$(<$dotfiles_pokemon_state)
if [[ -o interactive && -t 1 && ${DOTFILES_WELCOME:-$dotfiles_welcome_default} != 0 && -z ${SSH_CONNECTION}${SSH_CLIENT}${SSH_TTY} ]]; then
  if (( $+commands[fastfetch] )); then
    if [[ ${DOTFILES_POKEMON:-$dotfiles_pokemon_default} != 0 ]] && (( $+commands[python3] )) && [[ -x "$HOME/.local/bin/pokemon-welcome" ]]; then
      "$HOME/.local/bin/pokemon-welcome"
    else
      fastfetch
    fi
  fi
fi
unset dotfiles_welcome_state dotfiles_welcome_default dotfiles_pokemon_state dotfiles_pokemon_default

if (( $+commands[starship] )); then
  eval "$(starship init zsh)"
fi
