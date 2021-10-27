#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

if [ "$#" -ne 2 ]; then
  echo 'Invalid number of arguments'
  echo "Usage: ./activate-env.sh <envTarball> <dstFolder>"
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

  if ! [[ -d $_envFolder ]]; then
    echo "Environment not found at '$_envFolder'"
    return
  fi

  echo "--> Sourcing new environment at $_envFolder..."
  # Need to disable unbound errors for activate
  set +u
  source "$_envFolder/bin/activate"
  set -u

  echo "--> Calling conda-unpack..."
  conda-unpack

  echo "--> Disabling user-installed packages..."
  # https://github.com/conda/conda/issues/448#issuecomment-195848539
  export PYTHONNOUSERSITE=True
}

_sourceDotenv() {
  local _dotenv=$1

  if ! [[ -f $_dotenv ]]; then
    echo "Dotenv file not found at '$_dotenv'"
    return
  fi

  source $_dotenv
}

_main() {
  local _envTarball=$1
  local _dstFolder=$2
  local _envFolder="$_dstFolder/environment"

  _unpackEnv $_envTarball $_envFolder
  _activateEnv $_envFolder

  local _dotenv="$_dstFolder/.env"
  _sourceDotenv $_dotenv
}

_main $1 $2
