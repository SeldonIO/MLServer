import orjson

from functools import lru_cache
from typing import Optional, Tuple
from importlib_resources import files

MODEL_NAME_PARAMETER = "model_name"
MODEL_VERSION_PARAMETER = "model_version"


@lru_cache
def get_openapi_schema() -> dict:
    openapi_schema_path = files(__package__).joinpath("dataplane.json")
    return orjson.loads(openapi_schema_path.read_bytes())


def get_model_schema_uri(model_name: str, model_version: Optional[str]) -> str:
    base = f"/v2/models/{model_name}"
    if model_version:
        base = f"{base}/versions/{model_version}"

    return f"{base}/docs/dataplane.json"


@lru_cache
def get_model_schema(model_name: str, model_version: Optional[str]) -> dict:
    openapi_schema = get_openapi_schema()
    generic_paths = openapi_schema["paths"]
    model_paths = {}

    for path_spec in generic_paths.items():
        filled_path_spec = _fill_path_spec(path_spec, model_name, model_version)
        if filled_path_spec:
            model_path, model_spec = filled_path_spec
            model_paths[model_path] = model_spec

    model_schema = openapi_schema.copy()
    model_schema["info"] = _get_model_info(openapi_schema, model_name, model_version)
    model_schema["paths"] = model_paths
    return model_schema


def _get_model_info(
    openapi_schema: dict, model_name: str, model_version: Optional[str]
) -> dict:
    model_title = f"Model {model_name}"
    if model_version:
        model_title = f"{model_title} ({model_version})"

    title = f"Data Plane for {model_title}"
    description = f"REST protocol to interact with {model_title}"

    model_info = openapi_schema["info"].copy()
    model_info["title"] = title
    model_info["description"] = description

    return model_info


def _fill_path_spec(path_spec, model_name, model_version) -> Optional[Tuple[str, dict]]:
    path, spec = path_spec

    model_name_placeholder = f"{{{MODEL_NAME_PARAMETER}}}"
    if model_name_placeholder not in path:
        # If this is not a model endpoint, don't include it
        return None

    model_path = path.replace(model_name_placeholder, model_name)

    model_version_placeholder = f"{{{MODEL_VERSION_PARAMETER}}}"
    if model_version:
        if model_version_placeholder not in model_path:
            # If this is a model endpoint, but it has no version, then it
            # refers to the default.
            # Therefore, it can't be included in the schema for a versioned
            # model.
            return None

        model_path = model_path.replace(model_version_placeholder, model_version)

    model_spec = spec.copy()
    parameters = spec.get("parameters", [])
    model_spec["parameters"] = _remove_prefilled_parameters(
        parameters, model_name, model_version
    )

    return (model_path, model_spec)


def _remove_prefilled_parameters(
    parameters: list, model_name: str, model_version: Optional[str]
) -> list:
    filtered_parameters = []

    prefilled_parameter_names = [MODEL_NAME_PARAMETER]
    if model_version:
        prefilled_parameter_names.append(MODEL_VERSION_PARAMETER)

    for parameter in parameters:
        if parameter["name"] not in prefilled_parameter_names:
            filtered_parameters.append(parameter)

    return filtered_parameters
