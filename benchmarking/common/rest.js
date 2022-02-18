import { check } from "k6";
import http from "k6/http";

function checkResponse(res) {
  check(res, {
    "is status 200": (r) => r.status === 200,
  });
}

export class RestClient {
  constructor() {
    this.restHost = `http://${__ENV.MLSERVER_HOST}:${__ENV.MLSERVER_HTTP_PORT}`;
  }

  loadModel(name) {
    const res = http.post(`${this.restHost}/v2/repository/models/${name}/load`);

    checkResponse(res);
    return res;
  }

  unloadModel(name) {
    const res = http.post(
      `${this.restHost}/v2/repository/models/${name}/unload`
    );

    checkResponse(res);
    return res;
  }

  infer(name, payload) {
    const headers = { "Content-Type": "application/json" };
    const res = http.post(
      `${this.restHost}/v2/models/${name}/infer`,
      JSON.stringify(payload),
      { headers }
    );

    checkResponse(res);
    return res;
  }
}
