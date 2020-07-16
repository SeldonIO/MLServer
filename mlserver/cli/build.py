"""
Tools to containerise a machine learning inference server.
"""
import os
import shutil

from textwrap import dedent

BUNDLE_NAME = "_bundle"

BASE_IMAGE_BLOCK = "FROM registry.access.redhat.com/ubi8/python-38"
UPGRADE_BLOCK = dedent(
    """
    # Upgrade pip
    RUN pip install --upgrade pip setuptools wheel
    """
)
INSTALL_MLSERVER_BLOCK = dedent(
    """
    # Install mlserver dependency
    # TODO: Install with pip once it's published in PyPi
    RUN pip install git+https://github.com/seldonio/mlserver#egg=mlserver
    """
)
REQUIREMENTS_TXT_BLOCK = dedent(
    """
    # Install requirements.txt
    COPY requirements.txt .
    RUN pip install -r requirements.txt
    """
)
COPY_LOCAL_BLOCK = dedent(
    """
    # Copy local files
    COPY . .
    """
)
CMD_BLOCK = 'CMD ["mlserver", "serve", "."]'

DOCKERIGNORE = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".Python",
    "env",
    "pip-log.txt",
    "pip-delete-this-directory.txt",
    ".tox",
    ".coverage",
    ".coverage.*",
    ".cache",
    "nosetests.xml",
    "coverage.xml",
    "*,cover",
    "*.log",
    ".git",
]


def generate_dockerfile(folder: str) -> str:
    """
    Generates a Dockerfile to build a Docker image.
    """
    blocks = [
        BASE_IMAGE_BLOCK,
        UPGRADE_BLOCK,
        INSTALL_MLSERVER_BLOCK,
    ]

    # If there is a `requirements.txt` file, install it
    requirements_txt = os.path.join(folder, "requirements.txt")
    if os.path.isfile(requirements_txt):
        blocks.append(REQUIREMENTS_TXT_BLOCK)

    blocks.extend([COPY_LOCAL_BLOCK, CMD_BLOCK])

    return "\n".join(blocks)


def generate_bundle(folder: str, bundle_folder: str = None) -> str:
    """
    Bundles your code and config into a folder.
    """
    if bundle_folder is None:
        # Default to _bundle
        bundle_folder = os.path.join(folder, BUNDLE_NAME)

    # Empty bundle folder
    shutil.rmtree(bundle_folder, ignore_errors=True)

    # Copy build context to bundle
    ignore = shutil.ignore_patterns(bundle_folder, *DOCKERIGNORE)
    shutil.copytree(folder, bundle_folder, ignore=ignore)

    # Write Dockerfile
    dockerfile_path = os.path.join(bundle_folder, "Dockerfile")
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile_content = generate_dockerfile(folder)
        dockerfile.write(dockerfile_content)

    # Write .dockerignore
    dockerignore_path = os.path.join(bundle_folder, ".dockerignore")
    with open(dockerignore_path, "w") as dockerignore:
        dockerignore_content = "\n".join(DOCKERIGNORE)
        dockerignore.write(dockerignore_content)

    return bundle_folder
