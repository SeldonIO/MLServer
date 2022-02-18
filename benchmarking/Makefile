start-testserver:
	mlserver start ${PWD}/testserver

install-dev:
	pip install -r requirements.txt
	@if [[ ! -x "$$(command -v k6)" ]];\
	then \
		echo "k6 command not found!"; \
		echo "To install k6, please check: "; \
		echo "    https://k6.io/docs/getting-started/installation/"; \
	fi

generate:
	python generator.py

benchmark-rest:
	k6 run \
		-e MLSERVER_HOST=0.0.0.0:8080 \
		--vus 100 \
		--duration 60s \
		scenarios/inference.js

benchmark-grpc:
	ghz \
		--insecure \
		--proto ../proto/dataplane.proto \
		--call inference.GRPCInferenceService/ModelInfer \
		--binary-file ./data/iris/grpc-requests.pb \
		--total 100000 \
		--connections 100 \
		--concurrency 100 \
		localhost:8081
