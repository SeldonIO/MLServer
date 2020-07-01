start-testserver:
	python testserver.py

profile-testserver:
	mkdir -p profiles
	python -m cProfile \
		-o "profiles/$(shell date +'%Y-%m-%dT%H:%M:%S').prof" \
		testserver.py

install-dev:
	GO111MODULE=on go get github.com/bojand/ghz/cmd/ghz@v0.55.0
	GO111MODULE=on go get github.com/rakyll/hey@v0.1.3

generate:
	python generator.py

benchmark-rest:
	hey \
		-n 100000 \
		-c 100 \
		-m POST \
		-T 'application/json' \
		-D ./data/rest-requests.json \
		http://localhost:8080/v2/models/sum-model/versions/v1.2.3/infer

benchmark-grpc:
	ghz \
		--insecure \
		--proto ../proto/dataplane.proto \
		--call mlserver.dataplane.GRPCInferenceService/ModelInfer \
		--binary-file ./data/grpc-requests.pb \
		--total 100000 \
		--connections 50 \
		--concurrency 100 \
		localhost:8081
