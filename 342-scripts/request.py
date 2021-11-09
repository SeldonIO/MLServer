import requests

inference_request = {
    "parameters": {
        "content_type": "pd"
    },
    "inputs": [
        {
            "name": "a",
            "datatype": "INT32",
            "data": [10],
            "shape": [1]
        },
        {
            "name": "b",
            "datatype": "INT32",
            "data": [7],
            "shape": [1]
        },
        {
            "name": "c",
            "datatype": "INT32",
            "data": [6],
            "shape": [1]
        },
        {
            "name": "op",
            "datatype": "BYTES",
            "data": ["-"],
            "shape": [1],
            "parameters": {
                "content_type": "str"
            }
        }
    ]
}

endpoint = "http://localhost:8080/v2/models/example-sklearn-pd-pipeline/infer"
response = requests.post(endpoint, json=inference_request)

print(response)
print(response.json())
