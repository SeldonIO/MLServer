# MLSERVER_SYS_TRACING may be set to:
# - "sdt-sys-tracing" build SDT (static-defined tracing) native dependencies
# - "without-sys-tracing" no system tracing dependencies
ARG OPT_MLSERVER_SYS_TRACING="sdt-sys-tracing"
ARG LIBSTAPSDT_VERSION="0.1.1"


FROM python:3.10-slim AS wheel-builder
SHELL ["/bin/bash", "-l", "-c"]

ARG POETRY_VERSION="1.4.2"
ARG OPT_MLSERVER_SYS_TRACING

ENV OPT_MLSERVER_SYS_TRACING=${OPT_MLSERVER_SYS_TRACING:-without-sys-tracing}

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
    ./hack/build-wheels.sh /opt/mlserver/dist && \
    _extras=() && \
    if [[ "${OPT_MLSERVER_SYS_TRACING}" == "sdt-sys-tracing" ]]; then \
        _extras+=("-E tracepoints"); \
    fi && \
    poetry export --with all-runtimes \
        --without-hashes \
        "${_extras[@]}" \
        --format constraints.txt \
        -o /opt/mlserver/dist/constraints.txt && \
    sed -i 's/\[.*\]//g' /opt/mlserver/dist/constraints.txt


# Build native dependencies for tracepoints; 
# Almalinux is binary-compatible with rhel ubi images but contains repositories
# with additional devel packages (elfutils-libelf-devel needed here)
FROM almalinux/9-minimal AS libstapsdt-builder
SHELL ["/bin/bash", "-c"]

ARG LIBSTAPSDT_VERSION

# Install libstapsdt dev dependencies
RUN microdnf update -y && \
    microdnf install -y \
        wget \
        tar \
        gzip \
        gcc \
        make \
        findutils \
        elfutils-libelf-devel

# Get libstapsdt sources, compile and install into separate tree
# We also need to patch the resulting library symlink to be relative so that
# we may copy the resulting files in a different container directly
RUN wget "https://github.com/linux-usdt/libstapsdt/archive/refs/tags/v${LIBSTAPSDT_VERSION}.tar.gz" && \
    tar -xzf v${LIBSTAPSDT_VERSION}.tar.gz && \
    cd libstapsdt-${LIBSTAPSDT_VERSION} && \
    make && \
    make install DESTDIR=/libstapsdt-install && \
    cd /libstapsdt-install/usr/lib && \
    readlink libstapsdt.so | sed s+/libstapsdt-install/usr/lib/++ | xargs -I % ln -fs % libstapsdt.so


FROM registry.access.redhat.com/ubi9/ubi-minimal
SHELL ["/bin/bash", "-c"]

ARG PYTHON_VERSION=3.10.11
ARG CONDA_VERSION=23.1.0
ARG MINIFORGE_VERSION=${CONDA_VERSION}-1
ARG RUNTIMES="all"
ARG OPT_MLSERVER_SYS_TRACING

# Set a few default environment variables, including `LD_LIBRARY_PATH`
# (required to use GKE's injected CUDA libraries).
# NOTE: When updating between major Python versions make sure you update the
# `/opt/conda` path within `LD_LIBRARY_PATH`.
ENV MLSERVER_MODELS_DIR=/mnt/models \
    MLSERVER_ENV_TARBALL=/mnt/models/environment.tar.gz \
    MLSERVER_PATH=/opt/mlserver \
    OPT_MLSERVER_SYS_TRACING=${OPT_MLSERVER_SYS_TRACING:-without-sys-tracing} \
    CONDA_PATH=/opt/conda \
    PATH=/opt/mlserver/.local/bin:/opt/conda/bin:$PATH \
    LD_LIBRARY_PATH=/usr/local/nvidia/lib64:/opt/conda/lib/python3.10/site-packages/nvidia/cuda_runtime/lib:$LD_LIBRARY_PATH \
    TRANSFORMERS_CACHE=/opt/mlserver/.cache \
    NUMBA_CACHE_DIR=/opt/mlserver/.cache

# Install some base dependencies required for some libraries
RUN microdnf update -y && \
    microdnf install -y \
        tar \
        gzip \
        libgomp \
        mesa-libGL \
        glib2-devel \
        shadow-utils && \
        if [[ "${OPT_MLSERVER_SYS_TRACING}" == "sdt-sys-tracing" ]]; then \
            microdnf install -y \
                elfutils-libelf; \
        fi

# Install libstapsdt
COPY --from=libstapsdt-builder /libstapsdt-install /
# Update symlinks & ldconfig cache
RUN ldconfig

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
    _extras=() && \
    if [[ "${OPT_MLSERVER_SYS_TRACING}" == "sdt-sys-tracing" ]]; then \
        _extras+=( "tracepoints" ); \
    fi && \
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
    if [[ ${#_extras[@]} -gt 0 ]]; then \
        extras_list=$(IFS=, ; echo "${_extras[@]}") && \ 
        pip install $(ls "./dist/mlserver-"*.whl)[${extras_list}] --constraint ./dist/constraints.txt; \
    else \
        pip install $(ls "./dist/mlserver-"*.whl) --constraint ./dist/constraints.txt; \
    fi && \
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
