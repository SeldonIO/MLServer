import os

from typing import Dict
from setuptools import setup, find_packages

ROOT_PATH = os.path.dirname(__file__)
PKG_NAME = "mlserver"
PKG_PATH = os.path.join(ROOT_PATH, PKG_NAME)


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


env_marker_cpython = (
    "sys_platform != 'win32'"
    " and (sys_platform != 'cygwin'"
    " and platform_python_implementation != 'PyPy')"
)

setup(
    name=PKG_NAME,
    version=_load_version(),
    url="https://github.com/SeldonIO/MLServer.git",
    author="Seldon Technologies Ltd.",
    author_email="hello@seldon.io",
    description="ML server",
    include_package_data=True,
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "click",
        # 0.89.0: https://github.com/tiangolo/fastapi/issues/5861
        "fastapi >=0.88.0, <=0.89.1, !=0.89.0",
        "python-dotenv",
        "grpcio",
        # The importlib-resources backport is required to use some
        # functionality added in Python 3.10
        # https://setuptools.pypa.io/en/latest/userguide/datafiles.html#accessing-data-files-at-runtime
        "importlib-resources",
        "numpy",
        "pandas",
        # Force patch for CVE-2022-1941
        # https://github.com/huggingface/optimum/issues/733
        "protobuf == 3.20.3",
        "uvicorn",
        "starlette_exporter",
        "py-grpc-prometheus",
        "uvloop;" + env_marker_cpython,
        "aiokafka",
        "tritonclient[http]>=2.24",
        "aiofiles",
        "orjson",
    ],
    entry_points={"console_scripts": ["mlserver=mlserver.cli:main"]},
    long_description=_load_description(),
    long_description_content_type="text/markdown",
    license="Apache 2.0",
)
