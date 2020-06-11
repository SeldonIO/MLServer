"""
Starts an inference server.
"""
import uvicorn
import multiprocessing

from mlserver.rest import create_app
from mlserver.grpc import create_server
from mlserver.settings import Settings
from mlserver.handlers import DataPlane
from mlserver.registry import ModelRegistry

from mlserver.model import Model
from mlserver import types


class SumModel(Model):
    name = "sum-model"

    def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        total = 0
        for inp in payload.inputs:
            total += sum(inp.data)

        output = types.ResponseOutput(
            name="total", shape=[1], datatype="FP32", data=[total]
        )
        return types.InferenceResponse(model_name=self.name, id="1", outputs=[output])


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
    settings = Settings(debug=False)
    model_registry = ModelRegistry()

    sum_model = SumModel()
    model_registry.load(sum_model.name, sum_model)

    data_plane = DataPlane(model_registry)

    rest_process = _start_server(start_rest, settings, data_plane)
    grpc_process = _start_server(start_grpc, settings, data_plane)

    rest_process.join()
    grpc_process.join()


if __name__ == "__main__":
    main()
