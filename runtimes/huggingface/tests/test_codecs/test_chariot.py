import pytest
from mlserver_huggingface.codecs import ChariotImgModelOutputCodec
from PIL import Image
import numpy as np


@pytest.mark.parametrize(
    "task_type,class_int_to_str, hf_prediction,expected_chariot_output",
    [
        (
            "image-classification",
            None,
            [
                [
                    {"label": "tabby, tabby cat", "score": 0.94},
                    {"label": "tiger cat", "score": 0.04},
                    {"label": "Egyptian cat", "score": 0.02},
                ]
            ],
            ["tabby, tabby cat"],
        ),
        (
            "object-detection",
            None,
            [
                {
                    "score": 0.9897010326385498,
                    "label": "cat",
                    "box": {"xmin": 53, "ymin": 313, "xmax": 697, "ymax": 986},
                },
                {
                    "score": 0.9896764159202576,
                    "label": "cat",
                    "box": {"xmin": 974, "ymin": 221, "xmax": 1526, "ymax": 1071},
                },
            ],
            {
                "num_detections": 2,
                "detection_classes": ["cat", "cat"],
                "detection_scores": [0.9897010326385498, 0.9896764159202576],
                "detection_boxes": [[53, 313, 697, 986], [974, 221, 1526, 1071]],
            },
        ),
        (
            "image-segmentation",
            {0: "class_a", 1: "class_b"},
            [
                {
                    "score": None,
                    "label": "class_a",
                    "mask": Image.fromarray(
                        np.array([[0, 0, 0], [0, 255, 255], [0, 0, 0]]).astype("uint8"),
                        mode="L",
                    ),
                },
                {
                    "score": None,
                    "label": "class_b",
                    "mask": Image.fromarray(
                        np.array([[0, 0, 0], [0, 0, 0], [0, 255, 0]]).astype("uint8"),
                        mode="L",
                    ),
                },
            ],
            [[[0, 0, 0], [0, 1, 1], [0, 2, 0]]],
        ),
    ],
)
def test_encode_input(
    task_type, class_int_to_str, hf_prediction, expected_chariot_output
):
    chariot_output = ChariotImgModelOutputCodec.encode_output(
        hf_prediction, task_type, class_int_to_str
    )
    assert chariot_output == expected_chariot_output
