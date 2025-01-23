#!/bin/bash
set -euo nounset

if [[ "${USER_NAME:-user}" != "user" ]]; then
    usermod -md /home/${USER_NAME} -l ${USER_NAME} user || true
fi


readonly ENTRYPOINTD="/etc/codeserver.d/"
if [[ -d "${ENTRYPOINTD}" ]]; then
    echo "export USER_NAME='${USER_NAME:-user}'" >> /tmp/.env

    for f in `find "${ENTRYPOINTD}" -type f -executable -print`; do
        echo "Running '$f'"
        su - "${USER_NAME:-user}" -- /bin/bash -ce ". /tmp/.env; $f"
    done
fi

exec su - "${USER_NAME:-user}" -- "/usr/bin/code-server" --auth none --bind-addr "0.0.0.0:${CODER_PORT:-8080}" &
pid="$!"
trap 'kill -SIGTERM $pid; wait $pid' SIGTERM SIGINT
wait $pid
