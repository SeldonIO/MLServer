from mlserver.errors import MLServerError


class InvalidAlibiDetector(MLServerError):
    def __init__(self, detector_type: str, model_name: str):
        msg = f"Invalid Alibi Detector type {detector_type} for model {model_name}"
        super().__init__(msg)
