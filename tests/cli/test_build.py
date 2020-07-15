from mlserver.cli.build import generate_dockerfile


def test_generate_dockerfile(model_folder: str):
    dockerfile = generate_dockerfile(model_folder)

    assert "requirements.txt" not in dockerfile

    blocks = dockerfile.split("\n\n")
    assert len(blocks) == 5


def test_generate_dockerfile_with_reqs(model_folder_with_reqs: str):
    dockerfile = generate_dockerfile(model_folder_with_reqs)

    assert "requirements.txt" in dockerfile

    blocks = dockerfile.split("\n\n")
    assert len(blocks) == 6
