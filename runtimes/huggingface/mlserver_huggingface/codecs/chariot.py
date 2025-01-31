import numpy as np
import json

def is_list_of_dicts(var):
    """Check if a variable is a list of dicts"""
    if not isinstance(var, list):
        return False
    for item in var:
        if not isinstance(item, dict):
            return False
    return True


def get_det_dict_from_hf_obj_detect(obj_detect):
    """Convert hf object detection output to standard chariot object detection output"""
    det_dict = {
        "num_detections": 0,
        "detection_classes": [],
        "detection_boxes": [],
        "detection_scores": [],
    }
    for det in obj_detect:
        conf, cls = det["score"], det["label"]
        y1, x1, y2, x2 = (
            det["box"]["ymin"],
            det["box"]["xmin"],
            det["box"]["ymax"],
            det["box"]["xmax"],
        )
        det_dict["num_detections"] += 1
        det_dict["detection_classes"].append(cls)
        det_dict["detection_scores"].append(conf)
        det_dict["detection_boxes"].append([y1, x1, y2, x2])
    return det_dict


def get_chariot_seg_mask_from_hf_seg_output(seg_pred, class_int_to_str):
    """Convert hf segmentation output to standard chariot segmentation output"""
    mask_shape = np.array(seg_pred[0]["mask"]).shape
    class_str_to_int = {v: k for k, v in class_int_to_str.items()}
    # Create an empty mask
    combined_mask = np.full(mask_shape, None)
    for i in seg_pred:
        # Convert mask from PIL image to numpy array
        mask = np.array(i["mask"])
        class_str = i["label"]
        class_int = class_str_to_int[class_str]
        combined_mask[np.where(mask > 0)] = class_int
    predictions = combined_mask.tolist()
    return predictions


class ChariotImgModelOutputCodec:
    """Encoder that converts HF model output to the standard Chariot model output"""

    @classmethod
    def encode_output(
        cls, predictions, task_type, class_int_to_str, predict_proba=False
    ):
        if is_list_of_dicts(predictions):
            predictions = [predictions]
        if task_type == "image-classification":

            if predict_proba:
                # class_int_to_str: {0:"Egyptian cat",
                #                    1:"tabby, tabby cat",
                #                    2:"tiger cat"}
                # convert HF output: [[{"label": "tabby, tabby cat", "score": 0.94},
                #                      {"label": "tiger cat", "score"': 0.04},
                #                      {"label": "Egyptian cat", "score": 0.02}]]
                # to standard Chariot probability output: [[0.02,0.94,0.04]]
                # The probability scores are ordered by class id
                num_labels = len(class_int_to_str)
                class_to_proba = [
                    {d["label"]: d["score"] for d in p} for p in predictions
                ]
                predictions = [
                    [d.get(class_int_to_str[i]) for i in range(num_labels)]
                    for d in class_to_proba
                ]
            else:
                # get Top-1 predicted class
                # convert HF output: [[{"label": "tabby, tabby cat", "score": 0.94},
                #                      {"label": "tiger cat", "score": 0.04},
                #                      {"label": "Egyptian cat", "score": 0.02}]]
                # to standard Chariot output: ['"tabby, tabby cat"']
                predictions = [json.dumps(p[0]["label"]) for p in predictions]
        elif task_type == "object-detection":

            # convert HF output: [[{"score": 0.9897010326385498,
            #                       "label": 'cat',
            #                       "box": {"xmin": 53, "ymin": 313,
            #                               "xmax": 697, "ymax": 986}},
            #                       {"score": 0.9896764159202576,
            #                       "label": "cat",
            #                       "box": {"xmin": 974, "ymin": 221,
            #                               "xmax": 1526, "ymax": 1071}}]]

            # to standard Chariot output: [{"num_detections":2,
            #                             "detection_classes":["cat","cat"],
            #                             "detection_scores":[0.9897010326385498,0.9896764159202576],
            #                             "detection_boxes":[[313,53,986,697],
            #                                                [221,974,1071,1562]]}]
            predictions = [get_det_dict_from_hf_obj_detect(p) for p in predictions]

        elif task_type == "image-segmentation":

            # convert HF output: [[{"score": None,
            #                      "label": "wall",
            #                      "mask": <PIL.Image.Image>},
            #                     {"score": None,
            #                      "label": "floor",
            #                      "mask": <PIL.Image.Image>}]]
            # to standard Chariot output: [[[0,0,...,0],...,[0,0,0,...,0]]]
            # 2d array with size of the original image. Each pixel is a class int
            # Background uses class_int 0
            predictions = [
                get_chariot_seg_mask_from_hf_seg_output(p, class_int_to_str)
                for p in predictions
            ]
        return predictions
