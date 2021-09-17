from enum import Enum

#from mlserver_alibi_explain.explainers.anchor_image import AnchorImageWrapper
#from mlserver import MLModel

_ANCHOR_IMAGE_TAG = 'anchor_image'


class ExplainerEnum(str, Enum):
    anchor_image = _ANCHOR_IMAGE_TAG


# _TAG_TO_IMPL = {
#     _ANCHOR_IMAGE_TAG: type(AnchorImageWrapper)
# }
#
#
# def get_mlmodel_class(tag: ExplainerEnum) -> type(MLModel):
#     return _TAG_TO_IMPL[tag.value]


ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS = "MLSERVER_MODEL_ALIBI_EXPLAIN_"