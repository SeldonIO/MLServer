FROM python:3.7-slim

ENV MLSERVER_MODELS_DIR /mnt/models
ENV MLSERVER_ENV_TARBALL $MODELS_DIR/environment.tar.gz

SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
      libgomp1

WORKDIR /workspace
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

# Need to source `activate-env.sh` so that env changes get persisted
CMD . ./hack/activate-env.sh $ENV_TARBALL \
    && mlserver start $MODELS_DIR
