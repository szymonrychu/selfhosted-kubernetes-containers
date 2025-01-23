#!/bin/bash
set -euo nounset

if [[ "${USER_NAME:-user}" != "user" ]]; then
    usermod -md /home/${USER_NAME} -l ${USER_NAME} user
fi

readonly ENTRYPOINTD="/etc/codeserver.d/"
if [[ -d "${ENTRYPOINTD}" ]]; then
    find "${ENTRYPOINTD}" -type f -executable -print -exec su - "${USER_NAME:-user}" -- bash -ce '{}' \;
fi

exec su - "${USER_NAME:-user}" -- "/usr/bin/code-server" --auth none --bind-addr "0.0.0.0:${CODER_PORT:-8080}" &
pid="$!"
trap 'kill -SIGTERM $pid; wait $pid' SIGTERM SIGINT
wait $pid
