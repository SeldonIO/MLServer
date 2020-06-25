install-dev:
	pip install -r requirements-dev.txt
	pip install --editable .

install:
	pip install -r requirements.txt

generate:
	./hack/generate-types.sh

run: 
	python -m mlserver

test:
	pytest

lint:
	flake8 .
	mypy .

fmt:
	black . \
		--exclude "(mlserver/grpc/dataplane_pb2*)"
  
