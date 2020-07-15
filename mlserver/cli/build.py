"""
Tools to containerise a machine learning inference server.
"""
import os


def generate_dockerfile(folder: str) -> str:
    """
    Generates a Dockerfile to build a Docker image.
    """

    blocks = [
        "FROM registry.access.redhat.com/ubi8/python-38",
        """
        # Upgrade pip
        RUN pip install --upgrade pip setuptools wheel
        """,
        """
        # Install mlserver dependency
        # TODO: Install with pip once it's published in PyPi
        RUN pip install git+https://github.com/seldonio/mlserver#egg=mlserver
        """,
    ]

    # If there is a `requirements.txt` file, install it
    requirements_txt = os.path.join(folder, "requirements.txt")
    if os.path.isfile(requirements_txt):
        blocks.append(
            """
            # Install requirements.txt
            COPY requirements.txt .
            RUN pip install -r requirements.txt
            """
        )

    blocks.extend(
        [
            """
            # Copy local files
            COPY . .
            """,
            'CMD ["mlserver", "serve", "."]',
        ]
    )

    return "\n\n".join(blocks)
