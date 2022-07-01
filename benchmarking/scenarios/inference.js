import { group } from "k6";
import { readTestData } from "../common/helpers.js";
import { RestClient } from "../common/rest.js";
import { GrpcClient } from "../common/grpc.js";

const TestData = {
  iris: readTestData("iris"),
  sum_model: readTestData("sum-model"),
};

const rest = new RestClient();
const grpc = new GrpcClient();

const ScenarioDuration = "60s";
const ScenarioVUs = 200;

export const options = {
  scenarios: {
    iris_rest: {
      executor: "constant-arrival-rate",
      rate: 1000,
      timeUnit: "1s",
      duration: ScenarioDuration,
      preAllocatedVUs: 100,
      maxVUs: ScenarioVUs,
      tags: { model_name: "iris", protocol: "rest" },
      env: { MODEL_NAME: "iris", PROTOCOL: "rest" },
    },
    iris_grpc: {
      executor: "constant-arrival-rate",
      rate: 1000,
      timeUnit: "1s",
      duration: ScenarioDuration,
      preAllocatedVUs: 100,
      maxVUs: ScenarioVUs,
      startTime: ScenarioDuration,
      tags: { model_name: "iris", protocol: "grpc" },
      env: { MODEL_NAME: "iris", PROTOCOL: "grpc" },
    },
  },
};

export function setup() {
  rest.loadModel("iris");

  return TestData;
}

export default function (data) {
  const modelName = __ENV.MODEL_NAME;

  switch (__ENV.PROTOCOL) {
    case "rest":
      rest.infer(modelName, data[modelName].rest);
      break;
    case "grpc":
      grpc.infer(data[modelName].grpc);
      break;
  }
}

export function teardown(data) {
  rest.unloadModel("iris");
}
