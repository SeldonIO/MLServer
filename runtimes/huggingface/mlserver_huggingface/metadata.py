from typing import Dict, List
from mlserver.types import MetadataTensor

METADATA: Dict[str, Dict[str, List[MetadataTensor]]] = {
    "audio-classification": dict(
        inputs=[
            # file path inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
            # file content bytes inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="base64"),
            ),
            # numpy.ndarray inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="FP32",
                parameters=dict(content_type="nplist"),
            ),
        ],
        outputs=[
            MetadataTensor(
                name="output_*",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="hg_json"),
            ),
        ],
    ),
    "automatic-speech-recognition": dict(
        inputs=[
            # file path inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
            # file content bytes inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="base64"),
            ),
            # numpy.ndarray inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="FP32",
                parameters=dict(content_type="nplist"),
            ),
        ],
        outputs=[
            MetadataTensor(
                name="output_*",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="hg_json"),
            ),
        ],
    ),
    "feature-extraction": dict(
        inputs=[
            MetadataTensor(
                name="args",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
        ],
        outputs=[
            MetadataTensor(
                name="outputs",
                shape=[-1],
                datatype="FP64",
                parameters=dict(content_type="pd"),
            ),
        ],
    ),
    "text-classification": dict(
        inputs=[
            MetadataTensor(
                name="args",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
        ],
        outputs=[
            MetadataTensor(
                name="outputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="hg_json"),
            ),
        ],
    ),
    "token-classification": dict(
        inputs=[
            MetadataTensor(
                name="args",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
        ],
        outputs=[],
    ),
    "question-answering": dict(
        inputs=[
            MetadataTensor(
                name="context",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
            MetadataTensor(
                name="question",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
        ],
        outputs=[],
    ),
    "table-question-answering": dict(
        inputs=[
            MetadataTensor(
                name="array_inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="hg_jsonlist"),
            ),
        ],
        outputs=[],
    ),
    "visual-question-answering": dict(
        inputs=[
            MetadataTensor(
                name="array_inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="hg_jsonlist"),
            ),
        ],
        outputs=[],
    ),
    "fill-mask": dict(
        inputs=[
            MetadataTensor(
                name="array_inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
        ],
        outputs=[],
    ),
    "summarization": dict(
        inputs=[
            MetadataTensor(
                name="array_inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
        ],
        outputs=[],
    ),
    "translation": dict(
        inputs=[
            MetadataTensor(
                name="array_inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
        ],
        outputs=[],
    ),
    "text2text-generation": dict(
        inputs=[
            MetadataTensor(
                name="array_inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
        ],
        outputs=[],
    ),
    "text-generation": dict(
        inputs=[
            MetadataTensor(
                name="array_inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
        ],
        outputs=[],
    ),
    "zero-shot-classification": dict(
        inputs=[
            MetadataTensor(
                name="array_inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
            MetadataTensor(
                name="candidate_labels",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
        ],
        outputs=[],
    ),
    "zero-shot-image-classification": dict(
        inputs=[
            # file path inputs
            MetadataTensor(
                name="array_inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
            # file content bytes inputs
            MetadataTensor(
                name="array_inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="base64"),
            ),
            # numpy.ndarray inputs
            MetadataTensor(
                name="array_inputs",
                shape=[-1],
                datatype="FP32",
                parameters=dict(content_type="nplist"),
            ),
            MetadataTensor(
                name="candidate_labels",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
        ],
        outputs=[],
    ),
    "conversational": dict(
        inputs=[
            MetadataTensor(
                name="array_inputs",
                shape=[-1],
                datatype="FP32",
                parameters=dict(content_type="hg_conversation"),
            ),
        ],
        outputs=[],
    ),
    "image-classification": dict(
        inputs=[
            # file path inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
            # file content bytes inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="base64"),
            ),
            # pillow image  inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="pillow_image"),
            ),
        ],
        outputs=[],
    ),
    "image-segmentation": dict(
        inputs=[
            # file path inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
            # file content bytes inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="base64"),
            ),
            # pillow image  inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="pillow_image"),
            ),
        ],
        outputs=[],
    ),
    "object-detection": dict(
        inputs=[
            # file path inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="str"),
            ),
            # file content bytes inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="base64"),
            ),
            # pillow image  inputs
            MetadataTensor(
                name="inputs",
                shape=[-1],
                datatype="BYTES",
                parameters=dict(content_type="pillow_image"),
            ),
        ],
        outputs=[],
    ),
}
