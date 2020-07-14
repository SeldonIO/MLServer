IMAGE_NAME="seldonio/mlserver-custom"
IMAGE_VERSION=0.1.0

build:
	docker build . -t ${IMAGE_NAME}:${VERSION}

run:
	docker run -it --rm \
		-p 8080:8080 \
		-p 8081:8081 \
		${IMAGE_NAME}:${IMAGE_VERSION}


