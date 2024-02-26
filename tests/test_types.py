import pytest
import json
from mlserver.types import InferenceRequest
from pydantic import ValidationError

from mlserver import types


@pytest.mark.parametrize(
    "data",
    [
        [1, 2, 3],
        [1.0, 2.0, 3.0],
        [[1.0, 2.0, 3.0]],
        [34.5, 8.4],
        [True, False, True],
        ["one", "two", "three"],
    ],
)
def test_tensor_data(data):
    raw = json.dumps(data)
    tensor_data = types.TensorData.parse_raw(raw)

    assert tensor_data.__root__ == data
    for tensor_elem, elem in zip(tensor_data, data):
        assert isinstance(tensor_elem, type(elem))


async def test_request_invalid_datatype(
    inference_request_invalid_datatype, datatype_error_message
):
    with pytest.raises(ValidationError) as excinfo:
        InferenceRequest.parse_obj(inference_request_invalid_datatype)

    assert excinfo.value.errors()[0]["msg"] == datatype_error_message
