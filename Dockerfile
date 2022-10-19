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

FROM registry.access.redhat.com/ubi8/ubi-minimal
SHELL ["/bin/bash", "-c"]

ARG RUNTIMES="all"

ENV MLSERVER_MODELS_DIR=/mnt/models \
    MLSERVER_ENV_TARBALL=/mnt/models/environment.tar.gz \
    PATH=/opt/mlserver/.local/bin:$PATH

# TODO: Install ffpmeg
RUN microdnf update -y && \
    microdnf install -y \
        python38 \
        libgomp mesa-libGL \
        glib2-devel shadow-utils && \
    ln -s /usr/bin/pip3 /usr/bin/pip && \
    ln -s /usr/bin/python3 /usr/bin/python

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
    if [[ $RUNTIMES == "all" ]]; then \
        for _wheel in "./dist/mlserver_"*.whl; do \
            echo "--> Installing $_wheel..."; \
            pip install $_wheel; \
        done \
    else \
        for _runtime in $RUNTIMES; do \
            _wheelName=$(echo $_runtime | tr '-' '_'); \
            _wheel="./dist/$_wheelName-"*.whl; \
            echo "--> Installing $_wheel..."; \
            pip install $_wheel; \
        done \
    fi && \
    pip install $(ls "./dist/mlserver-"*.whl)

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
CMD source ./hack/activate-env.sh $MLSERVER_ENV_TARBALL && \
    mlserver start $MLSERVER_MODELS_DIR
