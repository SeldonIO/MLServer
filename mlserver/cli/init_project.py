import subprocess
from ..logging import logger


def init_cookiecutter_project(template: str):
    rc = subprocess.call(["which", "cookiecutter"])
    if rc == 0:
        cmd = f"cookiecutter {template}"
        subprocess.run(cmd, check=True, shell=True)
    else:
        logger.error(
            "The cookiecutter command is not found. \n\n"
            "Please install with 'pip install cookiecutter' and retry"
        )
