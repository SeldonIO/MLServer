#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

if [ "$#" -ne 1 ]; then
  echo 'Invalid number of arguments'
  echo "Usage: ./activate-env.sh <envTarball>"
  exit 1
fi

_unpackEnv() {
  local _envTarball=$1
  local _envFolder=$2

  if ! [[ -f $_envTarball ]]; then
    echo "Environment tarball not found at '$_envTarball'"
    return
  fi

  echo "--> Unpacking environment at $_envTarball..."
  mkdir -p $_envFolder
  tar -zxvf "$_envTarball" -C $_envFolder
}

_activateEnv() {
  local _envFolder=$1
  local _activate="$_envFolder/bin/activate"

  if ! [[ -f $_activate ]]; then
    echo "Environment not found at '$_envFolder'"
    return
  fi

  echo "--> Sourcing new environment at $_envFolder..."
  # Need to disable unbound errors for activate
  set +u
  source $_activate
  set -u

  echo "--> Calling conda-unpack..."
  conda-unpack

  echo "--> Disabling user-installed packages..."
  # https://github.com/conda/conda/issues/448#issuecomment-195848539
  export PYTHONNOUSERSITE=True
}

_main() {
  local _envTarball=$1
  local _envName=$(basename "${_envTarball%.tar.gz}")
  local _envFolder="./envs/$_envName"

  _unpackEnv $_envTarball $_envFolder
  _activateEnv $_envFolder
}

_main $1
