from dataclasses import dataclass
from functools import wraps
import tritonclient.http.aio as httpclient

import asyncio
import aiofiles
import logging
import click
import json
import orjson

from typing import Dict, List, Tuple

from mlserver.types import InferenceRequest, InferenceResponse, Parameters
from mlserver.codecs import NumpyCodec
from mlserver.logging import get_logger

from time import perf_counter as timer

from mlserver.utils import generate_uuid


CHOICES_TRANSPORT = ["rest", "grpc"]

logger = get_logger()


# Monkey patching is required for error responses coming from MLServer.
async def _get_error(response):
    """
    Returns the InferenceServerException object if response
    indicates the error. If no error then return None
    """
    if response.status != 200:
        result = await response.read()
        error_response = json.loads(result) if len(result) else {"error": ""}
        try:
            return httpclient.InferenceServerException(msg=error_response["error"])
        except KeyError:
            return httpclient.InferenceServerException(
                msg=json.dumps(error_response["detail"])
            )
    else:
        return None


httpclient._get_error = _get_error
del _get_error


def click_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@dataclass
class BatchInputItem:
    index: int
    item: bytes


@dataclass
class BatchOutputItem:
    index: int
    item: bytes


def setup_logging(debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)


def get_headers(request_id: str) -> Dict[str, str]:
    headers = {"content-type": "application/json"}
    if request_id:
        headers["seldon-puid"] = request_id
        headers["x-request-id"] = request_id
    return headers


@dataclass
class TritonRequest:
    id: str
    inputs: List[httpclient.InferInput]
    outputs: List[httpclient.InferRequestedOutput] = None

    @classmethod
    def from_inference_request(
        cls, inference_request: InferenceRequest, binary_data: bool
    ) -> Tuple[str, List[httpclient.InferInput], List[httpclient.InferRequestedOutput]]:
        inputs = []

        for request_input in inference_request.inputs or []:
            new_input = httpclient.InferInput(
                request_input.name, request_input.shape, request_input.datatype
            )
            new_input.set_data_from_numpy(
                NumpyCodec.decode_input(request_input),
                binary_data=binary_data,
            )
            inputs.append(new_input)

        outputs = []
        for request_output in inference_request.outputs or []:
            new_output = httpclient.InferRequestedOutput(
                request_output.name, binary_data=binary_data
            )
            outputs.append(new_output)

        return TritonRequest(inference_request.id, inputs, outputs)


def infer_result_to_infer_response(item: httpclient.InferResult) -> InferenceResponse:
    response = item.get_response()

    outputs = []
    for output_item in response["outputs"]:
        output_name = output_item["name"]
        output = NumpyCodec.encode_output(output_name, item.as_numpy(output_name))
        output_parameters = output_item["parameters"]
        if output_parameters is not None:
            # Create copy in case this code will ever be used in another context as
            # we are modifying the original parameters by removing unwanted key
            output_parameters = output_parameters.copy()
            if "binary_data_size" in output_parameters:
                del output_parameters["binary_data_size"]
            output.parameters = Parameters(**output_parameters)
        outputs.append(output)

    inference_response = InferenceResponse(
        model_name=response["model_name"],
        model_version=response.get("model_version", None),
        id=response.get("id", None),
        parameters=response.get("parameters", Parameters()),
        outputs=outputs,
    )

    return inference_response


def preprocess_item(item: BatchInputItem, binary_data: bool) -> TritonRequest:
    inference_request = InferenceRequest.parse_obj(orjson.loads(item.item))
    if inference_request.id is None:
        inference_request.id = generate_uuid()
    return TritonRequest.from_inference_request(inference_request, binary_data)


def postprocess_item(
    infer_result: httpclient.InferResult, index: int
) -> BatchOutputItem:
    inference_response = infer_result_to_infer_response(infer_result)
    inference_response.parameters.batch_index = index
    return BatchOutputItem(index=index, item=inference_response.json().encode())


