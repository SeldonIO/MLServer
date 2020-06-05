install-dev:
	pip install -r requirements-dev.txt

install:
	pip install -r requirements.txt

generate:
	./hack/generate-types.sh
