SHELL := /bin/bash
VERSION := $(shell sed 's/^__version__ = "\(.*\)"/\1/' ./mlserver/version.py)
IMAGE_NAME := seldonio/mlserver

.PHONY: install-dev _generate generate run build \
	push-test push test lint fmt version clean licenses

install-dev:
	pip install -r requirements/dev.txt
	for _runtime in ./runtimes/*; \
	do \
		pip install --editable $$_runtime; \
		if [[ -f $$_runtime/requirements/dev.txt ]]; \
		then \
			pip install -r $$_runtime/requirements/dev.txt; \
		fi \
	done
	pip install --editable .
	pip install -r ./requirements/docker.txt

_generate: # "private" target to call `fmt` after `generate`
	./hack/generate-types.sh

generate: | _generate fmt

run: 
	mlserver start \
		./tests/testdata

build: clean 
	./hack/build-images.sh ${VERSION}
	./hack/build-wheels.sh ./dist

clean:
	rm -rf ./dist ./build *.egg-info
	for _runtime in ./runtimes/*; \
	do \
		rm -rf $$_runtime/dist; \
		rm -rf $$_runtime/build; \
		rm -rf $$_runtime/*.egg-info; \
	done

push-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

push:
	twine upload dist/*
	docker push ${IMAGE_NAME}:${VERSION}
	docker push ${IMAGE_NAME}:${VERSION}-slim
	for _runtime in ./runtimes/*; \
	do \
	  _runtimeName=$$(basename $$_runtime); \
		docker push ${IMAGE_NAME}:${VERSION}-$$_runtimeName; \
	done

test:
	tox

lint: generate
	flake8 .
	mypy ./mlserver
	for _runtime in ./runtimes/*; \
	do \
		mypy $$_runtime || exit 1; \
	done
	mypy ./benchmarking
	mypy ./docs/examples
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
		--exclude "/(\.tox.*|mlserver/grpc/dataplane_pb2.*|venv.*)/"

version:
	@echo ${VERSION}
