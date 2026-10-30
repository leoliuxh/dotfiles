# Shell-agnostic aliases. Source from .bashrc or .zshrc.

# --- navigation ---
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias -- -='cd -'

# --- safety ---
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias mkdir='mkdir -p'

# --- human-readable sizes ---
alias df='df -h'
alias du='du -h'

# --- git ---
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gd='git diff'
alias gco='git checkout'
alias gb='git branch'
alias glog='git log --oneline --graph --decorate -20'

# --- GPU (skip quietly where there is no NVIDIA card) ---
if command -v nvidia-smi >/dev/null 2>&1; then
  alias gpu='nvidia-smi'
  alias gpuw='watch -n 1 nvidia-smi'
fi

# --- misc ---
alias h='history'
