#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

if [ "$#" -ne 1 ]; then
  _printUsage
  exit 1
fi

_unpackEnv() {
  local _envTarball=$1
  local _envName=$(basename "${_envTarball%.tar.gz}")

  mkdir -p ./envs/$_envName
  tar -zxvf "$_envTarball" -C "./envs/$_envName"
  source "./envs/$_envName/bin/activate"
  conda-unpack
}

_printUsage() {
  echo "Usage: ./run-in-env.sh <envTarball>"
}

_main() {
  local _envTarball=$1

  if [[ ! -f $_envTarball ]]; then
    echo "$_envTarball environment tarball not found"
    _printUsage
    exit 0
  fi

  _unpackEnv $_envTarball
}

_main $1
