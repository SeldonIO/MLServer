from typing import Optional

from ..errors import MLServerError


class InvalidParallelMethod(MLServerError):
    def __init__(self, method_name: str, reason: Optional[str] = None):
        msg = f"Method {method_name} can't be parallelised"
        if reason:
            msg += f": {reason}"

        super().__init__(msg)
