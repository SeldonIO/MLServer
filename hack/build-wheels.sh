#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

ROOT_FOLDER="$(git rev-parse --show-toplevel)"

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
  # move into the source folder and then go back again.
  pushd $_srcPath
  python setup.py \
    sdist -d $_outputPath \
    bdist_wheel -d $_outputPath
  popd
}

_main() {
  # Convert any path to absolute path (cross-platform way) taking into account
  # that the `./dist` folder may not exist yet
  local _outputPath=$(
    cd $(dirname $1)
    echo "$PWD/dist"
  )

  # Build MLServer
  echo "---> Building MLServer wheel"
  _buildWheel $ROOT_FOLDER $_outputPath

  for _runtime in "$ROOT_FOLDER/runtimes/"*; do
    echo "---> Building MLServer runtime: '$_runtime'"
    _buildWheel $_runtime $_outputPath
  done
}

_main $1
