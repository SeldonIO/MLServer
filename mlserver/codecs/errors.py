from typing import Optional, Any, Dict, List, Type

from ..types import RequestInput
from ..errors import MLServerError


class CodecNotFound(MLServerError):
    def __init__(
        self,
        name: Optional[str] = None,
        payload_type: Optional[str] = None,
        is_input: bool = False,
        is_request: bool = False,
    ):
        msg = ""
        if name:
            msg = f"with name '{name}'"

            if payload_type:
                msg = f"{msg} and type {payload_type}"
        elif payload_type:
            msg = f"with type {payload_type}"

        field_category = ""
        if is_input:
            if is_request:
                field_category = "input request"
            else:
                field_category = "input field"
        else:
            if is_request:
                field_category = "output response"
            else:
                field_category = "output field"

        msg = f"Codec not found for {field_category} {msg}"
        super().__init__(msg)


class CodecError(MLServerError):
    def __init__(self, msg: str):
        msg = f"There was an error encoding / decoding the payload: {msg}"
        super().__init__(msg)


class OutputNotFound(MLServerError):
    def __init__(self, output_idx: int, output_type: Type, output_hints: List[Type]):
        expected_outputs = [f"'{output_hint}'" for output_hint in output_hints]
        msg = (
            f"Unexpected output value at position '{output_idx}' ({output_type}). "
            f"Expected outputs are {', '.join(expected_outputs)} outputs."
        )
        super().__init__(msg)


class InputsNotFound(MLServerError):
    def __init__(self, inputs: List[RequestInput], input_hints: Dict[str, Any]):
        input_names = [f"'{inp.name}'" for inp in inputs]
        available_inputs = [f"'{input_name}'" for input_name in input_hints.keys()]
        msg = (
            f"Input {', '.join(input_names)} was not found. "
            f"Available inputs are {', '.join(available_inputs)}."
        )
        super().__init__(msg)
