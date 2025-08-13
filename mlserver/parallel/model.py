from typing import Any, Callable, Optional, AsyncIterator
from enum import Enum
from functools import wraps

from ..errors import InferenceError
from ..handlers.custom import get_custom_handlers, register_custom_handler
from ..model import MLModel
from ..types import MetadataModelResponse, InferenceRequest, InferenceResponse

from .messages import ModelRequestMessage
from .dispatcher import Dispatcher
import inspect

class ModelMethods(Enum):
    Predict = "predict"
    Metadata = "metadata"
    PredictStream = "predict_stream"  # <-- ADD THIS


def _returns_async_iterator(fn: Callable) -> bool:
    """
    Detect if `fn` is annotated to return an AsyncIterator[...].
    """
    ann = getattr(fn, "__annotations__", {})
    ret = ann.get("return")
    if ret is None:
        return False
    try:
        from typing import get_origin, AsyncIterator as TAsyncIterator
        from collections.abc import AsyncIterator as CAsyncIterator
        origin = get_origin(ret)
    except Exception:
        origin = None
        TAsyncIterator = AsyncIterator  # type: ignore
        from collections.abc import AsyncIterator as CAsyncIterator  # type: ignore
    return ret in (TAsyncIterator, CAsyncIterator) or origin in (TAsyncIterator, CAsyncIterator)


class ParallelModel(MLModel):
    def __init__(self, model: MLModel, dispatcher: Dispatcher):
        super().__init__(model.settings)
        self._model = model
        self._dispatcher = dispatcher
        self._metadata: Optional[MetadataModelResponse] = None
        self._add_custom_handlers()

    def _add_custom_handlers(self):
        custom_handlers = get_custom_handlers(self._model)
        for handler, method in custom_handlers:
            parallelised = self._parallelise(method)
            register_custom_handler(handler, parallelised)
            setattr(self, method.__name__, parallelised)

    def _parallelise(self, method: Callable):
        """
        Wrap a model method so calls are dispatched to the worker pool.
        Returns either:
          - an async *coroutine* (unary), or
          - an async *generator* (streaming).
        """
        if _returns_async_iterator(method):
            @wraps(method)
            async def _inner_streaming(*args, **kwargs):
                async for chunk in self._send_stream(method.__name__, *args, **kwargs):
                    yield chunk
            return _inner_streaming

        @wraps(method)
        async def _inner_unary(*args, **kwargs):
            return await self._send(method.__name__, *args, **kwargs)

        return _inner_unary

    async def metadata(self) -> MetadataModelResponse:
        # Cache metadata to avoid expensive worker calls for static data
        if self._metadata is None:
            metadata_response = await self._send(ModelMethods.Metadata.value)
            if not isinstance(metadata_response, MetadataModelResponse):
                raise InferenceError(f"Model '{self.name}' returned no metadata")
            self._metadata = metadata_response
        return self._metadata

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        inference_response = await self._send(ModelMethods.Predict.value, payload)
        if not isinstance(inference_response, InferenceResponse):
            raise InferenceError(
                f"Model '{self.name}' returned no predictions after inference"
            )
        return inference_response

    # NEW: streaming predict
    async def predict_stream(
        self, payloads: AsyncIterator[InferenceRequest]
    ) -> AsyncIterator[InferenceResponse]:
        """
        Stream-friendly predict. Forwards an AsyncIterator[InferenceRequest] to the
        worker and yields InferenceResponse chunks as they arrive.
        """
        async for chunk in self._send_stream(ModelMethods.PredictStream.value, payloads):
            yield chunk

    async def _send(self, method_name: str, *args, **kwargs) -> Optional[Any]:
        req_message = ModelRequestMessage(
            model_name=self.name,
            model_version=self.version,
            method_name=method_name,
            method_args=list(args),
            method_kwargs=kwargs,
        )
        response_message = await self._dispatcher.dispatch_request(req_message)
        return response_message.return_value

    async def _send_stream(
        self, method_name: str, *args, **kwargs
    ) -> AsyncIterator[Any]:
        """
        Dispatch a request expected to produce a stream of chunks. Yields chunks
        as they arrive from the worker.
        """
        req_message = ModelRequestMessage(
            model_name=self.name,
            model_version=self.version,
            method_name=method_name,
            method_args=list(args),
            method_kwargs=kwargs,
        )

        # Get the stream iterator from the dispatcher; it may be a coroutine that
        # resolves to an async-iterator, or an async-iterator directly.
        stream_iter = await self._dispatcher.dispatch_request_stream(req_message)
        try:
            async for chunk in stream_iter:
                yield chunk
        finally:
            aclose = getattr(stream_iter, "aclose", None)
            if callable(aclose):
                await aclose()
