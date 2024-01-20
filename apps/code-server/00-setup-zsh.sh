#!/bin/bash
set -euo nounset

if [[ ! -e "/home/${USER_NAME}/.oh-my-zsh" ]]; then
    cp -Rf /root/.oh-my-zsh "/home/${USER_NAME}/"
fi
chmod g-w,o-w /home/${USER_NAME}/.oh-my-zsh

if [[ ! -e "/home/${USER_NAME}/.local/share/helm" ]]; then
    mkdir -p "/home/${USER_NAME}/.local/share"
    cp -Rf /root/.local/share/helm "/home/${USER_NAME}/.local/share/"
fi

if [[ ! -e "/home/${USER_NAME}/.zshrc" ]]; then
    cp -Rf /root/.zshrc "/home/${USER_NAME}/"
fi