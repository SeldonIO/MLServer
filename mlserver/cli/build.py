"""
Tools to containerise a machine learning inference server.
"""
import os

from textwrap import dedent

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
