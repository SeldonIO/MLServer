from .sklearn import SKLearnModel
from .xgboost import XGBoostModel

_NUMPY_PRESENT = False

try:
    import numpy  # noqa

    _NUMPY_PRESENT = True
except ImportError:
    # TODO: Log warning message
    pass

__all__ = ["SKLearnModel", "XGBoostModel", "_NUMPY_PRESENT"]
