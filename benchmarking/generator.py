"""
CLI to generate test benchmark data.
"""
import os
import json
import numpy as np

from typing import List
from google.protobuf import json_format
from mlserver import types
from mlserver.grpc import converters

MODEL_NAME = "sum-model"
MODEL_VERSION = "1.2.3"
DATA_PATH = os.path.join(os.path.dirname(__file__), "data")


def generate_test_requests() -> List[types.InferenceRequest]:
    contents_lens = np.power(2, np.arange(0, 15)).astype(int)
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
        for req in requests
    ]
    infer_requests_dict = [json_format.MessageToDict(req) for req in infer_requests]
    _save_data("grpc-requests.json", infer_requests_dict)


def save_rest_requests(requests: List[types.InferenceRequest]):
    infer_requests_dict = [req.dict() for req in requests]
    _save_data("rest-requests.json", infer_requests_dict)


def _save_data(filename: str, payload):
    file_path = os.path.join(DATA_PATH, filename)
    with open(file_path, "w") as request_file:
        json.dump(payload, request_file)


def main():
    requests = generate_test_requests()

    save_grpc_requests(requests)
    save_rest_requests(requests)


if __name__ == "__main__":
    main()
