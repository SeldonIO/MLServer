import pytest


from mlserver.types import InferenceRequest
from mlserver.batching.shape import Shape


@pytest.fixture
def shape(inference_request: InferenceRequest) -> Shape:
    shape = inference_request.inputs[0].shape
    return Shape(shape)


def test_to_list(shape: Shape):
    shape_list = shape.to_list()
    assert shape_list == shape._shape

    shape_list[0] = 23
    assert shape_list != shape._shape


def test_batch_axis(shape: Shape):
    assert shape.batch_axis == 0


def test_batch_size(shape: Shape):
    assert shape.batch_size == 1

    shape.batch_size = 12
    assert shape.batch_size == 12
    assert shape.to_list() == [12, 3]


@pytest.mark.parametrize(
    "shape, expected",
    [
        (Shape([5, 2, 3]), 6),
        (Shape([5, 4]), 4),
        (Shape([5, 2, 3, 4]), 24),
    ],
)
def test_elem_size(shape: Shape, expected: int):
    assert shape.elem_size == expected
