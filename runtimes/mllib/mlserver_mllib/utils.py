from mlserver import ModelSettings
from .errors import InvalidMLlibFormat
from pyspark.mllib.classification import (
    LogisticRegressionModel,
    NaiveBayesModel,
    SVMModel,
)
from pyspark.mllib.clustering import KMeansModel
from pyspark.mllib.regression import (
    IsotonicRegressionModel,
    LinearRegressionModel,
    LassoModel,
    RidgeRegressionModel,
)
from pyspark.mllib.tree import (
    DecisionTreeModel,
    GradientBoostedTreesModel,
    RandomForestModel,
)

MODEL_DICT = {
    "LogisticRegression": LogisticRegressionModel.load,
    "NaiveBayes": NaiveBayesModel.load,
    "SVM": SVMModel.load,
    "KMeans": KMeansModel.load,
    "IsotonicRegression": IsotonicRegressionModel.load,
    "LinearRegression": LinearRegressionModel.load,
    "Lasso": LassoModel.load,
    "RidgeRegression": RidgeRegressionModel.load,
    "DecisionTree": DecisionTreeModel.load,
    "GradientBoostedTrees": GradientBoostedTreesModel.load,
    "RandomForest": RandomForestModel.load,
}


async def get_mllib_load(settings: ModelSettings):
    if not settings.parameters:
        raise InvalidMLlibFormat(settings.name)

    mllib_format = settings.parameters.format

    if not mllib_format:
        raise InvalidMLlibFormat(settings.name)

    if mllib_format not in MODEL_DICT:
        raise InvalidMLlibFormat(settings.name)

    return MODEL_DICT[mllib_format]
