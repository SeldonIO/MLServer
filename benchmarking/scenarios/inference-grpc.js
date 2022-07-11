import { group } from "k6";
import { readTestData } from "../common/helpers.js";
import { RestClient } from "../common/rest.js";
import { GrpcClient } from "../common/grpc.js";

const TestData = {
  iris: readTestData("iris"),
};

const rest = new RestClient();
const grpc = new GrpcClient();

const ScenarioDuration = "60s";
const ScenarioVUs = 300;

export const options = {
  scenarios: {
    iris_grpc: {
      executor: "constant-vus",
      duration: ScenarioDuration,
      vus: ScenarioVUs,
      tags: { model_name: "iris", protocol: "grpc" },
      env: { MODEL_NAME: "iris", PROTOCOL: "grpc" },
    },
  },
  thresholds: {
    // Adjust so that it fits within the resources available in GH Actions
    grpc_reqs: ["rate > 1500"],
  },
};

export function setup() {
  grpc.loadModel("iris");

  return TestData;
}

export default function (data) {
  const modelName = __ENV.MODEL_NAME;
  grpc.infer(data[modelName].grpc);
}

export function teardown(data) {
  grpc.unloadModel("iris");
}
