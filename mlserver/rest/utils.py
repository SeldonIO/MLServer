from fastapi import status


def to_status_code(flag: bool, error_code: int = status.HTTP_400_BAD_REQUEST) -> int:
    """
    Convert a boolean flag into a HTTP status code.
    """
    if flag:
        return status.HTTP_200_OK

    return error_code
