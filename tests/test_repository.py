import pytest

from mlserver.errors import ModelNotFound


@pytest.mark.parametrize(
    "name, version", [("sum-model", "v0"), ("sum-model-2", "v0"), ("sum-model", "v2")]
)
def test_get_model_not_found(model_repository, name, version):
    with pytest.raises(ModelNotFound) as err:
        model_repository.get_model(name, version)

        assert err.message == f"Model {name} with version {version} not found"


def test_get_model(model_repository, sum_model):
    found_model = model_repository.get_model(sum_model.name, sum_model.version)
    assert found_model == sum_model
