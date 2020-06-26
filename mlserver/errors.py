class ModelNotFound(Exception):
    def __init__(self, name: str, version: str):
        message = f"Model {name} with version {version} not found"
        super().__init__(message)
