FROM python:3.14-slim AS wheel-builder
SHELL ["/bin/bash", "-l", "-c"]

ARG POETRY_VERSION="2.1.1"

COPY ./hack/build-wheels.sh ./hack/build-wheels.sh
COPY ./mlserver ./mlserver
COPY ./runtimes ./runtimes
COPY \
    pyproject.toml \
    poetry.lock \
    README.md \
    .

# Install Poetry, build wheels and export constraints.txt file
# NOTE: Poetry outputs extras within the constraints, which are not supported
# by pip:
# https://github.com/python-poetry/poetry-plugin-export/issues/210
RUN pip install poetry==$POETRY_VERSION && \
    pip install poetry-plugin-export && \
    ./hack/build-wheels.sh /opt/mlserver/dist && \
    poetry export --with all-runtimes \
        --without-hashes \
        --format constraints.txt \
        -o /opt/mlserver/dist/constraints.txt && \
    sed -i 's/\[.*\]//g' /opt/mlserver/dist/constraints.txt && \
    # skip constraints for alibi libraries as they are currently pointing to git and thus confusing constraints \
    # remove when the alibi libraries versions are pointing to a released version
    sed -i '/git+https:\/\/github.com\/SeldonIO/d' /opt/mlserver/dist/constraints.txt

FROM registry.access.redhat.com/ubi9/ubi-minimal
SHELL ["/bin/bash", "-c"]

ARG PYTHON_VERSION=3.10.12
ARG CONDA_VERSION=23.11.0
ARG MINIFORGE_VERSION=${CONDA_VERSION}-0
ARG RUNTIMES="all"

# Set a few default environment variables, including `LD_LIBRARY_PATH`
# (required to use GKE's injected CUDA libraries).
# NOTE: When updating between major Python versions make sure you update the
# `/opt/conda` path within `LD_LIBRARY_PATH`.
ENV MLSERVER_MODELS_DIR=/mnt/models \
    MLSERVER_ENV_TARBALL=/mnt/models/environment.tar.gz \
    MLSERVER_PATH=/opt/mlserver \
    CONDA_PATH=/opt/conda \
    PATH=/opt/mlserver/.local/bin:/opt/conda/bin:$PATH \
    LD_LIBRARY_PATH=/usr/local/nvidia/lib64:/opt/conda/lib/python3.10/site-packages/nvidia/cuda_runtime/lib:$LD_LIBRARY_PATH \
    HF_HOME=/opt/mlserver/.cache \
    NUMBA_CACHE_DIR=/opt/mlserver/.cache

# Install some base dependencies required for some libraries
RUN microdnf update -y && \
    microdnf install -y \
        tar \
        gzip \
        libgomp \
        mesa-libGL \
        glib2-devel \
        shadow-utils \
        # git is used to pull alibi-detect and alibi-explain as we point now to master branches
        # remove git requirements when alibi-detect and alibi-explain are released
        git

# Install Conda, Python 3.10 and FFmpeg
RUN microdnf install -y wget && \
    wget "https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-x86_64.sh" \
        -O miniforge3.sh && \
    bash "./miniforge3.sh" -b -p $CONDA_PATH && \
    rm ./miniforge3.sh && \
    echo $PATH && \
    conda install --yes \
        conda=$CONDA_VERSION \
        python=$PYTHON_VERSION \
        ffmpeg && \
    conda clean -tipy && \
    microdnf remove -y wget && \
    echo "conda activate base" >> "$CONDA_PATH/etc/profile.d/conda.sh" && \
    ln -s "$CONDA_PATH/etc/profile.d/conda.sh" /etc/profile.d/conda.sh && \
    echo ". $CONDA_PATH/etc/profile.d/conda.sh" >> ~/.bashrc

RUN mkdir $MLSERVER_PATH
WORKDIR /opt/mlserver

# Create user and fix permissions
# NOTE: We need to make /opt/mlserver world-writable so that the image is
# compatible with random UIDs.
RUN useradd -u 1000 -s /bin/bash mlserver -d $MLSERVER_PATH && \
    chown -R 1000:0 $MLSERVER_PATH && \
    chmod -R 776 $MLSERVER_PATH

COPY --from=wheel-builder /opt/mlserver/dist ./dist
# NOTE: if runtime is "all" we install mlserver-<version>-py3-none-any.whl
# we have to use this syntax to return the correct file: $(ls ./dist/mlserver-*.whl)
# NOTE: Temporarily excluding mllib from the main image due to:
#   CVE-2022-25168
#   CVE-2022-42889
# NOTE: Removing explicitly requirements.txt file from spaCy's test
# dependencies causing false positives in Snyk.
RUN . $CONDA_PATH/etc/profile.d/conda.sh && \
    pip install --upgrade pip wheel setuptools && \
    if [[ $RUNTIMES == "all" ]]; then \
        for _wheel in "./dist/mlserver_"*.whl; do \
            if [[ ! $_wheel == *"mllib"* ]]; then \
                echo "--> Installing $_wheel..."; \
                pip install $_wheel --constraint ./dist/constraints.txt; \
            fi \
        done \
    else \
        for _runtime in $RUNTIMES; do \
            _wheelName=$(echo $_runtime | tr '-' '_'); \
            _wheel="./dist/$_wheelName-"*.whl; \
            echo "--> Installing $_wheel..."; \
            pip install $_wheel --constraint ./dist/constraints.txt; \
        done \
    fi && \
    pip install $(ls "./dist/mlserver-"*.whl) --constraint ./dist/constraints.txt && \
    rm -f /opt/conda/lib/python3.10/site-packages/spacy/tests/package/requirements.txt && \
    rm -rf /root/.cache/pip

COPY ./licenses/license.txt .
COPY ./licenses/license.txt /licenses/
COPY \
    ./hack/build-env.sh \
    ./hack/generate_dotenv.py \
    ./hack/activate-env.sh \
    ./hack/

USER 1000

# We need to build and activate the "hot-loaded" environment before MLServer
# starts
CMD . $CONDA_PATH/etc/profile.d/conda.sh && \
    source ./hack/activate-env.sh $MLSERVER_ENV_TARBALL && \
    mlserver start $MLSERVER_MODELS_DIR
