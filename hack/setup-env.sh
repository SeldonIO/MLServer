#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

# This script may be called with `source`, so we can't rely on the `$0` trick.
PARENT_FOLDER=$(dirname "$BASH_SOURCE")

if [ "$#" -ne 1 ]; then
  echo 'Invalid number of arguments'
  echo "Usage: ./setup-env.sh <srcFolder>"
  exit 1
fi

_installRequirements() {
  local _requirementsTxt=$1

  pip install -r $_requirementsTxt
}

_main() {
  local _srcFolder=$1

  local _envTarball="$_srcFolder/environment.tar.gz"
  local _activateEnv="$PARENT_FOLDER/activate-env.sh"
  if [[ -f $_envTarball ]] && [[ -f $_activateEnv ]]; then
    echo "---> Found custom Conda environment at $_envTarball"
    source $_activateEnv $_envTarball
  else
    echo "Environment tarball not found at '$_envTarball'"
  fi

  local _requirementsTxt="$_srcFolder/requirements.txt"
  if [[ -f $_requirementsTxt ]]; then
    echo "---> Found custom requirements.txt at $_requirementsTxt"
    _installRequirements $_requirementsTxt
  else
    echo "Requirements not found at '$_requirementsTxt'"
  fi

  echo "---> Generating and sourcing default environment variables"
  local _sourceSettings="$PARENT_FOLDER/source_settings.py"
  local _envFile="$_srcFolder/.env"
  $_sourceSettings . $_envFile
  source $_envFile
}

_main $1
