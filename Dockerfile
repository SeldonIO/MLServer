FROM python:3.7-slim

SHELL ["/bin/bash", "-c"]

ENV MLSERVER_MODELS_DIR=/mnt/models \
    MLSERVER_ENV_TARBALL=/mnt/models/environment.tar.gz \
    PATH=/home/default/.local/bin:$PATH \
    WORKDIR=/home/default/mlserver

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
      libgomp1

RUN useradd --create-home default

USER default

RUN mkdir $WORKDIR
WORKDIR $WORKDIR 

COPY --chown=default setup.py .
# TODO: This busts the Docker cache before installing the rest of packages,
# which we don't want, but I can't see any way to install only deps from
# setup.py
COPY --chown=default README.md .
COPY --chown=default ./mlserver/ ./mlserver/
RUN pip install .

COPY --chown=default ./runtimes/ ./runtimes/
RUN for _runtime in ./runtimes/*; \
    do \
    pip install $_runtime; \
    done

COPY --chown=default ./licenses/license.txt .

COPY --chown=default ./hack/activate-env.sh ./hack/activate-env.sh

# Need to source `activate-env.sh` so that env changes get persisted
CMD . ./hack/activate-env.sh $MLSERVER_ENV_TARBALL \
    && mlserver start $MLSERVER_MODELS_DIR
