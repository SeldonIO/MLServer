from mlserver import __version__
from mlserver.cli.build import generate_dockerfile, Dockerignore, DockerfileTemplate


def test_generate_dockerfile():
    source_folder = "."
    dockerfile, dockerignore = generate_dockerfile(source_folder)

    assert dockerignore == Dockerignore
    assert dockerfile == DockerfileTemplate.format(
        version=__version__, default_runtime="", source_folder=source_folder
    )
