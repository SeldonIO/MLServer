DockerfileName = "Dockerfile"
DockerfileTemplate = """
FROM continuumio/miniconda3:4.10.3 AS env-builder
SHELL ["/bin/bash", "-c"]

ARG MLSERVER_ENV_NAME="mlserver-custom-env" \\
    MLSERVER_ENV_TARBALL="./envs/environment.tar.gz"

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
            conda-pack \
                -n $MLSERVER_ENV_NAME \\
                -o $MLSERVER_ENV_TARBALL; \\
        fi \\
    done; \\
    chmod -R 776 $(dirname $MLSERVER_ENV_TARBALL)

FROM seldonio/mlserver:{version}-slim
SHELL ["/bin/bash", "-c"]

ENV MLSERVER_MODEL_IMPLEMENTATION={default_runtime}

# Copy all potential sources for custom environments
COPY --from=env-builder /envs/*.tar.gz .
COPY ./requirements.tx[t] .

RUN ./hack/setup-env.sh .

# Copy everything else
COPY . .
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
