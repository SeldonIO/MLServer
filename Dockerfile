FROM python:3.7-slim

ENV MLSERVER_MODELS_DIR=/mnt/models
ENV MLSERVER_ENV_TARBALL=$MODELS_DIR/environment.tar.gz

SHELL ["/bin/bash", "-c"]

# TODO: Remove git and openssh-client once tempo is published
RUN apt-get update && \
    apt-get -y --no-install-recommends install \
      libgomp1 git openssh-client

# Download public key for github.com
# TODO: Remove git once tempo is published
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

WORKDIR /workspace
COPY setup.py .
# TODO: This busts the Docker cache before installing the rest of packages,
# which we don't want, but I can't see any way to install only deps from
# setup.py
COPY README.md .
COPY ./mlserver/ ./mlserver/
RUN pip install .

COPY ./runtimes/ ./runtimes/
# TODO: Remove SSH once tempo is published
RUN --mount=type=ssh for _runtime in ./runtimes/*; \
    do \
    pip install $_runtime; \
    done

COPY ./licenses/license.txt .

COPY ./hack/activate-env.sh ./hack/activate-env.sh

# Need to source `activate-env.sh` so that env changes get persisted
CMD . ./hack/activate-env.sh $MLSERVER_ENV_TARBALL \
    && mlserver start $MLSERVER_MODELS_DIR
