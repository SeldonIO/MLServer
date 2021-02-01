FROM python:3.7-slim

ENV MODELS_DIR /mnt/models
ENV ENV_TARBALL $MODELS_DIR/environment.tar.gz

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

CMD ./hack/activate-env.sh \
    && mlserver start $MODELS_DIR
