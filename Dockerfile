FROM python:3.8-slim AS wheel-builder
SHELL ["/bin/bash", "-c"]

COPY ./hack/build-wheels.sh ./hack/build-wheels.sh
COPY ./mlserver ./mlserver
COPY ./runtimes ./runtimes
COPY \
    setup.py \
    README.md \
    .

# This will build the wheels and place will place them in the
# /opt/mlserver/dist folder
RUN ./hack/build-wheels.sh /opt/mlserver/dist

FROM python:3.8-slim
SHELL ["/bin/bash", "-c"]

ARG RUNTIMES="all"

ENV MLSERVER_MODELS_DIR=/mnt/models \
    MLSERVER_ENV_TARBALL=/mnt/models/environment.tar.gz \
    PATH=/opt/mlserver/.local/bin:$PATH

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
        libgomp1 libgl1-mesa-dev libglib2.0-0 build-essential

RUN mkdir /opt/mlserver
WORKDIR /opt/mlserver

# Create user and fix permissions
# NOTE: We need to make /opt/mlserver world-writable so that the image is
# compatible with random UIDs.
RUN useradd -u 1000 -s /bin/bash mlserver -d /opt/mlserver && \
    chown -R 1000:0 /opt/mlserver && \
    chmod -R 776 /opt/mlserver

COPY --from=wheel-builder /opt/mlserver/dist ./dist 
# note: if runtime is "all" we install mlserver-<version>-py3-none-any.whl
# we have to use this syntax to return the correct file: $(ls ./dist/mlserver-*.whl)
RUN pip install --upgrade pip wheel setuptools && \
    pip install $(ls ./dist/mlserver-*.whl)[all]; \
    if [[ $RUNTIMES == "all" ]]; then \
        pip install ./dist/mlserver_*.whl; \
    else \
        for _runtime in $RUNTIMES; do \
            _wheelName=$(echo $_runtime | tr '-' '_'); \
            pip install "./dist/$_wheelName-"*.whl; \
        done \
    fi

COPY requirements/docker.txt requirements/docker.txt
RUN pip install -r requirements/docker.txt

COPY ./licenses/license.txt .
COPY \
    ./hack/build-env.sh \
    ./hack/generate_dotenv.py \
    ./hack/activate-env.sh \
    ./hack/

USER 1000

# We need to build and activate the "hot-loaded" environment before MLServer
# starts
CMD source ./hack/activate-env.sh $MLSERVER_ENV_TARBALL . && \
    mlserver start $MLSERVER_MODELS_DIR
