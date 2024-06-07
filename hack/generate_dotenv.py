#!/usr/bin/env python
"""
This script will read the `settings.json` and `model-settings.json` on a given
folder and will export them as environment variables.

This is used when building custom Docker images, which may have a default set
of settings that we want to source always (e.g. the default runtime to use).
"""

import click
import json
from json import JSONDecodeError
import os

from typing import List, Tuple, Type
from pydantic_settings import BaseSettings

from mlserver.settings import Settings, ModelSettings, ModelParameters
from mlserver.cli.serve import DEFAULT_SETTINGS_FILENAME
from mlserver.repository import DEFAULT_MODEL_SETTINGS_FILENAME


def load_default_settings(folder: str) -> List[Tuple[Type[BaseSettings], dict]]:
    default_settings = []

    settings_path = os.path.join(folder, DEFAULT_SETTINGS_FILENAME)
    if os.path.isfile(settings_path):
        default_settings.append((Settings, _read_json_file(settings_path)))

    model_parameters = None
    model_settings_path = os.path.join(folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    if os.path.isfile(model_settings_path):
        raw_defaults = _read_json_file(model_settings_path)
        model_parameters = raw_defaults.pop("parameters", None)
        default_settings.append((ModelSettings, raw_defaults))

    if model_parameters:
        default_settings.append((ModelParameters, model_parameters))

    return default_settings


def _read_json_file(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return json.load(file)


def get_default_env(default_settings: List[Tuple[Type[BaseSettings], dict]]) -> dict:
    env = {}
    for settings_class, raw_defaults in default_settings:
        env.update(_convert_to_env(settings_class, raw_defaults))

    return env


def _convert_to_env(settings_class: Type[BaseSettings], raw_defaults: dict) -> dict:
    env = {}

    env_prefix = _get_env_prefix(settings_class)
    for field_name, field_value in raw_defaults.items():
        env_var_name = env_prefix + field_name.upper()
        env[env_var_name] = str(field_value)

    return env


def _get_env_prefix(settings_class: Type[BaseSettings]) -> str:
    if not hasattr(settings_class, "Config"):
        return ""

    config = settings_class.Config
    return getattr(config, "env_prefix", "")


def save_default_env(env: dict, output: str):
    with open(output, "w") as file:
        for name, value in env.items():
            file.write(_parse_dict_values(name, value))


def _parse_dict_values(name: str, value: str) -> str:
    try:
        value = value.replace("'", '"')
        json.loads(value)
        return f"{name}='{value}'\n"
    except JSONDecodeError:
        # If not JSON, then assume it's a plain string
        return f'{name}="{value}"\n'


@click.command()
@click.argument("folder", nargs=1)
@click.argument("output", nargs=1)
def main(folder: str, output: str):
    default_settings = load_default_settings(folder)
    default_env = get_default_env(default_settings)
    save_default_env(default_env, output)


if __name__ == "__main__":
    main()
