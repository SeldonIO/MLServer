#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

ROOT_FOLDER="$(dirname "${0}")/.."
IMAGE_NAME="seldonio/mlserver"

if [ "$#" -ne 1 ]; then
  echo 'Invalid number of arguments'
  echo "Usage: ./build-images.sh <version>"
  exit 1
fi

_buildImage() {
  local _runtimes=$1
  local _tag=$2

  DOCKER_BUILDKIT=1 docker build $ROOT_FOLDER \
    --build-arg RUNTIMES="$_runtimes" \
    -t "$IMAGE_NAME:$_tag"
}

_buildRuntimeImage() {
  local _runtimePath=$1
  local _version=$2
  local _runtimeName=$(basename $_runtimePath)

  echo "---> Building MLServer runtime image: $_runtimeName"
  _buildImage "mlserver-$_runtimeName" "$_version-$_runtimeName"
}

_main() {
  local _version=$1

  echo "---> Building core MLServer images"
  _buildImage "all" $_version
  _buildImage "" $_version-slim

  for _runtimePath in "$ROOT_FOLDER/runtimes/"*/; do
    [ -d "$_runtimePath" ] || continue
    _buildRuntimeImage $_runtimePath $_version
  done
}

_main $1