async def process_item(
    item: BatchInputItem,
    model_name: str,
    worker_id: int,
    triton_client: httpclient.InferenceServerClient,
    binary_data: bool,
) -> BatchOutputItem:
    try:
        triton_request = preprocess_item(item, binary_data)
    except Exception as e:
        logger.error(f"consumer {worker_id}: failed to preprocess item: {repr(e)}")
        raise

    try:
        logger.debug(f"consumer {worker_id}: sending request")
        infer_result = await triton_client.infer(
            model_name,
            triton_request.inputs,
            outputs=triton_request.outputs,
            request_id=triton_request.id,
            headers=get_headers(triton_request.id),
        )
        logger.debug(f"consumer {worker_id}: received response")
    except Exception as e:
        logger.error(f"consumer {worker_id}: failed to process task: {repr(e)}")
        raise

    try:
        output_item = postprocess_item(infer_result, item.index)
    except Exception as e:
        logger.error(f"consumer {worker_id}: failed to postprocess item: {repr(e)}")

    return output_item


async def produce(queue: asyncio.Queue, fname: str):
    async with aiofiles.open(fname, "rb") as f:
        index = 0
        async for line in f:
            await queue.put(BatchInputItem(index=index, item=line))
            index += 1


async def consume(
    model_name: str,
    worker_id: int,
    triton_client: httpclient.InferenceServerClient,
    binary_data: bool,
    extra_verbose: bool,
    queue_in: asyncio.Queue,
    queue_out: asyncio.Queue,
):
    while True:
        input_item = await queue_in.get()
        try:
            output_item = await process_item(
                input_item, model_name, worker_id, triton_client, binary_data
            )
        except Exception:
            if extra_verbose:
                logger.error(
                    f"consumer {worker_id}: failed to process item {input_item}"
                )
            queue_in.task_done()
            continue

        await queue_out.put(output_item)
        queue_in.task_done()


async def finalize(queue: asyncio.Queue, fname: str):
    # TODO: Test if output directory is writtable, sysexit otherwise.
    async with aiofiles.open(fname, "wb") as f:
        while True:
            batch_output = await queue.get()
            try:
                await f.write(batch_output.item)
                await f.write(b"\n")
            except Exception as e:
                logger.error(f"Failed to finalize task: {repr(e)}")
            queue.task_done()


async def process_batch(
    model_name,
    url,
    workers,
    input_data_path,
    output_data_path,
    binary_data,
    transport,
    use_ssl,
    insecure,
    verbose,
    extra_verbose,
):
    """
    Process batch requests against V2-compatible inference server.

    Currently, this is meant to be an entrypoint for the `mlserver infer ...` CLI.
    Note: this feature is currently experimental and API is subject to change.
    """
    start_time = timer()

    if transport == "grpc":
        raise click.BadParameter("The 'grpc' transport is not yet supported.")

    if extra_verbose:
        verbose = True
        logger.info("Running in extra verbose mode.")
    elif verbose:
        logger.info("Running in verbose mode.")

    setup_logging(debug=verbose)
    logger.info(f"Server url: {url}")
    logger.info(f"input file path: {input_data_path}")
    logger.info(f"output file path: {output_data_path}")

    if insecure:
        ssl_context = False
    else:
        ssl_context = None

    triton_client = httpclient.InferenceServerClient(
        url=url,
        verbose=extra_verbose,
        conn_limit=workers,
        ssl=use_ssl,
        ssl_context=ssl_context,
    )

    queue_in = asyncio.Queue(2 * workers)
    queue_out = asyncio.Queue(2 * workers)

    consumers = []
    for worker_id in range(workers):
        consumer = asyncio.create_task(
            consume(
                model_name,
                worker_id,
                triton_client,
                binary_data,
                extra_verbose,
                queue_in,
                queue_out,
            )
        )
        consumers.append(consumer)

    finalizer = asyncio.create_task(finalize(queue_out, output_data_path))

    await produce(queue_in, input_data_path)
    await queue_in.join()
    await queue_out.join()

    for consumer in consumers:
        consumer.cancel()

    finalizer.cancel()

    await asyncio.gather(*consumers, finalizer, return_exceptions=True)

    await triton_client.close()

    logger.info(f"Time taken: {(timer()-start_time):.2f} seconds")
