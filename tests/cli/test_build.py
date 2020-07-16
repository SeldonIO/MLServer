import os

from mlserver.cli.build import generate_dockerfile, generate_bundle, BUNDLE_NAME


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


def test_generate_bundle(model_folder: str, tmp_path):
    bundle_path = tmp_path / BUNDLE_NAME
    generated_bundle_path = generate_bundle(model_folder, bundle_path)

    files_to_assert = ["Dockerfile", "settings.json", "model-settings.json"]
    for file in files_to_assert:
        file_path = os.path.join(generated_bundle_path, file)
        assert os.path.isfile(file_path)
