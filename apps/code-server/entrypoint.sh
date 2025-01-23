#!/bin/bash
set -euo nounset

if [[ "${USER_NAME:-user}" != "user" ]]; then
    usermod -d "/home/${USER_NAME}" -l ${USER_NAME} user || true
    cd /home/user
    rsync -avhz . "/home/${USER_NAME}"
fi


readonly ENTRYPOINTD="/etc/codeserver.d/"
if [[ -d "${ENTRYPOINTD}" ]]; then
    echo "export USER_NAME='${USER_NAME:-user}'" >> /tmp/.tmp_env

    for f in `find "${ENTRYPOINTD}" -type f -executable -print`; do
        echo "Running '$f'"
        su - "${USER_NAME:-user}" -c "/bin/bash -ce . /tmp/.tmp_env; $f"
    done
fi

cd "/home/${USER_NAME}"
exec su - "${USER_NAME:-user}" -- "/usr/bin/code-server" --auth none --bind-addr "0.0.0.0:${CODER_PORT:-8080}" &
pid="$!"
trap 'kill -SIGTERM $pid; wait $pid' SIGTERM SIGINT
wait $pid
