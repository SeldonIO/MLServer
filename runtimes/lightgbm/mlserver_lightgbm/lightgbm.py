import lightgbm as lgb

from mlserver import types
from mlserver.model import MLModel
from mlserver.utils import get_model_uri
from mlserver.codecs import NumpyCodec, NumpyRequestCodec

from bigdl.ppml.ppml_context import *
from bigdl.ppml.kms.utils.kms_argument_parser import KmsArgumentParser
from pyspark import SparkConf

WELLKNOWN_MODEL_FILENAMES = ["model.bst"]


class LightGBMModel(MLModel):
    """
    Implementationof the MLModel interface to load and serve `lightgbm` models.
    """

    async def load(self) -> bool:
        model_uri = await get_model_uri(
            self._settings, wellknown_filenames=WELLKNOWN_MODEL_FILENAMES
        )

        # init a PPMLContext instance
        args = KmsArgumentParser().get_arg_dict()
        conf = SparkConf().set("spark.driver.host", "127.0.0.1")
        sc = PPMLContext(app_name='mlserver-lightgbm-serving',\
                ppml_args=args, spark_conf=conf)

        # use PPMLContext to load encrypted/plaintext lightgbm model
        self._model = sc.loadLightGBMClassificationModel(\
                model_path=model_uri, crypto_mode=args["input_encrypt_mode"])

        return True

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        decoded = self.decode_request(payload, default_codec=NumpyRequestCodec)
        prediction = self._model.predict(decoded)

        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[NumpyCodec.encode_output(name="predict", payload=prediction)],
        )
