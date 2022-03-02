import pytest
from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import RequestInput, InferenceRequest
from mlserver.codecs import CodecError
from mlserver_alibi_detect import AlibiDetectRuntime
from alibi_detect.od import OutlierVAE
from alibi_detect.utils.saving import save_detector
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, InputLayer

tf.keras.backend.clear_session()

X_REF_THRESHOLD = 0.05


@pytest.fixture
def alibi_detect_tabular_outlier_model_settings(
    alibi_detect_tabular_outlier_model_uri: str,
) -> ModelSettings:
    return ModelSettings(
        name="alibi-detect-model",
        parameters=ModelParameters(
            uri=alibi_detect_tabular_outlier_model_uri,
            version="v1.2.3",
            extra={
                "predict_parameters": {
                    "outlier_type": "instance",
                    "return_feature_score": False,
                    "return_instance_score": True,
                }
            },
        ),
    )


@pytest.fixture
def alibi_detect_tabular_outlier_model_uri(tmp_path) -> str:
    X_ref = np.array([[1, 2, 3]])
    n_features = X_ref.shape[1]
    latent_dim = 2
    encoder_net = tf.keras.Sequential(
        [
            InputLayer(input_shape=(n_features,)),
            Dense(25, activation=tf.nn.relu),
            Dense(10, activation=tf.nn.relu),
            Dense(5, activation=tf.nn.relu),
        ]
    )

    decoder_net = tf.keras.Sequential(
        [
            InputLayer(input_shape=(latent_dim,)),
            Dense(5, activation=tf.nn.relu),
            Dense(10, activation=tf.nn.relu),
            Dense(25, activation=tf.nn.relu),
            Dense(n_features, activation=None),
        ]
    )

    od = OutlierVAE(
        threshold=X_REF_THRESHOLD,
        score_type="mse",
        encoder_net=encoder_net,
        decoder_net=decoder_net,
        latent_dim=latent_dim,
        samples=5,
    )

    od.fit(X_ref, loss_fn=tf.keras.losses.mse, epochs=5, verbose=True)

    detector_uri = os.path.join(tmp_path, "alibi-detector-artifacts")
    save_detector(od, detector_uri)

    return detector_uri


@pytest.fixture
async def alibi_detect_tabular_outlier_model(
    alibi_detect_tabular_outlier_model_settings: ModelSettings,
) -> AlibiDetectRuntime:
    model = AlibiDetectRuntime(alibi_detect_tabular_outlier_model_settings)
    await model.load()

    return model


async def test_load_folder(
    alibi_detect_tabular_outlier_model_uri: str,
    alibi_detect_tabular_outlier_model_settings: ModelSettings,
):

    alibi_detect_tabular_outlier_model_settings.parameters.uri = (  # type: ignore
        alibi_detect_tabular_outlier_model_uri
    )

    model = AlibiDetectRuntime(alibi_detect_tabular_outlier_model_settings)
    await model.load()

    assert model.ready
    assert type(model._model) == OutlierVAE


async def test_predict(
    alibi_detect_tabular_outlier_model: AlibiDetectRuntime,
    inference_request: InferenceRequest,
    alibi_detect_tabular_outlier_model_settings: ModelSettings,
):
    response = await alibi_detect_tabular_outlier_model.predict(inference_request)

    assert len(response.outputs) == 3
    assert response.outputs[0].name == "instance_score"
    assert response.outputs[1].name == "feature_score"
    assert response.outputs[2].name == "is_outlier"
    assert response.outputs[2].shape == [1, 1]


async def test_multiple_inputs_error(
    alibi_detect_tabular_outlier_model: AlibiDetectRuntime,
    inference_request: InferenceRequest,
    alibi_detect_tabular_outlier_model_settings: ModelSettings,
):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[1, 3], data=[[0, 1, 6]], datatype="FP32")
    )

    with pytest.raises(CodecError):
        await alibi_detect_tabular_outlier_model.predict(inference_request)
