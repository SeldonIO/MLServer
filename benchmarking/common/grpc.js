import { check } from "k6";
import grpc from "k6/net/grpc";

function getClient(grpcHost) {
  const client = new grpc.Client();

  client.load(["definitions"], "../../../proto/dataplane.proto");

  return client;
}

function checkResponse(res) {
  check(res, {
    "status is OK": (r) => r && r.status === grpc.StatusOK,
  });
}

export class GrpcClient {
  constructor() {
    this.grpcHost = `${__ENV.MLSERVER_HOST}:${__ENV.MLSERVER_GRPC_PORT}`;
    this.client = getClient(this.grpcHost);

    // Client can't connect on the init context
    this.connected = false;
  }

  infer(payload) {
    if (!this.connected) {
      this.client.connect(this.grpcHost, { plaintext: true });
      this.connected = true;
    }

    const res = this.client.invoke(
      "inference.GRPCInferenceService/ModelInfer",
      payload
    );
    checkResponse(res);
  }

  close() {
    this.client.close();
  }
}
