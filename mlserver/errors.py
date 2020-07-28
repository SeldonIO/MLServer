class MLServerError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ModelNotFound(MLServerError):
    def __init__(self, name: str, version: str = None):
        msg = f"Model {name} not found"
        if version is not None:
            msg = f"Model {name} with version {version} not found"

        super().__init__(msg)


class InferenceError(MLServerError):
    def __init__(self, msg):
        super().__init__(msg)
