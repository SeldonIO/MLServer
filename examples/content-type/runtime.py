import io
import json
import numpy as np

from PIL import Image

from mlserver import MLModel
from mlserver.types import (
    InferenceRequest,
    InferenceResponse, 
    RequestInput, 
    ResponseOutput
)
from mlserver.codecs import NumpyCodec, _codec_registry as codecs

class PillowCodec(NumpyCodec):
    ContentType = "img"
    DefaultMode = "L"
    
    def encode(self, name: str, payload: Image) -> ResponseOutput:
        byte_array = io.BytesIO()
        payload.save(byte_array, mode=self.DefaultMode)
        
        return ResponseOutput(
            name=name,
            shape=payload.size,
            datatype="BYTES",
            data=byte_array.getvalue()
        )
    
    def decode(self, request_input: RequestInput) -> Image:
        if request_input.datatype != "BYTES":
            # If not bytes, assume it's an array
            image_array = super().decode(request_input)
            return Image.fromarray(image_array, mode=self.DefaultMode)
        
        encoded = request_input.data.__root__
        if isinstance(encoded, str):
            encoded = encoded.encode()

        return Image.frombytes(
            mode=self.DefaultMode,
            size=request_input.shape,
            data=encoded
        )
    
# Register our new codec so that it's used for payloads with `img` content type
codecs.register(content_type=PillowCodec.ContentType, codec=PillowCodec())

class EchoRuntime(MLModel):
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        outputs = []
        for request_input in payload.inputs:
            decoded_input = self.decode(request_input)
            print(f"------ Encoded Input ({request_input.name}) ------")
            print(json.dumps(request_input.dict(), indent=2))
            print(f"------ Decoded input ({request_input.name}) ------")
            print(decoded_input)
            
            outputs.append(
                ResponseOutput(
                    name=request_input.name,
                    datatype=request_input.datatype,
                    shape=request_input.shape,
                    data=request_input.data
                )
            )
        
        return InferenceResponse(model_name=self.name, outputs=outputs)
        
