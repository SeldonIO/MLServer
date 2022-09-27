from functools import wraps
import uuid
import tritonclient.http.aio as httpclient

import asyncio
import aiofiles
import logging
import click
import json
import orjson

from typing import Dict, List, Tuple

import numpy as np

from mlserver.types import InferenceRequest
from mlserver.codecs import NumpyCodec
from mlserver.logging import get_logger

from time import perf_counter as timer


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


def setup_logging(debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)


def json_to_triton(
    request_json: str, binary_data: bool
) -> Tuple[str, List[httpclient.InferInput], List[httpclient.InferRequestedOutput]]:
    inputs = []
    inference_request = InferenceRequest.parse_obj(orjson.loads(request_json))
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

    return inference_request.id, inputs, outputs


def serialize_triton_infer_result(triton_output: httpclient.InferResult):
    response = triton_output.get_response()
    for (n, output) in enumerate(response["outputs"]):
        data = triton_output.as_numpy(output["name"])
        response["outputs"][n]["data"] = data.flatten().tolist()

        # Removing "binary_data_size" parameters as now this is 1-D list
        if (
            output["parameters"] is not None
            and "binary_data_size" in output["parameters"]
        ):
            del response["outputs"][n]["parameters"]["binary_data_size"]

    return orjson.dumps(response)


async def produce(queue: asyncio.Queue, fname: str):
    async with aiofiles.open(fname, "rb") as f:
        async for line in f:
            await queue.put(line)


async def finalize(queue: asyncio.Queue, fname: str):
    # TODO: Test if output directory is writtable, sysexit otherwise.
    async with aiofiles.open(fname, "wb") as f:
        while True:
            item = await queue.get()
            try:
                output = serialize_triton_infer_result(item)
                await f.write(output)
                await f.write(b"\n")
            except Exception as e:
                logger.error(f"Failed to finalize task: {e}")
            queue.task_done()


def get_headers(request_id: str) -> Dict[str, str]:
    headers = {"content-type": "application/json"}
    if request_id:
        headers["seldon-puid"] = request_id
        headers["x-request-id"] = request_id
    return headers


async def consume(
    model_name: str,
    worker_id: int,
    triton_client: httpclient.InferenceServerClient,
    queue_in: asyncio.Queue,
    queue_out: asyncio.Queue,
    binary_data: bool,
):
    while True:
        item = await queue_in.get()
        try:
            request_id, inputs, outputs = json_to_triton(
                item, binary_data
            )
            if request_id is None or request_id == "":
                request_id = str(uuid.uuid4())
        except Exception as e:
            logger.error(f"Failed to deserialize item: {item}")
            queue_in.task_done()
            continue
        try:
            logger.debug(f"consumer {worker_id}: sending request")
            data = await triton_client.infer(
                model_name,
                inputs,
                outputs=outputs,
                request_id=request_id,
                headers=get_headers(request_id),
            )
            logger.debug(f"consumer {worker_id}: received response")
            await queue_out.put(data)
        except Exception as e:
            logger.error(f"Consumer {worker_id}: Failed to process task: {e}")
        queue_in.task_done()


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
                queue_in,
                queue_out,
                binary_data,
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
