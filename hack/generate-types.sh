ROOT_FOLDER="$(dirname "${BASH_SOURCE}")/.."

_generate_pb() {
  python -m grpc_tools.protoc \
    -I"${ROOT_FOLDER}/proto" \
    --python_out="${ROOT_FOLDER}/oink/grpc" \
    --grpc_python_out="${ROOT_FOLDER}/oink/grpc" \
    "${ROOT_FOLDER}/proto/dataplane.proto"
}

_generate_pydantic() {
  datamodel-codegen \
    --input "${ROOT_FOLDER}/openapi/dataplane.yaml" \
    --output "${ROOT_FOLDER}/oink/types.py"
}

_generate_pb
_generate_pydantic
