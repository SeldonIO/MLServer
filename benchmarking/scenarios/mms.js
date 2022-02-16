import http from "k6/http";

function loadModel(name) {
  http.post(`http://${__ENV.MLSERVER_HOST}/v2/repository/models/${name}/load`);
}

function unloadModel(name) {
  http.post(
    `http://${__ENV.MLSERVER_HOST}/v2/repository/models/${name}/unload`
  );
}

function infer(name, payload) {
  const headers = { "Content-Type": "application/json" };
  http.post(
    `http://${__ENV.MLSERVER_HOST}/v2/models/${name}/infer`,
    JSON.stringify(payload),
    { headers }
  );
}

function readRESTRequest(name) {
  return JSON.parse(open(`../data/${name}/rest-requests.json`));
}

const TestData = {
  iris: readRESTRequest("iris"),
  sum_model: readRESTRequest("sum-model"),
};

export function setup() {
  loadModel("iris");
  loadModel("sum-model");

  return TestData;
}

export default function (data) {
  infer("iris", data.iris);
  infer("sum-model", data.sum_model);
}

export function teardown(data) {
  unloadModel("iris");
  unloadModel("sum-model");
}
