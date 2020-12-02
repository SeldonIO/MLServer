import os

from typing import Dict
from setuptools import setup, find_packages

ROOT_PATH = os.path.dirname(__file__)
PKG_NAME = "mlserver-xgboost"
PKG_PATH = os.path.join(ROOT_PATH, PKG_NAME.replace("-", "_"))


def _load_version() -> str:
    version = ""
    version_path = os.path.join(PKG_PATH, "version.py")
    with open(version_path) as fp:
        version_module: Dict[str, str] = {}
        exec(fp.read(), version_module)
        version = version_module["__version__"]

    return version


setup(
    name=PKG_NAME,
    version=_load_version(),
    url="https://github.com/seldonio/mlserver.git",
    author="Seldon Technologies Ltd.",
    author_email="hello@seldon.io",
    description="XGBoost runtime for MLServer",
    packages=find_packages(),
    install_requires=["mlserver", "xgboost==1.1.1"],
)
