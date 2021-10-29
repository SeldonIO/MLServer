import os

from typing import Dict
from setuptools import setup, find_packages

ROOT_PATH = os.path.dirname(__file__)
PKG_NAME = "mlserver-mllib"
PKG_PATH = os.path.join(ROOT_PATH, PKG_NAME.replace("-", "_"))


def _load_version() -> str:
    version = ""
    version_path = os.path.join(PKG_PATH, "version.py")
    with open(version_path) as fp:
        version_module: Dict[str, str] = {}
        exec(fp.read(), version_module)
        version = version_module["__version__"]

    return version


def _load_description() -> str:
    readme_path = os.path.join(ROOT_PATH, "README.md")
    with open(readme_path) as fp:
        return fp.read()


setup(
    name=PKG_NAME,
    version=_load_version(),
    url="https://github.com/SeldonIO/MLServer.git",
    author="Seldon Technologies Ltd.",
    author_email="hello@seldon.io",
    description="Spark MLlib runtime for MLServer",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "mlserver",
        "pyspark",
    ],
    long_description=_load_description(),
    long_description_content_type="text/markdown",
    license="Apache 2.0",
)
