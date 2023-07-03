from typing import Union, Literal, Optional, Tuple
from pathlib import Path
import numpy as np

from alibi.api.interfaces import Explainer

from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver.codecs import NumpyCodec
from mlserver.settings import ModelSettings, ModelParameters
from mlserver_alibi_explain import AlibiExplainRuntime
from mlserver_alibi_explain.common import AlibiExplainSettings, import_and_get_class
from mlserver_alibi_explain.alibi_dependency_reference import get_alibi_class_as_str
from .sk_model import get_sk_income_model_uri


def train_explainer(
        explainer_tag: str,
        save_dir: Optional[Path],
        fit: Union[np.ndarray, Literal[False, 'no-data']] = False,
        *args,
        **kwargs
        ) -> Explainer:
    """
    Train and save an explainer.
    """
    # Instantiate explainer
    klass = import_and_get_class(get_alibi_class_as_str(explainer_tag))
    explainer = klass(*args, **kwargs)

    # Fit explainer
    if fit:
        explainer.fit() if fit == 'no-data' else explainer.fit(fit)

    # Save explainer
    if save_dir:
        explainer.save(save_dir)

    return explainer


def build_request(data: np.ndarray, **explain_kwargs) -> InferenceRequest:
    """
    Build an inference request from a numpy array.
    """
    inference_request = InferenceRequest(
        parameters=Parameters(
            content_type=NumpyCodec.ContentType,
            explain_parameters=explain_kwargs,
        ),
        inputs=[
            RequestInput(
                name="predict",
                shape=data.shape,
                data=data.tolist(),
                datatype="FP32",
            )
        ],
    )
    return inference_request


def build_test_case(explainer_type: str, init_kwargs: dict, explain_kwargs: dict,
               fit: Union[np.ndarray, Literal[False, 'no-data']], save_dir: Optional[Path], payload: np.ndarray) \
        -> Tuple[ModelSettings, Explainer, InferenceRequest, dict]:
    """
    Function to build a test case for a given explainer type. The function returns a model settings object, an
    explainer object, an inference request object and a dictionary of explain parameters.

    Parameters
    ----------
    explainer_type
        The type of explainer to build.
    init_kwargs
        Instantiation kwargs for the explainer.
    explain_kwargs
        Explain kwargs for the explainer.
    fit
        Data to fit the explainer on, `False` if no fit is required, or `'no-data'` to fit the explainer without
         data e.g. for `TreeShap` with path-dependent algorithm.
    save_dir
        Directory to save the explainer to, and then pass to `uri` in `ModelParameters`. If `None`, the explainer
        will not be saved to disk, and `init_parameters` will specified in `ModelSettings` instead.
    payload
        The payload to send as request to the explainer.
    """
    # Build explainer
    explainer = train_explainer(
        explainer_type,
        save_dir,
        fit=fit,
        **init_kwargs
    )

    # Explainer model settings
    model_settings = ModelSettings(
        name="foo",
        implementation=AlibiExplainRuntime,
        parameters=ModelParameters(
            uri=str(save_dir),
            extra=AlibiExplainSettings(
                explainer_type=explainer_type,
                infer_uri=str(get_sk_income_model_uri()),
            )
        ),
    )

    # Inference request
    inference_request = build_request(payload, **explain_kwargs)
    return model_settings, explainer, inference_request, explain_kwargs
