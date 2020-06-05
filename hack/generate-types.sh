ROOT_FOLDER="$(dirname "${BASH_SOURCE}")/.."

_generate_pb() {
  python -m grpc_tools.protoc \
    -I"${ROOT_FOLDER}/proto" \
    --python_out="${ROOT_FOLDER}/oink/grpc" \
    --grpc_python_out="${ROOT_FOLDER}/oink/grpc" \
    "${ROOT_FOLDER}/proto/service.proto"
}

_generate_pydantic() {

}

_generate_pb
_generate_pydantic
