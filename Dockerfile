FROM python:3.7-slim

SHELL ["/bin/bash", "-c"]

ENV MLSERVER_MODELS_DIR=/mnt/models \
    MLSERVER_ENV_TARBALL=/mnt/models/environment.tar.gz \
    PATH=/home/default/.local/bin:$PATH

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
      libgomp1

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

COPY ./licenses/license.txt .

COPY ./hack/activate-env.sh ./hack/activate-env.sh

# Create user and fix permissions
RUN useradd -u 1000 -s /bin/bash mlserver && \
    mkdir /opt/mlserver && \
    chown -R 1000:0 /opt/mlserver

USER 1000
WORKDIR /opt/mlserver

# Need to source `activate-env.sh` so that env changes get persisted
CMD . ./hack/activate-env.sh $MLSERVER_ENV_TARBALL \
    && mlserver start $MLSERVER_MODELS_DIR
