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

COPY ./runtimes/sklearn ./runtimes/sklearn
RUN pip install ./runtimes/sklearn

COPY ./runtimes/xgboost ./runtimes/xgboost
RUN pip install ./runtimes/xgboost

COPY ./runtimes/mllib ./runtimes/mllib
RUN pip install ./runtimes/mllib

COPY ./runtimes/lightgbm ./runtimes/lightgbm
RUN pip install ./runtimes/lightgbm

COPY ./licenses/license.txt .

CMD mlserver start $MODELS_DIR
