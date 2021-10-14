from typing import Tuple

from ..version import __version__

DockerfileTemplate = """
FROM continuumio/miniconda3:4.10.3 AS env-builder

ARG MLSERVER_ENV_NAME="mlserver-custom-env" \
    MLSERVER_ENV_TARBALL="environment.tar.gz"

COPY \
    {source_folder}/environment.yml \
    {source_folder}/conda.yml \
    .
RUN conda config --add channels conda-forge && \
    conda install conda-pack && \
    if [[ -f environment.yaml ]]; then \
        conda env create \
            --name $MLSERVER_ENV_NAME \
            --file environment.yaml; \
        conda-pack \
            -n $MLSERVER_ENV_NAME \
            -o $MLSERVER_ENV_TARBALL; \
    elif [[ -f conda.yaml ]]; then \
        conda env create \
            --name $MLSERVER_ENV_NAME \
            --file conda.yaml; \
        conda-pack \
            -n $MLSERVER_ENV_NAME \
            -o $MLSERVER_ENV_TARBALL; \
    fi

FROM seldonio/mlserver:{version}-slim

ENV MLSERVER_MODEL_IMPLEMENTATION={default_runtime}

# Copy all potential sources for custom environments
COPY --from=env-builder environment.tar.gz .
COPY {source_folder}/requirements.txt .

RUN ./hack/setup-env.sh .

# Copy everything else
COPY {source_folder} .
"""

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


def generate_dockerfile(folder: str) -> Tuple[str, str]:
    dockerfile = DockerfileTemplate.format(
        version=__version__, default_runtime="", source_folder=folder
    )

    return dockerfile, Dockerignore
