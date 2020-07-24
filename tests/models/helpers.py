import pytest

from mlserver.models.sklearn import _SKLEARN_PRESENT

skipif_sklearn_missing = pytest.mark.skipif(
    not _SKLEARN_PRESENT, reason="tensorflow is not present"
)
