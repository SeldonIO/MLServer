import requests

inference_request1 = {
    "inputs": [
        {"name": "args", "shape": [1], "datatype": "BYTES", "data": ["this is a test"]}
    ],
    "parameters": {"extra": {"max_new_tokens": 20}},
}

inference_request2 = {
    "inputs": [
        {"name": "args", "shape": [1], "datatype": "BYTES", "data": ["this is a test"]}
    ],
    "parameters": {"extra": {"max_new_tokens": 90}},
}
out1 = requests.post(
    "http://localhost:8080/v2/models/tinyllama/infer", json=inference_request1
).json()

out2 = requests.post(
    "http://localhost:8080/v2/models/tinyllama/infer", json=inference_request2
).json()
