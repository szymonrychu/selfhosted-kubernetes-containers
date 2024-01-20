#!/bin/bash
set -euo nounset

readonly GROUP_NAME="${GROUP_NAME:-user}"
readonly USER_NAME="${USER_NAME:-user}"
readonly USER_UID="${USER_UID:-1000}"
readonly USER_GID="${USER_GID:-1000}"
readonly USER_HOME="${USER_HOME:-"/home/${USER_NAME}"}"
readonly CODER_PORT="${CODER_PORT:-8080}"
readonly ENTRYPOINTD="/etc/codeserver.d/"

groupadd \
    --gid "${USER_GID}" \
        "${GROUP_NAME}" \
    || \
groupmod \
    --gid "${USER_GID}" \
        "${GROUP_NAME}" \

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

sed -i -e 's/%sudo	ALL=(ALL:ALL) ALL/%sudo	ALL=(ALL:ALL) NOPASSWD:ALL/g' /etc/sudoers

if [[ -d "${ENTRYPOINTD}" ]]; then
  find "${ENTRYPOINTD}" -type f -executable -print -exec su -p - "${USER_NAME}" -c '{}' \;
fi

su - "${USER_NAME}" -- "/usr/bin/code-server" --auth none --bind-addr "0.0.0.0:${CODER_PORT}"
