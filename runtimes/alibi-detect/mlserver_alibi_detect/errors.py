from mlserver.errors import MLServerError


class InvalidAlibiDetectorConfiguration(MLServerError):
    def __init__(self, model_name: str):
        msg = f"Invalid Alibi Detector configuration for model {model_name}"
        super().__init__(msg)
