FROM python:3.8-slim AS wheel-builder
SHELL ["/bin/bash", "-c"]

COPY ./hack/build-wheels.sh ./hack/build-wheels.sh

COPY setup.py .
COPY README.md .
COPY ./mlserver/ ./mlserver/
COPY ./runtimes/ ./runtimes/

# TODO: Cache this step with BuildKit?
# This will build the wheels and place will place them in the
# /opt/mlserver/dist folder
RUN ./hack/build-wheels.sh /opt/mlserver/dist

FROM python:3.8-slim
SHELL ["/bin/bash", "-c"]

ENV MLSERVER_MODELS_DIR=/mnt/models \
    MLSERVER_ENV_TARBALL=/mnt/models/environment.tar.gz \
    PATH=/opt/mlserver/.local/bin:$PATH

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
        libgomp1 libgl1-mesa-dev libglib2.0-0

RUN mkdir /opt/mlserver
WORKDIR /opt/mlserver

# Create user and fix permissions
# NOTE: We need to make /opt/mlserver world-writable so that the image is
# compatible with random UIDs.
RUN useradd -u 1000 -s /bin/bash mlserver -d /opt/mlserver && \
    chown -R 1000:0 /opt/mlserver && \
    chmod -R 776 /opt/mlserver

USER 1000

COPY --from=wheel-builder /opt/mlserver/dist ./dist 
RUN pip install --upgrade pip wheel setuptools && \
    pip install ./dist/*.whl

COPY requirements/docker.txt requirements/docker.txt
RUN pip install -r requirements/docker.txt

COPY ./licenses/license.txt .

COPY ./hack/activate-env.sh ./hack/activate-env.sh

# Need to source `activate-env.sh` so that env changes get persisted
CMD . ./hack/activate-env.sh $MLSERVER_ENV_TARBALL \
    && mlserver start $MLSERVER_MODELS_DIR
