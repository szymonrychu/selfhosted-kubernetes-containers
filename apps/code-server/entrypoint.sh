#!/bin/bash
set -euo nounset

readonly GROUP_NAME="${GROUP_NAME:=user}"
readonly USER_NAME="${USER_NAME:=user}"
readonly USER_UID="${USER_UID:=1000}"
readonly USER_GID="${USER_GID:=1000}"
readonly USER_HOME="${USER_HOME:="/home/${USER_NAME}"}"
readonly CODER_PORT="${CODER_PORT:=8080}"
readonly ENTRYPOINTD="${ENTRYPOINTD:=/etc/codeserver.d/}"

groupadd \
    --gid "${USER_GID}" \
        "${GROUP_NAME}"

useradd \
    --create-home \
    --home-dir "${USER_HOME}" \
    --uid "${USER_UID}" \
    --shell /usr/bin/zsh \
    --gid "${USER_GID}" \
        "${USER_NAME}"

usermod \
    --append \
    --groups sudo \
        "${USER_NAME}"

if [[ ! -e "${USER_HOME}/.oh-my-zsh" ]]; then
    cp -Rf /root/.oh-my-zsh "${USER_HOME}/"
    chown -R "${USER_UID}:${USER_GID}" "${USER_HOME}/.oh-my-zsh"
fi

if [[ ! -e "${USER_HOME}/.zshrc" ]]; then
    cp -Rf /root/.zshrc "${USER_HOME}/"
    chown -R "${USER_UID}:${USER_GID}" "${USER_HOME}/.zshrc"
fi

if [[ -d "${ENTRYPOINTD}" ]]; then
  find "${ENTRYPOINTD}" -type f -executable -print -exec {} \;
fi

su - "${USER_NAME}" -- "/usr/bin/code-server" --auth none --bind-addr "0.0.0.0:${CODER_PORT}"