class DataPlane:
    """
    Internal implementation of handlers, used by both the gRPC and REST
    servers.
    """

    def live(self) -> bool:
        return True

    def ready(self) -> bool:
        return True

    def metadata(self):
        pass

    def infer(self, model_name: str):
        pass
