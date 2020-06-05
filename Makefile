install-dev:
	pip install -r requirements-dev.txt

generate:
	python -m grpc_tools.protoc \
		-I./proto \
		--python_out=./oink/grpc \
		--grpc_python_out=./oink/grpc \
		./proto/service.proto
