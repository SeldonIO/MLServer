install-dev:
	pip install -r requirements-dev.txt
	pip install --editable .[all]

generate:
	./hack/generate-types.sh

run: 
	mlserver serve \
		./tests/testdata

test:
	tox

lint:
	flake8 .
	mypy .

fmt:
	black . \
		--exclude "(mlserver/grpc/dataplane_pb2*)"
  
