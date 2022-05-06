/*
 * This benchmark expects a pre-generated large-ish set of models.
 * This can be generated using the `clone-models.sh` script.
 */

import { group } from "k6";
import { readTestData } from "../common/helpers.js";
import { RestClient } from "../common/rest.js";

const TestData = {
  iris: readTestData("iris"),
  sum_model: readTestData("sum-model"),
};

const rest = new RestClient();

const ModelCount = 10;

export const options = {
  scenarios: {
    sum_model: {
      executor: "per-vu-iterations",
      vus: 1,
      iterations: ModelCount,
      tags: { model_name: "sum-model" },
      env: { MODEL_NAME: "sum-model" },
    },
    iris: {
      executor: "per-vu-iterations",
      vus: 1,
      iterations: ModelCount,
      tags: { model_name: "iris" },
      env: { MODEL_NAME: "iris" },
    },
  },
};

export function setup() {
  return TestData;
}

export default function (data) {
  const modelBasename = __ENV.MODEL_NAME;

  const modelData = data[modelBasename.replace("-", "_")];
  const modelName = `${modelBasename}-${__ITER + 1}`;

  rest.loadModel(modelName);
  rest.infer(modelName, modelData.rest);
  // rest.unloadModel(modelName);
}

export function teardown(data) {}
