from mlserver.errors import MLServerError


class InvalidAlibiDetector(MLServerError):
    def __init__(self, detector_type: str, model_name: str, e: Exception):
        msg = f"Invalid Alibi Detector type {detector_type} for model {model_name} {e}"
        super().__init__(msg)
