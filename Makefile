VERSION = $(shell sed 's/^__version__ = "\(.*\)"/\1/' ./mlserver/version.py)
IMAGE_NAME =seldonio/mlserver

.PHONY: install-dev _generate generate run build push-test push test lint fmt version clean licenses

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
	# docker build . -t ${IMAGE_NAME}:${VERSION}
	python setup.py sdist bdist_wheel
	python ./runtimes/sklearn/setup.py sdist bdist_wheel
	python ./runtimes/xgboost/setup.py sdist bdist_wheel
	python ./runtimes/mllib/setup.py sdist bdist_wheel

clean:
	rm -rf ./dist

push-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

push:
	docker push ${IMAGE_NAME}:${VERSION}
	twine upload dist/*

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

licenses:
	tox --recreate -e licenses
	cut -d, -f1,3 ./licenses/license_info.csv \
		> ./licenses/license_info.no_versions.csv

fmt:
	black . \
		--exclude "(mlserver/grpc/dataplane_pb2*)"

version:
	@echo ${VERSION}
  
