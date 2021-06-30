start-testserver:
	mlserver start ./testserver

install-dev:
	GO111MODULE=on go get github.com/bojand/ghz/cmd/ghz@v0.55.0
	GO111MODULE=on go get github.com/rakyll/hey@v0.1.3
	pip install -r requirements.txt

generate:
	python generator.py

benchmark-rest:
	hey \
		-n 100000 \
		-c 100 \
		-m POST \
		-T 'application/json' \
		-D ./data/iris/rest-requests.json \
		http://localhost:8080/v2/models/iris/infer

benchmark-grpc:
	ghz \
		--insecure \
		--proto ../proto/dataplane.proto \
		--call inference.GRPCInferenceService/ModelInfer \
		--binary-file ./data/iris/grpc-requests.pb \
		--total 100000 \
		--connections 50 \
		--concurrency 100 \
		localhost:8081
