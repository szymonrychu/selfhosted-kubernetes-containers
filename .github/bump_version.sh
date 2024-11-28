#!/bin/bash

set -euo nounset

readonly CURRENT_PWD="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
readonly REPO_ROOT="$(dirname "$CURRENT_PWD")"

readonly CONTAINER_NAME="$1"
readonly VERSION_FILE_PATH="${REPO_ROOT}/apps/${CONTAINER_NAME}/VERSION"

readonly CURRENT_VERSION="$(cat "$VERSION_FILE_PATH" | awk '{print $1}')"
readonly MAJOR="$(echo "$CURRENT_VERSION" | cut -d. -f1)"
readonly MINOR="$(echo "$CURRENT_VERSION" | cut -d. -f2)"
readonly PATCH="$(echo "$CURRENT_VERSION" | cut -d. -f3)"

readonly NEW_PATCH="$(expr "$PATCH" + 1)"

echo "Bumping ${REPO_ROOT}/apps/${CONTAINER_NAME} to ${MAJOR}.${MINOR}.${NEW_PATCH}"

echo "${MAJOR}.${MINOR}.${NEW_PATCH}" > "$VERSION_FILE_PATH"
