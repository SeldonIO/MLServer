#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

_printUsage() {
  echo "Usage: ./run-in-env.sh <envTarball>"
}

if [ "$#" -ne 1 ]; then
  echo 'Invalid number of arguments'
  _printUsage
  exit 1
fi

_unpackEnv() {
  local _envTarball=$1
  local _envName=$(basename "${_envTarball%.tar.gz}")

  echo "--> Unpacking environment..."
  mkdir -p ./envs/$_envName
  tar -zxvf "$_envTarball" -C "./envs/$_envName"

  echo "--> Sourcing new environment..."
  # Need to disable unbound errors for activate
  set +u
  source "./envs/$_envName/bin/activate"
  set -u

  echo "--> Calling conda-unpack..."
  conda-unpack

  echo "--> Disabling user-installed packages..."
  # https://github.com/conda/conda/issues/448#issuecomment-195848539
  export PYTHONNOUSERSITE=True
}

_main() {
  local _envTarball=$1

  if [[ -f $_envTarball ]]; then
    _unpackEnv $_envTarball
  else
    echo "Environment tarball not found at '$_envTarball'"
  fi
}

_main $1
