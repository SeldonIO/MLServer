import io
import json
from typing import Dict, Any, List
import base64
import numpy as np
from PIL import Image, ImageChops
from transformers.pipelines import Conversation

IMAGE_PREFIX = "data:image/"
DEFAULT_IMAGE_FORMAT = "PNG"


class HuggingfaceJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, Image.Image):
            buf = io.BytesIO()
            if not obj.format:
                obj.format = DEFAULT_IMAGE_FORMAT
            obj.save(buf, format=obj.format)
            return (
                IMAGE_PREFIX
                + obj.format.lower()
                + ";base64,"
                + base64.b64encode(buf.getvalue()).decode()
            )
        elif isinstance(obj, Conversation):
            return {
                "uuid": str(obj.uuid),
                "past_user_inputs": obj.past_user_inputs,
                "generated_responses": obj.generated_responses,
                "new_user_input": obj.new_user_input,
            }
        else:
            return json.JSONEncoder.default(self, obj)


def json_encode(payload: Any, use_bytes: bool = False):
    if use_bytes:
        return json.dumps(payload, cls=HuggingfaceJSONEncoder).encode()
    return json.dumps(payload, cls=HuggingfaceJSONEncoder)


def json_decode(payload):
    raw_dict = json.loads(payload)
    return Convertor.do(raw_dict)


conversation_keys = {
    "uuid",
    "past_user_inputs",
    "generated_responses",
    "new_user_input",
}


class Convertor:
    @classmethod
    def do(cls, raw):
        if isinstance(raw, dict):
            return cls.convert_dict(raw)
        elif isinstance(raw, list):
            return cls.convert_list(raw)
        else:
            return raw

    @classmethod
    def convert_conversation(cls, d: Dict[str, Any]):
        if set(d.keys()) == conversation_keys:
            return Conversation(
                text=d["new_user_input"],
                conversation_id=d["uuid"],
                past_user_inputs=d["past_user_inputs"],
                generated_responses=d["generated_responses"],
            )
        return None

    @classmethod
    def convert_dict(cls, d: Dict[str, Any]):
        conversation = cls.convert_conversation(d)
        if conversation is not None:
            return conversation
        tmp = {}
        for k, v in d.items():
            if isinstance(v, dict):
                if set(v.keys()) == conversation_keys:
                    tmp[k] = Conversation(text=v["new_user_input"])
                else:
                    tmp[k] = cls.convert_dict(v)
            elif isinstance(v, list):
                tmp[k] = cls.convert_list(v)
            elif isinstance(v, str):
                if v.startswith(IMAGE_PREFIX):
                    decoded = base64.b64decode(v.split(",")[1])
                    buf = io.BytesIO(decoded)
                    tmp[k] = Image.open(buf)
                else:
                    tmp[k] = v  # type: ignore
            else:
                tmp[k] = v
        return tmp

    @classmethod
    def convert_list(cls, list_data: List[Any]):
        nl = []
        for el in list_data:
            if isinstance(el, list):
                nl.append(cls.convert_list(el))
            elif isinstance(el, dict):
                nl.append(cls.convert_dict(el))
            else:
                nl.append(el)
        return nl


class EqualUtil:
    def pil_equal(img1: "Image.Image", img2: "Image.Image") -> bool:
        diff = ImageChops.difference(img1, img2)
        if diff.getbbox() is None:
            return True
        return False

    @staticmethod
    def list_equal(list1: List[Any], list2: List[Any]) -> bool:
        if len(list1) != len(list2):
            return False
        for idx, el in enumerate(list1):
            if isinstance(el, dict):
                if not EqualUtil.dict_equal(el, list2[idx]):
                    return False
            elif isinstance(el, list):
                if not EqualUtil.list_equal(el, list2[idx]):
                    return False
            elif isinstance(el, Image.Image):
                if not EqualUtil.pil_equal(el, list2[idx]):
                    return False
            elif isinstance(el, np.ndarray):
                if not np.array_equal(el, list2[idx]):
                    return False
            else:
                if el != list2[idx]:
                    return False
        return True

    @staticmethod
    def dict_equal(dict1: Dict[Any, Any], dict2: Dict[Any, Any]) -> bool:
        if not set(dict1.keys()) == set(dict2.keys()):
            return False
        for k, v in dict1.items():
            if isinstance(v, Image.Image):
                pass
            elif isinstance(v, Image.Image):
                if not EqualUtil.pil_equal(v, dict2[k]):
                    return False
            elif isinstance(v, dict):
                if not EqualUtil.dict_equal(v, dict2[k]):
                    return False
            elif isinstance(v, list):
                if not EqualUtil.list_equal(v, dict2[k]):
                    return False
            elif isinstance(v, np.ndarray):
                if not np.array_equal(v, dict2[k]):
                    return False
            else:
                if v != dict2[k]:
                    return False
        return True
