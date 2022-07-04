import { check } from "k6";
import { Counter } from "k6/metrics";
import grpc from "k6/net/grpc";

const grpcReqs = new Counter("grpc_reqs");

function getClient(grpcHost) {
  const client = new grpc.Client();

  client.load(["definitions"], "../../../proto/dataplane.proto");

  return client;
}

function checkResponse(res) {
  check(res, {
    "status is OK": (r) => r && r.status === grpc.StatusOK,
  });
  grpcReqs.add(1);
}

export class GrpcClient {
  constructor() {
    this.grpcHost = `${__ENV.MLSERVER_HOST}:${__ENV.MLSERVER_GRPC_PORT}`;
    this.client = getClient(this.grpcHost);
    this.connected = false;
  }

  connect() {
    if (!this.connected) {
      this.client.connect(this.grpcHost, { plaintext: true });
      this.connected = true;
    }
  }

  loadModel(name) {
    this.connect();

    const payload = {
      model_name: name,
    };

    const res = this.client.invoke(
      "inference.GRPCInferenceService/RepositoryModelLoad",
      payload
    );
    checkResponse(res);
  }

  unloadModel(name) {
    this.connect();

    const payload = {
      model_name: name,
    };

    const res = this.client.invoke(
      "inference.GRPCInferenceService/RepositoryModelUnload",
      payload
    );
    checkResponse(res);
  }

  infer(payload) {
    this.connect();

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
