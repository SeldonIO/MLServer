from ..grpc import service_pb2


class ServerHandlers:
    def live():
        return service_pb2.ServerLiveResponse(live=True)

    def ready():
        return service_pb2.ServerReadyResponse(ready=True)

    def metadata():
        pass
