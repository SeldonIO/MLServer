VERSION = $(shell sed 's/^__version__ = "\(.*\)"/\1/' ./mlserver/version.py)
IMAGE_NAME =seldonio/mlserver

install-dev:
	pip install -r requirements-dev.txt
	pip install --editable .[all]

generate:
	./hack/generate-types.sh

run: 
	mlserver start \
		./tests/testdata

build:
	docker build . -t ${IMAGE_NAME}:${VERSION}

push:
	docker push ${IMAGE_NAME}:${VERSION}

test:
	tox

lint:
	flake8 .
	mypy .

fmt:
	black . \
		--exclude "(mlserver/grpc/dataplane_pb2*)"

version:
	@echo ${VERSION}
  
