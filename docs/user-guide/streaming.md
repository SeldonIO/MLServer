# Streaming

Out of the box, MLServer includes support for streaming data to your models. The streaming support is available for both the REST and gRPC servers.


## REST Server

Streaming support for the REST server is limited only to server streaming. This means that the client sends a single request to the server, and the server responds with a stream of data.

The streaming endpoints are available for both the `infer` and `generate` methods through the following endpoints:

- `/v2/models/{model_name}/versions/{model_version}/infer_stream`
- `/v2/models/{model_name}/infer_stream`
- `/v2/models/{model_name}/versions/{model_version}/generate_stream`
- `/v2/models/{model_name}/generate_stream`

Note that for REST, the `generate` and `generate_stream` endpoints are aliases for the `infer` and `infer_stream` endpoints, respectively. Those names are used to better reflect the nature of the operation for Large Language Models (LLMs).


## gRPC Server

Streaming support for the gRPC server is available for both client and server streaming. This means that the client sends a stream of data to the server, and the server responds with a stream of data. 

The two streams operate independently, so the client and the sever cand read and write data however they want (e.g., the sever could either wait to receive all the client messages before sending a response, or it could send a response after each message). Note that the bi-directional streaming coveres all the possible combinations of client and server streaming: unary-stream, stream-unary, and stream-stream. The unary-unary case can be covered as well by the bi-directional streaming, but `mlserver` already has the `predict` method dedicated for this. This logic for how many messages are sent and received is defined by the client and server, and should be built in the runtime logic.

The stub method for streaming to be used by the client is `ModelStreamInfer`.


## Limitation

There are three main limitations of the streaming support in MLServer:

- the `parallel_workers` setting should be set to `0` to disable distributed workers (to be addressed in future releases)
- for REST, the `gzip_enabled` setting should be set to `false` to disable GZIP compression, as streaming is not compatible with GZIP compression (see issue [here]( https://github.com/encode/starlette/issues/20#issuecomment-704106436))
- `metrics_endpoint` are also disabled for streaming for gRPC (to be addressed in future releases)