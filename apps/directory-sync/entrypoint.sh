#!/bin/bash

set -euo nounset

readonly source_dir="${SOURCE_DIR:-}"
if [[ -z "${source_dir}" ]]; then
  echo "SOURCE_DIR emty!" 1>&2
  exit 1
fi

readonly destination_dir="${DESTINATION_DIR:-}"
if [[ -z "${destination_dir}" ]]; then
  echo "DESTINATION_DIR emty!" 1>&2
  exit 1
fi

readonly lockfile_path="${LOCKFILE_PATH:-/.lock}"

_term() {
  while [[ -f "${lockfile_path}" ]]; do
    sleep 1
  done
}

trap _term SIGTERM

cd "${source_dir}"
while inotifywait -r -e modify,create,delete,move "${source_dir}"; do
    touch "${lockfile_path}"
    rsync -avz . "${destination_dir}"
    rm "${lockfile_path}"
done