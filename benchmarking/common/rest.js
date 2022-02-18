import http from "k6/http";

export function loadModel(name) {
  http.post(`http://${__ENV.MLSERVER_HOST}/v2/repository/models/${name}/load`);
}

export function unloadModel(name) {
  http.post(
    `http://${__ENV.MLSERVER_HOST}/v2/repository/models/${name}/unload`
  );
}

export function infer(name, payload) {
  const headers = { "Content-Type": "application/json" };
  http.post(
    `http://${__ENV.MLSERVER_HOST}/v2/models/${name}/infer`,
    JSON.stringify(payload),
    { headers }
  );
}
