#!/bin/bash

SVN_DIR=$( pwd )

# add path to environment PATH
if ! grep -Exq "PATH=.*(~|$HOME)/GIT/univention-support-info/usi-check.*" "$HOME/.bash_local"; then
	echo "PATH=\$PATH:~/GIT/univention-support-info/usi-check" >>"$HOME/.bash_local"
fi
if ! grep -xq "\[ -f ~/.bash_local \] && . ~/.bash_local" "$HOME/.bashrc"; then
	echo -e "[ -f ~/.bash_local ] && . ~/.bash_local" >>"$HOME/.bashrc"
fi
