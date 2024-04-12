"""
CLI to generate test benchmark data.
"""

import os
import json
import numpy as np

from typing import List
from google.protobuf import json_format
from google.protobuf.internal.encoder import _VarintBytes  # type: ignore
from mlserver import types
from mlserver.grpc import converters

MODEL_NAME = "sum-model"
MODEL_VERSION = "v1.2.3"
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "sum-model")


def generate_test_requests() -> List[types.InferenceRequest]:
    contents_lens = np.power(2, np.arange(10, 16)).astype(int)
    max_value = 9999

    requests = []
    for contents_len in contents_lens:
        inputs = max_value * np.random.rand(contents_len)
        requests.append(
            types.InferenceRequest(
                inputs=[
                    types.RequestInput(
                        name="input-0",
                        shape=[contents_len],
                        datatype="FP32",
                        data=types.TensorData.parse_obj(inputs.tolist()),
                    )
                ]
            )
        )

    return requests


def save_grpc_requests(requests: List[types.InferenceRequest]):
    infer_requests = [
        converters.ModelInferRequestConverter.from_types(
            req, model_name=MODEL_NAME, model_version=MODEL_VERSION
        )
        # Use only the first request to make results comparable to HTTP.
        for req in requests[:1]
    ]

    requests_file_path = os.path.join(DATA_PATH, "grpc-requests.pb")
    with open(requests_file_path, "wb") as requests_file:
        for req in infer_requests:
            # To stream multiple messages we need to prefix each one with its
            # size
            # https://ghz.sh/docs/options#-b---binary
            size = req.ByteSize()
            size_varint = _VarintBytes(size)
            requests_file.write(size_varint)

            serialised = req.SerializeToString()
            requests_file.write(serialised)

    requests_file_path = os.path.join(DATA_PATH, "grpc-requests.json")
    with open(requests_file_path, "w") as json_file:
        as_dict = json_format.MessageToDict(infer_requests[0])
        json.dump(as_dict, json_file)


def save_rest_requests(requests: List[types.InferenceRequest]):
    # infer_requests_dict = [req.dict() for req in requests]
    # wrk doesn't work with multiple payloads, so take the smallest one.
    # We should consider moving to locust or vegeta.
    infer_requests_dict = requests[0].dict()
    requests_file_path = os.path.join(DATA_PATH, "rest-requests.json")
    with open(requests_file_path, "w") as requests_file:
        json.dump(infer_requests_dict, requests_file)


def main():
    requests = generate_test_requests()

    save_grpc_requests(requests)
    save_rest_requests(requests)


if __name__ == "__main__":
    main()
