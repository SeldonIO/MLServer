import { group } from "k6";
import { readTestData } from "../common/helpers.js";
import { RestClient } from "../common/rest.js";

const TestData = {
  iris: readTestData("iris"),
};

const rest = new RestClient();

const ScenarioDuration = "60s";
const ScenarioVUs = 300;

export const options = {
  scenarios: {
    iris_rest: {
      executor: "constant-vus",
      duration: ScenarioDuration,
      vus: ScenarioVUs,
      tags: { model_name: "iris", protocol: "rest" },
      env: { MODEL_NAME: "iris", PROTOCOL: "rest" },
    },
  },
  thresholds: {
    http_reqs: ["rate > 1100"],
  },
};

export function setup() {
  rest.loadModel("iris");

  return TestData;
}

export default function (data) {
  const modelName = __ENV.MODEL_NAME;
  rest.infer(modelName, data[modelName].rest);
}

export function teardown(data) {
  rest.unloadModel("iris");
}
