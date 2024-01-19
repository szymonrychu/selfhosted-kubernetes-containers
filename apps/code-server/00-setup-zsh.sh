#!/bin/bash
set -euo nounset

if [[ ! -e "${USER_HOME}/.oh-my-zsh" ]]; then
    cp -Rf /root/.oh-my-zsh "${USER_HOME}/"
fi
chmod g-w,o-w /home/${USER_NAME}/.oh-my-zsh

if [[ ! -e "${USER_HOME}/.local/share/helm" ]]; then
    mkdir -p "${USER_HOME}/.local/share"
    cp -Rf /root/.local/share/helm "${USER_HOME}/.local/share/"
fi

if [[ ! -e "${USER_HOME}/.zshrc" ]]; then
    cp -Rf /root/.zshrc "${USER_HOME}/"
fi