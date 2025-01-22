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
                "detection_boxes": [[313, 53, 986, 697], [221, 974, 1071, 1526]],
            },
        ),
        (
            "image-segmentation",
            {0: "class_0", 1: "class_1",2:"class_2"},
            [
                {
                    "score": None,
                    "label": "class_0",
                    "mask": Image.fromarray(
                        np.array([[255, 255, 255], [255, 0, 0], [255, 0, 255]]).astype("uint8"),
                        mode="L",
                    ),
                },
                {
                    "score": None,
                    "label": "class_1",
                    "mask": Image.fromarray(
                        np.array([[0, 0, 0], [0, 255, 255], [0, 0, 0]]).astype("uint8"),
                        mode="L",
                    ),
                },
                {
                    "score": None,
                    "label": "class_2",
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
