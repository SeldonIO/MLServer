from mlserver.errors import MLServerError


class InvalidMLlibFormat(MLServerError):
    def __init__(self, name: str, model_uri: str = None):
        msg = f"Invalid MLlib format for model {name}"
        if model_uri:
            msg += f" ({model_uri})"

        super().__init__(msg)
