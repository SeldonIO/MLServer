ROOT_FOLDER="$(dirname "${0}")/.."

_generate_pb() {
  local _api_name=$1

  python -m grpc_tools.protoc \
    -I"${ROOT_FOLDER}/proto" \
    --python_out="${ROOT_FOLDER}/mlserver/grpc" \
    --grpc_python_out="${ROOT_FOLDER}/mlserver/grpc" \
    --mypy_out="${ROOT_FOLDER}/mlserver/grpc" \
    "${ROOT_FOLDER}/proto/$_api_name.proto"

  # Change to relative import
  # https://github.com/protocolbuffers/protobuf/issues/1491
  sed -i "s/import $_api_name/from . import $_api_name/" \
    "${ROOT_FOLDER}/mlserver/grpc/${_api_name}_pb2_grpc.py"
}

_generate_pydantic() {
  local _api_name=$1

  datamodel-codegen \
    --input "${ROOT_FOLDER}/openapi/$_api_name.yaml" \
    --output "${ROOT_FOLDER}/mlserver/types/$_api_name.py" \
    --custom-template-dir "${ROOT_FOLDER}/hack/templates" \
    --disable-timestamp \
    --target-python-version 3.6
}

_generate_pb dataplane
_generate_pydantic dataplane

_generate_pb model_repository
_generate_pydantic model_repository
