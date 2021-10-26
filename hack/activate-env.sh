#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

if [ "$#" -ne 1 ]; then
  echo 'Invalid number of arguments'
  echo "Usage: ./activate-env.sh <srcFolder>"
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

  source $_envFile
}

_main() {
  local _srcFolder=$1
  local _envTarball="$_srcFolder/environment.tar.gz"
  local _envFolder="$_srcFolder/envs/environment"
  local _dotenv="$_srcFolder/.env"

  _unpackEnv $_envTarball $_envFolder
  _activateEnv $_envFolder
  _sourceDotenv $_dotenv
}

_main $1
