ROOT_FOLDER="$(dirname "${BASH_SOURCE}")/.."

_generate_pb() {
  python -m grpc_tools.protoc \
    -I"${ROOT_FOLDER}/proto" \
    --python_out="${ROOT_FOLDER}/mlserver/grpc" \
    --grpc_python_out="${ROOT_FOLDER}/mlserver/grpc" \
    --mypy_out="${ROOT_FOLDER}/mlserver/grpc" \
    "${ROOT_FOLDER}/proto/dataplane.proto"

  # Change to relative import
  # https://github.com/protocolbuffers/protobuf/issues/1491
  sed -i "s/import dataplane/from . import dataplane/" \
    "${ROOT_FOLDER}/mlserver/grpc/dataplane_pb2_grpc.py"
}

_generate_pydantic() {
  datamodel-codegen \
    --input "${ROOT_FOLDER}/openapi/dataplane.yaml" \
    --output "${ROOT_FOLDER}/mlserver/types.py" \
    --custom-template-dir "${ROOT_FOLDER}/hack/templates"
}

_generate_pb
_generate_pydantic
