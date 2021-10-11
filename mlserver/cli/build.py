from typing import Dict

from ..version import __version__

DockerfileTemplate = """
FROM seldonio/mlserver:{version}-slim

ENV MLSERVER_MODEL_IMPLEMENTATION={default_runtime}

# Copy all potential sources for custom environments
COPY \
    requirements.txt \
    # setup.py \
    environment.yaml \
    conda.yaml \
    .
RUN ./hack/setup-environment.sh .

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


def generate_dockerfile(folder: str) -> Dict[str, str]:
    dockerfile = DockerfileTemplate.format(
        version=__version__, default_runtime="", source_folder=folder
    )

    return {"Dockerfile": dockerfile, ".dockerignore": Dockerignore}
