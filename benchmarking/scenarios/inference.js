import { readTestData } from "../common/helpers.js";
import { loadModel, infer, unloadModel } from "../common/rest.js";

const TestData = {
  iris: readTestData("iris"),
  sum_model: readRESTRequest("sum-model"),
};

export function setup() {
  loadModel("iris");

  return TestData;
}

export default function (data) {
  infer("iris", data.iris.rest);
}

export function teardown(data) {
  unloadModel("iris");
}
