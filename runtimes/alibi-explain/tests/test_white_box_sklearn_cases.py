from typing import Tuple, Optional

from pathlib import Path
import numpy as np
import alibi
from alibi.api.interfaces import Explainer

from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver.settings import ModelSettings, ModelParameters
from mlserver.codecs import NumpyCodec
from mlserver_alibi_explain import AlibiExplainRuntime
from mlserver_alibi_explain.common import AlibiExplainSettings
from .helpers.sk_model import get_sk_income_model_uri


def case_tree_shap(sk_income_model, income_data, tmp_path) \
        -> Tuple[ModelSettings, Explainer, InferenceRequest]:
    # Explainer
    explainer = train_explainer(
        'TreeShap',
        tmp_path,
        fit=True,
        predictor=sk_income_model,
        feature_names=income_data['feature_names'],
        model_output='raw',
        task='classification',
    )

    # Explainer model settings
    model_settings = ModelSettings(
        name="foo",
        implementation=AlibiExplainRuntime,
        parameters=ModelParameters(
            uri=str(tmp_path),
            extra=AlibiExplainSettings(
                explainer_type="tree_shap",
                infer_uri=str(get_sk_income_model_uri()),
            )
        ),
    )

    # Inference request
    inference_request = build_request(income_data['X'][:1])
    return model_settings, explainer, inference_request


def case_tree_partial_dependence(sk_income_model, income_data, tmp_path) \
        -> Tuple[ModelSettings, Explainer, InferenceRequest]:
    # Explainer
    explainer = train_explainer(
        'TreePartialDependence',
        tmp_path,
        predictor=sk_income_model,
        feature_names=income_data['feature_names'],
        categorical_names=income_data['category_map'],
        target_names=income_data['target_names'],
    )

    # Explainer model settings
    model_settings = ModelSettings(
        name="foo",
        implementation=AlibiExplainRuntime,
        parameters=ModelParameters(
            uri=str(tmp_path),
            extra=AlibiExplainSettings(
                explainer_type="tree_partial_dependence",
                infer_uri=str(get_sk_income_model_uri()),
            )
        ),
    )

    # Inference request
    inference_request = build_request(income_data['X'][:1])
    return model_settings, explainer, inference_request


# TODO - Skip PartialDependenceVariance for now since it cannot be saved.
#  See https://github.com/SeldonIO/alibi/issues/938
#def case_tree_partial_dependence_variance(sk_income_model, income_data, tmp_path) \
#        -> Tuple[ModelSettings, Explainer, InferenceRequest]:
#    # Explainer
#    explainer = train_explainer(
#        'PartialDependenceVariance',
#        tmp_path,
#        predictor=sk_income_model,
#        feature_names=income_data['feature_names'],
#        categorical_names=income_data['category_map'],
#        target_names=income_data['target_names'],
#    )
#
#    # Explainer model settings
#    model_settings = ModelSettings(
#        name="foo",
#        implementation=AlibiExplainRuntime,
#        parameters=ModelParameters(
#            uri=str(tmp_path),
#            extra=AlibiExplainSettings(
#                explainer_type="tree_partial_dependence_variance",
#                infer_uri=str(get_sk_income_model_uri()),
#            )
#        ),
#    )
#
#    # Inference request
#    inference_request = build_request(income_data['X'][:1])
#    return model_settings, explainer, inference_request


def train_explainer(
        explainer_name: str,
        save_dir: Path,
        fit: bool = False,
        X: Optional[np.ndarray] = None,
        *args,
        **kwargs
        ) -> Explainer:
    # Instantiate explainer
    klass = getattr(alibi.explainers, explainer_name)
    explainer = klass(*args, **kwargs)

    # Fit explainer
    if fit:
        explainer.fit() if X is None else explainer.fit(X)

    # Save explainer
    explainer.save(save_dir)

    return explainer


def build_request(data: np.ndarray) -> InferenceRequest:  # TODO - add explainer kwarg's etc
    inference_request = InferenceRequest(
        parameters=Parameters(content_type=NumpyCodec.ContentType),
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
