#!/bin/bash

_copy() {
  local _src=$1
  local _newModelName=$2
  local _modelName=$(basename $_src)
  local _dst="$(dirname $_src)/$_newModelName"

  cp -r $_src $_dst
  sed -i "s/$_modelName/$_newModelName/" "$_dst/model-settings.json"
}

_main() {
  local _copies=10

  for _i in {1..$_copies}; do
    _copy "$PWD/testserver/models/iris" "iris-$_i"
    _copy "$PWD/testserver/models/sum-model" "sum-model-$_i"
  done
}

_main
