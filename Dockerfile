FROM python:3.8.5-slim

ENV MODELS_DIR /mnt/models

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
      libgomp1

WORKDIR /workspace
COPY setup.py .
# TODO: This busts the cache, which we don't want, but I can't see any
# way to install only deps from setup.py
COPY ./mlserver/ ./mlserver/
RUN pip install .[all]

CMD mlserver start $MODELS_DIR

