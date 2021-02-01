FROM python:3.7-slim

ENV MODELS_DIR /mnt/models

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

CMD mlserver start $MODELS_DIR
