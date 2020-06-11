start-testserver:
	python testserver.py

install-dev:
	GO111MODULE=on go get github.com/bojand/ghz/cmd/ghz@v0.55.0

generate:
	python generator.py

benchmark-grpc:
	ghz \
		--insecure \
		--proto ../proto/dataplane.proto \
		--call mlserver.dataplane.GRPCInferenceService/ModelInfer \
		--binary-file ./data/grpc-requests.pb \
		--total 1000 \
		localhost:8081
