#!/usr/bin/env bash

set -Eeuo pipefail

ROOT_FOLDER="$(dirname "${0}")/.."

TARGET="$1"

_generatePB() {
  local apiName=$1

  python -m grpc_tools.protoc \
    -I"${ROOT_FOLDER}/proto" \
    --python_out="${ROOT_FOLDER}/mlserver/grpc" \
    --grpc_python_out="${ROOT_FOLDER}/mlserver/grpc" \
    --mypy_out="${ROOT_FOLDER}/mlserver/grpc" \
    "${ROOT_FOLDER}/proto/$apiName.proto"

  # Change to relative import
  # https://github.com/protocolbuffers/protobuf/issues/1491
  sed -i "s/import $apiName/from . import $apiName/" \
    "${ROOT_FOLDER}/mlserver/grpc/${apiName}_pb2_grpc.py"
}

_generatePydantic() {
  local apiName=$1

  datamodel-codegen \
    --input "${ROOT_FOLDER}/openapi/$apiName.yaml" \
    --input-file-type openapi \
    --output "${ROOT_FOLDER}/mlserver/types/$apiName.py" \
    --custom-template-dir "${ROOT_FOLDER}/hack/templates" \
    --base-class ".base.BaseModel" \
    --disable-timestamp \
    --target-python-version 3.10
}

_generatePB "$TARGET"
_generatePydantic "$TARGET"
