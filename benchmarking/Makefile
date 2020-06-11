start-testserver:
	python testserver.py

install-ghz:
	GO111MODULE=on go get github.com/bojand/ghz/cmd/ghz@v0.55.0

generate-requests:
	python generator.py

benchmark-grpc:
	ghz \
		--insecure \
		--proto ../proto/dataplane.proto \
		--call mlserver.dataplane.GRPCInferenceService/ModelInfer \
		--data-file ./data/grpc-requests.json \
		localhost:8081
