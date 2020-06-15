import pytest

from fastapi import status
from mlserver.rest.utils import to_status_code


@pytest.mark.parametrize(
    "flag,expected", [(True, status.HTTP_200_OK), (False, status.HTTP_400_BAD_REQUEST)]
)
def test_to_status_code(flag: bool, expected: int):
    status_code = to_status_code(flag)
    assert status_code == expected
