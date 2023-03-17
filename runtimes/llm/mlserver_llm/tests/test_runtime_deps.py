import pytest

from mlserver_llm.dependency_reference import import_and_get_class, _TAG_TO_RT_IMPL


@pytest.mark.parametrize("runtime_reference", _TAG_TO_RT_IMPL.values())
def test_can_load_runtime_impl(runtime_reference):
    import_and_get_class(runtime_reference.runtime_class)
