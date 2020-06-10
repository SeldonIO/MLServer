import os

from google.protobuf import json_format

from ..conftest import TESTDATA_PATH

TESTDATA_GRPC_PATH = os.path.join(TESTDATA_PATH, "grpc")


def read_testdata_pb(pb_filename: str, pb_klass):
    payload_path = os.path.join(TESTDATA_GRPC_PATH, pb_filename)
    model_infer_request = pb_klass()
    with open(payload_path) as payload:
        json_format.Parse(payload.read(), model_infer_request)

    return model_infer_request
