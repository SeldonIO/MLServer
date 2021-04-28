from sklearn.dummy import DummyClassifier
from mlflow.pyfunc import PyFuncModel

from mlserver_mlflow import MLflowRuntime


def test_load(runtime: MLflowRuntime):
    assert runtime.ready

    assert type(runtime._model) == PyFuncModel
