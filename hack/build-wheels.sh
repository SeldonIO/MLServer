#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

ROOT_FOLDER="$(dirname "${0}")/.."

if [ "$#" -ne 1 ]; then
  echo 'Invalid number of arguments'
  echo "Usage: ./build-wheels.sh <outputPath>"
  exit 1
fi

_buildWheel() {
  local _srcPath=$1
  local _outputPath=$2
  local _currentDir=$PWD

  # Poetry doesn't let us send the output to a separate folder so we'll `cd`
  # into the folder and them move the wheels out
  # https://github.com/python-poetry/poetry/issues/3586
  pushd $_srcPath
  poetry build
  cp ./dist/* $_outputPath
  popd
}

_main() {
  # Convert any path into an absolute path
  local _outputPath=$1
  if ! [[ "$_outputPath" = /* ]]; then
    _outputPath="$PWD/$_outputPath"
  fi
  mkdir -p $_outputPath

  # Build MLServer
  echo "---> Building MLServer wheel"
  _buildWheel . $_outputPath

  for _runtime in "$ROOT_FOLDER/runtimes/"*; do
    echo "---> Building MLServer runtime: '$_runtime'"
    _buildWheel $_runtime $_outputPath
  done
}

_main $1
