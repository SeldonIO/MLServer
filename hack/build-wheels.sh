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

  # Python really expects the `setup.py` to be on the current folder, so we'll
  # `cd` into it and the go back again.
  cd $_srcPath
  python setup.py \
    sdist -d $_outputPath \
    bdist_wheel -d $_outputPath
  cd $_currentDir
}

_main() {
  local _outputPath="$PWD/$1"

  # Build MLServer
  echo "---> Building MLServer wheel"
  _buildWheel $ROOT_FOLDER $_outputPath

  for _runtime in "$ROOT_FOLDER/runtimes/"*; do
    echo "---> Building MLServer runtime: '$_runtime'"
    _buildWheel $_runtime $_outputPath
  done
}

_main $1
