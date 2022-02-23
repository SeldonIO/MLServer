export function readTestData(name) {
  return {
    rest: JSON.parse(open(`../data/${name}/rest-requests.json`)),
    grpc: JSON.parse(open(`../data/${name}/grpc-requests.json`)),
  };
}
