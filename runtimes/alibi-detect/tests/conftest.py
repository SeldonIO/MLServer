import pytest
import os
import asyncio
import numpy as np
import tensorflow as tf

from tensorflow.keras.layers import Dense, InputLayer
from alibi_detect.cd import TabularDrift
from alibi_detect.od import OutlierVAE
from alibi_detect.saving import save_detector

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest
from mlserver.utils import install_uvloop_event_loop

from mlserver_alibi_detect import AlibiDetectRuntime

tf.keras.backend.clear_session()

P_VAL_THRESHOLD = 0.05

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


@pytest.fixture
def event_loop():
    # By default use uvloop for tests
    install_uvloop_event_loop()
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def inference_request() -> InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return InferenceRequest.parse_file(payload_path)


@pytest.fixture
def outlier_detector_settings(
    outlier_detector_uri: str,
) -> ModelSettings:
    return ModelSettings(
        name="alibi-detect-model",
        implementation=AlibiDetectRuntime,
        parameters=ModelParameters(
            uri=outlier_detector_uri,
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
def outlier_detector_uri(tmp_path: str) -> str:
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
        threshold=0.05,
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
async def outlier_detector(
    outlier_detector_settings: ModelSettings,
) -> AlibiDetectRuntime:
    model = AlibiDetectRuntime(outlier_detector_settings)
    model.ready = await model.load()

    return model


@pytest.fixture
def drift_detector_settings(
    drift_detector_uri: str,
) -> ModelSettings:
    return ModelSettings(
        name="alibi-detect-model",
        implementation=AlibiDetectRuntime,
        parameters=ModelParameters(
            uri=drift_detector_uri,
            version="v1.2.3",
            extra={"predict_parameters": {"drift_type": "feature"}, "batch_size": 5},
        ),
    )


@pytest.fixture
def drift_detector_uri(tmp_path: str) -> str:
    X_ref = np.array([[1, 2, 3]])

    cd = TabularDrift(X_ref, p_val=P_VAL_THRESHOLD)

    detector_uri = os.path.join(tmp_path, "alibi-detector-artifacts")
    save_detector(cd, detector_uri)

    return detector_uri


@pytest.fixture
async def drift_detector(drift_detector_settings: ModelSettings) -> AlibiDetectRuntime:
    model = AlibiDetectRuntime(drift_detector_settings)
    model.ready = await model.load()

    return model
