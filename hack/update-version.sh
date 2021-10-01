#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

ROOT_FOLDER="$(dirname "${0}")/.."

if [ "$#" -ne 1 ]; then
  echo "Usage: ./update-version.sh <newVersion>"
  exit 1
fi

_updateVersion() {
  local _newVersion=$1
  local _versionPy=$2

  sed \
    -i "s/^__version__ = \"\(.*\)\"$/__version__ = \"$_newVersion\"/" \
    "$_versionPy"
}

_updateDocs() {
  local _newVersion=$1

  sed \
    -i "s/^release = \"\(.*\)\"$/release = \"$_newVersion\"/" \
    "$ROOT_FOLDER/docs/conf.py"
}

_main() {
  local _newVersion=$1

  # To call within `-exec`
  export -f _updateVersion

  find $ROOT_FOLDER \
    -type f -name version.py \
    \( \
    -path "$ROOT_FOLDER/mlserver/*" -or \
    -path "$ROOT_FOLDER/runtimes/**/*" \
    \) \
    -exec bash -c "_updateVersion $_newVersion {}" \;

  _updateDocs $_newVersion
}

_main $1
