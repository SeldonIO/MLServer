from mlserver.errors import MLServerError


class RemoteInferenceError(MLServerError):
    def __init__(self, code: int, reason: str):
        super().__init__(f"Remote inference call failed with {code}, {reason}", status_code=code)


class InvalidTranformerInitialisation(MLServerError):
    def __init__(self, code: int, reason: str):
        super().__init__(
            f"Remote inference call failed with {code}, {reason}",
            status_code=code,
        )
