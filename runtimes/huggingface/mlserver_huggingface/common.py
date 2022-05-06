import asyncio
import contextvars
import functools
from asyncio import AbstractEventLoop
from importlib import import_module
from typing import Optional, Callable, Awaitable

from pydantic import BaseSettings

HUGGINGFACE_TASK_TAG = "task"

ENV_PREFIX_HUGGINGFACE_SETTINGS = "MLSERVER_MODEL_HUGGINGFACE_"
HUGGINGFACE_PARAMETERS_TAG = "huggingface_parameters"


# TODO: this is very similar to `asyncio.to_thread` (python 3.9+),
# so lets use it at some point.
def execute_async(
    loop: Optional[AbstractEventLoop], fn: Callable, *args, **kwargs
) -> Awaitable:
    if loop is None:
        loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, fn, *args, **kwargs)
    return loop.run_in_executor(None, func_call)


class HuggingFaceSettings(BaseSettings):
    """
    Parameters that apply only to alibi huggingface models
    """

    class Config:
        env_prefix = ENV_PREFIX_HUGGINGFACE_SETTINGS

    task: str = ""
    pretrained_model: Optional[str] = None
    pretrained_tokenizer: Optional[str] = None


def import_and_get_class(class_path: str) -> type:
    last_dot = class_path.rfind(".")
    klass = getattr(import_module(class_path[:last_dot]), class_path[last_dot + 1 :])
    return klass
