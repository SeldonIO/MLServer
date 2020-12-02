VERSION = $(shell sed 's/^__version__ = "\(.*\)"/\1/' ./mlserver/version.py)
IMAGE_NAME =seldonio/mlserver

install-dev:
	pip install -r requirements-dev.txt
	pip install --editable .
	pip install --editable ./runtimes/sklearn
	pip install --editable ./runtimes/xgboost
	pip install --editable ./runtimes/mllib

_generate: # "private" target to call `fmt` after `generate`
	./hack/generate-types.sh

generate: | _generate fmt

run: 
	mlserver start \
		./tests/testdata

build:
	docker build . -t ${IMAGE_NAME}:${VERSION}

push:
	docker push ${IMAGE_NAME}:${VERSION}

test:
	tox

lint: generate
	flake8 .
	mypy .
	# Check if something has changed after generation
	git \
		--no-pager diff \
		--exit-code \
		.

fmt:
	black . \
		--exclude "(mlserver/grpc/dataplane_pb2*)"

version:
	@echo ${VERSION}
  
