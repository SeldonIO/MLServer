DockerfileName = "Dockerfile"
DockerfileTemplate = """
FROM continuumio/miniconda3:4.12.0 AS env-builder
SHELL ["/bin/bash", "-c"]

ARG MLSERVER_ENV_NAME="mlserver-custom-env" \\
    MLSERVER_ENV_TARBALL="./envs/base.tar.gz"

RUN conda config --add channels conda-forge && \\
    conda install conda-pack

# The `[]` character range will ensure that Docker doesn't complain if the
# files don't exist:
# https://stackoverflow.com/a/65138098/5015573
COPY \\
    ./environment.ym[l] \\
    ./environment.yam[l] \\
    ./conda.ym[l] \\
    ./conda.yam[l] \\
    .
RUN mkdir $(dirname $MLSERVER_ENV_TARBALL); \\
    for envFile in environment.yml environment.yaml conda.yml conda.yaml; do \\
        if [[ -f $envFile ]]; then \\
            conda env create \
                --name $MLSERVER_ENV_NAME \\
                --file $envFile; \\
            conda-pack --ignore-missing-files --quiet \
                -n $MLSERVER_ENV_NAME \\
                -o $MLSERVER_ENV_TARBALL; \\
        fi \\
    done; \\
    chmod -R 776 $(dirname $MLSERVER_ENV_TARBALL)

FROM seldonio/mlserver:{version}-slim
SHELL ["/bin/bash", "-c"]

# Copy all potential sources for custom environments
COPY \\
    --chown=1000 \\
    --from=env-builder \\
    /envs/base.tar.g[z] \\
    ./envs/base.tar.gz
COPY \\
    ./settings.jso[n] \\
    ./model-settings.jso[n] \\
    ./requirements.tx[t] \\
    .

USER root
# Install dependencies system-wide, to ensure that they are available for every
# user and give permissions to (future) environment folder.
RUN ./hack/build-env.sh . && \\
    mkdir -p ./envs/base && \\
    chown -R 1000:0 ./envs/base && \\
    chmod -R 776 ./envs/base && \\
    rm -rf /root/.cache/pip
USER 1000

# Copy everything else
COPY . .

# Override MLServer's own `CMD` to activate the embedded environment
# (optionally activating the hot-loaded one as well).
CMD source ./hack/activate-env.sh ./envs/base.tar.gz && \\
    mlserver start $MLSERVER_MODELS_DIR
"""

DockerignoreName = ".dockerignore"
Dockerignore = """
# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib
*.pyc
*.pyo
*.pyd
bin

# MLServer folders
.metrics
.envs

# Mac file system
**/.DS_Store

# Python dev
__pycache__
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.mypy_cache
eggs/
.eggs/
*.egg-info/
./pytest_cache
.tox
build/
dist/

# Notebook Checkpoints
.ipynb_checkpoints

.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*,cover
*.log
.git
"""
