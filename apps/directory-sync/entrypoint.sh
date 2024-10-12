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

while inotifywait -r -e modify,create,delete,move "${source_dir}"; do
    rsync -avz "${source_dir}" "${destination_dir}"
done