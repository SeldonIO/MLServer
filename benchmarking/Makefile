start-testserver:
	mlserver start ${PWD}/testserver

install-dev:
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
		-e MLSERVER_HOST=0.0.0.0 \
		-e MLSERVER_HTTP_PORT=8080 \
		-e MLSERVER_GRPC_PORT=8081 \
		scenarios/inference-rest.js

benchmark-grpc:
	k6 run \
		-e MLSERVER_HOST=localhost \
		-e MLSERVER_HTTP_PORT=8080 \
		-e MLSERVER_GRPC_PORT=8081 \
		scenarios/inference-grpc.js
