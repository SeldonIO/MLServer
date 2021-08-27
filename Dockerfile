FROM python:3.7-slim

SHELL ["/bin/bash", "-c"]

ENV MLSERVER_MODELS_DIR=/mnt/models \
    MLSERVER_ENV_TARBALL=/mnt/models/environment.tar.gz \
    PATH=/home/default/.local/bin:$PATH

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
    libgomp1 && \
    apt-get install -y libgl1-mesa-dev && \
    apt-get install -y libglib2.0-0 && \
    pip install --upgrade pip wheel setuptools

RUN mkdir /opt/mlserver
WORKDIR /opt/mlserver

COPY setup.py .
# TODO: This busts the Docker cache before installing the rest of packages,
# which we don't want, but I can't see any way to install only deps from
# setup.py
COPY README.md .
COPY ./mlserver/ ./mlserver/
RUN pip install .

COPY ./runtimes/ ./runtimes/
RUN for _runtime in ./runtimes/*; \
    do \
    pip install $_runtime; \
    done

COPY requirements/docker.txt requirements/docker.txt
RUN pip install -r requirements/docker.txt

COPY ./licenses/license.txt .

COPY ./hack/activate-env.sh ./hack/activate-env.sh

# Create user and fix permissions
# NOTE: We need to make /opt/mlserver world-writable so that the image is
# compatible with random UIDs.
RUN useradd -u 1000 -s /bin/bash mlserver && \
    chown -R 1000:0 /opt/mlserver && \
    chmod -R 776 /opt/mlserver

USER 1000

# Need to source `activate-env.sh` so that env changes get persisted
CMD . ./hack/activate-env.sh $MLSERVER_ENV_TARBALL \
    && mlserver start $MLSERVER_MODELS_DIR
