from mlserver.errors import MLServerError


class InvalidAlibiDetector(MLServerError):
    def __init__(self, model_name: str):
        msg = f"Invalid Alibi Detector type for model {model_name}"
        super().__init__(msg)
