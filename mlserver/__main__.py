"""
Starts an inference server.
"""
import uvicorn
import multiprocessing

from .rest import create_app
from .grpc import create_server
from .settings import Settings
from .handlers import DataPlane
from .registry import ModelRegistry

from .model import Model
from .types import InferenceRequest, InferenceResponse, ResponseOutput


class DummyModel(Model):
    def predict(self, payload: InferenceRequest) -> InferenceResponse:
        total = 0
        for inp in payload.inputs:
            print(inp.data)
            total += sum(inp.data)

        output = ResponseOutput(name="total", shape=[1], datatype="INT32", data=[total])
        return InferenceResponse(model_name="dummy", id="1", outputs=[output])


def start_rest(settings: Settings, data_plane: DataPlane):
    app = create_app(settings, data_plane)
    uvicorn.run(app, port=settings.http_port)


def start_grpc(settings: Settings, data_plane: DataPlane):
    server = create_server(settings, data_plane)
    server.start()
    server.wait_for_termination()


def _start_server(target: str, settings: Settings, data_plane: DataPlane):
    p = multiprocessing.Process(target=target, args=(settings, data_plane))
    p.start()
    return p


def main():
    settings = Settings()
    model_registry = ModelRegistry()
    data_plane = DataPlane(model_registry)

    model_registry.load("dummy", DummyModel())

    rest_process = _start_server(start_rest, settings, data_plane)
    grpc_process = _start_server(start_grpc, settings, data_plane)

    rest_process.join()
    grpc_process.join()


if __name__ == "__main__":
    main()
