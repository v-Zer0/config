# Git Shortcuts
alias gs="git status"
alias gd="git diff"
alias gl="git log"

# Misc bash shortcuts
alias bpr='source ~/.zshrc; printf "\nBash Profile reloaded!\n"'
alias l='ls -al'
alias psx="ps aux | grep $1"
alias please='sudo $(fc -ln -1)'
alias send="rsync -av --relative $1 $2"

parse_git_branch() {
  git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}

setopt PROMPT_SUBST
PROMPT='
%(!.%F{red}.%F{cyan})%n%f@%F{yellow}%m%f%(!.%F{red}.)%f:%{$(pwd|([[ $EUID == 0 ]] && GREP_COLORS="mt=01;31" grep --color=always /|| GREP_COLORS="mt=01;34" grep --color=always /))%${#PWD}G%}%F{red}$(parse_git_branch)%f
>'
