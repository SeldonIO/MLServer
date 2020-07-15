from mlserver.cli.build import generate_dockerfile


def test_generate_dockerfile(model_folder: str):
    dockerfile = generate_dockerfile(model_folder)
    breakpoint()
