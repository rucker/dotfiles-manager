# ~/.bashrc: executed by bash(1) for non-login shells.

export PS1="\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\] "
umask 022

 export LS_OPTIONS='--color=auto --group-directories-first'
 eval `dircolors`
 alias ls='ls $LS_OPTIONS'
 alias ll='ls $LS_OPTIONS -l'
 alias l='ls $LS_OPTIONS -lA'
 
 alias diff='colordiff'
 alias grep='grep --color=auto'
 alias gimme='sudo apt-get install'
 alias remove='sudo apt-get remove'
