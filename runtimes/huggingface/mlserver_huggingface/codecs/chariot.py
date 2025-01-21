import numpy as np

def is_list_of_dicts(var):
    '''Check if a variable is a list of dicts'''
    if not isinstance(var, list):
        return False
    for item in var:
        if not isinstance(item, dict):
            return False
    return True
def get_det_dict_from_hf_obj_detect(obj_detect):
    '''Convert hf object detection output to standard chariot object detection output'''
    det_dict = {
        "num_detections": 0,
        "detection_classes": [],
        "detection_boxes": [],
        "detection_scores": [],
    }
    for det in obj_detect:
        conf, cls = det["score"],det["label"]
        x1, y1, x2, y2  = det["box"]["xmin"],det["box"]["ymin"],det["box"]["xmax"],det["box"]["ymax"]
        det_dict["num_detections"] += 1
        det_dict["detection_classes"].append(cls)
        det_dict["detection_scores"].append(conf)
        det_dict["detection_boxes"].append([x1, y1, x2, y2])
    return det_dict
def get_chariot_seg_mask_from_hf_seg_output(seg_pred,class_int_to_str):
    '''Convert hf segmentation output to standard chariot segmentation output'''
    img_w,img_h = seg_pred[0]["mask"].size
    if class_int_to_str[0]!="background":
        # Let class_int 0 be background and increment all the other class_int by 1
        class_str_to_int = {v:k+1 for k,v in class_int_to_str.items()}
    else:
        class_str_to_int = {v:k for k,v in class_int_to_str.items()}
    # Create an empty mask
    combined_mask = np.zeros((img_h, img_w), dtype=np.uint8)
    for i in seg_pred:
        # Convert mask from PIL image to numpy array
        mask = np.array(i["mask"])
        class_str = i["label"]
        class_int = class_str_to_int[class_str] 
        combined_mask[np.where(mask>0)]=class_int
    predictions= [combined_mask]
    return predictions
        
    
class ChariotImgModelOutputCodec():
    """Encoder that converts HF model output to the standard Chariot model output 
    """
    @classmethod
    def encode_output(cls, predictions,task_type,pipeline):
        if task_type == "image-classification":
            if all([is_list_of_dicts(p) for p in predictions]):
                # get Top-1 predicted class
                # convert HF output: [[{"label": "tabby, tabby cat", "score": 0.94}, 
                #                      {"label": "tiger cat", "score": 0.04},
                #                      {"label": "Egyptian cat", "score": 0.02}]]
                # to standard Chariot output: ["tabby, tabby cat"]
                predictions = [p[0]["label"] for p in predictions]
        
        elif task_type == "object-detection":
            if is_list_of_dicts(predictions):
                # convert HF output: [{'score': 0.9897010326385498,
                #                       'label': 'cat',
                #                       'box': {'xmin': 53, 'ymin': 313, 'xmax': 697, 'ymax': 986}},
                #                       {'score': 0.9896764159202576,
                #                       'label': 'cat',
                #                       'box': {'xmin': 974, 'ymin': 221, 'xmax': 1526, 'ymax': 1071}}]

                # to standard Chariot output: [{"num_detections":2,
                #                             "detection_classes":["cat","cat"],
                #                             "detection_scores":[0.9897010326385498,0.9896764159202576],
                #                             "detection_boxes":[[53,313,697,986],
                #                                                [974,221,1526,1071]]}]
                predictions = get_det_dict_from_hf_obj_detect(predictions) 
        
        elif task_type == "image-segmentation":
            if is_list_of_dicts(predictions):
                    # convert HF output: [{"score": None,
                    #                      "label": "wall",
                    #                      "mask": <PIL.Image.Image image mode=L size=5362x3016>},
                    #                     {"score": None,
                    #                      "label": "floor",
                    #                      "mask": <PIL.Image.Image image mode=L size=5362x3016>}]

                    # to standard Chariot output: [[0,0,...,0],...,[0,0,0,...,0]] 
                    # 2d array with size of the original image. Each pixel is a class int
                    # Background uses class_int 0 
                    class_int_to_str=pipeline.model.config.id2label
                    predictions = get_chariot_seg_mask_from_hf_seg_output(predictions,class_int_to_str) 
        return predictions
    
