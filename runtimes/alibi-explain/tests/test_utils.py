import pytest

from mlserver_alibi_explain.common import import_and_get_class
from mlserver_alibi_explain.alibi_dependency_reference import _TAG_TO_RT_IMPL


@pytest.mark.parametrize("explainer_reference", _TAG_TO_RT_IMPL.values())
def test_can_load_runtime_impl(explainer_reference):
    import_and_get_class(explainer_reference.runtime_class)
    import_and_get_class(explainer_reference.alibi_class)
