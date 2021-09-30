import pytest

from mlserver_alibi_explain.common import _TAG_TO_RT_IMPL, import_and_get_class


@pytest.mark.parametrize("rt_class_str, alibi_class_str", _TAG_TO_RT_IMPL.values())
def test_can_load_runtime_impl(rt_class_str, alibi_class_str):
    import_and_get_class(rt_class_str)
    import_and_get_class(alibi_class_str)
